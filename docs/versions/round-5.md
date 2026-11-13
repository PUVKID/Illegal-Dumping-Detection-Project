<div align="center">

<a name="-5차"></a>
# 5차

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>
<!-- reading-levels:start -->
[LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

프로젝트 전체의 설명은 [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)부터 [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)까지 같은 범위로 연결됩니다.

<a id="reading-level-1"></a>
## LEVEL 1 - Beginner

### LEVEL 1 · 이 자료가 하는 일과 달라진 점

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

### LEVEL 1 · 실제 동작을 따라 읽기

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

CLI는 명령어와 옵션을 입력해 프로그램을 실행하는 방식입니다.

입력 — 쓰레기 영상·라벨·모델·선택한 차수 설정

처리 — 자료 준비·모델/영상 처리·평가 또는 상태 표시

출력 — 탐지 후보·평가 지표·화면·보고서

### LEVEL 1 · 준비하고 확인할 것

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 1 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [build_exe.py](../../5%EC%B0%A8/build_exe.py)<br>**정의된 옵션 이름:** `--build` |
| **진입 소스:** [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |
| **진입 소스:** [launcher.py](../../5%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |
| **진입 소스:** [pipeline.py](../../5%EC%B0%A8/pipeline.py)<br>**정의된 옵션 이름:** `--action`, `--params` |
| **진입 소스:** [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)<br>**정의된 옵션 이름:** `--prepare` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 1 · [build_exe.py](../../5%EC%B0%A8/build_exe.py)


| 내용 |
| --- |
| **설정·옵션:** [`--build`](../../5%EC%B0%A8/build_exe.py#L13)<br>**코드의 선언:** `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 내용 |
| --- |
| **거부 조건:** [`not available`](../../5%EC%B0%A8/build_exe.py#L19)<br>**오류 메시지:** 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

#### LEVEL 1 · [dashboard.py](../../5%EC%B0%A8/dashboard.py)


**설정·옵션:** [`LOG_LIMIT`](../../5%EC%B0%A8/dashboard.py#L14)

**코드의 선언:** `정의=64 * 1024`

**설정·옵션:** [`MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L15)

**코드의 선언:** `정의=4 * 1024**3`

**설정·옵션:** [`VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L16)

**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm'}`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/dashboard.py#L17)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent`


**거부 조건:** [`not isinstance(value, dict) or not isinstance(value.get('ok'), bool)`](../../5%EC%B0%A8/dashboard.py#L50)

**오류 메시지:** 파이프라인 JSON 응답 형식이 잘못되었습니다.

**거부 조건:** [`not isinstance(value, str) or not value`](../../5%EC%B0%A8/dashboard.py#L57)

**오류 메시지:** 파일 경로가 필요합니다.

**거부 조건:** [`not any(path.is_relative_to((self.work / area).resolve()) for area in areas)`](../../5%EC%B0%A8/dashboard.py#L63)

**오류 메시지:** 허용된 작업 폴더 밖의 경로입니다.

**거부 조건:** [`not path.is_file()`](../../5%EC%B0%A8/dashboard.py#L65)

**오류 메시지:** 파일이 없습니다.

**거부 조건:** [`path.suffix.lower() not in ('.log', '.txt')`](../../5%EC%B0%A8/dashboard.py#L71)

**오류 메시지:** 로그 파일만 읽을 수 있습니다.

**거부 조건:** [`size &gt; 2 * 1024**2`](../../5%EC%B0%A8/dashboard.py#L39)

**오류 메시지:** 파이프라인 JSON 응답이 2MB 상한을 넘었습니다.

**거부 조건:** [`self.headers.get('Transfer-Encoding')`](../../5%EC%B0%A8/dashboard.py#L201)

**오류 메시지:** Content-Length가 있는 요청만 허용합니다.

**거부 조건:** [`not 0 &lt; length &lt;= 64 * 1024`](../../5%EC%B0%A8/dashboard.py#L226)

**오류 메시지:** JSON 요청은 64KB 이하이어야 합니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/dashboard.py#L229)

**오류 메시지:** JSON 객체가 필요합니다.

**거부 조건:** [`not 0 &lt; length &lt;= MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L206)

**오류 메시지:** 영상은 0 초과 4GB 이하만 업로드할 수 있습니다.

**거부 조건:** [`suffix not in VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L209)

**오류 메시지:** 지원하지 않는 영상 확장자입니다.

**거부 조건:** [`not chunk`](../../5%EC%B0%A8/dashboard.py#L217)

**오류 메시지:** 영상 업로드가 중단되었습니다.


#### LEVEL 1 · [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/gpu_worker.py#L223)

**코드의 선언:** ``

**설정·옵션:** [`--params`](../../5%EC%B0%A8/gpu_worker.py#L224)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`--worker`](../../5%EC%B0%A8/gpu_worker.py#L225)

**코드의 선언:** ``

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/gpu_worker.py#L17)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/gpu_worker.py#L18)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/gpu_worker.py#L19)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/gpu_worker.py#L20)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`OLD_APP`](../../5%EC%B0%A8/gpu_worker.py#L21)

**코드의 선언:** `정의=PROJECT / "최종/3차/클린뷰"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/gpu_worker.py#L22)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`


**거부 조건:** [`not any(path.is_relative_to(p.resolve()) for p in VIDEO_ROOTS)`](../../5%EC%B0%A8/gpu_worker.py#L50)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`path.suffix.lower() not in {".mp4", ".avi", ".mov", ".mkv", ".m4v"} or not path.is_file() or not path.stat().st_size`](../../5%EC%B0%A8/gpu_worker.py#L52)

**오류 메시지:** 유효한 영상을 선택하세요.

**거부 조건:** [`not final`](../../5%EC%B0%A8/gpu_worker.py#L83)

**오류 메시지:** 보존된 final.json이 없습니다.

**거부 조건:** [`not all(Path(p).is_file() for p in weights)`](../../5%EC%B0%A8/gpu_worker.py#L87)

**오류 메시지:** 보존된 학습 모델을 찾을 수 없습니다.

**거부 조건:** [`model_root not in permitted`](../../5%EC%B0%A8/gpu_worker.py#L176)

**오류 메시지:** 선택 모델의 저장 위치가 허용되지 않습니다.

**거부 조건:** [`type(size) is not int or not 640 &lt;= size &lt;= 2048`](../../5%EC%B0%A8/gpu_worker.py#L200)

**오류 메시지:** 선택 모델의 추론 해상도가 올바르지 않습니다.

**거부 조건:** [`not ok or frame is None or not math.isfinite(fps) or fps &lt;= 0`](../../5%EC%B0%A8/gpu_worker.py#L66)

**오류 메시지:** 영상을 읽을 수 없습니다. 파일과 코덱을 확인하세요.

**거부 조건:** [`not cv2.imwrite(str(out), frame)`](../../5%EC%B0%A8/gpu_worker.py#L70)

**오류 메시지:** 영상 미리보기를 저장하지 못했습니다.

**거부 조건:** [`set(params) - {"path", "seconds", "abandon", "leave", "baseline"}`](../../5%EC%B0%A8/gpu_worker.py#L135)

**오류 메시지:** 지원하지 않는 탐지 설정입니다.

**거부 조건:** [`job.get("pid") and is_alive(job["pid"], job["id"])`](../../5%EC%B0%A8/gpu_worker.py#L131)

**오류 메시지:** GPU 작업이 이미 진행 중입니다. 완료 후 실행하세요.

**거부 조건:** [`not math.isfinite(number) or not low &lt;= number &lt;= high`](../../5%EC%B0%A8/gpu_worker.py#L140)

**오류 메시지:** 탐지 설정 범위를 확인하세요.

**거부 조건:** [`not isinstance(params.get("resume", False), bool)`](../../5%EC%B0%A8/gpu_worker.py#L144)

**오류 메시지:** 재개 설정은 true 또는 false여야 합니다.

**거부 조건:** [`(WORK / "training/final.json").exists()`](../../5%EC%B0%A8/gpu_worker.py#L146)

**오류 메시지:** 이 실험은 이미 완료됐습니다. 결과를 보존하며 자동 재학습하지 않습니다.

**거부 조건:** [`not (ROOT / "train_pipeline.py").is_file()`](../../5%EC%B0%A8/gpu_worker.py#L148)

**오류 메시지:** 학습 구성을 준비 중입니다.

**거부 조건:** [`set(params) - {"resume"}`](../../5%EC%B0%A8/gpu_worker.py#L150)

**오류 메시지:** 지원하지 않는 학습 설정입니다.


#### LEVEL 1 · [launcher.py](../../5%EC%B0%A8/launcher.py)


| 내용 |
| --- |
| **설정·옵션:** [`--no-browser`](../../5%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../5%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../5%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../5%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 내용 |
| --- |
| **거부 조건:** [`response.status != 200`](../../5%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

#### LEVEL 1 · [pipeline.py](../../5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/pipeline.py#L183)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../5%EC%B0%A8/pipeline.py#L184)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/pipeline.py#L162)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../5%EC%B0%A8/pipeline.py#L175)

**오류 메시지:** 지원하지 않는 작업입니다.


#### LEVEL 1 · [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../5%EC%B0%A8/prepare_training.py#L552)<br>**코드의 선언:** `action="store_true"; required=True` |
| **설정·옵션:** [`ROOT`](../../5%EC%B0%A8/prepare_training.py#L22)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/prepare_training.py#L23)<br>**코드의 선언:** `정의=ROOT.parent / "이전 도커 실험/3차실험/trash_round3"` |
| **설정·옵션:** [`TRAINING`](../../5%EC%B0%A8/prepare_training.py#L24)<br>**코드의 선언:** `정의=ROOT / "work/training"` |
| **설정·옵션:** [`SEED`](../../5%EC%B0%A8/prepare_training.py#L25)<br>**코드의 선언:** `정의=20261028` |
| **설정·옵션:** [`MAX_BYTES`](../../5%EC%B0%A8/prepare_training.py#L26)<br>**코드의 선언:** `정의=20 * 1024 ** 3` |
| **설정·옵션:** [`STREET_SIZE`](../../5%EC%B0%A8/prepare_training.py#L28)<br>**코드의 선언:** `정의=13728630001` |
| **설정·옵션:** [`_ERROR_LOCK`](../../5%EC%B0%A8/prepare_training.py#L29)<br>**코드의 선언:** `정의=threading.Lock()` |

**거부 조건:** [`not all(math.isfinite(n) and n &gt; 0 for n in (width, height))`](../../5%EC%B0%A8/prepare_training.py#L72)

**오류 메시지:** 이미지 크기가 올바르지 않습니다.

**거부 조건:** [`not url.startswith("https://") and not url.startswith("http://127.0.0.1:")`](../../5%EC%B0%A8/prepare_training.py#L193)

**오류 메시지:** HTTPS 데이터 출처만 허용됩니다.

**거부 조건:** [`length &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L207)

**오류 메시지:** 원본 크기가 올바르지 않습니다.

**거부 조건:** [`start &gt; length`](../../5%EC%B0%A8/prepare_training.py#L214)

**오류 메시지:** 부분 다운로드가 원본 크기보다 큽니다.

**거부 조건:** [`partial.stat().st_size != length`](../../5%EC%B0%A8/prepare_training.py#L236)

**오류 메시지:** 다운로드가 완성되지 않았습니다.

**거부 조건:** [`start &lt; 0 or end &lt; start or end - start &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L271)

**오류 메시지:** 허용 범위를 넘는 ZIP 부분 요청입니다.

**거부 조건:** [`len(data) != end - start + 1`](../../5%EC%B0%A8/prepare_training.py#L290)

**오류 메시지:** ZIP 부분 응답 크기가 다릅니다.

**거부 조건:** [`info.file_size &gt; 32 * 1024 ** 2 or info.compress_size &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L296)

**오류 메시지:** 과도한 단일 이미지 크기입니다.

**거부 조건:** [`header[:4] != b"PK\x03\x04"`](../../5%EC%B0%A8/prepare_training.py#L299)

**오류 메시지:** ZIP 지역 헤더가 올바르지 않습니다.

**거부 조건:** [`len(data) != info.file_size or zlib.crc32(data) & 0xffffffff != info.CRC`](../../5%EC%B0%A8/prepare_training.py#L313)

**오류 메시지:** ZIP 이미지 CRC가 일치하지 않습니다.

**거부 조건:** [`shutil.disk_usage(training).free &lt; 25 * 1024 ** 3`](../../5%EC%B0%A8/prepare_training.py#L367)

**오류 메시지:** 데이터 준비와 학습을 위한 여유 공간 25GB가 필요합니다.

**거부 조건:** [`len(accepted) &lt; 500`](../../5%EC%B0%A8/prepare_training.py#L513)

**오류 메시지:** 중복 배제 후 추가 학습 이미지가 500개 미만입니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(math.isfinite(n) for n in row)`](../../5%EC%B0%A8/prepare_training.py#L58)

**오류 메시지:** 단일 trash 클래스와 유한한 YOLO 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x - width / 2 and x + width / 2 &lt;= 1 + tolerance                                                            and -tolerance &lt;= y - height / 2 and y + height / 2 &lt;= 1 + tolerance)`](../../5%EC%B0%A8/prepare_training.py#L63)

**오류 메시지:** 라벨 상자가 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(math.isfinite(n) for n in (x, y, w, h)) or w &lt;= 0 or h &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L77)

**오류 메시지:** COCO 상자의 크기가 올바르지 않습니다.

**거부 조건:** [`right &lt;= left or bottom &lt;= top`](../../5%EC%B0%A8/prepare_training.py#L80)

**오류 메시지:** 이미지와 겹치지 않는 COCO 상자입니다.

**거부 조건:** [`not match`](../../5%EC%B0%A8/prepare_training.py#L103)

**오류 메시지:** 과거 pLitterStreet 자료의 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`digest != expected_md5`](../../5%EC%B0%A8/prepare_training.py#L240)

**오류 메시지:** 공식 MD5와 다운로드가 일치하지 않습니다.

**거부 조건:** [`decoder.unconsumed_tail or not decoder.eof`](../../5%EC%B0%A8/prepare_training.py#L307)

**오류 메시지:** ZIP 압축 해제 크기가 선언과 다릅니다.

**거부 조건:** [`load(path) != value`](../../5%EC%B0%A8/prepare_training.py#L321)

**오류 메시지:** 고정 데이터 명세를 현재 값으로 바꿀 수 없습니다.

**거부 조건:** [`manifest["sources_sha256"] != sha256_file(ROOT / "sources.json")`](../../5%EC%B0%A8/prepare_training.py#L362)

**오류 메시지:** 고정 명세 작성 뒤 데이터 출처 정책이 바뀌었습니다.

**거부 조건:** [`image.width &lt; 16 or image.height &lt; 16 or image.width * image.height &gt; 100000000`](../../5%EC%B0%A8/prepare_training.py#L125)

**오류 메시지:** 허용 범위 밖의 이미지 크기입니다.

**거부 조건:** [`count &lt; 0 or self.used + self.reserved + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L169)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`self.reserved &lt; 0`](../../5%EC%B0%A8/prepare_training.py#L176)

**오류 메시지:** 전송 예약량이 음수가 됐습니다.

**거부 조건:** [`count &lt; 0 or self.used + (0 if reserved else self.reserved) + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L181)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/")`](../../5%EC%B0%A8/prepare_training.py#L278)

**오류 메시지:** 서버가 정확한 ZIP 부분 요청을 지원하지 않습니다.

**거부 조건:** [`info["width"] != image["width"] or info["height"] != image["height"]`](../../5%EC%B0%A8/prepare_training.py#L453)

**오류 메시지:** COCO와 원본 이미지 크기가 다릅니다.

**거부 조건:** [`(info["width"], info["height"]) != (image["width"], image["height"])`](../../5%EC%B0%A8/prepare_training.py#L497)

**오류 메시지:** SALSA 라벨과 이미지 크기가 다릅니다.

**거부 조건:** [`count &gt; self.reserved`](../../5%EC%B0%A8/prepare_training.py#L184)

**오류 메시지:** 전송 예약보다 수신량이 큽니다.

**거부 조건:** [`start and (response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-"))`](../../5%EC%B0%A8/prepare_training.py#L222)

**오류 메시지:** 서버가 재개 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`int(response.headers.get("Content-Length", remaining)) != remaining`](../../5%EC%B0%A8/prepare_training.py#L224)

**오류 메시지:** 원본과 실제 전송 크기가 다릅니다.

**거부 조건:** [`not receipt.exists() or load(receipt)["sha256"] != sha256_file(destination)`](../../5%EC%B0%A8/prepare_training.py#L441)

**오류 메시지:** 기존 다운로드의 보존 해시가 없거나 다릅니다.

**거부 조건:** [`consecutive_failures &gt;= 3`](../../5%EC%B0%A8/prepare_training.py#L475)

**오류 메시지:** 이미지 확보가 연속 3개 실패했습니다. 원인을 확인한 뒤 재개하세요.


#### LEVEL 1 · [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`THRESHOLDS`](../../5%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의=[.05, .1, .15, .17, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .9]`


**거부 조건:** [`not choices`](../../5%EC%B0%A8/train_pipeline.py#L24)

**오류 메시지:** 선택할 검증 임계값이 없습니다.

**거부 조건:** [`not results`](../../5%EC%B0%A8/train_pipeline.py#L30)

**오류 메시지:** 비교할 검증 결과가 없습니다.

**거부 조건:** [`saved.exists() and load(saved) != contract`](../../5%EC%B0%A8/train_pipeline.py#L40)

**오류 메시지:** checkpoint의 데이터·학습 조건이 현재 명세와 다릅니다.

**거부 조건:** [`any(len(model.names) != 1 or model.names[0] != "trash" for model in models)`](../../5%EC%B0%A8/train_pipeline.py#L111)

**오류 메시지:** 단일 trash 클래스 가중치가 아닙니다.

**거부 조건:** [`sha256_file(best) != load(directory / "phase_complete.json")["best_sha256"]`](../../5%EC%B0%A8/train_pipeline.py#L220)

**오류 메시지:** 완료 학습 모델이 기록된 해시와 다릅니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L43)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L47)

**오류 메시지:** 원래 계약 없는 checkpoint는 자동 재개할 수 없습니다.

**거부 조건:** [`not allow_resume`](../../5%EC%B0%A8/train_pipeline.py#L49)

**오류 메시지:** 중단 checkpoint가 있습니다. 재개를 명시적으로 선택하세요.

**거부 조건:** [`not best.is_file()`](../../5%EC%B0%A8/train_pipeline.py#L216)

**오류 메시지:** 완료 학습 가중치가 없습니다.


</details>

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

### LEVEL 1 · 결과와 주의할 범위

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


[자료 폴더](../../5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/final-to-5.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-2"></a>
## LEVEL 2 - Explorer

### LEVEL 2 · 목적과 구성의 연결

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

### LEVEL 2 · 입력에서 출력으로

**단계:** 입력

**내용:** 쓰레기 영상·라벨·모델·선택한 차수 설정

**단계:** 처리

**내용:** 자료 준비·모델/영상 처리·평가 또는 상태 표시

**단계:** 출력

**내용:** 탐지 후보·평가 지표·화면·보고서


입력·처리·출력은 위의 같은 자료 흐름을 다른 단계에서 읽는 기준입니다. 처리 조건과 출력의 의미를 함께 확인합니다.

### LEVEL 2 · 설정과 처리 순서의 관계

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 2 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [build_exe.py](../../5%EC%B0%A8/build_exe.py)<br>**정의된 옵션 이름:** `--build` |
| **진입 소스:** [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |
| **진입 소스:** [launcher.py](../../5%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |
| **진입 소스:** [pipeline.py](../../5%EC%B0%A8/pipeline.py)<br>**정의된 옵션 이름:** `--action`, `--params` |
| **진입 소스:** [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)<br>**정의된 옵션 이름:** `--prepare` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 2 · [build_exe.py](../../5%EC%B0%A8/build_exe.py)


| 내용 |
| --- |
| **설정·옵션:** [`--build`](../../5%EC%B0%A8/build_exe.py#L13)<br>**코드의 선언:** `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 내용 |
| --- |
| **거부 조건:** [`not available`](../../5%EC%B0%A8/build_exe.py#L19)<br>**오류 메시지:** 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

#### LEVEL 2 · [dashboard.py](../../5%EC%B0%A8/dashboard.py)


**설정·옵션:** [`LOG_LIMIT`](../../5%EC%B0%A8/dashboard.py#L14)

**코드의 선언:** `정의=64 * 1024`

**설정·옵션:** [`MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L15)

**코드의 선언:** `정의=4 * 1024**3`

**설정·옵션:** [`VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L16)

**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm'}`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/dashboard.py#L17)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent`


**거부 조건:** [`not isinstance(value, dict) or not isinstance(value.get('ok'), bool)`](../../5%EC%B0%A8/dashboard.py#L50)

**오류 메시지:** 파이프라인 JSON 응답 형식이 잘못되었습니다.

**거부 조건:** [`not isinstance(value, str) or not value`](../../5%EC%B0%A8/dashboard.py#L57)

**오류 메시지:** 파일 경로가 필요합니다.

**거부 조건:** [`not any(path.is_relative_to((self.work / area).resolve()) for area in areas)`](../../5%EC%B0%A8/dashboard.py#L63)

**오류 메시지:** 허용된 작업 폴더 밖의 경로입니다.

**거부 조건:** [`not path.is_file()`](../../5%EC%B0%A8/dashboard.py#L65)

**오류 메시지:** 파일이 없습니다.

**거부 조건:** [`path.suffix.lower() not in ('.log', '.txt')`](../../5%EC%B0%A8/dashboard.py#L71)

**오류 메시지:** 로그 파일만 읽을 수 있습니다.

**거부 조건:** [`size &gt; 2 * 1024**2`](../../5%EC%B0%A8/dashboard.py#L39)

**오류 메시지:** 파이프라인 JSON 응답이 2MB 상한을 넘었습니다.

**거부 조건:** [`self.headers.get('Transfer-Encoding')`](../../5%EC%B0%A8/dashboard.py#L201)

**오류 메시지:** Content-Length가 있는 요청만 허용합니다.

**거부 조건:** [`not 0 &lt; length &lt;= 64 * 1024`](../../5%EC%B0%A8/dashboard.py#L226)

**오류 메시지:** JSON 요청은 64KB 이하이어야 합니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/dashboard.py#L229)

**오류 메시지:** JSON 객체가 필요합니다.

**거부 조건:** [`not 0 &lt; length &lt;= MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L206)

**오류 메시지:** 영상은 0 초과 4GB 이하만 업로드할 수 있습니다.

**거부 조건:** [`suffix not in VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L209)

**오류 메시지:** 지원하지 않는 영상 확장자입니다.

**거부 조건:** [`not chunk`](../../5%EC%B0%A8/dashboard.py#L217)

**오류 메시지:** 영상 업로드가 중단되었습니다.


#### LEVEL 2 · [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/gpu_worker.py#L223)

**코드의 선언:** ``

**설정·옵션:** [`--params`](../../5%EC%B0%A8/gpu_worker.py#L224)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`--worker`](../../5%EC%B0%A8/gpu_worker.py#L225)

**코드의 선언:** ``

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/gpu_worker.py#L17)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/gpu_worker.py#L18)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/gpu_worker.py#L19)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/gpu_worker.py#L20)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`OLD_APP`](../../5%EC%B0%A8/gpu_worker.py#L21)

**코드의 선언:** `정의=PROJECT / "최종/3차/클린뷰"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/gpu_worker.py#L22)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`


**거부 조건:** [`not any(path.is_relative_to(p.resolve()) for p in VIDEO_ROOTS)`](../../5%EC%B0%A8/gpu_worker.py#L50)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`path.suffix.lower() not in {".mp4", ".avi", ".mov", ".mkv", ".m4v"} or not path.is_file() or not path.stat().st_size`](../../5%EC%B0%A8/gpu_worker.py#L52)

**오류 메시지:** 유효한 영상을 선택하세요.

**거부 조건:** [`not final`](../../5%EC%B0%A8/gpu_worker.py#L83)

**오류 메시지:** 보존된 final.json이 없습니다.

**거부 조건:** [`not all(Path(p).is_file() for p in weights)`](../../5%EC%B0%A8/gpu_worker.py#L87)

**오류 메시지:** 보존된 학습 모델을 찾을 수 없습니다.

**거부 조건:** [`model_root not in permitted`](../../5%EC%B0%A8/gpu_worker.py#L176)

**오류 메시지:** 선택 모델의 저장 위치가 허용되지 않습니다.

**거부 조건:** [`type(size) is not int or not 640 &lt;= size &lt;= 2048`](../../5%EC%B0%A8/gpu_worker.py#L200)

**오류 메시지:** 선택 모델의 추론 해상도가 올바르지 않습니다.

**거부 조건:** [`not ok or frame is None or not math.isfinite(fps) or fps &lt;= 0`](../../5%EC%B0%A8/gpu_worker.py#L66)

**오류 메시지:** 영상을 읽을 수 없습니다. 파일과 코덱을 확인하세요.

**거부 조건:** [`not cv2.imwrite(str(out), frame)`](../../5%EC%B0%A8/gpu_worker.py#L70)

**오류 메시지:** 영상 미리보기를 저장하지 못했습니다.

**거부 조건:** [`set(params) - {"path", "seconds", "abandon", "leave", "baseline"}`](../../5%EC%B0%A8/gpu_worker.py#L135)

**오류 메시지:** 지원하지 않는 탐지 설정입니다.

**거부 조건:** [`job.get("pid") and is_alive(job["pid"], job["id"])`](../../5%EC%B0%A8/gpu_worker.py#L131)

**오류 메시지:** GPU 작업이 이미 진행 중입니다. 완료 후 실행하세요.

**거부 조건:** [`not math.isfinite(number) or not low &lt;= number &lt;= high`](../../5%EC%B0%A8/gpu_worker.py#L140)

**오류 메시지:** 탐지 설정 범위를 확인하세요.

**거부 조건:** [`not isinstance(params.get("resume", False), bool)`](../../5%EC%B0%A8/gpu_worker.py#L144)

**오류 메시지:** 재개 설정은 true 또는 false여야 합니다.

**거부 조건:** [`(WORK / "training/final.json").exists()`](../../5%EC%B0%A8/gpu_worker.py#L146)

**오류 메시지:** 이 실험은 이미 완료됐습니다. 결과를 보존하며 자동 재학습하지 않습니다.

**거부 조건:** [`not (ROOT / "train_pipeline.py").is_file()`](../../5%EC%B0%A8/gpu_worker.py#L148)

**오류 메시지:** 학습 구성을 준비 중입니다.

**거부 조건:** [`set(params) - {"resume"}`](../../5%EC%B0%A8/gpu_worker.py#L150)

**오류 메시지:** 지원하지 않는 학습 설정입니다.


#### LEVEL 2 · [launcher.py](../../5%EC%B0%A8/launcher.py)


| 내용 |
| --- |
| **설정·옵션:** [`--no-browser`](../../5%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../5%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../5%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../5%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 내용 |
| --- |
| **거부 조건:** [`response.status != 200`](../../5%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

#### LEVEL 2 · [pipeline.py](../../5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/pipeline.py#L183)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../5%EC%B0%A8/pipeline.py#L184)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/pipeline.py#L162)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../5%EC%B0%A8/pipeline.py#L175)

**오류 메시지:** 지원하지 않는 작업입니다.


#### LEVEL 2 · [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../5%EC%B0%A8/prepare_training.py#L552)<br>**코드의 선언:** `action="store_true"; required=True` |
| **설정·옵션:** [`ROOT`](../../5%EC%B0%A8/prepare_training.py#L22)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/prepare_training.py#L23)<br>**코드의 선언:** `정의=ROOT.parent / "이전 도커 실험/3차실험/trash_round3"` |
| **설정·옵션:** [`TRAINING`](../../5%EC%B0%A8/prepare_training.py#L24)<br>**코드의 선언:** `정의=ROOT / "work/training"` |
| **설정·옵션:** [`SEED`](../../5%EC%B0%A8/prepare_training.py#L25)<br>**코드의 선언:** `정의=20261028` |
| **설정·옵션:** [`MAX_BYTES`](../../5%EC%B0%A8/prepare_training.py#L26)<br>**코드의 선언:** `정의=20 * 1024 ** 3` |
| **설정·옵션:** [`STREET_SIZE`](../../5%EC%B0%A8/prepare_training.py#L28)<br>**코드의 선언:** `정의=13728630001` |
| **설정·옵션:** [`_ERROR_LOCK`](../../5%EC%B0%A8/prepare_training.py#L29)<br>**코드의 선언:** `정의=threading.Lock()` |

**거부 조건:** [`not all(math.isfinite(n) and n &gt; 0 for n in (width, height))`](../../5%EC%B0%A8/prepare_training.py#L72)

**오류 메시지:** 이미지 크기가 올바르지 않습니다.

**거부 조건:** [`not url.startswith("https://") and not url.startswith("http://127.0.0.1:")`](../../5%EC%B0%A8/prepare_training.py#L193)

**오류 메시지:** HTTPS 데이터 출처만 허용됩니다.

**거부 조건:** [`length &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L207)

**오류 메시지:** 원본 크기가 올바르지 않습니다.

**거부 조건:** [`start &gt; length`](../../5%EC%B0%A8/prepare_training.py#L214)

**오류 메시지:** 부분 다운로드가 원본 크기보다 큽니다.

**거부 조건:** [`partial.stat().st_size != length`](../../5%EC%B0%A8/prepare_training.py#L236)

**오류 메시지:** 다운로드가 완성되지 않았습니다.

**거부 조건:** [`start &lt; 0 or end &lt; start or end - start &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L271)

**오류 메시지:** 허용 범위를 넘는 ZIP 부분 요청입니다.

**거부 조건:** [`len(data) != end - start + 1`](../../5%EC%B0%A8/prepare_training.py#L290)

**오류 메시지:** ZIP 부분 응답 크기가 다릅니다.

**거부 조건:** [`info.file_size &gt; 32 * 1024 ** 2 or info.compress_size &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L296)

**오류 메시지:** 과도한 단일 이미지 크기입니다.

**거부 조건:** [`header[:4] != b"PK\x03\x04"`](../../5%EC%B0%A8/prepare_training.py#L299)

**오류 메시지:** ZIP 지역 헤더가 올바르지 않습니다.

**거부 조건:** [`len(data) != info.file_size or zlib.crc32(data) & 0xffffffff != info.CRC`](../../5%EC%B0%A8/prepare_training.py#L313)

**오류 메시지:** ZIP 이미지 CRC가 일치하지 않습니다.

**거부 조건:** [`shutil.disk_usage(training).free &lt; 25 * 1024 ** 3`](../../5%EC%B0%A8/prepare_training.py#L367)

**오류 메시지:** 데이터 준비와 학습을 위한 여유 공간 25GB가 필요합니다.

**거부 조건:** [`len(accepted) &lt; 500`](../../5%EC%B0%A8/prepare_training.py#L513)

**오류 메시지:** 중복 배제 후 추가 학습 이미지가 500개 미만입니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(math.isfinite(n) for n in row)`](../../5%EC%B0%A8/prepare_training.py#L58)

**오류 메시지:** 단일 trash 클래스와 유한한 YOLO 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x - width / 2 and x + width / 2 &lt;= 1 + tolerance                                                            and -tolerance &lt;= y - height / 2 and y + height / 2 &lt;= 1 + tolerance)`](../../5%EC%B0%A8/prepare_training.py#L63)

**오류 메시지:** 라벨 상자가 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(math.isfinite(n) for n in (x, y, w, h)) or w &lt;= 0 or h &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L77)

**오류 메시지:** COCO 상자의 크기가 올바르지 않습니다.

**거부 조건:** [`right &lt;= left or bottom &lt;= top`](../../5%EC%B0%A8/prepare_training.py#L80)

**오류 메시지:** 이미지와 겹치지 않는 COCO 상자입니다.

**거부 조건:** [`not match`](../../5%EC%B0%A8/prepare_training.py#L103)

**오류 메시지:** 과거 pLitterStreet 자료의 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`digest != expected_md5`](../../5%EC%B0%A8/prepare_training.py#L240)

**오류 메시지:** 공식 MD5와 다운로드가 일치하지 않습니다.

**거부 조건:** [`decoder.unconsumed_tail or not decoder.eof`](../../5%EC%B0%A8/prepare_training.py#L307)

**오류 메시지:** ZIP 압축 해제 크기가 선언과 다릅니다.

**거부 조건:** [`load(path) != value`](../../5%EC%B0%A8/prepare_training.py#L321)

**오류 메시지:** 고정 데이터 명세를 현재 값으로 바꿀 수 없습니다.

**거부 조건:** [`manifest["sources_sha256"] != sha256_file(ROOT / "sources.json")`](../../5%EC%B0%A8/prepare_training.py#L362)

**오류 메시지:** 고정 명세 작성 뒤 데이터 출처 정책이 바뀌었습니다.

**거부 조건:** [`image.width &lt; 16 or image.height &lt; 16 or image.width * image.height &gt; 100000000`](../../5%EC%B0%A8/prepare_training.py#L125)

**오류 메시지:** 허용 범위 밖의 이미지 크기입니다.

**거부 조건:** [`count &lt; 0 or self.used + self.reserved + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L169)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`self.reserved &lt; 0`](../../5%EC%B0%A8/prepare_training.py#L176)

**오류 메시지:** 전송 예약량이 음수가 됐습니다.

**거부 조건:** [`count &lt; 0 or self.used + (0 if reserved else self.reserved) + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L181)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/")`](../../5%EC%B0%A8/prepare_training.py#L278)

**오류 메시지:** 서버가 정확한 ZIP 부분 요청을 지원하지 않습니다.

**거부 조건:** [`info["width"] != image["width"] or info["height"] != image["height"]`](../../5%EC%B0%A8/prepare_training.py#L453)

**오류 메시지:** COCO와 원본 이미지 크기가 다릅니다.

**거부 조건:** [`(info["width"], info["height"]) != (image["width"], image["height"])`](../../5%EC%B0%A8/prepare_training.py#L497)

**오류 메시지:** SALSA 라벨과 이미지 크기가 다릅니다.

**거부 조건:** [`count &gt; self.reserved`](../../5%EC%B0%A8/prepare_training.py#L184)

**오류 메시지:** 전송 예약보다 수신량이 큽니다.

**거부 조건:** [`start and (response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-"))`](../../5%EC%B0%A8/prepare_training.py#L222)

**오류 메시지:** 서버가 재개 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`int(response.headers.get("Content-Length", remaining)) != remaining`](../../5%EC%B0%A8/prepare_training.py#L224)

**오류 메시지:** 원본과 실제 전송 크기가 다릅니다.

**거부 조건:** [`not receipt.exists() or load(receipt)["sha256"] != sha256_file(destination)`](../../5%EC%B0%A8/prepare_training.py#L441)

**오류 메시지:** 기존 다운로드의 보존 해시가 없거나 다릅니다.

**거부 조건:** [`consecutive_failures &gt;= 3`](../../5%EC%B0%A8/prepare_training.py#L475)

**오류 메시지:** 이미지 확보가 연속 3개 실패했습니다. 원인을 확인한 뒤 재개하세요.


#### LEVEL 2 · [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`THRESHOLDS`](../../5%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의=[.05, .1, .15, .17, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .9]`


**거부 조건:** [`not choices`](../../5%EC%B0%A8/train_pipeline.py#L24)

**오류 메시지:** 선택할 검증 임계값이 없습니다.

**거부 조건:** [`not results`](../../5%EC%B0%A8/train_pipeline.py#L30)

**오류 메시지:** 비교할 검증 결과가 없습니다.

**거부 조건:** [`saved.exists() and load(saved) != contract`](../../5%EC%B0%A8/train_pipeline.py#L40)

**오류 메시지:** checkpoint의 데이터·학습 조건이 현재 명세와 다릅니다.

**거부 조건:** [`any(len(model.names) != 1 or model.names[0] != "trash" for model in models)`](../../5%EC%B0%A8/train_pipeline.py#L111)

**오류 메시지:** 단일 trash 클래스 가중치가 아닙니다.

**거부 조건:** [`sha256_file(best) != load(directory / "phase_complete.json")["best_sha256"]`](../../5%EC%B0%A8/train_pipeline.py#L220)

**오류 메시지:** 완료 학습 모델이 기록된 해시와 다릅니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L43)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L47)

**오류 메시지:** 원래 계약 없는 checkpoint는 자동 재개할 수 없습니다.

**거부 조건:** [`not allow_resume`](../../5%EC%B0%A8/train_pipeline.py#L49)

**오류 메시지:** 중단 checkpoint가 있습니다. 재개를 명시적으로 선택하세요.

**거부 조건:** [`not best.is_file()`](../../5%EC%B0%A8/train_pipeline.py#L216)

**오류 메시지:** 완료 학습 가중치가 없습니다.


</details>

### LEVEL 2 · 관측과 해석을 구분하기

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


[자료 폴더](../../5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/final-to-5.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-3"></a>
## LEVEL 3 - Practitioner

### LEVEL 3 · 이 차수를 준비하는 범위

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 3 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [build_exe.py](../../5%EC%B0%A8/build_exe.py)<br>**정의된 옵션 이름:** `--build` |
| **진입 소스:** [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |
| **진입 소스:** [launcher.py](../../5%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |
| **진입 소스:** [pipeline.py](../../5%EC%B0%A8/pipeline.py)<br>**정의된 옵션 이름:** `--action`, `--params` |
| **진입 소스:** [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)<br>**정의된 옵션 이름:** `--prepare` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 3 · [build_exe.py](../../5%EC%B0%A8/build_exe.py)


| 내용 |
| --- |
| **설정·옵션:** [`--build`](../../5%EC%B0%A8/build_exe.py#L13)<br>**코드의 선언:** `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 내용 |
| --- |
| **거부 조건:** [`not available`](../../5%EC%B0%A8/build_exe.py#L19)<br>**오류 메시지:** 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

#### LEVEL 3 · [dashboard.py](../../5%EC%B0%A8/dashboard.py)


**설정·옵션:** [`LOG_LIMIT`](../../5%EC%B0%A8/dashboard.py#L14)

**코드의 선언:** `정의=64 * 1024`

**설정·옵션:** [`MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L15)

**코드의 선언:** `정의=4 * 1024**3`

**설정·옵션:** [`VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L16)

**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm'}`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/dashboard.py#L17)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent`


**거부 조건:** [`not isinstance(value, dict) or not isinstance(value.get('ok'), bool)`](../../5%EC%B0%A8/dashboard.py#L50)

**오류 메시지:** 파이프라인 JSON 응답 형식이 잘못되었습니다.

**거부 조건:** [`not isinstance(value, str) or not value`](../../5%EC%B0%A8/dashboard.py#L57)

**오류 메시지:** 파일 경로가 필요합니다.

**거부 조건:** [`not any(path.is_relative_to((self.work / area).resolve()) for area in areas)`](../../5%EC%B0%A8/dashboard.py#L63)

**오류 메시지:** 허용된 작업 폴더 밖의 경로입니다.

**거부 조건:** [`not path.is_file()`](../../5%EC%B0%A8/dashboard.py#L65)

**오류 메시지:** 파일이 없습니다.

**거부 조건:** [`path.suffix.lower() not in ('.log', '.txt')`](../../5%EC%B0%A8/dashboard.py#L71)

**오류 메시지:** 로그 파일만 읽을 수 있습니다.

**거부 조건:** [`size &gt; 2 * 1024**2`](../../5%EC%B0%A8/dashboard.py#L39)

**오류 메시지:** 파이프라인 JSON 응답이 2MB 상한을 넘었습니다.

**거부 조건:** [`self.headers.get('Transfer-Encoding')`](../../5%EC%B0%A8/dashboard.py#L201)

**오류 메시지:** Content-Length가 있는 요청만 허용합니다.

**거부 조건:** [`not 0 &lt; length &lt;= 64 * 1024`](../../5%EC%B0%A8/dashboard.py#L226)

**오류 메시지:** JSON 요청은 64KB 이하이어야 합니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/dashboard.py#L229)

**오류 메시지:** JSON 객체가 필요합니다.

**거부 조건:** [`not 0 &lt; length &lt;= MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L206)

**오류 메시지:** 영상은 0 초과 4GB 이하만 업로드할 수 있습니다.

**거부 조건:** [`suffix not in VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L209)

**오류 메시지:** 지원하지 않는 영상 확장자입니다.

**거부 조건:** [`not chunk`](../../5%EC%B0%A8/dashboard.py#L217)

**오류 메시지:** 영상 업로드가 중단되었습니다.


#### LEVEL 3 · [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/gpu_worker.py#L223)

**코드의 선언:** ``

**설정·옵션:** [`--params`](../../5%EC%B0%A8/gpu_worker.py#L224)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`--worker`](../../5%EC%B0%A8/gpu_worker.py#L225)

**코드의 선언:** ``

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/gpu_worker.py#L17)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/gpu_worker.py#L18)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/gpu_worker.py#L19)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/gpu_worker.py#L20)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`OLD_APP`](../../5%EC%B0%A8/gpu_worker.py#L21)

**코드의 선언:** `정의=PROJECT / "최종/3차/클린뷰"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/gpu_worker.py#L22)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`


**거부 조건:** [`not any(path.is_relative_to(p.resolve()) for p in VIDEO_ROOTS)`](../../5%EC%B0%A8/gpu_worker.py#L50)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`path.suffix.lower() not in {".mp4", ".avi", ".mov", ".mkv", ".m4v"} or not path.is_file() or not path.stat().st_size`](../../5%EC%B0%A8/gpu_worker.py#L52)

**오류 메시지:** 유효한 영상을 선택하세요.

**거부 조건:** [`not final`](../../5%EC%B0%A8/gpu_worker.py#L83)

**오류 메시지:** 보존된 final.json이 없습니다.

**거부 조건:** [`not all(Path(p).is_file() for p in weights)`](../../5%EC%B0%A8/gpu_worker.py#L87)

**오류 메시지:** 보존된 학습 모델을 찾을 수 없습니다.

**거부 조건:** [`model_root not in permitted`](../../5%EC%B0%A8/gpu_worker.py#L176)

**오류 메시지:** 선택 모델의 저장 위치가 허용되지 않습니다.

**거부 조건:** [`type(size) is not int or not 640 &lt;= size &lt;= 2048`](../../5%EC%B0%A8/gpu_worker.py#L200)

**오류 메시지:** 선택 모델의 추론 해상도가 올바르지 않습니다.

**거부 조건:** [`not ok or frame is None or not math.isfinite(fps) or fps &lt;= 0`](../../5%EC%B0%A8/gpu_worker.py#L66)

**오류 메시지:** 영상을 읽을 수 없습니다. 파일과 코덱을 확인하세요.

**거부 조건:** [`not cv2.imwrite(str(out), frame)`](../../5%EC%B0%A8/gpu_worker.py#L70)

**오류 메시지:** 영상 미리보기를 저장하지 못했습니다.

**거부 조건:** [`set(params) - {"path", "seconds", "abandon", "leave", "baseline"}`](../../5%EC%B0%A8/gpu_worker.py#L135)

**오류 메시지:** 지원하지 않는 탐지 설정입니다.

**거부 조건:** [`job.get("pid") and is_alive(job["pid"], job["id"])`](../../5%EC%B0%A8/gpu_worker.py#L131)

**오류 메시지:** GPU 작업이 이미 진행 중입니다. 완료 후 실행하세요.

**거부 조건:** [`not math.isfinite(number) or not low &lt;= number &lt;= high`](../../5%EC%B0%A8/gpu_worker.py#L140)

**오류 메시지:** 탐지 설정 범위를 확인하세요.

**거부 조건:** [`not isinstance(params.get("resume", False), bool)`](../../5%EC%B0%A8/gpu_worker.py#L144)

**오류 메시지:** 재개 설정은 true 또는 false여야 합니다.

**거부 조건:** [`(WORK / "training/final.json").exists()`](../../5%EC%B0%A8/gpu_worker.py#L146)

**오류 메시지:** 이 실험은 이미 완료됐습니다. 결과를 보존하며 자동 재학습하지 않습니다.

**거부 조건:** [`not (ROOT / "train_pipeline.py").is_file()`](../../5%EC%B0%A8/gpu_worker.py#L148)

**오류 메시지:** 학습 구성을 준비 중입니다.

**거부 조건:** [`set(params) - {"resume"}`](../../5%EC%B0%A8/gpu_worker.py#L150)

**오류 메시지:** 지원하지 않는 학습 설정입니다.


#### LEVEL 3 · [launcher.py](../../5%EC%B0%A8/launcher.py)


| 내용 |
| --- |
| **설정·옵션:** [`--no-browser`](../../5%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../5%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../5%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../5%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 내용 |
| --- |
| **거부 조건:** [`response.status != 200`](../../5%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

#### LEVEL 3 · [pipeline.py](../../5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/pipeline.py#L183)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../5%EC%B0%A8/pipeline.py#L184)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/pipeline.py#L162)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../5%EC%B0%A8/pipeline.py#L175)

**오류 메시지:** 지원하지 않는 작업입니다.


#### LEVEL 3 · [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../5%EC%B0%A8/prepare_training.py#L552)<br>**코드의 선언:** `action="store_true"; required=True` |
| **설정·옵션:** [`ROOT`](../../5%EC%B0%A8/prepare_training.py#L22)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/prepare_training.py#L23)<br>**코드의 선언:** `정의=ROOT.parent / "이전 도커 실험/3차실험/trash_round3"` |
| **설정·옵션:** [`TRAINING`](../../5%EC%B0%A8/prepare_training.py#L24)<br>**코드의 선언:** `정의=ROOT / "work/training"` |
| **설정·옵션:** [`SEED`](../../5%EC%B0%A8/prepare_training.py#L25)<br>**코드의 선언:** `정의=20261028` |
| **설정·옵션:** [`MAX_BYTES`](../../5%EC%B0%A8/prepare_training.py#L26)<br>**코드의 선언:** `정의=20 * 1024 ** 3` |
| **설정·옵션:** [`STREET_SIZE`](../../5%EC%B0%A8/prepare_training.py#L28)<br>**코드의 선언:** `정의=13728630001` |
| **설정·옵션:** [`_ERROR_LOCK`](../../5%EC%B0%A8/prepare_training.py#L29)<br>**코드의 선언:** `정의=threading.Lock()` |

**거부 조건:** [`not all(math.isfinite(n) and n &gt; 0 for n in (width, height))`](../../5%EC%B0%A8/prepare_training.py#L72)

**오류 메시지:** 이미지 크기가 올바르지 않습니다.

**거부 조건:** [`not url.startswith("https://") and not url.startswith("http://127.0.0.1:")`](../../5%EC%B0%A8/prepare_training.py#L193)

**오류 메시지:** HTTPS 데이터 출처만 허용됩니다.

**거부 조건:** [`length &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L207)

**오류 메시지:** 원본 크기가 올바르지 않습니다.

**거부 조건:** [`start &gt; length`](../../5%EC%B0%A8/prepare_training.py#L214)

**오류 메시지:** 부분 다운로드가 원본 크기보다 큽니다.

**거부 조건:** [`partial.stat().st_size != length`](../../5%EC%B0%A8/prepare_training.py#L236)

**오류 메시지:** 다운로드가 완성되지 않았습니다.

**거부 조건:** [`start &lt; 0 or end &lt; start or end - start &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L271)

**오류 메시지:** 허용 범위를 넘는 ZIP 부분 요청입니다.

**거부 조건:** [`len(data) != end - start + 1`](../../5%EC%B0%A8/prepare_training.py#L290)

**오류 메시지:** ZIP 부분 응답 크기가 다릅니다.

**거부 조건:** [`info.file_size &gt; 32 * 1024 ** 2 or info.compress_size &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L296)

**오류 메시지:** 과도한 단일 이미지 크기입니다.

**거부 조건:** [`header[:4] != b"PK\x03\x04"`](../../5%EC%B0%A8/prepare_training.py#L299)

**오류 메시지:** ZIP 지역 헤더가 올바르지 않습니다.

**거부 조건:** [`len(data) != info.file_size or zlib.crc32(data) & 0xffffffff != info.CRC`](../../5%EC%B0%A8/prepare_training.py#L313)

**오류 메시지:** ZIP 이미지 CRC가 일치하지 않습니다.

**거부 조건:** [`shutil.disk_usage(training).free &lt; 25 * 1024 ** 3`](../../5%EC%B0%A8/prepare_training.py#L367)

**오류 메시지:** 데이터 준비와 학습을 위한 여유 공간 25GB가 필요합니다.

**거부 조건:** [`len(accepted) &lt; 500`](../../5%EC%B0%A8/prepare_training.py#L513)

**오류 메시지:** 중복 배제 후 추가 학습 이미지가 500개 미만입니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(math.isfinite(n) for n in row)`](../../5%EC%B0%A8/prepare_training.py#L58)

**오류 메시지:** 단일 trash 클래스와 유한한 YOLO 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x - width / 2 and x + width / 2 &lt;= 1 + tolerance                                                            and -tolerance &lt;= y - height / 2 and y + height / 2 &lt;= 1 + tolerance)`](../../5%EC%B0%A8/prepare_training.py#L63)

**오류 메시지:** 라벨 상자가 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(math.isfinite(n) for n in (x, y, w, h)) or w &lt;= 0 or h &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L77)

**오류 메시지:** COCO 상자의 크기가 올바르지 않습니다.

**거부 조건:** [`right &lt;= left or bottom &lt;= top`](../../5%EC%B0%A8/prepare_training.py#L80)

**오류 메시지:** 이미지와 겹치지 않는 COCO 상자입니다.

**거부 조건:** [`not match`](../../5%EC%B0%A8/prepare_training.py#L103)

**오류 메시지:** 과거 pLitterStreet 자료의 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`digest != expected_md5`](../../5%EC%B0%A8/prepare_training.py#L240)

**오류 메시지:** 공식 MD5와 다운로드가 일치하지 않습니다.

**거부 조건:** [`decoder.unconsumed_tail or not decoder.eof`](../../5%EC%B0%A8/prepare_training.py#L307)

**오류 메시지:** ZIP 압축 해제 크기가 선언과 다릅니다.

**거부 조건:** [`load(path) != value`](../../5%EC%B0%A8/prepare_training.py#L321)

**오류 메시지:** 고정 데이터 명세를 현재 값으로 바꿀 수 없습니다.

**거부 조건:** [`manifest["sources_sha256"] != sha256_file(ROOT / "sources.json")`](../../5%EC%B0%A8/prepare_training.py#L362)

**오류 메시지:** 고정 명세 작성 뒤 데이터 출처 정책이 바뀌었습니다.

**거부 조건:** [`image.width &lt; 16 or image.height &lt; 16 or image.width * image.height &gt; 100000000`](../../5%EC%B0%A8/prepare_training.py#L125)

**오류 메시지:** 허용 범위 밖의 이미지 크기입니다.

**거부 조건:** [`count &lt; 0 or self.used + self.reserved + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L169)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`self.reserved &lt; 0`](../../5%EC%B0%A8/prepare_training.py#L176)

**오류 메시지:** 전송 예약량이 음수가 됐습니다.

**거부 조건:** [`count &lt; 0 or self.used + (0 if reserved else self.reserved) + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L181)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/")`](../../5%EC%B0%A8/prepare_training.py#L278)

**오류 메시지:** 서버가 정확한 ZIP 부분 요청을 지원하지 않습니다.

**거부 조건:** [`info["width"] != image["width"] or info["height"] != image["height"]`](../../5%EC%B0%A8/prepare_training.py#L453)

**오류 메시지:** COCO와 원본 이미지 크기가 다릅니다.

**거부 조건:** [`(info["width"], info["height"]) != (image["width"], image["height"])`](../../5%EC%B0%A8/prepare_training.py#L497)

**오류 메시지:** SALSA 라벨과 이미지 크기가 다릅니다.

**거부 조건:** [`count &gt; self.reserved`](../../5%EC%B0%A8/prepare_training.py#L184)

**오류 메시지:** 전송 예약보다 수신량이 큽니다.

**거부 조건:** [`start and (response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-"))`](../../5%EC%B0%A8/prepare_training.py#L222)

**오류 메시지:** 서버가 재개 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`int(response.headers.get("Content-Length", remaining)) != remaining`](../../5%EC%B0%A8/prepare_training.py#L224)

**오류 메시지:** 원본과 실제 전송 크기가 다릅니다.

**거부 조건:** [`not receipt.exists() or load(receipt)["sha256"] != sha256_file(destination)`](../../5%EC%B0%A8/prepare_training.py#L441)

**오류 메시지:** 기존 다운로드의 보존 해시가 없거나 다릅니다.

**거부 조건:** [`consecutive_failures &gt;= 3`](../../5%EC%B0%A8/prepare_training.py#L475)

**오류 메시지:** 이미지 확보가 연속 3개 실패했습니다. 원인을 확인한 뒤 재개하세요.


#### LEVEL 3 · [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`THRESHOLDS`](../../5%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의=[.05, .1, .15, .17, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .9]`


**거부 조건:** [`not choices`](../../5%EC%B0%A8/train_pipeline.py#L24)

**오류 메시지:** 선택할 검증 임계값이 없습니다.

**거부 조건:** [`not results`](../../5%EC%B0%A8/train_pipeline.py#L30)

**오류 메시지:** 비교할 검증 결과가 없습니다.

**거부 조건:** [`saved.exists() and load(saved) != contract`](../../5%EC%B0%A8/train_pipeline.py#L40)

**오류 메시지:** checkpoint의 데이터·학습 조건이 현재 명세와 다릅니다.

**거부 조건:** [`any(len(model.names) != 1 or model.names[0] != "trash" for model in models)`](../../5%EC%B0%A8/train_pipeline.py#L111)

**오류 메시지:** 단일 trash 클래스 가중치가 아닙니다.

**거부 조건:** [`sha256_file(best) != load(directory / "phase_complete.json")["best_sha256"]`](../../5%EC%B0%A8/train_pipeline.py#L220)

**오류 메시지:** 완료 학습 모델이 기록된 해시와 다릅니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L43)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L47)

**오류 메시지:** 원래 계약 없는 checkpoint는 자동 재개할 수 없습니다.

**거부 조건:** [`not allow_resume`](../../5%EC%B0%A8/train_pipeline.py#L49)

**오류 메시지:** 중단 checkpoint가 있습니다. 재개를 명시적으로 선택하세요.

**거부 조건:** [`not best.is_file()`](../../5%EC%B0%A8/train_pipeline.py#L216)

**오류 메시지:** 완료 학습 가중치가 없습니다.


</details>

### LEVEL 3 · 실제 사용·실험 순서

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

**단계:** 입력

**내용:** 쓰레기 영상·라벨·모델·선택한 차수 설정

**단계:** 처리

**내용:** 자료 준비·모델/영상 처리·평가 또는 상태 표시

**단계:** 출력

**내용:** 탐지 후보·평가 지표·화면·보고서


### LEVEL 3 · 결과와 실패를 확인하기

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


### LEVEL 3 · 실행 전 대조할 차수 조건

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

[자료 폴더](../../5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/final-to-5.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-4"></a>
## LEVEL 4 - Advanced

### LEVEL 4 · 설계 의도와 검토 경계

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

### LEVEL 4 · 이 차수 구현의 실제 근거

| 내용 |
| --- |
| **파일:** [build_exe.py](../../5%EC%B0%A8/build_exe.py)<br>**원문에 정의된 역할·구성:** PyInstaller 의존성 확인과 사용자가 선택한 빌드를 수행합니다. |
| **파일:** [dashboard.py](../../5%EC%B0%A8/dashboard.py)<br>**원문에 정의된 역할·구성:** Codex와 독립 실행되는 루프백 전용 대시보드입니다. |
| **파일:** [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)<br>**원문에 정의된 역할·구성:** 기존 GPU 환경에서 탐지와 학습을 독립 프로세스로 실행합니다. |
| **파일:** [launcher.py](../../5%EC%B0%A8/launcher.py)<br>**원문에 정의된 역할·구성:** 독립 대시보드 실행기입니다. 학습은 자동 시작하지 않습니다. |
| **파일:** [pipeline.py](../../5%EC%B0%A8/pipeline.py)<br>**원문에 정의된 역할·구성:** D 드라이브의 앱과 기존 GPU 컨테이너를 연결합니다. |
| **파일:** [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)<br>**원문에 정의된 역할·구성:** 출처와 고정 평가 자료를 보존하며 추가 학습 데이터를 준비합니다. |
| **파일:** [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)<br>**원문에 정의된 역할·구성:** 검증에서 기존 모델과 추가 학습 모델을 비교하고 고정 테스트를 한 번 평가합니다. |
| **파일:** [verify_sources.py](../../5%EC%B0%A8/verify_sources.py)<br>**원문에 정의된 역할·구성:** 소스의 UTF-8·문법과 납품 파일 존재를 검사합니다. |
| **파일:** [tests/test_dashboard.py](../../5%EC%B0%A8/tests/test_dashboard.py)<br>**원문에 정의된 역할·구성:** 실제 HTTP 경계와 파이프라인 오류 전달을 검사합니다. |

**단계:** 입력

**내용:** 쓰레기 영상·라벨·모델·선택한 차수 설정

**단계:** 처리

**내용:** 자료 준비·모델/영상 처리·평가 또는 상태 표시

**단계:** 출력

**내용:** 탐지 후보·평가 지표·화면·보고서


### LEVEL 4 · 조건·변경·결과를 함께 검토하기

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 4 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [build_exe.py](../../5%EC%B0%A8/build_exe.py)<br>**정의된 옵션 이름:** `--build` |
| **진입 소스:** [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |
| **진입 소스:** [launcher.py](../../5%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |
| **진입 소스:** [pipeline.py](../../5%EC%B0%A8/pipeline.py)<br>**정의된 옵션 이름:** `--action`, `--params` |
| **진입 소스:** [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)<br>**정의된 옵션 이름:** `--prepare` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 4 · [build_exe.py](../../5%EC%B0%A8/build_exe.py)


| 내용 |
| --- |
| **설정·옵션:** [`--build`](../../5%EC%B0%A8/build_exe.py#L13)<br>**코드의 선언:** `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 내용 |
| --- |
| **거부 조건:** [`not available`](../../5%EC%B0%A8/build_exe.py#L19)<br>**오류 메시지:** 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

#### LEVEL 4 · [dashboard.py](../../5%EC%B0%A8/dashboard.py)


**설정·옵션:** [`LOG_LIMIT`](../../5%EC%B0%A8/dashboard.py#L14)

**코드의 선언:** `정의=64 * 1024`

**설정·옵션:** [`MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L15)

**코드의 선언:** `정의=4 * 1024**3`

**설정·옵션:** [`VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L16)

**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm'}`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/dashboard.py#L17)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent`


**거부 조건:** [`not isinstance(value, dict) or not isinstance(value.get('ok'), bool)`](../../5%EC%B0%A8/dashboard.py#L50)

**오류 메시지:** 파이프라인 JSON 응답 형식이 잘못되었습니다.

**거부 조건:** [`not isinstance(value, str) or not value`](../../5%EC%B0%A8/dashboard.py#L57)

**오류 메시지:** 파일 경로가 필요합니다.

**거부 조건:** [`not any(path.is_relative_to((self.work / area).resolve()) for area in areas)`](../../5%EC%B0%A8/dashboard.py#L63)

**오류 메시지:** 허용된 작업 폴더 밖의 경로입니다.

**거부 조건:** [`not path.is_file()`](../../5%EC%B0%A8/dashboard.py#L65)

**오류 메시지:** 파일이 없습니다.

**거부 조건:** [`path.suffix.lower() not in ('.log', '.txt')`](../../5%EC%B0%A8/dashboard.py#L71)

**오류 메시지:** 로그 파일만 읽을 수 있습니다.

**거부 조건:** [`size &gt; 2 * 1024**2`](../../5%EC%B0%A8/dashboard.py#L39)

**오류 메시지:** 파이프라인 JSON 응답이 2MB 상한을 넘었습니다.

**거부 조건:** [`self.headers.get('Transfer-Encoding')`](../../5%EC%B0%A8/dashboard.py#L201)

**오류 메시지:** Content-Length가 있는 요청만 허용합니다.

**거부 조건:** [`not 0 &lt; length &lt;= 64 * 1024`](../../5%EC%B0%A8/dashboard.py#L226)

**오류 메시지:** JSON 요청은 64KB 이하이어야 합니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/dashboard.py#L229)

**오류 메시지:** JSON 객체가 필요합니다.

**거부 조건:** [`not 0 &lt; length &lt;= MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L206)

**오류 메시지:** 영상은 0 초과 4GB 이하만 업로드할 수 있습니다.

**거부 조건:** [`suffix not in VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L209)

**오류 메시지:** 지원하지 않는 영상 확장자입니다.

**거부 조건:** [`not chunk`](../../5%EC%B0%A8/dashboard.py#L217)

**오류 메시지:** 영상 업로드가 중단되었습니다.


#### LEVEL 4 · [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/gpu_worker.py#L223)

**코드의 선언:** ``

**설정·옵션:** [`--params`](../../5%EC%B0%A8/gpu_worker.py#L224)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`--worker`](../../5%EC%B0%A8/gpu_worker.py#L225)

**코드의 선언:** ``

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/gpu_worker.py#L17)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/gpu_worker.py#L18)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/gpu_worker.py#L19)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/gpu_worker.py#L20)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`OLD_APP`](../../5%EC%B0%A8/gpu_worker.py#L21)

**코드의 선언:** `정의=PROJECT / "최종/3차/클린뷰"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/gpu_worker.py#L22)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`


**거부 조건:** [`not any(path.is_relative_to(p.resolve()) for p in VIDEO_ROOTS)`](../../5%EC%B0%A8/gpu_worker.py#L50)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`path.suffix.lower() not in {".mp4", ".avi", ".mov", ".mkv", ".m4v"} or not path.is_file() or not path.stat().st_size`](../../5%EC%B0%A8/gpu_worker.py#L52)

**오류 메시지:** 유효한 영상을 선택하세요.

**거부 조건:** [`not final`](../../5%EC%B0%A8/gpu_worker.py#L83)

**오류 메시지:** 보존된 final.json이 없습니다.

**거부 조건:** [`not all(Path(p).is_file() for p in weights)`](../../5%EC%B0%A8/gpu_worker.py#L87)

**오류 메시지:** 보존된 학습 모델을 찾을 수 없습니다.

**거부 조건:** [`model_root not in permitted`](../../5%EC%B0%A8/gpu_worker.py#L176)

**오류 메시지:** 선택 모델의 저장 위치가 허용되지 않습니다.

**거부 조건:** [`type(size) is not int or not 640 &lt;= size &lt;= 2048`](../../5%EC%B0%A8/gpu_worker.py#L200)

**오류 메시지:** 선택 모델의 추론 해상도가 올바르지 않습니다.

**거부 조건:** [`not ok or frame is None or not math.isfinite(fps) or fps &lt;= 0`](../../5%EC%B0%A8/gpu_worker.py#L66)

**오류 메시지:** 영상을 읽을 수 없습니다. 파일과 코덱을 확인하세요.

**거부 조건:** [`not cv2.imwrite(str(out), frame)`](../../5%EC%B0%A8/gpu_worker.py#L70)

**오류 메시지:** 영상 미리보기를 저장하지 못했습니다.

**거부 조건:** [`set(params) - {"path", "seconds", "abandon", "leave", "baseline"}`](../../5%EC%B0%A8/gpu_worker.py#L135)

**오류 메시지:** 지원하지 않는 탐지 설정입니다.

**거부 조건:** [`job.get("pid") and is_alive(job["pid"], job["id"])`](../../5%EC%B0%A8/gpu_worker.py#L131)

**오류 메시지:** GPU 작업이 이미 진행 중입니다. 완료 후 실행하세요.

**거부 조건:** [`not math.isfinite(number) or not low &lt;= number &lt;= high`](../../5%EC%B0%A8/gpu_worker.py#L140)

**오류 메시지:** 탐지 설정 범위를 확인하세요.

**거부 조건:** [`not isinstance(params.get("resume", False), bool)`](../../5%EC%B0%A8/gpu_worker.py#L144)

**오류 메시지:** 재개 설정은 true 또는 false여야 합니다.

**거부 조건:** [`(WORK / "training/final.json").exists()`](../../5%EC%B0%A8/gpu_worker.py#L146)

**오류 메시지:** 이 실험은 이미 완료됐습니다. 결과를 보존하며 자동 재학습하지 않습니다.

**거부 조건:** [`not (ROOT / "train_pipeline.py").is_file()`](../../5%EC%B0%A8/gpu_worker.py#L148)

**오류 메시지:** 학습 구성을 준비 중입니다.

**거부 조건:** [`set(params) - {"resume"}`](../../5%EC%B0%A8/gpu_worker.py#L150)

**오류 메시지:** 지원하지 않는 학습 설정입니다.


#### LEVEL 4 · [launcher.py](../../5%EC%B0%A8/launcher.py)


| 내용 |
| --- |
| **설정·옵션:** [`--no-browser`](../../5%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../5%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../5%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../5%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 내용 |
| --- |
| **거부 조건:** [`response.status != 200`](../../5%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

#### LEVEL 4 · [pipeline.py](../../5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/pipeline.py#L183)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../5%EC%B0%A8/pipeline.py#L184)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/pipeline.py#L162)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../5%EC%B0%A8/pipeline.py#L175)

**오류 메시지:** 지원하지 않는 작업입니다.


#### LEVEL 4 · [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../5%EC%B0%A8/prepare_training.py#L552)<br>**코드의 선언:** `action="store_true"; required=True` |
| **설정·옵션:** [`ROOT`](../../5%EC%B0%A8/prepare_training.py#L22)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/prepare_training.py#L23)<br>**코드의 선언:** `정의=ROOT.parent / "이전 도커 실험/3차실험/trash_round3"` |
| **설정·옵션:** [`TRAINING`](../../5%EC%B0%A8/prepare_training.py#L24)<br>**코드의 선언:** `정의=ROOT / "work/training"` |
| **설정·옵션:** [`SEED`](../../5%EC%B0%A8/prepare_training.py#L25)<br>**코드의 선언:** `정의=20261028` |
| **설정·옵션:** [`MAX_BYTES`](../../5%EC%B0%A8/prepare_training.py#L26)<br>**코드의 선언:** `정의=20 * 1024 ** 3` |
| **설정·옵션:** [`STREET_SIZE`](../../5%EC%B0%A8/prepare_training.py#L28)<br>**코드의 선언:** `정의=13728630001` |
| **설정·옵션:** [`_ERROR_LOCK`](../../5%EC%B0%A8/prepare_training.py#L29)<br>**코드의 선언:** `정의=threading.Lock()` |

**거부 조건:** [`not all(math.isfinite(n) and n &gt; 0 for n in (width, height))`](../../5%EC%B0%A8/prepare_training.py#L72)

**오류 메시지:** 이미지 크기가 올바르지 않습니다.

**거부 조건:** [`not url.startswith("https://") and not url.startswith("http://127.0.0.1:")`](../../5%EC%B0%A8/prepare_training.py#L193)

**오류 메시지:** HTTPS 데이터 출처만 허용됩니다.

**거부 조건:** [`length &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L207)

**오류 메시지:** 원본 크기가 올바르지 않습니다.

**거부 조건:** [`start &gt; length`](../../5%EC%B0%A8/prepare_training.py#L214)

**오류 메시지:** 부분 다운로드가 원본 크기보다 큽니다.

**거부 조건:** [`partial.stat().st_size != length`](../../5%EC%B0%A8/prepare_training.py#L236)

**오류 메시지:** 다운로드가 완성되지 않았습니다.

**거부 조건:** [`start &lt; 0 or end &lt; start or end - start &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L271)

**오류 메시지:** 허용 범위를 넘는 ZIP 부분 요청입니다.

**거부 조건:** [`len(data) != end - start + 1`](../../5%EC%B0%A8/prepare_training.py#L290)

**오류 메시지:** ZIP 부분 응답 크기가 다릅니다.

**거부 조건:** [`info.file_size &gt; 32 * 1024 ** 2 or info.compress_size &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L296)

**오류 메시지:** 과도한 단일 이미지 크기입니다.

**거부 조건:** [`header[:4] != b"PK\x03\x04"`](../../5%EC%B0%A8/prepare_training.py#L299)

**오류 메시지:** ZIP 지역 헤더가 올바르지 않습니다.

**거부 조건:** [`len(data) != info.file_size or zlib.crc32(data) & 0xffffffff != info.CRC`](../../5%EC%B0%A8/prepare_training.py#L313)

**오류 메시지:** ZIP 이미지 CRC가 일치하지 않습니다.

**거부 조건:** [`shutil.disk_usage(training).free &lt; 25 * 1024 ** 3`](../../5%EC%B0%A8/prepare_training.py#L367)

**오류 메시지:** 데이터 준비와 학습을 위한 여유 공간 25GB가 필요합니다.

**거부 조건:** [`len(accepted) &lt; 500`](../../5%EC%B0%A8/prepare_training.py#L513)

**오류 메시지:** 중복 배제 후 추가 학습 이미지가 500개 미만입니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(math.isfinite(n) for n in row)`](../../5%EC%B0%A8/prepare_training.py#L58)

**오류 메시지:** 단일 trash 클래스와 유한한 YOLO 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x - width / 2 and x + width / 2 &lt;= 1 + tolerance                                                            and -tolerance &lt;= y - height / 2 and y + height / 2 &lt;= 1 + tolerance)`](../../5%EC%B0%A8/prepare_training.py#L63)

**오류 메시지:** 라벨 상자가 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(math.isfinite(n) for n in (x, y, w, h)) or w &lt;= 0 or h &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L77)

**오류 메시지:** COCO 상자의 크기가 올바르지 않습니다.

**거부 조건:** [`right &lt;= left or bottom &lt;= top`](../../5%EC%B0%A8/prepare_training.py#L80)

**오류 메시지:** 이미지와 겹치지 않는 COCO 상자입니다.

**거부 조건:** [`not match`](../../5%EC%B0%A8/prepare_training.py#L103)

**오류 메시지:** 과거 pLitterStreet 자료의 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`digest != expected_md5`](../../5%EC%B0%A8/prepare_training.py#L240)

**오류 메시지:** 공식 MD5와 다운로드가 일치하지 않습니다.

**거부 조건:** [`decoder.unconsumed_tail or not decoder.eof`](../../5%EC%B0%A8/prepare_training.py#L307)

**오류 메시지:** ZIP 압축 해제 크기가 선언과 다릅니다.

**거부 조건:** [`load(path) != value`](../../5%EC%B0%A8/prepare_training.py#L321)

**오류 메시지:** 고정 데이터 명세를 현재 값으로 바꿀 수 없습니다.

**거부 조건:** [`manifest["sources_sha256"] != sha256_file(ROOT / "sources.json")`](../../5%EC%B0%A8/prepare_training.py#L362)

**오류 메시지:** 고정 명세 작성 뒤 데이터 출처 정책이 바뀌었습니다.

**거부 조건:** [`image.width &lt; 16 or image.height &lt; 16 or image.width * image.height &gt; 100000000`](../../5%EC%B0%A8/prepare_training.py#L125)

**오류 메시지:** 허용 범위 밖의 이미지 크기입니다.

**거부 조건:** [`count &lt; 0 or self.used + self.reserved + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L169)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`self.reserved &lt; 0`](../../5%EC%B0%A8/prepare_training.py#L176)

**오류 메시지:** 전송 예약량이 음수가 됐습니다.

**거부 조건:** [`count &lt; 0 or self.used + (0 if reserved else self.reserved) + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L181)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/")`](../../5%EC%B0%A8/prepare_training.py#L278)

**오류 메시지:** 서버가 정확한 ZIP 부분 요청을 지원하지 않습니다.

**거부 조건:** [`info["width"] != image["width"] or info["height"] != image["height"]`](../../5%EC%B0%A8/prepare_training.py#L453)

**오류 메시지:** COCO와 원본 이미지 크기가 다릅니다.

**거부 조건:** [`(info["width"], info["height"]) != (image["width"], image["height"])`](../../5%EC%B0%A8/prepare_training.py#L497)

**오류 메시지:** SALSA 라벨과 이미지 크기가 다릅니다.

**거부 조건:** [`count &gt; self.reserved`](../../5%EC%B0%A8/prepare_training.py#L184)

**오류 메시지:** 전송 예약보다 수신량이 큽니다.

**거부 조건:** [`start and (response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-"))`](../../5%EC%B0%A8/prepare_training.py#L222)

**오류 메시지:** 서버가 재개 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`int(response.headers.get("Content-Length", remaining)) != remaining`](../../5%EC%B0%A8/prepare_training.py#L224)

**오류 메시지:** 원본과 실제 전송 크기가 다릅니다.

**거부 조건:** [`not receipt.exists() or load(receipt)["sha256"] != sha256_file(destination)`](../../5%EC%B0%A8/prepare_training.py#L441)

**오류 메시지:** 기존 다운로드의 보존 해시가 없거나 다릅니다.

**거부 조건:** [`consecutive_failures &gt;= 3`](../../5%EC%B0%A8/prepare_training.py#L475)

**오류 메시지:** 이미지 확보가 연속 3개 실패했습니다. 원인을 확인한 뒤 재개하세요.


#### LEVEL 4 · [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`THRESHOLDS`](../../5%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의=[.05, .1, .15, .17, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .9]`


**거부 조건:** [`not choices`](../../5%EC%B0%A8/train_pipeline.py#L24)

**오류 메시지:** 선택할 검증 임계값이 없습니다.

**거부 조건:** [`not results`](../../5%EC%B0%A8/train_pipeline.py#L30)

**오류 메시지:** 비교할 검증 결과가 없습니다.

**거부 조건:** [`saved.exists() and load(saved) != contract`](../../5%EC%B0%A8/train_pipeline.py#L40)

**오류 메시지:** checkpoint의 데이터·학습 조건이 현재 명세와 다릅니다.

**거부 조건:** [`any(len(model.names) != 1 or model.names[0] != "trash" for model in models)`](../../5%EC%B0%A8/train_pipeline.py#L111)

**오류 메시지:** 단일 trash 클래스 가중치가 아닙니다.

**거부 조건:** [`sha256_file(best) != load(directory / "phase_complete.json")["best_sha256"]`](../../5%EC%B0%A8/train_pipeline.py#L220)

**오류 메시지:** 완료 학습 모델이 기록된 해시와 다릅니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L43)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L47)

**오류 메시지:** 원래 계약 없는 checkpoint는 자동 재개할 수 없습니다.

**거부 조건:** [`not allow_resume`](../../5%EC%B0%A8/train_pipeline.py#L49)

**오류 메시지:** 중단 checkpoint가 있습니다. 재개를 명시적으로 선택하세요.

**거부 조건:** [`not best.is_file()`](../../5%EC%B0%A8/train_pipeline.py#L216)

**오류 메시지:** 완료 학습 가중치가 없습니다.


</details>

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


### LEVEL 4 · 재현과 전체 비교

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

위 구성요소의 입력·출력과 실패 조건을 같은 차수 소스에 연결해 검토합니다. 전체 비교는 추가·수정·삭제와 원래 보관 범위를 구분하는 근거입니다.

[자료 폴더](../../5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/final-to-5.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<a id="reading-level-5"></a>
## LEVEL 5 - Expert

기존의 전체 설명·표·코드·함수 참조·파일별 비교는 아래에 그대로 이어집니다. [자료 폴더](../../5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/final-to-5.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<!-- reading-levels:end -->



[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../5%EC%B0%A8) · [← 이전: 최종/최종](stage-5.md) · [다음: 6차 →](round-6.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

**항목:** 1

**이 차수에서 확인할 내용:** 대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.


<a name="-입력처리출력"></a>
## 입력·처리·출력

**단계:** 입력

**내용:** 쓰레기 영상·라벨·모델·선택한 차수 설정

**단계:** 처리

**내용:** 자료 준비·모델/영상 처리·평가 또는 상태 표시

**단계:** 출력

**내용:** 탐지 후보·평가 지표·화면·보고서


<a name="usage"></a>

<a name="️-화면과-사용-흐름"></a>
## 화면과 사용 흐름

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

<a name="structure"></a>

<a name="-실제-자료-구성"></a>
## 실제 자료 구성

| 내용 |
| --- |
| **경로:** [docs/](../../5%EC%B0%A8/docs)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [tests/](../../5%EC%B0%A8/tests)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [web/](../../5%EC%B0%A8/web)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [README.md](../../5%EC%B0%A8/README.md)<br>**자료 종류:** MD 파일 |
| **경로:** [build_exe.py](../../5%EC%B0%A8/build_exe.py)<br>**자료 종류:** PY 파일 |
| **경로:** [dashboard.py](../../5%EC%B0%A8/dashboard.py)<br>**자료 종류:** PY 파일 |
| **경로:** [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)<br>**자료 종류:** PY 파일 |
| **경로:** [launcher.py](../../5%EC%B0%A8/launcher.py)<br>**자료 종류:** PY 파일 |
| **경로:** [pipeline.py](../../5%EC%B0%A8/pipeline.py)<br>**자료 종류:** PY 파일 |
| **경로:** [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)<br>**자료 종류:** PY 파일 |
| **경로:** [sources.json](../../5%EC%B0%A8/sources.json)<br>**자료 종류:** JSON 파일 |
| **경로:** [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)<br>**자료 종류:** PY 파일 |
| **경로:** [verify_sources.py](../../5%EC%B0%A8/verify_sources.py)<br>**자료 종류:** PY 파일 |
| **경로:** [사용안내.txt](../../5%EC%B0%A8/%EC%82%AC%EC%9A%A9%EC%95%88%EB%82%B4.txt)<br>**자료 종류:** TXT 파일 |
| **경로:** [실행.bat](../../5%EC%B0%A8/%EC%8B%A4%ED%96%89.bat)<br>**자료 종류:** BAT 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 내용 |
| --- |
| **파일:** [build_exe.py](../../5%EC%B0%A8/build_exe.py)<br>**원문에 정의된 역할·구성:** PyInstaller 의존성 확인과 사용자가 선택한 빌드를 수행합니다. |
| **파일:** [dashboard.py](../../5%EC%B0%A8/dashboard.py)<br>**원문에 정의된 역할·구성:** Codex와 독립 실행되는 루프백 전용 대시보드입니다. |
| **파일:** [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)<br>**원문에 정의된 역할·구성:** 기존 GPU 환경에서 탐지와 학습을 독립 프로세스로 실행합니다. |
| **파일:** [launcher.py](../../5%EC%B0%A8/launcher.py)<br>**원문에 정의된 역할·구성:** 독립 대시보드 실행기입니다. 학습은 자동 시작하지 않습니다. |
| **파일:** [pipeline.py](../../5%EC%B0%A8/pipeline.py)<br>**원문에 정의된 역할·구성:** D 드라이브의 앱과 기존 GPU 컨테이너를 연결합니다. |
| **파일:** [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)<br>**원문에 정의된 역할·구성:** 출처와 고정 평가 자료를 보존하며 추가 학습 데이터를 준비합니다. |
| **파일:** [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)<br>**원문에 정의된 역할·구성:** 검증에서 기존 모델과 추가 학습 모델을 비교하고 고정 테스트를 한 번 평가합니다. |
| **파일:** [verify_sources.py](../../5%EC%B0%A8/verify_sources.py)<br>**원문에 정의된 역할·구성:** 소스의 UTF-8·문법과 납품 파일 존재를 검사합니다. |
| **파일:** [tests/test_dashboard.py](../../5%EC%B0%A8/tests/test_dashboard.py)<br>**원문에 정의된 역할·구성:** 실제 HTTP 경계와 파이프라인 오류 전달을 검사합니다. |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

<a name="️-소스에서-제공하는-cli-옵션"></a>
### 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [build_exe.py](../../5%EC%B0%A8/build_exe.py)<br>**정의된 옵션 이름:** `--build` |
| **진입 소스:** [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |
| **진입 소스:** [launcher.py](../../5%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |
| **진입 소스:** [pipeline.py](../../5%EC%B0%A8/pipeline.py)<br>**정의된 옵션 이름:** `--action`, `--params` |
| **진입 소스:** [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)<br>**정의된 옵션 이름:** `--prepare` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [build_exe.py](../../5%EC%B0%A8/build_exe.py)


| 내용 |
| --- |
| **설정·옵션:** [`--build`](../../5%EC%B0%A8/build_exe.py#L13)<br>**코드의 선언:** `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 내용 |
| --- |
| **거부 조건:** [`not available`](../../5%EC%B0%A8/build_exe.py#L19)<br>**오류 메시지:** 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

### [dashboard.py](../../5%EC%B0%A8/dashboard.py)


**설정·옵션:** [`LOG_LIMIT`](../../5%EC%B0%A8/dashboard.py#L14)

**코드의 선언:** `정의=64 * 1024`

**설정·옵션:** [`MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L15)

**코드의 선언:** `정의=4 * 1024**3`

**설정·옵션:** [`VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L16)

**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm'}`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/dashboard.py#L17)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent`


**거부 조건:** [`not isinstance(value, dict) or not isinstance(value.get('ok'), bool)`](../../5%EC%B0%A8/dashboard.py#L50)

**오류 메시지:** 파이프라인 JSON 응답 형식이 잘못되었습니다.

**거부 조건:** [`not isinstance(value, str) or not value`](../../5%EC%B0%A8/dashboard.py#L57)

**오류 메시지:** 파일 경로가 필요합니다.

**거부 조건:** [`not any(path.is_relative_to((self.work / area).resolve()) for area in areas)`](../../5%EC%B0%A8/dashboard.py#L63)

**오류 메시지:** 허용된 작업 폴더 밖의 경로입니다.

**거부 조건:** [`not path.is_file()`](../../5%EC%B0%A8/dashboard.py#L65)

**오류 메시지:** 파일이 없습니다.

**거부 조건:** [`path.suffix.lower() not in ('.log', '.txt')`](../../5%EC%B0%A8/dashboard.py#L71)

**오류 메시지:** 로그 파일만 읽을 수 있습니다.

**거부 조건:** [`size &gt; 2 * 1024**2`](../../5%EC%B0%A8/dashboard.py#L39)

**오류 메시지:** 파이프라인 JSON 응답이 2MB 상한을 넘었습니다.

**거부 조건:** [`self.headers.get('Transfer-Encoding')`](../../5%EC%B0%A8/dashboard.py#L201)

**오류 메시지:** Content-Length가 있는 요청만 허용합니다.

**거부 조건:** [`not 0 &lt; length &lt;= 64 * 1024`](../../5%EC%B0%A8/dashboard.py#L226)

**오류 메시지:** JSON 요청은 64KB 이하이어야 합니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/dashboard.py#L229)

**오류 메시지:** JSON 객체가 필요합니다.

**거부 조건:** [`not 0 &lt; length &lt;= MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L206)

**오류 메시지:** 영상은 0 초과 4GB 이하만 업로드할 수 있습니다.

**거부 조건:** [`suffix not in VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L209)

**오류 메시지:** 지원하지 않는 영상 확장자입니다.

**거부 조건:** [`not chunk`](../../5%EC%B0%A8/dashboard.py#L217)

**오류 메시지:** 영상 업로드가 중단되었습니다.


### [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/gpu_worker.py#L223)

**코드의 선언:** ``

**설정·옵션:** [`--params`](../../5%EC%B0%A8/gpu_worker.py#L224)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`--worker`](../../5%EC%B0%A8/gpu_worker.py#L225)

**코드의 선언:** ``

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/gpu_worker.py#L17)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/gpu_worker.py#L18)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/gpu_worker.py#L19)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/gpu_worker.py#L20)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`OLD_APP`](../../5%EC%B0%A8/gpu_worker.py#L21)

**코드의 선언:** `정의=PROJECT / "최종/3차/클린뷰"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/gpu_worker.py#L22)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`


**거부 조건:** [`not any(path.is_relative_to(p.resolve()) for p in VIDEO_ROOTS)`](../../5%EC%B0%A8/gpu_worker.py#L50)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`path.suffix.lower() not in {".mp4", ".avi", ".mov", ".mkv", ".m4v"} or not path.is_file() or not path.stat().st_size`](../../5%EC%B0%A8/gpu_worker.py#L52)

**오류 메시지:** 유효한 영상을 선택하세요.

**거부 조건:** [`not final`](../../5%EC%B0%A8/gpu_worker.py#L83)

**오류 메시지:** 보존된 final.json이 없습니다.

**거부 조건:** [`not all(Path(p).is_file() for p in weights)`](../../5%EC%B0%A8/gpu_worker.py#L87)

**오류 메시지:** 보존된 학습 모델을 찾을 수 없습니다.

**거부 조건:** [`model_root not in permitted`](../../5%EC%B0%A8/gpu_worker.py#L176)

**오류 메시지:** 선택 모델의 저장 위치가 허용되지 않습니다.

**거부 조건:** [`type(size) is not int or not 640 &lt;= size &lt;= 2048`](../../5%EC%B0%A8/gpu_worker.py#L200)

**오류 메시지:** 선택 모델의 추론 해상도가 올바르지 않습니다.

**거부 조건:** [`not ok or frame is None or not math.isfinite(fps) or fps &lt;= 0`](../../5%EC%B0%A8/gpu_worker.py#L66)

**오류 메시지:** 영상을 읽을 수 없습니다. 파일과 코덱을 확인하세요.

**거부 조건:** [`not cv2.imwrite(str(out), frame)`](../../5%EC%B0%A8/gpu_worker.py#L70)

**오류 메시지:** 영상 미리보기를 저장하지 못했습니다.

**거부 조건:** [`set(params) - {"path", "seconds", "abandon", "leave", "baseline"}`](../../5%EC%B0%A8/gpu_worker.py#L135)

**오류 메시지:** 지원하지 않는 탐지 설정입니다.

**거부 조건:** [`job.get("pid") and is_alive(job["pid"], job["id"])`](../../5%EC%B0%A8/gpu_worker.py#L131)

**오류 메시지:** GPU 작업이 이미 진행 중입니다. 완료 후 실행하세요.

**거부 조건:** [`not math.isfinite(number) or not low &lt;= number &lt;= high`](../../5%EC%B0%A8/gpu_worker.py#L140)

**오류 메시지:** 탐지 설정 범위를 확인하세요.

**거부 조건:** [`not isinstance(params.get("resume", False), bool)`](../../5%EC%B0%A8/gpu_worker.py#L144)

**오류 메시지:** 재개 설정은 true 또는 false여야 합니다.

**거부 조건:** [`(WORK / "training/final.json").exists()`](../../5%EC%B0%A8/gpu_worker.py#L146)

**오류 메시지:** 이 실험은 이미 완료됐습니다. 결과를 보존하며 자동 재학습하지 않습니다.

**거부 조건:** [`not (ROOT / "train_pipeline.py").is_file()`](../../5%EC%B0%A8/gpu_worker.py#L148)

**오류 메시지:** 학습 구성을 준비 중입니다.

**거부 조건:** [`set(params) - {"resume"}`](../../5%EC%B0%A8/gpu_worker.py#L150)

**오류 메시지:** 지원하지 않는 학습 설정입니다.


### [launcher.py](../../5%EC%B0%A8/launcher.py)


| 내용 |
| --- |
| **설정·옵션:** [`--no-browser`](../../5%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../5%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../5%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../5%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 내용 |
| --- |
| **거부 조건:** [`response.status != 200`](../../5%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

### [pipeline.py](../../5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../5%EC%B0%A8/pipeline.py#L183)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../5%EC%B0%A8/pipeline.py#L184)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../5%EC%B0%A8/pipeline.py#L162)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../5%EC%B0%A8/pipeline.py#L175)

**오류 메시지:** 지원하지 않는 작업입니다.


### [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../5%EC%B0%A8/prepare_training.py#L552)<br>**코드의 선언:** `action="store_true"; required=True` |
| **설정·옵션:** [`ROOT`](../../5%EC%B0%A8/prepare_training.py#L22)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ARCHIVE`](../../5%EC%B0%A8/prepare_training.py#L23)<br>**코드의 선언:** `정의=ROOT.parent / "이전 도커 실험/3차실험/trash_round3"` |
| **설정·옵션:** [`TRAINING`](../../5%EC%B0%A8/prepare_training.py#L24)<br>**코드의 선언:** `정의=ROOT / "work/training"` |
| **설정·옵션:** [`SEED`](../../5%EC%B0%A8/prepare_training.py#L25)<br>**코드의 선언:** `정의=20261028` |
| **설정·옵션:** [`MAX_BYTES`](../../5%EC%B0%A8/prepare_training.py#L26)<br>**코드의 선언:** `정의=20 * 1024 ** 3` |
| **설정·옵션:** [`STREET_SIZE`](../../5%EC%B0%A8/prepare_training.py#L28)<br>**코드의 선언:** `정의=13728630001` |
| **설정·옵션:** [`_ERROR_LOCK`](../../5%EC%B0%A8/prepare_training.py#L29)<br>**코드의 선언:** `정의=threading.Lock()` |

**거부 조건:** [`not all(math.isfinite(n) and n &gt; 0 for n in (width, height))`](../../5%EC%B0%A8/prepare_training.py#L72)

**오류 메시지:** 이미지 크기가 올바르지 않습니다.

**거부 조건:** [`not url.startswith("https://") and not url.startswith("http://127.0.0.1:")`](../../5%EC%B0%A8/prepare_training.py#L193)

**오류 메시지:** HTTPS 데이터 출처만 허용됩니다.

**거부 조건:** [`length &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L207)

**오류 메시지:** 원본 크기가 올바르지 않습니다.

**거부 조건:** [`start &gt; length`](../../5%EC%B0%A8/prepare_training.py#L214)

**오류 메시지:** 부분 다운로드가 원본 크기보다 큽니다.

**거부 조건:** [`partial.stat().st_size != length`](../../5%EC%B0%A8/prepare_training.py#L236)

**오류 메시지:** 다운로드가 완성되지 않았습니다.

**거부 조건:** [`start &lt; 0 or end &lt; start or end - start &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L271)

**오류 메시지:** 허용 범위를 넘는 ZIP 부분 요청입니다.

**거부 조건:** [`len(data) != end - start + 1`](../../5%EC%B0%A8/prepare_training.py#L290)

**오류 메시지:** ZIP 부분 응답 크기가 다릅니다.

**거부 조건:** [`info.file_size &gt; 32 * 1024 ** 2 or info.compress_size &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L296)

**오류 메시지:** 과도한 단일 이미지 크기입니다.

**거부 조건:** [`header[:4] != b"PK\x03\x04"`](../../5%EC%B0%A8/prepare_training.py#L299)

**오류 메시지:** ZIP 지역 헤더가 올바르지 않습니다.

**거부 조건:** [`len(data) != info.file_size or zlib.crc32(data) & 0xffffffff != info.CRC`](../../5%EC%B0%A8/prepare_training.py#L313)

**오류 메시지:** ZIP 이미지 CRC가 일치하지 않습니다.

**거부 조건:** [`shutil.disk_usage(training).free &lt; 25 * 1024 ** 3`](../../5%EC%B0%A8/prepare_training.py#L367)

**오류 메시지:** 데이터 준비와 학습을 위한 여유 공간 25GB가 필요합니다.

**거부 조건:** [`len(accepted) &lt; 500`](../../5%EC%B0%A8/prepare_training.py#L513)

**오류 메시지:** 중복 배제 후 추가 학습 이미지가 500개 미만입니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(math.isfinite(n) for n in row)`](../../5%EC%B0%A8/prepare_training.py#L58)

**오류 메시지:** 단일 trash 클래스와 유한한 YOLO 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x - width / 2 and x + width / 2 &lt;= 1 + tolerance                                                            and -tolerance &lt;= y - height / 2 and y + height / 2 &lt;= 1 + tolerance)`](../../5%EC%B0%A8/prepare_training.py#L63)

**오류 메시지:** 라벨 상자가 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(math.isfinite(n) for n in (x, y, w, h)) or w &lt;= 0 or h &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L77)

**오류 메시지:** COCO 상자의 크기가 올바르지 않습니다.

**거부 조건:** [`right &lt;= left or bottom &lt;= top`](../../5%EC%B0%A8/prepare_training.py#L80)

**오류 메시지:** 이미지와 겹치지 않는 COCO 상자입니다.

**거부 조건:** [`not match`](../../5%EC%B0%A8/prepare_training.py#L103)

**오류 메시지:** 과거 pLitterStreet 자료의 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`digest != expected_md5`](../../5%EC%B0%A8/prepare_training.py#L240)

**오류 메시지:** 공식 MD5와 다운로드가 일치하지 않습니다.

**거부 조건:** [`decoder.unconsumed_tail or not decoder.eof`](../../5%EC%B0%A8/prepare_training.py#L307)

**오류 메시지:** ZIP 압축 해제 크기가 선언과 다릅니다.

**거부 조건:** [`load(path) != value`](../../5%EC%B0%A8/prepare_training.py#L321)

**오류 메시지:** 고정 데이터 명세를 현재 값으로 바꿀 수 없습니다.

**거부 조건:** [`manifest["sources_sha256"] != sha256_file(ROOT / "sources.json")`](../../5%EC%B0%A8/prepare_training.py#L362)

**오류 메시지:** 고정 명세 작성 뒤 데이터 출처 정책이 바뀌었습니다.

**거부 조건:** [`image.width &lt; 16 or image.height &lt; 16 or image.width * image.height &gt; 100000000`](../../5%EC%B0%A8/prepare_training.py#L125)

**오류 메시지:** 허용 범위 밖의 이미지 크기입니다.

**거부 조건:** [`count &lt; 0 or self.used + self.reserved + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L169)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`self.reserved &lt; 0`](../../5%EC%B0%A8/prepare_training.py#L176)

**오류 메시지:** 전송 예약량이 음수가 됐습니다.

**거부 조건:** [`count &lt; 0 or self.used + (0 if reserved else self.reserved) + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L181)

**오류 메시지:** 추가 데이터 전송 누적 20GB 상한에 도달했습니다.

**거부 조건:** [`response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/")`](../../5%EC%B0%A8/prepare_training.py#L278)

**오류 메시지:** 서버가 정확한 ZIP 부분 요청을 지원하지 않습니다.

**거부 조건:** [`info["width"] != image["width"] or info["height"] != image["height"]`](../../5%EC%B0%A8/prepare_training.py#L453)

**오류 메시지:** COCO와 원본 이미지 크기가 다릅니다.

**거부 조건:** [`(info["width"], info["height"]) != (image["width"], image["height"])`](../../5%EC%B0%A8/prepare_training.py#L497)

**오류 메시지:** SALSA 라벨과 이미지 크기가 다릅니다.

**거부 조건:** [`count &gt; self.reserved`](../../5%EC%B0%A8/prepare_training.py#L184)

**오류 메시지:** 전송 예약보다 수신량이 큽니다.

**거부 조건:** [`start and (response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-"))`](../../5%EC%B0%A8/prepare_training.py#L222)

**오류 메시지:** 서버가 재개 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`int(response.headers.get("Content-Length", remaining)) != remaining`](../../5%EC%B0%A8/prepare_training.py#L224)

**오류 메시지:** 원본과 실제 전송 크기가 다릅니다.

**거부 조건:** [`not receipt.exists() or load(receipt)["sha256"] != sha256_file(destination)`](../../5%EC%B0%A8/prepare_training.py#L441)

**오류 메시지:** 기존 다운로드의 보존 해시가 없거나 다릅니다.

**거부 조건:** [`consecutive_failures &gt;= 3`](../../5%EC%B0%A8/prepare_training.py#L475)

**오류 메시지:** 이미지 확보가 연속 3개 실패했습니다. 원인을 확인한 뒤 재개하세요.


### [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`THRESHOLDS`](../../5%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의=[.05, .1, .15, .17, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .9]`


**거부 조건:** [`not choices`](../../5%EC%B0%A8/train_pipeline.py#L24)

**오류 메시지:** 선택할 검증 임계값이 없습니다.

**거부 조건:** [`not results`](../../5%EC%B0%A8/train_pipeline.py#L30)

**오류 메시지:** 비교할 검증 결과가 없습니다.

**거부 조건:** [`saved.exists() and load(saved) != contract`](../../5%EC%B0%A8/train_pipeline.py#L40)

**오류 메시지:** checkpoint의 데이터·학습 조건이 현재 명세와 다릅니다.

**거부 조건:** [`any(len(model.names) != 1 or model.names[0] != "trash" for model in models)`](../../5%EC%B0%A8/train_pipeline.py#L111)

**오류 메시지:** 단일 trash 클래스 가중치가 아닙니다.

**거부 조건:** [`sha256_file(best) != load(directory / "phase_complete.json")["best_sha256"]`](../../5%EC%B0%A8/train_pipeline.py#L220)

**오류 메시지:** 완료 학습 모델이 기록된 해시와 다릅니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L43)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L47)

**오류 메시지:** 원래 계약 없는 checkpoint는 자동 재개할 수 없습니다.

**거부 조건:** [`not allow_resume`](../../5%EC%B0%A8/train_pipeline.py#L49)

**오류 메시지:** 중단 checkpoint가 있습니다. 재개를 명시적으로 선택하세요.

**거부 조건:** [`not best.is_file()`](../../5%EC%B0%A8/train_pipeline.py#L216)

**오류 메시지:** 완료 학습 가중치가 없습니다.


</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

<a name="️-제약과-문제-해결"></a>
## 제약과 문제 해결

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


<a name="changes"></a>

<a name="-직전-자료와-전체-비교"></a>
## 직전 자료와 전체 비교

최종/최종에서 5차로 이어지는 실제 파일 비교입니다.

[전체 비교·자료 범위](../comparisons/final-to-5.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>파일별 비교·크기·해시 자세히 보기</summary>

[공개 폴더](../../5차/) · [실행과 고정 테스트 기록](../../5차/README.md) · [최종/최종과 파일 비교](../comparisons/final-to-5.md)

</details>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../5%EC%B0%A8) · [← 이전: 최종/최종](stage-5.md) · [다음: 6차 →](round-6.md)
