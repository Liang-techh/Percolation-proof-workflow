# Finite Fourier shifted storage

`ShiftedStorage.lean` compiled successfully with the pinned offline cache.
All declarations are in namespace `RouteBShiftedStorage`.

The follow-up leaf `ActualShift.lean` composes this generic result with the
encoded rows of `PotentialSlice`, excludes constant row 8, and proves the
exact shift. See `ACTUAL_SHIFT.md` and use the separate `verify_actual.sh`.

## Main theorem and exact assumptions

For any finite coordinate type `ι`, finite mode type `ν`, and functions
`kp q : ι → ℝ`, `a phase : ν → ℝ`, define

```text
Q = (1/2) Σ_i kp_i q_i²
W = Q + Σ_n a_n (cos(phase_n) - 1)
B = 2 Σ_n max(a_n, 0).
```

`quadratic_le_shifted_storage` proves `Q ≤ W+B` without any condition on
the gains, coefficients, phases, or coordinates. The scalar proof uses
`-1 ≤ cos phase ≤ 1`: when `a≥0`, the term is at least `-2a`; when `a≤0`,
it is nonnegative. Summing these inequalities proves the shift bound.

Under the sole additional hypothesis `hkp : ∀ i, (2/5 : ℝ) ≤ kp i`,
`shifted_storage_chain` proves both links

```text
W+B ≥ Q ≥ (1/5) Σ_i q_i².
```

`shifted_storage_coercivity` gives the composed inequality.
`shift_nonneg` proves `B≥0`. The proof uses finite-sum inequalities and
never expands the coordinates or modes into an enumerated polynomial.
Empty finite index types are allowed. No mode independence, tensor symmetry,
mass property, differentiability, dynamics, or coefficient sign is assumed.

Phases can be specialized pointwise to `phase n = Σ_i frequency n i * q i`.
Their linearity is unnecessary for this bound. For a constant shift across
configurations, the coefficient family `a` must be fixed. Every mode supplied
is counted once: a table containing both conjugate rows needs no extra factor
of two in W. The factor two in B comes solely from the lower bound `cos-1≥-2`.
Keeping a zero-frequency row with phase zero is valid but can inflate B.

## Optional energy and block bounds

`kinetic M v = (1/2) Σ_i v_i (Σ_j M_ij v_j)`.
`shifted_energy_lower` has the explicit premises

```text
hkp   : ∀ i, kp_i ≥ 2/5
hmass : μ Σ_i v_i² ≤ Σ_i v_i (Σ_j M_ij v_j)
hE    : E = kinetic M v + W.
```

It proves `E+B ≥ (μ/2)Σ_i v_i² + (1/5)Σ_i q_i²`.
This algebraic implication holds for any real μ and arbitrary real matrix M;
using it as positive velocity coercivity requires μ>0. The specialization
below uses the explicitly positive rational `μ=9401/1000000`.

For `q v : Fin 6 → ℝ`, the exact definition is

```text
p45 q v = (3/2)(q 3² + q 4²) + (4/5)(v 3² + v 4²).
```

Lean indices 3 and 4 mean physical joints 4 and 5. These weights were read
from the actual target sources, not inferred from the requested comparison
constant. `block45_sq_le_total` bounds each pair of squares by the full sum
using inclusion of the finite set `{3,4}`.

`p45_le_shifted_energy` assumes exactly
`(9401/2000000)Σ_i v_i² + (1/5)Σ_i q_i² ≤ E+B` and proves
`p45 q v ≤ (1600000/9401)(E+B)`. The coefficient comparison uses
`(4/5)/(9401/2000000)=1600000/9401 ≥ (3/2)/(1/5)`.

`fourier_p45_bound` composes the results for finite Fourier modes, with the
three explicit premises hkp, hmass (μ=9401/1000000), and hE above. It does not
assume or prove that the actual target mass matrix meets hmass.

## Source binding boundary

The generic proof does not import the actual Fourier coefficients or prove
that the target storage equals W. The actual coefficient/phase identification
and mass lower bound remain required for target instantiation. In particular,
no `hslice` premise from `StorageObstruction.lean` is discharged here.
No actual-source numerical value of B is certified by this Lean file.

The inspected `examples/routeb_fd_force_budget/storage_report.md` reports
`B=4079979/400000` after exact coefficient counting. The generic file uses
the symbolic `2 Σ max(a_n,0)`; the separate `ActualShift.lean` leaf proves
the displayed numerical value for the imported coefficient encoding.

A shift changes the storage level used for any cap: if `E≤Ecap`, the shifted
quantity has cap `Ecap+B`; the initial storage value also shifts by B. These
lemmas alone do not close an energy tube, first-exit argument, or terminal
block certificate, and do not prove a derivative identity.

Read-only weight provenance (under
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`):

- `debug_12g_composite_routeB.jl:43`: `pw = [1.5, 0.8]`;
  line 92: `p = pw[1]*(qa^2+qb^2)+pw[2]*(dqa^2+dqb^2)`.
  SHA-256 `6c785db7aadc7943eb71f72c7af65a8eb80c7c165fb63381a665a8d5e6240344`.
- `routeB_compact_energy_storage_to_block_audit.py:28`: `P_Q=Q(3,2)`;
  line 29: `P_DQ=Q(4,5)`; line 108 explicitly identifies q4,q5,dq4,dq5.
  SHA-256 `80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9`.

Only these weight definitions are used, not the historical audit's other
storage or trajectory claims. The inspected storage report SHA-256 is
`2428fff0ba0b7be126ce7d2ec6ab3ca06068cc03443fa28e7a70203b9d4d5954`.

## Reproduction and actual evidence

From the workspace root in PowerShell:

```powershell
wsl.exe -d Ubuntu -- bash examples/routeb_shifted_storage/verify.sh
```

The script directly invokes the existing Lean executable and cached package
objects, without Lake builds, dependency downloads, comparator rebuilds, or
broad tests. All run outputs and source/script snapshots are written to a new
`output/run-*` directory here. Only `ShiftedStorage.lean` is compiled.

Successful first attempt: `output/run-pKu0JIpS/verify.log`, UTC
`2026-09-05T17:49:42Z`; axiom reports: `output/run-pKu0JIpS/compile.log`.

```text
Lean: 4.33.1, x86_64-unknown-linux-gnu
Lean commit: 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
mathlib: 0df444a360eaa60ab8c11dca51a86af692955474
warningAsError=true
LEAN_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
```

All ten theorem axiom reports list only Lean's standard
`[propext, Classical.choice, Quot.sound]`. There is no `sorryAx`, admitted
proof, or custom axiom. Source and compiled object SHA-256:

```text
ShiftedStorage.lean:
d74f40bcb946c30a0f04b398595c8ba59864436f3db7aa9a6278ba93e16dc30d
ShiftedStorage.olean:
f14284fbc99090f834b6447d7634c854b3e0e460f6fbcb47f2075673002d07e7
```

All task writes are confined to `examples/routeb_shifted_storage/`.
No target files or other example directories were changed.
