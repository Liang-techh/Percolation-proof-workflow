---
kind: review_result
review_id: review-GH-LEAN-BODY6-PATHCONTRACT-RECEIPT-20260908T110208
task_id: GH-LEAN-BODY6-PATHCONTRACT-RECEIPT
source_agent: codex-local
created_at: 2026-09-08T11:02:08-06:00
inspected_commit: c7ab49a3c55c002076ae18f325eedc8a146ac9bd
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_PATHCONTRACT_REASSIGNED_20260908.lean
artifact_sha256: ff5e2dfbcf0375d96cce232c739e0098381ce5b1828f7142dae23ac3e86a68fc
probe_path: examples/routeb_b45_source_comparator_lean/NEW_PATHCONTRACT_REASSIGNED_Probe20260908.lean
probe_sha256: 78cd395e47fc5edc7e781ba1574562ddcb8fa41135c0c3e8613cdcbfd7e98206
proof_status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
compile_receipt_status: not_produced
source_receipt_status: not_produced
registry_mutation: false
formal_certificate_allowed: false
requested_action: Use the isolated probe in a separately authorized pinned GitHub check; return compile and source statuses separately.
---

# Revision-804 follow-up：probe 与 pinned receipt checklist

revision 804 是请求提供的上下文编号，本轮不将其当作 Git commit/source receipt。
只新增 probe 和本 review；原候选 SHA 未变。没有运行本机/远程 Lean/Lake、
GitHub workflow、receipt、checker 或 integrator。没有修改旧文件/state/registry。

## 1. Probe 入口

新增 NEW_PATHCONTRACT_REASSIGNED_Probe20260908.lean，导入原候选，执行计划为：

- #check Prop structure 及五个字段的完整类型。
- 检查 (5:Fin6).val=5，并将隐式列 numeral 5 与显式 ⟨5,proof⟩ 作 rfl 比较。
- 用完整 binders 再次消费原 cap theorem，h 仍然是输入假设。
- #print 两个原 theorem，#print axioms 两个原 theorem 与 probe wrapper。

这些是尚未执行的 Lean 源命令，不是检查结果。Fin 构造中 by decide 仅用于
证明 5<6，不是 source 或 path 判定；没有 native_decide。
结构有类型、投影存在或 wrapper 可接受，均不意味着有
SixthColumnPathContract embed qOf domain Omega path rows physicalRow cap 的实例。

## 2. 明确选定一个 pin，不混用其他 lane

本轮读取 examples/local_fkg 的文件锁，拟用作 BODY6 的隔离检查环境：

```text
Lean: leanprover/lean4:v4.32.0
Mathlib: 81a5d257c8e410db227a6665ed08f64fea08e997
toolchain SHA256: 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e
manifest SHA256: 6cad04cdeb731b8af3594767512923ac9b9fe7e00808f91ddcb30c846e3891f3
```

这是读到的 manifest/toolchain pin，不是本轮确认的 executable、Mathlib checkout
或环境成功。不要与 FLT lane 的 Lean 4.33.1/Mathlib 0df444... 混用。
local_fkg manifest 还含 path dependency PercolationContinuity；GitHub 不应直接
复制整个本地环境并猜测路径。可用隔离包只 require 上述 Mathlib revision，
再按实际 import closure 加入必要的项目源。若项目 API 在此 pin 不兼容，返回
准确失败日志；未经授权不得升级 pin、改候选或用 sorry 补齐。

## 3. GitHub Lean agent 的执行顺序（本轮未运行）

1. 固定 repository checkout SHA 与候选/probe source SHA；本候选可能不在当前
   checkout 中，必须另记录 overlay artifact 的来源与字节，不能只填 inspected HEAD。
2. 创建独立工作目录，安装指定 Lean 与指定 Mathlib git revision，记录全部 lock
   与 actions 的不可变 SHA。只在该隔离目录生成构建产物。
3. 从候选递归解析项目 import 名称，逐模块确定唯一源路径与 SHA，再依依赖顺序
   编译。不得把源目录放入 LEAN_PATH 就当作 imported modules 会自动编译。
4. 将新生成的项目 OLean 目录加入 LEAN_PATH，并记录该路径；避免任何旧本机
   .olean 或同名模块遮蔽。获取匹配 pin 的 Mathlib 依赖产物后再检查候选。
5. 在隔离包内、源文件及输出目录已准备好时，可使用下列入口：

```text
lake env lean -DwarningAsError=true -o out/NEW_PATHCONTRACT_REASSIGNED_20260908.olean NEW_PATHCONTRACT_REASSIGNED_20260908.lean
lake env lean -DwarningAsError=true -o out/NEW_PATHCONTRACT_REASSIGNED_Probe20260908.olean NEW_PATHCONTRACT_REASSIGNED_Probe20260908.lean
```

第二条的 import 需通过前一步 LEAN_PATH 解析到第一条新输出。out 的创建、
项目依赖闭包与隔离 lake 配置属于 runner setup，不由以上两行自动完成。
没有授权执行任何主工程 build、state 更新或 registry integrator。

## 4. 实际 import / numeral 风险

原候选直接导入 RouteBO1Body6CanonicalExportTargets，其又导入
RouteBO1PerBodyExactSource、BodyTraceEvaluator。前者导入
SourceBodyMassExtensionalProbe、SourceContractIndexAdapter、Mathlib；后者导入
Mathlib。因此这是跨目录 source closure，不是单文件纯 Prop 编译。
本轮未穷尽递归闭包；runner 必须生成并返回 source manifest，不能沿用泛型
PATHDOMAINPROJECTION 的窄闭包作为替代。

源 sourceBodyMass 的类型为 Q6→Body→Mat6，显式本体 5 与末位列 5 都应落在
Fin6。没有静态迹象表明此处 5 越界；风险是人类一基 joint/body 与零基 Fin
语义的源映射，而不是可以盲目把 5 改成 6。probe 仅核对 Lean numeral typing，
不证明物理标签转换。Fin 类型对一般越界 numeral 可能模约简，不能用它自动
验证外部 CSV 的 range。

cap rewrite 中 physical_eq_canonical_on_path 是完整显式参数调用；尚待检的是
隐式 X/Physical、sourceIdentity 中 q 推断、结构投影依赖参数与 rw 目标匹配。
embed 是固定函数，不带 Injective，这足够单向 cap transport；不宣称逆向恢复。

## 5. 最小 compile receipt 与 source receipt 分离

Compile receipt 必须包含：repository/checkout/overlay 身份；候选、probe 与
全部 project imports 的 SHA；Lean executable --version、Mathlib revision、
lock hashes；命令/cwd/LEAN_PATH；exit code、完整 stdout/stderr URLs/hashes；
新 OLean hashes；完整 theorem types 与逐声明 axioms。若出现 sorryAx/新增公理、
哈希不符或 import 遮蔽，明确返回失败/拒绝；没有材料则 pending。

Source receipt 另需同一组参数下的五个实例：projection、inclusion、physicalIdentity、
sourceIdentity、canonicalCap，绑定固定 embed/qOf/domain/Omega/path/rows/physicalRow/cap。
不能以 structure 构造器名称、#check 输出或一个假设 h 替代实例。
第六列候选的完整 source/geometry/data 依赖及接受证据也须单列，不能只引用名字。

CanonicalRow 的 rational 值等同不恢复 raw body、分子/分母标签或 CSV 字节。
Raw provenance 要另给 body6 一基→Fin5、entry 索引、完整有符号频率、整行系数
标签与列表重数绑定。第六列相等不能充当 full matrix/storage alignment。
最终报告应允许“纯 consumer 编译成功但 source/path 实例仍缺失”，不得自动
注册或标 VERIFIED。新 probe 本轮保持 OPEN_UNCOMPILED。
