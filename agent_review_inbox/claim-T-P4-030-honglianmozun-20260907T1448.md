---
kind: task_claim
task_id: T-P4-030
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T14:48:00-06:00
integration_status: pending
continuation_of:
  - abce0d21c9ff175afb5ddc989cce0d6d01ccc686
  - 727086574670cb753dbd3212161ac9589f649111
---

# Claim — T-P4-030

Scope: handle the dissipation/co-state algebra requested by 梁智炜 after the Route-B force-port sign correction. Starting from the nominal-distal identities `M_DD*v + DeltaM_DB*a_B = 0`, `r_B - M_BD*v = 0`, and the corrected physical port map `R_port = -M_BD*M_DD(mu)^(-1)*(M_DB-M0_DB)`, derive a minimal sign ledger for linear power/co-state/cross-term consumers, while separating the globally sign-invariant norm-square/Frobenius/Schur consumers that may reuse `R_gain=-R_port`.

Deliverable: (i) exact elimination showing `r_B=R_port*a_B`, (ii) a parity/sign theorem distinguishing odd linear consumers from even quadratic contractions, (iii) sign-safe Young/Schur inequalities and cancellation identities, (iv) an explicit obstruction boundary for any downstream consumer whose coefficient binding is not visible, and (v) candidate Lean/exact-algebra theorem statements suitable for a small sidecar.

Boundary: this claim does not redo the source formula audit, Frobenius bound, evaluator enclosure, Float64/solve semantics, controller damping reconciliation, provenance/admission, registry promotion, or independent verifier receipt. `柳冠一` retains source notation/binding work and `封不觉` retains independent sign-consistency verification.
