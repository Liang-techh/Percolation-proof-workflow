---
kind: companion_log
review_id: companion-T-P5-066-zero-surface-recentering-liuguanyi-20260908T0423
task_id: T-P5-066-ZERO-SURFACE-RECENTERING
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T04:23:00-06:00
parent_review: review-T-P5-066-zero-surface-recentering-liuguanyi-20260908T0420
parent_review_commit: 3a4784366f29802d446f6c859ab528c99dd49a07
admission_label: pending
---

# 柳冠一协作说明：T-P5-066 simple-zero recentering

本轮补的是 T-P5-064/065 之后仍缺的一类数学接口：remainder 不是 nominal monomial 的倍数，因此会移动零点，但 nominal contact 本身是 simple zero。结论不是继续硬保留旧坐标，而是证明在明确的 `C^0 + transversality` 条件下可以安全换到真实零点坐标。

对

`h(x)=u(x)(x-c)+e(x)`，`x∈[c-H,c+H]`

若同一 cell 上有固定符号 `sigma`，并证明

`m <= sigma*u <= U`，

`Lip(u)<=Lu`，`|e|<=eps`，`Lip(e)<=Le`，

则定义

`mu = m-H*Lu-Le`，`M=U+H*Lu+Le`。

两个核心 exact gate 是：

`eps < m*H`：保证实际零点仍在 cell 内；

`H*Lu+Le < m`：保证 `mu>0`，阻止图像折返并维持 simple transversality。

由此严格推出每个 `x<y` 都满足

`mu(y-x) <= sigma(h(y)-h(x)) <= M(y-x)`。

所以实际零点 `r` 唯一，并有无除法位置界

`m*|r-c| <= eps`。

更重要的是可构造新的 exact unit `v`，使

`h(x)=(x-r)v(x)`，

`mu <= sigma*v(x) <= M`。

因此 lower-order remainder 并不是自动 fatal；它真正破坏的是“旧 zero coordinate”。在 simple-root transversality 成立时，可以改用真实坐标 `xi=x-r`，valuation 仍为 1、parity 仍为 odd，但必须针对新坐标重新做 domain/coverage transport。

为了保持 exact rational，source checker 不需要计算 `eps/m`。只要选择有理 `delta` 满足

`eps <= m*delta` 且 `delta<H`，

就有 `|r-c|<=delta`，并且新的公共 centered core

`|xi|<=H-delta`

保证仍落在原始 cell 内。这是后续 T-P5-063/T-P5-064 最适合消费的 domain contract。

两个反例已写入正式 review：第一，`C^0` 很小仍可能产生多个根，因此不能省略 transversality；第二，即使仍只有一个根，`C^0` 很小也可能把 simple root 退化成高重数 root，使新 unit 在 contact 处为 0。另一个边界是 `eps=mH` 只能保证根碰到 cell endpoint，公共 recentered core 会退化。

如果参数 `y` 变化，且各 fiber 有同一个 `mu>0`，同时 `|h_y(x)-h_y'(x)|<=Lp*d(y,y')`，则真实 root graph 还满足

`mu*|r(y)-r(y')| <= Lp*d(y,y')`。

因此可用 exact rational `Lr`、`Lp<=mu*Lr` 得到 root graph Lipschitz，并形成 triangular coordinate chart `(x,y)->(x-r(y),y)`。但这一层只有在两个 fiber 的 root 都处于同一个 typed overlap domain 时才能消费。

给后续 Agent 的建议：优先形式化 `signed_secant_bounds`、`root_displacement_mul_le`、`exists_recentered_unit_of_signed_secant` 和 `recentered_core_subset` 四个小 theorem。不要先做 numerical root solver，也不要把一个 root interval midpoint 当 exact root。若需要 T-P5-064 的定量 Lipschitz unit budget，还需额外证明 divided-difference/C1,1 regularity；本轮只给 unit 的 exact factorization 与正上下界，没有越权宣称它 Lipschitz。

当前仍未闭合：deployed CSE 的真实 simple factor identity、`m/U/Lu/eps/Le/H`、symbolic root source binding、多 factor intersection、multiple-root splitting、Float64/libm/FD、P8 coverage、Lean/kernel/comparator/admission。结果保持 pending mathematical/interface child。
