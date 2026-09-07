---
kind: review_result
task_id: T-FLT-TRANSPORT-ADAPTER
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-FLT-TRANSPORT-ADAPTER transport adapter audit

Scope: read-only scan of `upstream/anthropics-fermats-last-theorem` at fixed commit `aa2d8b3` for non-number-theoretic adapters involving continuous maps, linear equivalences, pairing transport, representations, and coordinate changes. I did not run a full build, and I did not change `state`, `registry`, or `task_queue`.

## 1. Best-fit adapters for immediate sidecar use

These are the cleanest non-number-theoretic transport adapters I found. They are explicit about their premises, preserve provenance, and can be isolated into a small Route-B/PDE sidecar if needed.

### 1.1 `Theorems/Thm_AlgebraicGeometry_RiemannForm_transportIso_tensorObj.lean`

- Exact statement/path: `theorem AlgebraicGeometry.RiemannForm.transportIso_tensorObj`
- Imports: `Definitions.Def_AlgebraicGeometry_RiemannForm`, `Definitions.Def_AlgebraicGeometry_ModulesPullbackMonoidalV2`, `P2M.Util`, `P2M.Sol.S_AlgebraicGeometry_RiemannForm_transportIso_tensorObj`
- Core statement: transport along `h : T ≫ g = g` distributes over tensor objects via pullback functoriality and the tensor pullback isomorphisms.
- Key hypotheses: `A : Scheme`, `T g : A ⟶ A`, equality `T ≫ g = g`, arbitrary modules `M M' : A.Modules`.
- Route-B/PDE risk: low. This is categorical transport, not number-theoretic, and the only real risk is overgeneralizing the transport identity beyond the stated commutative diagram.
- Provenance/license: file is a short wrapper over a `P2M.Sol` proof; repository-wide attribution and license are Apache 2.0 per `ATTRIBUTION.md` and `LICENSE`.
- Minimal sidecar suggestion: keep as a tiny transport lemma sidecar, with one theorem per commutative-square transport rule and no extra semantic claims.

### 1.2 `Theorems/Thm_AlgebraicCurve_exists_linearEquiv_structureSheafH1_cechH1.lean`

- Exact statement/path: `theorem AlgebraicCurve.exists_linearEquiv_structureSheafH1_cechH1`
- Imports: `Mathlib`, `Definitions.Def_AlgebraicCurve_DivisorClassGroup`, `Definitions.Def_AlgebraicCurve_Repartitions`, `Definitions.Def_AlgebraicCurve_CurveModel`, `Definitions.Def_AlgebraicGeometry_TwoChartCech`, `Definitions.Def_AlgebraicGeometry_TwoAffineOpenCover`, `Definitions.Def_AlgebraicCurve_CechSectionsOfDivisor`, `Definitions.Def_AlgebraicCurve_PlacesOf`, `P2M.Util`, `P2M.Sol.S_AlgebraicCurve_exists_linearEquiv_structureSheafH1_cechH1`
- Core statement: under a two-affine-open-cover setup of a smooth separated integral curve over a field, the H1 of the structure sheaf is linearly equivalent to the Čech H1 quotient, with an explicit compatibility formula on representatives.
- Key hypotheses: `[Field K]`, `C : Scheme`, `𝒱 : C.TwoAffineOpenCover`, `c : C ⟶ Spec (CommRingCat.of K)`, `[IsIntegral C]`, `[IsSeparated c]`, `[SmoothOfRelativeDimension 1 c]`, plus nonemptiness of both cover pieces.
- Route-B/PDE risk: medium. The transport is mathematically clean, but the ambient geometry is specialized to algebraic curves and cohomology; do not reuse it as if it were a generic functional-analytic or PDE coordinate change.
- Provenance/license: wrapper over an upstream FLT/P2M solution file; Apache 2.0 according to repository attribution.
- Minimal sidecar suggestion: isolate as a cohomology transport sidecar with explicit curve/cover hypotheses and a strict “algebraic geometry only” boundary.

### 1.3 `Theorems/Thm_CuspForm_HeckeGaloisRepDatum_exists_algHom_comp_eq_and_linearEquiv_semilinear_auxLevel_ML.lean`

- Exact statement/path: `theorem CuspForm.HeckeGaloisRepDatum.exists_algHom_comp_eq_and_linearEquiv_semilinear_auxLevel_ML`
- Imports: `Definitions.Def_CuspForm_HeckeLocal`, `Definitions.Def_CuspForm_HeckeGaloisRepDatum`, `Definitions.Def_CuspForm_AuxLevelHeckeModule`, `Definitions.Def_GaloisRep_DeformationRingData`, `Definitions.Def_GaloisRep_LocalConditions`, `Definitions.Def_GaloisRep_Flat`, `Definitions.Def_GaloisRep_Residual`, `Definitions.Def_GaloisRep_ResidualEquiv`, `P2M.Util`, `P2M.Sol.S_CuspForm_HeckeGaloisRepDatum_exists_algHom_comp_eq_and_linearEquiv_semilinear_auxLevel_ML`
- Core statement: from a Hecke/Galois datum, an admissible deformation ring map, and a compatible auxiliary level module isomorphism, one gets a corrected algebra homomorphism factorization and a semilinear linear equivalence `Θ`.
- Key hypotheses: DVR/adic-complete residue-field setup, `ρbar.IsAbsolutelyIrreducible`, prime-level exclusions and squarefree support conditions, local conditions at `p`, a local hom `φ`, a local deformation datum `Dmin`, and an auxiliary linear equivalence `eML` compatible with Hecke action.
- Route-B/PDE risk: medium-low. This is a transport/rigidity lemma, but it lives in arithmetic deformation theory; the risk is not in the transport algebra itself but in importing its arithmetic side conditions into unrelated continuous-map work.
- Provenance/license: wrapper over `P2M.Sol` with repository Apache 2.0 provenance.
- Minimal sidecar suggestion: use a “representation transport” sidecar that records the exact algebraic hypotheses and keeps the `Θ` conclusion separate from any downstream modularity or lifting claim.

### 1.4 `Theorems/Thm_AlgebraicCurve_Pic0_torsion_exists_addMonoidHom_eval_eq_pairing.lean`

- Exact statement/path: `theorem AlgebraicCurve.Pic0.torsion.exists_addMonoidHom_eval_eq_pairing`
- Imports: `Definitions.Def_AlgebraicCurve_WeilDatum`, `Definitions.Def_AlgebraicCurve_JacobianH1Autoduality`, `P2M.Util`, `P2M.Sol.S_AlgebraicCurve_Pic0_torsion_exists_addMonoidHom_eval_eq_pairing`
- Core statement: under Weil reciprocity, a constancy condition, and a moving-support hypothesis, one can build an additive homomorphism from torsion Picard points to the multiplicative Hom target so that evaluation matches the Weil pairing.
- Key hypotheses: fields `K F`, `Algebra K F`, `NeZero n`, `HasPrincipalDivisors K F`, `WeilReciprocity K F`, the strong constancy axiom on functions with zero place-valuation, and a moving-divisor support condition.
- Route-B/PDE risk: medium. The pairing transport is structurally reusable, but it is genuinely algebro-geometric and divisor-theoretic; it should not be reinterpreted as a generic bilinear-form transport or continuous pairing on analytic spaces.
- Provenance/license: wrapper over `P2M.Sol`; Apache 2.0 per repository attribution.
- Minimal sidecar suggestion: a “pairing transport” sidecar that keeps the divisor/Weil reciprocity premises explicit and treats the hom construction as provenance-bearing, not canonical outside this context.

## 2. Usable but with stronger boundary control

These are reusable as transport adapters, but the ambient theory is more entangled with FLT/representation-theoretic plumbing, so I would keep them separate from any Route-B/PDE-facing adapter until the sidecar contract is explicit.

### 2.1 `Theorems/Thm_GaloisRepAdic_IsEquiv_isUnipotentOnInertiaAt.lean`

- Exact statement/path: `theorem GaloisRepAdic.IsEquiv.isUnipotentOnInertiaAt`
- Imports: `Definitions.Def_GaloisRep_DeformationRingData`, `Definitions.Def_CuspForm_HeckeGaloisRepDatum`, `Definitions.Def_CuspForm_HeckeLocal`, `Definitions.Def_CuspForm_IntegralStructure`, `Definitions.Def_FLTPrelim_ModularRep`, `Definitions.Def_GaloisRep_LocalConditions`, `Definitions.Def_GaloisRep_Flat`, `Definitions.Def_EllipticCurve_TateModule`, `Definitions.Def_GaloisRep_Residual`, `Definitions.Def_GaloisRep_ResidualEquiv`, `Definitions.Def_Algebra_PatchingDatum`, `Mathlib.RingTheory.Ideal.Cotangent`, `Mathlib.RingTheory.Length`, `P2M.Util`, `P2M.Sol.S_GaloisRepAdic_IsEquiv_isUnipotentOnInertiaAt`
- Core statement: if two adic Galois representations are equivalent, unipotence on inertia at `q` transfers from one to the other.
- Key hypotheses: `{𝒪 A : Type}` with `[CommRing 𝒪]`, `[CommRing A]`, `[IsLocalRing A]`, `[Algebra 𝒪 A]`, `q : ℕ`, `ρ ρ' : GaloisRepAdic A`, and an equivalence witness `h : ρ.IsEquiv ρ'`.
- Route-B/PDE risk: medium-high. This is a clean equivalence transport, but the meaning of `IsUnipotentOnInertiaAt` is specialized arithmetic structure; do not pull it into a PDE sidecar unless the arithmetic semantics stay quarantined.
- Provenance/license: direct `P2M.Sol` wrapper, Apache 2.0 repository license.
- Minimal sidecar suggestion: if needed, place it in a strict “representation equivalence transport” sidecar with no claim about analytical continuity or PDE invariants.

### 2.2 `Theorems/Thm_WeierstrassCurve_exists_variableChange_map_eq_and_reduceHom_vcFun_eq.lean`

- Exact statement/path: `theorem WeierstrassCurve.exists_variableChange_map_eq_and_reduceHom_vcFun_eq`
- Imports: `Mathlib`, `Definitions.Def_WeierstrassCurve_VariableChangePointEquiv`, `Definitions.Def_WeierstrassCurve_ReduceHom`, `P2M.Util`, `P2M.Sol.S_WeierstrassCurve_exists_variableChange_map_eq_and_reduceHom_vcFun_eq`
- Core statement: given a variable change over a valuation subring and a nondegenerate discriminant condition on the residue reductions, one can lift a compatible variable change from the residue field and compare `reduceHom` with the induced `vcFun` point transport.
- Key hypotheses: field `L`, valuation subring `A`, decidable equality on `L` and `ResidueField A`, discriminant nonvanishing after reduction for both curves, and a point-level equality `hC : C • W₁.map A.subtype = W₂.map A.subtype`.
- Route-B/PDE risk: medium. This is the canonical coordinate-change adapter, but it is curve-specific and depends on a nonzero discriminant gate; the main risk is overusing it as a generic “change of variables” lemma.
- Provenance/license: wrapper over `P2M.Sol`; Apache 2.0 repository provenance.
- Minimal sidecar suggestion: a dedicated coordinate-change sidecar with a hard rule that the theorem only transports Weierstrass data through valuation-residue compatibility.

### 2.3 `Theorems/Thm_FreyPackage_freyGaloisRep_isUnramifiedAt.lean`

- Exact statement/path: `theorem FreyPackage.freyGaloisRep_isUnramifiedAt`
- Imports: `Mathlib`, `Definitions.Def_FLTPrelim_FreyPackage`, `Definitions.Def_FLTPrelim_GaloisRep`, `Definitions.Def_FLTPrelim_Modularity`, `Definitions.Def_FLTPrelim_ModularRep`, `Definitions.Def_FLTPrelim_Ramification`, `Definitions.Def_FLTPrelim_CofixedLine`, `P2M.Util`, `P2M.Sol.S_FreyPackage_freyGaloisRep_isUnramifiedAt`
- Core statement: a Frey package gives an unramified Galois representation at primes `q` satisfying the stated exclusions.
- Key hypotheses: `P : FreyPackage`, `q : ℕ`, `hq : q.Prime`, `hq2 : q ≠ 2`, `hqp : q ≠ P.p`.
- Route-B/PDE risk: high. It is representation transport in the FLT arithmetic core; it is not a PDE-adapter candidate and should stay outside any Route-B/PDE-facing abstraction except as provenance or comparison material.
- Provenance/license: wrapper over `P2M.Sol` and intermediate FLT port material; repository license is Apache 2.0, and the file family is covered by `ATTRIBUTION.md`.
- Minimal sidecar suggestion: keep only as a quarantined arithmetic reference sidecar, not as a reusable adapter for current Route-B/PDE work.

## 3. Excluded or only weakly relevant

These files are adjacent to the requested theme but are not good candidates for a Route-B/PDE adapter boundary.

- Pure number-theory or modularity plumbing with no clean transport interface for the target workflow.
- `Theorems/Thm_FreyPackage_freyGaloisRep_isUnramifiedAt.lean` falls here for the current use case.
- Anything whose main claim is a classical FLT arithmetic step rather than a transport, equivalence, or coordinate-change rule.

## Bottom line

If we want the smallest safe Route-B/PDE-facing sidecar, I would start with:

1. `RiemannForm.transportIso_tensorObj` for categorical transport,
2. `exists_linearEquiv_structureSheafH1_cechH1` for a genuine `linearEquiv`,
3. `exists_addMonoidHom_eval_eq_pairing` for pairing transport,
4. `exists_variableChange_map_eq_and_reduceHom_vcFun_eq` for coordinate change,
5. `exists_algHom_comp_eq_and_linearEquiv_semilinear_auxLevel_ML` only if we need the representation-theoretic bridge.

Everything else I inspected should stay in a separate arithmetic/FLT bucket unless the sidecar contract explicitly allows that scope.
