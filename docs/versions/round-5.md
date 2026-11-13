<div align="center">

<a name="-5차"></a>
# 5차

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../5%EC%B0%A8) · [← 이전: 최종/최종](stage-5.md) · [다음: 6차 →](round-6.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

| 항목 | 이 차수에서 확인할 내용 |
|---|---|
| 1 | 대시보드와 독립 실행 빌드, 데이터 준비·학습·평가 코드 및 검사를 보관합니다. 기존 테스트 150장은 이미 사용한 벤치마크이며 새로운 독립 평가가 아닙니다. 기존 보고서와 평가 조건이 달라 단순 개선률로 해석하지 않습니다. |

<a name="-입력처리출력"></a>
## 입력·처리·출력

| 단계 | 내용 |
|---|---|
| 입력 | 쓰레기 영상·라벨·모델·선택한 차수 설정 |
| 처리 | 자료 준비·모델/영상 처리·평가 또는 상태 표시 |
| 출력 | 탐지 후보·평가 지표·화면·보고서 |

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

| 경로 | 자료 종류 |
|---|---|
| [docs/](../../5%EC%B0%A8/docs) | 하위 자료 폴더 |
| [tests/](../../5%EC%B0%A8/tests) | 하위 자료 폴더 |
| [web/](../../5%EC%B0%A8/web) | 하위 자료 폴더 |
| [README.md](../../5%EC%B0%A8/README.md) | MD 파일 |
| [build_exe.py](../../5%EC%B0%A8/build_exe.py) | PY 파일 |
| [dashboard.py](../../5%EC%B0%A8/dashboard.py) | PY 파일 |
| [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py) | PY 파일 |
| [launcher.py](../../5%EC%B0%A8/launcher.py) | PY 파일 |
| [pipeline.py](../../5%EC%B0%A8/pipeline.py) | PY 파일 |
| [prepare_training.py](../../5%EC%B0%A8/prepare_training.py) | PY 파일 |
| [sources.json](../../5%EC%B0%A8/sources.json) | JSON 파일 |
| [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py) | PY 파일 |
| [verify_sources.py](../../5%EC%B0%A8/verify_sources.py) | PY 파일 |
| [사용안내.txt](../../5%EC%B0%A8/%EC%82%AC%EC%9A%A9%EC%95%88%EB%82%B4.txt) | TXT 파일 |
| [실행.bat](../../5%EC%B0%A8/%EC%8B%A4%ED%96%89.bat) | BAT 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [build_exe.py](../../5%EC%B0%A8/build_exe.py) | PyInstaller 의존성 확인과 사용자가 선택한 빌드를 수행합니다. |
| [dashboard.py](../../5%EC%B0%A8/dashboard.py) | Codex와 독립 실행되는 루프백 전용 대시보드입니다. |
| [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py) | 기존 GPU 환경에서 탐지와 학습을 독립 프로세스로 실행합니다. |
| [launcher.py](../../5%EC%B0%A8/launcher.py) | 독립 대시보드 실행기입니다. 학습은 자동 시작하지 않습니다. |
| [pipeline.py](../../5%EC%B0%A8/pipeline.py) | D 드라이브의 앱과 기존 GPU 컨테이너를 연결합니다. |
| [prepare_training.py](../../5%EC%B0%A8/prepare_training.py) | 출처와 고정 평가 자료를 보존하며 추가 학습 데이터를 준비합니다. |
| [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py) | 검증에서 기존 모델과 추가 학습 모델을 비교하고 고정 테스트를 한 번 평가합니다. |
| [verify_sources.py](../../5%EC%B0%A8/verify_sources.py) | 소스의 UTF-8·문법과 납품 파일 존재를 검사합니다. |
| [tests/test_dashboard.py](../../5%EC%B0%A8/tests/test_dashboard.py) | 실제 HTTP 경계와 파이프라인 오류 전달을 검사합니다. |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

<a name="️-소스에서-제공하는-cli-옵션"></a>
### 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [build_exe.py](../../5%EC%B0%A8/build_exe.py) | `--build` |
| [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py) | `--action`, `--params`, `--worker` |
| [launcher.py](../../5%EC%B0%A8/launcher.py) | `--no-browser`, `--port`, `--self-test`, `--hidden` |
| [pipeline.py](../../5%EC%B0%A8/pipeline.py) | `--action`, `--params` |
| [prepare_training.py](../../5%EC%B0%A8/prepare_training.py) | `--prepare` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [build_exe.py](../../5%EC%B0%A8/build_exe.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--build`](../../5%EC%B0%A8/build_exe.py#L13) | `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not available`](../../5%EC%B0%A8/build_exe.py#L19) | 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

### [dashboard.py](../../5%EC%B0%A8/dashboard.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`LOG_LIMIT`](../../5%EC%B0%A8/dashboard.py#L14) | `정의=64 * 1024` |
| [`MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L15) | `정의=4 * 1024**3` |
| [`VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L16) | `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm'}` |
| [`ROOT`](../../5%EC%B0%A8/dashboard.py#L17) | `정의=Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not isinstance(value, dict) or not isinstance(value.get('ok'), bool)`](../../5%EC%B0%A8/dashboard.py#L50) | 파이프라인 JSON 응답 형식이 잘못되었습니다. |
| [`not isinstance(value, str) or not value`](../../5%EC%B0%A8/dashboard.py#L57) | 파일 경로가 필요합니다. |
| [`not any(path.is_relative_to((self.work / area).resolve()) for area in areas)`](../../5%EC%B0%A8/dashboard.py#L63) | 허용된 작업 폴더 밖의 경로입니다. |
| [`not path.is_file()`](../../5%EC%B0%A8/dashboard.py#L65) | 파일이 없습니다. |
| [`path.suffix.lower() not in ('.log', '.txt')`](../../5%EC%B0%A8/dashboard.py#L71) | 로그 파일만 읽을 수 있습니다. |
| [`size &gt; 2 * 1024**2`](../../5%EC%B0%A8/dashboard.py#L39) | 파이프라인 JSON 응답이 2MB 상한을 넘었습니다. |
| [`self.headers.get('Transfer-Encoding')`](../../5%EC%B0%A8/dashboard.py#L201) | Content-Length가 있는 요청만 허용합니다. |
| [`not 0 &lt; length &lt;= 64 * 1024`](../../5%EC%B0%A8/dashboard.py#L226) | JSON 요청은 64KB 이하이어야 합니다. |
| [`not isinstance(params, dict)`](../../5%EC%B0%A8/dashboard.py#L229) | JSON 객체가 필요합니다. |
| [`not 0 &lt; length &lt;= MAX_UPLOAD`](../../5%EC%B0%A8/dashboard.py#L206) | 영상은 0 초과 4GB 이하만 업로드할 수 있습니다. |
| [`suffix not in VIDEO_EXT`](../../5%EC%B0%A8/dashboard.py#L209) | 지원하지 않는 영상 확장자입니다. |
| [`not chunk`](../../5%EC%B0%A8/dashboard.py#L217) | 영상 업로드가 중단되었습니다. |

### [gpu_worker.py](../../5%EC%B0%A8/gpu_worker.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--action`](../../5%EC%B0%A8/gpu_worker.py#L223) | `` |
| [`--params`](../../5%EC%B0%A8/gpu_worker.py#L224) | `default="{}"` |
| [`--worker`](../../5%EC%B0%A8/gpu_worker.py#L225) | `` |
| [`ROOT`](../../5%EC%B0%A8/gpu_worker.py#L17) | `정의=Path(__file__).resolve().parent` |
| [`PROJECT`](../../5%EC%B0%A8/gpu_worker.py#L18) | `정의=ROOT.parent` |
| [`WORK`](../../5%EC%B0%A8/gpu_worker.py#L19) | `정의=ROOT / "work"` |
| [`ARCHIVE`](../../5%EC%B0%A8/gpu_worker.py#L20) | `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"` |
| [`OLD_APP`](../../5%EC%B0%A8/gpu_worker.py#L21) | `정의=PROJECT / "최종/3차/클린뷰"` |
| [`VIDEO_ROOTS`](../../5%EC%B0%A8/gpu_worker.py#L22) | `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not any(path.is_relative_to(p.resolve()) for p in VIDEO_ROOTS)`](../../5%EC%B0%A8/gpu_worker.py#L50) | 허용된 영상 폴더가 아닙니다. |
| [`path.suffix.lower() not in {".mp4", ".avi", ".mov", ".mkv", ".m4v"} or not path.is_file() or not path.stat().st_size`](../../5%EC%B0%A8/gpu_worker.py#L52) | 유효한 영상을 선택하세요. |
| [`not final`](../../5%EC%B0%A8/gpu_worker.py#L83) | 보존된 final.json이 없습니다. |
| [`not all(Path(p).is_file() for p in weights)`](../../5%EC%B0%A8/gpu_worker.py#L87) | 보존된 학습 모델을 찾을 수 없습니다. |
| [`model_root not in permitted`](../../5%EC%B0%A8/gpu_worker.py#L176) | 선택 모델의 저장 위치가 허용되지 않습니다. |
| [`type(size) is not int or not 640 &lt;= size &lt;= 2048`](../../5%EC%B0%A8/gpu_worker.py#L200) | 선택 모델의 추론 해상도가 올바르지 않습니다. |
| [`not ok or frame is None or not math.isfinite(fps) or fps &lt;= 0`](../../5%EC%B0%A8/gpu_worker.py#L66) | 영상을 읽을 수 없습니다. 파일과 코덱을 확인하세요. |
| [`not cv2.imwrite(str(out), frame)`](../../5%EC%B0%A8/gpu_worker.py#L70) | 영상 미리보기를 저장하지 못했습니다. |
| [`set(params) - {"path", "seconds", "abandon", "leave", "baseline"}`](../../5%EC%B0%A8/gpu_worker.py#L135) | 지원하지 않는 탐지 설정입니다. |
| [`job.get("pid") and is_alive(job["pid"], job["id"])`](../../5%EC%B0%A8/gpu_worker.py#L131) | GPU 작업이 이미 진행 중입니다. 완료 후 실행하세요. |
| [`not math.isfinite(number) or not low &lt;= number &lt;= high`](../../5%EC%B0%A8/gpu_worker.py#L140) | 탐지 설정 범위를 확인하세요. |
| [`not isinstance(params.get("resume", False), bool)`](../../5%EC%B0%A8/gpu_worker.py#L144) | 재개 설정은 true 또는 false여야 합니다. |
| [`(WORK / "training/final.json").exists()`](../../5%EC%B0%A8/gpu_worker.py#L146) | 이 실험은 이미 완료됐습니다. 결과를 보존하며 자동 재학습하지 않습니다. |
| [`not (ROOT / "train_pipeline.py").is_file()`](../../5%EC%B0%A8/gpu_worker.py#L148) | 학습 구성을 준비 중입니다. |
| [`set(params) - {"resume"}`](../../5%EC%B0%A8/gpu_worker.py#L150) | 지원하지 않는 학습 설정입니다. |

### [launcher.py](../../5%EC%B0%A8/launcher.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--no-browser`](../../5%EC%B0%A8/launcher.py#L55) | `action='store_true'` |
| [`--port`](../../5%EC%B0%A8/launcher.py#L56) | `type=int; default=0` |
| [`--self-test`](../../5%EC%B0%A8/launcher.py#L57) | `action='store_true'` |
| [`--hidden`](../../5%EC%B0%A8/launcher.py#L58) | `action='store_true'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`response.status != 200`](../../5%EC%B0%A8/launcher.py#L20) | 루프백 상태 검사에 실패했습니다. |

### [pipeline.py](../../5%EC%B0%A8/pipeline.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--action`](../../5%EC%B0%A8/pipeline.py#L183) | `required=True` |
| [`--params`](../../5%EC%B0%A8/pipeline.py#L184) | `default="{}"` |
| [`ROOT`](../../5%EC%B0%A8/pipeline.py#L10) | `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent` |
| [`PROJECT`](../../5%EC%B0%A8/pipeline.py#L12) | `정의=ROOT.parent` |
| [`WORK`](../../5%EC%B0%A8/pipeline.py#L13) | `정의=ROOT / "work"` |
| [`CONTAINER`](../../5%EC%B0%A8/pipeline.py#L14) | `정의="2026"` |
| [`REMOTE`](../../5%EC%B0%A8/pipeline.py#L15) | `정의="/workspace/2026/월요일 PBL/5차"` |
| [`PYTHON`](../../5%EC%B0%A8/pipeline.py#L16) | `정의="/opt/venvs/torch/bin/python"` |
| [`ARCHIVE`](../../5%EC%B0%A8/pipeline.py#L17) | `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"` |
| [`VIDEO_ROOTS`](../../5%EC%B0%A8/pipeline.py#L18) | `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]` |
| [`EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L19) | `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../5%EC%B0%A8/pipeline.py#L47) | 지원하는 영상 파일을 선택하세요. |
| [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../5%EC%B0%A8/pipeline.py#L49) | 허용된 영상 폴더가 아닙니다. |
| [`not p.stat().st_size`](../../5%EC%B0%A8/pipeline.py#L51) | 0바이트 영상은 처리할 수 없습니다. |
| [`not isinstance(params, dict)`](../../5%EC%B0%A8/pipeline.py#L162) | 설정은 JSON 객체여야 합니다. |
| [`name not in {"probe", "detect", "train", "health"}`](../../5%EC%B0%A8/pipeline.py#L175) | 지원하지 않는 작업입니다. |

### [prepare_training.py](../../5%EC%B0%A8/prepare_training.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--prepare`](../../5%EC%B0%A8/prepare_training.py#L552) | `action="store_true"; required=True` |
| [`ROOT`](../../5%EC%B0%A8/prepare_training.py#L22) | `정의=Path(__file__).resolve().parent` |
| [`ARCHIVE`](../../5%EC%B0%A8/prepare_training.py#L23) | `정의=ROOT.parent / "이전 도커 실험/3차실험/trash_round3"` |
| [`TRAINING`](../../5%EC%B0%A8/prepare_training.py#L24) | `정의=ROOT / "work/training"` |
| [`SEED`](../../5%EC%B0%A8/prepare_training.py#L25) | `정의=20261028` |
| [`MAX_BYTES`](../../5%EC%B0%A8/prepare_training.py#L26) | `정의=20 * 1024 ** 3` |
| [`STREET_SIZE`](../../5%EC%B0%A8/prepare_training.py#L28) | `정의=13728630001` |
| [`_ERROR_LOCK`](../../5%EC%B0%A8/prepare_training.py#L29) | `정의=threading.Lock()` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not all(math.isfinite(n) and n &gt; 0 for n in (width, height))`](../../5%EC%B0%A8/prepare_training.py#L72) | 이미지 크기가 올바르지 않습니다. |
| [`not url.startswith("https://") and not url.startswith("http://127.0.0.1:")`](../../5%EC%B0%A8/prepare_training.py#L193) | HTTPS 데이터 출처만 허용됩니다. |
| [`length &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L207) | 원본 크기가 올바르지 않습니다. |
| [`start &gt; length`](../../5%EC%B0%A8/prepare_training.py#L214) | 부분 다운로드가 원본 크기보다 큽니다. |
| [`partial.stat().st_size != length`](../../5%EC%B0%A8/prepare_training.py#L236) | 다운로드가 완성되지 않았습니다. |
| [`start &lt; 0 or end &lt; start or end - start &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L271) | 허용 범위를 넘는 ZIP 부분 요청입니다. |
| [`len(data) != end - start + 1`](../../5%EC%B0%A8/prepare_training.py#L290) | ZIP 부분 응답 크기가 다릅니다. |
| [`info.file_size &gt; 32 * 1024 ** 2 or info.compress_size &gt; 32 * 1024 ** 2`](../../5%EC%B0%A8/prepare_training.py#L296) | 과도한 단일 이미지 크기입니다. |
| [`header[:4] != b"PK\x03\x04"`](../../5%EC%B0%A8/prepare_training.py#L299) | ZIP 지역 헤더가 올바르지 않습니다. |
| [`len(data) != info.file_size or zlib.crc32(data) & 0xffffffff != info.CRC`](../../5%EC%B0%A8/prepare_training.py#L313) | ZIP 이미지 CRC가 일치하지 않습니다. |
| [`shutil.disk_usage(training).free &lt; 25 * 1024 ** 3`](../../5%EC%B0%A8/prepare_training.py#L367) | 데이터 준비와 학습을 위한 여유 공간 25GB가 필요합니다. |
| [`len(accepted) &lt; 500`](../../5%EC%B0%A8/prepare_training.py#L513) | 중복 배제 후 추가 학습 이미지가 500개 미만입니다. |
| [`len(row) != 5 or row[0] != 0 or not all(math.isfinite(n) for n in row)`](../../5%EC%B0%A8/prepare_training.py#L58) | 단일 trash 클래스와 유한한 YOLO 좌표가 필요합니다. |
| [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x - width / 2 and x + width / 2 &lt;= 1 + tolerance                                                            and -tolerance &lt;= y - height / 2 and y + height / 2 &lt;= 1 + tolerance)`](../../5%EC%B0%A8/prepare_training.py#L63) | 라벨 상자가 이미지 경계를 벗어났습니다. |
| [`not all(math.isfinite(n) for n in (x, y, w, h)) or w &lt;= 0 or h &lt;= 0`](../../5%EC%B0%A8/prepare_training.py#L77) | COCO 상자의 크기가 올바르지 않습니다. |
| [`right &lt;= left or bottom &lt;= top`](../../5%EC%B0%A8/prepare_training.py#L80) | 이미지와 겹치지 않는 COCO 상자입니다. |
| [`not match`](../../5%EC%B0%A8/prepare_training.py#L103) | 과거 pLitterStreet 자료의 원본 ID를 확인할 수 없습니다. |
| [`digest != expected_md5`](../../5%EC%B0%A8/prepare_training.py#L240) | 공식 MD5와 다운로드가 일치하지 않습니다. |
| [`decoder.unconsumed_tail or not decoder.eof`](../../5%EC%B0%A8/prepare_training.py#L307) | ZIP 압축 해제 크기가 선언과 다릅니다. |
| [`load(path) != value`](../../5%EC%B0%A8/prepare_training.py#L321) | 고정 데이터 명세를 현재 값으로 바꿀 수 없습니다. |
| [`manifest["sources_sha256"] != sha256_file(ROOT / "sources.json")`](../../5%EC%B0%A8/prepare_training.py#L362) | 고정 명세 작성 뒤 데이터 출처 정책이 바뀌었습니다. |
| [`image.width &lt; 16 or image.height &lt; 16 or image.width * image.height &gt; 100000000`](../../5%EC%B0%A8/prepare_training.py#L125) | 허용 범위 밖의 이미지 크기입니다. |
| [`count &lt; 0 or self.used + self.reserved + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L169) | 추가 데이터 전송 누적 20GB 상한에 도달했습니다. |
| [`self.reserved &lt; 0`](../../5%EC%B0%A8/prepare_training.py#L176) | 전송 예약량이 음수가 됐습니다. |
| [`count &lt; 0 or self.used + (0 if reserved else self.reserved) + count &gt; self.limit`](../../5%EC%B0%A8/prepare_training.py#L181) | 추가 데이터 전송 누적 20GB 상한에 도달했습니다. |
| [`response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/")`](../../5%EC%B0%A8/prepare_training.py#L278) | 서버가 정확한 ZIP 부분 요청을 지원하지 않습니다. |
| [`info["width"] != image["width"] or info["height"] != image["height"]`](../../5%EC%B0%A8/prepare_training.py#L453) | COCO와 원본 이미지 크기가 다릅니다. |
| [`(info["width"], info["height"]) != (image["width"], image["height"])`](../../5%EC%B0%A8/prepare_training.py#L497) | SALSA 라벨과 이미지 크기가 다릅니다. |
| [`count &gt; self.reserved`](../../5%EC%B0%A8/prepare_training.py#L184) | 전송 예약보다 수신량이 큽니다. |
| [`start and (response.status != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {start}-"))`](../../5%EC%B0%A8/prepare_training.py#L222) | 서버가 재개 범위 요청을 보존하지 않았습니다. |
| [`int(response.headers.get("Content-Length", remaining)) != remaining`](../../5%EC%B0%A8/prepare_training.py#L224) | 원본과 실제 전송 크기가 다릅니다. |
| [`not receipt.exists() or load(receipt)["sha256"] != sha256_file(destination)`](../../5%EC%B0%A8/prepare_training.py#L441) | 기존 다운로드의 보존 해시가 없거나 다릅니다. |
| [`consecutive_failures &gt;= 3`](../../5%EC%B0%A8/prepare_training.py#L475) | 이미지 확보가 연속 3개 실패했습니다. 원인을 확인한 뒤 재개하세요. |

### [train_pipeline.py](../../5%EC%B0%A8/train_pipeline.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`THRESHOLDS`](../../5%EC%B0%A8/train_pipeline.py#L12) | `정의=[.05, .1, .15, .17, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .9]` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not choices`](../../5%EC%B0%A8/train_pipeline.py#L24) | 선택할 검증 임계값이 없습니다. |
| [`not results`](../../5%EC%B0%A8/train_pipeline.py#L30) | 비교할 검증 결과가 없습니다. |
| [`saved.exists() and load(saved) != contract`](../../5%EC%B0%A8/train_pipeline.py#L40) | checkpoint의 데이터·학습 조건이 현재 명세와 다릅니다. |
| [`any(len(model.names) != 1 or model.names[0] != "trash" for model in models)`](../../5%EC%B0%A8/train_pipeline.py#L111) | 단일 trash 클래스 가중치가 아닙니다. |
| [`sha256_file(best) != load(directory / "phase_complete.json")["best_sha256"]`](../../5%EC%B0%A8/train_pipeline.py#L220) | 완료 학습 모델이 기록된 해시와 다릅니다. |
| [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L43) | 완료 학습의 원래 계약이 없습니다. |
| [`not saved.exists()`](../../5%EC%B0%A8/train_pipeline.py#L47) | 원래 계약 없는 checkpoint는 자동 재개할 수 없습니다. |
| [`not allow_resume`](../../5%EC%B0%A8/train_pipeline.py#L49) | 중단 checkpoint가 있습니다. 재개를 명시적으로 선택하세요. |
| [`not best.is_file()`](../../5%EC%B0%A8/train_pipeline.py#L216) | 완료 학습 가중치가 없습니다. |

</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

<a name="️-제약과-문제-해결"></a>
## 제약과 문제 해결

| 상황 | 확인할 내용 |
|---|---|
| 학습 또는 화면이 시작되지 않음 | 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다. |
| 원본 계약 검사 실패 | 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다. |
| 지표 해석이 어려움 | 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다. |

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
