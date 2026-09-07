---
kind: review_result
review_id: review-T-P5-034-sumengchen-20260907T1724
task_id: T-P5-034
agent: 苏梦辰
source_agent: 苏梦辰
claimed_at: 2026-09-07T17:13:00-06:00
created_at: 2026-09-07T17:24:00-06:00
upstream_review: review-T-P5-034-honglianmozun-20260907T1701
inspected_commit: fb21ff7351a5f9fb64e23103f4317488ff9fed52
sidecar_path: examples/routeb_p5_block45_15_16_sos_lean
integration_status: compiled_candidate
admission_label: pending
requested_action: independent_validation_then_coordinator_integration
---

# T-P5-034 — Lean formalization of exact `15/16` block-(4,5) coercivity

## 0. Formalization result

I formalized the source-independent algebra supplied by 红莲魔尊 in
`review-T-P5-034-honglianmozun-20260907T1701` as a new portable Lean sidecar:

```text
examples/routeb_p5_block45_15_16_sos_lean/
```

The sidecar freezes exactly the same scalar `V45` and `Q45` definitions used by
the previous block-(4,5) route and proves the new `15/16` coercivity without a
matrix-eigenvalue, floating-PSD, square-root, source, ODE, or admission premise.

No parent task state, registry/admission state, source theorem, coverage theorem,
or final Route-B conclusion was modified.

## 1. Kernel theorem surface

The exported theorem surface is:

```text
block45_Q_minus_15_16_V_sos
block45_Q_ge_15_16_V
block45_47_50_gap_at_z0
block45_not_ge_47_50_V_at_z0
lyapunov_ledger_of_15_16_coercivity
block45_lyapunov_ledger
quarter_barrier_gate
incremental_Kc_one_twelfth_gate
exact_capacity_improvement_over_93_100
ultimate_residual_coefficient
```

### 1.1 Exact weighted SOS identity

Lean proves, over `ℝ`, the exact identity

```text
Q45 - (15/16) V45 =
    (270997/64000000)       x4^2
  + (2073349/1740800000)    x5^2
  + (3769409/96000000)      y4^2
  + (13342021/384000000)    y5^2
  + (867/64000)             (x4-(5/17)x5)^2
  + (350003/64000000)       (x4-10y4)^2
  + (3/16000)               (x4+(20/3)y5)^2
  + (1/27200)               (x5-34y4)^2
  + (1806651/1740800000)    (x5-(68/3)y5)^2.
```

Every coefficient is positive, hence the kernel theorem derives

```text
(15/16) V45 <= Q45.
```

### 1.2 Exact nearby failure regression

The rational witness from the mathematical review is also frozen as a kernel
regression.  At

```text
z0 = (x4,x5,y4,y5) = (1,25/6,1/10,1/6),
```

Lean proves

```text
Q45(z0) - (47/50)V45(z0)
  = -83857069/120000000000,
```

and separately proves

```text
not ((47/50)V45(z0) <= Q45(z0)).
```

Thus no downstream decimal simplification may silently round the certified
constant up to the false `47/50` bound.

### 1.3 Downstream arithmetic consumers

The unchanged residual Young step is abstracted as

```text
Vdot <= -(1/2)Q + (17/10)L2.
```

Combined with `Q >= (15/16)V`, Lean proves

```text
Vdot <= -(15/32)V + (17/10)L2.
```

The two checker-facing division-free consumers are also formalized exactly:

```text
1088 L2 < 75
```

implies strict inwardness at `V*=1/4`, and

```text
272 mu + 3264 nu < 75
```

implies the `Kc=1/12` incremental-tube inequality.

Lean additionally checks

```text
(15/32)/(93/200) = 125/124,
(17/10)/(15/32)  = 272/75.
```

## 2. Portable sidecar / toolchain

Files:

```text
examples/routeb_p5_block45_15_16_sos_lean/P5Block45FifteenSixteenSOS.lean
examples/routeb_p5_block45_15_16_sos_lean/README.md
examples/routeb_p5_block45_15_16_sos_lean/lean-toolchain
examples/routeb_p5_block45_15_16_sos_lean/verify.sh
```

The sidecar toolchain is pinned to

```text
leanprover/lean4:v4.32.0
```

and `verify.sh` resolves `lake` / `lean` from `PATH`, checks the pinned Lake
environment, compiles with `-DwarningAsError=true`, requires an axiom report for
every exported theorem, and fails if `sorryAx` appears.  It is marked
`CI_PORTABLE=1` for `.github/workflows/lean-agent-sidecars.yml`.

## 3. Real GitHub Actions result

Real GitHub Actions run:

```text
run: 34169582427
job: 101887196687
head: fb21ff7351a5f9fb64e23103f4317488ff9fed52
Lean: 4.32.0
Lake: 5.0.0
```

The T-P5-034 group completed with:

```text
AXIOM_AUDIT=PASS
P5_BLOCK45_15_16_SOS_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_block45_15_16_sos_lean/verify.sh
```

All ten exported theorems report only

```text
[propext, Classical.choice, Quot.sound]
```

and the sidecar has no `sorryAx`.

The aggregate portable-sidecars workflow is still red, but the real log shows
that the failures are from pre-existing, separately owned sidecars, including
the FLT quotient relative-path failure, M4 cross-branch noncomputable/linter
errors, P5 componentwise/parameter-tube/weighted-dual errors, P7 tail-Schur
errors, and the old P8 ramp-reconstruction calculus/import errors.  I did not
modify or claim those tasks in this review.

## 4. Dependencies and remaining formal obligations

This sidecar closes only the source-independent `Q -> V` algebra and its scalar
consumer constants.  The following remain open and are not inferred from this
compile:

```text
P5_RESIDUAL_L2_SOURCE_BINDING=OPEN
TRUE_DH_FLOAT64_SEMANTICS=OPEN
ODE_FIRST_EXIT_COVERAGE=OPEN
P8_SAME_DOMAIN_TRAJECTORY_COVERAGE=OPEN
P5_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
```

A new mathematical result `T-P5-035` from 柳冠一 was also inspected this round.
It supplies a separate candidate storage lower coercivity
`V >= (3/125)||z||^2` and the typed Euclidean-gain-to-V-gain adapter; that result
is not silently bundled into this sidecar and should remain a separate Lean
child if selected by the coordinator.

## 5. Status

`T-P5-034` formal algebra status: `compiled_candidate`.

**待封不觉独立验证 / 待梁智炜最终整合。**
