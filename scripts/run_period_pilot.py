#!/usr/bin/env python3
"""Run a bounded, sequential PERIOD pilot inside the authors' Linux image.
No scientific result is inferred from a process exit status alone.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import time

PIN = "cb8deb9a176e5bb292d70d46557dd61dc0e98069"
CASES = [("smoke_double_free", "test/doubleFree", "df", 3),
         ("CS.reorder_3_bad", "evaluation/CS/reorder_3", "reorder_3_bad", 3),
         ("CS.reorder_4_bad", "evaluation/CS/reorder_4", "reorder_4_bad", 3)]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def execute(command, cwd, log, timeout):
    start = time.monotonic()
    started = utc()
    timed_out = False
    with log.open("w", encoding="utf-8") as output:
        output.write("Started UTC: " + started + "\nCommand: " + json.dumps(command) + "\n")
        output.flush()
        try:
            process = subprocess.Popen(command, cwd=str(cwd), stdout=output,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(process.pid, signal.SIGKILL)
                code = process.wait()
        except OSError as error:
            output.write("Launch failed: " + str(error) + "\n")
            code = 127
        elapsed = time.monotonic() - start
        output.write("\nRunner exit_code={} timed_out={} elapsed_seconds={:.6f}\n".format(code, timed_out, elapsed))
    return {"started_utc": started, "finished_utc": utc(), "exit_code": code,
            "timed_out": timed_out, "elapsed_seconds": elapsed,
            "command": command, "log": log.name,
            "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest()}


def read_metrics(path):
    text = re.sub(r"\x1b\[[0-9;]*m", "", path.read_text(errors="replace"))
    schedules = [int(x) for x in re.findall(r"(?m)^test\s+(\d+):", text)]
    current = None
    first = None
    errors = 0
    for line in text.splitlines():
        match = re.match(r"^test\s+(\d+):", line)
        if match:
            current = int(match.group(1))
        if "[Error Found]:" in line:
            errors += 1
            if first is None:
                first = current
    return {"observed_schedule_count": len(schedules),
            "last_observed_schedule": max(schedules) if schedules else None,
            "first_error_schedule": first, "reported_buggy_schedules": errors,
            "end_marker": "End Testing!" in text,
            "timeout_reports": len(re.findall(r"\[Timeout\s", text))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("/workdir/PERIOD"))
    parser.add_argument("--output", type=Path, default=Path("/evidence"))
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    env = {"captured_utc": utc(), "platform": platform.platform(),
           "python": platform.python_version(), "upstream_pin": PIN,
           "affinity": sorted(os.sched_getaffinity(0)),
           "proc_status": [line for line in Path("/proc/self/status").read_text().splitlines()
                           if line.startswith(("CapEff:", "Seccomp:", "Cpus_allowed_list:"))],
           "os_release": Path("/etc/os-release").read_text()}
    (out / "container_environment.json").write_text(json.dumps(env, indent=2) + "\n")
    results = []
    for label, relative, binary, depth in CASES:
        directory = args.root / relative
        if not directory.is_dir():
            results.append({"case": label, "phase": "build", "status": "missing_directory"})
            continue
        record = execute(["bash", "build.sh"], directory, out / (binary + "_build.txt"), 180)
        record.update({"case": label, "phase": "build"})
        results.append(record)
        if record["exit_code"] or not (directory / binary).is_file():
            continue
        for repetition in range(1, 4):
            name = "{}_d{}_r{}.txt".format(binary, depth, repetition)
            command = ["python3", str(args.root / "tool/DBDS/run_PDS.py"),
                       "-y", "-d", str(depth), "-f", "10000", "./" + binary]
            record = execute(command, directory, out / name, 90)
            record.update({"case": label, "phase": "run", "depth": depth, "repeat": repetition})
            record.update(read_metrics(out / name))
            record["status"] = "complete" if record["exit_code"] == 0 and record["end_marker"] else "incomplete"
            results.append(record)
            # Preserve all small error witnesses without executables or bitcode.
            for folder in sorted(directory.glob("out_*")):
                for sub in ("Errors", "Timeouts"):
                    for witness in sorted((folder / sub).glob("*")):
                        if witness.is_file() and witness.stat().st_size < 100000:
                            target = out / "witnesses" / binary / folder.name / sub / witness.name
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_bytes(witness.read_bytes())
            (out / "runs.json").write_text(json.dumps(results, indent=2) + "\n")
    (out / "runs.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    complete = [x for x in results if x.get("status") == "complete"]
    return 0 if len(complete) == len(CASES) * 3 else 1


if __name__ == "__main__":
    raise SystemExit(main())
