---
kind: review_result
review_id: review-T-P4-006-sumengchen-20260906T2241
task_id: T-P4-006
parent_task_id: T-P4-005
source_review_id: review-T-P4-005-liuguanyi-20260906T2206
source_agent: 苏梦辰
created_at: 2026-09-06T22:41:00-06:00
inspected_commit: 820a8158f02e8efc8ba84ea7099d5b6b14e4571e
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: focused_compile_then_independent_validation
---

# T-P4-006 — sharp one-channel Schur formalization

## Question and handoff consumed

This task formalizes the exact-real mathematics proposed by 柳冠一 in
`review-T-P4-005-liuguanyi-20260906T2206.md` (blob
`fec977f38720baf22477b6d44b4dcba1d5bd87ea`).  The formalization target is the
sharp scalar Schur condition

```text
(∀ x, 0 ≤ p*x^2 + 2*x*r + d*y^2)  ↔  r^2 ≤ p*d*y^2,
```

under `0 < p`, together with the zero-`y` obstruction and a concrete rational
`c = 1/4` corollary for the existing block-4 coefficients.

This result does not redo source provenance/receipt/admission and does not claim
true-DH binding, domain coverage, P4 closure, or M4 closure.

## New formalization artifacts

Created the isolated sidecar:

- `examples/routeb_p4_sharp_schur_sidecar/P4SharpSchur.lean`
  - current blob: `fbfbf3d03c448760f8c9e042f05df5bef41c221c`
- `examples/routeb_p4_sharp_schur_sidecar/verify.sh`
  - current blob: `c923ff717e361c0037636d18a376715af3b2d783`
- `examples/routeb_p4_sharp_schur_sidecar/lean-toolchain`
  - pinned to `leanprover/lean4:v4.33.1`
- `examples/routeb_p4_sharp_schur_sidecar/README.md`

The file is intentionally independent of the existing
`examples/routeb_p4_next_child/P4RationalSchurAbsorption.lean` (upstream blob
`d85c2e1c258a88355b076ac5cce322180eb827ad`), so the new theorem does not alter
or overwrite the already checked stronger `ell = 1/100` child.

## Theorem decomposition implemented

### 1. Sharp iff theorem

```lean
schur_residual_nonnegative_iff
    (p d r y : ℝ) (hp : 0 < p) :
    (∀ x : ℝ, 0 ≤ p * x ^ 2 + 2 * x * r + d * y ^ 2) ↔
      r ^ 2 ≤ p * d * y ^ 2
```

Formal proof structure:

- necessity evaluates the universal quadratic at its exact minimizer
  `x = -r/p`, multiplies by the positive `p`, and reduces by field/ring
  normalization to `0 ≤ p*d*y^2-r^2`;
- sufficiency avoids division: multiply the target quadratic by `p` and use the
  exact identity

```text
p * Q = (p*x+r)^2 + (p*d*y^2-r^2).
```

Both summands are nonnegative under the sharp budget.

### 2. Zero-slice obstruction

```lean
zero_y_forces_zero_residual
```

formalizes that if `p > 0` and

```text
∀ x, 0 ≤ p*x^2 + 2*x*r,
```

then `r = 0`.  This is the precise theorem-level version of the mathematical
warning that a nonzero additive source bias at an allowed `y=0` state cannot be
hidden in the present universal scalar PMI.

### 3. Concrete rational budget

The sidecar reifies only the exact-real block-4 constants

```text
p4 = 3/5,
d4 = 116667666666667 / 10^15.
```

and proves

```text
(1/4)^2 < p4*d4.
```

It then derives:

```lean
quarter_residual_absorption
    (x y residual : ℝ)
    (hresidual : residual ^ 2 ≤ (1/4 : ℝ) ^ 2 * y ^ 2) :
    0 ≤ p4 * x ^ 2 + 2 * x * residual + d4 * y ^ 2
```

by feeding the relaxed source envelope into the sharp iff theorem.

## Verification performed in this runtime

The current runtime exposes neither `lean` nor `lake`, so a kernel compile was
not fabricated.

Commands/checks actually run:

```text
command -v lean
command -v lake
```

Result: both returned no executable path.

The new `verify.sh` was separately shell-parsed with:

```text
bash -n /tmp/verify_p4_sharp.sh
```

Result:

```text
SHELL_SYNTAX=PASS
```

The concrete rational arithmetic was independently replayed with exact Python
`Fraction` arithmetic:

```text
(1/4)^2 = 1/16
p4*d4   = 350003000000001/5000000000000000
margin  = 37503000000001/5000000000000000
quarter_sq_lt_pd = True
```

This checks the intended concrete coefficient inequality only; it is not Lean
kernel evidence.

## Focused compile path

When a pinned Mathlib environment is available, run:

```text
cd examples/routeb_p4_sharp_schur_sidecar
./verify.sh
```

The script fails closed with exit code 2 if `lake` is absent, otherwise invokes
Lean with `-DwarningAsError=true`, requires all four `#print axioms` targets to
appear, and rejects `sorryAx`, unknown modules, reported axioms, or Lean errors.

No `FOCUSED_CHECK=PASS` or axiom PASS is claimed in this review because the
command could not be executed in the present runtime.

## Remaining blockers / next handoff

1. **Formalization compile:** 苏梦辰/臭屁猪 (whichever next has a usable pinned
   Lean environment) should run only the focused sidecar verifier.  If Lean
   rejects the minimizer normalization, the only expected repair surface is the
   local `field_simp/ring` proof of the necessity direction; the mathematical
   theorem statement should not be weakened.
2. **Independent validation:** after compile, `封不觉` should independently
   inspect the theorem statement, compile log and `#print axioms` before any
   admission label changes.
3. **Physical source mathematics remains open:** the source lane must still
   prove a same-domain envelope such as `residual^2 ≤ (1/4)^2*y^2` (or the exact
   sharp budget).  This sidecar proves only that such an envelope is sufficient.
4. **Zero-slice blocker remains substantive:** if the deployed residual does not
   vanish on an allowed `y=0` slice, the present PMI interface must be changed
   (e.g. explicit bias/slack) rather than repeatedly tightening receipts.

## Conclusion

The mathematical handoff from `T-P4-005` has been converted into a small,
explicit Lean sidecar with the sharp iff theorem, zero-slice obstruction, and a
`1/4` rational sufficient corollary.  The artifact is ready for focused kernel
compilation, but admission remains `pending` until that compile and the unique
validator's independent gate are complete.
