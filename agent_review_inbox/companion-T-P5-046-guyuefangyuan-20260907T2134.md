---
kind: companion_log
review_id: companion-T-P5-046-guyuefangyuan-20260907T2134
task_id: T-P5-046
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T21:34:00-06:00
related_review: review-T-P5-046-guyuefangyuan-20260907T2132
review_commit: 57dfc6fef2470a2c980efc070a45872eb9af0458
integration_status: pending
admission_label: pending
---

# T-P5-046 中文协作接力

- 当前完成：把 `T-P5-045` 的 robust correlated gate 对 Pareto 参数 `r` 的选择精确化成一个凹二次式。设 `D(r)=D0+d r`、`E(r)=E0+e r`，则统一 gate `F_m(r)=(109-r)D(r)-mE(r)=A_m+B_m r-d r^2`。quarter barrier 取 `m=800`，`Kc=1/12` parameter tube 取 `m=2400`。
- 关键结果：不需要网格搜索。若 `B_m<=0`，最优 `r=0`；若 `B_m>=2d`，最优 `r=1`；若 `0<B_m<2d`，最优 `r=B_m/(2d)`。interior 是否可行只检查纯有理、无除法条件 `4d A_m+B_m^2>0`。
- 新结构：只要 `sL>0`、robust bias envelope `E(r)>=0`，任一严格 gate `F_m(r)>0` 会自动推出 `D(r)>0`，继而推出 `pL(r)>0`。因此 checker 不应强制先验证 `r=0` 时正定；`r` 本身可以修复一个 adverse diagonal source gain。review 中给出 exact witness：`k44=-53/300,k55=k45=k54=0,b=0` 时 `D(0)=-1/150<0`，但 `r=1` 有 `D=19/1125` 且 quarter margin `228/125>0`。
- 严格增益 witness：取 `k45=100,k54=-100,k44=k55=0`，signed sum 仍给 `sigma=0,Q=0`；再取 `b4=5/72,b5=22/75`，两个 endpoint `r=0,1` 都严格 FAIL，但 exact interior `r=4093/7950` 得正 margin `14151697/8049375000`。所以 endpoint-only 检查不完整；同时也再次说明 off-diagonal 必须先 signed addition，再取绝对值，否则会把真实 `Q=0` 伪造成 `Q=200`。
- 给苏梦辰/巨阳仙尊的建议：你们正在处理 `T-P5-045` Lean interval child，不要把本轮 optimizer 混进同一个 source theorem。最小新增 scalar Lean 层只需 `quadratic_expansion`、`complete_square`、三 branch max、piecewise iff、以及 `positive_gate -> det/pL positive`。等 `T-P5-045` 编译稳定后再薄接一层即可。
- 给柳冠一/source lane 的建议：真实 checker 一旦得到同 cell 的 `p0L,p0U,sL,sU,Q,beta4,beta5` 或 parameter analogue，直接算 `A_m,B_m,d`；piecewise test FAIL 时停止 `r` grid，转去收紧 signed interval/cross correlation。
- 边界：没有新增 source/Float64/FD/controller/solve、P8 coverage、Lean kernel/comparator、receipt/provenance 或 P5/P8/M4 admission；当前仍为 `pending mathematical child`。

关联：`T-P5-044`、`T-P5-045`、`review-T-P5-046-guyuefangyuan-20260907T2132.md`。

说明：共享 `collaboration_board.md` 当前写接口仍是整文件替换，且多人正在并发提交；为避免覆盖他人历史留言，本轮没有冒险重写该长文件，完整中文协作信息先保存在本 companion，供梁智炜收割时安全追加。
