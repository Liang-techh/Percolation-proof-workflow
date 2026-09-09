---
kind: companion_log
companion_id: companion-T-P5-145-canonical-range-dual-descent-liuguanyi-20260909T1014Z
task_id: T-P5-145-CANONICAL-RANGE-DUAL-DESCENT
source_agent: 柳冠一
created_at: 2026-09-09T10:14:00Z
review_commit: d5adca58a70ff24d658275d6cbd3c5f0d9e261c3
integration_status: pending
admission_label: pending
---

# 柳冠一协作记录：T-P5-145

本轮补的是 T-P5-143 的 source-to-math seam，不与红莲魔尊的 T-P5-144 `G>=0` 半正定 physical-cell nullspace elimination 重叠；这里始终假设 `G>0`。

关键桥是：奇异 `K>=0` 的 canonical range solve 不必要求 producer 输出 `ker K` 基。只要给同源 exact witnesses

`K y=b`, `K w=G y`,

第二条就等价于 `y` 对 `ker K` 的 `G`-正交性，因此自动选出唯一 canonical `y`。同时有 intrinsic identity

`s=Q_G(y)=b^T w`。

更重要的是，同一个 dual witness 给出 `s>4R` 分支的无根小步下降证书。对 `K_d=K+dG` 的 exact sharp floor，存在精确展开

`4(E_d-E_0)=d(4R-s)+d^2 t_d`,

其中 `t_d>=0` 且 `t_d^2<=U s`, `U=Q_G(w)`。令 `h=s-4R>0`，若 checker 验证

`4 d^2 U s <= h^2`,

即可得到 division-free 定量结论

`8E_d+d h <= 8E_0`。

因此 singular boundary 的 `s>4R` lane 不再必须先做 kernel-basis projection、restricted-coercivity 常数或一次 shifted solve 才能知道向右移动确实改善；producer 可直接提一个有理 `d`，trusted side 只做 exact linear identities 与多项式不等式。

下一步若要继续推进，最值得做的是 actual same-key `K/G/b/y/w/R/tau` source packet；若 dual solve 只有近似残差，则必须另立 signed residual bridge，不能把本轮 exact theorem 直接套用。Lean、封不觉独立验证、coverage、Float64/runtime 与 admission/registry 仍保持 OPEN。
