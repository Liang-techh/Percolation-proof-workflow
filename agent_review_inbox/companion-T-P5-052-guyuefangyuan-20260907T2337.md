---
kind: companion_log
task_id: T-P5-052
review_id: review-T-P5-052-guyuefangyuan-20260907T2334
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T23:37:00-06:00
integration_status: pending
admission_label: pending
---

# T-P5-052 协作接力 — 古月方源

- 当前完成：把 `T-P5-BRANCHFREE-AFFINE-MAJORANT` 留下的“相关余量必须整体 enclosure”推进成 exact-rational Bernstein cell gate。若同一 cell 上的 `p,s,sigma,b4,b5` 对一个有理参数是仿射的，则 `Rtr` 至多二次、`Rdet` 至多三次；直接检查它们的 Bernstein 控制点非负即可证明整 cell 非负，完全保留 `kappa*D4-Nsig` 的抵消。
- 新数学性质：二次/三次 Bernstein 控制点可用 dyadic de Casteljau 纯有理细分；若真实余量在闭区间上严格为正，足够细的 dyadic 划分最终一定让每个子 cell 的全部控制点严格为正。因此这是 strict-positivity 的完整半判定过程，不需要求根、sqrt、eigenvalue 或浮点优化。
- 重要 fail-closed 规则：单个 Bernstein 控制点为负不能直接判 FAIL，只能继续细分或返回 UNDECIDED；只有找到 exact rational 点使余量 `<0`，或有其他必要性证明，才是数学 obstruction。端点正也不够，`1-5t+5t^2` 在两端都等于 1、但中点为 `-1/4`，可作为 checker 负控。
- 给 source/interval Agent 的建议：拿到最小 signed source cell 后，先整体构造 `Rtr=4*kappa*(p+s)-b4^2-b5^2` 与 `Rdet=kappa*(4ps-sigma^2)-(s*b4^2-sigma*b4*b5+p*b5^2)`，再做 exact Bernstein/subdivision；不要先分别对 `D4` 和 `Nsig` 取 extrema。`sigma=k45+k54` 仍必须先完成 signed addition 再做任何绝对值包络。
- 给 Lean Agent 的建议：最小 formal core 只需 `quad/cubic_bernstein_identity`、控制点非负消费者和 `decasteljau_half`；最终 P5 theorem 直接调用已经落地的 branch-free two-gate consumer，不要重复 2×2 completion。strict-positivity 的 eventual-subdivision theorem 可作为后续可选分析层，不是 trusted checker 的必要前提。
- 仍未闭合：deployed source 是否给出仿射/低阶多项式 same-key 表达、Float64/FD/controller/solve enclosure、多维 coverage、ODE/P8，以及独立 Lean/admission。当前只应登记为 pending mathematical child。
- 关联任务/Review：`T-P5-052`、`review-T-P5-052-guyuefangyuan-20260907T2334`、`T-P5-BRANCHFREE-AFFINE-MAJORANT`、`T-P5-051`。

说明：共享 `collaboration_board.md` 当前通过 contents API 只能整文件替换，没有原子 append；多人并发写入下直接覆盖存在丢失他人留言风险。本轮完整中文协作内容先持久化在此 companion，供梁智炜收割时安全追加到留言板。
