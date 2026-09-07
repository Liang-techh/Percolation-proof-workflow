---
kind: companion_log
companion_id: companion-T-P4-037-liuguanyi-20260907T1523
task_id: T-P4-037
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T15:23:00-06:00
integration_status: pending
---

# T-P4-037 协作摘要

- 当前完成：把 `T-P4-030` 留下的 combined-Schur 符号问题进一步闭合成可直接消费的数学 adapter。若旧 combined cross block 是 `C0+Cp`、物理修正后是 `C0-Cp`，定义 `X=C0ᵀHCp+CpᵀHC0`，则新旧 Schur quadratic 的差精确为 `Q_- - Q_+ = -2X`，对应 margin 精确满足 `M_- = M_+ + 2X`。
- 最关键的接口：旧 plus-sign certificate 能否原预算复用，不应看最终 `PSD/PASS` 布尔值，而应看 `(M_+,X)`。若 `X>=0` 可无损复用；若 `X>=-Delta` 且 `M_+>=2Delta` 仍可原预算复用；若只有 `M_+>=0`，则把预算增加 `2Delta` 即可安全修复。
- 若旧 artifact 没保存 mixed term `X`，但保存了分离的 `A0=C0ᵀHC0`、`Ap=CpᵀHCp`，则任意有理 `theta>0`、两种符号都满足 `Q_s <= (1+theta)A0+(1+1/theta)Ap`。无除法形式的差恰好是 `(theta C0-s Cp)ᵀH(theta C0-s Cp)>=0`，适合 exact-rational checker/Lean，且比先压成 Frobenius 标量更保留方向信息。
- 明确 obstruction：若只剩旧 `Q_+` 的最终 PSD 状态，没有 `X` 也没有 `A0/Ap`，则不能推出修正后的 `Q_-`。一维 `H=1,C0=1,Cp=-1,D=0` 给出 `Q_+=0`、`Q_-=4` 的精确反例。
- 给梁智炜的建议：受 `R_gain -> R_port=-R_gain` 影响的 combined-S-lemma/Schur artifact 先按三类收割：保留 `(M_+,X)` 的走 exact transport；保留 `(A0,Ap)` 的走 sign-robust matrix Young；只保留最终 PASS 的继续 pending，不必盲目整套重算，也不能直接复用。
- 给形式化层的建议：最小 theorem 只需 `combined_cross_sign_difference`、`combined_schur_margin_transport`、`combined_schur_additive_repair`、`sign_robust_quadratic_young_mul`。先做 fixed-vector quadratic evaluation 版本即可，不需要先搭完整 Loewner-order API。
- 重要边界：如果上游 `Cp` 已经由物理 `R_port` 构造，就不要再做一次负号转换；符号转换与之前 normalization 一样只能发生一次。source binding、Float64、coverage、Lean/kernel、admission 均仍 open。
- 关联结果：`review-T-P4-037-liuguanyi-20260907T1520.md`。
