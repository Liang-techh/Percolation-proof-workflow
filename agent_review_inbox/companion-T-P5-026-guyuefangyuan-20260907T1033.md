---
kind: companion_log
task_id: T-P5-026
source_agent: 古月方源
created_at: 2026-09-07T10:33:00-06:00
related_review: review-T-P5-026-guyuefangyuan-20260907T1031
integration_status: pending
---

# T-P5-026 中文协作接力

### 2026-09-07 10:33 — 古月方源
- 当前完成：在柳冠一 `T-P5-025` 的直接 `K_path` small-gain 路线上继续去掉两层保守性。对每个 `(x,y,x+y)` 的符号关系，八个形式符号三元组里实际上只有六个可行；两个通道因此只有 36 个可行锥，利用全局同时反号后只需 18 个不同证书，而不是原来的 32 个 all-sign 矩阵。
- 数学推进：给六个单通道锥写出了显式整数/幺模参数化。每个两通道可行锥可写成 `z=T_C u, u>=0`，并且 `|Lz|^T K|z|<=mu Q(z)` 与 18 个锥上 `u^T H_C(mu)u>=0` 精确等价。这里真正需要的是非负正交象限上的二次型非负，而不是整个 `R^4` 上 PSD。
- 新的 checker 接口：对每个锥只要给出精确有理分解 `H_C=S_C+N_C`，其中 `S_C` PSD、`N_C` 逐项非负，就可推出锥上非负。`S_C` 可用有理 `LDL^T` 验证，`N_C` 逐项检查；不需要平方根或数值特征值。全局 PSD 是 `N_C=0` 的特例，因此这条接口至少在证书类别上严格更弱、更灵活。
- 重要边界：本轮没有具体 source-bound `K_path`，所以没有声称真实系统已经通过 18 个锥；SPN 搜索失败也不能当成 copositivity 反例，只能回退到 `T-P5-025` 或 `T-P5-024` 的 scalar `ell2_path` 路线。
- 给形式化 Agent 的建议：优先拆 `channel_cone_cover`、`two_channel_cone_cover`、`entrywise_nonnegative_quadratic_nonnegative`、`spn_quadratic_nonnegative_on_orthant`、`feasible_cone_direct_small_gain`；最有价值的是再补一个 exact equivalence `direct_abs_envelope_for_all_z <-> all_feasible_cone_quadratics_nonnegative`，把精确数学和 SPN 这个充分 checker 表示分开。
- 给 source/checker Agent 的建议：一旦拿到具体 `K_path`，先保留完整 2×4 分量矩阵跑 18-cone rational SPN search，不要第一步就坍缩成 Frobenius `ell2_path`；真正的 Float64/solve/controller 不连续偏差仍放 additive bias branch。
- 关联任务/Review：`T-P5-026`、`review-T-P5-026-guyuefangyuan-20260907T1031.md`、`T-P5-025`、`T-P5-024`、`T-P5-020`。

> 说明：当前 GitHub 连接器对共享 `collaboration_board.md` 只有整文件替换写入，而该长文件读取结果会被截断；为避免违反“不得覆盖/删除历史留言”的规则，本轮没有冒险重写共享板。以上内容为完整中文接力，供梁智炜下一次安全收割/追加。
