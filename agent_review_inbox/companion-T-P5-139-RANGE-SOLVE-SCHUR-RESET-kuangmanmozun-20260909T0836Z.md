---
kind: companion_log
task_id: T-P5-139-RANGE-SOLVE-SCHUR-RESET
source_agent: 狂蛮魔尊
created_at: 2026-09-09T08:36:00Z
review_path: agent_review_inbox/review-T-P5-139-RANGE-SOLVE-SCHUR-RESET-kuangmanmozun-20260909T0834Z.md
review_commit: f0198916eb5fe1783cbeb9055031c9d9bd0dc954
admission_label: pending
integration_status: pending
---

# T-P5-139 companion — 固定 multiplier 的 range-solve Schur closure

本轮把 T-P5-138 固定 `tau` 后仍需检查的 rank-one PSD 矩阵进一步压成了“一个 exact 线性方程 + 一个 scalar floor”。设

`K=H+tau G`, `e=E-C-tau R`，若 `K>=0` 且存在 `y` 满足 `K y=b`，则恒等式

`4[x^T Kx-t b^T x+e t^2] = (2x-t y)^T K(2x-t y)+t^2(4e-b^T y)`

说明只要

`4e-b^T y>=0`

就得到完整 augmented Schur PSD。反向也 sharp：若 block PSD，直接代 `(x,t)=(y,2)` 就得到 `4e-b^T y>=0`。因此固定 `tau` 的最小 certificate floor 由

`4(E-C-tau R)=b^T y`

精确决定，不需要 inverse、sqrt、pseudoinverse、augmented LDL 或 rank-one PSD 检查。

奇异 `K` 也可以合法消费：若 `Ky=b` 有多个解，则 `b^T y` 对所有解相同；真正的 obstruction 是 `b` 看到了 `ker K`。二维 exact 例子 `K=diag(0,2), b=(0,3)` 给 `y=(0,3/2)`、`b^T y=9/2`，对应物理 ellipsoid reset 的真实最优值精确为 `17/8`。相反 `b=(1,0)` 时没有解，任何有限 floor 都无法使这个固定 multiplier 的 block PSD。

给 source/CSE 的最小下一步：冻结一个 rational `tau` 后，输出同键 `K_tau` 的 exact PSD witness、rational `y_tau`、等式 `K_tau y_tau=b` 和 scalar reserve `4(E-C-tau R)-b^T y_tau`。若 solve 不一致，就直接给 nullspace witness 并移动 `tau`；若 scalar reserve 为负，`(y_tau,2)` 本身就是 exact rejection witness。

当前仍是 `CONDITIONAL_PASS / pending`；未升级 actual source、same-cell coverage、Float64/controller、P8、Lean/kernel、独立验证、admission、registry 或 P5/M4 parent closure。
