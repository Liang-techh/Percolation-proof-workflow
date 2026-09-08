---
kind: companion_log
review_id: companion-T-P5-041-liuguanyi-20260907T2023
task_id: T-P5-041
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T20:23:00-06:00
related_review: review-T-P5-041-liuguanyi-20260907T2020
review_commit: f00df0c286872089548d203eef70f8c7b805d966
integration_status: pending
admission_label: pending
---

# T-P5-041 协作摘要 — 柳冠一

- 当前完成：补上 `T-P5-022/023/028` 的 source component transport 与最新 `T-P5-040` mixed relative-plus-additive consumer 之间的数学桥。关键恒等式是对当前 frozen block-(4,5) 储能取 `u=x+y` 后，严格有 `V=(1/2)u^T M u+(1/2)x^T(K+D-M)x`；也就是说 residual power 坐标 `u` 与 transverse 坐标 `x` 在该储能里正好块对角。
- 新接口：若 source 已在 `(u,x)` 坐标给出一行 `|l_a|<=r4|u4|+r5|u5|+t4|x4|+t5|x5|`，则任选 `0<=rho_i<=r_i`，都能在 `V<=Vstar` 上生成 exact-rational additive square budget `B_i(rho_i)`。quarter barrier 时公式只含 `m4,m5` 与显式有理 `H^{-1}`，可直接送入 `T-P5-040` 的 polynomial gate；取 `rho=0` 又自动退化成 `T-P5-039` 的 component additive caps。
- 对现有 `K_path` 的安全 fallback：原 `(x4,x5,y4,y5)` 非负行 `(p4,p5,q4,q5)` 可转为 `(u,x)` 行 `(q4,q5,p4+q4,p5+q5)`。这不需要新的 source 假设，但会损失 cancellation。
- 最重要的 source 建议：如果后续想真正利用 relative residual 结构，应在取绝对值以前先做 signed Jacobian 坐标变换 `(J_x,J_y)->(J_y,J_x-J_y)`。例如真实 residual `l=alpha(x+y)` 的 transverse Jacobian 本来精确为 0；若先做 entrywise abs，再从旧 `K_path` 转换，就会错误产生 `2|alpha|` 的 transverse charge。这个信息一旦被绝对值抹掉，后面的 Frobenius/orthant consumer 都无法恢复。
- anchor 边界：`T-P5-022` 的 `K_path` 默认是 centered transport，不能直接冒充 full one-trajectory residual。若要接 `T-P5-040`，应保留旧 anchor adapter 在 collapse 到总 `B2` 之前的 component boxes `C4,C5`，再与 centered component budget 分别合并；不能只留下一个 isotropic `B2` 后假装 anisotropic 信息仍在。
- 建议下一步：source/checker lane 若能保留 transformed signed interval rows，优先输出 `(r4,r5,t4,t5)`；否则直接消费旧 `K_path` fallback。Lean lane只需形式化 `storage_ux_diagonalization`、energy-dual square bound、row-to-mixed budget、signed-Jacobian transform 四个小 theorem，不必重做 `T-P5-040` 的能量吸收。
- 仍未闭合：真实 Julia/Float64 Jacobian interval、signed row correlation、anchor component boxes、controller/solve/FD remainder、first-exit/cell/trajectory coverage、Lean/kernel/comparator/admission。结果继续严格保持 `pending`。
