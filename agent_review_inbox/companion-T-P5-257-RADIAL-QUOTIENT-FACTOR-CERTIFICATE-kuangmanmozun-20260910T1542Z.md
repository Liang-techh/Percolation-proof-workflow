---
kind: companion_log
task_id: T-P5-257-RADIAL-QUOTIENT-FACTOR-CERTIFICATE
source_agent: 狂蛮魔尊
created_at: 2026-09-10T15:42:00Z
review_commit: 44b112238f3be56d3915e4c8aa4270d40a79830e
status: pending
admission_label: pending
---

# 狂蛮魔尊 — T-P5-257 协作记录

本轮没有接手 provenance、receipt、admission 或重复验证，而是直接续攻 T-P5-256 留下的 radial fallback。

## 当前完成

证明了 radial packet 与 mixed Hessian packet 之间的严格逻辑分层。对 rational `D` 先取独立行基 `Dbar`，写成 `D=L Dbar`，则 quotient metric `W=L^T L>0` 且 `||D theta||^2=(Dbar theta)^T W(Dbar theta)`。若 contracted polynomial `F(s,theta)=B(s,theta)theta` 在中心正半径椭球上满足 radial inequality，则它在 `ker(D)` 上必为零；利用 rational kernel/right-inverse 坐标，可构造 exact polynomial factorization

`F(s,theta)=A(s,theta) Dbar theta`。

因此正确路线是“先 quotient factor，再做 Gram”，而不是继续强迫 ambient mixed matrix annihilate `ker(D)`。

## 新 exact gate

把 `theta=R0 u+Nz` 代入后，精确计算 `Rem(s,z)=F(s,0,z)`：

- `Rem=0`：存在 polynomial quotient factor，可以继续 closure；
- `Rem!=0`：在任意中心正半径 source ellipsoid 上都能找到任意小的 kernel witness，使 RHS 为 0、LHS 为正，因此这是实际数学 FAIL，而不是 certificate-not-found。

若 quotient factor `A=sum c_i A_i` 且 source 给出 correlated packet `cc^T<=qC`，只需比较

`S^T(C tensor I)S <= kappa W`

即可推出 radial bound。对线性 `A(theta)`，又可用 `det(M),adj(M)` 做完全 fraction-free 的 rational PSD gate。

## 关键反例

取 `b(x,y)=xy`、`D=[1,0]`、`q=x^2+y^2`。Hessian contraction 为 `B=[y,x]`，radial vector `F=2xy=(2y)Dtheta`，并且

`F^2 <= 4q||Dtheta||^2`，

且 `4qx^2-F^2=4x^4` 是单个 quotient square，`kappa=4` sharp。

但 mixed packet 对 kernel test vector `e2` 要求 `x^2<=0`，所以任何 finite `kappa` 都失败。这个例子证明 mixed failure 绝不能上推成 radial/end-point failure。

另一个边界是 `F=x=Dtheta`：虽然 kernel factor 已存在，但 `F^2<=kappa q(Dtheta)^2` 在原点附近不可能有有限 `kappa`。因此必须同时保留二阶/order-smallness gate；仅有 ideal divisibility 不足。

## 给其他 Agent 的建议

如果后续 source lane 能生成真实 `F=B(theta)theta`，优先先做 exact kernel remainder 和 row-space factorization，不要直接跑 ambient Hessian operator-norm。若 quotient 维数大于 1，下一条真正值得数学槽处理的是 realized-direction scalar inequality

`u^T[kappa q W-A^T A]u>=0`

与 quotient matrix PSD gate 的差距；可以寻找 rank-one syzygy 或 degree-bounded quotient-SOS，从而进一步减少保守性。

当前仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。actual P5 source、coverage、Float64、Lean/kernel、封不觉独立验证、registry/admission 与 parent closure 均未升级。
