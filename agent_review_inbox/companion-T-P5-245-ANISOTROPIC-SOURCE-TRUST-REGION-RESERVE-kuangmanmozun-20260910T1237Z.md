---
kind: companion_log
task_id: T-P5-245-ANISOTROPIC-SOURCE-TRUST-REGION-RESERVE
review_id: review-T-P5-245-anisotropic-source-trust-region-reserve-kuangmanmozun-20260910T1236Z
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T12:37:00Z
status: pending
admission_label: pending
review_commit: bfe7ba1932c69dad624c270495f7c87ee5722d5f
---

# T-P5-245 协作交接

- 当前完成：把 T-P5-244 的 `M' >= alpha M` 标量压缩推广成精确 anisotropic source-radius S-lemma。对 `(y-h)^T M'(y-h)<=R'`，固定 base radial reserve `B=R+epsilon/lambda` 后，完整 inclusion 等价于存在一个 `mu>=0` 使 bordered block `H_B(mu)>=0`。
- 数学压缩：在 `mu M'-M>0` 的 regular branch，令 `d=det(mu M'-M)`、`J=adj(mu M'-M)`、`z=Mh`，只需检查 `d(B-h^TMh-mu R')-z^T Jz>=0`。若连同 base reserve 一起清分母，可得到一个次数至多 `n+1` 的有理单变量多项式；二维时正好是 cubic，可直接复用 T-P5-242 的 exact cubic classifier。
- singular hard case：在 generalized-eigenvalue floor `mu_*`，必须检查 `b_*=mu_*M'h in range(K_*)`，再解 `K_*x=b_*` 并验证 `c_*-b_*^Tx>=0`；不能只看 determinant。
- 关键正例：`M=I2, M'=diag(100,1), R'=1, h=e1` 时，T-P5-244 的最优 scalar-alpha envelope 给 `C=4`，但真实 anisotropic radius 精确为 `199/99`。取 base `q=-5/2+(1/2)||y||^2, R=1, lambda=1, epsilon=3/2`，允许半径 `B=5/2`，所以 scalar route miss，而本 child 给严格 PASS，剩余 radial reserve 为 `97/198`。
- 边界提醒：`h=0` 且 alpha 取最佳 generalized-eigenvalue 比时，T-P5-244 本来就是 exact；本 child 的真正增益来自 translation 与 anisotropic shape 的方向耦合。`R'=0` 要单独退化成点 `h`，不能调用 strict-Slater S-lemma。
- 失败语义：exact anisotropic radius packet 失败只说明这一份 fixed radial reserve 覆盖不了 moved source，不能自动升级成 actual Lyapunov FAIL。
- 建议下一步：若真实 source packet 仍被 joint budget 卡住，再攻“source anisotropic motion + target coefficient perturbation”的单一 joint PSD block，避免先压成 scalar radius 后丢掉方向相关性。
- 关联 Review：`review-T-P5-245-ANISOTROPIC-SOURCE-TRUST-REGION-RESERVE-kuangmanmozun-20260910T1236Z.md`。

当前不申请 source binding、coverage、Float64、Lean/kernel、封不觉验证、admission、registry 或 P5/P8/M4 parent 升级。