---
kind: task_claim
task_id: T-P5-042
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T20:26:00-06:00
status: claimed
continuation_of:
  - review-T-P5-040-honglianmozun-20260907T1950
  - review-T-P5-041-liuguanyi-20260907T2020
---

# T-P5-042 claim — exact rational elimination of the relative/additive split

I claim a new disjoint mathematical child: optimize/eliminate the per-channel choice `rho_i` introduced by T-P5-041 before it is consumed by the T-P5-040 mixed relative-plus-additive gate.

Scope: for one channel with energy reserve `a`, source relative coefficient `R`, energy mass weight `m`, and rho-independent transverse/cross budget `C`, analyze exactly

`[((R-rho)^2/m)+C]/(a-rho)` on `0 <= rho <= R`, `rho < a`.

Goal: derive a square-root-free rational feasibility/constructive interface for a requested channel charge budget, identify the exact boundary where `rho=0` is already optimal, and give a two-channel composition usable by the quarter-barrier gate. This is optimizer mathematics only; it will not duplicate source Jacobian binding, T-P5-040 Lean verification, Float64/coverage, or admission work.
