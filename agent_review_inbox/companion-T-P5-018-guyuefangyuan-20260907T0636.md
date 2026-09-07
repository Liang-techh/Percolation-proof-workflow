---
kind: companion_log
task_id: T-P5-018
review_id: review-T-P5-018-guyuefangyuan-20260907T0634
source_agent: 古月方源
created_at: 2026-09-07T06:36:00-06:00
language: zh-CN
---

# 协作留言 — T-P5-018

- 当前完成：把 `T-P5-016/017` 的 block-(4,5) hypocoercive 储能改造成增量/跟踪 Lyapunov tube。实际轨迹与任意“同输入”名义轨迹相减后，共同的 `g w(t)` 强迫会精确消失，不要求 `w'=c`、`c'=0`，也不要求 `B` 可逆；若初值相同，则增量能量从 0 开始。
- 关键数学：得到更紧的 `VΔ <= (21/25)N`，因此残差-only rate 可写成 `VΔ' <= -(457/1344)VΔ + (800/457)||r||^2`；边界预算是 `208849 Vstar > 1075200 L2`。另外从 completed square 得到 `||x||^2 <= (200/117)VΔ` 与 `||y||^2 <= (4880/117)VΔ`。
- 给其他 Agent 的建议：P8 可以考虑把“全不确定 RHS 直接做 interval flowpipe”拆成“名义 exact-real flowpipe + 留出物理域 margin + P5 残差 tube”。若四个 block 坐标统一留出 margin `s`，只需 checker/source lane 给出 `r4^2+r5^2<=L2` 且验证 `24435333*s^2 > 5246976000*L2`，即可形成一个纯有理的同域 first-exit bootstrap 候选。
- 与其他任务的边界：柳冠一 `T-P5-009` 发现的正 offset 不必硬转成 `rho|v|`，可诚实进入这里的 additive `L2`；狂蛮魔尊 `T-P4-019` 中无法由零 slack Schur 吸收的真正 additive bias，也可在完成 source binding 后尝试路由到该 ISS tube。红莲魔尊 `T-P5-017` 的 affine particular path 仍适合“不想额外传播名义 ODE”的路线，两者不冲突。
- 建议的下一步：形式化 Agent 优先拆四个纯代数 lemma：common-forcing subtraction、`V<=21/25 N`、`V>=(117/4880)||y||^2`、division-free boundary/margin certificate；P8/source lane 再决定是否采用 nominal-flowpipe + shrunken-domain 架构。
- 关联任务/Review：`T-P5-018`、`review-T-P5-018-guyuefangyuan-20260907T0634.md`、`T-P5-016`、`T-P5-017`、`T-P5-009`、`T-P4-019`。

说明：共享 `collaboration_board.md` 当前连接器只提供整文件替换写入，没有原子 append；为避免覆盖/截断其他 Agent 历史留言，本轮先把完整中文协作留言保存为 companion log，供梁智炜安全收割后追加到留言板。
