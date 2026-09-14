---
kind: companion_log
task_id: T-P5-147-SEMIDEFINITE-CELL-AFFINE-RESIDUAL-CAP
source_agent: 狂蛮魔尊
created_at: 2026-09-09T10:50:00Z
review_path: agent_review_inbox/review-T-P5-147-SEMIDEFINITE-CELL-AFFINE-RESIDUAL-CAP-kuangmanmozun-20260909T1047Z.md
review_commit: 3ad8366c1317e48bbdd0678c77ce0a4370cec0bf
admission_label: pending
---

# T-P5-147 协作记录 — 狂蛮魔尊

- 当前完成：补上 T-P5-144 明确留下的 `A u=b_N` 近似求解缝隙，但保持 `A L=H_NM` 的 cross solve 精确，不与古月方源正在处理的 T-P5-146 inexact-dual lane 重叠。
- 核心结论：令 `r=b_N-Au`。在 `A⪰0` 的无界物理 nullspace 中，存在有限统一 residual charge 的充要条件是 `r∈range(A)`；一个完全 root-free 的等价证书是存在 `sigma>=0` 使 `sigma A-r r^T⪰0`。该证书直接推出 `4(r^T e-e^T A e)<=sigma`。
- 常数强度：若 `Az=r`，内禀 residual energy `rho=r^T z` 与解的选择无关，最小可行 `sigma` 恰为 `rho`，真实最坏 charge 恰为 `rho/4`。因此 `1/4` 不是 Young 松弛，而是 sharp 常数。
- 对 quotient 的影响：在 cross solve 精确时，近似 affine solve 不需要削弱 `b_eff` 或 `H_eff`；只把常数改成 `C_bar=C+(b_N^T u+r^T u)/4+sigma/4`。若后来拿到 exact correction，保守损失精确等于 `(sigma-rho)/4`。
- 明确 obstruction：即使 residual 的欧氏范数任意小，只要含有非零 `ker A` 分量，就会沿零曲率方向产生线性无界逃逸；因此 Float64“小 residual”或普通 norm tolerance 不能替代 range/PSD certificate。
- 给其他 Agent 的建议：后续 source 若能交 `A,L,u,r,sigma`，优先验证 rank-one PSD cap，不要先做 pseudoinverse 或重新调 Young 参数。若实际问题连 `A L=H_NM` 也是近似的，应另拆 matrix-valued cross-residual child，不能把它塞进本轮的 `sigma`。
- 当前边界：仍为 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`；未证明真实 source、same-cell coverage、Float64/runtime、Lean/kernel、独立验证、registry 或 P5 parent closure。
