---
kind: companion_log
review_id: companion-T-P5-202-psd-mixed-domain-recession-polar-gate-kuangmanmozun-20260910T0131Z
task_id: T-P5-202-PSD-MIXED-DOMAIN-RECESSION-POLAR-GATE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T01:31:00Z
status: pending
admission_label: pending
related_review: agent_review_inbox/review-T-P5-202-PSD-MIXED-DOMAIN-RECESSION-POLAR-GATE-kuangmanmozun-20260910T0131Z.md
---

# 狂蛮魔尊协作记录：T-P5-202

本轮没有发现梁智炜对“狂蛮魔尊”的新点名，因此没有转去做 audit、receipt 或 admission，而是接 T-P5-201 后仍未闭合的 mixed-domain support finiteness seam。

数学推进有三点：

1. 当二次域矩阵 `P` 是普通 PSD 且混合域非空时，真实 recession cone 精确等于 `r>=0, Cr<=0, Pr=0`。因此 T-P5-201 的 zero-cost recession witness 在这个分支里不是“仅充分”，而是完整的 recession 描述。
2. 线性 support 是否有限可先做纯 LP/Farkas 判定：存在 `lambda>=0, nu` 使 `C^T lambda + P nu - b >=0` 当且仅当不存在正 support recession ray。若存在 ray，可归一化为 `b^T r>=1`，给出严格数学 FAIL witness。
3. polar witness 一旦存在，任取有理 `tau>0` 就能构造 `B_tau=d^Tlambda+tau*rho+(nu^TPnu)/(4tau)`。对应 T-P5-201 augmented matrix 自动分解成一个 PSD square 加一个非负 orthant cross term，因此无需 generic copositivity search 即可得到 rational finite cap。

最重要的边界：这一压缩严格依赖 ordinary PSD，不能只用 copositivity。已给出一个 3x3 copositive 但 indefinite 的反例，其中真实 recession ray 满足 `r^TPr=0` 却 `Pr!=0`，而且 `P` 甚至可逆；若误用 PSD kernel test 会漏掉真正的 unbounded support。

给后续数学 Agent 的建议：PSD mixed-domain 分支今后先跑“positive recession LP / polar LP”二择一，再决定是否需要 T-P5-201 的强 copositivity 优化。若构造出的 `B_tau` 太松，只能标记“finite but bound too loose”，不能误报 support unbounded。下一条值得攻的是如何在保持 rational certificate 的前提下优化 `B_tau(lambda,nu)`，以及它与 full augmented optimum 的 gap。
