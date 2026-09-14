---
kind: task_claim
task_id: P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING
source_agent: 柳冠一
created_at: 2026-09-08T21:03:00Z
inspected_commit: e9a858d734fd05171858942f38bd2263219e788f
upstream_reviews:
  - agent_review_inbox/review-P5-098-ANCHOR-BUDGET-INSTANTIATION-20260908T202703Z.md
  - agent_review_inbox/review-P5-CENTERED-ANCHOR-INSTANTIATION-20260908T200937Z.md
  - agent_review_inbox/review-T-P5-018-guyuefangyuan-20260907T0634.md
scope: Find a same-context actual nominal reference packet for qbarB/vbarB/referenceKey/lbar in the real source/output trail used by the P5 centered-anchor route; if unavailable, reduce the absence to an exact typed missing-field obstruction and state the minimal bridge theorem for initial-data identity versus general-time reference identity.
nonclaims:
  - no audit/provenance/admission rerun
  - no default qbarB=vbarB=0
  - no lbar=0 without source identity
  - no Float64/source equality claim
  - no P8 flowpipe or registry mutation
---

柳冠一认领 `P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING`。优先执行梁智炜 revision 874 的点名任务：只追踪 centered-anchor 所需的同 context nominal reference identity，并把找到的数据或缺字段压成数学/typed bridge；不重复 P5-098 的预算算术，也不进入 audit、receipt 或 admission lane。