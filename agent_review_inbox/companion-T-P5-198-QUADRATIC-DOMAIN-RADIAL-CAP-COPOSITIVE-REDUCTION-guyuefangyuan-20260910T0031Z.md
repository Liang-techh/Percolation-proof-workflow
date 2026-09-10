---
kind: companion_log
task_id: T-P5-198-QUADRATIC-DOMAIN-RADIAL-CAP-COPOSITIVE-REDUCTION
review_id: review-T-P5-198-quadratic-domain-radial-cap-copositive-reduction-guyuefangyuan-20260910T0028Z
agent: 古月方源
source_agent: 古月方源
created_at: '2026-09-10T00:31:00Z'
status: handoff
---

# 古月方源协作接力：二次域直接生成 T-P5-197 径向上界

本轮把 T-P5-197 需要的 `beta^T y <= B` 与已有二次域 `y^T P y <= rho` 精确接起来了。给定 `P` 在非负正交锥上 copositive、`beta>=0`、`rho>0`，一个候选有理数 `B>=0` 对整个二次域有效，当且仅当

`B^2 P - rho beta beta^T`

在非负正交锥上 copositive。这个条件是精确 iff，不需要先找共同权重 `w`，也不需要平方根或逆矩阵。

给 source/CSE lane 的建议：如果真实 selector/domain 已经有同键的齐次二次约束 `e^T W e<=rho`，优先直接输出 selector 生成矩阵 `V` 并形成 `P=V^T W V`；然后每个 amplitude majorant `beta_k` 各自找一个有理 `B_k`，检查 rank-one loaded matrix 的 copositivity。这样比强迫所有 generator 共用一个 `w,R,kappa` 更紧，也更容易复用现有 T-P5-157/164/168/170/172 的低维 copositivity 分支。

一个重要实现提醒：不要把 loaded matrix 强制要求 PSD。精确例子 `P=[[1,1/2],[1/2,1]]`、`beta=(1,0)`、`rho=B=1` 时 radial cap `y1<=1` 是 sharp 的，但 loaded matrix `[[0,1/2],[1/2,1]]` 行列式为 `-1/4`，虽非 PSD 却在正交锥上 copositive。反过来，如果存在 `y>=0` 使 `y^T P y=0` 且 `beta^T y>0`，则该方向是真正的无界 obstruction；loaded matrix 会在同一方向给出严格负 witness。

给 Lean lane 的建议：先做纯标量的 `rho*s^2 <= B^2*q` 与 `q<=rho` 推出 `s<=B`；反向证明单独拆 `q=0` recession branch 和 `q>0` boundary-scaling branch。矩阵/outer-product API 可以后置，2x2 情况直接复用已有 root-free copositivity lemma。

尚未闭合的是 actual same-key `W,V,rho,beta_k,B_k` 数据、真实域是否齐次/中心化、Float64 包络、物理轨迹覆盖以及封不觉独立验证；本轮没有把这些数学适配器升级成 source/admission 结论。
