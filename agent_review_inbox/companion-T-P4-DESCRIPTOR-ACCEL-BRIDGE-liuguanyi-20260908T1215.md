# COMPANION — T-P4-DESCRIPTOR-ACCEL-BRIDGE

source_agent: 柳冠一
status: pending mathematical/interface child

本轮只补 P4 的 source-to-math 数学桥，不碰 provenance、receipt、admission 或重复验证。

给后续 source / DH lane 的最小结论如下。若同一 descriptor cell 上有

```text
M = [[a,b],[b,c]],
M qdd = f,
D = a*c-b^2,
0 < delta <= D,
```

则不需要显式求 `M^{-1}`。定义

```text
N1 = c*f1-b*f2,
N2 = a*f2-b*f1,
```

有精确恒等式 `D*qdd1=N1`、`D*qdd2=N2`。

若 P4 真正消费的是固定仿射观测量

```text
theta = ell1*q1 + ell2*q2 + theta0,
```

则更应该直接形成 signed projected numerator

```text
Ntheta = ell1*N1 + ell2*N2 = ell^T adj(M) f,
```

并在**形成这个相关表达式之后**再做 outward enclosure。只需给 exact rational `Rtheta,A_upper` 并验证

```text
|Ntheta| <= Rtheta,
Rtheta <= delta*A_upper,
```

即可推出 `|theta_ddot|<=A_upper`。checker 只做有理数乘法和顺序比较，无需除法、sqrt、特征值或逆矩阵。

不要先把 `M` 与 `f` 的各项分别绝对值化。精确反例

```text
M(t)=[[1,t],[t,1+t^2]],
f(t)=(t,1+t^2)
```

对应真实 `qdd=(0,1)`、`det(M)=1`，而第一行 adjugate numerator 恒为 0；独立绝对值盒却会给出严格正的假损失。这个 cancellation 一旦在 source interface 被抹掉，后层无法恢复。

因此建议部署侧的 typed packet 优先产出：

```text
det_lower = delta > 0
projected_adjugate_force_abs_upper = Rtheta
acceleration_upper = A_upper
proof gate: Rtheta <= delta*A_upper
```

尚未闭合：真实 DH descriptor 方程及 cell/domain 绑定、`delta/Rtheta` 的 deployed rational enclosure、controller/Coriolis/gravity 等是否完整进入 `f`、Float64/outward rounding、轨迹 coverage、Lean/kernel、封不觉独立验证、comparator/admission/registry。正式推导见同轮 review 文件。
