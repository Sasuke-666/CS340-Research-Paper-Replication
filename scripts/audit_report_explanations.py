#!/usr/bin/env python3
"""Independently recount evidence used in the report's 22 November explanations.

Read-only standard-library check of archived hashes, logs and source. Imports no
measurement runner or existing summary parser. It does not bind natural-language
prose automatically, reconstruct an execution trace or establish causal effects.
"""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


BATCH = 'results/2026-11-07/comparison-42381922637'
FOLLOWUP = 'results/2026-11-07/followup'
ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
SCOPE = ('Checks the archived evidence underlying the named explanations. '
         'Natural-language report prose is not automatically bound or validated; '
         'requested-order and source checks do not reconstruct actual '
         'memory-operation traces or establish causal effects.')


def require(condition, message):
    """Keep every evidence check active under Python optimization flags."""
    if not condition:
        raise ValueError(message)


def audit(root):
    root = Path(root).resolve()
    files, checked = {}, set()
    manifests = [(BATCH + '/archive_manifest.json', BATCH + '/'),
                 ('results/2026-11-07/manifest.json', '')]
    for manifest, prefix in manifests:
        for row in json.loads((root / manifest).read_text(encoding='utf-8'))['files']:
            files[prefix + row['path']] = row

    def verified_text(relative):
        data = (root / relative).read_bytes()
        row = files[relative]
        require(hashlib.sha256(data).hexdigest() == row['sha256'],
                'Digest mismatch: ' + relative)
        require(len(data) == row['bytes'], 'Size mismatch: ' + relative)
        checked.add(relative)
        return ANSI.sub('', data.decode('utf-8'))

    def read_run(relative):
        text = verified_text(relative)
        require('Runner exit_code=0 timed_out=False' in text,
                'Incomplete or timed-out invocation: ' + relative)
        require(text.count('Start Testing!') == 1, 'Ambiguous start: ' + relative)
        body = text.split('Start Testing!', 1)[1]
        require('End Testing!' in body, 'Missing completion: ' + relative)
        body = body.split('End Testing!', 1)[0]
        sequences, failures, layers = [], [], []
        current = None
        for line in body.splitlines():
            layer = re.search(r'Targeting bugs that bug depth = (\d+) \. Iterate for (\d+) periods', line)
            if layer:
                layers.append(tuple(map(int, layer.groups())))
            request = re.search(r'test\s+(\d+):\s*(\[.*\])', line)
            if request:
                current = int(request[1])
                require(current == len(sequences) + 1,
                        'Nonsequential request: ' + relative)
                value = ast.literal_eval(request[2])
                require(isinstance(value, list) and value
                        and all(isinstance(v, list) for v in value),
                        'Invalid request representation: ' + relative)
                require(layers and len(value) == layers[-1][1],
                        'Period count mismatch: ' + relative)
                sequences.append(value)
            if '[Error Found]' in line:
                require(current is not None and 'assertion failed' in line,
                        'Unexpected error event: ' + relative)
                failures.append(current)
        return {'sequence': sequences, 'failures': failures, 'layers': layers,
                'first_error': failures[0] if failures else None}

    expected = {
        ('account', 'period'): {10: 9, 11: 1},
        ('lazy01', 'period'): {8: 10},
        ('twostage', 'period'): {4: 9, 17: 1},
        ('account', 'author_serialized_abi16'): {4: 8, 20: 1, 25: 1},
        ('lazy01', 'author_serialized_abi16'): {4: 8, 16: 1, 24: 1},
    }
    frequency_results = []
    for (case, method), distribution in expected.items():
        runs = [read_run(f'{BATCH}/{case}/{method}_r{i:02d}.txt') for i in range(1, 11)]
        frequency = Counter(row['first_error'] for row in runs)
        require(frequency == distribution, 'First-failure frequency changed: ' + case + '/' + method)
        item = {'case': case, 'method': method, 'n': len(runs),
                'first_error_frequency': dict(sorted(frequency.items()))}
        if (case, method) == ('twostage', 'period'):
            buggy = Counter(len(row['failures']) for row in runs)
            require(buggy == {1: 1, 2: 9}, 'Twostage buggy-count frequency changed')
            item['buggy_count_frequency'] = dict(sorted(buggy.items()))
        frequency_results.append(item)

    source_root = BATCH + '/reorder_3/source/'
    source_expectations = {
        'run_PDS.py': ['period_limit = bugDepth + 1',
                       'for iterPeriod in range(2, period_limit+1):'],
        'run_OldPDS_abi16.py': ['period_limit = bugDepth + N - 1',
                              'for iterPeriod in range(N_after_DryRun, period_limit+1):',
                              'N_after_DryRun = N'],
        'sbp_sched_mixed_end.py': ['ONLY kps from a same thread can be in a same',
                                 'last period may contain key points from various threads'],
    }
    for filename, expected_fragments in source_expectations.items():
        source = verified_text(source_root + filename)
        require(all(fragment in source for fragment in expected_fragments),
                'Scheduler source declaration changed: ' + filename)
    mapping = {}
    for method, expected_layers in [('period', [(1, 2), (2, 3), (3, 4)]),
                                    ('author_serialized_abi16', [(1, 3), (2, 4), (3, 5)])]:
        row = read_run(f'{BATCH}/reorder_3/{method}_r01.txt')
        require(row['layers'] == expected_layers, 'Observed depth/period mapping changed: ' + method)
        mapping[method] = row['layers']

    extensions = {(d, r): read_run(f'{FOLLOWUP}/extension_d{d}_r{r}.txt')
                  for d in (1, 2, 3) for r in (1, 2, 3)}
    full = extensions[3, 1]['sequence']
    expected_counts = {1: 3, 2: 13, 3: 27}
    require(len(full) == 27, 'Depth-3 request count changed')
    for (depth, repeat), row in extensions.items():
        identity = f'depth {depth}, repetition {repeat}'
        require(len(row['sequence']) == expected_counts[depth], 'Request count changed: ' + identity)
        require(row['sequence'] == full[:expected_counts[depth]], 'Nested-prefix mismatch: ' + identity)
        require(row['layers'] == [(d, d + 1) for d in range(1, depth + 1)],
                'Extension depth/period mapping changed: ' + identity)
        require(row['first_error'] == (None if depth == 1 else 6),
                'Extension first-failure result changed: ' + identity)
    layer_counts = dict(sorted(Counter(map(len, full)).items()))
    require(layer_counts == {2: 3, 3: 10, 4: 14}, 'Depth-3 layer counts changed')
    require(full[5] == [[0], [2], [0, 1, 1]], 'Request 6 changed')

    benchmark = verified_text(source_root + 'reorder_3_bad.c')
    require('static int iSet = 2;' in benchmark and 'static int iCheck = 1;' in benchmark,
            'Benchmark thread counts changed')
    require(benchmark.index('pthread_create(&setPool[i]') < benchmark.index('pthread_create(&checkPool[i]'),
            'Benchmark thread creation order changed')
    require(re.search(r'void \*setThread\(void \*param\) \{\s*a = 1;\s*b = -1;', benchmark),
            'Setter source order changed')
    require('(a == 0 && b == 0) || (a == 1 && b == -1)' in benchmark,
            'Checker source condition changed')
    configuration = verified_text(source_root + 'ConConfig.reorder_3_bad')
    require(configuration.splitlines() == ['reorder_bad.c:71', 'reorder_bad.c:72', 'reorder_bad.c:78'],
            'Key-point configuration changed')
    require(len(checked) == 66, 'Unexpected evidence-file coverage')

    return {
        'integrity_ok': True,
        'evidence_verification': {'hash_and_size_checked_files': len(checked),
                                  'raw_logs': 61, 'source_and_configuration_files': 5,
                                  'manifests': [entry[0] for entry in manifests]},
        'comparison_frequency_results': frequency_results,
        'three_thread_depth_period_pairs': mapping,
        'extension_runs_checked': len(extensions),
        'extension_request_counts': expected_counts,
        'all_extension_sequences_equal_corresponding_depth3_prefix': True,
        'depth3_request_count_by_periods': layer_counts,
        'first_failure_at_depth2_and_depth3': 6,
        'request_6': full[5],
        'source_checks': 'Thread counts, creation order, setter write order, checker condition and key-point configuration.',
        'prose_automatically_bound': False,
        'scope': SCOPE,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1],
                        help='Repository root; defaults to the parent of scripts/')
    args = parser.parse_args()
    try:
        result = audit(args.root)
    except (OSError, ValueError, KeyError, TypeError, SyntaxError) as error:
        print(json.dumps({'integrity_ok': False, 'error': str(error), 'scope': SCOPE}, indent=2))
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
