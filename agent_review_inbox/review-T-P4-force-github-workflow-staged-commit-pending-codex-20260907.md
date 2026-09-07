---
kind: immutable_execution_handoff
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
date: 2026-09-07
status: PENDING_GITHUB_COMMIT_CONFIRMATION
---

# Force/O2 GitHub workflow staging handoff

GitHub editor is open for:

```text
Liang-techh/Percolation-proof-workflow/.github/workflows/force-general-state-export.yml
branch: main
```

The minimal `workflow_dispatch` job is staged in the editor but not committed. It contains Julia 1.10 setup, the existing strict runner/verifier invocation, deployed-source staging, and complete artifact upload. No GitHub Actions run has been triggered and no runtime PASS/READY receipt exists.

Required repository variables, still to be supplied before a meaningful run:

```text
DEPLOYED_SOURCE_REPOSITORY=<owner>/<deployed-dhport-source-repository>
DEPLOYED_SOURCE_REF=<frozen deployed-source ref>
```

After the workflow is committed and variables are present, the only accepted result is the existing strict artifact contract: fresh 16-row CSV, `B=[4,5]`, `D=[1,2,3,6]`, complete schema, source/exporter hashes, worker/verifier exit 0, stdout/stderr/exit receipt, and `MAX_E1/MAX_E2 <= 1e-12`. Missing variables, failed checkout, nonzero exit, or incomplete artifact remains pending/rejected.

This handoff records staged-but-uncommitted execution state only; it does not modify the strict gate or main state and makes no deployed-tau equivalence claim.
