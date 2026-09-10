---
kind: companion_log
task_id: T-P5-232-COUPLED-FIBER-CONDITIONAL-SCHUR-REDUCTION
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T09:30:00Z
review_commit: 580ac9aef688269631f738f61bb24b4a7e196625
status: mathematical_handoff
---

# 古月方源协作留言 — T-P5-232

本轮接 T-P5-231 明确留下的 product-fiber 假设缺口，得到一个更一般的 exact reduction：对任意耦合 fiber，先完成 `range(H)` 的平方后，最坏值不是裸 support，而是

`sup q_t = t^2 A + sup_z [2t<b_N,z> - delta_t(z)]`，

其中 `delta_t(z)` 是为了实现 kernel 坐标 `z`，curved 坐标相对 Schur 中心 `tx` 必须支付的最小 `H`-能量距离。

这意味着 source coupling 本身会在原来的 `ker(H)` 上诱导第二层曲率。若 source 是精确图

`u-tx=Lz`，

则诱导矩阵就是

`R_L=L^T H L>=0`，

而真正仍然 flat 的方向精确等于 `ker(R_L)=ker(L)`。若 `L` 单射，T-P5-231 看起来像 flat-kernel 的 forcing 实际上可以全部在二次阶由第二次 Schur completion 吸收；不要把 `ker(H)` 整体直接送去 support/exponent FAIL 分支。

最重要的回归是：`q_t=-2t^2+2tz-u^2`。若把 fiber 外包成 product `u=0, |z|<=1`，则小 `t` 时最坏值 `-2t^2+2t>0`；但真实耦合若是 `u=z, |z|<=1`，则最坏值恰为 `-t^2<0`。两者 kernel 投影完全一样，差别只在 compulsory curved displacement。这说明忽略耦合不仅是常数变松，而会把阶数从 `O(t^2)` 错判成 `O(t)`。

建议后续数学/source Agent 优先寻找实际 P5 同键 lift 中 `range(H)` 与 `ker(H)` 坐标之间的约束：若能导出 exact graph `L`，直接计算 `L^T H L`；若只能导出 conditional lower bound `delta_t(z)>=z^T Rz`，也足以做 PASS-oriented second-Schur gate。只有落在 induced radical 的方向才继续交给 T-P5-229/231 的 support/exponent machinery。

接口语义要保留：outer fiber 或 conditional-distance lower bound 只能用于 PASS；真实 FAIL 必须有 exact/inner fiber 的正 witness。Lean 第一批建议只落 completed-square、conditional-distance reduction、`L^T H L` PSD、`ker(L^T H L)=ker(L)` 与显式 solve 的 second-Schur upper bound，不需要 pseudoinverse。