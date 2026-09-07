# P4：ordered block Schur elimination 与 forcing/defect seam

日期：2026-09-07。仅新增 `NEW_P4_032_SchurElimination.lean` 与本 review。
状态：**未编译的 source-independent Lean skeleton**。未运行 Lean/Lake，未修改旧文件、
state、registry 或共享脚本；不涉及 defect norm 或 quadratic load。

## 核心身份

复用已有 block projection，物理顺序 B=(4,5)、D=(1,2,3,6)，内部索引
bIdx=[3,4]、dIdx=[0,1,2,5]。定义：

```text
T = MBD*MDDinv : 2×4，
Schur = MBB−MBD*(MDDinv*MDB) : 2×2，
eliminate(x) = projB(x)−T*projD(x)。
```

`schur_projection_identity` 仅在显式 `MDDinv*MDD=I` 前提下给出：

```text
projB(M*a)−(MBD*MDDinv)*projD(M*a) = Schur*projB(a)。
```

证明脚本先使用已有 D-row projection 展开被消元项，将
`(MBD*MDDinv)*MDD` 按结合律变成 `MBD*(MDDinv*MDD)=MBD`，
再使用 B-row projection 消去相同的 `MBD*aD` 项。
`schur_projection_left_associated` 另给用户通常写法
`(MBB−MBD*MDDinv*MDB)*projB(a)`，只通过结合律转换括号。

矩阵乘法从不交换因子。只用左逆，不构造 inverse，不要求右逆、对称、PSD、
正定性或 Schur 可逆性。因此该结果是消元身份，不是唯一求解或正性定理。

## Forcing 与 defect 的符号

`forcing_with_defect` 接受显式完整 balance `M*a=F+e`，输出：

```text
Schur*aB = (FB−T*FD) + (eB−T*eD)，
FB=projB(F)，FD=projD(F)，eB=projB(e)，eD=projD(e)。
```

`block_forcing_with_defects` 不要求构造完整六向量 forcing，而直接接受：

```text
MBB*aB+MBD*aD=FB+eB，
MDD*aD+MDB*aB=FD+eD。
```

它给出同一个结论，两个 defect 均保留。注意这里 force-side 加性 defect 的
condensed 项是 **eB−T*eD**。前轮 O1 使用另一套定义
`MDD*delta_a_D+DeltaMDB*aB=eD`、`rB−MBD*delta_a_D=eB`，因而出现
`rB=Rport*aB+T*eD+eB`。不能仅凭相同的 eD/eB 名称互换这两种符号约定。

`forcing_identity` 是显式 exact balance `M*a=F` 下的无 defect 推论。
`canonical_forcing_defect` 则总可以取代数表达式 `e=M*a−F`，保留
`Schur*aB=eliminate(F)+eliminate(e)`；这不证明或估计任何部署求解误差。

## 剩余前提与边界

- 本文件及所导入的 BlockDefects skeleton 尚需 elaboration/kernel、公理检查。
  末尾 `#print axioms` 未执行，本轮没有 Lean compile 声明。
- 实际 M、a、F、defect 与六轴 source 顺序和 generalized-force normalization 的身份。
  这里没有新增 normalization，也没有把 residual 重新归一化一次。
- 精确左逆证明；近似逆不能替代，存在 inverse defect 时需另加其传播项。
- 若使用 forcing 版本，须证明相应精确 balance；Float64 backslash 不是该前提的证明。
- 实际 defects 的界、source-domain/coverage、后续 Schur 可逆性或 PSD、ODE/flowpipe
  与 admission 均在本任务之外。本轮没有从身份推出这些性质。
