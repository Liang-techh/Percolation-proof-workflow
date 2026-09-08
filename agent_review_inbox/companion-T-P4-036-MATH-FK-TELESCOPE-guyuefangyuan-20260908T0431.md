---
kind: companion_log
review_id: companion-T-P4-036-MATH-FK-TELESCOPE-guyuefangyuan-20260908T0431
task_id: T-P4-036-MATH-FK-TELESCOPE
source_agent: 古月方源
created_at: 2026-09-08T04:31:00-06:00
parent_review: review-T-P4-036-MATH-FK-TELESCOPE-guyuefangyuan-20260908T0428
parent_review_commit: f37611b2ca9388bf50d3c1cbcb66b7803da18a89
admission_label: pending
---

# 古月方源协作说明：T-P4-036 standard-DH / FK telescoping

本轮先发现一个需要避免的重复：我上一轮认领的“12 行 quarter-turn phase cancellation”其实已经由更早的 `T-P4-036.2` 数学 review 完整证明，并且巨阳仙尊已经把 12 个 theorem 编译成 compiled candidate。因此没有重新做同一证明，已用单独 review 把旧 claim 标成 duplicate/superseded。

新的实质推进放在仍然开放的 finite-DH propagation。对显式 standard-DH 矩阵 `A(a,d,theta,alpha)`，可以精确算出：

`||A||_F^2 = 4+a^2+d^2`，完全与两个角和 quarter-turn phase 无关；

固定 alpha 时，

`||A(theta)-A(theta')||_F^2 = 4(2+a^2) sin^2((theta-theta')/2) <= (2+a^2)(theta-theta')^2`；

固定 theta 时，

`||A(alpha)-A(alpha')||_F^2 = 8 sin^2((alpha-alpha')/2) <= 2(alpha-alpha')^2`。

更强的是两个切向量在 Frobenius 内积下处处正交，并且平方范数恒为 `2+a^2` 与 `2`，所以沿直线参数路径可得到

`||A(theta,alpha)-A(theta',alpha')||_F^2 <= (2+a^2) dtheta^2 + 2 dalpha^2`。

这说明 exact-real 层根本不需要把每一个 sin/cos entry 独立 intervalize 后再做 4x4 盒运算；可以保留 `sin^2+cos^2=1` 的相关性，直接输出一个 link-level square budget。

对 n 个 link 的乘积 `P=A1...An`，用 telescoping identity、Frobenius 次乘法和 `||sum Xi||^2 <= n sum ||Xi||^2`，定义

`Mi = 4+ai^2+di^2`，

`Ri = (2+ai^2)dtheta_i^2 + 2 dalpha_i^2`，

即可得到纯平方、无根号的 exact bound

`||P-P'||_F^2 <= n * sum_i [ Ri * product_{j!=i} Mj ]`。

六连杆时就是前面的 `n=6`。如果 `a_i,d_i` 和角误差半径是 rational/dyadic，整个右侧都是 exact rational；trusted checker 不需要三角函数、sqrt、特征值或逆矩阵。

与 `T-P4-036.2` 的相位表还存在一个很好的简化：同一 link 的 frozen quarter-turn phase 在比较两个 q 时完全相消，所以 theta perturbation 只剩 `q_i-q_i'`。例如整个 `[-3/20,3/20]^6` 的任意两点可直接得到系数 `27/50` 的 whole-box chain diameter；从 `q=0` 中心出发则是 `27/200`。

给后续 Agent 的建议：Lean 第一版不要一开始就做 matrix-valued path integral。先形式化 `standardDH_frobenius_sq`、theta/alpha 两个 exact chord identity、各自 square upper bound，再做 calculus-free 的 two-angle fallback 和 generic finite-product telescoping。若需要把常数从 fallback 再收紧 2 倍，再单独形式化切向量正交 + straight-path theorem。已有 `T-P4-022` 负责 generic `||Tz||` Frobenius consumer，不要重复证明；本轮只提供 DH-specific `||P-P'||_F^2`。

必须保留的边界：这个结论依赖 Section 1 明写的 standard-DH convention。modified-DH、转置排列或部署端额外修正不能因为名字都叫“DH”就直接消费。source lane 必须先证明实际 link transform 等于该矩阵，或通过固定正交左右乘变换等距输运。Float64/libm、matrix assembly rounding、COM/Jacobian/M/C/G、FD/solve、P8 coverage 和 admission 仍全部开放。

当前建议的最短接力是：source lane 冻结真实 link matrix convention 与 `a_i,d_i`；Lean lane只做上述 5 个小代数 theorem + 一个 square telescoping theorem。这样可以把 finite-DAG 的第一层从逐 entry 宽区间改成结构保持的 link-level bound。
