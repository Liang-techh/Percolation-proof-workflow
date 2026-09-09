---
kind: companion_log
review_id: review-T-P5-194-correlated-zonotope-defect-adapter-guyuefangyuan-20260909T2328Z
task_id: T-P5-194-CORRELATED-ZONOTOPE-DEFECT-ADAPTER
source_agent: 古月方源
created_at: 2026-09-09T23:30:00Z
review_commit: f6a493131c273ba0739ede6c2f7a986b71660ae1
admission_label: pending
---

# T-P5-194 中文协作接力

本轮把 T-P5-193 明确留下的“相关残差不要先膨胀成独立坐标 box”缺口闭合成一个固定方向 zonotope 叶。若真实 source 能给出同键

`rho = Z diag(H e+h0) xi`, `|xi|<=1`, `H e+h0>=0`,

请优先保留 `Z`，不要只导出坐标半宽。对任意方向 `w`，精确 worst case 是

`|Z^T w|^T(H e+h0)`，

而坐标 box hull 只给较松的 `|w|^T|Z|(H e+h0)`。

对 finite-value cone `N e>=0`，直接生成 `S=|N Z|`，然后检查

`N A-S H=Lambda N`、`Lambda` 非对角元非负、`N c>=S h0`。

对 T-P5-192 selector，请生成 `F=Z^T G`，按 `Sigma F e>=0` 划 latent sign sector；每个 sector 仍只是 polyhedral cone，最坏 defect 可精确展开成二次项加一次项，然后直接复用已有 copositivity checker。

一个必须保留的回归是 `Z=(1,1)^T`、`n=(1,-1)`：真实 zonotope 在该 normal 上 worst defect 恰为 0，但坐标 box hull 给 2。若 producer 在这类方向上先丢掉共享 latent sign，会产生纯粹由 enclosure 引入的假 FAIL。

建议后续 source/CSE lane 先回答一个最小问题：部署 residual 是否天然存在少量共享 perturbation/FD/solver latent directions，可否在同一 cell 上绑定固定 `Z` 与 affine nonnegative amplitudes。若只有 componentwise interval 而没有共享 latent 语义，不要反向臆造 zonotope。Lean lane 可先落 `zonotope_sup_dot`、`zonotope_support_le_coordinateBoxHull` 与 sign-sector quadratic expansion；Metzler 部分直接复用 T-P5-191，不必复制证明。

尚未闭合：真实 `Z,H,h0` source、外包络的 rounding/coverage、actual sector cover、copositivity 实例、Float64/P8/M4、Lean/kernel、封不觉独立验证及 admission/registry。