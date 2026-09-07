# Route-B C2 audit: P4 source / D-row residual normalization

日期：2026-09-06。范围是工作流项目与只读外部项目
`C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized`。
本文件只记录数学审计；没有修改外部源、`state`、registry 或既有文件，也没有运行
Julia、全局仿真、SOS 长任务或长回归。

## 结论

当前 C2 不能关闭，但可以形成一个有明确边界的最小 exact-real child theorem。
最重要的归一化结论是：

1. 外部 Julia 的 `a` 是加速度，满足 `a = M(q) \ rhs`；
2. 外部 P4 的 `f` 是 acceleration-style nominal expression，`Ival .* f` 才是
   nominal generalized force；
3. `l45 = I_B f_B - M0_BB a_B` 是 force-side residual，不是 acceleration residual；
4. M4 文档中的 `D(e)=∫||e||²` 当前没有在 Julia 中被定义成同一个对象：导出器保存的
   `l2` 是点态 `||l45||²`，而现有 Lean residual-power theorem 的 `e` 语义是加性
   force；
5. 若 terminal `D` 要保持 acceleration-side，必须另证 `e_F=M e_A` 或其带求解误差的
   变体，并用统一的质量/逆质量范数界换算积分预算。当前接口没有这个桥。

因此，当前可接受的状态是
`C2 = CONDITIONAL_EXACT_REAL_ALGEBRA + OPEN_SOURCE/UNIT/DROW_BINDING`，而不是
`LEAN_VERIFIED_PHYSICAL`、全局 residual bound 或 M4 closure。

## 1. 当前 canonical source 与证据优先级

`robot_final/README_final.md:64-66` 说明 `robot_final/routeB_pmi_certificate.jl`
是参考副本，而 `rerun_julia.bat` 执行的是 `routeB_dense_Mq/` 原件。因此对于 P4
求解器语义，以 `routeB_dense_Mq` 为 deployed source；`robot_final` 用来核对打包副本。
五个关键文件中，`dhport_lib.jl`、`routeB_descriptor_residual_interface.jl`、
`routeB_export_traj.jl` 与 `routeB_Mq_M0.csv` 的 SHA-256 在两处相同；P4 求解器副本
本身不同，不能只按文件名认定其 provenance 相同。

外部代码证据：

- `routeB_dense_Mq/dhport_lib.jl:22-29` 声明正则化和中心差分语义；
  `:46-60` 用 DH Jacobian 构造 `M(q)` 并加 `1e-6 I`；`:73-99` 用 `h=1e-5`
  中心差分生成 `C(q,dq)dq` 与 `G(q)`；`:102-109` 返回 `M^{-1}` 求得的加速度。
- `routeB_dense_Mq/routeB_pmi_certificate.jl:85-89` 从 `M0` 取两个 block 对角元；
  `:255-289` 构造 `D0,c1,c2,D_elim_c`；`:290-305` 构造两个 PMI 多项式；
  `:316-329` 再将 `D_elim_c` 和其他项送入多项式 PMI。
- `routeB_dense_Mq/routeB_export_traj.jl:101-105` 同样以 `M\(tau-Cdq-Gq)` 得到
  `acc`；`:170-181` 计算 `lv`、`l2=||lv||²` 与 bracket `bound`，没有定义
  `∫_0^1 ||e||² dt`。

## 2. force-vs-acceleration 的实际缩放

令 block `B=(4,5)`，按当前代码

```text
I_B = diag(I4,I5) = diag(1/5, 1/10).
M0_BB = diag(0.116667666666667, 0.05018475).
```

`I_B` 来自 `dhport_lib.jl:12-18` 的 `I_val`；`M0_BB` 来自
`routeB_Mq_M0.csv`，并由 `routeB_descriptor_residual_interface.jl:22-29` 和
`routeB_pmi_certificate.jl:85-88` 读取。特别地，`M0_BB != I_B`，所以把 `I_B`
和 `M0_BB` 当作同一个缩放会改变 residual 的语义。

### 2.1 nominal expression

`routeB_pmi_certificate.jl:47-50,98-100` 和已编译的
`SourceToP4Bridge.lean:16-30` 给出同一可见 nominal expression：

```text
f4 = -(15/4) q4 - 4 dq4 + (1/20) q5 + w,
f5 = -(29/5) q5 - (13/2) dq5 + (1/20) q4 + w.
```

乘以 `I_B` 后得到 generalized force：

```text
I_B f_B =
  (-3/4 q4 - 4/5 dq4 + 1/100 q5 + 1/5 w,
   -29/50 q5 - 13/20 dq5 + 1/200 q4 + 1/10 w).
```

这正是 `artifacts/routeb_agent_p4_semantic_contract_20260906T100000Z/AUDIT_REPORT.md:18-29`
确认的 coefficient-level match。它只证明 exact-real nominal polynomial 的展开，
不证明该 polynomial 等于 DH/Float64 执行值。

### 2.2 deployed acceleration 与 P4 residual

实际 descriptor 是

```text
M(q) a = tau - C(q,dq)dq - G(q),
a = M(q)^(-1) rhs.
```

接口脚本 `routeB_descriptor_residual_interface.jl:40-48` 先求 `a`，再定义

```text
l_F = I_B f_B - M0_BB a_B.
```

两项的单位都是 generalized force：`I_B f_B` 是 inertia × acceleration，
`M0_BB a_B` 是 reference mass × acceleration。因此 `l_F` 是 force residual。
把它直接称为 `e_A` 或直接放入 acceleration-side `D(e)` 没有数学依据。

用已实际写出的 block identity，`debug_11_violpoint.jl:62-67` 还显示

```text
l_F = (M_BB(q)-M0_BB) a_B + M_BD(q) a_D
      + C_B(q,dq)dq + (G_B(q)-G_B(0))
      - mgl_B q_B + kc_B(q_B).
```

这里远端项是 `M_BD(q) a_D`。旧的 `debug_11_distal.jl:16-24` 注释写过
`(M-M0)_{B,D} a_D`，但当前独立 identity 的实际代码采用 `M_{B,D}a_D`；这是一项
文档/代码边界，不能把旧注释当作已证明公式。

### 2.3 三种 residual 不可互换

| 名称 | 当前表达式 | 数学角色 | 是否等于 M4 的 `e` |
|---|---|---|---|
| `l_F` | `I_B f_B-M0_BB a_B` | block generalized-force/reference residual | 未决定；当前不能当 acceleration |
| `e_A` | 需要另定义，通常是 actual acceleration defect | acceleration residual | 只有 terminal contract 选它时才是 |
| `e_F` | Lean `forceError` 或 full force mismatch | additive generalized force | 可直接接 residual-power，但须 source binding |

若同一 exact-real mass operator `M(q)` 已绑定且没有额外 solve defect，则可用

```text
e_F = M(q) e_A,
||e_A||² <= m_*^(-2) ||e_F||²       if sigma_min(M(q)) >= m_*>0,
||e_F||² <= M_*² ||e_A||²           if ||M(q)|| <= M_*.
```

积分后才有 `D_A <= m_*^{-2} D_F` 或 `D_F <= M_*² D_A`。对当前 `l_F`，还必须先
证明它确实等于 `M(q)e_A`；因为它含 `M_BB-M0_BB`、`M_BD a_D` 和 FD/重力/参数项，
这个等式当前不存在。若改用 `M0_BB^{-1}l_F`，得到的只是 reference-model
acceleration residual，不能自动升级为 actual acceleration residual。

## 3. D-row / Schur 语义

### 3.1 Julia P4 的 D-row 不是当前 Lean scalar row 的现成实例

Julia 的实际 P4 对象是

```text
D_elim_c = D0 - c1 - c2,
Pm1 = 4 q1 y1² + 2 nu1 y1 y2 + c1 y2²,
Pm2 = 4 q2 y3² + 2 nu2 y3 y4 + c2 y4².
```

证据是 `routeB_pmi_certificate.jl:284-305`。`c1,c2` 是在
`:269-270` 运行时创建的 SOS polynomial；现有导出没有固定有理系数和可复核 Gram
witness。因此它们不能直接被 Lean reify 为一个已绑定的 `D-row`。

Lean `P4InterfacePMI.lean:11-24` 定义的是抽象 scalar block

```text
[[p, ell], [ell, d]],       ell*x + d*a = 0,
```

并在 `:44-72` 证明“显式 D-row + `d>0` + FullStatePSD ⇒ Schur residual 非负”。
这是可靠的 exact-real algebra，但不是 Julia `D_elim_c/Pm1/Pm2` 的 source
correspondence theorem。

`SourceToP4Bridge.lean:75-104` 目前只取
`p=3/5`、`ell=1/100`、`d=116667666666667/10^15`，并以显式 interface equality
调用抽象 Schur theorem。其报告明确说 `sourceD` 只是 decimal Float64 snapshot，
没有绑定 Julia 计算、第二个 `M0[5,5]` 或 rounding provenance
(`artifacts/routeb_agent_p4_semantic_contract_20260906T100000Z/AUDIT_REPORT.md:38-52`)。

### 3.2 D-row correlated remote candidate 的单位

已有结构审计 `artifacts/routeb_agent_schur_drow_contract_20260906T101500Z/AUDIT.md:9-25`
定义

```text
s_D = r_D - M_DB a_B = M_DD a_D,
K = M_BD (M_DD + 10^-6 I)^(-1),
M_BD a_D = K s_D.
```

`s_D` 仍是 force；`K` 是 mass × inverse-mass 的无量纲映射；`K s_D` 又是 force。
因此该 candidate 可以降低 remote force budget，但不能把 `s_D` 或 `K s_D` 直接
改名为 acceleration residual。其可用契约仍需要每个 covered cell 上的
`A a_D=s_D`、`||s_D||²` 外包和 `||K||_F²` 外包
(`AUDIT.md:47-71`)；该 sidecar 自己也没有完成 deployed DH/Float64 binding。

## 4. 当前 Julia / Lean 接口矩阵

| 层 | 当前接口 | 已证明/已检查 | 明确未证明 |
|---|---|---|---|
| Julia dynamics | `dhport_lib.jl:46-109` | 代码级 `M,C,G,a` 语义；默认 `mu=1e-6,h=1e-5` | exact-real/Float64 rounding enclosure、全域 coercivity |
| Julia P4 | `routeB_descriptor_residual_interface.jl:40-57` | 点样本 descriptor solve 与独立重算 linking map | residual bound；`l_F` 与 actual `e_A` 的等同 |
| Julia SOS | `routeB_pmi_certificate.jl:255-329` | 运行时 polynomial/PMI construction shape | 固定 rational `D0,c1,c2`、Gram reification、source D-row binding |
| Julia exporter | `routeB_export_traj.jl:170-181,224-240` | 记录 pointwise `l2` 与 bracket；manifest 标记 empirical | `D(e)=∫||e||²`、continuous residual budget |
| Lean force power | `DHPowerBinding.lean:15-36,42-79` | `forceError` 的一次性 force identity 和 `e²/(2D_i)` energy bound | concrete DH/Julia binding；acceleration conversion |
| Lean residual power | `ResidualPower.lean:43-92` | 对任意 exact-real additive force `e` 的 pointwise Young bound | `e` 的物理单位和轨迹积分 |
| Lean P4 PMI | `P4InterfacePMI.lean:11-72` | abstract D-row/Schur identity and PSD implication | Julia `D_elim_c/Pm1/Pm2` correspondence |
| Lean source bridge | `SourceToP4Bridge.lean:35-42,63-104` | nominal force expansion；descriptor equality ⇒ residual zero；conditional Schur call | `arm_MCG` identity、Float64 snapshot、M0[5,5]、coverage |

特别是 `DHPowerBinding.forceError` (`:27-29`) 已把 mass difference、controller/
parameter difference、FD C/G difference 与 linear-solve residual 作为 force error
相加；`implemented_energy_bound` (`:70-79`) 消费的正是这个 force error。这是目前
最自然的 normalization lane，但 `Vec := Fin 6 → ℝ` 也没有在类型层编码“force”，
所以仍需一个 explicit source/unit contract。

## 5. 能否形成最小可证明 child theorem

可以，但只能选下面的窄合同，不应命名为 physical P4 closure。

### Child A：force-native C2 seam（当前最短、可复用）

建议合同对 `t∈[0,1]` 显式提供：

```text
J_B = diag(1/5,1/10),
f_B(t) = exact nominal acceleration expression,
a_B(t) = deployed/abstract block acceleration,
l_F(t) = J_B f_B(t) - M0_BB a_B(t),
h_desc(t): sourceForce_B(t) = M_BB(t)a_B(t)+M_BD(t)a_D(t)+r_B(t),
h_bind(t): sourceForce_B(t) = J_B f_B(t),
|e_F,i(t)| <= eps_i(t),
```

然后先证明纯代数：

```text
l_F = (M_BB-M0_BB)a_B + M_BD a_D + r_B
```

再将 full-six force residual `e_F` 送入现有
`DHPowerBinding.implemented_energy_bound_of_component_enclosures` 或
`ResidualPower.supply_with_squared_force_error`。这条 child 能在 exact-real 层
成立，且不会混淆 force 与 acceleration；它仍把 `h_desc`、`h_bind`、`eps` 作为
前提。

当前已有叶可覆盖的部分是：

- `SourceToP4Bridge.source_force_expansion`：`sourceForce45=J_B f_B`；
- `ResidualDecomposition.residual_decomposition`：在显式 descriptor equality 下
  展开 `rho_C + rho_G + rho_mgl + rho_kc + rho_mass + rho_remote`；
- `DHPowerBinding.implemented_force_identity`：把 actual force balance 的所有
  差异收进一次 `forceError`；
- `ResidualPower.supply_with_squared_force_error`：对 additive force error 给出
  `(631227/1086800) w² + Σ e_F²/(2D_i)`。

这些叶的组合目前缺少 concrete deployed-source premises，因此最小 theorem 的
状态应写成 `CONDITIONAL_EXACT_REAL_FORCE_CHILD`。

### Child B：acceleration-native terminal seam（必须新增转换假设）

如果固定 M4 的 `D` 为 acceleration-side，则最小合同必须额外有：

```text
e_F(t) = M_exec(t)e_A(t) + e_solve(t),
sigma_min(M_exec(t)) >= m_* > 0,
||e_solve(t)|| <= eps_solve(t),
```

并证明逐时或积分形式的

```text
||e_A||² <= 2 m_*^(-2) ||e_F||² + 2 m_*^(-2)||e_solve||²,
```

或更紧的同一误差分解。若 `e_F` 取当前 `l_F`，还必须先证明
`l_F=e_F`；目前 `l_F` 是 reference block row，不能自动满足。该 child 是数学上
可行的最小转换，但当前仓库没有现成 theorem 或 concrete premise，不能把它标成
已完成。

## 6. 精确 open frontier

按阻塞的逻辑顺序，C2 的 frontier 是：

1. **选择唯一 residual kind。** 在 M4、Julia manifest、Lean contract 中统一声明
   `force`、`acceleration` 或 `reference-mass-scaled`；禁止同名 `D` 跨三种语义。
2. **完成 source binding。** 绑定六轴 `M(q)`、`C_fd`、`G_fd`、`mu=1e-6`、
   `h=1e-5`、controller arrays、`Ival`、`M0[4,4]` 与 `M0[5,5]`，并处理 Float64
   literal、`sin/cos`、矩阵乘法和求解误差。P4 semantic audit 已明确这些不是
   当前 bridge 的结论 (`AUDIT_REPORT.md:32-52`)。
3. **完成 D-row correspondence。** 给出 `D0,c1,c2,D_elim_c` 的固定多项式/Gram
   导出、变量顺序、`Pm1/Pm2` 的 block order，并证明它们确实实例化
   `ell*x+d*a=0` 或另一个明确的 full-state row。当前 `D0,c1,c2` 在
   `build_cert` 内运行时生成，现有 sidecar 明确报告 coefficient gap。
4. **固定 residual decomposition。** 选择 `e_F=l_F` 或 full-six `forceError`，
   明确远端 `M_BD a_D`、mass/reference mismatch、FD truncation、Float64 rounding
   和 solve residual 每项只收费一次。
5. **若选择 acceleration D，补 inverse-mass bridge。** 需要全 covered domain 的
   `m_*` 和 `M_*`，并把 solve residual 纳入同一积分账本；不能用 `M0_BB^{-1}l_F`
   代替实际 `e_A`。
6. **完成 global budget，而非 pointwise sample。** 证明同一 full initial ball、
   `w(t)=ct,c²<=3`、原始 domain、`T=1` 下的 coverage/continuation，并得到
   `rho(t)>=Σe_i²` 与 `∫rho<=4483/2000`。当前 P3 geometry 只有
   `geometry_coverage_complete=true`，而 `dynamics_coverage_complete=false`
   (`robot_final/P3_PARTITION_COVERAGE.md:3-11`)；当前 bracket gate 仍是
   `UNKNOWN_NEEDS_COVERAGE` (`robot_final/P1_BRACKET_DECISION_GATE.md:3-10`)。
7. **保持 admission fail-closed。** P4 interface 的 Lean receipt 是窄的
   `LEAN_COMPILED_EXACT_REAL_FINITE_DIMENSIONAL`，source bridge 是 conditional；
   它们不能进入 physical/formal verified registry。已有 P4 sidecar 的报告和
   `D_elim_c` result 都把 source binding、coefficient recovery、DH、coverage 标为
   未完成。

## 7. 哈希与未知项

下列哈希是本次只读审计现场读取的 SHA-256；路径均为审计输入，不是新生成物。

| 输入 | SHA-256 |
|---|---|
| external `robot_final/dhport_lib.jl` | `AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936` |
| external `robot_final/routeB_pmi_certificate.jl` | `C1B1759161DCE5E5740283A5FF379F6E87FB95D25B5BE21A425B382CCD604EA5` |
| external `routeB_dense_Mq/routeB_pmi_certificate.jl` | `235F4876ED1A3343F6D84F83C0079B4D279886585DC36AEB55B9FC0289177A77` |
| external `routeB_dense_Mq/routeB_descriptor_residual_interface.jl` | `D3D21705E5E904A080E4B86DC4C380788D2323C155570A8E7B40D62B11BB0A24` |
| external `routeB_dense_Mq/routeB_export_traj.jl` | `35EBE806A46273068AF1AF937C0C0152378D6889024EC5586BF3C7AABD30ECCF` |
| external `routeB_dense_Mq/routeB_Mq_M0.csv` | `28D98AD71D1D6C2CBE830872CAD9077F2F7B4E2D932794217EB68868FD2E2B40` |
| workflow `docs/routeb-m4-next-obligations.md` | `4B451D84A4A844B5C268D2EC56E69F76DF907D9196DDDD37422A38C8BB2EB33A` |
| workflow `P4InterfacePMI.lean` | `9371BA9AA44A05B4D508216BB6106925CBE6165EF73B3C1BF2A4638166F3DB57` |
| workflow `SourceToP4Bridge.lean` | `7CE0E8C183C25E706D55CA55E3FDB3153D5B13B383CFCD6C7F19148F4958DDDE` |
| workflow `ResidualPower.lean` | `0F74BF60DBE7473F4B7F7D78C759A6FBFF03AE984BB932F203A31C8C8DE7DE3D` |
| workflow `DHPowerBinding.lean` | `1DA1530182F3713433C2423107F7EFD6F1F6A1E9A616DF783908688E41732D1A` |

明确未知项：

- `M0` 的数学生成 provenance 与 Float64-to-real outward conversion 未在本次源文件
  中给出可供 Lean 消费的 theorem；
- `routeB_pmi_certificate.jl` 的运行时 `D0,c1,c2` 没有固定 rational coefficient
  table/checked Gram witness；
- 当前 deployed `l_F` 尚未绑定到 full-six `forceError`，也未绑定到 terminal
  acceleration residual；
- 没有同一 normalization 下的 `D(e)` 连续积分 receipt；
- 没有 full-domain residual/Schur coverage、first-exit、T=1 flowpipe 或 terminal
  transfer theorem。

**最终判定：** C2 的“单位澄清 + exact-real algebra seam”已足够明确，最小 child
theorem 可以按 Child A 继续；但 force-to-acceleration conversion、deployed
D-row correspondence 和 global residual budget 仍是精确 open frontier。不得据此
宣称 M4、physical certificate、formal certificate 或 registry admission 已闭合。
