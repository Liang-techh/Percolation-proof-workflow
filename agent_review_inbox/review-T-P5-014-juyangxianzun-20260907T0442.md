---
kind: review_result
review_id: T-P5-014-juyangxianzun-20260907T0442
task_id: T-P5-014
source_agent: 巨阳仙尊
created_at: 2026-09-07T04:42:00-06:00
inspected_math_review: agent_review_inbox/review-T-P5-014-liuguanyi-20260907T0417.md
inspected_math_blob_sha: deefb6a1c7f74dff7fb755668ad0d65a0ec16cf3
claim: agent_review_inbox/claim-T-P5-014-juyangxianzun-20260907T0429.md
lean_head_commit: 7c034a708824520ed24d69f21602c815a8591b24
admission_label: compiled_candidate
integration_status: pending
registry_mutation: false
---

# T-P5-014 — weighted-dual execution-remainder adapter Lean sidecar

## Question formalized

Formalize the smallest source-independent theorem package from 柳冠一's
`T-P5-014` review that transports identified generalized-force error boxes into
the damping-weighted dual budget used by the P5 power consumer, while keeping
coordinate normalization explicit and retaining the fixed-bias/undamped
obstructions.  Do **not** authenticate Julia/DH/Float64 source semantics or
claim P5/P8/M4 closure.

## Added portable sidecar

- `examples/routeb_p5_weighted_dual_adapter_lean/P5WeightedDualAdapter.lean`
- `examples/routeb_p5_weighted_dual_adapter_lean/README.md`
- `examples/routeb_p5_weighted_dual_adapter_lean/lean-toolchain`
- `examples/routeb_p5_weighted_dual_adapter_lean/verify.sh`

The sidecar pins `leanprover/lean4:v4.32.0`; `verify.sh` locates `lake` from
`PATH`, checks the sibling `examples/local_fkg` toolchain, carries the marker
`CI_PORTABLE=1`, compiles with `-DwarningAsError=true`, and audits all printed
axiom reports for `sorryAx` / undeclared axioms.

## Theorem decomposition

The file defines, for `Vec6 := Fin 6 → ℝ`,

- `weightedDual d r = Σ_i r_i^2 / d_i`,
- `dampingSq d v = Σ_i d_i v_i^2`,
- `power r v = Σ_i r_i v_i`,
- `diagonalScale s e = (s_i e_i)_i`.

It then proves eight source-independent theorems:

1. `weightedDual_nonneg`: positive diagonal damping implies nonnegative dual
   quadratic form.
2. `box_to_weightedDual`: if `|r_i| ≤ eps_i`, then
   `weightedDual d r ≤ Σ_i eps_i^2/d_i`.
3. `box_to_rate_budget`: the previous cap feeds the finite-horizon rate budget
   directly when `Σ_i eps_i^2/d_i ≤ 4*gR*BR`.
4. `diagonal_normalization_dual_identity`:
   `weightedDual d (diag(s)e) = Σ_i s_i^2 e_i^2/d_i`; implementation scaling
   therefore cannot be silently dropped.
5. `diagonal_box_to_weightedDual`: a raw component box `|e_i|≤eta_i` transported
   through diagonal scaling yields exactly the expected scaled weighted cap.
6. `local_relative_to_weightedDual`: coordinatewise square-relative bounds
   `r_i^2 ≤ kappa_i d_i A` imply
   `weightedDual d r ≤ (Σ_i kappa_i) A`, without square roots.
7. `fixed_bias_not_uniformly_relative_scalar`: for `d>0`, `r≠0`, and any finite
   `gamma≥0`, there exists a velocity `v` such that
   `gamma*(d*v^2) < |r*v|`; hence a nonzero fixed force bias cannot be promoted
   to a homogeneous damping estimate near zero velocity.
8. `undamped_direction_obstruction_scalar`: if a coordinate has zero damping,
   a nonzero force on that coordinate defeats every damping-only power bound.

This package intentionally does not duplicate the weighted Cauchy/Young power
consumer already represented by `examples/routeb_p5_weighted_dual_residual_lean/`.
It supplies the new adapter layer in front of that consumer.

## Real CI loop and repair

### First run — failed on this sidecar

GitHub Actions `Lean agent sidecars` run **34112015455**, job
**101710273451**, checked out head
`6480e97414d4654d028b80f0e82b357f196425c6` and used Lean **4.32.0**.
The new sidecar reached the compiler and exposed three concrete proof-script
issues:

- line 146: `rw [div_lt_iff₀ hgp]` could not match the target
  `gamma * (1 / (gamma + 1)) < 1`;
- two subsequent `ring` calls reported `No goals to be solved` because
  `field_simp` had already discharged those identities;
- consequently `fixed_bias_not_uniformly_relative_scalar` temporarily printed
  `sorryAx` in that failed elaboration.

The run also exposed unrelated pre-existing failures in
`anthropic_flt_quotient_transport_sidecar/verify.sh` and
`routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`; those were
not modified because the latter is the separate 臭屁猪/T-P5-007 lane.

### Repair

Commit `7c034a708824520ed24d69f21602c815a8591b24` changed only the new adapter
proof:

- rewrote the scalar ratio step through the explicit lemma
  `gamma/(gamma+1) < 1`, then normalized with `div_eq_mul_inv`;
- removed the redundant `ring` calls after `field_simp`.

No linter, warning, or axiom gate was disabled.

### Second run — focused PASS

GitHub Actions run **34112495194**, job **101711677819**, checked out the repair
commit and compiled the new sidecar under Lean **4.32.0**.  Its log contains:

```text
AXIOM_AUDIT=PASS
P5_WEIGHTED_DUAL_ADAPTER_FOCUSED_CHECK=PASS
SOURCE_FORCE_COORDINATE_MAP=OPEN
SOURCE_COMPONENT_INTERVALS=OPEN
DAMPING_COEFFICIENT_SOURCE_BINDING=OPEN
P8_SAME_DOMAIN_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_weighted_dual_adapter_lean/verify.sh
```

All eight `#print axioms` reports are exactly within the standard set
`[propext, Classical.choice, Quot.sound]`; the repaired theorem has no
`sorryAx`.

The shared workflow still concludes `failure`, but after this repair the new
T-P5-014 sidecar is explicitly PASS.  The remaining failures are unrelated
existing lanes: the FLT quotient verifier's `../local_fkg` path and the
T-P5-007 weighted-dual residual sidecar's unused `hκ1` / disjunction-projection
errors and resulting `sorryAx`.  I did not take ownership of those lanes.

## Formal interface boundary / remaining blockers

The formal adapter now consumes already-identified generalized-force error
coordinates.  Physical admission still requires all of the following on the
same P8-covered domain:

1. a source-level coordinate map `J` from raw Julia/Float64 execution errors to
   the six generalized-force residual coordinates (the diagonal theorem is
   ready for a diagonal `J`; a genuinely non-diagonal map needs a separately
   typed quadratic-form bridge);
2. certified componentwise execution-error intervals or local-relative square
   bounds for the actual mass/controller/C/G/solve remainder;
3. source binding and strict positivity of the damping coefficients `d_i` for
   every coordinate charged through `weightedDual`; any zero-damping coordinate
   must be handled outside this consumer;
4. P8 same-domain coverage for every source interval/bound used by the P5
   energy ledger.

No Julia/DH semantic equality, IEEE interval, P8 flowpipe coverage, P5/M4
closure, provenance/admission, registry entry, or final theorem integration is
claimed here.

## Proposed integration target

Treat this sidecar as the formal adapter immediately upstream of the existing
weighted power consumer and the `T-P5-013` finite-horizon budget theorem.  The
source/checker lane can export either component boxes `eps_i` or
coordinatewise relative coefficients `kappa_i`; the Lean consumer then turns
those directly into the damping-dual scalar budget without introducing an
unrelated Euclidean norm.

**Status:** `compiled_candidate` — 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
