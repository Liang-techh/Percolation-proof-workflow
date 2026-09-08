---
kind: companion_log
task_id: T-P5-055
review_id: review-T-P5-055-guyuefangyuan-20260908T0031
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-08T00:34:00-06:00
integration_status: pending
admission_label: pending
---

# 古月方源协作摘要 — T-P5-055

- 本轮补上 `T-P5-052/053` 明确留下的 eventual Bernstein completeness：若 exact polynomial `P` 在整个 `[0,1]^d` 上有严格余量 `P>=delta>0`，定义 `C_P=sum_{beta!=0}|c_beta|(2^|beta|-1)`，那么任意满足 `2^N*delta>C_P` 的 dyadic 深度 `N` 都保证**所有 child 的所有 tensor Bernstein controls 严格为正**。checker 只需 exact doubling，不需要 log、求根或优化。
- 更精确的统一控制误差是 `E_P(h)=sum |c_beta|((1+h)^|beta|-1)`，并有 `|control-P(child_corner)|<=E_P(h)<=h*C_P`。因此即使只有 `P>=0`，深度 `N` 的任何负 control 也至少被压到 `>=-2^-N C_P`；这给出了定量 near-pass，但不能当 exact PASS。
- 关键 sharp obstruction：`Z(t)=(t-1/3)^2>=0`。在每一个 dyadic 深度，包含 `1/3` 的唯一 cell 的 quadratic middle control 都精确等于 `-2/(9*4^N)<0`；即使升阶到 cubic，也始终有一个 interior control 精确等于 `-1/(9*4^N)<0`。因此“非负但接触 0”不能保证 dyadic all-controls checker 终止，negative noncorner control 必须继续保持 `SUBDIVIDE/UNDECIDED`，不能被当成反例。
- 同一个 obstruction 若在有理零点 `1/3` 处分裂，左右 child 的 controls 分别为 `(1/9,0,0)` 与 `(0,0,4/9)`，立即 exact PASS。这说明 real P5 cell 若在 rank-deficient / `Rdet=0` 边界长期卡住，应切换到 rational-root split、factorization/SOS 或专门 zero-contact certificate，而不是无限加深 dyadic 或提前绝对值化。
- 对当前 P5 branch-free lane：若 `Rtr>=delta_tr>0`、`Rdet>=delta_det>0`，分别算 `C_tr,C_det`，找共同 `N` 使 `2^N delta_tr>C_tr`、`2^N delta_det>C_det`，就得到整个 parent box 的有限 exact Bernstein realization。若 determinant 只有非负无严格 margin，则本轮反例说明必须保留 boundary-aware lane。
- Lean 建议先只做现有 1D sidecar 上的极小 theorem：quadratic/cubic child-control lower bound、uniform-margin finite depth、`(t-1/3)^2` 的 dyadic negative-control regression；等 `T-P5-053` tensor package 真正编译后再推广 finite-sum tensor theorem。
- 与 `T-P5-054` 的关系：柳冠一刚证明 near-singular source perturbation 必须保留 correlated determinant correction；本轮进一步证明 near-singular exact nonnegativity也不能指望 dyadic positive controls 自动终止。这两条应一起作为 singular-boundary fail-closed 纪律。
- 尚未闭合：真实 source polynomial/enclosure、真实 `delta_tr/delta_det`、Float64/FD/controller/solve、same-key domain、P8/ODE、tensor Lean、独立验证与 admission。当前仍为 pending mathematical child。
