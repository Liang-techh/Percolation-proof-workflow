---
kind: review_result
review_id: T-P4-023-LIUCHUANAFENG-20261001T1816Z
task_id: T-P4-023
source_agent: 流川枫
created_at: 2026-10-01T12:16:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 4110781a23bb6f121c7ba3d00e2f5afe430818bd
claim_commit: 735f67e72b30eb3460e4e55baae9bbffcf03c5e1
---

# T-P4-023 audit: weighted Frobenius port-energy adapter is still open

## Exact question

Does the recorded composition

```text
B = S^T S, S invertible, T = R S^{-1}, ||T||_F^2 ≤ ρ
  ⇒  ||R a||_2^2 ≤ ρ (a^T B a)  for every a
```

have a pinned Lean receipt, and can the Route-B names `R`, `B_up`, and `rho_F` be bound without a rational Cholesky factor and without promoting interval entries or robust-PMI `E_k`? If not, return the fail-closed obstruction and the square-root-free surface that must stay external.

## Inspected commit / paths

- Pre-claim tree: `4110781a23bb6f121c7ba3d00e2f5afe430818bd`.
- Claim written in `735f67e72b30eb3460e4e55baae9bbffcf03c5e1` as `agent_review_inbox/claim-T-P4-023-liuchuanafeng-20261001T1812Z.md`. This review does not edit that claim.
- `agent_review_inbox/task_queue.md` card `T-P4-023` still `status: open`. Blob of the queue at the inspected tree: `b905132efb6e8a9b356a3023adb6d14905e6d686`.
- Inbox tree at the inspected commit: no prior `claim-T-P4-023-*` or `review-T-P4-023-*`.
- Code search for a Lean theorem naming `B_up` / `rho_F` returned no indexed hit. Absence of an index hit is not a proof that no file exists; no Lean file was compiled in this pass.
- No Lean/Lake compile, checker, or `scripts/check_routeb_p4_interface_consistency.py` run was executed. Exit code: not applicable.

## Algebra recorded, not admitted

The finite-dimensional implication is standard and does not need a square root in the consumer.

Let `z = S a`. Invertibility gives `a = S^{-1} z` and `R a = T z`. The Frobenius norm dominates the induced 2-norm, so

```text
||R a||_2^2 = ||T z||_2^2 ≤ ||T||_F^2 ||z||_2^2 ≤ ρ ||z||_2^2
||z||_2^2 = a^T S^T S a = a^T B a
```

Hence `||R a||_2^2 ≤ ρ (a^T B a)`. This argument consumes a separate Frobenius hypothesis. It does not discharge `T-P4-022`, and it does not turn an entrywise interval majorant into `||T||_F^2 ≤ ρ`.

Square-root-free restatement, which is the adapter surface required by the factorization guard:

```text
B ≻ 0  ∧  ρ B - R^T R  ≽ 0
  ⇔  ||R a||_2^2 ≤ ρ (a^T B a)  for every a
  ⇔  PSD of the Schur block [[ρ B, R^T], [R, I]]
```

`B_up` may be rational diagonal. A real factor `S = B_up^{1/2}` can introduce non-rational square roots. No rational Cholesky factor is asserted. The PSD/Schur form is the preferred theorem surface; `S` stays optional witness data.

Notation guard retained: `ρ` in this card is `rho_F^2`, matching the squared Frobenius hypothesis and the raw-port budget. A receipt that substitutes unsquared `rho_F` is rejected by this audit even if the algebra above is later formalized.

## Typed adapter target (not admitted)

```text
theorem frobenius_port_energy_sqrt_free
    (R : Matrix m n ℝ) (B : Matrix n n ℝ) (rho : ℝ)
    (hB : B.PosDef) (hschur : (ρ • B - R.transpose * R).PosSemidef) :
    ∀ a, ‖R.mulVec a‖^2 ≤ rho * (a ᵀ• B.mulVec a)

theorem routeb_port_adapter_conditional
    (hname : rho = rhoF ^ 2)
    (hB : Bup = declaredRationalDiagonal)
    (hR : R = sourcePortMap)
    (hF : frobeniusBudget sourcePortMap rhoF) :
    ∀ aB, ‖R.mulVec aB‖^2 ≤ rho * (aB ᵀ• Bup.mulVec aB)
```

The second theorem is an adapter. Its premises `sourcePortMap` and `frobeniusBudget` are external. Binding `A_up = a_B^T B_up a_B` for `T-P4-024` is out of scope here.

## What is not proved

1. No pinned Lean theorem, imports, or `#print axioms` receipt.
2. No source binding of `R` to the deployed or lifted port map `R_port`.
3. No proof that interval entries satisfy `||T||_F^2 ≤ rho_F^2`.
4. No identification with robust-PMI `E_k`, a positive ledger margin, or a one-cell sample.
5. No coverage, flowpipe, or P4/M4 admission. `formal_certificate_allowed` and `registry_promoted` are unchanged.
6. The interface-consistency checker was not run; its PASS would be non-authoritative in any case.

## Admission label

`pending`

Strongest statement retained: the card's composition is a source-independent finite-dimensional target, and the square-root-free PSD form avoids inventing a rational factor of `B_up`. Neither form is a kernel receipt, and Route-B names remain unbound.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction on `T-P4-023`. Do not close the parent or consume it as a premise of `T-P4-024`.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Next child, out of scope here: a pinned exact-real theorem for the PSD/Schur surface only, with `rho = rho_F^2` explicit and `B_up` / `R` left as adapter hypotheses.

## Unresolved blockers

1. No compiled theorem for `frobenius_port_energy_sqrt_free`.
2. `T-P4-022` remains a separate input and was not re-audited in this pass.
3. Source equality of `R` and a certified Frobenius budget on the true-DH port are absent.

## Response / handoff

流川枫 claimed open `T-P4-023` and recorded a pending fail-closed boundary: the weighted Frobenius implication is algebraically standard and has a square-root-free PSD form, but there is no pinned Lean receipt and no source binding of `R`, `B_up`, or `rho_F^2`. No registry or formal-proof edit.
