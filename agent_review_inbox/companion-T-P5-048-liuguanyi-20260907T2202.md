---
kind: companion_log
review_id: companion-T-P5-048-liuguanyi-20260907T2202
task_id: T-P5-048
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T22:02:00-06:00
related_review: review-T-P5-048-liuguanyi-20260907T2200
review_commit: fafee85feac4eb47874b374b2e623450bef3e7cc
integration_status: pending
admission_label: pending
---

# T-P5-048 协作摘要

本轮没有发现梁智炜新的点名，也没有重做 T-P5-046/T-P5-047 的单门/双门优化。新结果解决的是一个更上层的跨 cell 接口：如果最终 P5 证书必须冻结同一个 `r`，那么有限多个 `(cell, consumer)` gate 如何共享这个参数，以及各 cell 的二次曲率不同时怎样安全接入。

对共同曲率 `f_i(r)=A_i+B_i r-d r^2`，有限族的共享严格可行性只需检查：`r=0`、`r=1`、每一行的顶点、每一对行的交点。顶点候选 `r_i=B_i/(2d)` 对任意第 `k` 行的无除法检查是

`4d A_k + 2 B_k B_i - B_i^2 > 0`。

两行交点用 `c=A_i-A_j`、`q=B_i-B_j`，若 `c(c+q)<0`，则候选在 `(0,1)`；对任意第 `k` 行只需检查

`q^2 A_k - B_k c q - d c^2 > 0`。

因此有限族仍然不需要 `r` 网格、平方根或浮点优化。候选总数最多是 `2+n+n(n-1)/2`。

真正重要的阻塞是：跨 cell 时 `d_i` 往往由 `sL_i` 决定，因此不能默认相同。不同曲率时，两行之差变成二次式，不再是 T-P5-047 使用的仿射式。精确反例

`f1=3/16-r^2`，`f2=r-2r^2`

有

`f1-f2=(r-1/4)(r-3/4)`，

在 `[0,1]` 内有两个交点。也就是说，如果 adapter 丢掉 `d_i` 字段后仍调用“至多一个 crossover”的 shared-r theorem，会产生真正的数学错误。

给出的安全 bridge 是 curvature homogenization。取统一有理数 `D>=d_i`，并允许每行选一个有理 pivot `c_i`，定义

`g_i(r)=f_i(r)-(D-d_i)(r-c_i)^2`。

则 `g_i(r)<=f_i(r)` 对所有实数 `r` 成立，而且所有 `g_i` 都具有相同曲率 `-D`。展开后仍是 exact-rational 二次式，因此可以直接送入有限族 shared-r checker。损失完全显式，就是 `(D-d_i)(r-c_i)^2`；在 `r=c_i` 处零损失。若已知真 witness 有 margin `eta_i`，只要该 square tax 小于 `eta_i`，同一个 witness 就能通过 homogenized family。

建议后续 typed contract 把 `d` 作为每个 gate row 的一等字段，严格区分 `SameCurvatureBundle` 与 `VaryingCurvatureBundle`。后者只有在补了 `D>=d_i` 和 square-minorant witness 后才允许复用共同曲率 theorem。

Lean 最小优先级建议：先做 `same_curvature_vertex_eval_mul`、`same_curvature_cross_eval_mul`、`curvature_homogenized_minorant`、`pivoted_curvature_homogenized_minorant` 和 explicit-candidate soundness；有限 lower-envelope 的 completeness theorem 可后置，因为正证书只需要 soundness，而宣告“所有候选都失败所以无解”才需要 completeness。

当前仍是 `pending mathematical/interface child`。source/Float64、真实 cell 数据、first-exit/P8 coverage、Lean/kernel/comparator 与 admission 均未触碰。
