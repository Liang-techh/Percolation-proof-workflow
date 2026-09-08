---
kind: companion_log
task_id: T-P5-084-NONLINEAR-CHART-SECANT-GEOMETRY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T09:57:00-06:00
status: pending
review_commit: aa09cbc1fa140694696b81690657b948e0b63135
---

# T-P5-084 中文协作留言 — nonlinear chart 的 global secant / inverse reserve

本轮没有发现梁智炜对“狂蛮魔尊”的新点名。柳冠一的 T-P5-082 已把 nonlinear differential pullback 和 finite-step curvature defect 做清楚，古月方源的 T-P5-083 又补了 Euler segment coverage；我补的是 T-P5-082 明确留下的另一块：**chart injectivity / image coverage 不能从局部 Jacobian 可逆性直接推出。**

最重要的反例是

`T(x,y)=(e^x cos y, e^x sin y)`，`(x,y) in [0,1] x [0,2pi]`。

这里

`DT^T DT=e^(2x) I >= I`，并且 `det DT=e^(2x)>0`，

所以每一点 Jacobian 都方向保持、最小奇异值至少为 1；但

`T(0,0)=T(0,2pi)`。

因此 `sigma_min(DT)>=mu`、`det DT>0`、local inverse theorem 都不能单独充当 global chart certificate。真正需要控制的是沿 source segment 的平均 Jacobian，也就是 secant operator。

本轮给出两个可落 trusted checker 的充分 gate。

第一种是 fixed metric `H` 下的强单调 Jacobian：若整个凸 cell 上

`v^T(H DT + DT^T H)v >= 2 mu v^T H v`，`mu>0`，

则对任意两点都有

`<T(z)-T(w),z-w>_H >= mu ||z-w||_H^2`

以及

`||T(z)-T(w)||_H >= mu ||z-w||_H`。

所以直接得到 global injectivity 和 inverse `1/mu`-Lipschitz reserve。这个 gate 很干净，但只是充分条件；例如 90 度旋转是完美 isometry，symmetric part 却为 0，不能因此误判 FAIL。

第二种更适合一般 orientation：source 选一个固定可逆 reference matrix `A`，证明

`||A v||_H >= m ||v||_H`

和

`||(DT(u)-A)v||_H <= eps ||v||_H`，其中 `0<=eps<m`。

则整个 convex cell 上精确得到

`||T(z)-T(w)||_H >= (m-eps)||z-w||_H`。

这个 `m-eps` 在现有 envelope 下是 sharp 的；一维 `T(z)=(m-eps)z` 精确达到。它不会像逐点 singular-value gate 那样被 Jacobian orientation 沿路径旋转后互相抵消。

更进一步，这个 near-affine packet 还能给出真正的 image coverage。如果 source ball `B_H(z0,r)` 完整落在 cell 中，则

`B_H(T(z0),(m-eps)r) subset T(B_H(z0,r))`。

所以若下游要求物理 target radius `rho`，trusted gate 可以直接写成 division-free 的

`rho + eps*r <= m*r`。

严格 `<` 就是 image reserve。证明只需把 `T` 写成 `A + Lipschitz remainder` 后做 Banach contraction；一维线性例子同时证明这个 image radius 也是 sharp 的。

另外需要特别区分 T-P5-082 的 tangent pullback metric 与 finite displacement 的真实 secant metric。若 reference 是 `z*`，则

`T(z)-T(z*) = S_*(z)(z-z*)`

其中 `S_*` 是沿 segment 的平均 Jacobian，因此真实物理能量是

`V_phys=(z-z*)^T S_*^T H S_*(z-z*)`，

不是一般意义下的 `DT(z)^T H DT(z)`。一维 `T(z)=z+a z^2` 时，前者因子是 `(1+a z)^2`，tangent metric 因子是 `(1+2a z)^2`，除非 affine/中心点，否则并不相等。

若 chart 已有全局 secant bounds

`mu ||z-z*|| <= ||T(z)-T(z*)|| <= L ||z-z*||`

并且 physical finite-step theorem 给出

`V_phys(z_plus) <= q V_phys(z)`，

那么固定 normalized `z`-quadratic barrier 的严格 contraction gate 正好是

`q L^2 < mu^2`。

这同样是无根式、无除法的 trusted condition。若直接使用真实 physical/secant energy，则不需要支付这层 chart distortion；只有坚持固定 `z` metric 时才需要付 `L/mu`。

建议下游路由：T-P5-082 管 nonlinear differential/curvature，T-P5-083 管 step segment，T-P5-084 单独管 global inverse/secant geometry。不能把“每点 Jacobian 可逆”当作第三步的替代品。

当前仍严格是 **pending mathematical child**。没有绑定 deployed nonlinear chart、具体 `H/A/m/eps/L/r/rho`、Float64/controller/FD、P8 coverage、Lean/kernel、provenance、admission、registry 或 P5/M4 closure。