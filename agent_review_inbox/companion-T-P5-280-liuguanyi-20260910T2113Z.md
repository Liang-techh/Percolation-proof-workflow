---
kind: companion_log
task_id: T-P5-280-CUBIC-FOUR-FUNCTIONAL-DIRECTIONAL-UNCERTAINTY-ADAPTER
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T21:13:00Z
review_commit: db44c62644ef571a900d89abc93342c3fb3e2d06
status: mathematical_handoff
---

# T-P5-280 协作交接 — 柳冠一

本轮承接 T-P5-279 的 source-facing cubic uncertainty seam，已完成数学层而未做 provenance/receipt/admission/re-audit。

核心桥接：固定 `L<R` 后，任意 cubic `d(t)` 可由四个区间适配线性 functional 唯一表示：`d(L), d(R), r_L, r_R`，其中 `r(t)=a3(t+L+R)+a2`。精确恒等式为

`d(t)=C(t)-(t-L)(R-t)r(t)`，

`C(t)=((R-t)d(L)+(t-L)d(R))/(R-L)`。

因此若 source 同一 uncertainty family 上证明 `d(L)>=ell_L`、`d(R)>=ell_R`、`r_L<=k_L`、`r_R<=k_R`，就直接得到 shape-preserving lower support；若下游必须保持 quadratic degree，只需用 `kappa=max(k_L,k_R)` 替换 affine `r(t)`。已证明该 `kappa` 在“只保留四个独立 one-sided marginals”的信息类中 minimax sharp，不能靠重新整理同四个数字继续降低。

四 functional map 的 determinant 为 `(R-L)^2`，所以它不是 heuristic summary，而是 cubic coefficient space 的可逆坐标。每个 functional 都对 `(a0,a1,a2,a3)` 线性，真实 rational polytope/FD packet 可用 exact LP 或 extreme-vertex support 直接产生这四个方向的界，避免先做 symmetric `|Delta a_j|` envelope。

仿射 fiber 变换 `t=alpha u+beta` 下，endpoint value 不变、remainder endpoint 乘 `alpha^2`、barrier 因子 `(t-L)(R-t)` 也乘 `alpha^2`，故整个 support exact covariant；纯 chart re-expression 不应计入 physical coefficient error。

Fail-closed：四方向 box 无法吃进 margin 时只能报 `INCONCLUSIVE_FROM_DIRECTIONAL_SUMMARY`；若真实 projected uncertainty set 有相关性，仍可能由 joint support 通过。`R=L` 需单点特判。actual P5 source key/chart/domain binding、trajectory/state realizability、FD halo、Float64/interval、Lean/kernel、封不觉验证与 admission/registry 均保持 OPEN。

建议下一条数学 seam：对真实 source uncertainty set 在 `(d_L,d_R,r_L,r_R)` 四维 feature space 的**联合投影**做低复杂度 support reduction，识别何种 polytope/zonotope/affine-arithmetic 结构能让 `inf_f w(t)^T f` 保持低次数 piecewise polynomial/rational，从而利用 feature correlation 而不进入 general CAD。