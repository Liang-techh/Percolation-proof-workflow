---
kind: companion_log
review_id: companion-T-P5-229-bounded-flat-fiber-support-closure-kuangmanmozun-20260910T0831Z
task_id: T-P5-229-BOUNDED-FLAT-FIBER-SUPPORT-CLOSURE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T08:31:00Z
integration_status: pending
admission_label: pending
---

# T-P5-229 中文交接

本轮接 T-P5-228 留下的“平坦但仅有界 gauge fiber”缝隙。若 `G^TQG=0`，固定代表元 `w` 后，整个 fiber 上的最坏二次型精确等于

`w^TQw + 2 h_K(G^TQw)`，

所以不需要新的二次优化器，只需要消费 gauge 参数集合 `K` 的 support function。

三个可直接给 checker 的精确分支已经闭合：盒域给出 `q0+2 sum_i T_i|b_i|<=0`；有理椭球用 `d=det(R), H=adj(R)` 化成无平方根条件 `q0<=0` 与 `d q0^2 >= 4T^2 b^THb`；有理多面体用 LP 对偶证书 `lambda>=0, F^Tlambda=b, q0+2g^Tlambda<=0`。

特别提醒：不能把每个 gauge 坐标单独拿同一份负 margin 来验。反例 `q0=-1, T=(1,1), b=(2/5,2/5)` 中两个单轴测试都通过，但联合 box 的真实最大值为 `3/5>0`。

本轮还得到一个 source 语义上更重要的尺度律。若物理基方向缩放为 `t w`，gauge 半径为 `rho(t)`，则最坏值是 `t^2 q0 + 2t rho(t) h_K(b)`。因此决定是否强制 radical 的量是 `rho(t)/t`：该比值趋于无穷时，只要符号定理在 `t->0` 仍有效，就强制 span-relative `b=0`；比值趋于常数时得到有限 support budget；比值趋于 0 时 cross term 只是局部高阶。也就是说，“有界 gauge”本身不足以决定路由，source producer 必须说明 fiber 宽度怎样随物理幅值缩放。

下一条适合数学槽继续强攻的是 curved bounded-fiber/trust-region 分支 `A=G^TQG<0`：先做负定 unconstrained Schur completion，再处理边界 active 的 rational KKT certificate。当前 source binding、coverage、Float64、Lean/kernel、封不觉验证、admission、registry 与 parent closure 均未升级。