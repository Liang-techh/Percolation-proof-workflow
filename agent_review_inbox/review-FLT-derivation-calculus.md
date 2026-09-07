---
kind: review_result
task_id: T-FLT-DERIV-CALC
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-FLT-DERIV-CALC review: derivation / calculus / smooth / continuous / integral / limit reuse scan

## Scope and method

Reviewed only `upstream/anthropics-fermats-last-theorem` at commit `aa2d8b34692b` and only files under `Definitions/` and `Theorems/` whose path/name intersects the requested families:
`derivation`, `calculus`, `derivative`, `smooth`, `continuous`, `integral`, `limit`.

No Lean build, no full tree compilation, no registry/state edits, no upstream source mutation.

The filter kept theorem-adjacent infrastructure and proof seams, not the number-theoretic end theorems themselves.

## Judgment summary

I found a small set of reusable theorem infrastructure in three bands:

- direct reuse: generic analytic/algebraic bridge theorems that already expose the right target shape and do not embed FLT-specific arithmetic;
- light adaptation: theorems whose statement shape is reusable but whose ambient objects are specialized to `Place`, curve models, or complex geometry;
- architecture only: transport/limit/tendsto scaffolding that is structurally useful but too domain-bound to lift as-is.

I did not find a clean direct-reuse candidate among the curve/place theorem family that can be moved unchanged into a nontrivial downstream calculus proof without changing the ambient typeclass stack.

## Direct reuse

| Level | Exact relative path | Namespace / theorem name | Dependencies / reuse notes | Adaptation risk |
|---|---|---|---|---|
| direct reuse | `Theorems/Thm_Algebra_exists_bijOn_eval_differentiableOn_of_smooth_of_kaehlerDifferential.lean` | `Algebra.exists_bijOn_eval_differentiableOn_of_smooth_of_kaehlerDifferential` | Imports `Mathlib`, `P2M.Util`, and the matching `P2M.Sol` proof. Statement packages `Algebra.Smooth ℂ S`, `Module.rank S (KaehlerDifferential ℂ S) = 1`, and a nonvanishing Kähler differential into a local bijection/differentiability theorem for evaluation at `σ₀ t`, plus a local openness/finite support stability clause. | Low to moderate. The shape is very reusable for downstream “smooth implies local differentiable coordinate parametrization” work, but the ambient field is complex, the target is algebra homs `S →ₐ[ℂ] ℂ`, and the proof is tied to the Kähler differential setup. |
| direct reuse | `Theorems/Thm_Algebra_exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential.lean` | `Algebra.exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential` | Same basic imports and proof style as above, but with a finite coordinate family `Fin n → S` and a rank condition `Module.rank S (KaehlerDifferential ℂ S) = n`. The theorem provides a bijection to a ball in `Fin n → ℂ`, with the same differentiable factorization and local stability clause. | Low to moderate. This is the best reusable finite-dimensional version of the previous theorem. The only real adaptation risk is replacing the `ℂ`-linear ambient with the downstream scalar field or topology. |

## Light adaptation

| Level | Exact relative path | Namespace / theorem name | Dependencies / reuse notes | Adaptation risk |
|---|---|---|---|---|
| light adaptation | `Theorems/Thm_Algebra_trace_inv_mul_derivation_eq_inv_norm_mul_derivation_norm.lean` | `Algebra.trace_inv_mul_derivation_eq_inv_norm_mul_derivation_norm` | Imports `Mathlib.RingTheory.Norm.Basic`, `Mathlib.RingTheory.Trace.Basic`, `Mathlib.RingTheory.Derivation.Basic`, and proves a trace/norm identity for derivations along an algebra tower. The theorem is algebraic, not geometric, but the conclusion is a clean reusable identity template for “derivation commutes with extension” style arguments. | Moderate. It is reusable as a lemma schema, but the downstream environment must still supply the matching tower `R ⟶ F ⟶ F'`, the compatibility hypothesis `hd`, and the same trace/norm normalization. |
| light adaptation | `Theorems/Thm_AlgebraicCurve_Place_continuous_restrictAlong.lean` | `AlgebraicCurve.Place.continuous_restrictAlong` | Imports `Definitions.Def_AlgebraicCurve_Correspondence`, `Definitions.Def_AlgebraicCurve_IsCurveOver`, `Definitions.Def_AlgebraicCurve_PlaceEvaluation`, and proves continuity of `w ↦ w.restrictAlong φ hφ` for curve places under a heavy meromorphic-at/ord hypothesis on both source and target curves. | Moderate to high. The continuity statement is reusable as a transport theorem, but the ambient objects are deeply curve-specific and the hypotheses are meromorphic, charted, compact, and T2 conditions on `Place ℂ F`. |
| light adaptation | `Theorems/Thm_AlgebraicCurve_Place_derivation_apply_eq_diffCoeff_D_mul.lean` | `AlgebraicCurve.Place.derivation_apply_eq_diffCoeff_D_mul` | Imports `Definitions.Def_AlgebraicCurve_Differentials` and proves a derivation evaluation formula `δ f = Place.diffCoeff t (KaehlerDifferential.D K F f) * δ t` under a valuation-order-1 hypothesis. This is a highly local coefficient identity, but its derivative/derivation seam is exactly the kind of bridge one might want in a local calculus adapter. | Moderate. The statement is very specific to `Place`, `ord`, and `diffCoeff`; it can seed a local adapter, but it is not portable as a general derivative lemma without rebuilding the ambient valuation geometry. |
| light adaptation | `Theorems/Thm_AlgebraicCurve_Place_exists_sub_algebraMap_evalAt_eq_mul_of_derivative_evalEval_ne_zero.lean` | `AlgebraicCurve.Place.exists_sub_algebraMap_evalAt_eq_mul_of_derivative_evalEval_ne_zero` | Imports `Definitions.Def_AlgebraicCurve_PlaceEvaluation` and proves a divisibility-style factorization from a nonzero evaluated derivative: `y - algebraMap K F (v.evalAt y) = h * (z - algebraMap K F (v.evalAt z))`. This is a root-separation/implicit-function-flavored statement built from the derivative nonvanishing hypothesis. | Moderate. The shape is reusable as a local factorization lemma, but the proof is anchored to rational places, valuation subrings, and polynomial `evalEval` infrastructure. |

## Architecture only

| Level | Exact relative path | Namespace / theorem name | Dependencies / reuse notes | Adaptation risk |
|---|---|---|---|---|
| architecture only | `Theorems/Thm_AlgebraicGeometry_exists_tendsto_appLE_of_isProper_of_smoothOfRelativeDimension_one_complex.lean` | `AlgebraicGeometry.exists_tendsto_appLE_of_isProper_of_smoothOfRelativeDimension_one_complex` | Imports `Definitions.Def_CerednikDrinfeld_QMModuli` and a large number of `AlgebraicCurve`, `ModularCurve`, and `Topology` simp/instance overrides. The theorem is a compactness/properness-driven `Tendsto` extraction over `SchemeHomOver`, with a strict monotone subsequence and eventual section control. | High. This is useful as a proof-architecture pattern for limit extraction and subsequence control, but the ambient scheme/moduli stack is too specialized to lift directly into a generic calculus library. |
| architecture only | `Definitions/Def_Dieudonne_WittHomColimit.lean` | `Deformation.TruncWitt.verschiebungIter`, `shiftLE`, `shiftLE_truncate`, `coeff_shiftLE`, `shiftLE_refl`, `shiftLE_shiftLE`, `shiftLE_succ`, `shiftLE_injective`, `map_shiftLE`, `frobeniusFun_shiftLE`, `verschiebung_shiftLE`, `verschiebung_iterate_eq_zero` | This is not calculus in the analytic sense, but it is a genuine limit/transport infrastructure file: iterated Verschiebung, compatibility of truncation lifts, functoriality under ring maps, and stabilization identities. It is good evidence for an inverse-system API pattern. | High. The file is algebraic/Witt-vector infrastructure, not analytic limit theory. Reuse should stay at the level of transport/refinement shape, not theorem content. |
| architecture only | `Theorems/Thm_AlgebraicCurve_coeffIn_local_calculus.lean` | `AlgebraicCurve.coeffIn_local_calculus` | The path name suggests a local-calculus helper in the curve setting; even without promoting any statement here, it sits in the exact seam where coefficient extraction and local analytic reasoning are wired together. | High. Treat as a namespace/organization clue only unless the downstream project also uses the same local curve calculus apparatus. |

## What I would actually carry forward

If the target project needs a calculus-adjacent reusable kernel, the best acquisition order is:

1. `Algebra.exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential`
2. `Algebra.exists_bijOn_eval_differentiableOn_of_smooth_of_kaehlerDifferential`
3. `Algebra.trace_inv_mul_derivation_eq_inv_norm_mul_derivation_norm`
4. `AlgebraicCurve.Place.continuous_restrictAlong`
5. `AlgebraicCurve.Place.derivation_apply_eq_diffCoeff_D_mul`
6. `AlgebraicCurve.Place.exists_sub_algebraMap_evalAt_eq_mul_of_derivative_evalEval_ne_zero`
7. `AlgebraicGeometry.exists_tendsto_appLE_of_isProper_of_smoothOfRelativeDimension_one_complex` only for proof-architecture reference, not theorem transfer

## Boundary note

I excluded the bulk of the FLT arithmetic/core number-theory statements, even when their filenames mention `continuous`, `smooth`, `integral`, or `limit`, because they are not reusable as calculus infrastructure without importing the surrounding number-field package and its proof obligations.

No authoritative state, registry entry, or upstream source was changed by this review.
