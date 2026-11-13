<div align="center">

<a name="--10차--입체-실험-대시보드"></a>
# 10차 · 입체 실험 대시보드

확정 시안을 참조해 다운로드·데이터 준비·GPU 학습·검증·최종 평가를 실제 Three.js WebGL 메시와 단계별 움직임으로 구현했습니다. 현재 작업과 다음 단계, 활성·완료·실패·재시도·대기를 문구와 색상으로 함께 구분합니다. 영상 탐지·성능 분석·작업 기록, 나눔고딕 Bold와 기존 접근 제한을 유지합니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../10%EC%B0%A8) · [← 이전: 9차](round-9.md) · [다음: 11차 →](round-11.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

확정 시안을 참조해 다운로드·데이터 준비·GPU 학습·검증·최종 평가를 실제 Three.js WebGL 메시와 단계별 움직임으로 구현했습니다. 현재 작업과 다음 단계, 활성·완료·실패·재시도·대기를 문구와 색상으로 함께 구분합니다. 영상 탐지·성능 분석·작업 기록, 나눔고딕 Bold와 기존 접근 제한을 유지합니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

| 항목 | 이 차수에서 확인할 내용 |
|---|---|
| 1 | 확정 시안을 참조해 다운로드·데이터 준비·GPU 학습·검증·최종 평가를 실제 Three.js WebGL 메시와 단계별 움직임으로 구현했습니다. 현재 작업과 다음 단계, 활성·완료·실패·재시도·대기를 문구와 색상으로 함께 구분합니다. 영상 탐지·성능 분석·작업 기록, 나눔고딕 Bold와 기존 접근 제한을 유지합니다. |
| 2 | 현재 파일의 진행률은 전체 실험 진행률이 아닙니다. 속도·남은 시간은 유효 표본이 있을 때만 표시하고 최종 평가 전 성능은 미측정으로 남깁니다. 시안의 예시 날짜와 숫자는 실험값으로 사용하지 않습니다. 단계 선택은 설명을 바꾸며 학습이나 탐지를 시작하지 않습니다. |
| 3 | 두 비교 문서의 전체 패치는 텍스트의 주석·공백·개행을 포함하고, 바이너리는 크기와 SHA-256으로 구분합니다. 공개 소스·검사·설명·시안·로컬 의존 자산과 라이선스 38개를 포함합니다. 첫 화면과 전체 차수·파일 비교 목차를 연결하며, 기존 공개 자료 정리 안내와 원문 제외 상태를 보존합니다. |
| 4 | Python 검사 52개·JavaScript 검사 21개와 소스 검사를 통과했습니다. Windows 공유 읽기 검사와 원자적 교체 재현, 실화면 대조·재생/정지·작은 화면·영상 기능의 구체적인 범위는 [화면 검증](../../10차/design-qa.md)에 기록했습니다. 초기 잘못된 영역 캡처는 무효 기록을 보존했습니다. |
| 5 | 현재 작업의 5단계를 실제 WebGL 모형과 상태 문구·색으로 표시합니다. 정지·재생과 모션 축소, 작은 화면의 접근을 지원합니다. |

<a name="-입력처리출력"></a>
## 입력·처리·출력

| 단계 | 내용 |
|---|---|
| 입력 | 7차 작업의 상태·진행·결과 기록 |
| 처리 | 원본 계약 확인 → 상태 읽기 → 대시보드 상태·단계 표시 |
| 출력 | 작업 진행·완료·대기·오류 화면 |

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
| [design/](../../10%EC%B0%A8/design) | 하위 자료 폴더 |
| [docs/](../../10%EC%B0%A8/docs) | 하위 자료 폴더 |
| [tests/](../../10%EC%B0%A8/tests) | 하위 자료 폴더 |
| [web/](../../10%EC%B0%A8/web) | 하위 자료 폴더 |
| [README.md](../../10%EC%B0%A8/README.md) | MD 파일 |
| [dashboard.py](../../10%EC%B0%A8/dashboard.py) | PY 파일 |
| [design-qa.md](../../10%EC%B0%A8/design-qa.md) | MD 파일 |
| [launcher.py](../../10%EC%B0%A8/launcher.py) | PY 파일 |
| [pipeline.py](../../10%EC%B0%A8/pipeline.py) | PY 파일 |
| [safe_io.py](../../10%EC%B0%A8/safe_io.py) | PY 파일 |
| [verify_sources.py](../../10%EC%B0%A8/verify_sources.py) | PY 파일 |
| [대시보드실행.bat](../../10%EC%B0%A8/%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C%EC%8B%A4%ED%96%89.bat) | BAT 파일 |
| [변경기록.md](../../10%EC%B0%A8/%EB%B3%80%EA%B2%BD%EA%B8%B0%EB%A1%9D.md) | MD 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [dashboard.py](../../10%EC%B0%A8/dashboard.py) | 8차 인증·영상 경계를 상속하고 명시한 로컬 3D 모듈만 제공합니다. |
| [launcher.py](../../10%EC%B0%A8/launcher.py) | 독립 대시보드 실행기입니다. 학습은 자동 시작하지 않습니다. |
| [pipeline.py](../../10%EC%B0%A8/pipeline.py) | 8차의 실측 상태와 작업 경계를 재사용하는 10차 표시 어댑터입니다. |
| [safe_io.py](../../10%EC%B0%A8/safe_io.py) | 원자 교체를 막지 않는 읽기 전용 파일 접근을 제공합니다. |
| [verify_sources.py](../../10%EC%B0%A8/verify_sources.py) | 10차 배포 소스·공식 의존·보존 원본을 직접 검사합니다. |
| [tests/test_adapter.py](../../10%EC%B0%A8/tests/test_adapter.py) | 상태 출처와 시각·중복 시작·원래 HTTP 경계를 회귀 검사합니다. |
| [tests/test_presentation.py](../../10%EC%B0%A8/tests/test_presentation.py) | 운영 상태가 UI 문구와 현재 파일 진행률로 정확히 변환되는지 검사합니다. |
| [tests/test_safe_io.py](../../10%EC%B0%A8/tests/test_safe_io.py) | 읽기 공유, 엄격한 오류 처리와 핸들 정리를 실제 임시 파일로 검사합니다. |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

<a name="-이-차수-원래-안내의-세부-조건"></a>
### 이 차수 원래 안내의 세부 조건

<a name="️-실행과-표시-조건"></a>
### 실행과 표시 조건

Windows에서 `대시보드실행.bat`을 사용합니다. 같은 프로젝트의 5차 영상 실행 자료와 7차 작업 자료, Docker 환경과 필요한 모델·데이터가 별도로 필요합니다. 공개 저장소만 복제하여 전체 실험이 자동으로 재현되는 것은 아닙니다. 기존 8차의 로컬 서버 및 접근 제한을 재사용하며 접속 세션 값은 공개하지 않습니다.

애니메이션은 초당 최대 30프레임과 화면 배율 상한을 두고, 탭 숨김·운영체제의 움직임 줄이기 설정·사용자 정지를 존중합니다. WebGL을 사용할 수 없거나 그래픽 문맥이 끊겨도 텍스트 상태와 단계 정보를 유지하도록 구성합니다. 나눔고딕 Bold, Three.js 0.180.0, Lucide 0.468.0은 로컬 파일과 각각의 라이선스를 함께 보관합니다. 출처와 해시는 `docs/`의 각 명세를 확인하세요.

Windows의 상태 파일 읽기는 삭제 공유를 허용하도록 구성해 원자적 교체와 충돌하지 않도록 했습니다. 8차 원본을 수정하지 않고 10차에서 읽기 함수를 연결합니다. 과거 권한 오류의 책임 프로세스는 확정하지 않았습니다.

<a name="️-소스에서-제공하는-cli-옵션"></a>
### 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [launcher.py](../../10%EC%B0%A8/launcher.py) | `--no-browser`, `--port`, `--self-test`, `--hidden` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [dashboard.py](../../10%EC%B0%A8/dashboard.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT`](../../10%EC%B0%A8/dashboard.py#L8) | `정의=Path(__file__).resolve().parent` |
| [`ASSETS`](../../10%EC%B0%A8/dashboard.py#L12) | `정의={'/assets/brand-leaf.png': 'image/png', **{'/icons/' + name + '.svg': 'image/svg+xml' for name in ('flask-conical', 'video', 'chart-no-axes-column', 'notebook-text', 'refresh-cw', 'cpu', 'clock-3', 'chevrons-right')}}` |
| [`MODULES`](../../10%EC%B0%A8/dashboard.py#L13) | `정의={'/scene.js', '/presentation.js', '/vendor/three.module.js', '/vendor/three.core.js'}` |

### [launcher.py](../../10%EC%B0%A8/launcher.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--no-browser`](../../10%EC%B0%A8/launcher.py#L56) | `action='store_true'` |
| [`--port`](../../10%EC%B0%A8/launcher.py#L57) | `type=int; default=0` |
| [`--self-test`](../../10%EC%B0%A8/launcher.py#L58) | `action='store_true'` |
| [`--hidden`](../../10%EC%B0%A8/launcher.py#L59) | `action='store_true'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`response.status != 200`](../../10%EC%B0%A8/launcher.py#L21) | 루프백 상태 검사에 실패했습니다. |

### [pipeline.py](../../10%EC%B0%A8/pipeline.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT`](../../10%EC%B0%A8/pipeline.py#L7) | `정의=Path(__file__).resolve().parent` |
| [`PREVIOUS`](../../10%EC%B0%A8/pipeline.py#L8) | `정의=ROOT.parent / '5차'` |
| [`TRAINING_ROOT`](../../10%EC%B0%A8/pipeline.py#L9) | `정의=ROOT.parent / '7차'` |
| [`ACTIVE`](../../10%EC%B0%A8/pipeline.py#L25) | `정의=round8.ACTIVE` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not isinstance(params, dict)`](../../10%EC%B0%A8/pipeline.py#L100) | 설정은 JSON 객체여야 합니다. |
| [`set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../10%EC%B0%A8/pipeline.py#L104) | resume은 명시적 참 또는 거짓만 허용합니다. |
| [`status()['busy']`](../../10%EC%B0%A8/pipeline.py#L106) | 7차 자료 준비 또는 학습 작업이 이미 진행 중입니다. |

### [safe_io.py](../../10%EC%B0%A8/safe_io.py)

| 정의 | 소스에 적힌 역할 |
|---|---|
| [`safe_read_text`](../../10%EC%B0%A8/safe_io.py#L53) | 기존 호출자의 경로 검증을 유지하며 엄격하게 텍스트를 읽습니다. |
| [`safe_read_json`](../../10%EC%B0%A8/safe_io.py#L63) | 파일이 없을 때만 기본값을 반환하고 해독·JSON·접근 오류는 전파합니다. |

| 설정·옵션 | 코드의 선언 |
|---|---|
| [`_WINDOWS`](../../10%EC%B0%A8/safe_io.py#L8) | `정의=os.name == 'nt'` |

### [verify_sources.py](../../10%EC%B0%A8/verify_sources.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT`](../../10%EC%B0%A8/verify_sources.py#L8) | `정의=Path(__file__).resolve().parent` |

</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

화면에서 읽은 상태와 실제 학습 성능을 구분합니다. 3D 단계나 진행률은 작업 상태의 표현이며 90% 정확도 달성값이 아닙니다.

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

9차에서 10차로 이어지는 실제 파일 비교입니다.

[전체 비교·자료 범위](../comparisons/9-to-10.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>파일별 비교·크기·해시 자세히 보기</summary>

[9차 → 10차 전체 비교](../comparisons/9-to-10.md)는 추가 36개·수정 2개입니다. 9차는 7차 재개를 기록한 문서이고 10차는 화면 소프트웨어입니다. [8차 → 10차 전체 비교](../comparisons/8-to-10.md)는 추가 24개·수정 12개·삭제 3개·동일 2개입니다. 이 삭제 수는 두 폴더의 상대 경로 차이이며 이전 차수 파일을 제거했다는 뜻이 아닙니다.

</details>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../10%EC%B0%A8) · [← 이전: 9차](round-9.md) · [다음: 11차 →](round-11.md)
