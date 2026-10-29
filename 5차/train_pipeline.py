"""검증에서 기존 모델과 추가 학습 모델을 비교하고 고정 테스트를 한 번 평가합니다."""
import csv
import hashlib
import json
import math
import time
from pathlib import Path

from prepare_training import (ARCHIVE, ROOT, TRAINING, SEED, atomic_json, freeze_manifest,
                              load, prepare, sha256_file, validate_yolo, verify_records)

THRESHOLDS = [.05, .1, .15, .17, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .9]


def select_threshold(counts, thresholds):
    choices = []
    for index, threshold in enumerate(thresholds):
        tp, fp, fn = (int(counts[key][index]) for key in ("tp", "fp", "fn"))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        choices.append({"threshold": threshold, "precision": precision, "recall": recall,
                        "f1": f1, "tp": tp, "fp": fp, "fn": fn, "iou": .5})
    if not choices:
        raise ValueError("선택할 검증 임계값이 없습니다.")
    return max(choices, key=lambda c: (min(c["precision"], c["recall"]), c["f1"]))


def choose_candidate(results):
    if not results:
        raise ValueError("비교할 검증 결과가 없습니다.")
    # 호출자는 기존 선택을 먼저 전달합니다. 동점이면 기존 모델을 보존합니다.
    return max(results, key=lambda r: (min(r["operating"]["precision"], r["operating"]["recall"]),
                                      r["operating"]["f1"], r["metrics"]["metrics/mAP50(B)"]))


def resume_decision(directory, contract, allow_resume=True):
    directory = Path(directory)
    saved = directory / "run_contract.json"
    if saved.exists() and load(saved) != contract:
        raise ValueError("checkpoint의 데이터·학습 조건이 현재 명세와 다릅니다.")
    if (directory / "phase_complete.json").exists():
        if not saved.exists():
            raise ValueError("완료 학습의 원래 계약이 없습니다.")
        return "complete"
    if (directory / "weights/last.pt").exists():
        if not saved.exists():
            raise ValueError("원래 계약 없는 checkpoint는 자동 재개할 수 없습니다.")
        if not allow_resume:
            raise ValueError("중단 checkpoint가 있습니다. 재개를 명시적으로 선택하세요.")
        return "resume"
    return "new"


def iou(left, right):
    intersection = max(0, min(left[2], right[2]) - max(left[0], right[0])) * max(0, min(left[3], right[3]) - max(left[1], right[1]))
    area_left = max(0, left[2] - left[0]) * max(0, left[3] - left[1])
    area_right = max(0, right[2] - right[0]) * max(0, right[3] - right[1])
    union = area_left + area_right - intersection
    return intersection / union if union else 0.0


def nms(predictions):
    pending = sorted(predictions, key=lambda r: r[4], reverse=True)
    selected = []
    for row in pending:
        if all(iou(row, old) <= .5 for old in selected):
            selected.append(row)
        if len(selected) >= 300:
            break
    return selected


def match_predictions(predictions, targets, threshold):
    used, matches = set(), []
    for prediction in predictions:
        choices = [(iou(prediction, target), index) for index, target in enumerate(targets) if index not in used]
        overlap, index = max(choices, default=(0.0, -1))
        matched = overlap >= threshold
        matches.append(matched)
        if matched:
            used.add(index)
    return matches


def average_precision(rows, targets, column):
    if not targets:
        return 0.0
    ordered = sorted(rows, key=lambda r: r[0], reverse=True)
    tp, points = 0, []
    for index, (_, matches) in enumerate(ordered):
        tp += int(matches[column])
        points.append((tp / targets, tp / (index + 1)))
    # 단일 클래스, 신뢰도 순 일대일 IoU 매칭의 101점 보간 AP입니다.
    return sum(max((p for r, p in points if r >= step / 100), default=0.0) for step in range(101)) / 101


def evaluate(weights, records, out, notify, threshold=None):
    from ultralytics import YOLO
    import torch
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    contract = {"weights": {str(p): sha256_file(p) for p in weights},
                "images": {r["id"]: [r["sha256"], r["label_sha256"]] for r in records},
                "imgsz": 1280, "nms_iou": .5, "max_det": 300,
                "operating_threshold": threshold, "evaluator": "greedy confidence IoU, 101-point interpolated AP v1"}
    freeze_manifest(out / "contract.json", contract)
    if (out / "metrics.json").exists():
        return load(out / "metrics.json")
    models = [YOLO(str(p)) for p in weights]
    if any(len(model.names) != 1 or model.names[0] != "trash" for model in models):
        raise ValueError("단일 trash 클래스 가중치가 아닙니다.")
    scored, total_targets = [], 0
    for index, record in enumerate(records):
        cached = out / "predictions" / (record["id"] + ".json")
        if cached.exists():
            predictions = load(cached)
        else:
            predictions = []
            for model in models:
                result = model.predict(record["image"], imgsz=1280, conf=.001, iou=.5,
                                       max_det=300, device=0, verbose=False)[0]
                predictions += result.boxes.data[:, :5].detach().cpu().tolist()
            predictions = nms(predictions)
            atomic_json(cached, predictions)
        labels = validate_yolo(Path(record["label"]).read_text(encoding="utf-8"))
        w, h = record["width"], record["height"]
        targets = [[(x - bw / 2) * w, (y - bh / 2) * h, (x + bw / 2) * w, (y + bh / 2) * h]
                   for _, x, y, bw, bh in labels]
        total_targets += len(targets)
        matches = [match_predictions(predictions, targets, .5 + offset * .05) for offset in range(10)]
        scored += [(row[4], [matches[offset][j] for offset in range(10)]) for j, row in enumerate(predictions)]
        if index % 10 == 0:
            notify(stage=f"검증·평가 {out.name}", evaluated=index + 1, evaluation_images=len(records))
    candidates = THRESHOLDS if threshold is None else [threshold]
    counts = {"tp": [], "fp": [], "fn": []}
    for conf in candidates:
        chosen = [matches[0] for score, matches in scored if score >= conf]
        tp = sum(chosen)
        counts["tp"].append(tp)
        counts["fp"].append(len(chosen) - tp)
        counts["fn"].append(total_targets - tp)
    result = {"weights": list(map(str, weights)), "policy": "full", "images": len(records), "imgsz": 1280,
              "operating": select_threshold(counts, candidates),
              "metrics": {"metrics/mAP50(B)": average_precision(scored, total_targets, 0),
                          "metrics/mAP50-95(B)": sum(average_precision(scored, total_targets, k) for k in range(10)) / 10},
              "evaluator": contract["evaluator"], "threshold_source": "validation only"}
    atomic_json(out / "metrics.json", result)
    del models
    torch.cuda.empty_cache()
    return result


def run(job, notify=lambda **kw: None, resume=False):
    from ultralytics import YOLO
    import torch
    TRAINING.mkdir(parents=True, exist_ok=True)
    status = {"job": job, "epoch": 0, "epochs": 180}
    def progress(**kwargs):
        status.update(kwargs, updated=time.time())
        atomic_json(TRAINING / "status.json", status)
        notify(**kwargs)
    if (TRAINING / "final.json").exists():
        progress(stage="완료한 결과 재사용")
        final = load(TRAINING / "final.json")
        publish_selection(final)
        return final
    manifest = prepare(notify=progress)
    manifest_hash = sha256_file(TRAINING / "data_manifest.json")
    progress(stage="검증 기준과 추가 학습 조건 고정", **manifest["counts"])
    reference = load(ARCHIVE / "final.json")["selected"]
    baseline = [ARCHIVE / Path(p).relative_to("/root/환경 PBL/trash_round3") for p in reference["weights"]]
    initial = ARCHIVE / "runs/yolo26l_p2_focus/weights/best.pt"
    directory = TRAINING / "runs/yolo26l_p2_extra"
    contract = {"manifest_sha256": manifest_hash, "initial_sha256": sha256_file(initial), "seed": SEED,
                "pipeline_sha256": sha256_file(Path(__file__)),
                "preparation_sha256": sha256_file(ROOT / "prepare_training.py"),
                "epochs": 180, "patience": 35, "imgsz": 1280, "batch": 2, "optimizer": "AdamW",
                "selection": "maximize min(precision,recall), then F1, then AP50; baseline wins ties"}
    mode = resume_decision(directory, contract, allow_resume=resume)
    directory.mkdir(parents=True, exist_ok=True)
    freeze_manifest(directory / "run_contract.json", contract)
    if mode != "complete":
        last = directory / "weights/last.pt"
        resuming = mode == "resume"
        if resuming:
            checkpoint = torch.load(last, map_location="cpu", weights_only=False)
            epoch = int(checkpoint.get("epoch", -1))
            del checkpoint
            if epoch < 0:
                if (directory / "weights/best.pt").exists() and (directory / "results.csv").exists():
                    mode = "complete"
                else:
                    raise ValueError("정리된 checkpoint에 완료 결과가 없습니다.")
        if mode != "complete":
            model = YOLO(str(last if resuming else initial))
            def epoch_end(trainer):
                metrics = {str(k): float(v) for k, v in trainer.metrics.items()}
                progress(stage="YOLO26l-P2 추가 학습", epoch=trainer.epoch + 1, epochs=180,
                         precision=metrics.get("metrics/precision(B)"), recall=metrics.get("metrics/recall(B)"),
                         map50=metrics.get("metrics/mAP50(B)"), metrics=metrics)
            model.add_callback("on_fit_epoch_end", epoch_end)
            progress(stage="checkpoint 재개" if resuming else "YOLO26l-P2 추가 학습 시작")
            if resuming:
                model.train(resume=True, device=0)
            else:
                model.train(data=str(TRAINING / "dataset.yaml"), project=str(TRAINING / "runs"),
                            name=directory.name, exist_ok=True, epochs=180, patience=35, imgsz=1280,
                            batch=2, device=0, workers=4, cache=False, amp=True, seed=SEED,
                            optimizer="AdamW", lr0=.00015, lrf=.05, cos_lr=True, warmup_epochs=3,
                            mosaic=.5, close_mosaic=15, scale=.5, translate=.1, fliplr=.5, degrees=5,
                            plots=True, save=True, deterministic=True)
            del model
            torch.cuda.empty_cache()
        best = directory / "weights/best.pt"
        if not best.is_file():
            raise ValueError("완료 학습 가중치가 없습니다.")
        atomic_json(directory / "phase_complete.json", {"best_sha256": sha256_file(best), "completed": time.time()})
    best = directory / "weights/best.pt"
    if sha256_file(best) != load(directory / "phase_complete.json")["best_sha256"]:
        raise ValueError("완료 학습 모델이 기록된 해시와 다릅니다.")
    verify_records(manifest["records"])
    validation = [r for r in manifest["records"] if r["split"] == "val"]
    historical_test = [r for r in manifest["records"] if r["split"] == "test"]
    results = []
    for name, weights in [("baseline_ensemble", baseline), ("baseline_l_p2", [initial]), ("additional_l_p2", [best])]:
        result = evaluate(weights, validation, TRAINING / "evaluation" / name, progress)
        result["name"] = name
        results.append(result)
        atomic_json(TRAINING / "validation_comparison.json", results)
    selected = choose_candidate(results)
    freeze_manifest(TRAINING / "selection.json", selected)
    # 테스트 계약을 선택 직후 고정합니다. 이후 선택이나 임계값이 바뀌면 재평가를 차단합니다.
    test_contract = {"selected": selected, "manifest_sha256": manifest_hash,
                     "protocol": "historical benchmark; no tuning on test; cached per-image predictions"}
    freeze_manifest(TRAINING / "test_contract.json", test_contract)
    progress(stage="선택 완료 · 과거 고정 테스트 최종 평가")
    test = evaluate(selected["weights"], historical_test, TRAINING / "evaluation/test_final", progress,
                    threshold=selected["operating"]["threshold"])
    target = test["operating"]["precision"] >= .9 and test["operating"]["recall"] >= .9
    final = {"selected": selected, "test": test, "target_met": target, "manifest_sha256": manifest_hash,
             "test_protocol": manifest["test_protocol"], "external_test": None,
             "baseline_retained": selected["name"] != "additional_l_p2", "finished": time.time(),
             "metric_limit": "AP evaluator and 1280 input differ from round3; compare candidates within this run"}
    publish_selection(final)
    atomic_json(TRAINING / "final.json", final)
    progress(stage="학습·비교·고정 평가 완료", target_met=target, precision=test["operating"]["precision"],
             recall=test["operating"]["recall"], map50=test["metrics"]["metrics/mAP50(B)"])
    return final


def publish_selection(final):
    selected = final["selected"]
    atomic_json(ROOT / "work/selected_model.json", {"weights": selected["weights"][0], "ensemble": selected["weights"],
                "policy": "full", "imgsz": selected["imgsz"], "conf": selected["operating"]["threshold"],
                "source": selected["name"], "test": final["test"], "target_met": final["target_met"]})
