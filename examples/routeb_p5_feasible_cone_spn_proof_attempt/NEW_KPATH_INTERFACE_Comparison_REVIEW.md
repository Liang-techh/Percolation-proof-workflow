# P5-026：exact componentwise comparison contract/checker

日期：2026-09-07。结果：新增精确有理算术检查器及未编译的 typed seam。
本轮没有运行本机或远端 Lean/Lake，没有给 concrete K_path 赋值。

仅新增本目录四个文件，未修改之前的接口、旧 P5 文件、state、registry 或共享脚本：

- `NEW_KPATH_INTERFACE_Comparison.py`：只读输入，stdout 报告，失败 exit 1。
- `NEW_KPATH_INTERFACE_Comparison_test.py`：内存中的 synthetic arithmetic fixtures 和负控。
- `NEW_KPATH_INTERFACE_RationalBinding.lean`：**UNCOMPILED CANDIDATE**，有理表到实数 gain 的类型契约。
- `NEW_KPATH_INTERFACE_Comparison_REVIEW.md`：本 review。

## 1. 检查的恰好是哪两件事

对于输入的精确有理 A、非负 Hjac/Scoord、非负 K_path 和非负 K_cert，检查全部 8 项：

```text
K_path[a,k] = Σs Σi Σj |A[a,i]| Hjac[s,i,j] Scoord[s,j,k],
K_path[a,k] ≤ K_cert[a,k].
```

第一行使用现有 `RouteBP5PiecewiseTransport.pathK/segmentK` 的有限求和公式。
检查器不信任单独声明的 K_path 表，不接受缺失 A/Hjac/Scoord 后仅比较两张表。
第二行使用精确整数交叉乘法：若左边为 p/q，右边为 r/s（q,s>0），则检查
`r*q-p*s≥0`。不设 tolerance，不取 float，不运行 eigensolver，也不比较 ell2。

每个通过的条目输出行/列名称、左右有理数、精确 slack 和交叉差。
只有全部身份等式和逐项不等式成立后，才输出 `arithmetic_valid=true`。
中途失败不会输出部分成功表或可注册结果。

这只是**输入表的有理算术关系**。A/Hjac/Scoord 的源语义、同域界、路径连接性、
归一化和实际残差身份完全没有通过这些数值获得证明。

## 2. 输入契约

唯一格式为 UTF-8 JSON，顶层字段必须恰好是：

| 字段 | 要求 |
|---|---|
| `schema` | `T-P5-026-exact-componentwise-comparison-v1` |
| `scope` | `source-independent-unbound` |
| `coordinates` | 恰好 `state=["x4","x5","y4","y5"]`、`force=["r4","r5"]` |
| `path` | 恰好包含 A、Hjac、Scoord、K_path |
| `K_cert` | 2×4 非负有理表 |

`path` 的具体形状：

```text
A       : 2 × m             可以带符号；公式中恰好取一次 |A|
Hjac    : R × m × n         非负
Scoord  : R × n × 4         非负
K_path  : 2 × 4             非负；必须等于完整重算结果
```

维度从数组推导，不接受额外维度声明。Hjac 和 Scoord 的第 s 项必须对应同一段，
所有行保持顺序；不按值去重。不接受缺行、额外行、ragged arrays 或转置表。
当前资源上限为输入 262144 bytes、`1≤R,m,n≤32`、`R*m*n≤2048`。
空路径不在 v1 范围内。超限表示无法按此接口检查，不表示数学命题为假。

所有矩阵条目必须是 **JSON 字符串中的 canonical rational**：整数形式或既约分数，
分母严格为正。例如 `"0"`、`"-1"`、`"3/7"`；符号只在 A 中允许为负。
分子、分母各最多 64 位十进制数字。零只能写成 `"0"`，整数不能写成 `/1`。

拒绝：JSON 数字（包括整数）、布尔值、null、decimal、exponent、NaN/Infinity、
零/负分母、前导零、前导加号、空白、`-0`、未约分形式。
所有层级拒绝重复 JSON key 和未定义字段；不采用“最后一个键覆盖前一个键”。
CLI 有界读取，非法 UTF-8/JSON、I/O 错误、深度或运行时表示限制均失败退出。

格式比旧 SPN checker 的整数/有理输入更严格，未更改旧格式。未来 exporter 应逐项
以精确有理运算规范化，不可先将浮点数转成分数字符串来冒充来源证明。

这里没有可运行的 concrete input JSON：上游尚未提交真实绑定数据。
测试中的数表仅为带明确 synthetic 标签的内存算术 fixture，不会导出为 source artifact。

## 3. 如何连接既有实数接口

新增候选 `ExactComparisonBinding K G` 包含：

```text
pathTable, certTable : Fin 2 → Fin 4 → ℚ
path_nonnegative, cert_nonnegative
comparison : ∀ a j, pathTable[a,j] ≤ certTable[a,j]
path_entry_eq : ∀ a j, K.value[a,j] = ↑pathTable[a,j]
cert_entry_eq : ∀ a j, G.value[a,j] = ↑certTable[a,j]
```

候选 `toComponentLE` 通过两条实数身份和有理到实数的序保持转换，接到现有
`RouteBP5KPathInterface.ComponentLE K.value G.value`。其预定调用位置是：

```text
K := 既有 transportedGain A Hjac Scoord hH hS
G := 未来 ConeGapBinding / SPN 消费的同一个非负 gain
ExactComparisonBinding K G
  -> ComponentLE K.value G.value
  -> 既有 componentwise_spn_power 的 comparison 参数
```

**本轮未运行或声称验证这个 Lean 文件。** Python 不产生 Lean proof term，
JSON 的 `true`、stdout 成功状态和 SHA-256 不能构造 `ExactComparisonBinding`。
除编译候选外，上游还须证明 rational A/Hjac/Scoord 与实际实数表相符，以及
`path_entry_eq` 的求和/绝对值/cast 身份；checker 的有限计算不自动完成这个桥接。
`cert_entry_eq` 同样必须对应未来 SPN 文件实际使用的 K，不能换成另一张表。

若实际 pathK 不是有理数，但有经证明的有理上界，应在上游提供实数逐项上界证明，
再用现有 `ComponentLE` 传递；不能把这里的精确 `path_entry_eq` 偷换成数值近似。
本 v1 要求给定表精确相等，尚不支持 interval endpoint 作为另一种输入模式。

## 4. H 的序不能偷换

`Hjac` 是非负 path transport 系数；锥矩阵 `H_gap(c)` 是另一个对象。
给定同一个 mu、Q、chart 和精确 gap binding，`K_path≤K_cert` 蕴含：

```text
|Lz|ᵀ K_path |z| ≤ |Lz|ᵀ K_cert |z|,
uᵀ H_gap(K_cert,c) u ≤ uᵀ H_gap(K_path,c) u,  u≥0.
```

第二行只是非负正交象限上的二次型反向比较，不是 H_gap 的逐项矩阵序，
也不是全空间 PSD/Loewner 序。检查器完全不接受 H 字段、不构造 H 矩阵，
也不声称产生 PSD/SPN 分解。`H_matrix_order_proved=false` 始终保留。

同样，较大的 Frobenius 范数不保证逐项上界；负控显式使一项小于 K_path、
另一项极大，仍必须拒绝。单项仅差 `10^-40` 也拒绝，没有“足够接近”的分支。

## 5. 来源、坐标和哈希边界

检查器只读核对现有 `P5PiecewiseTransport.lean` 的固定 SHA-256：

```text
c445e4110584c5c536f023ad08b2a8c5eccef21fc9b97aa363f24e0a9ae95208
```

它固定本轮所依据的公式版本，**不执行 Lean、不解析 Lean 证明、不认证数学语义**。
开始和结束均核对该文件，版本改变即拒绝继续使用该 pin。

成功报告含输入原始 bytes 的 SHA-256，以及两张有理 gain 的 canonical data digest。
后者是固定编码标签、固定坐标次序和规范化有理条目的紧凑、排序 JSON 哈希。
`K_cert` 的规范表也直接输出，供未来 exporter 对照其 actual K 条目。
这些 digest 用来追踪数据一致性，不是来源签名、域证明或 admission receipt。

坐标标签一致不证明真实物理变量排列正确；A 应当是恰好一次的力坐标映射。
把 A 错误重复归一化后连同 K_path 一起重算，算术仍可能通过，物理绑定仍然错误。
对应负控只证明“改了 A 却沿用旧 K_path”会拒绝，并不声称侦测所有语义归一化错误。
同理，所有上游表若被一致伪造，单纯算术检查不可能据此认证来源。

## 6. 本轮验证

普通模式与 `python -O` 模式各运行 12 组 unittest，均通过（exit 0）：

```powershell
python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_Comparison_test.py
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_Comparison_test.py
```

正控：独立手算的多段/非均匀 rational fixture、全部 8 个正 slack、A 整体反号
保持 |A| 不变、零 gain 的纯算术接受。fixture 从未标记为实际 K_path。

负控：全部 8 个 pathK 身份条目分别篡改、全部 8 个比较条目分别仅缩小 `10^-40`、
仅标量范数更大、非 canonical/非 rational 值、各非负表负项、缺项/额外项/错序、
改动 A 后旧表不匹配、重复嵌套键、非有限数、超限输入、错误 scope、伪造 source/
registry/H/tolerance 字段、修改公式版本 pin。
三个 stdin CLI 探针验证成功 exit 0、重复键 exit 1、缺输入 exit 1，且始终不升级状态。

测试脚本没有调用旧 `NEW_KPATH_INTERFACE_check.py`，也没有调用任何 Lean/Lake。
未重跑宽泛回归或旧 SPN 检查。测试不写 fixture、临时文件、字节码或报告文件。

使用未来已有真实输入（本轮没有该输入）：

```powershell
python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_Comparison.py --input <existing-comparison.json>
```

`--input -` 从 stdin 读取。算术未通过/无法检查返回 `rejected_or_uncheckable`；
通过返回 `unbound_exact_arithmetic_pass`。失败不是 copositivity 反例。

实现 SHA-256：

```text
NEW_KPATH_INTERFACE_Comparison.py
d7dd1275a46bda19733d0d3e2700ca891f4759c918e62f786bd2a238f5c08392
NEW_KPATH_INTERFACE_Comparison_test.py
ebb410a3b86d6b970f80cbce84e2c1034d2330b3c48f23142d4d449853a958fe
NEW_KPATH_INTERFACE_RationalBinding.lean
2f46e4c077c44c91d5a9152140f2253dcfdf8c7d3edbebd4c4a6617c2e4ad06d
```

无论成功或失败，以下字段均为 false：`source_binding_verified`、
`pathK_lean_binding_verified`、`kernel_verified`、`spn_verified`、
`H_matrix_order_proved`、`source_coverage_verified`、`registry_eligible`、`P5_P8_M4_closed`。
具体源表、同域 residual envelope、18 份 SPN、source/coverage/P8/M4 closure 继续开放。
