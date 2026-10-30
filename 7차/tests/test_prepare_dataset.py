"""원본 보존·예산·분할 누출·좌표 변환의 실패 경로를 검사합니다."""
import hashlib
import collections
import importlib.util
import io
import http.server
import json
import os
import errno
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import zipfile
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from PIL import Image, ImageDraw

if importlib.util.find_spec('prepare_dataset'):
    import prepare_dataset as data
else:
    data = None


@contextmanager
def range_server(content, behavior=lambda attempt: {}):
    """실제 작은 HTTP 응답으로 중단·서버 오류·범위 위반을 재현합니다."""
    calls=[]
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            start,end=map(int,self.headers['Range'].removeprefix('bytes=').split('-'))
            calls.append((start,end))
            reply=behavior(len(calls))
            status=reply.get('status',206)
            self.send_response(status)
            if status==206:
                self.send_header('Content-Range',reply.get('range',f'bytes {start}-{end}/{len(content)}'))
            if 'retry_after' in reply:self.send_header('Retry-After',reply['retry_after'])
            self.send_header('Content-Length',str(end-start+1 if status==206 else 0))
            self.end_headers()
            if status==206:
                self.wfile.write(reply.get('body',content[start:end+1]))
                self.wfile.flush()
            if reply.get('stall'):threading.Event().wait(reply['stall'])
            self.close_connection=True
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=lambda:server.serve_forever(poll_interval=.01),daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/file',calls
    finally:
        server.shutdown();server.server_close();thread.join()


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(data, '자료 준비 구현이 필요합니다.')
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        if hasattr(self, 'temp'):
            self.temp.cleanup()

    def jpeg(self, name='source.jpg', orientation=1):
        path = self.root / name
        image = Image.new('RGB', (120, 80), (120, 30, 5))
        ImageDraw.Draw(image).rectangle((60,0,119,79),fill=(5,30,180))
        exif = Image.Exif()
        exif[274] = orientation
        image.save(path, exif=exif)
        return path

    def test_jpeg_rotation_metadata_removed_without_pixel_rotation(self):
        for orientation in (1, 3, 6, 8):
            with self.subTest(orientation=orientation):
                source = self.jpeg(str(orientation)+'.jpg', orientation)
                before = source.read_bytes()
                target = self.root / ('normalized'+str(orientation)+'.jpg')
                result = data.normalize_image(source, target, expected_size=(120, 80), reserve=lambda n: None)
                self.assertEqual(source.read_bytes(), before)
                self.assertEqual((result['width'], result['height']), (120, 80))
                self.assertTrue(target.read_bytes().endswith(b'\xff\xd9'))
                with Image.open(target) as image:
                    self.assertNotIn(274, image.getexif())
                    with Image.open(source) as original:
                        self.assertLess(sum(abs(a-b) for a,b in zip(image.getpixel((20,40)),original.getpixel((20,40)))),12)
                self.assertEqual(result['raw_sha256'], hashlib.sha256(before).hexdigest())

    def test_normalization_refuses_source_overwrite_and_wrong_coordinates(self):
        source = self.jpeg()
        with self.assertRaises(ValueError):
            data.normalize_image(source, source, expected_size=(120, 80), reserve=lambda n: None)
        with self.assertRaises(ValueError):
            data.normalize_image(source, self.root/'out.jpg', expected_size=(80, 120), reserve=lambda n: None)

    def test_yolo_rounding_tolerance_does_not_accept_real_outside_box(self):
        self.assertEqual(len(data.validate_yolo('0 .5 .5 1.0000001 1')), 1)
        for text in ('0 .5 .5 1.001 1', '1 .5 .5 .1 .1', '0 nan .5 .1 .1', '0 .5 .5 0 .1'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                data.validate_yolo(text)

    def test_coco_mapping_excludes_bins_and_rejects_unknown_classes(self):
        image = {'width': 100, 'height': 100}
        rows = data.coco_labels(image, [{'category_id': 4, 'bbox': [0,0,90,90]},
                                       {'category_id': 1, 'bbox': [10,20,20,40]}], {1:0, 4:None})
        self.assertEqual(rows, [[0, .2, .4, .2, .4]])
        with self.assertRaises(ValueError):
            data.coco_labels(image, [{'category_id': 7, 'bbox': [1,2,3,4]}], {1:0})
        with self.assertRaises(ValueError):
            data.coco_labels(image, [{'category_id': 1, 'bbox': [-3,2,30,4]}], {1:0})

    def test_duplicate_components_are_transitive_and_order_independent(self):
        records = [{'id':'a','group':'a','sha256':'a','signature':'0000000000000000'},
                   {'id':'b','group':'b','sha256':'b','signature':'000000000000000f'},
                   {'id':'c','group':'c','sha256':'c','signature':'00000000000000ff'},
                   {'id':'z','group':'z','sha256':'z','signature':'ffffffffffffffff'}]
        expected = {'a':'a', 'b':'a', 'c':'a', 'z':'z'}
        self.assertEqual(data.components(records), expected)
        self.assertEqual(data.components(list(reversed(records))), expected)

    def test_group_identity_connects_frames_even_when_pixels_differ(self):
        rows = [{'id':'a','group':'capture','sha256':'a','signature':'0000000000000000'},
                {'id':'b','group':'capture','sha256':'b','signature':'ffffffffffffffff'}]
        self.assertEqual(data.components(rows), {'a':'a', 'b':'a'})

    def test_unseen_test_source_cannot_touch_previous_used_images(self):
        old = {'id':'old','group':'old','sha256':'same','signature':'0000000000000000','source':'TACO','split':'historical_val'}
        new = {'id':'new','group':'new','sha256':'same','signature':'0000000000000000','source':'UAVVaste','split':'external_test'}
        kept, rejected = data.protect_splits([old,new])
        self.assertEqual([r['id'] for r in kept], ['old'])
        self.assertEqual(rejected[0]['id'], 'new')

    def test_historical_original_not_in_round5_still_protects_new_source(self):
        archive=self.root/'archive'
        directory=archive/'data/full/images/train';directory.mkdir(parents=True)
        raw=self.jpeg();(directory/'old.jpg').write_bytes(raw.read_bytes())
        digest=hashlib.sha256(raw.read_bytes()).hexdigest()
        with patch.object(data,'ARCHIVE',archive):
            ghosts=data.historical_protection([], [{'raw_sha256':digest,'source':'UAVVaste'}])
        self.assertEqual(len(ghosts),1)
        self.assertTrue(ghosts[0]['available'])
        self.assertEqual(ghosts[0]['sha256'],digest)

    def test_historical_missing_photo_keeps_original_hash_and_url(self):
        missing={'source':'TACO unofficial','image':str(self.root/'missing.jpg'),'sha256':'originalhash','url':'https://example.invalid/photo'}
        with patch.object(data,'ARCHIVE',self.root/'archive'):
            ghosts=data.historical_protection([missing],[])
        self.assertEqual(ghosts[0]['sha256'],'originalhash')
        self.assertEqual(ghosts[0]['original_url'],'https://example.invalid/photo')
        self.assertFalse(ghosts[0]['available'])

    def test_connected_new_validation_group_moves_whole_group_out_of_train(self):
        rows = [{'id':'a','group':'a','sha256':'a','signature':'0000000000000000','source':'PlastOPol','split':'train'},
                {'id':'b','group':'b','sha256':'b','signature':'000000000000000f','source':'PlastOPol','split':'val'}]
        kept, _ = data.protect_splits(rows)
        self.assertEqual({r['split'] for r in kept}, {'val'})

    def test_identical_training_bytes_are_counted_once(self):
        rows=[{'id':'a','group':'a','sha256':'same','signature':'0000000000000000','source':'PlastOPol','split':'train'},
              {'id':'b','group':'b','sha256':'same','signature':'0000000000000000','source':'PlastOPol','split':'train'}]
        kept,rejected=data.protect_splits(rows)
        self.assertEqual([r['id'] for r in kept],['a'])
        self.assertEqual(len(rejected),1)

    def test_crop_preserves_split_parent_and_rejects_heldout_augmentation(self):
        parent = {'id':'parent','split':'train','width':100,'height':100}
        labels = [[0,.5,.5,.2,.2], [0,.99,.99,.02,.02]]
        rows = data.crop_labels(parent, labels, (25,25,75,75))
        self.assertEqual(rows, [[0,.5,.5,.4,.4]])
        with self.assertRaises(ValueError):
            data.crop_labels({**parent,'split':'val'}, labels, (0,0,50,50))

    def test_partial_box_crop_is_rejected_rather_than_silently_unlabelled(self):
        parent = {'id':'p','split':'train','width':100,'height':100}
        self.assertIsNone(data.crop_labels(parent, [[0,.5,.5,.4,.4]], (0,0,40,100)))

    def test_empty_training_crop_is_not_created(self):
        parent = {'id':'p','split':'train','width':100,'height':100}
        self.assertEqual(data.crop_labels(parent, [[0,.9,.9,.1,.1]], (0,0,20,20)), [])

    def test_archive_path_traversal_and_link_are_rejected(self):
        archive = self.root/'bad.zip'
        with zipfile.ZipFile(archive,'w') as z:
            z.writestr('../escape.txt', '금지')
        with self.assertRaises(ValueError):
            data.extract_zip(archive, self.root/'out', reserve=lambda n:None)
        self.assertFalse((self.root/'escape.txt').exists())

    def test_zip_resume_verifies_existing_member_bytes(self):
        archive = self.root/'ok.zip'
        with zipfile.ZipFile(archive,'w') as z:
            z.writestr('a.txt','original')
        data.extract_zip(archive,self.root/'out',reserve=lambda n:None)
        (self.root/'out/a.txt').write_text('modified',encoding='utf-8')
        with self.assertRaises(ValueError):
            data.extract_zip(archive,self.root/'out',reserve=lambda n:None)

    @unittest.skipUnless(os.name=='posix','실제 Linux 파일 링크 경계를 검사합니다.')
    def test_existing_parent_symlink_cannot_redirect_zip_write(self):
        archive=self.root/'link.zip'
        with zipfile.ZipFile(archive,'w') as z:z.writestr('redirect/a.txt','external write')
        outside=self.root/'outside';outside.mkdir()
        target=self.root/'extract';target.mkdir()
        (target/'redirect').symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ValueError):data.extract_zip(archive,target,reserve=lambda n:None)
        self.assertFalse((outside/'a.txt').exists())

    def test_budget_persists_partial_transfers_and_refuses_overrun(self):
        budget = data.DownloadBudget(self.root, limit=10, minimum_free=0)
        budget.charge(7)
        again = data.DownloadBudget(self.root, limit=10, minimum_free=0)
        self.assertEqual(again.used, 7)
        with self.assertRaises(ValueError):
            again.charge(4)
        self.assertEqual(json.loads((self.root/'download_ledger.json').read_text())['download_bytes'],7)

    def test_disk_reservation_preserves_floor(self):
        budget = data.DownloadBudget(self.root, limit=100, minimum_free=100)
        usage=collections.namedtuple('usage','total used free')(1000,850,150)
        with patch('prepare_dataset.shutil.disk_usage', return_value=usage):
            budget.space(50)
            with self.assertRaises(ValueError):
                budget.space(51)

    def test_balancing_retains_all_originals_and_distinguishes_repetition(self):
        records = [{'id':str(i),'image':str(i),'source':'pLitterStreet','split':'train'} for i in range(8)]
        records += [{'id':'t','image':'t','source':'TACO','split':'train'}]
        paths = data.balanced_paths(records)
        self.assertTrue(set(map(str,range(8))) | {'t'} <= set(paths))
        self.assertGreater(paths.count('t'),1)

    def test_frozen_manifest_cannot_be_rebased_to_changed_values(self):
        path=self.root/'contract.json'
        data.freeze(path, {'sha':'old'})
        with self.assertRaises(ValueError):
            data.freeze(path, {'sha':'new'})
        self.assertEqual(json.loads(path.read_text()),{'sha':'old'})

    def test_prefetch_receipt_is_charged_exactly_once_and_cannot_change(self):
        receipt=self.root/'prefetch.json'
        receipt.write_text('{"download_bytes":7}',encoding='utf-8')
        budget=data.DownloadBudget(self.root/'budget',limit=20,minimum_free=0)
        budget.import_prefetch(receipt)
        budget.import_prefetch(receipt)
        self.assertEqual(budget.used,7)
        receipt.write_text('{"download_bytes":8}',encoding='utf-8')
        with self.assertRaises(ValueError):budget.import_prefetch(receipt)

    def test_prefetch_complete_receipt_accepts_status_progress_fields(self):
        work=self.root/'work';sources=work/'sources';prefetch=work/'prefetch'
        target=sources/'downloads/images.zip';target.parent.mkdir(parents=True);target.write_bytes(b'official')
        prefetch.mkdir(parents=True)
        spec={'url':'https://example.invalid/file','size':8,'md5':hashlib.md5(b'official').hexdigest()}
        receipt={'path':str(target),'url':spec['url'],'expected_bytes':8,'md5':spec['md5'],
                 'sha256':hashlib.sha256(b'official').hexdigest(),'download_bytes':8,'started':1.}
        data.atomic_json(prefetch/'complete.json',receipt)
        data.atomic_json(prefetch/'status.json',{**receipt,'state':'complete','stage':'완료','updated':2.})
        data.atomic_json(prefetch/'download_ledger.json',{'download_bytes':8})
        budget=data.DownloadBudget(sources,limit=100,minimum_free=0)
        with patch.object(data,'WORK',work),patch.object(data,'SOURCES',sources):
            data.download(spec,target,budget)
            data.download(spec,target,budget)
        self.assertEqual(budget.used,8)

    def test_http_partial_resume_charges_received_bytes_and_verifies_final_md5(self):
        content=b'official-bytes'
        calls=[]
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                start,end=map(int,self.headers['Range'].removeprefix('bytes=').split('-'))
                calls.append((start,end))
                self.send_response(206)
                self.send_header('Content-Range',f'bytes {start}-{end}/{len(content)}')
                self.send_header('Content-Length',str(end-start+1))
                self.end_headers()
                self.wfile.write(content[start:start+4] if len(calls)==1 else content[start:end+1])
                self.close_connection=True
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            spec={'url':f'http://127.0.0.1:{server.server_port}/file','size':len(content),'md5':hashlib.md5(content).hexdigest()}
            budget=data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0)
            target=self.root/'source.zip'
            with patch.object(data.time,'sleep'):
                data.download(spec,target,budget)
            self.assertEqual(target.read_bytes(),content)
            self.assertEqual(budget.used,len(content))
            self.assertEqual(calls,[(0,len(content)-1),(4,len(content)-1)])
        finally:
            server.shutdown();server.server_close();thread.join()

    def test_timeout_after_body_prefix_resumes_from_saved_disk_bytes(self):
        content=b'official-bytes'
        progress=[]
        with range_server(content,lambda attempt:{'body':content[:4],'stall':.15} if attempt==1 else {}) as (url,calls):
            spec={'url':url,'size':14,'md5':hashlib.md5(content).hexdigest()}
            budget=data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0,notify=lambda **value:progress.append(value))
            target=self.root/'timeout.zip'
            def short_request(url,headers=None):
                return urllib.request.urlopen(urllib.request.Request(url,headers=headers or {}),timeout=.05)
            with patch.object(data,'open_request',side_effect=short_request),patch.object(data.time,'sleep'):
                data.download(spec,target,budget)
            self.assertEqual(calls,[(0,13),(4,13)])
            self.assertEqual(target.read_bytes(),content)
            self.assertEqual(budget.used,14)
            self.assertEqual(data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0).used,14)
            retries=[value for value in progress if value.get('retry_wait_seconds',0)>0]
            self.assertEqual(len(retries),1)
            self.assertEqual(retries[0]['downloaded_bytes'],4)
            self.assertIn('TimeoutError',retries[0]['retry_reason'])
            self.assertIsNone(progress[-1]['retry_reason'])
            self.assertEqual(progress[-1]['retry_wait_seconds'],0)

    def test_http_429_and_503_retry_after_is_bounded_before_success(self):
        content=b'official-bytes'
        for status in (429,503):
            with self.subTest(status=status),range_server(content,lambda attempt:{'status':status,'retry_after':'120'} if attempt==1 else {}) as (url,calls):
                spec={'url':url,'size':14,'md5':hashlib.md5(content).hexdigest()}
                budget=data.DownloadBudget(self.root/str(status),limit=100,minimum_free=0)
                target=self.root/(str(status)+'.zip')
                with patch.object(data.time,'sleep') as sleep:
                    data.download(spec,target,budget)
                self.assertEqual(calls,[(0,13),(0,13)])
                self.assertEqual(target.read_bytes(),content)
                self.assertEqual(budget.used,14)
                self.assertEqual(sleep.call_args_list[0].args,(60,))

    def test_invalid_content_range_is_not_retried(self):
        content=b'official-bytes'
        with range_server(content,lambda attempt:{'range':'bytes 1-13/14'}) as (url,calls):
            spec={'url':url,'size':14,'md5':hashlib.md5(content).hexdigest()}
            budget=data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0)
            with patch.object(data.time,'sleep') as sleep,self.assertRaisesRegex(ValueError,'범위'):
                data.download(spec,self.root/'range.zip',budget)
            self.assertEqual(calls,[(0,13)])
            self.assertEqual(budget.used,0)
            sleep.assert_not_called()

    def test_budget_overrun_is_rejected_before_request_without_retry(self):
        content=b'official-bytes'
        with range_server(content) as (url,calls):
            spec={'url':url,'size':14,'md5':hashlib.md5(content).hexdigest()}
            budget=data.DownloadBudget(self.root/'budget',limit=12,minimum_free=0)
            with patch.object(data.time,'sleep') as sleep,self.assertRaisesRegex(ValueError,'예산'):
                data.download(spec,self.root/'budget.zip',budget)
            self.assertEqual(calls,[])
            self.assertEqual(budget.used,0)
            sleep.assert_not_called()

    def test_retry_exhaustion_preserves_prefix_and_charged_failed_transfer(self):
        content=b'official-bytes'
        progress=[]
        with range_server(content,lambda attempt:{'body':content[:4]} if attempt==1 else {'status':503}) as (url,calls):
            spec={'url':url,'size':14,'md5':hashlib.md5(content).hexdigest()}
            budget=data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0,notify=lambda **value:progress.append(value))
            target=self.root/'exhaust.zip'
            with patch.object(data.time,'sleep') as sleep,self.assertRaises(urllib.error.HTTPError):
                data.download(spec,target,budget)
            self.assertFalse(target.exists())
            self.assertEqual(target.with_suffix('.zip.part').read_bytes(),b'offi')
            self.assertEqual(budget.used,4)
            self.assertEqual(data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0).used,4)
            self.assertEqual(calls,[(0,13)]+[(4,13)]*6)
            self.assertEqual([call.args[0] for call in sleep.call_args_list],[2,4,8,16,32,60])
            self.assertEqual(len([value for value in progress if value.get('retry_wait_seconds',0)>0]),6)
            self.assertIn('한도 초과',progress[-1]['stage'])
            self.assertIn('HTTPError',progress[-1]['retry_reason'])

    def test_received_bytes_remain_charged_when_disk_write_check_fails(self):
        content=b'official-bytes'
        with range_server(content) as (url,calls):
            spec={'url':url,'size':14,'md5':hashlib.md5(content).hexdigest()}
            budget=data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0)
            with patch.object(budget,'space',side_effect=[None,None,OSError(errno.ENOSPC,'검사용 공간 부족')]),patch.object(data.time,'sleep') as sleep:
                with self.assertRaises(OSError):data.download(spec,self.root/'disk.zip',budget)
            self.assertEqual(calls,[(0,13)])
            self.assertEqual(budget.used,14)
            self.assertEqual(data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0).used,14)
            sleep.assert_not_called()

    def test_http_403_is_not_retried(self):
        content=b'official-bytes'
        with range_server(content,lambda attempt:{'status':403}) as (url,calls):
            spec={'url':url,'size':14,'md5':hashlib.md5(content).hexdigest()}
            budget=data.DownloadBudget(self.root/'budget',limit=100,minimum_free=0)
            with patch.object(data.time,'sleep') as sleep,self.assertRaises(urllib.error.HTTPError):
                data.download(spec,self.root/'denied.zip',budget)
            self.assertEqual(calls,[(0,13)])
            sleep.assert_not_called()

    def test_wrong_zip_crc_is_not_extracted_as_success(self):
        archive=self.root/'crc.zip'
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:z.writestr('a.txt',b'original')
        raw=bytearray(archive.read_bytes());raw[35]^=1;archive.write_bytes(raw)
        with self.assertRaises((ValueError,zipfile.BadZipFile)):
            data.extract_zip(archive,self.root/'crc',reserve=lambda n:None)
        self.assertFalse((self.root/'crc/a.txt').exists())


if __name__ == '__main__':
    unittest.main()
