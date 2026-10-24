#!/usr/bin/env python3
"""Print scoped, non-secret environment information; does not run experiments."""
import datetime
import json
import os
import platform
import shutil
import subprocess


def version(command):
    if not shutil.which(command[0]):
        return {'available': False}
    try:
        p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, timeout=10)
        return {'available': True, 'exit_code': p.returncode,
                'version_output': (p.stdout or p.stderr).strip()[:3000]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'available': True, 'error_type': type(exc).__name__}


result = {
    'captured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'system': platform.system(), 'kernel_release': platform.release(),
    'architecture': platform.machine(), 'logical_cpus': os.cpu_count(),
    'python_version': platform.python_version(),
    'git': version(['git', '--version']),
    'gcc': version(['gcc', '--version']),
    'clang': version(['clang', '--version']),
    'make': version(['make', '--version']),
    'scope': 'Environment inventory only; not a PERIOD experiment or validation.',
    'manual_fields_needed': ['CPU model', 'RAM', 'OS distribution/version',
                             'VM/container details', 'experiment-affecting settings']
}
print(json.dumps(result, ensure_ascii=False, indent=2))
