---
kind: review_result
review_id: review-T-P4-KC-COORDINATE-ADAPTER-liuchuanafeng-20261002T1321Z
source_agent: 流川枫
created_at: 2026-10-02T13:21:00Z
inspected_commit: a0f127e028de29009438041cfe8cfc6df06cd510
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - examples/routeb_b45_5_residual_decomposition_lean/README.md
  - examples/routeb_b45_5_residual_decomposition_lean/DERIVATION.md
  - examples/routeb_b45_5_residual_decomposition_lean/ResidualDecomposition.lean
  - examples/routeb_b45_5_residual_decomposition_lean/COMPILE_RECEIPT_forceScaleKc_20260907.md
  - examples/routeb_b45_5_residual_decomposition_lean/FINAL_RECEIPT.md
  - examples/routeb_b45_5_residual_decomposition_lean/verify.sh
task_id: T-P4-KC-COORDINATE-ADAPTER
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P4-KC-COORDINATE-ADAPTER admission probe: normalized-to-force map

## Question

At commit `a0f127e028de29009438041cfe8cfc6df06cd510`, do `forceScaleKc_eq_rhoKc` and `rhoKc_sq_le_of_block_energy` already discharge the exact normalized-to-force adapter, and can that adapter be admitted as DH equivalence, residual absorption, domain coverage, or M4 closure?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The current Lean sidecar states the requested coordinate map and the local block-energy budget. That statement matches the queue contract as an exact-real adapter only. It does not bind deployed source, and this pass did not re-run the pinned compiler.

This is not `rejected`: the map was not disproved. It is not a fresh `compiled_candidate` from this agent: `verify.sh` was not executed here, and the two checked-in receipts do not share a source SHA-256. It is not `verified`. It is not `architecture_only`: the object is a concrete theorem statement, not only a design note.

## Evidence inspected (read-only)

1. **Queue contract is still open and narrow.**
   `task_queue.md` lists `T-P4-KC-COORDINATE-ADAPTER` as `open`. Required object: compile/inspect `forceScaleKc_eq_rhoKc` and `rhoKc_sq_le_of_block_energy`, mapping normalized `(q5/20,q4/20)` through `diag(1/5,1/10)` to force `(q5/100,q4/200)`, with block-domain budget `||rho_kc||^2 <= 7/18750`. Forbidden: treating the adapter as DH equivalence, domain coverage, residual absorption, or M4 closure.

2. **Canonical sidecar states that map, with index order explicit.**
   `ResidualDecomposition.lean` git blob `bc765fa9a2de1bda886e8d8f3c5e55d620dc52d3`. `Vec2` is destructured as `⟨q4, q5⟩`, so `.1 = q4` and `.2 = q5`.
   - `rhoKcNormalized q = (q.2/20, q.1/20) = (q5/20, q4/20)`.
   - `forceScaleKc q = ((1/5)*(q5/20), (1/10)*(q4/20)) = (q5/100, q4/200)`.
   - `rhoKc q = (q.2/100, q.1/200) = (q5/100, q4/200)`.
   - `forceScaleKc_eq_rhoKc` is `ring` after `Prod.ext`.
   - `rhoKc_exact` is `rfl` to `(q.2/100, q.1/200)`.
   Force and normalized coordinates stay distinct. No sorry/admit token appears in this source.

3. **The budget is the stated conditional inequality, and it is sharp on paper.**
   `rhoKc_sq_le_of_block_energy` assumes `(3/2)(q4^2+q5^2) <= 28/5` and concludes `rhoKcSq q <= 7/18750`, proved by `nlinarith`. Expanding the conclusion gives `(q5/100)^2 + (q4/200)^2 = (4 q5^2 + q4^2)/40000`. On the energy disk `q4^2+q5^2 <= 56/15`, the maximum of `4 q5^2 + q4^2` is `224/15` at `q4=0`, and `(224/15)/40000 = 7/18750`. The hypothesis remains an external domain premise; the theorem does not prove that every certification cell satisfies it.

4. **Checked-in receipts are historical and not interchangeable.**
   - `COMPILE_RECEIPT_forceScaleKc_20260907.md` blob `341cd707af0934f8c07031361e153b78b4cfd9e2` records Lean `4.33.1` commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`, compile exit `0`, theorem-check exit `0`, source SHA-256 `3946389828B94AFF3B258A4635B58A7CA1BE6FF2CE4414E9BEF9553E25653CC9`, and axioms `propext`, `Classical.choice`, `Quot.sound` for both adapter theorems. It explicitly leaves source comparator, Float64 binding, and registry promotion open.
   - `FINAL_RECEIPT.md` blob `63407fc136b09de7a411005bfdf23c12ab8934dc` records the same toolchain pins and exit `0`, but source SHA-256 `efb2222f53d9fbc6ed18927c94b09a15ccc9f6eba9c3e96e7a9b756c95053d2e`. That is not the force-scale receipt hash.
   This pass did not recompute either SHA-256 and did not re-run `verify.sh`. That script pins a machine-local Lean path `/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean` and cache `/home/z5242/sos_lean`, so it is not a portable replay from this review.

5. **README and derivation keep the source premise outside the adapter.**
   `README.md` blob `0009465c98cc0a8fc5e85d52f8f5b30500f82d08` and `DERIVATION.md` blob `ebdbef325847642a76b6ad1d595d4cb25da3c103` say the force cross term matches the normalized `kc=1/20` image under `diag(1/5,1/10)` only as a conditional algebraic candidate. `residual_decomposition` still takes `hdesc : sourceForce = vadd (massBB aB) remote` as an explicit hypothesis and does not discharge `M_BD(q) a_D`.

## Obstruction

The adapter statement is present. The open obligations are replay and binding, not a missing formula:

```text
replay: verify.sh was not run in this pass; local toolchain path is not portable
receipt_identity: FINAL_RECEIPT source SHA-256 != COMPILE_RECEIPT source SHA-256
source_binding: deployed tau / dhport_lib.jl equality not claimed
domain: (3/2)(q4^2+q5^2) <= 28/5 remains an external premise
remote: M_BD(q) a_D is not supplied by forceScaleKc_eq_rhoKc
```

## Assumptions still required

- fresh pinned compile on the current blob, with matching source SHA-256;
- source comparator for deployed `kc`, `I4=1/5`, `I5=1/10`, and index order `(q4,q5)`;
- a cell witness before the energy hypothesis can be used;
- force coordinates kept distinct from normalized `f` coordinates and from acceleration residuals.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-KC-COORDINATE-ADAPTER` open.
- Requested action: do not treat the 2026-09-07 receipts as a fresh compile of blob `bc765fa9a2de1bda886e8d8f3c5e55d620dc52d3`, and do not promote the coordinate adapter to DH equivalence, residual absorption, coverage, or registry. Do not edit registry, `state.json`, or formal certificates.
- Next owner should re-run the pinned checker against the current file and return exit code, source hash, and `#print axioms` in one receipt.

## Forbidden-boundary compliance

- Did not treat the coordinate adapter as DH equivalence.
- Did not treat the budget theorem as domain coverage or residual absorption.
- Did not close P4 or M4.
- Did not edit registry, state, task queue, or formal proofs.
