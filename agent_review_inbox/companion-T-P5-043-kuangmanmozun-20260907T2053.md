---
kind: companion_log
review_id: companion-T-P5-043-kuangmanmozun-20260907T2053
task_id: T-P5-043
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T20:53:00-06:00
related_review: review-T-P5-043-kuangmanmozun-20260907T2050
review_commit: 24fc4d4c2c2b672f64b7350a2a0d1a77c2c0d911
integration_status: pending
admission_label: pending
---

# T-P5-043 协作留言 — 狂蛮魔尊

- 当前完成：接古月方源 `T-P5-042`，把最后剩下的 `ell4,ell5` 搜索也从“是否可行”的决定层消掉了。对每个通道先按 `mC-R(2a-R)` 的符号分成 endpoint / interior 两类，再按 E/E、I/E、E/I、I/I 四种组合检查一组完全有理的严格多项式条件；其中 I/I 只需三个 gate：`T>0`、`S>0`、`S^2>64 m4^2 m5^2 D4 D5`。
- 实质意义：这个 gate 是必要且充分的。若 active branch 精确 FAIL，就已经证明在当前“两个独立 scalar mixed residual 通道”模型中，不存在任何 `rho4,rho5` 能闭合 centered decay；继续扫 `rho` 或 `ell` 没有数学意义，应直接升级 signed Jacobian、相关二通道矩阵/SPN 或 source partition。
- 反例提醒：双重平方时三个符号都不能删。只保留最终平方会误判，例如 `T<0` 仍可能最终平方 PASS；`S<0` 也能最终平方 PASS；最终一层若用 `>=` 而不是 `>`，则会把零 reserve 的 boundary-only 情形误收成严格 decay。
- exact regression：两相同通道 `a=m=1,R=1/2,C=1/100,L=1/20` 属 I/I；直接 gate 给 `T=41/20`、`S=849/400`、最终严格 margin `28577/160000>0`。取有理 `rho4=rho5=49/100` 时，每通道 `g=101/5100`，总和 `101/2550<1/20`，剩余 `53/5100`。
- boundary regression：改成 `C=11/100,L=2/5` 后，最终 gate 恰好等号 `S^2=64D4D5=5184/625`，因此只能 boundary-only，不能宣称严格 decay。
- 给 Lean/checker Agent 的建议：先形式化一根号和两根号的带符号 square-free iff，再做四个 branch theorem 与一个 FAIL obstruction corollary。最终 checker 决定层不必保存 sqrt、optimizer、rho 网格或 ell 网格；PASS 后再调用 `T-P5-042` 的 rational `ell -> rho` constructor 产出核友好 witness。
- 仍未闭合：真实 signed `(u,x)` source row、anchor/FD/controller/solve bias、Float64/true-DH、P8 coverage、Lean/kernel/comparator、P5/P8/M4 admission。
- 关联任务/Review：`T-P5-041`、`T-P5-042`、`review-T-P5-043-kuangmanmozun-20260907T2050.md`。

备注：共享 `collaboration_board.md` 仍是并发整文件更新接口，本轮避免覆盖其他 Agent 的新留言；中文 handoff 先以 companion 持久化，供梁智炜 harvest 时安全并入留言板。
