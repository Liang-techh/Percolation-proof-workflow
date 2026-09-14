---
kind: companion_log
task_id: T-P5-122-CURL-METRIC-PULLBACK-CLOSURE
review_id: review-T-P5-122-curl-metric-pullback-closure-kuangmanmozun-20260909T0342Z
source_agent: 狂蛮魔尊
created_at: 2026-09-09T03:46:00Z
review_commit: 1ad2545fbe4175bed3808d77c49b533cded84b88
status: handoff
---

# 狂蛮魔尊中文接力 — T-P5-122

本轮接 T-P5-120/T-P5-121 的最小未闭合不等式：物理 curl/skew-action 已有 `S_z=J^T S_x J`，但此前没有把物理 tangent metric、physical force/covector metric 与 normalized tangent/covector metric 的 quantitative transport 压成可信的 root-free gate。

核心结论有两层。

第一层是最强的 direct gate。若 source 能把同一点的 `J` 与 `S_x=Dr-Dr^T` 一起形成 signed pulled matrix `S_z=J^T S_x J`，则直接证明

`K_z P_Z - S_z^T R_G S_z >= 0`（PSD）

即可得到 `Q_G(S_z eta)<=K_z Q_Z(eta)`。这条路线不需要 Jacobian inverse、平方根或谱范数，而且先保留了 `J^T S_x J` 内部的 orientation cancellation。

第二层是 source 只能给独立 metric envelope 时的 factored gate。若

`K P_X-S_x^T R_F S_x >=0`，

`mu_X P_Z-J^T P_X J >=0`，

`mu_F R_F-J R_G J^T >=0`，

则纯 PSD congruence 推出

`Q_G(J^T S_x J eta) <= mu_F*mu_X*K*Q_Z(eta)`。

这里两个 chart factor 都是真的：一个来自 tangent input `J eta`，另一个来自 covector pullback `J^T f`。二维 `J=sI`、Euclidean metric、constant skew `S_x` 上正好达到 `mu_F*mu_X*K=s^4 K`，因此只掌握三条独立 envelope 时不能普遍少付一个 factor。

但 factored gate 可能极松。二维取 `S_x=[[0,-1],[1,0]]`、`J=diag(M,1/M)`，两个独立 Euclidean transport factor 都是 `M^2`，factored budget 为 `M^4`；而因为 `det J=1`，精确有 `J^T S_x J=S_x`，direct constant 仍是 `1`。所以 factored gate FAIL 只能标 `NOT_CERTIFIED_BY_FACTORED_METRIC_TRANSPORT`，不能判真实 pulled curl FAIL；应优先回 direct PSD lane。

本轮还区分了 pointwise curl-action 与 T-P5-121 已经积分完成的 radial remainder。若物理 remainder 已满足

`4 Q_F(n_x)<=K Q_X(T(z)-q0)`，

则 normalized covector `n_z=J^T n_x` 只先支付 covector factor：

`4 Q_G(n_z)<=mu_F K Q_X(T(z)-q0)`。

只有当 consumer 还要把有限 physical displacement 换成 `z-z0` 时，才需要另付 **secant** factor `mu_sec`。若同一 normalized 直线段上 uniform 有 `Q_X(J(z_s)eta)<=mu_X Q_Z(eta)`，quadratic Jensen 可证明 `mu_sec=mu_X`；只有 endpoint Jacobian 不够。

精确反例：`T_N(z)=z+N(2z-z^2)` 在 `[0,1]` 上严格单调，且 `T_N'(1)=1`，但 `T_N(1)-T_N(0)=1+N`。所以 endpoint tangent cap 可以固定为 1，而 finite-displacement ratio 可任意大；radial remainder 的 normalized displacement 替换必须有 whole-segment/secant coverage。

接入 T-P5-121 的 small-gain 后，如果 reshaped storage 直接控制 physical displacement `m_X Q_X(T(z)-q0)<=V`，只需检查

`mu_F K <= 16 m_X alpha delta_d`

即可给 generalized residual power 收费；如果 storage 只控制 normalized displacement，则 gate 变成

`mu_F K mu_sec <= 16 m_Z alpha delta_d`。

因此不要在已经有 physical displacement comparator 时无条件再乘 `mu_X`，那会重复收费。

moving chart 还有一个硬边界：总 residual work 是

`n_x^T(T_t+Ju)=n_z^T u+n_x^T T_t`。

只证明 generalized part 的 small-gain 不能覆盖 frame-power；取 `u=0,T_t=n_x` 就得到 generalized power 为 0、真实 physical work 为 `||n_x||^2>0`。后续 source lane 要么直接在 physical velocity 变量中闭合，要么显式保留 `n_x^T T_t` packet。

建议 Lean/typed sidecar 最先形式化两个纯矩阵叶：`curl_action_pullback_direct` 与 `curl_action_pullback_factored`；其次是 `uniform_tangent_transport_implies_secant`。真正 source/CSE lane 应优先输出 signed `J^T S_x J` 再 enclosure，不要先把 `J` 与 `S_x` 各自压成 operator norm。

当前仍为 `pending / CONDITIONAL_PASS`；没有升级实际 `Dr/J/metric` source、segment coverage、moving-frame budget、Float64/FD/controller、P8、Lean/kernel、registry 或 P5/M4 closure。

共享 `collaboration_board.md` 本轮已读取。当前 GitHub connector 对该共享文件只提供整文件 replacement，不提供原子 append；为避免并发覆盖其他 Agent 的新增留言，本轮没有重写该共享文件，协作建议完整保存在本 immutable companion，供梁智炜收割。
