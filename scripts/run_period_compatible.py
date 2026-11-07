#!/usr/bin/env python3
"""Backport the current 16-bit IPC ABI into the authors' serialized driver.
Scheduling enumeration, depth rules and calibration logic remain unmodified.
"""
import ctypes
import difflib
import hashlib
import json
from pathlib import Path
import sys
import run_period_comparison as study


def adapt_serial(old, current):
    start = 'def setup_share_memroy():'
    stop = 'def create_DBDS_subprocess(check_STDOUT, check_STDERR):'
    for text in (old, current):
        if text.count(start) != 1 or text.count(stop) != 1:
            raise ValueError('Pinned IPC block changed')
    a, b = old.index(start), old.index(stop)
    x, y = current.index(start), current.index(stop)
    result = old[:a] + current[x:y] + old[b:]
    for name, size in [('kpNumArray', 'SHARE_THREAD_NUM'), ('kpYieldArray', 'SHARE_ARRAY_SIZE'),
                       ('kpLocArray', 'SHARE_ARRAY_SIZE'), ('kpOrderArray', 'SHARE_ARRAY_SIZE')]:
        source = name + ' = (c_uint*' + size + ')(0)'
        if result.count(source) != 1:
            raise ValueError('Pinned array initializer changed: ' + name)
        result = result.replace(source, name + ' = (c_uint16*' + size + ')(0)')
    marker = 'period_limit = bugDepth + N - 1'
    if old.count(marker) != 1 or result[result.index(marker):] != old[old.index(marker):]:
        raise ValueError('Enumeration changed unexpectedly')
    return result


def probe_existing_segment():
    libc = ctypes.CDLL(None, use_errno=True)
    libc.shmget.argtypes = [ctypes.c_int, ctypes.c_size_t, ctypes.c_int]
    libc.shmget.restype = ctypes.c_int
    libc.shmat.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    libc.shmat.restype = ctypes.c_void_p
    sizes = {'current_16bit': 8 + 4*3 + 2*(100+3*1990),
             'old_32bit': 8 + 4*(3+100+3*1990)}
    result = {'scope': 'Read-only requests against the actual runtime key 1111; no memmove on a failed address'}
    for label, size in sizes.items():
        ctypes.set_errno(0)
        identifier = libc.shmget(1111, size, 0)
        result[label] = {'requested_bytes': size, 'shmget_return': identifier, 'errno': ctypes.get_errno()}
    if result['old_32bit']['shmget_return'] == -1:
        ctypes.set_errno(0)
        ptr = libc.shmat(-1, None, 0)
        result['invalid_attach'] = {'failed_sentinel': ptr == ctypes.c_void_p(-1).value,
                                    'errno': ctypes.get_errno()}
    return result


def main():
    def option(flag, default):
        return Path(sys.argv[sys.argv.index(flag)+1]) if flag in sys.argv else Path(default)
    root, out = option('--root','/workdir/PERIOD'), option('--output','/evidence')
    out.mkdir(parents=True, exist_ok=True)
    if (out/'records.json').exists(): raise ValueError('Existing measurements')
    old_path, new_path = root/'tool/DBDS/run_OldPDS.py', root/'tool/DBDS/run_PDS.py'
    old, current = old_path.read_text(encoding='utf-8'), new_path.read_text(encoding='utf-8')
    adapted = adapt_serial(old, current)
    target = root/'tool/DBDS/run_OldPDS_abi16.py'; target.write_text(adapted,encoding='utf-8')
    patch = ''.join(difflib.unified_diff(old.splitlines(True), adapted.splitlines(True),
                     fromfile='upstream/run_OldPDS.py', tofile='adapted/run_OldPDS_abi16.py'))
    (out/'serial_abi16.diff').write_text(patch,encoding='utf-8')
    (out/'serial_abi16.json').write_text(json.dumps({'scope':'IPC block and four array types only; scheduler section byte-identical',
        'original_sha256':hashlib.sha256(old.encode()).hexdigest(),
        'adapted_sha256':hashlib.sha256(adapted.encode()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    study.METHODS = {'period':'run_PDS.py','author_serialized_abi16':'run_OldPDS_abi16.py'}
    code = study.main()
    (out/'ipc_abi_probe.json').write_text(json.dumps(probe_existing_segment(),indent=2)+'\n',encoding='utf-8')
    return code

if __name__=='__main__': raise SystemExit(main())
