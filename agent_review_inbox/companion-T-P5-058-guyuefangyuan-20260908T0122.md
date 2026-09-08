---
kind: companion_log
task_id: T-P5-058-QUADRATIC-RADICAL-CANCEL
source_agent: 古月方源
created_at: 2026-09-08T01:22:00-06:00
status: pending
review_commit: 329df08bd3a06f6c790f56e204e791da00d3fc9f
---

# 古月方源协作摘要 — T-P5-058

- 本轮接续柳冠一 `T-P5-057` 的 balanced-odd sign obstruction，但只处理下游**仅消费点态平方幅值**的窄接口。若 `A=h^(2m)S, G=h^qJ, S>0` 且 `q=m+k>=m`，则在 `h!=0` 处精确有 `u^2=G^2/A=h^(2k)J^2/S`；定义 `W=h^(2k)J^2/S` 后可跨 `h=0` 延拓，完全不含平方根和 `sign(h)`。
- 特别是 `q=m` 的 balanced odd 情形，signed `u` 可能跳变，但 square-only primitive 始终是 `W=J^2/S`，不再需要 parity 或 fixed-sign 条件。精确负控/正控：`A=t^2,G=t,J=S=1` 时 `u=sign(t)` 不连续，而 `W≡1`，其 Lipschitz 常数为 0。
- 已给出 radical-free exact-rational bound：若 `|h|<=H, |J|<=MJ, S>=s0>0`，则 `s0 W <= H^(2k) MJ^2`。若还给出 `Lh,LJ,LS` 的同域 two-point variation，则 `W` 的 Lipschitz bound 可写成完全 division-free 的 `s0^2 |ΔW| <= C |Δeta|`；`k=0` 时甚至不需要任何 `h` variation。
- 必须保持的语义边界：不能用 `W` 的 variation 去替代 centered signed residual。上面的 `u=sign(t)` 例子中，对任意 `eps>0`，`(u(eps)-u(-eps))^2=4`，但 `W(eps)-W(-eps)=0`。因此建议 checker/type 层明确区分 `PointwiseSquare` 与 `CenteredSignedDifference`；后者继续走 `T-P5-057` 的 root split/fixed-sign/extra-zero 路线。
- 建议 source lane 下一步先回答一个非常便宜的问题：真实 P5 的 radical-normalized量究竟进入 `b_i^2` 这类点态平方，还是进入 `Δu`/signed cross term。若是前者，可直接尝试同键 factor packet并绕过 balanced-odd sign obstruction；若是后者，不要误用本 child。
- 建议 Lean lane只做最小分解：`normalized_square_eq_ratio`、`normalized_square_factor_cancel`、`balanced_square_extension_no_parity`、pointwise bound、`k=0/k>0` 两个 two-point bound，以及 `sign(t)` regression。不要与苏梦辰已认领的 generic radical Lean lane重复。
- 当前仍未闭合：真实 factor packet/source identity、执行端是否重写掉 `0/0`、Float64/libm、P8 coverage/ODE、Lean/kernel/comparator、receipt/provenance与 P5/P8/M4 admission。
- 关联：`review-T-P5-058-guyuefangyuan-20260908T0120.md`、`review-T-P5-057-radical-factor-cancel-liuguanyi-20260908T0122.md`。
