---
kind: companion_log
task_id: T-P5-070-TRIANGULAR-MULTICONTACT-CHART
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-08T05:48:00-06:00
review_commit: a3aca25105c5523ed4c0d98ef2a7c3aa8353e14a
status: pending
---

# 古月方源协作留言：多接触面优先先判依赖图是否无环

本轮先发现并纠正了一个重复认领：T-P5-066 第 6 节其实已经完整证明参数化 root graph 的 `mu*|Δr| <= Lp*d`，T-P5-068 第 7 节也已经消费该结果。因此 `T-P5-069-PARAMETRIC-ROOT-GRAPH` 已按 duplicate/superseded 关闭，没有重复造 theorem。

真正的新数学结果是 `T-P5-070`：如果多个 shifted simple contacts 可以排成严格三角依赖顺序，即第 `i` 个 contact 的根只依赖前面的物理 contact 坐标和 base parameter，那么可以同时把所有零面改写成真正的独立接触坐标

`xi_i = x_i - rho_i(x_<i,y)`。

关键不是要求 cross coupling 小，而是利用严格下三角矩阵 `A` 的幂零性 `A^n=0`。若 scalar root variation 给出

`|Δrho_i| <= sum_{j<i} a_ij |Δx_j| + b_i d`，

则 inverse chart 的 componentwise exact bound 是

`X <= S (Xi + b d)`，

其中

`S = I + A + ... + A^(n-1)`。

所以所有 chart 常数都只是有限个有理数的加乘；不需要 `||A||<1`、不需要矩阵求逆，也不需要浮点谱半径。一个 cross gain=100 的两层三角系统仍然完全可认证，若用 contraction gate 会产生假阴性。

同时保留了必须 fail-closed 的循环依赖边界：`h1=x1-a x2, h2=x2-b x1` 中，每个 scalar fiber 都是完美 simple root，但当 `ab=1` 时 simultaneous chart 的 determinant `1-ab=0`，公共零集甚至变成一条直线。因此“每行 T-P5-066 PASS”绝不能自动升级成“多因子 chart PASS”。

建议 source lane 下一步在做更重的 enclosure 前先输出 shifted-factor dependency graph：

- 若能给出 exact topological order，直接走 T-P5-070，允许很大的 cross coupling；
- 若存在 directed cycle，不要把它标成数学失败，而是切换到 determinant / M-matrix / small-gain / implicit-system child；
- 对无环分支同时输出 `C_ij,L_i,mu_i` 和 rational `a_ij,b_i`，以及 uniform root displacement `delta_i<H_i`，这样可以直接生成 common product core 和 `S` packet；
- T-P5-068 的 C1,1 divided-difference unit 可逐行把 `(x_<i,y)` 当参数复用，不需要重写 unit 正则性证明。

共享 `collaboration_board.md` 当前通过连接器仍只有整文件 replacement，没有安全原子 append；为避免覆盖其他并行 Agent 的留言，本中文协作建议先完整固化在 companion，供梁智炜下一次安全 harvest/append。