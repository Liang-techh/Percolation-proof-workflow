---
kind: companion_log
task_id: T-P5-187-ACTIVE-FAN-OVERLAP-KERNEL-GAUGE
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T21:26:00Z
parent_review: review-T-P5-187-ACTIVE-FAN-OVERLAP-KERNEL-GAUGE-guyuefangyuan-20260909T2124Z.md
parent_review_commit: 1b4d00d6d3c2cbcbf3c1eadc4d7a3e729b7d808e
status: pending
---
# 协作留言 — T-P5-187

本轮先检查了 `README.md`、`task_queue.md`、`collaboration_board.md`，以及最新的 T-P5-184 companion、T-P5-185 与 T-P5-186 review。未发现梁智炜对“古月方源”的更新点名，也没有发现尚未完成且与本任务重叠的现役 claim，因此新开 T-P5-187，只处理 active-face fan 的重叠缝合数学问题。

## 当前完成

证明了同一个 PSD inherited block、同一个 external direction 下，任意两个满足 orthant KKT/complementarity 的最小点，其差必在 `ker(P)` 中；并且两者的 KKT residual **完全相同**。所以 singular PSD 情况下不同 face/minimizer 只存在 kernel gauge，不存在 reduced-energy 歧义。

若两个线性 transport `Y_alpha,Y_beta` 在同一 overlap cone 上都有效，则

`P(Y_alpha-Y_beta)e=0`

对 overlap 中所有 `e` 成立，并自动扩张到其线性张成空间。进一步得到 overlap generator matrix `V` 上的精确恒等式

`V^T(K_alpha-K_beta)V=0`。

因此 piecewise Schur fan 在边界上无需额外“连续性假设”；只要两个区域 KKT packet 各自正确，能量缝合自动成立。

## 发现的问题

不能把正确 seam contract 错写成全空间 `K_alpha=K_beta`。本轮构造了精确有理二锥例子：`P=1`、`B^T=(-1,1)`、`C=[[1,-1],[-1,1]]`，两个 face 的 reduced matrices 分别是 `0` 和 `C`，全局并不相等，但在公共射线 `e1=e2` 上 reduced energy 与 minimizer 完全一致，且完整二次型就是 `(u-e1+e2)^2>=0`。

同样，singular PSD 时也不能要求 transport 自身相等；`P=[[1,-1],[-1,1]]` 下沿 `(1,1)` 的差异只是 kernel gauge。

## 给其他 Agent 的建议

后续若 source/CSE 生成 T-P5-185/T-P5-186 的 face fan，建议对每个真实 overlap generator `V` 做三个很便宜的 exact consistency gate：

1. `P(Y_alpha-Y_beta)V=0`；
2. `(R_alpha-R_beta)V=0`；
3. `V^T(K_alpha-K_beta)V=0`。

前两个/第三个在数学上由双边 KKT packet 自动推出，所以它们更适合作为 producer/source-key/坐标顺序的诊断，而不是新增 proof burden。若 exact mismatch，应优先怀疑 overlap 标注、source key、归一化或某个 KKT packet，而不要解释成真实能量跳变。

另外，KKT residual 是 canonical 的：`r_i>0` 的 inherited 坐标在所有 minimizer 中都必须为零，只有 `r_i=0` 的 critical set 才能通过 kernel gauge 改变 support。建议 singular fan producer 先按 canonical residual-zero set 做边界归一化，再选 minimal-support representative，可减少重复 face。

## 建议的 Lean 接力

优先落四个小叶：`orthantKKT_twoSolutions_kernelDiff`、`orthantKKT_residual_unique`、`transportOverlap_kernelGauge`、`transportOverlap_reducedPullback_eq`。证明只需要二次式展开、非负性和 `PSD + x^TPx=0 => Px=0`，不需要 inverse/pseudoinverse/spectral decomposition。

当前 source binding、actual cone overlap、Float64/controller/FD、Lean/kernel、封不觉独立验证和 admission/registry 均保持 pending。

共享 `collaboration_board.md` 的当前连接器写接口仍要求整文件 replacement，无法安全做并发原子追加；为避免覆盖其他 Agent 同时新增的留言，本条中文协作接力写入 immutable companion，未冒险重写共享留言板。