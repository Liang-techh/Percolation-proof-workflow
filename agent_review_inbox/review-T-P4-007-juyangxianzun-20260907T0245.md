---
kind: review_result
review_id: review-T-P4-007-juyangxianzun-20260907T0245
task_id: T-P4-007
source_review_id: review-T-P4-007-liuguanyi-20260907T0212
source_agent: 巨阳仙尊
claimed_at: 2026-09-07T02:33:00-06:00
created_at: 2026-09-07T02:45:00-06:00
inspected_commit: eb09c0f5e00d4648fc29de87a5b508e5d14b9639
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_validate_by_封不觉_then_harvest_by_梁智炜_Codex
---

# T-P4-007 — execution-lift residual algebra Lean sidecar

## Scope

This formalization consumes the substantive mathematics in
`review-T-P4-007-liuguanyi-20260907T0212.md` (blob
`34960b13374d77a8780bb5dce12acac4ab2af47e`).  It does not redo source audit or
residual estimation.  The goal is only to make the source-independent algebra
kernel-checkable while keeping all Float64/source/coverage premises outside the
theorem definitions.

The mathematical interface being formalized is:

```text
solveDefect_B := M_BB a_B + M_BD a_D - (tau_B - C_B - G_B),

l_F := I_B f_B - M0_BB a_B,

l_F
 = (I_B f_B - tau_B)
   + (M_BB a_B - M0_BB a_B)
   + M_BD a_D + C_B + G_B - solveDefect_B.
```

The minus sign on `solveDefect_B` is retained explicitly; no exact-solve premise
is silently inserted.

## Artifact

Created the portable sidecar
`examples/routeb_p4_execution_residual_lean/`:

- `P4ExecutionResidual.lean`
  - blob `2b6dec076808acc56d0b7152db496bca7ad0856d`;
- `README.md`
  - blob `f29a04d1c1b16015fd67be9c63de3af7b8c0cfef`;
- `verify.sh`
  - blob `f8581ec84200d6967a1b2a92ff46e8cb038fc403`;
- `lean-toolchain`
  - blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`;
  - pin `leanprover/lean4:v4.32.0`, matching the repository's
    `examples/local_fkg` environment.

`verify.sh` contains `CI_PORTABLE=1`, resolves `lake` from `PATH`, checks the
sibling Lake root/toolchain, compiles with `-DwarningAsError=true`, and rejects
`sorryAx`, unknown-module, and compile-error output.

## Formalized theorem decomposition

The sidecar uses

```lean
abbrev VecB := Fin 2 → ℝ
```

and keeps all physical terms as typed two-component real vectors.

### 1. Solve-defect sign convention

```lean
def blockSolveDefect
    (massLocal massRemote tau C G : VecB) : VecB :=
  fun i => massLocal i + massRemote i - (tau i - C i - G i)
```

```lean
theorem block_tau_from_solve_defect ... :
  tau = fun i =>
    massLocal i + massRemote i + C i + G i
      - blockSolveDefect massLocal massRemote tau C G i
```

This fixes the execution-lift sign convention before any quantitative error
bound is supplied.

### 2. Full block residual identity

```lean
theorem block_residual_with_solve_defect ... :
  blockResidual If M0a = fun i =>
    (If i - tau i)
      + (massLocal i - M0a i)
      + massRemote i + C i + G i
      - blockSolveDefect massLocal massRemote tau C G i
```

The theorem is purely algebraic and does not identify the abstract arguments
with deployed DH values.

### 3. Exact-solve specialization

```lean
theorem block_residual_exact_solve ...
    (hsolve : blockSolveDefect massLocal massRemote tau C G = 0) :
  blockResidual If M0a = fun i =>
    (If i - tau i)
      + (massLocal i - M0a i)
      + massRemote i + C i + G i
```

Thus the older exact-solve formula is formally a corollary, not the default
execution theorem.

### 4. Centered runtime/reference split

For arbitrary state type `α`, the sidecar proves both

```text
Gexec(q)-Gexec(q0)
 = [Gref(q)-Gref(q0)] + [delta(q)-delta(q0)]
```

and the model-subtracted form

```text
Gexec(q)-Gexec(q0)-model(q)
 = [Gref(q)-Gref(q0)-model(q)] + [delta(q)-delta(q0)].
```

These are `centered_reference_split` and
`centered_reference_split_with_model`.  They preserve the mathematical point
from the source review that a runtime offset evaluated by the same routine at
the reference state should enter as a centered difference rather than be
charged twice as unrelated additive bias.

### 5. Relative-envelope zero-slice obstruction

The sidecar proves:

```lean
theorem relative_envelope_zero_slice
    (l y k : ℝ)
    (h : |l| ≤ k * |y|)
    (hy : y = 0) :
    l = 0
```

plus a pointwise state-space version and the contrapositive obstruction:

```lean
theorem no_relative_envelope_of_nonzero_zero_slice ... :
  ¬ (∀ x, |l x| ≤ k * |y x|)
```

whenever one state has `y=0` but `l≠0`.  This is the formal fail-closed boundary
for attempts to compress the entire P4 execution residual into a single
coordinate-relative envelope.

## CI loop: failure, repair, focused pass

### First GitHub-hosted run

Initial portable head:

```text
d14eed2eef80a97ed356efbf6615c36bdc3aa06a
```

GitHub Actions:

```text
workflow: Lean agent sidecars
run_id:   34101358190
job_id:   101676326163
runner:   ubuntu-24.04
```

The new sidecar genuinely reached Lean and failed at
`P4ExecutionResidual.lean:86:2`:

```text
error: `simp` made no progress
```

inside `block_residual_exact_solve`.  Because the failed theorem was still
printed, the axiom report correctly exposed `sorryAx`.  This was a local proof
script defect, not a mathematical counterexample.

I repaired only that theorem by replacing the brittle final `simp [hs]` step
with a pointwise `funext`, explicit `rw [hs]`, and `ring`.  Repair/tested head:

```text
eb09c0f5e00d4648fc29de87a5b508e5d14b9639
```

### Second GitHub-hosted run

GitHub Actions:

```text
workflow: Lean agent sidecars
run_id:   34101891552
job_id:   101677980412
runner:   ubuntu-24.04
Lean:     4.32.0
Lake:     5.0.0-src+8c9756b
```

The focused result is now:

```text
AXIOM_AUDIT=PASS
P4_EXECUTION_RESIDUAL_FOCUSED_CHECK=PASS
FLOAT64_RUNTIME_BOUNDS=OPEN
DH_SOURCE_BINDING=OPEN
P8_DOMAIN_COVERAGE=OPEN
P4_FULL_RESIDUAL_ABSORPTION=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_execution_residual_lean/verify.sh
```

All eight printed declarations have exactly the ordinary Mathlib axiom set

```text
[propext, Classical.choice, Quot.sound]
```

and the repaired theorem set has no `sorryAx`.

The aggregate workflow job still concludes `failure`, but this is caused by
other independent portable artifacts: the Anthropic FLT quotient transport
sidecar still has a bad relative Lake-root path, and the separately owned P5
weighted-dual residual sidecar still has its known zero-`kappa` Lean errors.
The shared workflow is non-fail-fast, so the log unambiguously records this
T-P4-007 sidecar as `SIDECAR_RESULT=PASS` before the aggregate failure.

## Dependency and admission boundary

This sidecar closes only the formal algebra.  It does **not** prove any of the
following physical premises:

- an IEEE/Float64 bound on `solveDefect_B`;
- the source bindings for local `ΔM`, remote `ΔM_BD a_D`, `ΔC`, centered
  `ΔG(q)-ΔG(q0)`, or controller execution error;
- the exact-real DH/source semantic bridge;
- same-domain P8 trajectory/flowpipe coverage;
- combination with the independent T-P4-012 remote-mass energy consumer;
- a global relative residual envelope or full P4/M4 closure.

The useful theorem-chain interface is now explicit:

```text
source/runtime quantitative bounds
        ↓
block_residual_with_solve_defect
        ↓
separate local / remote / C / centered-G / controller / solve budgets
        ↓
appropriate Schur, mass-metric, relative, or bias consumers.
```

No source term is automatically absorbed merely because the algebra compiles.

## Recommended next formal/source split

- Source/interval lane should bound `solveDefect_B` and the centered runtime
  remainders on the same P8 domain.
- The remote exact-real term should continue through the independent
  `T-P4-012` mass-metric theorem rather than being collapsed into an entrywise
  residual envelope.
- Formalization can later compose the individual bounds only after their units
  and reference-coordinate roles are frozen.

This result is only a Lean `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.  No authoritative P4/M4 status or registry entry was changed.
