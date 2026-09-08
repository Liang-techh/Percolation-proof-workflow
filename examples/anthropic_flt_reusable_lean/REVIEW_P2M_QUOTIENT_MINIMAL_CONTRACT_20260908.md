# Poincare follow-up 2：P2M / quotient 最小 reusable contract

状态：REVIEW_ONLY / NOT_VERIFIED_THIS_TURN。只定点读取现有 sidecar、scan handoff
和两个固定 upstream Git blob；没有整仓扫描，没有运行 Lean/Lake、verify.sh 或远程任务。
本轮唯一写入为本 review；不修改实现、registry、state 或共享 adapter。

## 结论与分类

可独立于 Mathlib 构建的最小交付应是 **Lean-only proof-card 工具契约**，不是 quotient 定理。
quotient/CLM 保留为另一个依赖锁定 Mathlib 的小型 consumer；可复用匹配的依赖缓存、
只编译目标闭包，但不能称其“不依赖 Mathlib”。缺缓存时不自动回退整仓编译。

| 候选 | 分类 | 目标侧最小接口 |
|---|---|---|
| upstream `p2m_exact_reverting` | 轻改；upstream 的完整实现可作直接复用基线 | `import Lean`，接受 proof term，按顺序 revert 非实现细节局部声明，针对新目标 elaboration，拒绝剩余 expression metavariables，赋值当前目标 |
| upstream `#p2m_type_eq` | 轻改；当前 sidecar 弱化了契约 | 两个全限定声明名 → 类型可定义相等检查 + statement universe 不被专化/合并；失败必须报错 |
| `Submodule.Quotient.continuousLinearEquiv` | 类型契约可直接复用；目标名字/import 轻改 | 给定 e 与子模精确 map 等式，返回商空间 CL equivalence |
| `Submodule.quotientPiContinuousLinearEquiv` | 轻改 | 有限指标、逐分量拓扑模与子模 → product quotient CL equivalence；逆映射 continuity API 适配 |
| P2M proof-card → provenance → admission 分层 | 架构借鉴 | 将 API/type check、数学证明及注册动作分开；不将工具成功日志视为数学证书 |

## 固定 upstream 与归属

本轮以本地源仓库 origin 和固定 Git object 为准：

```text
repository https://github.com/anthropics/fermats-last-theorem
commit     aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
Lean       leanprover/lean4:v4.33.1
Mathlib    db584cd6d46c92f209a44c0f1c829460d327499d

path       P2M/Util.lean
Git blob   0a73367f78bc165bb5d35e42ca14f5055252e7f6

path       Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean
Git blob   eab66288efedd1e634203abb927805413a716aa7
```

可定位到 immutable source 的链接：
[P2M/Util.lean](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/P2M/Util.lean)，
[Quotient.lean](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean)。
链接根据已读 Git 对象组成，本轮未测试 HTTP 可达性。

现 AnthropicFLTReusable.lean / README / ATTRIBUTION 的仓库 URL 写作
`anthropics/anthropic-fermats-last-theorem`，与本地 origin/scan 不一致。
不猜测这是重命名或 redirect；新 provenance 应记录 canonical origin、原文本 URL
和此差异，不在本轮改旧文件。

Apache-2.0：保留 LICENSE、NOTICE、ATTRIBUTION。P2M 工具归属 upstream Anthropic
仓库（NOTICE：Copyright 2026 Anthropic, PBC）。quotient 文件的第三方来源由
ATTRIBUTION.md 第 53 行指定：整个文件来自
`FLT/Mathlib/Topology/Algebra/Module/Quotient.lean`，© 2025 Salvatore Mercuri，
authors Salvatore Mercuri、Kevin Buzzard、Pietro Monticone。
不能把 quotient 全部归给 Anthropic；也不为 Imperial 原始文件编造未查到的独立 commit。

## 当前 P2M sidecar 的两个具体差异

检查对象：`AnthropicFLTReusable.lean`，当前文件 SHA-256：
`481d8ebe4c3077d071231795a013e4b6d2cc90675c795ccbfb77b45a40c3d3ca`。

1. `g.revert`：upstream 同时指定 `preserveOrder := true` 和
   `clearAuxDeclsInsteadOfRevert := true`；当前 sidecar 只指定前者。
   因此不能宣称 auxiliary/local declaration 行为与 upstream 完全相同。
   最小 contract 应保留第二选项，或明确限制到无 auxiliary-declaration 的输入上下文，
   并用 focused probes 检查差异。不能靠现 Nat/rfl 示例证明一般上下文适配。
2. `#p2m_type_eq`：upstream 在 `isDefEq` 后检查 statement universe 参数是否被固定，
   或两个参数是否被识别成同一个 level；当前 sidecar 完全省略该段。
   因而当前成功日志只表明 fresh universe metavariables 下匹配成功，
   不足以证明 proof 与 statement 一样泛化。
   建议未来复用 upstream 的 `P2M_UNDERGENERAL` fail-closed gate，
   而非将现 gate 直接提升为完整契约。此处不实现修复。

该 gate 本身是 metaprogram 检查，不是“两个 theorem 已被 kernel 验证”的替代品。
即便保留 upstream universe 检查，也仍需输出声明的真实类型和依赖公理审计。

最小未来 probe contract（本轮不执行）：

- 正例：closed proof、带依赖假设的上下文、确实泛化的 universe-polymorphic pair。
- 反例：类型不同、proof universe 仅在 statement 专化/合并后可匹配、剩余 expression mvar。
- revert 边界：局部 let/auxiliary declaration、多个活跃 goals；确认只处理当前目标，
  不遗失其余目标；错误是否 fail closed 由实际 Lean runner 记录。

## quotient 目标侧 exact contract

第一项保留以下全部输入，不暗加规范结构：

```lean
{R : Type*} [Ring R] (G H : Type*)
[AddCommGroup G] [Module R G] [AddCommGroup H] [Module R H]
[TopologicalSpace G] [TopologicalSpace H]
(G' : Submodule R G) (H' : Submodule R H)
(e : G ≃L[R] H) (h : Submodule.map e.toLinearMap G' = H')
-- output: (G ⧸ G') ≃L[R] (H ⧸ H')
```

第二项：

```lean
{R ι : Type*} [CommRing R] {G : ι → Type*}
[(i : ι) → AddCommGroup (G i)] [(i : ι) → Module R (G i)]
[(i : ι) → TopologicalSpace (G i)]
[(i : ι) → IsTopologicalAddGroup (G i)] [Fintype ι] [DecidableEq ι]
(p : (i : ι) → Submodule R (G i))
-- output: (((i : ι) → G i) ⧸ Submodule.pi Set.univ p)
--           ≃L[R] ((i : ι) → G i ⧸ p i)
```

有限指标不等于每个 G i 有限维；第一项不要求 IsTopologicalAddGroup，
第二项明确要求。两者均不返回 norm equality、isometry、Sobolev norm bound 或 Poincare 常数。

现目标实现位于 sibling `anthropic_flt_quotient_transport_sidecar/`
`NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean`，namespace `FLTQuotientCLMAPIRepair`。
目标记录为 Lean v4.33.1 / Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`，
与 upstream Mathlib pin 不同。其两个显式 imports 是
`Mathlib.LinearAlgebra.Quotient.Pi`、`Mathlib.Topology.Algebra.Module.Equiv`。
逆 continuity 的轻改包括 `continuous_finset_sum` → `continuous_finsetSum`、
显式 `Submodule.quotientPi_aux.invFun` / `Submodule.piQuotientLift` 与类型参数。
本 review 没有验证这些接口可编译。

若作为 Poincare consumer，应另外要求代表元计算契约：
`E (Quotient.mk x) = Quotient.mk (e x)`，以及有限积映射逐坐标计算规则。
这两条是建议补交的目标 lemma，不在本轮冒充现有 witness。
均值零子模/常数子模、物理域、边界条件、微分算子、范数与常数保持必须另行绑定。

## 最小 provenance / admission packet

每个 reusable 单元独立记录：

- source repository、commit、path、blob、license/notice/第三方来源；
  adapter 实际字节 SHA、完整改动清单，不能用源 commit 替代 adapter 身份。
- source 与 target toolchain/Mathlib pin 分栏；P2M-only 的 Mathlib 是 provenance-only，
  不应伪报为运行依赖。锁定 Lean distribution 与真实 import search paths。
- 全限定目标名、完整 binder/type/universe contract、显式条件与输出声明；
  除 pretty-print 文本外保留可重放 probe/source 与对应 hash。
- 独立状态记录：source-inspected、elaborated、kernel-checked、axioms-audited、
  comparator-accepted、registry-promoted；缺证据不得以成功默认值填充。

P2M 单元只需 Lean distribution 的匹配模块，不需 FLT 或 Mathlib 工程。
quotient 单元应消费 exact-lock Mathlib 缓存并只编译 adapter/probe；
现 handoff 已记录静态可达闭包 2877 模块，说明“两条 import”不等于“两文件依赖”。
未来 runner 必须核对真实编译解析的依赖与缓存身份；静态 inventory 不是编译 receipt。

现 `verify.sh` 的所谓 axiom audit 只是再次运行 Lean 并 grep 诊断，
被运行的源文件没有显式 `#print axioms`；无 axiom 文本不等于依赖公理清单为空。
未来 admission 必须实际导出目标声明依赖公理，检查 sorryAx / 新公理并按政策分类，
不能仅沿用 `AXIOM_AUDIT=PASS (no axiom/sorry diagnostics)` 标签。

仅获得工具构建成功，不代表一般 proof-card gate 正确；仅获得 quotient consumer
构建成功，不代表 Poincare/PDE/trajectory 定理。编译候选与 registry promotion
必须保持独立。本轮不刷新任何历史验证状态，也不产生新的 admission receipt。
