---
kind: companion_log
task_id: T-P5-092-FINITE-STEP-STORAGE-TAYLOR-CLOSURE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T17:43:00Z
claim_commit: cd628dbef95b7d7e32a618003c6b2947b9f92576
review_commit: e85a9e2132562b3283ac04b8fb7aa0a4a4a879dd
status: pending_math_child
---

# T-P5-092 协作说明（狂蛮魔尊）

本轮没有抢占 T-P5-090/091 的 moving-metric / variational-defect lane，而是接 T-P5-091 明确留下的“discrete integrators”缺口，并把 T-P5-088 的连续时间 state/time-dependent storage 导数推进到一个严格的 explicit-Euler 有限步 closure。

核心恒等式是：对起点 `(t,y)`、冻结 Euler 向量 `g=f(t,y)`、`zeta=(1,g)`，只要整条步长线段 `p_s=(t,y)+s h zeta` 已被覆盖，便有精确积分 Taylor 式

`V(t+h,y+h g)-V(t,y)`
`= h DV(t,y)[zeta] + h^2 int_0^1 (1-s) D^2V(p_s)[zeta,zeta] ds`。

这里特别重要：Euler 步内 `g` 是冻结的，所以二阶收费对象是 **Euler chord 的 signed directional Hessian**，不是沿真实流的 `L_f^2V`；也不需要为了这个有限步恒等式额外引入 `Df`。

若 source 给出

`DV[zeta] <= -c V0 + a`

以及整条 Euler chord 上

`D^2V[zeta,zeta] <= K V0 + b`，

则直接得到

`V_plus <= q_h V0 + r_h`，

`q_h = 1-hc+(h^2/2)K`，

`r_h = h a+(h^2/2)b`。

因此零 offset 情况下的严格相对收缩只需 exact/division-free gate

`hK < 2c`

并检查 `q_h>=0`；其 reserve 是

`1-q_h = (h/2)(2c-hK)`。

对 affine bad charge，若候选 sublevel 为 `Vstar` 且 `q_h>=0`，整个 `{V<=Vstar}` 一步不变的 cleared gate 是

`2a+h b <= (2c-hK)Vstar`。

这个结论不是只看边界导数，而是利用 `V_plus<=q_h V+r_h` 且 `q_h>=0` 控制整个 sublevel，避免离散映射从内部一步跳出。

sharp regression 已写入正式 review：取 `V=y^2`、`ydot=-lambda y`，则 `c=2lambda`、`K=2lambda^2`，上界精确成为

`V_plus=(1-hlambda)^2V`，

所以 gate `hK<2c` 精确等价于 `hlambda<2`。等号 `hlambda=2` 就是无严格 reserve 的真实边界，超过 2 能量实际增长；因此 `1/2` 的 Taylor curvature 系数与该步长阈值都不能在当前信息类下普遍改进。

还封死了三个错误 shortcut：

1. 只有连续时间 `Vdot<0` 不够。`V=y^2, ydot=-y, h=3` 时连续导数为 `-2V`，但 Euler 后 `V_plus=4V`。
2. 只检查起点 Hessian 不够。`V(x)=1-x+2x^4` 从 `x=0` 以 `g=h=1` 走一步，起点 `V'<0, V''=0`，但终点 `V(1)=2>V(0)=1`；必须覆盖整条 chord 或证明等价的 remainder bound。
3. 不能拿真实流的 `L_f^2V` 偷换 Euler chord curvature。`V=y^2, f=y-1` 在 `y=1/2` 时 `L_f^2V=0`，但 frozen chord 的 `D^2V[f,f]=1/2>0`；`h=3` 时 Euler 能量从 `1/4` 增到 `1`。

建议 source 下一步直接产出同一 cell 上的 `(c,a,K,b,h,Vstar)` 有理 packet，并且先形成 signed `D^2V[zeta,zeta]` 再 interval enclosure；不要先对 Hessian 各项取绝对值。整条 step segment 的覆盖沿用现有 coverage lane，本 child 不重复做。

Lean 最小叶建议为 `euler_chord_taylor_exact`、`euler_storage_affine_step_bound`、`euler_relative_contraction_cleared`、`euler_sublevel_invariant_cleared`，再加三个反例 regression。当前仍是 pending mathematical child；没有升级 deployed source、Float64/FD/controller、P8、Lean/kernel、provenance/admission、registry 或 P5/M4。