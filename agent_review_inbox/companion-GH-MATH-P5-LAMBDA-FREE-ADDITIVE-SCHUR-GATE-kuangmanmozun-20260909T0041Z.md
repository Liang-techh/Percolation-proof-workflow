---
kind: companion_log
task_id: GH-MATH-P5-LAMBDA-FREE-ADDITIVE-SCHUR-GATE
review_id: GH-MATH-P5-LAMBDA-FREE-ADDITIVE-SCHUR-GATE-kuangmanmozun-20260909T0038Z
source_agent: 狂蛮魔尊
status: handoff
admission_label: pending
---

## 中文协作接力

本轮把当前 additive-port Schur consumer 里的辅助参数 `lambda>1` 完全消掉了。若同一 PSD metric `H` 下已经有真实 port cap `q_H(d)<=Delta`，令

`L=q_H(v_ref)`，`C=beta-target-L-Delta`，

则只需检查两个无除法条件

`C>=0`，`C^2>=4*L*Delta`，

即可直接得到 `target<=beta-q_H(v_ref+d)`。如果还要显式正余量 `tau`，把 `C` 改成 `beta-target-tau-L-Delta` 即可。这个 gate 只用加法、乘法、平方和序关系，不需要矩阵平方根、`lambda`、除法或浮点优化。

它在 `L>0,Delta>0` 时正好等价于“存在某个有限 `lambda>1` 使旧 Schur numerator 非负”，但严格修复了旧接口的两个边界洞：`Delta=0,A=L` 与 `L=0,A=Delta` 的真实总 residual 都可以在 equality 上成立，而任何有限 `lambda>1` 都会拒绝。另一个精确 regression 是 `L=4,Delta=1,A=9`：真实总量与新 gate 都在 equality 上通过，固定 `lambda=2` 却给 numerator `-1`；所以固定 lambda 失败只能叫策略失败，不能叫 Schur 数学失败。

对“additive forcing 能不能塞进 homogeneous gain”也得到明确 no-go。若能量变量 `x>=0` 上只有 `q_H(v)<=kappa*x`、`Delta<=rho*x+B`，而 headroom 纯齐次 `beta-target>=eta*x`，只要 `B>0` 且域含 `x=0`，从这些 envelope 本身就不可能统一闭合；在原点允许 `v=0`、`q_H(d)=B` 的一维反例会直接打破 target。即使另加常数 headroom `a0=B`，当 `kappa>0,B>0` 时也通常只够闭合单点 `x=0`：小正 `x` 的 cross charge 是 `O(sqrt(x))`，而剩余 affine headroom 只有 `O(x)`，因此整个低能邻域仍失败。要覆盖邻域必须有严格额外 additive floor、证明实际 `B` 消失、排除低能区域，或拿到 signed correlation。

若 source 以后给出 affine energy envelopes `L<=kappa*x`、`Delta<=rho*x+B`、headroom `>=a0+eta*x`，可把全区间检查压成一个线性条件和一个二次多项式 `P(x)>=0`；二次最小值也已经给出完全有理、无除法的端点/顶点 case split。建议下一棒在真实 K7/graph packet 出现后直接输出同源 `(L,Delta,beta,target)`，优先走这个 discriminant gate；只有确实需要兼容旧接口时再选固定 `lambda`。

当前仍是纯数学 `pending` child；没有 source binding、K7 实例、coverage、Lean/kernel、registry 或 admission 升级。
