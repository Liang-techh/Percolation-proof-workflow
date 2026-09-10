---
kind: companion_log
task_id: T-P5-214-COPOSITIVE-SCHUR-ZERO-SUPPORT-DECOMPOSITION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T04:33:00Z
review_commit: 6f8b539f94aba1fcf3a9106a8989ee88e7a1c38b
status: mathematical_handoff
---

# T-P5-214 协作交接 — 狂蛮魔尊

本轮处理的是 T-P5-213 明确保留的 `K` 仅 copositive、但不是 ordinary PSD 的 reduced-Schur 分支，没有做 provenance / receipt / admission / 重复验证。

核心结论：对任意对称 copositive `K`，若 `eta>=0` 且 `eta^T K eta=0`，令 `S=supp(eta)`，则真实支撑上的 principal block `K_SS` **自动 ordinary PSD**，并且 `K_SS eta_S=0`。证明只用 `eta_S>0` 后允许在支撑内做正负两侧小扰动：零点成为普通二次型的两侧局部极小，从而一阶项全消失、二阶项对所有 signed direction 非负。

因此全局 indefinite-copositive 的零集可以精确写成有限个 supportwise PSD kernel cone 的并：不再需要 generic semialgebraic zero solver。T-P5-210 的 common-zero debit residual `g=Tz>=0` 又把候选支撑先缩到 `J0={i:g_i=0}`。在 T-P5-213 的 active-flat `E=N^TPN=0` 分支，每个 surviving support 都可直接调用 T-P5-212 的 PSD-kernel generator machinery，形成 `M_S=W_S^T G W_S`；该 support 存在正二阶 debit witness 当且仅当 `M_S!=0`。

最重要的防误用反例是 `K=[[0,1],[1,0]]`：`e1,e2` 都是零方向，但 `e1+e2` 不是零方向。因此不同 support 的 zero rays 不能拼成一个全局 generator cone；只有当更大的 principal block 本身 PSD 时，才能安全在同一 support branch 内做 conic mixing。

另一个 exact 例子 `K=[[1,-1,1],[-1,1,1],[1,1,0]]` 满足 `q=(x-y)^2+2z(x+y)>=0` on orthant，但矩阵有负特征值。`eta=(1,1,0)` 是零方向，却有 `Keta=(0,0,2)`，说明 copositive zero 一般不是 full-kernel vector；真正正确的对象就是其 support 上的 PSD principal kernel。

建议下一步：若要优化复杂度，可研究基于 `K` 的零/符号图对 support loop 做 maximal-support / clique pruning；但在证明该 pruning 完备之前，不要把当前有限 support enumeration 压成一个全局 kernel cone。

当前仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`；没有升级实际 source、coverage、Float64/interval、Lean/kernel、封不觉独立验证、registry/admission 或 P5/P8/M4 parent closure。
