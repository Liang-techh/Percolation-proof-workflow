---
kind: companion_log
task_id: T-P4-017
source_agent: 狂蛮魔尊
created_at: 2026-09-07T04:51:00-06:00
related_review: review-T-P4-017-kuangmanmozun-20260907T0449
---

# T-P4-017 协作摘要

- 当前 canonical `docs/routeb-p4-kc-force-contract.md` 把 P4 generalized-force `kc` 固定为 `(q5/20,q4/20)`；因此后续 source-facing block-4 预算应使用 `c=1/20`，不要继续把 `c=1/100` 的历史 normalized toy specialization 当作 canonical 结论。
- `T-P4-014/015/016` 的通用 Schur、slice、aggregate 数学仍可复用；需要替换的是硬编码的 block-4 数值 specialization。
- 在总 `1/4` consumer 下，所有 same-`q5` execution remainder 的共享余量应为 `beta_total<=1/5`，不是 `6/25`。
- 若错误使用 `6/25`，canonical 总系数变为 `29/100`，已经超过 block-4 sharp limit；显式取 `y=1,e=6/25,x=-29/60` 时二次型等于 `-70496999999999/3000000000000000<0`。
- 修正后的统一 source/checker 预算为 `5000000000000000*(1/20+BETA)^2 + 583338333333335*KAPPA <= 350003000000001`。
- 如果仍把总 same-coordinate 系数压到 `1/4`，横向总预算 `KAPPA<=37503000000001/583338333333335` 保持不变；变化的是 same-coordinate headroom，而不是 quarter 边界的 transverse curvature。
- 建议形式化 Agent 复用现有 generic theorem，只新增 `c=1/20, beta=1/5` 的 canonical rational corollary 与 `6/25` failure witness；不要重写整个 Schur sidecar。
