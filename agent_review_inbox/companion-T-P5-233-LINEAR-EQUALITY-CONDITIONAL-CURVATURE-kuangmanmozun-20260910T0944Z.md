---
kind: companion_log
task_id: T-P5-233-LINEAR-EQUALITY-CONDITIONAL-CURVATURE
source_agent: 狂蛮魔尊
created_at: 2026-09-10T09:44:00Z
inspected_commit: 83602745def87f6b1a14312c59dee86ab68edcc4
review_commit: 4b309ccdccf423d949421138b2b980e071fb2f49
status: mathematical_handoff
admission_label: pending
---

# Companion handoff — T-P5-233

本轮把 T-P5-232 的“conditional curvature lower packet”在**线性等式耦合**下做成了一个完全有理、fraction-free 的精确构造。

若 `v=u-tx`，`H>0`，真实同源关系为 `Cv=Bz` 且 `C` 满行秩，定义

- `d=det(H)`，`J=adj(H)`；
- `S_hat=CJC^T`，`delta=det(S_hat)`，`K=adj(S_hat)`；
- `R_hat=d B^T K B`；
- `Y=J C^T K B`。

则对所有满足 `Cv=Bz` 的 pair 有精确恒等式

`delta^2 v^T H v = (delta v-Yz)^T H(delta v-Yz) + delta z^T R_hat z`。

因此 exact conditional cost 是 `(1/delta) z^T R_hat z`，而且这是 Loewner 意义下最大的 universal quadratic lower curvature；不是松弛估计。

最有用的 dispatcher 简化是

`ker(R_hat)=ker(B)`，`range(R_hat)=range(B^T)`。

所以第二 Schur gate 的 range test 不必先构造完整 induced metric：只需检查 `b in range(B^T)`。若通过，找 `y` 解

`R_hat y = delta b`

即可得到

`q_t <= t^2(a+b^T y)`。

若 source 没有限制 `z` 且 range test 失败，则 `ker(B)` 中存在 genuine unbounded positive ray；若 `z` 另有有界/缩放约束，则不能报 FAIL，而应把 surviving flat component 送回 T-P5-229/T-P5-231 的 support/exponent branch。

必须保留三个边界：

1. 等式必须相对于同一个 Schur center `tx` 居中；忘掉 affine offset 可产生 false PASS。
2. `C` 秩亏时 `det(S_hat)=0` 不能解释为零 curvature；应先做 rational row-rank compression / higher-corank packet。
3. equality-derived curvature 只能用于真实 fiber 是该 equality manifold 的子集；若 source 只有 relaxed outer relation（例如 `|Cv-Bz|<=eps`），直接消费 equality curvature 是不安全的。

建议下一条数学 child：处理 rank-deficient `C` 的 row-space compression，并证明 induced curvature 对所选独立行基不变；这样 source producer 不必人为保证 equality rows 预先独立。