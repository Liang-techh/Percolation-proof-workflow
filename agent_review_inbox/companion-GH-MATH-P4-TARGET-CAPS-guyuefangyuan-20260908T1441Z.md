# 协作留言 — GH-MATH-P4-TARGET-CAPS

- `task_id`: `GH-MATH-P4-TARGET-CAPS`
- `review_id`: `GH-MATH-P4-TARGET-CAPS`
- `agent`: `古月方源`
- `source_agent`: `古月方源`
- `status`: `数学层已有结果，等待 source packet`

梁智炜：本轮已经把 target-cap / `V<=1` 的逻辑方向拆清楚。这里最容易出现一个会导致错误 admission 的反向推理：

1. 从 coercivity / energy lower bound 能证明的是 `{V<=1} ⊆ target box`。例如若 `V >= a_i z_i^2`，则只需检查 `1 <= a_i H_i^2`；对当前半宽分别是 q: `25 a_q >= 4`，v: `225 a_v >= 1`，w: `4 a_w >= 1`。
2. 但若 descriptor/remainder theorem 的前提是 `V<=1`，而我们要覆盖整个 target box，真正需要的是反方向 `target box ⊆ {V<=1}`。这个方向必须有 V 在 target box 上的**上界 packet**或直接的 source inclusion theorem，不能用 coercivity 倒推。

我给出了一个 exact-rational 可直接冻结的通用接口：若展开后的 storage 为

`V(z)=c+Σ l_i z_i+Σ P_ij z_i z_j`

且 `|z_i|<=H_i`，则

`V(z) <= c+Σ|l_i|H_i+Σ|P_ij|H_iH_j =: U(H)`。

只要 `U(H)<=1`，就精确证明 whole target box 在 `V<=1` 内。若 full box 过不了，还可以用 rational `r∈[0,1]` 检查

`c+rL+r^2 Q <= 1`

从而得到 `B(rH) ⊆ {V<=1}` 的严格内层覆盖；不用 sqrt 或 quadratic root。未覆盖的保守 shell 是 `B(H)\B(rH)`，真实 energy-uncovered shell 是 `{z∈B(H):V(z)>1}`。

重要 source blocker：在本轮检查的 `main` 上，任务指定的 `combined_descriptor_remainder_v1.json` 以该文件名不存在；repo code search 对 `combined_descriptor` 和 `remainder_v1` 也均无命中。我也没有找到冻结的真实 DH target-domain/storage packet，因而当前不能诚实实例化 `|q|<=5/2, |v|<=15, |w|<=2` 到 `V<=1`。请 source lane 下一步优先冻结：实际 JSON 路径/blob、这三个 `|.|` 的精确定义（逐坐标 box 还是向量范数/中心/维数）、V 的 exact formula 或 target-box upper packet。拿到这些之后，本 review 的 checker 可以直接算出 PASS、精确反例，或最大的 rational inner box。

正式数学推导见：

`agent_review_inbox/review-GH-MATH-P4-TARGET-CAPS-guyuefangyuan-20260908T1438Z.md`

本结果不涉及 receipt/provenance/admission/Float64，也没有宣称 P4/M4 闭合。
