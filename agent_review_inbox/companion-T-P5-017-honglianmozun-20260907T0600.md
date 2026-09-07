---
kind: companion_log
task_id: T-P5-017
review_id: review-T-P5-017-honglianmozun-20260907T0558
source_agent: 红莲魔尊
created_at: 2026-09-07T06:00:00-06:00
integration_status: pending
---

### 2026-09-07 06:00 — 红莲魔尊
- 当前完成：在 `T-P5-016` 的 moving-equilibrium 建议上继续推进，发现只做 `q=x+h w` 还不够；因为 `c'=0`，可以再加一个静态 `r c` 平移，取 `h=B^{-1}g`、`r=-B^{-1}Dh`，从而把 `w=c t` 的幅值 forcing 和剩余的常数 ramp-rate forcing **同时精确消掉**。变换后得到 `M y'+D y+B x=-l`，能量账本只剩真实 generalized-force residual `l`。
- 发现的问题：这个方法把 ramp 代价从“持续功率收费”搬到了“初始相对能量”。对 `q(0)=v(0)=w(0)=0`，精确得到 `V_rel(0)=C0 c^2` 且 `C0<1/12`；因此 `c^2<=3` 时 `V_rel(0)<1/4`。若同域 `||l||^2<=L2` 且 `5120000 L2<208849`，则 `V_rel=1/4` 边界严格向内，是一个完全有理的 residual-only barrier。
- 给其他 Agent 的建议：形式化层只需先做 `Bh=g`、`Br+Dh=0`、shifted scalar block substitution 和 `V0<1/4` 四个小 lemma，再复用 `T-P5-016` 的 hypocoercive rate；source/P4 lane应继续给 force-coordinate `l` 的同域平方界，不必再给 ramp-work budget。
- 建议的下一步：有限 `[0,1]` 主线仍保留已编译的 `T-P5-013/015` 作为 baseline；若目标转向更长时域/跟踪，优先比较本 affine-particular-solution 路线。必须继续单独处理 P8 物理 `q,w` domain coverage，因为相对能量衰减并不意味着绝对 ramp 轨迹留在有限 source box。
- 关联任务/Review：`T-P5-017`、`review-T-P5-017-honglianmozun-20260907T0558.md`、`T-P5-016`、`T-P5-013`、`T-P4-018`。

> 说明：共享 `collaboration_board.md` 当前只能整文件替换，缺少安全原子 append；仓库已有追加截断事故记录。本轮不冒险覆盖并行留言，故先把中文协作摘要写入 companion log，供梁智炜收割时安全并入留言板。
