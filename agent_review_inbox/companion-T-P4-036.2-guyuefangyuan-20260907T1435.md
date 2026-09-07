---
kind: companion_log
task_id: T-P4-036.2
source_agent: 古月方源
created_at: 2026-09-07T14:35:00-06:00
integration_status: pending
related_review: review-T-P4-036.2-guyuefangyuan-robust-phase-cells-20260907T1434
---

# 协作留言

- 当前完成：把 T-P4-036.2 的 exact interval/range-reduction 数学从单个 theta2 行推广到全部 6 个 theta + 6 个 alpha 行，并进一步给出“上游角度形成误差 eps → exact sin/cos 目标盒”的统一鲁棒接口。
- 关键简化：exact-real 下 `x=q+k*pi/2` 再减同一个 `k*pi/2` 后严格就是 `q`，因此这一层不需要 `piBox` 或 CSV `reducedRowSound` 前提；只需 `|sin r|<=|r|` 与 `1-r^2/2<=cos r<=1`。对 theta 的 `q∈[-3/20,3/20]`，统一得到 `|sin q|<=3/20`、`cos q>=791/800`；alpha 六行则退化成精确 quarter-turn 点值。
- 新接口：若 `.1` 能证明实际 Float64 形成角 `xhat` 的 real-lift 满足 `|xhat-(q+k*pi/2)|<=eps`，则数学层自动得到 reduced radius `|rhat|<=3/20+eps`（alpha 为 `<=eps`），再按 phase `-1/0/+1` 生成 exact trig cell。这样 `.3` 只需独立证明 libm 输出包住 `Real.sin/cos xhat`，不需要把 libm 内部 range reduction 混进数学证明。
- 给其他 Agent 的建议：形式化 Agent 优先做 `base_trig_cell_of_abs_le`、`formed_angle_error_to_reduced_radius`、`phase_neg/zero/pos_quarter_cell` 四类最小 theorem；source/runtime Agent 则只负责导出每行 angle-formation error radius 与独立 libm inclusion。不要再把 CSV trig endpoint 当作 exact-real theorem 的 premise。
- 仍未解决：Float64 形成误差的真实数值、libm/runtime 语义、authority receipt、parent/sibling coverage、D1/D2/D3 propagation 与 O2 admission；这些继续 fail-closed。
- 关联结果：`review-T-P4-036.2-guyuefangyuan-robust-phase-cells-20260907T1434.md`。
