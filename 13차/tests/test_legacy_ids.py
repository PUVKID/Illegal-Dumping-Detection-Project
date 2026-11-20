"""이전 파일명과 공식 ID 대응의 잘못된 확장을 잡습니다."""
import copy
import unittest
import legacy_ids

def sample():
    image={'id':47668,'file_name':'Site_GH01_1.jpg','path':'/datasets/Site/GH01_1.jpg','width':1920,'height':1080}
    annotation={'images':[image],'annotations':[],'categories':[]}
    row={'source':'pLitterStreet','image':'/legacy/plitter_47668.jpg','url':legacy_ids.STREET_URL,'sha256':'a'*64}
    return [row],annotation

class LegacyIdsTests(unittest.TestCase):
    def test_real_legacy_basename_resolves_47668(self):
        match=legacy_ids.legacy_match('/root/환경 PBL/trash_round3/data/additional/images/train/plitter_47668.jpg')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1),'47668')

    def test_other_parent_numbers_cannot_become_image_identity(self):
        self.assertIsNone(legacy_ids.legacy_match('/street_999/other.jpg'))

    def test_complete_basename_rejects_partial_suffix_and_invalid_types(self):
        for value in ('other_47668.jpg','plitter_47668.jpg.bak','plitter_47668.png','plitter_0.jpg','plitter_047668.jpg','plitter_47668.jpg?x=1',None,123):
            with self.subTest(value=value):self.assertIsNone(legacy_ids.legacy_match(value))

    def test_windows_separator_and_preserved_street_prefix(self):
        self.assertEqual(legacy_ids.legacy_match('C:\\data\\street_12.jpg').group(1),'12')

    def test_official_metadata_map_has_independent_literal_counts(self):
        rows,annotation=sample()
        function=getattr(legacy_ids,'provenance_map',lambda *args:None)
        result=function(rows,annotation,copy.deepcopy(annotation),('47668',))
        self.assertEqual(result.get('counts') if result else None,{'prior':1,'previous_round5':1,'overlap':1,'union':1})
        self.assertEqual(result['rows'][0]['legacy_encoded_sha256'],'a'*64)
        self.assertEqual(result['rows'][0]['official_file_name'],'Site_GH01_1.jpg')

    def test_unknown_official_id_is_rejected(self):
        rows,annotation=sample();rows[0]['image']='/legacy/plitter_99.jpg'
        with self.assertRaises(ValueError):legacy_ids.provenance_map(rows,annotation,annotation)

    def test_duplicate_official_or_legacy_id_is_rejected(self):
        rows,annotation=sample()
        with self.assertRaises(ValueError):legacy_ids.provenance_map(rows+rows,annotation,annotation)
        annotation['images']*=2
        with self.assertRaises(ValueError):legacy_ids.provenance_map(rows,annotation,annotation)

    def test_changed_original_annotation_is_rejected(self):
        rows,annotation=sample();changed=copy.deepcopy(annotation);changed['images'][0]['width']=1
        with self.assertRaises(ValueError):legacy_ids.provenance_map(rows,annotation,changed)

    def test_wrong_source_or_non_hash_is_rejected(self):
        for key,value in (('url','https://example.invalid/other.zip'),('sha256','bad')):
            rows,annotation=sample();rows[0][key]=value
            with self.assertRaises(ValueError):legacy_ids.provenance_map(rows,annotation,annotation)

    def test_prior_round_id_without_official_counterpart_is_rejected(self):
        rows,annotation=sample()
        with self.assertRaises(ValueError):legacy_ids.provenance_map(rows,annotation,annotation,('999',))
