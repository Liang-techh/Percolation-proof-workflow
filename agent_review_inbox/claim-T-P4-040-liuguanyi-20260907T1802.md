---
kind: task_claim
task_id: T-P4-040
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T18:02:00-06:00
inspected_commit: ef81e9d0f507af8cb1b815c5fd5846892a5c2c64
scope: compress T-P4-039 common-parameter mathematics into four Lean-friendly division-free algebraic theorems and make the Rat/Real boundary explicit; no source/P8/coverage/admission work
related_tasks:
  - T-P4-037
  - T-P4-038
  - T-P4-039
  - T-P4-041
  - T-P4-042
  - T-P4-043
status: claimed
---

# Claim — T-P4-040

柳冠一认领梁智炜在 revision 742 明确派发的 `T-P4-040`。

本轮只推进 `T-P4-039` 背后的纯代数：把 completed-square、rational-radius feasibility、shared witness 与 strict reserve 压缩成 Lean-friendly、尽量 multiplication-only 的 statement，并明确“外部 exact rational checker 生成 witness / Lean theorem 在 `ℝ` 中消费”的边界。

不重复 `T-P4-041` 的 Lean 编译/receipt，不抢 `T-P4-042` 的 adapter 独立审计，也不处理 `T-P4-043` 的 boundary-only 反例闭包。禁止引入 concrete source、P8、coverage、true-DH、registry/admission 假设。