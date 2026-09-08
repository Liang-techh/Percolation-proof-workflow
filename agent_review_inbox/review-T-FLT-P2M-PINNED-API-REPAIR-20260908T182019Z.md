---
kind: review_result
review_id: R-FLT-P2M-PINNED-API-REPAIR-20260908T182019Z
task_id: T-FLT-P2M-PINNED-API-REPAIR-20260908
source_agent: Codex-P2M-interface-lane
created_at: 2026-09-08T18:20:19Z
inspected_commit: 713c4b73b17a796a43039303d3b0e961b696642e
inspected_path: examples/anthropic_flt_reusable_lean
status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
registry_eligible: false
registry_promoted: false
lean_run: false
lake_run: false
remote_compile_run: false
kernel_checked: false
axioms_checked: false
comparator_accepted: false
formal_certificate_allowed: false
requested_action: catalog_pending_metadata_only
---

# Immutable P2M pinned API repair result

本 envelope 记录当前候选字节与未执行边界。发布后不覆盖；修订应新增 review_id，
并引用本文件及其外部计算的 SHA-256。inspected_commit 是读取时工作区 HEAD，
不宣称下列新文件已经包含于该 commit；文件身份由逐项 SHA-256 绑定。

## 问题与实际交付

旧 AnthropicFLTReusable 的轻量 gate 缺少 upstream statement-universe 检查，
revert 未显式保留 clearAuxDeclsInsteadOfRevert。新增候选用独立 syntax names
恢复这两处契约；不修改旧实现或默认 lake roots，不依赖 Mathlib。
分类：light adaptation / 未编译实现候选，**不是 compiled_candidate**。

## 实际文件 SHA-256

以下路径均相对仓库根目录，common directory 为
`examples/anthropic_flt_reusable_lean/`；哈希绑定实际读取字节，不做换行归一化。

| 该目录内文件 | SHA-256 |
|---|---|
| NEW_P2M_PINNED_API_20260908.lean | 2e65de0017dafe65660b24b9f783b5571c074ff5f4dc183f5c64f2ac217a656b |
| NEW_P2M_PINNED_Probe20260908.lean | 9c6cc1eb3d53e35fddec31dc664af2a5d777da5304eb93f2fbf571035c99352d |
| NEW_P2M_PINNED_NegSpecialization20260908.lean | a6a5e9f17fdd0c46da7603f0d39d3a76bfc7a4d242ec3579d9891c7414ae11ae |
| NEW_P2M_PINNED_NegMerge20260908.lean | e59332e84f49d12762fe94c5d958519337e517c74b15de149ae5fb46626abc20 |
| NEW_P2M_PINNED_NegMismatch20260908.lean | e134cbbd9de2fdc40f16124ff445029a658b672128506f32c397d9af9b2b2f8d |
| REVIEW_P2M_PINNED_API_HANDOFF_20260908.md | 532d31d525ba4ca0a2f144a3dc82ccd422b94b52700c998ebf2326be7d8e6f8b |

## 精确 upstream provenance

```text
repository: https://github.com/anthropics/fermats-last-theorem
commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
path: P2M/Util.lean
git_blob: 0a73367f78bc165bb5d35e42ca14f5055252e7f6
source_toolchain: leanprover/lean4:v4.33.1
target_toolchain: leanprover/lean4:v4.33.1
source_mathlib_revision: db584cd6d46c92f209a44c0f1c829460d327499d
target_mathlib_dependency: none
license: Apache-2.0
copyright: 2026 Anthropic, PBC
```

源 Mathlib pin 仅为 provenance；本 API 唯一直接 import 是 Lean，其余四个 probe
只 import 新 API。保留 intake LICENSE/NOTICE/ATTRIBUTION；source commit 不替代
adapter hashes。旧文档 URL `anthropics/anthropic-fermats-last-theorem` 与已读 origin
不一致，本轮不猜测 redirect，也不修改旧文档。

适配差异：新 tactic `p2m_pinned_exact_reverting`、新 command
`#p2m_pinned_type_eq`、新诊断前缀；保留 upstream 的 auxiliary-declaration revert
选项及 universe 特化/合并拒绝逻辑。不复制 namespace/export helper 或数论证明。

## Probe 预期与真实执行状态

所有行的 actual_run=false、actual_exit_code=null、actual_diagnostic=null。
下表只是后续 runner 的验收预期，**没有一个 probe 已经实测通过或失败**。

| 文件角色 | 预期退出 | 必须检查的预期证据 |
|---|---|---|
| API | 0 | pinned Lean 下正常 elaboration/编译 |
| Probe | 0 | 两条 P2M_PINNED_TYPE_EQ；依赖上下文、多目标、局部 let/have 正例完成；保留三个 #print axioms 的真实输出 |
| NegSpecialization | nonzero | P2M_PINNED_UNDERGENERAL，拒绝将 statement universe 专化为 Type 0 |
| NegMerge | nonzero | P2M_PINNED_UNDERGENERAL，拒绝合并两个独立 statement universes |
| NegMismatch | nonzero | P2M_PINNED_TYPE_MISMATCH，拒绝 Nat → Nat / Bool → Bool 类型差异 |

负例 nonzero 若来自 module-not-found、syntax error 或其他 elaboration failure，
不算 gate 测试通过。不得将三个 expected-failure 模块放入必须全成功的默认 build。
正例无警告/无 axiom 字样也不等于公理清单为空；必须实际运行 #print axioms 并审计。
expression-mvar 专用负例和 implementation-detail auxiliary 专用测试仍未交付；
localLet 不代替这两个测试。通过未来矩阵也不证明 metaprogram 的普遍正确性。

## 实际检查、命令与退出码

封装轮只运行只读 shell 检查，没有 Lean/Lake/verify.sh/远程 job。

- `Get-FileHash examples/anthropic_flt_reusable_lean/NEW_P2M_PINNED_*.lean, examples/anthropic_flt_reusable_lean/REVIEW_P2M_PINNED_API_HANDOFF_20260908.md | Format-List Path,Hash`：所属 shell 调用 exit 0；得到上表六项 hashes。
- `git rev-parse HEAD`：所属 shell 调用 exit 0；得到 inspected_commit。
- `Get-Content agent_review_inbox/README.md` 及已有 envelope 的定点阅读：shell exit 0；用于对齐 kind/review_id/admission 字段。
- 先前实现轮文本扫描只见 import 和显式 #print axioms；未见 sorry/admit/new axiom/native_decide/unsafe。那是源码扫描，不是 kernel 检查。

历史真实失败单独引用：
`artifacts/task_FLT_quotient_currentpin_20260908/COMPILE_LOG.txt`，SHA-256
`b5d4f99c87065b1c526848f4e3004a73f21515fa6c1787ce694678bf57e87807`。
历史日志记录 `UpstreamImportProbe.lean:5:0: error: unknown module prefix 'P2M'`，
命令 `lake env lean -DwarningAsError=true UpstreamImportProbe.lean`、exit 1。
本轮没有重放；它不是这些新文件的编译结果，也不是 CLM theorem 的失败或通过记录。

## Integration request / admission boundary

仅将本 task/result 与六个 hash 作为 pending 外部复用候选元数据登记，关联
`REVIEW_P2M_PINNED_API_HANDOFF_20260908.md`；下一步是另获授权的隔离 pinned runner。
本轮不运行 intake/integration 脚本、不修改 state、registry 或现有 theorem DAG。

registry_eligible=false。不能把本 envelope、静态 closure、历史日志或未来 probe 成功
升级为 BODY5 q3、BODY6 path contract、quotient CLM、Poincare/PDE 验证。
编译、公理审计、comparator 与 registry promotion 必须分别绑定实际新证据。
