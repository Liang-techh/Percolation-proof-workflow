---
kind: task_claim
task_id: T-P4-018
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-07T05:04:00-06:00
inspected_commit: 2d92d4ba4b97863d2bb6bc77cddf689229637752
status: claimed
---

# T-P4-018 — force/acceleration congruence bridge for the canonical `kc` seam

I claim a new disjoint interface-mathematics child triggered by the scale conflict between `T-P4-017` / `docs/routeb-p4-kc-force-contract.md` and the existing force-native descriptor contract in `docs/routeb-c2-d-normalization-audit.md` / B45-5.

The target is to prove the exact normalization theorem relating the acceleration-style nominal expression `f_B`, the generalized-force residual `l_F = I_B f_B - M0_BB a_B`, and any scalar Schur consumer. In particular I will determine which `kc` coefficient belongs to which coordinate layer, show the congruence transformation needed to transport a Schur theorem between those layers, and give an explicit obstruction to mixing an acceleration-side `kc=1/20` with force-side `p,d` constants without transforming the quadratic form.

This does not take over source authentication, Float64/IEEE interval generation, remote `M_BD a_D`, residual absorption, Lean implementation, validation, provenance/admission, or final P4/M4 integration.
