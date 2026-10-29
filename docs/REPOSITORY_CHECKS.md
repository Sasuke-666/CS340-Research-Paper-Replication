# Repository safeguard verification

Date: 2026-10-30 (Beijing time).
Starting remote commit: `18295412609bc31785c52418b3034268544a974e`.
Scope: repository engineering and regression testing. No PERIOD experiment ran.

## Run locally

Requirements: Git and Python 3.9 or newer; no third-party Python dependencies.
Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 scripts/check_repository.py --staged
git diff --check
```

The ordinary check inspects tracked working-tree files. The staged check inspects
the proposed index content and paths, including file type changes, and ignores
staged deletions. Untracked files are outside a Git repository's ordinary check;
stage intended additions before checking them. Without Git initialization, the
ordinary check scans files under the supplied root, excluding `.git` metadata.

## Coverage and observed repairs

The suite contains 43 test methods, with parameterized boundary cases using
`unittest.subTest`. Temporary Git repositories exercise actual index and hook
behavior without touching the caller's Git configuration or history.

| Area | Coverage |
| --- | --- |
| File size | Zero, below/exactly/above 50,000,000 bytes; oversized sparse file rejected without reading it; staged blob size and skipped content load (smaller patched threshold) |
| Credentials | GitHub token families, AWS access-key shape, private-key headers, binary content, short tokens and word boundaries, `.env.example` scanning, redacted diagnostics |
| Generated files | Forbidden suffixes and case variants, nested output directories, credential filenames, environment files, versioned shared libraries, CMake output/cache and numeric core dumps; small research outputs remain allowed |
| Git/filesystem | Tracked/untracked/missing files; differing index and working-tree content; deletion, rename and type changes; spaces, Unicode and newlines in filenames; repository-root requirement |
| Symlinks | Ordinary and broken links, staged link with a regular working-tree replacement, both directions of regular-file/symlink conversion |
| Identity and hook | ID length/character boundaries, placeholders, known TA ID, Unicode names, malformed names, exact subject prefix, description length, missing configuration, mismatched Git name |
| CLI | Real subprocess exits 0 for success, 1 for rule violations and 2 for unavailable Git/invalid arguments; simulated OS/Git/size errors also return 2 |

Running the final suite against the original checker produced **10 failing
assertions across four test methods** (43 methods total; exit 1). The failures
identified three repair areas:

1. `--diff-filter=ACMR` omitted `T`, allowing staged regular-file/symlink changes
   to bypass inspection in both directions. Add `T` to preserve the same checks.
2. The checker missed numeric `.so` versions, `cmake-build-*` directories,
   `CMakeCache.txt` and numeric core dumps, despite existing `.gitignore` rules
   for those artifacts. Add narrow path checks; keep `core.py` and `core.c` valid.
3. Private-key detection omitted DSA and encrypted private-key headers. Extend
   the existing header pattern without changing diagnostic redaction.

After those changes, **all 43 methods passed** (exit 0; no skips).

## Recorded local evidence

Environment: Linux x86-64, Python 3.12.14, Git 2.51.1.

| Record | Observed result |
| --- | --- |
| [Before repair](validation/repository-checks-20261030/before-fix.txt) | 43 methods; 10 failed assertions; exit 1 |
| [After repair](validation/repository-checks-20261030/after-fix.txt) | 43 methods; all passed; exit 0 |
| [Final safeguards](validation/repository-checks-20261030/final-checks.txt) | Tracked and staged checks, commit-subject hook, workflow structure and whitespace verification |

Log timestamps are UTC; add eight hours for Beijing time. Repository absolute
paths in the captured test output are normalized to `<repository>`; trailing
whitespace is trimmed and line endings are LF. An initial formatting check found
CRLF/trailing spaces in the CSV/log output; normalization resolved them. Test failures
are intentionally preserved as regression evidence, not presented as passing runs.

Local files were obtained through the authenticated GitHub connector and their
blob hashes and baseline tree were checked against the remote. The shell has no
GitHub credentials. A synthetic local snapshot supports diffs/tests only; it must
never be pushed. Remote publication, if successful, uses the original remote
commit as parent. Commit timestamps do not establish push time; verify the remote
head, GitHub `pushed_at` and the Actions run separately.

## Continuous checks and limits

`.github/workflows/repository-checks.yml` runs the suite and tracked-file checker
on pushes, pull requests and manual dispatch, using Ubuntu 24.04 and Python 3.9 /
3.12. It has read-only repository permissions, a five-minute timeout per job,
SHA-pinned official actions and no persisted checkout credentials. No project
dependencies, workloads or secrets are required. The initial remote run must be
checked in [GitHub Actions](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions);
local success alone does not verify GitHub execution or the Python 3.9 job.

The workflow tests identity validation and the commit-message hook; it does not
validate every historical commit identity. Local hooks still need explicit
installation as described in `CONTRIBUTING.md`. Neither path rules nor token
patterns provide exhaustive secret detection. Identity validation checks shape
and configured consistency, not university enrollment. Windows behavior has not
been tested. Human review is pending and recorded in `docs/AI_USAGE.md`.

Course relevance: these changes support README/code quality, repository management
and reproducibility safeguards. The teaching team decides whether the work earns
weekly credit. The first check date and check timezone remain unresolved; this
work does not claim a paper reproduction result or guarantee course marks.
