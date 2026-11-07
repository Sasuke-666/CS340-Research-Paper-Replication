# Sources, attribution and version record

1. Instructor-provided `2609_CS340_Research_Paper_Replication(1).pdf`, academic
   year 2026–2027. Pages 1–4 define milestones, report and repository criteria.
   The course PDF and slides are not redistributed.
2. Wen, C., He, M., Wu, B., Xu, Z. and Qin, S. (2022). *Controlled Concurrency
   Testing via Periodical Scheduling*. ICSE 2022. DOI: 10.1145/3510003.3510178.
   https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf
   Table 2 (PDF p. 9) supplies the selected reference counts; section 4.1.3
   (PDF p. 8) supplies the original experiment settings. The PDF is not bundled.
3. Authors' implementation: https://github.com/wcventure/PERIOD
   Starting commit: `cb8deb9a176e5bb292d70d46557dd61dc0e98069`.
   The runner downloads this public source at that commit. Benchmark source is
   not edited. Its instrumentation/static-analysis layer is rebuilt from this
   checkout; installed compiler/SVF dependencies come from the recorded image.
4. Authors' container: `wcventure/period:stable`, resolved during the first pilot
   to `wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc`.
   Subsequent scripts default to that digest. See the archived image inspection,
   compiler output and environment records. A digest pins image contents, not
   the host kernel or CPU. Do not identify it as a fresh build of every original
   2022 dependency.
5. Upstream license: the complete MIT notice copied from the pinned checkout is
   retained as `results/2026-11-07/pilot/upstream_LICENSE.txt`, and again with the
   follow-up. Other dependencies retain their own licenses; no blanket license
   is assigned to them or to the group's future work.

## Project additions

Project-owned additions are the scripts under `scripts/`, workflow files,
experiment protocols, tests, analysis documents and measurement records.
The `scripts/period_container_pilot.sh` overlay restores the pinned source over
an existing dependency image; it rebuilds the original analysis/instrumentation
layer but does not modify benchmark logic. Generated bitcode/executables remain
inside the disposable container and are not committed. No original library,
compiler binary, disk image or credentials are redistributed.

The wrapper uses a fixed `/workdir/PERIOD` location inside the container because
that is the authors' installed layout. Host paths are derived from the repository
location and the chosen output directory; no student's home directory is required.
