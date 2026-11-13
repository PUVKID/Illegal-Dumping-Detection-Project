<div align="center">

<a name="-11차--고정-실험-계약을-보존하는-수신-복구"></a>
# 11차 · 고정 실험 계약을 보존하는 수신 복구

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>
<!-- reading-levels:start -->
[LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

프로젝트 전체의 설명은 [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)부터 [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)까지 같은 범위로 연결됩니다.

<a id="reading-level-1"></a>
## LEVEL 1 - Beginner

### LEVEL 1 · 이 자료가 하는 일과 달라진 점

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

### LEVEL 1 · 실제 동작을 따라 읽기

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

CLI는 명령어와 옵션을 입력해 프로그램을 실행하는 방식입니다. 체크포인트는 이후에 이어서 사용할 수 있도록 저장한 학습 상태입니다.

입력 — 원래7차의 동결 기준16개 파일과 중단 상태

처리 — 불변 기준 대조 → 안전한 복구 조건 판별

출력 — 복구 검사·상태 기록

### LEVEL 1 · 준비하고 확인할 것

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다. 11차 복구 도구는 원래 7차 동결 환경의 기준 16개 파일을 요구합니다. 공개 사본에는 일부 원래 문서와 CRLF 바이트가 달라 원본 계약을 만족하지 않을 수 있습니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 1 · 이 차수 원래 안내의 세부 조건

#### LEVEL 1 · 실행 조건

실제 시작은 독립 검증 후 같은 Docker Linux에서 수행합니다. 고정 7차 작업자만 `--pipeline`으로 허용하며 `--start`가 새 작업을 만들고 기존 작업자의 중복 잠금·실패 기록을 사용합니다. 원래 화면은 같은 7차 작업 상태를 읽습니다. 이 저장소만으로 데이터·모델·GPU 환경이 설치되지는 않습니다.

```text
python -B -X utf8 11차/recover.py --pipeline 7차/worker.py --start
```

동결 검사는 `verify_sources.py --expected-digest <독립 검토한 고정값>`으로 실행합니다. `--print-digest`는 후보 계산이며 검증 영수증이 아닙니다. 실제 실행 인자·검사 결과·원격 반영은 별도 기록으로 확인해야 합니다. 이 차수의 작성만으로 다운로드·학습 완료나 정밀도·재현율 각각 90% 달성을 뜻하지 않습니다.

#### LEVEL 1 · 2026-11-02 · 고정 실험 계약을 보존하는 복구 실행기

7차 원자료 수신의 범위 경과 제한과 재시도 소진을 다루기 위해 별도 실행기를 추가했습니다. 이번 구현은 7차·10차 제품 코드를 수정하거나 준비·학습 계약을 현재 값으로 갱신하지 않습니다. 기존 파일·부분 파일·원장·모델·체크포인트를 보존합니다.

#### LEVEL 1 · 수신 계약

64KiB부터 4MiB 이내에서 실제 완료 시간에 따라 범위를 조정합니다. 원장에는 매 수신을 합산하고 일반 화면 갱신만 약 2초 간격으로 합칩니다. 단계·재시도 진입·원인 해제는 즉시 알립니다. 실제 통신 오류는 최대 6회 재시도하고, 오류 없이 진행한 범위의 경과 제한만 저장 위치를 보존해 다음 범위로 나눕니다.

공식 범위 응답·크기·MD5·SHA-256·전송 100GiB·잔여 공간 100GiB를 유지합니다. 원장·통지·디스크 쓰기 실패는 재시도로 숨기지 않으며 요청 전 불확실 표식이 남으면 자동 재개를 차단합니다. 공식 원자료를 모두 검증한 뒤 원래 7차 준비·분할·학습·평가 함수를 호출합니다.

#### LEVEL 1 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [recover.py](../../11%EC%B0%A8/recover.py)<br>**정의된 옵션 이름:** `--pipeline`, `--start`, `--worker` |
| **진입 소스:** [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)<br>**정의된 옵션 이름:** `--expected-digest`, `--print-digest` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 1 · [recover.py](../../11%EC%B0%A8/recover.py)

| 내용 |
| --- |
| **정의:** [`Progress`](../../11%EC%B0%A8/recover.py#L47)<br>**소스에 적힌 역할:** 원장 합산은 매 본문마다 유지하고 화면 쓰기만 합칩니다. |
| **정의:** [`NetworkRetry`](../../11%EC%B0%A8/recover.py#L63)<br>**소스에 적힌 역할:** 연결·본문 읽기 경계의 실제 일시 오류만 나타냅니다. |

**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--pipeline`](../../11%EC%B0%A8/recover.py#L310)<br>**코드의 선언:** `required=True` |
| **설정·옵션:** [`--start`](../../11%EC%B0%A8/recover.py#L312)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--worker`](../../11%EC%B0%A8/recover.py#L313)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../11%EC%B0%A8/recover.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ORIGINAL`](../../11%EC%B0%A8/recover.py#L16)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`MIN_RANGE`](../../11%EC%B0%A8/recover.py#L17)<br>**코드의 선언:** `정의=64 * 1024` |
| **설정·옵션:** [`MAX_RANGE`](../../11%EC%B0%A8/recover.py#L18)<br>**코드의 선언:** `정의=4 * 1024 * 1024` |

**거부 조건:** [`path.is_symlink() or path.resolve() != (ORIGINAL / 'worker.py').resolve()`](../../11%EC%B0%A8/recover.py#L23)

**오류 메시지:** 고정된 7차 작업자 경로만 허용합니다.

**거부 조건:** [`data.load(data.TRAINING / 'preparation_contract.json') != expected`](../../11%EC%B0%A8/recover.py#L213)

**오류 메시지:** 원래 준비 계약과 보존 입력이 다릅니다. 계약을 갱신하지 않습니다.

**거부 조건:** [`data.load(data.SOURCES / 'source_contract.json') != {'files': data.SOURCE_FILES, 'license_evidence': 'evidence/공식데이터출처.json'}`](../../11%EC%B0%A8/recover.py#L215)

**오류 메시지:** 고정 공식 원자료 계약이 다릅니다.

**거부 조건:** [`resume is not True`](../../11%EC%B0%A8/recover.py#L240)

**오류 메시지:** 기존 계약의 명시적 재개만 허용합니다.

**거부 조건:** [`os.name != 'posix'`](../../11%EC%B0%A8/recover.py#L280)

**오류 메시지:** 실제 복구는 동일 Docker Linux에서 실행해야 합니다.

**거부 조건:** [`Path(module.__file__).resolve().parent != ORIGINAL.resolve()`](../../11%EC%B0%A8/recover.py#L42)

**오류 메시지:** 다른 프로젝트의 모듈은 실행할 수 없습니다.

**거부 조건:** [`target.stat().st_size != spec['size'] or self.data.digest_file(target, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L195)

**오류 메시지:** 기존 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`state.get('state') == 'running'`](../../11%EC%B0%A8/recover.py#L226)

**오류 메시지:** 기존 사전 수신 상태가 실행 중입니다.

**거부 조건:** [`any(value.get('state') in worker.ACTIVE for value in worker.jobs())`](../../11%EC%B0%A8/recover.py#L284)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/recover.py#L92)

**오류 메시지:** 수신 경로의 연결 파일을 허용하지 않습니다.

**거부 조건:** [`marker.exists()`](../../11%EC%B0%A8/recover.py#L96)

**오류 메시지:** 이전 수신의 원장·디스크 반영이 불확실합니다. 복구 기록 감사가 필요합니다.

**거부 조건:** [`partial.exists() and (not metadata.exists() or self.data.load(metadata) != identity)`](../../11%EC%B0%A8/recover.py#L101)

**오류 메시지:** 부분 파일의 공식 원자료 계약이 다릅니다.

**거부 조건:** [`start &gt; spec['size']`](../../11%EC%B0%A8/recover.py#L104)

**오류 메시지:** 부분 파일이 공식 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or self.data.digest_file(partial, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L189)

**오류 메시지:** 완성 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`saved != start or self.data.load(metadata) != identity`](../../11%EC%B0%A8/recover.py#L116)

**오류 메시지:** 수신 중 부분 파일·계약이 변경됐습니다.

**거부 조건:** [`budget.used + end - start + 1 &gt; budget.limit`](../../11%EC%B0%A8/recover.py#L118)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`(partial.stat().st_size if partial.exists() else 0) != start`](../../11%EC%B0%A8/recover.py#L166)

**오류 메시지:** 닫힌 부분 파일의 실제 저장량이 다릅니다.

**거부 조건:** [`budget.path.exists() and self.data.load(budget.path)['download_bytes'] != budget.used`](../../11%EC%B0%A8/recover.py#L168)

**오류 메시지:** 실제 전송 원장이 메모리 계상과 다릅니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../11%EC%B0%A8/recover.py#L130)

**오류 메시지:** 공식 범위 응답이 요청과 다릅니다.

**거부 조건:** [`len(block) &gt; end - start + 1`](../../11%EC%B0%A8/recover.py#L153)

**오류 메시지:** 수신 본문이 공식 범위를 넘었습니다.

**거부 조건:** [`stream.write(block) != len(block)`](../../11%EC%B0%A8/recover.py#L156)

**오류 메시지:** 부분 파일을 모두 기록하지 못했습니다.


#### LEVEL 1 · [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)


**설정·옵션:** [`--expected-digest`](../../11%EC%B0%A8/verify_sources.py#L43)

**코드의 선언:** ``

**설정·옵션:** [`--print-digest`](../../11%EC%B0%A8/verify_sources.py#L44)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../11%EC%B0%A8/verify_sources.py#L9)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PRODUCTS`](../../11%EC%B0%A8/verify_sources.py#L10)

**코드의 선언:** `정의=('README.md', 'docs/복구설계.md', 'original-baseline.json', 'recover.py', 'tests/test_recover.py', 'verify_sources.py', '변경기록.md')`


**거부 조건:** [`args.expected_digest and (not re.fullmatch(r'[0-9a-f]{64}', args.expected_digest) or digest != args.expected_digest)`](../../11%EC%B0%A8/verify_sources.py#L49)

**오류 메시지:** 외부 검사 명세에 고정한 11차 해시와 다릅니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L17)

**오류 메시지:** 제품 파일의 링크를 허용하지 않습니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L32)

**오류 메시지:** 제품 경로의 링크를 허용하지 않습니다.


</details>

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

### LEVEL 1 · 결과와 주의할 범위

복구 가능 여부는 기준 파일과 실제 상태 대조 결과입니다. 학습·평가 완료와 별도입니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


[자료 폴더](../../11%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/10-to-11.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-2"></a>
## LEVEL 2 - Explorer

### LEVEL 2 · 목적과 구성의 연결

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

### LEVEL 2 · 입력에서 출력으로

**단계:** 입력

**내용:** 원래7차의 동결 기준16개 파일과 중단 상태

**단계:** 처리

**내용:** 불변 기준 대조 → 안전한 복구 조건 판별

**단계:** 출력

**내용:** 복구 검사·상태 기록


입력·처리·출력은 위의 같은 자료 흐름을 다른 단계에서 읽는 기준입니다. 처리 조건과 출력의 의미를 함께 확인합니다.

### LEVEL 2 · 설정과 처리 순서의 관계

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다. 11차 복구 도구는 원래 7차 동결 환경의 기준 16개 파일을 요구합니다. 공개 사본에는 일부 원래 문서와 CRLF 바이트가 달라 원본 계약을 만족하지 않을 수 있습니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 2 · 이 차수 원래 안내의 세부 조건

#### LEVEL 2 · 실행 조건

실제 시작은 독립 검증 후 같은 Docker Linux에서 수행합니다. 고정 7차 작업자만 `--pipeline`으로 허용하며 `--start`가 새 작업을 만들고 기존 작업자의 중복 잠금·실패 기록을 사용합니다. 원래 화면은 같은 7차 작업 상태를 읽습니다. 이 저장소만으로 데이터·모델·GPU 환경이 설치되지는 않습니다.

```text
python -B -X utf8 11차/recover.py --pipeline 7차/worker.py --start
```

동결 검사는 `verify_sources.py --expected-digest <독립 검토한 고정값>`으로 실행합니다. `--print-digest`는 후보 계산이며 검증 영수증이 아닙니다. 실제 실행 인자·검사 결과·원격 반영은 별도 기록으로 확인해야 합니다. 이 차수의 작성만으로 다운로드·학습 완료나 정밀도·재현율 각각 90% 달성을 뜻하지 않습니다.

#### LEVEL 2 · 2026-11-02 · 고정 실험 계약을 보존하는 복구 실행기

7차 원자료 수신의 범위 경과 제한과 재시도 소진을 다루기 위해 별도 실행기를 추가했습니다. 이번 구현은 7차·10차 제품 코드를 수정하거나 준비·학습 계약을 현재 값으로 갱신하지 않습니다. 기존 파일·부분 파일·원장·모델·체크포인트를 보존합니다.

#### LEVEL 2 · 수신 계약

64KiB부터 4MiB 이내에서 실제 완료 시간에 따라 범위를 조정합니다. 원장에는 매 수신을 합산하고 일반 화면 갱신만 약 2초 간격으로 합칩니다. 단계·재시도 진입·원인 해제는 즉시 알립니다. 실제 통신 오류는 최대 6회 재시도하고, 오류 없이 진행한 범위의 경과 제한만 저장 위치를 보존해 다음 범위로 나눕니다.

공식 범위 응답·크기·MD5·SHA-256·전송 100GiB·잔여 공간 100GiB를 유지합니다. 원장·통지·디스크 쓰기 실패는 재시도로 숨기지 않으며 요청 전 불확실 표식이 남으면 자동 재개를 차단합니다. 공식 원자료를 모두 검증한 뒤 원래 7차 준비·분할·학습·평가 함수를 호출합니다.

#### LEVEL 2 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [recover.py](../../11%EC%B0%A8/recover.py)<br>**정의된 옵션 이름:** `--pipeline`, `--start`, `--worker` |
| **진입 소스:** [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)<br>**정의된 옵션 이름:** `--expected-digest`, `--print-digest` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 2 · [recover.py](../../11%EC%B0%A8/recover.py)

| 내용 |
| --- |
| **정의:** [`Progress`](../../11%EC%B0%A8/recover.py#L47)<br>**소스에 적힌 역할:** 원장 합산은 매 본문마다 유지하고 화면 쓰기만 합칩니다. |
| **정의:** [`NetworkRetry`](../../11%EC%B0%A8/recover.py#L63)<br>**소스에 적힌 역할:** 연결·본문 읽기 경계의 실제 일시 오류만 나타냅니다. |

**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--pipeline`](../../11%EC%B0%A8/recover.py#L310)<br>**코드의 선언:** `required=True` |
| **설정·옵션:** [`--start`](../../11%EC%B0%A8/recover.py#L312)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--worker`](../../11%EC%B0%A8/recover.py#L313)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../11%EC%B0%A8/recover.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ORIGINAL`](../../11%EC%B0%A8/recover.py#L16)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`MIN_RANGE`](../../11%EC%B0%A8/recover.py#L17)<br>**코드의 선언:** `정의=64 * 1024` |
| **설정·옵션:** [`MAX_RANGE`](../../11%EC%B0%A8/recover.py#L18)<br>**코드의 선언:** `정의=4 * 1024 * 1024` |

**거부 조건:** [`path.is_symlink() or path.resolve() != (ORIGINAL / 'worker.py').resolve()`](../../11%EC%B0%A8/recover.py#L23)

**오류 메시지:** 고정된 7차 작업자 경로만 허용합니다.

**거부 조건:** [`data.load(data.TRAINING / 'preparation_contract.json') != expected`](../../11%EC%B0%A8/recover.py#L213)

**오류 메시지:** 원래 준비 계약과 보존 입력이 다릅니다. 계약을 갱신하지 않습니다.

**거부 조건:** [`data.load(data.SOURCES / 'source_contract.json') != {'files': data.SOURCE_FILES, 'license_evidence': 'evidence/공식데이터출처.json'}`](../../11%EC%B0%A8/recover.py#L215)

**오류 메시지:** 고정 공식 원자료 계약이 다릅니다.

**거부 조건:** [`resume is not True`](../../11%EC%B0%A8/recover.py#L240)

**오류 메시지:** 기존 계약의 명시적 재개만 허용합니다.

**거부 조건:** [`os.name != 'posix'`](../../11%EC%B0%A8/recover.py#L280)

**오류 메시지:** 실제 복구는 동일 Docker Linux에서 실행해야 합니다.

**거부 조건:** [`Path(module.__file__).resolve().parent != ORIGINAL.resolve()`](../../11%EC%B0%A8/recover.py#L42)

**오류 메시지:** 다른 프로젝트의 모듈은 실행할 수 없습니다.

**거부 조건:** [`target.stat().st_size != spec['size'] or self.data.digest_file(target, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L195)

**오류 메시지:** 기존 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`state.get('state') == 'running'`](../../11%EC%B0%A8/recover.py#L226)

**오류 메시지:** 기존 사전 수신 상태가 실행 중입니다.

**거부 조건:** [`any(value.get('state') in worker.ACTIVE for value in worker.jobs())`](../../11%EC%B0%A8/recover.py#L284)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/recover.py#L92)

**오류 메시지:** 수신 경로의 연결 파일을 허용하지 않습니다.

**거부 조건:** [`marker.exists()`](../../11%EC%B0%A8/recover.py#L96)

**오류 메시지:** 이전 수신의 원장·디스크 반영이 불확실합니다. 복구 기록 감사가 필요합니다.

**거부 조건:** [`partial.exists() and (not metadata.exists() or self.data.load(metadata) != identity)`](../../11%EC%B0%A8/recover.py#L101)

**오류 메시지:** 부분 파일의 공식 원자료 계약이 다릅니다.

**거부 조건:** [`start &gt; spec['size']`](../../11%EC%B0%A8/recover.py#L104)

**오류 메시지:** 부분 파일이 공식 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or self.data.digest_file(partial, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L189)

**오류 메시지:** 완성 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`saved != start or self.data.load(metadata) != identity`](../../11%EC%B0%A8/recover.py#L116)

**오류 메시지:** 수신 중 부분 파일·계약이 변경됐습니다.

**거부 조건:** [`budget.used + end - start + 1 &gt; budget.limit`](../../11%EC%B0%A8/recover.py#L118)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`(partial.stat().st_size if partial.exists() else 0) != start`](../../11%EC%B0%A8/recover.py#L166)

**오류 메시지:** 닫힌 부분 파일의 실제 저장량이 다릅니다.

**거부 조건:** [`budget.path.exists() and self.data.load(budget.path)['download_bytes'] != budget.used`](../../11%EC%B0%A8/recover.py#L168)

**오류 메시지:** 실제 전송 원장이 메모리 계상과 다릅니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../11%EC%B0%A8/recover.py#L130)

**오류 메시지:** 공식 범위 응답이 요청과 다릅니다.

**거부 조건:** [`len(block) &gt; end - start + 1`](../../11%EC%B0%A8/recover.py#L153)

**오류 메시지:** 수신 본문이 공식 범위를 넘었습니다.

**거부 조건:** [`stream.write(block) != len(block)`](../../11%EC%B0%A8/recover.py#L156)

**오류 메시지:** 부분 파일을 모두 기록하지 못했습니다.


#### LEVEL 2 · [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)


**설정·옵션:** [`--expected-digest`](../../11%EC%B0%A8/verify_sources.py#L43)

**코드의 선언:** ``

**설정·옵션:** [`--print-digest`](../../11%EC%B0%A8/verify_sources.py#L44)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../11%EC%B0%A8/verify_sources.py#L9)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PRODUCTS`](../../11%EC%B0%A8/verify_sources.py#L10)

**코드의 선언:** `정의=('README.md', 'docs/복구설계.md', 'original-baseline.json', 'recover.py', 'tests/test_recover.py', 'verify_sources.py', '변경기록.md')`


**거부 조건:** [`args.expected_digest and (not re.fullmatch(r'[0-9a-f]{64}', args.expected_digest) or digest != args.expected_digest)`](../../11%EC%B0%A8/verify_sources.py#L49)

**오류 메시지:** 외부 검사 명세에 고정한 11차 해시와 다릅니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L17)

**오류 메시지:** 제품 파일의 링크를 허용하지 않습니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L32)

**오류 메시지:** 제품 경로의 링크를 허용하지 않습니다.


</details>

### LEVEL 2 · 관측과 해석을 구분하기

복구 가능 여부는 기준 파일과 실제 상태 대조 결과입니다. 학습·평가 완료와 별도입니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


[자료 폴더](../../11%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/10-to-11.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-3"></a>
## LEVEL 3 - Practitioner

### LEVEL 3 · 이 차수를 준비하는 범위

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다. 11차 복구 도구는 원래 7차 동결 환경의 기준 16개 파일을 요구합니다. 공개 사본에는 일부 원래 문서와 CRLF 바이트가 달라 원본 계약을 만족하지 않을 수 있습니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 3 · 이 차수 원래 안내의 세부 조건

#### LEVEL 3 · 실행 조건

실제 시작은 독립 검증 후 같은 Docker Linux에서 수행합니다. 고정 7차 작업자만 `--pipeline`으로 허용하며 `--start`가 새 작업을 만들고 기존 작업자의 중복 잠금·실패 기록을 사용합니다. 원래 화면은 같은 7차 작업 상태를 읽습니다. 이 저장소만으로 데이터·모델·GPU 환경이 설치되지는 않습니다.

```text
python -B -X utf8 11차/recover.py --pipeline 7차/worker.py --start
```

동결 검사는 `verify_sources.py --expected-digest <독립 검토한 고정값>`으로 실행합니다. `--print-digest`는 후보 계산이며 검증 영수증이 아닙니다. 실제 실행 인자·검사 결과·원격 반영은 별도 기록으로 확인해야 합니다. 이 차수의 작성만으로 다운로드·학습 완료나 정밀도·재현율 각각 90% 달성을 뜻하지 않습니다.

#### LEVEL 3 · 2026-11-02 · 고정 실험 계약을 보존하는 복구 실행기

7차 원자료 수신의 범위 경과 제한과 재시도 소진을 다루기 위해 별도 실행기를 추가했습니다. 이번 구현은 7차·10차 제품 코드를 수정하거나 준비·학습 계약을 현재 값으로 갱신하지 않습니다. 기존 파일·부분 파일·원장·모델·체크포인트를 보존합니다.

#### LEVEL 3 · 수신 계약

64KiB부터 4MiB 이내에서 실제 완료 시간에 따라 범위를 조정합니다. 원장에는 매 수신을 합산하고 일반 화면 갱신만 약 2초 간격으로 합칩니다. 단계·재시도 진입·원인 해제는 즉시 알립니다. 실제 통신 오류는 최대 6회 재시도하고, 오류 없이 진행한 범위의 경과 제한만 저장 위치를 보존해 다음 범위로 나눕니다.

공식 범위 응답·크기·MD5·SHA-256·전송 100GiB·잔여 공간 100GiB를 유지합니다. 원장·통지·디스크 쓰기 실패는 재시도로 숨기지 않으며 요청 전 불확실 표식이 남으면 자동 재개를 차단합니다. 공식 원자료를 모두 검증한 뒤 원래 7차 준비·분할·학습·평가 함수를 호출합니다.

#### LEVEL 3 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [recover.py](../../11%EC%B0%A8/recover.py)<br>**정의된 옵션 이름:** `--pipeline`, `--start`, `--worker` |
| **진입 소스:** [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)<br>**정의된 옵션 이름:** `--expected-digest`, `--print-digest` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 3 · [recover.py](../../11%EC%B0%A8/recover.py)

| 내용 |
| --- |
| **정의:** [`Progress`](../../11%EC%B0%A8/recover.py#L47)<br>**소스에 적힌 역할:** 원장 합산은 매 본문마다 유지하고 화면 쓰기만 합칩니다. |
| **정의:** [`NetworkRetry`](../../11%EC%B0%A8/recover.py#L63)<br>**소스에 적힌 역할:** 연결·본문 읽기 경계의 실제 일시 오류만 나타냅니다. |

**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--pipeline`](../../11%EC%B0%A8/recover.py#L310)<br>**코드의 선언:** `required=True` |
| **설정·옵션:** [`--start`](../../11%EC%B0%A8/recover.py#L312)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--worker`](../../11%EC%B0%A8/recover.py#L313)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../11%EC%B0%A8/recover.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ORIGINAL`](../../11%EC%B0%A8/recover.py#L16)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`MIN_RANGE`](../../11%EC%B0%A8/recover.py#L17)<br>**코드의 선언:** `정의=64 * 1024` |
| **설정·옵션:** [`MAX_RANGE`](../../11%EC%B0%A8/recover.py#L18)<br>**코드의 선언:** `정의=4 * 1024 * 1024` |

**거부 조건:** [`path.is_symlink() or path.resolve() != (ORIGINAL / 'worker.py').resolve()`](../../11%EC%B0%A8/recover.py#L23)

**오류 메시지:** 고정된 7차 작업자 경로만 허용합니다.

**거부 조건:** [`data.load(data.TRAINING / 'preparation_contract.json') != expected`](../../11%EC%B0%A8/recover.py#L213)

**오류 메시지:** 원래 준비 계약과 보존 입력이 다릅니다. 계약을 갱신하지 않습니다.

**거부 조건:** [`data.load(data.SOURCES / 'source_contract.json') != {'files': data.SOURCE_FILES, 'license_evidence': 'evidence/공식데이터출처.json'}`](../../11%EC%B0%A8/recover.py#L215)

**오류 메시지:** 고정 공식 원자료 계약이 다릅니다.

**거부 조건:** [`resume is not True`](../../11%EC%B0%A8/recover.py#L240)

**오류 메시지:** 기존 계약의 명시적 재개만 허용합니다.

**거부 조건:** [`os.name != 'posix'`](../../11%EC%B0%A8/recover.py#L280)

**오류 메시지:** 실제 복구는 동일 Docker Linux에서 실행해야 합니다.

**거부 조건:** [`Path(module.__file__).resolve().parent != ORIGINAL.resolve()`](../../11%EC%B0%A8/recover.py#L42)

**오류 메시지:** 다른 프로젝트의 모듈은 실행할 수 없습니다.

**거부 조건:** [`target.stat().st_size != spec['size'] or self.data.digest_file(target, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L195)

**오류 메시지:** 기존 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`state.get('state') == 'running'`](../../11%EC%B0%A8/recover.py#L226)

**오류 메시지:** 기존 사전 수신 상태가 실행 중입니다.

**거부 조건:** [`any(value.get('state') in worker.ACTIVE for value in worker.jobs())`](../../11%EC%B0%A8/recover.py#L284)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/recover.py#L92)

**오류 메시지:** 수신 경로의 연결 파일을 허용하지 않습니다.

**거부 조건:** [`marker.exists()`](../../11%EC%B0%A8/recover.py#L96)

**오류 메시지:** 이전 수신의 원장·디스크 반영이 불확실합니다. 복구 기록 감사가 필요합니다.

**거부 조건:** [`partial.exists() and (not metadata.exists() or self.data.load(metadata) != identity)`](../../11%EC%B0%A8/recover.py#L101)

**오류 메시지:** 부분 파일의 공식 원자료 계약이 다릅니다.

**거부 조건:** [`start &gt; spec['size']`](../../11%EC%B0%A8/recover.py#L104)

**오류 메시지:** 부분 파일이 공식 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or self.data.digest_file(partial, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L189)

**오류 메시지:** 완성 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`saved != start or self.data.load(metadata) != identity`](../../11%EC%B0%A8/recover.py#L116)

**오류 메시지:** 수신 중 부분 파일·계약이 변경됐습니다.

**거부 조건:** [`budget.used + end - start + 1 &gt; budget.limit`](../../11%EC%B0%A8/recover.py#L118)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`(partial.stat().st_size if partial.exists() else 0) != start`](../../11%EC%B0%A8/recover.py#L166)

**오류 메시지:** 닫힌 부분 파일의 실제 저장량이 다릅니다.

**거부 조건:** [`budget.path.exists() and self.data.load(budget.path)['download_bytes'] != budget.used`](../../11%EC%B0%A8/recover.py#L168)

**오류 메시지:** 실제 전송 원장이 메모리 계상과 다릅니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../11%EC%B0%A8/recover.py#L130)

**오류 메시지:** 공식 범위 응답이 요청과 다릅니다.

**거부 조건:** [`len(block) &gt; end - start + 1`](../../11%EC%B0%A8/recover.py#L153)

**오류 메시지:** 수신 본문이 공식 범위를 넘었습니다.

**거부 조건:** [`stream.write(block) != len(block)`](../../11%EC%B0%A8/recover.py#L156)

**오류 메시지:** 부분 파일을 모두 기록하지 못했습니다.


#### LEVEL 3 · [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)


**설정·옵션:** [`--expected-digest`](../../11%EC%B0%A8/verify_sources.py#L43)

**코드의 선언:** ``

**설정·옵션:** [`--print-digest`](../../11%EC%B0%A8/verify_sources.py#L44)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../11%EC%B0%A8/verify_sources.py#L9)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PRODUCTS`](../../11%EC%B0%A8/verify_sources.py#L10)

**코드의 선언:** `정의=('README.md', 'docs/복구설계.md', 'original-baseline.json', 'recover.py', 'tests/test_recover.py', 'verify_sources.py', '변경기록.md')`


**거부 조건:** [`args.expected_digest and (not re.fullmatch(r'[0-9a-f]{64}', args.expected_digest) or digest != args.expected_digest)`](../../11%EC%B0%A8/verify_sources.py#L49)

**오류 메시지:** 외부 검사 명세에 고정한 11차 해시와 다릅니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L17)

**오류 메시지:** 제품 파일의 링크를 허용하지 않습니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L32)

**오류 메시지:** 제품 경로의 링크를 허용하지 않습니다.


</details>

### LEVEL 3 · 실제 사용·실험 순서

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

**단계:** 입력

**내용:** 원래7차의 동결 기준16개 파일과 중단 상태

**단계:** 처리

**내용:** 불변 기준 대조 → 안전한 복구 조건 판별

**단계:** 출력

**내용:** 복구 검사·상태 기록


### LEVEL 3 · 결과와 실패를 확인하기

복구 가능 여부는 기준 파일과 실제 상태 대조 결과입니다. 학습·평가 완료와 별도입니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


### LEVEL 3 · 실행 전 대조할 차수 조건

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

[자료 폴더](../../11%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/10-to-11.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-4"></a>
## LEVEL 4 - Advanced

### LEVEL 4 · 설계 의도와 검토 경계

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

### LEVEL 4 · 이 차수 구현의 실제 근거

| 내용 |
| --- |
| **파일:** [recover.py](../../11%EC%B0%A8/recover.py)<br>**원문에 정의된 역할·구성:** 7차 계약을 보존하며 작은 범위의 원자료 수신을 앞에 연결합니다. |
| **파일:** [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)<br>**원문에 정의된 역할·구성:** 외부에서 고정한 11차 전체 해시와 7차 원본 불변을 검사합니다. |
| **파일:** [tests/test_recover.py](../../11%EC%B0%A8/tests/test_recover.py)<br>**원문에 정의된 역할·구성:** 작은 공식 범위 수신과 기존 작업자 연결의 실패 경로를 검사합니다. |

**단계:** 입력

**내용:** 원래7차의 동결 기준16개 파일과 중단 상태

**단계:** 처리

**내용:** 불변 기준 대조 → 안전한 복구 조건 판별

**단계:** 출력

**내용:** 복구 검사·상태 기록


### LEVEL 4 · 조건·변경·결과를 함께 검토하기

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다. 11차 복구 도구는 원래 7차 동결 환경의 기준 16개 파일을 요구합니다. 공개 사본에는 일부 원래 문서와 CRLF 바이트가 달라 원본 계약을 만족하지 않을 수 있습니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 4 · 이 차수 원래 안내의 세부 조건

#### LEVEL 4 · 실행 조건

실제 시작은 독립 검증 후 같은 Docker Linux에서 수행합니다. 고정 7차 작업자만 `--pipeline`으로 허용하며 `--start`가 새 작업을 만들고 기존 작업자의 중복 잠금·실패 기록을 사용합니다. 원래 화면은 같은 7차 작업 상태를 읽습니다. 이 저장소만으로 데이터·모델·GPU 환경이 설치되지는 않습니다.

```text
python -B -X utf8 11차/recover.py --pipeline 7차/worker.py --start
```

동결 검사는 `verify_sources.py --expected-digest <독립 검토한 고정값>`으로 실행합니다. `--print-digest`는 후보 계산이며 검증 영수증이 아닙니다. 실제 실행 인자·검사 결과·원격 반영은 별도 기록으로 확인해야 합니다. 이 차수의 작성만으로 다운로드·학습 완료나 정밀도·재현율 각각 90% 달성을 뜻하지 않습니다.

#### LEVEL 4 · 2026-11-02 · 고정 실험 계약을 보존하는 복구 실행기

7차 원자료 수신의 범위 경과 제한과 재시도 소진을 다루기 위해 별도 실행기를 추가했습니다. 이번 구현은 7차·10차 제품 코드를 수정하거나 준비·학습 계약을 현재 값으로 갱신하지 않습니다. 기존 파일·부분 파일·원장·모델·체크포인트를 보존합니다.

#### LEVEL 4 · 수신 계약

64KiB부터 4MiB 이내에서 실제 완료 시간에 따라 범위를 조정합니다. 원장에는 매 수신을 합산하고 일반 화면 갱신만 약 2초 간격으로 합칩니다. 단계·재시도 진입·원인 해제는 즉시 알립니다. 실제 통신 오류는 최대 6회 재시도하고, 오류 없이 진행한 범위의 경과 제한만 저장 위치를 보존해 다음 범위로 나눕니다.

공식 범위 응답·크기·MD5·SHA-256·전송 100GiB·잔여 공간 100GiB를 유지합니다. 원장·통지·디스크 쓰기 실패는 재시도로 숨기지 않으며 요청 전 불확실 표식이 남으면 자동 재개를 차단합니다. 공식 원자료를 모두 검증한 뒤 원래 7차 준비·분할·학습·평가 함수를 호출합니다.

#### LEVEL 4 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [recover.py](../../11%EC%B0%A8/recover.py)<br>**정의된 옵션 이름:** `--pipeline`, `--start`, `--worker` |
| **진입 소스:** [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)<br>**정의된 옵션 이름:** `--expected-digest`, `--print-digest` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 4 · [recover.py](../../11%EC%B0%A8/recover.py)

| 내용 |
| --- |
| **정의:** [`Progress`](../../11%EC%B0%A8/recover.py#L47)<br>**소스에 적힌 역할:** 원장 합산은 매 본문마다 유지하고 화면 쓰기만 합칩니다. |
| **정의:** [`NetworkRetry`](../../11%EC%B0%A8/recover.py#L63)<br>**소스에 적힌 역할:** 연결·본문 읽기 경계의 실제 일시 오류만 나타냅니다. |

**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--pipeline`](../../11%EC%B0%A8/recover.py#L310)<br>**코드의 선언:** `required=True` |
| **설정·옵션:** [`--start`](../../11%EC%B0%A8/recover.py#L312)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--worker`](../../11%EC%B0%A8/recover.py#L313)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../11%EC%B0%A8/recover.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ORIGINAL`](../../11%EC%B0%A8/recover.py#L16)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`MIN_RANGE`](../../11%EC%B0%A8/recover.py#L17)<br>**코드의 선언:** `정의=64 * 1024` |
| **설정·옵션:** [`MAX_RANGE`](../../11%EC%B0%A8/recover.py#L18)<br>**코드의 선언:** `정의=4 * 1024 * 1024` |

**거부 조건:** [`path.is_symlink() or path.resolve() != (ORIGINAL / 'worker.py').resolve()`](../../11%EC%B0%A8/recover.py#L23)

**오류 메시지:** 고정된 7차 작업자 경로만 허용합니다.

**거부 조건:** [`data.load(data.TRAINING / 'preparation_contract.json') != expected`](../../11%EC%B0%A8/recover.py#L213)

**오류 메시지:** 원래 준비 계약과 보존 입력이 다릅니다. 계약을 갱신하지 않습니다.

**거부 조건:** [`data.load(data.SOURCES / 'source_contract.json') != {'files': data.SOURCE_FILES, 'license_evidence': 'evidence/공식데이터출처.json'}`](../../11%EC%B0%A8/recover.py#L215)

**오류 메시지:** 고정 공식 원자료 계약이 다릅니다.

**거부 조건:** [`resume is not True`](../../11%EC%B0%A8/recover.py#L240)

**오류 메시지:** 기존 계약의 명시적 재개만 허용합니다.

**거부 조건:** [`os.name != 'posix'`](../../11%EC%B0%A8/recover.py#L280)

**오류 메시지:** 실제 복구는 동일 Docker Linux에서 실행해야 합니다.

**거부 조건:** [`Path(module.__file__).resolve().parent != ORIGINAL.resolve()`](../../11%EC%B0%A8/recover.py#L42)

**오류 메시지:** 다른 프로젝트의 모듈은 실행할 수 없습니다.

**거부 조건:** [`target.stat().st_size != spec['size'] or self.data.digest_file(target, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L195)

**오류 메시지:** 기존 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`state.get('state') == 'running'`](../../11%EC%B0%A8/recover.py#L226)

**오류 메시지:** 기존 사전 수신 상태가 실행 중입니다.

**거부 조건:** [`any(value.get('state') in worker.ACTIVE for value in worker.jobs())`](../../11%EC%B0%A8/recover.py#L284)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/recover.py#L92)

**오류 메시지:** 수신 경로의 연결 파일을 허용하지 않습니다.

**거부 조건:** [`marker.exists()`](../../11%EC%B0%A8/recover.py#L96)

**오류 메시지:** 이전 수신의 원장·디스크 반영이 불확실합니다. 복구 기록 감사가 필요합니다.

**거부 조건:** [`partial.exists() and (not metadata.exists() or self.data.load(metadata) != identity)`](../../11%EC%B0%A8/recover.py#L101)

**오류 메시지:** 부분 파일의 공식 원자료 계약이 다릅니다.

**거부 조건:** [`start &gt; spec['size']`](../../11%EC%B0%A8/recover.py#L104)

**오류 메시지:** 부분 파일이 공식 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or self.data.digest_file(partial, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L189)

**오류 메시지:** 완성 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`saved != start or self.data.load(metadata) != identity`](../../11%EC%B0%A8/recover.py#L116)

**오류 메시지:** 수신 중 부분 파일·계약이 변경됐습니다.

**거부 조건:** [`budget.used + end - start + 1 &gt; budget.limit`](../../11%EC%B0%A8/recover.py#L118)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`(partial.stat().st_size if partial.exists() else 0) != start`](../../11%EC%B0%A8/recover.py#L166)

**오류 메시지:** 닫힌 부분 파일의 실제 저장량이 다릅니다.

**거부 조건:** [`budget.path.exists() and self.data.load(budget.path)['download_bytes'] != budget.used`](../../11%EC%B0%A8/recover.py#L168)

**오류 메시지:** 실제 전송 원장이 메모리 계상과 다릅니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../11%EC%B0%A8/recover.py#L130)

**오류 메시지:** 공식 범위 응답이 요청과 다릅니다.

**거부 조건:** [`len(block) &gt; end - start + 1`](../../11%EC%B0%A8/recover.py#L153)

**오류 메시지:** 수신 본문이 공식 범위를 넘었습니다.

**거부 조건:** [`stream.write(block) != len(block)`](../../11%EC%B0%A8/recover.py#L156)

**오류 메시지:** 부분 파일을 모두 기록하지 못했습니다.


#### LEVEL 4 · [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)


**설정·옵션:** [`--expected-digest`](../../11%EC%B0%A8/verify_sources.py#L43)

**코드의 선언:** ``

**설정·옵션:** [`--print-digest`](../../11%EC%B0%A8/verify_sources.py#L44)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../11%EC%B0%A8/verify_sources.py#L9)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PRODUCTS`](../../11%EC%B0%A8/verify_sources.py#L10)

**코드의 선언:** `정의=('README.md', 'docs/복구설계.md', 'original-baseline.json', 'recover.py', 'tests/test_recover.py', 'verify_sources.py', '변경기록.md')`


**거부 조건:** [`args.expected_digest and (not re.fullmatch(r'[0-9a-f]{64}', args.expected_digest) or digest != args.expected_digest)`](../../11%EC%B0%A8/verify_sources.py#L49)

**오류 메시지:** 외부 검사 명세에 고정한 11차 해시와 다릅니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L17)

**오류 메시지:** 제품 파일의 링크를 허용하지 않습니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L32)

**오류 메시지:** 제품 경로의 링크를 허용하지 않습니다.


</details>

복구 가능 여부는 기준 파일과 실제 상태 대조 결과입니다. 학습·평가 완료와 별도입니다.

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

[자료 폴더](../../11%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/10-to-11.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<a id="reading-level-5"></a>
## LEVEL 5 - Expert

기존의 전체 설명·표·코드·함수 참조·파일별 비교는 아래에 그대로 이어집니다. [자료 폴더](../../11%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/10-to-11.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<!-- reading-levels:end -->



[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../11%EC%B0%A8) · [← 이전: 10차](round-10.md) · [다음: 12차 →](round-12.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

**항목:** 1

**이 차수에서 확인할 내용:** 7차의 부분 수신을 보존해 단계적으로 다시 받고, 검증된 공식 원자료를 확보한 뒤 원래 준비·학습 절차를 호출하는 별도 도구입니다. 10차 화면과 기존 7차 원본 코드는 보존합니다. 2026-11-02 문서 작성 시점의 검사는 통제된 회귀 검사이며 장기 수신이나 GPU 학습 완료와 구분합니다.


<a name="-입력처리출력"></a>
## 입력·처리·출력

**단계:** 입력

**내용:** 원래7차의 동결 기준16개 파일과 중단 상태

**단계:** 처리

**내용:** 불변 기준 대조 → 안전한 복구 조건 판별

**단계:** 출력

**내용:** 복구 검사·상태 기록


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
| **경로:** [docs/](../../11%EC%B0%A8/docs)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [tests/](../../11%EC%B0%A8/tests)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [README.md](../../11%EC%B0%A8/README.md)<br>**자료 종류:** MD 파일 |
| **경로:** [original-baseline.json](../../11%EC%B0%A8/original-baseline.json)<br>**자료 종류:** JSON 파일 |
| **경로:** [recover.py](../../11%EC%B0%A8/recover.py)<br>**자료 종류:** PY 파일 |
| **경로:** [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)<br>**자료 종류:** PY 파일 |
| **경로:** [변경기록.md](../../11%EC%B0%A8/%EB%B3%80%EA%B2%BD%EA%B8%B0%EB%A1%9D.md)<br>**자료 종류:** MD 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 내용 |
| --- |
| **파일:** [recover.py](../../11%EC%B0%A8/recover.py)<br>**원문에 정의된 역할·구성:** 7차 계약을 보존하며 작은 범위의 원자료 수신을 앞에 연결합니다. |
| **파일:** [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)<br>**원문에 정의된 역할·구성:** 외부에서 고정한 11차 전체 해시와 7차 원본 불변을 검사합니다. |
| **파일:** [tests/test_recover.py](../../11%EC%B0%A8/tests/test_recover.py)<br>**원문에 정의된 역할·구성:** 작은 공식 범위 수신과 기존 작업자 연결의 실패 경로를 검사합니다. |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다. 11차 복구 도구는 원래 7차 동결 환경의 기준 16개 파일을 요구합니다. 공개 사본에는 일부 원래 문서와 CRLF 바이트가 달라 원본 계약을 만족하지 않을 수 있습니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

<a name="-이-차수-원래-안내의-세부-조건"></a>
### 이 차수 원래 안내의 세부 조건

<a name="-실행-조건"></a>
### 실행 조건

실제 시작은 독립 검증 후 같은 Docker Linux에서 수행합니다. 고정 7차 작업자만 `--pipeline`으로 허용하며 `--start`가 새 작업을 만들고 기존 작업자의 중복 잠금·실패 기록을 사용합니다. 원래 화면은 같은 7차 작업 상태를 읽습니다. 이 저장소만으로 데이터·모델·GPU 환경이 설치되지는 않습니다.

```text
python -B -X utf8 11차/recover.py --pipeline 7차/worker.py --start
```

동결 검사는 `verify_sources.py --expected-digest <독립 검토한 고정값>`으로 실행합니다. `--print-digest`는 후보 계산이며 검증 영수증이 아닙니다. 실제 실행 인자·검사 결과·원격 반영은 별도 기록으로 확인해야 합니다. 이 차수의 작성만으로 다운로드·학습 완료나 정밀도·재현율 각각 90% 달성을 뜻하지 않습니다.

### 2026-11-02 · 고정 실험 계약을 보존하는 복구 실행기

7차 원자료 수신의 범위 경과 제한과 재시도 소진을 다루기 위해 별도 실행기를 추가했습니다. 이번 구현은 7차·10차 제품 코드를 수정하거나 준비·학습 계약을 현재 값으로 갱신하지 않습니다. 기존 파일·부분 파일·원장·모델·체크포인트를 보존합니다.

<a name="-수신-계약"></a>
### 수신 계약

64KiB부터 4MiB 이내에서 실제 완료 시간에 따라 범위를 조정합니다. 원장에는 매 수신을 합산하고 일반 화면 갱신만 약 2초 간격으로 합칩니다. 단계·재시도 진입·원인 해제는 즉시 알립니다. 실제 통신 오류는 최대 6회 재시도하고, 오류 없이 진행한 범위의 경과 제한만 저장 위치를 보존해 다음 범위로 나눕니다.

공식 범위 응답·크기·MD5·SHA-256·전송 100GiB·잔여 공간 100GiB를 유지합니다. 원장·통지·디스크 쓰기 실패는 재시도로 숨기지 않으며 요청 전 불확실 표식이 남으면 자동 재개를 차단합니다. 공식 원자료를 모두 검증한 뒤 원래 7차 준비·분할·학습·평가 함수를 호출합니다.

<a name="️-소스에서-제공하는-cli-옵션"></a>
### 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [recover.py](../../11%EC%B0%A8/recover.py)<br>**정의된 옵션 이름:** `--pipeline`, `--start`, `--worker` |
| **진입 소스:** [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)<br>**정의된 옵션 이름:** `--expected-digest`, `--print-digest` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [recover.py](../../11%EC%B0%A8/recover.py)

| 내용 |
| --- |
| **정의:** [`Progress`](../../11%EC%B0%A8/recover.py#L47)<br>**소스에 적힌 역할:** 원장 합산은 매 본문마다 유지하고 화면 쓰기만 합칩니다. |
| **정의:** [`NetworkRetry`](../../11%EC%B0%A8/recover.py#L63)<br>**소스에 적힌 역할:** 연결·본문 읽기 경계의 실제 일시 오류만 나타냅니다. |

**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--pipeline`](../../11%EC%B0%A8/recover.py#L310)<br>**코드의 선언:** `required=True` |
| **설정·옵션:** [`--start`](../../11%EC%B0%A8/recover.py#L312)<br>**코드의 선언:** `action='store_true'` |
| **설정·옵션:** [`--worker`](../../11%EC%B0%A8/recover.py#L313)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../11%EC%B0%A8/recover.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`ORIGINAL`](../../11%EC%B0%A8/recover.py#L16)<br>**코드의 선언:** `정의=ROOT.parent / '7차'` |
| **설정·옵션:** [`MIN_RANGE`](../../11%EC%B0%A8/recover.py#L17)<br>**코드의 선언:** `정의=64 * 1024` |
| **설정·옵션:** [`MAX_RANGE`](../../11%EC%B0%A8/recover.py#L18)<br>**코드의 선언:** `정의=4 * 1024 * 1024` |

**거부 조건:** [`path.is_symlink() or path.resolve() != (ORIGINAL / 'worker.py').resolve()`](../../11%EC%B0%A8/recover.py#L23)

**오류 메시지:** 고정된 7차 작업자 경로만 허용합니다.

**거부 조건:** [`data.load(data.TRAINING / 'preparation_contract.json') != expected`](../../11%EC%B0%A8/recover.py#L213)

**오류 메시지:** 원래 준비 계약과 보존 입력이 다릅니다. 계약을 갱신하지 않습니다.

**거부 조건:** [`data.load(data.SOURCES / 'source_contract.json') != {'files': data.SOURCE_FILES, 'license_evidence': 'evidence/공식데이터출처.json'}`](../../11%EC%B0%A8/recover.py#L215)

**오류 메시지:** 고정 공식 원자료 계약이 다릅니다.

**거부 조건:** [`resume is not True`](../../11%EC%B0%A8/recover.py#L240)

**오류 메시지:** 기존 계약의 명시적 재개만 허용합니다.

**거부 조건:** [`os.name != 'posix'`](../../11%EC%B0%A8/recover.py#L280)

**오류 메시지:** 실제 복구는 동일 Docker Linux에서 실행해야 합니다.

**거부 조건:** [`Path(module.__file__).resolve().parent != ORIGINAL.resolve()`](../../11%EC%B0%A8/recover.py#L42)

**오류 메시지:** 다른 프로젝트의 모듈은 실행할 수 없습니다.

**거부 조건:** [`target.stat().st_size != spec['size'] or self.data.digest_file(target, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L195)

**오류 메시지:** 기존 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`state.get('state') == 'running'`](../../11%EC%B0%A8/recover.py#L226)

**오류 메시지:** 기존 사전 수신 상태가 실행 중입니다.

**거부 조건:** [`any(value.get('state') in worker.ACTIVE for value in worker.jobs())`](../../11%EC%B0%A8/recover.py#L284)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/recover.py#L92)

**오류 메시지:** 수신 경로의 연결 파일을 허용하지 않습니다.

**거부 조건:** [`marker.exists()`](../../11%EC%B0%A8/recover.py#L96)

**오류 메시지:** 이전 수신의 원장·디스크 반영이 불확실합니다. 복구 기록 감사가 필요합니다.

**거부 조건:** [`partial.exists() and (not metadata.exists() or self.data.load(metadata) != identity)`](../../11%EC%B0%A8/recover.py#L101)

**오류 메시지:** 부분 파일의 공식 원자료 계약이 다릅니다.

**거부 조건:** [`start &gt; spec['size']`](../../11%EC%B0%A8/recover.py#L104)

**오류 메시지:** 부분 파일이 공식 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or self.data.digest_file(partial, 'md5') != spec['md5']`](../../11%EC%B0%A8/recover.py#L189)

**오류 메시지:** 완성 원자료의 공식 크기·MD5가 다릅니다.

**거부 조건:** [`saved != start or self.data.load(metadata) != identity`](../../11%EC%B0%A8/recover.py#L116)

**오류 메시지:** 수신 중 부분 파일·계약이 변경됐습니다.

**거부 조건:** [`budget.used + end - start + 1 &gt; budget.limit`](../../11%EC%B0%A8/recover.py#L118)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`(partial.stat().st_size if partial.exists() else 0) != start`](../../11%EC%B0%A8/recover.py#L166)

**오류 메시지:** 닫힌 부분 파일의 실제 저장량이 다릅니다.

**거부 조건:** [`budget.path.exists() and self.data.load(budget.path)['download_bytes'] != budget.used`](../../11%EC%B0%A8/recover.py#L168)

**오류 메시지:** 실제 전송 원장이 메모리 계상과 다릅니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../11%EC%B0%A8/recover.py#L130)

**오류 메시지:** 공식 범위 응답이 요청과 다릅니다.

**거부 조건:** [`len(block) &gt; end - start + 1`](../../11%EC%B0%A8/recover.py#L153)

**오류 메시지:** 수신 본문이 공식 범위를 넘었습니다.

**거부 조건:** [`stream.write(block) != len(block)`](../../11%EC%B0%A8/recover.py#L156)

**오류 메시지:** 부분 파일을 모두 기록하지 못했습니다.


### [verify_sources.py](../../11%EC%B0%A8/verify_sources.py)


**설정·옵션:** [`--expected-digest`](../../11%EC%B0%A8/verify_sources.py#L43)

**코드의 선언:** ``

**설정·옵션:** [`--print-digest`](../../11%EC%B0%A8/verify_sources.py#L44)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../11%EC%B0%A8/verify_sources.py#L9)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`PRODUCTS`](../../11%EC%B0%A8/verify_sources.py#L10)

**코드의 선언:** `정의=('README.md', 'docs/복구설계.md', 'original-baseline.json', 'recover.py', 'tests/test_recover.py', 'verify_sources.py', '변경기록.md')`


**거부 조건:** [`args.expected_digest and (not re.fullmatch(r'[0-9a-f]{64}', args.expected_digest) or digest != args.expected_digest)`](../../11%EC%B0%A8/verify_sources.py#L49)

**오류 메시지:** 외부 검사 명세에 고정한 11차 해시와 다릅니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L17)

**오류 메시지:** 제품 파일의 링크를 허용하지 않습니다.

**거부 조건:** [`path.is_symlink() or getattr(path, 'is_junction', lambda: False)()`](../../11%EC%B0%A8/verify_sources.py#L32)

**오류 메시지:** 제품 경로의 링크를 허용하지 않습니다.


</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

복구 가능 여부는 기준 파일과 실제 상태 대조 결과입니다. 학습·평가 완료와 별도입니다.

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

10차에서 11차로 이어지는 실제 파일 비교입니다.

[전체 비교·자료 범위](../comparisons/10-to-11.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>파일별 비교·크기·해시 자세히 보기</summary>

[11차 폴더](../../11차/) · [실행과 계약](../../11차/README.md) · [변경 기록](../../11차/변경기록.md) · [10차와 전체 비교](../comparisons/10-to-11.md)

</details>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../11%EC%B0%A8) · [← 이전: 10차](round-10.md) · [다음: 12차 →](round-12.md)
