"""검증 선택·예측 좌표·재개 계약·고정 테스트의 경계를 검사합니다."""
import importlib.util
import json
import tempfile
import unittest
import types
from pathlib import Path

if importlib.util.find_spec('train_pipeline'):
    import train_pipeline as train
else:
    train=None


class TrainingTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(train,'학습 파이프라인 구현이 필요합니다.')
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)

    def tearDown(self):
        if hasattr(self,'temp'):self.temp.cleanup()

    def test_joint_precision_recall_selection_preserves_baseline_on_tie(self):
        def row(name,p,r,ap=.5):
            return {'name':name,'operating':{'precision':p,'recall':r,'f1':2*p*r/(p+r)},'metrics':{'AP50':ap}}
        old=row('baseline',.6,.6)
        self.assertIs(train.choose_candidate([old,row('new',.99,.55)]),old)
        self.assertIs(train.choose_candidate([old,row('new',.6,.6)]),old)
        self.assertEqual(train.choose_candidate([old,row('new',.7,.7)])['name'],'new')

    def test_iou_matching_is_one_to_one_and_confidence_ordered(self):
        predictions=[[0,0,10,10,.2],[0,0,10,10,.8]]
        matches=train.match_predictions(predictions,[[0,0,10,10]],.5)
        self.assertEqual(matches,[False,True])

    def test_tiling_covers_image_without_unbounded_tiles(self):
        tiles=train.tile_boxes(5000,3000,3)
        self.assertEqual(len(tiles),9)
        self.assertEqual(min(x[0] for x in tiles),0)
        self.assertEqual(max(x[2] for x in tiles),5000)
        self.assertEqual(max(x[3] for x in tiles),3000)

    def test_shifted_tile_prediction_maps_back_to_original(self):
        self.assertEqual(train.shift_predictions([[1,2,8,9,.5]],(100,200,300,400)),[[101,202,108,209,.5]])

    def test_resume_requires_same_contract_and_explicit_permission(self):
        (self.root/'weights').mkdir()
        (self.root/'weights/last.pt').write_bytes(b'checkpoint')
        train.freeze(self.root/'run_contract.json',{'manifest':'old'})
        with self.assertRaises(ValueError):train.resume_decision(self.root,{'manifest':'new'},True)
        with self.assertRaises(ValueError):train.resume_decision(self.root,{'manifest':'old'},False)
        self.assertEqual(train.resume_decision(self.root,{'manifest':'old'},True),'resume')

    def test_completed_phase_requires_matching_weight_hash(self):
        train.freeze(self.root/'run_contract.json',{'a':1})
        (self.root/'weights').mkdir()
        (self.root/'weights/best.pt').write_bytes(b'original')
        train.atomic_json(self.root/'phase_complete.json',{'best_sha256':'bad'})
        with self.assertRaises(ValueError):train.resume_decision(self.root,{'a':1},True)

    def test_test_contract_refuses_threshold_changes_after_freeze(self):
        path=self.root/'test_contract.json'
        train.freeze(path,{'threshold':.1})
        with self.assertRaises(ValueError):train.freeze(path,{'threshold':.2})

    def test_threshold_selection_uses_validation_only(self):
        rows=[(.9,[True]*10),(.8,[False]*10),(.1,[True]*10)]
        result=train.summarize(rows,2)
        self.assertEqual(result['operating']['tp'],2)
        self.assertEqual(result['operating']['fp'],1)
        self.assertEqual(result['operating']['threshold'],.1)

    def test_size_breakdown_counts_missed_small_targets(self):
        result=train.image_counts([[0,0,100,100,.8]],[[0,0,10,10],[0,0,100,100]],.5)
        self.assertEqual(result['tp'],1)
        self.assertEqual(result['fn'],1)
        self.assertEqual(result['sizes']['small']['fn'],1)

    def test_test_target_uses_both_metrics_and_does_not_hide_failure(self):
        self.assertFalse(train.target_met({'operating':{'precision':.99,'recall':.89}}))
        self.assertTrue(train.target_met({'operating':{'precision':.9,'recall':.9}}))

    def test_time_budget_cannot_restart_at_six_hours_on_resume(self):
        self.assertEqual(train.remaining_seconds(18000,6),3600)
        with self.assertRaises(ValueError):train.remaining_seconds(21601,6)

    def test_epoch_cap_stops_even_if_ultralytics_time_changes_epochs(self):
        trainer=types.SimpleNamespace(epoch=59,epochs=1000,stop=False)
        train.enforce_epoch_cap(trainer,60)
        self.assertTrue(trainer.stop)
        trainer=types.SimpleNamespace(epoch=58,epochs=1000,stop=False)
        train.enforce_epoch_cap(trainer,60)
        self.assertFalse(trainer.stop)


if __name__=='__main__':unittest.main()
