---
kind: companion_log
review_id: companion-T-P4-OBSERVATION-KERNEL-REPAIR-kuangmanmozun-20260908T2244Z
task_id: T-P4-OBSERVATION-KERNEL-REPAIR
source_agent: 狂蛮魔尊
created_at: 2026-09-08T22:44:00Z
parent_review: review-T-P4-OBSERVATION-KERNEL-REPAIR-kuangmanmozun-20260908T2242Z
integration_status: pending
admission_label: pending
registry_mutation: false
---

# 给梁智炜与 source lane 的中文接力

本轮接住古月方源刚给出的“二维观测无法控制三维 SPD defect energy”的结构性阻塞，但没有重复他的 actual-source 搜索，而是把**怎样最小修复这个阻塞**做成了 sharp 数学定理。

结论是：设已有观测为 `L d`，新增观测为 `N d`，完整 defect energy 为 `D=d^T H d`、`H>0`。存在有限统一能量 cap 的充要结构条件就是

`ker L ∩ ker N = {0}`。

trusted consumer 不需要做奇异值或开方；只需 source 给出一个有理 `C>=0` 并证明

`C(L^T L+N^T N)-H >= 0`（PSD），

便立刻得到

`D <= C( ||Ld||^2 + ||Nd||^2 )`。

如果共同核非零，则即使两个观测预算都等于零，沿共同核射线 `d=t v` 仍有 `D~t^2` 无界，所以这条 gate 在信息结构上是 sharp 的。

对当前最关心的三维 rank-2 情形，新增**一个标量** `c^T d` 就够了，且充要条件精确是它在旧核方向 `v` 上不消失：`c^T v != 0`。因此 source 并不一定要为了 `D` 单独恢复完整六维 `y=Xz_A`；只要已有两条 defect 观测被正确 reify，再补一条真正看见旧 nullspace 的同源 scalar，就可以闭合三维能量。不过“非零”只保证有限，不保证预算好：例 `c=(1,0,1/100)` 虽然满秩，但旧核方向的能量系数至少要付 `10000`，所以还必须有 quantitative inverse/PSD reserve。

更强的是：若三条 scalar 组成可逆 `T`，source 给 exact rational `U` 满足 `UT=TU=I`，那么无需任何 Cauchy/Young 损失，直接有

`D = y^T (U^T H U) y`, `y=T d`。

若三条观测各有 interval，则三维 convex quadratic 的 box 最大值只需检查 8 个顶点。这个路径保留 signed cross term，通常会比 operator/Frobenius norm 紧得多。

对当前 symbolic block456 `H=M0_CC^-1`，若未来真实同源 packet 最终能给 `|d4|<=b4, |d5|<=b5, |d6|<=b6`，则 exact symmetric-box cap 可直接写成

`Dcap = (50003000000/5000400003)b4^2 + (4000000/200739)b5^2 + (350003000000/5000400003)b6^2 + (100000000000/5000400003)b4*b6`。

最后一项来自负的 `H46`，最大顶点取 `d4,d6` 异号。注意这只是**条件公式**：古月方源已经指出当前 rows4/5 packet 有 controller coefficient omission，不能把旧 payload 按名字直接当成 `d4,d5`。

建议 source 下一棒不要再泛化成“大而全的六维 packet”才开始算，而是先回答最小问题：能否在同一 source/config/domain key 下得到两条已修复 defect observation + 一条 transverse scalar，并给 rational two-sided inverse 或 PSD-cap witness。若可以，`D` 可由 exact reconstruction + 8 顶点直接生成；若第三条仍落在前两条 span 内，则当前 block456 `D` consumer 继续数学上不可闭合。

正式 review：`review-T-P4-OBSERVATION-KERNEL-REPAIR-kuangmanmozun-20260908T2242Z.md`。状态严格保持 `CONDITIONAL_PASS / source-independent mathematics only`，没有 source/coverage/Lean/kernel/admission/registry 升级。

共享 `collaboration_board.md` 当前写接口仍需要整文件 replacement，而且刚有并发新提交；为避免覆盖他人留言，本轮没有直接改写该文件，以上中文接力通过 companion 留给梁智炜安全收割。
