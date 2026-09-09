---
kind: companion_log
review_id: review-T-P5-128-root-free-ellipsoid-sum-and-center-tracking-kuangmanmozun-20260909T0538Z
task_id: T-P5-128-ROOT-FREE-ELLIPSOID-SUM-AND-CENTER-TRACKING
source_agent: 狂蛮魔尊
created_at: 2026-09-09T05:42:00Z
inspected_commit: 274afb22d19b47aa467684899cdb6017c88c4bd9
integration_status: pending
---

# T-P5-128 中文协作接力

- 当前完成：把 T-P5-127 的 moving-center `p,q` 加权 gate 消元成一个 sharp、无调参、无平方根的二次型求和判据，并确认它与 T-P5-125 的 recentered collar 判据其实是同一个通用 lemma。
- 核心 gate：若 `Q(a)<=A`、`S Q(b)<=G`，令 `D=S(R-A)-G`，只需检查 `D>=0` 和 `D^2>=4SAG`，即可推出 `Q(a+b)<=R`。该条件在只知道两个独立 energy cap 的信息模型下是 sharp 的。
- 对 T-P5-127 直接取 `S=4mu^2`，得到 `D_center=4mu^2(Rout-Rin)-G01`，以及 `D_center^2>=16mu^2 Rin G01`；以后无需再搜索正的 `p,q`。
- 重要边界：旧 `p,q>0` family 在退化端点会漏掉真实 equality。例 `S=1,A=0,G=1,R=1` 时新 gate 精确 PASS，但旧 gate 会要求 `p^2<=0`，任何有限 `p>0` 都无法通过。
- 必须保留 branch guard `D>=0`。只看平方会假通过；`S=A=G=1,R=0` 时 `D^2=4=4SAG`，但 `a=b=1` 给 `Q(a+b)=4>0`。
- 新 theorem 还能直接带 rational reserve：把 `Rout` 换成 `Rout-tau` 即得到显式 source-cell/FD collar；也可递归应用到 piecewise reference 的多 knot center drift。真正 discontinuous jump 仍交给已有 hybrid jump lane，不重复收费。
- 给其他 Agent 的建议：下一步 actual source 不要再提交 Young tuning 参数；优先给同一 key 下更小的 `G01` / `h^2 Gdot`，或给 old-offset 与 center-drift 的 signed cross correlation。若有 signed correlation，应直接消费，不要退回最坏 Cauchy 对齐。
- 关联：`T-P5-125`、`T-P5-127`、`T-P5-128`；正式 review commit `274afb22d19b47aa467684899cdb6017c88c4bd9`。

说明：本轮已读取 `collaboration_board.md`；共享板当前仍需整文件 replacement 才能写入。为避免覆盖并行 Agent 的新留言，本轮中文协作信息以 companion log 保存，待梁智炜统一收割/追加。