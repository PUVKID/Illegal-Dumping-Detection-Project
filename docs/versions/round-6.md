<div align="center">

<a name="-6차의-변경-전-5차-보존본"></a>
# 6차의 변경 전 5차 보존본

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

**기술 분류:** 5차 변경 전 부분 스냅샷

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>
<!-- reading-levels:start -->
[LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

프로젝트 전체의 설명은 [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)부터 [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)까지 같은 범위로 연결됩니다.

<a id="reading-level-1"></a>
## LEVEL 1 - Beginner

### LEVEL 1 · 이 자료가 하는 일과 달라진 점

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

### LEVEL 1 · 실제 동작을 따라 읽기

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

CLI는 명령어와 옵션을 입력해 프로그램을 실행하는 방식입니다.

입력 — build_exe.py·pipeline.py·web/app.js·검사2개의 변경 전 파일

처리 — 5차 변경 대상 구현과 검사 비교

출력 — 다섯 파일의 이전 구현 기준

### LEVEL 1 · 준비하고 확인할 것

텍스트 편집기로 보존된 다섯 파일과 5차 전체 코드를 나란히 읽습니다. 제품 전체 실행 폴더가 아닙니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

#### LEVEL 1 · 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py) | `--build` |
| [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py) | `--action`, `--params` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 1 · [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--build`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L13) | `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not available`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L19) | 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

#### LEVEL 1 · [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L163)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L164)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L142)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L155)

**오류 메시지:** 지원하지 않는 작업입니다.


</details>

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

### LEVEL 1 · 결과와 주의할 범위

공개 비교에서 변경 전 동작과 검사 차이를 확인합니다. 별도 학습·추론 결과는 포함하지 않습니다.

| 상황 | 확인할 내용 |
|---|---|
| 실행 자료가 부족함 | 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다. |
| 결과 범위 해석 | 자료 열람·기능 확인·실험 성적을 각각 구분합니다. |

[자료 폴더](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-6-snapshot.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-2"></a>
## LEVEL 2 - Explorer

### LEVEL 2 · 목적과 구성의 연결

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

### LEVEL 2 · 입력에서 출력으로

| 단계 | 내용 |
|---|---|
| 입력 | build_exe.py·pipeline.py·web/app.js·검사2개의 변경 전 파일 |
| 처리 | 5차 변경 대상 구현과 검사 비교 |
| 출력 | 다섯 파일의 이전 구현 기준 |

입력·처리·출력은 위의 같은 자료 흐름을 다른 단계에서 읽는 기준입니다. 처리 조건과 출력의 의미를 함께 확인합니다.

### LEVEL 2 · 설정과 처리 순서의 관계

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

텍스트 편집기로 보존된 다섯 파일과 5차 전체 코드를 나란히 읽습니다. 제품 전체 실행 폴더가 아닙니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

#### LEVEL 2 · 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py) | `--build` |
| [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py) | `--action`, `--params` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 2 · [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--build`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L13) | `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not available`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L19) | 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

#### LEVEL 2 · [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L163)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L164)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L142)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L155)

**오류 메시지:** 지원하지 않는 작업입니다.


</details>

### LEVEL 2 · 관측과 해석을 구분하기

공개 비교에서 변경 전 동작과 검사 차이를 확인합니다. 별도 학습·추론 결과는 포함하지 않습니다.

| 상황 | 확인할 내용 |
|---|---|
| 실행 자료가 부족함 | 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다. |
| 결과 범위 해석 | 자료 열람·기능 확인·실험 성적을 각각 구분합니다. |

[자료 폴더](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-6-snapshot.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-3"></a>
## LEVEL 3 - Practitioner

### LEVEL 3 · 이 차수를 준비하는 범위

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

텍스트 편집기로 보존된 다섯 파일과 5차 전체 코드를 나란히 읽습니다. 제품 전체 실행 폴더가 아닙니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

#### LEVEL 3 · 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py) | `--build` |
| [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py) | `--action`, `--params` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 3 · [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--build`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L13) | `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not available`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L19) | 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

#### LEVEL 3 · [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L163)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L164)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L142)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L155)

**오류 메시지:** 지원하지 않는 작업입니다.


</details>

### LEVEL 3 · 실제 사용·실험 순서

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

| 단계 | 내용 |
|---|---|
| 입력 | build_exe.py·pipeline.py·web/app.js·검사2개의 변경 전 파일 |
| 처리 | 5차 변경 대상 구현과 검사 비교 |
| 출력 | 다섯 파일의 이전 구현 기준 |

### LEVEL 3 · 결과와 실패를 확인하기

공개 비교에서 변경 전 동작과 검사 차이를 확인합니다. 별도 학습·추론 결과는 포함하지 않습니다.

| 상황 | 확인할 내용 |
|---|---|
| 실행 자료가 부족함 | 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다. |
| 결과 범위 해석 | 자료 열람·기능 확인·실험 성적을 각각 구분합니다. |

### LEVEL 3 · 실행 전 대조할 차수 조건

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

[자료 폴더](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-6-snapshot.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-4"></a>
## LEVEL 4 - Advanced

### LEVEL 4 · 설계 의도와 검토 경계

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

### LEVEL 4 · 이 차수 구현의 실제 근거

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py) | PyInstaller 의존성 확인과 사용자가 선택한 빌드를 수행합니다. |
| [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py) | D 드라이브의 앱과 기존 GPU 컨테이너를 연결합니다. |
| [tests/test_dashboard.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/tests/test_dashboard.py) | 실제 HTTP 경계와 파이프라인 오류 전달을 검사합니다. |
| [tests/test_pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/tests/test_pipeline.py) | 허용 경로와 API 설정 실패 경로를 확인합니다. |

| 단계 | 내용 |
|---|---|
| 입력 | build_exe.py·pipeline.py·web/app.js·검사2개의 변경 전 파일 |
| 처리 | 5차 변경 대상 구현과 검사 비교 |
| 출력 | 다섯 파일의 이전 구현 기준 |

### LEVEL 4 · 조건·변경·결과를 함께 검토하기

텍스트 편집기로 보존된 다섯 파일과 5차 전체 코드를 나란히 읽습니다. 제품 전체 실행 폴더가 아닙니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

#### LEVEL 4 · 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py) | `--build` |
| [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py) | `--action`, `--params` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 4 · [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--build`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L13) | `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not available`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L19) | 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

#### LEVEL 4 · [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L163)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L164)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L142)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L155)

**오류 메시지:** 지원하지 않는 작업입니다.


</details>

공개 비교에서 변경 전 동작과 검사 차이를 확인합니다. 별도 학습·추론 결과는 포함하지 않습니다.

| 상황 | 확인할 내용 |
|---|---|
| 실행 자료가 부족함 | 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다. |
| 결과 범위 해석 | 자료 열람·기능 확인·실험 성적을 각각 구분합니다. |

### LEVEL 4 · 재현과 전체 비교

1. 실제 자료 구성에서 필요한 원문 파일을 엽니다.
2. 고유 설명에 적힌 입력 조건·경로·대상을 확인합니다.
3. 연결된 비교와 기록의 관측 범위를 대조합니다.

위 구성요소의 입력·출력과 실패 조건을 같은 차수 소스에 연결해 검토합니다. 전체 비교는 추가·수정·삭제와 원래 보관 범위를 구분하는 근거입니다.

[자료 폴더](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-6-snapshot.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<a id="reading-level-5"></a>
## LEVEL 5 - Expert

기존의 전체 설명·표·코드·함수 참조·파일별 비교는 아래에 그대로 이어집니다. [자료 폴더](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-6-snapshot.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<!-- reading-levels:end -->



[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8) · [← 이전: 5차](round-5.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

**항목:** 1

**이 차수에서 확인할 내용:** 5차 파일 다섯 개의 변경 전 보존 스냅샷입니다. 독립 모델이나 5차 전체의 복사본으로 해석하지 않습니다.


<a name="-입력처리출력"></a>
## 입력·처리·출력

| 단계 | 내용 |
|---|---|
| 입력 | build_exe.py·pipeline.py·web/app.js·검사2개의 변경 전 파일 |
| 처리 | 5차 변경 대상 구현과 검사 비교 |
| 출력 | 다섯 파일의 이전 구현 기준 |

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
| [tests/](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/tests) | 하위 자료 폴더 |
| [web/](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/web) | 하위 자료 폴더 |
| [README.md](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/README.md) | MD 파일 |
| [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py) | PY 파일 |
| [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py) | PY 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py) | PyInstaller 의존성 확인과 사용자가 선택한 빌드를 수행합니다. |
| [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py) | D 드라이브의 앱과 기존 GPU 컨테이너를 연결합니다. |
| [tests/test_dashboard.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/tests/test_dashboard.py) | 실제 HTTP 경계와 파이프라인 오류 전달을 검사합니다. |
| [tests/test_pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/tests/test_pipeline.py) | 허용 경로와 API 설정 실패 경로를 확인합니다. |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

텍스트 편집기로 보존된 다섯 파일과 5차 전체 코드를 나란히 읽습니다. 제품 전체 실행 폴더가 아닙니다.

관련 파일을 아래 링크에서 열어 순서대로 대조합니다.

<a name="️-소스에서-제공하는-cli-옵션"></a>
### 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py) | `--build` |
| [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py) | `--action`, `--params` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [build_exe.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--build`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L13) | `action='store_true'; help='확인만 하지 않고 실제 EXE를 빌드합니다.'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not available`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/build_exe.py#L19) | 빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다. |

### [pipeline.py](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py)


**설정·옵션:** [`--action`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L163)

**코드의 선언:** `required=True`

**설정·옵션:** [`--params`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L164)

**코드의 선언:** `default="{}"`

**설정·옵션:** [`ROOT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L10)

**코드의 선언:** `정의=Path(sys.executable).resolve().parent if getattr(sys, "frozen", False)         else Path(__file__).resolve().parent`

**설정·옵션:** [`PROJECT`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L12)

**코드의 선언:** `정의=ROOT.parent`

**설정·옵션:** [`WORK`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L13)

**코드의 선언:** `정의=ROOT / "work"`

**설정·옵션:** [`CONTAINER`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L14)

**코드의 선언:** `정의="2026"`

**설정·옵션:** [`REMOTE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L15)

**코드의 선언:** `정의="/workspace/2026/월요일 PBL/5차"`

**설정·옵션:** [`PYTHON`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L16)

**코드의 선언:** `정의="/opt/venvs/torch/bin/python"`

**설정·옵션:** [`ARCHIVE`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L17)

**코드의 선언:** `정의=PROJECT / "이전 도커 실험/3차실험/trash_round3"`

**설정·옵션:** [`VIDEO_ROOTS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L18)

**코드의 선언:** `정의=[WORK / "uploads", PROJECT / "최종/3차/테스트영상", ARCHIVE / "videos"]`

**설정·옵션:** [`EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L19)

**코드의 선언:** `정의={".mp4", ".avi", ".mov", ".mkv", ".m4v"}`


**거부 조건:** [`not p.is_file() or p.suffix.lower() not in EXTENSIONS`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L47)

**오류 메시지:** 지원하는 영상 파일을 선택하세요.

**거부 조건:** [`not any(p.is_relative_to(root.resolve()) for root in VIDEO_ROOTS)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L49)

**오류 메시지:** 허용된 영상 폴더가 아닙니다.

**거부 조건:** [`not p.stat().st_size`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L51)

**오류 메시지:** 0바이트 영상은 처리할 수 없습니다.

**거부 조건:** [`not isinstance(params, dict)`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L142)

**오류 메시지:** 설정은 JSON 객체여야 합니다.

**거부 조건:** [`name not in {"probe", "detect", "train", "health"}`](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8/pipeline.py#L155)

**오류 메시지:** 지원하지 않는 작업입니다.


</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

공개 비교에서 변경 전 동작과 검사 차이를 확인합니다. 별도 학습·추론 결과는 포함하지 않습니다.

<a name="️-제약과-문제-해결"></a>
## 제약과 문제 해결

| 상황 | 확인할 내용 |
|---|---|
| 실행 자료가 부족함 | 이 묶음의 보존 범위와 원래 참조 차수를 확인합니다. |
| 결과 범위 해석 | 자료 열람·기능 확인·실험 성적을 각각 구분합니다. |

<a name="changes"></a>

<a name="-직전-자료와-전체-비교"></a>
## 직전 자료와 전체 비교

5차에서 6차로 이어지는 실제 파일 비교입니다.

[전체 비교·자료 범위](../comparisons/5-to-6-snapshot.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>파일별 비교·크기·해시 자세히 보기</summary>

[공개 폴더](../../6차/변경전_5차/) · [5차 대응 파일 비교](../comparisons/5-to-6-snapshot.md)

</details>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../6%EC%B0%A8/%EB%B3%80%EA%B2%BD%EC%A0%84_5%EC%B0%A8) · [← 이전: 5차](round-5.md)
