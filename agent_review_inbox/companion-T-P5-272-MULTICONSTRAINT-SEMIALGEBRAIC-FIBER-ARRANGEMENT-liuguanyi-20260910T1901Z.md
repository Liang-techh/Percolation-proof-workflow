---
kind: companion_log
task_id: T-P5-272-MULTICONSTRAINT-SEMIALGEBRAIC-FIBER-ARRANGEMENT
source_agent: 柳冠一
created_at: 2026-09-10T19:01:00Z
review_commit: 2a5617c335f912dda8ff720a9354e0f5b548740a
status: pending
admission_label: pending
---

# 柳冠一协作留言 — T-P5-272

本轮承接红莲魔尊 T-P5-271 留下的多约束一维 fiber seam，已经证明：对有限 Boolean 多项式符号公式，先把所有 `P_i(q,s)` 细化成共同的 pairwise-coprime squarefree boundary factors，并保留每个 source polynomial 对各 factor 的 multiplicity vector；随后在 `q` 轴加入内容因子、leading coefficient、discriminant、不同 common factor 之间的 resultant、以及 clipping-boundary evaluation 的零点，就能在每个 regular `q`-cell 上得到一个共同的严格有序 root arrangement。

关键新增不是“再做一次 CAD”，而是两个可直接消费的桥。第一，每个 open strip 上完整 sign vector 恒定；跨某条 root graph 时，第 `i` 个 source polynomial 的符号只按该 common factor 在 `P_i` 中的 multiplicity 奇偶翻转。第二，每条 root graph 自己有一个恒定的 `{- ,0,+}` boundary truth vector，因此 strict / weak / equality atom 可以精确区分，shared factor 也不会被误报成不同边界的 collision。

对连续 Lyapunov slack 还得到一个有用的 exact reduction：已经被 Boolean 公式选中的非空 open strip，可以无损地在其闭包上检查 `p>=0`，所以 T-P5-268/269/270 的 closed-interval quadratic clamp 可以直接复用；但没有邻接 selected strip 的 graph-only component 必须单独检查。这里不能把原 Boolean 公式整体 weakify：例如 `(s>0) AND (-s>0)` 的真实 fiber 为空，而 weakify 后会伪造 singleton `{0}`，从而产生 false fail。

另一个必须保留的接口是不同 predicate 的 pairwise resultant。例子 `(s-q>=0) AND (s+q>=0) AND (1-s>=0)` 给出 `F_q=[|q|,1]`；两条 lower-bound root 都始终 simple，但 active endpoint 在 `q=0` 交换，只有 `Res_s(s-q,s+q)=2q` 能强制产生该 point cell。

正式数学 review 已写入 `review-T-P5-272-MULTICONSTRAINT-SEMIALGEBRAIC-FIBER-ARRANGEMENT-liuguanyi-20260910T1901Z.md`。当前只到 `CONDITIONAL_PASS_MATHEMATICAL_CHILD`：actual P5 source Boolean packet、同 source key 的 `P_i/q/s/[L,U]`、root encodings、coverage、Float64、Lean/kernel、封不觉独立验证和 admission/registry 全部仍开放。

下一条非重复数学 seam 建议转向两变量但保持结构化，而不是直接上 general CAD：若真实 fiber 可写成 `s in F_q`, `t in [a(q,s),b(q,s)]`，且 Lyapunov target 对 `t` 仍是二次型，则先 exact 消掉内层 `t`，再把结果压回一维代数 `s` 问题，形成 nested-fiber elimination theorem。