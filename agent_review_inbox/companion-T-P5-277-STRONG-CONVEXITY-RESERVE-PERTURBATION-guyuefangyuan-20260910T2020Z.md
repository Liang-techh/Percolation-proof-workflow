---
kind: companion_log
review_id: companion-T-P5-277-strong-convexity-reserve-perturbation-guyuefangyuan-20260910T2020Z
task_id: T-P5-277-STRONG-CONVEXITY-RESERVE-PERTURBATION
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T20:20:00Z
inspected_commit: 027071e5a48bbb6ba67788c47479a24681aeca08
review_commit: 1a6f2fb0616fd3d695673dbae48d4e0f7f789a94
status: completed_math_child
admission_label: pending
---

# 古月方源协作留言 — T-P5-277

- 当前完成：承接 T-P5-276 留下的 strict-convexity perturbation seam。若 nominal fiber target 在一个共同 collar 上有 `p''>=mu>0`，旧 minimizer `tau` 有 reserve `rho`，新 bracket 为 `C=[a,b]`，则先取 nominal constrained minimizer `y=clamp(tau,a,b)`。bracket 移动本身在共同 strong-convexity collar 内不消耗 reserve；若把 `tau` 排除在新 bracket 外，nominal reserve 反而至少增加 `mu*(y-tau)^2/2`。
- 新的 fraction-free gate：若 perturbation `e=p_tilde-p` 满足 `e(y)>=-eps` 与 secant cone `(e(t)-e(y))^2<=D(t-y)^2`，并有可选 bonus witness `(y-tau)^2>=S`，令 `R2=2(rho-eps)+mu*S`。只需 exact scalar 检查 `R2>=0`、`D<=mu*R2`，即可证明整个新 fiber 上 `p_tilde>=eta`。核心恒等式 `(2R+mu s^2)^2-4D s^2=(2R-mu s^2)^2+4(2muR-D)s^2` 完全无 sqrt/division。
- 数学敏感度：若 `x` 是 perturbed target 在新 bracket 上任意全局 minimizer，且 `e'(x)^2<=D`，则 `mu^2(x-y)^2<=D`；无需先解 perturbed critical polynomial，也不要求 perturbed target 自身仍凸。若两端移动平方都 `<=H`，另有 `(y-tau)^2<=H`，从而 `mu^2(x-tau)^2<=2D+2mu^2H`。
- branch-stability：若 nominal derivative 在新两端有严格 margins `p'(a)<=-sigma_L`、`p'(b)>=sigma_R`，而 endpoint derivative errors 的平方严格小于对应 `sigma^2`，再加 `e''>=-nu`、`nu<mu`，则 T-P5-276 的 INTERIOR branch 本身保持，不必重建 root matching。
- 重要 obstruction：bracket 的 zero-debit 只在已认证共同 convexity collar 内成立。给定任意 `h>0`，`p_A(t)=t^2+A(1-t)^3` 在 `[0,1]` 上可有 `p''>=2` 且显式正 reserve，但取足够大 `A` 后在 `1+h` 变负；所以“端点只移动很小”不能替代 collar/source 证明。
- 给其他 Agent 的建议：actual-source 接入时优先寻找同键 `mu,rho,e(y),D`；若 scalar gate 已通过，不要再扩展抽象 root machinery。只有 actual packet 因 `D` 太粗而失败，才值得保留 `e(t)-e(y)` 的 signed polynomial graph 做更锐的 structured perturbation closure。
- 仍未闭合：actual P5 source/endpoint/collar binding、FD/Float64 error packet、state realization、cell/flowpipe/FD/reference-halo coverage、Lean/kernel、封不觉独立验证、admission/registry/parent propagation。
- 关联 Review：`review-T-P5-277-STRONG-CONVEXITY-RESERVE-PERTURBATION-guyuefangyuan-20260910T2019Z.md`；正式数学 commit `1a6f2fb0616fd3d695673dbae48d4e0f7f789a94`。
