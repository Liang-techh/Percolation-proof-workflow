# 接管 Lean/API lane：P2M pinned API candidate

本轮优先 FLT/P2M Lean-only seam，新增 API、positive probe、三个独立 expected-failure
probe；不改旧实现、lakefile、verify.sh、BODY5/BODY6、state 或 registry。
状态全部为 OPEN_UNCOMPILED / NOT_RUN；未运行本机或远程 Lean/Lake。

## 最小源契约与修复

固定来源：`https://github.com/anthropics/fermats-last-theorem`，commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`，`P2M/Util.lean`，
Git blob `0a73367f78bc165bb5d35e42ca14f5055252e7f6`。
Apache-2.0 / Copyright 2026 Anthropic, PBC；沿用 intake 的 LICENSE/NOTICE/ATTRIBUTION。
目标 Lean v4.33.1。上游 Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`
仅用于 provenance，不是这五个文件的依赖。

`NEW_P2M_PINNED_API_20260908.lean` 只 import Lean：

- 新语法 `p2m_pinned_exact_reverting` 保留 upstream 的
  `preserveOrder := true` 和 `clearAuxDeclsInsteadOfRevert := true`。
- `#p2m_pinned_type_eq` 恢复 upstream 的 statement-universe 特化/合并检查。
- 新语法和诊断前缀避免与原 P2M sidecar 冲突；未引入原 P2M 的 namespace/export helpers。
- 分类为轻改；不是新数学定理，也不是已证明完善的 metaprogram。

## 可重放 probe 矩阵（期待值，不是实测值）

| 文件 | 期望 | 检查点 |
|---|---|---|
| API | exit 0 | Lean-only API elaboration |
| Probe | exit 0；两个 P2M_PINNED_TYPE_EQ | 单/双 universe 正例、依赖上下文、多个目标、局部 let/have |
| NegSpecialization | nonzero + P2M_PINNED_UNDERGENERAL | 任意 Type u 的 statement 不能由仅 Type 0 的 proof 契约通过 |
| NegMerge | nonzero + P2M_PINNED_UNDERGENERAL | 两个独立 universe 不能为匹配而合并 |
| NegMismatch | nonzero + P2M_PINNED_TYPE_MISMATCH | Nat → Nat 与 Bool → Bool 不匹配 |

完整文件名前缀为 NEW_P2M_PINNED_，后缀为 20260908.lean；API 名称含 API_20260908。
三个负例是有意报错的源文件，不能放进“所有文件必须 exit 0”的默认 build。
仅 nonzero 不算负例通过：必须确认命中指定 gate，而不是 import/syntax/type 错误。
同理，不允许用 warning 或日志 grep 替代正例的成功编译。

Probe 对三个 theorem 显式 `#print axioms`。未来 runner 应保存完整输出，
检查 sorryAx/新公理并按准入政策分类；未实际执行，不能宣称输出为空。
expression-mvar 的负例和真正 implementation-detail auxiliary declaration 的专用测试
尚未交付；localLet 只覆盖普通局部定义，不代替这两个边界。

## 执行契约（后续获授权的 runner，本轮不执行）

在新隔离目录，只放本轮五个文件，使用确切 Lean v4.33.1 distribution；
记录 compiler 版本/身份及所有 LEAN_PATH 条目。无需 Mathlib 或完整 FLT 项目。
不要直接调用旧 verify.sh：默认 lake root 仍是旧 AnthropicFLTReusable。

1. 先将 API 编译成独立输出目录中的同名 .olean，记录 stdout/stderr/exit/SHA。
2. 后续 source imports 仅解析该 fresh API 输出以及 pinned Lean distribution。
3. 单独编译 Probe，再分别执行三个负例；每例独立日志和退出码。
4. 对照上表确认实际 gate 诊断。即使整个矩阵通过，也只标记该 API/probe
   在这个 pin 下的编译/测试状态，不标记 Poincare 或 quotient 已验证。

API 自身直接使用 Lean elaborator internals：revert 参数、Term.withSynthesize、
instantiateLevelMVars、level unification 都有版本敏感性。固定 pin 不等于已消除风险。

## 真实历史失败：与本轮静态风险分栏

只读材料：`artifacts/task_FLT_quotient_currentpin_20260908/COMPILE_LOG.txt`。
当前文件 SHA-256：
`b5d4f99c87065b1c526848f4e3004a73f21515fa6c1787ce694678bf57e87807`。

日志第 20–24 行记录：

```text
COMMAND: lake env lean -DwarningAsError=true UpstreamImportProbe.lean
EXIT: 1
UpstreamImportProbe.lean:5:0: error: unknown module prefix 'P2M'
```

第 29–36 行还记录 P2MUtilProbe.lean 同类 error/exit 1。
这是已存在日志中的实际 import failure，本轮没有重放。
它说明该历史环境缺少源项目 P2M.Util 搜索路径，不说明本轮 fresh Lean-only API 会失败。
该目录处理的是代数 kernel/quotient theorem，不是 continuous-linear-equivalence 文件；
不能把它随后成功的代数 reproof 记录转移为 CLM sidecar 的验证证据。

本轮新增候选没有任何实际编译错误记录；universe/revert 差异是源码对照发现，
不可写作“本轮 Lean 已拒绝旧 gate”。一次 rg 的 Windows wildcard 路径错误已改用 -g
重跑，这是检索错误，不是 Lean failure。

## 与 quotient/BODY5/BODY6 的 admission 隔离

- CLM sidecar 仍需要 target Mathlib
  `0df444a360eaa60ab8c11dca51a86af692955474` 的匹配依赖；本 API 的正负例不能补其 continuity 证明。
- 静态 import closure 不是 elaboration/kernel receipt；旧成功日志不自动绑定新文件。
- BODY5 q3 数据 Perm、BODY6 path/domain/source 参数和几何义务均没有因接管消失。
- 不修改 registry；任何后续编译结果必须与准确源字节、声明、环境、公理报告绑定，
  comparator/registry admission 单独授权和记录。

## 当前字节绑定

```text
NEW_P2M_PINNED_API_20260908.lean
2e65de0017dafe65660b24b9f783b5571c074ff5f4dc183f5c64f2ac217a656b
NEW_P2M_PINNED_Probe20260908.lean
9c6cc1eb3d53e35fddec31dc664af2a5d777da5304eb93f2fbf571035c99352d
NEW_P2M_PINNED_NegSpecialization20260908.lean
a6a5e9f17fdd0c46da7603f0d39d3a76bfc7a4d242ec3579d9891c7414ae11ae
NEW_P2M_PINNED_NegMerge20260908.lean
e59332e84f49d12762fe94c5d958519337e517c74b15de149ae5fb46626abc20
NEW_P2M_PINNED_NegMismatch20260908.lean
e134cbbd9de2fdc40f16124ff445029a658b672128506f32c397d9af9b2b2f8d
```

只做了静态 imports/禁用占位符文本扫描、SHA 和 Git diff；未发现新增文件中的
sorry/admit/axiom 声明/native_decide/unsafe。此描述不代替 parser、kernel 或公理审计。
