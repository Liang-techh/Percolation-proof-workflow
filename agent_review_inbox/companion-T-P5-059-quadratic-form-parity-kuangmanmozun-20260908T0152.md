---
kind: companion_log
task_id: T-P5-059-QUADRATIC-FORM-PARITY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T01:52:00-06:00
claim_commit: 5f2521916f14c407e251defdc2c2eab7186ef556
review_commit: 66c23f3876ad086ff695ea610389deab786f7a0f
review_path: agent_review_inbox/review-T-P5-059-quadratic-form-parity-kuangmanmozun-20260908T0148.md
status: mathematical_child_complete_integration_pending
---

# 狂蛮魔尊协作留言 — T-P5-059

- 当前完成：补上 T-P5-057 的 signed primitive 与 T-P5-058 的 square-only consumer 之间的 mixed quadratic-form 缺口。若多个 normalized primitives 共享一个会换号的零因子，真正危险的只有“balanced 且奇偶阶不同”的交叉项。
- 核心判据：把 balanced indices 按 `m_i` 奇偶拆成 even/odd 两组。对称二次型 `u^T K u` 在零接触处对任意 reduced contact data 都可移除，当且仅当 balanced block 的 even-odd cross block `K_EO=0`；等价于 parity conjugation `P K_BB P = K_BB`。
- 精确 jump：左右极限差为 `4 v_E^T K_EO v_O`。因此某个具体轨迹点可以偶然抵消，但若没有额外 source theorem，不能把这种点态偶然抵消当作 robust certificate。
- 反例：`A1=t^2,G1=t` 与 `A2=t^4,G2=t^2` 的两个平方都恒为 1；取正定 `K=[[1,1/2],[1/2,1]]`，二次型却是 `2+sign(t)`，左右极限分别 3 和 1。说明 square-only PASS 不能直接升级为 mixed quadratic PASS。
- 反方向结果：若 balanced components 全部同奇偶（尤其全部 odd），即使每个 signed primitive 自己跳变，整个二次型仍可完全不变；因此要求每个 primitive 连续又过强。
- 给梁智炜/后续 Agent 的建议：zero-contact consumer 应按 signed/linear、diagonal-square、mixed-quadratic 三类分流；mixed quadratic 使用本任务 parity-block gate。实际 deployed `K`、factor discovery、Float64、coverage 和 Lean receipt 仍保持 open。
- 最小 Lean 叶：先做两通道 `Qplus-Qminus=4*c*x*y`、`c=0` invariant、`K=[[1,1/2],[1/2,1]]` regression、all-odd invariant；随后再上 finite-index parity conjugation。
