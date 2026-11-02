<div align="center">

# 🧹 12차 · 실험 종료 후 보고서 생성 도구

이미 지정된 실험이 끝나고 결과·테스트·가중치 해시가 일치할 때 작성자 관점의 Word와 같은 원고 PDF를 만드는 후처리 소프트웨어입니다. 이 도구는 자료 다운로드나 학습을 시작하지 않습니다. 실패·중단을 성공으로 바꾸지 않으며 실측 전 성능을 만들지 않습니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 원본 자료](../../12%EC%B0%A8) · [← 이전: 11차](round-11.md)

## 🎯 목적과 이 차수의 역할

이미 지정된 실험이 끝나고 결과·테스트·가중치 해시가 일치할 때 작성자 관점의 Word와 같은 원고 PDF를 만드는 후처리 소프트웨어입니다. 이 도구는 자료 다운로드나 학습을 시작하지 않습니다. 실패·중단을 성공으로 바꾸지 않으며 실측 전 성능을 만들지 않습니다.

<a name="features"></a>

## ✨ 핵심 기능과 보존 범위

| 항목 | 이 차수에서 확인할 내용 |
|---|---|
| 1 | 이미 지정된 실험이 끝나고 결과·테스트·가중치 해시가 일치할 때 작성자 관점의 Word와 같은 원고 PDF를 만드는 후처리 소프트웨어입니다. 이 도구는 자료 다운로드나 학습을 시작하지 않습니다. 실패·중단을 성공으로 바꾸지 않으며 실측 전 성능을 만들지 않습니다. |
| 2 | 공개 설명 본문은 보고서 생성기의 고정 템플릿이며, 실제 작성자 설정과 최종 보고서는 별도 비공개 자료입니다. 합성 결과로 만든 시제품의 8쪽 렌더와 44개 단위 검사는 실제 실험의 성과나 미래 최종 보고서 검토를 뜻하지 않습니다. |
| 3 | 기존 7차 동결 설치 환경이 필요합니다. 공개 저장소에는 기준 문서 두 개가 없고 검사 파일 하나의 줄바꿈 바이트가 달라 단독 복제본만으로 원본 해시 검사를 통과하지 못할 수 있습니다. 기준 해시를 현재 값으로 바꾸어 우회하지 않으며, 10차 안전 읽기와 글꼴 및 11차 복구 코드의 고정 의존성도 확인합니다. |

## 🔄 입력·처리·출력

| 단계 | 내용 |
|---|---|
| 📥 입력 | 종료된 지정 실험의 결과·테스트·가중치 해시 |
| ⚙️ 처리 | 완료 상태·해시 일치 확인 → 고정 템플릿에 실측값 반영 → Word·PDF 생성 |
| 📤 출력 | 같은 원고의 Word·PDF 보고서 |

<a name="usage"></a>

## 🖐️ 화면과 사용 흐름

1. 기존 7차 동결 환경과 10·11차 고정 의존성을 확인합니다.
2. 실험 종료·테스트·가중치 해시와 실제 결과의 대응을 확인합니다.
3. 보고서 생성기의 작성자 설정과 출력 위치를 준비합니다.
4. 같은 원고의 Word·PDF를 생성하고 실제 표·그림·수치를 검토합니다.

<a name="structure"></a>

## 📁 실제 자료 구성

| 경로 | 자료 종류 |
|---|---|
| [docs/](../../12%EC%B0%A8/docs) | 하위 자료 폴더 |
| [tests/](../../12%EC%B0%A8/tests) | 하위 자료 폴더 |
| [README.md](../../12%EC%B0%A8/README.md) | MD 파일 |
| [ROUTING-LESSONS.md](../../12%EC%B0%A8/ROUTING-LESSONS.md) | MD 파일 |
| [report_core.py](../../12%EC%B0%A8/report_core.py) | PY 파일 |
| [report_outputs.py](../../12%EC%B0%A8/report_outputs.py) | PY 파일 |
| [report_sections.json](../../12%EC%B0%A8/report_sections.json) | JSON 파일 |
| [verify_sources.py](../../12%EC%B0%A8/verify_sources.py) | PY 파일 |
| [watcher.py](../../12%EC%B0%A8/watcher.py) | PY 파일 |
| [변경기록.md](../../12%EC%B0%A8/%EB%B3%80%EA%B2%BD%EA%B8%B0%EB%A1%9D.md) | MD 파일 |

## 🧩 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [report_core.py](../../12%EC%B0%A8/report_core.py) | 학습을 실행하지 않고 보존된 실험 결과와 해시를 검증합니다. |
| [report_outputs.py](../../12%EC%B0%A8/report_outputs.py) | 검증된 결과로 Word 초안과 비공개 표·그림을 만듭니다. |
| [verify_sources.py](../../12%EC%B0%A8/verify_sources.py) | 배포 파일과 엄격 UTF-8 및 보존한 원본 해시를 검사합니다. |
| [watcher.py](../../12%EC%B0%A8/watcher.py) | 지정 작업 하나만 관찰하며 학습을 시작하거나 재개하지 않습니다. |
| [tests/fixtures.py](../../12%EC%B0%A8/tests/fixtures.py) | 보고서 검사용 합성 자료이며 실제 실험 결과가 아닙니다. |
| [tests/make_fixture.py](../../12%EC%B0%A8/tests/make_fixture.py) | 문서 품질 점검용 합성 결과만 생성하며 운영 작업을 읽지 않습니다. |
| [tests/test_outputs.py](../../12%EC%B0%A8/tests/test_outputs.py) | 문서의 실측·가상 구분과 렌더 차단을 검사합니다. |
| [tests/test_report.py](../../12%EC%B0%A8/tests/test_report.py) | 실제 학습 없이 고정 결과의 완료 판정과 보고서 정합성을 검사합니다. |
| [tests/test_watcher.py](../../12%EC%B0%A8/tests/test_watcher.py) | 운영 작업 없이 1회 생성과 불완료 및 보안 경계를 검사합니다. |

<a name="setup"></a>

## 🚀 설치 환경과 실행·사용법

report_core.py·report_outputs.py·watcher.py와 docs의 원본 계약·결과 해시·계획/렌더 서식을 확인합니다. 기존 완료 실험과 해당 문서 렌더 환경이 필요합니다.

실험 종료 후 후처리 도구를 사용합니다. 자료 다운로드나 학습을 시작하는 도구가 아닙니다. 공개 고정 템플릿과 비공개 작성자 설정·완성 보고서의 범위를 구분합니다.

### ⚙️ 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [watcher.py](../../12%EC%B0%A8/watcher.py) | `--plan`, `--once` |
| [make_fixture.py](../../12%EC%B0%A8/tests/make_fixture.py) | `--output`, `--font`, `--author` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>🔬 함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [report_core.py](../../12%EC%B0%A8/report_core.py)

| 정의 | 소스에 적힌 역할 |
|---|---|
| [`safe_reader`](../../12%EC%B0%A8/report_core.py#L18) | 공유 삭제 핸들을 사용한 기존 읽기를 원본 수정 없이 불러옵니다. |
| [`local_path`](../../12%EC%B0%A8/report_core.py#L43) | 기존 Docker 경로를 지정 프로젝트 안의 실제 파일로 대응합니다. |
| [`validate_bundle`](../../12%EC%B0%A8/report_core.py#L122) | 완료 상태와 결과 및 모든 동결 계약이 함께 맞을 때만 반환합니다. |
| [`match_rows`](../../12%EC%B0%A8/report_core.py#L215) | 7차와 같은 신뢰도 내림차순 탐욕 매칭이며 새 추론을 하지 않습니다. |

| 설정·옵션 | 코드의 선언 |
|---|---|
| [`TEST_SPLITS`](../../12%EC%B0%A8/report_core.py#L10) | `정의={'historical_taco': 'historical_test', 'new_plastopol': 'test',                'source_heldout_uav': 'external_test'}` |
| [`EVALUATOR`](../../12%EC%B0%A8/report_core.py#L12) | `정의='single-class confidence-greedy IoU; 101-point interpolated AP; v2'` |
| [`TEST_PROTOCOL`](../../12%EC%B0%A8/report_core.py#L13) | `정의='freeze model, tiles and threshold before tests; no test tuning; per-image prediction cache'` |
| [`SECTIONS`](../../12%EC%B0%A8/report_core.py#L14) | `정의=('overview', 'problem', 'development', 'architecture', 'dataset', 'preprocess',             'training', 'selection', 'results', 'analysis', 'application', 'limits', 'conclusion')` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not path.is_relative_to(project)`](../../12%EC%B0%A8/report_core.py#L38) | 근거 파일이 지정 프로젝트 경계를 벗어났습니다. |
| [`not isinstance(job_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', job_id)`](../../12%EC%B0%A8/report_core.py#L64) | 허용되지 않는 작업 ID입니다. |
| [`not isinstance(job, dict) or job.get('id') != job_id or job.get('kind') != 'train'`](../../12%EC%B0%A8/report_core.py#L72) | 지정 작업의 식별자 또는 종류가 일치하지 않습니다. |
| [`op.get('iou') != .5`](../../12%EC%B0%A8/report_core.py#L103) | 고정 IoU .5 계약이 아닙니다. |
| [`type(row.get('images')) is not int or row['images'] &lt;= 0`](../../12%EC%B0%A8/report_core.py#L107) | 실제 평가 이미지 수가 없습니다. |
| [`not isinstance(expected, str) or not re.fullmatch('[a-f0-9]{64}', expected)`](../../12%EC%B0%A8/report_core.py#L113) | SHA-256 형식이 잘못됐습니다. |
| [`job.get('state') != 'complete'`](../../12%EC%B0%A8/report_core.py#L126) | 정상 완료 작업만 성공 보고서를 만들 수 있습니다. |
| [`not isinstance(final, dict) or job.get('result') != final`](../../12%EC%B0%A8/report_core.py#L129) | 작업 결과와 최종 결과가 일치하지 않습니다. |
| [`selection != final['selected'] or test_contract['selected'] != selection or test_contract['experiment'] != experiment`](../../12%EC%B0%A8/report_core.py#L137) | 선택 및 테스트 계약이 최종 결과와 다릅니다. |
| [`selection not in comparison`](../../12%EC%B0%A8/report_core.py#L139) | 검증 비교표에 선택된 모델이 없습니다. |
| [`test_contract.get('protocol') != TEST_PROTOCOL`](../../12%EC%B0%A8/report_core.py#L141) | 고정 테스트의 프로토콜이 다릅니다. |
| [`selection.get('imgsz') != config['evaluation_imgsz']             or selection.get('policy') not in config['validation_policies']             or selection.get('evaluator') != EVALUATOR`](../../12%EC%B0%A8/report_core.py#L143) | 선택된 모델의 추론 및 평가 설정이 고정 명세와 다릅니다. |
| [`set(final['tests']) != set(TEST_SPLITS)`](../../12%EC%B0%A8/report_core.py#L147) | 세 고정 테스트가 모두 있어야 합니다. |
| [`final.get('test') != final['tests']['historical_taco']`](../../12%EC%B0%A8/report_core.py#L149) | 주평가 결과가 과거 TACO와 일치하지 않습니다. |
| [`final['manifest_sha256'] != experiment['manifest_sha256']`](../../12%EC%B0%A8/report_core.py#L152) | 최종 manifest 계약이 다릅니다. |
| [`final['counts'] != manifest['counts']`](../../12%EC%B0%A8/report_core.py#L160) | 데이터 집계와 manifest가 다릅니다. |
| [`set(selection['weights']) != set(selected_weights)`](../../12%EC%B0%A8/report_core.py#L163) | 선택 가중치와 해시 목록이 다릅니다. |
| [`final.get('target_met') != targets['historical_taco']             or final.get('all_test_targets_met') != all(targets.values())`](../../12%EC%B0%A8/report_core.py#L200) | 기록된 목표 판정과 실제 정밀도·재현율이 다릅니다. |
| [`tuple(row['id'] for row in data['sections']) != SECTIONS`](../../12%EC%B0%A8/report_core.py#L301) | 보고서 고정 본문의 절 구성이 계약과 다릅니다. |
| [`not all(row['paragraphs'] and all(isinstance(p, str) and p.strip() for p in row['paragraphs']) for row in data['sections'])`](../../12%EC%B0%A8/report_core.py#L303) | 보고서 본문 문단이 비었습니다. |
| [`type(op.get(key)) is not int or op[key] &lt; 0`](../../12%EC%B0%A8/report_core.py#L93) | TP/FP/FN은 음수가 아닌 정수여야 합니다. |
| [`not isinstance(predictions, list) or any(len(p) != 5 or not all(math.isfinite(v) for v in p) for p in predictions)`](../../12%EC%B0%A8/report_core.py#L263) | 고정 예측 캐시 형식이 잘못됐습니다. |
| [`len(values) != 5 or values[0] != 0 or not all(math.isfinite(v) for v in values)`](../../12%EC%B0%A8/report_core.py#L257) | 고정 정답 라벨 형식이 잘못됐습니다. |

### [report_outputs.py](../../12%EC%B0%A8/report_outputs.py)

| 정의 | 소스에 적힌 역할 |
|---|---|
| [`plot`](../../12%EC%B0%A8/report_outputs.py#L36) | 축과 단위 및 범례가 있는 정적 그래프를 별도 분석 도구 없이 그립니다. |
| [`create_docx`](../../12%EC%B0%A8/report_outputs.py#L112) | 저작 전 마커는 이 함수를 호출하는 진입점에서 실행해야 합니다. |
| [`render_document`](../../12%EC%B0%A8/report_outputs.py#L251) | 검토한 명시적 렌더 설정 없이는 실행하지 않습니다. |

| 설정·옵션 | 코드의 선언 |
|---|---|
| [`LABELS`](../../12%EC%B0%A8/report_outputs.py#L17) | `정의={'historical_taco': '과거 TACO 고정 테스트', 'new_plastopol': 'PlastOPol 고정 테스트',           'source_heldout_uav': 'UAVVaste 외부 출처 테스트'}` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not config or config.get('approved') is not True`](../../12%EC%B0%A8/report_outputs.py#L253) | 문서 렌더 환경의 명시적 승인 전에는 최종 납품을 준비하지 않습니다. |
| [`not all(p.is_file() for p in (python,helper,soffice))`](../../12%EC%B0%A8/report_outputs.py#L258) | 렌더 설정의 실제 실행 파일이 없습니다. |
| [`config.get('helper_sha256') != hashlib.sha256(helper.read_bytes()).hexdigest()`](../../12%EC%B0%A8/report_outputs.py#L260) | 검토한 렌더 도구 해시가 다릅니다. |
| [`result.returncode`](../../12%EC%B0%A8/report_outputs.py#L270) | 공식 문서 렌더 명령이 실패했습니다. 비공개 렌더 영수증을 확인하세요. |
| [`not pdf.is_file() or not pdf.stat().st_size or not pages`](../../12%EC%B0%A8/report_outputs.py#L274) | PDF 또는 전체 페이지 렌더 결과가 없습니다. |

### [verify_sources.py](../../12%EC%B0%A8/verify_sources.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT`](../../12%EC%B0%A8/verify_sources.py#L8) | `정의=Path(__file__).resolve().parent` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`sha(ROOT/'report_sections.json')!=contract['narrative_sha256']`](../../12%EC%B0%A8/verify_sources.py#L55) | 별도 담당자가 동결한 본문이 변경됐습니다. |

### [watcher.py](../../12%EC%B0%A8/watcher.py)

| 정의 | 소스에 적힌 역할 |
|---|---|
| [`watch_lock`](../../12%EC%B0%A8/watcher.py#L22) | 프로세스가 종료되면 운영체제가 해제하는 단일 관찰 잠금입니다. |
| [`publish_pair`](../../12%EC%B0%A8/watcher.py#L87) | 검증된 같은 원고 두 파일만 신규 납품 폴더에 저장합니다. |
| [`verify_receipt`](../../12%EC%B0%A8/watcher.py#L98) | 운영 영수증만으로 완료를 믿지 않고 실제 두 파일과 입력을 대조합니다. |

| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--plan`](../../12%EC%B0%A8/watcher.py#L188) | `required=True; help='비공개 계획 JSON'` |
| [`--once`](../../12%EC%B0%A8/watcher.py#L189) | `action='store_true'; help='한 번 읽고 종료하며 학습은 실행하지 않음'` |
| [`ROOT`](../../12%EC%B0%A8/watcher.py#L17) | `정의=Path(__file__).resolve().parent` |
| [`INTERVAL_SECONDS`](../../12%EC%B0%A8/watcher.py#L18) | `정의=60` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`plan.get('schema') != 1`](../../12%EC%B0%A8/watcher.py#L56) | 지원하지 않는 비공개 계획 형식입니다. |
| [`not output.is_relative_to(project / '최종')`](../../12%EC%B0%A8/watcher.py#L62) | 납품 위치는 프로젝트 최종 폴더 안이어야 합니다. |
| [`not support.is_relative_to(project / '12차/work')`](../../12%EC%B0%A8/watcher.py#L64) | 비공개 지원 자료는 12차 work 안이어야 합니다. |
| [`output == project / '최종' or output == support`](../../12%EC%B0%A8/watcher.py#L66) | 기존 최종 폴더를 직접 덮어쓸 수 없습니다. |
| [`plan.get('deliver_formats') != ['docx', 'pdf']`](../../12%EC%B0%A8/watcher.py#L68) | 최종 납품은 Word와 같은 원고 PDF 두 개만 허용합니다. |
| [`not isinstance(plan.get('author'), str) or not plan['author'].strip()`](../../12%EC%B0%A8/watcher.py#L70) | 비공개 계획에 작성자를 지정해야 합니다. |
| [`not node.is_file() or not script.is_file()`](../../12%EC%B0%A8/watcher.py#L78) | 저작 마커의 실제 Node 또는 스크립트가 없습니다. |
| [`{p.name for p in output.iterdir()} != {'최종보고서.docx', '최종보고서.pdf'}`](../../12%EC%B0%A8/watcher.py#L93) | 최종 납품 폴더의 파일 구성이 두 형식과 다릅니다. |
| [`receipt.get('job_id')!=plan['job_id'] or receipt.get('state') not in ('complete','incomplete_report')             or receipt.get('output_dir')!=relative(output,project)             or set(receipt.get('outputs',{}))!=expected_names`](../../12%EC%B0%A8/watcher.py#L101) | 기존 완료 영수증의 작업·출력 위치·파일 목록이 다릅니다. |
| [`not output.is_dir() or {p.name for p in output.iterdir()}!=expected_names`](../../12%EC%B0%A8/watcher.py#L105) | 완료 영수증에 해당하는 실제 두 보고서 파일이 없습니다. |
| [`output.exists()`](../../12%EC%B0%A8/watcher.py#L139) | 기존 최종 결과는 덮어쓰지 않습니다. |
| [`state!='validate' or not isinstance(final,dict) or job.get('result')!=final                 or digest(project/'7차/work/training/final.json')!=receipt.get('input_final_sha256')`](../../12%EC%B0%A8/watcher.py#L118) | 완료 보고서의 지정 작업 및 최종 입력 바인딩이 다릅니다. |
| [`state!='incomplete' or receipt.get('input_final_sha256') is not None`](../../12%EC%B0%A8/watcher.py#L121) | 미완료 보고서와 현재 지정 작업의 상태가 다릅니다. |

</details>

<a name="results"></a>

## 📊 처리 결과와 출력 읽기

결과 해시·테스트·가중치 결합을 확인한 뒤 만든 Word·PDF의 표·그림·수치를 대조합니다. 공개 템플릿 자체가 작성 완료 보고서는 아닙니다.

## 🛠️ 제약과 문제 해결

| 상황 | 확인할 내용 |
|---|---|
| 결과 준비 대기 | watcher의 완료 상태와 해시 계약을 확인합니다. |
| 렌더 실패 | 보고서 출력 도구와 렌더 설정, 출력 파일을 확인합니다. |

<a name="changes"></a>

## 🔍 직전 자료와 전체 비교

11차에서 12차로 이어지는 실제 파일 비교입니다.

[📄 전체 비교·자료 범위](../comparisons/11-to-12.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>📚 파일별 비교·크기·해시 자세히 보기</summary>

[12차 폴더](../../12차/) · [실행과 범위](../../12차/README.md) · [변경 기록](../../12차/변경기록.md) · [11차와 전체 비교](../comparisons/11-to-12.md)

</details>

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 원본 자료](../../12%EC%B0%A8) · [← 이전: 11차](round-11.md)
