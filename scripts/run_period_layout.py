#!/usr/bin/env python3
"""Registered one-factor shared-memory layout study; Python 3.6 compatible.

The benchmark and runtime are unchanged. Only the PERIOD Python driver's
SHARE_ARRAY_SIZE constant differs between the two experimental conditions.
"""
import argparse
import ctypes
import difflib
import errno
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import struct
import sys
import time

from run_period_comparison import parse_log, new_output_folders
from run_period_pilot import execute, utc

PIN = 'cb8deb9a176e5bb292d70d46557dd61dc0e98069'
CASES = {'account': 'account_bad', 'lazy01': 'lazy01_bad'}
CONDITIONS = {'capacity1990': 'run_PDS.py', 'capacity3964': 'run_PDS_layout3964.py'}
FIELDS = ('time', 'N', 'M', 'TestedBounds', 'kpNumArray', 'kp', 'kpLoc', 'kpOrder')
EXPECTED_OFFSETS = dict(zip(FIELDS, (0, 8, 12, 16, 20, 220, 8148, 16076)))
DEADLINE_PROBE = '''import ctypes,json,os
class Attr(ctypes.Structure):
 _fields_=[('size',ctypes.c_uint32),('policy',ctypes.c_uint32),('flags',ctypes.c_uint64),('nice',ctypes.c_int32),('priority',ctypes.c_uint32),('runtime',ctypes.c_uint64),('deadline',ctypes.c_uint64),('period',ctypes.c_uint64)]
a=Attr();a.size=ctypes.sizeof(a);a.policy=6;a.runtime=1000000;a.deadline=10000000;a.period=10000000
libc=ctypes.CDLL(None,use_errno=True);r=libc.syscall(314,0,ctypes.byref(a),0)
print(json.dumps({'sched_setattr_return':r,'errno':ctypes.get_errno(),'observed_policy':os.sched_getscheduler(0)}))
raise SystemExit(0 if r==0 and os.sched_getscheduler(0)==6 else 1)
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def adapt_capacity(original):
    """Preserve every byte other than the single declared decimal constant."""
    anchor = 'SHARE_ARRAY_SIZE = 1990'
    if original.count(anchor) != 1 or not re.search(r'(?m)^' + anchor + r'\r?$', original):
        raise ValueError('Pinned capacity declaration changed')
    amended = original.replace(anchor, 'SHARE_ARRAY_SIZE = 3964', 1)
    if amended.replace('SHARE_ARRAY_SIZE = 3964', anchor, 1) != original:
        raise ValueError('Unexpected changes outside capacity declaration')
    return amended


def condition_order(repetition):
    return ['capacity1990', 'capacity3964'] if repetition % 2 else ['capacity3964', 'capacity1990']


def make_layout_probe(runtime):
    """Compile the pinned runtime's actual declarations, without its execution code."""
    declarations = []
    for name, value in [('SHARE_MEMORY_THREAD_NUM', 100), ('SHARE_MEMORY_ARRAY_SIZE', 3964)]:
        matches = re.findall(r'(?m)^#define\s+' + name + r'\s+([0-9]+)\s*$', runtime)
        if matches != [str(value)]:
            raise ValueError('Unexpected runtime declaration: ' + name)
        declarations.append('#define {} {}'.format(name, value))
    structs = re.findall(r'typedef struct Sched_Info\s*\{.*?\}\s*sched_info;', runtime, re.S)
    if len(structs) != 1:
        raise ValueError('Pinned runtime structure changed')
    pairs = ','.join('\\"{}\\":%zu'.format(field) for field in FIELDS)
    arguments = ','.join('offsetof(sched_info,{})'.format(field) for field in FIELDS)
    return ('#include <stdint.h>\n#include <stddef.h>\n#include <stdio.h>\n' +
            '\n'.join(declarations) + '\n' + structs[0] + '\n' +
            'int main(){printf("{\\"sizeof\\":%zu,\\"offsets\\":{' + pairs +
            '}}\\n",sizeof(sched_info),' + arguments + ');return 0;}\n')


def synthetic_decode_probe(layout):
    """A labelled synthetic byte-array check, never a benchmark observation."""
    if layout.get('sizeof') != 24008 or layout.get('offsets') != EXPECTED_OFFSETS:
        raise ValueError('Actual compiled runtime layout differs from registered x86-64 layout')
    memory = bytearray(layout['sizeof'])
    for field, value in [('kp', 101), ('kpLoc', 202), ('kpOrder', 303)]:
        for index in range(3964):
            struct.pack_into('=H', memory, layout['offsets'][field] + 2 * index, value)
    result = {'scope': 'Synthetic sentinel bytes using the compiled runtime offsets; no workload execution',
              'expected_location_value': 202, 'expected_order_value': 303, 'conditions': {}}
    for capacity in (1990, 3964):
        offsets = {'kp': 220, 'kpLoc': 220 + 2 * capacity, 'kpOrder': 220 + 4 * capacity}
        result['conditions']['capacity' + str(capacity)] = {
            'offsets': offsets,
            'decoded_location': struct.unpack_from('=H', memory, offsets['kpLoc'])[0],
            'decoded_order': struct.unpack_from('=H', memory, offsets['kpOrder'])[0]}
    return result


def live_targets(binary):
    """Find only this built executable in the container's private PID namespace."""
    expected = str(binary.resolve())
    found = []
    for item in Path('/proc').iterdir():
        if not item.name.isdigit():
            continue
        try:
            actual = os.readlink(str(item / 'exe'))
            status = (item / 'status').read_text(encoding='utf-8')
            if actual == expected and not re.search(r'(?m)^State:\s+Z', status):
                found.append(int(item.name))
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
    return sorted(found)


def reset_trial_state(binary):
    """Remove only this target's residual processes and fixed key in private IPC."""
    killed = live_targets(binary)
    for pid in killed:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    for _ in range(20):
        if not live_targets(binary):
            break
        time.sleep(0.05)
    if live_targets(binary):
        raise RuntimeError('Target processes survive cleanup; stop to avoid contamination')
    libc = ctypes.CDLL(None, use_errno=True)
    libc.shmget.argtypes = [ctypes.c_int, ctypes.c_size_t, ctypes.c_int]
    libc.shmget.restype = ctypes.c_int
    libc.shmctl.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    libc.shmctl.restype = ctypes.c_int
    ctypes.set_errno(0)
    identifier = libc.shmget(1111, 1, 0)
    previous_errno = ctypes.get_errno()
    row = None
    rows = Path('/proc/sysvipc/shm').read_text(encoding='utf-8').splitlines()
    if rows:
        header = rows[0].split()
        for text in rows[1:]:
            candidate = dict(zip(header, text.split()))
            if int(candidate['shmid']) == identifier:
                row = candidate
    if identifier >= 0:
        if row is None or int(row['nattch']) != 0:
            raise RuntimeError('Shared segment still attached; stop to avoid unsafe reset')
        ctypes.set_errno(0)
        if libc.shmctl(identifier, 0, None) != 0:  # IPC_RMID
            raise OSError(ctypes.get_errno(), 'Shared segment cleanup failed')
    elif previous_errno != errno.ENOENT:
        raise OSError(previous_errno, 'Cannot inspect trial shared memory')
    ctypes.set_errno(0)
    after = libc.shmget(1111, 1, 0)
    after_errno = ctypes.get_errno()
    if after != -1 or after_errno != errno.ENOENT:
        raise RuntimeError('Shared-memory key is not absent after cleanup')
    return {'scope': 'Container-private IPC/PID namespaces; key 1111 and this built binary only',
            'killed_target_pids': killed, 'previous_shmid': identifier,
            'previous_errno': previous_errno, 'previous_segment': row,
            'key_absent': True, 'post_shmget': after, 'post_errno': after_errno}


def write_manifest(out):
    ignored = {'manifest.json', 'container_console.txt', 'container_exit_code.txt', 'wrapper_exit_code.txt'}
    files = []
    for path in sorted(out.rglob('*')):
        if path.is_file() and path.name not in ignored:
            files.append({'path': path.relative_to(out).as_posix(),
                          'bytes': path.stat().st_size, 'sha256': digest(path)})
    write_json(out / 'manifest.json', {'created_utc': utc(), 'files': files})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('/workdir/PERIOD'))
    parser.add_argument('--output', type=Path, default=Path('/evidence'))
    parser.add_argument('--case', required=True, choices=sorted(CASES))
    parser.add_argument('--repetitions', type=int, default=10)
    parser.add_argument('--comparison-timeout', type=int, default=120)
    args = parser.parse_args()
    if args.repetitions < 1 or args.comparison_timeout < 1:
        parser.error('Positive repetitions and timeout required')
    if os.environ.get('CS340_PRIVATE_STUDY_CONTAINER') != '1':
        parser.error('Use the private-namespace disposable-container wrapper')
    root, out = args.root, args.output
    out.mkdir(parents=True, exist_ok=True)
    if (out / 'records.json').exists():
        raise ValueError('Refuse to overwrite a measured batch')
    records = []
    directory = root / 'evaluation/CS' / args.case
    binary = directory / CASES[args.case]

    def save():
        write_json(out / 'records.json', records)

    def run(command, name, phase, timeout, cwd=None, **metadata):
        record = execute(command, cwd or directory, out / name, timeout)
        record.update(phase=phase, case=args.case, **metadata)
        records.append(record)
        save()
        return record

    environment = {'captured_utc': utc(), 'source_commit': PIN,
                   'platform': platform.platform(), 'python': platform.python_version(),
                   'cpu_affinity': sorted(os.sched_getaffinity(0)),
                   'cpu_models': sorted(set(line.split(':', 1)[1].strip() for line in
                                           Path('/proc/cpuinfo').read_text(encoding='utf-8').splitlines()
                                           if line.startswith('model name'))),
                   'os_release': Path('/etc/os-release').read_text(encoding='utf-8'),
                   'same_built_binary': True, 'private_ipc_and_pid_requested_by_wrapper': True,
                   'settings': {'depth': 3, 'schedule_budget': 10000,
                                'repetitions_per_condition': args.repetitions,
                                'outer_timeout_seconds': args.comparison_timeout,
                                'only_driver_change': 'SHARE_ARRAY_SIZE = 1990 to 3964'}}
    write_json(out / 'environment.json', environment)
    write_json(out / 'planned_trials.json', [
        {'case': args.case, 'repeat': repetition, 'position': position,
         'condition': condition, 'phase': 'layout'}
        for repetition in range(1, args.repetitions + 1)
        for position, condition in enumerate(condition_order(repetition), 1)])
    save()
    try:
        source = out / 'source'
        source.mkdir()
        original_path = root / 'tool/DBDS/run_PDS.py'
        original = original_path.read_bytes().decode('utf-8')
        adapted = adapt_capacity(original)
        amended_path = root / 'tool/DBDS' / CONDITIONS['capacity3964']
        amended_path.write_bytes(adapted.encode('utf-8'))
        for path in (root / 'tool/DBDS').glob('*.py'):
            shutil.copyfile(str(path), str(source / path.name))
        shutil.copyfile(str(root / 'LICENSE'), str(source / 'LICENSE.txt'))
        runtime_path = root / 'tool/staticAnalysis/DBDS-INSTRU/llvm-mode/DBDSFunction.cpp'
        shutil.copyfile(str(runtime_path), str(source / 'DBDSFunction.cpp'))
        patch = ''.join(difflib.unified_diff(original.splitlines(True), adapted.splitlines(True),
                                            fromfile='upstream/run_PDS.py', tofile='adapted/run_PDS_layout3964.py'))
        (out / 'capacity.diff').write_bytes(patch.encode('utf-8'))
        write_json(out / 'capacity_change.json', {'original_sha256': digest(original_path),
                   'adapted_sha256': digest(amended_path), 'runtime_sha256': digest(runtime_path),
                   'only_changed_declaration': 'SHARE_ARRAY_SIZE = 1990 -> SHARE_ARRAY_SIZE = 3964'})
        probe_source = source / 'runtime_layout_probe.cpp'
        probe_source.write_text(make_layout_probe(runtime_path.read_text(encoding='utf-8')), encoding='utf-8')
        probe_binary = root / 'cs340_runtime_layout_probe'
        compile_record = run(['g++', '-std=c++11', str(probe_source), '-o', str(probe_binary)],
                             'layout_probe_build.txt', 'layout_probe_build', 30, cwd=root)
        if compile_record['exit_code'] != 0:
            return 2
        probe_record = run([str(probe_binary)], 'layout_probe.txt', 'layout_probe', 10, cwd=root)
        if probe_record['exit_code'] != 0:
            return 2
        raw = (out / 'layout_probe.txt').read_text(encoding='utf-8')
        rows = [json.loads(line) for line in raw.splitlines() if line.startswith('{')]
        if len(rows) != 1:
            raise ValueError('One compiled layout observation required')
        layout = rows[0]
        write_json(out / 'runtime_layout.json', {'scope': 'Native sizeof/offsetof compiled from actual pinned runtime declaration',
                   'runtime_source_sha256': digest(runtime_path), 'probe_source_sha256': digest(probe_source),
                   'observed_layout': layout})
        write_json(out / 'synthetic_decode_probe.json', synthetic_decode_probe(layout))
        deadline = run([sys.executable, '-c', DEADLINE_PROBE], 'deadline_probe.txt', 'deadline_probe', 10, cwd=root)
        if deadline['exit_code'] != 0:
            return 2
        build = run(['bash', 'build.sh'], 'build.txt', 'build', 180)
        if build['exit_code'] != 0 or not binary.is_file():
            return 2
        binary_hash = digest(binary)
        environment['binary_sha256'] = binary_hash
        environment['drivers'] = {condition: digest(root / 'tool/DBDS' / name)
                                  for condition, name in CONDITIONS.items()}
        for path in directory.iterdir():
            if path.is_file() and (path.suffix in ('.c', '.cpp', '.sh') or path.name.startswith('ConConfig.')):
                shutil.copyfile(str(path), str(source / path.name))
        write_json(out / 'environment.json', environment)
        for repetition in range(1, args.repetitions + 1):
            for position, condition in enumerate(condition_order(repetition), 1):
                if digest(binary) != binary_hash:
                    raise ValueError('Benchmark binary changed during comparison')
                reset = reset_trial_state(binary)
                reset_name = '{}_r{:02d}_reset.json'.format(condition, repetition)
                write_json(out / reset_name, reset)
                previous_names = {path.name for path in directory.glob('out_' + binary.name + '_*')}
                command = [sys.executable, str(root / 'tool/DBDS' / CONDITIONS[condition]),
                           '-y', '-d', '3', '-f', '10000', './' + binary.name]
                name = '{}_r{:02d}.txt'.format(condition, repetition)
                record = run(command, name, 'layout', args.comparison_timeout,
                             condition=condition, repeat=repetition, position=position,
                             timeout_seconds=args.comparison_timeout, binary_sha256=binary_hash,
                             reset_log=reset_name, reset_log_sha256=digest(out / reset_name))
                text = (out / name).read_text(encoding='utf-8', errors='replace')
                record.update(parse_log(text))
                record['status'] = ('complete' if not record['timed_out'] and record['exit_code'] == 0
                                    and record['complete_markers'] else 'incomplete')
                record['error_labels'] = re.findall(r'\[Error Found\]:\s*NO\.\d+\s+([^\x1b\r\n]+)', text)
                folders = new_output_folders(directory, binary.name, previous_names)
                record['new_witness_folders'] = [path.name for path in folders]
                witness_count = 0
                for folder in folders:
                    for kind in ('Errors', 'Timeouts'):
                        for path in sorted((folder / kind).glob('*')):
                            if path.is_file() and path.stat().st_size < 100000:
                                target = out / 'witnesses' / condition / ('r%02d' % repetition) / kind / path.name
                                target.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copyfile(str(path), str(target))
                                witness_count += 1
                record['preserved_witness_count'] = witness_count
                record['cleanup_after'] = reset_trial_state(binary)
                save()
        completed = [record for record in records if record.get('phase') == 'layout'
                     and record.get('status') == 'complete']
        print(json.dumps({'case': args.case, 'layout_attempts': args.repetitions * 2,
                          'complete': len(completed)}))
        return 0 if len(completed) == args.repetitions * 2 else 1
    except Exception as error:
        write_json(out / 'study_error.json', {'type': type(error).__name__, 'message': str(error), 'utc': utc()})
        raise
    finally:
        save()
        write_manifest(out)


if __name__ == '__main__':
    raise SystemExit(main())
