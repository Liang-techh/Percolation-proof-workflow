---
kind: companion_log
task_id: T-P4-015
source_agent: 柳冠一
created_at: 2026-09-07T03:28:00-06:00
related_review: review-T-P4-015-liuguanyi-20260907T0326
---

# T-P4-015 协作摘要

- 给 source/IEEE lane：对 `DeltaG/delta_ctrl/solveDefect` 不要只给总绝对值。先分别报告参考点值 `R(ref)` 与中心化增量；只有增量才有资格尝试做相对/横向路由。
- 给 interval lane：若是 exact-real 光滑层，可在同一 P8 box 上给 cross 坐标导数界 `beta` 与其余坐标导数界 `gamma_j`；这样自动得到 `|R| <= beta|y| + sum gamma_j|z_j|`。若是 Float64 real-lift 层，不要直接对解析公式求导冒充 execution Lipschitz，优先给直接增量 enclosure 或先拆 smooth + IEEE remainder。
- 给 P4 certificate lane：若现有横向正储备为 `H=sum h_j z_j^2`，只需消费一个 dual budget `kappa=sum gamma_j^2/h_j`。block 4 的联合条件是 `(1/100+beta_total)^2 + d4*kappa <= p4*d4`；历史 `6/25` 是所有 same-q5 项共享的预算，不是每项各自拥有。
- 关键 obstruction：`R(0,0)=0` 不等于 `R(0,z)=0`。例如 `R(y,z)=z` 已足以排除纯 `|R|<=beta|y|`；参考点非零 bias 在没有独立常数 slack 的同次 Schur 块里也无法靠状态二次项吸收。
- 给形式化 lane：最小接口先做 `slice_decomposition`、`slice_increment_envelope`、`relative_plus_quadratic_transverse_schur`；MVT/derivative witness 与有限维 weighted-Cauchy 可作为后续独立 bridge，不要把 Float64 calculus 混进纯代数 theorem。
