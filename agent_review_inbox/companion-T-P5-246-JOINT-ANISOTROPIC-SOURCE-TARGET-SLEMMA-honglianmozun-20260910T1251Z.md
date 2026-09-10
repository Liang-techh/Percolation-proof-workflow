---
kind: companion_log
task_id: T-P5-246-JOINT-ANISOTROPIC-SOURCE-TARGET-SLEMMA
source_agent: 红莲魔尊
created_at: 2026-09-10T12:51:00Z
inspected_commit: c472530e93129c6972b0ee8354327ea8b6b0e9d5
review_commit: f4457fd93d95b1ed58c5ec4f3fbb995a2f73fb9a
admission_label: pending
---

# T-P5-246 协作交接 — 红莲魔尊

本轮完成了 T-P5-245 留下的联合 source/target 相关性 seam。核心不是继续给中心位移 `h`、`DeltaA`、`Deltal`、`DeltaG` 分别做绝对值预算，而是先把移动后的 source 精确重心化，再只看重心化后的有效误差：

`deltaG=DeltaG`，

`deltal_h=Deltal+(G+DeltaG)h`，

`deltaA_h=DeltaA+2(l+Deltal)^T h+h^T(G+DeltaG)h`。

这三个量直接进入一个 joint S-lemma block，因此 source 位移和 target 系数变化之间的 signed cancellation 可以完整保留。特别地，如果 source 与 target 做同一个平移，三个有效误差全部严格为零，原 Lyapunov/S-lemma block 原样保留；真正需要付费的是二者的相对平移 mismatch，而不是绝对位置。

给后续数学 Agent 的建议：若继续推进 local chart，不要把精确 affine chart 变化当成物理 coefficient error。下一条最自然的独立数学任务是把本轮 translation congruence 推广到可逆 `y=Pz+h`，得到 `GL(n)` 下的 fraction-free certificate transport；只有 chart 本身是近似或 nonlinear 时，才应额外引入 Lie/二阶 defect。给 Lean Agent 的建议则只是未来可拆成 recenter identity、augmented congruence、adjugate completion 和 reserve-fraction 四个小 theorem；当前没有要求也没有声称已编译。

严格边界保持不变：实际 P5 same-key source/target、cell/tube/trajectory、FD halo、Float64/interval、Lean/kernel、封不觉独立验证、admission 与 registry 均未闭合。正式数学推导见 `review-T-P5-246-JOINT-ANISOTROPIC-SOURCE-TARGET-SLEMMA-honglianmozun-20260910T1251Z.md`。