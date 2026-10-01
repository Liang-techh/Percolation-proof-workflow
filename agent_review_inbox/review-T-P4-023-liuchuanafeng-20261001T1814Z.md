---
kind: review_result
review_id: T-P4-023-LIUCHUANAFENG-20261001T1814Z
task_id: T-P4-023
source_agent: 流川枫
created_at: 2026-10-01T12:14:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 9973101df212ea2bb25f20169f81af541cdfaf2b
claim_commit: dfcdc3392187d5b0cce2ec7949d42b9dbe265d31
---

# T-P4-023 audit: weighted Frobenius adapter stays uncompiled

## Exact question

Does the composition

```text
B = S^T S, S invertible, T = R S^{-1}, ||T||_F^2 ≤ rho
  ⇒ ∀ a, ||R a||_2^2 ≤ rho (a^T B a)
```

exist as a pinned Lean theorem, with Route-B names `R`, `B_up`, and `rho_F` bound only in a separate adapter, and with an explicit decision on whether a square-root-free PSD surface can replace a rational Cholesky factor? If not, record the obstruction and an uncompiled interface only.

## Inspected commit / paths

- Pre-claim tree: `9973101df212ea2bb25f20169f81af541cdfaf2b`.
- Claim commit, written before this review: `dfcdc3392187d5b0cce2ec7949d42b9dbe265d31`.
- `agent_review_inbox/task_queue.md` still marks `T-P4-023` as `status: open` (formalization target recorded locally at Route-B revision 413). Owner routing there is 巨阳仙尊 for the finite-dimensional proof and 柳冠一 for the `B_up` adapter. No prior `claim-T-P4-023-*` or `review-T-P4-023-*` was in the inspected tree.
- Workflow lint only, not executed: `scripts/check_routeb_p4_interface_consistency.py` (blob `0fa46b617b57e868ce675a4c976fdfabc63ff122`). It reads `artifacts/routeb_6dof/state.json` and checks that `P4.weighted_frobenius_port_energy_bridge` uses `rho_F^2` and binds `B_up`. Its own docstring says a PASS cannot enter the registry. This pass did not run it and did not call any `record_routeb_*.py` writer.
- Provider contract, design only: `scripts/record_routeb_port_frobenius_bound.py` (blob `3e4eda01919318d3bdcdbca2fe8d4ec9028f36b2`) states `provided_quantity = ||R_port a_B||_2^2 <= rho_F^2 * (a_B^T B_up a_B)` and `source_map = T = R_port B_up^(-1/2)`, and sets `robust_pmi_E_k_equivalent = False`.
- Downstream contract, design only: `scripts/record_routeb_combined_schur_adapter.py` (blob `8c38d357209dfa996dbcaa673e4796112dc094cd`) requires `P4.weighted_frobenius_port_energy_bridge`, fixes `rho` as `rho_F^2`, and records `B_up = diag(1402217/12000000, 200739/4000000)` as an external-document citation, not as a theorem.
- Sibling input: this agent's `review-T-P4-022-liuchuanafeng-20261001T1718Z.md` already leaves the entrywise majorant uncompiled. That file is not reused as a proof of this composition.
- No Lean file for `T-P4-023` was opened. No Lake/Lean command was run. Exit code: not applicable. `#print axioms`: not applicable. Placeholder scan: not applicable.

## Algebraic surface (obligation, not a receipt)

The factorization form is the task target. With `z = S a`, `T z = R a` and `||z||_2^2 = a^T B a`, so

```text
||R a||_2^2 = ||T z||_2^2 ≤ ||T||_F^2 ||z||_2^2 ≤ rho (a^T B a).
```

`T-P4-022` can be consumed only as a separate input, and only after the specialization `U_ij = |T_ij|`, which makes `sum U_ij^2 = ||T||_F^2`. The generic majorant does not supply `rho`, `B_up`, or `R`.

Square-root-free alternate, preferred for the adapter layer:

```text
B ≻ 0 ∧ R^T R ≼ rho B  ⇒  ∀ a, ||R a||_2^2 ≤ rho (a^T B a)
```

equivalently the block matrix `[[rho B, R^T], [R, I]]` is PSD. This avoids exhibiting `S`. It is not a Lean theorem here. Classification: `INTERFACE_DRAFT__UNCOMPILED`.

## Factorization guard

The cited diagonal is positive rational, so a real diagonal square-root factor exists, but it is not rational:

- `12000000 = 2^8 * 3 * 5^6` is not a square, so `1402217/12000000` is not a square in `Q`.
- `4000000 = (2*10^3)^2`, while `448^2 = 200704` and `449^2 = 201601`, so `200739` is not a square. Hence `200739/4000000` is not a square in `Q`.

No rational Cholesky factor is recorded. A receipt that writes `S` with rational entries for this `B_up` should be rejected.

## Notation and non-equivalence

- `rho` in this leaf is `rho_F^2`, matching the squared Frobenius hypothesis and the raw-port budget. Substituting unsquared `rho_F` is a notation failure.
- `||R a_B||_2^2` is not the robust-PMI factor `E_k` in `l_true = l_poly,k + E_k xi`. The provider script already marks that route as not provided.
- A positive Young margin, `RESOLVED` cell status, or a workflow-lint PASS is not kernel evidence.

## Explicit non-admissions

- Not compiled: no pinned Lean theorem, imports, statement identity, or axiom print.
- Not proved: the factorization implication or the PSD block form.
- Not proved: source binding of `R_port`, `B_up`, or `rho_F` to deployed DH/Float64 data.
- Not proved: interval entries, the 5120-cell partition, or coverage.
- Not proved: consumption by `T-P4-024` or residual PMI.
- Not opened: P4/M4 admission. `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the composition is a source-independent finite-dimensional target, and the cited `B_up` forbids a rational Cholesky factor. The in-repo scripts name the contract and the square-root map; they do not discharge it.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction on `T-P4-023`. Do not close `T-P4-022`, `T-P4-024`, or the P4 parent.
2. Do not write `state.json`, the verified registry, or a Lean source file from this review.
3. Next child, out of scope here: a pinned square-root-free lemma `R^T R ≼ rho B → ||R a||_2^2 ≤ rho (a^T B a)` with `#print axioms`, kept free of Route-B names. Binding `B_up` stays a separate adapter.

## Unresolved blockers

1. No Lean file and no compile receipt for either surface.
2. `T-P4-022` is not yet a consumable pinned theorem.
3. The external partition/ledger cited by the provider recorder was not replayed in this pass.

## Response / handoff

流川枫 claimed open `T-P4-023` and recorded a pending fail-closed boundary: the weighted port-energy implication is specified, a rational Cholesky factor is unavailable for the cited diagonal, and the square-root-free PSD surface is only `INTERFACE_DRAFT__UNCOMPILED`. No registry or formal-proof edit.
