# Independent technical audit of v1.0.1 and Windows Python 3.14

**Prepared by:** 李扬烁, student ID 1240001156, GitHub `barkhorn996`

**Audit date:** 22 November 2026, Asia/Shanghai (UTC+08:00)

**Audited release:** `v1.0.1`

**Tag commit:** `10ff18acd17d3acd6ccda3d5582c8eecbb496c88`

**Declared source commit:** `58266473e462e096f1701e91f9a136cd98cf0300`

This audit adds no experiment and changes no released document. It independently verifies the downloadable v1.0.1 release and exercises the repository's supported Windows analysis and export paths using native Windows Python 3.14.7.

## 1. Release asset download and hash verification

All seven release assets were downloaded through the GitHub Release API. Each local SHA-256 was compared with the remote asset digest returned by GitHub. All seven matched.

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `CS340_Final_Deliverables_20261124.zip` | 9,001,319 | `bcbfafafb8a73849471547bd6c2b3a65a391f326c180ad9e3bc887434d4432ab` |
| `CS340_Final_Submission_Handbook_20261124.docx` | 43,249 | `c41eb8bb1d610fabd9008929a4513b85c8eb63a4e8583214dcce02aa79cbbd0d` |
| `CS340_Final_Submission_Handbook_20261124.pdf` | 307,232 | `f3934adac25cf36975518fc1377566dd4c0147880ec5568238b6c492fca3090c` |
| `CS340_PERIOD_Final_Presentation_20261124.pdf` | 258,059 | `06b000ecb580c40d003263bd012f632cda69ca794a480ba8d4a88f4439c080e7` |
| `CS340_PERIOD_Final_Presentation_20261124.pptx` | 85,521 | `7169c8cfee4a7ffca77b405b496441b8fe41759840125625e835abb2fcb3c7f0` |
| `CS340_PERIOD_Final_Report_20261124.docx` | 340,466 | `1fd881a341110eb843e6bc7742bf0094d54c248f70ba1a88580e29270a976f31` |
| `CS340_PERIOD_Final_Report_20261124.pdf` | 489,673 | `102588a4e5c1ed1905752f1ded2bb536018db4d98bdb5e66474a3f497bc2284b` |

The six document assets were then compared across three locations:

1. Direct release download.
2. Top-level copy extracted from the complete ZIP.
3. `Repository/submission/` copy inside the complete ZIP.

For every file, the local hash, extracted top-level hash, embedded repository hash and `FINAL_RELEASE.json` hash were identical.

## 2. Complete ZIP verification

The release ZIP has the expected remote digest and local SHA-256:

`bcbfafafb8a73849471547bd6c2b3a65a391f326c180ad9e3bc887434d4432ab`

ZIP structure checks:

| Check | Result |
| --- | ---: |
| Total entries | 7,690 |
| Files under `Repository/` | 7,682 |
| Top-level final documents | 6 |
| Delivery metadata | `DELIVERY.json` and `START_HERE.txt` present |
| Git metadata | Absent |
| Duplicate paths | 0 |

The 7,682 extracted files under `Repository/` were independently compared with every file tracked at tag commit `10ff18acd17d3acd6ccda3d5582c8eecbb496c88`. All 7,682 file paths and SHA-256 values matched. No tracked file was missing or altered.

The declared source commit `58266473e462e096f1701e91f9a136cd98cf0300` is an ancestor of the release tag commit.

## 3. Extracted release self-check

Running the release's own verifier on the extracted repository:

```text
python scripts/check_final_submission.py --root Repository
```

returned:

```json
{
  "tag": "v1.0.1",
  "report_revision": "2026-11-24",
  "source_commit": "58266473e462e096f1701e91f9a136cd98cf0300",
  "verified_documents": 6,
  "verified_sources": 25,
  "git_commit_verified": false,
  "status": "passed"
}
```

`git_commit_verified=false` is expected for an extracted delivery package because the ZIP intentionally contains no `.git` metadata. Git ancestry was checked separately against the source checkout, as described above.

## 4. Windows native environment

| Item | Value |
| --- | --- |
| Operating system | Windows 10 Pro x64 |
| CPU | Intel Core i5-14490F, 10 cores and 16 logical processors |
| Python | CPython 3.14.7 |
| Git | 2.55.0.windows.5 |
| Report dependencies | `python-docx 1.2.0`, `reportlab 4.4.9`, `CairoSVG 2.8.2`, installed in an isolated virtual environment from `requirements-report.txt` |
| Input | Extracted `Repository/` from the v1.0.1 complete ZIP |

## 5. Windows supported audit

The repository's existing Windows-supported evidence path was executed with native Windows Python 3.14 and completed successfully.

Verified checks:

- Portable archive tests: 3/3 passed.
- Repository file checks: passed.
- Historical PERIOD evidence: 126 manifest files and 40 command logs verified.
- Original comparison batches: all manifest and summary checks passed.
- Original compatible comparison: 90 complete results among 100 attempts, with 40 diagnostics.
- Four-thread follow-up: 6/6 complete and eligible, three pairs.
- Independent member account batch: 20/20 complete and eligible, ten pairs.
- Controlled capacity studies: both readable cases 20/20 complete and eligible, ten pairs each.
- Fresh-host acceptance: 30 complete eligible comparisons, 15 pairs and 40 diagnostics.
- Twostage recount: all six logs and all reported mean/sample-SD cells reproduced.
- Report table audit: 321 cells checked, including 236 quantitative or missingness cells, with no integrity error.
- Explanation evidence audit: 66 files checked, including 61 raw logs and five source/configuration files.
- Member review integration: 40 request-sequence logs and 12 replay checks passed.

The complete command transcript is preserved in `evidence/1240001156-release-windows-audit-20261124/windows-supported-audit.log`.

## 6. Windows report export

With the pinned report dependencies installed, native Windows Python 3.14 completed:

- All three `test_report_exports.py` tests.
- A fresh report export through `scripts/export_stage_report.py`.

The generated Word and PDF opened and were structurally readable. Their bytes differ from the signed Linux-generated release files because document generation includes environment-dependent font, PDF metadata and Office-package details. They were not substituted for the frozen release artifacts and were not added to the release manifest.

The export transcript is preserved in `evidence/1240001156-release-windows-audit-20261124/windows-report-export.log`.

## 7. Full Linux-oriented unit suite on Windows

Running all 164 tests on native Windows produced 5 failures and 22 errors. This does not indicate a damaged v1.0.1 package; every supported Windows audit above still passed.

The failures fall into these categories:

- Tests that intentionally invoke Bash or Make entry points. The benchmark pipeline is specified for Linux/Docker, and this Windows host has no working default WSL Bash distribution.
- Tests that create symbolic links without Windows Developer Mode or elevated symlink privileges.
- Tests that create a filename containing a newline, which is invalid on Windows.
- A timeout test that calls the POSIX-only `os.killpg`.
- Synthetic layout and temporary-Git fixture tests whose path/platform assumptions differ on Windows; the actual archived layout and Git-independent evidence checks pass.

The complete raw failure log is retained outside the repository with the independent audit evidence. The release's official Windows CI scope remains the portable-archive and offline-evidence path exercised in Section 5, not benchmark execution or every POSIX-only unit test.

## 8. Conclusion

The v1.0.1 release is internally consistent and downloadable without corruption:

- All seven GitHub release asset digests match local downloads.
- All six final documents match `FINAL_RELEASE.json`.
- The complete ZIP contains exactly the 7,682 tracked files at the release commit, with no Git metadata or duplicate paths.
- The extracted package passes its own final-submission verifier.
- The supported Windows evidence and report-export paths pass under Python 3.14.7.

No release content, experimental data or scientific conclusion was changed by this audit.
