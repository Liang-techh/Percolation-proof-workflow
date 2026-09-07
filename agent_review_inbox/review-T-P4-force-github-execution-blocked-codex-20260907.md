---
kind: execution_block_handoff
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
date: 2026-09-07
status: BLOCKED_WORKFLOW_NOT_LANDED
---

# Force runtime execution blocker

本轮只检查 GitHub Actions 执行入口。GitHub 已登录且 Actions 页面可访问，但当前仓库 `Liang-techh/Percolation-proof-workflow` 的 workflow list 仅显示：

```text
Lean agent sidecars
Workflow tests, Harris replay, and local-FKG verification
```

force `workflow_dispatch` job 不在当前 Actions list，因此没有可触发的 Julia runner。未提交 workflow、未触发其他 workflow、未生成 CSV/receipt，也未将 pending 改为 PASS。

Evidence page:

```text
https://github.com/Liang-techh/Percolation-proof-workflow/actions
```

## Minimal handoff to unblock

1. 将既有 handoff 中的 job 落地为：

```text
.github/workflows/force-general-state-export.yml
```

2. 设置 repository variables：

```text
DEPLOYED_SOURCE_REPOSITORY=<owner>/<deployed-dhport-source-repository>
DEPLOYED_SOURCE_REF=<frozen deployed-source ref>
```

3. 在 Actions 页面选择 `force-general-state-export`，执行 `Run workflow`。

4. 仅接收该 job 上传的完整 artifact：16-row CSV、runtime receipt、worker stdout/stderr/exit-code、verifier stdout；验收字段仍必须同时满足既定 source/exporter hash、`B=[4,5]`、`D=[1,2,3,6]`、完整 schema、exit 0、`MAX_E1/MAX_E2 <= 1e-12`。

恢复执行时沿用：

```text
agent_review_inbox/review-T-P4-force-github-job-handoff-short-codex-20260907.md
```

本文件是执行阻塞记录，不是 runtime receipt；不修改 strict gate，不修改主 state，不声称 deployed tau 等价。
