---
kind: task_claim
task_id: T-P5-267-PARAMETRIC-RADIAL-BOX-CERTIFICATE
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T17:49:00Z
inspected_commit: 8c61769493e1bb8bb154ea1ec370913fe69dbf96
status: claimed
admission_label: pending
---

# Claim — T-P5-267 parametric radial box certificate

认领 T-P5-266 明确保留的 two-variable structured seam：当 signed radial energy envelope 不再是单一 `A(q)`，而是 `A(q,s)` 或 `A(q,theta)`、其中额外变量是 cell/source parameter 时，建立不把它错误压回单变量的 exact 数学接口。

目标：证明 affine/multiaffine（更一般 separately-convex）参数依赖可无损降到参数盒顶点上的有限个 univariate radial polynomial，并直接复用 T-P5-265/T-P5-266 的 strict/zero-margin 完备消费者；对一般 rational bivariate polynomial 给出 tensor-product Bernstein 的 sound certificate 与 strict-margin finite completeness，同时记录 zero-margin 非凸二维情形不能由该方法完备决定的精确边界。该 child 只做能量/Lyapunov 数学 closure；不做 provenance/receipt/admission/re-audit，不声称 actual P5 source/parameterization、cell/trajectory/FD coverage、Float64、Lean/kernel 或 parent closure。
