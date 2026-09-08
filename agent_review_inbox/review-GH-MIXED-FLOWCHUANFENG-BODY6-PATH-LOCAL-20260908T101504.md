---
kind: review_result
review_id: review-GH-MIXED-FLOWCHUANFENG-BODY6-PATH-LOCAL-20260908T101504
task_id: GH-MIXED-FLOWCHUANFENG-BODY6-PATH
source_agent: codex-local
created_at: 2026-09-08T10:15:04-06:00
inspected_commit: 218f8f45a05b4146951810d99e6ce6fb3badb825
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHREASSIGNED20260908.lean
artifact_sha256: 2343ca9a6ad775643e344d2e78d66f4dd7960fa0c10a910fdb9864da1fa402ec
proof_status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
compile_performed_this_review: false
kernel_verified_this_review: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: Reuse the existing typed sidecar for a separately authorized pinned check; retain physical path and source witnesses as external obligations.
---

# 独立 bounded review：复用 BODY6 typed path sidecar

本轮不新增重复 Lean，不修改任何候选、依赖、旧 review、state 或 registry。
只新增本 review_result。没有运行 Lean/Lake、Python checker、回归或远程编译。
候选可用于后续独立检查；此处“可复用”不是 compiled/VERIFIED 判断。

## 1. 窄接口选择

选用 `NEW_BODY6_SLICE_PATHREASSIGNED20260908.lean`，直接依赖仅
`NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907`。它的 TransferInputs 索引
project、固定 D、Q、同一 full-state path、F/G、B/cap/bar，并外置五个字段：

| 字段 | 必须由调用者提供的事实 |
|---|---|
| projection | t∈[0,1] 且 x∈D(t) 时，project(x)∈Q |
| wholePath | 每个 t∈[0,1]，path(t)∈指定的 D(t) |
| value | 同一投影域上 G(t,x)=F(t,x)+B |
| sourceCap | 每个 t∈[0,1]，F(t,path(t))≤cap |
| budget | cap+B≤bar |

adapter 只将字段传给现有 transfer theorem；没有构造任何实际 source/path witness。
预算中 B 只支付一次；若输入已经是 F+B 的 cap，应使用依赖内另一个
already_shifted_cap_transfer_attempt，不应重复收费。

候选 namespace `NEW_BODY6_SLICE_PATHREASSIGNED20260908` 的五个声明：

```text
repaired_contract_adapter_attempt
pullback_projection_attempt
pullback_membership_iff_attempt
fixed_domain_supplies_pullback_attempt
projected_membership_does_not_certify_fixed_domain_attempt
```

pullbackDomain={x | project(x)∈Q} 只表达投影包含；其 wholePath 与逐时投影包含
定义等价。指定 D 的 wholePath 加 projection 可以推出 pullback wholePath，反向
不成立。现有反例 Q=univ、project=id、path(t)=t、D(t)=Iic(0) 在 t=1 失败。
这是逻辑域反例，不声称它是物理 DH 轨迹。

## 2. 较宽 consumer 的义务不可被包装抹去

另完整阅读 INITIALPATHCAPS、ACTUALSTORAGEALIGN、ALIGNEDPATHCAPCONSUMER 与
PATHCONTRACT。其结构可保留，但本轮不选择较宽闭包作为最小复用入口。

INITIALPATHCAPS 的 IntegratedGrowth 是已积分上界的输入，不是积分定理。
PATHCONTRACT 使用 initial、growth、on-path value、逐时 budget 得出 cap；
它没有 D 字段，因为 on-path value 已经承载所需值恒等式。不能据此宣称 physical
domain 不再需要证明：从域上 Alignment 产生 on-path value 时仍必须用到
projection 与 wholePath。ALIGNEDPATHCAPCONSUMER.ConsumerPremises 保留这两项。

ACTUALSTORAGEALIGN.Alignment 要求同一 Q 上 sameMass 与 sameRemainder。
其 actualBase 只是 f=1,h=0 的指定 specialization；不自动等于 active candidate。
实际 source 坐标、完整速度状态、初始集、ODE 存在/延拓、积分增长、whole-path
coverage、物理 DH/数值执行绑定仍外置。结构字段不是已接纳 witness，名称也不
构成 authority key；不能通过选取便利的 D、Q、F/G 代替真实源契约。

## 3. Import / placeholder / axiom 风险

- PATHREASSIGNED → PATHDOMAINPROJECTION → Mathlib。没有直接导入 storage/source
  adapter，但传递闭包仍包含完整 Mathlib；一行 import 不表示最小 Mathlib 闭包。
- 窄 sidecar 主要使用记录投影、函数应用、rfl、已有 theorem；需后续核对当前
  pinned 环境的 import resolution、隐式参数、Set membership 定义归约。
- 对所读六份 Lean 文本扫描未见 sorry/admit/axiom/native_decide/unsafe/
  implemented_by 标记。没有解析 AST 或执行 #print axioms，也未检查完整依赖树；
  因此不把文本扫描升级成“无额外公理”。Prop 结构中的显式假设不是 placeholder，
  但它们的实例尚未交付。
- 较宽 PATHCONTRACT 闭包进一步进入 ActualStorage/ActualShift，本轮只读取其
  alignment adapter，不宣称检查这些上游源码、公理或 OLean。

## 4. 旧 receipt 的有限可用范围

阅读 `agent_review_inbox/review-T-P4-033-O1-body6-slice-lean-receipt-codex-20260908T082220.md`。
该文档报告依赖 PATHDOMAINPROJECTION 与 INITIALPATHCAPS 曾在 Lean 4.32.0
exit 0，并报告 baseline axioms；这是旧 receipt 的陈述，不是本轮运行结果。
本轮未重演其中命令，未核查原始日志、OLean 或 toolchain/mathlib pins。

PATHDOMAINPROJECTION 的当前完整 SHA 与 receipt 一致：
`f55de2b76ed401e7962b1494d02826c8fc2f951d7137f02461edeb56d5757d62`。
INITIALPATHCAPS 当前完整 SHA 为
`5cad04f2e8b0af13c8d8a099455812fe1f6d17a66a0d567be5b85963252d224f`，
而该 receipt 的对应字符串缺少末尾 f，只有 63 位。因此不能称该字段为匹配的
完整 SHA-256；本轮不修旧 receipt。此问题不改变窄 sidecar 的直接依赖选择。

旧成功报告即使完整，也不能代替 PATHREASSIGNED 自身五个声明的编译/axiom
receipt。本轮不作该 sidecar 全库 receipt 不存在的穷尽断言；所读材料不足以
提升它，保持 OPEN_UNCOMPILED/pending。

## 5. 后续最小检查建议（本轮未执行）

先绑定上述候选和直接依赖的精确源 SHA，再在单一 pinned Lean/Mathlib 环境
编译窄 sidecar，保留 command、exit/log hashes、OLean hashes 与五个声明的
#print axioms。不得借目录里已有 .olean 推断当前源通过。
只有实际 elaboration 错误出现时才做局部新 repair；当前静态审阅没有依据要求
扩大数学命题、添加公理或重写 dependency。

本 review 只建议 metadata/后续检查，不执行 workflow、integrator 或 registry
promotion。即使编译成功，也不产生 sourceCap、projection 或 wholePath 实例。
