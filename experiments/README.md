# Experiments

No experiment implementation or result is included at initialization.

Add build/run scripts only after checking them against the actual pinned
upstream version. Keep benchmark selection and configuration changes versioned.
Each run must produce identifiable logs and a machine-readable run record with
its command, exit status, workload, environment and metric definitions.

A container does not pin the host kernel. Record the actual kernel separately.
Any privileged or system-affecting experiment needs an appropriate controlled
machine/VM and explicit operator approval. Do not run it automatically from a
repository-creation script or a hosted CI workflow.
