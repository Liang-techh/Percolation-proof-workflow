kind: companion_log
review_id: companion-T-P4-024-kuangmanmozun-20260907T1250
task_id: T-P4-024
source_agent: 狂蛮魔尊
created_at: 2026-09-07T12:50:00-06:00
status: pending
related_review: review-T-P4-024-kuangmanmozun-20260907T1248

# 协作留言

本轮已把 `T-P4-024` 的 Young/Schur 数学部分压成一个更适合 Lean 的无除法接口。建议巨阳仙尊优先形式化 `lambda` 版本，而不是先处理 `theta⁻¹`：

`lambda*||l||² + lambda*(lambda-1)*||r||² - (lambda-1)*||l+r||²`
`= ||l-(lambda-1)r||²`。

所以只要 `lambda>1`、`||r||²<=R` 且

`(lambda-1)b >= lambda||l||² + lambda*(lambda-1)R`，

就直接推出 `||l+r||²<=b`。这个版本只有加法、乘法、范数平方和最后一次用 `lambda-1>0` 消去正因子，避免平方根和逆元 API。

对应 affine PMI 也有精确 scaled-square identity，Schur 条件不是保守充分条件，而是等价于

`(lambda-1)(b-lambda R) >= lambda||l||²`。

柳冠一后续只需要在 adapter 层绑定 `R=rho*A_up`、`A_up=a_BᵀB_up a_B`、`l=l_base`；不要把这个 `r` 与 robust-PMI 的 `E_k` 混用。

对当前候选 `lambda=2`，恒等式进一步退化成

`2||l||²+2||r||²-||l+r||²=||l-r||²`，

因此这一档参数的数学消费层非常干净。需要特别保留 fixed-per-cell 语义：点态最优 `lambda=1+sqrt(L/R)` 依赖状态比值，不能偷偷拿来替换每个 cell 的固定有理 `lambda_k`。

本结果只到数学 child；未做 source binding、cell coverage 或 Lean/kernel admission。待封不觉独立验证 / 待梁智炜最终整合。
