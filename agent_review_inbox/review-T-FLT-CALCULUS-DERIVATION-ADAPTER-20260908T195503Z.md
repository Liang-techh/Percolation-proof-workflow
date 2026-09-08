---
kind: review_result
review_id: review-T-FLT-CALCULUS-DERIVATION-ADAPTER-20260908T195503Z
task_id: T-FLT-CALCULUS-DERIVATION-ADAPTER-20260908
source_agent: Codex-FLT-derivation-adapter
created_at: 2026-09-08T19:55:03Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: SOURCE_BOUND_MINIMAL_COTANGENT_HANDOFF_NOT_COMPILED
selected_api: Algebra.PointDerivations.map_comp
abstract_contract_classification: 1
routeb_adapter_classification: 2
lean_compile_status: not_run
lean_run: false
lake_run: false
kernel_checked: false
axioms_checked: false
comparator_accepted: false
routeb_source_binding_proven: false
routeb_chain_rule_proven: false
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
shared_scripts_mutation: false
requested_action: retain pending; hand off only the generic API and cotangent specialization to an authorized pinned runner
---

# D1: linear post-composition as a minimal cotangent adapter

Selected one API family: `Algebra.PointDerivations.map_comp`, with its necessary
`PointDerivations` definition, `map` and `map_apply_coe` support. It is the best
small transferable candidate in this bounded scan, not a global optimality claim.
It transports an already established point derivation through a linear map on
its **values**. It does not construct a derivative or change the observable
algebra/evaluation point. The useful next step beyond the existing D1 handoff
is the fixed cotangent-map specialization below, with an explicit analytic
commuting-square obligation.

Only this new review is written. No local or remote Lean/Lake, dependency build,
comparator or physical simulation was run; no `.lean` or compiled artifact was
created. All mathematical handoff statements below are statically reviewed,
**uncompiled**, and are not Route-B proofs.

## Inspected inputs and source identity

Read the three current files in `examples/anthropic_flt_derivation_adapter`,
`artifacts/anthropic_fermats_intake/{PROVENANCE.md,catalog.json}`, the D1 section
of `review-T-FLT-DERIVATION-CALCULUS-SCAN-20260908T182536Z.md`, and the older
`review-FLT-derivation-calculus.md`. Independently retrieved the complete
selected source from the Git object database, rather than trusting old receipts.

Repository: https://github.com/anthropics/fermats-last-theorem

Local snapshot: `artifacts/anthropic_fermats_last_theorem`; current HEAD and
the explicitly inspected commit are both
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`.

| Pinned source | Git blob SHA-1 | Raw Git-object SHA-256 |
|---|---|---|
| Definitions/Def_Algebra_PointDerivations.lean | a6a95f7e3170eb079c42c30deaa06a562d42f53d | e54ef18402112ab66421a3eccb0a8f30ea9402cc167be91c6770da0c43d144cd |
| lean-toolchain | a8afa7d1b02d96f0671eba854a8dc4b416beb473 | 3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71 |
| lake-manifest.json | 2b5a9ec02a1d760170e6034ebcd43e72fa9a42c3 | 435fe2ab2550e2b82c0a93fd421c96d197d6dd55bc739481e2a4a07e04b979bf |

[Immutable source declaration](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/Definitions/Def_Algebra_PointDerivations.lean#L58).
Evidence here is local Git-object retrieval, not an assertion that the web page
was live-checked. The source file is absent from this sparse working tree;
an initial filesystem hash check failed for that reason. `git show commit:path`
succeeded, and SHA-256 was computed from its raw stdout bytes without decoding
or newline conversion. No checkout or reconstructed source file was needed.

The source pins Lean `leanprover/lean4:v4.33.1` and Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d` (manifest rev and inputRev).
Only `import Mathlib` occurs in the selected 64-line file; no P2M imports.
This broad import does not demonstrate a minimal transitive dependency closure.

License: Apache-2.0; NOTICE says Copyright 2026 Anthropic, PBC and preserves
third-party notices. Exact selected filename was not found in ATTRIBUTION.md;
that absence does not prove original authorship, and NOTICE explicitly warns
that small Mathlib restatements are not individually traced. Preserve NOTICE,
ATTRIBUTION and Mathlib provenance in any later port. Their pinned Git blobs:
NOTICE `5411679f5f1878e72d1622a88c54b8fbb3f29282`, ATTRIBUTION.md
`ac80b9de81c8132d3bccc57f13463b293a340422`.

## Exact declaration and all assumptions

Source lines 5, 9-11 and 25-26 supply the ambient parameters:

```lean
universe u v w w'
-- k : Type u, A : Type v
-- [Field k] [CommRing A] [Algebra k A]
-- ev : A →+* k
-- M : Type w, M' : Type w'
-- [AddCommGroup M] [Module k M]
-- [AddCommGroup M'] [Module k M']
```

`Algebra.PointDerivations k A ev M : Submodule k (A →ₗ[k] M)` has carrier
exactly `{D | ∀ a b : A, D (a*b) = ev a • D b + ev b • D a}`.
Thus D is already k-linear and already satisfies the evaluation-Leibniz law.

Necessary API, lines 47-53:

```lean
def map (ev : A →+* k) (φ : M →ₗ[k] M') :
    ↥(PointDerivations k A ev M) →ₗ[k] ↥(PointDerivations k A ev M')

@[simp] theorem map_apply_coe (ev : A →+* k) (φ : M →ₗ[k] M')
    (D : ↥(PointDerivations k A ev M)) (a : A) :
    (map ev φ D : A →ₗ[k] M') a = φ (D.1 a)
```

Selected theorem, lines 58-60, in namespace `Algebra.PointDerivations`:

```lean
theorem map_comp {M'' : Type w} [AddCommGroup M''] [Module k M'']
    (ev : A →+* k) (φ : M →ₗ[k] M') (ψ : M' →ₗ[k] M'')
    (D : ↥(PointDerivations k A ev M)) :
    map ev (ψ.comp φ) D = map ev ψ (map ev φ D) := by
  ext a; rfl
```

Important exactness details:

- M'' shares **w** with M in the source; generalizing to a new universe would
  be a separately checked adaptation, not the verbatim signature.
- ev is a RingHom, not a supplied AlgHom. The additional scalar-compatibility
  assumption `ev.comp (algebraMap k A) = RingHom.id k` belongs to `ev_smul`
  at line 44, not to `map`, `map_apply_coe` or `map_comp`.
- No norm, topology, finite dimension, completeness, differentiability,
  invertibility, number field or positive characteristic is assumed.
- `map` sends D to `φ.comp D.1`; its membership proof uses linear map add/smul
  preservation and D's supplied Leibniz law. `map_comp` compares these values
  by extensionality. This proof-text inspection is not a kernel/axiom audit.

## Classification and bounded alternatives

1 = exact abstract contract reusable; 2 = light port/specialization;
3 = architecture only for the requested physical target. None means compiled.

Selected family: **1 at the abstract algebra API, 2 for a Route-B adapter**.
This refines, rather than silently overwrites, the existing D1 packet's `1`:
the physical derivative instance and target-pin compilation are not supplied.
No claim that an algebraic post-composition theorem alone gives graph regularity.

As a discriminating comparison, inspected the opening of
`Definitions/Def_AutomorphicForm_ArchDerivCasimirComplexAPI.lean` at the same
commit, blob `9ecba5988f7cdaa75e13459f8a2d8d660af25fca`.
Its generic `hasDerivAt_ofReal_mul_const (c : ℂ) (t : ℝ)` proves
`HasDerivAt (fun s : ℝ => (s : ℂ)*c) c t` directly from Mathlib's ofReal CLM.
That exact scalar fact is class 1 abstractly, but adds little over current
Mathlib for this task; importing the archimedean/automorphic module is not a
minimal handoff. Its specialized flow is not the Route-B flow. The intake's
complex algebraic chart candidate remains class 3 for Route-B, not an analytic
chart witness. No pure-number-theoretic theorem was acquired or ported.

## The useful new specialization: cotangent post-composition

Take real normed spaces E, Z, Y and fixed continuous linear maps
`L : Z →L[ℝ] E`, `H : Y →L[ℝ] Z`. Set `E* = E →L[ℝ] ℝ` and similarly Z*,Y*.
Define the linear value-map Φ_L : E* →ₗ[ℝ] Z* by Φ_L(ℓ)=ℓ.comp L.
Its add/smul laws follow by pointwise linearity; continuity as a map on the
dual is not required by the FLT API (any norm bound is a separate conclusion).

For any independently established `D : PointDerivations ℝ A ev E*`, the
selected API returns `map ev Φ_L D : PointDerivations ℝ A ev Z*`, with

```text
(map ev Φ_L D)(a)(v) = D(a)(L(v))
Φ_H ∘ Φ_L = Φ_(L ∘ H)
map ev Φ_(L ∘ H) D = map ev Φ_H (map ev Φ_L D)
```

The order L∘H is essential. This is a genuine cotangent-value transport, not
an input-coordinate theorem: the algebra A and ev are unchanged on both sides.
No polynomial-only limitation is intrinsic to this abstract API, but neither
does it provide sin/cos differentiability for an analytic DAG.

For a physical use, choose an observable algebra A with a real AlgHom
ρ : A →ₐ[ℝ] (E → ℝ), and ev(a)=ρ(a)(x). To set
D_x(a)=fderiv ℝ (ρ(a)) x, first supply differentiability of **every** represented
observable at x and prove linearity and evaluation-Leibniz; do not rely on the
totalized `fderiv` value at nondifferentiable functions. Then identify D_x with
the source-bound derivative being consumed by Route-B.

For a chart T : Z→E, x=T(z), L=DT(z), the separate analytic square is

```text
D_z(ρ(a) ∘ T) = Φ_L(D_x(a)),  x=T(z).
```

This changes observable functions and evaluation point, so **map_comp does not
prove it**. It needs HasFDerivAt T L z and HasFDerivAt (ρ(a)) (D_x(a)) (T z).
Current Mathlib already supplies the applicable chain rule; do not attribute
that analytic theorem to FLT. A pointwise choice L=DT(z) is permitted; what is
not permitted is differentiating the transported field while omitting the
derivative of a varying L. Moving charts require time/space derivative terms.

## Current target pin and actual Route-B gap

Freshly read `examples/local_fkg/lean-toolchain`: Lean **4.32.0**.
Its current lake-manifest Mathlib rev/inputRev and package Git HEAD agree at
`81a5d257c8e410db227a6665ed08f64fea08e997`. This differs from the older intake's
`0df444a360eaa60ab8c11dca51a86af692955474`; do not carry that old target pin into
a new receipt. Manifest raw SHA-256:
`6cad04cdeb731b8af3594767512923ac9b9fe7e00808f91ddcb30c846e3891f3`.
No binary or build-cache compatibility was checked.

At target commit 81a5d257..., `Mathlib/Analysis/Calculus/FDeriv/Comp.lean`, blob
`b569401f8f2ceb72d072d6b088af2630a164d1ed`, lines 105-107 has
`HasFDerivAt.comp`: for a nontrivially normed field k, normed additive groups
and k-normed spaces E,F,G, f:E→F, g:F→G, continuous linear derivatives f',g',
x:E, hg:HasFDerivAt g g' (f x) and hf:HasFDerivAt f f' x, the result is
`HasFDerivAt (g ∘ f) (g'.comp f') x`. Lines 74-78 give the within-set variant
with the additional MapsTo f s t premise. These are Mathlib, not FLT imports.
Source was checked via git show after observing LF Git-object/CRLF working-file
hash differences; filtered working-file hash agrees with that blob.

P5's verify.sh defaults LAKE_ROOT to local_fkg and its sidecar pins Lean 4.32.0.
Read `P5MovingMetricContraction.lean` at raw SHA-256
`e5950ad1b8ac474ddc814dd3fc993f68de128b5028d11726345e2b9ce3a44468`:
`physical_variation_rate_identity` lines 92-100 **assumes hdV**;
`moving_metric_contraction_tensor_congruence` lines 110-134 **assumes hk1/hk2**.
The selected D1 API discharges none of those actual derivative/covariance
premises. Chart regularity, source identity, material metric and moving-frame
terms, full-domain hypotheses, remainder/error bounds, physical contraction
and trajectory/flowpipe coverage remain separate. A generic API receipt cannot
close those Route-B leaves or establish a continuous-PDE theorem.

## Minimal handoff, not dispatched or compiled

An authorized runner can attempt exactly this small unit:

1. Pin source commit/blob above and the agreed target Lean/Mathlib pair. Retain
   attribution. Place the PointDerivations definition and necessary map family
   in an isolated namespace; do not import the whole FLT tree. Determine and
   record actual imports instead of claiming `import Mathlib` is minimal.
2. Preserve the original map_comp signature as a comparator target. Add only
   Φ_L, its evaluation formula and the correctly ordered two-map cotangent
   composition statement. No physical D or analytic chart is to be fabricated.
3. Return source/adapter/import hashes, toolchain and package commit identities,
   full command/exit/stdout/stderr, declaration-level #print axioms without
   sorryAx, and exact statement-comparator evidence for the generic contract.
   Include a separate comparison for the Φ_L specialization, not a comparison
   that assumes the desired Route-B conclusion.
4. A successful generic receipt still stays pending for Route-B until the
   actual observable algebra, evaluation, derivative and analytic square are
   independently supplied. Do not modify registry or state as part of this unit.

Present handoff has no proof artifact, no compilation receipt and no comparator
acceptance. Static checks establish exact source identity, declared assumptions,
composition direction and an actionable target seam only. Existing D1 metadata,
intake/catalog, review files and shared scripts were not edited. Concurrent
collaboration-board/queue and other agents' source changes were observed and
left untouched.
