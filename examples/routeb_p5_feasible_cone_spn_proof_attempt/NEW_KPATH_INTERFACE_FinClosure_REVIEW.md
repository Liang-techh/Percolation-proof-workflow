# P5 K_path：Fin 索引与代表 SPN 的 typed closure skeleton

日期：2026-09-07。状态：**未编译、未运行 Lean/Lake 的 source-independent 候选**。
仅新增 `NEW_KPATH_INTERFACE_FinClosure.lean` 和本 review；未改旧 checker、旧接口、
state、registry 或共享脚本，未重审/重跑旧 checker，未实例化 concrete K/source 数据。

## 本轮补上的类型连接

1. `slotEquiv : Fin 8 ≃ Fin 2 × Fin 4`。固定 row-major 次序：
   `(r4,x4),(r4,x5),(r4,y4),(r4,y5),(r5,x4),(r5,x5),(r5,y4),(r5,y5)`。
   `encode(a,j)=4*a+j`，附双逆证明脚本；`sum_slots` 保留每项一次，不按数值去重。
2. `EightComparisons` 收纳两张 `Fin 8 → ℚ` 表、两组非负证明及全部 8 项比较证明。
   `SlotBinding K G` 要求两组精确实数身份，将这些槽绑定到实际 `K.value/G.value`。
   `toRationalBinding` 接到上一轮 `ExactComparisonBinding`，再得到 2×4 `ComponentLE`。
3. `slotSlack` 固定为
   `|Lz[a]|*(G[a,j]-K[a,j])*|z[j]|`；分别给出每项非负、8 项求和等于 envelope 差、
   该差非负的证明脚本。这里没有 H_gap 矩阵条目的序判断。
4. `allConeWitnesses` 调用现有 `liftSPN`，利用同一个 H 的 `flip_eq` 从 18 个代表
   提升到全部 36 个标签。`every_cone_nonnegative` 调用既有 SPN 非负项求和定理，
   得到每个锥、每个 `u≥0` 的二次型非负。
5. `typed_spn_power` 汇合上述输入；`path_spn_power` 进一步把 K 在类型上固定为
   `transportedGain A Hjac Scoord path.hH path.hS`，直接消费既有 `PathBinding`。

预定最终结论仅是：对提供了 `hx : D x` 的同一个使用点，

```text
|(L z(x))ᵀ rc(x)| ≤ mu Q(z(x)).
```

没有从此推出轨迹、衰减或任何 source/coverage/P8/M4 closure。

## 重数保持的精确范围

8 个 gain 条目槽与锥索引是两套独立索引。`cone_slot_counts` 的候选计数为
`36*8=288` 和 `18*8=144`；后者仍需要保留代表与反号两个方向。

`cone_slot_sum_preserving` 对任意 `w(c,s)` 复用现有重数保持求和接口：

```text
Σc Σs w(c,s) = Σr (Σs w(rep(r),s) + Σs w(flip(rep(r)),s)).
```

只有另外提供逐槽 `w(flip(c),s)=w(c,s)` 时，`cone_slot_sum_invariant` 才化成
每个代表的二倍权重。不会按相等的 gain、H 或 S/N 值去重；全零或特化重合不改变计数。
此求和恒等式是重编号结论，**不能用“所有锥之和非负”替代“每个锥非负”**。
证书提升只要求 H 的反号身份，不宣称不同代表的 S/N 数据相同或具有唯一标准形式。

## 精确剩余前提

- **Checker 到 proof 的桥接**：对实际导入的同一份 canonical rational 数据，构造
  `EightComparisons` 中的 16 项非负证明和 8 项比较证明，证明 JSON 行/列与上述
  `encode/decode` 对齐。原 checker 的 pass、整数交叉差报告和 digest 都不是 Lean
  proof term。本轮没有实现或认证 parser/reflection 的正确性。
- **两组实数表身份**：全部 8 项 `K.value[a,j]=↑path[encode(a,j)]` 和全部 8 项
  `G.value[a,j]=↑cert[encode(a,j)]`。前者涉及实际 pathK 的有限求和、abs、cast 以及
  实数 A/Hjac/Scoord 与有理输入的绑定；后者必须识别未来 SPN 真正消费的同一个 G。
  不接受近似、容差、标量范数或把有理上界冒充等式。
- **源侧同域输入**：`PathBinding D z rc A Hjac Scoord`，包括非负 Hjac/Scoord、
  各段状态位移界、残差增量界及同一增量之和经过一次 A 映射的 `force_eq`。
  路径覆盖/FTOC/归一化和实际 source 识别仍在上游；或者由上游直接提供
  `ComponentBinding D z rc K`。使用点仍必须另给 `hx : D x`。
- **Gap 与证书**：同一个 G、Q、mu 的 `ConeGapBinding`，包含每个锥的精确 gap
  身份与 H 的全局反号等式；以及全部 18 个代表的 `SPNWitness`（精确 H=S+N、
  S 全空间二次型非负、N 逐项非负）。没有提供冻结 Q/H 实例或任何具体 SPN 数据。
- **编译与公理检查**：本文件及上一轮 `RationalBinding.lean` 尚需授权环境中的
  elaboration/kernel 检查。文件末尾 `#print axioms` 只是将来要执行的命令，当前没有
  输出或 receipt。需隔离同名 `P5FeasibleConeSPN` 模块，明确选择
  `examples/routeb_p5_feasible_cone_spn_lean/` 的通用 sidecar，不能盲目导入本目录旧 proof attempt。

本轮只作源码层面的接口检查和依赖声明核对，未运行 Lean/Lake，也未生成 olean。
没有 `LEAN_VERIFIED`、kernel PASS、registry eligibility 或具体系统证明声明。
