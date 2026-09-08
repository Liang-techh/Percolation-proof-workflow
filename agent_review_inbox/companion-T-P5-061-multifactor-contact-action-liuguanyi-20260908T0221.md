---
kind: companion_log
review_id: companion-T-P5-061-multifactor-contact-action-liuguanyi-20260908T0221
task_id: T-P5-061
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T02:21:00-06:00
parent_review: review-T-P5-061-multifactor-contact-action-liuguanyi-20260908T0218
parent_review_commit: 98546fee82ce098c58bb9d9d2f7891b2b790e0ba
integration_status: pending
admission_label: pending
---

# T-P5-061 中文协作摘要

本轮补上 T-P5-060 明确留下的多零面交汇缺口。一个 contact 若由多个独立因子 `h_1,...,h_r` 控制，balanced channel 不应只标一个“奇/偶”，而应标一个 `F_2^r` parity mask。真正决定 affine/quadratic/bilinear term 能否跨 contact 安全延拓的，不是全局 mask 本身，而是该 source domain 实际可到达的相对 sign subgroup `H`。

核心结论：定义 `H^perp` 为所有对 reachable flips 都取偶 parity 的 mask，则 affine 系数 `a_i` 只有在 `alpha_i∈H^perp` 时允许非零；二次项 `K_ij` 只有在 `alpha_i+alpha_j∈H^perp` 时允许非零；双线性项同理。若整 cell 能到所有 `2^r` 个 sign chambers，就退化成“affine 只能接 trivial mask，quadratic/bilinear 只能接相同 mask”；若 cell 是 one-sided/fixed-sign，则 `H` 平凡，不需要 parity gate，正好恢复 T-P5-057 的 fixed-sign lane。

特别提醒：同一个 coupling 可以在只跨一个零面的 codim-1 cell 上安全，却在更高 codimension 的零面交点失效。因此以后 source checker 必须把 `active_factors` 和 `reachable_generators` 与 cell/domain key 一起输出，不能把一个单零面证书静默复用到 intersection cell。反过来，也不能对只允许部分 sign chambers 的 domain 强行用 full `Z_2^r` gate，否则会产生假拒绝。

建议后续 Lean 不必一上来形式化群表示。最小 trusted core 可以只消费有限个 relative sign generators，并为每个 channel 保存 `±1` signature；证明 generator-wise affine/quadratic/bilinear invariance iff 即可。factorization→signature 另做独立 child，这样不会把 sqrt/root/source 语义塞进 parity theorem。

当前仍为 pending mathematical/interface child。source factor identity、reachable-side/domain 证明、multi-factor reduced-limit、Float64、P8/first-exit、Lean/kernel、封不觉独立验证和 admission 均未关闭。
