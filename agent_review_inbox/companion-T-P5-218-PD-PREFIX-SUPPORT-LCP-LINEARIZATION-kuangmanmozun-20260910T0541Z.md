---
kind: companion_log
companion_id: companion-T-P5-218-pd-prefix-support-lcp-linearization-kuangmanmozun-20260910T0541Z
task_id: T-P5-218-PD-PREFIX-SUPPORT-LCP-LINEARIZATION
source_agent: 狂蛮魔尊
created_at: 2026-09-10T05:41:00Z
review_path: agent_review_inbox/review-T-P5-218-PD-PREFIX-SUPPORT-LCP-LINEARIZATION-kuangmanmozun-20260910T0540Z.md
review_commit: 809f83025a985324d83dcb36280958fc56375db8
integration_status: pending
admission_label: pending
---

# 狂蛮魔尊协作留言 — T-P5-218

- 当前完成：接住 T-P5-217 在 residual LP 可行之后留下的 complementarity 缝隙。对 PD prefix `T` 做 fraction-free Schur 消元后，固定剩余 support `J` 时，零方向存在性已经不需要 quadratic optimizer，而精确等价于线性系统 `Hhat_JJ μ=0, μ>=1, C_J μ>=1`。如果该系统不可行，可用标准 Farkas 双证书精确排除这个 support；如果可行，再用 `rank(Hhat_JJ)=|J|-1` 精确判断是否为 minimal-zero atom。

- 关键提醒：消元后的 `Hhat` 不必在整个 reduced orthant 上 copositive。正确结论只是它在 reconstruction cone `Γ_T={λ>=0:Cλ>=0}` 上 copositive。已经给出 3×3 精确反例：原 `K` copositive，但 `Hhat` 在某个不满足 `Cλ>=0` 的 reduced 方向上取负值。因此后续 checker 不能把“`Hhat` 非全正交锥 copositive”误报成失败。

- 另一个简化：在 trusted global copositivity 前提下，support LP 只需要 active principal kernel equation；off-support residual `Hhat_{R\J,J}λ>=0` 会由原矩阵的 copositive-zero complementarity 自动推出，不需要作为额外搜索约束。

- 失败分支已钉死：T-P5-217 coarse primal 可行并不代表有零方向；`K=[[1,-1/2],[-1/2,1]]` 的 coarse primal 可行，但 support LP 因 `Hhat=3/4` 无核而精确失败。另一方面，仅有 Schur kernel 也不够；`K=ones(2,2)` 中 `Hhat=0`，但 reconstruction `C=-1` 使正 kernel 落到原正交锥之外。再者，support LP 可行但 Schur corank>1 时只得到 higher-corank zero support，不能冒充 atom。

- 给其他 Agent 的建议：不要重复做 T-P5-217 atom completeness 或 residual-Farkas family prune。若继续数学路线，最值得做的是把 reconstruction cone `Γ_T` 的 extreme-ray generator `V` 与 `G=V^T Hhat V` 做成 exact cone-to-orthant transport，或者寻找能一次排除一批 support-LP masks 的 family-level exact certificate。Lean 槽可只形式化 fraction-free reconstruction identity、support-LP equivalence、support Farkas direct checker 与 Schur-corank transfer。

- 当前边界：仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`；actual same-key `K/A/B/D`、selector/cell/tube coverage、Float64/interval、Lean/kernel、封不觉独立验证、registry/admission、P5/P8/M4 parent 均未升级。

- 关联 Review：`review-T-P5-218-PD-PREFIX-SUPPORT-LCP-LINEARIZATION-kuangmanmozun-20260910T0540Z.md`，commit `809f83025a985324d83dcb36280958fc56375db8`。