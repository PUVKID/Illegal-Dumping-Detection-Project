<div align="center">

# 🧹 이전 도커 실험

도커 실험의 앱과 설정을 보관합니다. 폴더 이름만으로 정확한 차수나 시간 순서를 확정하지 않습니다. 비교는 동일 상대 경로 기준이며 용도와 위치가 달라 대부분 추가·삭제로 나타날 수 있습니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 원본 자료](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98)

## 🎯 목적과 이 차수의 역할

도커 실험의 앱과 설정을 보관합니다. 폴더 이름만으로 정확한 차수나 시간 순서를 확정하지 않습니다. 비교는 동일 상대 경로 기준이며 용도와 위치가 달라 대부분 추가·삭제로 나타날 수 있습니다.

<a name="features"></a>

## ✨ 핵심 기능과 보존 범위

| 항목 | 이 차수에서 확인할 내용 |
|---|---|
| 1 | 도커 실험의 앱과 설정을 보관합니다. 폴더 이름만으로 정확한 차수나 시간 순서를 확정하지 않습니다. 비교는 동일 상대 경로 기준이며 용도와 위치가 달라 대부분 추가·삭제로 나타날 수 있습니다. |

## 🔄 입력·처리·출력

| 단계 | 내용 |
|---|---|
| 📥 입력 | 쓰레기 영상·라벨·모델·선택한 차수 설정 |
| ⚙️ 처리 | 자료 준비·모델/영상 처리·평가 또는 상태 표시 |
| 📤 출력 | 탐지 후보·평가 지표·화면·보고서 |

<a name="usage"></a>

## 🖐️ 화면과 사용 흐름

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

<a name="structure"></a>

## 📁 실제 자료 구성

| 경로 | 자료 종류 |
|---|---|
| [3차실험/](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98) | 하위 자료 폴더 |
| [불법투기탐지/](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/%EB%B6%88%EB%B2%95%ED%88%AC%EA%B8%B0%ED%83%90%EC%A7%80) | 하위 자료 폴더 |
| [README.md](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/README.md) | MD 파일 |

## 🧩 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [3차실험/trash_round3/app/data_pipeline.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/data_pipeline.py) | Round 3: fixed photo identities, original-resolution inputs, new labelled data. |
| [3차실험/trash_round3/app/inference.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/inference.py) | Identical full-image / overlapping-tile inference for evaluation and the app. |
| [3차실험/trash_round3/app/train_round3.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/train_round3.py) | New architectures, dataset expansion, focused refinement, validation-only selection. |
| [불법투기탐지/illegal_dumping_detector.ipynb](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/%EB%B6%88%EB%B2%95%ED%88%AC%EA%B8%B0%ED%83%90%EC%A7%80/illegal_dumping_detector.ipynb) | 노트북 31개 셀 |
| [3차실험/trash_round3/app/backend.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py) | Docker worker. All paths are rooted in the existing PBL directory. |
| [3차실험/trash_round3/app/detector.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/detector.py) | Conservative stationary-object event candidates, not legal determinations. |
| [3차실험/trash_round3/app/launcher.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py) | Windows executable: local UI + Docker GPU worker (no Python install needed). |
| [3차실험/trash_round3/app/make_report.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/make_report.py) | Run in Docker after round 2 completes. Offline Korean Bold report, honest target status. |
| [3차실험/trash_round3/data/taco/demo.ipynb](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/demo.ipynb) | 노트북 16개 셀 |

<a name="setup"></a>

## 🚀 설치 환경과 실행·사용법

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

### 📦 이 보관본의 의존성 목록

[3차실험/trash_round3/app/requirements-docker.txt](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/requirements-docker.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
ultralytics==8.4.160
opencv-python==4.14.0.94
imageio-ffmpeg==0.6.0
requests
PyYAML
matplotlib
```

### ⚙️ 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [launcher.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py) | `--no-browser`, `--port`, `--self-test` |
| [download.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/download.py) | `--dataset_path` |
| [detector.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py) | `--model`, `--dataset`, `--round`, `--lrate`, `--use_aug`, `--use_transplants`, `--class_map` |
| [split_dataset.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/split_dataset.py) | `--dataset_dir`, `--test_percentage`, `--val_percentage`, `--nr_trials` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>🔬 함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [3차실험/trash_round3/app/backend.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L6) | `정의=BASE / 'trash_round3'` |
| [`APP`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L7) | `정의=ROOT / 'app'` |
| [`STATE`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L8) | `정의=APP / 'state'` |
| [`JOBS`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L9) | `정의=STATE / 'jobs'` |
| [`VIDEO_EXT`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L10) | `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v'}` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not any(p.is_relative_to(r.resolve()) for r in [ROOT/'videos',APP/'uploads'])`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L52) | 허용된 영상 폴더가 아닙니다. |
| [`not p.is_file() or p.suffix.lower() not in VIDEO_EXT`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L54) | 영상 파일이 없습니다. |
| [`p.stat().st_size == 0`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L60) | 0바이트 파일입니다. 원본 영상을 다시 복사하세요. |
| [`kind == 'improve' and (ROOT/'experiment_plan.json').exists()`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L77) | 이미 시작한 3차 실험입니다. 중복 학습 대신 현재 작업을 확인하세요. |
| [`kind not in ['improve','detect']`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L80) | 지원하지 않는 작업 |
| [`not ok or frame is None`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L65) | 첫 프레임을 읽을 수 없습니다. 복사 완료 여부와 코덱/파일 손상을 확인하세요. |
| [`not math.isfinite(fps) or fps &lt;= 0`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L66) | 유효한 FPS가 없습니다. 영상을 재인코딩하세요. |
| [`any(j.get('state') in ['queued','running'] for j in status()['jobs'])`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L83) | 진행 중인 작업이 있습니다. 완료 후 실행하세요. |
| [`not all(c.isalnum() or c=='_' for c in args['job'])`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/backend.py#L118) | 잘못된 작업 ID |

### [3차실험/trash_round3/app/data_pipeline.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/data_pipeline.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`REF`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/data_pipeline.py#L9) | `정의=ROOT/'data/reference'` |
| [`FULL`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/data_pipeline.py#L10) | `정의=ROOT/'data/full'` |
| [`SEED`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/data_pipeline.py#L11) | `정의=20261013` |

### [3차실험/trash_round3/app/detector.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/detector.py)


| 거부 조건 | 오류 메시지 |
|---|---|
| [`not any(weights.is_relative_to(r.resolve()) for r in [ROOT/'runs']) or not weights.is_file() or weights.suffix!='.pt'`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/detector.py#L60) | 학습된 best.pt를 선택하세요. |
| [`not(0&lt;=seconds&lt;=86400 and 1&lt;=abandon&lt;=600 and 0&lt;=leave&lt;=120 and .01&lt;=conf&lt;=1 and 0&lt;=baseline&lt;=60)`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/detector.py#L63) | 탐지 설정 범위 오류 |
| [`any(len(m.names)!=1 or m.names[0]!='trash' for m in trash)`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/detector.py#L73) | 1-class trash 학습 모델이 아닙니다. |
| [`total&lt;=0`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/detector.py#L77) | 처리할 프레임이 없습니다. |
| [`len(roi)&lt;3 or any(len(v)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) and 0&lt;=x&lt;=1 for x in v) for v in roi)`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/detector.py#L66) | 구역은 0~1 좌표의 다각형이어야 합니다. |

### [3차실험/trash_round3/app/launcher.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--no-browser`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L132) | `action='store_true'` |
| [`--port`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L132) | `type=int; default=0` |
| [`--self-test`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L133) | `action='store_true'` |
| [`CONTAINER`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L7) | `정의='2026-2'` |
| [`ASSETS`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L9) | `정의=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))` |
| [`CACHE`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L11) | `정의=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'TrashDetector3'` |
| [`DOCKER`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L13) | `정의='docker'` |
| [`FLAGS`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L14) | `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`'..' in p.parts or not p.is_relative_to(PurePosixPath(REMOTE+'/results'))`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L58) | 잘못된 결과 경로 |
| [`not 0&lt;length&lt;1024*1024`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L121) | 잘못된 요청 크기 |
| [`ext not in {'.mp4','.avi','.mov','.mkv','.m4v'}`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L108) | 지원하지 않는 영상 확장자 |
| [`not 0&lt;length&lt;=4*1024**3`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L109) | 파일 크기는 0 초과 4GB 이하이어야 합니다. |
| [`not chunk`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/launcher.py#L116) | 영상 업로드가 중단되었습니다. |

### [3차실험/trash_round3/app/make_report.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/make_report.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`APP`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/make_report.py#L10) | `정의=Path(__file__).resolve().parent` |
| [`OUT`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/app/make_report.py#L11) | `정의=ROOT/'report'` |

### [3차실험/trash_round3/data/taco/detector/detector.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`command`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L201) | `help="Opt: 'train', 'evaluate', 'test'"` |
| [`--model`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L202) | `required=True; help="Path to weights .h5 file or 'coco'"` |
| [`--dataset`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L203) | `required=True; help='Directory of the dataset'` |
| [`--round`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L204) | `required=True; type=int; help='Split number'` |
| [`--lrate`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L205) | `required=False; default=0.001; type=float; help='learning rate'` |
| [`--use_aug`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L206) | `action='store_true'` |
| [`--use_transplants`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L208) | `required=False; default=None; help='Path to transplanted dataset'` |
| [`--class_map`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L209) | `required=True; help=' Target classes'` |
| [`ROOT_DIR`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L60) | `정의=os.path.abspath("./models")` |
| [`COCO_MODEL_PATH`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L63) | `정의=os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")` |
| [`DEFAULT_LOGS_DIR`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/detector.py#L66) | `정의=os.path.join(ROOT_DIR, "logs")` |

### [3차실험/trash_round3/data/taco/detector/split_dataset.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/split_dataset.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--dataset_dir`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/split_dataset.py#L10) | `required=True; help='Path to dataset annotations'` |
| [`--test_percentage`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/split_dataset.py#L11) | `type=int; default=10; required=False; help='Percentage of images used for the testing set'` |
| [`--val_percentage`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/split_dataset.py#L12) | `type=int; default=10; required=False; help='Percentage of images used for the validation set'` |
| [`--nr_trials`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/split_dataset.py#L13) | `type=int; default=10; required=False; help='Number of splits'` |

### [3차실험/trash_round3/data/taco/detector/visualize.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/visualize.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT_DIR`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/detector/visualize.py#L25) | `정의=os.path.abspath("../")` |

### [3차실험/trash_round3/data/taco/download.py](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/download.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--dataset_path`](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98/3%EC%B0%A8%EC%8B%A4%ED%97%98/trash_round3/data/taco/download.py#L15) | `required=False; default='./data/annotations.json'; help='Path to annotations'` |

</details>

<a name="results"></a>

## 📊 처리 결과와 출력 읽기

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

## 🛠️ 제약과 문제 해결

| 상황 | 확인할 내용 |
|---|---|
| 학습 또는 화면이 시작되지 않음 | 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다. |
| 원본 계약 검사 실패 | 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다. |
| 지표 해석이 어려움 | 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다. |

<a name="changes"></a>

## 🔍 직전 자료와 전체 비교

이 자료의 보존 범위와 기준 파일을 연결합니다.

[📄 전체 비교·자료 범위](../comparisons/docker-to-3.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>📚 파일별 비교·크기·해시 자세히 보기</summary>

[공개 폴더](../../이전%20도커%20실험/) · [최종/3차와 파일 비교](../comparisons/docker-to-3.md)

</details>

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 원본 자료](../../%EC%9D%B4%EC%A0%84%20%EB%8F%84%EC%BB%A4%20%EC%8B%A4%ED%97%98)
