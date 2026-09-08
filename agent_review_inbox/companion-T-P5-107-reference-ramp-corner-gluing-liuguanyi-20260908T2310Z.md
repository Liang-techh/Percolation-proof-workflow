---
kind: companion_log
task_id: T-P5-107-REFERENCE-RAMP-CORNER-GLUING
source_agent: 柳冠一
created_at: 2026-09-08T23:10:00Z
review_commit: 1b4bb059823129ebf27fc00fb2dcbee9a320ba1c
integration_status: pending
admission_label: pending
---

# T-P5-107 协作补充

本轮承接红莲魔尊 `T-P5-106` 明确留下的 continuous piecewise-affine ramp gluing seam，没有重复其 `B a=g`、slope-energy PSD 或 `pB` bridge。

数学上已经闭合两个边界：

1. 若 `q,v,w` 在 ramp knot 连续，即使 `w'` 左右斜率发生跳变，position-only recenter `z=q-aw, s=v` 与二次 storage `Vc(z,s)` 都严格连续，因此 knot **零 reset debit**。每个 segment 只需 `20 R >= 7 S_j`，有限多段拼接后仍保持同一个 `R`，预算不随 knot 数量累积。
2. 若 `w` 的值本身跳变 `Delta`，则不能免费拼接；精确 reset 为
   `Vc+ - Vc- = -Delta c_s^T x- + (Delta^2/2) a^T(K+D)a`。
   对当前 rational packet，`a^T(K+D)a=11275620/75672601`。另新增 exact certificate `25P-2Q>0`，从而得到 `(c_s^T x)^2 <= (63/8)Vc`，可把真正的 value jump 写成完全无 sqrt/无逆的 rational reset gate。

建议 Lean 拆成纯代数叶 `position_recenter_storage_continuous_at_slope_knot`、`position_recenter_input_jump_energy_identity`、`reference_Qd_le_25_Vc`，以及一个独立 scalar analysis 叶 `piecewise_dissipative_collar_glue`。不要把 slope jump、input value jump 和 amplitude/domain cap 合并成一个 generic disturbance budget，否则会丢掉 T-P5-106 已证明的结构消去。

仍未闭合：actual `referenceKey`、真实 ramp partition/slopes、source/runtime coefficient semantics、`Wbar`、whole-path/FD/reference halo、P8 flowpipe、Lean/kernel、封不觉独立验证及 admission/registry。
