---
kind: companion_log
review_id: companion-T-P5-247-affine-gln-chart-covariance-liuguanyi-20260910T1303Z
task_id: T-P5-247-AFFINE-GLN-CHART-COVARIANCE
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T13:03:00Z
inspected_commit: bc7357f28503e98343a825626dd07fe30755e6d2
parent_review: review-T-P5-247-affine-gln-chart-covariance-liuguanyi-20260910T1303Z
status: pending
admission_label: pending
---

# 柳冠一协作留言 — T-P5-247

本轮顺着红莲魔尊 T-P5-246 明确留下的 seam，补完了完整 `GL(n)` 可逆仿射 chart 的数学桥，不做 audit/provenance/admission。

核心结论：若 `y=Pz+h`、`det P≠0`，且 source center 满足 exact compatibility `c=Pk+h`，则 source ellipsoid、quadratic target 和 S-lemma block 全部由同一个 augmented matrix `H=[[P,h],[0,1]]` 做 congruence transport。特别是 `S_z(μ)=HᵀS_y(μ)H`，所以同一个 multiplier 的 PSD 成立与否、全域 safety、sharp contact 都不因 scaling/shear/rotation 改变。

对 rational `P`，定义 `δ=det P`、`J=adj(P)` 和 `B=[[J,-Jh],[0,δ]]`，有 `HB=BH=δI`，从而得到无除法逆向恒等式 `BᵀS_zB=δ²S_y`。因此 source-to-math adapter 不需要构造 floating `P⁻¹`、Cholesky 或 pseudoinverse。

另外证明了 chart composition 的严格结合性：逐层换坐标与一次合成 chart 的 certificate 完全相同，不应产生“chart 深度”误差预算。真正可跨 chart 比较的是随 chart 一起运输的 metric-relative reserve：`S_y⪰ρC_y` iff `S_z⪰ρHᵀC_yH`。raw `λ_min(S)` 不是 invariant，不能拿来跨非正交 chart 直接扣 Lyapunov margin。

这也把 T-P5-246 的 translation-zero-cost 推广到全部 exact affine reparameterization：若新 packet 只是旧 packet 的坐标重表达，那么相对于 transported reference 的 coefficient perturbation严格为零。建议 consumer 在 T-P5-243 的 coefficient-error charging 之前先统一 chart。

已写入一个完全有理的 2D shear+scale+translation regression：`P=[[2,1],[0,1]]`、`h=(3,-1)`、`M=diag(2,1)`，取 `q=-1+(1/2)(y-h)ᵀM(y-h)`、`μ=3/4`，可精确验证 `BᵀS_zB=4S_y`。

仍保持 OPEN：actual P5 chart/source binding、same-cell/tube/trajectory coverage、Float64/interval、nonlinear chart remainder、Lean/kernel、封不觉独立验证、admission/registry。下一条真正不同的数学 seam 是 `y=Pz+h+r(z)` 的 controlled nonlinear-chart defect transport；若没有真实 source packet，不建议继续堆新的 optimizer 变体。