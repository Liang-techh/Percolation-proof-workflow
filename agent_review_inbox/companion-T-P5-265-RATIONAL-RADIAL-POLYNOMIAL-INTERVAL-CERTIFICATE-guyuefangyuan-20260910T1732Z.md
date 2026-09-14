---
kind: companion_log
review_id: review-T-P5-265-rational-radial-polynomial-interval-certificate-guyuefangyuan-20260910T1729Z
task_id: T-P5-265-RATIONAL-RADIAL-POLYNOMIAL-INTERVAL-CERTIFICATE
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T17:32:00Z
inspected_commit: 66ce97393a21d0db9a52f75dc1f271af751fd70c
result_commit: 913ed31d66c77016e82fe2371d3734b033e76e5f
admission_label: pending
---

# 古月方源 — T-P5-265 协作交接

- 当前完成：承接 T-P5-264 的 full-radial-interval seam，把保留 signed same-parity / same-total-degree cancellation 后得到的 `q=Q(u)∈[0,R]` 有理径向多项式，变成 exact Bernstein 区间证书；不再需要用 `q=R` 粗暴替换高阶项。
- 核心恒等式：在有理子区间 `[a,b]` 上，`p(a+(b-a)t)` 的 degree-`n` Bernstein 系数为 `β_i=Σ_{k≤i} [C(i,k)/C(n,k)](b-a)^k p^(k)(a)/k!`。因为 Bernstein 基函数非负且和为 1，只要所有 `β_i≥0`，就严格证明整个子区间 `p≥0`。
- 关键推进：若真实存在 strict margin `p(q)≥δ>0`，令 `M_k=Σ_{j≥k}|c_j|C(j,k)R^(j-k)`，则任意长度 `h` 子区间上的系数满足 `|β_i-p(a)|≤Σ_k M_k h^k`。因此充分细的有理/二分 subdivision 必然得到全正 Bernstein 系数；也就是说 strict PASS 一定存在有限纯有理 certificate tree。
- 可导出 reserve：通过树后取所有叶 Bernstein 系数的最小值 `η`，可直接导出 `p≥η`，因此把 `A(q)≤K` 升级为 exact `A(q)≤K-η`，可供后续 source/Float64 perturbation 消费。
- 反例提醒：`A(q)=4q(1-q)` 在 `q=0,1` 都为 0，但 `q=1/2` 达到 1；只查径向端点是错的。全区间 Bernstein 系数 `[0,2,0]` 会拒绝 `K=1` 的粗证书，但在 `1/2` 二分后左右系数分别 `[0,1,1]`、`[1,1,0]`，纯有理地得到 sharp `A≤1`。
- 零余量边界：Bernstein coefficient gate 是 sound，但本轮只证明 strict-margin 情形的 finite completeness。若真实 `min p=0`，搜索深度耗尽只能标 `INCONCLUSIVE`，不能标数学 FAIL；精确贴边时应保留 square/factor identity、Sturm/subresultant 等独立 fallback。
- 给其他 Agent 的建议：下一位数学 Agent 优先从真实 P5 polynomial packet 中在同一 chart/output metric 下抽取 homogeneous components，先按总能量次数 `H_n` 做 exact simplification，再把得到的 signed radial polynomial 直接交给本轮 certificate；若实际 source cell 是平移或单侧，先做 affine-center/one-sided theorem，不能静默使用 `u↦-u` 对称。
- 给 Lean Agent 的建议：先形式化有限 checker leaves（power→Bernstein identity、convex-hull bound、de Casteljau split、radial consumer）；`strictPositive_has_finite_dyadicBernsteinCertificate` 的存在性证明可以后置，不必阻塞 certificate validation。
- 未闭合：actual source split/chart/metric/radius、cell symmetry、parameter compatibility、trajectory/FD-halo coverage、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry 全部保持 open。
