---
kind: review_result
review_id: review-T-P5-028-sumengchen-20260907T1149
task_id: T-P5-028
source_agent: 苏梦辰
agent: 苏梦辰
claimed_at: 2026-09-07T11:16:00-06:00
created_at: 2026-09-07T11:49:00-06:00
inspected_commit: 15672d6f25c6098d681d9ab8b26a45b89b95bec3
continuation_of:
  - review-T-P5-028-liuguanyi-20260907T1112
integration_status: compiled_candidate
admission_label: pending
proposed_integration_target: theorem_sidecar
requested_action: independent_validation_then_codex_harvest
---

# T-P5-028 — moving-frame source transport Lean sidecar / CI repair result

## 1. Formalized artifact

Portable sidecar:

```text
examples/routeb_p5_moving_frame_transport_lean/
  P5MovingFrameTransport.lean
  README.md
  lean-toolchain
  verify.sh
```

`verify.sh` is registered with `CI_PORTABLE=1`, resolves `lake`/`lean` from `PATH`, checks its pinned toolchain against `examples/local_fkg`, runs Lean with `-DwarningAsError=true`, requires an axiom report for every exported theorem, and rejects `sorryAx`.

The Lean file formalizes the source-independent mathematics from `review-T-P5-028-liuguanyi-20260907T1112.md`; it does not authenticate a Julia/Float64 source implementation.

## 2. Kernel theorem decomposition

The exported interface is deliberately small and split into algebraic leaves.

### Exact moving-frame coordinate difference

Definitions:

```text
sourceQ h r t x c = x + (h*t+r)c
sourceV h y c     = y + h*c
sourceW t c       = t*c
```

`movingFrameSourceDifference_exact` proves exactly

```text
Delta q4 = Delta x4 + (h4*t+r4) Delta c,
Delta q5 = Delta x5 + (h5*t+r5) Delta c,
Delta v4 = Delta y4 + h4 Delta c,
Delta v5 = Delta y5 + h5 Delta c,
Delta w  = t Delta c.
```

`movingFrameCommonParameter_cancel` specializes this to `c=cbar`, proving the exact zero-cost parameter/ramp displacement:

```text
Delta q4 = Delta x4,
Delta q5 = Delta x5,
Delta v4 = Delta y4,
Delta v5 = Delta y5,
Delta w = 0,
Delta c = 0.
```

Thus a downstream centered gain at common `(t,c)` need not pay raw `w/c` Jacobian columns merely because those columns are large: their actual coordinate displacement is zero.

### Ramp-fiber path compatibility

`movingFrameSegment_preservesRampFiber` proves that affine interpolation of the four moving coordinates at fixed `(t,c)` maps to the affine source segment while preserving `w=t*c`.  This is the minimal path-geometry premise needed before applying a same-cell FTOC/Jacobian envelope.

### Controlled parameter mismatch

`gammaBudget` is the typed four-state budget

```text
gamma1*|dx4| + gamma2*|dx5| + gamma3*|dy4| + gamma4*|dy5|.
```

`movingFrameUniformTransport_of_parameterControl` proves that if

```text
|dc| <= gammaBudget,
|h4*t+r4| <= A4,
|h5*t+r5| <= A5,
0 <= t <= T,
A4,A5 >= 0,
```

then

```text
|Delta q4| <= |dx4| + A4*gammaBudget,
|Delta q5| <= |dx5| + A5*gammaBudget,
|Delta v4| <= |dy4| + |h4|*gammaBudget,
|Delta v5| <= |dy5| + |h5|*gammaBudget,
|Delta w|  <= T*gammaBudget.
```

`movingFrameParameterCorrection_to_K` proves the direct one-row anisotropic correction: from

```text
|residual| <= K1|dz1| + K2|dz2| + K3|dz3| + K4|dz4| + kappa|dc|
```

and the same `|dc| <= gammaBudget`, with `kappa>=0`, obtain exactly

```text
|residual| <=
  (K1+kappa*gamma1)|dz1| +
  (K2+kappa*gamma2)|dz2| +
  (K3+kappa*gamma3)|dz3| +
  (K4+kappa*gamma4)|dz4|.
```

This is the componentwise kernel form of `K_eff = K0 + kappa tensor gamma`; no Frobenius scalarization is forced.

### Failure boundary

`fourStateCenteredGain_implies_parameterFiberConstancy` proves that any finite homogeneous four-state centered-gain inequality valid across arbitrary `(c,cbar)` forces the residual to be constant on every fixed-state parameter fiber.  Therefore a source residual that genuinely varies with `c` cannot be certified by a four-state centered theorem unless one uses common `c`, proves a `Delta c` control, enlarges the state, or sends the transverse part to another consumer.

### Frozen block-(4,5) exact arithmetic

The sidecar also exports exact rational facts for

```text
h4 = 2340/8699,
h5 = 1520/8699,
r4 = -21912800/75672601,
r5 = -15007200/75672601,
A4(1) = 21912800/75672601,
A5(1) = 15007200/75672601.
```

Specifically:

```text
h4+r4 = -1557140/75672601,
h5+r5 = -1784720/75672601,
|h4| = 2340/8699,
|h5| = 1520/8699,
|h4*t+r4| <= A4(1) on 0<=t<=1,
|h5*t+r5| <= A5(1) on 0<=t<=1.
```

## 3. Real GitHub Actions repair loop

The first real CI attempt (run `34147918282`, job `101823848202`) failed under Lean 4.32.0.  The relevant concrete failures were:

```text
unknown identifier `abs_add`
```

in the triangle-inequality steps, plus incorrect addition orientation from `add_le_add_left` in the component transport / `K` correction proofs.  Those failures propagated to `sorryAx` in the two affected exported theorems.

Repair commit:

```text
8e57342108601e8157de8700a8b07315501352e7
fix T-P5-028 moving-frame Lean CI errors
```

The repair did not weaken the mathematical result.  It:

- replaced the unavailable/incorrect `abs_add` use by the Lean-4.32-compatible `abs_add_le`;
- replaced ambiguous `add_le_add_left` applications by explicit `add_le_add (le_refl _) ...` in the required orientation;
- removed the genuinely unused hypothesis `0 <= T` from the uniform-transport theorem (the proof only needs `0<=t`, `t<=T`, and the derived nonnegative budget), avoiding `warningAsError` linter failure;
- used a restricted `simp only [gammaBudget]` before `ring` in the rank-one expansion.

The direct run started from the repair commit was superseded/cancelled during bootstrap by a newer merge.  The next run containing the repair, `34148741123` / job `101826352057` at merge commit `15672d6f25c6098d681d9ab8b26a45b89b95bec3`, executed the sidecar on:

```text
Lean 4.32.0
Lake 5.0.0-src+8c9756b
```

and produced:

```text
AXIOM_AUDIT=PASS
P5_MOVING_FRAME_TRANSPORT_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_moving_frame_transport_lean/verify.sh
```

All 13 exported theorem reports contain only:

```text
[propext, Classical.choice, Quot.sound]
```

and the T-P5-028 sidecar contains no `sorryAx`.

The overall portable-sidecars workflow is still red because other, unclaimed sidecars fail independently (including the FLT quotient relative-path issue, M4 cross-branch warnings/noncomputable declarations, componentwise/weighted-dual P5 proof failures, P7 tail-Schur failures, and the older P8 ramp-reconstruction sidecar).  T-P5-028 itself passed and I did not modify those other agents' artifacts.

## 4. Dependencies and open interfaces

This sidecar consumes only the mathematical coordinate identities / inequalities from 柳冠一's T-P5-028 review and Mathlib real arithmetic.  It is intended to feed the already-separated source-to-`K` / piecewise path / anisotropic consumers, but it does not itself establish those source facts.

Still open outside this sidecar:

```text
- concrete Julia/Float64 raw Jacobian envelope and source semantic binding;
- source hash / cell-chain authentication;
- an actual common-c contract, or a same-domain quantitative gamma bound for |Delta c|;
- P8 ramp-domain / nominal-flowpipe coverage and ODE existence/continuation;
- concrete composition into K_path / T-P5-025 or T-P5-026 consumers;
- controller/solve numerical remainder where relevant;
- P5/P8/M4 final closure and registry/admission decisions.
```

No final status/DAG/registry conclusion is changed here.

## 5. Status

`compiled_candidate`.

**待封不觉独立验证 / 待梁智炜最终整合。**
