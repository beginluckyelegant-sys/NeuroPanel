"""CLI with exclusive output directories and private trace files."""
import argparse
import json
import os
from pathlib import Path
from .backend import HTTPBackend, MockBackend
from .pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(description='NeuroPanel reconstructed reference inference')
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--bank', type=Path)
    parser.add_argument('--prompts', type=Path, default=Path('prompts/reference'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    kind = config['backend']['kind']
    if kind not in ('mock', 'http'):
        parser.error('backend.kind must be mock or http')
    backend = MockBackend() if kind == 'mock' else HTTPBackend(config['backend'])
    pipeline = Pipeline(config, backend, args.prompts)
    case = json.loads(args.case.read_text())
    bank = json.loads(args.bank.read_text()) if args.bank else []
    if config['mode'] == 'full' and config['retrieval']['enabled'] and args.bank is None:
        parser.error('Retrieval requires --bank')
    args.output.mkdir(mode=0o700, parents=True, exist_ok=False)
    def write(name, value):
        fd = os.open(args.output / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as f:
            json.dump(value, f, indent=2, ensure_ascii=False)
            f.write('\n')
    try:
        result = pipeline.run(case, bank)
        write('result.json', result)
    except Exception as exc:
        print('Inference failed:', str(exc))
        return 1
    finally:
        write('trace.json', pipeline.trace)
    print('Completed:', args.output / 'result.json')
    print('Reference implementation only; inspect trace.json for provenance and unresolved critic issues.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
