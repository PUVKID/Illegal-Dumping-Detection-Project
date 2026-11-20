"""실제 DMF를 사용하며 경계 보호가 제거되면 실패하는 통합 검사."""
import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'work' / 'DMF원본'

class AdapterContract(unittest.TestCase):
    def test_reproducible_entrypoint_exists(self):
        self.assertTrue((ROOT / '실행검증.py').is_file(), '미구현: 재현 가능한 실행 진입점 필요')

class IntegrationContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (ROOT / 'dmf_adapter.py').exists():
            raise unittest.SkipTest('연결 코드 구현 전 제어된 TDD 단계')
        sys.path.insert(0, str(ROOT))
        import dmf_adapter
        cls.api = dmf_adapter

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='ict_dmf_')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.inputs = self.base / '자료'
        self.inputs.mkdir()
        for name, content in {
            '프로젝트개요.md': '목적과 기존 동작\n',
            '안전경계.md': '원영상 공개 금지와 평가 분할 보존\n',
            '개발내용.md': '기존 쓰레기 탐지 기능 설명\n',
            '관측사실.json': '{"precision": 0.5204460966542751, "target_met": false}\n',
        }.items():
            (self.inputs / name).write_text(content, encoding='utf-8')
        self.out = self.base / '결과'

    def run_adapter(self, **kwargs):
        return self.api.run(UPSTREAM, self.inputs, self.out, **kwargs)

    def test_real_library_versions_and_input_preservation(self):
        original = {p.name: p.read_bytes() for p in self.inputs.iterdir()}
        result = self.run_adapter()
        self.assertEqual(result['summary']['passed'], result['summary']['total'])
        self.assertGreaterEqual(result['summary']['total'], 10)
        self.assertEqual(result['state'], 'Shadow')
        versions = json.loads((self.out / '버전기록.json').read_text(encoding='utf-8'))['versions']
        self.assertEqual(len(versions), 3)
        self.assertEqual(versions[2]['parent_version_id'], versions[1]['version_id'])
        self.assertEqual(versions[2]['module_manifest_hash'], versions[0]['module_manifest_hash'])
        self.assertNotEqual(versions[1]['module_manifest_hash'], versions[0]['module_manifest_hash'])
        self.assertTrue(result['upstream']['imported_files'])
        self.assertEqual({p.name: p.read_bytes() for p in self.inputs.iterdir()}, original)
        self.api.verify_bundle(self.out, UPSTREAM, self.inputs)

    def test_existing_output_is_never_overwritten(self):
        self.out.mkdir()
        marker = self.out / '사용자파일.txt'
        marker.write_bytes(b'keep')
        with self.assertRaises((ValueError, FileExistsError)):
            self.run_adapter()
        self.assertEqual(marker.read_bytes(), b'keep')

    def test_path_escape_and_duplicate_selection_rejected(self):
        policy = json.loads((ROOT / 'configs/입력명세.json').read_text(encoding='utf-8-sig'))
        for bad in ('../외부.md', '/외부.md', 'C:/외부.md'):
            broken = copy.deepcopy(policy)
            broken['modules'][0]['path'] = bad
            with self.subTest(path=bad), self.assertRaises(ValueError):
                self.run_adapter(input_spec=broken)
        broken = copy.deepcopy(policy)
        broken['modules'][1]['path'] = broken['modules'][0]['path']
        with self.assertRaises(ValueError):
            self.run_adapter(input_spec=broken)

    def test_output_tampering_rejected(self):
        self.run_adapter()
        target = self.out / '버전기록.json'
        target.write_bytes(target.read_bytes() + b' ')
        with self.assertRaises(ValueError):
            self.api.verify_bundle(self.out, UPSTREAM, self.inputs)

    def test_original_input_change_rejected(self):
        self.run_adapter()
        (self.inputs / '관측사실.json').write_text('{}', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.api.verify_bundle(self.out, UPSTREAM, self.inputs)

    def test_unpinned_upstream_rejected_before_import(self):
        altered = self.base / '다른원본'
        shutil.copytree(UPSTREAM, altered)
        python_files = list(altered.rglob('*.py'))
        self.assertTrue(python_files)
        python_files[0].write_bytes(python_files[0].read_bytes() + b'\n# tamper\n')
        with self.assertRaises(ValueError):
            self.api.run(altered, self.inputs, self.out)
        self.assertFalse(self.out.exists())

    def test_policy_change_detected_after_execution(self):
        from unittest.mock import patch
        self.run_adapter()
        with patch.object(self.api, 'source_hashes', return_value={'changed': 'policy'}):
            with self.assertRaises(ValueError):
                self.api.verify_bundle(self.out, UPSTREAM, self.inputs)

    def test_simulated_reparse_link_is_rejected(self):
        # 실제 링크를 생성하지 않는 통제 시험이다. 경로의 재분석 속성을 모사한다.
        from unittest.mock import patch
        from types import SimpleNamespace
        target = self.inputs / '안전경계.md'
        real_lstat = Path.lstat
        def link_stat(path, *args, **kwargs):
            if path == target:
                original = real_lstat(path, *args, **kwargs)
                return SimpleNamespace(st_mode=original.st_mode, st_file_attributes=1024, st_nlink=1)
            return real_lstat(path, *args, **kwargs)
        with patch.object(Path, 'lstat', link_stat):
            with self.assertRaises(ValueError):
                self.run_adapter()
        self.assertFalse(self.out.exists())

    def test_cli_exit_and_readonly_verification(self):
        completed = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(ROOT / '실행검증.py'), '--dmf-root', str(UPSTREAM), '--input-dir', str(self.inputs), '--output-dir', str(self.out)], capture_output=True, text=True, encoding='utf-8', cwd=ROOT.parent)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.api.verify_bundle(self.out, UPSTREAM, self.inputs)

if __name__ == '__main__':
    unittest.main()
