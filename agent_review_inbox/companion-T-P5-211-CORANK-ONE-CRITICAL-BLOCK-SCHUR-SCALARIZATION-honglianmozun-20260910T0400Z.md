---
kind: companion_log
task_id: T-P5-211-CORANK-ONE-CRITICAL-BLOCK-SCHUR-SCALARIZATION
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T04:00:00Z
claim_commit: b6dd1995fe47805d22414bf0e4ac0cc5364c4853
review_commit: 682b7bd77f7babedc1d0310091ce188a0767d3ba
language: zh-CN
---

# 红莲魔尊协作留言 — T-P5-211

本轮承接 T-P5-210 明确保留的 corank-one critical-block scalarization，没有重复 provenance / receipt / admission / re-audit。

新结论：先用 T-P5-180 对端点 critical block 做 anchor Schur completion。若 active block `A` 与 reduced Schur block `K` 都是 PSD corank one，且两条 kernel ray 都严格落在对应正锥内部，那么整个 `H`-零能量 critical sheet 只有二维：

`v(alpha,beta)=(alpha z-beta X xi, beta xi)`, `beta>=0`。

把 debit `Q=[[P,T^T],[T,U]]` 拉回该 sheet，定义

`g=Tz-X^TPz`,

`G=U+X^TPX-TX-X^TT^T`。

在 T-P5-210 的 common-zero 条件 `z^TPz=0` 下，真正的双临界一阶条件只剩 `beta xi^Tg=0`。若 `J=adj(K)`，则完全无需显式求 `xi`：

`Bcrit=g^TJg=0`

恰好表示 pulled first-order residual 在 reduced kernel 上消失，而

`Ccrit=tr(JG)>0`

恰好表示 surviving zero mode 上存在严格正二阶 debit。因此本分支的 exact endpoint gate 是

**`Bcrit=0` 且 `Ccrit>0`。**

其中 `Bcrit=0` 等价于 bordered determinant `det([[K,g],[g^T,0]])=0`，`Ccrit>0` 等价于 `det(K+sG)` 在 `s=0` 的一阶导数为正。所有量都可保持 rational / division-free；不需要 eigenvector、pseudoinverse、sqrt 或浮点 nullspace tolerance。

我还写入了两个严格 rational regression。第一个例子 active support determinant slope 为零，但经过 Schur active correction 后仍出现 `v^THv=0`、`(Qx*)^Tv=0`、`v^TQv=2`，所以任意正 debit 参数立即产生负能量；第二个例子故意让 `Ccrit>0` 但 `Bcrit>0`，此时双临界条件会把整个 inactive zero ray 排除，证明 `Bcrit=0` 是硬 gate。

后续若真实 source packet 落入本 corridor，建议优先把这两个 scalar gate 接到 T-P5-207 的 error-budget endpoint 上；若 `K` 高余维则不要硬套 adjugate（此时 `adj(K)=0`），直接回到 T-P5-174/T178/T182 的 higher-corank kernel machinery。当前 source binding、global coverage、Float64、Lean、封不觉独立验证与 registry 均未升级。