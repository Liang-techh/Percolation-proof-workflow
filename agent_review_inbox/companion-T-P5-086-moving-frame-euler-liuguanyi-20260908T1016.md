---
kind: companion_log
task_id: T-P5-086-MOVING-FRAME-EULER
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T10:16:00-06:00
status: pending mathematical/interface child
claim_commit: 840da2bf43efd3d37cdccd2c6bff24d788621913
review_commit: 6f96c363348d39ac218b07ba30f5011edbe70314
---

# 柳冠一协作留言：T-P5-086 moving-frame Euler 数学桥

本轮补的是 T-P5-082 明确留下的“时间依赖 nonlinear chart 的离散一步”边界。核心结论是：时间依赖坐标变换不能把 `T_t` 当成二阶小误差；它必须在一阶 transformed field 中就被准确吸收。若

`x=T(t,z)`，`x_dot=-F(t,x)`，`z_dot=-G(t,z)`，

则正确的 moving-frame 恒等式是

`D_zT · G = F(t,T) + T_t`。

固定基点的 `G0=G(t,z)`，对 normalized Euler `z-hG0` 在新时间 `t+h` 的物理像，和 physical Euler `T(t,z)-hF(t,T(t,z))` 之间，有精确余项

`r_mov = h^2 ∫_0^1 (1-s) C_T(t+sh,z-shG0;G0) ds`，

其中

`C_T = T_tt - 2 D_tzT[G0] + D_zz^2T[G0,G0]`。

这三个项必须尽量先形成完整的 signed/correlated `C_T`，再做区间或绝对值 enclosure。一个最小精确例子是 `T(t,z)=(t+z)^2`、`G0=1`：沿 `(t+sh,z-sh)`，chart 值严格不变，而三项分别是 `2,-4,2`，总和正好为 0。若先逐项绝对值，就会凭空收取 `8` 的 curvature charge。

对固定物理权重 `Q_W(v)=v^T Wv`，如果整条 spacetime step path 上已有

`Q_W(C_T) <= K_C`，

则加权 Cauchy/Jensen 直接给出

`Q_W(r_mov) <= h^4 K_C / 4`。

因此下游 checker 只需 exact-rational gate

`h^4 K_C <= 4 D_mov`，

即可把 `D_mov` 当作已有 P5 additive defect 使用；若还保留与 nominal defect 的 signed correlation，则可进入 correlation-aware lane。这个接口不需要 sqrt、矩阵逆或 operator norm。

另一个必须保留的阻塞例子是 `T(t,z)=z+t`、`F=0`。正确 moving-frame 给 `G=1`，于是 `T(t+h,z-h)=T(t,z)`。若误用静态规则 `JG=F` 得到 `G=0`，离散一步会产生恰好 `h` 的误差。这说明漏掉 `T_t` 是一阶错误，不是可以塞进 curvature budget 的二阶误差。

对时间依赖 affine chart `T(t,z)=c(t)+S(t)z` 也不能直接复用 T-P5-079 的 time-independent exact similarity，因为虽然 `T_zz=0`，仍有

`C_T=c''+S''z'-2S'G0`。

只有沿当前 spacetime Euler path 满足 `C_T=0` 时，才恢复 exact one-step conjugacy。

建议后续 source lane 输出最小 packet：基点 `t,z,h,G0`、base moving-frame 等式、整条 `gamma(s)=(t+sh,z-shG0)` 的 tube inclusion、固定 `W`、correlated `K_C`、以及 scalar gate `h^4 K_C<=4D_mov`。不要先拆散 `T_tt/T_tz/T_zz` 做绝对值盒。

Lean 建议先拆四个小叶：`moving_frame_euler_defect_identity`、`weighted_square_integral_triangle_kernel`、`moving_frame_defect_sq_le`、`moving_frame_defect_budget_of_mul_le`。其中第一条只负责 Taylor 路径恒等式，第二条只负责独立的 weighted integral inequality，避免把 source 几何和 scalar gate 混在一起。

当前仍是 `pending mathematical/interface child`。未闭合项包括真实 deployed chart/source 绑定、整条 spacetime path 的 domain coverage、具体 rational `K_C`、time/state-dependent physical metric、higher-order integrator、Float64/FD/controller/solve、P8/ODE coverage、Lean/kernel、封不觉独立验证以及 comparator/admission/registry。本轮没有改动 authoritative gate。
