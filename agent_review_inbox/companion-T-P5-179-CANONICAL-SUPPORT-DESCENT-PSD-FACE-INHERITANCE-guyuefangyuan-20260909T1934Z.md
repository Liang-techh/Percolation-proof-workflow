---
kind: companion_log
companion_id: companion-T-P5-179-canonical-support-descent-psd-face-inheritance-guyuefangyuan-20260909T1934Z
task_id: T-P5-179-CANONICAL-SUPPORT-DESCENT-PSD-FACE-INHERITANCE
review_id: review-T-P5-179-canonical-support-descent-psd-face-inheritance-guyuefangyuan-20260909T1931Z
source_agent: 古月方源
created_at: 2026-09-09T19:34:00Z
status: pending
admission_label: pending
---
# 古月方源协作接力：T-P5-179 真支撑集下降与 PSD 父面继承

- 当前完成：闭合 T-P5-178 明确留下的“声明 active support 内有零坐标”边界。任意正交锥零接触都应先精确缩到真正的正支撑集 `S=supp_+(x*)`；在这个支撑上，局部非负自动推出 active block PSD、active gradient 为零、inactive residual 非负，然后可直接复用 T-P5-178 的 critical-cone / range-solve / Schur 结论，不需要再造一套递归算法。
- 关键纠错：不能把包含零坐标的 nominal support 当成全部 signed-active。精确反例 `M=[[0,1],[1,0]]` 在非负正交锥上全局 copositive，`x*=(1,0)` 是零接触；但整个 2x2 矩阵不 PSD。若把第二坐标错误当 signed-active 会得到假 FAIL。真正支撑只有 `{1}`，第二坐标 residual 为正，属于一阶严格保护方向。
- 新的 PSD 父面继承：若 T-P5-177 的 zero-loaded parent block `A0>=0`，且边界 kernel optimizer 写成 `(z>0,0_U)`，则所有被删掉的 `U` 坐标 residual 精确为 0；同时 PSD 自动给出 `B_U ker(A)=0`、`range(B_U^T) subset range(A)`，所以这些 inherited critical rows 的 range solve 不可能失败，且其 generalized Schur 自块 PSD。
- 对 P5 的直接意义：T-P5-177 的边界 optimizer 不要重新对 `U` 跑 first-order floor LP；`g_U=0` 且 residual 恒为 0，它们应直接进入 T-P5-178 critical set。真正新增的 hidden-kernel obstruction 只可能来自 parent face 外部的零 residual 行；不过 `U` 与这些外部行的 reduced cross-coupling 仍可能导致最终 copositivity FAIL，不能把 `U` 整体删除。
- 给 source/CSE lane 的建议：边界 optimizer 应输出 exact partition `S=supp_+(z)`、`U=S0\S`，并保留 parent PSD witness。不要用 Float64 tolerance 猜 active set，也不要在更大的 nominal support 上做 PSD gate。
- 给 Lean lane 的建议：优先形式化 `psdBlock_kernel_cross_zero`，其次是 `psdBlock_rangeSolve_schurPSD` 和两个小标量方向导数 lemma。这样 T-P5-179 的主体可直接复用 T-P5-178，不必复制 mixed-cone 证明。
- 仍未闭合：actual source/key、exact support producer、global copositivity、Float64/interval residual sign、Lean/kernel、封不觉独立验证与 registry/admission 均保持 pending。
- 关联：`T-P5-179-CANONICAL-SUPPORT-DESCENT-PSD-FACE-INHERITANCE`；上游 `T-P5-178`、`T-P5-177`。

注：共享 `collaboration_board.md` 当前 GitHub 写接口仍是整文件 replacement；在多 Agent 并行下无法保证安全原子末尾追加，因此本轮没有覆盖留言板，以上中文协作内容以 immutable companion 形式保存，供下一轮统一收割。