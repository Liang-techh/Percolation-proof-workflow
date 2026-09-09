---
kind: companion_log
task_id: T-P5-115-ROOT-FREE-SECOND-JET-INDEPENDENT-ENERGY
review_id: review-T-P5-115-ROOT-FREE-SECOND-JET-INDEPENDENT-ENERGY-kuangmanmozun-20260909T0143Z
source_agent: 狂蛮魔尊
created_at: 2026-09-09T01:46:00Z
status: handoff
---

## 中文协作接力

- 当前完成：接 T-P5-114 的“独立三项 energy fallback”。如果只能拿到同一 PSD metric 下 `Q(r)<=U_r`、`Q(m)<=U_m`、`Q(c)<=U_c`，不必直接付 `3(U_r+U_m+U_c)`。先给 `g=m+c` 一个辅助有理 cap `K`，检查 `K-U_m-U_c>=0` 与 `(K-U_m-U_c)^2>=4U_mU_c`；再给 `J2=r-g` 的最终 cap `H2` 检查 `H2-U_r-K>=0` 与 `(H2-U_r-K)^2>=4U_rK`，即可严格推出 `Q(J2)<=H2`。全程只有加乘平方和序比较，无平方根、除法、固定 Young 参数。
- sharp 边界：只保留三项独立 energy 时，真实最坏上界就是 `(sqrt(U_r)+sqrt(U_m)+sqrt(U_c))^2`；一维取 `r=sqrt(U_r), m=-sqrt(U_m), c=-sqrt(U_c)` 精确取等。上述两层 discriminant gate 在允许实辅助 `K` 时正好达到该最优值；限制 `K` 为有理数时，任何严格高于最优值的有理 `H2` 都可用有理 `K` 认证。因此再想降常数必须增加 signed Gram / orthogonality / range 等新信息，不能只换 Young 参数。
- 与 T-P5-114 的关系：T-P5-114 的系数 3 在“先把三项压成一个总和”这个信息模型下仍然 sharp；本轮只是保留 `U_r,U_m,U_c` 的分布信息，所以不矛盾。例：`U_r=100,U_m=U_c=1` 时旧 fallback 是 `306`，新 gate 取 `K=4,H2=144`，且一维 `r=10,m=c=-1` 精确饱和 144。
- rational regression：`U_r=1,U_m=2,U_c=3` 时取 `K=10,H2=87/5`，两层平方 gate 都精确通过，因此可证 `Q(J2)<=17.4`；旧 factor-3 只能给 18，而真实最优约 17.1915。说明非平方有理 cap 也不需要在 checker 里算根号。
- homogeneous cell 版本：若 `Q(r)<=u_r Z2`、`Q(m)<=u_m Z2`、`Q(c)<=u_c Z2`，可直接在系数层检查 `k-u_m-u_c>=0`、其平方 `>=4u_mu_c`，以及 `h-u_r-k>=0`、其平方 `>=4u_rk`，得到 `Q(J2)<=h Z2`。若 `Z2=Q_Z(delta)^2` 且 `Q_Z(delta)<=S`，则直接接成 `H2=hS^2` 给 T-P5-112/T-P5-113。
- 必须 fail-closed 的坑：平方判据必须同时带非负 branch guard。比如 `U_m=U_c=1,K=0` 时 `(K-U_m-U_c)^2=4` 会假装通过，但 `m=c=1` 实际 `Q(m+c)=4>K`。同理外层 `H2-U_r-K>=0` 不能删。
- 给 source/CSE Agent 的建议：优先仍是 direct signed `J2` / signed Gram；只有没有 correlation 时才用本轮 gate。即便如此，也请保留三项独立 cap，不要过早压成 `U_r+U_m+U_c`，否则会永久丢掉本轮能收回的 slack。
- 给 Lean Agent 的建议：最小叶为 `quadratic_two_term_discriminant`、`second_jet_independent_energy_nested`、`second_jet_independent_energy_homogeneous`；可选再做带三个正有理权重的 `quadratic_three_term_weighted_mul` 作为独立证明/回归。不要把 generic compile 升级成真实 P5 source closure。
- 关联任务：T-P5-112、T-P5-113、T-P5-114、T-P5-115。当前仍是 `CONDITIONAL_PASS / pending`，未升级 source、coverage、Lean/kernel、admission、registry 或 P5/M4。

注：共享 `collaboration_board.md` 当前写接口是整文件 replacement，且并行 agent 正在写仓库；为避免覆盖别人留言，本轮不冒险重写该文件。以上中文内容作为新的 `companion_log` 留给协调者安全收割。
