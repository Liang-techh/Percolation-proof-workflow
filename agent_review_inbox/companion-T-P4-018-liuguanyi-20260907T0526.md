---
kind: companion_log
task_id: T-P4-018
source_agent: 柳冠一
created_at: 2026-09-07T05:26:00-06:00
continuation_of: review-T-P4-018-liuguanyi-20260907T0522
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: 梁智炜先协调 P4 的 nominal/acceleration-style 与 generalized-force 两层 scale，再决定 T-P4-017 concrete specialization 是否进入主线
---

# T-P4-018 协作提醒

本轮发现一个会直接影响 P4 常数收割的坐标层冲突：当前 `docs/routeb-p4-kc-force-contract.md` / `routeb_source_contract.py` 把 PMI `f` 中的字面 `kc=1/20` 直接标成 generalized-force scale；但 B45-5/C2 的既有 residual 定义仍是 `l_F = I_B f_B - M0_BB a_B`，其中 `I_B=diag(1/5,1/10)`。在这个 residual 定义下，`kc` 对 `l_F` 的精确贡献必然是 `(q5/100,q4/200)`。

数学上两套坐标都能使用，但必须做 congruence：若 scalar force residual `r_F=j r_A`，则把 Schur auxiliary 改成 `x_A=j x_F` 时，正二次系数必须同时改成 `p_A=p_F/j^2`。channel 4 因此是完全等价的两种写法：`(p_F,c_F)=(3/5,1/100)` 或 `(p_A,c_A)=(15,1/20)`。直接保留 `p=3/5` 却把 `c` 改成 `1/20` 只能视为额外保守 surrogate，不能再称为 exact source-coordinate transport。

给其他 Agent 的建议：在梁智炜协调这一层之前，不要把 `T-P4-017` 的 `1/5` same-coordinate headroom 当成 `l_F` 的 canonical exact headroom；对当前 force-side `1/4` consumer，精确 `kc` 仍只收费 `1/100`，剩余 force headroom 为 `6/25`。若 remainder 有的来自 acceleration-style `f` 层、有的已经是 force-side solve/IEEE remainder，应先统一到 force 坐标再相加：channel 4 的混合预算是 `(1/5)*beta_A + beta_F <= 6/25`。

建议形式化 Agent 优先做 `kc_force_normalization`、division-free `schur_coordinate_congruence` 和 `mixed_normalization_residual_bound`；不要重做 generic Schur theorem。待封不觉独立验证 / 待梁智炜最终整合。
