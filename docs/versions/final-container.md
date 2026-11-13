<div align="center">

<a name="-최종"></a>
# 최종

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다.
- 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

**기술 분류:** 3차 실험·4차 보조 자료·최종 보고서 묶음

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../%EC%B5%9C%EC%A2%85)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

- 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다.
- 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

| 항목 | 이 차수에서 확인할 내용 |
|---|---|
| 1 | - 최종/3차에는 데이터 준비·학습·추론 앱 코드가 있습니다. - 최종/4차는 저장 모델의 단일 프레임 확인과 문서 렌더 작업을, 최종/최종은 보존된 3차 보고서를 담습니다. |
| 2 | 하위 3차·4차·최종을 포함하는 컨테이너입니다. 파일 수 표의 최종 52개와 하위 파일을 중복 합산하지 않습니다. |
| 3 | 셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. |
| 4 | 최종 폴더에는 학습·추론 코드, 설명 이미지와 성능보고서를 함께 정리했습니다. |

<a name="-입력처리출력"></a>
## 입력·처리·출력

| 단계 | 내용 |
|---|---|
| 입력 | 하위3차·4차·최종의 코드·기록·보고서 |
| 처리 | 실험 구성과 단일 프레임, 최종 성능보고서를 각각 연결 |
| 출력 | 자료별 설명과 원본 탐색 |

<a name="usage"></a>

<a name="️-화면과-사용-흐름"></a>
## 화면과 사용 흐름

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

<a name="structure"></a>

<a name="-실제-자료-구성"></a>
## 실제 자료 구성

| 경로 | 자료 종류 |
|---|---|
| [3차/](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8) | 하위 자료 폴더 |
| [4차/](../../%EC%B5%9C%EC%A2%85/4%EC%B0%A8) | 하위 자료 폴더 |
| [최종/](../../%EC%B5%9C%EC%A2%85/%EC%B5%9C%EC%A2%85) | 하위 자료 폴더 |
| [폴더안내.txt](../../%EC%B5%9C%EC%A2%85/%ED%8F%B4%EB%8D%94%EC%95%88%EB%82%B4.txt) | TXT 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py) | Round 3: fixed photo identities, original-resolution inputs, new labelled data. |
| [3차/클린뷰/inference.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/inference.py) | Identical full-image / overlapping-tile inference for evaluation and the app. |
| [3차/클린뷰/train_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/train_round3.py) | New architectures, dataset expansion, focused refinement, validation-only selection. |
| [3차/_작업/check_external_archive.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_external_archive.py) | 소스 본문과 설정을 함께 읽는 구성요소 |
| [3차/_작업/check_models.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_models.py) | 정의: `collect` |
| [3차/_작업/check_report_contract.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/check_report_contract.py) | Synthetic report-format check; never evaluates or writes the real test split. |
| [3차/_작업/migrate_inputs.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/migrate_inputs.py) | Move reusable inputs; verify identity before removing obsolete experiment trees. |
| [3차/_작업/save_results_now.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/save_results_now.py) | Save finished results without filling the system drive with new training photos. |
| [3차/_작업/wait_code.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/_%EC%9E%91%EC%97%85/wait_code.py) | 소스 본문과 설정을 함께 읽는 구성요소 |

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

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py) | `--prepare` |
| [launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py) | `--no-browser`, `--port`, `--self-test` |
| [download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py) | `--dataset_path` |
| [detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py) | `--model`, `--dataset`, `--round`, `--lrate`, `--use_aug`, `--use_transplants`, `--class_map` |
| [split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py) | `--dataset_dir`, `--test_percentage`, `--val_percentage`, `--nr_trials` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [3차/데이터/taco/detector/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`command`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L201) | `help="Opt: 'train', 'evaluate', 'test'"` |
| [`--model`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L202) | `required=True; help="Path to weights .h5 file or 'coco'"` |
| [`--dataset`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L203) | `required=True; help='Directory of the dataset'` |
| [`--round`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L204) | `required=True; type=int; help='Split number'` |
| [`--lrate`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L205) | `required=False; default=0.001; type=float; help='learning rate'` |
| [`--use_aug`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L206) | `action='store_true'` |
| [`--use_transplants`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L208) | `required=False; default=None; help='Path to transplanted dataset'` |
| [`--class_map`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L209) | `required=True; help=' Target classes'` |
| [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L60) | `정의=os.path.abspath("./models")` |
| [`COCO_MODEL_PATH`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L63) | `정의=os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")` |
| [`DEFAULT_LOGS_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/detector.py#L66) | `정의=os.path.join(ROOT_DIR, "logs")` |

### [3차/데이터/taco/detector/split_dataset.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--dataset_dir`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L10) | `required=True; help='Path to dataset annotations'` |
| [`--test_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L11) | `type=int; default=10; required=False; help='Percentage of images used for the testing set'` |
| [`--val_percentage`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L12) | `type=int; default=10; required=False; help='Percentage of images used for the validation set'` |
| [`--nr_trials`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/split_dataset.py#L13) | `type=int; default=10; required=False; help='Number of splits'` |

### [3차/데이터/taco/detector/visualize.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT_DIR`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/detector/visualize.py#L25) | `정의=os.path.abspath("../")` |

### [3차/데이터/taco/download.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--dataset_path`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%EB%8D%B0%EC%9D%B4%ED%84%B0/taco/download.py#L15) | `required=False; default='./data/annotations.json'; help='Path to annotations'` |

### [3차/클린뷰/backend.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L6) | `정의=BASE / 'trash_round3'` |
| [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L7) | `정의=ROOT / 'app'` |
| [`STATE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L8) | `정의=APP / 'state'` |
| [`JOBS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L9) | `정의=STATE / 'jobs'` |
| [`VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L10) | `정의={'.mp4', '.avi', '.mov', '.mkv', '.m4v'}` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not any(p.is_relative_to(r.resolve()) for r in [ROOT/'videos',APP/'uploads'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L52) | 허용된 영상 폴더가 아닙니다. |
| [`not p.is_file() or p.suffix.lower() not in VIDEO_EXT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L54) | 영상 파일이 없습니다. |
| [`p.stat().st_size == 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L60) | 0바이트 파일입니다. 원본 영상을 다시 복사하세요. |
| [`kind == 'improve' and (ROOT/'experiment_plan.json').exists()`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L77) | 이미 시작한 3차 실험입니다. 중복 학습 대신 현재 작업을 확인하세요. |
| [`kind not in ['improve','detect']`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L80) | 지원하지 않는 작업 |
| [`not ok or frame is None`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L65) | 첫 프레임을 읽을 수 없습니다. 복사 완료 여부와 코덱/파일 손상을 확인하세요. |
| [`not math.isfinite(fps) or fps &lt;= 0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L66) | 유효한 FPS가 없습니다. 영상을 재인코딩하세요. |
| [`any(j.get('state') in ['queued','running'] for j in status()['jobs'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L83) | 진행 중인 작업이 있습니다. 완료 후 실행하세요. |
| [`not all(c.isalnum() or c=='_' for c in args['job'])`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/backend.py#L118) | 잘못된 작업 ID |

### [3차/클린뷰/data_pipeline.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`REF`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L9) | `정의=ROOT/'data/reference'` |
| [`FULL`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L10) | `정의=ROOT/'data/full'` |
| [`SEED`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/data_pipeline.py#L11) | `정의=20261013` |

### [3차/클린뷰/detector.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py)


| 거부 조건 | 오류 메시지 |
|---|---|
| [`not any(weights.is_relative_to(r.resolve()) for r in [ROOT/'runs']) or not weights.is_file() or weights.suffix!='.pt'`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L60) | 학습된 best.pt를 선택하세요. |
| [`not(0&lt;=seconds&lt;=86400 and 1&lt;=abandon&lt;=600 and 0&lt;=leave&lt;=120 and .01&lt;=conf&lt;=1 and 0&lt;=baseline&lt;=60)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L63) | 탐지 설정 범위 오류 |
| [`any(len(m.names)!=1 or m.names[0]!='trash' for m in trash)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L73) | 1-class trash 학습 모델이 아닙니다. |
| [`total&lt;=0`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L77) | 처리할 프레임이 없습니다. |
| [`len(roi)&lt;3 or any(len(v)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) and 0&lt;=x&lt;=1 for x in v) for v in roi)`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/detector.py#L66) | 구역은 0~1 좌표의 다각형이어야 합니다. |

### [3차/클린뷰/finalize_round3.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--prepare`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L113) | `action='store_true'` |
| [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L4) | `정의=Path(__file__).resolve().parent` |
| [`DESKTOP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L5) | `정의=SOURCE.parents[1]` |
| [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L6) | `정의=DESKTOP/'3차'` |
| [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L9) | `정의='20261013_060956_6d373b'` |
| [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finalize_round3.py#L10) | `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0` |

### [3차/클린뷰/finish_on_exit.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`SOURCE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L5) | `정의=Path(__file__).resolve().parent` |
| [`DEST`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L6) | `정의=SOURCE.parent` |
| [`WORK`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L7) | `정의=DEST / '_작업' / 'completion_once'` |
| [`JOB`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L8) | `정의='20261013_060956_6d373b'` |
| [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/finish_on_exit.py#L10) | `정의=subprocess.CREATE_NO_WINDOW` |

### [3차/클린뷰/launcher.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--no-browser`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132) | `action='store_true'` |
| [`--port`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L132) | `type=int; default=0` |
| [`--self-test`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L133) | `action='store_true'` |
| [`CONTAINER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L7) | `정의='2026-2'` |
| [`ASSETS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L9) | `정의=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))` |
| [`CACHE`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L11) | `정의=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'TrashDetector3'` |
| [`DOCKER`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L13) | `정의='docker'` |
| [`FLAGS`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L14) | `정의=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`'..' in p.parts or not p.is_relative_to(PurePosixPath(REMOTE+'/results'))`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L58) | 잘못된 결과 경로 |
| [`not 0&lt;length&lt;1024*1024`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L121) | 잘못된 요청 크기 |
| [`ext not in {'.mp4','.avi','.mov','.mkv','.m4v'}`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L108) | 지원하지 않는 영상 확장자 |
| [`not 0&lt;length&lt;=4*1024**3`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L109) | 파일 크기는 0 초과 4GB 이하이어야 합니다. |
| [`not chunk`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/launcher.py#L116) | 영상 업로드가 중단되었습니다. |

### [3차/클린뷰/make_report.py](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`APP`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L10) | `정의=Path(__file__).resolve().parent` |
| [`OUT`](../../%EC%B5%9C%EC%A2%85/3%EC%B0%A8/%ED%81%B4%EB%A6%B0%EB%B7%B0/make_report.py#L11) | `정의=ROOT/'report'` |

</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

최종 보고서의 성능은3차 고정 평가 조건에 속합니다. 상위 폴더 이름 최종이 모든 후속 차수의 최신 모델을 의미하지 않습니다.

<a name="️-제약과-문제-해결"></a>
## 제약과 문제 해결

| 상황 | 확인할 내용 |
|---|---|
| 실행 자료가 부족함 | 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다. |
| 결과 범위 해석 | 자료 열람·기능 확인·실험 성적을 각각 구분합니다. |

<a name="changes"></a>

<a name="-직전-자료와-전체-비교"></a>
## 직전 자료와 전체 비교

이 자료의 보존 범위와 기준 파일을 연결합니다.

[전체 비교·자료 범위](../comparisons/final-container.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.
