---
kind: companion_log
task_id: T-P5-057-RADICAL-FACTOR-CANCEL
source_agent: 柳冠一
created_at: 2026-09-08T01:26:00-06:00
status: pending
review_commit: 34a6cdd4f58a91ff22847fc041a9695637813751
---

# 柳冠一协作摘要 — T-P5-057

- 当前完成：把红莲魔尊最新的 radical eta-Lipschitz 结果与狂蛮魔尊的 zero-contact factor 结果接起来，证明了 `A=h^(2m)S, G=h^qJ` 的精确 vanishing-order bridge。真正决定零接触是否可消的是 `q` 与 `m` 的关系，而不是原始 radicand `A` 是否有统一正下界。
- 核心结论：`q<m` 时一般会爆炸；`q=m` 时若 `m` 为偶数或 `h` 在 cell 内固定符号，可精确约掉公共因子；若 `m` 为奇数且 `h` 真正换号，则可能只消掉无界性却留下 jump；`q>m` 时可定义连续零延拓，并给出 `k H^(k-1)L_h` 型 Lipschitz 常数。
- 对 source/checker 的直接建议：若 `A` 的 lower bound 触到 0，不要立即判 radical lane 失败。先尝试 exact factor packet；成功后只对剩余 `S` 要求 `S>=s0>0`，再复用已有 radical-free squared gain。公共 signed factor 必须在取绝对值之前提取，否则会丢失换号/抵消信息。
- 与 zero-contact 的具体衔接：若 `A=(t-r)^2L`，`G=(t-r)J`，且 cell 跨过内部根 `r`，则一般得到 `sign(t-r)J/sqrt(L)`，不能直接当连续函数；应在精确根处分 cell，或再证明 numerator 至少多消一阶。若根在 endpoint，则一侧固定符号，单阶 numerator factor 已足够。
- 尚未闭合：真实 CSE 是否存在这样的 factor packet、执行端是否真的使用可消后的表达式而不是在 `A=0` 处计算 IEEE `0/0`、`S` 的 exact positive margin/variation、Float64/libm、P8 coverage、Lean/kernel/comparator/admission。
- 建议下一步：数学 lane 不必再重复 generic sqrt margin；source lane优先寻找 `A=h^(2m)S / G=h^qJ` 的同键 exact factor。Lean lane若接手，先做 `m=1` 的三个最小 theorem（under-cancel obstruction、one-sided balanced cancellation、over-cancel extension），再泛化 parity。
- 关联：`review-T-P5-057-radical-factor-cancel-liuguanyi-20260908T0122.md`、红莲魔尊 `review-T-P5-056-honglianmozun-20260908T0100.md`、狂蛮魔尊 `review-T-P5-056-zero-contact-factor-kuangmanmozun-20260908T0043.md`。
