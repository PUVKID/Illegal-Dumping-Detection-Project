import sys,json,gc
from pathlib import Path
sys.path.insert(0,'/root/환경 PBL/trash_round3/app')
import torch
from ultralytics import YOLO
from data_pipeline import ROOT,save,verify_holdout
from ultralytics.models.yolo.detect import DetectionValidator

v=DetectionValidator(save_dir=Path('/tmp/round3_metric_check'))
pred={'bboxes':torch.tensor([[0.,0,10,10],[30.,30,40,40]]),'cls':torch.zeros(2),'conf':torch.tensor([.9,.8])}
gt={'bboxes':torch.tensor([[0.,0,10,10]]),'cls':torch.zeros(1)}
tp=v._process_batch(pred,gt)['tp'];assert tp[0].all() and not tp[1].any()
verify_holdout()
records=[]
def collect(x):
    if torch.is_tensor(x) and x.requires_grad:return [x.float().square().mean()]
    if isinstance(x,dict):return [z for v in x.values() for z in collect(v)]
    if isinstance(x,(list,tuple)):return [z for v in x for z in collect(v)]
    return []
for arch,weight in [('yolo26x.pt','yolo26x.pt'),('yolo26l-p2.yaml','yolo26l.pt')]:
    p=ROOT/'pretrained'/weight
    if not p.exists():YOLO(str(p))
    model=YOLO(str(p)) if arch.endswith('.pt') else YOLO(arch).load(str(p))
    model.model.requires_grad_(True).cuda().train();torch.cuda.reset_peak_memory_stats()
    image=torch.rand(2,3,1536,1536,device='cuda')
    with torch.autocast('cuda'):
        output=model.model(image);loss=sum(collect(output))
    loss.backward();torch.cuda.synchronize()
    record={'architecture':arch,'batch':2,'imgsz':1536,'forward_backward':'passed','peak_GB':torch.cuda.max_memory_allocated()/1e9}
    records.append(record);print(record,flush=True)
    del model,image,output,loss;gc.collect();torch.cuda.empty_cache()
save(ROOT/'model_memory_smoke.json',{'models':records,'metric_match_test':'passed','heldout_hashes':'passed','note':'Random inputs, no optimizer update, no accuracy evaluation'})
