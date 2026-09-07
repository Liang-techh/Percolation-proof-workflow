---
kind: companion_log
task_id: T-P4-011
source_agent: 狂蛮魔尊
created_at: 2026-09-07T00:48:00-06:00
---

### 协作提示

- 已完成 corrected `kc=1/20` 的精确 Schur/Young 数学：旧 `1/100` residual envelope 已确定过严且不能复用，但新的 `c=1/4` sharp-Schur consumer 足够容纳该项。
- 若 P4 typed adapter 能把 channel-4 的 Schur 坐标绑定为 `y=q5`、channel-5 绑定为 `y=q4`，则 `kc` 每通道只消耗 `1/20` 的线性 residual 系数，给其他同坐标 force residual 留下干净的 `1/5` 系数预算；block-4 的 exact sharp margin 仍很大。
- 若当前 auxiliary `y` 与物理交叉坐标保持独立，则存在精确反例：`q5=1,y=0,p=3/5,x=-1/12` 给出 `Q=-1/240`。所以只给 joint-limit 或 `Pstate<=28/5` 的绝对 residual 上界无法完成 universal Schur closure。
- corrected `rho_kc` 还有一个很有用的状态相对恒等式：`Pstate - 600*||rho_kc||^2 = (4/5)(v4^2+v5^2)`，故本地 `Pstate<=28/5` 时 `||rho_kc||^2<=7/750`；这与全局 joint-limit 的 `pi^2/200` 必须分开记录。
- 建议下一步：形式化 `kc_state_identity / kc_cross_schur / kc_plus_other_quarter`；P4 source/interface lane 只需回答 `y<->q_cross` typed mapping，若不能证明，就改为显式 q-quadratic slack，不要继续调 stale `1/100` 常数。
- 关联：`T-P4-011`，`review-T-P4-011-kuangmanmozun-20260907T0046.md`。
