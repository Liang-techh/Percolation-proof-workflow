---
kind: task_claim
task_id: T-P5-020
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T07:32:00-06:00
inspected_commit: 06c1f2528e2146221f10596a69b92921ccaff9e4
status: claimed
---

# T-P5-020 — centered residual small-gain / anchor-split contraction

Claim a new disjoint mathematical child continuing `T-P5-018` and `T-P5-019`.

Scope: derive a source-independent theorem that routes the actual-minus-nominal block-(4,5) residual into (i) a centered state-increment branch controlled by a same-domain Lipschitz/Jacobian bound and (ii) a nominal-anchor additive branch. Use the direct residual metric `5 ||x+y||^2 <= 17 Q` to obtain exact rational small-gain and barrier thresholds, plus a checker-facing Jacobian/Frobenius sufficient condition.

Boundary: mathematics only. Do not re-audit provenance/admission, do not duplicate the existing `T-P5-019` direct metric or FD affine-box adapter, and do not claim Float64/source binding, P8 flowpipe coverage, P5/P8/M4 closure, or registry promotion.
