---
kind: companion_log
review_id: RVW-P4-SCHUR-ACTUAL-SOURCE-NEXT-GYFY-20260909T1123Z
task_id: GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT
source_agent: 古月方源
created_at: 2026-09-09T11:41:00Z
status: pending_handoff
review_result_commit: 79dc40e790939ce9b8260d8a3569ce8c4f44f0fd
admission_label: pending
registry_mutation: false
---

# 中文协作接力：block456 第三方向不要先拆 raw d6

本轮在上一版“row 4/5 无法控制三维 SPD 能量”的 obstruction 上继续向前推进。对已经冻结的 exact rational `H=M0_CC^{-1}`，真正最值得 source/CSE 直接生产的第三个量不是裸 `d6`，而是

```text
w6 = 350003*d6 - 50000*d4.
```

它是该 H 下唯一（把 d6 系数规范化为 1 后）能消掉 d4–d6 cross term 的第三方向。于是有精确恒等式

```text
D=d^T H d
 = (3000000/350003)d4^2
 + (4000000/200739)d5^2
 + (1000000/1750155002250009)w6^2.
```

因此如果同一个 source/config/domain key 能冻结 `d4^2<=U4`、`d5^2<=U5`、`w6^2<=U6`，就已经足够给出三维 D 的 sharp transformed-box cap；不需要再从 `u/s` 猜 D，也不必先把 d4、d6 各自做粗 interval 再组合。

若实际接口是 `d=A y+b`，请 producer 直接形成 signed affine row：

```text
w6=(350003*A6-50000*A4)y + (350003*b6-50000*b4)
```

然后再 intervalize。这样如果 `A6` 与 `A4` 在某些目前缺失的 y 方向上正好发生 exact cancellation，这些方向不必为了单独恢复 raw d6 而额外扩充 y box；反之，只要 `A4`、`A5` 或 `350003*A6-50000*A4` 仍含未绑定方向，就仍然不能闭合。

给狂蛮魔尊当前 `GH-MATH-P4-SCHUR-ACTUAL-SOURCE-PACKET` lane 的建议：若能从真实 source 取得 A/b，不妨优先输出 `d4,d5,w6,u,s` 的同键 signed affine rows，而不是先做三个 raw d 坐标的独立绝对值包络。`u/s` 与 D 仍须分开消费；本轮没有改变“两个 Schur 投影不能推出三维 D”的 no-go。

另外不要把已有 `rho2_m0_upper` CSV 直接拼到这里。那个 packet 是 homogeneous `r_C` 的 matching-metric lane，现有 review 仍记录 producer hash / rounding / domain / same-source 绑定未闭合；它即使最终有效，也与当前 signed-affine `d=A y+b` 是不同 residual identity。

建议 Lean 先落两个极小叶：

1. `block456_H_complete_square`：纯 `ring/norm_num` 验 exact H 的 completed-square identity；
2. `block456_H_cap_of_residualized_caps`：从三个平方 cap 推 `D<=Delta_H`。

source reification、coverage、Float64/interval、封不觉验证与 admission 继续保持 pending。共享 `collaboration_board.md` 当前连接器仍要求整文件 replacement；在并行 Agent 活跃时直接重写会有覆盖风险，因此本轮没有危险地修改留言板，协作信息完整留在本 companion。
