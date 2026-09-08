# BODY6 typed-interface audit (2026-09-08): pending

结论：两个接口在同一 F/G、full-state path、[0,1] 和 B 下可以组合；缺口不是
single-shift 算术。缺的是具体 source/path/domain 的实例、对上游 ledger 的
state/storage/strict-threshold adapter，以及尚未进入 frontier 的显式依赖。
本文不提升 admission，不修改既有 Lean、state、registry 或共享脚本。

## Exact inspected contracts

在 `examples/routeb_b45_source_comparator_lean`：

| 文件 | 位置 | 提供的接口 |
|---|---|---|
| NEW_BODY6_SLICE_PATHCONTRACT20260908.lean | 13–29 | `PathContract F G path a B bar b`：initial、growth、on-path value、pointwise budget → `FullPathCap G path bar` |
| NEW_BODY6_SLICE_PATHREASSIGNED20260908.lean | 11–26 | `TransferInputs project D Q path F G B cap bar`：projection、wholePath、Q 上 value、sourceCap、budget → 同一 G/path 的全程 cap |
| NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean | 29–52 | `ConsumerPremises` 的 initial/start/growth/uniformGrowth、alignment、projection/path 与 budget |

PATHCONTRACT 的原文 SHA256：
`bd96b283accae86e695a180bfe9223e9b396b6efdd0178dac380394eac6321f2`。
PATHREASSIGNED 的原文 SHA256：
`2343ca9a6ad775643e344d2e78d66f4dd7960fa0c10a910fdb9864da1fa402ec`。
兩者与现有 review 的 source hash 一致。

`PathContract.value` 仅在指定 path 上成立；`TransferInputs.value` 在 [0,1]
的所有 `project x∈Q` 上成立，且后者保留调用者指定的 D。不能将前者反推出后者
的域证明。`pullbackDomain project Q` 可表达 projected membership，但不等于
包含速度、slope 或其他物理约束的固定 D，也不产生全路径归属。

## Three minimal adapters

可复用 Lean 代码保存在 `NEW_SEAM_BODY6_TYPED_check.py` 的 `ADAPTERS` 字符串，
通过 `lean --stdin` 检查，不写 `.lean`、`.olean` 或 `.ilean` 文件。

| Adapter | 输入与输出 | 保持的边界 |
|---|---|---|
| `initial_growth_to_transfer_inputs` | initial a + growth b + `b(t)≤beta` + projection/path/Q-value + `(a+beta)+B≤bar` → `TransferInputs`，cap=`a+beta` | 复用 existing `growth_supplies_full_cap_attempt`；不积分或构造轨迹 |
| `transfer_inputs_to_algebraic_path_contract` | `TransferInputs` → `PathContract`，a=`F(0,path(0))`，b(t)=`cap−F(0,path(0))` | 将已有 full cap 作代数重包装；不恢复调用者原来的 initial/growth provenance |
| `path_contract_to_transfer_inputs_with_domain` | `PathContract` + supplied projection、wholePath、Q-value → `TransferInputs`，cap=`bar−B` | 数值 cap 可构造；域与 off-path identity 必须独立提供 |

第二个 adapter 的证明：initial 取 reflexivity；由 F(t)≤cap 得
F(t)≤F(0)+(cap−F(0))；将投影后的 wholePath 代入 Q-value 得 G(t)=F(t)+B；
预算化简为 cap+B≤bar。这里的 b 是已知 full cap 的重述，不是微分不等式积分。

第三个 adapter 的证明：F(t)≤F(0)+b(t)≤a+b(t)≤bar−B；
`(bar−B)+B≤bar` 是等式。**不能把 pointwise budget 与 uniform cap 的区别
误报成不可组合的数值缺口**。真正缺失的是 DomainProjection、WholePathMembership
和 ShiftIdentityOnQ 的全域语义；要保留预先指定的 cap/a/b，还需相应 compatibility。

ALIGNED consumer 的各字段可直接喂入第一个 adapter：initial+start 给 initial path
cap，alignment 给 Q-wide identity，projection/wholePath 不变，cap=a+beta。
其结果和现有 `aligned_premises_to_path_contract_attempt` 是同一个 conclusion
的两条消费路径；无需把 PATHCONTRACT 与 PATHREASSIGNED 互相 import。

## Single-shift budget

正确链条只有 `F(t)≤cap`、`G(t)=F(t)+B`、`cap+B≤bar`，因此 G(t)≤bar。
value 中 B 与 budget 中 B 是同一项，不能在得到 G 的 cap 后再加一次 B。
若传入的 cap 已经界住 F+B，复用 PATHDOMAINPROJECTION 的
`already_shifted_cap_transfer_attempt`，不能再提交给要求 unshifted source cap
的 `TransferInputs` 来重复收费。上述算术 adapter 不需要 B≥0。

本分支 shiftB=4079979/400000，等于 PATHDOMAINPROJECTION.routeBShift 和
ONESHIFTREPAIR.exactB 的同一有理数；代码形式都是同一 Real quotient。
在 normalized origin 路径 F(0)=0 的条件下，任何 source full cap 都非负，
因此 bar=1 无法支付该 B。PathContract 也不能靠随意负 b(0) 绕过：growth 在 t=0
强制 b(0)≥0，initial 强制 a≥0，预算继而强制 B≤1。此为条件化预算阻碍，
不是当前实际轨迹/控制器失败声明。

## Parent/child composition gaps

1. `COMPILEDLEDGERBINDING.PathLedgerBinding` (lines 73–85) 消费
   `Sample={q,v,slope}`、一般 time-dependent `StorageData`、
   `L(t,x)=actualAt(d,t,x)`、sourceTube 和 `tube<ledgerBar=1`。
   ALIGNED consumer 的 `State=Vec×Vec` 且 source 固定 f=1、h=0、p 常数。
   必须显式给出 `rho : Sample→State`、path transport、初始集/域 transport、
   StorageData specialization 与 evaluator equality。投影丢掉 slope 后不能
   反推原始 Sample 域的路径约束。
2. `FullPathCap G path bar` 是非严格上界，不能直接成为 ledger 的 `<1`。
   若消费的是 G，需 `bar<1` 和 G 与目标 ledger 的 identity；若消费的是 F，
   可使用 adapter 得到的 source cap bar−B，但仍需 F 与 actualAt 的 identity
   和对应 cap<1。G=F+B 不能被当成 ledger 要求的零偏移 sameStorage。
3. `INITIALCROSSDELTA.keyed_initial_transfer_contract_attempt` (lines 88–102)
   令 scope.initial=scope.domain=blockInitial。它只支持 X0 的 one-sided delta，
   不提供 WholePathMembership 或 Q-wide equality；也不能生成 IntegratedGrowth。
   path 使用必须重新给出比较域、同域 bound、path inclusion 和匹配 receipt key。
4. `V0PARAMETERMAP.candidate_v0_transfer_attempt` 给 initial bound；它没有给
   initial-set 内成员资格、source dynamics 的增长或 path inclusion。数值 V0
   匹配也不产生 actual/target 同一存储。
5. 三个通用 adapter 的结论没有 sourceBody6=FourierBody6 的内容，不能关闭
   `P4.O1.source_comparator.h_body_6` 的 exact coefficient identity。

缺口应以具体实例字段保留：same-source/state/evaluator、initial/start、
integrated growth、fixed-domain projection/path、alignment/Q-value、threshold。
域 D 若以目标 barrier 自身定义，则还须防止用待证 barrier 反证 pathInDomain；
当前文件没有 ODE、continuation 或 first-exit producer 来消除这一依赖。

## Current frontier and minimal proposed DAG change

对 `artifacts/routeb_6dof/state.json` revision **764** 做了只读 checksum 验证与
WorkflowState 解析（未调用会创建 lock 的 StateStore.load）。相关节点如下：

| Node suffix / ID | Dependencies | 当前 frontier predicate |
|---|---|---|
| storage_identity_transfer / e64f0bd1919f467cb995c355c6028c66 | compiled_ledger_binding、keyed_storage_transfer | false |
| compiled_ledger_binding.v0_parameter_map / bdcd53d4826b412cb003f13a21b4f78c | 无 | true |
| keyed_storage_transfer.initial_cross_delta / 6d1e630d0e694b46a99804e29541167f | 无 | true |

state 的 node metadata 及 `register_routeb_sidecar_frontier.py` 均没有
PATHCONTRACT/PATHREASSIGNED/ALIGNEDPATHCAPCONSUMER 的引用。
PATHREASSIGNED processed receipt 的 `integrated_as_pending_metadata` 只记录
review 接收，不等于它成为上述图中的 child 或提供 theorem dependency。
因此，当前没有可供调度的这两个新 leaf 的依赖边，更没有父结论 assembly。
并发任务在本次检查期间推进了 state revision；本文固定到已读的 764 snapshot。

建议的最小变更（仅建议，未改 DAG）：

- 编译图：把 PATHCONTRACT 的 generic record+consumer 提取成只 import
  INITIALPATHCAPS 的 core，aligned→contract 留作单独 adapter。core 和
  PATHREASSIGNED 是共享 PATHDOMAIN/INITIAL 基础设施的平行分支；三条 glue
  theorem 仅依赖 generic core+PATHREASSIGNED，避免 ActualStorage closure
  阻塞纯标量接口。完整 aligned 分支仍保留自己的 import/compile gate。
- 数学图：在 storage-transfer 支线记录独立的 generic composition 与 actual
  instantiation/strict-ledger bridge 待办。initial V0、initial delta、domain/path、
  alignment、growth 作为明确的 producer obligations，不把两个 initial-only
  leaf 当成足以 assembly 全路径 barrier。父结论继续 pending，必须有匹配
  parent receipt / semantic obligations 才能声称组合完成。
- `model.py:363–384` 将 `dependencies` 定义为 theorem-tree children，
  `metadata.required_node_ids` 才是跨支线 theorem 输入；后者检查 closed **且
  在 registry 中**。禁止把 compiled_candidate 或 pending receipt 放进去后
  宣称可运行，也不能为绕过此检查提升 admission。共享 `.olean` 的 compile
  prerequisite 应保留在单独的 artifact/compile 依赖说明里，不伪装成已满足
  theorem edge。现有 API 无法在不经过真正 admission 的前提下让这种 required
  theorem edge 被满足。

## Focused validation scope

直接使用 pinned Lean 4.32.0（commit 8c9756b28d64dab099da31a4c09229a9e6a2ef35），
LEAN_PATH 仅含 BODY 目录与 local_fkg 现有 package build directories。
没有运行全项目 Lean 回归、重建依赖或写入 `.olean`。

完整 PATHCONTRACT 的一次检查 exit 1，精确 blocker 为：
`unknown module prefix 'NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908'`。
现有 083415 receipt 报告更上游 ActualStorage cache 的 incompatible header；
本次仅引用该历史诊断，没有重新运行该依赖。当前 import 缺失已实际复核。

随后以 stdin 检查完整 PATHREASSIGNED 原文、PATHCONTRACT **精确截取的 generic
record+consumer**，以及三条新 adapter。它不包括两个 aligned adapter，也不能
替代完整 PATHCONTRACT 的 compilation receipt。首次 50 秒上限超时；延长该
单项后发现新 adapter 的 `dsimp made no progress`，已在本次新脚本中改成
显式 `change`。失败那次自动出现的 sorryAx 不能计作有效证据。

最终单项检查 exit **0**；完整 PATHREASSIGNED 的五个 theorem、generic consumer
及三条 adapter 共九个 `#print axioms` 均只有
`propext, Classical.choice, Quot.sound`，没有 sorryAx。
最终运行结果见 `NEW_SEAM_BODY6_TYPED_RECEIPT.json`；所有 admission/source/path
实例标志继续 false。该检查器仅写 stdout，外层 exit 3 表示 pending；应单独
查看 `runs[*].exit_code` 判断 Lean 是否成功。

旧 082220 receipt 中 INITIALPATHCAPS 的 displayed hash 少末尾 f（63 字符）；
现存原文完整 hash 为 `5cad04f2e8b0af13c8d8a099455812fe1f6d17a66a0d567be5b85963252d224f`。
本次另记录实际 source/object digest，不把那条截断文本当作精确 hash binding。

复现这个已完成的窄检查（不重编译依赖）：

```powershell
python -B examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_BODY6_TYPED_check.py --adapters-only --timeout 150
exit $LASTEXITCODE
```

本次只新增本目录下 `NEW_SEAM_BODY6_TYPED_check.py`、
`NEW_SEAM_BODY6_TYPED_RECEIPT.json`、`NEW_SEAM_BODY6_TYPED_REVIEW.md`。
