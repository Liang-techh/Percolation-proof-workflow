# P5 feasible-cone/SPN：闭锥逆映射与完整有理多项式检查

日期：2026-09-07。状态：**精确算术检查通过；Lean 未运行；source/admission 未闭合**。

本轮选择用户允许的 rational-checker 分支。新增文件只有本 review 与
`NEW_exact_geometry_spn.py`；未修改原 Lean、原 checker、lake 配置、state、registry
或其他 agent 的文件。运行时只读输入、输出到 stdout，并禁用 Python 字节码写入。

已阅读 `P5FeasibleConeSPN.lean`、`check_exact.py`，以及：

- `agent_review_inbox/review-T-P5-025-liuguanyi-20260907T1020.md`
- `agent_review_inbox/review-T-P5-026-guyuefangyuan-20260907T1031.md`

## 1. 本轮推进

原 checker 已有六锥符号系数检查、324 个参数基检查、18 份 toy SPN 分解和
17 个负控；原自检在本轮运行通过。本轮增加了以下独立校验：

1. 用逆映射和非负线性组合证书验证六个**完整闭锥**的等价参数化，覆盖部分不再依赖状态抽样。
2. 枚举全部 8 种弱符号情况，验证省略的两种情况仅包含原点；验证 36 个交错映射的双侧逆。
3. 在 `Q[mu,K00,...,K13,u0,...,u3]` 中完整展开 36 个 gap 恒等式，并与原 checker 的符号矩阵逐项比较。
4. 独立检查任意矩阵的 congruence 恒等式与对角因子的平方和恒等式；重新验算 18 份证书及其反号配对的全部 36 个矩阵。

所有系数使用标准库 `Fraction`，多项式使用稀疏单项式字典；没有浮点数、特征值、数值优化或状态采样。

## 2. 覆盖的可检查数学证据

单通道状态记为 `v=(x,y)`，正交象限参数记为 `u=(a,b)`。
对符号三元组 `(sx,sy,ss)`，令

```text
D = [[sx,0], [0,sy], [ss,ss]].
```

`Dv>=0` 正是 `sx*x>=0, sy*y>=0, ss*(x+y)>=0`。对六个既有 `G`，检查器提供如下逆映射 `J`：

| Cone | `J v = (a,b)` | `W` 选择 `D` 的行（从 0 编号） |
|---|---|---|
| pp | `(x,y)` | `(0,1)` |
| nn | `(-x,-y)` | `(0,1)` |
| pnPos | `(-y,x+y)` | `(1,2)` |
| pnNeg | `(x,-x-y)` | `(0,2)` |
| npPos | `(-x,x+y)` | `(0,2)` |
| npNeg | `(y,-x-y)` | `(1,2)` |

逐项精确验证：

```text
JG = GJ = I,   DG >= 0 entrywise,   J = WD,   W >= 0 entrywise.
```

因此 `u>=0 => DGu>=0`；反向 `Dv>=0 => Jv=WDv>=0` 且 `GJv=v`。
这给出 `G(R^2_+) = {v : Dv>=0}`，包括所有坐标为零、和为零的边界。

任意实数 `x,y,x+y` 均可选择弱符号。六个三元组之外只剩 `(+,+,-)` 与 `(-,-,+)`。
在这两种情形，`D` 的三个行向量之和为零，且前两行构成可逆矩阵。
若三项 `Dv` 均非负，其和为零强制每项为零，继而 `v=0`；原点已属于 pp。
所以这两种情形在弱符号约定下是**仅原点**，不能写成空集。

将 `G,J` 分别交错到 `(x4,x5,y4,y5)` 与 `(a4,a5,b4,b5)`，检查全部 36 个
`T*Tinv=Tinv*T=I`。非负性与覆盖由两个单通道证据相乘获得。
这里覆盖的是抽象 `R^4` 的符号几何，**不是 source/P8 域或轨迹覆盖**。

## 3. sign/map/congruence 的交叉检查

检查器用受限 AST 算术读取器检查原 Lean 文件中的 `cx,cy,sx,sy,ss,reverse,P,L`
八个定义表。只允许整数、有理算术、有限列表和绑定的 `a,b`，不执行 `eval`。
这只是这八个定义的文本算术核对；它不是 Lean parser/elaborator，未核验其他 Lean 定义及证明。

另一条计算路径直接用标量表达式

```text
Q(z) = 3/4*x4^2 + 29/50*x5^2 - 3/200*x4*x5
     + 2049997/3000000*y4^2 + 2399261/4000000*y5^2
     + 1/400*x4*y5 - 1/400*x5*y4
```

及两个显式通道和展开 envelope。它与矩阵路径独立比较：

```text
A = L^T D_tau K D_sigma,   B = (A+A^T)/2,
H = T^T(mu P-B)T,
u^T H u = mu Q(Tu) - sum[a,j] tau[a]*(LTu)[a]*K[a,j]*sigma[j]*(Tu)[j].
```

在先前验证的弱符号条件下，右端最后一项等于 `|LTu|^T K |Tu|`。
完整多项式恒等式不需要 `K>=0` 或 `mu>=0`；外部 SPN 输入接口继续要求这两个非负条件。

全部 36 个符号矩阵还与原 checker 的 `matrices` 计算比较。原 checker 在执行其
fixture/比较函数前先校验已审阅 SHA-256；它不负责新检查器的证书接受判定。
保留了共同依赖：两条计算路径均使用本轮的稀疏多项式运算内核，因此这不是独立证明内核。

全局同时反号使 `T,sigma,tau` 同时变号，完整多项式检查验证 `B,H` 不变。
`(pp,pnPos,pnNeg) × Cone` 与其反号集合不交且并集为全部 36 个索引。
本轮实际计算得到 18 个不同的符号代表矩阵；具体 `K,mu` 特化后仍可能重合。

通用恒等式另行展开检查，第一条不假设 `M` 对称：

```text
u^T(U^T M U)u = (Uu)^T M(Uu),
u^T(R^T diag(d)R)u = sum[i] d[i]*(Ru)[i]^2.
```

## 4. SPN 输入与验证结果

接口沿用 `T-P5-026-rational-spn-v1`，仅支持 `scope=source-independent-unbound`。
恰好需要 18 个无重复代表索引，字段仍为 `cone,S,N,R,d`。
新 checker 直接逐项求和验算 `S[i,j]=sum[a] d[a]*R[a,i]*R[a,j]`，
核对 `H=S+N`、对称性、`d>=0` 和 `N>=0`，并将同一分解应用于反号矩阵重验。
允许零对角因子及奇异 PSD；`R` 不要求三角形。

本轮实际运行结果：

- 原 checker `--self-test`：exit 0。
- 新 checker `--self-test`：exit 0；`python -O` 版本亦通过。
- 6 个 inverse/Farkas 证书、8 个弱符号情况、36 个双侧逆、18 个反号轨道通过。
- 36 个完整 gap、36 个原 checker 符号交叉检查、36 个反号恒等式通过。
- 原 toy 的 `K[a,j]=1/1000, mu=1/2`，18 份 SPN 及全部 36 个配对矩阵通过。
- `S=0, N[0,1]=N[1,0]=1` 的奇异 SPN 被接受，向量 `(1,-1,0,0)` 上二次型精确为 `-2`。
- 24 个负控全部拒绝：包括错误逆/符号/Farkas 行、Lean 表篡改、congruence 转置、
  遗漏 sym 的 `1/2`、交错坐标次序、`R` 转置、缺项/重复代表、浮点/布尔输入及伪造 source/admission 字段。
- 原 toy 通过 stdin 输入新 CLI：exit 0；含重复 JSON key 的 stdin：exit 1，明确输出 `rejected_or_uncheckable`。

toy 与非 PSD 示例只测试算术接口及矩阵证书类别；均不是实际 `K_path`。
未搜索或生成任何 source-bound 证书。`mu_lt_one` 只是精确算术标记，不能独自证明衰减。
拒绝/无法检查不表示 copositivity 反例。

可从仓库根目录复现（PowerShell；所有报告写 stdout）：

```powershell
python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_exact_geometry_spn.py --self-test
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_exact_geometry_spn.py --self-test
python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/check_exact.py --print-toy-fixture | python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_exact_geometry_spn.py --certificate -
```

也支持 `--certificate <已有 JSON 路径>`。成功输出输入字节 SHA-256，仍不认证来源。

## 5. 后续远端 Lean 的最小验证接口

现有大文件已经包含候选证明。本轮没有新增未经运行的替代 Lean 文件。可将下列六组接口
作为远端分批验证目标；这里列的是所需义务，**没有远端编译或 kernel 结果**。

| 接口 | 足够的证明内容 |
|---|---|
| 闭锥 cover | 从 `JG=GJ=I, DG>=0, J=WD, W>=0` 推导双向包含；处理两个仅原点符号情况 |
| 双通道 map/sign | 两个 cover 交错；`interleave=T*u`；`abs` 弱符号等式 |
| gap | 有限和 congruence、sym 二次型相等、固定 `Q` 系数恒等式 |
| 18 代表 | 全局 flip 下 `H` 不变；每个产品锥属于代表或代表的 flip |
| rational SPN | 有理等式/不等式 cast 到实数；`R^T diag(d)R` 的平方和；`N` 的逐项非负 |
| consumer | residual 的分量 envelope 经三角不等式，到 SPN 全空间 envelope 的传递 |

其中 cover 与 gap 给出精确等价；SPN 提供充分证书。不要把 “SPN 分解未找到”
替换成 “精确等价的右侧为假”。现有 `exact_eighteen_cone_reduction`、
`diagonal_factor_psd`、`spn_feasible_cone_small_gain` 是最终组合目标。

## 6. 证据版本与未闭合边界

本轮读取的原文件 SHA-256（复核与首次读取一致）：

```text
P5FeasibleConeSPN.lean
fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824
check_exact.py
d887aade11edf9adf1e7f532d8b173a089aac9e2fadba2e25fbc2f169e1e4211
NEW_exact_geometry_spn.py
263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42
```

本轮未执行 Lean/Lake、远端命令或安装环境。Python 的精确有限计算与上述数学推导
不能记作 `LEAN_VERIFIED`；文本表核对也不能证明原 Lean 文件可 elaboration。

仍需实际同域 `K_path`、源残差分量 envelope、坐标/力归一化绑定、IEEE 与 additive bias
分离、P8/source 域覆盖、ODE continuation，以及任何衰减结论所需的度量与轨迹桥接。
所有输出保持 `kernel_verified=false`、`concrete_K_path_bound=false`、
`source_coverage_verified=false`、`registry_eligible=false`、`P5_P8_M4_closed=false`。
