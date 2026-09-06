# Route-B exact rational supply sidecar

This directory proves only the six-dimensional quadratic damping/disturbance
supply core. It does not certify the complete DH model, the Julia audit,
Float64 dynamics, an invariant region, or a finite-time theorem.

## Mathematical result

For arbitrary `v : Fin 6 → ℝ` and scalar `w : ℝ`, define

```text
D = [13/10, 11/10, 19/20, 4/5, 13/20, 1/2]
G = [1, 1/2, 3/10, 1/5, 1/10, 1/20]
c = [5/13, 5/22, 3/19, 1/8, 1/13, 1/20] = G/(2D)
P(v,w) = -sum_i D_i v_i^2 + sum_i G_i v_i w
gamma = 631227/2173600 = sum_i G_i^2/(4D_i)
margin = 1542373/2173600 = 1 - gamma > 0
```

`vector_completion_identity` proves exactly

```text
gamma*w^2 - P(v,w) = sum_i D_i (v_i - c_i*w)^2.
```

`completion_six` expands the right side into all six rationally weighted
squares. `pointwise_supply_bound` gives `P(v,w) ≤ gamma*w²`, without a
domain restriction, circle constraint, or hypothesis on `w`. The positive
damping and exact value of gamma are proved from the definitions.

`supply_at_center` proves equality at `v_i = c_i*w`.
`uniform_supply_coefficient_iff` proves that a real coefficient `beta`
bounds `P(v,w)` by `beta*w²` for **all** real vectors and inputs if and
only if `gamma ≤ beta`. This sharpness concerns this unconstrained
quadratic form; it does not assert that an extremizing vector is attained
along a particular DH trajectory.

The conditional interfaces expose the missing physical premises:

- `power_bound_with_remainder`: from `dE = P(v,w) + remainder` and
  `remainder ≤ defect`, conclude `dE ≤ gamma*w² + defect`.
- `unit_supply_of_power_identity`: from the same power identity and
  `remainder ≤ margin*w² + completion(v,w)`, conclude `dE ≤ w²`.
- `unit_supply_of_margin_bound`: the simpler sufficient assumption is
  `remainder ≤ margin*w²`. At `w = 0` this requires nonpositive remainder;
  a fixed positive absolute error does not satisfy it automatically.

These are explicit premises, not asserted axioms about the DH source.
The index order is fixed: Lean `Fin 6` index 0 is Julia joint 1.

## Duplication check and source evidence

Inspected the target's four `.lean` files under
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/`
and workflow `examples/` Lean sources outside `.lake` packages.
The existing `energy_invariant_formal_core.lean` contains `young_term`
(line 47), `diagonal_young` (62), `diagonal_dissipation_bound` (78),
and `descriptor_energy_derivative_bound` (265). Its scalar Young proof
already uses a generic single-square identity. No occurrence of the
exact `631227/2173600` constant or the concrete six-vector completion
was found in those existing Lean sources. The new namespace
`RouteBSupplyCore` adds the explicit vector identity, exact specialization,
attainment/minimality statement, and completion-credit supply implication.
It imports no target files and does not change existing theorems.

The authoritative Julia directory inspected read-only was
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.

| File and lines | Observed content | SHA-256 of inspected file |
| --- | --- | --- |
| `routeB_compact_corrected_newton_euler_dh_supply_audit.jl`, 20–21 and 98 | Exact rational `D_DH`, `GW_DH`, and `sum(GW_DH[i]^2/(4*D_DH[i]))` | `e68d8fc5aa1072354f29cfb711aa95e8d6027797e0221c7b4417c78ea9bf9b78` |
| `dhport_lib.jl`, 15–17 and 108 | `Kd+b_fr`, and disturbance force `(gw_coef .* I_val) .* w` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |

The existing CSV reports `gamma_DH=631227//2173600`, the positive margin,
and an exact syzygy modulo circles. Its recorded controller SHA-256
matches the current controller file above. The CSV explicitly sets
`formal_certificate_allowed=false`. The Julia audit was inspected, not
rerun; its syzygy claim is not proved or imported by this Lean sidecar.
The hashes above are new provenance notes, not updates to old ledgers.

## Reproduce offline

From PowerShell:

```powershell
wsl -d Ubuntu -- bash /mnt/c/Users/z5242/Desktop/重构版/工作流/examples/routeb_supply_core/verify.sh
```

The script uses the already installed Lean 4.33.1 binary directly and
Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474` cached in
`/home/z5242/sos_lean/.lake/packages/mathlib`. This matches
`examples/minimal_lean/lean-toolchain` (`leanprover/lean4:v4.33.1`).
The minimal example itself has no Mathlib dependency and its challenge
contains proof holes, so none of its proof files are imported. The
WSL environment also has other Lean versions; this script selects 4.33.1.

No `lake`, `elan`, cache getter, or download command runs. Dependency
build directories are passed through `LEAN_PATH` and read without rebuilding.
`ROUTEB_LEAN_CACHE` and `ROUTEB_LEAN_BIN` may point at another already
populated compatible environment; the Mathlib revision remains checked.
Every run creates a fresh `output/run-*` directory in this sidecar and
records the compiler version, dependency revisions, input hashes,
command, compiler output, axiom audit, and compiled object hash.

Strict verification runs with `-DwarningAsError=true`. The script rejects
proof-escape tokens, requires all 18 `#print axioms` reports, and allows
only the standard foundational axioms `propext`, `Classical.choice`, and
`Quot.sound`. Thus “no axioms” here means **no added/custom axioms and
no `sorryAx`**, not the absence of Lean/Mathlib's standard foundations.

## Actual compilation evidence

The successful run is `output/run-T5uqSOxk/` (2026-09-05 UTC):

- `verify.log`: full environment, command, input hashes, successful exit,
  axiom audit, and output hash.
- `compile.log`: all 18 actual Lean `#print axioms` reports.
- `RouteBSupplyCore.olean`: compiled object.

```text
Lean 4.33.1, compiler commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Lean exit code: 0
Axiom audit: 18 declarations; unexpected axioms: 0
PASS: 18 theorem axiom reports; zero proof holes; no custom axioms.
Lean source SHA-256:
646c1052c10c1d8606342010c4303c0c25e40e008664ce7f1c1b1649c51f6971
Compiled object SHA-256:
f304644744c10b0bc2387d380443f0cae06a76c11b6208000ff5d79a2e5b1631
```

The earlier `output/run-zON1nXUp/` logs are retained as failed-attempt
history: strict compilation rejected two unnecessary tactic sequencing
warnings. Those two proof-script lines were corrected before the successful
run above. There is no successful object claimed for the earlier run.

## Remaining source-binding obligations

1. **Parameter/model binding.** The exact decimal-rational vectors have
   been transcribed and checked against the inspected source. A formal
   source extraction or refinement must bind these Lean definitions to
   the chosen controller semantics. Julia's Float64 evaluation of
   `Kd+b_fr` and `(gw_coef .* I_val)` is not rational arithmetic.
2. **Exact energy/power binding.** Establish the energy derivative
   premise for the selected analytic DH model. A relevant candidate is
   `E = 1/2 vᵀ(M_DH(q)+mu I)v + U(q) + 1/2 sum Kp_i q_i² - G0·q`,
   with `mu=1/1000000` when retaining the audited regularizer.
   This requires the actual kinematics, kinetic-energy identity,
   potential-gradient identity, controller substitution, and consistency
   of constant compensation `G0`. No positivity of this candidate energy
   or storage comparison follows from the supply algebra alone.
3. **Syzygy/lift binding.** Prove or certify the exported polynomial
   identity and its use under the circle/lift equations. The inspected
   Julia audit has 36 velocity rows, 21 split-force rows, and six global
   balance rows. This sidecar does not establish those rows, their
   coefficient normalization, or the source-to-polynomial translation.
4. **Numerical residual binding.** `dhport_lib.jl` uses mass regularization
   `1e-6`, central finite differences with step `1e-5`, and a floating
   linear solve. Relate its `C/G`, gains, and acceleration to the analytic
   model with signed power-remainder bounds on an explicitly justified
   domain. The nominal gamma spends all physical damping in the
   square completion; any residual absorption must satisfy one of the
   stated remainder premises or use a separately proved damping allocation.
5. **Trajectory and final claim binding.** Supply the ODE/chain-rule
   hypotheses, existence/continuation, disturbance convention and
   integration, block-(4,5) storage comparison, domain/flowpipe inclusion,
   initial conditions, and final barrier or finite-time obligations.
   The quadratic coefficient theorem proves none of these.

All created sources and compilation outputs are confined to this directory.
Workflow `src`, state, reports, the target repository, and historical
hash records were not edited.
