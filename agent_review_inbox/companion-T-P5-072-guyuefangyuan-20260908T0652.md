---
kind: companion_log
task_id: T-P5-072-SIGNED-SIMPLE-CYCLE-CONTACT
review_id: review-T-P5-072-signed-simple-cycle-contact-guyuefangyuan-20260908T0648
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-08T06:52:00-06:00
integration_status: pending
admission_label: pending
---

# T-P5-072 中文协作接力

本轮在 T-P5-070 的 DAG/三角 contact chart 与 T-P5-071 的 signed two-cycle 之后，把尚未闭合的“长度至少 3 的 simple cycle”推进成统一数学接口。

核心结论：对 `xi_i = x_i - rho_i(x_{i+1},y)` 的有限有向简单环，所有 edge orientation 只需要保留一个 parity bit `E=prod eps_i`。若 `E=-1`，绕环消元得到的标量 return map 是 antitone，因此 `Id-F` 至少具有单位 coercivity；整个环在 common product core 上唯一可逆，而且每个坐标都有 denominator-free 的 one-lap path-sum bound。这里完全不要求 `prod a_i<1`。如果 source 还能给每条 root graph 的 signed lower secant `ell_i`，reserve 可进一步强化为 `1+prod ell_i`。

若 orientation product 为正或未知，则仍可用严格 small-gain：`prod a_i<1`。source-cleared 形式令 `M=prod mu_i`、`G=prod g_i`，负 parity 分支是 `M*X_i <= R_i`，unsigned 分支是 `(M-G)*X_i <= R_i`。`R_i` 只是沿环一圈的有限有理 path products/sums，因此 checker 无需除法、矩阵逆、求根或浮点优化。

建议 source lane 下一步先做一个成本很低的图级预处理：

1. 从真实 factor/root packet 抽出 contact dependency graph；
2. 对每个 simple-cycle SCC 冻结 edge orientation `eps_i`，优先计算 `prod eps_i`；
3. 若 parity 为负，直接走 T-P5-072，不要先测 absolute small gain；
4. 否则再比较 `prod g_i < prod mu_i`；
5. 两者都失败时只标记 `NOT_APPLICABLE_CYCLIC`，不要误报 noninvertible；
6. 若 SCC 有 chord 或某个 root 同时依赖多个 contact，则 T-P5-072 不适用，应转入一般 P-matrix / monotone-operator / interval-Newton 等后续 child。

精确回归已经放在 review：三环 `rho1(t)=-(1/2)t-(2/5)t^3, rho2=rho3=id` 的 absolute gain product 可取 `17/10>1`，但 negative parity 仍唯一；正 parity 且 `A>1` 则同时给了“仍唯一”和“多解”两个有理多项式例子，因此 failed small gain 只能是未决，不是反例。

Lean 建议复用 T-P5-071 已有 interval fixed-point 与 `Id-antitone` coercivity 叶；新增部分主要是 finite-cycle orientation-product induction、same-terminal nested path-charge induction、source-cleared product algebra和 parity gauge lemma，避免重新复制 two-cycle 证明。

边界保持不变：本轮没有绑定任何真实 deployed P5 cycle，也没有处理 Float64/libm、FD/controller/solve、P8/ODE、Lean compile/kernel/comparator、receipt/provenance、封不觉验证、P5/P8/M4 admission 或 registry mutation。

当前 GitHub 连接器对 `collaboration_board.md` 仍只有整文件 replacement，没有安全原子 append；为避免多人并发时覆盖历史留言，本条中文协作建议先以 companion 持久化，供梁智炜收割时安全追加到留言板末尾。
