#!/usr/bin/env python3
"""Reproduce the driver mapping-size failure on an isolated System V IPC segment.

No benchmark runs and no author runtime key are used. The fresh private segment
is removed after the probe. Layout is from the pinned DBDSFunction.cpp runtime.
"""
import ctypes
import errno
import json
import secrets
import platform
from pathlib import Path


def ipc_probe():
    """Test IPC size failure on a fresh private segment, then remove that segment."""
    class Runtime(ctypes.Structure):
        _fields_ = [('time',ctypes.c_uint64),('N',ctypes.c_uint32),('M',ctypes.c_uint32),
                    ('bounds',ctypes.c_uint32),('counts',ctypes.c_uint16*100),
                    ('kp',ctypes.c_uint16*3964),('loc',ctypes.c_uint16*3964),
                    ('order',ctypes.c_uint16*3964)]
    libc = ctypes.CDLL(None, use_errno=True)
    libc.shmget.argtypes = [ctypes.c_int,ctypes.c_size_t,ctypes.c_int]
    libc.shmget.restype = ctypes.c_int
    libc.shmat.argtypes = [ctypes.c_int,ctypes.c_void_p,ctypes.c_int]
    libc.shmat.restype = ctypes.c_void_p
    libc.shmctl.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_void_p]
    libc.shmctl.restype = ctypes.c_int
    key = secrets.randbelow(0x6fffffff) + 0x10000000
    size, old_size, current_size = ctypes.sizeof(Runtime), 24300, 12160
    ident = libc.shmget(key, size, 0o1000 | 0o2000 | 0o600)
    if ident < 0:
        raise OSError(ctypes.get_errno(), 'Could not create isolated IPC probe')
    try:
        ctypes.set_errno(0)
        bad = libc.shmget(key, old_size, 0o1000 | 0o600)
        bad_errno = ctypes.get_errno()
        ctypes.set_errno(0)
        good = libc.shmget(key, current_size, 0o1000 | 0o600)
        good_errno = ctypes.get_errno()
        ctypes.set_errno(0)
        failed_address = libc.shmat(-1, None, 0)
        attach_errno = ctypes.get_errno()
        result = {'scope':'isolated IPC mechanism probe, not a benchmark repetition',
                  'runtime_struct_bytes':size, 'old_requested_bytes':old_size,
                  'current_requested_bytes':current_size, 'old_return':bad,
                  'old_errno':bad_errno, 'current_request_succeeded':good==ident,
                  'current_errno':good_errno,
                  'invalid_attach_is_minus_one':failed_address==ctypes.c_void_p(-1).value,
                  'invalid_attach_errno':attach_errno,
                  'runtime_offsets':{name:getattr(Runtime,name).offset for name,_ in Runtime._fields_}}
        if bad != -1 or bad_errno != errno.EINVAL or good != ident:
            raise ValueError('IPC mechanism did not match predicted size-error behavior')
        return result
    finally:
        if libc.shmctl(ident, 0, None) != 0:
            raise OSError(ctypes.get_errno(), 'Could not remove own IPC probe segment')



if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    result = ipc_probe()
    result['environment'] = {'platform': platform.platform(), 'python': platform.python_version()}
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        if args.output.exists(): raise SystemExit('Refuse to overwrite an existing probe')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    print(text)
