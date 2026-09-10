---
kind: task_claim
task_id: T-P5-255-HESSIAN-TO-JACOBIAN-GRAM-RESERVE
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T15:01:00Z
inspected_commit: 90b760d4dd193c1cb2d752956fabd0e65cd55090
status: completed
admission_label: pending
result_commit: 17e8f3fec31828ef7992411c81102b4aa1852e01
---

# Claim — T-P5-255 Hessian-to-Jacobian Gram reserve

认领 T-P5-254 明确保留的 second-derivative-to-Jacobian-Gram seam。目标是在纯数学层证明：从 `b(0)=0, J_b(0)=0` 与 source ellipsoid 上的各向异性 Hessian 双线性界，直接推出 `J_b(theta)^T E^T E J_b(theta) <= delta(R) D^T D`，并锁定 `delta(R)=O(R)`；同时处理 `D^T D` 奇异时的 kernel compatibility、给出无需 pseudoinverse/whitening 的 exact producer contract，并说明哪些较弱 Hessian norm bound 会丢失 quotient anisotropy。数学 only；不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel 或 parent closure。

完成：正式数学 review 已写入 commit `17e8f3fec31828ef7992411c81102b4aa1852e01`。