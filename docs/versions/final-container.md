<div align="center">

<a name="-최종"></a>
# 최종

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다.
- 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

**기술 분류:** 3차 실험·4차 보조 자료·최종 보고서 묶음

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>
<!-- reading-levels:start -->
[LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

프로젝트 전체의 설명은 [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)부터 [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)까지 같은 범위로 연결됩니다.

<a id="reading-level-1"></a>
## LEVEL 1 - Beginner

### LEVEL 1 · 이 자료가 하는 일과 달라진 점

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다.
- 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

### LEVEL 1 · 실제 동작을 따라 읽기

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다. - 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

하위 3차·4차·최종을 포함하는 컨테이너입니다. 파일 수 표의 최종 52개와 하위 파일을 중복 합산하지 않습니다.

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다.

최종 폴더에는 학습·추론 코드, 설명 이미지와 성능보고서를 함께 정리했습니다.

CLI는 명령어와 옵션을 입력해 프로그램을 실행하는 방식입니다. CSV는 값을 쉼표로 나눈 표 파일입니다.

입력 — 하위3차·4차·최종의 코드·기록·보고서

처리 — 실험 구성과 단일 프레임, 최종 성능보고서를 각각 연결

출력 — 자료별 설명과 원본 탐색

### LEVEL 1 · 준비하고 확인할 것

하위 폴더마다 자료 성격과 실행 조건이 다릅니다. 3차 실험 코드, 4차 보조 도구, 최종 HTML/CSV를 선택해서 읽습니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

#### LEVEL 1 · 이 보관본의 의존성 목록

[3차/클린뷰/requirements-docker.txt](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/requirements-docker.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
ultralytics==8.4.160
opencv-python==4.14.0.94
imageio-ffmpeg==0.6.0
requests
PyYAML
matplotlib
```

#### LEVEL 1 · 소스에서 제공하는 CLI 옵션

**진입 소스:** [finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)

**정의된 옵션 이름:** `--prepare`

**진입 소스:** [launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)

**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`

**진입 소스:** [download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)

**정의된 옵션 이름:** `--dataset_path`

**진입 소스:** [detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)

**정의된 옵션 이름:** `--model`, `--dataset`, `--round`, `--lrate`, `--use_aug`, `--use_transplants`, `--class_map`

**진입 소스:** [split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)

**정의된 옵션 이름:** `--dataset_dir`, `--test_percentage`, `--val_percentage`, `--nr_trials`


각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 1 · [3차/데이터/taco/detector/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)


**설정·옵션:** [`command`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L201)

**코드의 선언:** `help="Opt: 'train', 'evaluate', 'test'"`

**설정·옵션:** [`--model`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L202)

**코드의 선언:** `required=True; help="Path to weights .h5 file or 'coco'"`

**설정·옵션:** [`--dataset`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L203)

**코드의 선언:** `required=True; help='Directory of the dataset'`

**설정·옵션:** [`--round`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L204)

**코드의 선언:** `required=True; type=int; help='Split number'`

**설정·옵션:** [`--lrate`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L205)

**코드의 선언:** `required=False; default=0.001; type=float; help='learning rate'`

**설정·옵션:** [`--use_aug`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L206)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--use_transplants`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L208)

**코드의 선언:** `required=False; default=None; help='Path to transplanted dataset'`

**설정·옵션:** [`--class_map`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L209)

**코드의 선언:** `required=True; help=' Target classes'`

**설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L60)

**코드의 선언:** `정의=os.path.abspath("./models")`

**설정·옵션:** [`COCO_MODEL_PATH`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L63)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")`

**설정·옵션:** [`DEFAULT_LOGS_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L66)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "logs")`


#### LEVEL 1 · [3차/데이터/taco/detector/split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)


**설정·옵션:** [`--dataset_dir`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L10)

**코드의 선언:** `required=True; help='Path to dataset annotations'`

**설정·옵션:** [`--test_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L11)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the testing set'`

**설정·옵션:** [`--val_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L12)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the validation set'`

**설정·옵션:** [`--nr_trials`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L13)

**코드의 선언:** `type=int; default=10; required=False; help='Number of splits'`


#### LEVEL 1 · [3차/데이터/taco/detector/visualize.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py#L25)<br>**코드의 선언:** `정의=os.path.abspath("../")` |

#### LEVEL 1 · [3차/데이터/taco/download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)


**설정·옵션:** [`--dataset_path`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py#L15)

**코드의 선언:** `required=False; default='./data/annotations.json'; help='Path to annotations'`


#### LEVEL 1 · [3차/클린뷰/backend.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L6)<br>**코드의 선언:** `정의=BASE / 'trash_round3'` |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L7)<br>**코드의 선언:** `정의=ROOT / 'app'` |
| **설정·옵션:** [`STATE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L8)<br>**코드의 선언:** `정의=APP / 'state'` |
| **설정·옵션:** [`JOBS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L9)<br>**코드의 선언:** `정의=STATE / 'jobs'` |
| **설정·옵션:** [`VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L10)<br>**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v'}` |

**거부 조건:** [`not any(p.is_relative_to(r.resolve()) for r in [ROOT/'videos',APP/'uploads'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L52)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.is_file() or p.suffix.lower() not in VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L54)

**오류 메시지:** 영상 파일이 없습니다.

**거부 조건:** [`p.stat().st_size == 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L60)

**오류 메시지:** 0바이트 파일입니다. 원본 영상을 다시 복사하세요.

**거부 조건:** [`kind == 'improve' and (ROOT/'experiment_plan.json').exists()`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L77)

**오류 메시지:** 이미 시작한 3차 실험입니다. 중복 학습 대신 현재 작업을 확인하세요.

**거부 조건:** [`kind not in ['improve','detect']`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L80)

**오류 메시지:** 지원하지 않는 작업

**거부 조건:** [`not ok or frame is None`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L65)

**오류 메시지:** 첫 프레임을 읽을 수 없습니다. 복사 완료 여부와 코덱/파일 손상을 확인하세요.

**거부 조건:** [`not math.isfinite(fps) or fps &lt;= 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L66)

**오류 메시지:** 유효한 FPS가 없습니다. 영상을 재인코딩하세요.

**거부 조건:** [`any(j.get('state') in ['queued','running'] for j in status()['jobs'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L83)

**오류 메시지:** 진행 중인 작업이 있습니다. 완료 후 실행하세요.

**거부 조건:** [`not all(c.isalnum() or c=='_' for c in args['job'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L118)

**오류 메시지:** 잘못된 작업 ID


#### LEVEL 1 · [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py)


| 내용 |
| --- |
| **설정·옵션:** [`REF`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L9)<br>**코드의 선언:** `정의=ROOT/'data/reference'` |
| **설정·옵션:** [`FULL`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L10)<br>**코드의 선언:** `정의=ROOT/'data/full'` |
| **설정·옵션:** [`SEED`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L11)<br>**코드의 선언:** `정의=20261013` |

#### LEVEL 1 · [3차/클린뷰/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py)


**거부 조건:** [`not any(weights.is_relative_to(r.resolve()) for r in [ROOT/'runs']) or not weights.is_file() or weights.suffix!='.pt'`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L60)

**오류 메시지:** 학습된 best.pt를 선택하세요.

**거부 조건:** [`not(0&lt;=seconds&lt;=86400 and 1&lt;=abandon&lt;=600 and 0&lt;=leave&lt;=120 and .01&lt;=conf&lt;=1 and 0&lt;=baseline&lt;=60)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L63)

**오류 메시지:** 탐지 설정 범위 오류

**거부 조건:** [`any(len(m.names)!=1 or m.names[0]!='trash' for m in trash)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L73)

**오류 메시지:** 1-class trash 학습 모델이 아닙니다.

**거부 조건:** [`total&lt;=0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L77)

**오류 메시지:** 처리할 프레임이 없습니다.

**거부 조건:** [`len(roi)&lt;3 or any(len(v)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) and 0&lt;=x&lt;=1 for x in v) for v in roi)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L66)

**오류 메시지:** 구역은 0~1 좌표의 다각형이어야 합니다.


#### LEVEL 1 · [3차/클린뷰/finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L113)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L4)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DESKTOP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L5)<br>**코드의 선언:** `정의=SOURCE.parents[1]` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L6)<br>**코드의 선언:** `정의=DESKTOP/'3차'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L9)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0` |

#### LEVEL 1 · [3차/클린뷰/finish_on_exit.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py)


| 내용 |
| --- |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L5)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L6)<br>**코드의 선언:** `정의=SOURCE.parent` |
| **설정·옵션:** [`WORK`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L7)<br>**코드의 선언:** `정의=DEST / '_작업' / 'completion_once'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L8)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW` |

#### LEVEL 1 · [3차/클린뷰/launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)


**설정·옵션:** [`--no-browser`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--port`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `type=int; default=0`

**설정·옵션:** [`--self-test`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L133)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`CONTAINER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L7)

**코드의 선언:** `정의='2026-2'`

**설정·옵션:** [`ASSETS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L9)

**코드의 선언:** `정의=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))`

**설정·옵션:** [`CACHE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L11)

**코드의 선언:** `정의=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'TrashDetector3'`

**설정·옵션:** [`DOCKER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L13)

**코드의 선언:** `정의='docker'`

**설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L14)

**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0`


**거부 조건:** [`'..' in p.parts or not p.is_relative_to(PurePosixPath(REMOTE+'/results'))`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L58)

**오류 메시지:** 잘못된 결과 경로

**거부 조건:** [`not 0&lt;length&lt;1024*1024`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L121)

**오류 메시지:** 잘못된 요청 크기

**거부 조건:** [`ext not in {'.mp4','.avi','.mov','.mkv','.m4v'}`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L108)

**오류 메시지:** 지원하지 않는 영상 확장자

**거부 조건:** [`not 0&lt;length&lt;=4*1024**3`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L109)

**오류 메시지:** 파일 크기는 0 초과 4GB 이하이어야 합니다.

**거부 조건:** [`not chunk`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L116)

**오류 메시지:** 영상 업로드가 중단되었습니다.


#### LEVEL 1 · [3차/클린뷰/make_report.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py)


| 내용 |
| --- |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L10)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`OUT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L11)<br>**코드의 선언:** `정의=ROOT/'report'` |

</details>

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

### LEVEL 1 · 결과와 주의할 범위

최종 보고서의 성능은3차 고정 평가 조건에 속합니다. 상위 폴더 이름 최종이 모든 후속 차수의 최신 모델을 의미하지 않습니다.

**상황:** 실행 자료가 부족함

**확인할 내용:** 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다.

**상황:** 결과 범위 해석

**확인할 내용:** 자료 열람·기능 확인·실험 성적을 각각 구분합니다.


[자료 폴더](../../%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](../comparisons/final-container.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-2"></a>
## LEVEL 2 - Explorer

### LEVEL 2 · 목적과 구성의 연결

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다.
- 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다. - 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

하위 3차·4차·최종을 포함하는 컨테이너입니다. 파일 수 표의 최종 52개와 하위 파일을 중복 합산하지 않습니다.

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다.

최종 폴더에는 학습·추론 코드, 설명 이미지와 성능보고서를 함께 정리했습니다.

### LEVEL 2 · 입력에서 출력으로

**단계:** 입력

**내용:** 하위3차·4차·최종의 코드·기록·보고서

**단계:** 처리

**내용:** 실험 구성과 단일 프레임, 최종 성능보고서를 각각 연결

**단계:** 출력

**내용:** 자료별 설명과 원본 탐색


입력·처리·출력은 위의 같은 자료 흐름을 다른 단계에서 읽는 기준입니다. 처리 조건과 출력의 의미를 함께 확인합니다.

### LEVEL 2 · 설정과 처리 순서의 관계

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

하위 폴더마다 자료 성격과 실행 조건이 다릅니다. 3차 실험 코드, 4차 보조 도구, 최종 HTML/CSV를 선택해서 읽습니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

#### LEVEL 2 · 이 보관본의 의존성 목록

[3차/클린뷰/requirements-docker.txt](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/requirements-docker.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
ultralytics==8.4.160
opencv-python==4.14.0.94
imageio-ffmpeg==0.6.0
requests
PyYAML
matplotlib
```

#### LEVEL 2 · 소스에서 제공하는 CLI 옵션

**진입 소스:** [finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)

**정의된 옵션 이름:** `--prepare`

**진입 소스:** [launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)

**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`

**진입 소스:** [download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)

**정의된 옵션 이름:** `--dataset_path`

**진입 소스:** [detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)

**정의된 옵션 이름:** `--model`, `--dataset`, `--round`, `--lrate`, `--use_aug`, `--use_transplants`, `--class_map`

**진입 소스:** [split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)

**정의된 옵션 이름:** `--dataset_dir`, `--test_percentage`, `--val_percentage`, `--nr_trials`


각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 2 · [3차/데이터/taco/detector/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)


**설정·옵션:** [`command`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L201)

**코드의 선언:** `help="Opt: 'train', 'evaluate', 'test'"`

**설정·옵션:** [`--model`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L202)

**코드의 선언:** `required=True; help="Path to weights .h5 file or 'coco'"`

**설정·옵션:** [`--dataset`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L203)

**코드의 선언:** `required=True; help='Directory of the dataset'`

**설정·옵션:** [`--round`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L204)

**코드의 선언:** `required=True; type=int; help='Split number'`

**설정·옵션:** [`--lrate`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L205)

**코드의 선언:** `required=False; default=0.001; type=float; help='learning rate'`

**설정·옵션:** [`--use_aug`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L206)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--use_transplants`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L208)

**코드의 선언:** `required=False; default=None; help='Path to transplanted dataset'`

**설정·옵션:** [`--class_map`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L209)

**코드의 선언:** `required=True; help=' Target classes'`

**설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L60)

**코드의 선언:** `정의=os.path.abspath("./models")`

**설정·옵션:** [`COCO_MODEL_PATH`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L63)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")`

**설정·옵션:** [`DEFAULT_LOGS_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L66)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "logs")`


#### LEVEL 2 · [3차/데이터/taco/detector/split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)


**설정·옵션:** [`--dataset_dir`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L10)

**코드의 선언:** `required=True; help='Path to dataset annotations'`

**설정·옵션:** [`--test_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L11)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the testing set'`

**설정·옵션:** [`--val_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L12)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the validation set'`

**설정·옵션:** [`--nr_trials`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L13)

**코드의 선언:** `type=int; default=10; required=False; help='Number of splits'`


#### LEVEL 2 · [3차/데이터/taco/detector/visualize.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py#L25)<br>**코드의 선언:** `정의=os.path.abspath("../")` |

#### LEVEL 2 · [3차/데이터/taco/download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)


**설정·옵션:** [`--dataset_path`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py#L15)

**코드의 선언:** `required=False; default='./data/annotations.json'; help='Path to annotations'`


#### LEVEL 2 · [3차/클린뷰/backend.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L6)<br>**코드의 선언:** `정의=BASE / 'trash_round3'` |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L7)<br>**코드의 선언:** `정의=ROOT / 'app'` |
| **설정·옵션:** [`STATE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L8)<br>**코드의 선언:** `정의=APP / 'state'` |
| **설정·옵션:** [`JOBS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L9)<br>**코드의 선언:** `정의=STATE / 'jobs'` |
| **설정·옵션:** [`VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L10)<br>**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v'}` |

**거부 조건:** [`not any(p.is_relative_to(r.resolve()) for r in [ROOT/'videos',APP/'uploads'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L52)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.is_file() or p.suffix.lower() not in VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L54)

**오류 메시지:** 영상 파일이 없습니다.

**거부 조건:** [`p.stat().st_size == 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L60)

**오류 메시지:** 0바이트 파일입니다. 원본 영상을 다시 복사하세요.

**거부 조건:** [`kind == 'improve' and (ROOT/'experiment_plan.json').exists()`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L77)

**오류 메시지:** 이미 시작한 3차 실험입니다. 중복 학습 대신 현재 작업을 확인하세요.

**거부 조건:** [`kind not in ['improve','detect']`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L80)

**오류 메시지:** 지원하지 않는 작업

**거부 조건:** [`not ok or frame is None`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L65)

**오류 메시지:** 첫 프레임을 읽을 수 없습니다. 복사 완료 여부와 코덱/파일 손상을 확인하세요.

**거부 조건:** [`not math.isfinite(fps) or fps &lt;= 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L66)

**오류 메시지:** 유효한 FPS가 없습니다. 영상을 재인코딩하세요.

**거부 조건:** [`any(j.get('state') in ['queued','running'] for j in status()['jobs'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L83)

**오류 메시지:** 진행 중인 작업이 있습니다. 완료 후 실행하세요.

**거부 조건:** [`not all(c.isalnum() or c=='_' for c in args['job'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L118)

**오류 메시지:** 잘못된 작업 ID


#### LEVEL 2 · [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py)


| 내용 |
| --- |
| **설정·옵션:** [`REF`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L9)<br>**코드의 선언:** `정의=ROOT/'data/reference'` |
| **설정·옵션:** [`FULL`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L10)<br>**코드의 선언:** `정의=ROOT/'data/full'` |
| **설정·옵션:** [`SEED`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L11)<br>**코드의 선언:** `정의=20261013` |

#### LEVEL 2 · [3차/클린뷰/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py)


**거부 조건:** [`not any(weights.is_relative_to(r.resolve()) for r in [ROOT/'runs']) or not weights.is_file() or weights.suffix!='.pt'`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L60)

**오류 메시지:** 학습된 best.pt를 선택하세요.

**거부 조건:** [`not(0&lt;=seconds&lt;=86400 and 1&lt;=abandon&lt;=600 and 0&lt;=leave&lt;=120 and .01&lt;=conf&lt;=1 and 0&lt;=baseline&lt;=60)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L63)

**오류 메시지:** 탐지 설정 범위 오류

**거부 조건:** [`any(len(m.names)!=1 or m.names[0]!='trash' for m in trash)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L73)

**오류 메시지:** 1-class trash 학습 모델이 아닙니다.

**거부 조건:** [`total&lt;=0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L77)

**오류 메시지:** 처리할 프레임이 없습니다.

**거부 조건:** [`len(roi)&lt;3 or any(len(v)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) and 0&lt;=x&lt;=1 for x in v) for v in roi)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L66)

**오류 메시지:** 구역은 0~1 좌표의 다각형이어야 합니다.


#### LEVEL 2 · [3차/클린뷰/finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L113)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L4)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DESKTOP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L5)<br>**코드의 선언:** `정의=SOURCE.parents[1]` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L6)<br>**코드의 선언:** `정의=DESKTOP/'3차'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L9)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0` |

#### LEVEL 2 · [3차/클린뷰/finish_on_exit.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py)


| 내용 |
| --- |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L5)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L6)<br>**코드의 선언:** `정의=SOURCE.parent` |
| **설정·옵션:** [`WORK`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L7)<br>**코드의 선언:** `정의=DEST / '_작업' / 'completion_once'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L8)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW` |

#### LEVEL 2 · [3차/클린뷰/launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)


**설정·옵션:** [`--no-browser`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--port`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `type=int; default=0`

**설정·옵션:** [`--self-test`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L133)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`CONTAINER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L7)

**코드의 선언:** `정의='2026-2'`

**설정·옵션:** [`ASSETS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L9)

**코드의 선언:** `정의=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))`

**설정·옵션:** [`CACHE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L11)

**코드의 선언:** `정의=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'TrashDetector3'`

**설정·옵션:** [`DOCKER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L13)

**코드의 선언:** `정의='docker'`

**설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L14)

**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0`


**거부 조건:** [`'..' in p.parts or not p.is_relative_to(PurePosixPath(REMOTE+'/results'))`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L58)

**오류 메시지:** 잘못된 결과 경로

**거부 조건:** [`not 0&lt;length&lt;1024*1024`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L121)

**오류 메시지:** 잘못된 요청 크기

**거부 조건:** [`ext not in {'.mp4','.avi','.mov','.mkv','.m4v'}`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L108)

**오류 메시지:** 지원하지 않는 영상 확장자

**거부 조건:** [`not 0&lt;length&lt;=4*1024**3`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L109)

**오류 메시지:** 파일 크기는 0 초과 4GB 이하이어야 합니다.

**거부 조건:** [`not chunk`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L116)

**오류 메시지:** 영상 업로드가 중단되었습니다.


#### LEVEL 2 · [3차/클린뷰/make_report.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py)


| 내용 |
| --- |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L10)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`OUT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L11)<br>**코드의 선언:** `정의=ROOT/'report'` |

</details>

### LEVEL 2 · 관측과 해석을 구분하기

최종 보고서의 성능은3차 고정 평가 조건에 속합니다. 상위 폴더 이름 최종이 모든 후속 차수의 최신 모델을 의미하지 않습니다.

**상황:** 실행 자료가 부족함

**확인할 내용:** 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다.

**상황:** 결과 범위 해석

**확인할 내용:** 자료 열람·기능 확인·실험 성적을 각각 구분합니다.


[자료 폴더](../../%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](../comparisons/final-container.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-3"></a>
## LEVEL 3 - Practitioner

### LEVEL 3 · 이 차수를 준비하는 범위

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다.
- 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

하위 폴더마다 자료 성격과 실행 조건이 다릅니다. 3차 실험 코드, 4차 보조 도구, 최종 HTML/CSV를 선택해서 읽습니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

#### LEVEL 3 · 이 보관본의 의존성 목록

[3차/클린뷰/requirements-docker.txt](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/requirements-docker.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
ultralytics==8.4.160
opencv-python==4.14.0.94
imageio-ffmpeg==0.6.0
requests
PyYAML
matplotlib
```

#### LEVEL 3 · 소스에서 제공하는 CLI 옵션

**진입 소스:** [finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)

**정의된 옵션 이름:** `--prepare`

**진입 소스:** [launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)

**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`

**진입 소스:** [download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)

**정의된 옵션 이름:** `--dataset_path`

**진입 소스:** [detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)

**정의된 옵션 이름:** `--model`, `--dataset`, `--round`, `--lrate`, `--use_aug`, `--use_transplants`, `--class_map`

**진입 소스:** [split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)

**정의된 옵션 이름:** `--dataset_dir`, `--test_percentage`, `--val_percentage`, `--nr_trials`


각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 3 · [3차/데이터/taco/detector/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)


**설정·옵션:** [`command`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L201)

**코드의 선언:** `help="Opt: 'train', 'evaluate', 'test'"`

**설정·옵션:** [`--model`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L202)

**코드의 선언:** `required=True; help="Path to weights .h5 file or 'coco'"`

**설정·옵션:** [`--dataset`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L203)

**코드의 선언:** `required=True; help='Directory of the dataset'`

**설정·옵션:** [`--round`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L204)

**코드의 선언:** `required=True; type=int; help='Split number'`

**설정·옵션:** [`--lrate`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L205)

**코드의 선언:** `required=False; default=0.001; type=float; help='learning rate'`

**설정·옵션:** [`--use_aug`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L206)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--use_transplants`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L208)

**코드의 선언:** `required=False; default=None; help='Path to transplanted dataset'`

**설정·옵션:** [`--class_map`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L209)

**코드의 선언:** `required=True; help=' Target classes'`

**설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L60)

**코드의 선언:** `정의=os.path.abspath("./models")`

**설정·옵션:** [`COCO_MODEL_PATH`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L63)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")`

**설정·옵션:** [`DEFAULT_LOGS_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L66)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "logs")`


#### LEVEL 3 · [3차/데이터/taco/detector/split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)


**설정·옵션:** [`--dataset_dir`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L10)

**코드의 선언:** `required=True; help='Path to dataset annotations'`

**설정·옵션:** [`--test_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L11)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the testing set'`

**설정·옵션:** [`--val_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L12)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the validation set'`

**설정·옵션:** [`--nr_trials`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L13)

**코드의 선언:** `type=int; default=10; required=False; help='Number of splits'`


#### LEVEL 3 · [3차/데이터/taco/detector/visualize.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py#L25)<br>**코드의 선언:** `정의=os.path.abspath("../")` |

#### LEVEL 3 · [3차/데이터/taco/download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)


**설정·옵션:** [`--dataset_path`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py#L15)

**코드의 선언:** `required=False; default='./data/annotations.json'; help='Path to annotations'`


#### LEVEL 3 · [3차/클린뷰/backend.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L6)<br>**코드의 선언:** `정의=BASE / 'trash_round3'` |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L7)<br>**코드의 선언:** `정의=ROOT / 'app'` |
| **설정·옵션:** [`STATE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L8)<br>**코드의 선언:** `정의=APP / 'state'` |
| **설정·옵션:** [`JOBS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L9)<br>**코드의 선언:** `정의=STATE / 'jobs'` |
| **설정·옵션:** [`VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L10)<br>**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v'}` |

**거부 조건:** [`not any(p.is_relative_to(r.resolve()) for r in [ROOT/'videos',APP/'uploads'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L52)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.is_file() or p.suffix.lower() not in VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L54)

**오류 메시지:** 영상 파일이 없습니다.

**거부 조건:** [`p.stat().st_size == 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L60)

**오류 메시지:** 0바이트 파일입니다. 원본 영상을 다시 복사하세요.

**거부 조건:** [`kind == 'improve' and (ROOT/'experiment_plan.json').exists()`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L77)

**오류 메시지:** 이미 시작한 3차 실험입니다. 중복 학습 대신 현재 작업을 확인하세요.

**거부 조건:** [`kind not in ['improve','detect']`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L80)

**오류 메시지:** 지원하지 않는 작업

**거부 조건:** [`not ok or frame is None`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L65)

**오류 메시지:** 첫 프레임을 읽을 수 없습니다. 복사 완료 여부와 코덱/파일 손상을 확인하세요.

**거부 조건:** [`not math.isfinite(fps) or fps &lt;= 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L66)

**오류 메시지:** 유효한 FPS가 없습니다. 영상을 재인코딩하세요.

**거부 조건:** [`any(j.get('state') in ['queued','running'] for j in status()['jobs'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L83)

**오류 메시지:** 진행 중인 작업이 있습니다. 완료 후 실행하세요.

**거부 조건:** [`not all(c.isalnum() or c=='_' for c in args['job'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L118)

**오류 메시지:** 잘못된 작업 ID


#### LEVEL 3 · [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py)


| 내용 |
| --- |
| **설정·옵션:** [`REF`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L9)<br>**코드의 선언:** `정의=ROOT/'data/reference'` |
| **설정·옵션:** [`FULL`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L10)<br>**코드의 선언:** `정의=ROOT/'data/full'` |
| **설정·옵션:** [`SEED`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L11)<br>**코드의 선언:** `정의=20261013` |

#### LEVEL 3 · [3차/클린뷰/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py)


**거부 조건:** [`not any(weights.is_relative_to(r.resolve()) for r in [ROOT/'runs']) or not weights.is_file() or weights.suffix!='.pt'`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L60)

**오류 메시지:** 학습된 best.pt를 선택하세요.

**거부 조건:** [`not(0&lt;=seconds&lt;=86400 and 1&lt;=abandon&lt;=600 and 0&lt;=leave&lt;=120 and .01&lt;=conf&lt;=1 and 0&lt;=baseline&lt;=60)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L63)

**오류 메시지:** 탐지 설정 범위 오류

**거부 조건:** [`any(len(m.names)!=1 or m.names[0]!='trash' for m in trash)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L73)

**오류 메시지:** 1-class trash 학습 모델이 아닙니다.

**거부 조건:** [`total&lt;=0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L77)

**오류 메시지:** 처리할 프레임이 없습니다.

**거부 조건:** [`len(roi)&lt;3 or any(len(v)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) and 0&lt;=x&lt;=1 for x in v) for v in roi)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L66)

**오류 메시지:** 구역은 0~1 좌표의 다각형이어야 합니다.


#### LEVEL 3 · [3차/클린뷰/finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L113)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L4)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DESKTOP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L5)<br>**코드의 선언:** `정의=SOURCE.parents[1]` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L6)<br>**코드의 선언:** `정의=DESKTOP/'3차'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L9)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0` |

#### LEVEL 3 · [3차/클린뷰/finish_on_exit.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py)


| 내용 |
| --- |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L5)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L6)<br>**코드의 선언:** `정의=SOURCE.parent` |
| **설정·옵션:** [`WORK`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L7)<br>**코드의 선언:** `정의=DEST / '_작업' / 'completion_once'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L8)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW` |

#### LEVEL 3 · [3차/클린뷰/launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)


**설정·옵션:** [`--no-browser`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--port`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `type=int; default=0`

**설정·옵션:** [`--self-test`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L133)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`CONTAINER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L7)

**코드의 선언:** `정의='2026-2'`

**설정·옵션:** [`ASSETS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L9)

**코드의 선언:** `정의=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))`

**설정·옵션:** [`CACHE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L11)

**코드의 선언:** `정의=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'TrashDetector3'`

**설정·옵션:** [`DOCKER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L13)

**코드의 선언:** `정의='docker'`

**설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L14)

**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0`


**거부 조건:** [`'..' in p.parts or not p.is_relative_to(PurePosixPath(REMOTE+'/results'))`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L58)

**오류 메시지:** 잘못된 결과 경로

**거부 조건:** [`not 0&lt;length&lt;1024*1024`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L121)

**오류 메시지:** 잘못된 요청 크기

**거부 조건:** [`ext not in {'.mp4','.avi','.mov','.mkv','.m4v'}`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L108)

**오류 메시지:** 지원하지 않는 영상 확장자

**거부 조건:** [`not 0&lt;length&lt;=4*1024**3`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L109)

**오류 메시지:** 파일 크기는 0 초과 4GB 이하이어야 합니다.

**거부 조건:** [`not chunk`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L116)

**오류 메시지:** 영상 업로드가 중단되었습니다.


#### LEVEL 3 · [3차/클린뷰/make_report.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py)


| 내용 |
| --- |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L10)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`OUT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L11)<br>**코드의 선언:** `정의=ROOT/'report'` |

</details>

### LEVEL 3 · 실제 사용·실험 순서

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

**단계:** 입력

**내용:** 하위3차·4차·최종의 코드·기록·보고서

**단계:** 처리

**내용:** 실험 구성과 단일 프레임, 최종 성능보고서를 각각 연결

**단계:** 출력

**내용:** 자료별 설명과 원본 탐색


### LEVEL 3 · 결과와 실패를 확인하기

최종 보고서의 성능은3차 고정 평가 조건에 속합니다. 상위 폴더 이름 최종이 모든 후속 차수의 최신 모델을 의미하지 않습니다.

**상황:** 실행 자료가 부족함

**확인할 내용:** 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다.

**상황:** 결과 범위 해석

**확인할 내용:** 자료 열람·기능 확인·실험 성적을 각각 구분합니다.


### LEVEL 3 · 실행 전 대조할 차수 조건

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다. - 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

하위 3차·4차·최종을 포함하는 컨테이너입니다. 파일 수 표의 최종 52개와 하위 파일을 중복 합산하지 않습니다.

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다.

최종 폴더에는 학습·추론 코드, 설명 이미지와 성능보고서를 함께 정리했습니다.

[자료 폴더](../../%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](../comparisons/final-container.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-4"></a>
## LEVEL 4 - Advanced

### LEVEL 4 · 설계 의도와 검토 경계

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다.
- 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다. - 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

하위 3차·4차·최종을 포함하는 컨테이너입니다. 파일 수 표의 최종 52개와 하위 파일을 중복 합산하지 않습니다.

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다.

최종 폴더에는 학습·추론 코드, 설명 이미지와 성능보고서를 함께 정리했습니다.

### LEVEL 4 · 이 차수 구현의 실제 근거

**파일:** [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py)

**원문에 정의된 역할·구성:** Round 3: fixed photo identities, original-resolution inputs, new labelled data.

**파일:** [3차/클린뷰/inference.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/inference.py)

**원문에 정의된 역할·구성:** Identical full-image / overlapping-tile inference for evaluation and the app.

**파일:** [3차/클린뷰/train_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/train_round3.py)

**원문에 정의된 역할·구성:** New architectures, dataset expansion, focused refinement, validation-only selection.

**파일:** [3차/_작업/check_external_archive.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_external_archive.py)

**원문에 정의된 역할·구성:** 소스 본문과 설정을 함께 읽는 구성요소

**파일:** [3차/_작업/check_models.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_models.py)

**원문에 정의된 역할·구성:** 정의: `collect`

**파일:** [3차/_작업/check_report_contract.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_report_contract.py)

**원문에 정의된 역할·구성:** Synthetic report-format check; never evaluates or writes the real test split.

**파일:** [3차/_작업/migrate_inputs.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/migrate_inputs.py)

**원문에 정의된 역할·구성:** Move reusable inputs; verify identity before removing obsolete experiment trees.

**파일:** [3차/_작업/save_results_now.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/save_results_now.py)

**원문에 정의된 역할·구성:** Save finished results without filling the system drive with new training photos.

**파일:** [3차/_작업/wait_code.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/wait_code.py)

**원문에 정의된 역할·구성:** 소스 본문과 설정을 함께 읽는 구성요소


**단계:** 입력

**내용:** 하위3차·4차·최종의 코드·기록·보고서

**단계:** 처리

**내용:** 실험 구성과 단일 프레임, 최종 성능보고서를 각각 연결

**단계:** 출력

**내용:** 자료별 설명과 원본 탐색


### LEVEL 4 · 조건·변경·결과를 함께 검토하기

하위 폴더마다 자료 성격과 실행 조건이 다릅니다. 3차 실험 코드, 4차 보조 도구, 최종 HTML/CSV를 선택해서 읽습니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

#### LEVEL 4 · 이 보관본의 의존성 목록

[3차/클린뷰/requirements-docker.txt](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/requirements-docker.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
ultralytics==8.4.160
opencv-python==4.14.0.94
imageio-ffmpeg==0.6.0
requests
PyYAML
matplotlib
```

#### LEVEL 4 · 소스에서 제공하는 CLI 옵션

**진입 소스:** [finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)

**정의된 옵션 이름:** `--prepare`

**진입 소스:** [launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)

**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`

**진입 소스:** [download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)

**정의된 옵션 이름:** `--dataset_path`

**진입 소스:** [detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)

**정의된 옵션 이름:** `--model`, `--dataset`, `--round`, `--lrate`, `--use_aug`, `--use_transplants`, `--class_map`

**진입 소스:** [split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)

**정의된 옵션 이름:** `--dataset_dir`, `--test_percentage`, `--val_percentage`, `--nr_trials`


각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 4 · [3차/데이터/taco/detector/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)


**설정·옵션:** [`command`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L201)

**코드의 선언:** `help="Opt: 'train', 'evaluate', 'test'"`

**설정·옵션:** [`--model`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L202)

**코드의 선언:** `required=True; help="Path to weights .h5 file or 'coco'"`

**설정·옵션:** [`--dataset`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L203)

**코드의 선언:** `required=True; help='Directory of the dataset'`

**설정·옵션:** [`--round`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L204)

**코드의 선언:** `required=True; type=int; help='Split number'`

**설정·옵션:** [`--lrate`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L205)

**코드의 선언:** `required=False; default=0.001; type=float; help='learning rate'`

**설정·옵션:** [`--use_aug`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L206)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--use_transplants`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L208)

**코드의 선언:** `required=False; default=None; help='Path to transplanted dataset'`

**설정·옵션:** [`--class_map`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L209)

**코드의 선언:** `required=True; help=' Target classes'`

**설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L60)

**코드의 선언:** `정의=os.path.abspath("./models")`

**설정·옵션:** [`COCO_MODEL_PATH`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L63)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")`

**설정·옵션:** [`DEFAULT_LOGS_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L66)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "logs")`


#### LEVEL 4 · [3차/데이터/taco/detector/split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)


**설정·옵션:** [`--dataset_dir`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L10)

**코드의 선언:** `required=True; help='Path to dataset annotations'`

**설정·옵션:** [`--test_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L11)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the testing set'`

**설정·옵션:** [`--val_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L12)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the validation set'`

**설정·옵션:** [`--nr_trials`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L13)

**코드의 선언:** `type=int; default=10; required=False; help='Number of splits'`


#### LEVEL 4 · [3차/데이터/taco/detector/visualize.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py#L25)<br>**코드의 선언:** `정의=os.path.abspath("../")` |

#### LEVEL 4 · [3차/데이터/taco/download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)


**설정·옵션:** [`--dataset_path`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py#L15)

**코드의 선언:** `required=False; default='./data/annotations.json'; help='Path to annotations'`


#### LEVEL 4 · [3차/클린뷰/backend.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L6)<br>**코드의 선언:** `정의=BASE / 'trash_round3'` |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L7)<br>**코드의 선언:** `정의=ROOT / 'app'` |
| **설정·옵션:** [`STATE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L8)<br>**코드의 선언:** `정의=APP / 'state'` |
| **설정·옵션:** [`JOBS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L9)<br>**코드의 선언:** `정의=STATE / 'jobs'` |
| **설정·옵션:** [`VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L10)<br>**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v'}` |

**거부 조건:** [`not any(p.is_relative_to(r.resolve()) for r in [ROOT/'videos',APP/'uploads'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L52)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.is_file() or p.suffix.lower() not in VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L54)

**오류 메시지:** 영상 파일이 없습니다.

**거부 조건:** [`p.stat().st_size == 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L60)

**오류 메시지:** 0바이트 파일입니다. 원본 영상을 다시 복사하세요.

**거부 조건:** [`kind == 'improve' and (ROOT/'experiment_plan.json').exists()`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L77)

**오류 메시지:** 이미 시작한 3차 실험입니다. 중복 학습 대신 현재 작업을 확인하세요.

**거부 조건:** [`kind not in ['improve','detect']`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L80)

**오류 메시지:** 지원하지 않는 작업

**거부 조건:** [`not ok or frame is None`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L65)

**오류 메시지:** 첫 프레임을 읽을 수 없습니다. 복사 완료 여부와 코덱/파일 손상을 확인하세요.

**거부 조건:** [`not math.isfinite(fps) or fps &lt;= 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L66)

**오류 메시지:** 유효한 FPS가 없습니다. 영상을 재인코딩하세요.

**거부 조건:** [`any(j.get('state') in ['queued','running'] for j in status()['jobs'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L83)

**오류 메시지:** 진행 중인 작업이 있습니다. 완료 후 실행하세요.

**거부 조건:** [`not all(c.isalnum() or c=='_' for c in args['job'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L118)

**오류 메시지:** 잘못된 작업 ID


#### LEVEL 4 · [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py)


| 내용 |
| --- |
| **설정·옵션:** [`REF`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L9)<br>**코드의 선언:** `정의=ROOT/'data/reference'` |
| **설정·옵션:** [`FULL`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L10)<br>**코드의 선언:** `정의=ROOT/'data/full'` |
| **설정·옵션:** [`SEED`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L11)<br>**코드의 선언:** `정의=20261013` |

#### LEVEL 4 · [3차/클린뷰/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py)


**거부 조건:** [`not any(weights.is_relative_to(r.resolve()) for r in [ROOT/'runs']) or not weights.is_file() or weights.suffix!='.pt'`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L60)

**오류 메시지:** 학습된 best.pt를 선택하세요.

**거부 조건:** [`not(0&lt;=seconds&lt;=86400 and 1&lt;=abandon&lt;=600 and 0&lt;=leave&lt;=120 and .01&lt;=conf&lt;=1 and 0&lt;=baseline&lt;=60)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L63)

**오류 메시지:** 탐지 설정 범위 오류

**거부 조건:** [`any(len(m.names)!=1 or m.names[0]!='trash' for m in trash)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L73)

**오류 메시지:** 1-class trash 학습 모델이 아닙니다.

**거부 조건:** [`total&lt;=0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L77)

**오류 메시지:** 처리할 프레임이 없습니다.

**거부 조건:** [`len(roi)&lt;3 or any(len(v)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) and 0&lt;=x&lt;=1 for x in v) for v in roi)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L66)

**오류 메시지:** 구역은 0~1 좌표의 다각형이어야 합니다.


#### LEVEL 4 · [3차/클린뷰/finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L113)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L4)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DESKTOP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L5)<br>**코드의 선언:** `정의=SOURCE.parents[1]` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L6)<br>**코드의 선언:** `정의=DESKTOP/'3차'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L9)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0` |

#### LEVEL 4 · [3차/클린뷰/finish_on_exit.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py)


| 내용 |
| --- |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L5)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L6)<br>**코드의 선언:** `정의=SOURCE.parent` |
| **설정·옵션:** [`WORK`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L7)<br>**코드의 선언:** `정의=DEST / '_작업' / 'completion_once'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L8)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW` |

#### LEVEL 4 · [3차/클린뷰/launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)


**설정·옵션:** [`--no-browser`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--port`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `type=int; default=0`

**설정·옵션:** [`--self-test`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L133)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`CONTAINER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L7)

**코드의 선언:** `정의='2026-2'`

**설정·옵션:** [`ASSETS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L9)

**코드의 선언:** `정의=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))`

**설정·옵션:** [`CACHE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L11)

**코드의 선언:** `정의=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'TrashDetector3'`

**설정·옵션:** [`DOCKER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L13)

**코드의 선언:** `정의='docker'`

**설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L14)

**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0`


**거부 조건:** [`'..' in p.parts or not p.is_relative_to(PurePosixPath(REMOTE+'/results'))`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L58)

**오류 메시지:** 잘못된 결과 경로

**거부 조건:** [`not 0&lt;length&lt;1024*1024`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L121)

**오류 메시지:** 잘못된 요청 크기

**거부 조건:** [`ext not in {'.mp4','.avi','.mov','.mkv','.m4v'}`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L108)

**오류 메시지:** 지원하지 않는 영상 확장자

**거부 조건:** [`not 0&lt;length&lt;=4*1024**3`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L109)

**오류 메시지:** 파일 크기는 0 초과 4GB 이하이어야 합니다.

**거부 조건:** [`not chunk`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L116)

**오류 메시지:** 영상 업로드가 중단되었습니다.


#### LEVEL 4 · [3차/클린뷰/make_report.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py)


| 내용 |
| --- |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L10)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`OUT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L11)<br>**코드의 선언:** `정의=ROOT/'report'` |

</details>

최종 보고서의 성능은3차 고정 평가 조건에 속합니다. 상위 폴더 이름 최종이 모든 후속 차수의 최신 모델을 의미하지 않습니다.

**상황:** 실행 자료가 부족함

**확인할 내용:** 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다.

**상황:** 결과 범위 해석

**확인할 내용:** 자료 열람·기능 확인·실험 성적을 각각 구분합니다.


### LEVEL 4 · 재현과 전체 비교

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

위 구성요소의 입력·출력과 실패 조건을 같은 차수 소스에 연결해 검토합니다. 전체 비교는 추가·수정·삭제와 원래 보관 범위를 구분하는 근거입니다.

[자료 폴더](../../%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](../comparisons/final-container.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<a id="reading-level-5"></a>
## LEVEL 5 - Expert

기존의 전체 설명·표·코드·함수 참조·파일별 비교는 아래에 그대로 이어집니다. [자료 폴더](../../%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](../comparisons/final-container.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<!-- reading-levels:end -->



[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../%EC%B5%9C%EC%A2%85)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다.
- 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

**항목:** 1

**이 차수에서 확인할 내용:** - 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다. - 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

**항목:** 2

**이 차수에서 확인할 내용:** 하위 3차·4차·최종을 포함하는 컨테이너입니다. 파일 수 표의 최종 52개와 하위 파일을 중복 합산하지 않습니다.

**항목:** 3

**이 차수에서 확인할 내용:** 셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다.

**항목:** 4

**이 차수에서 확인할 내용:** 최종 폴더에는 학습·추론 코드, 설명 이미지와 성능보고서를 함께 정리했습니다.


<a name="-입력처리출력"></a>
## 입력·처리·출력

**단계:** 입력

**내용:** 하위3차·4차·최종의 코드·기록·보고서

**단계:** 처리

**내용:** 실험 구성과 단일 프레임, 최종 성능보고서를 각각 연결

**단계:** 출력

**내용:** 자료별 설명과 원본 탐색


<a name="usage"></a>

<a name="️-화면과-사용-흐름"></a>
## 화면과 사용 흐름

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

<a name="structure"></a>

<a name="-실제-자료-구성"></a>
## 실제 자료 구성

| 내용 |
| --- |
| **경로:** [3차/](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [4차/](../../%EC%B5%9C%EC%A2%85/4%EC%B0%A8)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [최종/](../../%EC%B5%9C%EC%A2%85/%EC%B5%9C%EC%A2%85)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [폴더안내.txt](../../%EC%B5%9C%EC%A2%85/%ED%8F%B4%EB%8D%94%EC%95%88%EB%82%B4.txt)<br>**자료 종류:** TXT 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

**파일:** [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py)

**원문에 정의된 역할·구성:** Round 3: fixed photo identities, original-resolution inputs, new labelled data.

**파일:** [3차/클린뷰/inference.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/inference.py)

**원문에 정의된 역할·구성:** Identical full-image / overlapping-tile inference for evaluation and the app.

**파일:** [3차/클린뷰/train_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/train_round3.py)

**원문에 정의된 역할·구성:** New architectures, dataset expansion, focused refinement, validation-only selection.

**파일:** [3차/_작업/check_external_archive.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_external_archive.py)

**원문에 정의된 역할·구성:** 소스 본문과 설정을 함께 읽는 구성요소

**파일:** [3차/_작업/check_models.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_models.py)

**원문에 정의된 역할·구성:** 정의: `collect`

**파일:** [3차/_작업/check_report_contract.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_report_contract.py)

**원문에 정의된 역할·구성:** Synthetic report-format check; never evaluates or writes the real test split.

**파일:** [3차/_작업/migrate_inputs.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/migrate_inputs.py)

**원문에 정의된 역할·구성:** Move reusable inputs; verify identity before removing obsolete experiment trees.

**파일:** [3차/_작업/save_results_now.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/save_results_now.py)

**원문에 정의된 역할·구성:** Save finished results without filling the system drive with new training photos.

**파일:** [3차/_작업/wait_code.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/wait_code.py)

**원문에 정의된 역할·구성:** 소스 본문과 설정을 함께 읽는 구성요소


<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

하위 폴더마다 자료 성격과 실행 조건이 다릅니다. 3차 실험 코드, 4차 보조 도구, 최종 HTML/CSV를 선택해서 읽습니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

<a name="-이-보관본의-의존성-목록"></a>
### 이 보관본의 의존성 목록

[3차/클린뷰/requirements-docker.txt](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/requirements-docker.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
ultralytics==8.4.160
opencv-python==4.14.0.94
imageio-ffmpeg==0.6.0
requests
PyYAML
matplotlib
```

<a name="️-소스에서-제공하는-cli-옵션"></a>
### 소스에서 제공하는 CLI 옵션

**진입 소스:** [finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)

**정의된 옵션 이름:** `--prepare`

**진입 소스:** [launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)

**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`

**진입 소스:** [download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)

**정의된 옵션 이름:** `--dataset_path`

**진입 소스:** [detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)

**정의된 옵션 이름:** `--model`, `--dataset`, `--round`, `--lrate`, `--use_aug`, `--use_transplants`, `--class_map`

**진입 소스:** [split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)

**정의된 옵션 이름:** `--dataset_dir`, `--test_percentage`, `--val_percentage`, `--nr_trials`


각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [3차/데이터/taco/detector/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)


**설정·옵션:** [`command`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L201)

**코드의 선언:** `help="Opt: 'train', 'evaluate', 'test'"`

**설정·옵션:** [`--model`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L202)

**코드의 선언:** `required=True; help="Path to weights .h5 file or 'coco'"`

**설정·옵션:** [`--dataset`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L203)

**코드의 선언:** `required=True; help='Directory of the dataset'`

**설정·옵션:** [`--round`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L204)

**코드의 선언:** `required=True; type=int; help='Split number'`

**설정·옵션:** [`--lrate`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L205)

**코드의 선언:** `required=False; default=0.001; type=float; help='learning rate'`

**설정·옵션:** [`--use_aug`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L206)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--use_transplants`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L208)

**코드의 선언:** `required=False; default=None; help='Path to transplanted dataset'`

**설정·옵션:** [`--class_map`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L209)

**코드의 선언:** `required=True; help=' Target classes'`

**설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L60)

**코드의 선언:** `정의=os.path.abspath("./models")`

**설정·옵션:** [`COCO_MODEL_PATH`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L63)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")`

**설정·옵션:** [`DEFAULT_LOGS_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L66)

**코드의 선언:** `정의=os.path.join(ROOT_DIR, "logs")`


### [3차/데이터/taco/detector/split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)


**설정·옵션:** [`--dataset_dir`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L10)

**코드의 선언:** `required=True; help='Path to dataset annotations'`

**설정·옵션:** [`--test_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L11)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the testing set'`

**설정·옵션:** [`--val_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L12)

**코드의 선언:** `type=int; default=10; required=False; help='Percentage of images used for the validation set'`

**설정·옵션:** [`--nr_trials`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L13)

**코드의 선언:** `type=int; default=10; required=False; help='Number of splits'`


### [3차/데이터/taco/detector/visualize.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py#L25)<br>**코드의 선언:** `정의=os.path.abspath("../")` |

### [3차/데이터/taco/download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)


**설정·옵션:** [`--dataset_path`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py#L15)

**코드의 선언:** `required=False; default='./data/annotations.json'; help='Path to annotations'`


### [3차/클린뷰/backend.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L6)<br>**코드의 선언:** `정의=BASE / 'trash_round3'` |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L7)<br>**코드의 선언:** `정의=ROOT / 'app'` |
| **설정·옵션:** [`STATE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L8)<br>**코드의 선언:** `정의=APP / 'state'` |
| **설정·옵션:** [`JOBS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L9)<br>**코드의 선언:** `정의=STATE / 'jobs'` |
| **설정·옵션:** [`VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L10)<br>**코드의 선언:** `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v'}` |

**거부 조건:** [`not any(p.is_relative_to(r.resolve()) for r in [ROOT/'videos',APP/'uploads'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L52)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.is_file() or p.suffix.lower() not in VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L54)

**오류 메시지:** 영상 파일이 없습니다.

**거부 조건:** [`p.stat().st_size == 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L60)

**오류 메시지:** 0바이트 파일입니다. 원본 영상을 다시 복사하세요.

**거부 조건:** [`kind == 'improve' and (ROOT/'experiment_plan.json').exists()`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L77)

**오류 메시지:** 이미 시작한 3차 실험입니다. 중복 학습 대신 현재 작업을 확인하세요.

**거부 조건:** [`kind not in ['improve','detect']`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L80)

**오류 메시지:** 지원하지 않는 작업

**거부 조건:** [`not ok or frame is None`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L65)

**오류 메시지:** 첫 프레임을 읽을 수 없습니다. 복사 완료 여부와 코덱/파일 손상을 확인하세요.

**거부 조건:** [`not math.isfinite(fps) or fps &lt;= 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L66)

**오류 메시지:** 유효한 FPS가 없습니다. 영상을 재인코딩하세요.

**거부 조건:** [`any(j.get('state') in ['queued','running'] for j in status()['jobs'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L83)

**오류 메시지:** 진행 중인 작업이 있습니다. 완료 후 실행하세요.

**거부 조건:** [`not all(c.isalnum() or c=='_' for c in args['job'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L118)

**오류 메시지:** 잘못된 작업 ID


### [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py)


| 내용 |
| --- |
| **설정·옵션:** [`REF`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L9)<br>**코드의 선언:** `정의=ROOT/'data/reference'` |
| **설정·옵션:** [`FULL`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L10)<br>**코드의 선언:** `정의=ROOT/'data/full'` |
| **설정·옵션:** [`SEED`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L11)<br>**코드의 선언:** `정의=20261013` |

### [3차/클린뷰/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py)


**거부 조건:** [`not any(weights.is_relative_to(r.resolve()) for r in [ROOT/'runs']) or not weights.is_file() or weights.suffix!='.pt'`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L60)

**오류 메시지:** 학습된 best.pt를 선택하세요.

**거부 조건:** [`not(0&lt;=seconds&lt;=86400 and 1&lt;=abandon&lt;=600 and 0&lt;=leave&lt;=120 and .01&lt;=conf&lt;=1 and 0&lt;=baseline&lt;=60)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L63)

**오류 메시지:** 탐지 설정 범위 오류

**거부 조건:** [`any(len(m.names)!=1 or m.names[0]!='trash' for m in trash)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L73)

**오류 메시지:** 1-class trash 학습 모델이 아닙니다.

**거부 조건:** [`total&lt;=0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L77)

**오류 메시지:** 처리할 프레임이 없습니다.

**거부 조건:** [`len(roi)&lt;3 or any(len(v)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) and 0&lt;=x&lt;=1 for x in v) for v in roi)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L66)

**오류 메시지:** 구역은 0~1 좌표의 다각형이어야 합니다.


### [3차/클린뷰/finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)


| 내용 |
| --- |
| **설정·옵션:** [`--prepare`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L113)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L4)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DESKTOP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L5)<br>**코드의 선언:** `정의=SOURCE.parents[1]` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L6)<br>**코드의 선언:** `정의=DESKTOP/'3차'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L9)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0` |

### [3차/클린뷰/finish_on_exit.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py)


| 내용 |
| --- |
| **설정·옵션:** [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L5)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L6)<br>**코드의 선언:** `정의=SOURCE.parent` |
| **설정·옵션:** [`WORK`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L7)<br>**코드의 선언:** `정의=DEST / '_작업' / 'completion_once'` |
| **설정·옵션:** [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L8)<br>**코드의 선언:** `정의='20261013_060956_6d373b'` |
| **설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L10)<br>**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW` |

### [3차/클린뷰/launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)


**설정·옵션:** [`--no-browser`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--port`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132)

**코드의 선언:** `type=int; default=0`

**설정·옵션:** [`--self-test`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L133)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`CONTAINER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L7)

**코드의 선언:** `정의='2026-2'`

**설정·옵션:** [`ASSETS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L9)

**코드의 선언:** `정의=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))`

**설정·옵션:** [`CACHE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L11)

**코드의 선언:** `정의=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'TrashDetector3'`

**설정·옵션:** [`DOCKER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L13)

**코드의 선언:** `정의='docker'`

**설정·옵션:** [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L14)

**코드의 선언:** `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0`


**거부 조건:** [`'..' in p.parts or not p.is_relative_to(PurePosixPath(REMOTE+'/results'))`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L58)

**오류 메시지:** 잘못된 결과 경로

**거부 조건:** [`not 0&lt;length&lt;1024*1024`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L121)

**오류 메시지:** 잘못된 요청 크기

**거부 조건:** [`ext not in {'.mp4','.avi','.mov','.mkv','.m4v'}`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L108)

**오류 메시지:** 지원하지 않는 영상 확장자

**거부 조건:** [`not 0&lt;length&lt;=4*1024**3`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L109)

**오류 메시지:** 파일 크기는 0 초과 4GB 이하이어야 합니다.

**거부 조건:** [`not chunk`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L116)

**오류 메시지:** 영상 업로드가 중단되었습니다.


### [3차/클린뷰/make_report.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py)


| 내용 |
| --- |
| **설정·옵션:** [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L10)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`OUT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L11)<br>**코드의 선언:** `정의=ROOT/'report'` |

</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

최종 보고서의 성능은3차 고정 평가 조건에 속합니다. 상위 폴더 이름 최종이 모든 후속 차수의 최신 모델을 의미하지 않습니다.

<a name="️-제약과-문제-해결"></a>
## 제약과 문제 해결

**상황:** 실행 자료가 부족함

**확인할 내용:** 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다.

**상황:** 결과 범위 해석

**확인할 내용:** 자료 열람·기능 확인·실험 성적을 각각 구분합니다.


<a name="changes"></a>

<a name="-직전-자료와-전체-비교"></a>
## 직전 자료와 전체 비교

이 자료의 보존 범위와 기준 파일을 연결합니다.

[전체 비교·자료 범위](../comparisons/final-container.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.
