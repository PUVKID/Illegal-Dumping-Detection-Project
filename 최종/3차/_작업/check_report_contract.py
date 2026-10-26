"""Synthetic report-format check; never evaluates or writes the real test split."""
import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,'/root/환경 PBL/trash_round3/app')
import make_report
root=Path('/tmp/round3_report_contract');root.mkdir(exist_ok=True)
(root/'runs').mkdir(exist_ok=True)
for name in ('test_final','val_contract_full'):(root/'evaluation'/name).mkdir(parents=True,exist_ok=True)
op={'threshold':.2,'precision':.5,'recall':.5,'f1':.5,'tp':1,'fp':1,'fn':1,'iou':.5}
selected={'candidate':'contract','policy':'full','weights':['contract.pt'],'operating':op,'metrics':{'metrics/mAP50(B)':.5,'metrics/mAP50-95(B)':.5}}
final={'test':selected,'selected':selected,'target_met':False,'history':[],
       'data':{'original_train':1200,'salsa_train':1243,'additional_taco':1,'additional_street':1,'zoom_images':1},
       'best_sha256':{'contract.pt':'synthetic-only'}}
(root/'final.json').write_text(json.dumps(final));(root/'validation_comparison.json').write_text(json.dumps([selected]))
(root/'evaluation/val_contract_full/operating_thresholds.json').write_text(json.dumps([op]))
np.savez(root/'evaluation/test_final/stats.npz',tp=np.array([[True]*10,[False]*10]),conf=np.array([.9,.8]),pred_cls=np.zeros(2),target_cls=np.zeros(2),target_img=np.zeros(1))
make_report.ROOT=root;make_report.OUT=root/'report';make_report.main()
assert (root/'report/3차_최종보고서.html').is_file()
assert len(list((root/'report').glob('*.png')))==5
print('Synthetic report contract passed; no real test data used.')
