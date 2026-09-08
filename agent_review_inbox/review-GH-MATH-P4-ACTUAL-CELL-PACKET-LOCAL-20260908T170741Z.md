---
kind: review_result
review_id: review-GH-MATH-P4-ACTUAL-CELL-PACKET-LOCAL-20260908T170741Z
task_id: GH-MATH-P4-ACTUAL-CELL-PACKET
source_agent: codex-half-active-packet-audit
created_at: 2026-09-08T17:07:41Z
integration_status: pending
admission_label: pending
status: SAME_SOURCE_ACTUAL_PACKET_ABSENT
source_binding_proven: false
actual_cell_packet_found: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
rank_audit_repeated: false
new_cell_search: false
state_mutation: false
registry_mutation: false
requested_action: supply the actual physical row/defect binding and a matching determinant, signed numerator and observable packet on the existing domain
---

# Half-active actual packet: shortest remaining gap

Only the existing half_active_vanis2 domain and its two DH force payloads
were reread, with current hashes below. No new cell search, rank audit,
producer, Lean/Julia or regression was run. Only this new review is written.

The existing domain payload contains analytic mass/RHS intervals, X and
contraction/acceleration radii; formal=false. The DH payloads contain
preconditioned/centered row expressions and explicitly leave physical
substitution and analytic-vs-FD obligations open. None supplies a completed
actual same-cell adjugate packet. Unchanged hashes bind this finding to the
previously audited objects, without repeating their support/rank analysis.

| Needed component | Current evidence boundary |
|---|---|
| Same actual S*u=f | Analytic row expressions are not an actual acceleration valuation or certified model/runtime defect |
| Positive determinant lower | No bound for the selected physical principal/Schur S is supplied as this packet's field; X contraction and unrelated mass bounds are not that field |
| Complete signed numerator | No enclosure of ell^T adj(S) f with the full retained coupling and actual defect on this domain |
| Observable covector | No fixed ell, coordinate/time units and actual second-derivative binding |
| Metric/gate | No matching residual H-budget/normalization and rational delta,R,A gate attached to those same physical objects |

The current workspace SameCellEvidence interface requires row1, row2,
determinant_lower, numerator_upper and observable_binding for one source
object and domain. Its rational gate R<=delta*A is not itself source evidence.
H is a separate residual-budget metric, not the preconditioner X and not an
implicit field supplied by the adjugate interface.

Three layers must remain separate:

- **Nominal:** template residual/port budgets, possibly another block metric.
- **Analytic:** current polynomial/slab candidate and repaired gain expressions.
- **Runtime actual:** the same loaded configuration, actual acceleration and
  finite arithmetic, with controller/FD/mass/assembly/solve discrepancy bound.

For the retained-coupling principal route on B=(4,5), the required actual RHS
is `F_B+e_B-M_BD*a_D`, D=(1,2,3,6), under convention M*a=F+e. A nominal
RHS or six-dimensional analytic acceleration radius does not identify this
function or its signed projected numerator. A Schur route additionally needs
its actual eliminated-row/inverse witnesses; no route switching is performed.

The shortest next evidence is therefore an authenticated actual physical-row
and defect binding on THIS domain, followed by the selected S determinant,
complete signed numerator and fixed observable witnesses. If a claim is only
about the analytic model, label it accordingly and prove its exact equations;
do not promote it to runtime actual. No packet constants are synthesized.

## Current SHA256

External root:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds`.

| File | SHA256 |
|---|---|
| half_active_vanis2_domain_probe.json | 28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e |
| preconditioned_force_balance_identity_dh_v1.json | e0969aade062fe7c7648a655ea95282e8fd27f9eb7d47c3ffc1b38e33c920f48 |
| force_balance_bridge_dh_v1.json | 3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107 |

The five-field interface was reread from workspace
`examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean`.
No compile or historical execution evidence was revalidated. No VERIFIED,
source admission, state/registry change or full-domain/trajectory claim.
