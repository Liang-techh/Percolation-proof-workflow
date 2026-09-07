---
kind: review_result
review_id: review-T-P5-011-sumengchen-20260907T0221
task_id: T-P5-011
parent_review_id: review-T-P5-011-honglianmozun-20260907T0155
source_agent: 苏梦辰
claimed_at: 2026-09-07T02:08:00-06:00
created_at: 2026-09-07T02:21:00-06:00
inspected_commit: 8b1aa04700829e8147a94f68a4e0e65d13876de1
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_by_封不觉_then_harvest_by_梁智炜
---

# T-P5-011 — portable Lean cubic-energy self-bootstrap child

## Scope and mathematical source

This pass formalizes only the source-independent algebra from
`review-T-P5-011-honglianmozun-20260907T0155.md`.  It does not compute/source-bind
`S_F`, prove the physical lower bound `W_min`, identify Float64 central-FD
execution with the exact-real cubic model, close controller/solve bias, prove
first-exit/ODE coverage, mutate the registry, or change P5/M4 admission.

The mathematical seam is the square-only implication

```text
A >= 0,
Lambda >= 0,
g >= 0,
A <= K Z,
PC^2 <= Lambda A^3,
Lambda K Z <= g^2
--------------------------------
|PC| <= g A.
```

Together with the Lyapunov ledger

```text
Zdot <= -A + PC + PR + PB,
PR <= kappaR A,
PB <= 0,
kappaR <= 1,
Lambda K Z <= (1-kappaR)^2,
```

this gives `Zdot <= 0`.  A strict barrier, `A>0`, and `kappaR<1` give
`Zdot<0`.

## Portable sidecar

Created:

- `examples/routeb_p5_cubic_energy_barrier_lean/P5CubicEnergyBarrier.lean`
  - blob `f2cc87d9d690fdc07063f9721b8158e84dc50c49`;
- `examples/routeb_p5_cubic_energy_barrier_lean/verify.sh`
  - blob `ab25af82db280e7a234c3d0155d3366790f1abdc`;
- `examples/routeb_p5_cubic_energy_barrier_lean/README.md`
  - blob `ac9f3baea6e7bb0ea20b509f9536c1acd39a1de0`;
- `examples/routeb_p5_cubic_energy_barrier_lean/lean-toolchain`
  - blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`;
  - pin `leanprover/lean4:v4.32.0`, matching `examples/local_fkg`.

`verify.sh` contains `CI_PORTABLE=1`, resolves `lake` from `PATH`, checks the
local-FKG pinned toolchain, compiles with `-DwarningAsError=true`, requires an
axiom report for every theorem, and fails closed on `sorryAx`, compiler errors,
or missing declarations.

## Formalized theorem decomposition

The sidecar proves:

1. `abs_le_of_sq_le_sq_nonneg` — nonnegative square domination implies an
   absolute-value bound.
2. `cubic_square_absorption_from_energy_barrier` — the generic square-only
   energy bootstrap above.
3. `cubic_square_strict_absorption_from_energy_barrier` — strict barrier and
   positive `A,g` imply `|PC| < g*A`.
4. `cubic_energy_barrier_dissipation` — the relative-residual/bias ledger gives
   `Zdot <= 0`.
5. `cubic_energy_barrier_strict_dissipation` — the strict ledger gives
   `Zdot < 0`.
6. `regularizer_to_damping_coercivity` — from
   `A <= (13/10)*normSq` and `(1/2000000)*normSq <= Z`, derive the exact scalar
   bridge `A <= 2600000*Z`.
7. `fdLambda_mul_K_exact` — with
   `fdLambda(SF)=SF/(144*100000^4)`, prove exactly
   `fdLambda(SF)*2600000 = 13*SF/72000000000000000`.
8. `fourier_barrier_from_division_free` — convert
   `13*SF*Z <= 72000000000000000*g^2` to the normalized barrier
   `fdLambda(SF)*2600000*Z <= g^2`.
9. `fourier_cubic_absorption_from_division_free_barrier` — final one-scalar
   exact-real Fourier consumer with no square roots.

The first GitHub compile also exposed that `Z>=0`, `K>=0`, and `kappaR>=0` are
not logical premises of the core algebra once `A<=KZ` and the barrier are
already supplied.  Those hypotheses were removed instead of suppressing the
linter, so the final theorem interface is strictly smaller than the informal
starting statement.

## Math -> Lean -> CI -> repair loop

### Attempt 1: unused-premise failure

GitHub Actions:

```text
run_id: 34099162362
job_id: 101669446692
head: efb3514bf2d24f93bb5f4282f422a48283a15d22
runner: ubuntu-24.04
Lean: 4.32.0
```

The theorem bodies elaborated and printed ordinary Mathlib axioms, but
`-DwarningAsError=true` correctly rejected unused hypotheses:

```text
hZ      unused
hK      unused
hkappa0 unused (both ledger theorems)
```

The hypotheses were removed rather than hidden.

### Attempt 2: strict square-to-absolute-value proof failure

GitHub Actions:

```text
run_id: 34099490182
job_id: 101670408778
head: 8965e61c6d24cd8152cffb3b1bbd3474f86af408
runner: ubuntu-24.04
Lean: 4.32.0
```

The non-strict core and all non-strict consumers compiled, but the hand-written
strict branch ended with two `linarith failed to find a contradiction` errors;
that propagated `sorryAx` into the strict theorem and strict ledger theorem.
The repair replaced the manual sign split by Mathlib's exact
`abs_lt_of_sq_lt_sq` bridge after proving `(g*A)>=0`.

### Attempt 3: focused PASS

GitHub Actions:

```text
run_id: 34099849716
job_id: 101671527766
head: 8b1aa04700829e8147a94f68a4e0e65d13876de1
runner: ubuntu-24.04
Lean: 4.32.0
```

The focused log records:

```text
AXIOM_AUDIT=PASS
P5_CUBIC_ENERGY_BARRIER_FOCUSED_CHECK=PASS
FOURIER_SF_SOURCE_BINDING=OPEN
NONKINETIC_STORAGE_LOWER_BOUND=OPEN
IEEE_CUBIC_REMAINDER=OPEN
CONTROLLER_SOLVE_BIAS_CLOSURE=OPEN
FIRST_EXIT_ODE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_cubic_energy_barrier_lean/verify.sh
```

All nine printed theorem declarations depend only on

```text
[propext, Classical.choice, Quot.sound]
```

and the successful focused run contains no `sorryAx` for this sidecar.

The aggregate Actions job remains red for two disjoint pre-existing sidecars:

1. `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` still uses a
   bad relative `../local_fkg` path;
2. `examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`
   still has an unused `hκ1`, an invalid projection from a disjunction, and
   resulting `sorryAx` in the zero-kappa branch.

Those failures are outside this claim and were not modified.

## Exact remaining boundary

The Lean algebraic consumer is now available, but physical closure still needs
all of the following as separate typed inputs:

- a generated and source-bound exact rational `S_F` from the frozen Fourier
  tensor-error coefficients;
- the modified non-kinetic storage lower bound `W_min` on the same domain, hence
  the physical meaning of `Z`;
- an explicit Float64/IEEE remainder ledger for `dM`, `cijk`, and ordered
  accumulation, which is not part of `S_F`;
- controller/solve bias closure; a genuine positive additive bias cannot be
  hidden inside this cubic theorem;
- first-exit/ODE regularity and same-domain coverage if this barrier is used as
  an invariant-region argument.

The current artifact is therefore only `compiled_candidate` mathematical/formal
evidence: **待封不觉独立验证 / 待梁智炜最终整合**.
