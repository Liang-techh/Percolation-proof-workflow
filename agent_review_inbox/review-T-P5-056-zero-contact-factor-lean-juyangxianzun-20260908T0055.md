---
kind: review_result
task_id: T-P5-056
agent: 巨阳仙尊
source_agent: 巨阳仙尊
reviewed_math_source: 狂蛮魔尊
status: compiled_candidate
integration_status: pending
admission_label: compiled_candidate
lean_sidecar: examples/routeb_p5_zero_contact_factor_lean/
lean_commit: 89eba88407d62e2a8eec7f14b05af70f78385d3e
actions_run: 34196284729
actions_job: 101964692039
---

# T-P5-056 review — exact zero-contact factor Lean trusted core

本轮读取了 `README.md`、`task_queue.md`、`collaboration_board.md`，并消费狂蛮魔尊刚提交的 `T-P5-056` 数学 review / companion（主 review commit `f12ed16cd6539dccf31258fe925a730b806ad86b`，companion commit `371eab9864a8edc8133496508417d6299b135d46`）。未发现苏梦辰或臭屁猪认领该数学结果的 Lean 分解，因此由巨阳仙尊完成 source-independent trusted-core 形式化；未重复 `T-P5-055` 的 Bernstein completeness，也未触碰 provenance / admission / registry。

## Lean sidecar

路径：`examples/routeb_p5_zero_contact_factor_lean/`

- `P5ZeroContactFactor.lean`
- `README.md`
- `verify.sh`
- `lean-toolchain`

sidecar 使用仓库 `examples/local_fkg/lake-manifest.json` 与同版本 `leanprover/lean4:v4.32.0`；`verify.sh` 仅从 `PATH` 查找 `lake` / `lean`，无本机专属路径，并带 `CI_PORTABLE=1`。

本轮落成 16 个公开 theorem：

1. `quadratic_repeated_root_factor_identity`
2. `quadratic_repeated_root_nonneg`
3. `quadratic_repeated_root_contact`
4. `affine_nonneg_of_endpoint_values`
5. `cubic_repeated_root_factor_identity`
6. `cubic_repeated_root_contact`
7. `cubic_repeated_root_nonneg_on_unit`
8. `left_endpoint_factor_identity`
9. `left_endpoint_factor_nonneg`
10. `right_endpoint_factor_identity`
11. `right_endpoint_factor_nonneg`
12. `one_third_square_regression`
13. `one_third_square_nonneg_regression`
14. `simple_root_negative_regression`
15. `endpoint_simple_root_regression`
16. `zero_contact_packets_feed_two_remainder_consumer`

### 最小 kernel-facing statements

二次式 `P(t)=a t^2+b t+c` 不信任任何 root finder；外部只交一个 witness `r`，Lean 核验 division-free 等式

- `b + 2*a*r = 0`
- `c - a*r^2 = 0`

即可推出精确 factor identity `P(t)=a*(t-r)^2`。若再有 `0≤a`，则得到全实轴 `P(t)≥0`；因此此 theorem 不人为添加冗余的 `r∈[0,1]` 或 `t∈[0,1]` 假设。

三次式 `P(t)=a t^3+b t^2+c t+d` 核验

- `c + 3*a*r^2 + 2*b*r = 0`
- `d - 2*a*r^3 - b*r^2 = 0`

得到精确

`P(t)=(t-r)^2*(a*t + (b+2*a*r))`。

在 `0≤t≤1` 上，只需再检查剩余 affine factor 两端

- `0 ≤ b+2*a*r`
- `0 ≤ a+b+2*a*r`

即可由 Lean 推出整个 cell 非负。

endpoint zero 被单独 typed：`d=0` 时使用 `P(t)=t*Q(t)`，`a+b+c+d=0` 时使用 `P(t)=(1-t)*Q(t)`，因此不会把合法的 simple endpoint root 错误强迫成 even multiplicity。回归还冻结了 `(t-1/3)^2` 的 exact PASS、两个 interior simple roots 的负中点反例，以及 `P(t)=t` 的合法 simple endpoint root。最后一个 theorem 将已核验的 quadratic `Rtr` packet 和 cubic `Rdet` packet送入既有 `0≤Rtr → 0≤Rdet → P` consumer，不重证 P5 branch-free completion。

## 真实 GitHub Actions / focused compile

最终 Lean-triggering head：`89eba88407d62e2a8eec7f14b05af70f78385d3e`

- workflow run: `34196284729`
- job: `101964692039`
- environment: Lean `4.32.0`, Lake `5.0.0`
- `PLACEHOLDER_SCAN=PASS`
- `AXIOM_AUDIT=PASS`
- `P5_ZERO_CONTACT_FACTOR_FOCUSED_CHECK=PASS`
- `SIDECAR_RESULT=PASS path=examples/routeb_p5_zero_contact_factor_lean/verify.sh`

16 个公开 theorem 的 `#print axioms` 均只出现 `[propext, Classical.choice, Quot.sound]`，本 lane 无 `sorryAx`。本 sidecar 在首轮真实 Actions 即通过，因此本轮没有虚构或需要执行 T-P5-056 自身的失败→修复循环。

shared portable workflow 总体仍为 red：本 run 还包含 FLT quotient、M4 cross-branch、P5 componentwise / correlated-matrix / direct-two-channel / parameter-tube / weighted-dual、P7 tail Schur、旧 P8 ramp reconstruction 等已有独立 lane 的失败；这些与 `T-P5-056` focused verifier 无关，本轮未越权修改。

## 仍开放的接口边界

- rational-root / gcd / CAS discovery 仍是不可信前端；trusted core 只检查 witness identity。
- 狂蛮魔尊提出的 certificate-level completeness / dispatcher 完备性 theorem 尚未形式化。
- `T-P5-055` strict-positive Bernstein eventual completeness 不被替代；本 sidecar 只是补 zero-contact 分支。
- deployed `Rtr/Rdet` coefficient/source binding 未做。
- Float64 / FD / controller / solve semantics 未做。
- P8 same-domain ODE / flowpipe coverage 未做。
- non-strict zero-contact PASS 不等价于 positive reserve、strict decay 或 rounding robustness。
- P5/P8/M4 final closure 与 registry/admission mutation 均未做。

当前严格状态：`compiled_candidate`。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
