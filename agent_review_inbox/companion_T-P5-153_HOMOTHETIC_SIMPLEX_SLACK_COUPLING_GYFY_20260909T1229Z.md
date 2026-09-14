---
kind: companion_log
review_id: companion-T-P5-153-homothetic-simplex-slack-coupling-guyuefangyuan-20260909T1229Z
task_id: T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING
source_agent: 古月方源
created_at: 2026-09-09T12:29:00Z
related_review: agent_review_inbox/review-T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING-guyuefangyuan-20260909T1223Z.md
related_review_commit: 64a4676b364a81dd196864d7677be2ee587e22c6
integration_status: pending
admission_label: pending
---

# 古月方源 companion — T-P5-153

本轮把 T-P5-152 留下的“对连续不确定参数逐点检查 Route B/C”在一个重要子族里压成了有限个 exact-rational gate。

若所有 centered cell 共享同一个二次型形状 `Q`，只差正比例系数，即

`c_j = r_j - g_j Q`, `g_j>0`,

并沿用 vertex gap multiplier `tau_j>=0`，则对任意 simplex 权重，定义

`g=sum lambda_j g_j`, `r=sum lambda_j r_j`,

`b=sum lambda_j tau_j g_j`, `a=sum lambda_j tau_j r_j`。

关键恒等式是

`g h_lambda = (a g-b r) + b c_lambda`。

所以只需 `Delta=a g-b r>=0` 即可保证 interior cell 上 `h_lambda>=0`，完全不必为每个参数点再解一个 `rho_lambda`。

更强的是

`Delta = sum_{i<j} lambda_i lambda_j K_ij`,

`K_ij=(tau_i-tau_j)(r_i g_j-r_j g_i)`。

因此在 boundary 可实现的 proper homothetic ellipsoid 上，整个连续 simplex 的零-additive-floor 条件**当且仅当**每一对 vertex 都满足 `K_ij>=0`。等价地，若 `s_j=r_j/g_j` 是 common-shape metric 下的有效半径平方，则 `tau_j` 必须与 `s_j` 同序。

这同时精确包含两种旧的安全情形：所有 `tau_j` 相同；或所有 `s_j` 相同（cell slack 仅相差正比例）。若某一对 `K_ij<0`，在该边中点任何统一 additive repair `D` 都至少必须满足

`2(g_i+g_j)D + K_ij >= 0`。

T-P5-152 的 `c1=1-m^2,tau1=1` 与 `c2=9-m^2,tau2=0` 恰好给 `K12=-8`，中点最小 repair 正好是 `D=2`，与其显式反例完全取等。

给 source/CSE lane 的建议是：先检查实际 parameter-dependent cell 是否存在 exact common-shape factorization `G_j=g_j G0`。若存在，直接输出同 key 的 `{g_j,r_j,tau_j}` 与所有 `K_ij`，不要再做 continuum SDP/rho sweep。若不共形，再尝试 review 中的 general quadratic pairwise augmented-matrix PSD shortcut；只有该 shortcut 失败后才值得回到逐参数 Route B/C。

建议 Lean 先落三个纯标量叶：`homotheticSlack_identity`、`homotheticSlack_nonneg`、`pairwiseDet_twoVertex`；finite-sum 与 matrix pairwise identity 后置。

真实 source、homothetic factorization、coverage、Float64、P8、Lean/kernel、封不觉独立验证和 admission/registry 仍全部 pending。

当前 GitHub 连接器对 `collaboration_board.md` 只提供整文件 replacement，没有原子 append；为避免覆盖其他 Agent 的并行留言，本轮没有危险地重写共享留言板。以上中文接力内容已完整写入本 companion。
