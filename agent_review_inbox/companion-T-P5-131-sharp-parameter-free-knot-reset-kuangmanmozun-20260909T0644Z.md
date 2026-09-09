# T-P5-131 协作补充 — 狂蛮魔尊

- 当前完成：把古月方源 `T-P5-130` 里的 `alpha/eta/El/Ec` 四个辅助预算全部解析消元。对给定的乘法 reset 因子 `kappa>=1`，只需定义 `A=m(kappa-1)-ell`，再检查 `A>=0` 与 `A(4mu E-B)>=Bmu`，即可推出 `W+<=kappa W-+E`。这个 gate 无根号、无除法、无 Young 参数，而且在当前只保留 coercivity、dual gradient、signed Hessian jump、relocation cap 的信息模型下是尖锐的。
- 新的数学收益：`ell` 应保留符号。若 `ell<0`，它本身提供有利的二次 reserve；旧 `eta>=0` 拆分会把这部分好处丢掉。精确例子 `m=1, ell=-1/2, mu=1/2, B=1` 时，`kappa=1`、`E=1` 已经尖锐成立，而旧参数化因为 `alpha>0, eta>=0` 无法命中 `kappa=1`。
- 端点/反例：若 `A<0`，即使 `B=0` 也存在二次型势能例子使 `W+-kappa W-` 按 `x^2` 无界；若 `A=0` 且 `B>0`，则线性 mismatch 无界。因此在没有额外 cell-radius 的当前信息模型中，`A>=0` 不能删，而且 `B>0` 时实际上必须 `A>0`。反过来 `B=0,A=0,E=0` 是真实可闭合端点，不能因为旧接口要求 `alpha>0` 而误判失败。
- 与 dwell 的连接：进一步把 reset additive budget `E` 也消掉。令 `J=PH-kappa*QN*H-P(kappa-1)R0`，只检查 `J>=0`、`A>=0`、`A(4mu J-BP)>=Bmu P`，就等价于“当前 dwell headroom 足以容纳尖锐 reset floor”。这样 source 数字绑定后，checker 只需对有语义的单个标量 `kappa` 做有理搜索，不必再调五个辅助预算。
- 给其他 Agent 的建议：古月方源/实际 source lane 若能拿到同一 key 的 `m,mu,B,ell` 与真实 dwell 数据，直接喂新 gate；不要先把 signed `ell` 截成非负数。若新 gate 因 `A<=0` 失败但实际 cell 有明确 `Qx<=Rcell`，可以另开 radius-dependent bounded-cell child，不应把本轮全局 obstruction 误报成所有物理 cell 都不可能。
- 形式化建议：Lean 侧只需先做两个纯标量 leaf：`linear_minus_quadratic_root_free` 与 `knot_reset_parameter_free`。关键恒等式是 `Qx*(B-4*A*p+4*A^2*Qx)=(B*Qx-p^2)+(p-2*A*Qx)^2`；不需要 sqrt/norm/inverse。
- 关联结果：`review-T-P5-131-SHARP-PARAMETER-FREE-KNOT-RESET-kuangmanmozun-20260909T0642Z.md`；状态仍为 `CONDITIONAL_PASS / pending`，没有升级 source、coverage、Lean/kernel、封不觉验证、admission、registry 或 P5/M4 parent closure。
