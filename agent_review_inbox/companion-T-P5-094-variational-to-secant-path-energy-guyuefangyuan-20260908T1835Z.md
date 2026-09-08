---
kind: companion_log
task_id: T-P5-094-VARIATIONAL-TO-SECANT-PATH-ENERGY
review_id: review-T-P5-094-variational-to-secant-path-energy-guyuefangyuan-20260908T1832Z
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-08T18:35:00Z
status: math_handoff
---

# T-P5-094 中文协作接力

本轮补上 T-P5-090/T-P5-091 明确留下的“variational contraction 如何升级成 finite-separation/secant contraction”缺口，且没有碰 T-P5-092 sampled impulse、T-P5-093 base-flow Lie defect 或其 Lean lane。

最值得梁智炜/苏梦辰后续直接收割的数学接口有三层：

1. **无需 exp 的 exact-rational 有限时域衰减。** 若 `Vdot <= -2 mu V`、`V>=0`，则任意一步都有 `(1+2 mu Δt)V(t+Δt)<=V(t)`。把 `[0,h]` 等分 `N` 份后清分母得到
   ` (N+2 mu h)^N V(h) <= N^N V(0) `。
   因此 checker 可以只验有理加乘、自然数幂和序比较；`N` 越大越接近标准 `exp(-2 mu h)`，但 trusted 层不需要计算指数函数。

2. **固定 metric 的真正 secant theorem。** 若 straight segment 全部在证书域内，且沿段有
   `A Q_W(DPsi(z)v) <= B Q_W(v)`，其中 `W` 固定 PSD，则由 FTC + quadratic integral Jensen 精确推出
   `A Q_W(Psi(x)-Psi(y)) <= B Q_W(x-y)`。
   这可以作为非常小的 Lean leaf，直接把 differential/Jacobian certificate 变成两点 finite separation certificate。

3. **state-dependent metric 时必须改用 path energy。** 定义
   `E_W(gamma)=∫ gamma'(s)^T W(gamma(s)) gamma'(s) ds`。
   点态 tangent certificate 直接积分成 `A E_out(Psi∘gamma)<=B E_in(gamma)`，再对 connecting paths 取 infimum 得到 finite-separation contraction。T-P5-090 的 moving chart 下，`M=J^T W J` 会让 path energy 精确保持：`E_M(zeta)=E_W(T∘zeta)`，因此没有 Jacobian condition-number 损失。

有一个应当进入 regression 的 exact obstruction：物理空间取 `W=1`、`Phi(x)=x/2`，非线性 chart 取 `T(z)=1/z`。则 normalized map 是 `Psi(z)=2z`，raw Euclidean chord squared 反而扩大 4 倍；但 pullback metric `M(z)=1/z^4` 下 tangent/path energy 仍精确缩小到 `1/4`。所以不能把 moving-metric contraction 偷换成任意 nonlinear normalized coordinates 中的 Euclidean chord contraction。

协作建议：苏梦辰若要形式化，第一版优先做 `rational_decay_one_step_of_deriv_le`、`rational_decay_equal_partition_pow`、`quadratic_integral_jensen_psd`、`jacobian_bound_implies_secant_bound_const_metric`。Riemannian/geodesic infimum API 可以后置；当前最有价值的是先把固定 metric 的 secant bridge 与 division-free `N`-slice factor 做成可复用 leaf。

source/coverage 侧需要注意：真正 moving-metric finite separation 不只要求两条 endpoint trajectory 在 tube 内，而要求**整张 flowed connecting-path sheet**都在 T-P5-090 contraction-certified tube 内。若只冻结 endpoints，不能自动宣称 pairwise contraction。

共享 `collaboration_board.md` 当前连接器没有原子 append 动作，只有整文件 replacement；为避免覆盖其他并行 Agent 留言，本轮未冒险重写留言板。请梁智炜在安全 harvest 时把以上协作建议追加到留言板末尾。
