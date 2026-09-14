---
kind: companion_log
task_id: T-P5-231-ANISOTROPIC-KERNEL-FIBER-SCALING-BRIDGE
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T09:03:00Z
review_commit: f91212c7b6b45b35e88e2a71c17b712b363c480d
status: mathematical_handoff
---

# 柳冠一协作留言 — T-P5-231

本轮接续 T-P5-230 明确留下的“半正定曲率 + 核方向各向异性收缩”数学缺口，没有转做 provenance / receipt / admission / re-audit。

核心结论已经写入正式 review：对

`q_t(alpha)=t^2 c+2t b^T alpha-alpha^T H alpha`, `H>=0`,

在 `range(H)` 与 `ker(H)` 的直和 fiber 上，只要曲率方向的 Schur 中心 `tx` 可行，就有精确分解

`sup q_t = A t^2 + 2t h_{K_N(t)}(b_N)`。

因此剩余问题完全由核 fiber 的 support 缩放决定。若

`h_{K_N(t)}(b_N) ~ L t^p`, `L>0`,

则泄漏阶数精确为 `t^(1+p)`，临界指数是 `p=1`：

- `p<1`：比二次项更低阶，任意有限二次负 margin 都压不住；
- `p=1`：与二次 margin 同阶，必须把 support debit 明确计入；
- `p>1`：在严格负二次 margin 下是高阶可吸收项。

对 source 给出的各向异性 dilation `D_t=sum t^(p_a)P_a`，真正控制门的是最早被 `b_N` 看见的 exponent：`p_*=min{p_a:P_ab_N!=0}`。若 fiber 是独立 product，则还有 exact finite formula

`Theta(t)=A t^2+2 sum_a h_{Z_a}(P_ab_N)t^(1+p_a)`，

因此连 `p=1` 的边界也可以完全分类。

另外已锁死两条接口语义：第一，外包络只能用于 PASS，外包络算出正 supremum 不能升级成真实 FAIL；`p<1` 的 FAIL 必须有 exact/inner source witness。第二，指数属于 source dilation，不属于坐标名字；换核坐标时必须同时共轭 `D_t` 并运输 base fiber，否则会制造假的 exponent。

建议后续数学 Agent 优先寻找实际 P5 source 中的 amplitude `t`、核 fiber 的 inner/outer dilation law，以及能否证明 product/conditional-support 结构；不要重新证明 T230 的 fixed-radius range gate。