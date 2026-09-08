---
kind: companion_log
review_id: companion-T-P4-040-divfree-liuguanyi-20260907T1819
task_id: T-P4-040
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T18:19:00-06:00
related_review: review-T-P4-040-divfree-liuguanyi-20260907T1816
admission_label: pending
---

# T-P4-040 companion — 柳冠一

已完成 revision 742 对柳冠一的定向任务：把 T-P4-039 的 common-parameter 数学压缩为四个 division-free ordered-ring theorem。

关键缩减：`young_radius_poly_nonpos` 只需要 `A>0` 与两条平方不等式；`theta>0`、`P>=0`、`G>0`、`s>=0` 不应错误塞进该核心 theorem。inner interval 也已改写为 `G-s <= 2*A*theta <= G+s`，所以 trusted core 不需要 `(G±s)/(2A)` 的除法。

新增 reserve 形式为 `center^2 <= s^2`、`s^2+4*A*theta*m <= Delta` 推出 `q(theta)+theta*m<=0`；再由 T-P4-038 的已有乘法恒等式，在 `theta>0` 时恢复实际 Young reserve `>=m`。

Rat/Real 边界建议统一为：checker 输出 exact `ℚ` witness，四个 theorem 尽量泛化到 `LinearOrderedRing`，物理 consumer 直接在 `ℝ` 上用同一 rational coercion 实例化；禁止 `Rat -> Float64 -> Real`。

另发现任务标签碰撞：仓库已有更早的 `T-P4-040-RATIONAL-LAMBDA-GUARD` sibling。最新 revision 742 又把短标签 `T-P4-040` 派给本 child。建议 DAG 使用独立 key `P4.common_lambda_division_free_core`，保留两份历史，不互相覆盖。
