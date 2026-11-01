"""운영 상태가 UI 문구와 현재 파일 진행률로 정확히 변환되는지 검사합니다."""
import unittest
import pipeline


class PresentationTests(unittest.TestCase):
    def value(self, **changes):
        training = {'job': 'real', 'state': 'running', 'stage': '공식 원자료 다운로드',
                    'downloaded_bytes': 50, 'file_bytes': 200}
        training.update(changes)
        return pipeline.presentation(training)

    def test_loaded_round8_uses_delete_sharing_reader(self):
        from safe_io import safe_read_json
        self.assertIs(pipeline.round8.read, safe_read_json)

    def test_download_only_file_progress(self):
        p = self.value()
        self.assertEqual(p['file_percent'], 25)
        self.assertEqual(p['step'], 0)
        self.assertEqual([s['status'] for s in p['steps']], ['active'] + ['pending'] * 4)
        self.assertEqual(p['gpu_state'], '대기 중')
        self.assertIsNone(p['epoch'])

    def test_unknown_progress_not_zero_or_global(self):
        self.assertIsNone(self.value(file_bytes=None)['file_percent'])
        self.assertIsNone(self.value(downloaded_bytes=None)['file_percent'])
        self.assertIsNone(self.value(file_bytes=0)['file_percent'])

    def test_empty_no_active_stage(self):
        p = pipeline.presentation({})
        self.assertIsNone(p['step'])
        self.assertEqual(p['badge'], '자료 없음')
        self.assertEqual(p['next'], '작업 대기 / 기록 없음')
        self.assertTrue(all(s['status'] == 'pending' for s in p['steps']))

    def test_preparation_and_integrity_are_not_gpu(self):
        for stage in ['공식 ZIP CRC 검사·원본 추출', '원본 대응 정규화·좌표 검증', '학습 전용 작은 객체 crop']:
            p = self.value(stage=stage)
            self.assertEqual(p['step'], 1)
            self.assertIsNone(p['epoch'])

    def test_md5_receive_is_download_stage(self):
        self.assertEqual(self.value(stage='공식 원자료 MD5 검사·재개 수신')['step'], 0)

    def test_next_guidance_follows_actual_phase(self):
        download = self.value()
        self.assertEqual(download['next'], '다운로드 검증 및 데이터 준비')
        training = self.value(stage='학습 small_l_p2')
        self.assertEqual(training['next'], '검증')
        self.assertIn('후보 학습이 끝나면', training['next_description'])
        self.assertNotIn('다운로드가 완료', training['next_description'])
        waiting = self.value(stage='다른 GPU 작업을 보존하며 여유 VRAM 확인')
        self.assertIn('여유 메모리', waiting['next_description'])
        failed = self.value(state='failed')
        self.assertEqual(failed['next'], '오류 기록 확인')
        self.assertNotIn('자동으로', failed['next_description'])

    def test_prior_completion_requires_specific_later_stage(self):
        p = self.value(stage='자료 준비와 학습 시작')
        self.assertEqual(p['steps'][0]['status'], 'pending')
        p = self.value(stage='학습 small_l_p2')
        self.assertEqual([s['status'] for s in p['steps']], ['complete','complete','active','pending','pending'])

    def test_gpu_and_validation_and_final(self):
        self.assertEqual(self.value(stage='학습 small_l_p2', epoch=2)['epoch'], 2)
        self.assertEqual(self.value(stage='고정 검증·평가 taco_val')['step'], 3)
        self.assertEqual(self.value(stage='고정 검증·평가 historical_taco')['step'], 4)

    def test_gpu_resource_wait_is_not_training(self):
        p = self.value(stage='다른 GPU 작업을 보존하며 여유 VRAM 확인', epoch=3)
        self.assertEqual(p['badge'], '자원 대기')
        self.assertEqual(p['gpu_state'], '대기 중')
        self.assertIsNone(p['epoch'])

    def test_retry_uses_record(self):
        p = self.value(retry_attempt=2, retry_reason='실제 타임아웃')
        self.assertTrue(p['retry'])
        self.assertEqual(p['badge'], '재시도')

    def test_failure_does_not_claim_retrying(self):
        p = self.value(state='failed', error='실제 오류', retry_attempt=6, retry_reason='실제 타임아웃')
        self.assertEqual(p['badge'], '실패')
        self.assertIn('작업 기록에서 오류를 확인', p['description'])
        self.assertNotIn('실제 오류', p['description'])

    def test_complete_all_steps_complete(self):
        p = self.value(state='complete')
        self.assertTrue(all(s['status'] == 'complete' for s in p['steps']))
        self.assertEqual(p['badge'], '완료')

    def test_stale_does_not_change_execution_state(self):
        self.assertEqual(self.value(stale=True)['badge'], '진행 중')


if __name__ == '__main__':
    unittest.main()
