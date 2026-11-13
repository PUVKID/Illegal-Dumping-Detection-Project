<div align="center">

<a name="-8차"></a>
# 8차

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>
<!-- reading-levels:start -->
[LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

프로젝트 전체의 설명은 [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)부터 [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)까지 같은 범위로 연결됩니다.

<a id="reading-level-1"></a>
## LEVEL 1 - Beginner

### LEVEL 1 · 이 자료가 하는 일과 달라진 점

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

### LEVEL 1 · 실제 동작을 따라 읽기

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

CLI는 명령어와 옵션을 입력해 프로그램을 실행하는 방식입니다.

입력 — 7차 작업의 상태·진행·결과 기록

처리 — 원본 계약 확인 → 상태 읽기 → 대시보드 상태·단계 표시

출력 — 작업 진행·완료·대기·오류 화면

### LEVEL 1 · 준비하고 확인할 것

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 1 · 소스에서 제공하는 CLI 옵션

| 진입 소스 · 정의된 옵션 이름 |
| --- |
| **진입 소스:** [launcher.py](../../8%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 1 · [dashboard.py](../../8%EC%B0%A8/dashboard.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/dashboard.py#L8)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`not match`](../../8%EC%B0%A8/dashboard.py#L25)

**오류 메시지:** 7차 로그는 등록된 작업 ID만 허용합니다.

**거부 조건:** [`not any(row['id'] == job for row in records)`](../../8%EC%B0%A8/dashboard.py#L29)

**오류 메시지:** 등록되지 않은 작업 로그입니다.

**거부 조건:** [`path.parent != base or not path.is_file()`](../../8%EC%B0%A8/dashboard.py#L33)

**오류 메시지:** 허용되지 않은 작업 로그입니다.


#### LEVEL 1 · [launcher.py](../../8%EC%B0%A8/launcher.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`--no-browser`](../../8%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../8%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../8%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../8%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 거부 조건 · 오류 메시지 |
| --- |
| **거부 조건:** [`response.status != 200`](../../8%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

#### LEVEL 1 · [pipeline.py](../../8%EC%B0%A8/pipeline.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/pipeline.py#L11)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`PREVIOUS`](../../8%EC%B0%A8/pipeline.py#L12)<br>**코드의 선언:** `정의=ROOT.parent / '5차'` |
| **설정·옵션:** [`TRAINING_ROOT`](../../8%EC%B0%A8/pipeline.py#L13)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`ACTIVE`](../../8%EC%B0%A8/pipeline.py#L14)<br>**코드의 선언:** `정의={'running', 'queued', 'starting'}` |
| **설정·옵션:** [`KST`](../../8%EC%B0%A8/pipeline.py#L15)<br>**코드의 선언:** `정의=timezone(timedelta(hours=9), 'Asia/Seoul')` |

**거부 조건:** [`not isinstance(params, dict)`](../../8%EC%B0%A8/pipeline.py#L120)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`not isinstance(value, dict) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value.get('id', '')) or path.stem != value['id']`](../../8%EC%B0%A8/pipeline.py#L46)

**오류 메시지:** 작업 기록 ID와 파일명이 일치하지 않습니다.

**거부 조건:** [`not re.fullmatch(r'[A-Za-z0-9_-]+', name)`](../../8%EC%B0%A8/pipeline.py#L56)

**오류 메시지:** 학습 후보 이름이 잘못됐습니다.

**거부 조건:** [`set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../8%EC%B0%A8/pipeline.py#L125)

**오류 메시지:** resume은 명시적 참 또는 거짓만 허용합니다.

**거부 조건:** [`status()['busy']`](../../8%EC%B0%A8/pipeline.py#L127)

**오류 메시지:** 7차 자료 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`number is not None and not math.isfinite(number)`](../../8%EC%B0%A8/pipeline.py#L68)

**오류 메시지:** 학습 곡선에 유효하지 않은 값이 있습니다.


#### LEVEL 1 · [verify_sources.py](../../8%EC%B0%A8/verify_sources.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/verify_sources.py#L7)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

</details>

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

### LEVEL 1 · 결과와 주의할 범위

화면에서 읽은 상태와 실제 학습 성능을 구분합니다. 3D 단계나 진행률은 작업 상태의 표현이며 90% 정확도 달성값이 아닙니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


[자료 폴더](../../8%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/7-to-8.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-2"></a>
## LEVEL 2 - Explorer

### LEVEL 2 · 목적과 구성의 연결

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

### LEVEL 2 · 입력에서 출력으로

**단계:** 입력

**내용:** 7차 작업의 상태·진행·결과 기록

**단계:** 처리

**내용:** 원본 계약 확인 → 상태 읽기 → 대시보드 상태·단계 표시

**단계:** 출력

**내용:** 작업 진행·완료·대기·오류 화면


입력·처리·출력은 위의 같은 자료 흐름을 다른 단계에서 읽는 기준입니다. 처리 조건과 출력의 의미를 함께 확인합니다.

### LEVEL 2 · 설정과 처리 순서의 관계

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 2 · 소스에서 제공하는 CLI 옵션

| 진입 소스 · 정의된 옵션 이름 |
| --- |
| **진입 소스:** [launcher.py](../../8%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 2 · [dashboard.py](../../8%EC%B0%A8/dashboard.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/dashboard.py#L8)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`not match`](../../8%EC%B0%A8/dashboard.py#L25)

**오류 메시지:** 7차 로그는 등록된 작업 ID만 허용합니다.

**거부 조건:** [`not any(row['id'] == job for row in records)`](../../8%EC%B0%A8/dashboard.py#L29)

**오류 메시지:** 등록되지 않은 작업 로그입니다.

**거부 조건:** [`path.parent != base or not path.is_file()`](../../8%EC%B0%A8/dashboard.py#L33)

**오류 메시지:** 허용되지 않은 작업 로그입니다.


#### LEVEL 2 · [launcher.py](../../8%EC%B0%A8/launcher.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`--no-browser`](../../8%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../8%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../8%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../8%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 거부 조건 · 오류 메시지 |
| --- |
| **거부 조건:** [`response.status != 200`](../../8%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

#### LEVEL 2 · [pipeline.py](../../8%EC%B0%A8/pipeline.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/pipeline.py#L11)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`PREVIOUS`](../../8%EC%B0%A8/pipeline.py#L12)<br>**코드의 선언:** `정의=ROOT.parent / '5차'` |
| **설정·옵션:** [`TRAINING_ROOT`](../../8%EC%B0%A8/pipeline.py#L13)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`ACTIVE`](../../8%EC%B0%A8/pipeline.py#L14)<br>**코드의 선언:** `정의={'running', 'queued', 'starting'}` |
| **설정·옵션:** [`KST`](../../8%EC%B0%A8/pipeline.py#L15)<br>**코드의 선언:** `정의=timezone(timedelta(hours=9), 'Asia/Seoul')` |

**거부 조건:** [`not isinstance(params, dict)`](../../8%EC%B0%A8/pipeline.py#L120)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`not isinstance(value, dict) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value.get('id', '')) or path.stem != value['id']`](../../8%EC%B0%A8/pipeline.py#L46)

**오류 메시지:** 작업 기록 ID와 파일명이 일치하지 않습니다.

**거부 조건:** [`not re.fullmatch(r'[A-Za-z0-9_-]+', name)`](../../8%EC%B0%A8/pipeline.py#L56)

**오류 메시지:** 학습 후보 이름이 잘못됐습니다.

**거부 조건:** [`set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../8%EC%B0%A8/pipeline.py#L125)

**오류 메시지:** resume은 명시적 참 또는 거짓만 허용합니다.

**거부 조건:** [`status()['busy']`](../../8%EC%B0%A8/pipeline.py#L127)

**오류 메시지:** 7차 자료 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`number is not None and not math.isfinite(number)`](../../8%EC%B0%A8/pipeline.py#L68)

**오류 메시지:** 학습 곡선에 유효하지 않은 값이 있습니다.


#### LEVEL 2 · [verify_sources.py](../../8%EC%B0%A8/verify_sources.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/verify_sources.py#L7)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

</details>

### LEVEL 2 · 관측과 해석을 구분하기

화면에서 읽은 상태와 실제 학습 성능을 구분합니다. 3D 단계나 진행률은 작업 상태의 표현이며 90% 정확도 달성값이 아닙니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


[자료 폴더](../../8%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/7-to-8.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-3"></a>
## LEVEL 3 - Practitioner

### LEVEL 3 · 이 차수를 준비하는 범위

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 3 · 소스에서 제공하는 CLI 옵션

| 진입 소스 · 정의된 옵션 이름 |
| --- |
| **진입 소스:** [launcher.py](../../8%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 3 · [dashboard.py](../../8%EC%B0%A8/dashboard.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/dashboard.py#L8)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`not match`](../../8%EC%B0%A8/dashboard.py#L25)

**오류 메시지:** 7차 로그는 등록된 작업 ID만 허용합니다.

**거부 조건:** [`not any(row['id'] == job for row in records)`](../../8%EC%B0%A8/dashboard.py#L29)

**오류 메시지:** 등록되지 않은 작업 로그입니다.

**거부 조건:** [`path.parent != base or not path.is_file()`](../../8%EC%B0%A8/dashboard.py#L33)

**오류 메시지:** 허용되지 않은 작업 로그입니다.


#### LEVEL 3 · [launcher.py](../../8%EC%B0%A8/launcher.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`--no-browser`](../../8%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../8%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../8%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../8%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 거부 조건 · 오류 메시지 |
| --- |
| **거부 조건:** [`response.status != 200`](../../8%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

#### LEVEL 3 · [pipeline.py](../../8%EC%B0%A8/pipeline.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/pipeline.py#L11)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`PREVIOUS`](../../8%EC%B0%A8/pipeline.py#L12)<br>**코드의 선언:** `정의=ROOT.parent / '5차'` |
| **설정·옵션:** [`TRAINING_ROOT`](../../8%EC%B0%A8/pipeline.py#L13)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`ACTIVE`](../../8%EC%B0%A8/pipeline.py#L14)<br>**코드의 선언:** `정의={'running', 'queued', 'starting'}` |
| **설정·옵션:** [`KST`](../../8%EC%B0%A8/pipeline.py#L15)<br>**코드의 선언:** `정의=timezone(timedelta(hours=9), 'Asia/Seoul')` |

**거부 조건:** [`not isinstance(params, dict)`](../../8%EC%B0%A8/pipeline.py#L120)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`not isinstance(value, dict) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value.get('id', '')) or path.stem != value['id']`](../../8%EC%B0%A8/pipeline.py#L46)

**오류 메시지:** 작업 기록 ID와 파일명이 일치하지 않습니다.

**거부 조건:** [`not re.fullmatch(r'[A-Za-z0-9_-]+', name)`](../../8%EC%B0%A8/pipeline.py#L56)

**오류 메시지:** 학습 후보 이름이 잘못됐습니다.

**거부 조건:** [`set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../8%EC%B0%A8/pipeline.py#L125)

**오류 메시지:** resume은 명시적 참 또는 거짓만 허용합니다.

**거부 조건:** [`status()['busy']`](../../8%EC%B0%A8/pipeline.py#L127)

**오류 메시지:** 7차 자료 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`number is not None and not math.isfinite(number)`](../../8%EC%B0%A8/pipeline.py#L68)

**오류 메시지:** 학습 곡선에 유효하지 않은 값이 있습니다.


#### LEVEL 3 · [verify_sources.py](../../8%EC%B0%A8/verify_sources.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/verify_sources.py#L7)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

</details>

### LEVEL 3 · 실제 사용·실험 순서

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

**단계:** 입력

**내용:** 7차 작업의 상태·진행·결과 기록

**단계:** 처리

**내용:** 원본 계약 확인 → 상태 읽기 → 대시보드 상태·단계 표시

**단계:** 출력

**내용:** 작업 진행·완료·대기·오류 화면


### LEVEL 3 · 결과와 실패를 확인하기

화면에서 읽은 상태와 실제 학습 성능을 구분합니다. 3D 단계나 진행률은 작업 상태의 표현이며 90% 정확도 달성값이 아닙니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


### LEVEL 3 · 실행 전 대조할 차수 조건

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

[자료 폴더](../../8%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/7-to-8.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-4"></a>
## LEVEL 4 - Advanced

### LEVEL 4 · 설계 의도와 검토 경계

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

### LEVEL 4 · 이 차수 구현의 실제 근거

| 파일 · 원문에 정의된 역할·구성 |
| --- |
| **파일:** [dashboard.py](../../8%EC%B0%A8/dashboard.py)<br>**원문에 정의된 역할·구성:** 원래 루프백 HTTP 보안과 영상 저장 경계를 유지하는 8차 서버입니다. |
| **파일:** [launcher.py](../../8%EC%B0%A8/launcher.py)<br>**원문에 정의된 역할·구성:** 독립 대시보드 실행기입니다. 학습은 자동 시작하지 않습니다. |
| **파일:** [pipeline.py](../../8%EC%B0%A8/pipeline.py)<br>**원문에 정의된 역할·구성:** 5차 영상 파이프라인을 보존하며 7차 상태만 읽는 8차 어댑터입니다. |
| **파일:** [verify_sources.py](../../8%EC%B0%A8/verify_sources.py)<br>**원문에 정의된 역할·구성:** 배포 파일의 문자·구문과 의존 원본 불변을 검사합니다. |
| **파일:** [tests/test_adapter.py](../../8%EC%B0%A8/tests/test_adapter.py)<br>**원문에 정의된 역할·구성:** 상태 출처와 시각·중복 시작·원래 HTTP 경계를 회귀 검사합니다. |

**단계:** 입력

**내용:** 7차 작업의 상태·진행·결과 기록

**단계:** 처리

**내용:** 원본 계약 확인 → 상태 읽기 → 대시보드 상태·단계 표시

**단계:** 출력

**내용:** 작업 진행·완료·대기·오류 화면


### LEVEL 4 · 조건·변경·결과를 함께 검토하기

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 4 · 소스에서 제공하는 CLI 옵션

| 진입 소스 · 정의된 옵션 이름 |
| --- |
| **진입 소스:** [launcher.py](../../8%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 4 · [dashboard.py](../../8%EC%B0%A8/dashboard.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/dashboard.py#L8)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`not match`](../../8%EC%B0%A8/dashboard.py#L25)

**오류 메시지:** 7차 로그는 등록된 작업 ID만 허용합니다.

**거부 조건:** [`not any(row['id'] == job for row in records)`](../../8%EC%B0%A8/dashboard.py#L29)

**오류 메시지:** 등록되지 않은 작업 로그입니다.

**거부 조건:** [`path.parent != base or not path.is_file()`](../../8%EC%B0%A8/dashboard.py#L33)

**오류 메시지:** 허용되지 않은 작업 로그입니다.


#### LEVEL 4 · [launcher.py](../../8%EC%B0%A8/launcher.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`--no-browser`](../../8%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../8%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../8%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../8%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 거부 조건 · 오류 메시지 |
| --- |
| **거부 조건:** [`response.status != 200`](../../8%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

#### LEVEL 4 · [pipeline.py](../../8%EC%B0%A8/pipeline.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/pipeline.py#L11)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`PREVIOUS`](../../8%EC%B0%A8/pipeline.py#L12)<br>**코드의 선언:** `정의=ROOT.parent / '5차'` |
| **설정·옵션:** [`TRAINING_ROOT`](../../8%EC%B0%A8/pipeline.py#L13)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`ACTIVE`](../../8%EC%B0%A8/pipeline.py#L14)<br>**코드의 선언:** `정의={'running', 'queued', 'starting'}` |
| **설정·옵션:** [`KST`](../../8%EC%B0%A8/pipeline.py#L15)<br>**코드의 선언:** `정의=timezone(timedelta(hours=9), 'Asia/Seoul')` |

**거부 조건:** [`not isinstance(params, dict)`](../../8%EC%B0%A8/pipeline.py#L120)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`not isinstance(value, dict) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value.get('id', '')) or path.stem != value['id']`](../../8%EC%B0%A8/pipeline.py#L46)

**오류 메시지:** 작업 기록 ID와 파일명이 일치하지 않습니다.

**거부 조건:** [`not re.fullmatch(r'[A-Za-z0-9_-]+', name)`](../../8%EC%B0%A8/pipeline.py#L56)

**오류 메시지:** 학습 후보 이름이 잘못됐습니다.

**거부 조건:** [`set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../8%EC%B0%A8/pipeline.py#L125)

**오류 메시지:** resume은 명시적 참 또는 거짓만 허용합니다.

**거부 조건:** [`status()['busy']`](../../8%EC%B0%A8/pipeline.py#L127)

**오류 메시지:** 7차 자료 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`number is not None and not math.isfinite(number)`](../../8%EC%B0%A8/pipeline.py#L68)

**오류 메시지:** 학습 곡선에 유효하지 않은 값이 있습니다.


#### LEVEL 4 · [verify_sources.py](../../8%EC%B0%A8/verify_sources.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/verify_sources.py#L7)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

</details>

화면에서 읽은 상태와 실제 학습 성능을 구분합니다. 3D 단계나 진행률은 작업 상태의 표현이며 90% 정확도 달성값이 아닙니다.

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

[자료 폴더](../../8%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/7-to-8.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<a id="reading-level-5"></a>
## LEVEL 5 - Expert

기존의 전체 설명·표·코드·함수 참조·파일별 비교는 아래에 그대로 이어집니다. [자료 폴더](../../8%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/7-to-8.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<!-- reading-levels:end -->



[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../8%EC%B0%A8) · [← 이전: 7차](round-7.md) · [다음: 9차 →](round-9.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

**항목:** 1

**이 차수에서 확인할 내용:** 원래5차 화면 복원과7차 현재 상태 연결을 수행합니다. 한국 시각·마지막 관측·지연을 구분합니다. 기존 학습을 재시작하거나 학습 성능을 높였다는 차수가 아닙니다. 실제 변경 목록·미세 텍스트 차이·검증·공개 제외는 연결 문서에서 확인합니다.


<a name="-입력처리출력"></a>
## 입력·처리·출력

**단계:** 입력

**내용:** 7차 작업의 상태·진행·결과 기록

**단계:** 처리

**내용:** 원본 계약 확인 → 상태 읽기 → 대시보드 상태·단계 표시

**단계:** 출력

**내용:** 작업 진행·완료·대기·오류 화면


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

| 경로 · 자료 종류 |
| --- |
| **경로:** [docs/](../../8%EC%B0%A8/docs)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [tests/](../../8%EC%B0%A8/tests)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [web/](../../8%EC%B0%A8/web)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [README.md](../../8%EC%B0%A8/README.md)<br>**자료 종류:** MD 파일 |
| **경로:** [dashboard.py](../../8%EC%B0%A8/dashboard.py)<br>**자료 종류:** PY 파일 |
| **경로:** [launcher.py](../../8%EC%B0%A8/launcher.py)<br>**자료 종류:** PY 파일 |
| **경로:** [pipeline.py](../../8%EC%B0%A8/pipeline.py)<br>**자료 종류:** PY 파일 |
| **경로:** [verify_sources.py](../../8%EC%B0%A8/verify_sources.py)<br>**자료 종류:** PY 파일 |
| **경로:** [변경기록.md](../../8%EC%B0%A8/%EB%B3%80%EA%B2%BD%EA%B8%B0%EB%A1%9D.md)<br>**자료 종류:** MD 파일 |
| **경로:** [사용안내.md](../../8%EC%B0%A8/%EC%82%AC%EC%9A%A9%EC%95%88%EB%82%B4.md)<br>**자료 종류:** MD 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 파일 · 원문에 정의된 역할·구성 |
| --- |
| **파일:** [dashboard.py](../../8%EC%B0%A8/dashboard.py)<br>**원문에 정의된 역할·구성:** 원래 루프백 HTTP 보안과 영상 저장 경계를 유지하는 8차 서버입니다. |
| **파일:** [launcher.py](../../8%EC%B0%A8/launcher.py)<br>**원문에 정의된 역할·구성:** 독립 대시보드 실행기입니다. 학습은 자동 시작하지 않습니다. |
| **파일:** [pipeline.py](../../8%EC%B0%A8/pipeline.py)<br>**원문에 정의된 역할·구성:** 5차 영상 파이프라인을 보존하며 7차 상태만 읽는 8차 어댑터입니다. |
| **파일:** [verify_sources.py](../../8%EC%B0%A8/verify_sources.py)<br>**원문에 정의된 역할·구성:** 배포 파일의 문자·구문과 의존 원본 불변을 검사합니다. |
| **파일:** [tests/test_adapter.py](../../8%EC%B0%A8/tests/test_adapter.py)<br>**원문에 정의된 역할·구성:** 상태 출처와 시각·중복 시작·원래 HTTP 경계를 회귀 검사합니다. |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

<a name="️-소스에서-제공하는-cli-옵션"></a>
### 소스에서 제공하는 CLI 옵션

| 진입 소스 · 정의된 옵션 이름 |
| --- |
| **진입 소스:** [launcher.py](../../8%EC%B0%A8/launcher.py)<br>**정의된 옵션 이름:** `--no-browser`, `--port`, `--self-test`, `--hidden` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [dashboard.py](../../8%EC%B0%A8/dashboard.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/dashboard.py#L8)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`not match`](../../8%EC%B0%A8/dashboard.py#L25)

**오류 메시지:** 7차 로그는 등록된 작업 ID만 허용합니다.

**거부 조건:** [`not any(row['id'] == job for row in records)`](../../8%EC%B0%A8/dashboard.py#L29)

**오류 메시지:** 등록되지 않은 작업 로그입니다.

**거부 조건:** [`path.parent != base or not path.is_file()`](../../8%EC%B0%A8/dashboard.py#L33)

**오류 메시지:** 허용되지 않은 작업 로그입니다.


### [launcher.py](../../8%EC%B0%A8/launcher.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`--no-browser`](../../8%EC%B0%A8/launcher.py#L55)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--port`](../../8%EC%B0%A8/launcher.py#L56)<br>**코드의 선언:** `type=int; default=0` |
| **설정·옵션:** [`--self-test`](../../8%EC%B0%A8/launcher.py#L57)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--hidden`](../../8%EC%B0%A8/launcher.py#L58)<br>**코드의 선언:** `action='store_true'` |

| 거부 조건 · 오류 메시지 |
| --- |
| **거부 조건:** [`response.status != 200`](../../8%EC%B0%A8/launcher.py#L20)<br>**오류 메시지:** 루프백 상태 검사에 실패했습니다. |

### [pipeline.py](../../8%EC%B0%A8/pipeline.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/pipeline.py#L11)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`PREVIOUS`](../../8%EC%B0%A8/pipeline.py#L12)<br>**코드의 선언:** `정의=ROOT.parent / '5차'` |
| **설정·옵션:** [`TRAINING_ROOT`](../../8%EC%B0%A8/pipeline.py#L13)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`ACTIVE`](../../8%EC%B0%A8/pipeline.py#L14)<br>**코드의 선언:** `정의={'running', 'queued', 'starting'}` |
| **설정·옵션:** [`KST`](../../8%EC%B0%A8/pipeline.py#L15)<br>**코드의 선언:** `정의=timezone(timedelta(hours=9), 'Asia/Seoul')` |

**거부 조건:** [`not isinstance(params, dict)`](../../8%EC%B0%A8/pipeline.py#L120)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`not isinstance(value, dict) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value.get('id', '')) or path.stem != value['id']`](../../8%EC%B0%A8/pipeline.py#L46)

**오류 메시지:** 작업 기록 ID와 파일명이 일치하지 않습니다.

**거부 조건:** [`not re.fullmatch(r'[A-Za-z0-9_-]+', name)`](../../8%EC%B0%A8/pipeline.py#L56)

**오류 메시지:** 학습 후보 이름이 잘못됐습니다.

**거부 조건:** [`set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../8%EC%B0%A8/pipeline.py#L125)

**오류 메시지:** resume은 명시적 참 또는 거짓만 허용합니다.

**거부 조건:** [`status()['busy']`](../../8%EC%B0%A8/pipeline.py#L127)

**오류 메시지:** 7차 자료 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`number is not None and not math.isfinite(number)`](../../8%EC%B0%A8/pipeline.py#L68)

**오류 메시지:** 학습 곡선에 유효하지 않은 값이 있습니다.


### [verify_sources.py](../../8%EC%B0%A8/verify_sources.py)


| 설정·옵션 · 코드의 선언 |
| --- |
| **설정·옵션:** [`ROOT`](../../8%EC%B0%A8/verify_sources.py#L7)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

화면에서 읽은 상태와 실제 학습 성능을 구분합니다. 3D 단계나 진행률은 작업 상태의 표현이며 90% 정확도 달성값이 아닙니다.

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

7차에서 8차로 이어지는 실제 파일 비교입니다.

[전체 비교·자료 범위](../comparisons/7-to-8.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>파일별 비교·크기·해시 자세히 보기</summary>

[공개 폴더](../../8차/) · [실행 안내](../../8차/README.md) · [공개용 변경 기록](../../8차/변경기록.md) · [직전7차와 전체 파일 비교](../comparisons/7-to-8.md)

</details>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../8%EC%B0%A8) · [← 이전: 7차](round-7.md) · [다음: 9차 →](round-9.md)
