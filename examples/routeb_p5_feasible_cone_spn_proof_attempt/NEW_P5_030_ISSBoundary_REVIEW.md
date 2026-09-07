# T-P5-030：C0 与 ISS twelfth-tube 边界代数

日期：2026-09-07。新增 `NEW_P5_030_ISSBoundary.lean` 与本 review，状态为
**未编译的 source-independent Lean skeleton**。未运行 Lean/Lake，未修改旧文件、
state、registry、共享脚本，未重复 SPN increment 或 checker 工作。

依据：`agent_review_inbox/review-T-P5-030-honglianmozun-20260907T1205.md`。
新文件仅导入 Mathlib，无前几轮同名 P5 模块或未编译 adapter 的依赖。

## 形式化目标

1. `C0` 使用精确有理数 `474733828336525417/5726342542105201000`，
   给出 `0<C0<1/12` 及精确 margin 的 `norm_num` 证明脚本：

   ```text
   1/12 − C0 = 7384150516723999/17179027626315603000 > 0。
   ```

2. 显式定义 review 中的四变量 storage 多项式及 h4/h5/r4/r5。
   `initial_energy_identity` 将 `X0=−r*dc,Y0=−h*dc` 代入，目标为
   `storage(X0,Y0)=C0*dc²`。它不证明真实物理初始化或实际 moving-frame 身份。
   `initial_strict_of_identity` 再用 `dc≠0` 推出 `V0<dc²/12`。

3. `incremental_residual_ledger` 以两条外部标量不等式为参数：

   ```text
   dV ≤ −(457/1344)V + (17/10)L2，
   L2 ≤ mu*V + nu*dc2，
   ```

   得到 `dV≤−[(457/1344)−(17/10)mu]V+(17/10)nu*dc2`。
   不推断 L2 是真实 residual square；这个语义身份仍由调用者证明。

4. `ParameterGate` 保留 `mu≥0,nu≥0` 和
   `11424*mu+137088*nu<2285`。`damping_positive` 给出正齐次耗散系数。
   在且仅在这里指定的**边界** `V=dc2/12`，精确代数为：

   ```text
   ISS右端 = −(2285−11424*mu−137088*nu)*dc2/80640。
   ```

   `twelfth_boundary_strict` 使用 `dc2>0` 得到 `dV<0`；`initial_and_boundary`
   将 `dc2=dc²` 与严格初始界组合成一个 conjunction，不声称轨迹不变性。

## 必须保留的边界

- `dc≠0`/`dc2>0` 不可省略。`zero_width_boundary` 的候选命题说明在零宽、V=0
  时，ISS 不等式允许 dV=0，因此不能推出严格负导数；本轮也不证明同参数轨迹唯一性。
- 边界导数严格为负不意味着 tube 内每一点的导数严格为负。
- 原始绝对 residual cap 不能冒充同域的 incremental envelope。
- 所有常数属于声明的精确数学模型；没有推断部署 Float64、力归一化、source 坐标或参数语义。

精确剩余前提是：真实 V0 的初始化身份；真实 dV 与 storage 导数的识别及原 ISS
耗散界；同域 residual difference 的平方身份和 envelope；满足 gate 的真实 mu/nu。
若要从本代数结果继续推出 tube 不变性，还须提供时间连续性/可微性、dc 的常量身份、
边界上前提的持续有效性，以及 first-exit、ODE continuation 和域覆盖证明。
这些均未在本文件中假定为已验证事实，也未使用形式化 ODE 包装掩盖其缺失。

## 本轮验证范围

只进行源码接口检查，以及一次 Python 标准库 `Fraction` 的独立精确算术核对：
从所列 storage、h、r 常数算出的初始系数与 C0 完全相等，margin 与上式完全相等；
边界三项系数为 `−457/16128`、`17/120`、`17/10`，对应公分母 80640。
该计算仅写 stdout，没有生成 fixture 或日志文件，不是 Lean 验证。

Lean 证明脚本和末尾 `#print axioms` 尚未执行，需要后续授权环境的 elaboration/
kernel 与公理检查。本轮没有 kernel PASS、LEAN_VERIFIED、source/coverage/P8/M4 closure
或 registry admission 声明。
