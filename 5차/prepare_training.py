"""출처와 고정 평가 자료를 보존하며 추가 학습 데이터를 준비합니다."""
import argparse
import collections
import concurrent.futures
import hashlib
import io
import json
import math
import os
import random
import re
import shutil
import struct
import threading
import time
import urllib.request
import uuid
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent / "이전 도커 실험/3차실험/trash_round3"
TRAINING = ROOT / "work/training"
SEED = 20261028
MAX_BYTES = 20 * 1024 ** 3
STREET_URL = "https://zenodo.org/api/records/8288500/files/images.zip/content"
STREET_SIZE = 13728630001
_ERROR_LOCK = threading.Lock()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix("." + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def sha256_file(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_yolo(text):
    rows = []
    for line in text.split("\n"):
        if not line.strip():
            continue
        row = list(map(float, line.split()))
        if len(row) != 5 or row[0] != 0 or not all(math.isfinite(n) for n in row):
            raise ValueError("단일 trash 클래스와 유한한 YOLO 좌표가 필요합니다.")
        _, x, y, width, height = row
        # 보존 라벨 소수점 7자리 반올림의 최대 5e-8 경계 차이를 허용합니다.
        tolerance = 1e-7
        if width <= 0 or height <= 0 or not (-tolerance <= x - width / 2 and x + width / 2 <= 1 + tolerance
                                                           and -tolerance <= y - height / 2 and y + height / 2 <= 1 + tolerance):
            raise ValueError("라벨 상자가 이미지 경계를 벗어났습니다.")
        rows.append([0, x, y, width, height])
    return rows


def coco_to_yolo(image, annotations):
    width, height = float(image["width"]), float(image["height"])
    if not all(math.isfinite(n) and n > 0 for n in (width, height)):
        raise ValueError("이미지 크기가 올바르지 않습니다.")
    rows = []
    for annotation in annotations:
        x, y, w, h = map(float, annotation["bbox"])
        if not all(math.isfinite(n) for n in (x, y, w, h)) or w <= 0 or h <= 0:
            raise ValueError("COCO 상자의 크기가 올바르지 않습니다.")
        left, top, right, bottom = max(0, x), max(0, y), min(width, x + w), min(height, y + h)
        if right <= left or bottom <= top:
            raise ValueError("이미지와 겹치지 않는 COCO 상자입니다.")
        rows.append([0, (left + right) / (2 * width), (top + bottom) / (2 * height),
                     (right - left) / width, (bottom - top) / height])
    return rows


def group_key(source, image):
    path = PurePosixPath(str(image.get("path", image.get("file_name", image.get("id", "unknown")))).replace("\\", "/"))
    parts = [s for s in path.parts if s not in {"/", "datasets"}]
    location = parts[0] if len(parts) > 1 else "unknown-location"
    match = re.search(r"G[HX]\d{2}(\d{4})", path.stem)
    # 같은 GoPro 녹화의 장 번호와 물체 종류별 하위 폴더는 분리하지 않습니다.
    identity = match.group(1) if match else location
    return f"{source}:{location}:{identity}"


def prior_street_ids(records):
    identities = set()
    for row in records:
        if row.get("source") != "pLitterStreet":
            continue
        match = re.search(r"(?:plitter|street)_(\d+)(?:\.[^/\\]+)?$", str(row.get("image", "")))
        if not match:
            raise ValueError("과거 pLitterStreet 자료의 원본 ID를 확인할 수 없습니다.")
        identities.add(match.group(1))
    return identities


def split_groups(records, seen_groups=(), seed=SEED):
    groups = sorted({r["group"] for r in records} - set(seen_groups))
    random.Random(seed).shuffle(groups)
    count = max(1, len(groups) // 10) if len(groups) >= 10 else 0
    mapping = {g: "external_test" for g in groups[:count]}
    mapping.update({g: "external_val" for g in groups[count:2 * count]})
    return [{**r, "split": mapping.get(r["group"], "train")} for r in sorted(records, key=lambda r: r["id"])]


def image_info(path):
    from PIL import Image, UnidentifiedImageError
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image.load()
            if image.width < 16 or image.height < 16 or image.width * image.height > 100000000:
                raise ValueError("허용 범위 밖의 이미지 크기입니다.")
            gray = image.convert("L").resize((9, 8))
            pixels = [gray.getpixel((x, y)) for y in range(8) for x in range(9)]
            signature = sum((pixels[y * 9 + x] > pixels[y * 9 + x + 1]) << (y * 8 + x)
                            for y in range(8) for x in range(8))
            return {"sha256": sha256_file(path), "signature": f"{signature:016x}",
                    "width": image.width, "height": image.height, "bytes": Path(path).stat().st_size}
    except (OSError, UnidentifiedImageError, SyntaxError) as error:
        raise ValueError("이미지를 완전히 해독할 수 없습니다.") from error


def deduplicate(records, protected=(), distance=4):
    accepted, rejected = [], []
    hashes = {r["sha256"] for r in protected}
    signatures = [int(r["signature"], 16) for r in protected]
    for record in records:
        signature = int(record["signature"], 16)
        reason = "동일 해시" if record["sha256"] in hashes else "근접 이미지" if any(
            (signature ^ old).bit_count() <= distance for old in signatures) else None
        if reason:
            rejected.append({**record, "excluded_reason": reason})
        else:
            accepted.append(record)
            hashes.add(record["sha256"])
            signatures.append(signature)
    return accepted, rejected


class BudgetExceeded(ValueError):
    pass


class DownloadBudget:
    def __init__(self, root, limit=MAX_BYTES, notify=lambda **kw: None):
        self.root = Path(root)
        self.path = self.root / "download_ledger.json"
        self.limit, self.notify = min(limit, MAX_BYTES), notify
        self.used = int(load(self.path)["download_bytes"]) if self.path.exists() else 0
        self.reserved = 0
        self.lock = threading.Lock()

    def reserve(self, count):
        with self.lock:
            if count < 0 or self.used + self.reserved + count > self.limit:
                raise BudgetExceeded("추가 데이터 전송 누적 20GB 상한에 도달했습니다.")
            self.reserved += count

    def release(self, count):
        with self.lock:
            self.reserved -= count
            if self.reserved < 0:
                raise ValueError("전송 예약량이 음수가 됐습니다.")

    def charge(self, count, reserved=False):
        with self.lock:
            if count < 0 or self.used + (0 if reserved else self.reserved) + count > self.limit:
                raise BudgetExceeded("추가 데이터 전송 누적 20GB 상한에 도달했습니다.")
            if reserved:
                if count > self.reserved:
                    raise ValueError("전송 예약보다 수신량이 큽니다.")
                self.reserved -= count
            self.used += count
            atomic_json(self.path, {"download_bytes": self.used, "limit_bytes": self.limit})
            self.notify(download_bytes=self.used, download_limit_bytes=self.limit)


def request(url, **kwargs):
    if not url.startswith("https://") and not url.startswith("http://127.0.0.1:"):
        raise ValueError("HTTPS 데이터 출처만 허용됩니다.")
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "CleanView/5 research preparation", **kwargs.pop("headers", {})}, **kwargs), timeout=40)


def download(url, destination, budget, expected_md5=None):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    receipt = destination.with_suffix(destination.suffix + ".download.json")
    if destination.exists() and receipt.exists() and load(receipt)["sha256"] == sha256_file(destination):
        return destination
    with request(url, method="HEAD") as response:
        length = int(response.headers["Content-Length"])
        etag = response.headers.get("ETag")
    if length <= 0:
        raise ValueError("원본 크기가 올바르지 않습니다.")
    partial = destination.with_suffix(destination.suffix + ".part")
    metadata = destination.with_suffix(destination.suffix + ".part.json")
    identity = {"url": url, "etag": etag, "size": length}
    resume = bool(etag and partial.exists() and metadata.exists() and load(metadata) == identity)
    start = partial.stat().st_size if resume else 0
    if start > length:
        raise ValueError("부분 다운로드가 원본 크기보다 큽니다.")
    atomic_json(metadata, identity)
    if start < length:
        remaining = length - start
        budget.reserve(remaining)
        try:
            with request(url, headers={"Range": f"bytes={start}-", "If-Range": etag} if start else {}) as response:
                if start and (response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-")):
                    raise ValueError("서버가 재개 범위 요청을 보존하지 않았습니다.")
                if int(response.headers.get("Content-Length", remaining)) != remaining:
                    raise ValueError("원본과 실제 전송 크기가 다릅니다.")
                with partial.open("ab" if start else "wb") as stream:
                    while remaining:
                        block = response.read(min(256 * 1024, remaining))
                        if not block:
                            break
                        budget.charge(len(block), reserved=True)
                        remaining -= len(block)
                        stream.write(block)
        finally:
            budget.release(remaining)
    if partial.stat().st_size != length:
        raise ValueError("다운로드가 완성되지 않았습니다.")
    if expected_md5:
        digest = hashlib.md5(partial.read_bytes(), usedforsecurity=False).hexdigest()
        if digest != expected_md5:
            raise ValueError("공식 MD5와 다운로드가 일치하지 않습니다.")
    partial.replace(destination)
    atomic_json(receipt, {**identity, "sha256": sha256_file(destination)})
    return destination


class RemoteZip:
    def __init__(self, url, size, budget):
        self.url, self.size, self.budget, self.pos = url, size, budget, 0

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else self.size + offset
        return self.pos

    def read(self, n=-1):
        n = min(self.size - self.pos, n if n >= 0 else self.size - self.pos)
        if n <= 0:
            return b""
        data = range_bytes(self.url, self.pos, self.pos + n - 1, self.budget)
        self.pos += len(data)
        return data


def range_bytes(url, start, end, budget):
    if start < 0 or end < start or end - start > 32 * 1024 ** 2:
        raise ValueError("허용 범위를 넘는 ZIP 부분 요청입니다.")
    remaining = end - start + 1
    budget.reserve(remaining)
    blocks = []
    try:
        with request(url, headers={"Range": f"bytes={start}-{end}"}) as response:
            if response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/"):
                raise ValueError("서버가 정확한 ZIP 부분 요청을 지원하지 않습니다.")
            while remaining:
                block = response.read(min(256 * 1024, remaining))
                if not block:
                    break
                budget.charge(len(block), reserved=True)
                remaining -= len(block)
                blocks.append(block)
    finally:
        budget.release(remaining)
    data = b"".join(blocks)
    if len(data) != end - start + 1:
        raise ValueError("ZIP 부분 응답 크기가 다릅니다.")
    return data


def zip_member(info, budget):
    if info.file_size > 32 * 1024 ** 2 or info.compress_size > 32 * 1024 ** 2:
        raise ValueError("과도한 단일 이미지 크기입니다.")
    header = range_bytes(STREET_URL, info.header_offset, info.header_offset + 29, budget)
    if header[:4] != b"PK\x03\x04":
        raise ValueError("ZIP 지역 헤더가 올바르지 않습니다.")
    name_size, extra_size = struct.unpack_from("<HH", header, 26)
    offset = info.header_offset + 30 + name_size + extra_size
    payload = range_bytes(STREET_URL, offset, offset + info.compress_size - 1, budget)
    if info.compress_type == zipfile.ZIP_DEFLATED:
        decoder = zlib.decompressobj(-15)
        data = decoder.decompress(payload, info.file_size + 1)
        if decoder.unconsumed_tail or not decoder.eof:
            raise ValueError("ZIP 압축 해제 크기가 선언과 다릅니다.")
    elif info.compress_type == zipfile.ZIP_STORED:
        data = payload
    else:
        raise ValueError("지원하지 않는 ZIP 압축입니다.")
    if len(data) != info.file_size or zlib.crc32(data) & 0xffffffff != info.CRC:
        raise ValueError("ZIP 이미지 CRC가 일치하지 않습니다.")
    return data


def freeze_manifest(path, value):
    path = Path(path)
    if path.exists():
        if load(path) != value:
            raise ValueError("고정 데이터 명세를 현재 값으로 바꿀 수 없습니다.")
        return
    atomic_json(path, value)


def failure(training, source, identity, error):
    with _ERROR_LOCK:
        with (training / "download_errors.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps({"kst": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "source": source,
                                     "id": identity, "error": str(error)}, ensure_ascii=False) + "\n")


def write_labels(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(" ".join(f"{v:.9g}" for v in row) + "\n" for row in rows)
    validate_yolo(text)
    path.write_text(text, encoding="utf-8", newline="\n")


def verify_records(records):
    for row in records:
        if sha256_file(row["image"]) != row["sha256"] or sha256_file(row["label"]) != row["label_sha256"]:
            raise ValueError("고정 이미지 또는 라벨이 변경됐습니다: " + row["id"])


def _prepare(notify=lambda **kw: None, street_limit=4000, salsa_limit=1400):
    training = TRAINING
    training.mkdir(parents=True, exist_ok=True)
    status = {}
    status_lock = threading.Lock()
    def progress(**kw):
        with status_lock:
            status.update(kw, updated=time.time())
            atomic_json(training / "status.json", status)
            notify(**kw)
    progress(stage="학습 데이터와 고정 평가 자료 확인", epoch=0, epochs=180)
    manifest_path = training / "data_manifest.json"
    if manifest_path.exists():
        manifest = load(manifest_path)
        if manifest["sources_sha256"] != sha256_file(ROOT / "sources.json"):
            raise ValueError("고정 명세 작성 뒤 데이터 출처 정책이 바뀌었습니다.")
        verify_records(manifest["records"])
        progress(stage="고정 데이터 명세 재사용", **manifest["counts"])
        return manifest
    if shutil.disk_usage(training).free < 25 * 1024 ** 3:
        raise ValueError("데이터 준비와 학습을 위한 여유 공간 25GB가 필요합니다.")
    budget = DownloadBudget(training, notify=progress)
    records, rejected, protected = [], [], []
    for manifest_name, base in [("reference_holdout_sha256.json", ARCHIVE / "data/reference"),
                                ("original_holdout_sha256.json", ARCHIVE)]:
        for relative, expected in load(ARCHIVE / manifest_name).items():
            source = base / relative
            if sha256_file(source) != expected:
                raise ValueError("과거 고정 평가 기준과 다릅니다: " + str(source))
    for split in ["val", "test", "train"]:
        folder = ARCHIVE / "data/full/images" / split
        for index, image in enumerate(sorted(folder.glob("*"))):
            if not image.is_file():
                continue
            label = ARCHIVE / "data/full/labels" / split / (image.stem + ".txt")
            validate_yolo(label.read_text(encoding="utf-8"))
            info = image_info(image)
            row = {**info, "id": "taco_" + split + "_" + image.stem, "source": "TACO preserved",
                   "image": str(image), "label": str(label), "label_sha256": sha256_file(label),
                   "group": "taco:" + image.stem, "split": split}
            records.append(row)
            if split != "train":
                protected.append(row)
                reference = ARCHIVE / "data/reference/images" / split / image.name
                if reference.is_file():
                    protected.append(image_info(reference))
            if index % 100 == 0:
                progress(stage=f"원본 {split} 무결성 검사", checked=index + 1)
    baseline_train, removed = deduplicate([r for r in records if r["split"] == "train"], protected)
    rejected.extend(removed)
    records = [r for r in records if r["split"] != "train"] + baseline_train
    protected_for_external = records + protected
    raw = training / "downloads"
    raw.mkdir(exist_ok=True)
    sources = load(ROOT / "sources.json")
    old_street_manifest = ARCHIVE / "sources/additional_manifest.json"
    used_street_ids = prior_street_ids(load(old_street_manifest))
    # 공식 원자료와 MD5를 보존하고 ZIP 전체 대신 선택한 이미지 범위만 읽습니다.
    annotations = download("https://zenodo.org/api/records/8288500/files/annotations.zip/content",
                           raw / "plitter_annotations.zip", budget, "2484e076b1e9d66036b0a15e9928692f")
    with zipfile.ZipFile(annotations) as archive:
        name = next(n for n in archive.namelist() if n.endswith("10_class_splits/annotations_all.json"))
        street = json.loads(archive.read(name))
    by_id = collections.defaultdict(list)
    for annotation in street["annotations"]:
        if annotation["category_id"] != 4:
            by_id[annotation["image_id"]].append(annotation)
    images = [i for i in street["images"] if by_id[i["id"]] and not i.get("deleted")]
    random.Random(SEED).shuffle(images)
    with zipfile.ZipFile(RemoteZip(STREET_URL, STREET_SIZE, budget)) as remote:
        members = collections.defaultdict(list)
        for member in remote.infolist():
            if not member.is_dir():
                members[PurePosixPath(member.filename).name].append(member)
    choices = []
    for image in images:
        found = members.get(image["file_name"], [])
        exact = [m for m in found if m.filename.endswith(image.get("path", "").removeprefix("/datasets/"))]
        member = exact[0] if len(exact) == 1 else found[0] if len(found) == 1 else None
        if member:
            choices.append((image, member))
        if len(choices) >= street_limit:
            break
    progress(stage="pLitterStreet 원본 이미지 확보", requested=len(choices), downloaded=0, download_bytes=budget.used)
    external = []
    def acquire(pair):
        image, member = pair
        identity = f"plitter_{image['id']}"
        destination = training / "data/images/train" / (identity + ".jpg")
        label = training / "data/labels/train" / (identity + ".txt")
        receipt = destination.with_suffix(".source.json")
        try:
            if destination.exists():
                if not receipt.exists() or load(receipt)["sha256"] != sha256_file(destination):
                    raise ValueError("기존 다운로드의 보존 해시가 없거나 다릅니다.")
            else:
                data = zip_member(member, budget)
                destination.parent.mkdir(parents=True, exist_ok=True)
                temporary = destination.with_suffix(".part")
                temporary.write_bytes(data)
                image_info(temporary)
                temporary.replace(destination)
                atomic_json(receipt, {"sha256": sha256_file(destination), "zip_member": member.filename,
                                      "crc32": member.CRC, "zip_bytes": STREET_SIZE, "url": STREET_URL})
            info = image_info(destination)
            if info["width"] != image["width"] or info["height"] != image["height"]:
                raise ValueError("COCO와 원본 이미지 크기가 다릅니다.")
            write_labels(label, coco_to_yolo(image, by_id[image["id"]]))
            return {**info, "id": identity, "source": "pLitterStreet", "image": str(destination),
                    "label": str(label), "label_sha256": sha256_file(label), "group": group_key("pLitterStreet", image),
                    "split": "train", "url": STREET_URL, "zip_member": member.filename, "license": "CC-BY-4.0",
                    "source_id": str(image["id"]), "identity_status": "restored" if str(image["id"]) in used_street_ids
                    else "new_to_round3_manifest"}
        except BudgetExceeded:
            raise
        except Exception as error:
            failure(training, "pLitterStreet", identity, error)
            return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        consecutive_failures = 0
        for start in range(0, len(choices), 6):
            for index, row in enumerate(pool.map(acquire, choices[start:start + 6]), start):
                if row:
                    external.append(row)
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                if consecutive_failures >= 3:
                    raise ValueError("이미지 확보가 연속 3개 실패했습니다. 원인을 확인한 뒤 재개하세요.")
                progress(stage="pLitterStreet 원본 이미지 확보", downloaded=index + 1, valid_images=len(external), requested=len(choices))
    if len(external) < min(500, street_limit):
        raise ValueError(f"pLitterStreet 유효 이미지 부족: {len(external)}. download_errors.jsonl을 확인하세요.")
    # 기존 학습에 사용한 데이터셋은 새로운 독립 테스트라고 표시하지 않습니다.
    # pLitterStreet와 SALSA는 전부 학습 전용이며 고정 TACO val/test는 따로 유지합니다.
    salsa_path = ARCHIVE / "sources/salsa/annotations.json"
    salsa = load(salsa_path)
    salsa_by_id = collections.defaultdict(list)
    for annotation in salsa["annotations"]:
        salsa_by_id[annotation["image_id"]].append(annotation)
    salsa_images = [i for i in salsa["images"] if i.get("license") == 1 and not i["file_name"].startswith("batch_") and salsa_by_id[i["id"]]]
    random.Random(SEED).shuffle(salsa_images)
    progress(stage="SALSA CC BY 4.0 이미지 복원", requested=min(len(salsa_images), salsa_limit), downloaded=0)
    for index, image in enumerate(salsa_images[:salsa_limit]):
        identity = f"salsa_{image['id']}"
        destination = training / "data/images/train" / (identity + ".jpg")
        label = training / "data/labels/train" / (identity + ".txt")
        try:
            download(image["flickr_url"], destination, budget)
            info = image_info(destination)
            if (info["width"], info["height"]) != (image["width"], image["height"]):
                raise ValueError("SALSA 라벨과 이미지 크기가 다릅니다.")
            write_labels(label, coco_to_yolo(image, salsa_by_id[image["id"]]))
            external.append({**info, "id": identity, "source": "SALSA", "image": str(destination), "label": str(label),
                             "label_sha256": sha256_file(label), "group": "SALSA:OpenLitterMap", "split": "train",
                             "url": image["flickr_url"], "license": "CC-BY-4.0", "annotations_license": "ODbL-1.0"})
        except BudgetExceeded:
            raise
        except Exception as error:
            failure(training, "SALSA", identity, error)
        if index % 10 == 0:
            progress(stage="SALSA CC BY 4.0 이미지 복원", downloaded=index + 1)
    progress(stage="고정 평가 우선 해시·근접 중복 배제")
    accepted, excluded = deduplicate(external, protected_for_external)
    rejected.extend(excluded)
    records += accepted
    if len(accepted) < 500:
        raise ValueError("중복 배제 후 추가 학습 이미지가 500개 미만입니다.")
    counts = dict(collections.Counter(r["split"] for r in records))
    counts.update(additional=len(accepted), original_train=len(baseline_train),
                  plitter=sum(r["source"] == "pLitterStreet" for r in accepted),
                  salsa=sum(r["source"] == "SALSA" for r in accepted), excluded=len(rejected),
                  restored=sum(r.get("identity_status") == "restored" for r in accepted),
                  new_identity=sum(r.get("identity_status") == "new_to_round3_manifest" for r in accepted))
    for split in ["train", "val", "test"]:
        (training / (split + ".txt")).write_text("".join(r["image"] + "\n" for r in records if r["split"] == split), encoding="utf-8", newline="\n")
    config = {"path": str(training), "train": str(training / "train.txt"), "val": str(training / "val.txt"),
              "test": str(training / "test.txt"), "names": {0: "trash"}}
    # JSON은 YAML의 부분집합이므로 별도 YAML 패키지 없이 같은 명세를 저장합니다.
    atomic_json(training / "dataset.yaml", config)
    atomic_json(training / "excluded.json", rejected)
    manifest = {"schema": 1, "seed": SEED, "records": records, "counts": counts,
                "sources": sources, "sources_sha256": sha256_file(ROOT / "sources.json"),
                "prior_street_manifest_sha256": sha256_file(old_street_manifest), "prior_street_ids": len(used_street_ids),
                "download_bytes": budget.used, "test_protocol": "historical benchmark: previously evaluated 150 photographs",
                "external_test": None, "near_duplicate": "64-bit difference hash, Hamming <= 4; holdout wins",
                "created": time.time()}
    freeze_manifest(manifest_path, manifest)
    progress(stage="학습 데이터 고정 완료", **counts, download_bytes=budget.used)
    return manifest


def prepare(notify=lambda **kw: None, street_limit=4000, salsa_limit=1400):
    import fcntl
    TRAINING.mkdir(parents=True, exist_ok=True)
    with (TRAINING / "preparation.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError("다른 데이터 준비 프로세스가 실행 중입니다.") from error
        return _prepare(notify=notify, street_limit=street_limit, salsa_limit=salsa_limit)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", required=True)
    args = parser.parse_args()
    result = prepare(notify=lambda **kw: print(json.dumps(kw, ensure_ascii=False), flush=True))
    print(json.dumps(result["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
