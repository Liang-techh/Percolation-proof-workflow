---
kind: review_result
review_id: review-P5-CENTERED-ANCHOR-INSTANTIATION-20260908T200937Z
task_id: P5-CENTERED-ANCHOR-INSTANTIATION-20260908
source_agent: Codex-centered-anchor-source
created_at: 2026-09-08T20:09:37Z
inspected_commit: ce7163d1f6ca10435136894d4484ac78de1fb68d
status: CONDITIONAL_ANCHOR_CONSTRUCTED_REFERENCE_AND_SOURCE_REIFICATION_PENDING
integration_status: pending
admission_label: pending
pointwise_anchor_construction: conditional
actual_source_anchor_verified: false
source_binding_proven: false
lean_run: false
lake_run: false
producer_run: false
registry_promoted: false
formal_certificate_allowed: false
P5_closed: false
---

# Centering anchor：可以给出具体构造，但不能把 z=0 当作物理原点

## 判定

可以基于已定位的 Route-B residual evaluator 写出**条件式、同 context 的 anchor**，
不需要搜索 K_path 表，也不需要另猜 remote acceleration：替换 local position/velocity
为 nominal 值，保持其余独立变量，随后重新求解完整六维 acceleration graph。

关键修正：T-P5-018 定义 x=qB-qbarB、y=dqB-dqbarB，T-P5-022 沿用四维 consumer error。
所以 z=0 一般意味着 qB=qbarB、dqB=dqbarB，不意味着 qB=dqB=0。
物理置零只是 qbarB=dqbarB=0 的特例；不能由 global-origin G0 推出这个特例。
这也是前轮“stateMap 必须实例化”的具体内容，不是推翻原 contract。

本轮没有得到部署 Float64 source 的 anchor theorem。下面明确分开 source code 的
可调用构造、exact-real 重解释下的数学推导，以及仍需证明的实际 source/域接线。
只新增本 immutable review；未改 state/registry/shared scripts，未跑 Lean/Lake、
Julia producer、轨迹、采样或回归。没有再次检索 K_path 数表。

## 1. 实际 source：选定完整 residual evaluator，不用 compact remote port 替代

外部根 E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`。
S = E/routeB_descriptor_residual_interface.jl，L = E/dhport_lib.jl。

S:40–59 的 evaluate(q,dq,w) 实际执行：

```text
(M,Cdq,G) := arm_MCG(q,dq)
tau := -KP*q -(KD+b_fr)*dq + G0 +(GW .* IVAL)*w
R := tau-Cdq-G
a := M \ R
l := diag(IVAL[4],IVAL[5])*nominal_f(q,dq,w)[4:5] - Mref*a[4:5]
```

Mref 是 S:22–23 读取 E/routeB_Mq_M0.csv 后取其 (4,4)、(5,5) 的对角矩阵。
它不是当点 MBB(q)，也不由本轮改成 exactized rational nominal matrix。
`nominal_f` 的 block 分量只依赖 local qB/dqB 与 w，含 cross-coupling KC=0.05。
上述 l 是此 evaluator 的完整 block residual；不是 compact source 的单个 rB=MBD*v。

L:102–109 的 exact_ddq 同样是 Float64 M\R 算法，函数名 exact 不代表 exact arithmetic。
S 使用自身 KP/KD/IVAL/GW 与库中的 b_fr/mgl，不能仅因数组看似相同就更换调用路径。
推荐以 S.evaluate 的表达式作为此 anchor 的同源定义，保持它的全部常量与依赖。

## 2. 具体 anchor 与保持/重算清单

给定同一时刻的 pointwise nominal block qbarB=(qbar4,qbar5)、vbarB=(vbar4,vbar5)，定义

```text
eta = (q1,q2,q3,q6, dq1,dq2,dq3,dq6,
       t,w, nominal qbarB,vbarB,lbar, fixed model/controller/semantics parameters)
z = (q4-qbar4, q5-qbar5, dq4-vbar4, dq5-vbar5)

qhat  = (q1,q2,q3,qbar4,qbar5,q6)
vhat  = (dq1,dq2,dq3,vbar4,vbar5,dq6)
Mhat,Chat,Ghat := arm_MCG(qhat,vhat; same semantics)
Rhat := -KP*qhat -(KD+b_fr)*vhat + G0 +(GW .* IVAL)*w - Chat-Ghat
ahat := unique solution of Mhat*ahat=Rhat          -- exact graph interpretation
lhat := diag(IVAL_B)*nominal_f(qhat,vhat,w)_B - Mref*ahat_B
```

这里所有下标均 human/Julia 1-based；B=(4,5)、D=(1,2,3,6)。

| 字段 | anchor 动作 |
|---|---|
| remote qD/dqD | 与 actual 完全相同；不改成 nominal remote state |
| qB/dqB | 改成指定 nominal block 值，不一般置零 |
| t、w、外部固定参数、nominal reference | 保持相同；若 w=c0*t，还保持同一 c0 |
| global reference G0、冻结 Mref、regularizer、FD step | 保持原定义/参数，不改成在 qhat 重新定义的 G0 或 reference mass |
| trigonometric lifts、frames、M、C、G、tau/R | 在 qhat/vhat 上重新计算；lifts 不能保持 actual 值 |
| 完整 aB 和 aD | 都需重新求解；不能只改 B 分量或保留 actual aD |
| path/Jacobian/FD error witness | 如后续要用，须对应新点；旧点 witness 不能自动搬用 |

这是 algebraic descriptor graph 上的 pointwise anchor，不要求 anchor 自身是某条
实际轨迹在时刻 t 的状态。若 D 原来仅是一个实际 flowpipe 的图，anchor 不一定在 D。
要使用前轮 anchorDomain/path contract，应证明合适的 bounding domain 同时包含
actual 与此 hybrid anchor；不能偷偷把“在 actual trajectory 上”当作保持条件。

给定 qbarB/vbarB 即可定义这个 pointwise 构造，不需要先证明 nominal ODE 存在。
但将它接回 P5 incremental dynamics，仍需 nominal trajectory/残差 lbar 的选定 source
及同 forcing 的方程。现有 T-P5-018 review 提供的是这个条件接口，不是实际轨迹数据。

## 3. Acceleration graph 的存在性：exact-real 有直接充分结构

L:46–60 的 mass_matrix 用正质量、正惯量构造 Gram 和，再加正 regularizer。
在该公式的 **exact-real 重解释** 下，对任何 h∈R6，

```text
h^T M(q) h
 = sum_link m_link ||Jv_link h||^2
 + sum_link (I_link/3) ||R_link^T Jw_link h||^2
 + mu_reg ||h||^2
 >= mu_reg ||h||^2.
```

只要 mu_reg>0，就有 M(q) 正定、唯一可逆，故任意 finite real qhat/vhat/w 都有唯一 ahat。
这里甚至不需要借旋转正交性消去 R：上述 Gram 写法本身足够。
因此在已证明 exact-real source reification 后，“anchor 需要求解完整 graph”不是
必须额外数值搜索的障碍；此 mass 结构直接给出存在唯一性。

当前库默认 mu_reg=1e-6、h_fd=1e-5。仅作本机 Python binary64 literal 的精确解码：

```text
mu_binary64 = 4722366482869645 / 4722366482869645213696 > 0
h_binary64  = 5902958103587057 / 590295810358705651712 > 0
```

这两个分数不是自动把 Julia 执行语义认证为 exact-real 的证据。
若选 decimal-rational idealization，可用 1/1000000 与 1/100000，
但它是另一个明确标注的理想模型，不能冒充实际 binary64 常量。
若选择 regularization=0，则不能使用上述严格正定结论，需另外证明可逆。

**Float64 边界：**实际 mass assembly、libm、FD、线性求解都有舍入。
exact-real Gram 下界不自动是已舍入 Mhat 的精确下界；M\R 的返回也不保证实数意义
Mahat=Rhat。有限性、可逆/solve success、solve defect 与 reification 仍待绑定。
本轮未执行两次 evaluate，未声称构造已在部署程序中成功运行。
FD 模型中的 centered differences 可以在 exact-real reification 下处理；
Float64 返回值 map 不可直接视为可微实函数。

## 4. fullForce / rc / bias 的实际源接线

此处用 l(X) 表示上面选定 S.evaluate 的 full residual 语义，并固定同一个 nominal
block residual lbar(t)（可以是假设给出的0，但不能未经证明设0）。
P5 incremental consumer 所需的是 **actual-minus-nominal** residual：

```text
fullForce(X) := l(X)-lbar(t)
rc(X)        := l(X)-lhat(X)
bias(X)      := lhat(X)-lbar(t)

fullForce(X) = rc(X)+bias(X).
```

这是一条确切的加减同项 identity，不要求 lhat=lbar，不要求 bias=0。
anchor 保持 nominal reference 与 eta，所以 fullForce(anchor X)=bias(X)。
在 exact graph、确定 source 函数和未缩放 error coordinates 下，z=0 时
qhat=q、vhat=dq；唯一性给 ahat=a，故 lhat=l、rc=0。
若 z 是缩放/仿射 error，需先给出相应零集等价；不能仅依据名字 x4/y4。

若把数值程序输出 lift 到实数，也可**定义**这些三个实数差得到 split identity；
但这不证明数值 fullForce 与理想 residual 相等，也不提供导数界或 graph equality。
零 fibre 还需同一规范输入/确定执行状态，不能用 Floats 的符号零等细节替代 source proof。

### 本次可直接缩减的 centered residual 表达式

在同一 exact-real 线性 nominal_f 解释下，记

```text
J=diag(IVAL_B)
Dnom=diag(KD4+b_fr4,KD5+b_fr5)
Bnom=[[KP4+mgl4, -IVAL4*KC],[-IVAL5*KC, KP5+mgl5]]
```

由于 local reference 的输入 w 与 actual 相同，J*nominal_f 的 forcing 差恰好消去，
得到

```text
rc = -Bnom*x - Dnom*y - Mref*(aB-ahatB).
bias = J*nominal_f(qhat,vhat,w)_B - Mref*ahatB - lbar.
```

这给真正 source gain 的明确下一个对象：**同 remote/context 下的
block acceleration difference aB-ahatB**，而非裸 MBD 或 remote correction v。
remote qD/dqD 虽保持不变，它们通过 Mhat/Rhat 与 ahat 影响 bias，不能删除。

在另行选定 exact decimal/rational DH nominal coefficients 时，Bnom/Dnom 可化为
前轮 P5 的有理矩阵；本 review 不把这个精确化直接赋予 Float64 S 的每一步运算。
Mref 的实际 CSV 对角 token 也不能自动替换成 350003/3000000 与 200739/4000000。
这两个 reference 的精确同一性/差额预算必须独立处理。

对于不减 nominal 的绝对 residual consumer，可以取 lbar=0 并解释 fullForce=l，
此时 bias=lhat；这不是证明当前 incremental nominal 残差为零。
无论哪条路线，signed power 分裂为 `(Lz)·rc+(Lz)·bias`。
中心化只保证 rc 在 error 零点消失，不给 bias 的任何上界或 P5 absorption。

## 5. 与旧 descriptor reference 的区别

旧 compact nominal-subtracted remote reference 以“同一个 aB”构造 vD，
目标是 MDD*vD+DeltaMDB*aB=0；它不是将 qB/dqB 换为 qbarB/vbarB 的 source graph。
本 anchor 一般改变 aB。不得强加 ahatB=aB，也不得认为 vD=aD-ahatD 自动成立。
如要在该 remote-port decomposition 内使用本 anchor，必须重新推导带 eD/eB 的
reference identity；本轮 full residual 路线无需先完成这个额外消元桥。

## 6. 最小剩余 obstruction 与已满足字段

本轮已从实际 source 找到：full residual 的具体 evaluator、六维重新求解位置、
所依赖的 Mref 文件和 semantics knobs；并给出精确理想公式下的 anchor 与 bias identity。
不是所有内容都仅停留在抽象变量名。

剩余最少三项：

1. **Reference/state identity**：为当前 P5 选择 actual nominal qbarB/vbarB/lbar，
   给出 z 的 error/scaling identity。数学 review 不是该 actual reference instance。
2. **Source interpretation bridge**：选定 S 的 numerical lift 或明确的 exact-real
   DH/FD reification，保留实际 Mref/常量/branch，并证明 source equality或显式误差分裂。
   exact-real Gram 可逆性推导不代替 Float64 solver/FD 证据。
3. **Anchor domain**：证明 hybrid anchor 在用于增量界的域内；后续若用导数积分，
   还需 actual↔anchor 的同域路径。只有实际时刻/flowpipe 成员条件不够。

不需要为了定义 anchor 保持完整 actual acceleration，不需要把远端坐标归零，
不需要先找到 K_path/G 或运行数值试探。上述三项齐备后才可合法导出 actual rc/bias
供后续 H bounds 使用；目前保持 pending，而非宣称 anchor 不存在。

## 7. 本轮 source hashes 与只读执行范围

W=`C:/Users/z5242/Desktop/重构版/工作流`。下列 SHA-256 本轮重新读取。

| 精确路径 | SHA-256 |
|---|---|
| E/routeB_descriptor_residual_interface.jl | d3d21705e5e904a080e4b86dc4c380788d2323c155570a8e7b40d62b11bb0a24 |
| E/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| E/routeB_Mq_M0.csv | 28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40 |
| E/routeB_compact_direct_descriptor_structure.jl | 2c2f623f966425952cbbbd3c04bae84858147fe7fdd386f5bc5f4ff35e2fb98c |
| W/agent_review_inbox/review-T-P5-018-guyuefangyuan-20260907T0634.md | af7492a242d4fadf9f95bbd677725cc65ef94478e6b7020c64496f5104a39270 |
| W/agent_review_inbox/review-P5-SOURCE-KPATH-REPAIR-BOUNDARY-20260908T200217Z.md | 81014b2eda017eea15a3c8adf39860163ea1c852f96b1102cd0e8b4d1769144f |

辅助阅读 T-P5-020/022/023 的 error/path 讨论以及 source export 的变量映射，
没有将它们或某个历史编译状态当作新的 source witness。
执行仅文本查阅、相关 state/reference 名称定位、hash/Git/时间读取，以及
Python Fraction 对两个 literal 的精确解码。无 K_path 数据搜索、Julia/Lean 执行、
闭合比较、认证 receipt 或 state/registry mutation。
