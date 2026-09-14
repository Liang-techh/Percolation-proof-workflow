---
kind: companion_log
task_id: T-P5-234-RANK-DEFICIENT-EQUALITY-QUOTIENT-DUAL
source_agent: 红莲魔尊
created_at: 2026-09-10T09:52:00Z
inspected_commit: 91817309af5e6b1ef68128914ba0ac96e7ee6b34
review_commit: 69e1214a25f1e14137fb606bb6025b33ae187dd3
status: mathematical_handoff
admission_label: pending
---

# Companion handoff — T-P5-234

本轮接上 T-P5-233 的秩亏 equality seam，得到两个可直接给下游数学 consumer 使用的结果。

第一，不能把 dependent equality rows 直接删掉。若 `C0` 是 `C` 的一个最大独立行基，必须同时保留一个 compatibility matrix `E_hat`，使

`Cv=Bz <-> (C0v=B0z and E_hat z=0)`。

这样 T-P5-233 的 conditional curvature 在 `Z=ker(E_hat)` 上仍是精确的。不同独立行基得到的 ambient curvature matrix 可能不同，但在真实可行子空间 `Z` 上对应的 bilinear form 完全一致；只有当 `range(B) subseteq range(C)`、即所有 `z` 都兼容时，两个 ambient matrices 才应要求全局相同。

第二，若最终只需要第二次 Schur/Lyapunov scalar closure，其实可以完全绕开 row-basis。令 `d=det(H)`、`J=adj(H)`、`S_hat=CJC^T`。只要找到有理 `mu,nu` 满足

`B^T mu=b`,

`S_hat mu=B nu`,

则 unrestricted exact equality manifold 上

`sup [a t^2+2t b^Tz-v^THv] = t^2[a+(mu^T S_hat mu)/d]`。

因此 trusted fraction-free gate 只需检查

`d a + mu^T S_hat mu <= 0`。

这个 packet 对 `rank(C)` 没有任何要求，也不需要 inverse、sqrt、pseudoinverse 或 nullspace eigenvector；而且 rational 数据在 supremum 有限时一定存在 rational `(mu,nu)` KKT packet。

必须保留的 FAIL 边界：若 `b notin range(B^T)` 且 `z` 在 exact equality manifold 上不另加界，则 `ker(B)` 给出 genuine unbounded positive ray；若真实 source 对该 flat coordinate 另有有界/缩放约束，则应回 T-P5-229/231 的 support/exponent 分支，不能直接报物理 FAIL。

一个重要 regression 是 `C=(1,2)^T, B=(1,0)^T`。原系统强制 `v=z=0`。选第一行做 basis 会得到非零 ambient curvature，选第二行会得到零 ambient curvature；二者只有在 compatibility 子空间 `Z={0}` 上才相同。这个例子应保留，防止后续 checker 错把“删 dependent rows”当作等价变换。

建议下一条数学 seam：处理 **exact equality + bounded ellipsoid fiber**，把本轮 rank-free equality multiplier 与 T-P5-230 的 trust-region/S-lemma multiplier合并成一个不显式构造 nullspace basis 的 block/KKT packet；重点判断 equality multiplier 与 trust-region multiplier 何时可以无损交换。