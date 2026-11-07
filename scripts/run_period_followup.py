#!/usr/bin/env python3
"""Controlled depth sensitivity and replay checks after the initial pilot."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
from run_period_pilot import execute, read_metrics, utc

WITNESSES = {
    'reorder_3_bad': ('evaluation/CS/reorder_3', '[[0, 2], [2, 0], [1, 0]]\n',
                    'witnesses/reorder_3_bad/out_reorder_3_bad_1/Errors/000001_0000006_assertion-failed'),
    'reorder_4_bad': ('evaluation/CS/reorder_4', '[[0, 2], [2, 0], [2, 0], [1, 0]]\n',
                    'witnesses/reorder_4_bad/out_reorder_4_bad_2/Errors/000001_0000009_assertion-failed'),
    'df': ('test/doubleFree', '[[1, 2], [0, 2]]\n',
           'witnesses/df/out_df_1/Errors/000004_0000006_double-free'),
}

PROBE = '''import ctypes,json,os
class Attr(ctypes.Structure):
 _fields_=[('size',ctypes.c_uint32),('policy',ctypes.c_uint32),('flags',ctypes.c_uint64),('nice',ctypes.c_int32),('priority',ctypes.c_uint32),('runtime',ctypes.c_uint64),('deadline',ctypes.c_uint64),('period',ctypes.c_uint64)]
a=Attr();a.size=ctypes.sizeof(a);a.policy=6;a.runtime=1000000;a.deadline=10000000;a.period=10000000
libc=ctypes.CDLL(None,use_errno=True);r=libc.syscall(314,0,ctypes.byref(a),0)
print(json.dumps({'sched_setattr_return':r,'errno':ctypes.get_errno(),'observed_policy':os.sched_getscheduler(0)}))
raise SystemExit(0 if r==0 and os.sched_getscheduler(0)==6 else 1)
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('/workdir/PERIOD'))
    parser.add_argument('--output', type=Path, default=Path('/evidence'))
    args = parser.parse_args()
    root, out = args.root, args.output
    out.mkdir(parents=True, exist_ok=True)
    cpu = [line for line in Path('/proc/cpuinfo').read_text().splitlines()
           if line.startswith('model name')]
    (out / 'environment.json').write_text(json.dumps({
        'captured_utc': utc(), 'platform': platform.platform(),
        'python': platform.python_version(), 'affinity': sorted(os.sched_getaffinity(0)),
        'cpu_model': cpu[0] if cpu else 'unavailable',
        'source_sha': 'cb8deb9a176e5bb292d70d46557dd61dc0e98069'}, indent=2) + '\n')
    records = []
    probe = execute([sys.executable, '-c', PROBE], root, out / 'deadline_probe.txt', 10)
    probe['phase'] = 'deadline_probe'; records.append(probe)
    if probe['exit_code']:
        (out / 'followup.json').write_text(json.dumps(records, indent=2) + '\n')
        return 2
    built = set()
    for binary, (relative, witness, origin) in WITNESSES.items():
        record = execute(['bash', 'build.sh'], root / relative, out / (binary + '_build.txt'), 180)
        record.update({'phase': 'build', 'case': binary}); records.append(record)
        if record['exit_code'] == 0 and (root / relative / binary).is_file():
            built.add(binary)
    # Balanced order chosen before this follow-up; workload and binary unchanged.
    if 'reorder_3_bad' in built:
        directory = root / 'evaluation/CS/reorder_3'
        for repetition, order in enumerate(((1, 2, 3), (3, 1, 2), (2, 3, 1)), 1):
            for depth in order:
                log = out / ('extension_d{}_r{}.txt'.format(depth, repetition))
                record = execute(['python3', str(root / 'tool/DBDS/run_PDS.py'), '-y',
                                  '-d', str(depth), '-f', '10000', './reorder_3_bad'], directory, log, 90)
                record.update(read_metrics(log))
                record.update({'phase': 'extension', 'case': 'reorder_3_bad',
                               'depth': depth, 'repeat': repetition})
                records.append(record)
                (out / 'followup.json').write_text(json.dumps(records, indent=2) + '\n')
    for binary, (relative, witness, origin) in WITNESSES.items():
        if binary not in built:
            continue
        witness_file = out / (binary + '_fixed_witness.txt')
        witness_file.write_text(witness)
        for repetition in range(1, 6):
            log = out / ('replay_{}_r{}.txt'.format(binary, repetition))
            record = execute(['python3', str(root / 'tool/DBDS/run_PDS.py'), '-y',
                              '-r', str(witness_file), './' + binary], root / relative, log, 20)
            text = log.read_text(errors='replace')
            record.update({'phase': 'replay', 'case': binary, 'repeat': repetition,
                           'origin_artifact_id': 13571979839, 'origin_witness_path': origin,
                           'fixed_witness_sha256': hashlib.sha256(witness_file.read_bytes()).hexdigest(),
                           'expected_error_observed': ('AddressSanitizer: attempting double-free' in text)
                             if binary == 'df' else ('Assertion' in text and 'failed' in text)})
            records.append(record)
            (out / 'followup.json').write_text(json.dumps(records, indent=2) + '\n')
    (out / 'followup.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(records, indent=2))
    return 0 if len(built) == 3 and not any(r['timed_out'] for r in records) else 1


if __name__ == '__main__':
    raise SystemExit(main())
