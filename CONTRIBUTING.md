# Contribution and commit rules

## Actual identities

Each member contributes using their own GitHub account and their own verified
student ID and full name. Never attribute AI-generated or another member's work
to a student without recording the actual contribution and review.

Before contributing from a new clone, configure the following values **locally**
with real values, not the documentation placeholders:

```sh
git config --local user.name "Full Name"
git config --local user.email "your verified GitHub email or GitHub noreply email"
git config --local cs340.studentId "YOUR_REAL_STUDENT_ID"
git config --local cs340.fullName "Full Name"
git config --local core.hooksPath .githooks
```

The owner bootstrap script performs these local settings for its operator using
the authenticated GitHub account. It does not modify global Git configuration.

Every commit subject follows:

```text
[STUDENT_ID] Full Name: specific, meaningful change
```

The `commit-msg` hook checks the ID and name against local configuration. It
cannot independently prove a person's university identity. Use accurate values.
Hooks are local safeguards, not a server-side enforcement policy. GitHub web
commits and other clients can bypass them, so manually preserve the same rule.
Merge and squash messages must also include the actual responsible member's
student ID and full name.

## Weekly progress

The course checks repositories each Sunday at 23:59. Push a meaningful code,
script, result or documentation change during that week. Whitespace and typo-only
changes do not count. The teaching team decides whether a contribution is
substantive; the scaffold does not guarantee weekly credit.

The source does not explicitly specify the timezone or first calendar check date.
Confirm those with the teaching team. A group may use Asia/Macau internally, but
must record this as a planning assumption until confirmed.

## Safe repository contents

Do not commit build outputs, disk images, large traces, credentials, or files
larger than 50 MB. The supplied file check conservatively enforces 50,000,000
bytes and screens common credential patterns. It is not a complete secret scanner.
It deliberately keeps small raw logs, CSV data and figures trackable.

Do not upload paid/restricted benchmarks or instructor material without the
necessary permission. Preserve upstream licenses and attribution.

## Research integrity

Record the exact upstream starting commit, changes, environment, inputs,
commands, failed runs and deviations. Record actual contributions in
`docs/CONTRIBUTIONS.csv` and actual AI use in `docs/AI_USAGE.md`.
Use generic assistance terminology in maintained prose and commit messages.
Keep the actual scope of assistance and review status clear, with academic
sources and original contributors credited separately.
Do not generate results, student identities or progress dates to fill a template.
Do not backdate history or create empty commits to simulate weekly progress.
