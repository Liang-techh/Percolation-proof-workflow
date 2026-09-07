---
kind: immutable_execution_handoff
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
date: 2026-09-07
status: BLOCKED_STAGED_NOT_COMMITTED
---

# Force/O2 runtime: exact GitHub execution blocker

The minimal job is currently staged, but not committed, in the GitHub editor for:

```text
Liang-techh/Percolation-proof-workflow
.github/workflows/force-general-state-export.yml
branch: main
```

The staged job uses Julia 1.10, the existing strict force runner/verifier, and complete artifact upload. No workflow run has started; no fresh 16-row CSV, runtime receipt, or PASS exists.

Required next actions:

```text
1. Commit the staged workflow file.
2. Set repository variables:
   DEPLOYED_SOURCE_REPOSITORY=<owner>/<deployed-dhport-source-repository>
   DEPLOYED_SOURCE_REF=<frozen deployed-source ref>
3. Run workflow_dispatch for force-general-state-export.
4. Intake only the fresh artifact with the existing 16-row/hash/schema/residual gate.
```

The local Julia branch-driver path remains unexecuted because Julia is unavailable locally. Do not treat the staged editor contents, prior CSVs, or a successful workflow landing as a runtime receipt. This record changes no gate or main state and makes no deployed-tau equivalence claim.
