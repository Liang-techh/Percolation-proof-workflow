---
kind: companion_log
task_id: T-P5-259-TERNARY-QUARTIC-GRAM-BRIDGE
source_agent: 柳冠一
created_at: 2026-09-10T16:09:00Z
review_path: agent_review_inbox/review-T-P5-259-TERNARY-QUARTIC-GRAM-BRIDGE-liuguanyi-20260910T1607Z.md
admission_label: pending
---

# T-P5-259 companion — 柳冠一

本轮承接红莲魔尊 T-P5-258 明确保留的 `r=3` realized-direction seam，没有转做 provenance、receipt、admission 或重复验证。

数学结果：对三维 quotient 的齐次 quartic `p(x,y,z)`，使用二次单项式 lift `[x²,y²,z²,xy,xz,yz]` 后，所有 Gram 表示恰好形成一个 **6 参数** affine fiber；review 给出了完全显式、乘 `2` 后无 `1/2` 的 `6×6` Gram 矩阵。这个 6 维数不是实现选择，而是 `dim Sym_6 - dim H_{3,4}=21-15=6` 的最小值。

消费经典 Hilbert ternary-quartic theorem 后，`p>=0` 与“存在这 6 个 gauge 使 Gram PSD”严格等价。因此 `r=3` 仍可像 `r=2` 一样绕开 stronger operator matrix gate，直接验证真实 realized energy，只是搜索从一个标量扩成六维 spectrahedron。

严格有理分支进一步闭合：若 rational ternary quartic 对所有非零方向严格为正，则 Gram fiber 内一定存在 **rational positive-definite witness**。理由是先由严格 margin 加上 `diag(1,1,1,2,2,2)` 得到实 PD Gram，再利用该 Gram affine fiber 的 rational 6-gauge basis 与 PD cone 开性，取邻近 rational gauges。于是 strict checker 只需六个 rational gauges 加六个 leading principal minors。

坐标接口也闭合：`u=Pv` 时二次 monomial lift 按 `Sym²(P)` 运输，Gram 精确 congruence；若 `P` rational，反向运输可用 `adj(P)` 写成 `det(P)^4 G_u = Sym²(adj P)^T G_v Sym²(adj P)`，不需要 whitening/eigenvector。

高维边界：写入显式 rational 四元 quartic `x²y²+y²z²+z²x²+w⁴-4xyzw`。AM-GM 证明其全域非负；若假设为 quadratic SOS，则零 `x⁴,y⁴,z⁴,x²w²,y²w²,z²w²` 系数会逐项强制每个平方中的 `x²,y²,z²,xw,yw,zw` 系数全为零，于是无法产生 `xyzw` 项，与 `-4xyzw` 矛盾。因此 `r>=4` 时 Gram 搜索失败不能自动升级成 physical FAIL。

尚未闭合：actual deployed quotient dimension/`A,M,W`、参数/单元统一 selector、source/coverage、Float64/interval、Lean/kernel、封不觉独立验证与 admission。下一条更贴 source 的数学 seam 是 **cell-dependent ternary Gram selector**：区分 constant gauge、affine/polynomial gauge selector 与 pointwise SOS 但有限 selector 不足的情形。