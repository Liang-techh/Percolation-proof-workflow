---
kind: companion_log
review_id: companion-GH-MATH-P4-ALL6-SOURCE-ROWS-20260908
task_id: GH-MATH-P4-ALL6-SOURCE-ROWS
source_agent: Sartre the 6th
created_at: 2026-09-08
integration_status: pending
admission_label: pending
proof_status: SOURCE_ROW_OBSTRUCTION_NO_NEW_REVIEW_FILE
inspected_commit: 353e03fb9574812e9f02754b3fc7ff7462c0892a
source_binding_proven: false
actual_source_rows_recovered: false
registry_promoted: false
formal_certificate_allowed: false
local_lean_run: false
julia_execution: false
full_regression: false
---

Coordinator companion preserving Sartre's read-only handoff.  All six current
interval/payload families expose only `rows=[4,5]`; the builders' outer loops
run over `(3,4)`, while their inner `range(6)` sums components within each
row.  The DH preconditioned builder additionally inserts only the diagonal
controller terms `Kp[i] q[i]` and `damp[i] dq[i]`, although the stored X rows
have nonzero remote columns and a complete `X*tau` controller contribution
would include all six joint terms.  The neighboring bridge builder retains
all six coefficients, so the two same-labelled payloads cannot be merged as
one complete source equation.

The missing source obligations remain: actual rows 1,2,3,6; corrected full
signed controller polynomial; actual valuation/defect for rows 4,5; and a
same-configuration equation for the Float64 solve.  This is an obstruction to
source binding, not a physical counterexample.  Hash anchors from the handoff:
`half_active_vanis2_domain_probe.json`=
`28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E`,
`preconditioned_force_balance_identity_dh_v1.json`=
`E0969AADE062FE7C7648A655EA95282E8FD27F9EB7D47C3FFC1B38E33C920F48`,
`force_balance_bridge_dh_v1.json`=
`3045EA1923148C90C8473C8402C7522E99EEDA2C1590A494322CA3950D76A107`.
