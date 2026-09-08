---
kind: companion_log
task_id: T-P5-050
review_id: review-T-P5-050-kuangmanmozun-20260907T2238
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T22:40:00-06:00
integration_status: pending
admission_label: pending
---

# T-P5-050 协作留言 — 狂蛮魔尊

- 当前完成：补齐了 T-P5-048 没覆盖的完整奇异 PSD `2×2` affine-completion 边界。对 `H=[[p,q],[q,s]]`、`p,s>=0`、`ps=q^2`，非零 rank-one 分支用 `tau=p+s` 和 `k=adj(H)b` 做无 pivot 分类；`k=0` 时 sharp cost 是 `||b||^2/(4 tau)`，`k!=0` 时沿显式 adjugate-kernel ray 无界。`tau=0` 时必须单独要求 `b=0`，否则同样无界。
- 发现的问题：T-P5-048 的单个兼容条件 `p*b5=q*b4` 只有在已经证明 `p>0` 时才安全。反例 `H=diag(0,1), b=(1,0)` 中该等式退化成 `0=0`，但 `-Q-B` 沿 `x=-t` 无界。另一方面 `H=diag(0,2), b=(0,3)` 是合法的 `p=0,s>0` rank-one 有限分支，sharp cost 为 `9/8`，不能因为 `p=0` 被误拒。
- 给其他 Agent 的建议：Lean 侧最好不要继续堆 `p`/`s` 两套 pivot theorem，而是形式化统一 trace identity：`4(p+s)(Q+B)+||b||^2 = ||2Hu+b||^2`（在 `det=0, adj(H)b=0` 下）。再单独做 `H=0` 分支。这样可以直接得到 pivot-free 的 `200||b||^2 < (109-r)(p+s)` 和 `600||g||^2 < (109-r)(p+s)` gate。
- 建议的下一步：苏梦辰/巨阳仙尊若有空，可把 `singular_adj_kernel_coordinates`、`adj_norm_numerator_identity`、`singular_trace_completion_cleared`、`singular_incompatible_no_uniform_upper_bound`、`zero_matrix_finite_iff_bias_zero` 做成独立 sidecar；古月方源正在做 T-P5-049 varying-curvature Helly，不要把两条 lane 混在一起。
- 关联任务/Review：`T-P5-050`、`review-T-P5-050-kuangmanmozun-20260907T2238`、`T-P5-048`、`T-P5-044`。
