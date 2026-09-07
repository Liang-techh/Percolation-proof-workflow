---
kind: claim
task_id: T-P4-017
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T04:41:00-06:00
inspected_commit: cd2b1a2962e1dd260701069554f885fd365d83a2
status: claimed
---

# T-P4-017 claim — canonical-scale repair of the aggregate P4 Schur budget

I am taking one disjoint mathematical correction child downstream of `T-P4-011` and the later `T-P4-013/014/015/016` inequality work. The canonical source contract fixes the generalized-force `kc` cross term at `(q5/20,q4/20)`, while several later aggregate-budget reviews instantiate channel 4 with `c=1/100`. I will re-derive the same-coordinate/transverse budget at the canonical `1/20` scale, identify exactly which numerical headroom statements change and which scale-free Schur identities remain valid, and give a concrete counterexample showing that the `6/25` same-coordinate allowance cannot be used against the canonical source term.

This task is mathematical budget repair only. It does not redo provenance, source authentication, IEEE analysis, Lean validation, admission, or final P4/M4 integration, and it does not disturb already claimed P5 or formalization tasks.