# Results and evidence

There are **no experimental measurements yet**.

Keep small raw logs under `logs/`. For each result, record its source run and
metric definition. Preserve failed runs and timeouts. Derived tables and figures
must be reproducible from actual logs using versioned analysis scripts.

Do not commit build outputs, disk images, large traces, credentials, or files
larger than 50 MB. Plan bounded logging or transparent, lossless splitting of
ordinary textual logs when needed; do not split prohibited disk images or large
traces to circumvent the course rule. Make each reported number traceable to
acceptable evidence stored in the repository.

Paper values and our measured values must be labeled separately. No dummy data
belongs in the final-result paths. Automated tests must label any fixtures as
synthetic and keep them outside research results.
