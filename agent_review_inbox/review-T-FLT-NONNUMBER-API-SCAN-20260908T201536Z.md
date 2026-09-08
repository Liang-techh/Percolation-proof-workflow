---
kind: review_result
review_id: review-T-FLT-NONNUMBER-API-SCAN-20260908T201536Z
task_id: T-FLT-NONNUMBER-API-SCAN-20260908
source_agent: Codex-independent-nonnumber-scan
created_at: 2026-09-08T20:15:36Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: NEW_QUALITATIVE_UNIFORM_SLICE_DERIVATIVE_BOUND_CANDIDATE
selected_declaration: ContDiff.exists_forall_norm_iteratedDeriv_slice_le_of_isCompact
abstract_reuse_classification: 1
routeb_adapter_classification: 2
lean_compile_status: not_run
lean_run: false
lake_run: false
kernel_checked: false
axioms_checked: false
comparator_accepted: false
certified_constant: null
routeb_source_closure: false
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
shared_scripts_mutation: false
requested_action: consider a small independent smooth-family port; retain actual source regularity and quantitative remainder obligations as separate pending producers
---

# Non-number-theoretic API scan: a new compact-family bound seam

**Positive result:** a small FLT smooth-family theorem adds a common bound for
finitely many slice-derivative orders over a compact parameter set. This is
new capability beyond the previously selected composition APIs: the order of
quantifiers gives one C for all parameters, slice locations and orders up to N.
It is not logically stronger than a chain rule in every sense: it has much
stronger smoothness/compactness hypotheses and a different conclusion.

**Negative result for immediate Route-B closure:** no inspected candidate
provides a computable/certified numerical C, actual DH-source regularity,
finite-difference remainder, machine error or trajectory coverage. The selected
theorem therefore cannot by itself close an error-budget or source-binding leaf.

This bounded scan excludes the completed PointDerivations.map_comp and
HasFDerivWithinAt.comp/congr' adapter units. It examines generic calculus and
linear-map declarations, not pure-number-theoretic results. Only this immutable
review is written. No local/remote Lean, Lake, comparator, build, exporter or
simulation ran. All proof assessment is static and **uncompiled**.

## 1. Repository and version identities

Two separate Anthropic repositories were inspected; they must not be conflated.

| Repository/local snapshot | Inspected commit | Source Lean / Mathlib |
|---|---|---|
| anthropics/fermats-last-theorem; artifacts/anthropic_fermats_last_theorem | aa2d8b34692b16c70f699536de0d8e75b9a3e9ef | leanprover/lean4:v4.33.1 / db584cd6d46c92f209a44c0f1c829460d327499d |
| anthropics/formal-math; upstream/formal-math, zeta23 subproject | 795efb86f191735c5481675763537cfb4ff37e55 | leanprover/lean4:v4.33.0-rc2 / 51e6992efd06126df61a496bebf8f49482a4e129 |

The second repository remote is https://github.com/anthropics/formal-math.git;
each subproject has its own lock. In particular a zeta23 source path must not
be cataloged under the FLT commit. Both pins above were read from committed
toolchain/manifest files. Current local_fkg target remains Lean 4.32.0 and
Mathlib checkout HEAD 81a5d257c8e410db227a6665ed08f64fea08e997; no cross-pin
compatibility is established by static reading.

The FLT file-tree filter was restricted to generic ContDiff/ContinuousLinearMap/
LinearMap prefixes, followed by selected wrapper/proof reads. formal-math was
screened by calculus/taper-related paths, then one generic coercion lemma was
read. Names containing arithmetic terminology were not acquired as candidates.
This is not an exhaustive search of either theorem corpus. A first local rg
used an unsupported literal wildcard directory argument; it was corrected to
explicit directories. That search error is not a build or theorem failure.

## 2. A — selected: uniform boundedness of slice derivatives

Wrapper:
`Theorems/Thm_ContDiff_exists_forall_norm_iteratedDeriv_slice_le_of_isCompact.lean`
at FLT commit above; declaration lines 7-13:

```lean
theorem ContDiff.exists_forall_norm_iteratedDeriv_slice_le_of_isCompact
    {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    (Ψ : E → ℝ → F)
    (hΨ : ContDiff ℝ (⊤ : ℕ∞) (fun p : E × ℝ => Ψ p.1 p.2))
    (S : Set E) (hS : IsCompact S) (R : ℝ) (N : ℕ) :
    (∀ a : E, ContDiff ℝ N (Ψ a)) ∧
    ∃ C : ℝ, 0 ≤ C ∧ ∀ a ∈ S, ∀ u ∈ Set.Icc (-R) R,
      ∀ n ≤ N, ‖iteratedDeriv n (Ψ a) u‖ ≤ C
```

No further ambient assumptions are hidden by a section in the wrapper.
In particular F need not be finite-dimensional or complete. S need not be
nonempty; R has **no positivity hypothesis**. If R<0 the interval is empty;
a meaningful Route-B slice application must separately choose R>0. N=0
includes the function itself. The smoothness hypothesis is global joint C∞,
not merely differentiability of every separate slice, and not ContDiffOn S.
The first conjunct quantifies every a:E, not only a∈S.

The constant C can depend on Ψ,S,R,N but not a,u,n inside the bound. A packet
containing a separately chosen C(a,u,n) would be the wrong quantifier contract.
Nothing says the same C bounds all natural orders simultaneously.

### Proof source and minimal reusable helper

Complete 78-line solution read:
`P2M/Sol/S_ContDiff_exists_forall_norm_iteratedDeriv_slice_le_of_isCompact.lean`.
It defines a directional tower in namespace
`P2MW.S_ContDiff_exists_forall_norm_iteratedDeriv_slice_le_of_isCompact.Ws31.SmoothFamily`:

```text
dU G 0 = G
dU G (n+1) p = fderiv ℝ (dU G n) p (0,1)
```

`iteratedDeriv_slice` (25-40) has exactly E,F real normed-space assumptions
(no FiniteDimensional premise), G:E×ℝ→F and global hG:ContDiff ℝ ∞ G:

```text
∀ n a u, iteratedDeriv n (fun u => G(a,u)) u = dU G n (a,u).
```

The proof first establishes every dU layer jointly C∞ via fderiv_right and
continuous-linear-map evaluation (16-23). It identifies the scalar slice
derivative with the ambient derivative in direction (0,1). The main proof
(42-67) takes the compact product S×[-R,R], bounds the continuous dU layers,
and uses a finite sum of absolute chosen bounds to get one nonnegative C.
This is a noncomputable compactness/choice argument, not a numeric evaluator.

Static observation: the displayed main proof does not explicitly use its
FiniteDimensional E premise once hS is given. Removing it might strengthen
the theorem, but is **not verified here** and is not part of the initial port.
Preserve the exact wrapper assumptions first. Similarly, replacing global C∞
by finite-order/local-neighborhood regularity needs a separate proof.

Wrapper imports Mathlib, P2M.Util and the matching solution; wrapper proof uses
p2m_exact_reverting. Solution imports Mathlib and P2M.Util, but its displayed
mathematical proof uses no p2m tactic. A small independent namespace containing
dU, contDiff_dU, iteratedDeriv_slice and main is a plausible class-2 port that
avoids the FLT theorem tree and orchestration wrapper. Minimal Mathlib import
closure remains unverified; the source uses an umbrella import.

**Classification: 1 abstract contract / 2 implementation and Route-B adapter.**
Preserve the source's existential conclusion rather than inventing a bound.

### Route-B adapter assumptions and proposed DAG role

For a fixed matrix entry (r,c) and coordinate direction j, let

```text
Ψ(q,u) = M_NE^0(q + u e_j)[r,c],  E = Fin 6 → ℝ, F = ℝ.
```

This is a **proposed mathematical instantiation**, not a claimed source export.
The required independent producers are:

1. Exact source-to-ideal-real identity for M_NE^0, with fixed constants,
   occurrence/lifetime semantics and the observation boundary before regularizer.
2. Global joint ContDiff ℝ ∞ of the chosen Ψ. The snapshot's fixed-size mass
   expression uses sin/cos, sums, products and fixed positive-natural division;
   that suggests a structural proof for the ideal-real graph, but does not
   constitute one. Arbitrary controller inverse/branching terms are not included.
3. A compact real parameter set S and a chosen R>0; all q+u e_j used must stay
   in the source-refinement/physical validity region. If evidence is local only,
   supply a compatible global smooth extension and its equality on the required
   neighborhood, or prove a separate localized theorem. Do not weaken hΨ silently.
4. Identification of slice derivatives with the intended directional derivatives
   of the same matrix entry. If a joint matrix norm is used instead of F=ℝ,
   explicitly prove the desired entry/norm conversion.

The proposed theorem-DAG output is **existence of a uniform finite-order slice
bound**, conditional on these producers. To cover all finitely many r,c,j,
take a proved finite maximum/sum of their nonnegative existential bounds; do
not assert that one entry/direction already covers the full Hessian tensor.
Mixed derivatives and arbitrary directions need their own identification.

Choosing N=3 may support a later exact-real central-difference remainder
argument, but the present theorem contains no Taylor/remainder inequality,
computable C, step-size selection or Float64/libm error. None is generated here.
An existential C cannot be inserted as a numerical error-budget receipt.

The real snapshot was re-read at
`examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`,
SHA-256 `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.
The current H_acc intake still has null graph, mapping, updates, runtime and
interval components. Thus producer 1 is not supplied by the current intake;
this candidate does not change that status.

## 3. B — secondary: one injective approximant on a finite-dimensional space

Exact wrapper declaration:

```lean
theorem LinearMap.exists_forall_eq_zero_of_tendsto_apply_of_finiteDimensional
    {X : Type*} (Y : Submodule ℂ (X → ℂ)) [FiniteDimensional ℂ ↥Y]
    (T : ℕ → (↥Y →ₗ[ℂ] (X → ℂ)))
    (hT : ∀ (y : ↥Y) (x : X),
      Filter.Tendsto (fun n => T n y x) Filter.atTop
        (nhds ((y : X → ℂ) x))) :
    ∃ n, ∀ y : ↥Y, T n y = 0 → y = 0
```

Wrapper and entire solution were read. Both reside at the FLT pin under
`Theorems/Thm_LinearMap_exists_forall_eq_zero_of_tendsto_apply_of_finiteDimensional.lean`
and the corresponding `P2M/Sol/S_LinearMap_exists_forall_eq_zero_of_tendsto_apply_of_finiteDimensional.lean`.
Imports are Mathlib/P2M.Util plus the solution in the wrapper.

X has no topology assumption; Y is a complex function subspace. T n maps into
all functions X→ℂ, not necessarily back into Y. No norm convergence is assumed:
the hypothesis is pointwise convergence for **every** y and x. The result is
existence of one injective T n, not a computed index, numerical rank test,
operator lower bound or a claim that every n works.

Proof: finite-dimensionality yields finitely many evaluations separating Y;
evaluate a finite basis there, use convergence and openness of linear
independence, and transfer injectivity back. It gives no certificate that a
particular user-selected finite sample set separates the actual residual space.

**Classification: 1 abstract / 2 for a complex finite-dimensional Route-B
surrogate adapter.** Need an exact finite-dimensional Y, linearity of the
actual approximation maps and the full pointwise limit, plus identification
with physical observables if used there. A real-scalar generalization is a
separate port, not the original theorem. Useful as a qualitative projection/
identifiability leaf; lower priority than A for the current derivative-bound gap.

## 4. Other screened results and negative classifications

### C — symmetric shifted-range intersection (not selected)

`ContinuousLinearMap.eq_zero_of_forall_exists_mem_sub_real_smul_eq` has:
H:Type*, NormedAddCommGroup H, InnerProductSpace ℂ H, CompleteSpace H;
T:H→L[ℂ]H, E:Submodule ℂ H;
hsym:∀x∈E,∀y∈E, inner(Tx,y)=inner(x,Ty);
v:H; hsurj:∀c:ℝ,∃w∈E,Tw-(c:ℂ)•w=v. Conclusion is **v=0**, not T=0.
E need not be closed/invariant, and T is assumed symmetric only on E.

Wrapper was fully read; a long solution was only partially inspected and is
not audited as a whole. The all-real-shifts range assumption, including
spectral shifts, is much stronger than invertibility at one off-spectrum
point. This supplies no quantitative derivative or residual estimate.
**Abstract relevance 1; current Route-B reuse 3** without a concrete spectral
range producer. Do not promote the theorem merely from its name.

### D — formal-math scalar coercion (not a new high-value leaf)

In formal-math's separate zeta23 pin,
`zeta23/Zeta23/Taper/Strip.lean` lines 40-43:

```lean
theorem Zeta23.Taper.deriv_ofReal_comp {f : ℝ → ℝ}
    (hf : Differentiable ℝ f) :
    deriv (fun u => (f u : ℂ)) = fun u => ((deriv f u : ℝ) : ℂ)
```

The statement is shown fully qualified here; the source declares it inside
Zeta23.Taper. No TaperProfile, support, L or w premise leaks from the section
into this declaration. Its proof is the existing Mathlib ofReal derivative
API and function extensionality. Direct source imports: Algebra.Order.Star.Real,
MeasureTheory.Integral.Bochner.Set and Zeta23.Taper.Basic.
**1 abstract / 2 for an isolated real-to-complex observable adapter**, but
not a stronger result than already available calculus infrastructure. Importing
the taper module is unnecessary for this small coercion identity. No zeta-zero
or other number-theoretic theorem is used.

## 5. Declaration-level provenance ledger

For A/B/C the repository commit is FLT aa2d8b...e9ef; hashes below are raw
Git-object bytes, not assumed working-tree copies. W=wrapper, S=solution.

| Item | Git blob SHA-1 | Raw SHA-256 |
|---|---|---|
| A-W | 1d6f663436f34f7672509010d46c936ca1179834 | e77be0367417759c609fa8b70b87859d47b5732dab0853c95887af57da57adf4 |
| A-S | 6e7a0942dc2eb02fa174626fb5a3176509b6332c | 4873a180bdd675d9ed8af864690a810c41a7fc28df2f62dbe803de911cf1285f |
| B-W | 50f04fec35a7abe221d0519fc4d98dc4088b6201 | 912a525b07d8dd7faaa41783fe8ef4f70b468632219f4ec00409d88ec86f00d9 |
| B-S | 1df8853769365ec64390b524ddb4a3424f51e88e | 794301cf5b257efd4a50a40b740c6eeea28347ebc5c71aa63faf96c9714dcb85 |
| C-W | 6c715bff9f03620afbcc8c7796cfe1a42cf63ecb | fedaa11208300fc02554a28a37569500061eb9eb9446b0fee695a6e1dc045f02 |
| D, formal-math 795efb...e55 | c9f0745b73ec50906dafebaea1a31c78b55b8066 | 03bd8e55856a7a5e58a02ecf477db74d231e599e46858bc9cf8397462de2d04c |

C-W path is
`Theorems/Thm_ContinuousLinearMap_eq_zero_of_forall_exists_mem_sub_real_smul_eq.lean`.

[A source](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/P2M/Sol/S_ContDiff_exists_forall_norm_iteratedDeriv_slice_le_of_isCompact.lean#L42),
[B source](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/P2M/Sol/S_LinearMap_exists_forall_eq_zero_of_tendsto_apply_of_finiteDimensional.lean#L7),
[D source](https://github.com/anthropics/formal-math/blob/795efb86f191735c5481675763537cfb4ff37e55/zeta23/Zeta23/Taper/Strip.lean#L40).
These are immutable provenance pointers; source evidence was obtained locally.

FLT is Apache-2.0 with repository NOTICE/ATTRIBUTION. No exact A/B/C filename
match was found in the pinned ATTRIBUTION list, which is not proof of original
authorship or absence of short Mathlib-derived material. Preserve all relevant
notices in a later port. D's file explicitly says Copyright 2026 Anthropic,
PBC, Apache-2.0. No proof module was copied into the workspace by this task.

## 6. Small next handoff and stopping condition

For an authorized future runner, prefer A alone: isolate dU and the three
small helper/main proofs, retain the exact wrapper contract, remove the P2M
orchestration dependency only after pin-specific import checking, and report
actual source/import/object hashes, command/exit/logs, declarations, axioms
and exact comparator evidence. Test that the bound remains one C outside all
a/u/n quantifiers, that n=0 is included, and that global joint smoothness is
not silently replaced by slice-wise smoothness. Empty S or R<0 may make the
bound vacuous and are not evidence for a nonempty physical region.

The final packet should call the result qualitative compact-family boundedness,
not H_acc_round or a numerical FD constant. If the actual consumer requires a
numerical rational bound immediately, **this candidate is insufficient**;
an explicit derivative enclosure/remainder producer remains the relevant leaf.
All generic ports and all physical instantiations remain pending. No shared
state/registry/scripts, prior reviews or intake files were changed.
