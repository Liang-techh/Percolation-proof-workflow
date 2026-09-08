---
kind: companion_log
task_id: T-P5-082-NONLINEAR-CHART-PULLBACK
source_agent: 柳冠一
created_at: 2026-09-08T09:20:00-06:00
review_id: review-T-P5-082-nonlinear-chart-pullback-liuguanyi-20260908T0918
admission_label: pending
---

# T-P5-082 中文协作摘要 — nonlinear chart pullback / curvature defect

本轮补上 `T-P5-079`、`T-P5-081` 明确留下的 nonlinear chart 边界。结论需要分成两层，不能混为一谈。

第一层是连续时间/微分几何层。对 `x=T(t,z)`、`J=D_zT`、物理系统 `x_dot=-F(t,x)`，若用乘法式

`J G = F(t,T)+T_t`

定义 `z_dot=-G`，并把物理定常 SPD metric `W` 拉回成

`M=J^T W J`，

则有精确恒等式

`D M[G] + DG^T M + M DG - M_t`
`= J^T(A^T W+WA)J`，

其中 `A=D_xF`。所以只要物理侧有 `A^T W+WA >= 2 mu W`，nonlinear chart 下的微分能量仍以完全相同的 `mu` 衰减。这里 Hessian/connection 项会被 pullback metric 的导数精确抵消，不能先绝对值化后再额外收费。

第二层是 P5 当前真正消费的 finite-step/secant corrector。这里 affine chart 的 exact conjugacy 不再成立。固定 nonlinear chart 下，若 `JG=F∘T`，normalized Euler `z_E=z-hG` 映回物理坐标后与 physical Euler 的差恰好是

`r_curv=T(z-hG)-[T(z)-hF(Tz)]`

`=h^2 ∫_0^1 (1-t) D^2T(z-thG)[G,G]dt`。

因此 nonlinear chart 的有限步代价不是一个模糊的 condition-number penalty，而是一个精确 curvature remainder。若整个 step segment 上

`||D^2T(u)[v,v]||_W <= K_T ||v||_Z^2`

且 `||G||_Z^2<=B_G`，则

`||r_curv||_W <= (K_T/2) h^2 B_G`，

并可用完全无除法的 gate

`K_T^2 h^4 B_G^2 <= 4 D_curv`

得到 `Q_W(r_curv)<=D_curv`。这个 `D_curv` 应直接送进 `T-P5-078/T-P5-081` 的 additive defect lane；若能证明 signed correlation，则送进 `T-P5-080`。不要再额外收第二份“chart motion”费用。

`1/2` 常数是 sharp 的：在 `T(z)=z+z^2/2`、`z=0,h=1,G=1/2` 上，curvature remainder 精确等于 `1/8`，正好达到 `(1/2)h^2G^2`。

还给了一个 exact rational obstruction：物理 `F(x)=x` 的强单调常数是 `mu=1`，但经 `T(z)=z+z^3` 变换后 `G=(z+z^3)/(1+3z^2)`，在 `z=1` 与 `z=1/2` 两点的 secant ratio 只有 `2/7`。所以 nonlinear chart 下不能把 `T-P5-079` 的 finite-secant `mu` 原数值照搬；能无损搬运的是 pullback metric 下的 differential rate。

给后续 Agent 的建议：如果 deployed source 真存在 nonlinear normalization，先查清它消费的是 differential/Riemannian theorem 还是 finite-step corrector。前者优先证明 exact covariance 与 connection identity；后者必须再给 step-segment inclusion、Hessian cap 与 `G` 的平方上界，生成 `D_curv`。这两个 lane 的证据不能互相冒充。

当前仍是 `pending mathematical/interface child`；source binding、chart coverage、Float64/FD/controller、P8、Lean/kernel、封不觉独立验证、admission/registry 均未闭合。
