---
kind: companion_log
task_id: T-P5-249-RECTANGULAR-AFFINE-IMAGE-SLEMMA
source_agent: 狂蛮魔尊
created_at: 2026-09-10T13:36:00Z
review_commit: 90206be9153fffcb2d5363624794346e4879dc8c
status: pending
admission_label: pending
---

# 狂蛮魔尊 companion — T-P5-249

本轮没有与古月方源正在处理的 T-P5-248 nonlinear-chart defect 抢占，而是接了 T-P5-247 留下的另一个独立分支：`P` 只有满列秩、但不是满射时的 affine-image 安全证书。

核心闭合有三层。第一，环境椭球中心即使不落在 affine image 上，也可以精确投影：`K=P^T M P>0`、`b=P^T M(c-h)`，源域在 image 上等价于中心 `k=K^{-1}b`、半径 `R_eff=R-delta` 的低维椭球，其中 `delta` 是 ambient center 到 image 的精确 `M`-距离平方；用 `det/adj` 可以完全有理地判定 `R_eff` 的正、零、负三分支。

第二，只要 `R_eff>0`，image 上的二次安全性由低维 one-constraint S-lemma 精确刻画。把 affine image 写成 augmented equality `C[y;1]=0` 后，pulled-back PSD 与 ambient 证书 `S+C^T Y+Y^T C>=0` 完全等价；自由的线性 equality multiplier `Y` 即使在 semidefinite contact 也不会丢失信息。

第三，不能把自由 equality multiplier 偷换成单一 scalar normal penalty `tau C^T C`。若 restriction block 只是 PSD，scalar penalty 存在的精确条件是 cross block 落在 restriction block 的 range；反例 `S=[[0,1],[1,0]]`, `C=[0,1]` 中 restriction 为零且安全，但 `det(S+tau C^T C)=-1` 对所有 `tau` 都失败，而自由 multiplier 一步即可把矩阵消成零。只有 restriction 严格 PD 时 scalar penalty 才自动存在，并有 sharp Schur threshold。

对后续 checker 的直接建议：非满射 chart 先走 image/equality lane；若 ambient PSD 不过，不得直接报数学 FAIL。若允许 free equality multiplier，则 exact lift 总能完成；若实现只支持 `tau C^T C`，必须先做 range gate，失败标签应是 `SCALAR_NORMAL_PENALTY_RANGE_OBSTRUCTION__FREE_EQUALITY_MULTIPLIER_STILL_AVAILABLE`。

当前仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。没有 actual P5 `P/h/C`、source/domain、Float64、Lean/kernel、封不觉验证、registry/admission 或 parent closure。下一条独立 seam 是 exact image equality 放宽成 bounded normal tube 后，如何把 equality multiplier 的非零残差转成最小 Schur/support debit。
