---
kind: companion_log
task_id: T-P4-033
review_id: review-T-P4-033-joint-defect-metric-liuguanyi-20260907T1422
source_agent: 柳冠一
created_at: 2026-09-07T14:25:00-06:00
status: pending
---

# T-P4-033 协作摘要

本轮补的是 T-P4-032 typed defect convention 之后的联合二次预算接口，不重复 T-P4-024 的 fixed-lambda Young/Schur consumer。

核心结论：若 source 对 typed defect pair `z=(e_D,e_B)` 给出联合二次预算 `<z,Wz> <= E`，且 correction map `C_s=[sT,I]`（O1 用 `s=+1`，force-side 用 `s=-1`）满足 exact-rational PSD 条件 `C_s^*C_s <= mu W`，则直接得到 `||C_s z||^2 <= mu E`。这条路可以保留 source 的相关性和加权结构，不必先把 `T e_D`、`e_B` 各自压成独立 norm cap。

最重要的跨 convention 提醒：correction-only 关系 `d_O=-e_D, b_O=e_B` 对应 `J=diag(-I_D,I_B)`。若 force-side metric 写成 `W_F=[[W_D,X],[X^*,W_B]]`，等价的 O1 metric 必须是 `W_O=J^*W_FJ=[[W_D,-X],[-X^*,W_B]]`。也就是说，联合 metric 有 distal/port cross block 时，切换 defect convention 必须同时翻转 cross block 符号；直接复制同一个 `W` 不是坐标等价。只有 block-diagonal/separable metric 对这个 sign flip 不敏感。

还给了 source-friendly 的 sharp scalar corollary：若 `alpha||d||^2+beta||b||^2<=E`，`||Td||^2<=tau^2||d||^2`，则

`alpha*beta*||±Td+b||^2 <= (beta*tau^2+alpha)E`。

它来自精确平方恒等式

`(beta*tau^2+alpha)(alpha x^2+beta y^2)-alpha*beta*(tau x+y)^2=(alpha x-beta*tau*y)^2`，

所以不需要平方根，且在只知道 `tau,alpha,beta` 时是 sharp 的。

若 `W` 只半正定，还出现一个明确 obstruction：存在 `z in ker(W)` 但 `C_s z != 0` 时，不可能有任何有限 `mu`。source metric 的零收费方向必须同时是 correction map 的零方向。

建议后续由巨阳仙尊只形式化很小的 `joint_metric_pushforward`、`joint_metric_congruence`、`defect_sign_flip_metric`、`scalar_weighted_defect_pushforward_mul`；真实 source metric、`T=M_BD M_DD_inv`、Float64/solve 语义、coverage 与 admission 仍保持 open。
