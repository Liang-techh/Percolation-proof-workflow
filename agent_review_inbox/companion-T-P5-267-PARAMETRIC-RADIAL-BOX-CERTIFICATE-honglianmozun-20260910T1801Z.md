---
kind: companion_log
task_id: T-P5-267-PARAMETRIC-RADIAL-BOX-CERTIFICATE
source_agent: 红莲魔尊
created_at: 2026-09-10T18:01:00Z
review_commit: 3f2f9004e7fe2c1a0f3fc315f59d33a2ed4dbde5
status: mathematical_handoff
admission_label: pending
---

# T-P5-267 中文数学交接

本轮把 T-P5-266 留下的“`A(q)` 若带额外 cell parameter 怎么办”拆成两个严格分支。

第一分支是 exact 的：若 `A(q,theta)` 对参数盒中的每个参数分别凸，则固定 `q` 时最大值一定落在盒顶点，因此

`A(q,theta)<=K` 在 `[0,R] x B` 全域成立

当且仅当所有顶点 `v` 上的一元多项式 `A(q,v)<=K` 在 `[0,R]` 成立。multi-affine 情形更强，直接有顶点 barycentric 恒等式，不需要任何曲率估计；一个参数二次型 `A=A0+A1 s+A2 s^2` 时，只需先用一元精确判据证明 `A2(q)>=0`，之后仍只查两个端点。顶点各自若有 reserve `eta_v`，全盒 reserve 精确可取 `min_v eta_v`。

第二分支处理 genuinely bivariate polynomial：对 `p(q,s)=K-A(q,s)` 使用 tensor-product Bernstein。任一 rational rectangle 的 Bernstein 系数均可由二维 Taylor + power-to-Bernstein 公式精确得到；所有系数非负即可 sound PASS。若真实 `p>=delta>0` 有严格 margin，则利用 derivative coefficient bound 可证明足够细的 rational/dyadic 二维 subdivision 必然得到全部正系数，因此 strict PASS 有有限 exact-rational certificate。

零 margin 不能照搬这个 completeness。反例 `p(x,y)=(x-y)^2` 在单位方形上全域非负，但零集是一整条对角线；任意有限 axis-aligned subdivision 总有一个 leaf 的内部被对角线穿过。该内部零点处所有 tensor Bernstein basis 都严格正，所以若 leaf 系数全非负，零值会迫使所有系数都为零，矛盾。因此一般二维 touching case 必须保留 `BIVARIATE_ZERO_MARGIN_CERTIFICATE_OPEN`，不能把 Bernstein 不闭合报成数学 FAIL。

建议下一条数学 seam：处理 concave quadratic parameter

`A(q,s)=A0(q)+A1(q)s-A2(q)s^2`, `A2(q)>0`。

其最大值可能在内部 `s*=A1/(2A2)`；应把 `[a,b]` clamp 条件、`A0+A1^2/(4A2)` 的分母正性和 endpoint branches 全部改写成 fraction-free 一元多项式 gate，再交给 T-P5-265/T-P5-266。这样可以覆盖第一个真正需要 interior parameter maximizer、但仍无需二维 CAD 的分支。

仍未闭合：actual P5 `A(q,theta)` source/key/cell binding、真实 parameter box、trajectory/FD-halo coverage、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry。不要把本数学 child 提升为 parent closure。
