---
kind: review_result
review_id: review-GH-MATH-P4-ACTUAL-CELL-PACKET-LOCAL-20260908T155615Z
task_id: GH-MATH-P4-ACTUAL-CELL-PACKET
source_agent: codex-actual-cell-source-lane
created_at: 2026-09-08T15:56:15Z
integration_status: pending
status: MISSING_SAME_CELL_SOURCE_WITNESSES
admission_label: pending
proof_status: existing_artifact_inventory_and_missing_witness_obstruction
actual_cell_packet_found: false
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
counterexample_repeated: false
state_mutation: false
registry_mutation: false
requested_action: complete the same-cell metric, actual-defect, observable and descriptor witnesses without combining incompatible blocks
---

# Actual cell packet search: one traceable partial candidate, no complete packet

## Scope and result

Only this new inbox review is written. Read-only artifact/schema/source searches
and SHA256 computations were performed; no producer, solver, Julia, Lean,
numeric experiment or regression was run. Existing status labels below are
reported artifact contents, not newly authenticated enclosure proofs.

External root P is
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
Paths below are relative to P unless marked workspace.

The bounded search covered the workspace adjugate/same-source/Schur interfaces,
external `routeB_dense_Mq` exact/interval CSV and report candidates, and
`robot_formal_v1/interval_bounds` identities and remainder artifacts.
Searches for projected numerator, adjugate, observable binding and determinant
lower fields found no complete actual packet in these inspected outputs.
This is not a claim that no such evidence exists anywhere on the machine.

## Closest actual cell anchor

The existing `routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.csv`
contains a RESOLVED row with key `(eta=5.6, depth=3, box_id=83)`. Its matching
record in `routeB_compact_qbox_cover_depth3.csv` is INTERSECTS and supplies:

| Coordinate | Exact lower token | Exact upper token |
|---|---|---|
| q2 | -1932183566159/1000000000000 | -5796550698477/4000000000000 |
| q3 | -5796550698477/4000000000000 | -1932183566159/2000000000000 |
| q4 | -1932183566159/2000000000000 | -1932183566159/4000000000000 |
| q5 | -1932183566159/2000000000000 | -1932183566159/4000000000000 |

These are copied existing geometry tokens, not newly generated enclosures.
The producer defaults to that cover but permits an environment override; a
matching key/current default is a traceable candidate join, not authenticated
proof of which cover bytes the historic run loaded. No historic environment
receipt was authenticated here. The geometry does not specify velocity,
disturbance, acceleration or trajectory containment.

`routeB_compact_block456_port_bi_partition_probe.jl` lines 14-15 fixes
D=[1,2,3], C=[4,5,6]. Lines 107-115 use q2..q5 from the row and q1=q6=0
for evaluation, construct M_DD and DeltaM_DC. Extending those fixed coordinates
requires the appropriate source independence theorem, not a silently enlarged cell.
Lines 169-184 explicitly compute the matching-M0 metric column via
`L0^-1 R B_up^-1/2`, with `L0 L0^T=Mzero_CC`.

The relevant row field is `rho2_m0_upper` (existing token starts
`0.421808231698443960457815691416593499...`), not `rho2_upper` or
`rho2_bchol_upper`. This abbreviated display is not a usable bound token.
The exact row remains in the hashed CSV; no rounding certificate was rerun.

`routeB_compact_block456_residual_schur_interface_audit.jl` lines 21-34
uses H=inv(M0CC456Q), nominal lBase, total lT and betaC456. The included
`routeB_compact_block456_descriptor_structure_audit.jl` lines 43-50 defines
M0CC456 from the origin of the analytic mass plus one regularizer.
Thus the intended metric match is identifiable, but a same-source equality
Mzero_CC=M0CC456Q and interval/coordinate transport are still witness obligations.
The fixed worst-cell coefficients in that symbolic interface are diagnostic
templates; they are not a filled per-cell actual-residual packet.

## Why the five requested groups do not close

| Group | Located evidence | Minimal missing witness |
|---|---|---|
| Cell and block order | Exact cover record; C=(4,5,6), D=(1,2,3) producer indices | Authenticated row/cover/config join and full state domain |
| Same H | Matching-M0 producer column and symbolic inverse metric definition | Same-source matrix identity and common metric transport for every residual term |
| ell / observable | lBase is a 3-vector nominal force residual | A fixed physical observable, coefficients, units and derivative binding; do not identify it with lBase by symbol |
| Actual residual defect | Symbolic total-residual decomposition; analytic preconditioned remainder data elsewhere | Actual source-to-descriptor valuation and all FD/controller/solve/model defects on this cell |
| det / numerator / row | Port-norm ledger and symbolic constraints | Same descriptor row equations, positive determinant bound and correlated signed projected numerator enclosure for the selected observable |

In particular, the workspace
`examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean`
lines 93-106 requires exactly row1, row2, determinant_lower, numerator_upper,
observable_binding for one symmetric 2x2 descriptor and one cell. The located
block456 producer is three-dimensional. It cannot instantiate those five
fields without a separately proved two-dimensional restriction/effective RHS
or reduction. Alternatively, a three-dimensional consumer needs its own
reviewed interface; no new consumer is proposed or implemented in this audit.

The Schur nominal residual vector ell and the adjugate affine-observable
coefficient covector ell have different roles and potentially different
dimensions. A common name or common source hash is not their identification.

## Other exact/interval candidates and why they cannot fill the gaps

1. `routeB_compact_block_schur_interval_certificate_probe.csv` reports
   CERTIFIED_LOCAL_MASS_SCHUR on q1=q2=q3=q6=0, q4,q5 in [-3/20,3/20].
   Its implication is M(q)-c E45 >=0. It is neither the above cell nor a
   signed numerator/actual-force witness. A Cholesky pivot lower bound is
   not the requested 2x2 determinant lower field by renaming.
2. `routeB_physical_rational_descriptor_bridge.csv` identifies B=(4,5),
   D=(1,2,3,6), retained energy determinants, and the complete origin M0_BB
   determinant. It labels itself algebraic_subcertificate, not residual bound
   or theorem. None is automatically a varying reduced-descriptor determinant
   over cell 83, and it has no observable numerator.
3. `robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json`
   reports EXACT_PRECONDITIONED_FORCE_BALANCE_IDENTITY_DH_GAINS, formal=false,
   with equation `X*((M+epsilon*I)*a-tau_DH+C(q,dq)*dq+G(q))=0`.
   Its rows contain support data for preconditioned rows 4 and 5, not the
   symmetric unpreconditioned 2x2 descriptor required by SameCellEvidence.
   Its own scope leaves analytic-vs-FD and positivity open. Its referenced
   domain is `half_active_vanis2_domain_probe.json`, not this q-box ledger.
4. `combined_descriptor_remainder_v1.json` reports
   COMBINED_POLYNOMIAL_DESCRIPTOR_BOUND, formal=false, analytic CSV semantics,
   symmetric slab domains and |w|<=2, not a flowpipe. Existing six-component
   preconditioned defect/acceleration bounds are not an actual defect for the
   selected reduced rows. `DESCRIPTOR_DEFECT_CONTRIBUTION_AUDIT_V1.md` explicitly
   says its decomposition is not an estimate of actual error. Its H=(I-C)^-1|X|
   is a comparison operator, not the block force metric M0_CC^-1.
5. `routeB_compact_composed_interval_partition_bounds.csv` and its Python
   producer provide another q2..q5 port-bound family with B=(4,5), D=(1,2,3,6).
   The producer labels it rigorous-numerical candidate only. It does not bind
   the three-dimensional H/actual defect/observable above.
6. The exact Fourier PMI identity audit retains nonzero residual coefficients
   and an identity-loading allowance, with formal_certificate_allowed=False.
   Its matrix identity/loading is not a source solve-defect or observable bound.

The actual `dhport_lib.jl` was read at mass_matrix, arm_MCG and exact_ddq:
it has regularized mass, central-difference C/G, and a Float64 backslash solve.
An analytic polynomial row identity with DH controller gains does not itself
prove that runtime satisfies the exact row equation. No runtime residual was
generated or assumed zero here.

## Minimal obstruction and next evidence

The obstruction is missing same-object evidence, not a numerical impossibility
result. Keep the existing cell-83 cover/port row as a partial starting point,
without constructing a synthetic completed packet.

Next evidence must freeze one block/reduction and one nonempty full-state cell;
bind source/config, H and actual total residual (including defect) to it;
freeze the observable independently of nominal residual notation; and provide
the matching row, determinant and signed projected numerator witnesses. Include
the row's actual beta/normalization allocation, not just a port gain. A single
cell result would still not imply global coverage or trajectory containment.

No Cramer/Young proof, q6 ray, or target-cap counterexample was repeated.
No source admission is claimed; integration and registry eligibility remain pending/false.

## Current raw SHA256 anchors

All below were recomputed in this turn; paths relative to P.

| Artifact | SHA256 |
|---|---|
| routeB_dense_Mq/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| routeB_dense_Mq/routeB_compact_qbox_cover_depth3.csv | 85b907bf8d12f46ee003731c5518a00a9a106c8f5a12e492037ae8fc52b04fdf |
| routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.csv | 1af8d59bf7253f992f13ad9318ea16ad5adb8cfa387dc5866b2f41ca4836dce4 |
| routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.jl | 62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129 |
| routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3d68fff2e71e3c912d45463ce1166e4381a98cefb049478b989cc279520d4d98 |
| routeB_dense_Mq/routeB_compact_block_schur_interval_certificate_probe.csv | 5df1400cc38dd1c66243926f9016d2cb72dd6dd8ea2e784ce802cd0526094d71 |
| routeB_dense_Mq/routeB_physical_rational_descriptor_bridge.csv | 8313f4a7c6b580d480200b88ed7457e5a9acc3262925a5358f360be93fe6fccb |
| robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json | 68596f1557aa709d86bc8711ed7985552684dffe7fde290abf03b511f6bd9805 |
| robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json | e0969aade062fe7c7648a655ea95282e8fd27f9eb7d47c3ffc1b38e33c920f48 |

Hashes record inspected bytes, not recursively verified dependencies or
authenticated historical execution. Workspace prior packet/source reviews were
used for routing; current concrete findings above were checked against the
indicated artifacts and source excerpts.
