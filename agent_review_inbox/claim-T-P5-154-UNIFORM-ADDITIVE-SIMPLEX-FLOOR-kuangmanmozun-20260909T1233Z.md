---
type: review_claim
review_id: RVW-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-KMMZ-20260909T1233Z
task_id: T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: '2026-09-09T12:33:00Z'
lease_expires_at: '2026-09-09T13:33:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-153-homothetic-simplex-slack-coupling-guyuefangyuan-20260909T1223Z]'
status: completed
result_path: agent_review_inbox/review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z.md
result_commit: c9b94c1f931c76c20a0f22e428425a4d659b57bb
companion_path: agent_review_inbox/companion_T-P5-154_UNIFORM_ADDITIVE_SIMPLEX_FLOOR_KMMZ_20260909T1238Z.md
companion_commit: a8eb33c86ffb1dd6987c8fe853c45bab54bea660
---
# Review Claim — uniform additive simplex floor

Completed. T-P5-153's positive uniform additive-repair problem over a homothetic uncertainty simplex is exactly a copositivity problem. For a candidate `D`, define the symmetric matrix `M_D` by

`M_D[i,i]=D g_i`,

`2 M_D[i,j]=K_ij+D(g_i+g_j)`.

Then every simplex weight satisfies

`lambda^T M_D lambda = Delta_lambda+D g_lambda`.

Hence a uniform floor is valid exactly when `M_D` is copositive on the nonnegative orthant, under the same boundary-attainability convention used for necessity upstream. Pairwise edge repair is not sufficient once `N>=3`: with `g_i=1`, all `K_ij=-4`, and `D=1`, every edge has `(2t-1)^2>=0` while the simplex barycenter gives `-1/3`.

For the complete symmetric family `g_i=g`, `K_ij=-kappa`, the sharp floor is `D_*=kappa(N-1)/(2gN)`, whereas each edge only demands `kappa/(4g)`. Exact rational PSD of `M_D` is a sound root-free fast path, and a rational nonnegative vector with negative quadratic value is a decisive obstruction; PSD failure alone remains `NOT_CERTIFIED`, not mathematical failure.

Actual source/common-shape binding, same uncertainty weights, coverage, Float64, Lean/kernel, independent validation, admission and registry remain pending.