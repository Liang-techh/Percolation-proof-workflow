---
kind: companion_log
review_id: companion-T-P5-049-guyuefangyuan-20260907T2238
task_id: T-P5-049
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T22:38:00-06:00
related_review: review-T-P5-049-guyuefangyuan-20260907T2234
review_commit: 09ce4a35611a1dac9433c4b55a048c1b979ca8ab
integration_status: pending
admission_label: pending
---

# T-P5-049 协作接力

本轮接着柳冠一 `T-P5-048` 明确留下的“不同 cell 曲率 `d_i` 时需要 future genuine varying-curvature optimizer”继续推进，没有抢占其 finite same-curvature/homogenization、红莲魔尊 rank-one Lyapunov、苏梦辰/巨阳仙尊 Lean/CI，也没有做 provenance/admission 重审。

新的核心结论是：对有限族

`f_i(r)=A_i+B_i r-d_i r^2, d_i>0, r∈[0,1]`

其实可以完全绕过统一曲率 `D`。每个严格正集 `{r|f_i(r)>0}` 都是一个开区间，因此把 `[0,1]` 也视为一个区间后，一维有限 Helly 告诉我们：全局共享 `r` 存在，当且仅当每个 row 自己与 `[0,1]` 相交、且任意两个 row 的正区间相交。

单行检查完全有理：记 `Delta=B^2+4dA`，则

- `B<=0` 时 iff `A>0`；
- `0<B<2d` 时 iff `Delta>0`；
- `2d<=B` 时 iff `A+B-d>0`。

两行也能把平方根完全消掉。记

`C=B_i d_j-B_j d_i`，

`S=C^2-d_j^2 Delta_i-d_i^2 Delta_j`，

`K=4 d_i^2 d_j^2 Delta_i Delta_j`。

在 `Delta_i,Delta_j>0` 下，两条正区间相交 **iff**

`S<=0 OR S^2<K`。

因此有限 varying-curvature shared-r 的必要且充分条件只需要 `n` 个单行检查加 `n(n-1)/2` 个 pair 检查，全程只做有理加乘、平方和序比较；不需要 sqrt、代数根、固定网格、共同 `D` 或 pivot。这一层既能给正可行性，也能给真正的 pairwise fail-fast obstruction。

建议 source/checker lane 保留 `(A_i,B_i,d_i)` typed row，先跑这个 exact Helly gate。若任意 pair FAIL，直接报告数学无解；若全部 PASS，则严格共同区间非空，而且由于是有限个开正集与 `[0,1]` 的交，必然存在 exact rational（甚至 dyadic）共享 witness。之后 source/search 只需找一个 rational `r` 并逐行重验。`T-P5-048` 的 pivoted homogenization 仍可保留为“复用现有 common-curvature Lean stack”的安全构造路线，但其失败不能再当成原 varying-curvature family 的真实 obstruction。

两个 exact regression 已写入 review：一个 varying-curvature family 的真共享区间为 `(7/10,9/10)`，但 `D=max d_i` 的**无 pivot** minorant 第一行 discriminant 为 `-536/25<0`，直接假阴性；另一个两行各自都在 `[0,1]` 可行，但 pair 数据 `S=92/25>0` 且 `S^2=8464/625>64/625=K`，因此严格证明没有共享 `r`。

给 Lean lane 的最小顺序建议：先形式化 `4d f(r)=Delta-(2dr-B)^2`、三个 Local branch、pair-overlap 的 root-free iff；最后再做 finite interval Helly。pair theorem 内部可以用 `Real.sqrt` 证明，但 theorem statement / checker 接口不应暴露 sqrt。

**更正 review Section 9 的伪 Lean 记法：**其中三个 local theorem 的 `exists r, 0<=r -> r<=1 -> f r>0` 只是排版伪码，不应按 implication 解释。正式 statement 必须是

`∃ r, 0 ≤ r ∧ r ≤ 1 ∧ f r > 0`。

原 review 按 inbox immutable 纪律不重写，本 companion 作为 canonical statement correction。

当前仍严格 `pending mathematical child`：真实 source row、Float64/FD/controller/solve、P8 coverage/ODE、Lean kernel/comparator、receipt/provenance 与 P5/P8/M4 admission 均未闭合。