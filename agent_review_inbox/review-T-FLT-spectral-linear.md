---
kind: review_result
task_id: T-FLT-SPECTRAL-LINEAR
source_agent: Codex
integration_status: pending
---

Fixed commit scanned: `aa2d8b34` (`Fermat's Last Theorem in Lean 4 (Lean 4.33.1, Mathlib v4.33.0)`).

Scope actually checked: non-number-theory Lean content in `spectral` / `eigenspace` / finite-dimensional linear algebra / exact-sequence-adjacent material. I did not build the repo, and I did not touch state/registry/task_queue.

1 direct reuse

- `Theorems/Thm_Submodule_exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace.lean`
  - declaration: `Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`
  - key statement: constructs an injective `k`-linear map
    `k ⊗[A ⧸ 𝔪] ↥(torsionBySet A J 𝔪) →ₗ[k] k ⊗[ℤ] ↥(torsionBySet A J I)`
    whose range is exactly the simultaneous eigenspace condition
    `∀ a : A, ((DistribSMul.toLinearMap ... a).baseChange k) w = ι (mk 𝔪 a) • w`
  - hypotheses: `CommRing A`, module `J`, field `k`, prime `p`, `CharP k p`, maximal ideal `𝔪`, `I ≤ 𝔪`, `p ∈ I`, finiteness of `Submodule.torsionBySet A J I`, and a residue-field algebra map `ι : A ⧸ 𝔪 →+* k`
  - imports: `Mathlib.RingTheory.TensorProduct.Basic`, `Mathlib.Algebra.Module.Torsion.Basic`, `Mathlib.Algebra.CharP.Defs`, `Mathlib.RingTheory.Ideal.Quotient.Basic`, `P2M.Util`, `P2M.Sol.S_Submodule_exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`
  - pin: Lean `4.33.1`, Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`
  - provenance/license: Apache-2.0 repo file; theorem is a thin wrapper over `p2m_exact_reverting` into `_root_.P2MW.S_Submodule_exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace.solution`
  - Route-B/P7 availability: high-value sidecar candidate; structurally direct and already phrased as the exact eigenspace/range bridge that a current-pin focused sidecar would want
  - blocker: only the imported `P2M.Sol...` proof body is opaque here; no upstream build or kernel verification was run in this pass

- `Theorems/Thm_Representation_exists_basis_toMatrix_mem_subfield_of_trace_det_mem_of_hasEigenvalue.lean`
  - declaration: `Representation.exists_basis_toMatrix_mem_subfield_of_trace_det_mem_of_hasEigenvalue`
  - key statement: for a 2-dimensional representation, if every `ρ g` has trace and determinant in a subfield `F`, and one element has an eigenvalue `a ∈ F` but is not scalar, then there exists a basis in which every matrix entry of every `ρ g` lies in `F`
  - hypotheses: `Field Ω`, `Module.finrank Ω V = 2`, irreducibility of invariant submodules, trace/det landing in `F`, one `g₀` with `HasEigenvalue`, and non-scalarity `ρ g₀ ≠ a • id`
  - imports: `Mathlib`, `P2M.Util`, `P2M.Sol.S_Representation_exists_basis_toMatrix_mem_subfield_of_trace_det_mem_of_hasEigenvalue`
  - pin: Lean `4.33.1`, Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`
  - provenance/license: Apache-2.0 repo file; wrapper around `_root_.P2MW.S_Representation_exists_basis_toMatrix_mem_subfield_of_trace_det_mem_of_hasEigenvalue.solution`
  - Route-B/P7 availability: strong current-pin sidecar candidate for finite-dimensional linear algebra / eigenvalue extraction; less direct than the eigenspace bridge above, but still highly reusable
  - blocker: depends on the opaque `P2M.Sol...` implementation and does not itself expose a decomposition argument

2 light adaptation

- `Theorems/Thm_Rep_exists_shortExact_coind_res.lean`
  - declaration: `Rep.exists_shortExact_coind_res`
  - key statement: given a finite-index subgroup and a family of local finite-dimensionality hypotheses, produces `Q` and maps `N ⟶ coind(...) ⟶ Q` with injective/surjective exactness-style conditions, plus finite-dimensionality and fixed-field control on both middle and output objects
  - hypotheses: `Field k`, `Group G`, representation `r`, subgroup `S` of finite index, `N : Rep k G` finite-dimensional, and a per-vector finite-subfield invariance hypothesis `hsm`
  - imports: `Mathlib`, `P2M.Util`, `P2M.Sol.S_Rep_exists_shortExact_coind_res`
  - pin: Lean `4.33.1`, Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`
  - provenance/license: Apache-2.0 repo file; wrapper over `_root_.P2MW.S_Rep_exists_shortExact_coind_res.solution`
  - Route-B/P7 availability: useful as a reusable exact-sequence construction, but it is more architectural than the eigenspace bridge and likely needs local retargeting to the present pin
  - blocker: exact-sequence witness structure is tied to the repo’s `Rep.coind`/`Rep.res` API and to the imported solution theorem

- `Theorems/Thm_Rep_shortExact_coind_ker_trace.lean`
  - declaration: `Rep.shortExact_coind_ker_trace`
  - key statement: if `α` is injective, `β` is surjective, and the kernel-image condition `β b = 0 ↔ ∃ a, α a = b` holds, then the induced maps on coinduced representations and on kernel objects again satisfy the corresponding injective/surjective/exact conditions
  - hypotheses: `Field k`, `Group G`, finite-index subgroup `U`, a short-exact-like triple `A ⟶ B ⟶ C`, trace maps `τA τB τC` satisfying explicit finite-sum formulas, and auxiliary injections `iA iB iC` with exactness witnesses
  - imports: `Mathlib`, `P2M.Util`, `P2M.Sol.S_Rep_shortExact_coind_ker_trace`
  - pin: Lean `4.33.1`, Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`
  - provenance/license: Apache-2.0 repo file; wrapper over `_root_.P2MW.S_Rep_shortExact_coind_ker_trace.solution`
  - Route-B/P7 availability: architecture-only exact-sequence scaffold; valuable as a template for transport of short exactness, but not a direct spectral sidecar
  - blocker: heavy categorical/representation-specific surface area; likely needs adaptation to any new local API shape

3 architecture-only

- `Theorems/Thm_TaylorWiles_exists_mem_ker_cycloChar_hasDistinctRationalEigenvalues.lean`
  - declaration: `TaylorWiles.exists_mem_ker_cycloChar_hasDistinctRationalEigenvalues`
  - key statement: under residual irreducibility and a split-trace/det hypothesis, finds an element in the cyclotomic-character kernel whose residual representation has distinct rational eigenvalues
  - hypotheses: number field `L`, residue field `𝕜`, prime `p ≠ 2`, primitive root `ζ`, `h2 : (2 : 𝕜) ≠ 0`, spanning/irreducibility of the residual image, and a factorization hypothesis for trace and determinant
  - imports: `Mathlib`, `Definitions.Def_TaylorWiles_CyclotomicChar`, `P2M.Util`, `P2M.Sol.S_TaylorWiles_exists_mem_ker_cycloChar_hasDistinctRationalEigenvalues`
  - pin: Lean `4.33.1`, Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`
  - provenance/license: Apache-2.0 repo file; wrapper over `_root_.P2MW.S_TaylorWiles_exists_mem_ker_cycloChar_hasDistinctRationalEigenvalues.solution`
  - Route-B/P7 availability: structurally related to eigenvalue extraction, but this is number-theoretic/Taylor-Wiles-specific and not the best sidecar for the requested non-number-theory slice
  - blocker: domain mismatch for your requested non-number-theory scan; keep as background architecture only

Recommendation for a current-pin focused sidecar:

- Best candidate: `Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`
- Second choice: `Representation.exists_basis_toMatrix_mem_subfield_of_trace_det_mem_of_hasEigenvalue`

The main reason is that both are already phrased in a reusable interface style and sit closest to the spectral/eigenspace / finite-dimensional linear algebra boundary you asked for, while the exact-sequence items are more scaffolding than direct spectral leverage.
