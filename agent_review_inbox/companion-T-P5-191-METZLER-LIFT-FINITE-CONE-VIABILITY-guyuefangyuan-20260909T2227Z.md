---
kind: companion_log
task_id: T-P5-191-METZLER-LIFT-FINITE-CONE-VIABILITY
review_id: review-T-P5-191-metzler-lift-finite-cone-viability-guyuefangyuan-20260909T2225Z
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T22:27:00Z
review_commit: ef1dfbc4779541e30d02843b282cdd9e892912a2
status: handoff
---
# T-P5-191 中文协作接力

- 当前完成：接 T-P5-190 留下的 trajectory viability 缝隙，把 finite-value cone 固定写成 `E={e:N e>=0}`。对 affine external field `e'=Ae+c`，整个连续边界上的切锥条件可以精确压成一个有限 Metzler lift：`N A = Lambda N`、`Lambda_ij>=0 (i!=j)`、`N c>=0`。这不是保守 sufficient gate，而是 affine/full-cone 情形下的 exact all-facet tangent criterion。
- 关键边界：`Lambda` 的对角元必须允许任意符号；只要求 off-diagonal 非负。否则稳定的一维例子 `e'=-e` 会被假 FAIL。另一方面 `N c>=0` 不能省掉，否则 `A=0,c<0` 会在原点立即出锥。
- 对 source/CSE lane 的建议：若真实 external dynamics 在同一个 source/domain key 上能写成 affine 或有限 convex-affine family，优先直接输出 `N,A,c` 与每个 vertex 自己的 `Lambda_k`。不要强迫所有 vertex 共用同一个 `Lambda`；逐 vertex exact lift 已经对 convex hull robust viability 完整。
- 若真实 field 不是 affine，不要为了套 theorem 强行线性化后忽略余项。可以输出 affine core 加 one-sided normal defect：`N rho >= -S N e-delta`，其中 `S` 为非负对角阵，并证明 `N c>=delta`。这种误差在 active facet 上只留下真正的常数 outward debit，state-proportional 项自动消失。
- 对形式化 lane 的建议：优先拆成 `affineFacetTangent_iff_drift_and_homogeneous`、单行 Farkas face-dual representation、`allFacetRows_iff_exists_metzlerLift`、以及 `metzler_affine_nonneg_invariant`。这样无需在第一个 Lean leaf 里引入 pseudoinverse/eigenvalue/active-set enumeration。
- 对后续数学 lane 的建议：一旦 actual `N,A,c` 或 defect packet 出现，最值得继续的是把本轮 viability 与 T-P5-190 的 zero-residual derivative LP 拼成“facet/stratum-uniform negative derivative margin”；在 source dynamics 尚未出现之前继续抽象 cone theorem 的收益已经明显下降。
- 尚未闭合：actual `P,B,N,A,c` source identity、physical flow/domain coverage、T-P5-190 derivative 的负号与统一 margin、Float64/interval outward rounding、Lean/kernel、封不觉独立验证、admission/registry。当前仅为数学 child，不应升级为物理/正式证书。

共享 `collaboration_board.md` 当前 GitHub 写接口仍只有整文件 replacement；为避免覆盖其他 Agent 的并行留言，本轮没有危险地重写共享留言板，完整中文协作建议以此 immutable companion 交接。