# T-P4-019 协作补充 — 狂蛮魔尊

- task_id: `T-P4-019`
- source_agent: 狂蛮魔尊
- status: `pending`

本轮得到的关键协作结论是：`T-P4-007` 中若某个 execution remainder 真的是与状态无关的 additive bias，就不能因为 Schur 还有剩余曲率而直接吸收。对

`Q = p x^2 + 2x(a y+b) + d y^2 + s`

在 `Delta=pd-a^2>0` 下，统一吸收 `|b|<=B` 的尖锐条件是

`Delta*s >= d*B^2`。

这里的 `s` 必须是证书里真实存在、且独立可用的常数正储备；若原证书没有该项，就只能取 `s=0`，于是任何 `B>0` 都不可能闭合。建议 source/IEEE lane 把 `DeltaM/DeltaC/DeltaG/delta_ctrl/solve defect` 先分类成“同坐标相对 / 横向状态相对 / 真正 additive”三类，再交给对应 consumer，避免把常数 bias 重新塞进 `1/4|q_cross|`。

canonical block 4 的两个精确收费口径：

- 若总 same-coordinate 系数已经花到 `a=1/4`：`37503000000001*s >= 583338333333335*B^2`；
- 若只消费 canonical `kc=1/20`：`337503000000001*s >= 583338333333335*B^2`。

因此若后续确认存在真正 additive 的 solve/IEEE 误差，保留 same-coordinate Schur 曲率会显著提高可承受的 additive budget；不要无必要地把 `beta` 花满到 `1/5`。

关联正式结果：`review-T-P4-019-kuangmanmozun-20260907T0550.md`。待封不觉独立验证 / 待梁智炜收割与最终整合。
