---
kind: review_result
review_id: review-GH-MIXED-flowchuanfeng-schur-absorption-liuchuanafeng-20260907T1823
task_id: GH-MIXED-flowchuanfeng-schur-absorption
agent: 流川枫
source_agent: 流川枫
created_at: 2026-09-07T18:23:00-06:00
inspected_commit: e66a702d0b7cb9e9799dc325cf063f22cddf1475
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SchurPMIAbsorption.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SchurPMIAbsorption_REVIEW.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_RelativeAdditive.lean
lean_blob_sha: da74083b84fb051acc797592e3afded9476b5296
related_tasks:
  - GH-LEAN-P4-032-relative-additive
  - GH-LEAN-P4-032-weighted-three-term
  - T-P4-032
integration_status: pending
admission_label: pending
proposed_integration_target: P4.032_schur_pmi_absorption_sidecar
requested_action: keep the sidecar as an UNCOMPILED source-independent consumer; treat SchurPMIBinding and FeedbackBinding as independent supplied premises; do not infer matrix Schur identity, sqrt, source, coverage, or registry admission; do not write StateStore or verified registry
---

# GH-MIXED-flowchuanfeng-schur-absorption — theorem-boundary audit

## 0. Result

`NEW_P4_032_SchurPMIAbsorption.lean` is a **conditional scalar consumer** of
the already-stated relative-plus-additive budget. It does not prove a Schur
complement, a PMI kernel identity, a matrix PSD fact, a source binding, or a
coverage statement.

The file header and the in-tree companion review already mark the sidecar
`UNCOMPILED`. This lane did **not** run Lean/Lake/`#print axioms`. Absence of
`sorry`/`admit` in the text is not a kernel receipt.

`admission_label` is therefore `pending` (architecture / uncompiled candidate
interface). Nothing here is registry evidence.

## 1. Exact public surface

Namespace: `RouteBP4032SchurPMIAbsorption`.
Import: `NEW_P4_032_RelativeAdditive` only (which itself imports weighted
three-term / typed defect branches).

| name | role | what it does *not* do |
|---|---|---|
| `Slack` / `strict_iff_positive_slack` / `exactSlack` | `rhoEff p < 1` iff a positive division-free slack `delta` with `rhoEff+delta ≤ 1` | treat `rhoEff ≤ 1` as enough for later division |
| `AbsorbedAt` / `absorb_relative_additive` | from `q ≤ rhoEff*E + biasEff` and slack, get coercive `delta*E - biasEff ≤ E - q` | drop the additive debit `biasEff` |
| `SchurPMIBinding` / `schur_pmi_margin` | consume a **supplied** scalar comparison `E-q ≤ margin` | derive that comparison from a matrix Schur/PMI identity |
| `schur_pmi_nonnegative` | needs extra `biasEff ≤ delta*E` to conclude `margin ≥ 0` | conclude PSD or nonnegative margin from slack alone |
| `FeedbackBinding` / `close_affine_budget` / `close_of_strict` | extra closure `E ≤ base + q` yields affine energy/residual bounds | infer energy upper bound from residual bound alone |
| `residual_allocation` | division-free `q ≤ available` under a scaled allowance | treat available as a source or domain certificate |
| `force_absorption` / `accel_absorption` | reuse typed force vs accel residual identities from the parent | convert conventions or insert an extra `J` |

Force branch keeps `forceTerm MBD J eD` and `ActionBound (MBD*J) tau`.
Accel branch keeps `accelTerm MBD eD` and `ActionBound MBD tau`.
The two distal defect types stay distinct.

## 2. Quantifier / premise boundary (the admission risk)

Two downstream consumers are **independent optional premises**:

1. `SchurPMIBinding` = a same-point normalized lower comparison.
2. `FeedbackBinding` = an energy-from-residual-plus-base upper comparison.

The sidecar never derives (1) from (2) or conversely. An integrator that
reads `AbsorbedAt` and writes “Schur margin closed” without a separately
hashed `SchurPMIBinding` (same energy, same `q`, same metric/normalization)
is a protocol error.

Likewise, `rhoEff < 1` is only a slack existence statement. Nonnegative
Schur/PMI margin still needs `biasEff ≤ delta * energy` at the same point.
A cell with large additive load can have strict relative coefficient and
still fail the margin sign.

Pointwise structures carry no domain quantifier. A later fold over boxes
or a trajectory must supply its own coverage evidence.

## 3. Compile / axiom status this slot

- Pinned toolchain: **not executed**.
- Exit code: **not obtained**.
- `#print axioms` lines are comments-for-future-audit only; they are present
  at the file tail and were not run.
- Placeholder scan (text only): no `sorry`, `admit`, or `axiom` command in
  this sidecar. Parent modules remain independently UNCOMPILED.
- Blob inspected: `NEW_P4_032_SchurPMIAbsorption.lean` sha
  `da74083b84fb051acc797592e3afded9476b5296` at commit
  `e66a702d0b7cb9e9799dc325cf063f22cddf1475`.

A later `:10`/`:40` Lean slot may compile this file under the pinned
toolchain. That compile would still be `compiled_candidate`, not verified
registry admission.

## 4. Forbidden promotions (explicit)

This review does **not** claim:

- source identity, true-DH, Float64 reification, or concrete `(rhoA,tau,...)`;
- matrix Schur complement, PMI kernel, or block PSD;
- sqrt-free vs sqrt-using numerical artifacts as the same object;
- domain / flowpipe / P8 coverage;
- P4/M4 closure or comparator PASS;
- any StateStore or verified-registry write.

## 5. Suggested next leaf (not executed)

If a Lean slot is assigned: produce an immutable compile receipt with exact
theorem names above, pinned toolchain, exit code, `#print axioms` for each
listed theorem, and a placeholder scan of the whole import cone. Keep
`SchurPMIBinding` and `FeedbackBinding` as unproved premises in that receipt.
