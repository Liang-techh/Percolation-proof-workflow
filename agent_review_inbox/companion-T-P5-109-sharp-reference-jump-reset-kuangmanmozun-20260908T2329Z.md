---
kind: companion_log
task_id: T-P5-109-SHARP-REFERENCE-JUMP-RESET
source_agent: 狂蛮魔尊
created_at: 2026-09-08T23:29:00Z
review_commit: 15972fa1ff297000441e4352f59a5de630db9239
integration_status: pending
admission_label: pending
---

# T-P5-109 协作补充

本轮没有重复 T-P5-108 的 dwell recurrence，而是把 T-P5-107 的 jump inequality 做到 sharp。关键结构是 `e=(a,0)` 与 `c_s=((K+D)a,Ma)` 满足精确关系 `c_s=P e`，其中 `Vc=1/2 x^T P x`。因此 jump observable 的真实 storage-dual 常数是

`A=e^T P e=11275620/75672601`，

从而

`(c_s^T x)^2 <= 2A Vc = (22551240/75672601)Vc`。

旧 packet 的 `63/8` 系数约大 26.425 倍。新界在 `x∈span(e)` 上取等，所以不是再调 Young 参数，而是 full storage ellipsoid 上的 sharp 常数。最小 Lean 证明甚至不需要逆矩阵：令 `A=n/d`，展开非负平方 `(n x-d(c_s^T x)e)^T P(n x-d(c_s^T x)e)` 即可得到 `d(c_s^T x)^2<=n x^TPx`。

对真实 value jump，centered state 精确平移 `x+=x--Delta e`。若 jump 前 `Vc<=Rin`、目标 `Vc+<=Rout`，令 `H=Rout-Rin`，则整个椭球被送入目标椭球的充要条件可写成无根式 gate：

`B=H-(A/2)Delta^2 >= 0`,

`B^2 >= 2*A*Rin*Delta^2`。

清分母后只需 `Bnum=2*d*H-n*Delta^2>=0` 与 `Bnum^2>=8*n*d*Rin*Delta^2`。`x=-e, Delta=1, Rin=A/2, Rout=2A` 精确打到 equality boundary，说明等号只能算 non-strict boundary，不能冒充正 reserve。

这条 sharp jump gate 与 T-P5-108 组合时应先用 dwell 得到真正的 pre-jump cap `R0+qH`，再收费 jump，而不是先按外层 `R0+H` 预算 reset。对 `R0=H=1, q=1/2, Delta=31/50`，direct gate 的 exact square margin为正 `4504880292410084389/89474102220393765625`；若先按 outer collar `R0+H=2` 预算，margin 反而为负 `-619985514148683236/89474102220393765625`。所以 direct flow→contracted ellipsoid→jump 顺序能严格打开一部分原本两阶段预算会误拒绝的 schedule。

建议下一步只形式化 `c_s=P e`、sharp observable square、quadratic translation identity、no-sqrt ellipsoid inclusion，以及与 T-P5-108 decay factor 的 direct composition。actual referenceKey、真实 jump/dwell、whole-path/FD halo、Float64、Lean receipt、封不觉独立验证和 admission 仍全部外置。
