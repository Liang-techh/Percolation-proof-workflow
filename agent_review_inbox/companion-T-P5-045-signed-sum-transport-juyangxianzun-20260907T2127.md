---
kind: companion_log
task_id: T-P5-045
agent: 巨阳仙尊
source_agent: 巨阳仙尊
source_review: review-T-P5-045-liuguanyi-20260907T2108
companion_to: examples/routeb_p5_robust_correlated_interval_lean/
main_formalization_owner: 苏梦辰
head_commit: 0014da7cac3d52098b7db00703bd87b3e91c604e
status: compiled_candidate
integration_status: pending
admission_label: pending
---

# T-P5-045 signed-sum interval transport companion — 巨阳仙尊

## Coordination / ownership

本轮读取柳冠一 `review-T-P5-045-liuguanyi-20260907T2108.md` 后，最初开始拆分 robust signed-symmetric interval theorem。随后从最新 commit 检测到苏梦辰已经并发提交主 formalization：

`examples/routeb_p5_robust_correlated_interval_lean/`

因此本 Agent 立即缩窄 claim，不再重复 determinant / adjugate-bias / quarter gate / parameter gate，只保留主 sidecar 尚未直接表达的最小 source-independent adapter：**先做 signed interval addition，再取 absolute cap**。

## Lean artifact

路径：

`examples/routeb_p5_correlated_interval_gate_lean/`

主文件：

`examples/routeb_p5_correlated_interval_gate_lean/P5CorrelatedIntervalGate.lean`

portable verifier：

`CI_PORTABLE=1 bash examples/routeb_p5_correlated_interval_gate_lean/verify.sh`

固定 toolchain：`leanprover/lean4:v4.32.0`；本次 GitHub-hosted runner 实际记录 `Lean 4.32.0` / `Lake 5.0.0-src+8c9756b`。

## Minimal theorem statements

1. `signed_sum_interval_transport`

从

- `k45L ≤ k45 ≤ k45U`,
- `k54L ≤ k54 ≤ k54U`,
- `-Q ≤ k45L + k54L`,
- `k45U + k54U ≤ Q`

推出

`-Q ≤ k45 + k54 ∧ k45 + k54 ≤ Q`。

2. `signed_sum_abs_transport`

在相同 hypotheses 下推出 checker-facing seam

`|k45 + k54| ≤ Q`。

3. `skew_family_signed_sum_zero`

`M + (-M) = 0`。

4. `skew_family_signed_sum_abs_zero`

`|M + (-M)| = 0`。

这四条 theorem 明确冻结了 T-P5-045 的接口边界：不能先对 `k45,k54` 分别取绝对值再相加，否则会丢失 pure-skew cancellation。

## Real GitHub Actions evidence

最终 companion head：

`0014da7cac3d52098b7db00703bd87b3e91c604e`

GitHub Actions：

- workflow: `Lean agent sidecars`
- run: `34183168831`
- job: `101926237376`
- runner: Ubuntu 24.04
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

本 sidecar 的真实日志：

```text
PLACEHOLDER_SCAN=PASS
'RouteBP5SignedSumIntervalTransport.signed_sum_interval_transport' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP5SignedSumIntervalTransport.signed_sum_abs_transport' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP5SignedSumIntervalTransport.skew_family_signed_sum_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP5SignedSumIntervalTransport.skew_family_signed_sum_abs_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
AXIOM_AUDIT=PASS
P5_SIGNED_SUM_INTERVAL_TRANSPORT_FOCUSED_CHECK=PASS
SIGNED_INTERVAL_ADDITION_BEFORE_ABS=true
SKEW_COORDINATE_CHARGED=false
MAIN_T_P5_045_FORMALIZATION_OWNER=苏梦辰
SIDECAR_RESULT=PASS path=examples/routeb_p5_correlated_interval_gate_lean/verify.sh
```

因此四个公开 theorem 均无 `sorryAx`，axiom set 均为 `[propext, Classical.choice, Quot.sound]`。

## Shared-workflow status / concrete blocker observed

shared workflow 整体 `failure` **不是本 companion lane 导致**。同一真实日志中存在多个历史独立 lane failure；与 T-P5-045 直接相关的是苏梦辰主 sidecar：

`examples/routeb_p5_robust_correlated_interval_lean/P5RobustCorrelatedInterval.lean:84:5`

在 `-DwarningAsError=true` 下报：

```text
Variable name `hbeta5` is not explicitly referenced.
```

其公开 theorem 的 `#print axioms` 在该 run 中仍未出现 `sorryAx`，但 portable verifier 因 warning-as-error 返回 exit 1。因此主 T-P5-045 formalization 仍需要苏梦辰做最小 linter repair（删除冗余 hypothesis，或若确为隐式接口需要则改为 `_` 命名并保持 statement 语义），然后重新跑真实 GitHub Actions。巨阳仙尊未修改苏梦辰已认领的主 sidecar，以避免并发抢占。

其他 shared failures（FLT path、M4 cross-branch、P5 componentwise/direct-two-channel/parameter-tube/weighted-dual、P7 tail Schur、P8 ramp reconstruction）属于已有独立 lane，本轮不越权处理。

## Remaining boundaries

本 companion 只关闭 signed-entry-interval → `sigma=k45+k54` → `|sigma|≤Q` 的代数 adapter。以下仍 open：

- actual source exporter 对 `k45/k54` signed intervals 的正确性；
- 苏梦辰主 robust determinant/bias/gate sidecar 的 warning-as-error repair 与最终 CI PASS；
- actual `b/g` enclosures；
- Float64/libm/FD/controller/solve semantics；
- same-P8-domain trajectory/coverage；
- P5/P8/M4 final closure；
- provenance/admission/registry/final integration。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
