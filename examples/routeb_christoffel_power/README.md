# Christoffel power identity

`ChristoffelPower.lean` proves the requested identity for every tensor
`T : Fin 6 → Fin 6 → Fin 6 → ℝ` and velocity `v : Fin 6 → ℝ`:

```text
Cforce_i = Σ_j Σ_k ((T_kij + T_jik - T_ijk)/2) v_j v_k
Mdot_ij  = Σ_k T_kij v_k
Σ_i v_i Cforce_i = (1/2) Σ_i v_i (Σ_j Mdot_ij v_j).
```

The main result actually works for any type `ι` with `[Fintype ι]`.
There are no additional hypotheses on `T` or `v`: no tensor or matrix symmetry,
positivity, invertibility, smoothness, nonzero velocity, or equation of motion.
All entries and divisions are in the exact real field.

## Mathematical proof

Write

```text
A = Σ_i Σ_j Σ_k T_kij v_i v_j v_k
B = Σ_i Σ_j Σ_k T_jik v_i v_j v_k
D = Σ_i Σ_j Σ_k T_ijk v_i v_j v_k.
```

Expanding only scalar arithmetic and distributing finite sums gives
`Σ_i v_i Cforce_i = (A + B - D)/2`. Exchange the outer dummy indices `i,j`
in `B` using `Finset.sum_comm`; commutativity of real multiplication gives
`B = D`. The remainder `A/2` is precisely the specified mass-rate power.
The proof never enumerates `Fin 6`, expands 216 entries, or assumes a
permutation symmetry of the tensor. `ring` is used only on scalar expressions
and on the three already-collected contractions.

## Lean interface and target boundary

All declarations are in namespace `RouteBChristoffelPower`:

- `contraction_swap`: the dummy-index exchange.
- `christoffel_power_identity`: arbitrary finite index type.
- `christoffel_power_identity_fin6`: the fully expanded requested statement.
- `christoffelMatrix_mul_velocity`: identifies the matrix convention with
  `christoffelForce`.
- `mechanical_energy_hC`: exactly the orientation and matrix shape of the
  `hC` premise in `RobotFormalEnergy.mechanical_energy_power_identity`.

Here the matrix convention is
`christoffelMatrix T v i j = Σ_k ((T k i j + T j i k - T i j k)/2) * v k`.
Once the target's `Mdot` and `C` are identified with `massRate T v` and
`christoffelMatrix T v`, respectively, the proof term for its `hC` is
`RouteBChristoffelPower.mechanical_energy_hC T v`.

For the physical interpretation, the remaining analytic binding is
`T k i j = ∂ M_ij / ∂ q_k` at the actual configuration, together with the
chain-rule identification of the actual time derivative `Mdot` and the actual
Christoffel matrix with these definitions. This file proves the algebraic
contraction after those identifications. It does not establish those derivative
facts, the target's kinetic derivative premise `hK`, potential derivative
premise `hU`, or energy decomposition `hE`. In particular, arbitrary tensors
need not arise as derivatives of a mass matrix. No target module is imported
or modified, and no full target compilation is claimed.

## Reproduce without downloads

From the workspace root in PowerShell:

```powershell
wsl.exe -d Ubuntu -- bash examples/routeb_christoffel_power/verify.sh
```

The script directly invokes the installed Lean executable and uses only the
existing `/home/z5242/sos_lean/.lake/packages/*/.lake/build/lib/lean` caches.
It checks the mathlib commit and toolchain pin, sets `warningAsError=true`,
and compiles just the new proof. No Lake build, dependency download,
comparator rebuild, or regression suite is invoked. Every run writes a new
`output/run-*` directory here, with source/script snapshots, checksums,
compiler output, and (on success) the `.olean`. Cache files are read only.

## Actual compilation evidence

Successful attempt: `output/run-YC2fOLUR/verify.log`, UTC
`2026-09-05T17:26:30Z`.

```text
Lean 4.33.1, x86_64-unknown-linux-gnu
Lean commit: 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
mathlib: 0df444a360eaa60ab8c11dca51a86af692955474
LEAN_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
```

The five `#print axioms` reports in `output/run-YC2fOLUR/compile.log` each list
only `[propext, Classical.choice, Quot.sound]`, the standard Lean foundations.
There are no proof holes, `sorryAx`, or user-declared axioms in the successful
proof. This is not a claim of being free of Lean's standard axioms.

```text
ChristoffelPower.lean SHA-256:
7546f38946f67bb3dfe6cca27c97b007c5320a9fbf4059d58742005f4f707c7c
ChristoffelPower.olean SHA-256:
438b27034753470dfdda0f3125a6e3d952f7b97466971a5039679435188272fc
```

The initial attempt `output/run-SHOXXDZl/` is retained as failure evidence.
Its minimal imports omitted the sum exchange/distribution lemmas and the
`Fin` Fintype instance. Replacing the basic group-sum import with
`Mathlib.Algebra.BigOperators.Fin` resolved the errors; the mathematical proof
did not change. Only the successful run is evidence for the final theorem.

All task writes are confined to this directory. This session exposed no
subagent tool, so no parallel-agent execution is claimed; independent
read-only inspection calls were run in parallel.
