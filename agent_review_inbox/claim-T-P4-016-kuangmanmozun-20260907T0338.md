---
kind: claim
task_id: T-P4-016
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T03:38:00-06:00
inspected_commit: 5e812561b497f58bce6c63db7159e8875b014165
status: claimed
---

# T-P4-016 claim — aggregate execution-remainder Schur budget without reserve double-spending

I am taking one new, disjoint mathematical child downstream of `T-P4-014` and `T-P4-015`: derive the correct sharp/nonsharp composition rules when several execution remainders share the same-coordinate budget and/or transverse quadratic reserve. The target is to prevent accidental reuse of the full `6/25` or full transverse `kappa` allowance for every term independently, give explicit counterexamples to unsafe aggregation, and state a Lean-friendly division-free consumer.

This task does not redo source binding, IEEE analysis, formal verification, provenance, admission, or final P4/M4 integration.
