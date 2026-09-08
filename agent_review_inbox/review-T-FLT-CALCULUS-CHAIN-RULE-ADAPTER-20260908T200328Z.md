---
kind: review_result
review_id: review-T-FLT-CALCULUS-CHAIN-RULE-ADAPTER-20260908T200328Z
task_id: T-FLT-CALCULUS-CHAIN-RULE-ADAPTER-20260908
source_agent: Codex-chain-rule-adapter
created_at: 2026-09-08T20:03:28Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: WITHIN_SET_CHAIN_RULE_AND_SOURCE_CONGRUENCE_HANDOFF_NOT_COMPILED
selected_api: HasFDerivWithinAt.comp
support_api: HasFDerivWithinAt.congr'
abstract_contract_classification: 1
routeb_adapter_classification: 2
lean_compile_status: not_run
lean_run: false
lake_run: false
kernel_checked: false
axioms_checked: false
comparator_accepted: false
routeb_source_binding_proven: false
routeb_chain_rule_instance_proven: false
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
shared_scripts_mutation: false
requested_action: hand off only the static generic unit below to an authorized pinned runner; keep source and domain producers separate
---

# Chain rule handoff: preserve the domain and expose source congruence

Recommendation: use current target Mathlib's `HasFDerivWithinAt.comp` together
with `HasFDerivWithinAt.congr'`. This supplies the missing analytic interface
beside FLT `PointDerivations.map_comp`, without importing FLT to obtain a
standard Mathlib chain rule. Keep the result as **HasFDerivWithinAt** until
there is a reason and a uniqueness witness to identify `fderivWithin`.

New contribution relative to the earlier D1 review: an explicit restricted-domain
adapter with a source-equality premise, plus the optional uniqueness-gated
direction-evaluation corollary. It neither proves its input derivatives nor
produces source equality. Only this immutable Markdown review was written;
no local/remote Lean, Lake, simulator, compiler, comparator or runner was invoked.
The code below is **uncompiled handoff text**, not a tested implementation.

## 1. Pinned provenance and import boundary

FLT source remains `https://github.com/anthropics/fermats-last-theorem`, commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`; local HEAD was rechecked.
Its committed toolchain is Lean 4.33.1 and Mathlib rev/inputRev
`db584cd6d46c92f209a44c0f1c829460d327499d`.
Selected FLT file is `Definitions/Def_Algebra_PointDerivations.lean`, blob
`a6a95f7e3170eb079c42c30deaa06a562d42f53d`, raw Git-object SHA-256
`e54ef18402112ab66421a3eccb0a8f30ea9402cc167be91c6770da0c43d144cd`.
It imports `Mathlib`; map/map_apply_coe/map_comp are lines 47-60.

For the analytic adapter, use a **separate, explicitly identified Mathlib
source**, `https://github.com/leanprover-community/mathlib4`, commit
`81a5d257c8e410db227a6665ed08f64fea08e997`. Current
`examples/local_fkg/lake-manifest.json` rev/inputRev and package HEAD agree;
toolchain is Lean 4.32.0. The manifest's raw SHA-256 is
`6cad04cdeb731b8af3594767512923ac9b9fe7e00808f91ddcb30c846e3891f3`.
This is not the old intake target `0df444a...`, nor FLT's Mathlib pin.
No claim of binary/cache compatibility or cross-pin theorem compatibility.

All following source bytes were retrieved with `git show commit:path`, and
digests computed directly from those bytes (not newline-normalized terminal
text). They identify original source declarations, not build evidence.

| Mathlib path under Mathlib/Analysis/Calculus/FDeriv/ | Git blob SHA-1 | Raw SHA-256 |
|---|---|---|
| Comp.lean | b569401f8f2ceb72d072d6b088af2630a164d1ed | 22b49670dfaa646c560b62e60674ac86288f32b09e920c00cf2d867c60f36a80 |
| Congr.lean | fa50ff49921b4ef098c0bd002b539889fa104963 | 5cad1d8c7480eac00c7004b6ec5ee9dd64ac80a833f10ad92936cdac4abe9673 |
| Basic.lean | 538d55195de38bdc0f57b569fd484ecea2f295b9 | a4e41e70a5c80c4289f24e2ca5e9511ca8278b2aec9ab0b9e5100f7df9ef7929 |
| Linear.lean | f0f78fdab141575c21f16a99dc2d1f88a62674dd | df53c9bc6a1b7969ab1169640a608479f7c796e736345ea85646a586f782cc4c |

[Comp source](https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Analysis/Calculus/FDeriv/Comp.lean#L74),
[Congr source](https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Analysis/Calculus/FDeriv/Congr.lean#L166).
Links are immutable provenance pointers; evidence was read from local Git.

The proposed unit directly imports only `FDeriv.Comp` and `FDeriv.Congr`;
both publicly import `FDeriv.Basic`. Basic has its own asymptotic/operator/
tangent-cone imports; this is a small direct import surface, not a verified
minimal transitive closure. Linear is optional for a fixed linear chart, not
required when its derivative is already supplied. No FLT/P2M import is needed
for the analytic unit. A separately ported D1 module can be connected afterward.

Mathlib headers: Copyright (c) 2019 Jeremy Avigad; authors Jeremy Avigad,
Sebastien Gouezel, Yury Kudryashov; Apache-2.0. Preserve those source notices.
For a later FLT D1 port preserve Anthropic's Apache-2.0 NOTICE/ATTRIBUTION and
third-party provenance as documented in the preceding D1 review.

## 2. Exact assumptions and classification

Classification 1 means exact abstract contract reuse, 2 means a small typed
Route-B specialization/port, 3 means architecture only for that target.
No classification means compiled or physically instantiated.

For Comp declarations below the full used ambient assumptions are:
`k : Type*`, `[NontriviallyNormedField k]`; E,F,G are types with
`[NormedAddCommGroup ...] [NormedSpace k ...]` each;
f:E→F, g:F→G, f':E→L[k]F, g':F→L[k]G, and explicit x:E.
Unreferenced section variables G', filters, and other functions are not extra
theorem premises. No completeness, finite dimension, invertibility or chart
existence assumption occurs.

| API | Exact additional premises and conclusion | Abstract / Route-B |
|---|---|---|
| HasFDerivAt.comp, Comp 105-107 | hg:HasFDerivAt g g' (f x); hf:HasFDerivAt f f' x; returns HasFDerivAt (g∘f) (g'.comp f') x | 1 / 2 |
| HasFDerivWithinAt.comp, Comp 74-78 | s:Set E, t:Set F; hg:HasFDerivWithinAt g g' t (f x); hf:HasFDerivWithinAt f f' s x; MapsTo f s t; returns HasFDerivWithinAt (g∘f) (g'.comp f') s x | 1 / 2, selected |
| HasFDerivAt.comp_hasFDerivWithinAt, Comp 81-84 | outer derivative unrestricted at f x, inner derivative within s; returns within-s composition without MapsTo | 1 / 2, useful when outer is global |
| fderivWithin_comp, Comp 140-143 | DifferentiableWithinAt for g on t at f x and f on s at x; MapsTo f s t; **UniqueDiffWithinAt k s x**; returns equality of chosen fderivWithin operators | 1 / 2, optional |
| FLT PointDerivations.map_comp | already linear evaluation-Leibniz derivation D and two linear value-maps; returns equality of their two post-compositions | 1 / 2, algebraic sibling, not analytic rule |

Within-set composition itself needs neither x∈s nor UniqueDiffWithinAt; do
not invent these as requirements of the source theorem. The handoff below
adds z∈s to consume source EqOn via congr'. No UniqueDiffWithinAt condition
on the **target** set t is required by fderivWithin_comp. At thin sets one
cannot silently infer uniqueness of the source derivative: on a singleton
every continuous linear map can satisfy the relative derivative relation,
so HasFDerivWithinAt alone does not identify a chosen fderivWithin operator.

`HasFDerivWithinAt.comp_of_tendsto`, Comp 87-90, is a more local alternative:
replace MapsTo by `Tendsto f (nhdsWithin x s) (nhdsWithin (f x) t)` with the
same two within derivatives. It avoids imposing global MapsTo if a genuine
neighborhood image witness exists; this review selects the simpler MapsTo API.
Do not shrink s to `s ∩ f⁻¹(t)` and claim coverage of the original s.

Exact source-congruence support, Congr 166-168:

```lean
theorem HasFDerivWithinAt.congr'
    (h : HasFDerivWithinAt f f' s x)
    (hs : Set.EqOn f₁ f s) (hx : x ∈ s) :
    HasFDerivWithinAt f₁ f' s x
```

Its source ambient assumptions are weaker than Comp: nontrivially normed k,
E/F with AddCommGroup, Module k, TopologicalSpace; f,f₁:E→F, f':E→L[k]F,
s:Set E, x:E. No norm/continuity typeclass hypotheses are added there.
The normed-space specialization below supplies these structures. Alternative
`congr` at 162-164 uses EqOn plus explicit f₁ x=f x instead of membership.
`congr_of_eventuallyEq` at 158-160 needs equality in nhdsWithin **and**
explicit basepoint equality; for the full-neighborhood version at 174-176,
eventual equality suffices. Class 1 abstractly / 2 for source-bound transport.

Optional `ContinuousLinearMap.hasFDerivAt`, Linear 57-58, has the same weak
ambient AddCommGroup/Module/TopologicalSpace assumptions on domain/codomain,
a nontrivially normed scalar field, L:E→L[k]F and x:E; conclusion
HasFDerivAt L L x. Its later `fderiv` theorem adds continuity of addition/scalar
multiplication and T2 on codomain. Do not conflate these signatures. In our
normed specialization they are available instances. A fixed linear chart is
therefore easy; a merely LinearMap in an arbitrary space is not enough.

For comparison, exact FLT assumptions remain k:Type u, A:Type v, Field k,
CommRing A, Algebra k A, ev:A→+*k; M:Type w, M':Type w', M'':Type w, each
AddCommGroup/Module k; φ:M→ₗ[k]M', ψ:M'→ₗ[k]M'',
D in the submodule of A→ₗ[k]M satisfying
D(ab)=ev(a)•D(b)+ev(b)•D(a). Conclusion:
`map ev (ψ.comp φ) D = map ev ψ (map ev φ D)`.
No ev/algebraMap compatibility premise is needed here (it is needed by the
different ev_smul lemma); no analytic differentiability follows.

No class-3 FLT curve/automorphic machinery is needed for this handoff.
The inspected Route-B `P5AnalyticUnitPullback.lean` is rational identities and
envelope/Lipschitz algebra, not HasFDerivAt or a general coordinate chart.
Its filename is not evidence that the current analytic gap is already closed.

## 3. Proposed minimal unit: uncompiled, assumptions left visible

The following is a handoff specification, deliberately not written as a Lean
artifact and not checked locally. It is a generic consumer, not a Route-B proof.

```lean
import Mathlib.Analysis.Calculus.FDeriv.Comp
import Mathlib.Analysis.Calculus.FDeriv.Congr

noncomputable section
namespace RouteBChainRuleHandoff

variable {Z E : Type*}
  [NormedAddCommGroup Z] [NormedSpace ℝ Z]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {T : Z → E} {f : E → ℝ} {actual : Z → ℝ}
  {J : Z →L[ℝ] E} {ell : E →L[ℝ] ℝ}
  {s : Set Z} {t : Set E} {z : Z}

theorem pullback_at
    (hT : HasFDerivAt T J z)
    (hf : HasFDerivAt f ell (T z)) :
    HasFDerivAt (f ∘ T) (ell.comp J) z :=
  hf.comp z hT

theorem source_pullback_within
    (hT : HasFDerivWithinAt T J s z)
    (hf : HasFDerivWithinAt f ell t (T z))
    (hmap : Set.MapsTo T s t)
    (hsource : Set.EqOn actual (f ∘ T) s)
    (hz : z ∈ s) :
    HasFDerivWithinAt actual (ell.comp J) s z :=
  (hf.comp z hT hmap).congr' hsource hz

theorem source_pullback_direction
    (hT : HasFDerivWithinAt T J s z)
    (hf : HasFDerivWithinAt f ell t (T z))
    (hmap : Set.MapsTo T s t)
    (hsource : Set.EqOn actual (f ∘ T) s)
    (hz : z ∈ s) (hu : UniqueDiffWithinAt ℝ s z) (v : Z) :
    (fderivWithin ℝ actual s z) v = ell (J v) := by
  have hd := source_pullback_within hT hf hmap hsource hz
  rw [hd.fderivWithin hu]
  rfl

end RouteBChainRuleHandoff
```

The optional last theorem uses Basic 426-430. In its source formulation
HasFDerivWithinAt.fderivWithin additionally assumes ContinuousAdd and
ContinuousSMul on both spaces and T2Space on the codomain; these are supplied
by the normed real structures above. No syntax/elaboration success is asserted.
The direction formula evaluates the relative derivative operator on v; at
a boundary it is not a claim that every direction is realized by a path in s.

For the earlier cotangent API, choose Φ_J(ell)=ell.comp J and independently
establish D_x(a)=the actual differential of observable a at x=T z. The new
analytic unit gives the pointwise formula Φ_J(D_x(a)); FLT map_comp then
organizes two **value** transports. If H:Y→L[ℝ]Z, the order is
Φ_H(Φ_J(ell))=ell.comp(J.comp H), not H.comp J. Changing the observable algebra
and ev from x to z still requires the analytic/source square above and the
linearity/Leibniz producer for D, not just a call to map_comp.

## 4. Source and physical admission boundary

The hsource field is an independently proved source-to-mathematical-function
identity on s. It is not to be manufactured by defining `actual := f ∘ T`
when actual is supposed to denote a deployed source evaluator. Equal values
at z, matching hashes, finite samples or an accepted generic comparator cannot
produce hsource. At 0, the functions 0 and x have equal values but different
derivatives; single-point equality is an invalid replacement for a germ identity.

A source-bound real DAG can be handled by proving its node functions regular
from exact operation semantics, then transporting derivatives using independent
source congruence. Comp alone does not provide the sin/cos/product rules, the
node interpretation, occurrence/lifetime binding or a Julia Float64 derivative.
Finite binary64-input equality is not neighborhood equality in ℝ and cannot
discharge hsource for real calculus. Runtime rounding and FD remainders stay open.

For a time-dependent chart T(t,z), this unit at frozen t covers only the spatial
pullback. It does not derive time terms, derivatives of J, material metric
terms or mixed-derivative symmetry. In the current P5 contraction source,
`physical_variation_rate_identity` still assumes hdV (line 94) and
`moving_metric_contraction_tensor_congruence` assumes hk1/hk2 (117/120).
Its verifier text explicitly leaves DIFFERENTIAL_COVARIANCE_DERIVATION open.
This review did not run it. Source SHA-256 observed for that Lean file:
`e5950ad1b8ac474ddc814dd3fc993f68de128b5028d11726345e2b9ce3a44468`.
The proposed unit cannot discharge those premises without the actual F/W/T/J
definitions, required regularity and derivative identities on the same domain.

MapsTo is a chart-domain mapping condition, not an ODE whole-path membership
certificate. UniqueDiffWithinAt is geometric uniqueness, not a flowpipe witness.
No contraction estimate, Hessian norm, inverse chart, bound constant, interval
coverage or continuous-PDE conclusion is supplied by these generic APIs.

## 5. Handoff acceptance checks, all still pending

An authorized runner should compile only the proposed isolated generic unit at
the agreed target pin, record source/import/toolchain/package identities and
actual command/exit/stdout/stderr, and return declaration-level axiom reports
without sorryAx plus a statement comparator. Do not compile FLT's full tree.
This review does not dispatch a runner or grant local Lean authorization.

The comparator must retain the derivative premises, hmap, hsource, hz, and
hu only for the direction corollary. Required discriminators:

- Removing MapsTo cannot retain the selected within-comp contract without
  supplying a legitimate alternative neighborhood-image witness.
- Replacing hsource by one-point equality must not yield source derivatives.
- Relative derivative existence must not silently become fderivWithin equality
  on a singleton or other non-unique tangent domain.
- Derivative composition order, basepoint T z, and exact s/t must remain fixed.
- A fixed-t success must not erase moving-frame/time derivative terms.

These are proposed focused validation requirements, not tests executed here.
Even a passing generic unit remains pending for physical integration until
independent source, derivative, domain and same-object producers are supplied.
No state, registry, shared script, existing intake, D1 handoff or prior review
was modified. No pure-number-theoretic theorem was acquired.
