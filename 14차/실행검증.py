"""DMF 로컬 실행과 읽기 전용 재검증 진입점."""
import argparse
import json
from pathlib import Path
from dmf_adapter import run, verify_bundle


def main():
    parser = argparse.ArgumentParser(description='ICT 안전 문서 DMF 로컬 검증')
    parser.add_argument('--dmf-root', type=Path, required=True)
    parser.add_argument('--input-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--expected-seal-sha256')
    args = parser.parse_args()
    try:
        result = verify_bundle(args.output_dir, args.dmf_root, args.input_dir, args.expected_seal_sha256) if args.verify_only else run(args.dmf_root, args.input_dir, args.output_dir)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'검증 거부: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
