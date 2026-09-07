---
kind: review_result
task_id: T-FLT-DERIV-CALC
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-FLT-DERIV-CALC review: derivation / calculus / continuous / integral / limit reuse scan

Inspected commit: `aa2d8b3` in `upstream/anthropics-fermats-last-theorem`.

Scope filtered to `Definitions/` and `Theorems/` entries whose file names or internal symbols are tied to `derivation`, `calculus`, `derivative`, `smooth`, `continuous`, `integral`, or `limit`. I did not run a full compile.

## Direct reuse

- `Definitions/Def_Algebra_PointDerivations.lean`
  - Namespace / theorem names: `Algebra.PointDerivations`, `PointDerivations.mem_iff`, `PointDerivations.apply_mul`, `PointDerivations.apply_one`, `PointDerivations.apply_algebraMap`, `PointDerivations.map`, `PointDerivations.map_id`, `PointDerivations.map_comp`.
  - Why reusable: this is clean algebraic infrastructure for pointwise derivations at an evaluation homomorphism; it is generic in `k`, `A`, and target module `M`.
  - Dependencies: only `Mathlib`, `Field`, `CommRing`, `Algebra`, `LinearMap`, `Submodule`, and the evaluation map `ev : A →+* k`.
  - Adaptation risk: low. The interface is abstract enough to port as-is if the target project needs point-derivation bookkeeping.

- `Definitions/Def_Analysis_HalfLineIntercept.lean`
  - Namespace / theorem names: `HalfLine.slope`, `HalfLine.intercept`, `HalfLine.slope_eq_of_forall_le_eq_add_mul`, `HalfLine.intercept_eq_of_forall_le_eq_add_mul`, `HalfLine.eq_and_eq_of_forall_le_eq_add_mul`.
  - Why reusable: this packages eventual affine asymptotics on `ℝ → ℂ` into a compact limit-based API.
  - Dependencies: `Mathlib.Analysis.Complex.Basic`, `Filter.limUnder`, `tendsto_nhds_of_eventually_eq`, `ring`.
  - Adaptation risk: low to medium. The shape is generic, but the codomain is specialized to `ℂ`; if the target wants another normed ring, the proofs need a small codomain-generalization.

- `Definitions/Def_AlgebraicCurve_Differentials.lean`
  - Namespace / theorem names: `AlgebraicCurve.Place.dCoordFn`, `Place.ord_dCoordFn`, `Place.dCoord_eq_D_dCoordFn`, `Place.chartRead`, `Place.chartRead_apply`, `Place.readDifferential`, `Place.readDifferential_apply`, `Place.IsPrimitiveAlong`, `Place.pathIntegral`, `Place.pathIntegral_def`, `Place.abelJacobiVec`, `Place.abelJacobiVec_def`, `Place.abelJacobiDiv`, `Place.abelJacobiDiv_single`, `Place.abelJacobiDiv_apply`, `Place.pathPeriodLattice`, `Place.mem_pathPeriodLattice_of_loop`.
  - Why reusable: this is a self-contained differential-reading / path-integral / Abel-Jacobi interface with explicit definitional equalities.
  - Dependencies: `Mathlib`, `Topology`, `Manifold`, `Place`, `Path`, `Ω[F⁄ℂ]`, and choice-based classical witnesses.
  - Adaptation risk: medium. The definitions are clean, but they are embedded in a place/curve geometry stack, so porting outside that geometry would require replacing the ambient objects, not just renaming.

- `Theorems/Thm_contDiff_top_and_hasCompactSupport_integral_comp_affine.lean`
  - Namespace / theorem name: `contDiff_top_and_hasCompactSupport_integral_comp_affine`.
  - Why reusable: this is a generic smoothness-under-integral theorem with compact support and a properness-type bound.
  - Dependencies: finite-dimensional normed spaces over `ℝ`, `MeasureTheory`, `ContDiff`, `HasCompactSupport`, `Continuous`, `IsFiniteMeasure`, and a coercive growth bound `hproper`.
  - Adaptation risk: low to medium. The theorem is broad, but the proof is a `p2m_exact_reverting` wrapper, so reuse is more about the statement shape than the proof body.

- `Theorems/Thm_Real_norm_le_and_norm_integral_cexp_sum_mul_le_mul_prod_inv_one_add_abs_sq_of_contDiff.lean` and `Theorems/Thm_Real_norm_le_and_norm_integral_cexp_mul_le_mul_inv_one_add_abs_sq_of_piecewise_contDiff_two.lean`
  - Why reusable: these are analytic estimate templates for oscillatory integrals under differentiability hypotheses.
  - Dependencies: `ContDiff`, `integral`, decay bounds, and real/complex norm control.
  - Adaptation risk: medium. They are likely useful as pattern templates, but the exact integrands and decay structure are specialized.

## Light adaptation

- `Theorems/Thm_AlgebraicCurve_Place_derivation_apply_eq_diffCoeff_D_mul.lean`
  - Namespace / theorem name: `AlgebraicCurve.Place.derivation_apply_eq_diffCoeff_D_mul`.
  - Why light adaptation: it gives a derivation evaluation identity in terms of `diffCoeff` and Kähler differential `D`, which is structurally reusable for local derivation calculations.
  - Dependencies: `Definitions.Def_AlgebraicCurve_Differentials`, `Place.diffCoeff`, `KaehlerDifferential.D`, `Derivation`, and algebraic-closure hypotheses on `F`.
  - Risk: medium. The theorem is tightly tied to algebraic curves and a chosen local parameter `t`, so the exact statement will need domain-specific adaptation.

- `Theorems/Thm_Algebra_trace_inv_mul_derivation_eq_inv_norm_mul_derivation_norm.lean`
  - Namespace / theorem name: `Algebra.trace_inv_mul_derivation_eq_inv_norm_mul_derivation_norm`.
  - Why light adaptation: this is a trace/norm/derivation compatibility identity, useful as a reusable algebraic lemma when moving derivations across finite extensions.
  - Dependencies: `RingTheory.Norm.Basic`, `RingTheory.Trace.Basic`, `RingTheory.Derivation.Basic`, and an extension-compatibility hypothesis `hd`.
  - Risk: medium. It is generic at the algebra level, but the proof is a direct `p2m_exact_reverting` shell and expects a very specific commutation hypothesis.

- `Theorems/Thm_UpperHalfPlane_integral_mul_eq_zero_of_periodic_of_tendsto_atImInfty.lean`
  - Namespace / theorem name: `UpperHalfPlane.integral_mul_eq_zero_of_periodic_of_tendsto_atImInfty`.
  - Why light adaptation: this is a useful contour/integral-vanishing pattern for periodic analytic functions with cusp decay.
  - Dependencies: `UpperHalfPlane`, `Complex`, `MeasureTheory`, periodicity, `Tendsto ω atImInfty`, holomorphicity on neighborhoods, and compact support cutoffs `p`, `ρ`.
  - Risk: medium to high. The theorem is analytically reusable, but its hypotheses are very tailored to the upper half-plane setup and a specific partition-of-unity style cutoff.

- `Theorems/Thm_AlgebraicCurve_Place_derivative_evalEval_evalAt_ne_zero_of_ord_sub_eq_one_of_forall_evalAt_ne.lean`
  - Why light adaptation: this is a local derivative nonvanishing criterion in the place/evaluation framework.
  - Dependencies: `Place.derivative`, `evalEval`, ord conditions, and separability-style assumptions.
  - Risk: medium. Likely reusable as a lemma template in local valuation/curve arguments, but not as a generic derivative fact.

## Architecture only

- `Theorems/Thm_AlgebraicCurve_Place_continuous_restrictAlong.lean`
  - Why architecture only: the file is about continuity of a restriction/transport map along places, but the payoff is bound to the place machinery rather than a general continuity infrastructure.
  - Dependencies: curve/place topology, charted spaces, `Continuous`, and specialized evaluation maps.
  - Risk: high if treated as a generic continuity lemma; the statement is best viewed as a local adapter around the place API.

- `Theorems/Thm_AlgebraicCurve_CurveModel_smoothOfRelativeDimension_genusFF_of_representsRelSubPic.lean`
  - Why architecture only: this is a high-level smoothness result in a curve-model pipeline, not a reusable smoothness tool.
  - Dependencies: algebraic geometry curve-model stack and representability hypotheses.
  - Risk: high for direct reuse; useful mainly as a map of how smoothness is threaded through the architecture.

- `Theorems/Thm_AlgebraicGeometry_Smooth_of_comp_of_smooth_of_surjective.lean`
  - Why architecture only: although it encodes a standard smoothness composition principle, in this repo it is used as a structural bridge inside a larger AG pipeline.
  - Dependencies: `Smooth`, `surjective`, and the ambient scheme/morphism framework.
  - Risk: medium. The mathematical content is standard, but the repo-specific role is mostly orchestration.

- `Theorems/Thm_groupCohomology_finiteDimensional_continuous_of_shortExact.lean`
  - Why architecture only: continuity is present in the name, but the theorem is really a cohomological finiteness transfer statement.
  - Dependencies: group cohomology, short exact sequences, and continuous module structures.
  - Risk: high for direct reuse outside the group-cohomology stack.

## Reuse summary

The strongest direct-reuse candidates are the abstract infrastructure files:

1. `Definitions/Def_Algebra_PointDerivations.lean`
2. `Definitions/Def_Analysis_HalfLineIntercept.lean`
3. `Definitions/Def_AlgebraicCurve_Differentials.lean`

The best light-adaptation candidates are the analytic/derivation theorem wrappers:

1. `Theorems/Thm_contDiff_top_and_hasCompactSupport_integral_comp_affine.lean`
2. `Theorems/Thm_Algebra_trace_inv_mul_derivation_eq_inv_norm_mul_derivation_norm.lean`
3. `Theorems/Thm_UpperHalfPlane_integral_mul_eq_zero_of_periodic_of_tendsto_atImInfty.lean`

The rest are mostly architectural markers for how the repo threads smoothness, continuity, and integration through specialized algebraic-geometry and arithmetic pipelines.

