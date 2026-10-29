"""기존 GPU 환경에서 탐지와 학습을 독립 프로세스로 실행합니다."""
import argparse
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import time
import traceback
import types
import uuid
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
WORK = ROOT / "work"
ARCHIVE = PROJECT / "이전 도커 실험/3차실험/trash_round3"
OLD_APP = PROJECT / "최종/3차/클린뷰"
VIDEO_ROOTS = [WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix("." + uuid.uuid4().hex + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def read(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def update(job, **kwargs):
    import fcntl
    path = WORK / "jobs" / f"{job}.json"
    with path.with_suffix(".lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        save(path, {**read(path, {}), **kwargs, "updated": time.time()})


def allowed_video(value):
    path = Path(value).resolve(strict=True)
    if not any(path.is_relative_to(p.resolve()) for p in VIDEO_ROOTS):
        raise ValueError("허용된 영상 폴더가 아닙니다.")
    if path.suffix.lower() not in {".mp4", ".avi", ".mov", ".mkv", ".m4v"} or not path.is_file() or not path.stat().st_size:
        raise ValueError("유효한 영상을 선택하세요.")
    return path


def probe(value):
    import cv2
    import hashlib
    path = allowed_video(value)
    cap = cv2.VideoCapture(str(path))
    try:
        ok, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if not ok or frame is None or not math.isfinite(fps) or fps <= 0:
            raise ValueError("영상을 읽을 수 없습니다. 파일과 코덱을 확인하세요.")
        out = WORK / "results" / ("preview_" + hashlib.sha256(str(path).encode()).hexdigest()[:20] + ".jpg")
        out.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(out), frame):
            raise RuntimeError("영상 미리보기를 저장하지 못했습니다.")
        return {"width": frame.shape[1], "height": frame.shape[0], "fps": fps,
                "frames": int(frames), "seconds": frames / fps, "bytes": path.stat().st_size, "preview": str(out)}
    finally:
        cap.release()


def ensure_selection():
    path = WORK / "selected_model.json"
    if path.exists():
        return read(path)
    final = read(ARCHIVE / "final.json")
    if not final:
        raise RuntimeError("보존된 final.json이 없습니다.")
    chosen = final["selected"]
    weights = [str(ARCHIVE / Path(p).relative_to("/root/환경 PBL/trash_round3")) for p in chosen["weights"]]
    if not all(Path(p).is_file() for p in weights):
        raise RuntimeError("보존된 학습 모델을 찾을 수 없습니다.")
    value = {"weights": weights[0], "ensemble": weights, "policy": chosen["policy"],
             "conf": chosen["operating"]["threshold"], "source": "3차 보존 모델", "test": final["test"]}
    save(path, value)
    return value


def is_alive(pid, identity):
    try:
        stat = Path(f"/proc/{int(pid)}/stat").read_text()
        command = Path(f"/proc/{int(pid)}/cmdline").read_bytes().split(b"\0")
        return (stat.split(") ", 1)[1].split()[0] != "Z"
                and str(Path(__file__).resolve()).encode() in command
                and identity.encode() in command)
    except (ValueError, FileNotFoundError, ProcessLookupError):
        return False


def reconcile():
    # 재부팅 뒤 같은 PID가 다른 프로세스에 재사용돼도 작업으로 오인하지 않습니다.
    import fcntl
    changed = 0
    jobs = WORK / "jobs"
    jobs.mkdir(parents=True, exist_ok=True)
    with (jobs / "start.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in jobs.glob("*.json"):
            job = read(path, {})
            if job.get("state") in {"queued", "running"} and not is_alive(job.get("pid", 0), job.get("id", "")):
                update(job["id"], state="interrupted", error="작업 프로세스가 종료됐습니다. 체크포인트 재개를 선택하세요.")
                changed += 1
    return {"reconciled": changed}


def start(kind, params):
    import fcntl
    jobs = WORK / "jobs"
    jobs.mkdir(parents=True, exist_ok=True)
    with (jobs / "start.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in jobs.glob("*.json"):
            job = read(path, {})
            if job.get("state") in {"queued", "running"}:
                if job.get("pid") and is_alive(job["pid"], job["id"]):
                    raise ValueError("GPU 작업이 이미 진행 중입니다. 완료 후 실행하세요.")
                update(job["id"], state="interrupted", error="Docker 또는 작업 프로세스가 종료됐습니다. 학습 재개를 선택하세요.")
        if kind == "detect":
            if set(params) - {"path", "seconds", "abandon", "leave", "baseline"}:
                raise ValueError("지원하지 않는 탐지 설정입니다.")
            allowed_video(params.get("path", ""))
            for key, low, high in [("seconds", 0, 86400), ("abandon", 1, 600), ("leave", 0, 120), ("baseline", 0, 60)]:
                number = float(params.get(key, {"seconds": 120, "abandon": 20, "leave": 5, "baseline": 10}[key]))
                if not math.isfinite(number) or not low <= number <= high:
                    raise ValueError("탐지 설정 범위를 확인하세요.")
                params[key] = number
        elif kind == "train":
            if not isinstance(params.get("resume", False), bool):
                raise ValueError("재개 설정은 true 또는 false여야 합니다.")
            if (WORK / "training/final.json").exists():
                raise ValueError("이 실험은 이미 완료됐습니다. 결과를 보존하며 자동 재학습하지 않습니다.")
            if not (ROOT / "train_pipeline.py").is_file():
                raise ValueError("학습 구성을 준비 중입니다.")
            if set(params) - {"resume"}:
                raise ValueError("지원하지 않는 학습 설정입니다.")
        else:
            raise ValueError("지원하지 않는 작업입니다.")
        identity = time.strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
        save(jobs / f"{identity}.json", {"id": identity, "kind": kind, "state": "queued", "params": params, "created": time.time()})
        with (jobs / f"{identity}.log").open("w") as log:
            process = subprocess.Popen([sys.executable, "-u", "-B", str(Path(__file__).resolve()), "--worker", identity],
                                       stdout=log, stderr=subprocess.STDOUT, start_new_session=True, cwd=str(WORK))
        update(identity, pid=process.pid)
        return {"job": identity, "state": "running"}


def detect(job, params):
    selection = ensure_selection()
    font = OLD_APP / "fonts"
    if not (WORK / "fonts").exists():
        shutil.copytree(font, WORK / "fonts")
    person = ARCHIVE / "pretrained/yolov8n.pt"
    if not person.is_file():
        person = PROJECT / "최종/3차/사전학습가중치/yolov8n.pt"
    if not (WORK / "yolov8n.pt").exists():
        os.symlink(person, WORK / "yolov8n.pt")
    adapter = types.ModuleType("backend")
    model_root = Path(selection["weights"]).resolve().parents[3]
    permitted = [ARCHIVE.resolve(), (WORK / "training").resolve()]
    if model_root not in permitted:
        raise ValueError("선택 모델의 저장 위치가 허용되지 않습니다.")
    for key, value in {"APP": WORK, "ROOT": model_root, "update": update, "probe": probe,
                       "allowed_video": allowed_video, "save": save, "read": read}.items():
        setattr(adapter, key, value)
    sys.modules["backend"] = adapter
    ffmpeg = types.ModuleType("imageio_ffmpeg")
    ffmpeg.get_ffmpeg_exe = lambda: shutil.which("ffmpeg") or (_ for _ in ()).throw(RuntimeError("ffmpeg가 없습니다."))
    sys.modules.setdefault("imageio_ffmpeg", ffmpeg)
    spec = importlib.util.spec_from_file_location("cleanview_legacy_inference", OLD_APP / "inference.py")
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    inference_adapter = types.ModuleType("inference")
    inference_adapter.predict = configured_predict(original.predict, selection)
    sys.modules["inference"] = inference_adapter
    sys.path.insert(0, str(OLD_APP))
    from detector import detect as run_detect
    chosen_conf = float(selection["conf"])
    run_detect(job, model=selection["weights"], conf=chosen_conf, **params)


def configured_predict(predict, selection):
    # 검증에서 선택한 해상도와 실제 앱 추론의 해상도를 일치시킵니다.
    size = selection.get("imgsz", 1536)
    if type(size) is not int or not 640 <= size <= 2048:
        raise ValueError("선택 모델의 추론 해상도가 올바르지 않습니다.")
    return partial(predict, imgsz=size)


def worker(identity):
    job = read(WORK / "jobs" / f"{identity}.json")
    update(identity, state="running", pid=os.getpid(), stage="준비 중")
    try:
        if job["kind"] == "detect":
            detect(identity, job["params"])
        else:
            from train_pipeline import run
            run(identity, notify=lambda **kw: update(identity, **kw), resume=job["params"].get("resume", False))
        update(identity, state="complete", finished=time.time())
    except Exception as error:
        traceback.print_exc()
        update(identity, state="failed", error=str(error), finished=time.time())
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action")
    parser.add_argument("--params", default="{}")
    parser.add_argument("--worker")
    args = parser.parse_args()
    if args.worker:
        worker(args.worker)
        return
    try:
        if args.action == "health":
            import torch
            import ultralytics
            result = {"cuda": torch.cuda.is_available(), "torch": torch.__version__, "ultralytics": ultralytics.__version__,
                      "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
                      "selection": ensure_selection(), "ffmpeg": shutil.which("ffmpeg")}
        elif args.action == "status":
            result = reconcile()
        elif args.action == "probe":
            result = probe(json.loads(args.params)["path"])
        else:
            result = start(args.action, json.loads(args.params))
        print(json.dumps({"ok": True, "data": result}, ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
