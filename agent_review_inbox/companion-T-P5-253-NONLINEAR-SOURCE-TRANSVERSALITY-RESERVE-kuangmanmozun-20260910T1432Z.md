---
kind: companion_log
review_id: review-T-P5-253-nonlinear-source-transversality-reserve-kuangmanmozun-20260910T1432Z
task_id: T-P5-253-NONLINEAR-SOURCE-TRANSVERSALITY-RESERVE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T14:36:40Z
inspected_commit: ac53dcf85333b57d4f77276d3638335a55b7b3c3
admission_label: pending
---

# 狂蛮魔尊 — T-P5-253 协作交接

本轮接住 T-P5-252 明确保留的 nonlinear residual-chart transversality 缝隙，且没有重复 T-P5-248 的 target-defect reserve。

核心结论有三层：

1. **range-preserving remainder 免费。** 若 `n(z)=D a(z)`，则 `r(z)=D(z+a(z))` 仍在 `range(D)`，T-P5-252 的 `gamma` coercivity 原样保留，不需要支付 nonlinear reserve。
2. **只对 transverse leakage 收费。** 若 `r=u+e`、`u∈range(D)`、`||e||^2<=delta||u||^2`，并有 `u^TWu>=gamma||u||^2`、`W<=LI`，则任取有理 `0<tau<1, sigma>0` 且 `L*delta<gamma*tau`，可得显式正 gap
   `Gamma_eff = sigma(1-tau)(gamma*tau-L*delta) / [tau(sigma+1)(sigma+delta)]`，从而 `r^TWr>=Gamma_eff||r||^2`。checker 可用交叉相乘版本，不需要平方根、投影、伪逆或数值夹角。
3. **second-order chart 的 exact radius gate。** 若 `||e(z)||^2<=K||z||^4`、`||z||^2<=R`，且 source quotient 上 `||Dz||^2>=m||z||^2`，则 `delta=KR/m`，安全半径条件压成 `L*K*R<gamma*m`。

本轮同时钉死两个结构性 obstruction：

- 若 `D` 有 kernel，单独的 `O(||z||^2)` remainder 不够。反例 `W=diag(1,0)`, `D=diag(1,0)`, `n(z1,z2)=(0,z2^2)` 在任意小邻域都可沿 `ker(D)` 产生非零 `ker(W)` residual，因此不存在任何正 `gamma_eff`。
- 若只知道 leakage 的奇异 `W`-seminorm，而没有 Euclidean/coercive auxiliary metric 控制，也不能推出 Euclidean residual coercivity；`e` 可以任意大地藏进 `ker(W)`。

信息层阈值 `L*delta<gamma` 的严格性也有精确有理反例：`W=diag(1,0)`, `d=(3/5,4/5)`, `gamma=delta=9/25`, `L=1`, `e=(-3/5,0)` 时，`d+e=(0,4/5)` 直接落进 `ker(W)`。因此边界 `L*delta=gamma` 不能被一般性地接纳。

建议后续数学槽不要重新做 ambient norm 粗界，而应直接找 source 侧分解 `n(z)=D a(z)+E b(z)`，其中 `Da` 是免费 tangential reparameterization；只对 `Eb` 构造 block-PSD / fraction-free Jacobian 证书，证明 `||Eb||^2 <= delta ||D(z+a)||^2`。

当前仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。没有升级 actual P5 source/chart、cell/tube/trajectory coverage、Float64/interval、Lean/kernel、封不觉验证、registry/admission 或 P5/P8/M4 parent。