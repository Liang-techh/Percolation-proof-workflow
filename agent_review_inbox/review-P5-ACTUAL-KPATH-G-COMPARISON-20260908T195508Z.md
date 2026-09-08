---
kind: review_result
review_id: review-P5-ACTUAL-KPATH-G-COMPARISON-20260908T195508Z
task_id: P5-ACTUAL-KPATH-G-COMPARISON-20260908
source_agent: Codex-actual-kpath-comparison
created_at: 2026-09-08T19:55:08Z
inspected_commit: ad5f9de1593dedac3b969cd6ab4f3eb8bdad3e78
status: ACTUAL_COMPONENT_GAIN_INPUT_ABSENT_IN_INSPECTED_SOURCES
integration_status: pending
admission_label: pending
actual_K_path_found: false
actual_G_family_found: false
actual_comparison_entries_checked: 0
actual_labels_discharged: 0
source_binding_proven: false
lean_run: false
lake_run: false
producer_run: false
registry_promoted: false
formal_certificate_allowed: false
P5_closed: false
---

# Actual block-(4,5) comparison：缺的是 gain 输入，不是八次有理比较

## 最小结论

当前实际 descriptor source **不是**空白：有 2×4 的 MBD(q)、两分量 rB 与 nominal
residual 的精确公式。但 **MBD 的四列是 distal acceleration corrections
(1,2,3,6)，不是 (x4,x5,y4,y5)**。不存在按形状直接把 MBD 填入 K_path 的合法接线。

所查源及数据没有供给同一 centered residual 的 A/Hjac/Scoord 或八项精确 gain，
也未找到可与其同域/同归一化配对的非 toy G/certificate family。
因此八个 inequality 均为 UNKNOWN，实际比较完成数 0，实际 36-label discharge 数 0。
这不是 K_path > G 的反例，也不是声称整个磁盘上不存在任何其他命名的数据。

本轮只新增本 immutable review；未改旧文件、state、registry、shared scripts，
未执行 Lean/Lake、Julia producer、Python checker、采样或回归。

## 1. 实际 source 定位：两个容易混淆的 2×4

外部根 E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`。
S = E/routeB_compact_direct_descriptor_structure.jl。

S:32–38 固定 Julia 1-based BIDX=[4,5]、DIDX=[1,2,3,6]、
mass regularizer = 1/1000000，nominal M0BB 对角值为
350003/3000000 与 200739/4000000。
它们不是 IVAL[4]=1/5、IVAL[5]=1/10，更不是 consumer 的 gain。

S:70–91 的公式是：

```text
MDD(q) v + DeltaMDB(q) aB = 0,
rB = MBD(q) v,
lBase = diag(1/5,1/10) fB - diag(M0BB_CONST) aB,
lTotal = lBase + rB.
```

其中 v 是 nominal-subtracted distal correction，不是完整 actual acceleration。
从第一式消去 v 还要同域 MDD 可逆，才能得
`rB = -MBD MDD^{-1} DeltaMDB aB`。
即使此式成立，它仍是 **block acceleration → generalized force** 的映射，
不是四个 P5 state coordinates → centered generalized force 的界。
缺少 actual graph 上 aB 的导数/增量与 z 的关系，不能直接读出八项 K。

`NEW_P4_032_BlockDefects.lean:full_equations_to_port` 还显式保留
canonicalDistalDefect 与 eB：

```text
rB = Rport aB + MBD MDD^{-1} eD + eB.
```

不能把 S 的零 defect nominal equation 当作全 source 的 eD=eB=0 证明。
更不能仅从 remote rB 的界推得 lTotal 的界，漏掉 lBase 或实际其他残差。

S 的默认 controller_branch 是 fourier；已存 `_structure_dh.csv` 前几行指定 dh
和 damping (13/10,11/10,19/20,4/5,13/20,1/2)。故不能只 hash S 而省略实际分支。
另一个实际 DH/FD 路径 E/routeB_descriptor_residual_interface.jl:36–55 定义
`a=M(q)^{-1}rhs`、`l=diag(IVAL_B)fB-M0_BB aB`，随后做随机样本 semantic regression。
其 CSV 不提供导数上界，不能转作 rational K_path 或同源解析路径证据。

## 2. 八项精确 comparison 与索引：全部保持缺失

consumer 的 row-major `Slot=Fin 8` 为 s=4a+k。
force 行是 human joints 4、5（full-state Lean zero-based joints 3、4），
state 列是数学 z=(x4,x5,y4,y5)，**不是** distal joints，也不默认等于未经缩放的 q/dq。

| slot | (a,k) | force/state 项 | 必需精确不等式 | 当前 K / G / slack |
|---|---|---|---|---|
| 0 | (0,0) | r4 / x4 | K4x4 ≤ G4x4 | missing / missing / unknown |
| 1 | (0,1) | r4 / x5 | K4x5 ≤ G4x5 | missing / missing / unknown |
| 2 | (0,2) | r4 / y4 | K4y4 ≤ G4y4 | missing / missing / unknown |
| 3 | (0,3) | r4 / y5 | K4y5 ≤ G4y5 | missing / missing / unknown |
| 4 | (1,0) | r5 / x4 | K5x4 ≤ G5x4 | missing / missing / unknown |
| 5 | (1,1) | r5 / x5 | K5x5 ≤ G5x5 | missing / missing / unknown |
| 6 | (1,2) | r5 / y4 | K5y4 ≤ G5y4 | missing / missing / unknown |
| 7 | (1,3) | r5 / y5 | K5y5 ≤ G5y5 | missing / missing / unknown |

给定实际有理表后，每项必须同时满足：

```text
K[a,k] = sum_{s,i,j} |A[a,i]| Hjac[s,i,j] Scoord[s,j,k],
K[a,k]=p[a,k]/q[a,k], G[a,k]=n[a,k]/d[a,k],
p,n >= 0; q,d > 0;
n[a,k]*q[a,k] - p[a,k]*d[a,k] >= 0.
slack[a,k] = (n*q-p*d)/(d*q).
```

这给出八次 exact/rational 比较的确定格式，**不是已填值或已通过的不等式**。
若上游只能提供 rational upper envelopes 而不是真实表的 exact casts，应先证明
`K_real ≤ Khat` 再比较 Khat≤G；不得伪造 SlotBinding.path_entry_eq 的等式。

现有 Comparison.py:126–181 已实现上述 identity 与 cross-difference 检查，但
只接受 source-independent-unbound，未认证 actual source。缺表时不能运行空/零表，
也不能将一个通过的旧 schema output 改标签为 source-bound。

## 3. Units、中心化、归一化：最早的语义阻碍

从运算维数可推断（不是 SI provenance 认证）：MBD 的单位是 force/acceleration，
K[a,k] 与 G[a,k] 必须是 **所选 generalized-force channel 单位 / 所选 z[k] 单位**。
因此 MBD 的数值/单位均不能通过把列重命名变成 K。
Hjac 的单位为 increment-output/increment-coordinate，Scoord 为
increment-coordinate/z[k]；三因子相乘必须回到 force/z[k]。

consumer 固定 `Lz=(x4+y4,x5+y5)`。若将 x 解释为角度、y 解释为角速度，
需要明确时间尺度/坐标变换使这个加法及 power pairing 与实际 Vdot 一致；
目前接口只给 ℝ，没有这些物理尺度。S:174 的实际示例 covector 是
`rt[i]=Vdv[i]/M0BB_CONST[i]`，且该 storage 明示只是暴露 Lie 缺项的 template。
没有 `rt=Lz` 或选定 P5 storage 的 source equality，不能自动复用其 residual pairing。

对 RawPMIForce，现有 typed adapter 只规定一次 diag(1/5,1/10) 转换。
已是 MBD*v 或 IVAL*f-M0*a 的 generalized force 不应再乘这一次转换。
这两个 IVAL 因子也不是 M0BB 或 mass regularizer；不能混用三者。

更早的必要条件是选定 rc：`ComponentBinding.zero_at_origin` 要求每一个 x∈D
只要 z(x)=0 就有 rc(x)=0。local 四坐标为零并不在已查接口中强制远端状态、w、
FD remainder 或 acceleration correction 为零。source 并未给出所需消失定理。
合法的候选构造是固定其余 source witness η，设
`rc(η,z)=F_B(η,z)-F_B(η,0)`，把 F_B(η,0) 放入独立 bias ledger。
这要求先选择 F_B 是完整 residual 还是单个 port，以及证明同域 anchor 可用。
没有这些选择，纯齐次八项表的对象尚未确定；本轮不宣称已找到非零 anchor 反例。

## 4. 36-label consumer：确定映射，不假装 discharge

六种每通道闭锥标签按 (x,y,x+y) 的符号细分，IDs 顺序：
0=pp，1=nn，2=pnPos，3=pnNeg，4=npPos，5=npNeg。
ConeIndex=(c4,c5)∈{0..5}²；可按 label=6*c4+c5 枚举36项。
全局反号 rev=(1,0,5,4,3,2)，flip 同时作用两通道。
18 代表是 c4∈{0,2,3}、c5∈{0..5}；Lean Fin3 rank 0/1/2 对应 IDs 0/2/3。

每通道作用在 (x4,y4) 或 (x5,y5) 的正交象限参数上的 2×2 chart 为：

```text
0 [[ 1, 0],[ 0, 1]]    1 [[-1, 0],[ 0,-1]]
2 [[ 1, 1],[-1, 0]]    3 [[ 1, 0],[-1,-1]]
4 [[-1, 0],[ 1, 1]]    5 [[-1,-1],[ 1, 0]]
```

把它们按 z=(x4,x5,y4,y5)、u=(a4,a5,b4,b5) 嵌入同一 T_c。
对同一 actual K/G 的八项比较，任何标签 c、u≥0 的精确传播式是：

```text
E_G(T_c u)-E_K(T_c u)
 = sum_{a,k} |(L T_c u)[a]| (G[a,k]-K[a,k]) |(T_c u)[k]| >= 0.
```

所以无需36张不同的 K 表；但须保留36个 consumer 标签及同一 G 的 gap identity。
这里的 36×8=288 是标签化使用位置，不是已执行288次检查。
需要同一 μ、Q、T、L 下的 ConeGapBinding 和18份代表 SPNWitness，
用 H_flip=H 提升至36。矩阵恰好相同、边界点重叠或 gain 均匀都不能删掉标签。
该 gap 单调性仅是 u≥0 上的二次型序，不推出全空间 Loewner 序。

没有找到 actual G 的证书族，因此当前不能把这一传播式实例化为实际 source 结论。
已存 UpdatedToySPN JSON 明确 scope=source-independent-unbound；它被排除，
本 review 不取其任何 toy gain 数字充任上表 G。

## 5. 最小补交：只要三件，不先重跑18份 toy SPN

1. **选定对象的一条 source identity**：同域 actual residual F_B、中心化 rc、z 的
   exact normalization、anchor/bias 与 power pairing，包含 controller branch。
2. **真正缺失的八项输入**：该 rc 的 rational A/Hjac/Scoord 及同域 path witnesses，
   或对 actual gain 的 rational enclosure 与上界证明。一个可实现的导数入口是
   在已证明可逆且同域的 actual graph 上用
   `∂a = M^{-1}(∂R-(∂M)a)`，再对选定 F_B 求导和沿合法路径积分。
   M/M^{-1}、R/DR、域、路径/anchor、FD 与 bias 的正确处理仍是前提；
   不能仅用全局 MBD 幅值取代这些导数界。
3. **同一坐标的 G/certificate family**：真实选择的 G 八项值及 μ/Q/chart 身份，
   18个完整标签 SPN witness 与 flip/gap binding。随后只做八个 cross differences。

这是输入阻碍，不是再增加 Norm/PSD-capacity schema 能消除的障碍。
三件中任一缺失保持 pending；若日后实际 cross difference 为负，只否定该 envelope
comparison，不自动否定物理 P5。此 review 不请求 state 或 registry 状态变更。

## 6. 检索边界与 source hashes

本轮实际只读查阅上述 S、factorized model、DH/FD residual interface、typed
BlockDefects、KPath Core/Comparison/FinClosure、ConeIndex 与历史相关 review。
在 workspace artifacts/examples 的 JSON/CSV 中检索精确字段名
K_path/Hjac/Scoord/K_cert（排除 state、版本化 obligations、package-lock）返回0文件；
E 下 jl/csv/json/md 的相同关键词只命中无关设计/interval材料，未定位实际三表。
对 robot_formal_v1 的同字段检索亦未命中。文件枚举/字段缺失不证明全磁盘绝对不存在，
但已检查的实际 producer 不输出 consumer 所需 gain，这一接口缺口由其定义直接可见。

以下是本轮 Get-FileHash 得到的实际字节身份，不是数学/编译认证。
CSV 系数文件仅记录 producer 引用与散列，未重建全部系数恒等式。

| E 下文件 | SHA-256 |
|---|---|
| routeB_compact_direct_descriptor_structure.jl | 2c2f623f966425952cbbbd3c04bae84858147fe7fdd386f5bc5f4ff35e2fb98c |
| routeB_compact_direct_descriptor_structure_dh.csv | 2ff3a201f480dbf5c697dcee01ee5e6f42583f20bc33176a5bf95983c9128b39 |
| routeB_factorized_descriptor_model.jl | c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427 |
| routeB_analytic_mass_full_cs_polynomial.csv | 1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451 |
| routeB_analytic_coriolis_cs_polynomial.csv | cdc587afd26b2ab5498c5917e8c620e7c9aada8b2f5b4128c88df14e78b4e4bb |
| routeB_analytic_gravity_cs_polynomial.csv | 2760489cba6dc2f2d25ac8f33fa5a25e430bb92040c022004d1ef949d3e09c5d |
| routeB_descriptor_residual_interface.jl | d3d21705e5e904a080e4b86dc4c380788d2323c155570a8e7b40d62b11bb0a24 |
| dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |

下表均在 workspace examples/routeb_p5_feasible_cone_spn_proof_attempt：

| 文件 | SHA-256 |
|---|---|
| NEW_KPATH_INTERFACE_Core.lean | 10c7e769e772a2f4475def1eb061e52319510cb906cb879c4234653f2d64a17c |
| NEW_KPATH_INTERFACE_Comparison.py | d7dd1275a46bda19733d0d3e2700ca891f4759c918e62f786bd2a238f5c08392 |
| NEW_KPATH_INTERFACE_FinClosure.lean | 437b31f7a76f1fb134a07099effb5ec4667d861158af6d1702357e6090b43537 |
| NEW_CONE_INDEX_Core.lean | b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602 |
| NEW_P4_032_BlockDefects.lean | aa1cce18e39b1b675483c9ece7cecbc1a2740c65df1846582ca57963c0a6cc51 |
| NEW_KPATH_PACKET_UpdatedToySPN20260908.json (excluded toy) | 962b97fd8b9cb70c850face843a15ae20ee3166dee272f504ba0086998a1218b |

source hashes不替代同源等式，尤其 factorized/analytic/FD/Float64 分支不可混用。
本轮不运行任何 source producer，也不刷新历史 Lean/checker 报告。
