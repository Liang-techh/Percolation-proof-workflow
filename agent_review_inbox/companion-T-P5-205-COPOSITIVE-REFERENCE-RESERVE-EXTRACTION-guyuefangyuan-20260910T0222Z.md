---
kind: companion_log
task_id: T-P5-205-COPOSITIVE-REFERENCE-RESERVE-EXTRACTION
review_id: R-T-P5-205-COPOSITIVE-REFERENCE-RESERVE-EXTRACTION-GUYUEFANGYUAN-20260910T0222Z
agent: 古月方源
source_agent: 古月方源
created_at: '2026-09-10T02:32:00Z'
related_result_path: agent_review_inbox/review-T-P5-205-COPOSITIVE-REFERENCE-RESERVE-EXTRACTION-guyuefangyuan-20260910T0222Z.md
related_result_commit: f3c7325dd1cb49f0e93523c11bed546502e77981
---

# 古月方源协作接力 — T-P5-205

本轮接 T-P5-204 明确留下的“真实 T-P5-192 参考证书如何产生正 Lyapunov reserve”缺口，未做 provenance / receipt / admission / re-audit。

数学结论已经压成一个很小的 checker 接口。若物理锥写成 `e=Vy, y>=0`，参考导数 pullback 为 `A=-V^T G_ref V`，Lyapunov pullback 为 `B=V^T H V`，那么任意正储备 `eta=p/q` 的精确条件就是：

`q A - p B` 在非负正交锥上 copositive，其中 `p>=0, q>0`。

不需要 generalized eigenvalue、sqrt、inverse 或浮点除法。并且若下游 T-P5-203/T-P5-204 的总修正 pullback 是 `C`，最推荐保留矩阵形状，直接证明第二张券：

`p B - q C` copositive。

两张券相加立即得到

`q(A-C) = (qA-pB) + (pB-qC)` copositive，

所以最终 deployed inequality 闭合。这个“reserve currency”组合比先把所有修正粗糙标量化成 `sigma B` 更少丢 cancellation。

如果 source 更容易给归一化界，也可以输出两个有理数 `m>0,U>0`：

`A-mJ` copositive，`UJ-B` copositive，`J=11^T`。

则 `UA-mB` 自动 copositive，对应储备 `m/U`，trusted checker 全程可以保持交叉相乘。若 T-P5-204 已经得到标量 slack `sigma B`，只需检查 `U sigma <= m`。

必须提醒其他数学 Agent 两个不能偷换的点：

1. T-P5-192 在 `eta=0` 的普通 PASS 不推出任何正 reserve。反例 `A=diag(1,0), B=I` 的 sharp reserve 就是 0。
2. 不能只检查 cone generators 上的 margin。`A=[[1,-9/10],[-9/10,1]], B=I` 在两个坐标 ray 上看起来 margin 都是 1，但内部方向 `(1,1)` 把真实 sharp reserve 压到 `1/10`。所以仍然要检查完整的 loaded copositivity `qA-pB`。

另外，`eta>0` 也不自动等于“所有非零物理状态严格衰减”；还需要 `B` 在物理锥上严格正/有 coercivity。若 `B` 有非零零方向，储备不等式在那里仍可能等号。

给梁智炜 / source-CSE lane 的下一步建议：从真实同键 T-P5-192 selector packet 直接导出 `V,G_ref,H`，先尝试一个小的正有理 `p/q` 并复用现有 copositivity checker；若失败保留 nonnegative witness 反推哪个 sector/方向耗尽 margin。若 direct loaded gate 不方便，再走 `(m,U)` 归一化双证书。不要从“当前 reference PASS”直接假设一个 `mu>0`。

给 Lean lane 的最小叶建议：`pullback_reserve_iff_copositive`、`copositive_sub_smul_mono`、`normalized_twoCertificate_reserve`、`reserve_currency_compose`，外加一个 zero-margin obstruction lemma 和上述 2×2 `norm_num` 回归。前四个基本只需要 copositive form 对加法/非负数乘闭合以及 `ring`。

协作留言说明：本轮开始前已检查 `collaboration_board.md`。当前 GitHub contents 写接口对该大文件仍是整文件 replacement，无法在并行 Agent 活跃时安全做原子末尾追加；为避免覆盖其他 Agent 的新留言，本轮没有重写共享板，以上中文协作建议以 immutable companion 形式落盘，供梁智炜和其他 Agent 读取。