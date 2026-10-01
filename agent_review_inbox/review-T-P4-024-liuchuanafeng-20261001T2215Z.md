---
kind: review_result
review_id: T-P4-024-LIUCHUANAFENG-20261001T2215Z
task_id: T-P4-024
source_agent: 流川枫
created_at: 2026-10-01T22:15:00Z
integration_status: pending
admission_label: pending
inspected_commit: 871ccd7f4abc0d925d7bdb2d05847250e228d6e1
---

# T-P4-024 audit: combined-Schur adapter is not source-bound

## Exact question

Does the open leaf `T-P4-024` have, at the inspected commit, a pinned Lean theorem plus a source-binding receipt for the exact implication

`theta>0 ∧ ||r||_2^2 ≤ rho*A ∧ b ≥ (1+theta)||l||_2^2 + (1+1/theta)rho*A ⇒ ||l+r||_2^2 ≤ b`,

with `lambda=1+1/theta>1` fixed per cell, `A=A_up=a_B^T B_up a_B`, and `rho` equal to `rho_F^2`, without identifying this budget with robust-PMI `E_k`? If not, record the obstruction only.

## Inspected commit / paths

- Commit: `871ccd7f4abc0d925d7bdb2d05847250e228d6e1`.
- `agent_review_inbox/task_queue.md` (blob `b905132efb6e8a9b356a3023adb6d14905e6d686`): `T-P4-024` remains `status: open` (formalization target recorded locally at Route-B revision 413). Required deliverable is the smallest pinned Lean theorem, exact statement identity, and a source-binding receipt for the declared base residual and `B_up` energy. Forbidden: treating a positive ledger margin, Float64 source, solver status, or one-cell result as kernel verification or P4/M4 closure.
- Prior inbox result, not rewritten: `agent_review_inbox/review-T-P4-024-kuangmanmozun-20260907T1248.md` (blob `fed4f3a6b4901855e7b75242e45415707ad0cea2`). It derives the source-independent Young/Schur identities, including the division-free relation `lambda*||l||^2 + lambda*(lambda-1)*||r||^2 - (lambda-1)*||l+r||^2 = ||l-(lambda-1)*r||^2`, and explicitly leaves `l_base` / `A_up` binding, coverage, and Lean receipt open. Its own admission is `pending`. Inspected commit of that review was `cf9e5735f81c955380d8006a45026c504e869287`, not this commit.
- In-repo sidecar: `examples/routeb_p4_young_feasibility_lean/P4YoungFeasibility.lean` (blob `038e3944fa19fadec331234bc9a47c166b2af03d`) and README (blob `0a70cc92f91dc58f1c9061b9f2faeaa666580e82`). Namespace `RouteBP4YoungFeasibility`. Public surface includes `youngCost`, `young_gap_mul_identity`, `young_scalar_budget_mul_iff`, `young_scalar_lambda_constructive`, `young_scalar_strict_margin_constructive`. The file header and README say it formalizes the scalar review `review-T-P4-038-guyuefangyuan-20260907T1521.md`, not the vector consumer of `T-P4-024`. It does not bind concrete `A`, `P`, `D`, or `m`, and it does not mention `l_base`, `a_B`, `B_up`, or `rho_F^2`.
- Toolchain pin recorded in that sidecar: Lean `4.32.0` (`examples/routeb_p4_young_feasibility_lean/lean-toolchain`, blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`). `verify.sh` was not executed in this pass. Exit code: not applicable. `#print axioms`: not re-run. Placeholder scan: the inspected Lean file contains `#print axioms` lines and no `sorry` / `admit` token in the retrieved text; that is a text scan, not a compile receipt.

## Quantity separation

- Task `A` means `A_up = a_B^T B_up a_B`. The sidecar symbol `A` is an unbound scalar in `youngCost`.
- Task `rho` means `rho_F^2`. The sidecar has no `rho` parameter.
- Task port residual is a vector `r` with `||r||_2^2 ≤ rho*A`. The sidecar consumes scalar `P`, not a vector residual.
- Robust-PMI factor `E_k` in `l_true = l_poly,k + E_k xi` is not a hypothesis of either the prior `T-P4-024` review or the sidecar. They remain non-interchangeable.
- `lambda=1+1/theta` in the task must stay a fixed per-cell rational. The sidecar theorem `young_scalar_lambda_constructive` builds `lambda = 1 + 2*A/G` from scalar slack `G`. That is a different, state/slack-dependent witness and is not the `T-P4-024` PMI block
  `[[b_base - lambda*rho*A_up, l_base^T], [l_base, ((lambda-1)/lambda) I_2]]`.

## What is not discharged

The prior review is a mathematical sketch of the abstract inequality. It is not a kernel receipt. The in-repo Lean file is a scalar Young feasibility sidecar for another leaf. Neither supplies:

- a pinned compile of `combined_port_energy_lambda_mul` or the affine-PMI Schur equivalence named in the prior review;
- a source equality identifying `l` with `l_base` and `R` with `rho_F^2 * a_B^T B_up a_B`;
- a `T-P4-023` port-energy premise receipt consumed as a hypothesis rather than assumed;
- all-cell coverage, flowpipe, or terminal transfer.

No positive ledger margin was used.

## Explicit non-admissions

- Not proved: the vector implication is kernel-checked at this commit.
- Not proved: `A_up` and `l_base` are bound to a declared base residual and `B_up` energy.
- Not proved: `examples/routeb_p4_young_feasibility_lean` instantiates `T-P4-024`.
- Not proved: a successful sidecar compile, if later produced, would be more than `compiled_candidate`.
- Not proved: residual decomposition, Float64/DH correctness, coverage, or P4/M4 closure.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the abstract combined-Schur consumer remains a source-independent sketch, and the only related Lean sidecar is the scalar T-P4-038 feasibility file. The open leaf is not discharged.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction on `T-P4-024`. Do not close the parent.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Do not treat `RouteBP4YoungFeasibility.young_scalar_lambda_constructive` as the required affine PMI block.
4. Next child, out of scope here: one source-independent vector theorem with pinned Lean receipt, still below registry, before any `l_base` / `A_up` adapter.

## Unresolved blockers

1. No pinned Lean receipt for the vector / affine-PMI statement of `T-P4-024`.
2. No source-binding receipt for `l_base`, `a_B`, `B_up`, or `rho_F^2`.
3. The existing scalar sidecar uses a slack-dependent `lambda = 1 + 2*A/G`, which the task forbids as a state-dependent parameter inside the Route-B affine PMI.

## Response / handoff

流川枫 claimed open `T-P4-024` and recorded a pending fail-closed boundary at `871ccd7f4abc0d925d7bdb2d05847250e228d6e1`. The prior algebraic review and the scalar Young sidecar do not meet the source-binding or pinned-vector-theorem deliverable. No registry or formal-proof edit.
