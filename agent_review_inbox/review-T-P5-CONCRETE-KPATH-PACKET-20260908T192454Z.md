---
kind: review_result
review_id: R-P5-CONCRETE-KPATH-PACKET-20260908T192454Z
task_id: T-P5-CONCRETE-KPATH-PACKET-20260908
source_agent: Codex-P5-mathematical-packet-lane
created_at: 2026-09-08T19:24:54Z
inspected_commit: 769590f5f704a658607040739a90945ea5b5a6ec
inspected_path: examples/routeb_p5_feasible_cone_spn_proof_attempt
status: EXACT_OBSTRUCTION_AND_CONDITIONAL_CONSTRUCTION
integration_status: pending
admission_label: pending
concrete_K_path_bound: false
source_binding: false
P5_closed: false
registry_eligible: false
registry_promoted: false
lean_run: false
lake_run: false
checker_run: false
requested_action: catalog_pending_math_and_missing_obligations
---

# P5 concrete K_path packet：目前不能组成；关键缺口与可补数学构造

唯一新增数学稿：
`examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_PACKET_ObstructionAndCapacity20260908.md`。
另新增本 immutable review。未改旧文件、state、registry 或 shared adapter。
不运行 checker/回归/Lean/Lake；本轮结论来自源码接口、精确代数推导和范围受限文件枚举。

## 结论

现有 artifacts 可以组成 **source-independent 条件结构**，不能组成同一 concrete
K_path packet。18 个标签/闭锥几何存在；18 份 toy SPN 的生成函数存在；
具体 source-indexed K_path、同域 residual/path 绑定以及同一 consumer 的输入身份未供给。
这不是只差一个 manifest hash：存在实质数学输入缺口。

数学新增：当前 toy 的固定 N-slack 更新对任意非零 E≥0 都失败（仅 pp×pp 即迫使 E=0）；
可改用 PSD-slack 的 18×4 有理线性约束容量区域，不必先重做全量数值搜索。
该构造与详细推导见数学稿；尚未计算任何实际 δ/E/t 或生成 concrete certificates。

## 已有内容的精确等级

- REVIEW_exact_geometry_spn.md 记录完整闭锥逆映射/Farkas、36 个 gap 符号恒等式、
  18 个反号代表和 toy SPN 的历史 exact-arithmetic 检查；不是本轮重跑或 source closure。
- check_exact.py:212–225 明确 toy K=全 1/1000、μ=1/2、scope=source-independent-unbound。
  每个 N 只有 N01=N10=1/10000；R/d 来自 toy S 的 exact LDL。
- NEW_CONE_INDEX_ConcreteConsumer20260908_REVIEW.md 记录过 Lean 4.32.0 source-bundle
  checking；本轮不否认该历史运行，也不刷新为当前编译。
  它明确不是到旧 H/SPN 对象的 typed bridge，standalone module imports 未验证。
- NEW_KPATH_INTERFACE_Core.lean 已定义 PathBinding/ConeGapBinding/SPNWitness 与
  componentwise_spn_power/pointwise_ledger 条件 consumer；它们没有实例化实际输入。
- Comparison.py 只接受 source-independent-unbound，重算有理 pathK 后比较 K_cert；
  输入 hash 和固定 formula-source hash 不认证真实 source tables。
- 本目录只读枚举未见 concrete certificate .json/.csv 数据文件；这不排除其他目录
  有数据，但已查 typed/review 材料自身明确 concrete_K_path_bound=false。

## 字段级 exact obstruction 与最小可补义务

| Packet 字段 | 当前证据/阻碍 | 最小补交 |
|---|---|---|
| packet_id/source_snapshot/state_schema | 没有一组绑定 actual source 与全部下游输入的 immutable packet | 指定 producer/commit/原始输入 hashes、状态字段/units、参数版本；不要把 workflow revision 当数学 state |
| D、z、rc | PathBinding 仅参数化 X/D/z/rc；未绑定同域 actual centered residual | 实际函数与域、z=(x4,x5,y4,y5) 身份、rc=(r4,r5) 定义及 centering；z=0 时 rc=0，否则拆 bias |
| chart/index identity | ConeIndex 36↔18×Bool 具标签结构；旧表与 typed core 的联系仍有 text-check 层 | 真实 chart/T/sign/Q 的 typed equality，Fin3 rank 对应 Python IDs (0,2,3)；边界不去重 |
| A/Hjac/Scoord | formula 和结构存在，无实际三表 | A:2×m、Hjac:R×m×n≥0、Scoord:R×n×4≥0，加源 hash/单位/归一化；A 只施加一次 |
| path witnesses | 未交 dxi/de/state_bound/increment_bound/force_eq | 同一 x∈D 上逐段界，rc=AΣs de_s；如果来自 Jacobian/FTOC，还须每段同域包含和正则性 |
| K_path | 不能用 toy 或声称的 2×4 表替代 | 八项 K_path[a,k]=Σsij |A[a,i]|Hjac[s,i,j]Scoord[s,j,k] 与 real/rational cast identity |
| G=K_cert 与 μ,Q | toy G/μ 有值，但不是真实路径的比较见证 | 八项 K_path≤G，固定同一 μ/Q/force/state normalization；不得用 norm 大小代替逐项比较 |
| H[r] identity | exact geometry 知道公式，不是实际 G 表的 certificate witness | 每个 indexed H[r]=Tᵀ(μP−sym(LᵀDτ G Dσ))T，及 gap identity、H_flip=H |
| 18 certificates | toy generator，不是 actual G 的 source-bound export | 恰好 18 个完整 representative IDs，各 S/N/R/d exact rationals，H=S+N、S=Rᵀdiag(d)R、d≥0、N≥0 |
| consumer identity | 同名 P5FeasibleConeSPN 模块有歧义；typed signed cover 不等于 H/SPN binding | 锁定实际 source path/SHA/module namespace、import search order、consumer full type 和每个参数实例 |
| build/admission | 历史 bundle 或 Python pass 不能代替本 packet receipts | 精确目标 pin/lock、candidate/import/type/axiom/comparator receipts；registry promotion 仍独立 |

K_path 的 Hjac 是 Jacobian/increment bound；锥 H 是 4×4 gap matrix。
source force A 与 cone absolute-state A_r 也不是一个对象，packet schema 应强制分名。

## 最小可构造的 single-packet 数学链

1. owner 先交同域 PathBinding 的实际三表与 witnesses，重算 K_path；不先编 18 toy certificates。
2. 固定 Q/μ/chart/index 与 certificate gain G：若 K_path≤K0，直接复用 K0 envelope；
   否则用 E=(K_path−K0)_+，尝试数学稿的 PSD-slack capacity（不是固定 N 扣减）。
3. 在同一 G 下构造 18 indexed SPN witnesses，用 H_flip 提升至 36；源理想数据与
   checker 输入分别绑定，禁止按相同矩阵值合并标签。
4. 使用同一个 x∈D、source ComponentBinding、K_path≤G、exact gap 和 certificates，
   实例化 RouteBP5KPathInterface.componentwise_spn_power，输出
   |(Lz(x))ᵀrc(x)|≤μQ(z(x))。
5. 仅有真实 Vdot inequality 时再接 pointwise_ledger；trajectory/P8/M4 仍独立。

其中“typed source-independent consumer 已检查”只解决通用蕴含，不会自动供给第1–3步。
某张 18表缺失或 fixed slack 不足应保持 pending，不等于数学 counterexample。

## Consumer/import 精确风险

NEW_KPATH_INTERFACE_Core 的 import P5FeasibleConeSPN 注释指向
`examples/routeb_p5_feasible_cone_spn_lean/` 的 generic sidecar，**不是**本目录
`P5FeasibleConeSPN.lean` proof attempt。同名 search-path 解析必须入最终 packet。
不能只记录模块字符串、或把 source-bundle concatenation 成功称为独立 OLean imports 成功。
本轮不运行 Lean，也不将既有历史报告统一改写成 UNCOMPILED。

## 输入快照（实际字节 SHA-256）

以下文件均在 inspected_path 下：

| 文件 | SHA-256 |
|---|---|
| check_exact.py | d887aade11edf9adf1e7f532d8b173a089aac9e2fadba2e25fbc2f169e1e4211 |
| NEW_exact_geometry_spn.py | 263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42 |
| NEW_KPATH_INTERFACE_Core.lean | 10c7e769e772a2f4475def1eb061e52319510cb906cb879c4234653f2d64a17c |
| NEW_KPATH_INTERFACE_Comparison.py | d7dd1275a46bda19733d0d3e2700ca891f4759c918e62f786bd2a238f5c08392 |
| NEW_CONE_INDEX_Core.lean | b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602 |
| NEW_CONE_INDEX_ConcreteConsumer20260908.lean | 5f50f2c68713a18d4b490573923315cb2f0a24cfafda3e281f7c1154c1d36205 |
| P5FeasibleConeSPN.lean | fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824 |

实际执行仅 rg/文件枚举、Get-Content、Get-FileHash、Git HEAD/UTC；最后定点检查
shell exit 0。未执行 checker/self-tests、符号工具、Julia、Lean/Lake 或远程任务。
数学稿的等式/充分条件为本轮推导，不声称经过 kernel 或程序验证。
不请求 state/registry 变更；下一步以补齐 actual path/source packet 为先。
