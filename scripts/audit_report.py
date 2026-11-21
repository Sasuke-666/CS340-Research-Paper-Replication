#!/usr/bin/env python3
"""Check maintained report tables against separately audited evidence.

This read-only check connects Tables 2--12 to the archived summaries, the
historical raw-log audit and native-layout records. Run through ``make audit``
to verify the underlying manifests and raw measurements first. It also checks
caption uniqueness, narrative references and local figure targets. It does not
validate every narrative claim, the original paper, visual layout or actual
memory-operation traces, and it does not execute a benchmark.
"""
import argparse
from calendar import month_name
from collections import Counter
import json
import math
from pathlib import Path
import re
import sys

from audit_period_results import audit as audit_historical
from report_config import revision_date


PIN = 'cb8deb9a176e5bb292d70d46557dd61dc0e98069'
CASES = ('reorder_3', 'reorder_4', 'account', 'lazy01', 'twostage')
SERIAL = 'author_serialized_abi16'
METRICS = (('First failing schedule', 'first_error'),
           ('Explored schedules', 'schedules'),
           ('Buggy schedules', 'buggy_schedules'))
SUMMARIES = {
    'primary': 'results/2026-11-07/summaries/comparison-42381922637/summary.json',
    'original': 'results/2026-11-07/summaries/comparison-42380929383/summary.json',
    'followup': 'results/2026-11-07/summaries/comparison-42384122902/summary.json',
    'member': 'results/member-reruns/1240001156-account-20261108T122201Z-summary/summary.json',
    'account': 'results/2026-11-14/summaries/layout-recovery-43575584325-account/summary.json',
    'lazy01': 'results/2026-11-14/summaries/layout-43570556202-lazy01/summary.json',
}
TABLE_IDS = tuple(str(i) for i in range(1, 14)) + ('A1',)
FIGURE_IDS = ('1', '2', '3', '4')
CAPTION = re.compile(r'^\*\*(Table|Figure)\s+(A?\d+)\.', re.M)


def clean(value):
    return ' '.join(value.replace('**', '').replace('`', '').split())


def read_json(root, relative):
    return json.loads((root / relative).read_text(encoding='utf-8'))


def unique(rows, **identity):
    matches = [row for row in rows if all(row.get(k) == v for k, v in identity.items())]
    if len(matches) != 1:
        raise ValueError('Missing or duplicate evidence row: ' + str(identity))
    return matches[0]


def statistic(row, n=None, signed=False):
    observed_n = row.get('n', row.get('measured_n'))
    if type(observed_n) is not int or observed_n < 0 or (n is not None and observed_n != n):
        raise ValueError('Unexpected statistic denominator')
    mean, sd = row['mean'], row['sample_sd']
    if observed_n == 0 and mean is None and sd is None:
        return 'Not observed'
    if (observed_n < 2 or type(mean) not in (int, float) or type(sd) not in (int, float)
            or not math.isfinite(mean) or not math.isfinite(sd) or sd < 0):
        raise ValueError('Invalid mean or sample standard deviation')
    return ('{:+.3f}' if signed else '{:.3f}').format(mean) + ' ± {:.3f}'.format(sd)


def load_evidence(root):
    """Build explicit table bindings; this never rewrites a summary or archive."""
    root = Path(root).resolve()
    revision = revision_date(root)
    sources = {key: read_json(root, path) for key, path in SUMMARIES.items()}
    expected_batches = {
        'primary': 'comparison-42381922637', 'original': 'comparison-42380929383',
        'followup': 'comparison-42384122902', 'member': '1240001156-account-20261108T122201Z',
        'account': 'layout-recovery-43575584325', 'lazy01': 'layout-43570556202',
    }
    for key, summary in sources.items():
        if (summary.get('integrity_ok') is not True or summary.get('integrity_errors')
                or summary.get('upstream_pin') != PIN or summary.get('batch') != expected_batches[key]):
            raise ValueError('Unverified or wrong-scope summary: ' + SUMMARIES[key])
        for row in summary['groups']:
            host = summary['provenance'][row['case']]['host_scope']
            if host != expected_batches[key] + '/' + row['case']:
                raise ValueError('Unexpected case/host scope in ' + key)
            if 'host_scope' in row and row['host_scope'] != host:
                raise ValueError('Group and provenance scopes disagree in ' + key)

    tables = {}

    def bind(number, headers, rows, evidence, numeric_columns, columns=None):
        tables[str(number)] = {
            'headers': headers, 'rows': rows, 'sources': evidence,
            'numeric_columns': numeric_columns,
            'checked_columns': columns if columns is not None else list(range(len(headers))),
        }

    def group(key, case, method, n):
        row = unique(sources[key]['groups'], case=case, method=method)
        if row['eligible_n'] != n or row['complete_n'] != n:
            raise ValueError('Report requires a distinct complete sample: ' + str((key, case, method)))
        return row

    primary_n = sources['primary']['design']['repetitions_per_method']
    followup_n = sources['followup']['design']['repetitions_per_method']
    member_n = sources['member']['design']['repetitions_per_method']
    if (primary_n, followup_n, member_n) != (10, 3, 10):
        raise ValueError('Registered report sample scopes changed; review bindings explicitly')

    headers = ['Case', 'Metric', 'Paper', 'Ours', 'Delta', 'Relative delta']
    for number, method in ((2, 'period'), (3, SERIAL)):
        rows = []
        for case in CASES:
            key = 'followup' if number == 3 and case == 'reorder_4' else 'primary'
            n = followup_n if key == 'followup' else primary_n
            row = group(key, case, method, n)
            for label, metric in METRICS:
                value = row[metric]
                reference = row['paper_table_2_gaps'][metric]['reference']
                delta = value['mean'] - reference
                rows.append([case, label, str(reference), statistic(value, n),
                             '{:+.3f}'.format(delta), '{:+.2f}%'.format(100 * delta / reference)])
        bind(number, headers, rows,
             [SUMMARIES['primary']] + ([SUMMARIES['followup']] if number == 3 else []), [2, 3, 4, 5])

    reduction, timings = [], []
    for case in CASES:
        key, n = ('followup', followup_n) if case == 'reorder_4' else ('primary', primary_n)
        period, serial = (group(key, case, method, n) for method in ('period', SERIAL))
        paired = unique(sources[key]['paired_comparisons'], case=case, serial_method=SERIAL)
        if paired['n_complete_pairs'] != n or paired['host_scope'] != expected_batches[key] + '/' + case:
            raise ValueError('Unexpected matched-pair scope for ' + case)
        counts = [row['schedules'] for row in (period, serial)]
        if any(row['n'] != n or row['sample_sd'] != 0 for row in counts):
            raise ValueError('Table 4 requires the recorded constant schedule totals')
        reduction.append([case, '{:g}'.format(counts[0]['mean']), '{:g}'.format(counts[1]['mean']),
                          '{:.2f}%'.format(100 * (counts[1]['mean'] - counts[0]['mean']) / counts[1]['mean'])])
        timings.append([case, statistic(period['elapsed_seconds'], n), statistic(serial['elapsed_seconds'], n),
                        statistic(paired['serial_minus_period_seconds'], n)])
    pair_sources = [SUMMARIES['primary'], SUMMARIES['followup']]
    bind(4, ['Case', 'PERIOD schedules', 'Serialized ABI16 schedules', 'Reduction'], reduction, pair_sources, [1, 2, 3])
    bind(5, ['Case', 'PERIOD seconds', 'Serialized ABI16 seconds', 'Paired time difference (Serial - PERIOD)'],
         timings, pair_sources, [1, 2, 3])

    # The existing independent historical auditor recounts logs and checks the
    # archived CSVs. Do not trust a copied depth/replay table as a new input.
    historical = audit_historical(root)
    replay = historical['replays']['reorder_3_bad']
    replay_rows = [['Original follow-up', '{}/{} expected assertions'.format(replay['signature_hits'], replay['trials']), 'Not run', '']]
    for key in ('original', 'primary'):
        diagnostic = unique(sources[key]['diagnostics'], case='reorder_3')
        cells = [expected_batches[key].split('-')[-1]]
        for condition, scale in (('default', 1.5), ('expanded', 6.0)):
            item = unique(diagnostic['conditions'], condition=condition)
            trials = [t for t in sources[key]['trials'] if t['phase'] == 'diagnostic' and t['condition'] == condition]
            if not trials or any(t['case'] != 'reorder_3' or t['scale'] != scale for t in trials):
                raise ValueError('Replay multiplier or case scope differs')
            hits = item['confirmed_assertion']
            target_codes = item['target_returncodes']
            if len(target_codes) != 1 or sum(target_codes.values()) != hits['n']:
                raise ValueError('Replay target codes are not uniform as reported')
            cells.append('{}/{}; target {}'.format(hits['successes'], hits['n'], next(iter(target_codes))))
        replay_rows.append(cells + [''])
    bind(6, ['Batch', 'Multiplier 1.5', 'Multiplier 6.0', 'Interpretation'], replay_rows,
         ['results/2026-11-07/followup/followup.json', SUMMARIES['original'], SUMMARIES['primary']], [1, 2], [0, 1, 2])

    depth_rows = []
    for depth in (1, 2, 3):
        metrics = {r['metric']: r for r in historical['summaries']
                   if r['batch'] == 'followup' and r['case'] == 'reorder_3_bad' and r['depth'] == depth}
        first = metrics['first_error_schedule']
        n = metrics['observed_schedule_count']['measured_n']
        if n != 3 or first['measured_n'] + first['missing_n'] != n:
            raise ValueError('Depth sample coverage differs')
        depth_rows.append([str(depth), statistic(metrics['observed_schedule_count'], n),
                           statistic(metrics['reported_buggy_schedules'], n),
                           '{}/{}'.format(first['measured_n'], n), statistic(first),
                           statistic(metrics['elapsed_seconds'], n)])
    bind(7, ['Bound', 'Explored schedules', 'Buggy schedules', 'Runs detecting failure',
             'First failing schedule', 'Whole-driver seconds'], depth_rows,
         ['results/2026-11-07/followup/followup.json', 'results/2026-11-07/extension_summary.csv'], [0, 1, 2, 3, 4, 5])

    member_rows = []
    for method, label in (('period', 'PERIOD'), (SERIAL, SERIAL)):
        row = group('member', 'account', method, member_n)
        member_rows.append([label] + [statistic(row[m], member_n) for m in
                                     ('first_error', 'schedules', 'buggy_schedules', 'elapsed_seconds')])
    bind(8, ['Method', 'First failing schedule', 'Explored schedules', 'Buggy schedules', 'Whole-driver seconds'],
         member_rows, [SUMMARIES['member']], [1, 2, 3, 4])

    layout_paths = {'account': 'results/2026-11-14/layout-recovery-43575584325/account',
                    'lazy01': 'results/2026-11-14/layout-43570556202/lazy01'}
    offsets = []
    for case in ('account', 'lazy01'):
        native = read_json(root, layout_paths[case] + '/runtime_layout.json')['observed_layout']['offsets']
        decoder = read_json(root, layout_paths[case] + '/synthetic_decode_probe.json')['conditions']
        offsets.append([[field, '{:,}'.format(native[field.split(',')[0]]),
                         '{:,}'.format(decoder['capacity1990']['offsets'][field.split(',')[0]]),
                         '{:,}'.format(decoder['capacity3964']['offsets'][field.split(',')[0]])]
                        for field in ('kp, scheduling/yield array', 'kpLoc, key-point location array', 'kpOrder, key-point order array')])
    if offsets[0] != offsets[1]:
        raise ValueError('Native/decoder offsets differ between the separately archived cases')
    bind(9, ['Field', 'Native runtime', 'Released capacity1990', 'Corrected capacity3964'], offsets[0],
         [p + '/' + name for p in layout_paths.values() for name in ('runtime_layout.json', 'synthetic_decode_probe.json')], [1, 2, 3])

    missing_path = 'experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json'
    missing = read_json(root, missing_path)
    planned = re.search(r'Original planned invocations=(\d+)', missing['note'])
    if (not planned or missing['original_run_id'] != '43570556202'
            or missing['account_artifact_readable'] is not False or missing['account_job_log_readable'] is not False):
        raise ValueError('Original account evidence availability changed; review unknown-denominator scope')
    denominator_rows = [['Original account, run 43570556202', planned[1], 'Unknown', 'Unknown', 'Unknown', 'Unknown']]
    for case, label in (('lazy01', 'Original lazy01, run 43570556202'), ('account', 'Recovery account, run 43575584325')):
        d = sources[case]['denominators']
        denominator_rows.append([label] + [str(d[k]) for k in ('planned_workload_attempts', 'workload_attempts',
                                                            'workload_complete', 'workload_eligible', 'complete_pairs')])
    bind(10, ['Scope', 'Planned', 'Recorded', 'Complete', 'Eligible', 'Complete pairs'], denominator_rows,
         [missing_path, SUMMARIES['lazy01'], SUMMARIES['account']], [1, 2, 3, 4, 5])

    condition_rows, change_rows = [], []
    for case in ('account', 'lazy01'):
        n = sources[case]['design']['repetitions_per_condition']
        if n != 10 or sources[case]['design']['cases'] != [case]:
            raise ValueError('Controlled capacity case/sample scope differs')
        for condition, label in (('capacity1990', 'A'), ('capacity3964', 'B')):
            row = unique(sources[case]['groups'], case=case, condition=condition)
            if row['eligible_n'] != n:
                raise ValueError('Incomplete capacity condition requires explicit report revision')
            condition_rows.append([case + ' / ' + label, str(n)] +
                                  [statistic(row[m], n) for m in ('first_error', 'schedules', 'buggy_schedules', 'elapsed_seconds')])
        paired = unique(sources[case]['paired_comparisons'], case=case)
        if (paired['n_complete_pairs'] != n or paired['delta_orientation'] != 'capacity3964 minus capacity1990'
                or paired['host_scope'] != expected_batches[case] + '/' + case):
            raise ValueError('Capacity paired orientation or host scope differs')
        change_rows.append([case + ' / ' + str(n)] + [statistic(paired[m + '_delta'], n, signed=True)
                                                    for m in ('first_error', 'schedules', 'buggy_schedules', 'elapsed_seconds')])
    layout_sources = [SUMMARIES['account'], SUMMARIES['lazy01']]
    bind(11, ['Case / condition', 'n', 'First failing schedule', 'Explored schedules', 'Buggy schedules', 'Whole-driver seconds'],
         condition_rows, layout_sources, [1, 2, 3, 4, 5])
    bind(12, ['Case / pairs', 'First-failure delta', 'Schedule-count delta', 'Buggy-count delta', 'Elapsed-second delta'],
         change_rows, layout_sources, [0, 1, 2, 3, 4])
    return {'tables': tables, 'root': root, 'revision_date': revision.isoformat(),
            'revision_marker': 'Stage report revised {} {} {}.'.format(
                revision.day, month_name[revision.month], revision.year)}


def narrative_references(text):
    """Count prose callouts, including ranges; captions and tables do not count."""
    body = text.split('## References', 1)[0]
    prose = '\n'.join(line for line in body.splitlines()
                      if not CAPTION.match(line) and not line.lstrip().startswith(('|', '![', '#')))
    result = {'Table': set(), 'Figure': set()}
    pattern = r'\b(Table|Figure)s?\s+(A?\d+(?:\s*(?:[-–]|,|and)\s*A?\d+)*)'
    for match in re.finditer(pattern, prose):
        expression = match[2]
        for token in re.findall(r'A?\d+', expression):
            result[match[1]].add(token)
        for a, b in re.findall(r'(?<![A\d])(\d+)\s*[-–]\s*(\d+)', expression):
            if int(b) >= int(a):
                result[match[1]].update(str(n) for n in range(int(a), int(b) + 1))
    return result


def audit_text(text, evidence):
    errors, coverage, tables, captions = [], [], {}, {}
    paragraphs = text.split('\n\n')
    if len(paragraphs) < 2 or evidence['revision_marker'] not in paragraphs[1]:
        errors.append('Report header does not match report/REVISION_DATE')
    matches = list(CAPTION.finditer(text))
    counts = Counter((m[1], m[2]) for m in matches)
    required = {('Table', n) for n in TABLE_IDS} | {('Figure', n) for n in FIGURE_IDS}
    for kind, number in sorted(required | set(counts)):
        count = counts[(kind, number)]
        if (kind, number) not in required or count != 1:
            errors.append('{} {}: expected one registered caption, found {}'.format(kind, number, count))
    refs = narrative_references(text)
    for kind, number in sorted(required):
        if number not in refs[kind]:
            errors.append('{} {}: missing narrative reference outside captions/tables'.format(kind, number))
    for match in matches:
        lines = text[match.start():].splitlines()
        captions[(match[1], match[2])] = clean(lines[0])
        if match[1] == 'Figure':
            before = text[:match.start()].rstrip().splitlines()
            image = re.fullmatch(r'!\[[^\]]*\]\(([^)]+)\)', before[-1] if before else '')
            if not image:
                errors.append('Figure {}: missing associated image'.format(match[2]))
            else:
                root = evidence['root']
                path = (root / 'report' / image[1]).resolve()
                if root not in path.parents or not path.is_file():
                    errors.append('Figure {}: missing or external image target'.format(match[2]))
            continue
        rows = []
        for line in lines[1:]:
            if not line.strip() and not rows:
                continue
            if not line.strip().startswith('|'):
                break
            cells = [clean(c) for c in line.strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                rows.append(cells)
        if not rows or len({len(r) for r in rows}) != 1:
            errors.append('Table {}: missing or malformed table'.format(match[2]))
        else:
            tables[match[2]] = rows

    for number, expected in evidence['tables'].items():
        rows = tables.get(number)
        if rows is None:
            continue
        if rows[0] != expected['headers']:
            errors.append('Table {}: header/metric/difference orientation differs'.format(number))
        if len(rows) - 1 != len(expected['rows']):
            errors.append('Table {}: expected {} evidence rows, found {}'.format(number, len(expected['rows']), len(rows) - 1))
        checked = numeric = 0
        for row_no, (observed, wanted) in enumerate(zip(rows[1:], expected['rows']), 1):
            for column in expected['checked_columns']:
                if column >= len(observed):
                    continue
                checked += 1
                if column in expected['numeric_columns']:
                    numeric += 1
                if observed[column] != clean(wanted[column]):
                    errors.append('Table {}, row {}, {}: {!r}; evidence requires {!r}'.format(
                        number, row_no, expected['headers'][column], observed[column], wanted[column]))
        coverage.append({'table': number, 'rows': len(expected['rows']), 'checked_cells': checked,
                         'quantitative_or_missingness_cells': numeric, 'sources': expected['sources']})

    # Sample sizes in prose captions are part of the table contract, as are the
    # reference batch and the signs of paired effects. These checks are narrow
    # statements about the maintained table definitions, not a semantic review.
    contracts = {
        '2': [r'n\s*=\s*10 per case'],
        '3': [r'n\s*=\s*10 except reorder_4, n\s*=\s*3 from follow-up 42384122902'],
        '4': [r'n\s*=\s*10 paired repetitions for four cases and n\s*=\s*3 for reorder_4 from follow-up 42384122902',
              r'\(Serial - PERIOD\) / Serial'],
        '5': [r'ten matched pairs for four cases and three for reorder_4 from the separate follow-up'],
        '7': [r'n\s*=\s*3\b'],
        '8': [r'n\s*=\s*10 per method'],
        '11': [r'A denotes released capacity1990; B denotes corrected capacity3964'],
        '12': [r'B minus A', r'ten complete pairs on its own case host'],
    }
    for number, patterns in contracts.items():
        caption = captions.get(('Table', number), '')
        for pattern in patterns:
            if not re.search(pattern, caption):
                errors.append('Table {}: missing or changed sample/batch/orientation declaration ({})'.format(number, pattern))
    if 'Signed delta is our mean minus the paper value' not in clean(text):
        errors.append('Tables 2–3: signed paper-gap orientation is missing or changed')
    return {
        'integrity_ok': not errors,
        'errors': errors,
        'revision_date': evidence['revision_date'],
        'quantitative_tables': [row['table'] for row in coverage],
        'checked_cells': sum(row['checked_cells'] for row in coverage),
        'quantitative_or_missingness_cells': sum(row['quantitative_or_missingness_cells'] for row in coverage),
        'caption_count': len(matches),
        'coverage': coverage,
        'scope': 'Tables 2–12, registered sample/batch/difference definitions, captions, narrative callouts, figure paths and report revision date. Underlying evidence audits run separately; original-paper accuracy, all prose, SVG plotting contents and final visual layout require their own review.',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--source', type=Path, help='Alternate report source for a read-only check')
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        source = args.source or root / 'report/EXPANDED_REPORT.md'
        result = audit_text(source.read_text(encoding='utf-8'), load_evidence(root))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('FAIL: report evidence check: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0 if result['integrity_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
