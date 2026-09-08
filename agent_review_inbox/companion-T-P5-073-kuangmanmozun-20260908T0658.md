---
kind: companion_log
task_id: T-P5-073-AFFINE-OFFSET-RELATIVE-DECAY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
status: pending_mathematical_child
review_commit: 18618ab0213677d83867b347a3b3acd7c9857b98
---

# 狂蛮魔尊协作留言 — T-P5-073

本轮补的是当前 `componentwise_relative_decay` 里“加性 force/FD offset 到底能不能被相对衰减吸收”的数学逻辑，不涉及 provenance/admission。

最关键的结构结论：如果 cell 包含 `v_i=0`，那么任何纯相对界

`|R_i(v)| <= kappa_i |v_i|`

都会强制整个横向切片 `R_i(0,v_{-i})` 恒等于零，而不只是中心 `R_i(0)=0`。所以一旦 source 能给出某个 `v_i=0` 的非零 residual witness，纯 componentwise-relative 路线就是数学上不可能，不应继续调常数；应改走 bias-aware box。

如果 source 能 exact 化成

`R_i=b_i(v_{-i})+v_i Q_i(v)`，

则零切片就是 `b_i`。多项式情形 `b_i≡0` 等价于 exact coordinate factor `v_i | R_i`；随后只需 bound `Q_i`。光知道 `R_i(0)=0` 不够，例如 `R_1(v1,v2)=v2` 会立刻击穿 componentwise relative bound。

若 cell 与零切片有 certified gap `|v_i|>=delta_i>0`，且只有 envelope

`|R_i|<=beta_i+kappa_i|v_i|`，

则 offset 可以被吸收，当且仅当 envelope-level strict gate

`beta_i < (1-kappa_i) delta_i`

通过；这是 sharp threshold，而且是 division-free。等号只能得到 ratio=1 的 boundary，不能升级 strict decay。

若 cell 包含零且 bias 真实存在，正确 bootstrap 是 box gate：

`beta_i + sum_j A_ij r_j < r_i`。

reserve 为 `r_i-beta_i-sum_j A_ij r_j`。在只掌握 unsigned envelope 的意义下，这个 gate 对“所有满足该 envelope 的 residual map 都严格映入 box 内部”是必要且充分的；实际 affine map 在对称 box 上的 exact sup 也是 `|b_i|+sum_j|a_ij|r_j`。

给梁智炜/source lane 的建议路由：

- cell 穿过 `v_i=0`：优先给 exact zero-slice identity 或非零 slice witness；
- zero-slice identity PASS 后，再给 quotient/`partial_i` bound；
- cell 有 gap：给 rational `beta,kappa,delta`，直接走 offset-absorption gate；
- 确有 bias 且 cell 含零：不要硬追 pure relative，改给 `beta,A,r` 做 box closure。

注意：一个粗上界 `beta>0` 本身不能证明真实 residual 非零，所以 envelope gate 失败时只能说“此 bound 无法认证”；只有 exact nonzero slice witness 才能说 pure-relative 数学上不可能。

当前仅为数学 child，未升级 concrete forceError/FD source、Float64/controller、P8 coverage、Lean/kernel、P5/M4 或 registry。