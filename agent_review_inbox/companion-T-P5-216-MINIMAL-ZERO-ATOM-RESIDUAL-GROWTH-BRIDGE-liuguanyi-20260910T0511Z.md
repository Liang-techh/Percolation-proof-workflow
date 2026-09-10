---
kind: companion_log
review_id: companion-T-P5-216-minimal-zero-atom-residual-growth-bridge-liuguanyi-20260910T0511Z
task_id: T-P5-216-MINIMAL-ZERO-ATOM-RESIDUAL-GROWTH-BRIDGE
source_agent: 柳冠一
created_at: 2026-09-10T05:11:00Z
inspected_commit: 803e7681f61385fee8a9c1c00b97c1d76061ee71
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
---

# 柳冠一协作补充 — T-P5-216

- 当前完成：把 T-P5-215 留下的“complete zero-ray packet”具体化为**全部 support-minimal zero atoms**。已证明 support-minimal zero 等价于 strict-positive corank-one principal kernel；任意 copositive zero 都能分解成这些最小 atom 的非负组合，而且同一分解中的 atom 自动两两 compatible。
- 关键压缩：higher-corank PSD support 不会产生新的 primitive zero ray；其所有极射线已经出现在更小的 corank-one minimal supports 中。因此 atom packet 一旦完整，就不必再对每个 higher-corank support 重复抽取极射线。
- 新的 exact growth gate：对当前 clique 取 `z_C=sum xi_i`、`r_C=K z_C`，候选 atom `eta` 可以加入当且仅当 `supp(eta)` 完全落在 `r_C` 的零坐标中。由于所有单 atom residual 非负，aggregate zero mask 正好是各 residual zero mask 的交集，没有保守性。
- 跨层结果：compatible atom clique 的 support union 自动对应普通 PSD principal block；完整 atom 图中的 maximal cliques 与 maximal zero supports 一一对应，并且 clique cone 就是对应 principal-kernel nonnegative cone。
- 重要边界：这没有解决 minimal atom 本身的最坏指数枚举。尤其不能只从 diagonal-zero singleton 开始 growth；`[[1,-1],[-1,1]]` 的唯一 minimal atom 是 `(1,1)`，没有 singleton zero seed。
- 给其他数学 Agent 的建议：下一步如果继续该线，不要再做 higher-corank ray extraction；优先研究 minimal-support atom enumeration 的 exact branch-and-bound，例如 rank/minor + residual feasibility 的整族剪枝，并给出 completeness 证明。
- 给 Lean Agent 的建议：最小 theorem leaves 可拆为 `minimalZero_iff_corankOnePrincipalKernel`、`zero_decompose_minimalAtoms`、`aggregateResidual_extension_iff`、`clique_unionSupport_psd`、`maximalClique_iff_maximalZeroSupport`。当前没有请求编译，也不应升级 source/admission/registry。
- 关联正式结果：`agent_review_inbox/review-T-P5-216-MINIMAL-ZERO-ATOM-RESIDUAL-GROWTH-BRIDGE-liuguanyi-20260910T0508Z.md`，review commit `803e7681f61385fee8a9c1c00b97c1d76061ee71`。