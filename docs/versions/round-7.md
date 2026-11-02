<div align="center">

# 🧹 7차

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 원본 자료](../../7%EC%B0%A8) · [← 이전: 5차](round-5.md) · [다음: 8차 →](round-8.md)

## 🎯 목적과 이 차수의 역할

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

<a name="features"></a>

## ✨ 핵심 기능과 보존 범위

| 항목 | 이 차수에서 확인할 내용 |
|---|---|
| 1 | 대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다. |

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
| [configs/](../../7%EC%B0%A8/configs) | 하위 자료 폴더 |
| [docs/](../../7%EC%B0%A8/docs) | 하위 자료 폴더 |
| [tests/](../../7%EC%B0%A8/tests) | 하위 자료 폴더 |
| [README.md](../../7%EC%B0%A8/README.md) | MD 파일 |
| [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py) | PY 파일 |
| [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py) | PY 파일 |
| [verify_sources.py](../../7%EC%B0%A8/verify_sources.py) | PY 파일 |
| [worker.py](../../7%EC%B0%A8/worker.py) | PY 파일 |
| [사용안내.txt](../../7%EC%B0%A8/%EC%82%AC%EC%9A%A9%EC%95%88%EB%82%B4.txt) | TXT 파일 |
| [학습상태.bat](../../7%EC%B0%A8/%ED%95%99%EC%8A%B5%EC%83%81%ED%83%9C.bat) | BAT 파일 |
| [학습실행.bat](../../7%EC%B0%A8/%ED%95%99%EC%8A%B5%EC%8B%A4%ED%96%89.bat) | BAT 파일 |

## 🧩 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [worker.py](../../7%EC%B0%A8/worker.py) | 준비와 GPU 학습을 Codex 없이 이어 실행하는 독립 작업자입니다. |
| [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py) | 공식 원자료를 보존하고 별도 정규화 사본·고정 분할을 준비합니다. |
| [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py) | 학습 시간을 제한하고 검증에서 모델·추론을 선택한 뒤 고정 테스트를 평가합니다. |
| [verify_sources.py](../../7%EC%B0%A8/verify_sources.py) | 소스 UTF-8·구문·실제 진입점·기존 모델 보존을 검사합니다. |
| [tests/test_prepare_dataset.py](../../7%EC%B0%A8/tests/test_prepare_dataset.py) | 원본 보존·예산·분할 누출·좌표 변환의 실패 경로를 검사합니다. |
| [tests/test_train_pipeline.py](../../7%EC%B0%A8/tests/test_train_pipeline.py) | 검증 선택·예측 좌표·재개 계약·고정 테스트의 경계를 검사합니다. |
| [tests/test_worker.py](../../7%EC%B0%A8/tests/test_worker.py) | 독립 작업의 중복 배제·상태·명시 재개 계약을 검사합니다. |

<a name="setup"></a>

## 🚀 설치 환경과 실행·사용법

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

### 📖 이 차수 원래 안내의 세부 조건

### 실행 조건

현재 운영 환경은 Windows D:/2026/월요일 PBL/7차, Docker컨테이너2026과 /workspace/2026 마운트, /opt/venvs/torch/bin/python입니다. 기존 모델·자료·5차 결과가 필요하고 이 저장소에는 모델·데이터·EXE·로그·인증정보·개인 지침을 포함하지 않습니다. 복제만으로 전체 실험이 재현된다고 보장하지 않습니다.

학습실행.bat은자료 준비와학습을독립프로세스로시작하고학습상태.bat은실제생존상태를조회합니다. 같은준비/학습을중복실행하지않고실패원문을보존합니다. 명시적재개에는원본·코드·모델·설정계약일치가필요합니다. Codex/API토큰을요구하지않지만PC와Docker는실행돼있어야합니다.

신규전송상한100GiB,최소잔여100GiB를확인합니다. 사전수신과제품준비는동일Linux의공유flock을사용하며완료된공식원본크기·MD5·SHA를재확인하고전송원장을한번만합산합니다.

### 학습과 평가

COCO YOLO26l960/batch4/최대60epochs와기존작은물체l-P2 1280/batch2/최대45epochs의두후보를비교합니다. 후보별누적학습예산6시간과patience12,epoch callback상한을적용합니다. 시간확인은배치·검증경계에서이뤄지고최종검증·checkpoint저장시간은추가될수있습니다. 강제종료시마지막시간원장저장뒤의일부시간이보존되지않을수있어반복강제종료에도엄밀한실제누적시간보증이라고표현하지않습니다.

TACO validation에서모델·일반/분할추론·신뢰도를선택해고정한후테스트합니다. 기존TACO test150은이미사용한historical benchmark이고,PlastOPol은사진·근접중복통제평가이며촬영장소독립성은미확인입니다. UAVVaste는항공시점외부테스트로CCTV정확도와구분합니다. 없어진과거원본1232장은전체지각중복검증을하지못한한계가있습니다. 테스트성능으로다시튜닝하거나쉬운출처하나만90%라고전체달성을주장하지않습니다.

### ⚙️ 소스에서 제공하는 CLI 옵션

| 진입 소스 | 정의된 옵션 이름 |
|---|---|
| [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py) | `--prepare`, `--smoke` |
| [worker.py](../../7%EC%B0%A8/worker.py) | `--action`, `--params`, `--worker` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>🔬 함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)

| 정의 | 소스에 적힌 역할 |
|---|---|
| [`_DownloadRetry`](../../7%EC%B0%A8/prepare_dataset.py#L234) | 통신 경계에서 확인한 일시 오류만 재시도 경로로 전달합니다. |

| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--prepare`](../../7%EC%B0%A8/prepare_dataset.py#L796) | `action='store_true'` |
| [`--smoke`](../../7%EC%B0%A8/prepare_dataset.py#L797) | `action='store_true'` |
| [`ROOT`](../../7%EC%B0%A8/prepare_dataset.py#L25) | `정의=Path(__file__).resolve().parent` |
| [`WORK`](../../7%EC%B0%A8/prepare_dataset.py#L26) | `정의=ROOT / 'work'` |
| [`SOURCES`](../../7%EC%B0%A8/prepare_dataset.py#L27) | `정의=WORK / 'sources'` |
| [`TRAINING`](../../7%EC%B0%A8/prepare_dataset.py#L28) | `정의=WORK / 'training'` |
| [`ARCHIVE`](../../7%EC%B0%A8/prepare_dataset.py#L29) | `정의=ROOT.parent / '이전 도커 실험/3차실험/trash_round3'` |
| [`PREVIOUS`](../../7%EC%B0%A8/prepare_dataset.py#L30) | `정의=ROOT.parent / '5차/work/training'` |
| [`SEED`](../../7%EC%B0%A8/prepare_dataset.py#L31) | `정의=20261030` |
| [`MAX_BYTES`](../../7%EC%B0%A8/prepare_dataset.py#L32) | `정의=100 * 1024**3` |
| [`MINIMUM_FREE`](../../7%EC%B0%A8/prepare_dataset.py#L33) | `정의=100 * 1024**3` |
| [`NORMALIZATION`](../../7%EC%B0%A8/prepare_dataset.py#L34) | `정의='rgb-jpeg-quality95-subsampling0-no-exif-no-rotation-v1'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not all(math.isfinite(x) and x &gt; 0 for x in (width, height))`](../../7%EC%B0%A8/prepare_dataset.py#L116) | COCO 이미지 크기가 잘못됐습니다. |
| [`source.resolve() == target.resolve()`](../../7%EC%B0%A8/prepare_dataset.py#L147) | 원본을 정규화 결과로 덮어쓸 수 없습니다. |
| [`target.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L158) | 출처 대응이 없는 기존 정규화 사본입니다. |
| [`not url.startswith('https://') and not url.startswith('http://127.0.0.1:')`](../../7%EC%B0%A8/prepare_dataset.py#L228) | 공식 HTTPS 출처만 허용됩니다. |
| [`start &gt; spec['size']`](../../7%EC%B0%A8/prepare_dataset.py#L325) | 부분 파일 크기가 원본보다 큽니다. |
| [`partial.stat().st_size != spec['size'] or digest_file(partial,'md5') != spec['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L394) | 완성 원자료의 공식 MD5가 일치하지 않습니다. |
| [`destination.is_symlink() or getattr(destination,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L403) | ZIP 추출 시작 위치가 파일 링크입니다. |
| [`parent['split'] != 'train'`](../../7%EC%B0%A8/prepare_dataset.py#L513) | crop 증강은 train 부모에서만 생성합니다. |
| [`not (0 &lt;= left &lt; right &lt;= parent['width'] and 0 &lt;= top &lt; bottom &lt;= parent['height'])`](../../7%EC%B0%A8/prepare_dataset.py#L516) | crop 영역이 부모 이미지 범위를 벗어났습니다. |
| [`path.exists() and path.read_text(encoding='utf-8')!=text`](../../7%EC%B0%A8/prepare_dataset.py#L548) | 기존 학습 라벨이 새 변환과 다릅니다. |
| [`sha256_file(path)!=manifest['historical_protection_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L591) | 과거 사용 자료 보호 명세가 바뀌었습니다. |
| [`os.name!='posix'`](../../7%EC%B0%A8/prepare_dataset.py#L660) | 실제 자료 준비는 동일 Docker2026/Linux 안에서 실행해야 합니다. |
| [`groups['val']&lt;3 or groups['test']&lt;3`](../../7%EC%B0%A8/prepare_dataset.py#L743) | PlastOPol 검증·테스트의 독립 이미지 그룹이 부족합니다. |
| [`before!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L780) | smoke 원본이 보존 계약과 다릅니다. |
| [`sha256_file(raw)!=before`](../../7%EC%B0%A8/prepare_dataset.py#L786) | smoke에서 원본이 변경됐습니다. |
| [`len(row) != 5 or row[0] != 0 or not all(map(math.isfinite, row))`](../../7%EC%B0%A8/prepare_dataset.py#L103) | 단일 trash 클래스와 유한한 좌표가 필요합니다. |
| [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x-width/2 and x+width/2 &lt;= 1+tolerance                                           and -tolerance &lt;= y-height/2 and y+height/2 &lt;= 1+tolerance)`](../../7%EC%B0%A8/prepare_dataset.py#L107) | 라벨이 이미지 경계를 벗어났습니다. |
| [`not all(map(math.isfinite, (x,y,w,h))) or w &lt;= 0 or h &lt;= 0`](../../7%EC%B0%A8/prepare_dataset.py#L126) | COCO 상자가 잘못됐습니다. |
| [`x &lt; -tolerance or y &lt; -tolerance or x+w &gt; width+tolerance or y+h &gt; height+tolerance`](../../7%EC%B0%A8/prepare_dataset.py#L129) | COCO 상자가 이미지 범위를 벗어났습니다. |
| [`result['raw_sha256'] != raw_hash or result['normalization'] != NORMALIZATION or result['sha256'] != sha256_file(target)`](../../7%EC%B0%A8/prepare_dataset.py#L153) | 정규화 사본의 보존 계약이 다릅니다. |
| [`(result['width'],result['height']) != tuple(expected_size)`](../../7%EC%B0%A8/prepare_dataset.py#L155) | 정규화 사본과 주석 크기가 다릅니다. |
| [`original.size != tuple(expected_size) or original.width*original.height &gt; 100000000`](../../7%EC%B0%A8/prepare_dataset.py#L164) | 해독한 원본 크기와 주석 좌표계가 다릅니다. |
| [`not encoded.endswith(b'\xff\xd9')`](../../7%EC%B0%A8/prepare_dataset.py#L173) | 정규화 JPEG의 종료 표식이 없습니다. |
| [`self.used &lt; 0 or self.used &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L196) | 기존 전송량이 7차 예산과 맞지 않습니다. |
| [`count &lt; 0 or free-count &lt; self.minimum_free`](../../7%EC%B0%A8/prepare_dataset.py#L201) | 쓰기 후 잔여 공간 100GiB를 보장할 수 없습니다. |
| [`count &lt; 0 or self.used+count &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L205) | 7차 누적 전송 예산을 초과했습니다. |
| [`value['bytes'] &lt; 0 or self.used+value['bytes'] &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L221) | 사전 전송을 합치면 7차 전송 예산을 초과합니다. |
| [`not metadata.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L319) | 출처 없는 부분 다운로드입니다. |
| [`old.get('url') != identity['url'] or old.get('size') != identity['size'] or old.get('md5',identity['md5']) != identity['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L322) | 부분 다운로드의 원자료 계약이 다릅니다. |
| [`row.get('available') and sha256_file(local(row['raw_image']))!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L594) | 추가로 대조한 과거 사용 원본이 바뀌었습니다. |
| [`manifest['contract']!=contract`](../../7%EC%B0%A8/prepare_dataset.py#L672) | 준비된 데이터 계약이 다릅니다. |
| [`sha256_file(raw)!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L695) | 보존 TACO 원본·라벨 계약과 다릅니다. |
| [`self.imports[identity] != value`](../../7%EC%B0%A8/prepare_dataset.py#L218) | 이미 합산한 사전 전송 영수증이 변경됐습니다. |
| [`state.get('state')=='running'`](../../7%EC%B0%A8/prepare_dataset.py#L290) | 수신 잠금은 풀렸지만 사전 수신 상태가 running입니다. 원인을 확인해야 합니다. |
| [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L334) | 재시도 전 부분 파일 크기·원자료 계약이 변경됐습니다. |
| [`budget.used+remaining &gt; budget.limit`](../../7%EC%B0%A8/prepare_dataset.py#L338) | 남은 전송 예산이 부족합니다. |
| [`path.is_absolute() or '..' in path.parts or ':' in info.filename or stat.S_ISLNK(info.external_attr &gt;&gt; 16)`](../../7%EC%B0%A8/prepare_dataset.py#L410) | ZIP에 허용하지 않는 경로가 있습니다. |
| [`not target.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L419) | ZIP 추출 경로가 원본 보관 폴더를 벗어납니다. |
| [`temporary.is_symlink() or not temporary.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L432) | ZIP 임시 파일이 허용 경로를 벗어납니다. |
| [`temporary.stat().st_size != info.file_size`](../../7%EC%B0%A8/prepare_dataset.py#L436) | ZIP 추출 크기가 다릅니다. |
| [`sha256_file(path)!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L572) | 과거 추가 자료가 보존 manifest와 다릅니다. |
| [`not match`](../../7%EC%B0%A8/prepare_dataset.py#L705) | 과거 pLitter 원본 ID를 확인할 수 없습니다. |
| [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/prepare_dataset.py#L283) | 공식 자료 수신 잠금 대기 12시간을 초과했습니다. |
| [`not target.exists() or sha256_file(target)!=receipt['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L300) | 사전 수신 SHA와 완성 원자료가 다릅니다. |
| [`existing.is_symlink() or getattr(existing,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L417) | ZIP 추출 경로에 기존 파일 링크가 있습니다. |
| [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../7%EC%B0%A8/prepare_dataset.py#L349) | 서버가 원본 범위 요청을 보존하지 않았습니다. |
| [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L378) | 실패 수신 후 부분 파일 크기·원자료 계약이 변경됐습니다. |
| [`len(block)&gt;remaining`](../../7%EC%B0%A8/prepare_dataset.py#L368) | 수신 본문이 요청한 원본 범위를 초과했습니다. |

### [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`EVALUATOR`](../../7%EC%B0%A8/train_pipeline.py#L12) | `정의='single-class confidence-greedy IoU; 101-point interpolated AP; v2'` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not results`](../../7%EC%B0%A8/train_pipeline.py#L69) | 검증 후보가 없습니다. |
| [`not math.isfinite(elapsed) or elapsed&lt;0 or hours*3600-elapsed&lt;=0`](../../7%EC%B0%A8/train_pipeline.py#L84) | 후보의 누적 학습 시간 예산이 끝났거나 잘못됐습니다. |
| [`width&lt;=0 or height&lt;=0 or grid not in (1,2,3)`](../../7%EC%B0%A8/train_pipeline.py#L94) | 허용하지 않는 타일 크기입니다. |
| [`path.exists() and load(path)!=contract`](../../7%EC%B0%A8/train_pipeline.py#L118) | checkpoint 원본·데이터·코드·학습 계약이 다릅니다. |
| [`not torch.cuda.is_available()`](../../7%EC%B0%A8/train_pipeline.py#L162) | CUDA GPU가 없습니다. CPU로 장기 학습을 우회하지 않습니다. |
| [`any(list(model.names.values())!=['trash'] for model in models)`](../../7%EC%B0%A8/train_pipeline.py#L188) | 단일 trash 클래스 모델이 아닙니다. |
| [`not best.exists()`](../../7%EC%B0%A8/train_pipeline.py#L310) | 학습 완료 가중치가 없습니다. |
| [`type(resume) is not bool`](../../7%EC%B0%A8/train_pipeline.py#L327) | 재개는 명시적 bool이어야 합니다. |
| [`not path.exists()`](../../7%EC%B0%A8/train_pipeline.py#L120) | 완료 학습의 원래 계약이 없습니다. |
| [`not best.exists() or sha256_file(best)!=load(directory/'phase_complete.json')['best_sha256']`](../../7%EC%B0%A8/train_pipeline.py#L122) | 완료 학습 가중치가 보존 해시와 다릅니다. |
| [`not path.exists() or not allow_resume`](../../7%EC%B0%A8/train_pipeline.py#L126) | 중단 checkpoint는 동일 계약과 명시적 재개가 필요합니다. |
| [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/train_pipeline.py#L168) | 다른 GPU 작업 때문에 필요한 여유 VRAM을 확보하지 못했습니다. |
| [`sha256_file(local(path))!=expected`](../../7%EC%B0%A8/train_pipeline.py#L320) | 선택 가중치가 최종 평가 계약과 다릅니다. |
| [`int(checkpoint.get('epoch',-1))&lt;0`](../../7%EC%B0%A8/train_pipeline.py#L297) | 완료 표식 없는 정리된 checkpoint입니다. 자동 재학습하지 않습니다. |

### [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`ROOT`](../../7%EC%B0%A8/verify_sources.py#L6) | `정의=Path(__file__).resolve().parent` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`config['download_limit_bytes']!=100*1024**3 or config['minimum_disk_free_bytes']!=100*1024**3`](../../7%EC%B0%A8/verify_sources.py#L23) | 신규 전송 예산·잔여 공간 계약이 다릅니다. |
| [`len(config['candidates'])!=2 or any(row['patience']!=12 for row in config['candidates'])`](../../7%EC%B0%A8/verify_sources.py#L25) | 검토한 두 후보 명세가 다릅니다. |

### [worker.py](../../7%EC%B0%A8/worker.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`--action`](../../7%EC%B0%A8/worker.py#L210) | `choices=['train', 'status']` |
| [`--params`](../../7%EC%B0%A8/worker.py#L211) | `default='{}'` |
| [`--worker`](../../7%EC%B0%A8/worker.py#L212) | `` |
| [`ROOT`](../../7%EC%B0%A8/worker.py#L15) | `정의=Path(__file__).resolve().parent` |
| [`WORK`](../../7%EC%B0%A8/worker.py#L16) | `정의=ROOT / 'work'` |
| [`PROC`](../../7%EC%B0%A8/worker.py#L17) | `정의=Path('/proc')` |
| [`ACTIVE`](../../7%EC%B0%A8/worker.py#L18) | `정의={'queued', 'running'}` |

| 거부 조건 | 오류 메시지 |
|---|---|
| [`not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value)`](../../7%EC%B0%A8/worker.py#L22) | 허용되지 않는 작업 ID입니다. |
| [`not isinstance(value, dict)`](../../7%EC%B0%A8/worker.py#L130) | 작업 기록이 없습니다. |
| [`not isinstance(params, dict) or set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../7%EC%B0%A8/worker.py#L158) | 설정은 resume: true 또는 false만 허용하는 JSON 객체입니다. |
| [`any(value.get('state') in ACTIVE for value in jobs())`](../../7%EC%B0%A8/worker.py#L162) | 준비 또는 학습 작업이 이미 진행 중입니다. |
| [`not value or value.get('state') != 'queued' or value.get('kind') != 'train'`](../../7%EC%B0%A8/worker.py#L186) | 새로 대기 중인 학습 작업만 실행할 수 있습니다. |
| [`not isinstance(result, dict)`](../../7%EC%B0%A8/worker.py#L195) | 학습 파이프라인이 결과 객체를 반환하지 않았습니다. |
| [`not blocking`](../../7%EC%B0%A8/worker.py#L62) | 준비 또는 학습 작업이 이미 진행 중입니다. |

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

5차에서 7차로 이어지는 실제 파일 비교입니다.

[📄 전체 비교·자료 범위](../comparisons/5-to-7.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>📚 파일별 비교·크기·해시 자세히 보기</summary>

[공개 폴더](../../7차/) · [실험과 실행 조건](../../7차/README.md) · [5차와 파일 비교](../comparisons/5-to-7.md)

[같은 7차의 다운로드 오류 수정과 전체 차이](../comparisons/7-recovery-20261030.md)도 함께 보존합니다.

</details>

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 원본 자료](../../7%EC%B0%A8) · [← 이전: 5차](round-5.md) · [다음: 8차 →](round-8.md)
