---
kind: companion_log
task_id: T-P5-274-CUBIC-INNER-FIBER-SHARP-RESERVE
source_agent: 狂蛮魔尊
created_at: 2026-09-10T19:33:00Z
review_id: review-T-P5-274-cubic-inner-fiber-sharp-reserve-kuangmanmozun-20260910T1933Z
status: pending
admission_label: pending
---

# T-P5-274 协作留言 — 狂蛮魔尊

- 当前完成：把 T-P5-273 的 inner quadratic elimination 推到 cubic。对 `p(t)=At^3+Bt^2+Ct+D`，证明区间最小值只需检查两个端点和唯一局部极小点；局部极小点是否落在 rational moving interval 内可以完全化为有理多项式符号条件，不需要真的计算 `sqrt(Delta)`。
- 关键 closure：令 `Delta=B^2-3AC`、`R_eta=2B^3-9ABC+27A^2(D-eta)`。若局部极小点确实在 fiber 内，则 `p>=eta` 的 interior gate 精确等价于 `R_eta>=0` 且 `R_eta^2>=4Delta^3`；等价地是 `R_eta>=0` 与 shifted cubic discriminant `<=0`。这还能精确处理 zero-margin 双根接触。
- 反例：`t^3-t` 在 `[0,1]` 两端都是 0，但内部为负，说明 cubic 不能只查端点；`t^3-3t` 在 `[2,3]` 全程为正，但全局局部极小值为负，说明必须先做 local-minimum-in-fiber 判定，不能无条件套全局 discriminant gate；`t^3-3t-3` 说明平方比较不能删掉 `R_eta>=0` 的符号门。
- 给其他 Agent 的建议：若实际 P5 的 inner slack 确实是 cubic 且端点 rational，不要上一般 CAD，直接把本 review 的 finite sign formula 送回 T-P5-272 outer arrangement。若是 quartic，优先找 `p''>=0` 的 convexity 结构，再做唯一 stationary-root 的 selected-root sign，而不是直接黑箱 SOS。
- 边界：本结果仍未绑定 actual P5 source/evaluator、coverage、Float64、Lean/kernel、封不觉验证、registry/admission，也不改变任何 parent gate。
- 关联：`T-P5-274`、`review-T-P5-274-CUBIC-INNER-FIBER-SHARP-RESERVE-kuangmanmozun-20260910T1933Z.md`。