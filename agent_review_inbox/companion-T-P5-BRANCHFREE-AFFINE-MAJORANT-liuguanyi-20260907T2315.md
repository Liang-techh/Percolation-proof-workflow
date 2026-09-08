---
kind: companion_log
task_id: T-P5-BRANCHFREE-AFFINE-MAJORANT
review_id: review-T-P5-BRANCHFREE-AFFINE-MAJORANT-liuguanyi-20260907T2312
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T23:15:00-06:00
integration_status: pending
admission_label: pending
---

# T-P5-BRANCHFREE-AFFINE-MAJORANT 协作留言 — 柳冠一

- 当前完成：把 T-P5-051 的正定 / 奇异 PSD / 零矩阵分支压成一个**固定正预算 `kappa` 的无分支二标量 gate**。在 T-P5-045 的 `sigma=k45+k54` 坐标下，只需同点证明 `b4²+b5² <= 4*kappa*(p+s)` 与 `s*b4²-sigma*b4*b5+p*b5² <= kappa*(4ps-sigma²)`，即可对所有 `(u4,u5)` 得到 affine energy 项 `<=kappa`；反过来这两个条件对 `kappa>0` 也是必要的。
- 数学关键：定义 `G_kappa=4*kappa*H-bbᵀ`，得到精确恒等式 `4*kappa*(Q+b·u+kappa)=uᵀG_kappa u+(b·u+2*kappa)²`。两个 gate 恰好是 `G_kappa` 的 trace/determinant 非负条件，所以跨 `det(H)>0` 到 `det(H)=0` 时不需要除 `Delta`、求逆、开根或切换 theorem API。奇异边界的 kernel compatibility 会由第二个 gate 自动强制，range 方向的 bias 大小则由第一个 gate 收费。
- 发现的问题：source cell 靠近奇异边界时，不能先独立取 `D4=4ps-sigma²` 的下界和 `N=s b4²-sigma b4b5+p b5²` 的上界。精确族 `p=t²,s=1,sigma=0,b4=2t,b5=0,t∈[0,1],kappa=1` 满足 `kappa*D4-N≡0`，但独立 extrema 给 `D4_lower=0,N_upper=4`，会把真实可证 cell 误判失败。
- 给其他 Agent 的建议：source/interval lane 应直接 enclosure 两个**相关多项式余量** `Rtr=4*kappa*(p+s)-(b4²+b5²)`、`Rdet=kappa*(4ps-sigma²)-(s b4²-sigma b4b5+p b5²)`，不要先拆成独立区间再组合；signed `sigma` 仍必须在 entrywise abs 之前形成。Lean lane若接手，只需做 scaled 2×2 trace-det 非负 lemma、completion ring identity 和 two-gate consumer，不必搭矩阵谱 API。
- 建议的下一步：寻找 deployed signed `(u4,u5)` Jacobian/affine remainder 是否能在同一 source cell 直接输出 `Rtr/Rdet` 的 interval lower bound；若只能输出旧 `K_path` 绝对包络，则继续走保守 fallback，不要伪装成本 gate。
- 关联任务/Review：`T-P5-BRANCHFREE-AFFINE-MAJORANT`、`T-P5-045`、`T-P5-051`；不占用 `T-P5-049` varying-curvature Helly 或 `T-P5-050` Lean lane。
