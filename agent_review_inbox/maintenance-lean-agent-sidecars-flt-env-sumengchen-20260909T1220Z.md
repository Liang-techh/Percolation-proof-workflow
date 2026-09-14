# 仓库维护记录：Anthropic FLT quotient sidecar 构建环境修复

- agent/source_agent: 苏梦辰
- scope: 仓库构建、pinned Lean/Lake 环境、GitHub Actions 可运行性
- 数学结论/registry: 未修改
- admission: pending CI；仓库能跑不等于证明完成

## 真实失败

默认分支 `Lean agent sidecars` Actions run `34344777191` / job `102443766956` 的 `Run portable agent sidecars` step 中，命令路径实际为：

```bash
LAKE_ROOT="$GITHUB_WORKSPACE/upstream/mathlib-flt-quotient" \
  bash examples/anthropic_flt_quotient_transport_sidecar/verify.sh
```

该 focused sidecar 返回 exit code `2`：

```text
BUILD_ENV_BLOCKED: toolchain mismatch: sidecar=leanprover/lean4:v4.33.1 lake_root=leanprover/lean4:v4.33.0
SIDECAR_RESULT=FAIL path=examples/anthropic_flt_quotient_transport_sidecar/verify.sh exit_code=2
```

这不是 theorem/proof 失败，而是仓库级 replay 环境绑定错误。sidecar 的来源是 Anthropic FLT commit `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`；该项目的 `lean-toolchain` 为 Lean `4.33.1`，其 `lake-manifest.json` 同时固定 Mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d`。但旧 workflow 直接把这个 Mathlib revision checkout 成 Lake root；该 Mathlib commit 自己的 standalone `lean-toolchain` 是 Lean `4.33.0`，因此 verifier 在进入 Lean 编译前就正确拒绝了环境。

## 最小修复

1. `examples/anthropic_flt_quotient_transport_sidecar/verify.sh`
   - commit: `2625d9429ac2957376ca3c8203fec2cdb80e71a8`
   - 保持 sidecar pinned toolchain `leanprover/lean4:v4.33.1` 不变。
   - `LAKE_ROOT` 改为要求指向 pinned Anthropic FLT project root。
   - 新增 Anthropic FLT root commit `aa2d8b...` 检查，并继续检查 manifest 中存在 pinned Mathlib `db584c...`。
   - 保留 `-DwarningAsError=true`、placeholder scan、`sorryAx` audit 和全部 theorem axiom report gate。

2. `examples/anthropic_flt_quotient_transport_sidecar/README.md`
   - commit: `e1bdaa8fa7ef7ae9a21b983053642a038b17ec1e`
   - 明确区分“upstream FLT project toolchain = 4.33.1”与“其 Mathlib dependency commit standalone toolchain = 4.33.0”，避免再次把 raw dependency root 当成来源项目的 replay root。

3. `.github/workflows/lean-agent-sidecars.yml`
   - commit: `4a797da28b39175da1f925e37e7fac450581ef59`
   - 不再 checkout raw Mathlib 作为该 sidecar 的 `LAKE_ROOT`；改为 checkout `anthropics/fermats-last-theorem@aa2d8b...` 到 `upstream/anthropic-flt`。
   - bootstrap 时检查 FLT commit、Lean `4.33.1`、manifest 中的 Mathlib `db584c...`，再执行 `lake exe cache get`。
   - focused runner 改为：

```bash
LAKE_ROOT="$GITHUB_WORKSPACE/upstream/anthropic-flt" \
  bash examples/anthropic_flt_quotient_transport_sidecar/verify.sh
```

没有关闭测试、没有降低 warning/error gate、没有加入 `sorry`/`admit`、没有修改 Lean theorem statement 或数学语义。

## 真实验证状态

修复后的 `Lean agent sidecars` run `34350320823` 已由最终 workflow commit `4a797da...` 触发；写本记录时状态仍为 `pending`，因此当前**不宣称 compile PASS / axiom PASS / workflow green**。下一轮优先读取该 run 的真实 job/step 日志；若仍失败，只按新的实际 command/exit code/file/line 继续最小修复。

注意：aggregate sidecar workflow 中还有若干其它 theorem/proof-specific FAIL（例如 `sorryAx` 或具体 Lean module/proof 失败）；这些不通过降低 aggregate gate处理，也不在本次环境修复中冒充已解决。

## 可复现 focused 路径

在仓库根目录准备 pinned upstream FLT checkout 后运行：

```bash
LAKE_ROOT="$PWD/upstream/anthropic-flt" \
  bash examples/anthropic_flt_quotient_transport_sidecar/verify.sh
```

预期环境必须同时满足：FLT root commit `aa2d8b...`、Lean `4.33.1`、FLT manifest 记录 Mathlib `db584c...`。

当前结论仅为：**仓库级 replay 环境错误已提交修复，等待真实 CI 验证；待梁智炜最终整合。**
