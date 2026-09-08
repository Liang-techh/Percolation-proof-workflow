# 协作留言 — T-P5-051 near-singular compatibility penalty

- agent: `狂蛮魔尊`
- source_agent: `狂蛮魔尊`
- task_id: `T-P5-051`
- 状态：`pending mathematical child`

梁智炜 / 各数学与形式化 Agent：

本轮没有抢占古月方源已经认领的 `T-P5-049`，而是沿我上一轮 `T-P5-050` 的奇异 2×2 affine-completion 分类继续补正定但接近奇异的边界。

核心新恒等式如下。令

`H=[[p,q],[q,s]]`, `tau=p+s`, `delta=ps-q^2>0`, `k=adj(H)b`。

则 sharp completion cost 不只是 `b^T H^{-1}b/4`，还可以精确拆成

`C_* = ||b||^2/(4 tau) + ||k||^2/(4 tau delta)`。

第一项就是 `T-P5-050` 奇异兼容分支的 trace cost，第二项是精确的 incompatibility penalty。因此靠近 `det H=0` 时真正要控制的不是单独的 determinant floor，也不是仅仅要求 `adj(H)b -> 0`，而是

`||adj(H)b||^2 / delta`。

等价的完全无除法预算 gate 是

`||adj(H)b||^2 <= delta (4 tau C - ||b||^2)`，

严格消费时把 `<=` 换成 `<`。

P5 两个常用 strict gate 可以直接写成：

- quarter：`delta[(109-r)tau-200||b||^2] > 200||adj(H)b||^2`；
- parameter：`delta[(109-r)tau-600||g||^2] > 600||adj(H)g||^2`。

这给 checker 一个很清楚的三分支接口：

1. `delta>0`：用本任务的 near-singular defect gate；
2. `delta=0, tau>0`：用 `T-P5-050` 的 pivot-free singular compatibility gate；
3. `delta=0, tau=0`：只有 bias 为零才有有限上界。

特别提醒一个容易误判的点：`adj(H_eps)b_eps -> 0` 本身远远不够。反例

`H_eps=diag(eps^4,1)`, `b_eps=(eps,0)`

有 `adj(H_eps)b_eps=(eps,0)->0`，但 sharp cost 是 `1/(4eps^2)->∞`。真正临界尺度是 `||adj(H)b||=O(sqrt(delta))`；例如 `H_eps=diag(eps^2,1), b_eps=(eps,0)` 时 cost 恰好恒为 `1/4`。

形式化侧建议优先做两个纯代数叶：

`adj(H)^2 = tau adj(H) - delta I`

以及

`||adj(H)b||^2 + delta||b||^2 = tau (b^T adj(H)b)`。

后面的 budget gate 基本只是清分母与正性消费。完整推导、四个反例/回归和 Lean-ready theorem 列表已经写在正式 review：

`agent_review_inbox/review-T-P5-051-near-singular-compatibility-kuangmanmozun-20260907T2340.md`

本轮没有声称 concrete source、Float64/true-DH、coverage、Lean/kernel 或 registry 已闭合。