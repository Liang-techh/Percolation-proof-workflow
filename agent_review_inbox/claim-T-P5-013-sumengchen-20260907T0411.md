---
kind: task_claim
task_id: T-P5-013
agent: 苏梦辰
source_agent: 苏梦辰
claimed_at: 2026-09-07T04:11:00-06:00
inspected_commit: 0beefb27b191335807f0fd46163a1e532128c062
status: claimed
---

# T-P5-013 — Lean pointwise finite-horizon energy-budget formalization

I claim only the formalization lane of 红莲魔尊's `review-T-P5-013-honglianmozun-20260907T0358.md`. The first target is the source-independent pointwise algebra: square-only weighted-dual work charging, the mixed cubic/remainder/ramp ledger, and the exact rational 50/50 `T=1` headroom criterion. If these compile cleanly, the calculus first-exit lemma will remain a separate next child rather than being hidden inside the algebraic sidecar.

This claim does not take over 柳冠一's `T-P5-014` source-to-weighted-dual adapter, source/IEEE interval generation, `S_F`, `Hbar`, `Rbar`, `W_min`, P8 ramp-domain coverage, ODE existence/continuation, validation, admission, or P5/M4 closure. It also does not modify the already compiled `T-P5-011` sidecar.
