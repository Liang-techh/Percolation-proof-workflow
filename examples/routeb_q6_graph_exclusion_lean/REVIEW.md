---
kind: review_result
review_id: review-GH-LEAN-P4-Q6-GRAPH-EXCLUSION-codex-20260908T092841
task_id: GH-LEAN-P4-Q6-GRAPH-EXCLUSION
source_agent: Codex-abstract-block-graph-exclusion
created_at: 2026-09-08T09:28:41-06:00
inspected_commit: 6509984f9a045c441df64e088b704ee341a1316d
inspected_paths:
  - examples/routeb_q6_graph_exclusion_lean/Q6GraphExclusionCandidate.lean
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
parsed: false
elaborated: false
kernel_checked: false
axioms_checked: false
verified: false
final_integration: false
registry_promoted: false
formal_certificate_allowed: false
requested_action: review the independent block-equation candidates; supply concrete map/projection/row/invertibility bindings separately before any downstream use
---

# Abstract block-equation graph exclusion

Five independent candidate lemmas have been added. No local Lean/Lake, compiler, solver or comparator was run. All declarations remain pending and uncompiled. The inspected commit is the workspace baseline, not a commit containing these newly added files.

## Statement and exact argument

For linear maps with correctly typed domain/codomain blocks, assume

```text
M_DD alpha_D + M_DC alpha_C = R_D,
M_CD alpha_D + M_CC alpha_C = R_C,
R_D = 0, alpha_C = 0,
M_DD is injective (in particular, invertible).
```

Linearity gives M_DC(0)=0, so the D row reduces to M_DD(alpha_D)=0=M_DD(0). Injectivity gives alpha_D=0. Substitution in the C row gives R_C=0. If R_C is nonzero, assuming alpha_C=0 contradicts this implication; hence alpha_C is nonzero.

| Candidate | Conclusion and assumptions |
|---|---|
| `zero_C_forces_zero_D` | Eliminates the D vector using the D row, R_D=0, alpha_C=0 and injectivity |
| `zero_C_forces_zero_rhs` | Uses both rows and the same vectors to conclude R_C=0 |
| `nonzero_rhs_forces_nonzero_C` | Retains both rows and R_D=0; concludes alpha_C!=0 from R_C!=0 |
| `fin3_zero_C_forces_zero_rhs` | Requested finite 3+3 block specialization with M_DD packaged as a LinearEquiv |
| `fin3_nonzero_rhs_forces_nonzero_C` | Requested finite-dimensional contrapositive |

The generic statements distinguish D and C types, so M_DC maps C to D and M_CD maps D to C. The concrete specialization uses Vec3 K = Fin 3 -> K for each block. M_DD is a linear equivalence on that space; its underlying linear map and injectivity instantiate the generic result. This represents an invertible 3-by-3 block without matrix inverse syntax or a basis-conversion proof. No symmetry, positive definiteness, Schur complement invertibility, norm bound or invertibility of the full 6-by-6 system is needed.

The scalar hypotheses are only Semiring K plus the relevant module structures; the result therefore specializes to a field such as the reals once a downstream caller supplies that scalar type. The generic proof does not need finite dimension. Injectivity is a deliberately weaker sufficient assumption, while the Fin 3 wrapper explicitly supplies the user-requested invertibility.

## Narrow API and import surface

The only direct imports are `Mathlib.Algebra.Module.Equiv.Defs` and `Mathlib.Algebra.Module.Pi`. The candidate uses linear-map zero preservation, LinearEquiv.toLinearMap/injective, equality transitivity, `intro`, `apply`, `exact` and `simpa only`. It does not use arithmetic automation, finite-case enumeration, matrix determinant/inverse APIs, or classical contradiction automation.

The two module paths were checked as source text at Mathlib revision `0df444a360eaa60ab8c11dca51a86af692955474`:

- [Linear equivalence definitions](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Algebra/Module/Equiv/Defs.lean).
- [Pi module instances](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Algebra/Module/Pi.lean).

This checks source availability only. The current local import environment, typeclass inference for Fin 3 functions, equivalence-to-map coercion and tactic completion have not been checked. No toolchain file, Lake configuration or compiled artifact was created. No umbrella Mathlib or application/source adapter is imported.

## Boundary and minimality

Dropping injectivity invalidates the implication: in a scalar model take M_DD=0, M_DC=0, M_CD=id, M_CC=0, alpha_D=1, alpha_C=R_D=0 and R_C=1. Dropping R_D=0 also invalidates it: with M_DD=M_CD=id, other blocks zero and alpha_D=R_D=R_C=1, alpha_C remains zero. These explanatory algebraic examples are not additional Lean declarations or physical states.

The contrapositive asserts nonzeroness of the C vector as a whole. It does not say each C coordinate is nonzero, give a positive norm floor, prove existence or uniqueness of a solution, or refute a physical trajectory. The filename/task label Q6 does not bind C to any particular physical joint or graph. Application requires independently supplied block-index projections, map identities, both exact row equations, the vanishing D residual and invertibility of the same D block.

There are no DH, CSV, floating-point, ODE or source-admission imports, definitions or bindings. No original source claim, registry entry, graph state or Route-B workflow state was modified. Written scope is restricted to the newly added candidate and this review.

Disposition: pending / OPEN_UNCOMPILED; abstract interface candidates only, with no Lean verification or registry admission claim.
