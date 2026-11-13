<div align="center">

<a name="-7차"></a>
# 7차

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

**기술 분류:** 컴퓨터 비전 · Python · 객체 탐지·실험 자료

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>
<!-- reading-levels:start -->
[LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

프로젝트 전체의 설명은 [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)부터 [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)까지 같은 범위로 연결됩니다.

<a id="reading-level-1"></a>
## LEVEL 1 - Beginner

### LEVEL 1 · 이 자료가 하는 일과 달라진 점

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

### LEVEL 1 · 실제 동작을 따라 읽기

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

CLI는 명령어와 옵션을 입력해 프로그램을 실행하는 방식입니다. epoch는 학습 자료를 한 차례 순회하는 단위입니다.

입력 — 쓰레기 영상·라벨·모델·선택한 차수 설정

처리 — 자료 준비·모델/영상 처리·평가 또는 상태 표시

출력 — 탐지 후보·평가 지표·화면·보고서

### LEVEL 1 · 준비하고 확인할 것

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 1 · 이 차수 원래 안내의 세부 조건

#### LEVEL 1 · 실행 조건

현재 운영 환경은 Windows D:/2026/월요일 PBL/7차, Docker컨테이너2026과 /workspace/2026 마운트, /opt/venvs/torch/bin/python입니다. 기존 모델·자료·5차 결과가 필요하고 이 저장소에는 모델·데이터·EXE·로그·인증정보·개인 지침을 포함하지 않습니다. 복제만으로 전체 실험이 재현된다고 보장하지 않습니다.

학습실행.bat은자료 준비와학습을독립프로세스로시작하고학습상태.bat은실제생존상태를조회합니다. 같은준비/학습을중복실행하지않고실패원문을보존합니다. 명시적재개에는원본·코드·모델·설정계약일치가필요합니다. Codex/API토큰을요구하지않지만PC와Docker는실행돼있어야합니다.

신규전송상한100GiB,최소잔여100GiB를확인합니다. 사전수신과제품준비는동일Linux의공유flock을사용하며완료된공식원본크기·MD5·SHA를재확인하고전송원장을한번만합산합니다.

#### LEVEL 1 · 학습과 평가

COCO YOLO26l960/batch4/최대60epochs와기존작은물체l-P2 1280/batch2/최대45epochs의두후보를비교합니다. 후보별누적학습예산6시간과patience12,epoch callback상한을적용합니다. 시간확인은배치·검증경계에서이뤄지고최종검증·checkpoint저장시간은추가될수있습니다. 강제종료시마지막시간원장저장뒤의일부시간이보존되지않을수있어반복강제종료에도엄밀한실제누적시간보증이라고표현하지않습니다.

TACO validation에서모델·일반/분할추론·신뢰도를선택해고정한후테스트합니다. 기존TACO test150은이미사용한historical benchmark이고,PlastOPol은사진·근접중복통제평가이며촬영장소독립성은미확인입니다. UAVVaste는항공시점외부테스트로CCTV정확도와구분합니다. 없어진과거원본1232장은전체지각중복검증을하지못한한계가있습니다. 테스트성능으로다시튜닝하거나쉬운출처하나만90%라고전체달성을주장하지않습니다.

#### LEVEL 1 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)<br>**정의된 옵션 이름:** `--prepare`, `--smoke` |
| **진입 소스:** [worker.py](../../7%EC%B0%A8/worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 1 · [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)

| 내용 |
| --- |
| **정의:** [`_DownloadRetry`](../../7%EC%B0%A8/prepare_dataset.py#L234)<br>**소스에 적힌 역할:** 통신 경계에서 확인한 일시 오류만 재시도 경로로 전달합니다. |

**설정·옵션:** [`--prepare`](../../7%EC%B0%A8/prepare_dataset.py#L796)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--smoke`](../../7%EC%B0%A8/prepare_dataset.py#L797)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../7%EC%B0%A8/prepare_dataset.py#L25)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`WORK`](../../7%EC%B0%A8/prepare_dataset.py#L26)

**코드의 선언:** `정의=ROOT / 'work'`

**설정·옵션:** [`SOURCES`](../../7%EC%B0%A8/prepare_dataset.py#L27)

**코드의 선언:** `정의=WORK / 'sources'`

**설정·옵션:** [`TRAINING`](../../7%EC%B0%A8/prepare_dataset.py#L28)

**코드의 선언:** `정의=WORK / 'training'`

**설정·옵션:** [`ARCHIVE`](../../7%EC%B0%A8/prepare_dataset.py#L29)

**코드의 선언:** `정의=ROOT.parent / '이전 도커 실험/3차실험/trash_round3'`

**설정·옵션:** [`PREVIOUS`](../../7%EC%B0%A8/prepare_dataset.py#L30)

**코드의 선언:** `정의=ROOT.parent / '5차/work/training'`

**설정·옵션:** [`SEED`](../../7%EC%B0%A8/prepare_dataset.py#L31)

**코드의 선언:** `정의=20261030`

**설정·옵션:** [`MAX_BYTES`](../../7%EC%B0%A8/prepare_dataset.py#L32)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`MINIMUM_FREE`](../../7%EC%B0%A8/prepare_dataset.py#L33)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`NORMALIZATION`](../../7%EC%B0%A8/prepare_dataset.py#L34)

**코드의 선언:** `정의='rgb-jpeg-quality95-subsampling0-no-exif-no-rotation-v1'`


**거부 조건:** [`not all(math.isfinite(x) and x &gt; 0 for x in (width, height))`](../../7%EC%B0%A8/prepare_dataset.py#L116)

**오류 메시지:** COCO 이미지 크기가 잘못됐습니다.

**거부 조건:** [`source.resolve() == target.resolve()`](../../7%EC%B0%A8/prepare_dataset.py#L147)

**오류 메시지:** 원본을 정규화 결과로 덮어쓸 수 없습니다.

**거부 조건:** [`target.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L158)

**오류 메시지:** 출처 대응이 없는 기존 정규화 사본입니다.

**거부 조건:** [`not url.startswith('https://') and not url.startswith('http://127.0.0.1:')`](../../7%EC%B0%A8/prepare_dataset.py#L228)

**오류 메시지:** 공식 HTTPS 출처만 허용됩니다.

**거부 조건:** [`start &gt; spec['size']`](../../7%EC%B0%A8/prepare_dataset.py#L325)

**오류 메시지:** 부분 파일 크기가 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or digest_file(partial,'md5') != spec['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L394)

**오류 메시지:** 완성 원자료의 공식 MD5가 일치하지 않습니다.

**거부 조건:** [`destination.is_symlink() or getattr(destination,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L403)

**오류 메시지:** ZIP 추출 시작 위치가 파일 링크입니다.

**거부 조건:** [`parent['split'] != 'train'`](../../7%EC%B0%A8/prepare_dataset.py#L513)

**오류 메시지:** crop 증강은 train 부모에서만 생성합니다.

**거부 조건:** [`not (0 &lt;= left &lt; right &lt;= parent['width'] and 0 &lt;= top &lt; bottom &lt;= parent['height'])`](../../7%EC%B0%A8/prepare_dataset.py#L516)

**오류 메시지:** crop 영역이 부모 이미지 범위를 벗어났습니다.

**거부 조건:** [`path.exists() and path.read_text(encoding='utf-8')!=text`](../../7%EC%B0%A8/prepare_dataset.py#L548)

**오류 메시지:** 기존 학습 라벨이 새 변환과 다릅니다.

**거부 조건:** [`sha256_file(path)!=manifest['historical_protection_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L591)

**오류 메시지:** 과거 사용 자료 보호 명세가 바뀌었습니다.

**거부 조건:** [`os.name!='posix'`](../../7%EC%B0%A8/prepare_dataset.py#L660)

**오류 메시지:** 실제 자료 준비는 동일 Docker2026/Linux 안에서 실행해야 합니다.

**거부 조건:** [`groups['val']&lt;3 or groups['test']&lt;3`](../../7%EC%B0%A8/prepare_dataset.py#L743)

**오류 메시지:** PlastOPol 검증·테스트의 독립 이미지 그룹이 부족합니다.

**거부 조건:** [`before!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L780)

**오류 메시지:** smoke 원본이 보존 계약과 다릅니다.

**거부 조건:** [`sha256_file(raw)!=before`](../../7%EC%B0%A8/prepare_dataset.py#L786)

**오류 메시지:** smoke에서 원본이 변경됐습니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(map(math.isfinite, row))`](../../7%EC%B0%A8/prepare_dataset.py#L103)

**오류 메시지:** 단일 trash 클래스와 유한한 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x-width/2 and x+width/2 &lt;= 1+tolerance                                           and -tolerance &lt;= y-height/2 and y+height/2 &lt;= 1+tolerance)`](../../7%EC%B0%A8/prepare_dataset.py#L107)

**오류 메시지:** 라벨이 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(map(math.isfinite, (x,y,w,h))) or w &lt;= 0 or h &lt;= 0`](../../7%EC%B0%A8/prepare_dataset.py#L126)

**오류 메시지:** COCO 상자가 잘못됐습니다.

**거부 조건:** [`x &lt; -tolerance or y &lt; -tolerance or x+w &gt; width+tolerance or y+h &gt; height+tolerance`](../../7%EC%B0%A8/prepare_dataset.py#L129)

**오류 메시지:** COCO 상자가 이미지 범위를 벗어났습니다.

**거부 조건:** [`result['raw_sha256'] != raw_hash or result['normalization'] != NORMALIZATION or result['sha256'] != sha256_file(target)`](../../7%EC%B0%A8/prepare_dataset.py#L153)

**오류 메시지:** 정규화 사본의 보존 계약이 다릅니다.

**거부 조건:** [`(result['width'],result['height']) != tuple(expected_size)`](../../7%EC%B0%A8/prepare_dataset.py#L155)

**오류 메시지:** 정규화 사본과 주석 크기가 다릅니다.

**거부 조건:** [`original.size != tuple(expected_size) or original.width*original.height &gt; 100000000`](../../7%EC%B0%A8/prepare_dataset.py#L164)

**오류 메시지:** 해독한 원본 크기와 주석 좌표계가 다릅니다.

**거부 조건:** [`not encoded.endswith(b'\xff\xd9')`](../../7%EC%B0%A8/prepare_dataset.py#L173)

**오류 메시지:** 정규화 JPEG의 종료 표식이 없습니다.

**거부 조건:** [`self.used &lt; 0 or self.used &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L196)

**오류 메시지:** 기존 전송량이 7차 예산과 맞지 않습니다.

**거부 조건:** [`count &lt; 0 or free-count &lt; self.minimum_free`](../../7%EC%B0%A8/prepare_dataset.py#L201)

**오류 메시지:** 쓰기 후 잔여 공간 100GiB를 보장할 수 없습니다.

**거부 조건:** [`count &lt; 0 or self.used+count &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L205)

**오류 메시지:** 7차 누적 전송 예산을 초과했습니다.

**거부 조건:** [`value['bytes'] &lt; 0 or self.used+value['bytes'] &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L221)

**오류 메시지:** 사전 전송을 합치면 7차 전송 예산을 초과합니다.

**거부 조건:** [`not metadata.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L319)

**오류 메시지:** 출처 없는 부분 다운로드입니다.

**거부 조건:** [`old.get('url') != identity['url'] or old.get('size') != identity['size'] or old.get('md5',identity['md5']) != identity['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L322)

**오류 메시지:** 부분 다운로드의 원자료 계약이 다릅니다.

**거부 조건:** [`row.get('available') and sha256_file(local(row['raw_image']))!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L594)

**오류 메시지:** 추가로 대조한 과거 사용 원본이 바뀌었습니다.

**거부 조건:** [`manifest['contract']!=contract`](../../7%EC%B0%A8/prepare_dataset.py#L672)

**오류 메시지:** 준비된 데이터 계약이 다릅니다.

**거부 조건:** [`sha256_file(raw)!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L695)

**오류 메시지:** 보존 TACO 원본·라벨 계약과 다릅니다.

**거부 조건:** [`self.imports[identity] != value`](../../7%EC%B0%A8/prepare_dataset.py#L218)

**오류 메시지:** 이미 합산한 사전 전송 영수증이 변경됐습니다.

**거부 조건:** [`state.get('state')=='running'`](../../7%EC%B0%A8/prepare_dataset.py#L290)

**오류 메시지:** 수신 잠금은 풀렸지만 사전 수신 상태가 running입니다. 원인을 확인해야 합니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L334)

**오류 메시지:** 재시도 전 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`budget.used+remaining &gt; budget.limit`](../../7%EC%B0%A8/prepare_dataset.py#L338)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`path.is_absolute() or '..' in path.parts or ':' in info.filename or stat.S_ISLNK(info.external_attr &gt;&gt; 16)`](../../7%EC%B0%A8/prepare_dataset.py#L410)

**오류 메시지:** ZIP에 허용하지 않는 경로가 있습니다.

**거부 조건:** [`not target.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L419)

**오류 메시지:** ZIP 추출 경로가 원본 보관 폴더를 벗어납니다.

**거부 조건:** [`temporary.is_symlink() or not temporary.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L432)

**오류 메시지:** ZIP 임시 파일이 허용 경로를 벗어납니다.

**거부 조건:** [`temporary.stat().st_size != info.file_size`](../../7%EC%B0%A8/prepare_dataset.py#L436)

**오류 메시지:** ZIP 추출 크기가 다릅니다.

**거부 조건:** [`sha256_file(path)!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L572)

**오류 메시지:** 과거 추가 자료가 보존 manifest와 다릅니다.

**거부 조건:** [`not match`](../../7%EC%B0%A8/prepare_dataset.py#L705)

**오류 메시지:** 과거 pLitter 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/prepare_dataset.py#L283)

**오류 메시지:** 공식 자료 수신 잠금 대기 12시간을 초과했습니다.

**거부 조건:** [`not target.exists() or sha256_file(target)!=receipt['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L300)

**오류 메시지:** 사전 수신 SHA와 완성 원자료가 다릅니다.

**거부 조건:** [`existing.is_symlink() or getattr(existing,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L417)

**오류 메시지:** ZIP 추출 경로에 기존 파일 링크가 있습니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../7%EC%B0%A8/prepare_dataset.py#L349)

**오류 메시지:** 서버가 원본 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L378)

**오류 메시지:** 실패 수신 후 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`len(block)&gt;remaining`](../../7%EC%B0%A8/prepare_dataset.py#L368)

**오류 메시지:** 수신 본문이 요청한 원본 범위를 초과했습니다.


#### LEVEL 1 · [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`EVALUATOR`](../../7%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의='single-class confidence-greedy IoU; 101-point interpolated AP; v2'`


**거부 조건:** [`not results`](../../7%EC%B0%A8/train_pipeline.py#L69)

**오류 메시지:** 검증 후보가 없습니다.

**거부 조건:** [`not math.isfinite(elapsed) or elapsed&lt;0 or hours*3600-elapsed&lt;=0`](../../7%EC%B0%A8/train_pipeline.py#L84)

**오류 메시지:** 후보의 누적 학습 시간 예산이 끝났거나 잘못됐습니다.

**거부 조건:** [`width&lt;=0 or height&lt;=0 or grid not in (1,2,3)`](../../7%EC%B0%A8/train_pipeline.py#L94)

**오류 메시지:** 허용하지 않는 타일 크기입니다.

**거부 조건:** [`path.exists() and load(path)!=contract`](../../7%EC%B0%A8/train_pipeline.py#L118)

**오류 메시지:** checkpoint 원본·데이터·코드·학습 계약이 다릅니다.

**거부 조건:** [`not torch.cuda.is_available()`](../../7%EC%B0%A8/train_pipeline.py#L162)

**오류 메시지:** CUDA GPU가 없습니다. CPU로 장기 학습을 우회하지 않습니다.

**거부 조건:** [`any(list(model.names.values())!=['trash'] for model in models)`](../../7%EC%B0%A8/train_pipeline.py#L188)

**오류 메시지:** 단일 trash 클래스 모델이 아닙니다.

**거부 조건:** [`not best.exists()`](../../7%EC%B0%A8/train_pipeline.py#L310)

**오류 메시지:** 학습 완료 가중치가 없습니다.

**거부 조건:** [`type(resume) is not bool`](../../7%EC%B0%A8/train_pipeline.py#L327)

**오류 메시지:** 재개는 명시적 bool이어야 합니다.

**거부 조건:** [`not path.exists()`](../../7%EC%B0%A8/train_pipeline.py#L120)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not best.exists() or sha256_file(best)!=load(directory/'phase_complete.json')['best_sha256']`](../../7%EC%B0%A8/train_pipeline.py#L122)

**오류 메시지:** 완료 학습 가중치가 보존 해시와 다릅니다.

**거부 조건:** [`not path.exists() or not allow_resume`](../../7%EC%B0%A8/train_pipeline.py#L126)

**오류 메시지:** 중단 checkpoint는 동일 계약과 명시적 재개가 필요합니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/train_pipeline.py#L168)

**오류 메시지:** 다른 GPU 작업 때문에 필요한 여유 VRAM을 확보하지 못했습니다.

**거부 조건:** [`sha256_file(local(path))!=expected`](../../7%EC%B0%A8/train_pipeline.py#L320)

**오류 메시지:** 선택 가중치가 최종 평가 계약과 다릅니다.

**거부 조건:** [`int(checkpoint.get('epoch',-1))&lt;0`](../../7%EC%B0%A8/train_pipeline.py#L297)

**오류 메시지:** 완료 표식 없는 정리된 checkpoint입니다. 자동 재학습하지 않습니다.


#### LEVEL 1 · [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/verify_sources.py#L6)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`config['download_limit_bytes']!=100*1024**3 or config['minimum_disk_free_bytes']!=100*1024**3`](../../7%EC%B0%A8/verify_sources.py#L23)

**오류 메시지:** 신규 전송 예산·잔여 공간 계약이 다릅니다.

**거부 조건:** [`len(config['candidates'])!=2 or any(row['patience']!=12 for row in config['candidates'])`](../../7%EC%B0%A8/verify_sources.py#L25)

**오류 메시지:** 검토한 두 후보 명세가 다릅니다.


#### LEVEL 1 · [worker.py](../../7%EC%B0%A8/worker.py)


**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--action`](../../7%EC%B0%A8/worker.py#L210)<br>**코드의 선언:** `choices=['train', 'status']` |
| **설정·옵션:** [`--params`](../../7%EC%B0%A8/worker.py#L211)<br>**코드의 선언:** `default='{}'` |
| **설정·옵션:** [`--worker`](../../7%EC%B0%A8/worker.py#L212)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/worker.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`WORK`](../../7%EC%B0%A8/worker.py#L16)<br>**코드의 선언:** `정의=ROOT / 'work'` |
| **설정·옵션:** [`PROC`](../../7%EC%B0%A8/worker.py#L17)<br>**코드의 선언:** `정의=Path('/proc')` |
| **설정·옵션:** [`ACTIVE`](../../7%EC%B0%A8/worker.py#L18)<br>**코드의 선언:** `정의={'queued', 'running'}` |

**거부 조건:** [`not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value)`](../../7%EC%B0%A8/worker.py#L22)

**오류 메시지:** 허용되지 않는 작업 ID입니다.

**거부 조건:** [`not isinstance(value, dict)`](../../7%EC%B0%A8/worker.py#L130)

**오류 메시지:** 작업 기록이 없습니다.

**거부 조건:** [`not isinstance(params, dict) or set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../7%EC%B0%A8/worker.py#L158)

**오류 메시지:** 설정은 resume: true 또는 false만 허용하는 JSON 객체입니다.

**거부 조건:** [`any(value.get('state') in ACTIVE for value in jobs())`](../../7%EC%B0%A8/worker.py#L162)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`not value or value.get('state') != 'queued' or value.get('kind') != 'train'`](../../7%EC%B0%A8/worker.py#L186)

**오류 메시지:** 새로 대기 중인 학습 작업만 실행할 수 있습니다.

**거부 조건:** [`not isinstance(result, dict)`](../../7%EC%B0%A8/worker.py#L195)

**오류 메시지:** 학습 파이프라인이 결과 객체를 반환하지 않았습니다.

**거부 조건:** [`not blocking`](../../7%EC%B0%A8/worker.py#L62)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.


</details>

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

### LEVEL 1 · 결과와 주의할 범위

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


[자료 폴더](../../7%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-7.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-2"></a>
## LEVEL 2 - Explorer

### LEVEL 2 · 목적과 구성의 연결

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

### LEVEL 2 · 입력에서 출력으로

**단계:** 입력

**내용:** 쓰레기 영상·라벨·모델·선택한 차수 설정

**단계:** 처리

**내용:** 자료 준비·모델/영상 처리·평가 또는 상태 표시

**단계:** 출력

**내용:** 탐지 후보·평가 지표·화면·보고서


입력·처리·출력은 위의 같은 자료 흐름을 다른 단계에서 읽는 기준입니다. 처리 조건과 출력의 의미를 함께 확인합니다.

### LEVEL 2 · 설정과 처리 순서의 관계

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 2 · 이 차수 원래 안내의 세부 조건

#### LEVEL 2 · 실행 조건

현재 운영 환경은 Windows D:/2026/월요일 PBL/7차, Docker컨테이너2026과 /workspace/2026 마운트, /opt/venvs/torch/bin/python입니다. 기존 모델·자료·5차 결과가 필요하고 이 저장소에는 모델·데이터·EXE·로그·인증정보·개인 지침을 포함하지 않습니다. 복제만으로 전체 실험이 재현된다고 보장하지 않습니다.

학습실행.bat은자료 준비와학습을독립프로세스로시작하고학습상태.bat은실제생존상태를조회합니다. 같은준비/학습을중복실행하지않고실패원문을보존합니다. 명시적재개에는원본·코드·모델·설정계약일치가필요합니다. Codex/API토큰을요구하지않지만PC와Docker는실행돼있어야합니다.

신규전송상한100GiB,최소잔여100GiB를확인합니다. 사전수신과제품준비는동일Linux의공유flock을사용하며완료된공식원본크기·MD5·SHA를재확인하고전송원장을한번만합산합니다.

#### LEVEL 2 · 학습과 평가

COCO YOLO26l960/batch4/최대60epochs와기존작은물체l-P2 1280/batch2/최대45epochs의두후보를비교합니다. 후보별누적학습예산6시간과patience12,epoch callback상한을적용합니다. 시간확인은배치·검증경계에서이뤄지고최종검증·checkpoint저장시간은추가될수있습니다. 강제종료시마지막시간원장저장뒤의일부시간이보존되지않을수있어반복강제종료에도엄밀한실제누적시간보증이라고표현하지않습니다.

TACO validation에서모델·일반/분할추론·신뢰도를선택해고정한후테스트합니다. 기존TACO test150은이미사용한historical benchmark이고,PlastOPol은사진·근접중복통제평가이며촬영장소독립성은미확인입니다. UAVVaste는항공시점외부테스트로CCTV정확도와구분합니다. 없어진과거원본1232장은전체지각중복검증을하지못한한계가있습니다. 테스트성능으로다시튜닝하거나쉬운출처하나만90%라고전체달성을주장하지않습니다.

#### LEVEL 2 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)<br>**정의된 옵션 이름:** `--prepare`, `--smoke` |
| **진입 소스:** [worker.py](../../7%EC%B0%A8/worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 2 · [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)

| 내용 |
| --- |
| **정의:** [`_DownloadRetry`](../../7%EC%B0%A8/prepare_dataset.py#L234)<br>**소스에 적힌 역할:** 통신 경계에서 확인한 일시 오류만 재시도 경로로 전달합니다. |

**설정·옵션:** [`--prepare`](../../7%EC%B0%A8/prepare_dataset.py#L796)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--smoke`](../../7%EC%B0%A8/prepare_dataset.py#L797)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../7%EC%B0%A8/prepare_dataset.py#L25)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`WORK`](../../7%EC%B0%A8/prepare_dataset.py#L26)

**코드의 선언:** `정의=ROOT / 'work'`

**설정·옵션:** [`SOURCES`](../../7%EC%B0%A8/prepare_dataset.py#L27)

**코드의 선언:** `정의=WORK / 'sources'`

**설정·옵션:** [`TRAINING`](../../7%EC%B0%A8/prepare_dataset.py#L28)

**코드의 선언:** `정의=WORK / 'training'`

**설정·옵션:** [`ARCHIVE`](../../7%EC%B0%A8/prepare_dataset.py#L29)

**코드의 선언:** `정의=ROOT.parent / '이전 도커 실험/3차실험/trash_round3'`

**설정·옵션:** [`PREVIOUS`](../../7%EC%B0%A8/prepare_dataset.py#L30)

**코드의 선언:** `정의=ROOT.parent / '5차/work/training'`

**설정·옵션:** [`SEED`](../../7%EC%B0%A8/prepare_dataset.py#L31)

**코드의 선언:** `정의=20261030`

**설정·옵션:** [`MAX_BYTES`](../../7%EC%B0%A8/prepare_dataset.py#L32)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`MINIMUM_FREE`](../../7%EC%B0%A8/prepare_dataset.py#L33)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`NORMALIZATION`](../../7%EC%B0%A8/prepare_dataset.py#L34)

**코드의 선언:** `정의='rgb-jpeg-quality95-subsampling0-no-exif-no-rotation-v1'`


**거부 조건:** [`not all(math.isfinite(x) and x &gt; 0 for x in (width, height))`](../../7%EC%B0%A8/prepare_dataset.py#L116)

**오류 메시지:** COCO 이미지 크기가 잘못됐습니다.

**거부 조건:** [`source.resolve() == target.resolve()`](../../7%EC%B0%A8/prepare_dataset.py#L147)

**오류 메시지:** 원본을 정규화 결과로 덮어쓸 수 없습니다.

**거부 조건:** [`target.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L158)

**오류 메시지:** 출처 대응이 없는 기존 정규화 사본입니다.

**거부 조건:** [`not url.startswith('https://') and not url.startswith('http://127.0.0.1:')`](../../7%EC%B0%A8/prepare_dataset.py#L228)

**오류 메시지:** 공식 HTTPS 출처만 허용됩니다.

**거부 조건:** [`start &gt; spec['size']`](../../7%EC%B0%A8/prepare_dataset.py#L325)

**오류 메시지:** 부분 파일 크기가 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or digest_file(partial,'md5') != spec['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L394)

**오류 메시지:** 완성 원자료의 공식 MD5가 일치하지 않습니다.

**거부 조건:** [`destination.is_symlink() or getattr(destination,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L403)

**오류 메시지:** ZIP 추출 시작 위치가 파일 링크입니다.

**거부 조건:** [`parent['split'] != 'train'`](../../7%EC%B0%A8/prepare_dataset.py#L513)

**오류 메시지:** crop 증강은 train 부모에서만 생성합니다.

**거부 조건:** [`not (0 &lt;= left &lt; right &lt;= parent['width'] and 0 &lt;= top &lt; bottom &lt;= parent['height'])`](../../7%EC%B0%A8/prepare_dataset.py#L516)

**오류 메시지:** crop 영역이 부모 이미지 범위를 벗어났습니다.

**거부 조건:** [`path.exists() and path.read_text(encoding='utf-8')!=text`](../../7%EC%B0%A8/prepare_dataset.py#L548)

**오류 메시지:** 기존 학습 라벨이 새 변환과 다릅니다.

**거부 조건:** [`sha256_file(path)!=manifest['historical_protection_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L591)

**오류 메시지:** 과거 사용 자료 보호 명세가 바뀌었습니다.

**거부 조건:** [`os.name!='posix'`](../../7%EC%B0%A8/prepare_dataset.py#L660)

**오류 메시지:** 실제 자료 준비는 동일 Docker2026/Linux 안에서 실행해야 합니다.

**거부 조건:** [`groups['val']&lt;3 or groups['test']&lt;3`](../../7%EC%B0%A8/prepare_dataset.py#L743)

**오류 메시지:** PlastOPol 검증·테스트의 독립 이미지 그룹이 부족합니다.

**거부 조건:** [`before!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L780)

**오류 메시지:** smoke 원본이 보존 계약과 다릅니다.

**거부 조건:** [`sha256_file(raw)!=before`](../../7%EC%B0%A8/prepare_dataset.py#L786)

**오류 메시지:** smoke에서 원본이 변경됐습니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(map(math.isfinite, row))`](../../7%EC%B0%A8/prepare_dataset.py#L103)

**오류 메시지:** 단일 trash 클래스와 유한한 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x-width/2 and x+width/2 &lt;= 1+tolerance                                           and -tolerance &lt;= y-height/2 and y+height/2 &lt;= 1+tolerance)`](../../7%EC%B0%A8/prepare_dataset.py#L107)

**오류 메시지:** 라벨이 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(map(math.isfinite, (x,y,w,h))) or w &lt;= 0 or h &lt;= 0`](../../7%EC%B0%A8/prepare_dataset.py#L126)

**오류 메시지:** COCO 상자가 잘못됐습니다.

**거부 조건:** [`x &lt; -tolerance or y &lt; -tolerance or x+w &gt; width+tolerance or y+h &gt; height+tolerance`](../../7%EC%B0%A8/prepare_dataset.py#L129)

**오류 메시지:** COCO 상자가 이미지 범위를 벗어났습니다.

**거부 조건:** [`result['raw_sha256'] != raw_hash or result['normalization'] != NORMALIZATION or result['sha256'] != sha256_file(target)`](../../7%EC%B0%A8/prepare_dataset.py#L153)

**오류 메시지:** 정규화 사본의 보존 계약이 다릅니다.

**거부 조건:** [`(result['width'],result['height']) != tuple(expected_size)`](../../7%EC%B0%A8/prepare_dataset.py#L155)

**오류 메시지:** 정규화 사본과 주석 크기가 다릅니다.

**거부 조건:** [`original.size != tuple(expected_size) or original.width*original.height &gt; 100000000`](../../7%EC%B0%A8/prepare_dataset.py#L164)

**오류 메시지:** 해독한 원본 크기와 주석 좌표계가 다릅니다.

**거부 조건:** [`not encoded.endswith(b'\xff\xd9')`](../../7%EC%B0%A8/prepare_dataset.py#L173)

**오류 메시지:** 정규화 JPEG의 종료 표식이 없습니다.

**거부 조건:** [`self.used &lt; 0 or self.used &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L196)

**오류 메시지:** 기존 전송량이 7차 예산과 맞지 않습니다.

**거부 조건:** [`count &lt; 0 or free-count &lt; self.minimum_free`](../../7%EC%B0%A8/prepare_dataset.py#L201)

**오류 메시지:** 쓰기 후 잔여 공간 100GiB를 보장할 수 없습니다.

**거부 조건:** [`count &lt; 0 or self.used+count &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L205)

**오류 메시지:** 7차 누적 전송 예산을 초과했습니다.

**거부 조건:** [`value['bytes'] &lt; 0 or self.used+value['bytes'] &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L221)

**오류 메시지:** 사전 전송을 합치면 7차 전송 예산을 초과합니다.

**거부 조건:** [`not metadata.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L319)

**오류 메시지:** 출처 없는 부분 다운로드입니다.

**거부 조건:** [`old.get('url') != identity['url'] or old.get('size') != identity['size'] or old.get('md5',identity['md5']) != identity['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L322)

**오류 메시지:** 부분 다운로드의 원자료 계약이 다릅니다.

**거부 조건:** [`row.get('available') and sha256_file(local(row['raw_image']))!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L594)

**오류 메시지:** 추가로 대조한 과거 사용 원본이 바뀌었습니다.

**거부 조건:** [`manifest['contract']!=contract`](../../7%EC%B0%A8/prepare_dataset.py#L672)

**오류 메시지:** 준비된 데이터 계약이 다릅니다.

**거부 조건:** [`sha256_file(raw)!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L695)

**오류 메시지:** 보존 TACO 원본·라벨 계약과 다릅니다.

**거부 조건:** [`self.imports[identity] != value`](../../7%EC%B0%A8/prepare_dataset.py#L218)

**오류 메시지:** 이미 합산한 사전 전송 영수증이 변경됐습니다.

**거부 조건:** [`state.get('state')=='running'`](../../7%EC%B0%A8/prepare_dataset.py#L290)

**오류 메시지:** 수신 잠금은 풀렸지만 사전 수신 상태가 running입니다. 원인을 확인해야 합니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L334)

**오류 메시지:** 재시도 전 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`budget.used+remaining &gt; budget.limit`](../../7%EC%B0%A8/prepare_dataset.py#L338)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`path.is_absolute() or '..' in path.parts or ':' in info.filename or stat.S_ISLNK(info.external_attr &gt;&gt; 16)`](../../7%EC%B0%A8/prepare_dataset.py#L410)

**오류 메시지:** ZIP에 허용하지 않는 경로가 있습니다.

**거부 조건:** [`not target.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L419)

**오류 메시지:** ZIP 추출 경로가 원본 보관 폴더를 벗어납니다.

**거부 조건:** [`temporary.is_symlink() or not temporary.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L432)

**오류 메시지:** ZIP 임시 파일이 허용 경로를 벗어납니다.

**거부 조건:** [`temporary.stat().st_size != info.file_size`](../../7%EC%B0%A8/prepare_dataset.py#L436)

**오류 메시지:** ZIP 추출 크기가 다릅니다.

**거부 조건:** [`sha256_file(path)!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L572)

**오류 메시지:** 과거 추가 자료가 보존 manifest와 다릅니다.

**거부 조건:** [`not match`](../../7%EC%B0%A8/prepare_dataset.py#L705)

**오류 메시지:** 과거 pLitter 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/prepare_dataset.py#L283)

**오류 메시지:** 공식 자료 수신 잠금 대기 12시간을 초과했습니다.

**거부 조건:** [`not target.exists() or sha256_file(target)!=receipt['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L300)

**오류 메시지:** 사전 수신 SHA와 완성 원자료가 다릅니다.

**거부 조건:** [`existing.is_symlink() or getattr(existing,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L417)

**오류 메시지:** ZIP 추출 경로에 기존 파일 링크가 있습니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../7%EC%B0%A8/prepare_dataset.py#L349)

**오류 메시지:** 서버가 원본 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L378)

**오류 메시지:** 실패 수신 후 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`len(block)&gt;remaining`](../../7%EC%B0%A8/prepare_dataset.py#L368)

**오류 메시지:** 수신 본문이 요청한 원본 범위를 초과했습니다.


#### LEVEL 2 · [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`EVALUATOR`](../../7%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의='single-class confidence-greedy IoU; 101-point interpolated AP; v2'`


**거부 조건:** [`not results`](../../7%EC%B0%A8/train_pipeline.py#L69)

**오류 메시지:** 검증 후보가 없습니다.

**거부 조건:** [`not math.isfinite(elapsed) or elapsed&lt;0 or hours*3600-elapsed&lt;=0`](../../7%EC%B0%A8/train_pipeline.py#L84)

**오류 메시지:** 후보의 누적 학습 시간 예산이 끝났거나 잘못됐습니다.

**거부 조건:** [`width&lt;=0 or height&lt;=0 or grid not in (1,2,3)`](../../7%EC%B0%A8/train_pipeline.py#L94)

**오류 메시지:** 허용하지 않는 타일 크기입니다.

**거부 조건:** [`path.exists() and load(path)!=contract`](../../7%EC%B0%A8/train_pipeline.py#L118)

**오류 메시지:** checkpoint 원본·데이터·코드·학습 계약이 다릅니다.

**거부 조건:** [`not torch.cuda.is_available()`](../../7%EC%B0%A8/train_pipeline.py#L162)

**오류 메시지:** CUDA GPU가 없습니다. CPU로 장기 학습을 우회하지 않습니다.

**거부 조건:** [`any(list(model.names.values())!=['trash'] for model in models)`](../../7%EC%B0%A8/train_pipeline.py#L188)

**오류 메시지:** 단일 trash 클래스 모델이 아닙니다.

**거부 조건:** [`not best.exists()`](../../7%EC%B0%A8/train_pipeline.py#L310)

**오류 메시지:** 학습 완료 가중치가 없습니다.

**거부 조건:** [`type(resume) is not bool`](../../7%EC%B0%A8/train_pipeline.py#L327)

**오류 메시지:** 재개는 명시적 bool이어야 합니다.

**거부 조건:** [`not path.exists()`](../../7%EC%B0%A8/train_pipeline.py#L120)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not best.exists() or sha256_file(best)!=load(directory/'phase_complete.json')['best_sha256']`](../../7%EC%B0%A8/train_pipeline.py#L122)

**오류 메시지:** 완료 학습 가중치가 보존 해시와 다릅니다.

**거부 조건:** [`not path.exists() or not allow_resume`](../../7%EC%B0%A8/train_pipeline.py#L126)

**오류 메시지:** 중단 checkpoint는 동일 계약과 명시적 재개가 필요합니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/train_pipeline.py#L168)

**오류 메시지:** 다른 GPU 작업 때문에 필요한 여유 VRAM을 확보하지 못했습니다.

**거부 조건:** [`sha256_file(local(path))!=expected`](../../7%EC%B0%A8/train_pipeline.py#L320)

**오류 메시지:** 선택 가중치가 최종 평가 계약과 다릅니다.

**거부 조건:** [`int(checkpoint.get('epoch',-1))&lt;0`](../../7%EC%B0%A8/train_pipeline.py#L297)

**오류 메시지:** 완료 표식 없는 정리된 checkpoint입니다. 자동 재학습하지 않습니다.


#### LEVEL 2 · [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/verify_sources.py#L6)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`config['download_limit_bytes']!=100*1024**3 or config['minimum_disk_free_bytes']!=100*1024**3`](../../7%EC%B0%A8/verify_sources.py#L23)

**오류 메시지:** 신규 전송 예산·잔여 공간 계약이 다릅니다.

**거부 조건:** [`len(config['candidates'])!=2 or any(row['patience']!=12 for row in config['candidates'])`](../../7%EC%B0%A8/verify_sources.py#L25)

**오류 메시지:** 검토한 두 후보 명세가 다릅니다.


#### LEVEL 2 · [worker.py](../../7%EC%B0%A8/worker.py)


**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--action`](../../7%EC%B0%A8/worker.py#L210)<br>**코드의 선언:** `choices=['train', 'status']` |
| **설정·옵션:** [`--params`](../../7%EC%B0%A8/worker.py#L211)<br>**코드의 선언:** `default='{}'` |
| **설정·옵션:** [`--worker`](../../7%EC%B0%A8/worker.py#L212)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/worker.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`WORK`](../../7%EC%B0%A8/worker.py#L16)<br>**코드의 선언:** `정의=ROOT / 'work'` |
| **설정·옵션:** [`PROC`](../../7%EC%B0%A8/worker.py#L17)<br>**코드의 선언:** `정의=Path('/proc')` |
| **설정·옵션:** [`ACTIVE`](../../7%EC%B0%A8/worker.py#L18)<br>**코드의 선언:** `정의={'queued', 'running'}` |

**거부 조건:** [`not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value)`](../../7%EC%B0%A8/worker.py#L22)

**오류 메시지:** 허용되지 않는 작업 ID입니다.

**거부 조건:** [`not isinstance(value, dict)`](../../7%EC%B0%A8/worker.py#L130)

**오류 메시지:** 작업 기록이 없습니다.

**거부 조건:** [`not isinstance(params, dict) or set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../7%EC%B0%A8/worker.py#L158)

**오류 메시지:** 설정은 resume: true 또는 false만 허용하는 JSON 객체입니다.

**거부 조건:** [`any(value.get('state') in ACTIVE for value in jobs())`](../../7%EC%B0%A8/worker.py#L162)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`not value or value.get('state') != 'queued' or value.get('kind') != 'train'`](../../7%EC%B0%A8/worker.py#L186)

**오류 메시지:** 새로 대기 중인 학습 작업만 실행할 수 있습니다.

**거부 조건:** [`not isinstance(result, dict)`](../../7%EC%B0%A8/worker.py#L195)

**오류 메시지:** 학습 파이프라인이 결과 객체를 반환하지 않았습니다.

**거부 조건:** [`not blocking`](../../7%EC%B0%A8/worker.py#L62)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.


</details>

### LEVEL 2 · 관측과 해석을 구분하기

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


[자료 폴더](../../7%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-7.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-3"></a>
## LEVEL 3 - Practitioner

### LEVEL 3 · 이 차수를 준비하는 범위

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 3 · 이 차수 원래 안내의 세부 조건

#### LEVEL 3 · 실행 조건

현재 운영 환경은 Windows D:/2026/월요일 PBL/7차, Docker컨테이너2026과 /workspace/2026 마운트, /opt/venvs/torch/bin/python입니다. 기존 모델·자료·5차 결과가 필요하고 이 저장소에는 모델·데이터·EXE·로그·인증정보·개인 지침을 포함하지 않습니다. 복제만으로 전체 실험이 재현된다고 보장하지 않습니다.

학습실행.bat은자료 준비와학습을독립프로세스로시작하고학습상태.bat은실제생존상태를조회합니다. 같은준비/학습을중복실행하지않고실패원문을보존합니다. 명시적재개에는원본·코드·모델·설정계약일치가필요합니다. Codex/API토큰을요구하지않지만PC와Docker는실행돼있어야합니다.

신규전송상한100GiB,최소잔여100GiB를확인합니다. 사전수신과제품준비는동일Linux의공유flock을사용하며완료된공식원본크기·MD5·SHA를재확인하고전송원장을한번만합산합니다.

#### LEVEL 3 · 학습과 평가

COCO YOLO26l960/batch4/최대60epochs와기존작은물체l-P2 1280/batch2/최대45epochs의두후보를비교합니다. 후보별누적학습예산6시간과patience12,epoch callback상한을적용합니다. 시간확인은배치·검증경계에서이뤄지고최종검증·checkpoint저장시간은추가될수있습니다. 강제종료시마지막시간원장저장뒤의일부시간이보존되지않을수있어반복강제종료에도엄밀한실제누적시간보증이라고표현하지않습니다.

TACO validation에서모델·일반/분할추론·신뢰도를선택해고정한후테스트합니다. 기존TACO test150은이미사용한historical benchmark이고,PlastOPol은사진·근접중복통제평가이며촬영장소독립성은미확인입니다. UAVVaste는항공시점외부테스트로CCTV정확도와구분합니다. 없어진과거원본1232장은전체지각중복검증을하지못한한계가있습니다. 테스트성능으로다시튜닝하거나쉬운출처하나만90%라고전체달성을주장하지않습니다.

#### LEVEL 3 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)<br>**정의된 옵션 이름:** `--prepare`, `--smoke` |
| **진입 소스:** [worker.py](../../7%EC%B0%A8/worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 3 · [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)

| 내용 |
| --- |
| **정의:** [`_DownloadRetry`](../../7%EC%B0%A8/prepare_dataset.py#L234)<br>**소스에 적힌 역할:** 통신 경계에서 확인한 일시 오류만 재시도 경로로 전달합니다. |

**설정·옵션:** [`--prepare`](../../7%EC%B0%A8/prepare_dataset.py#L796)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--smoke`](../../7%EC%B0%A8/prepare_dataset.py#L797)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../7%EC%B0%A8/prepare_dataset.py#L25)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`WORK`](../../7%EC%B0%A8/prepare_dataset.py#L26)

**코드의 선언:** `정의=ROOT / 'work'`

**설정·옵션:** [`SOURCES`](../../7%EC%B0%A8/prepare_dataset.py#L27)

**코드의 선언:** `정의=WORK / 'sources'`

**설정·옵션:** [`TRAINING`](../../7%EC%B0%A8/prepare_dataset.py#L28)

**코드의 선언:** `정의=WORK / 'training'`

**설정·옵션:** [`ARCHIVE`](../../7%EC%B0%A8/prepare_dataset.py#L29)

**코드의 선언:** `정의=ROOT.parent / '이전 도커 실험/3차실험/trash_round3'`

**설정·옵션:** [`PREVIOUS`](../../7%EC%B0%A8/prepare_dataset.py#L30)

**코드의 선언:** `정의=ROOT.parent / '5차/work/training'`

**설정·옵션:** [`SEED`](../../7%EC%B0%A8/prepare_dataset.py#L31)

**코드의 선언:** `정의=20261030`

**설정·옵션:** [`MAX_BYTES`](../../7%EC%B0%A8/prepare_dataset.py#L32)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`MINIMUM_FREE`](../../7%EC%B0%A8/prepare_dataset.py#L33)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`NORMALIZATION`](../../7%EC%B0%A8/prepare_dataset.py#L34)

**코드의 선언:** `정의='rgb-jpeg-quality95-subsampling0-no-exif-no-rotation-v1'`


**거부 조건:** [`not all(math.isfinite(x) and x &gt; 0 for x in (width, height))`](../../7%EC%B0%A8/prepare_dataset.py#L116)

**오류 메시지:** COCO 이미지 크기가 잘못됐습니다.

**거부 조건:** [`source.resolve() == target.resolve()`](../../7%EC%B0%A8/prepare_dataset.py#L147)

**오류 메시지:** 원본을 정규화 결과로 덮어쓸 수 없습니다.

**거부 조건:** [`target.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L158)

**오류 메시지:** 출처 대응이 없는 기존 정규화 사본입니다.

**거부 조건:** [`not url.startswith('https://') and not url.startswith('http://127.0.0.1:')`](../../7%EC%B0%A8/prepare_dataset.py#L228)

**오류 메시지:** 공식 HTTPS 출처만 허용됩니다.

**거부 조건:** [`start &gt; spec['size']`](../../7%EC%B0%A8/prepare_dataset.py#L325)

**오류 메시지:** 부분 파일 크기가 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or digest_file(partial,'md5') != spec['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L394)

**오류 메시지:** 완성 원자료의 공식 MD5가 일치하지 않습니다.

**거부 조건:** [`destination.is_symlink() or getattr(destination,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L403)

**오류 메시지:** ZIP 추출 시작 위치가 파일 링크입니다.

**거부 조건:** [`parent['split'] != 'train'`](../../7%EC%B0%A8/prepare_dataset.py#L513)

**오류 메시지:** crop 증강은 train 부모에서만 생성합니다.

**거부 조건:** [`not (0 &lt;= left &lt; right &lt;= parent['width'] and 0 &lt;= top &lt; bottom &lt;= parent['height'])`](../../7%EC%B0%A8/prepare_dataset.py#L516)

**오류 메시지:** crop 영역이 부모 이미지 범위를 벗어났습니다.

**거부 조건:** [`path.exists() and path.read_text(encoding='utf-8')!=text`](../../7%EC%B0%A8/prepare_dataset.py#L548)

**오류 메시지:** 기존 학습 라벨이 새 변환과 다릅니다.

**거부 조건:** [`sha256_file(path)!=manifest['historical_protection_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L591)

**오류 메시지:** 과거 사용 자료 보호 명세가 바뀌었습니다.

**거부 조건:** [`os.name!='posix'`](../../7%EC%B0%A8/prepare_dataset.py#L660)

**오류 메시지:** 실제 자료 준비는 동일 Docker2026/Linux 안에서 실행해야 합니다.

**거부 조건:** [`groups['val']&lt;3 or groups['test']&lt;3`](../../7%EC%B0%A8/prepare_dataset.py#L743)

**오류 메시지:** PlastOPol 검증·테스트의 독립 이미지 그룹이 부족합니다.

**거부 조건:** [`before!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L780)

**오류 메시지:** smoke 원본이 보존 계약과 다릅니다.

**거부 조건:** [`sha256_file(raw)!=before`](../../7%EC%B0%A8/prepare_dataset.py#L786)

**오류 메시지:** smoke에서 원본이 변경됐습니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(map(math.isfinite, row))`](../../7%EC%B0%A8/prepare_dataset.py#L103)

**오류 메시지:** 단일 trash 클래스와 유한한 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x-width/2 and x+width/2 &lt;= 1+tolerance                                           and -tolerance &lt;= y-height/2 and y+height/2 &lt;= 1+tolerance)`](../../7%EC%B0%A8/prepare_dataset.py#L107)

**오류 메시지:** 라벨이 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(map(math.isfinite, (x,y,w,h))) or w &lt;= 0 or h &lt;= 0`](../../7%EC%B0%A8/prepare_dataset.py#L126)

**오류 메시지:** COCO 상자가 잘못됐습니다.

**거부 조건:** [`x &lt; -tolerance or y &lt; -tolerance or x+w &gt; width+tolerance or y+h &gt; height+tolerance`](../../7%EC%B0%A8/prepare_dataset.py#L129)

**오류 메시지:** COCO 상자가 이미지 범위를 벗어났습니다.

**거부 조건:** [`result['raw_sha256'] != raw_hash or result['normalization'] != NORMALIZATION or result['sha256'] != sha256_file(target)`](../../7%EC%B0%A8/prepare_dataset.py#L153)

**오류 메시지:** 정규화 사본의 보존 계약이 다릅니다.

**거부 조건:** [`(result['width'],result['height']) != tuple(expected_size)`](../../7%EC%B0%A8/prepare_dataset.py#L155)

**오류 메시지:** 정규화 사본과 주석 크기가 다릅니다.

**거부 조건:** [`original.size != tuple(expected_size) or original.width*original.height &gt; 100000000`](../../7%EC%B0%A8/prepare_dataset.py#L164)

**오류 메시지:** 해독한 원본 크기와 주석 좌표계가 다릅니다.

**거부 조건:** [`not encoded.endswith(b'\xff\xd9')`](../../7%EC%B0%A8/prepare_dataset.py#L173)

**오류 메시지:** 정규화 JPEG의 종료 표식이 없습니다.

**거부 조건:** [`self.used &lt; 0 or self.used &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L196)

**오류 메시지:** 기존 전송량이 7차 예산과 맞지 않습니다.

**거부 조건:** [`count &lt; 0 or free-count &lt; self.minimum_free`](../../7%EC%B0%A8/prepare_dataset.py#L201)

**오류 메시지:** 쓰기 후 잔여 공간 100GiB를 보장할 수 없습니다.

**거부 조건:** [`count &lt; 0 or self.used+count &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L205)

**오류 메시지:** 7차 누적 전송 예산을 초과했습니다.

**거부 조건:** [`value['bytes'] &lt; 0 or self.used+value['bytes'] &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L221)

**오류 메시지:** 사전 전송을 합치면 7차 전송 예산을 초과합니다.

**거부 조건:** [`not metadata.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L319)

**오류 메시지:** 출처 없는 부분 다운로드입니다.

**거부 조건:** [`old.get('url') != identity['url'] or old.get('size') != identity['size'] or old.get('md5',identity['md5']) != identity['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L322)

**오류 메시지:** 부분 다운로드의 원자료 계약이 다릅니다.

**거부 조건:** [`row.get('available') and sha256_file(local(row['raw_image']))!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L594)

**오류 메시지:** 추가로 대조한 과거 사용 원본이 바뀌었습니다.

**거부 조건:** [`manifest['contract']!=contract`](../../7%EC%B0%A8/prepare_dataset.py#L672)

**오류 메시지:** 준비된 데이터 계약이 다릅니다.

**거부 조건:** [`sha256_file(raw)!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L695)

**오류 메시지:** 보존 TACO 원본·라벨 계약과 다릅니다.

**거부 조건:** [`self.imports[identity] != value`](../../7%EC%B0%A8/prepare_dataset.py#L218)

**오류 메시지:** 이미 합산한 사전 전송 영수증이 변경됐습니다.

**거부 조건:** [`state.get('state')=='running'`](../../7%EC%B0%A8/prepare_dataset.py#L290)

**오류 메시지:** 수신 잠금은 풀렸지만 사전 수신 상태가 running입니다. 원인을 확인해야 합니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L334)

**오류 메시지:** 재시도 전 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`budget.used+remaining &gt; budget.limit`](../../7%EC%B0%A8/prepare_dataset.py#L338)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`path.is_absolute() or '..' in path.parts or ':' in info.filename or stat.S_ISLNK(info.external_attr &gt;&gt; 16)`](../../7%EC%B0%A8/prepare_dataset.py#L410)

**오류 메시지:** ZIP에 허용하지 않는 경로가 있습니다.

**거부 조건:** [`not target.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L419)

**오류 메시지:** ZIP 추출 경로가 원본 보관 폴더를 벗어납니다.

**거부 조건:** [`temporary.is_symlink() or not temporary.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L432)

**오류 메시지:** ZIP 임시 파일이 허용 경로를 벗어납니다.

**거부 조건:** [`temporary.stat().st_size != info.file_size`](../../7%EC%B0%A8/prepare_dataset.py#L436)

**오류 메시지:** ZIP 추출 크기가 다릅니다.

**거부 조건:** [`sha256_file(path)!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L572)

**오류 메시지:** 과거 추가 자료가 보존 manifest와 다릅니다.

**거부 조건:** [`not match`](../../7%EC%B0%A8/prepare_dataset.py#L705)

**오류 메시지:** 과거 pLitter 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/prepare_dataset.py#L283)

**오류 메시지:** 공식 자료 수신 잠금 대기 12시간을 초과했습니다.

**거부 조건:** [`not target.exists() or sha256_file(target)!=receipt['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L300)

**오류 메시지:** 사전 수신 SHA와 완성 원자료가 다릅니다.

**거부 조건:** [`existing.is_symlink() or getattr(existing,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L417)

**오류 메시지:** ZIP 추출 경로에 기존 파일 링크가 있습니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../7%EC%B0%A8/prepare_dataset.py#L349)

**오류 메시지:** 서버가 원본 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L378)

**오류 메시지:** 실패 수신 후 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`len(block)&gt;remaining`](../../7%EC%B0%A8/prepare_dataset.py#L368)

**오류 메시지:** 수신 본문이 요청한 원본 범위를 초과했습니다.


#### LEVEL 3 · [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`EVALUATOR`](../../7%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의='single-class confidence-greedy IoU; 101-point interpolated AP; v2'`


**거부 조건:** [`not results`](../../7%EC%B0%A8/train_pipeline.py#L69)

**오류 메시지:** 검증 후보가 없습니다.

**거부 조건:** [`not math.isfinite(elapsed) or elapsed&lt;0 or hours*3600-elapsed&lt;=0`](../../7%EC%B0%A8/train_pipeline.py#L84)

**오류 메시지:** 후보의 누적 학습 시간 예산이 끝났거나 잘못됐습니다.

**거부 조건:** [`width&lt;=0 or height&lt;=0 or grid not in (1,2,3)`](../../7%EC%B0%A8/train_pipeline.py#L94)

**오류 메시지:** 허용하지 않는 타일 크기입니다.

**거부 조건:** [`path.exists() and load(path)!=contract`](../../7%EC%B0%A8/train_pipeline.py#L118)

**오류 메시지:** checkpoint 원본·데이터·코드·학습 계약이 다릅니다.

**거부 조건:** [`not torch.cuda.is_available()`](../../7%EC%B0%A8/train_pipeline.py#L162)

**오류 메시지:** CUDA GPU가 없습니다. CPU로 장기 학습을 우회하지 않습니다.

**거부 조건:** [`any(list(model.names.values())!=['trash'] for model in models)`](../../7%EC%B0%A8/train_pipeline.py#L188)

**오류 메시지:** 단일 trash 클래스 모델이 아닙니다.

**거부 조건:** [`not best.exists()`](../../7%EC%B0%A8/train_pipeline.py#L310)

**오류 메시지:** 학습 완료 가중치가 없습니다.

**거부 조건:** [`type(resume) is not bool`](../../7%EC%B0%A8/train_pipeline.py#L327)

**오류 메시지:** 재개는 명시적 bool이어야 합니다.

**거부 조건:** [`not path.exists()`](../../7%EC%B0%A8/train_pipeline.py#L120)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not best.exists() or sha256_file(best)!=load(directory/'phase_complete.json')['best_sha256']`](../../7%EC%B0%A8/train_pipeline.py#L122)

**오류 메시지:** 완료 학습 가중치가 보존 해시와 다릅니다.

**거부 조건:** [`not path.exists() or not allow_resume`](../../7%EC%B0%A8/train_pipeline.py#L126)

**오류 메시지:** 중단 checkpoint는 동일 계약과 명시적 재개가 필요합니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/train_pipeline.py#L168)

**오류 메시지:** 다른 GPU 작업 때문에 필요한 여유 VRAM을 확보하지 못했습니다.

**거부 조건:** [`sha256_file(local(path))!=expected`](../../7%EC%B0%A8/train_pipeline.py#L320)

**오류 메시지:** 선택 가중치가 최종 평가 계약과 다릅니다.

**거부 조건:** [`int(checkpoint.get('epoch',-1))&lt;0`](../../7%EC%B0%A8/train_pipeline.py#L297)

**오류 메시지:** 완료 표식 없는 정리된 checkpoint입니다. 자동 재학습하지 않습니다.


#### LEVEL 3 · [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/verify_sources.py#L6)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`config['download_limit_bytes']!=100*1024**3 or config['minimum_disk_free_bytes']!=100*1024**3`](../../7%EC%B0%A8/verify_sources.py#L23)

**오류 메시지:** 신규 전송 예산·잔여 공간 계약이 다릅니다.

**거부 조건:** [`len(config['candidates'])!=2 or any(row['patience']!=12 for row in config['candidates'])`](../../7%EC%B0%A8/verify_sources.py#L25)

**오류 메시지:** 검토한 두 후보 명세가 다릅니다.


#### LEVEL 3 · [worker.py](../../7%EC%B0%A8/worker.py)


**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--action`](../../7%EC%B0%A8/worker.py#L210)<br>**코드의 선언:** `choices=['train', 'status']` |
| **설정·옵션:** [`--params`](../../7%EC%B0%A8/worker.py#L211)<br>**코드의 선언:** `default='{}'` |
| **설정·옵션:** [`--worker`](../../7%EC%B0%A8/worker.py#L212)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/worker.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`WORK`](../../7%EC%B0%A8/worker.py#L16)<br>**코드의 선언:** `정의=ROOT / 'work'` |
| **설정·옵션:** [`PROC`](../../7%EC%B0%A8/worker.py#L17)<br>**코드의 선언:** `정의=Path('/proc')` |
| **설정·옵션:** [`ACTIVE`](../../7%EC%B0%A8/worker.py#L18)<br>**코드의 선언:** `정의={'queued', 'running'}` |

**거부 조건:** [`not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value)`](../../7%EC%B0%A8/worker.py#L22)

**오류 메시지:** 허용되지 않는 작업 ID입니다.

**거부 조건:** [`not isinstance(value, dict)`](../../7%EC%B0%A8/worker.py#L130)

**오류 메시지:** 작업 기록이 없습니다.

**거부 조건:** [`not isinstance(params, dict) or set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../7%EC%B0%A8/worker.py#L158)

**오류 메시지:** 설정은 resume: true 또는 false만 허용하는 JSON 객체입니다.

**거부 조건:** [`any(value.get('state') in ACTIVE for value in jobs())`](../../7%EC%B0%A8/worker.py#L162)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`not value or value.get('state') != 'queued' or value.get('kind') != 'train'`](../../7%EC%B0%A8/worker.py#L186)

**오류 메시지:** 새로 대기 중인 학습 작업만 실행할 수 있습니다.

**거부 조건:** [`not isinstance(result, dict)`](../../7%EC%B0%A8/worker.py#L195)

**오류 메시지:** 학습 파이프라인이 결과 객체를 반환하지 않았습니다.

**거부 조건:** [`not blocking`](../../7%EC%B0%A8/worker.py#L62)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.


</details>

### LEVEL 3 · 실제 사용·실험 순서

1. 이 묶음이 학습·추론·화면·보고서 중 무엇을 제공하는지 아래 고유 내용을 확인합니다.
2. 실제 데이터·모델·동결 설정과 보존 소스의 대응을 확인합니다.
3. 해당 차수의 실행 안내에 따라 처리하거나 이미 생성된 결과를 읽습니다.
4. 결과의 자료 출처·분할·선택 정책·측정 범위를 함께 확인합니다.

**단계:** 입력

**내용:** 쓰레기 영상·라벨·모델·선택한 차수 설정

**단계:** 처리

**내용:** 자료 준비·모델/영상 처리·평가 또는 상태 표시

**단계:** 출력

**내용:** 탐지 후보·평가 지표·화면·보고서


### LEVEL 3 · 결과와 실패를 확인하기

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

**상황:** 학습 또는 화면이 시작되지 않음

**확인할 내용:** 해당 차수 환경·모델·데이터·설정 경로를 확인합니다. 화면 전용 차수는 학습 코드의 대체물이 아닙니다.

**상황:** 원본 계약 검사 실패

**확인할 내용:** 원래 코드·설정·자료 해시를 대조합니다. 현재 해시로 기준을 바꿔 우회하지 않습니다.

**상황:** 지표 해석이 어려움

**확인할 내용:** 검증으로 선택한 정책과 고정 테스트, 기존 시험과 새 출처 외부 시험을 구분합니다.


### LEVEL 3 · 실행 전 대조할 차수 조건

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

[자료 폴더](../../7%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-7.md) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-4"></a>
## LEVEL 4 - Advanced

### LEVEL 4 · 설계 의도와 검토 경계

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

### LEVEL 4 · 이 차수 구현의 실제 근거

| 내용 |
| --- |
| **파일:** [worker.py](../../7%EC%B0%A8/worker.py)<br>**원문에 정의된 역할·구성:** 준비와 GPU 학습을 Codex 없이 이어 실행하는 독립 작업자입니다. |
| **파일:** [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)<br>**원문에 정의된 역할·구성:** 공식 원자료를 보존하고 별도 정규화 사본·고정 분할을 준비합니다. |
| **파일:** [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)<br>**원문에 정의된 역할·구성:** 학습 시간을 제한하고 검증에서 모델·추론을 선택한 뒤 고정 테스트를 평가합니다. |
| **파일:** [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)<br>**원문에 정의된 역할·구성:** 소스 UTF-8·구문·실제 진입점·기존 모델 보존을 검사합니다. |
| **파일:** [tests/test_prepare_dataset.py](../../7%EC%B0%A8/tests/test_prepare_dataset.py)<br>**원문에 정의된 역할·구성:** 원본 보존·예산·분할 누출·좌표 변환의 실패 경로를 검사합니다. |
| **파일:** [tests/test_train_pipeline.py](../../7%EC%B0%A8/tests/test_train_pipeline.py)<br>**원문에 정의된 역할·구성:** 검증 선택·예측 좌표·재개 계약·고정 테스트의 경계를 검사합니다. |
| **파일:** [tests/test_worker.py](../../7%EC%B0%A8/tests/test_worker.py)<br>**원문에 정의된 역할·구성:** 독립 작업의 중복 배제·상태·명시 재개 계약을 검사합니다. |

**단계:** 입력

**내용:** 쓰레기 영상·라벨·모델·선택한 차수 설정

**단계:** 처리

**내용:** 자료 준비·모델/영상 처리·평가 또는 상태 표시

**단계:** 출력

**내용:** 탐지 후보·평가 지표·화면·보고서


### LEVEL 4 · 조건·변경·결과를 함께 검토하기

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

#### LEVEL 4 · 이 차수 원래 안내의 세부 조건

#### LEVEL 4 · 실행 조건

현재 운영 환경은 Windows D:/2026/월요일 PBL/7차, Docker컨테이너2026과 /workspace/2026 마운트, /opt/venvs/torch/bin/python입니다. 기존 모델·자료·5차 결과가 필요하고 이 저장소에는 모델·데이터·EXE·로그·인증정보·개인 지침을 포함하지 않습니다. 복제만으로 전체 실험이 재현된다고 보장하지 않습니다.

학습실행.bat은자료 준비와학습을독립프로세스로시작하고학습상태.bat은실제생존상태를조회합니다. 같은준비/학습을중복실행하지않고실패원문을보존합니다. 명시적재개에는원본·코드·모델·설정계약일치가필요합니다. Codex/API토큰을요구하지않지만PC와Docker는실행돼있어야합니다.

신규전송상한100GiB,최소잔여100GiB를확인합니다. 사전수신과제품준비는동일Linux의공유flock을사용하며완료된공식원본크기·MD5·SHA를재확인하고전송원장을한번만합산합니다.

#### LEVEL 4 · 학습과 평가

COCO YOLO26l960/batch4/최대60epochs와기존작은물체l-P2 1280/batch2/최대45epochs의두후보를비교합니다. 후보별누적학습예산6시간과patience12,epoch callback상한을적용합니다. 시간확인은배치·검증경계에서이뤄지고최종검증·checkpoint저장시간은추가될수있습니다. 강제종료시마지막시간원장저장뒤의일부시간이보존되지않을수있어반복강제종료에도엄밀한실제누적시간보증이라고표현하지않습니다.

TACO validation에서모델·일반/분할추론·신뢰도를선택해고정한후테스트합니다. 기존TACO test150은이미사용한historical benchmark이고,PlastOPol은사진·근접중복통제평가이며촬영장소독립성은미확인입니다. UAVVaste는항공시점외부테스트로CCTV정확도와구분합니다. 없어진과거원본1232장은전체지각중복검증을하지못한한계가있습니다. 테스트성능으로다시튜닝하거나쉬운출처하나만90%라고전체달성을주장하지않습니다.

#### LEVEL 4 · 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)<br>**정의된 옵션 이름:** `--prepare`, `--smoke` |
| **진입 소스:** [worker.py](../../7%EC%B0%A8/worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 4 · [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)

| 내용 |
| --- |
| **정의:** [`_DownloadRetry`](../../7%EC%B0%A8/prepare_dataset.py#L234)<br>**소스에 적힌 역할:** 통신 경계에서 확인한 일시 오류만 재시도 경로로 전달합니다. |

**설정·옵션:** [`--prepare`](../../7%EC%B0%A8/prepare_dataset.py#L796)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--smoke`](../../7%EC%B0%A8/prepare_dataset.py#L797)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../7%EC%B0%A8/prepare_dataset.py#L25)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`WORK`](../../7%EC%B0%A8/prepare_dataset.py#L26)

**코드의 선언:** `정의=ROOT / 'work'`

**설정·옵션:** [`SOURCES`](../../7%EC%B0%A8/prepare_dataset.py#L27)

**코드의 선언:** `정의=WORK / 'sources'`

**설정·옵션:** [`TRAINING`](../../7%EC%B0%A8/prepare_dataset.py#L28)

**코드의 선언:** `정의=WORK / 'training'`

**설정·옵션:** [`ARCHIVE`](../../7%EC%B0%A8/prepare_dataset.py#L29)

**코드의 선언:** `정의=ROOT.parent / '이전 도커 실험/3차실험/trash_round3'`

**설정·옵션:** [`PREVIOUS`](../../7%EC%B0%A8/prepare_dataset.py#L30)

**코드의 선언:** `정의=ROOT.parent / '5차/work/training'`

**설정·옵션:** [`SEED`](../../7%EC%B0%A8/prepare_dataset.py#L31)

**코드의 선언:** `정의=20261030`

**설정·옵션:** [`MAX_BYTES`](../../7%EC%B0%A8/prepare_dataset.py#L32)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`MINIMUM_FREE`](../../7%EC%B0%A8/prepare_dataset.py#L33)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`NORMALIZATION`](../../7%EC%B0%A8/prepare_dataset.py#L34)

**코드의 선언:** `정의='rgb-jpeg-quality95-subsampling0-no-exif-no-rotation-v1'`


**거부 조건:** [`not all(math.isfinite(x) and x &gt; 0 for x in (width, height))`](../../7%EC%B0%A8/prepare_dataset.py#L116)

**오류 메시지:** COCO 이미지 크기가 잘못됐습니다.

**거부 조건:** [`source.resolve() == target.resolve()`](../../7%EC%B0%A8/prepare_dataset.py#L147)

**오류 메시지:** 원본을 정규화 결과로 덮어쓸 수 없습니다.

**거부 조건:** [`target.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L158)

**오류 메시지:** 출처 대응이 없는 기존 정규화 사본입니다.

**거부 조건:** [`not url.startswith('https://') and not url.startswith('http://127.0.0.1:')`](../../7%EC%B0%A8/prepare_dataset.py#L228)

**오류 메시지:** 공식 HTTPS 출처만 허용됩니다.

**거부 조건:** [`start &gt; spec['size']`](../../7%EC%B0%A8/prepare_dataset.py#L325)

**오류 메시지:** 부분 파일 크기가 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or digest_file(partial,'md5') != spec['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L394)

**오류 메시지:** 완성 원자료의 공식 MD5가 일치하지 않습니다.

**거부 조건:** [`destination.is_symlink() or getattr(destination,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L403)

**오류 메시지:** ZIP 추출 시작 위치가 파일 링크입니다.

**거부 조건:** [`parent['split'] != 'train'`](../../7%EC%B0%A8/prepare_dataset.py#L513)

**오류 메시지:** crop 증강은 train 부모에서만 생성합니다.

**거부 조건:** [`not (0 &lt;= left &lt; right &lt;= parent['width'] and 0 &lt;= top &lt; bottom &lt;= parent['height'])`](../../7%EC%B0%A8/prepare_dataset.py#L516)

**오류 메시지:** crop 영역이 부모 이미지 범위를 벗어났습니다.

**거부 조건:** [`path.exists() and path.read_text(encoding='utf-8')!=text`](../../7%EC%B0%A8/prepare_dataset.py#L548)

**오류 메시지:** 기존 학습 라벨이 새 변환과 다릅니다.

**거부 조건:** [`sha256_file(path)!=manifest['historical_protection_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L591)

**오류 메시지:** 과거 사용 자료 보호 명세가 바뀌었습니다.

**거부 조건:** [`os.name!='posix'`](../../7%EC%B0%A8/prepare_dataset.py#L660)

**오류 메시지:** 실제 자료 준비는 동일 Docker2026/Linux 안에서 실행해야 합니다.

**거부 조건:** [`groups['val']&lt;3 or groups['test']&lt;3`](../../7%EC%B0%A8/prepare_dataset.py#L743)

**오류 메시지:** PlastOPol 검증·테스트의 독립 이미지 그룹이 부족합니다.

**거부 조건:** [`before!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L780)

**오류 메시지:** smoke 원본이 보존 계약과 다릅니다.

**거부 조건:** [`sha256_file(raw)!=before`](../../7%EC%B0%A8/prepare_dataset.py#L786)

**오류 메시지:** smoke에서 원본이 변경됐습니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(map(math.isfinite, row))`](../../7%EC%B0%A8/prepare_dataset.py#L103)

**오류 메시지:** 단일 trash 클래스와 유한한 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x-width/2 and x+width/2 &lt;= 1+tolerance                                           and -tolerance &lt;= y-height/2 and y+height/2 &lt;= 1+tolerance)`](../../7%EC%B0%A8/prepare_dataset.py#L107)

**오류 메시지:** 라벨이 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(map(math.isfinite, (x,y,w,h))) or w &lt;= 0 or h &lt;= 0`](../../7%EC%B0%A8/prepare_dataset.py#L126)

**오류 메시지:** COCO 상자가 잘못됐습니다.

**거부 조건:** [`x &lt; -tolerance or y &lt; -tolerance or x+w &gt; width+tolerance or y+h &gt; height+tolerance`](../../7%EC%B0%A8/prepare_dataset.py#L129)

**오류 메시지:** COCO 상자가 이미지 범위를 벗어났습니다.

**거부 조건:** [`result['raw_sha256'] != raw_hash or result['normalization'] != NORMALIZATION or result['sha256'] != sha256_file(target)`](../../7%EC%B0%A8/prepare_dataset.py#L153)

**오류 메시지:** 정규화 사본의 보존 계약이 다릅니다.

**거부 조건:** [`(result['width'],result['height']) != tuple(expected_size)`](../../7%EC%B0%A8/prepare_dataset.py#L155)

**오류 메시지:** 정규화 사본과 주석 크기가 다릅니다.

**거부 조건:** [`original.size != tuple(expected_size) or original.width*original.height &gt; 100000000`](../../7%EC%B0%A8/prepare_dataset.py#L164)

**오류 메시지:** 해독한 원본 크기와 주석 좌표계가 다릅니다.

**거부 조건:** [`not encoded.endswith(b'\xff\xd9')`](../../7%EC%B0%A8/prepare_dataset.py#L173)

**오류 메시지:** 정규화 JPEG의 종료 표식이 없습니다.

**거부 조건:** [`self.used &lt; 0 or self.used &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L196)

**오류 메시지:** 기존 전송량이 7차 예산과 맞지 않습니다.

**거부 조건:** [`count &lt; 0 or free-count &lt; self.minimum_free`](../../7%EC%B0%A8/prepare_dataset.py#L201)

**오류 메시지:** 쓰기 후 잔여 공간 100GiB를 보장할 수 없습니다.

**거부 조건:** [`count &lt; 0 or self.used+count &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L205)

**오류 메시지:** 7차 누적 전송 예산을 초과했습니다.

**거부 조건:** [`value['bytes'] &lt; 0 or self.used+value['bytes'] &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L221)

**오류 메시지:** 사전 전송을 합치면 7차 전송 예산을 초과합니다.

**거부 조건:** [`not metadata.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L319)

**오류 메시지:** 출처 없는 부분 다운로드입니다.

**거부 조건:** [`old.get('url') != identity['url'] or old.get('size') != identity['size'] or old.get('md5',identity['md5']) != identity['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L322)

**오류 메시지:** 부분 다운로드의 원자료 계약이 다릅니다.

**거부 조건:** [`row.get('available') and sha256_file(local(row['raw_image']))!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L594)

**오류 메시지:** 추가로 대조한 과거 사용 원본이 바뀌었습니다.

**거부 조건:** [`manifest['contract']!=contract`](../../7%EC%B0%A8/prepare_dataset.py#L672)

**오류 메시지:** 준비된 데이터 계약이 다릅니다.

**거부 조건:** [`sha256_file(raw)!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L695)

**오류 메시지:** 보존 TACO 원본·라벨 계약과 다릅니다.

**거부 조건:** [`self.imports[identity] != value`](../../7%EC%B0%A8/prepare_dataset.py#L218)

**오류 메시지:** 이미 합산한 사전 전송 영수증이 변경됐습니다.

**거부 조건:** [`state.get('state')=='running'`](../../7%EC%B0%A8/prepare_dataset.py#L290)

**오류 메시지:** 수신 잠금은 풀렸지만 사전 수신 상태가 running입니다. 원인을 확인해야 합니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L334)

**오류 메시지:** 재시도 전 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`budget.used+remaining &gt; budget.limit`](../../7%EC%B0%A8/prepare_dataset.py#L338)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`path.is_absolute() or '..' in path.parts or ':' in info.filename or stat.S_ISLNK(info.external_attr &gt;&gt; 16)`](../../7%EC%B0%A8/prepare_dataset.py#L410)

**오류 메시지:** ZIP에 허용하지 않는 경로가 있습니다.

**거부 조건:** [`not target.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L419)

**오류 메시지:** ZIP 추출 경로가 원본 보관 폴더를 벗어납니다.

**거부 조건:** [`temporary.is_symlink() or not temporary.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L432)

**오류 메시지:** ZIP 임시 파일이 허용 경로를 벗어납니다.

**거부 조건:** [`temporary.stat().st_size != info.file_size`](../../7%EC%B0%A8/prepare_dataset.py#L436)

**오류 메시지:** ZIP 추출 크기가 다릅니다.

**거부 조건:** [`sha256_file(path)!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L572)

**오류 메시지:** 과거 추가 자료가 보존 manifest와 다릅니다.

**거부 조건:** [`not match`](../../7%EC%B0%A8/prepare_dataset.py#L705)

**오류 메시지:** 과거 pLitter 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/prepare_dataset.py#L283)

**오류 메시지:** 공식 자료 수신 잠금 대기 12시간을 초과했습니다.

**거부 조건:** [`not target.exists() or sha256_file(target)!=receipt['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L300)

**오류 메시지:** 사전 수신 SHA와 완성 원자료가 다릅니다.

**거부 조건:** [`existing.is_symlink() or getattr(existing,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L417)

**오류 메시지:** ZIP 추출 경로에 기존 파일 링크가 있습니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../7%EC%B0%A8/prepare_dataset.py#L349)

**오류 메시지:** 서버가 원본 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L378)

**오류 메시지:** 실패 수신 후 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`len(block)&gt;remaining`](../../7%EC%B0%A8/prepare_dataset.py#L368)

**오류 메시지:** 수신 본문이 요청한 원본 범위를 초과했습니다.


#### LEVEL 4 · [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`EVALUATOR`](../../7%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의='single-class confidence-greedy IoU; 101-point interpolated AP; v2'`


**거부 조건:** [`not results`](../../7%EC%B0%A8/train_pipeline.py#L69)

**오류 메시지:** 검증 후보가 없습니다.

**거부 조건:** [`not math.isfinite(elapsed) or elapsed&lt;0 or hours*3600-elapsed&lt;=0`](../../7%EC%B0%A8/train_pipeline.py#L84)

**오류 메시지:** 후보의 누적 학습 시간 예산이 끝났거나 잘못됐습니다.

**거부 조건:** [`width&lt;=0 or height&lt;=0 or grid not in (1,2,3)`](../../7%EC%B0%A8/train_pipeline.py#L94)

**오류 메시지:** 허용하지 않는 타일 크기입니다.

**거부 조건:** [`path.exists() and load(path)!=contract`](../../7%EC%B0%A8/train_pipeline.py#L118)

**오류 메시지:** checkpoint 원본·데이터·코드·학습 계약이 다릅니다.

**거부 조건:** [`not torch.cuda.is_available()`](../../7%EC%B0%A8/train_pipeline.py#L162)

**오류 메시지:** CUDA GPU가 없습니다. CPU로 장기 학습을 우회하지 않습니다.

**거부 조건:** [`any(list(model.names.values())!=['trash'] for model in models)`](../../7%EC%B0%A8/train_pipeline.py#L188)

**오류 메시지:** 단일 trash 클래스 모델이 아닙니다.

**거부 조건:** [`not best.exists()`](../../7%EC%B0%A8/train_pipeline.py#L310)

**오류 메시지:** 학습 완료 가중치가 없습니다.

**거부 조건:** [`type(resume) is not bool`](../../7%EC%B0%A8/train_pipeline.py#L327)

**오류 메시지:** 재개는 명시적 bool이어야 합니다.

**거부 조건:** [`not path.exists()`](../../7%EC%B0%A8/train_pipeline.py#L120)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not best.exists() or sha256_file(best)!=load(directory/'phase_complete.json')['best_sha256']`](../../7%EC%B0%A8/train_pipeline.py#L122)

**오류 메시지:** 완료 학습 가중치가 보존 해시와 다릅니다.

**거부 조건:** [`not path.exists() or not allow_resume`](../../7%EC%B0%A8/train_pipeline.py#L126)

**오류 메시지:** 중단 checkpoint는 동일 계약과 명시적 재개가 필요합니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/train_pipeline.py#L168)

**오류 메시지:** 다른 GPU 작업 때문에 필요한 여유 VRAM을 확보하지 못했습니다.

**거부 조건:** [`sha256_file(local(path))!=expected`](../../7%EC%B0%A8/train_pipeline.py#L320)

**오류 메시지:** 선택 가중치가 최종 평가 계약과 다릅니다.

**거부 조건:** [`int(checkpoint.get('epoch',-1))&lt;0`](../../7%EC%B0%A8/train_pipeline.py#L297)

**오류 메시지:** 완료 표식 없는 정리된 checkpoint입니다. 자동 재학습하지 않습니다.


#### LEVEL 4 · [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/verify_sources.py#L6)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`config['download_limit_bytes']!=100*1024**3 or config['minimum_disk_free_bytes']!=100*1024**3`](../../7%EC%B0%A8/verify_sources.py#L23)

**오류 메시지:** 신규 전송 예산·잔여 공간 계약이 다릅니다.

**거부 조건:** [`len(config['candidates'])!=2 or any(row['patience']!=12 for row in config['candidates'])`](../../7%EC%B0%A8/verify_sources.py#L25)

**오류 메시지:** 검토한 두 후보 명세가 다릅니다.


#### LEVEL 4 · [worker.py](../../7%EC%B0%A8/worker.py)


**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--action`](../../7%EC%B0%A8/worker.py#L210)<br>**코드의 선언:** `choices=['train', 'status']` |
| **설정·옵션:** [`--params`](../../7%EC%B0%A8/worker.py#L211)<br>**코드의 선언:** `default='{}'` |
| **설정·옵션:** [`--worker`](../../7%EC%B0%A8/worker.py#L212)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/worker.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`WORK`](../../7%EC%B0%A8/worker.py#L16)<br>**코드의 선언:** `정의=ROOT / 'work'` |
| **설정·옵션:** [`PROC`](../../7%EC%B0%A8/worker.py#L17)<br>**코드의 선언:** `정의=Path('/proc')` |
| **설정·옵션:** [`ACTIVE`](../../7%EC%B0%A8/worker.py#L18)<br>**코드의 선언:** `정의={'queued', 'running'}` |

**거부 조건:** [`not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value)`](../../7%EC%B0%A8/worker.py#L22)

**오류 메시지:** 허용되지 않는 작업 ID입니다.

**거부 조건:** [`not isinstance(value, dict)`](../../7%EC%B0%A8/worker.py#L130)

**오류 메시지:** 작업 기록이 없습니다.

**거부 조건:** [`not isinstance(params, dict) or set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../7%EC%B0%A8/worker.py#L158)

**오류 메시지:** 설정은 resume: true 또는 false만 허용하는 JSON 객체입니다.

**거부 조건:** [`any(value.get('state') in ACTIVE for value in jobs())`](../../7%EC%B0%A8/worker.py#L162)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`not value or value.get('state') != 'queued' or value.get('kind') != 'train'`](../../7%EC%B0%A8/worker.py#L186)

**오류 메시지:** 새로 대기 중인 학습 작업만 실행할 수 있습니다.

**거부 조건:** [`not isinstance(result, dict)`](../../7%EC%B0%A8/worker.py#L195)

**오류 메시지:** 학습 파이프라인이 결과 객체를 반환하지 않았습니다.

**거부 조건:** [`not blocking`](../../7%EC%B0%A8/worker.py#L62)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.


</details>

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

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

[자료 폴더](../../7%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-7.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<a id="reading-level-5"></a>
## LEVEL 5 - Expert

기존의 전체 설명·표·코드·함수 참조·파일별 비교는 아래에 그대로 이어집니다. [자료 폴더](../../7%EC%B0%A8) · [직전 비교·자료 범위](../comparisons/5-to-7.md) · [이 차수의 원래 전체 상세](#reading-level-5)
<!-- reading-levels:end -->



[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../7%EC%B0%A8) · [← 이전: 5차](round-5.md) · [다음: 8차 →](round-8.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

**항목:** 1

**이 차수에서 확인할 내용:** 대규모 자료 준비, 학습·평가 및 작업 실행 코드를 포함합니다. 90%는 정밀도와 재현율 각각의 목표이며 달성 여부는 학습과 평가의 실제 결과로 확인해야 합니다. 기존 테스트와 새 외부 테스트를 구분합니다. 비교는 표시된 기준 커밋에 한정됩니다.


<a name="-입력처리출력"></a>
## 입력·처리·출력

**단계:** 입력

**내용:** 쓰레기 영상·라벨·모델·선택한 차수 설정

**단계:** 처리

**내용:** 자료 준비·모델/영상 처리·평가 또는 상태 표시

**단계:** 출력

**내용:** 탐지 후보·평가 지표·화면·보고서


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
| **경로:** [configs/](../../7%EC%B0%A8/configs)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [docs/](../../7%EC%B0%A8/docs)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [tests/](../../7%EC%B0%A8/tests)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [README.md](../../7%EC%B0%A8/README.md)<br>**자료 종류:** MD 파일 |
| **경로:** [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)<br>**자료 종류:** PY 파일 |
| **경로:** [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)<br>**자료 종류:** PY 파일 |
| **경로:** [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)<br>**자료 종류:** PY 파일 |
| **경로:** [worker.py](../../7%EC%B0%A8/worker.py)<br>**자료 종류:** PY 파일 |
| **경로:** [사용안내.txt](../../7%EC%B0%A8/%EC%82%AC%EC%9A%A9%EC%95%88%EB%82%B4.txt)<br>**자료 종류:** TXT 파일 |
| **경로:** [학습상태.bat](../../7%EC%B0%A8/%ED%95%99%EC%8A%B5%EC%83%81%ED%83%9C.bat)<br>**자료 종류:** BAT 파일 |
| **경로:** [학습실행.bat](../../7%EC%B0%A8/%ED%95%99%EC%8A%B5%EC%8B%A4%ED%96%89.bat)<br>**자료 종류:** BAT 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 내용 |
| --- |
| **파일:** [worker.py](../../7%EC%B0%A8/worker.py)<br>**원문에 정의된 역할·구성:** 준비와 GPU 학습을 Codex 없이 이어 실행하는 독립 작업자입니다. |
| **파일:** [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)<br>**원문에 정의된 역할·구성:** 공식 원자료를 보존하고 별도 정규화 사본·고정 분할을 준비합니다. |
| **파일:** [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)<br>**원문에 정의된 역할·구성:** 학습 시간을 제한하고 검증에서 모델·추론을 선택한 뒤 고정 테스트를 평가합니다. |
| **파일:** [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)<br>**원문에 정의된 역할·구성:** 소스 UTF-8·구문·실제 진입점·기존 모델 보존을 검사합니다. |
| **파일:** [tests/test_prepare_dataset.py](../../7%EC%B0%A8/tests/test_prepare_dataset.py)<br>**원문에 정의된 역할·구성:** 원본 보존·예산·분할 누출·좌표 변환의 실패 경로를 검사합니다. |
| **파일:** [tests/test_train_pipeline.py](../../7%EC%B0%A8/tests/test_train_pipeline.py)<br>**원문에 정의된 역할·구성:** 검증 선택·예측 좌표·재개 계약·고정 테스트의 경계를 검사합니다. |
| **파일:** [tests/test_worker.py](../../7%EC%B0%A8/tests/test_worker.py)<br>**원문에 정의된 역할·구성:** 독립 작업의 중복 배제·상태·명시 재개 계약을 검사합니다. |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

선택한 차수의 노트북·requirements·Docker 및 설정을 확인합니다. 데이터셋·학습 가중치·실행 환경은 공개 코드와 별도일 수 있습니다. 이전 차수의 모델을 요구하는 경로는 해당 모델과 계약이 함께 필요합니다.

단일 노트북은 Jupyter에서 설정·데이터·모델 경로를 확인하고 셀 순서를 따릅니다. 모듈화된 차수는 해당 폴더 README의 실행 진입점과 동결 조건을 따릅니다. 보고서·운영 기록만 있는 묶음은 읽기 자료로 사용합니다.

<a name="-이-차수-원래-안내의-세부-조건"></a>
### 이 차수 원래 안내의 세부 조건

### 실행 조건

현재 운영 환경은 Windows D:/2026/월요일 PBL/7차, Docker컨테이너2026과 /workspace/2026 마운트, /opt/venvs/torch/bin/python입니다. 기존 모델·자료·5차 결과가 필요하고 이 저장소에는 모델·데이터·EXE·로그·인증정보·개인 지침을 포함하지 않습니다. 복제만으로 전체 실험이 재현된다고 보장하지 않습니다.

학습실행.bat은자료 준비와학습을독립프로세스로시작하고학습상태.bat은실제생존상태를조회합니다. 같은준비/학습을중복실행하지않고실패원문을보존합니다. 명시적재개에는원본·코드·모델·설정계약일치가필요합니다. Codex/API토큰을요구하지않지만PC와Docker는실행돼있어야합니다.

신규전송상한100GiB,최소잔여100GiB를확인합니다. 사전수신과제품준비는동일Linux의공유flock을사용하며완료된공식원본크기·MD5·SHA를재확인하고전송원장을한번만합산합니다.

### 학습과 평가

COCO YOLO26l960/batch4/최대60epochs와기존작은물체l-P2 1280/batch2/최대45epochs의두후보를비교합니다. 후보별누적학습예산6시간과patience12,epoch callback상한을적용합니다. 시간확인은배치·검증경계에서이뤄지고최종검증·checkpoint저장시간은추가될수있습니다. 강제종료시마지막시간원장저장뒤의일부시간이보존되지않을수있어반복강제종료에도엄밀한실제누적시간보증이라고표현하지않습니다.

TACO validation에서모델·일반/분할추론·신뢰도를선택해고정한후테스트합니다. 기존TACO test150은이미사용한historical benchmark이고,PlastOPol은사진·근접중복통제평가이며촬영장소독립성은미확인입니다. UAVVaste는항공시점외부테스트로CCTV정확도와구분합니다. 없어진과거원본1232장은전체지각중복검증을하지못한한계가있습니다. 테스트성능으로다시튜닝하거나쉬운출처하나만90%라고전체달성을주장하지않습니다.

<a name="️-소스에서-제공하는-cli-옵션"></a>
### 소스에서 제공하는 CLI 옵션

| 내용 |
| --- |
| **진입 소스:** [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)<br>**정의된 옵션 이름:** `--prepare`, `--smoke` |
| **진입 소스:** [worker.py](../../7%EC%B0%A8/worker.py)<br>**정의된 옵션 이름:** `--action`, `--params`, `--worker` |

각 옵션의 기본값·필수값·부작용은 해당 main과 인자 정의를 함께 확인합니다.


<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [prepare_dataset.py](../../7%EC%B0%A8/prepare_dataset.py)

| 내용 |
| --- |
| **정의:** [`_DownloadRetry`](../../7%EC%B0%A8/prepare_dataset.py#L234)<br>**소스에 적힌 역할:** 통신 경계에서 확인한 일시 오류만 재시도 경로로 전달합니다. |

**설정·옵션:** [`--prepare`](../../7%EC%B0%A8/prepare_dataset.py#L796)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`--smoke`](../../7%EC%B0%A8/prepare_dataset.py#L797)

**코드의 선언:** `action='store_true'`

**설정·옵션:** [`ROOT`](../../7%EC%B0%A8/prepare_dataset.py#L25)

**코드의 선언:** `정의=Path(__file__).resolve().parent`

**설정·옵션:** [`WORK`](../../7%EC%B0%A8/prepare_dataset.py#L26)

**코드의 선언:** `정의=ROOT / 'work'`

**설정·옵션:** [`SOURCES`](../../7%EC%B0%A8/prepare_dataset.py#L27)

**코드의 선언:** `정의=WORK / 'sources'`

**설정·옵션:** [`TRAINING`](../../7%EC%B0%A8/prepare_dataset.py#L28)

**코드의 선언:** `정의=WORK / 'training'`

**설정·옵션:** [`ARCHIVE`](../../7%EC%B0%A8/prepare_dataset.py#L29)

**코드의 선언:** `정의=ROOT.parent / '이전 도커 실험/3차실험/trash_round3'`

**설정·옵션:** [`PREVIOUS`](../../7%EC%B0%A8/prepare_dataset.py#L30)

**코드의 선언:** `정의=ROOT.parent / '5차/work/training'`

**설정·옵션:** [`SEED`](../../7%EC%B0%A8/prepare_dataset.py#L31)

**코드의 선언:** `정의=20261030`

**설정·옵션:** [`MAX_BYTES`](../../7%EC%B0%A8/prepare_dataset.py#L32)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`MINIMUM_FREE`](../../7%EC%B0%A8/prepare_dataset.py#L33)

**코드의 선언:** `정의=100 * 1024**3`

**설정·옵션:** [`NORMALIZATION`](../../7%EC%B0%A8/prepare_dataset.py#L34)

**코드의 선언:** `정의='rgb-jpeg-quality95-subsampling0-no-exif-no-rotation-v1'`


**거부 조건:** [`not all(math.isfinite(x) and x &gt; 0 for x in (width, height))`](../../7%EC%B0%A8/prepare_dataset.py#L116)

**오류 메시지:** COCO 이미지 크기가 잘못됐습니다.

**거부 조건:** [`source.resolve() == target.resolve()`](../../7%EC%B0%A8/prepare_dataset.py#L147)

**오류 메시지:** 원본을 정규화 결과로 덮어쓸 수 없습니다.

**거부 조건:** [`target.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L158)

**오류 메시지:** 출처 대응이 없는 기존 정규화 사본입니다.

**거부 조건:** [`not url.startswith('https://') and not url.startswith('http://127.0.0.1:')`](../../7%EC%B0%A8/prepare_dataset.py#L228)

**오류 메시지:** 공식 HTTPS 출처만 허용됩니다.

**거부 조건:** [`start &gt; spec['size']`](../../7%EC%B0%A8/prepare_dataset.py#L325)

**오류 메시지:** 부분 파일 크기가 원본보다 큽니다.

**거부 조건:** [`partial.stat().st_size != spec['size'] or digest_file(partial,'md5') != spec['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L394)

**오류 메시지:** 완성 원자료의 공식 MD5가 일치하지 않습니다.

**거부 조건:** [`destination.is_symlink() or getattr(destination,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L403)

**오류 메시지:** ZIP 추출 시작 위치가 파일 링크입니다.

**거부 조건:** [`parent['split'] != 'train'`](../../7%EC%B0%A8/prepare_dataset.py#L513)

**오류 메시지:** crop 증강은 train 부모에서만 생성합니다.

**거부 조건:** [`not (0 &lt;= left &lt; right &lt;= parent['width'] and 0 &lt;= top &lt; bottom &lt;= parent['height'])`](../../7%EC%B0%A8/prepare_dataset.py#L516)

**오류 메시지:** crop 영역이 부모 이미지 범위를 벗어났습니다.

**거부 조건:** [`path.exists() and path.read_text(encoding='utf-8')!=text`](../../7%EC%B0%A8/prepare_dataset.py#L548)

**오류 메시지:** 기존 학습 라벨이 새 변환과 다릅니다.

**거부 조건:** [`sha256_file(path)!=manifest['historical_protection_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L591)

**오류 메시지:** 과거 사용 자료 보호 명세가 바뀌었습니다.

**거부 조건:** [`os.name!='posix'`](../../7%EC%B0%A8/prepare_dataset.py#L660)

**오류 메시지:** 실제 자료 준비는 동일 Docker2026/Linux 안에서 실행해야 합니다.

**거부 조건:** [`groups['val']&lt;3 or groups['test']&lt;3`](../../7%EC%B0%A8/prepare_dataset.py#L743)

**오류 메시지:** PlastOPol 검증·테스트의 독립 이미지 그룹이 부족합니다.

**거부 조건:** [`before!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L780)

**오류 메시지:** smoke 원본이 보존 계약과 다릅니다.

**거부 조건:** [`sha256_file(raw)!=before`](../../7%EC%B0%A8/prepare_dataset.py#L786)

**오류 메시지:** smoke에서 원본이 변경됐습니다.

**거부 조건:** [`len(row) != 5 or row[0] != 0 or not all(map(math.isfinite, row))`](../../7%EC%B0%A8/prepare_dataset.py#L103)

**오류 메시지:** 단일 trash 클래스와 유한한 좌표가 필요합니다.

**거부 조건:** [`width &lt;= 0 or height &lt;= 0 or not (-tolerance &lt;= x-width/2 and x+width/2 &lt;= 1+tolerance                                           and -tolerance &lt;= y-height/2 and y+height/2 &lt;= 1+tolerance)`](../../7%EC%B0%A8/prepare_dataset.py#L107)

**오류 메시지:** 라벨이 이미지 경계를 벗어났습니다.

**거부 조건:** [`not all(map(math.isfinite, (x,y,w,h))) or w &lt;= 0 or h &lt;= 0`](../../7%EC%B0%A8/prepare_dataset.py#L126)

**오류 메시지:** COCO 상자가 잘못됐습니다.

**거부 조건:** [`x &lt; -tolerance or y &lt; -tolerance or x+w &gt; width+tolerance or y+h &gt; height+tolerance`](../../7%EC%B0%A8/prepare_dataset.py#L129)

**오류 메시지:** COCO 상자가 이미지 범위를 벗어났습니다.

**거부 조건:** [`result['raw_sha256'] != raw_hash or result['normalization'] != NORMALIZATION or result['sha256'] != sha256_file(target)`](../../7%EC%B0%A8/prepare_dataset.py#L153)

**오류 메시지:** 정규화 사본의 보존 계약이 다릅니다.

**거부 조건:** [`(result['width'],result['height']) != tuple(expected_size)`](../../7%EC%B0%A8/prepare_dataset.py#L155)

**오류 메시지:** 정규화 사본과 주석 크기가 다릅니다.

**거부 조건:** [`original.size != tuple(expected_size) or original.width*original.height &gt; 100000000`](../../7%EC%B0%A8/prepare_dataset.py#L164)

**오류 메시지:** 해독한 원본 크기와 주석 좌표계가 다릅니다.

**거부 조건:** [`not encoded.endswith(b'\xff\xd9')`](../../7%EC%B0%A8/prepare_dataset.py#L173)

**오류 메시지:** 정규화 JPEG의 종료 표식이 없습니다.

**거부 조건:** [`self.used &lt; 0 or self.used &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L196)

**오류 메시지:** 기존 전송량이 7차 예산과 맞지 않습니다.

**거부 조건:** [`count &lt; 0 or free-count &lt; self.minimum_free`](../../7%EC%B0%A8/prepare_dataset.py#L201)

**오류 메시지:** 쓰기 후 잔여 공간 100GiB를 보장할 수 없습니다.

**거부 조건:** [`count &lt; 0 or self.used+count &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L205)

**오류 메시지:** 7차 누적 전송 예산을 초과했습니다.

**거부 조건:** [`value['bytes'] &lt; 0 or self.used+value['bytes'] &gt; self.limit`](../../7%EC%B0%A8/prepare_dataset.py#L221)

**오류 메시지:** 사전 전송을 합치면 7차 전송 예산을 초과합니다.

**거부 조건:** [`not metadata.exists()`](../../7%EC%B0%A8/prepare_dataset.py#L319)

**오류 메시지:** 출처 없는 부분 다운로드입니다.

**거부 조건:** [`old.get('url') != identity['url'] or old.get('size') != identity['size'] or old.get('md5',identity['md5']) != identity['md5']`](../../7%EC%B0%A8/prepare_dataset.py#L322)

**오류 메시지:** 부분 다운로드의 원자료 계약이 다릅니다.

**거부 조건:** [`row.get('available') and sha256_file(local(row['raw_image']))!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L594)

**오류 메시지:** 추가로 대조한 과거 사용 원본이 바뀌었습니다.

**거부 조건:** [`manifest['contract']!=contract`](../../7%EC%B0%A8/prepare_dataset.py#L672)

**오류 메시지:** 준비된 데이터 계약이 다릅니다.

**거부 조건:** [`sha256_file(raw)!=row['sha256'] or sha256_file(label)!=row['label_sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L695)

**오류 메시지:** 보존 TACO 원본·라벨 계약과 다릅니다.

**거부 조건:** [`self.imports[identity] != value`](../../7%EC%B0%A8/prepare_dataset.py#L218)

**오류 메시지:** 이미 합산한 사전 전송 영수증이 변경됐습니다.

**거부 조건:** [`state.get('state')=='running'`](../../7%EC%B0%A8/prepare_dataset.py#L290)

**오류 메시지:** 수신 잠금은 풀렸지만 사전 수신 상태가 running입니다. 원인을 확인해야 합니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L334)

**오류 메시지:** 재시도 전 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`budget.used+remaining &gt; budget.limit`](../../7%EC%B0%A8/prepare_dataset.py#L338)

**오류 메시지:** 남은 전송 예산이 부족합니다.

**거부 조건:** [`path.is_absolute() or '..' in path.parts or ':' in info.filename or stat.S_ISLNK(info.external_attr &gt;&gt; 16)`](../../7%EC%B0%A8/prepare_dataset.py#L410)

**오류 메시지:** ZIP에 허용하지 않는 경로가 있습니다.

**거부 조건:** [`not target.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L419)

**오류 메시지:** ZIP 추출 경로가 원본 보관 폴더를 벗어납니다.

**거부 조건:** [`temporary.is_symlink() or not temporary.resolve().is_relative_to(boundary)`](../../7%EC%B0%A8/prepare_dataset.py#L432)

**오류 메시지:** ZIP 임시 파일이 허용 경로를 벗어납니다.

**거부 조건:** [`temporary.stat().st_size != info.file_size`](../../7%EC%B0%A8/prepare_dataset.py#L436)

**오류 메시지:** ZIP 추출 크기가 다릅니다.

**거부 조건:** [`sha256_file(path)!=row['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L572)

**오류 메시지:** 과거 추가 자료가 보존 manifest와 다릅니다.

**거부 조건:** [`not match`](../../7%EC%B0%A8/prepare_dataset.py#L705)

**오류 메시지:** 과거 pLitter 원본 ID를 확인할 수 없습니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/prepare_dataset.py#L283)

**오류 메시지:** 공식 자료 수신 잠금 대기 12시간을 초과했습니다.

**거부 조건:** [`not target.exists() or sha256_file(target)!=receipt['sha256']`](../../7%EC%B0%A8/prepare_dataset.py#L300)

**오류 메시지:** 사전 수신 SHA와 완성 원자료가 다릅니다.

**거부 조건:** [`existing.is_symlink() or getattr(existing,'is_junction',lambda:False)()`](../../7%EC%B0%A8/prepare_dataset.py#L417)

**오류 메시지:** ZIP 추출 경로에 기존 파일 링크가 있습니다.

**거부 조건:** [`response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}'`](../../7%EC%B0%A8/prepare_dataset.py#L349)

**오류 메시지:** 서버가 원본 범위 요청을 보존하지 않았습니다.

**거부 조건:** [`saved!=start or load(metadata)!=identity`](../../7%EC%B0%A8/prepare_dataset.py#L378)

**오류 메시지:** 실패 수신 후 부분 파일 크기·원자료 계약이 변경됐습니다.

**거부 조건:** [`len(block)&gt;remaining`](../../7%EC%B0%A8/prepare_dataset.py#L368)

**오류 메시지:** 수신 본문이 요청한 원본 범위를 초과했습니다.


### [train_pipeline.py](../../7%EC%B0%A8/train_pipeline.py)


**설정·옵션:** [`EVALUATOR`](../../7%EC%B0%A8/train_pipeline.py#L12)

**코드의 선언:** `정의='single-class confidence-greedy IoU; 101-point interpolated AP; v2'`


**거부 조건:** [`not results`](../../7%EC%B0%A8/train_pipeline.py#L69)

**오류 메시지:** 검증 후보가 없습니다.

**거부 조건:** [`not math.isfinite(elapsed) or elapsed&lt;0 or hours*3600-elapsed&lt;=0`](../../7%EC%B0%A8/train_pipeline.py#L84)

**오류 메시지:** 후보의 누적 학습 시간 예산이 끝났거나 잘못됐습니다.

**거부 조건:** [`width&lt;=0 or height&lt;=0 or grid not in (1,2,3)`](../../7%EC%B0%A8/train_pipeline.py#L94)

**오류 메시지:** 허용하지 않는 타일 크기입니다.

**거부 조건:** [`path.exists() and load(path)!=contract`](../../7%EC%B0%A8/train_pipeline.py#L118)

**오류 메시지:** checkpoint 원본·데이터·코드·학습 계약이 다릅니다.

**거부 조건:** [`not torch.cuda.is_available()`](../../7%EC%B0%A8/train_pipeline.py#L162)

**오류 메시지:** CUDA GPU가 없습니다. CPU로 장기 학습을 우회하지 않습니다.

**거부 조건:** [`any(list(model.names.values())!=['trash'] for model in models)`](../../7%EC%B0%A8/train_pipeline.py#L188)

**오류 메시지:** 단일 trash 클래스 모델이 아닙니다.

**거부 조건:** [`not best.exists()`](../../7%EC%B0%A8/train_pipeline.py#L310)

**오류 메시지:** 학습 완료 가중치가 없습니다.

**거부 조건:** [`type(resume) is not bool`](../../7%EC%B0%A8/train_pipeline.py#L327)

**오류 메시지:** 재개는 명시적 bool이어야 합니다.

**거부 조건:** [`not path.exists()`](../../7%EC%B0%A8/train_pipeline.py#L120)

**오류 메시지:** 완료 학습의 원래 계약이 없습니다.

**거부 조건:** [`not best.exists() or sha256_file(best)!=load(directory/'phase_complete.json')['best_sha256']`](../../7%EC%B0%A8/train_pipeline.py#L122)

**오류 메시지:** 완료 학습 가중치가 보존 해시와 다릅니다.

**거부 조건:** [`not path.exists() or not allow_resume`](../../7%EC%B0%A8/train_pipeline.py#L126)

**오류 메시지:** 중단 checkpoint는 동일 계약과 명시적 재개가 필요합니다.

**거부 조건:** [`time.monotonic()&gt;=deadline`](../../7%EC%B0%A8/train_pipeline.py#L168)

**오류 메시지:** 다른 GPU 작업 때문에 필요한 여유 VRAM을 확보하지 못했습니다.

**거부 조건:** [`sha256_file(local(path))!=expected`](../../7%EC%B0%A8/train_pipeline.py#L320)

**오류 메시지:** 선택 가중치가 최종 평가 계약과 다릅니다.

**거부 조건:** [`int(checkpoint.get('epoch',-1))&lt;0`](../../7%EC%B0%A8/train_pipeline.py#L297)

**오류 메시지:** 완료 표식 없는 정리된 checkpoint입니다. 자동 재학습하지 않습니다.


### [verify_sources.py](../../7%EC%B0%A8/verify_sources.py)


| 내용 |
| --- |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/verify_sources.py#L6)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |

**거부 조건:** [`config['download_limit_bytes']!=100*1024**3 or config['minimum_disk_free_bytes']!=100*1024**3`](../../7%EC%B0%A8/verify_sources.py#L23)

**오류 메시지:** 신규 전송 예산·잔여 공간 계약이 다릅니다.

**거부 조건:** [`len(config['candidates'])!=2 or any(row['patience']!=12 for row in config['candidates'])`](../../7%EC%B0%A8/verify_sources.py#L25)

**오류 메시지:** 검토한 두 후보 명세가 다릅니다.


### [worker.py](../../7%EC%B0%A8/worker.py)


**표 항목:** 설정·옵션 · 코드의 선언

| 내용 |
| --- |
| **설정·옵션:** [`--action`](../../7%EC%B0%A8/worker.py#L210)<br>**코드의 선언:** `choices=['train', 'status']` |
| **설정·옵션:** [`--params`](../../7%EC%B0%A8/worker.py#L211)<br>**코드의 선언:** `default='{}'` |
| **설정·옵션:** [`--worker`](../../7%EC%B0%A8/worker.py#L212)<br>**코드의 선언:** `` |
| **설정·옵션:** [`ROOT`](../../7%EC%B0%A8/worker.py#L15)<br>**코드의 선언:** `정의=Path(__file__).resolve().parent` |
| **설정·옵션:** [`WORK`](../../7%EC%B0%A8/worker.py#L16)<br>**코드의 선언:** `정의=ROOT / 'work'` |
| **설정·옵션:** [`PROC`](../../7%EC%B0%A8/worker.py#L17)<br>**코드의 선언:** `정의=Path('/proc')` |
| **설정·옵션:** [`ACTIVE`](../../7%EC%B0%A8/worker.py#L18)<br>**코드의 선언:** `정의={'queued', 'running'}` |

**거부 조건:** [`not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value)`](../../7%EC%B0%A8/worker.py#L22)

**오류 메시지:** 허용되지 않는 작업 ID입니다.

**거부 조건:** [`not isinstance(value, dict)`](../../7%EC%B0%A8/worker.py#L130)

**오류 메시지:** 작업 기록이 없습니다.

**거부 조건:** [`not isinstance(params, dict) or set(params) - {'resume'} or type(params.get('resume', False)) is not bool`](../../7%EC%B0%A8/worker.py#L158)

**오류 메시지:** 설정은 resume: true 또는 false만 허용하는 JSON 객체입니다.

**거부 조건:** [`any(value.get('state') in ACTIVE for value in jobs())`](../../7%EC%B0%A8/worker.py#L162)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.

**거부 조건:** [`not value or value.get('state') != 'queued' or value.get('kind') != 'train'`](../../7%EC%B0%A8/worker.py#L186)

**오류 메시지:** 새로 대기 중인 학습 작업만 실행할 수 있습니다.

**거부 조건:** [`not isinstance(result, dict)`](../../7%EC%B0%A8/worker.py#L195)

**오류 메시지:** 학습 파이프라인이 결과 객체를 반환하지 않았습니다.

**거부 조건:** [`not blocking`](../../7%EC%B0%A8/worker.py#L62)

**오류 메시지:** 준비 또는 학습 작업이 이미 진행 중입니다.


</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

precision·recall·mAP와 입력 데이터·분할·정책 선택 단계를 함께 읽습니다. 객체 탐지, 영상 사건 후보, 실제 투기 행위 판단은 다른 평가 대상입니다. 목표 90%와 완료된 시험 성적을 구분합니다.

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

5차에서 7차로 이어지는 실제 파일 비교입니다.

[전체 비교·자료 범위](../comparisons/5-to-7.md)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>파일별 비교·크기·해시 자세히 보기</summary>

[공개 폴더](../../7차/) · [실험과 실행 조건](../../7차/README.md) · [5차와 파일 비교](../comparisons/5-to-7.md)

[같은 7차의 다운로드 오류 수정과 전체 차이](../comparisons/7-recovery-20261030.md)도 함께 보존합니다.

</details>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../7%EC%B0%A8) · [← 이전: 5차](round-5.md) · [다음: 8차 →](round-8.md)
