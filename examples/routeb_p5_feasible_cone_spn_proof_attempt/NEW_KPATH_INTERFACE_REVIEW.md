# P5-026：非负 componentwise H/K_path binding interface

日期：2026-09-07。范围：条件式、source-independent 的类型连接。

本轮将现有 piecewise path transport 的完整 2×4 矩阵，接到现有
36→18 cone-index 与通用 SPN consumer。新增的是输入契约及其组合定理，
没有给 concrete K_path 填入任何值，也没有搜索、生成或接受具体 SPN 表。

仅新增同目录文件：

- `NEW_KPATH_INTERFACE_Core.lean`：非负 gain、同域 residual binding、path adapter、H binding、18 代表 consumer。
- `NEW_KPATH_INTERFACE_check.py`：固定依赖映射及 SHA-256、只读 Lean source-bundle 检查、公理审计。
- `NEW_KPATH_INTERFACE_REVIEW.md`：本 review。

本任务未修改旧 P5 文件、state、registry、共享脚本、Lake 配置或其他 agent 文件；
未注册、提交、推送或触发 CI。工作树中的其他并发改动保留原状。

## 1. 最小消费契约

固定状态次序 `z=(x4,x5,y4,y5)`、力分量次序 `(4,5)`，
`Lz=(x4+y4,x5+y5)`。两张非负 2×4 矩阵分别记为 `K` 和 `G`：
`K` 是源侧分量界，`G=K_cert` 是实际接受 SPN 检查的上界矩阵。

| 输入 | Lean 契约 | 必须由谁提供 |
|---|---|---|
| 非负矩阵 | `NonnegativeGain` 的 `value` 与全部 8 个非负证明 | source/exporter |
| 同域分量界 | `ComponentBinding D z rc K`：`D x → |rc(x)[a]| ≤ Σj K[a,j]|z(x)[j]|` | source/path lane |
| 上界比较 | `ComponentLE K.value G.value`：全部 8 项 `K[a,j] ≤ G[a,j]` | exact comparison/exporter |
| 同一个 G 的锥 gap | `ConeGapBinding G Q mu` | sign-fixed algebra/exporter |
| 代表证书 | 每个 `r : RouteBP5ConeIndex.Representative` 的 `SPNWitness (gap.H (representativeCone r))` | exact SPN exporter |
| 使用点 | `x : X` 与 `hx : D x` | 下游使用者 |

`X` 可以携带时间、状态、参数、参考状态和路径见证；`D` 是整个见证上的谓词。
所有残差界与下游结论使用同一个 `x,z,rc,D`。命名 `D` 不证明它非空，
不证明任何实际 source 是这些函数，也不证明轨迹保持在 `D` 中。

主定理 `componentwise_spn_power` 证明：

```text
上述输入
  => 对每个 x∈D， |(L z(x))ᵀ rc(x)| ≤ mu Q(z(x)).
```

可以令 `G=K` 并提供逐项自反比较，因此上界表不是必需的第二份 source 数据。
若用有理表向上包络真实 gain，必须逐项证明 `K≤G`；浮点近似、矩阵范数比较、
`ell2` 比较或“数值足够接近”均不满足该参数类型。本轮没有这样的有理实例。

## 2. 比较方向和“最小”的精确含义

`row_mono`、`envelope_mono` 分别证明：

```text
K ≤ G componentwise
  => K[a,:]|z| ≤ G[a,:]|z|
  => |Lz|ᵀK|z| ≤ |Lz|ᵀG|z|.
```

`component_le_iff_rows` 还证明逐项序与“对所有实数 z、所有行 a 的 row envelope
比较”等价；逆向逐一代入坐标基向量。这说明逐项序是这个全状态、逐行比较接口
的精确条件。它不宣称是给定受限 source 域上的必要条件，也不宣称是仅比较
power envelope、copositivity 或存在 SPN 分解的必要条件。

如果 `bK,bG` 都绑定同一个 `Q,mu`，`cone_gap_antitone` 证明对 `u≥0`：

```text
uᵀ H_G(c) u ≤ uᵀ H_K(c) u.
```

所以认证较大的 `G` 足以消费较小的 `K`。这不是 `H_G≤H_K` 的逐项矩阵序，
也不是全空间 Loewner 序。定理不把 G 的 S/N 分解直接改名为 K 的分解，
而是通过 envelope 比较传递最终功率界。没有使用 Frobenius scalar collapse。

## 3. 从现有 Hjac/Scoord 到 K_path

这里明确区分两个不同的 H：

- `Hjac[s,i,j]≥0` 是各段增量/Jacobian budget；
- `ConeGapBinding.H[c]` 是 4×4 gap 矩阵，一般没有逐项非负要求。

`transportedGain` 直接调用现有 `RouteBP5PiecewiseTransport.pathK`：

```text
K_path[a,k] = Σs Σi Σj |A[a,i]| Hjac[s,i,j] Scoord[s,j,k].
```

其全部 8 项非负性由 `Hjac≥0`、`Scoord≥0` 和绝对值非负性证明。
没有新定义的数值 K_path，也没有对 `pathK` 公式作改写或标量替代。

`PathBinding` 要求同一个域见证 x 上满足：

```text
|dxi(x)[s,j]| ≤ Σk Scoord[s,j,k] |z(x)[k]|,
|de(x)[s,i]|  ≤ Σj Hjac[s,i,j] |dxi(x)[s,j]|,
rc(x)[a] = A(Σs de(x)[s,:])[a].
```

`PathBinding.toComponentBinding` 复用既有
`piecewise_component_transport` 和 `forceMap_piecewise_abs_le`，得到完整
`ComponentBinding D z rc (transportedGain ...)`。随后把这个结果直接传入
`componentwise_spn_power` 即可。这是类型层面的调用，不是对旧代码公式的文本类比。

输入表 A/Hjac/Scoord 在该接口中固定，对 D 内所有 x 有效。若上游使用依点或
依路径变化的表，需要逐点实例化此条件定理，或者先提供同域统一上界；本轮不推断
统一性。路径表的来源、每段连接性、FTOC 前提以及真实端点 telescoping 仍须在
source lane 证明。`force_eq` 把已 telescoping 的结果作为显式前提，并不代替这些证明。

A 只应用一次。原始 PMI 力坐标到 consumer 广义力的转换必须在 A 或更上游完成，
已经归一化的 `forceError` 不能再乘一次惯量。共同 ramp 参数时，实际零位移的
w/c 行应在 Scoord 中为零；参数不匹配需要独立、已证明的位移比较，不能仅凭
Jacobian 灵敏度大就向 K_path 收费。本轮没有实例化 A 或这些坐标绑定。

## 4. 与现有 36→18/SPN 的实际连接

`ConeGapBinding G Q mu` 携带完整 36 个索引的 H 和两条证明：

```text
H(flip c) = H(c),
mu Q(chart(c,u)) - |L chart(c,u)|ᵀG|chart(c,u)| = uᵀH(c)u,  u≥0.
```

G 是该结构的类型参数；证书又以同一个结构中的 `H` 为索引，因此不允许将另一张
gain 表或另一个 H 的证书无证明地套入。H 的全局反号不变性不能从锥标签推断，
必须提供 `flip_eq`。Q 和 mu 对所有锥相同。

`liftSPN` 实际调用现有 `RouteBP5ConeIndex.liftFamily`，保留 36 个索引并从
18 个代表取得证书；`direct_envelope` 实际调用通用 sidecar 的
`global_abs_envelope_of_spn`，其覆盖前提由现有 `RouteBP5ConeIndex.cone_cover` 提供。
没有按特化后的矩阵值去重，也没有丢掉边界上的多重锥见证。

最小 `SPNWitness` 含 S/N、逐项 `H=S+N`、`∀v,0≤vᵀSv`、逐项 `N≥0`。
这恰好是既有通用 consumer 所需前提；对称性可由 exact exporter 额外要求，
本接口没有修改或放宽旧 rational certificate 文件格式。矩阵分解的数据与这些证明
均由调用者提供，Lean 不执行 certificate search。

本轮没有复核或导入同目录的旧 `P5FeasibleConeSPN.lean` proof attempt。
也没有实例化其冻结 P 对应的 Q、其具体 H 构造或 sign-fixed 恒等式。
应用到该冻结 block45 模型时，仍须提交该 Q 的精确识别及 `ConeGapBinding` 实例。
任意 Q 的条件定理本身不是冻结物理耗散形式的绑定证据。

## 5. Bias 与结论边界

`ComponentBinding.zero_at_origin` 证明：在 D 内，若 z(x)=0，则 rc(x)=0。
这给出排除隐藏 additive offset 的普遍实数定理；若 residual 在原点有非零缺陷，
任何有限 homogeneous K 都无法满足该 binding。单独的 IEEE、求解器或控制器
不连续误差不能仅靠对理想实数映射求导放进 Hjac/K_path。

`pointwise_ledger` 只在额外提供

```text
Vdot ≤ -Q(z) + (Lz)ᵀrc + biasPower
```

时推出 `Vdot ≤ -(1-mu)Q(z)+biasPower`。biasPower 保留在结论中；取零也需要
调用者使该前提成立。代数 consumer 本身不需要 mu≥0 或 mu<1；若要进一步给出
衰减结论，仍需严格余量、正定度量、实际 Vdot 身份和轨迹/continuation 桥接。

## 6. 验证方法与复现

验证只针对新增接口及它实际消费的固定依赖。仓库有两个同名、同 namespace 的
`P5FeasibleConeSPN.lean`，因此不能从当前目录盲目按同名模块加载。
检查器固定映射到 **通用 sidecar**，先核对三个依赖的 SHA-256，再将 Mathlib imports
置顶、原声明体按依赖顺序组装，最后附加新接口，通过 `lean --stdin` 检查。
它不修改旧源码，不生成临时源文件、olean、缓存、日志或 receipt。

这是同一 Lean 环境内、现有声明到新增声明的实际类型检查及 kernel 证明检查，
不是字符串公式比较。它仍不等同于独立 Lake module import/build：
`module_import_build_verified=false`。日后接入正式模块构建必须显式隔离同名文件。

从仓库根目录运行：

```powershell
python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_check.py
```

可加 `--emit-source` 仅向 stdout 输出待检查的完整 source bundle；
可加 `--lean <Lean-4.32.0-executable>` 指定可执行文件。依赖缓存来自现有
`examples/local_fkg/.lake/packages/*/.lake/build/lib/lean`，没有安装或重建缓存。
当前 Mathlib checkout HEAD 为 `81a5d257c8e410db227a6665ed08f64fea08e997`；
本轮未独立重建/审计所有缓存的来源。

固定依赖 SHA-256：

```text
NEW_CONE_INDEX_Core.lean
b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602
../routeb_p5_feasible_cone_spn_lean/P5FeasibleConeSPN.lean
8a2206d22747bc7c24be65e2d87b31fc23f94e769525a62aabad97326e5385e7
../routeb_p5_piecewise_transport_lean/P5PiecewiseTransport.lean
c445e4110584c5c536f023ad08b2a8c5eccef21fc9b97aa363f24e0a9ae95208
```

检查器拒绝依赖变化、非预期 import、错误工具链、Lean error/warning、sorryAx、
缺失公理输出或非标准额外公理，并在结束前重新核对输入，防止并发改动产生旧版本
成功报告。stdout 提供当前 Core 和整个 source bundle 的 SHA-256。

最终运行：上述命令 exit 0；Lean 4.32.0 exit 0，无 error/warning。
12 个新增公开接口的 `#print axioms` 均且仅为
`[propext, Classical.choice, Quot.sound]`，无 `sorryAx` 或额外公理。
两个既有通用 SPN/piecewise sidecar 也在本轮直接只读运行通过；
同目录旧 proof attempt 没有被检查或升级。

```text
NEW_KPATH_INTERFACE_Core.lean SHA-256
10c7e769e772a2f4475def1eb061e52319510cb906cb879c4234653f2d64a17c
实际通过检查的 UTF-8 source bundle SHA-256
16f022af31c24a86d91a54371977e7728f08e800dbd19d0cddb87f9d6a759abc
```

该记录是本轮本地 source-bundle 验证说明，不是 source/admission receipt，
也不是正式模块构建或 registry promotion。

## 7. 保持开放的上游输入

没有 concrete K_path、真实 source residual/归一化映射、Hjac calculus、完整路径覆盖、
同域 P8/first-exit 证明、具体冻结 Q/H 实例或 18 份 source-bound SPN 数据。
没有 ODE continuation、source/coverage/P8/M4 closure 或 registry admission。

所有成功报告仍明确：

```text
concrete_K_path_bound=false
concrete_H_gap_instantiated=false
concrete_spn_certificates_supplied=false
source_coverage_verified=false
registry_eligible=false
P5_P8_M4_closed=false
```

接口拒绝、缺少输入或 SPN 搜索失败均不是 copositivity 反例。
