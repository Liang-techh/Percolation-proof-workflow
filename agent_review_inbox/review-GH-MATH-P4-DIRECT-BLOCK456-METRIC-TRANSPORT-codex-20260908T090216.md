---
kind: review_result
review_id: review-GH-MATH-P4-DIRECT-BLOCK456-METRIC-TRANSPORT-codex-20260908T090216
task_id: GH-MATH-P4-DIRECT-BLOCK456-METRIC-TRANSPORT
source_agent: Codex-block456-metric-research
created_at: "2026-09-08T09:02:16.1036156-06:00"
inspected_commit: 29fc6330213f11f34e618d3857a599c44d7c17c2
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908_REVIEW.md
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_factorized_descriptor_model.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block456_direct_scalar_sos_budget_audit.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.jl
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
registry_mutation: false
source_binding: false
final_integration: false
requested_action: retain exact LDL metric transport as bounded research; obtain source reification and pinned Lean transport receipt; do not replace the metric or promote registry
---

# Block-(4,5,6): exact nominal-metric transport

**结论：dense metric 本身可以精确运输，并不存在实数线性代数障碍。** 本轮从实际 mass CSV 的
原点代入提取出一个简单、正主元的有理 LDL 分解。只需三个标量平方根即可接到已有 generic
Euclidean theorem；不必构造通用矩阵平方根库。当前 inspected source contract 尚未提供该
常矩阵的 Lean reification、total-residual/source 等式与 matching-metric cap 的验证见证，
因此仍是条件式数学接口，不能声称真实 source closure。

本轮只写这一份 bounded review；不新增 Lean 文件、不改旧文件、state、registry 或共享 adapter。
不重复二维 Schur 推导，不执行 Lean/Lake、Julia、interval producer、solver 或全回归。
此处 OPEN_UNCOMPILED 表示尚无本轮 kernel/transport receipt，不评价其他任务的运行结果。

## 1. 固定对象与原点矩阵

块序固定为 C=(4,5,6), D=(1,2,3)，内部 Fin 坐标为 (0,1,2) 对应物理 (4,5,6)。
descriptor source 以 `mu=1/1000000`、各 cos=1/sin=0 定义 `M0CC456`；它不是 q-dependent
`M_CC(q)`、二维 M0_BB、Gershgorin `B_up` 或 Float64 M0 文件。

重新读取 `routeB_factorized_descriptor_model.jl::load_mass` 的 num/den 与指数约定，
只解析 CSV 的 C×C 项，在原点保留 sin 指数全零的六项，再加三项 regularizer，得到

```text
M = M0_CC = [ 350003/3000000     0                 1/60             ]
            [ 0                 200739/4000000     0                ]
            [ 1/60              0                 50003/3000000    ].

N = 5000400003,
H = M^-1 = [ 50003000000/N       0                 -50000000000/N   ]
           [ 0                  4000000/200739     0                ]
           [ -50000000000/N     0                 350003000000/N   ].
```

因此所谓 dense metric 在这个固定原点实际只耦合 4 与 6，但该耦合不能删除。
这是一项对当前 CSV 精确有理数解释的检查，不是 CSV 到 Lean/DH/运行时值的已验证桥。

## 2. 最小 exact factor witness

令 a=50000/350003，并取

```text
U = [1 0 0; 0 1 0; a 0 1],
D = diag(350003/3000000, 200739/4000000, 5000400003/350003000000),
A = U^-1 = [1 0 0; 0 1 0; -a 0 1].

M = U D U^T,
H = A^T D^-1 A.
```

三个 D 主元严格为正，U 可逆，故纸面上 M、H 都是 SPD。已用精确有理数运算核对两个矩阵
恒等式和 `M*H=I`；不以“det>0”单独推 SPD。供交叉检查，三个顺序主子式为

```text
350003/3000000,
23419750739/4000000000000,
334591765400739/4000000000000000000.
```

令正有理权重

```text
w1=3000000/350003, w2=4000000/200739, w3=350003000000/5000400003.
```

对任意 v=(v4,v5,v6)，精确的无平方根形式是

```text
v^T H v = w1*v4² + w2*v5² + w3*(v6-a*v4)².
```

若直接复用未改写的 `GenericSchurAllocation`，定义一个固定实线性映射

```text
T(v) = (sqrt(w1)*v4, sqrt(w2)*v5, sqrt(w3)*(v6-a*v4)).
```

只需证明三个 `0<=wi` 与 `Real.sqrt wi ^ 2 = wi`，以及有限和/矩阵项展开，就有
`T^T*T=H`、`sq(Tv)=v^T H v`、`T(u+v)=Tu+Tv`。此 T 对 q/state 不变；无需处理随状态变化
的平方根，也没有因本次代数替换引入导数项。若以后改成 M(q)，必须另立对象，不能沿用常矩阵等式。

一般 API 的最小输入可直接是一个实线性 T 和 `forall v, sq(Tv)=v^T H v`；若因子已提供，
下游 scalar consumer 无须再消费 SPD、逆矩阵存在性或矩阵平方根定理。SPD 是从此处
`M^-1` 构造正规三维等距同构的充分条件。对称 PSD 也允许平方范数表示，但奇异 M 没有此 target
所指的普通逆；不能用库中 totalized inverse 偷换。

这里的“线性等距”是从内积 `<u,v>_H=u^T H v` 的加权空间到 EuclideanSpace 的等距，
不是标准 Euclidean 三空间自身的正交变换，更不是裸 `Fin 3 -> Real` 的默认 Pi/sup 范数等距。
实际接线只需上述有限 `sq` 等式和线性，不必先实现整个 `LinearIsometryEquiv` 类型。
若使用 Cholesky `M=C C^T`，正确变换是 `C^-1 v`；不能一般地换成 `C^-T v`。

## 3. 到 generic allocation 的唯一必要接线

对同一 source state x，必须先得到 `l_total(x)=ell(x)+r(x)`。然后同时设置

```text
n=3, ell_generic=T(ell(x)), r_generic=T(r(x)), base=beta_C(x),
W(x) >= r(x)^T H r(x), lambda>1,
H_generic=(lambda-1)*(beta_C(x)-target-lambda*W(x))
          -lambda*sq(T(ell(x))) >= 0.
```

调用现有 `combined_of_port_budget`，再用 T 的线性和 metric equality 改写其结论，恰好得到

```text
target <= beta_C(x) - l_total(x)^T H l_total(x).
```

同理，已有 `relaxed_target_le_exact_total` 的数学接口运输后是

```text
beta_C-lambda*W-lambda/(lambda-1)*ell^T H ell
  <= beta_C-l_total^T H l_total.
```

这里只实例化 generic 结论，不另推一遍 Schur。exact direct target 自身不需要 W/lambda；
它们仅在选择这个充分 relaxation 时出现，不能在 exact total 平方之外再扣一笔外部 port charge。
若还要连到其他 margin，另需同一 normalization/domain 的 lower comparison。

匹配的外部列是 `routeB_compact_block456_port_bi_partition_probe.jl` 的 `rho2_m0_upper`：
代码对 `Mzero[C,C]` 做 interval Cholesky，并计算 `C0^-1 R B_up^-1/2` 的 bound。
其预期 contract 正是 `r^T H r <= rho_m0²*a_C^T B_up a_C`，因此可令右端为 W。
原 `rho2_upper` 控制 Euclidean port，`rho2_bchol_upper` 控制另一 metric；不可按同维度替换。
这些是读取到的 producer 语义与候选列，未在本轮执行 interval 计算、证明向外舍入或认证覆盖。
尤其需要源 reference `Mzero[C,C]` 与上面 exact M 同一 regularizer、origin 和排列的证明。

## 4. 最小 obstruction：哪些替换绝对不成立

以下向量都是接口测试向量，不声称对应 robot 可达状态。

1. **SPD 不允许忽略 metric。** 对当前 H，v=(1,0,0), beta_C=2，Euclidean target 为 1>0，
   实际 target 为 `-40002199994/5000400003<0`。换成 I 会制造错误正结论。
2. **保留三个对角项仍不够。** v=(1,0,-1), beta_C=90 时，删掉 H46/H64 的 target 为
   `50030000270/5000400003>0`；保留真实交叉项则为 `-49969999730/5000400003<0`。
3. **invertible 或 det>0 不等于可 whitening。** 抽象 M=diag(-1,-1,1) 可逆且 det=1，但
   e1^T M^-1 e1=-1，不可能等于任何实 Euclidean square。这隔离 SPD/PSD 的必要角色。
4. **同为三维的全有理 whitening 不存在。** 若 T 是有理 3×3 且 T^T T=H，则 det(H) 必为
   有理数平方。但当前 `det(H)=4000000000000000000/334591765400739`，分子为 2000000000²，
   分母满足 `18291849²=334591739838801 < 334591765400739 < 334591776422500=18291850²`。
   因此不能要求这个 T 的所有系数仍是有理数。

第 4 点不阻止实数 T，不阻止上述有理加权平方分解，也不排除升维的有理矩形 Gram 因子。
它只否定“保持三维且所有 whitening 系数有理”。若 SOS/系数后端必须全有理，最小实际选择是
保留 H 或上述正有理权重的平方形式；要直接调用当前 Euclidean generic theorem，则接受三个
可精确表示的实数平方根及其证明。不要为了硬套同维有理 map 而丢失 4–6 耦合。

## 5. 当前能闭合什么，仍缺什么

此研究已经给出固定 CSV 模型下 explicit inverse、SPD/LDL 的精确数值见证和线性 map 公式。
所以把瓶颈笼统写成“dense metric 无法处理”已不准确。尚未闭合的是以下可区分的证明义务：

- **Coefficient/source reification：** 将 num/den、原点 substitution、mu 与 C 排列绑定到实际
  source `M0_CC` 的 Lean 常量；有理计算的结果不能替代该桥。
- **Source total equality：** descriptor `total_eq456` 是 `lT-lBase-rC` 的约束表达式，不自动证明
  执行 source 在域内满足它。控制器、mass/reference、FD/solve defect 的归属仍需明确。
- **Matching-metric port cap：** 必须是本 H 和同一个 r，而不是二维 r_B、零缺陷模型外推或别的 norm。
  若只持有 Euclidean cap，可用另证的 `H<=kappa*I` 放大为 W，但这会损失锐度且不再是 exact equality。
- **Target allocation/domain：** metric 等式不证明 beta_C 足够大。当前 source 的 betaC456 是
  residual-Schur audit 中选定的模板；它及所有 cap/normalization 必须在同一域上有效。
- **Pinned elaboration：** generic helper 与新 metric identity 的实际 Lean 结果、import/axiom/source/olean
  receipt 尚未由本轮提供。即使这一有限维桥编译成功，source/coverage/registry 仍是独立 gate。

静态接口附注：所检查 generic 文件的 `relaxed_target_le_exact_total` 最后把 `hzero : H_generic=0`
直接传给要求 `0<=H_generic` 的参数（当前行 104–106）。这是可见的 proof-type mismatch，应由其
所属 Lean lane 将 equality 转成 inequality，例如 `le_of_eq hzero.symm`。这是源码审阅发现，
不是本轮运行得到的 Lean 诊断；本任务没有修改 generic 文件。

## 6. 定向检查与文件身份

仅执行 shell 读取、内存内 SymPy/Fraction 精确计算：CSV 原点的 C×C 求和、加 mu、M/H 对称性、
`M*H=I`、LDL/正主元、加权平方恒等式、两个当前 H 的反例，以及 determinant 非平方整数夹逼。
检查均返回退出码 0；不解析 Lean、不执行 Julia source、不证明可达性或 interval correctness。
本 review 的 front matter/写入范围另做静态核对，不作为 theorem receipt。

| 输入 | SHA-256 |
|---|---|
| GenericSchurAllocation Lean | `A73DB0939F2AEAA3BF72ED141F9FA41741D76DC4387F7195209D4B90411845A7` |
| mass polynomial CSV | `1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451` |
| block456 descriptor source | `9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79` |
| block456 residual Schur source | `3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98` |
| block456 interval port source | `62DF8B89F8025081DBA985C35863C6F427DDE71C225F50E1DBA949F0F60BF129` |

inspected_commit 是工作区基线快照；上表绑定实际读取字节，外部 source 不宣称属于该 Git commit。
后续最小 pinned receipt：精确 Lean/Mathlib pin 与依赖闭包、上述 coefficient bridge/有限矩阵等式/
三项 sqrt identity/线性与 sq transport 的完整日志和退出码、全部 axiom 输出及 source/olean 哈希。
结果保持 pending；本 review 不授权任何 registry promotion。
