---
kind: review_result
task_id: T-P4-032
source_agent: Codex
created_at: 2026-09-07
integration_status: pending
review_status: ADVISORY_REPAIR_REQUIRED__UNCOMPILED
---

# T-P4-032 independent API/proof review

## Conclusion

The theorem statement and the `Fin d`/`Fin b` shapes are sound for a
conditional exact-real O1 identity. The current proof skeleton has the right
high-level route, but it should not be treated as compile-ready: the target
uses `linarith` without an explicit tactic import, and the `hB_left` type is
written with a left-associated three-matrix product while the nested
`Matrix.mulVec_mulVec` normalization naturally exposes the right-associated
form. No Lean/Lake command was run, so this remains an uncompiled advisory
repair, not a kernel receipt.

## Minimal repair

1. Add the tactic import used by the existing proof:

   ```lean
   import Mathlib.Tactic.Linarith
   ```

   `Mathlib.Data.Matrix.Basic`/`Mul` provide the matrix API but should not be
   relied on to expose the `linarith` tactic transitively. The duplicate
   `Mathlib.Data.Matrix.Mul` import may be retained or removed; it is not a
   proof issue.

2. In `hB_left`, either normalize the stated target with associativity:

   ```lean
   have hB_left :
       M_BD *ᵥ v +
         (M_BD * M_DD_inv * DeltaM_DB) *ᵥ a_B = 0 := by
     have h := congrArg
       (fun x : DVec d => M_BD *ᵥ x) hsolve
     simpa only [Matrix.mulVec_add, Matrix.mulVec_zero,
       Matrix.mulVec_mulVec, Matrix.mul_assoc] using h
   ```

   or write the product in the target as
   `M_BD * (M_DD_inv * DeltaM_DB)` and keep `Matrix.mul_assoc` out of that
   local `simpa`. Do not use `ring` to reorder matrix factors.

   The same associativity point applies to the report's claim that two
   `mulVec_mulVec` rewrites produce a left-associated product: the robust
   normal form for a nested action is
   `M_BD * (M_DD_inv * DeltaM_DB)`. `Matrix.mul_assoc` is only a
   parenthesization rewrite; it does not commute `B`, `D`, or `D`/`B` factors.

3. Keep the explicit inverse premise exactly as

   ```lean
   h_inv_left : M_DD_inv * M_DD = (1 : Matrix (Fin d) (Fin d) ℝ)
   ```

   This is the only inverse direction needed by the D-balance elimination.
   Do not replace it with `M_DD⁻¹` or hide a solver/backslash operation in the
   theorem. A canonical `nonsing_inv`/`IsUnit M_DD.det` adapter, if later
   required by the semantic contract, belongs in a separate theorem and is
   not needed by this core proof.

## Shape and direction audit

The current declaration is dimensionally consistent:

| object | Lean shape | action |
| --- | --- | --- |
| `v` | `Fin d → ℝ` | D-column |
| `a_B`, `r_B` | `Fin b → ℝ` | B-columns |
| `M_DD`, `M_DD_inv` | `Matrix (Fin d) (Fin d) ℝ` | D → D |
| `DeltaM_DB` | `Matrix (Fin d) (Fin b) ℝ` | B → D |
| `M_BD` | `Matrix (Fin b) (Fin d) ℝ` | D → B |
| `R_port` | `Matrix (Fin b) (Fin b) ℝ` | B → B |

Thus the product is `(B×D)(D×D)(D×B)=B×B`, and the proof must use
`Matrix.mulVec`/`*ᵥ` in that order. `Matrix.mulVec_mulVec` has the needed
direction

```text
M *ᵥ (N *ᵥ x) = (M * N) *ᵥ x
```

with `Fin d` and `Fin b` supplying the required finite-index instances. The
leading minus is also correct: `Matrix.neg_mulVec` is the relevant lemma for
`R_port = -(...)`; `Matrix.mulVec_neg` would refer to negating the vector.

## Boundary

This review confirms only the algebraic interface and a minimal proof repair.
It does not establish Lean compilation, zero-sorry/axiom receipts, source or
Float64 binding, coverage, positivity, flowpipe, admission, or registry
promotion. The inspected candidate, report, and receipt remain explicitly
`UNCOMPILED__NON_VERIFIED`; no main state or registry was changed.

## Evidence and provenance

- Candidate: `artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean`
  SHA-256 `679FABCDBF99113ADAE3BD17DC80E769077C6105ED070AC280AD67483207F0A2`.
- Report: `artifacts/task_routeb_o1_lean_api_audit_20260907/REPORT.md`
  SHA-256 `69C2C58EB1EDB20C1C5D464FFCBAE58F1680EE14AB6E09B29EB5E526BE24BCA6`.
- Receipt: `artifacts/task_routeb_o1_lean_api_audit_20260907/RECEIPT.json`
  SHA-256 `A0FB40F177EBE2D776C9398C2A5E33E86C1312209E0BBF7529678F5E7742F36E`.
- Read-only API sources: `artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/Mathlib/Data/Matrix/Mul.lean`
  (`mul_assoc`, `mulVec_add`, `mulVec_mulVec`, `one_mulVec`, `neg_mulVec`)
  and `.../Mathlib/LinearAlgebra/Matrix/NonsingularInverse.lean` (inverse
  adapter only).
- Read-only commands: `Get-Content`, `rg`, `Get-FileHash`, `git status`, and
  `git log -1`. No Lean/Lake, comparator, solver, state-store, or registry
  operation was performed. The pre-existing modified path
  `scripts/record_routeb_trig_chain_contract.py` was left untouched.
