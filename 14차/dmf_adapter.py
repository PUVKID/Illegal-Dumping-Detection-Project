"""고정 DMF 원본을 사용하는 ICT 안전 문서의 로컬 검증 연결 코드.

이 파일은 upstream 코드를 복제하지 않는다. 해시 검증 후 공개 API를 호출한다.
"""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import stat
import sys

ROOT = Path(__file__).resolve().parent
COMMIT = 'cf550e3b2ceb0946ba89f64e43b7d6c2f5164383'
TREE = '906a2d35af5abe9449a417f2e3dbc740abb0e4e8'
# 취득 완료 뒤 독립 원본 manifest로 고정하며 실행 중 자동 갱신하지 않는다.
PINNED_POLICY_SHA256 = '3331fdd907cfd54a1b18fcf365694723b5db55d9272c229e9c3f781ff329ce69'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def encoded(value) -> bytes:
    # 수치 원본은 이 함수로 보내지 않으며, 검증 메타데이터만 직렬화한다.
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def no_links(path: Path) -> None:
    """심볼릭 링크와 Windows 정션 등 모든 경로 구성요소의 재분석 지점을 거부한다."""
    for current in (path, *path.parents):
        if not current.exists() and not current.is_symlink():
            continue
        info = current.lstat()
        if (current == path and current.is_file() and getattr(info, 'st_nlink', 1) > 1) or current.is_symlink() or getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 1024):
            raise ValueError(f'링크/재분석 경로 거부: {current}')


def selected_file(base: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative or PurePosixPath(relative).is_absolute() or PureWindowsPath(relative).drive or any(p in ('..', '.', '') for p in relative.split('/')):
        raise ValueError(f'허용되지 않는 상대경로: {relative!r}')
    candidate = base / relative
    no_links(candidate)
    candidate.resolve().relative_to(base.resolve())
    if not candidate.is_file():
        raise ValueError(f'일반 파일이 아님: {candidate}')
    return candidate


def collect_inputs(input_dir: Path, spec: dict) -> tuple[list[dict], dict[str, bytes]]:
    no_links(input_dir)
    if not input_dir.is_dir():
        raise ValueError('입력 디렉터리가 없음')
    modules = spec.get('modules')
    if not isinstance(modules, list) or not 4 <= len(modules) <= 6:
        raise ValueError('명시적 입력 모듈 4~6개 필요')
    names, identifiers = set(), set()
    records, contents = [], {}
    for item in modules:
        name, identifier, level = item['path'], item['id'], item['level']
        key = name.casefold()
        if key in names or identifier in identifiers:
            raise ValueError('중복 모듈 경로 또는 ID')
        if level not in ('immutable', 'restricted', 'free'):
            raise ValueError('알 수 없는 변경 분류')
        names.add(key)
        identifiers.add(identifier)
        path = selected_file(input_dir, name)
        if path.suffix.lower() not in ('.md', '.json'):
            raise ValueError('Markdown/JSON 문서만 허용')
        data = path.read_bytes()
        data.decode('utf-8', errors='strict')
        records.append({'id': identifier, 'path': name, 'level': level, 'bytes': len(data), 'sha256': sha(data)})
        contents[identifier] = data
    return records, contents


def source_hashes() -> dict:
    files = [ROOT / 'dmf_adapter.py', ROOT / '실행검증.py', *sorted((ROOT / 'configs').glob('*.json')), *sorted((ROOT / 'tests').glob('*.py'))]
    return {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p.read_bytes()) for p in files}


def load_upstream(dmf_root: Path):
    dmf_root = Path(dmf_root).absolute()
    no_links(dmf_root)
    policy_path = ROOT / 'configs/DMF고정해시.json'
    no_links(policy_path)
    if sha(policy_path.read_bytes()) != PINNED_POLICY_SHA256:
        raise ValueError('고정 원본 해시 정책이 변경됨')
    policy = read_json(policy_path)
    if policy['commit'] != COMMIT or policy['tree'] != TREE or len(policy['files']) != 20:
        raise ValueError('원본 커밋/트리/파일수 불일치')
    expected = {item['path']: item for item in policy['files']}
    actual = set()
    for path in dmf_root.rglob('*'):
        relative = path.relative_to(dmf_root).as_posix()
        if relative.split('/')[0] == '_취득근거':
            continue
        no_links(path)
        if path.is_file():
            actual.add(relative)
    if actual != set(expected):
        raise ValueError('고정20파일 이외 추가/누락 원본 거부')
    for relative, record in expected.items():
        data = selected_file(dmf_root, relative).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
        if sha(data) != record['sha256'] or len(data) != record['bytes'] or blob != record['git_blob_sha1']:
            raise ValueError(f'원본 바이트 고정값 불일치: {relative}')
        data.decode('utf-8', errors='strict')
    # 기존 모듈 캐시를 신뢰하지 않고 검증한 디렉터리만 우선한다.
    for name in list(sys.modules):
        if name == 'dmf_integrity' or name.startswith('dmf_integrity.'):
            del sys.modules[name]
    importlib.invalidate_caches()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(dmf_root / 'src'))
    try:
        api = importlib.import_module('dmf_integrity')
    finally:
        sys.path.pop(0)
    imported = []
    for name, module in list(sys.modules.items()):
        if name == 'dmf_integrity' or name.startswith('dmf_integrity.'):
            path = Path(module.__file__).absolute()
            no_links(path)
            try:
                relative = path.relative_to(dmf_root).as_posix()
            except ValueError as exc:
                raise ValueError('다른 위치의 DMF 모듈 임포트 거부') from exc
            digest = sha(path.read_bytes())
            if relative not in expected or digest != expected[relative]['sha256']:
                raise ValueError('실제 임포트 파일과 고정 원본 불일치')
            imported.append({'module': name, 'path': relative, 'sha256': digest})
    return api, {'repository': policy['repository'], 'commit': COMMIT, 'tree': TREE, 'verified_source_files': len(expected), 'imported_files': sorted(imported, key=lambda x: x['path']), 'policy_sha256': PINNED_POLICY_SHA256}


def verify_versions(api, versions) -> None:
    if not versions:
        raise ValueError('빈 버전 체인')
    doc_id = versions[0].document_id
    for index, version in enumerate(versions, 1):
        if version.document_id != doc_id or version.version_no != index:
            raise ValueError('문서 ID 또는 버전 순서 불일치')
        if api.manifest_root(version.modules) != version.manifest_root or api.restrict_seal(version.modules) != version.restrict_seal:
            raise ValueError('저장된 manifest/seal과 재계산값 불일치')
        if index > 1 and api.check_restrictions(versions[index - 2].modules, version.modules):
            raise ValueError('불변 안전 경계 위반 버전')
    api.verify_version_chain(versions)


def verify_audit(api, entries, head) -> None:
    if not entries and tuple(head) != (0, '0' * 64):
        raise ValueError('비어 있는 감사 기록과 비영 앵커 불일치')
    if entries and len({entry.chain_id for entry in entries}) != 1:
        raise ValueError('감사 체인 ID 혼합')
    api.verify_chain(entries, expected_head=tuple(head))


def version_json(version) -> dict:
    from dataclasses import asdict
    result = asdict(version)
    result['version_id'] = version.version_hash
    result['parent_version_id'] = version.parent_version_hash
    result['module_manifest_hash'] = version.manifest_root
    return result


def restore_version(api, value):
    modules = tuple(api.ModuleRef(m['module_id'], m['kind'], api.Mutability(m['mutability']), m['ordinal'], m['content_sha256'], tuple(m['depends_on'])) for m in value['modules'])
    return api.VersionRecord(value['document_id'], value['version_no'], value['parent_version_hash'], modules, value['metadata'], value['manifest_root'], value['restrict_seal'], value['version_hash'])


def verify_bundle(output_dir: Path, dmf_root: Path, input_dir: Path, expected_seal_sha256: str | None = None) -> dict:
    output_dir, input_dir = Path(output_dir).absolute(), Path(input_dir).absolute()
    no_links(output_dir)
    seal_path = selected_file(output_dir, '실행봉인.json')
    if expected_seal_sha256 is not None and sha(seal_path.read_bytes()) != expected_seal_sha256:
        raise ValueError('독립 보존 봉인 SHA 불일치')
    seal = read_json(seal_path)
    if seal['source_hashes'] != source_hashes():
        raise ValueError('검증 후 어댑터/정책/검사 소스 변경')
    if {p.name for p in output_dir.iterdir()} != set(seal['output_hashes']) | {'실행봉인.json'}:
        raise ValueError('출력 파일 추가/누락')
    for name, digest in seal['output_hashes'].items():
        if sha(selected_file(output_dir, name).read_bytes()) != digest:
            raise ValueError(f'출력 바이트 변조: {name}')
    spec = read_json(ROOT / 'configs/입력명세.json')
    records, original_contents = collect_inputs(input_dir, spec)
    if records != read_json(output_dir / '입력해시.json')['modules']:
        raise ValueError('원본 입력 변경')
    api, upstream = load_upstream(Path(dmf_root))
    if upstream != seal['upstream']:
        raise ValueError('실제 임포트 근거 변경')
    document = read_json(output_dir / '버전기록.json')
    versions = [restore_version(api, value) for value in document['versions']]
    verify_versions(api, versions)
    if len(versions) != 3 or versions[2].manifest_root != versions[0].manifest_root or versions[2].version_hash == versions[0].version_hash:
        raise ValueError('롤백 내용/새 이력 조건 불일치')
    contents = read_json(output_dir / '모듈내용.json')['contents']
    for digest, content in contents.items():
        if sha(content.encode('utf-8')) != digest:
            raise ValueError('저장 모듈 바이트 변조')
    for version in versions:
        for module in version.modules:
            if module.content_sha256 not in contents:
                raise ValueError('내용 없는 모듈 참조')
    for record in records:
        if contents.get(record['sha256']) != original_contents[record['id']].decode('utf-8'):
            raise ValueError('입력과 저장 내용 불일치')
    from dmf_integrity.audit_chain import AuditEntry
    audit = read_json(output_dir / '감사기록.json')
    entries = [AuditEntry(**entry) for entry in audit['entries']]
    verify_audit(api, entries, seal['audit_head'])
    if len(entries) != 3 or [e.target for e in entries] != [v.version_hash for v in versions]:
        raise ValueError('감사와 버전 연결 불일치')
    result = read_json(output_dir / '검증결과.json')
    if result['state'] != 'Shadow' or result['scope'] != 'local_validation_only' or result['official_promotion'] != 'pending_human_review':
        raise ValueError('운영 승인 상태 위조')
    return {'status': 'PASS', 'seal_sha256': sha(seal_path.read_bytes()), 'versions': len(versions), 'audit_entries': len(entries)}


def run(dmf_root: Path, input_dir: Path, output_dir: Path, *, input_spec: dict | None = None) -> dict:
    from dataclasses import asdict, replace
    from datetime import datetime, timezone
    dmf_root, input_dir, output_dir = Path(dmf_root).absolute(), Path(input_dir).absolute(), Path(output_dir).absolute()
    no_links(output_dir)
    if output_dir.exists():
        raise FileExistsError('기존 출력 디렉터리 덮어쓰기 거부')
    # 출력 위치가 입력·원본·소스 내부이면 자체 오염을 막는다.
    for protected in (input_dir, dmf_root, ROOT / 'configs', ROOT / 'tests'):
        if output_dir == protected or protected in output_dir.parents or output_dir in protected.parents:
            raise ValueError('보호 입력/소스와 겹치는 출력 위치')
    spec = input_spec if input_spec is not None else read_json(ROOT / 'configs/입력명세.json')
    records, contents = collect_inputs(input_dir, spec)
    if input_spec is not None and spec != read_json(ROOT / 'configs/입력명세.json'):
        # 실험용 입력 명세도 안전성 검사를 먼저 수행하지만 공개 재현 정책을 바꾸지는 못한다.
        raise ValueError('고정 입력 명세와 다른 선택 거부')
    initial_source_hashes = source_hashes()
    api, upstream = load_upstream(dmf_root)
    from dmf_integrity.audit_chain import ChainBrokenError
    levels = {'immutable': api.Mutability.IMMUTABLE_CORE, 'restricted': api.Mutability.RESTRICTED, 'free': api.Mutability.MUTABLE}
    base = tuple(api.ModuleRef(r['id'], 'section', levels[r['level']], i, r['sha256']) for i, r in enumerate(records))
    meta = {'dc:title': 'ICT 안전 쓰레기 탐지 프로젝트 DMF 적용', 'state': 'Shadow', 'scope': 'local_validation_only', 'upstream_commit': COMMIT}
    checks = []

    def check(identifier, name, condition, detail):
        checks.append({'id': identifier, 'name': name, 'status': 'PASS' if condition else 'FAIL', 'detail': detail})
        if not condition:
            raise ValueError(f'검사 실패: {identifier}: {name}')

    def rejected(function, exceptions=(ValueError,)):
        try:
            function()
        except exceptions:
            return True
        return False

    def changed(modules, identifier, data):
        return tuple(replace(m, content_sha256=api.content_sha256(data)) if m.module_id == identifier else m for m in modules)

    free_ids = [r['id'] for r in records if r['level'] == 'free']
    if len(free_ids) < 2 or not any(r['level'] == 'immutable' for r in records) or not any(r['level'] == 'restricted' for r in records):
        raise ValueError('두 가변 모듈과 불변/제한 모듈 필요')
    modified_data = contents[free_ids[0]] + '\n로컬 검증 예시 개정: 운영 적용이나 승인 사실을 뜻하지 않는다.\n'.encode('utf-8')
    candidate = changed(base, free_ids[0], modified_data)
    violations = api.check_restrictions(base, candidate)
    check('normal_edit', '가변 모듈 정상 수정 허용', not violations and api.risk_floor(base, candidate) == 1, '실제 입력 사본의 예시 개정, R1')
    immutable_id = next(r['id'] for r in records if r['level'] == 'immutable')
    bad_core = changed(base, immutable_id, b'controlled core corruption')
    core_codes = [v.code for v in api.check_restrictions(base, bad_core)]
    check('immutable_reject', '불변 안전 경계 변경 거부', 'CORE_MODIFIED' in core_codes, ','.join(core_codes))
    restricted_id = next(r['id'] for r in records if r['level'] == 'restricted')
    restricted = changed(base, restricted_id, contents[restricted_id] + b'\n' + b'x' * (len(contents[restricted_id]) + 1))
    check('restricted_risk', '제한 모듈 대폭 변경의 R2 하한', api.risk_floor(base, restricted) == 2, '합성 사본의 추가 바이트가 원문 100% 초과. API는 변경률 20%를 계산하지 않고 제한 등급 접촉만으로 R2를 반환한다. 비율 정책 자동 집행 아님.')
    v1 = api.build_version('ict-safety-document', 1, None, base, meta)
    v2 = api.build_version('ict-safety-document', 2, v1, candidate, meta)
    v3 = api.build_version('ict-safety-document', 3, v2, base, meta)
    versions = [v1, v2, v3]
    verify_versions(api, versions)
    check('rollback', '롤백은 직전 버전에 연결한 새 버전', v3.parent_version_hash == v2.version_hash and v3.manifest_root == v1.manifest_root and v3.version_hash != v1.version_hash, 'v3 부모=v2, 내용=v1, 기존 버전 보존')
    check('history_tamper', '소급 버전 내용 변조 탐지', rejected(lambda: verify_versions(api, [v1, replace(v2, metadata={'state': 'tampered'}), v3])), '합성 사본 메타데이터 변조')
    check('manifest_field_tamper', '저장 manifest 필드 변조 탐지', rejected(lambda: verify_versions(api, [replace(v1, manifest_root='f' * 64), v2, v3])), 'wrapper에서 저장값과 실제 재계산값 추가 비교')
    check('seal_field_tamper', '저장 불변 봉인 필드 변조 탐지', rejected(lambda: verify_versions(api, [replace(v1, restrict_seal='f' * 64), v2, v3])), 'wrapper에서 저장값과 실제 재계산값 추가 비교')
    other = changed(base, free_ids[1], contents[free_ids[1]] + b'\nparallel example\n')
    merged = api.three_way_merge(base, candidate, other)
    merged_by_id = {m.module_id: m.content_sha256 for m in merged.modules}
    check('disjoint_merge', '서로 다른 모듈의 병합', merged.clean and not api.check_restrictions(base, merged.modules) and merged_by_id[free_ids[0]] == sha(modified_data) and merged_by_id[free_ids[1]] == sha(contents[free_ids[1]] + b'\nparallel example\n'), '두 편집 결과 해시 보존')
    conflict = api.three_way_merge(base, candidate, changed(base, free_ids[0], b'other concurrent content'))
    check('same_module_conflict', '같은 모듈 충돌 탐지', not conflict.clean and free_ids[0] in [c.module_id for c in conflict.conflicts], '자동 덮어쓰기 안 함')
    chain = api.AuditChain('ict-safety-document')
    for index, version in enumerate(versions, 1):
        chain.append(occurred_at=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'), actor='urn:ict-safety:local-validation-script', action='local.rollback.example' if index == 3 else 'local.version.example', target=version.version_hash, detail={'scope': 'local_validation_only', 'version_no': str(index), 'manifest_root': version.manifest_root})
    verify_audit(api, chain.entries, chain.head)
    check('audit_tamper', '감사 행 변조 탐지', rejected(lambda: verify_audit(api, [replace(chain.entries[0], actor='altered'), *chain.entries[1:]], chain.head), (ValueError, ChainBrokenError)), '합성 사본 actor 변경')
    check('audit_truncation', '감사 꼬리 삭제 탐지', rejected(lambda: verify_audit(api, chain.entries[:-1], chain.head), (ValueError, ChainBrokenError)), '동일 로컬 head와 대조')
    check('empty_audit_anchor', '빈 감사와 비영 앵커 거부', rejected(lambda: verify_audit(api, [], chain.head)), 'wrapper 빈체인 검사, 외부 앵커 아님')
    final_records, _ = collect_inputs(input_dir, spec)
    check('input_preserved', '원본 입력 바이트 보존', records == final_records, '입력 4파일 전후 SHA-256 일치')
    check('upstream_import', '실제 임포트된 고정 원본 확인', upstream['verified_source_files'] == 20 and len(upstream['imported_files']) == 7, '원본 20파일 바이트/크기/Git blob 및 실제 임포트 7파일 SHA 검증')
    if source_hashes() != initial_source_hashes:
        raise ValueError('실행 도중 소스 변경')
    result = {'schema': 'ict-dmf-validation-v1', 'state': 'Shadow', 'scope': 'local_validation_only', 'official_promotion': 'pending_human_review', 'upstream': upstream, 'checks': checks, 'summary': {'passed': len(checks), 'total': len(checks)}, 'limitations': ['운영 Shadow 배포 또는 실제 트래픽 비교가 아닌 로컬 검증 상태', 'G1~G9 전체 게이트 미수행, 사람 승인 미생성', 'PostgreSQL/OIDC/KMS/전자서명/외부 타임스탬프/DB 원자성 미구현', '동일 권한 주체가 코드·정책·전체 기록과 봉인을 함께 바꾸면 로컬 해시만으로 인증할 수 없음', '업스트림 라이선스 미확인: 원본 코드는 로컬 비공개 참조', 'restricted 위험도는 R2 하한이며 20% 변경률 정책의 자동 계산은 API 미구현']}
    outputs = {'버전기록.json': {'versions': [version_json(v) for v in versions], 'rollback_derived_from_version_id': v1.version_hash}, '감사기록.json': {'entries': [asdict(e) for e in chain.entries], 'head': list(chain.head)}, '입력해시.json': {'modules': records, 'input_selection': spec}, '모듈내용.json': {'contents': {sha(data): data.decode('utf-8') for data in [*contents.values(), modified_data]}}, '검증결과.json': result}
    output_dir.mkdir(parents=True, exist_ok=False)
    for name, value in outputs.items():
        with (output_dir / name).open('xb') as stream:
            stream.write(encoded(value))
    seal = {'schema': 'ict-dmf-local-seal-v1', 'source_hashes': initial_source_hashes, 'upstream': upstream, 'audit_head': list(chain.head), 'output_hashes': {name: sha((output_dir / name).read_bytes()) for name in outputs}, 'trust': 'local_integrity_only_no_server_attestation'}
    with (output_dir / '실행봉인.json').open('xb') as stream:
        stream.write(encoded(seal))
    verify_bundle(output_dir, dmf_root, input_dir, sha((output_dir / '실행봉인.json').read_bytes()))
    return result
