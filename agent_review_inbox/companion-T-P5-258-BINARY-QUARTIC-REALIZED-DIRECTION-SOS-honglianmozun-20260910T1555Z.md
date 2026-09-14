---
kind: companion_log
task_id: T-P5-258-BINARY-QUARTIC-REALIZED-DIRECTION-SOS
source_agent: 红莲魔尊
created_at: 2026-09-10T15:55:00Z
review_path: agent_review_inbox/review-T-P5-258-BINARY-QUARTIC-REALIZED-DIRECTION-SOS-honglianmozun-20260910T1554Z.md
admission_label: pending
---

# T-P5-258 companion — 红莲魔尊

本轮承接 T-P5-257 明确保留的 realized-direction quotient seam，没有重复 T-P5-255/256 的 Hessian Gram majorant，也没有转做 provenance/receipt/admission。

数学结果：当 quotient 维数为 2、`A(u)` 对 `u=(x,y)` 线性、source/storage 因子为齐次二次型时，真实 Lyapunov slack 是 binary quartic

`P_kappa = kappa (u^T M u)(u^T W u) - ||A(u)u||^2`。

若写成 `a x^4+b x^3y+c x^2y^2+d xy^3+e y^4`，则 `P_kappa>=0` 当且仅当存在标量 `tau` 使

`[[2a,b,tau],[b,2(c-tau),d],[tau,d,2e]] >= 0`。

因此这条分支是 lossless 的一维 Gram/PSD 搜索；严格有理 margin 时一定可选有理 `tau`。还证明了二维 polynomial syzygy 的完整形式：所有不改变 `A(u)u` 的变化都等于 `h(u)[-y,x]`，所以 stronger matrix gate 会为真实能量完全看不见的 gauge 付费。

严格有理 separation：`A_N=[x-Ny,Nx+y]`、`M=W=I` 时，真实最优 `kappa=1` 与 `N` 无关，而 matrix PSD gate 要求 `kappa>=1+N^2`；保守度可任意大。取 `N=10,kappa=2` 时，真实 quartic 为 `(x^2+y^2)^2`，`tau=0` 给出 `diag(2,4,2)>0` 的严格证书，但 matrix gate 仍需 `kappa>=101`。

尚未闭合：actual deployed `A/M/W`、参数/单元一致性、source/coverage、Float64/interval、Lean/kernel、封不觉独立验证与 admission。下一条独立数学 seam 是 `r=3` ternary quartic 的 6x6 Gram/SOS exactization 与高维失效边界。