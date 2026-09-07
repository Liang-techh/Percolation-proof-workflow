---
kind: review_result
review_id: review-T-P4-014-juyangxianzun-20260907T0348
task_id: T-P4-014
source_agent: 巨阳仙尊
upstream_review: review-T-P4-014-kuangmanmozun-20260907T0247
claimed_at: 2026-09-07T03:32:00-06:00
created_at: 2026-09-07T03:48:00-06:00
inspected_commit: 6f350c03ddd8a635bb14ea89461ae4e2dd9013a1
integration_status: compiled_candidate
admission_label: pending
requested_action: 梁智炜（Codex）收割 theorem/sidecar；封不觉仅作后续独立验证
---

# T-P4-014 — Lean formalization of the relative-plus-transverse Schur reserve

## Scope

This review formalizes the source-independent inequality result from 狂蛮魔尊's `review-T-P4-014-kuangmanmozun-20260907T0247.md`. It does **not** bind deployed Float64 execution remainders to physical coordinates, does not prove IEEE/source error bounds, and does not mutate P4/M4/registry status.

Claim: `agent_review_inbox/claim-T-P4-014-juyangxianzun-20260907T0332.md`.

Portable sidecar:

- `examples/routeb_p4_transverse_schur_lean/P4TransverseSchur.lean`
- `examples/routeb_p4_transverse_schur_lean/README.md`
- `examples/routeb_p4_transverse_schur_lean/verify.sh`
- `examples/routeb_p4_transverse_schur_lean/lean-toolchain`

The sidecar is pinned to Lean `4.32.0`, reuses the pinned `examples/local_fkg/lake-manifest.json`, resolves `lake` from `PATH`, compiles with `-DwarningAsError=true`, and is marked `CI_PORTABLE=1` for `.github/workflows/lean-agent-sidecars.yml`.

## Minimal theorem decomposition

The sidecar contains ten theorem/corollary declarations.

### 1. Residual envelope composition

`combined_residual_abs` proves, from

- `0 <= c`,
- `|e| <= beta |y|`,
- `|b| <= gamma |z|`,

that

`|c y + e + b| <= (c+beta)|y| + gamma|z|`.

No unnecessary sign hypotheses on `beta` or `gamma` are required at this lowest layer; their effective signs are already encoded by the supplied envelopes.

### 2. Division-free transverse Schur budget

`transverse_square_budget` proves that if

- `p > 0`,
- `Delta := p*d-a^2 > 0`,
- `d*gamma^2 <= Delta*h`,

then for all real `Y,Z`,

`0 <= p*d*Y^2 + p*h*Z^2 - (a*Y+gamma*Z)^2`.

The proof uses the exact polynomial identity

`Delta * [p*d*Y^2 + p*h*Z^2 - (aY+gammaZ)^2]`

`= (Delta*Y-a*gamma*Z)^2 + p*(Delta*h-d*gamma^2)*Z^2`.

Thus the Lean statement does not divide by `p`, `d`, `Delta`, or use square roots.

### 3. Residual square budget

`residual_square_budget` consumes

`|r| <= a|y| + gamma|z|`

plus the previous Schur reserve and proves

`r^2 <= p*(d*y^2+h*z^2)`.

### 4. Main P4 quadratic consumer

`relative_plus_transverse_schur` proves the final source-independent implication:

if

`|e| <= beta|y|`, `|b| <= gamma|z|`,

`p > 0`, `c,beta,gamma >= 0`,

`p*d-(c+beta)^2 > 0`,

and

`d*gamma^2 <= [p*d-(c+beta)^2]*h`,

then

`0 <= p*x^2 + 2*x*(c*y+e+b) + d*y^2 + h*z^2`.

### 5. Additive-bias specialization

`additive_bias_with_slack` instantiates the transverse coordinate with `z=1`. Therefore a uniform bias bound `|b| <= B` is absorbable only after providing an explicit positive scalar slack `sigma` satisfying

`d*B^2 <= [p*d-(c+beta)^2]*sigma`.

This keeps additive execution bias mathematically separate from same-coordinate relative residuals.

### 6. Sharpness / failed-budget witness

`transverse_reserve_failure_witness` formalizes a division-free counterexample to any attempt to weaken the transverse reserve condition. If

`[p*d-a^2]*h < d*gamma^2`

with `p>0` and `p*d-a^2>0`, choose the homogeneous witness

`z = p*(p*d-a^2)`,

`y = a*gamma*p`,

`x = -gamma*p*d`.

The resulting quadratic is exactly

`p^2*(p*d-a^2)*([(p*d-a^2)*h]-d*gamma^2) < 0`.

Hence, at this information level, the transverse budget is sharp. This witness avoids all divisions and is directly kernel-checkable by `ring` plus sign arithmetic.

### 7–10. Exact block-4 rational corollaries

The sidecar freezes

`p4 = 3/5`,

`d4 = 116667666666667/1000000000000000`,

and proves exactly

`p4*d4 - (1/100 + 6/25)^2 = 37503000000001/5000000000000000 > 0`.

It then proves the fully division-free integer budget

`583338333333335*gamma^2 <= 37503000000001*h`

implies the required Schur reserve, and finally obtains the concrete block-4 consumer with corrected normalized `kc=1/100` and the remaining relative reserve `beta=6/25`.

## Real CI loop

### First run — real compile failure

GitHub Actions run `34106950155`, job `101694129259`, reached this sidecar under Lean 4.32.0 and failed with the actual compiler errors

`Unknown identifier abs_add`

at the two triangle-inequality calls in `combined_residual_abs`. Because Lean elaborated through the failed declarations, the corresponding `#print axioms` output also correctly exposed transitive `sorryAx` in the affected consumers.

I did not disable warning/axiom checking. The sidecar was repaired against the pinned Mathlib API by replacing `abs_add` with `abs_add_le`; at the same time the low-level statement was tightened by removing two unnecessary sign hypotheses from `combined_residual_abs`.

The fix is commit `09bd3af33f8e574ecf517bc30feaa8d84379f70e`.

A direct follow-up run (`34107366541`) was cancelled by GitHub concurrency after another formalization push before reaching this sidecar, so it is not used as compile evidence.

### Confirming run — focused PASS

A later shared sidecar run containing the fixed commit, Actions run **`34107571992`**, job **`101696400270`**, compiled the sidecar on Lean 4.32.0 and printed:

`AXIOM_AUDIT=PASS`

`P4_TRANSVERSE_SCHUR_FOCUSED_CHECK=PASS`

`SIDECAR_RESULT=PASS path=examples/routeb_p4_transverse_schur_lean/verify.sh`

All ten printed declarations depend only on

`[propext, Classical.choice, Quot.sound]`

and none contains `sorryAx`.

The overall shared workflow remains red for independent existing artifacts, not for this sidecar: the FLT quotient sidecar still has its `../local_fkg` path failure, and `routeb_p5_weighted_dual_residual_lean` still has the known unused-`hκ1` / invalid-disjunction-projection / `sorryAx` failures. Those are outside this claim and were not modified.

## Interfaces deliberately left open

The Lean algebra is now closed, but P4 execution/source closure still requires separate typed premises:

1. classify the `T-P4-007` execution ledger terms (`DeltaM`, `DeltaC`, centered `DeltaG`, `delta_ctrl`, `solveDefect`) into same-coordinate relative pieces, transverse-coordinate pieces, and genuinely additive bias pieces;
2. prove source/IEEE bounds for those pieces on the same covered domain;
3. identify an actual positive certificate term `h*z^2` (or scalar `sigma`) available to pay the transverse/additive reserve budget;
4. compose with, but do not merge into, the independent `T-P4-012` remote mass-metric consumer;
5. retain the P8/source-domain coverage obligation required by all physical bounds.

The zero-slice obstruction from `T-P4-007` remains relevant: a remainder that can be nonzero when the historical cross coordinate is zero cannot be silently charged to the same-coordinate `|r| <= k|y|` envelope. `T-P4-014` gives a correct consumer only after an explicit transverse or scalar positive reserve has been supplied.

## Status

`compiled_candidate`, `admission_label: pending`.

No final integration, P4/M4 closure, source authentication, or registry mutation is claimed here.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
