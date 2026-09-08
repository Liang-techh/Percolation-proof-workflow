# P4 Schur/PMI closure: exact composition and physical residual obstruction

2026-09-08. **RESEARCH / UNCOMPILED / NO SOURCE CLOSURE**.

本任务只新增本 review 和同 stem `.lean`，不修改现有 absorption、其他 agent 的
`NEW_P4_032_BudgetClosureAudit.lean`、state、registry 或共享 adapter；无全回归、
Lean/Lake、远端构建或 registry promotion。当前结论是数学接口可组合，所检查的
真实 block-(4,5) source/producer 链仍不能填满它的前提；不是物理系统不可行的结论。

## 1. 当前 absorption 的正确结论及必要区分

记 `E=energy`, `Q=q`, `rho=rhoEff p`, `B=biasEff p`。
`NEW_P4_032_SchurPMIAbsorption.lean` 保留

```
E,Q,rho,B >= 0,   Q <= rho*E+B,
delta>0,         rho+delta<=1.
```

因此精确组合为

```
delta*E-B <= E-Q <= margin.
```

若只使用这个 floor，要推出 prescribed target `t<=margin`，充分条件是
`t+B<=delta*E`。该条件对所有只受此 floor 约束的抽象 margin 也是必要条件，
但并非某个实际更大 margin 的必要条件。已有并发 `BudgetClosureAudit` 给出这一层；
本研究不重复修改其证明。

`SchurPMIBinding.lower` 是调用者提供的 `E-Q<=margin`，不能从 Schur 消元恒等式、
矩阵名字、solver flag 或 residual cap 自动得到。`FeedbackBinding.upper` 则是另一条
方向相反、独立的 `E<=base+Q`，不是 margin lower comparison 的推论。

对真实非单位比较，令 `g>=0` 为已经验证的 residual-scalar gain/scale 乘积：

```
alpha*E+offset-g*Q <= margin
  => (alpha-g*rho)*E+offset-g*B <= margin.
```

要把它解释为正的 energy coercivity，检查的是 `alpha-g*rho>0`。
仅 `rho<1` 不够；目标分配是
`t+g*B <= (alpha-g*rho)*E+offset`。
若 E 有上界而非下界，不能直接用它替换正系数前面的 E 来证明正 target floor。

更一般的 feedback `E<=base+c*Q`, `c>=0` 给出两个精确 division-free 结果：

```
d = 1-c*rho,
d*E <= base+c*B,
d*Q <= rho*base+B.
```

只有 `d>0` 才能除以 d 得有限上界。由此分配 `Q<=available` 的正确条件是
`rho*base+B <= d*available`。residual 分子的 B 只有一次；energy 分子则是 cB。
`c=2,rho=1/4,B=1/4,base=1,E=3,Q=1` 同时达到四条等式，说明该系数是紧的。
这些是标量条件式，不证明 source 满足 feedback。

## 2. 从 port 到完整 residual 的 exact Schur composition

实际组合对象设为 `L=ell+r`，其中 ell 与 r 均为同一 generalized-force 坐标中的
二维向量。令 `Qp=||r||_2^2<=W`, `L0=||ell||_2^2`。不能以 Qp 代替 `||L||²`。

对 `lambda>1`，外部 combined-Schur producer 写出的 target 版本为

```
K_lambda = [ base-t-lambda*W       ell^T                  ]
           [ ell                 ((lambda-1)/lambda) I_2 ].
```

在实对称矩阵且该正对角块可逆时，完成平方给出数学等价：

```
K_lambda >= 0
  <=> S_lambda := base-t-lambda*W-lambda/(lambda-1)*L0 >= 0.
```

这条矩阵等价在本 review 纸面推导，伴随 Lean 不声称证明 Matrix.PosSemidef。
伴随文件证明尝试直接使用以下无除法的二维恒等式；设

```
H_lambda=(lambda-1)*(base-t-lambda*W)-lambda*L0.

(lambda-1)*(base-t-||ell+r||²)
 = H_lambda
   + ||ell-(lambda-1)*r||²
   + lambda*(lambda-1)*(W-||r||²).
```

所以 `H_lambda>=0`、`lambda>1`、`||r||²<=W` 足以给出
`t<=base-||ell+r||²`。不丢交叉项，不依赖 S-lemma losslessness，也不要求球有严格内部。
如果还有同一个 source 的 lower comparison `base-||ell+r||²<=margin`，再 trans 到 margin。

把现有 absorption 输出用于 PORT，取 `W=rho*E+B`；完整分配变成

```
t + lambda*(rho*E+B) + lambda/(lambda-1)*||ell||² <= base.
```

这与 `t+B<=delta*E` 是不同的消费式。后者只有当 Q 已经是完整 residual 平方，且
`E-Q<=margin` 已在同一 normalization 下证明时才能直接使用。
新 `combined_of_absorbed_port` 保留了 port 输入和 total-residual comparison 的区别。
连接原 `force_absorption` 仍需 `norm2(r)^2 = r0²+r1²` 的 Euclidean norm API 桥；
没有以 Pi/sup 范数替代，也未假装已经实现该库级桥。

若 base 是 `alpha*E+offset`，另有 `||ell||²<=kappa*E+B_ell`，完整有效系数为

```
rho_total = lambda*rho + lambda/(lambda-1)*kappa,
B_total   = lambda*B   + lambda/(lambda-1)*B_ell.
```

正 coercivity 要求 `alpha>rho_total`，目标再要求
`t+B_total <= (alpha-rho_total)*E+offset`。不能仅检查 raw port 的 rho 或 external gamma。

## 3. 单次扣除究竟要求什么

单次预算规则来自同一个 scalar expression 的恒等分解，并不是“相同名字只能出现一次”：

- 若 Q 已经是 total residual 平方，使用其 cap 替换 `-gQ` 一次；其中已含的 B 不再独立加到同一 loss。
- 若 cap 只控制 port，必须先组合 ell 与 port。上式的 lambda*B 是一次经 Young/Schur 放大的扣除，
  不是非法重复扣除；省略 lambda 会低估真实所需预算。
- 若执行/FD defect 已放进 distal/local envelope，W 已含其效应；不得把它再次作为“未计入的独立误差”
  宣称是同一个精确预算。真正独立的剩余项须有 source 恒等分解、符号/范数上界和自己的分配。
- 两个不同 loss 共用同一个 nominal energy 时，需证明其系数分配之和不超出可用系数；不能各自消费全额 front。
- 对同一个已扣除的 Q 再扣一次，只会得到更弱的下界，通常造成假阴性；它本身不是产生假阳性的证明漏洞。
  危险的是把这个更强需求当成原条件的等价式，或相反地漏掉 total residual 的交叉项/误差。

例：`E=2,Q=1,rho=1/2,B=0,delta=1/2,t=1` 有 `t=E-Q`，但 `E-2Q=0<t`。
这清楚区分“重复扣除损失可行性”和“漏扣导致错误正结论”。

## 4. 最小反例与固定 lambda 的真正限制

以下都是 exact scalar/二维接口反例，不声称是 descriptor 可达状态。

| 错误推论 | 最小指定值 | 实际结果 |
|---|---|---|
| 正 slack 可删掉 B | `E=0,Q=B=1,rho=delta=1/2,margin=-1` | 所有 relative/comparison 前提成立，margin 仍负 |
| port cap 就是 total cap | `r=(0,0),ell=(1,0),base=1/2,t=0` | `base-||r||²=1/2`，但 `base-||ell+r||²=-1/2` |
| rho<1 足以忽略 gain | `E=1,Q=rho=3/4,B=0,alpha=1,g=2,offset=0` | scaled margin 为 `-1/2` |
| 相对 residual 上界蕴含 feedback | `E=2,Q=rho=B=base=0` | relative 成立，`E<=base+Q` 不成立 |
| fixed finite lambda Schur 条件总是必要 | `W=0,ell=(1,0),base=1,t=0` | 球内仅 r=0，真实 margin=0；所有 lambda>1 都有 H_lambda=-1 |

最后一行是一个有用的新区分：failed fixed-lambda allocation 不必意味着 robust residual 条件失败。
对完整无方向约束的 Euclidean ball，精确最坏 residual 值为

```
sup_{||r||²<=W} ||ell+r||² = (sqrt(L0)+sqrt(W))²,  W>=0.
```

当 `L0,W>0` 时，`lambda*=1+sqrt(L0/W)` 使
`lambda*W+lambda/(lambda-1)*L0` 等于这个最坏值。
`W=0,L0>0` 需要 lambda 趋于无穷才达到边界；`L0=0,W>0` 需要 lambda 趋于 1。
两者都为零时任意 lambda>1 都达到零。边界的 robust 非负性可能成立而没有有限 lambda witness。
严格余量可消除这些端点不取到的问题，但不自动给出跨整个域的单个 uniform lambda。
上述 worst-case 是针对放大的完整球；真实 descriptor 有方向相关性时，它仍只是充分路线。

## 5. 与真实 block-(4,5) residual 的连接判定

本轮重新读取实际 producer/descriptor 源码，并核对本地 residual contracts。
检查范围内的判定为：**只存在条件式连接，尚不能构造真实 source closure witness。**

固定 B=(4,5), D=(1,2,3,6)，内部索引 B=(3,4), D=(0,1,2,5)。现有 source-independent
`BlockDefects.full_equations_to_port` 的精确结构是

```
R=-M_BD * (J * DeltaM_DB),   T=M_BD*J,   J*M_DD=I,
r_B=R*a_B+T*e_D+e_B.
```

必须有同一 a_B 的 actual/reference equations。若 a_B0 不同，distal defect 中额外出现
`-M0_DB*(a_B-a_B0)`；不能静默删掉。force-side balance defects 的 Schur 消元则是
`epsilon_B-T*epsilon_D`，不能与上述 O1 的 `+T*e_D+e_B` 按名字直接对接。
现有 `DefectConventionCore.adapt` 同时改变变量、参考项与误差，正是必需的区别。

实际 interval probe `routeB_compact_composed_interval_probe.py:258` 及其末尾说明控制的是
`R_port*a_B` 的力范数相对于 `A_up=a_B^T B_up a_B` 的系数，R 保留负号。
它不控制 `T*e_D+e_B`，也不控制 `ell`。`BlockDefects/RelativeAdditive` 提供保留这些项的
条件接口，但 ledger 行本身没有构造这些 defect envelope、tau 或 rhoEff/biasEff。

`routeB_compact_direct_descriptor_structure.jl` 的 `nominal_eq/port_eq/total_eq` 明确使用
零 distal descriptor defect、port link 和 `l_total=l_base+r_port`。其 l_base 来自
`IVAL*fB-M0BB_CONST*aB`，并且由 `ROUTEB_CONTROLLER_BRANCH` 选择 Fourier/DH controller。
这说明候选对象的公式存在，**不说明该零缺陷 descriptor 已绑定到执行状态**。

执行侧 `P4ExecutionResidual.block_residual_with_solve_defect` 保留真实 lift 的差项：

```
l_F=(I*f-tau_B)+(M_BB-M0_BB)*a_B+M_BD*a_D+C_B+G_B-epsilon_B,
epsilon_B=(M*a-(tau-C-G))_B.
```

所以至少还缺下表中的同实例证据，任何单一正系数行都不填充它们：

| 所需桥 | 当前缺口 |
|---|---|
| source/units | 选定 controller、storage、regularizer、reference、force coordinates 及精确 digests |
| residual identity | 执行 l_F 与所消费 ell+r 的等式；求解 defect、参考差和 FD/控制误差的去向 |
| squared port cap | source/interval 数值 reification、同域 coverage、nonzero defect envelopes 和 T action bound |
| metric/normalization | A_up 与所用 E 的等式或正确方向界；总 force norm 与 q；gain/beta/front 的量纲与符号 |
| Schur comparison | 从同一 storage/descriptor 推出真实 scalar margin 的 lower comparison，含交叉项 |
| allocation/closure | 同状态 base/ell/A_up 的 target 分配；若用 feedback，另证 upper closure；全域须 uniform |

特别是 `diag(1/5,1/10)` 是非等距 force conversion，不能因为都是二维就把 raw PMI norm 与
force norm 或两个 residual 当成同一个数；mass-block port 已在 force 坐标时也不能再缩放一次。
`routeb_residual_l1_contract.py` 审核的是 Gram 系数残差 `weighted_residual_l1_bound` 的 receipt；
它不因名字含 residual 就成为本处的物理 `||ell+r||²` bound。

## 6. 实际 ledger 行的有限结论

重新读取外部 CSV 的物理行 9：eta=5.6, theta=1, mu=1e-6,
rhoSq token=`0.07849312228597172`, charge token=`0.15698624457194343`,
gamma token=`0.2`, candidate_margin token=`0.04301375542805658`；
321 resolved/16 outside/0 unknown，`routeB_global_gate=False`。

这里 `operator_pmi_gamma_lower_bound` 是“所需 gamma 下限”的历史列名；producer 用其作为
PORT 平方系数的候选上界，不是 q 本身的 lower bound。其 rhoSq 与本 absorption 的 rhoEff
仍需按 weights/defects/metric 计算，不能直接相等。

精确十进制 token 算术有
`2*rhoSq-charge=1/10^17`，`printed_margin-(gamma-charge)=1/10^17`。
因此不能将三个打印 token 同时当作 exact identity 的值；它们的正 slack 也不代表已完成
向外舍入或 source reification。本轮未执行该 interval producer。

该行没有 base、ell、controller/storage key 或 prescribed target。对 theta=1，仍必须证明
`t+2||ell||²+charge*A_up<=base`，并先用有效界替代打印 charge。
本轮不从这条缺字段行推断真实 source 可行/不可行，也不混入其他行的 baseline。

## 7. 新增证明与定向检查

伴随 Lean 包含 10 个 theorem 候选：二维平方非负、exact remainder identity、port-cap consumer、
与 AbsorbedAt 的条件接线、scaled margin floor、general-gain feedback、port-only/gain 反例、
零半径 fixed-lambda obstruction 与该反例的真实 scalar margin。均 **UNCOMPILED**；
未运行其 10 条 `#print axioms`，未审计传递依赖。矩阵 PSD 等价、球上的最优 lambda、
source/WithLp norm 桥只在本 review 给出数学说明，没有冒称为该 Lean 文件的结论。

执行一次内存内 SymPy/Fraction 检查：完成平方的全参数二维多项式恒等式、零半径 H=-1、
port-only 与 gain 反例、gain=2 feedback 等式，以及两项十进制差值；全部通过，命令退出码 0。
另外只检查新增文件的占位 token/声明数量与行尾空白；没有全回归、Lean、Julia、solver 或 interval run。

建议下一项数学工作直接构造**同一个 source 的总 residual identity 与 base 分配**，保留 defect，
选择直接相关性分配或 Schur/Young 分配。再重复标量吸收公式不会解决缺少 source 对象的问题。

输入快照（SHA-256，仅用于定位，不是验证 receipt）：

| 输入 | SHA-256 |
|---|---|
| `NEW_P4_032_SchurPMIAbsorption.lean` | `F18F9FB180AEAFAAD0DC3CD5149894D03EE111DB5C45ABFB86CAA927DF4050E3` |
| `NEW_P4_032_RelativeAdditive.lean` | `6DB219F352AEB2FB0C5AD0985154BA65FBB7F59144A22C5B7A7CCF5E63F5EADD` |
| `NEW_P4_032_BlockDefects.lean` | `AA1CCE18E39B1B675483C9ECE7CECBC1A2740C65DF1846582CA57963C0A6CC51` |
| external `routeB_compact_external_budget_ledger.csv` | `A00383CB7FF547979028047C4489D7A4328D60B582B808EFB65B19C2BBA3C2C6` |
| external `routeB_compact_combined_schur_interface.py` | `C6D2AF78691325991D6B91C163CD01AC8CFC8EE8B455FC963920A9E3FDF3529C` |
| external `routeB_compact_direct_descriptor_structure.jl` | `2C2F623F966425952CBBBD3C04BAE84858147FE7FDD386F5BC5F4FF35E2FB98C` |

external 根目录：`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`。
