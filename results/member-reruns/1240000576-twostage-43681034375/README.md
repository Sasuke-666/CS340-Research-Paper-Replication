# Replay record for the archived twostage assertion

**Result: five matching assertions in five consecutive attempts.** The runner started the calls at 05:27:04–05:27:07 UTC on 15 November 2026. It used the same archived witness, a fresh process and per-invocation calibration each time. The member requested the run. Execution took place on a disposable GitHub-hosted x86_64 Ubuntu runner. The Windows desktop was used for the fresh clone and archive checks.

| Item | Recorded value |
| --- | --- |
| Team baseline / actual replay setup | `fd0d807f39a9d972dcd4929486d002f53ae4e4f3` / [`62cbb795`](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/commit/62cbb795567a644bf6809227af140d21735eef9d) |
| Upstream | `wcventure/PERIOD@cb8deb9a176e5bb292d70d46557dd61dc0e98069` |
| Container image | `wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc` |
| Host and container | Intel Xeon Platinum 8573C, CPU affinity 0–3, Linux 7.0.0-1017-azure, Docker 28.0.4. Container Ubuntu 18.04.5, Clang 10.0.0, GCC 7.5.0, Python 3.6.9. |
| Rebuilt target / target in original archive | Both SHA-256 `df747746b563700f9230cbf66073062c6f2ba73e84c28898163c5e85f7db9c61` |
| Witness | [Original witness](../../../results/2026-11-07/comparison-42381922637/twostage/witnesses/period/r01/000001_0000004_assertion-failed); SHA-256 `fc55bbedbf9a5469327c9ecbb84465bc1c000745882e2dac476739ce3568d262` |
| Run, job and artifact | [43681034375 / attempt 1](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43681034375), job [132711487889](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43681034375/job/132711487889), artifact `14148546207`. The files alongside this record retain the output after artifact expiry. |

## Commands and outputs

From the repository root on a disposable x86_64 Linux host with Docker and real-time scheduling support:

```bash
bash scripts/replay_twostage.sh "$RUNNER_TEMP/twostage-evidence"
```

Supply a new output directory. Outside Actions, substitute a fresh path in place of `$RUNNER_TEMP/twostage-evidence`. The script verifies the witness hash and upstream pin, checks source bytes, builds the instrumented target, then runs the following command five times inside the container in `/workdir/PERIOD/evaluation/CS/twostage`:

```bash
timeout -k 5s 30s python3 /workdir/PERIOD/tool/DBDS/run_PDS.py -y -r /witness ./twostage_bad
```

[Executed script](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/62cbb795567a644bf6809227af140d21735eef9d/scripts/replay_twostage.sh) · [Executed workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/62cbb795567a644bf6809227af140d21735eef9d/.github/workflows/twostage-witness-review.yml) · [Host transcript](host.txt) · [Container command and build transcript](container.txt)

| Attempt | Combined stdout/stderr | Driver/wrapper exit | Target result |
| ---: | --- | ---: | --- |
| 1 | [replay-1.txt](replay-1.txt) | [0](replay-1.exit) | `Bug found!` and line-48 assertion after reproduction marker |
| 2 | [replay-2.txt](replay-2.txt) | [0](replay-2.exit) | `Bug found!` and line-48 assertion after reproduction marker |
| 3 | [replay-3.txt](replay-3.txt) | [0](replay-3.exit) | `Bug found!` and line-48 assertion after reproduction marker |
| 4 | [replay-4.txt](replay-4.txt) | [0](replay-4.exit) | `Bug found!` and line-48 assertion after reproduction marker |
| 5 | [replay-5.txt](replay-5.txt) | [0](replay-5.exit) | `Bug found!` and line-48 assertion after reproduction marker |

All five target diagnostics are present in newly captured output. The stock driver records no separate target exit code in replay mode. No timeout or miss occurred in this five-call sample. The host-name warning occurred on each call and did not prevent the diagnostic. [Recount/classification output](verification.txt) · [Digests of the 12 raw files](SHA256SUMS)

To recheck from the repository root:
```bash
python3 scripts/verify_twostage_witness.py --replay-dir results/member-reruns/1240000576-twostage-43681034375
(cd results/member-reruns/1240000576-twostage-43681034375 && sha256sum -c SHA256SUMS)
```
