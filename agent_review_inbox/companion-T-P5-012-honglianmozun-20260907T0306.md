---
kind: companion_log
task_id: T-P5-012
source_agent: 红莲魔尊
created_at: 2026-09-07T03:06:00-06:00
related_review: review-T-P5-012-honglianmozun-20260907T0304
---

# T-P5-012 协作摘要

- 给 source/checker lane：`delta_ctrl` 不要先压成一个总常数。优先拆成 `S q + ell*w + b + K q + r`，其中 `S` 对称、`K` 反对称；`Sq+ell*w+b` 可进入储能，真正剩余的是 `Kq+r`，以及非零 ramp 下不可避免的 `-c ell^T q` 注入项。
- 给 P8 lane：若能给同域 `|q_i|<=Q_i` 与 `w=c*t` 覆盖，就同时能给新的储能上界 `Phi_max` 和 ramp-work 界 `|c| sum_i |ell_i|Q_i`；这比把 `ell*w` 当成恒定 force bias 更精确。
- 给形式化 lane：最小 theorem 是 `parameter_storage_shift_ledger` 和 affine directional identity `D Phi(v,c)=(Sq+ell*w+b)^T v+c ell^T q`；不要先做大 ODE API。
- 关键 obstruction：`c!=0` 时，仅证明“对每个固定 w 都是 q-gradient”不足以零成本移入储能；若 force 真依赖 `w`，必须留下 ramp-work。非保守常力余项也不能靠二次阻尼在整个 `v=0` 邻域严格吸收，精确最坏功率增量是 `r^T D^{-1}r/(4g)`。
- 关联：`T-P5-008`、`T-P5-011`、`T-P4-007`、`T-P8-008`；保持 `pending`，待封不觉独立验证、待梁智炜最终整合。
