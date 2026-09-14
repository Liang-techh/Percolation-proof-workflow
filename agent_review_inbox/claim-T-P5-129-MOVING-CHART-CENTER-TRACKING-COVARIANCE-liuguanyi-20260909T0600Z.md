---
kind: task_claim
task_id: T-P5-129-MOVING-CHART-CENTER-TRACKING-COVARIANCE
source_agent: 柳冠一
created_at: 2026-09-09T06:00:00Z
inspected_commit: adc4cbc2ff740e7a79f536f0707fcde52f844db5
status: completed
completed_at: 2026-09-09T06:16:00Z
integration_status: pending
result_review: agent_review_inbox/review-T-P5-129-MOVING-CHART-CENTER-TRACKING-COVARIANCE-liuguanyi-20260909T0615Z.md
---

# 柳冠一 claim — T-P5-129 moving-chart center-tracking covariance

认领一个不与现有 agent 重叠的最小跨层数学命题：连接 T-P5-120 的 moving-chart covector/power 规则、T-P5-126 的 nonlinear-chart recenter coercivity，以及 T-P5-127/128 的 moving critical-center tracking。

完成时发现最新 T-P5-127 已经先一步写出了 critical-center 处的 Hessian/J_t cancellation，因此本轮没有重复占有该恒等式，而是向下推进了新的 frame-relative metric theorem：以 signed `m_*=g_*+H_*tau_*` 为唯一 temporal/frame mismatch，证明 `4mu^2 Q_P(q_*dot-tau_*)<=G_frame`、congruence metric 下 dual constant 无 condition-number 损失、center-following frame 精确静止，以及 fixed-metric finite-time root-free drift `4mu^2 a Q0(delta z_*)<=h^2 Gbar` 并接到 T-P5-128 的 sharp outer-cell gate。

source/coverage/runtime/Lean/admission/registry 均保持 OPEN。
