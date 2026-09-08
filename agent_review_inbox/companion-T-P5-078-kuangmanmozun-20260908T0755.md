---
kind: companion_log
task_id: T-P5-078-MIXED-RELATIVE-ADDITIVE-CORRECTOR
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T07:55:00-06:00
review_commit: f0d1df5605088ee79b7416d61af04cf78c2d2f65
status: pending mathematical child
---

# T-P5-078 中文协作摘要

本轮补的是 T-P5-073 与 T-P5-075 之间还没有明确写出的共享预算规则：corrector 的 evaluator error 如果同时含“随根误差缩放的 relative 部分”和“不会随根误差消失的 additive 部分”，两者不能各自拿 nominal contraction reserve 全额消费。

设 nominal corrector 已有同一 weighted norm 下的

`Q(a) <= q Q(d)`，

relative evaluator 满足

`Q(e_rel) <= K Q(d)`，

实际先变成 `b=a-h e_rel`。对任意拟议的有理 effective factor `kappa`，定义

`S = kappa-q-h^2 K`。

则 uniform envelope 下 `Q(b)<=kappa Q(d)` 的精确 radical-free gate 是

`S>=0`，

`4 h^2 q K <= S^2`。

严格 contraction 直接取 `kappa=1`，因此必要充分的 envelope gate 是

`1-q-h^2K>0`，

`4 h^2 q K < (1-q-h^2K)^2`。

这封死了一个常见但错误的 shortcut：只检查 `q+h^2K<1` 不够。精确反例取 `q=9/25,h=1,K=1/4`，平方项相加只有 `61/100<1`，但 adversarial alignment 给出的真实最坏能量因子是 `(3/5+1/2)^2=121/100>1`。

relative 部分收费后，persistent additive defect `Q(e_abs)<=E` 必须对新的 `kappa` 收费。候选 barrier `Vstar` 的 gate 是

`R=(1-kappa)Vstar-h^2E>0`，

`4 h^2 kappa Vstar E < R^2`。

因此正确 ledger 顺序是

`nominal q -> relative K -> effective kappa -> additive E`，

不能分别把 K 和 E 都对旧 q 检查。

精确 joint-failure 反例：`q=1/4,h=1,K=1/16,E=4/25,Vstar=1`。relative-only 的 norm factor 是 `3/4<1`；additive-only 对 nominal q 的 norm factor是 `9/10<1`；但三项共同 adversarial alignment 后是 `23/20>1`，能量变成 `529/400`。所以“两条单独 PASS ⇒ 共同 PASS”是假的。

还要保持语义分层：`E=0` 时，只要 effective `kappa<1`，relative evaluator 可以保留真正的几何零收敛；`E>0` 的 persistent bias 一般只能得到 invariant/ultimate ball，不能声称收敛到原根。source packet 因此必须把 `K` 和 `E` 分开 typed，不能把常数偏差重新命名成 relative error。

下一步若要 Lean，最小叶是 `relative_defect_effective_factor`、`relative_defect_strict_contraction_gate`、`mixed_defect_barrier` 以及两个 exact rational counterexample regression。当前没有升级 deployed SCC/source、Float64/FD/controller、P8/ODE coverage、Lean/kernel、admission、registry 或 parent closure。