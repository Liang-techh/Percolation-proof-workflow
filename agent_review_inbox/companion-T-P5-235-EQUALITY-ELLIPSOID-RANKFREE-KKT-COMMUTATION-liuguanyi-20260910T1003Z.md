---
kind: companion_log
task_id: T-P5-235-EQUALITY-ELLIPSOID-RANKFREE-KKT-COMMUTATION
source_agent: 柳冠一
created_at: 2026-09-10T10:03:00Z
inspected_commit: 1c074f03d5855488ce9b5f96cea437c0d5481973
review_commit: fde193bcd1c1231efc817e804d5d985b7a244d5b
status: pending
admission_label: pending
---

# 柳冠一协作交接 — T-P5-235

本轮沿 T-P5-234 明确留下的 seam，闭合了“精确线性等式 + 椭球 source fiber”的 rank-free 数学接口，没有转做 provenance、receipt、admission 或重复验证。

核心结果：对 `q(y)=q0+2g^Ty-y^THy`、`Ay=0`、`y^TPy<=T^2`，其中 `H>=0,P>0`，安全性与存在 `lambda>=0,nu` 使

`[[H+lambda P, A^Tnu-g],[(A^Tnu-g)^T,-q0-lambda T^2]] >= 0`

完全等价，不要求 `A` 满行秩。固定 `lambda` 后，“先 quotient 到 `ker(A)` 再做 trust-region”与“先加入 `lambda P` 再用等式 multiplier `nu` 消去”等价；因此两个层次严格交换，不需要显式 nullspace basis。

在 active branch `lambda>0`，令 `K=H+lambda P`、`d=det K`、`J=adj K`、`r=g-A^Tnu`。则 PSD gate 精确退化为无除法标量条件

`d(q0+lambda T^2)+r^T J r <= 0`。

最佳等式 multiplier 满足 `AJr=0`；若进一步满足 active boundary

`(Jr)^T P(Jr)=d^2 T^2`，

则 `y*=Jr/d` 是真实 worst-case contact，且上述标量值给出 exact supremum。这样可以把 T-P5-234 的 equality quotient 与 T-P5-230 的 trust-region multiplier 合成一个 rational KKT packet。

重要边界：若 source equality 是 affine/未统一中心化，或只有 `||Ay||<=eps` 的 relaxed tube，上述交换 theorem 不能直接消费；outer ellipsoid 的 certificate 失败也不能升级成真实 source FAIL。sharp boundary 若唯一最优 `lambda` 为 irrational，则需要 algebraic/root-isolation 或 interval-certified multiplier；只有 strict reserve 时才可安全 rationalize 到附近有理数。

建议下一数学 seam：从真实 state/source 的物理椭球或能量 sublevel，经可能非单射的 lifted `(v,z)` 坐标运输出 quadratic fiber，并刻画 pullback 只在 equality quotient 上正定时的 coercivity 条件。这样可去掉当前 ambient `P>0` 的偏强假设，直接接 source-to-math adapter。
