# Route-B P8 minimal concrete RHS payload line

This example is a small, local-only producer/checker seam for one explicit
Route-B box. It reads the current file-level proof-facing candidate in the
external `6dof_sos_optimized/robot_final` tree and writes only into this
directory. It does not include or execute the external Julia file, run
ReachabilityAnalysis, invoke a solver, perform branch-and-bound, run a
regression, or touch registry/workflow state.

The selected source snapshot is:

```text
robot_final/cross_validation/routeB_reachability_full_dh_probe.jl
robot_final/dhport_lib.jl
```

The source contract is deliberately recorded as a 13-state Julia RHS:

```text
payload index  1..6   q1..q6  <- u[1:6]
payload index  7..12  v1..v6  <- u[7:12]  (Julia names this dq)
payload index  13     w      <- u[13]
payload index  14     c      <- sidecar only; not consumed by full_rhs!
```

The selected source assigns `du[13] = 0`. It does not establish the P8 ramp
equation `w' = c`; that ramp binding remains `OPEN`. The local box is exactly

```text
q1..q6, v1..v6, w in [-0.01, 0.01],   c in [-2, 2]
```

This is a single small box, not a claim about the full Route-B domain. The
generator emits `SOURCE_METADATA.json` and `receipt.template.json`. The latter
has 14 interval rows but intentionally leaves the dynamic endpoint values
missing; the two tail rows expose the source-text `du[13]=0` fact and the
unbound `c` tail without fabricating a numerical enclosure.

Generate the local artifacts:

```powershell
python .\generate_payload.py `
  --routeb-root C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized
```

Check only the pending structure (the default concrete check rejects it):

```powershell
python .\check_receipt.py .\receipt.template.json `
  --source-root C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized `
  --allow-pending
```

A future concrete receipt must replace all `null` endpoint values with exact
decimal/rational text and declare explicit outward endpoint rounding. The
checker then reports `candidate_payload_only`, never `theorem` or
`LEAN_VERIFIED`; it checks shape, ordering, source hashes, parameters, and
metadata, not the mathematical truth of an interval enclosure. Missing,
malformed, stale, or non-outward evidence is rejected fail-closed.

Focused tests:

```powershell
python -m unittest .\test_payload.py
```

The generated metadata always carries `formal_admission: null`,
`binding_conclusion: null`, and explicit false flags for global
branch-and-bound, solver, regression, registry mutation, theorem, and
`LEAN_VERIFIED` status.
