"""D 드라이브의 앱과 기존 GPU 컨테이너를 연결합니다."""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = (Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parent)
PROJECT = ROOT.parent
WORK = ROOT / "work"
CONTAINER = "2026"
REMOTE = "/workspace/2026/월요일 PBL/5차"
PYTHON = "/opt/venvs/torch/bin/python"
ARCHIVE = PROJECT / "이전 도커 실험/3차실험/trash_round3"
VIDEO_ROOTS = [WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]
EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".m4v"}


def load(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def remote_path(path):
    resolved = Path(path).resolve()
    base = Path("D:/2026").resolve()
    return "/workspace/2026/" + resolved.relative_to(base).as_posix()


def local_paths(value):
    if isinstance(value, dict):
        return {k: local_paths(v) for k, v in value.items()}
    if isinstance(value, list):
        return [local_paths(v) for v in value]
    if isinstance(value, str) and value.startswith("/workspace/2026/"):
        return str(Path("D:/2026") / value.removeprefix("/workspace/2026/"))
    return value


def video_path(value):
    p = Path(value).resolve(strict=True)
    if not p.is_file() or p.suffix.lower() not in EXTENSIONS:
        raise ValueError("지원하는 영상 파일을 선택하세요.")
    if not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS):
        raise ValueError("허용된 영상 폴더가 아닙니다.")
    if not p.stat().st_size:
        raise ValueError("0바이트 영상은 처리할 수 없습니다.")
    return p


def docker_call(arguments, timeout=25):
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    p = subprocess.run(["docker", "exec", CONTAINER, PYTHON, *arguments],
                       capture_output=True, timeout=timeout, creationflags=flags)
    if p.returncode:
        message = p.stderr.decode("utf-8", errors="replace")[-3500:]
        raise RuntimeError(message or "Docker 실행에 실패했습니다. Docker Desktop과 2026 컨테이너를 확인하세요.")
    output = p.stdout.decode("utf-8").strip()
    result = json.loads(output)
    if not result.get("ok"):
        raise RuntimeError(result.get("error", "GPU 작업 오류"))
    return local_paths(result["data"])


def tail(path, maximum=12000):
    if not path or not Path(path).is_file():
        return ""
    with Path(path).open("rb") as stream:
        stream.seek(max(0, Path(path).stat().st_size - maximum))
        return stream.read(maximum).decode("utf-8", errors="replace")


def history():
    import csv
    files = sorted((WORK / "training/runs").glob("*/results.csv"), key=lambda p: p.stat().st_mtime)
    if not files:
        return []
    with files[-1].open(encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    result = []
    for row in rows:
        row = {k.strip(): v for k, v in row.items()}
        try:
            result.append({"epoch": int(float(row["epoch"])),
                           "precision": float(row.get("metrics/precision(B)", 0)),
                           "recall": float(row.get("metrics/recall(B)", 0)),
                           "map50": float(row.get("metrics/mAP50(B)", 0)),
                           "loss": float(row.get("train/box_loss", 0))})
        except (KeyError, ValueError):
            continue
    return result


def status():
    jobs = [load(p, {}) for p in (WORK / "jobs").glob("*.json")]
    # 화면은 로컬 파일을 읽고, 실행 중 작업의 생존 여부만 30초 간격으로 확인합니다.
    check = load(WORK / "container_check.json", {})
    if any(j.get("state") in {"queued", "running"} for j in jobs) and time.time() - check.get("checked", 0) >= 30:
        try:
            docker_call([REMOTE + "/gpu_worker.py", "--action", "status"], timeout=6)
            check = {"checked": time.time(), "error": None}
            jobs = [load(p, {}) for p in (WORK / "jobs").glob("*.json")]
        except (RuntimeError, OSError, subprocess.SubprocessError) as error:
            check = {"checked": time.time(), "error": "Docker 연결 확인: " + str(error)}
        temporary = WORK / f"container_check.{os.getpid()}.tmp"
        temporary.write_text(json.dumps(check, ensure_ascii=False), encoding="utf-8")
        temporary.replace(WORK / "container_check.json")
    if check.get("error"):
        for job in jobs:
            if job.get("state") in {"queued", "running"}:
                job.update(error=check["error"])
    jobs = sorted(jobs, key=lambda j: j.get("created", 0), reverse=True)
    for job in jobs[:20]:
        job["log"] = tail(WORK / "jobs" / (job.get("id", "") + ".log"))
    final = load(WORK / "training/final.json") or load(ARCHIVE / "final.json", {})
    test = final.get("test", {})
    operating = test.get("operating", {})
    ap = test.get("metrics", {})
    metrics = {"precision": operating.get("precision"), "recall": operating.get("recall"),
               "map50": ap.get("metrics/mAP50(B)", ap.get("map50")),
               "map50_95": ap.get("metrics/mAP50-95(B)", ap.get("map50_95")),
               "split": "5차 최종 테스트" if (WORK / "training/final.json").is_file() else "3차 과거 테스트 150장",
               "target_met": final.get("target_met", False)}
    training_job = next((j for j in jobs if j.get("kind") == "train"), {})
    training = {**load(WORK / "training/status.json", {}), "history": history(), "log": training_job.get("log", "")}
    manifest = load(WORK / "training/data_manifest.json", {})
    dataset = {key: manifest[key] for key in ("counts", "sources", "download_bytes", "test_protocol", "external_test", "near_duplicate", "created") if key in manifest}
    dataset["manifest_path"] = str(WORK / "training/data_manifest.json")
    return local_paths({"jobs": jobs[:20], "selection": load(WORK / "selected_model.json", {}),
                        "metrics": metrics, "training": training,
                        "dataset": dataset,
                        "container": CONTAINER, "project": str(ROOT),
                        "independent": True, "note": "Codex/API 토큰 없이 이 PC의 Docker GPU에서 실행됩니다."})


def action(name, params):
    if not isinstance(params, dict):
        raise ValueError("설정은 JSON 객체여야 합니다.")
    if name == "status":
        return status()
    if name == "videos":
        # 같은 보존 영상을 두 번 나열하지 않고 대표 폴더를 사용합니다.
        stored = next((p for p in VIDEO_ROOTS[1:] if p.is_dir() and any(p.iterdir())), None)
        folders = [VIDEO_ROOTS[0]] + ([stored] if stored else [])
        return [{"path": str(p.resolve()), "name": p.name, "bytes": p.stat().st_size}
                for folder in folders if folder.exists()
                for p in sorted(folder.rglob("*")) if p.is_file() and p.suffix.lower() in EXTENSIONS]
    if name in {"probe", "detect"}:
        params = {**params, "path": remote_path(video_path(params.get("path", "")))}
    if name not in {"probe", "detect", "train", "health"}:
        raise ValueError("지원하지 않는 작업입니다.")
    return docker_call([REMOTE + "/gpu_worker.py", "--action", name,
                        "--params", json.dumps(params, ensure_ascii=False)], timeout=25)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", required=True)
    parser.add_argument("--params", default="{}")
    args = parser.parse_args()
    try:
        result = {"ok": True, "data": action(args.action, json.loads(args.params))}
    except Exception as error:
        result = {"ok": False, "error": str(error)}
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
