---
kind: companion_log
task_id: T-P5-121-APPROXIMATE-CONSERVATIVE-CURL-DEFECT
review_id: review-T-P5-121-approximate-conservative-curl-defect-guyuefangyuan-20260909T0332Z
source_agent: 古月方源
created_at: 2026-09-09T03:37:00Z
review_commit: a47987998ab1760fc4e3f626ab13fb9c58194682
status: handoff_with_metadata_correction
---

# 古月方源中文接力 — T-P5-121

本轮补的是 T-P5-119/T-P5-120 之后的“近似保守”缺口，不重复 exact conservative / moving-chart work-form identity。

核心数学结果：在同一个以 `q0` 为星形中心的物理 configuration cell 上，对 `C^1` force field `r(q)` 定义 radial potential

`Psi(q)=∫_0^1 <r(q0+s(q-q0)),q-q0> ds`。

无需假设 Jacobian 完全对称，就有精确分解

`n := r-grad Psi = ∫_0^1 s(Dr-Dr^T)(q0+s x) x ds`，其中 `x=q-q0`。

若同 cell 上有统一 skew-action cap

`Q_F((Dr-Dr^T)delta) <= K_curl Q_X(delta)`，

则由带权 quadratic Jensen 得到 sharp 的

`4 Q_F(n) <= K_curl Q_X(x)`。

`1/4` 常数在 constant skew affine field 上取等，不能只靠 uniform skew-action 信息继续改进。

若 reshaped storage 还有 `m Q_X(x)<=V`，power pairing 满足 `<v,n>^2<=Q_V(v)Q_F(n)`，并且 nominal ledger 留有 `-cV-dQ_V(v)`，那么选有理 `alpha,theta` 后，checker 只需验证

`K_curl <= 16 m alpha theta d`

就能推出

`<v,n> <= alpha V + theta d Q_V(v)`，

从而

`Vdot <= -(c-alpha)V -(1-theta)dQ_V(v)+p_other`。

这条 gate 完全不需要 sqrt / inverse / eigenvalue；并且非零 curl 在 storage 控制 displacement 时可以作为 relative loss 支付，不必自动产生 additive floor。

另一个值得下游保留的结构恒等式是 covector curl 的 nonlinear-chart pullback。若 `q=J^T(r o T)` 且 `D_z q=H_chart+J^T A J`、`H_chart^T=H_chart`，那么

`D_z q-D_z q^T = J^T(A-A^T)J`。

因此 nonlinear chart Hessian 不会制造假 curl；但 quantitative norm bound 仍可能需要 metric/J comparator。moving chart 下 residual 的 frame-power `n^T Tt` 也必须和 `(J^T n)^T zdot` 一起形成总 work 后再 enclosure。

硬 obstruction：只知道 anchor 点 `Dr(q0)` 对称完全不够。例 `r_N(x,y)=(0,Nx^2)` 在原点 Jacobian 为零，但从 `(0,0)` 到 `(1,0)` 的 radial remainder 是 `(0,2N/3)`，可任意大。所以必须证明 whole-ray/whole-cell skew cap；不能用单点 Hessian/symmetry sample 冒充。

建议 source/CSE lane 的最小 packet 是：同键 `r,Dr,q0`、star-segment coverage、`K_curl` 或直接 weighted integral cap、radial `Psi` evaluator、reshaped-storage coercivity/comparator `m`、paired power metric、nominal `(c,d)`。若 source 已有 exact potential，则直接走 `K_curl=0` 的 T-P5-119 branch，不要重复收费。

建议 Lean 先做纯标量叶 `curl_defect_power_absorption`：从 `4mQn<=KV`、`p^2<=QvQn`、`K<=16m alpha theta d` 推 `p<=alpha V+theta d Qv`；其次做纯矩阵 `covector_curl_pullback_algebra`。radial integral/gradient 的 calculus API 可后置。

## 元数据纠正

正式 review `a47987998ab1760fc4e3f626ab13fb9c58194682` 的 YAML 中，T-P5-119 upstream commit 被手误写错，且紧随其后的 prose note 也含一个错误猜测值。两者均不得作为 provenance 使用。

T-P5-119 的权威 review commit 经 GitHub commit object 重新读取确认为：

`31f9508aab519f8af557803999942934063c5eb1`

对应文件：

`agent_review_inbox/review-T-P5-119-conservative-bias-power-storage-shaping-honglianmozun-20260909T0257Z.md`

T-P5-120 的 upstream commit `282c801638022fcb40220e1f92f44f3ec0a3993d` 保持正确。由于 inbox 证据按 immutable/add-only 处理，本轮不重写已提交 review，而在本 companion 中显式纠正。

## 协作建议

给其他数学 Agent：若继续这条路线，优先寻找 actual force residual 的 whole-cell antisymmetric Jacobian action bound，不要从少量采样点“近似对称”推 exact conservativity；若实际 `K_curl` 很小，应先尝试本轮 relative small-gain gate，再退回 T-P5-118 的 additive-floor branch。

共享 `collaboration_board.md` 当前连接器仍只提供整文件 replacement，没有安全原子 append；为避免覆盖并行 Agent 留言，本轮没有冒险重写该共享文件，以上中文协作建议作为 immutable companion 交给梁智炜安全 harvest。
