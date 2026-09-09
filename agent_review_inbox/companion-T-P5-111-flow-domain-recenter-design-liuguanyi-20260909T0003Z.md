---
kind: companion_log
task_id: T-P5-111-FLOW-DOMAIN-RECENTER-DESIGN
source_agent: 柳冠一
created_at: 2026-09-09T00:03:00Z
review_commit: ded61132658e9aa71f401b45ced51eb18d6eb6a5
integration_status: pending
admission_label: pending
---

# T-P5-111 协作补充

本轮没有重复 T-P5-109 的 jump sharpness，也没有继续做 source/provenance。承接 T-P5-110 的开放边界，我补了“任意 recenter 向量 `a` 的 flow 成本如何回到绝对物理 block budget”这一层。

关键新结果是一个对所有 `a,w` 同时成立的 6x6 有理二次型证书：

`pB(z+a w,s) <= 34 Vc(z,s) + w^2[(13/8)a_1^2+2a_2^2]`。

证书矩阵 `H_dom` 的六个 leading principal minors 全部严格为正，因此不需要矩阵逆、平方根、特征值或每换一个 `a` 就重新做 5x5 PSD 搜索。

这与 T-P5-110 的 flow gate

`(1+eta)L_eta(a) <= eta lambda R`

可以直接拼成 typed contract：

`34R + W a^T G a <= PBbar`，`G=diag(13/8,2)`。

在 forcing-limited 分支，把两项合起来以后仍然是关于 `a` 的凸二次型，最优 witness 只需满足一个线性 normal equation `R_* a_*=h_*`；trusted checker 不需要算逆矩阵。这个 normal equation 比 T-P5-110 的 flow-only optimizer 多计入了绝对 domain-placement 成本，但仍明确不包含 jump、初始 collar 或 runtime/source 约束。

对旧 exact center `a_eq=(2340/8699,1520/8699)`，新移动中心系数是

`13518650/75672601 ≈ 0.17864656`，

比 T-P5-106 的 `41/200=0.205` 更小，但 centered multiplier 从 `67/2` 增到 `34`，因此是一个真正的 Pareto trade-off，不是无条件替代。按 cap 比较，新 packet 在 `R/W < 398846641/7567260100 ≈ 0.05270688` 时更优；若使用 T-P5-110 的 exact-center flow floor，则对应 `S/W < 0.15147001` 的 forcing-limited 区域。

建议后续：source lane 只需把实际 `B,g,W,S` 和 referenceKey 绑定到同一 semantics；数学层选择 `a,R`；jump 仍交给 T-P5-109，以同一个 `a` 重实例化 `A_jump(a)=a^T(K+D)a`。不要把 flow-only normal equation 当成全 hybrid 最优。
