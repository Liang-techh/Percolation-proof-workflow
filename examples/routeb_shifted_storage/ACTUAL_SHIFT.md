# Exact constant for the imported Fourier storage

`ActualShift.lean` imports the previously compiled `ShiftedStorage` and
`PotentialSlice`. It works with `RouteBPotentialSlice.W`, not an assumed
replacement for that definition.

The coefficient family is exactly

```lean
def a (i : Fin 17) : ℝ :=
  if i = 8 then 0 else RouteBPotentialSlice.coefficient (RouteBPotentialSlice.rows i)
```

`actualKp i` is the real cast of the imported rational `Kp i`;
`phases q i` is the imported phase of row i at q.

The eight theorems in namespace `RouteBActualShift` establish:

- `constant_row_phase`: row 8 has zero phase for every q.
- `potential_zero_eq_sum`: potential at zero is the sum of all coefficients.
- `actual_W_eq_storage`: the imported W is exactly
  `storage actualKp q a (phases q)`; the constant row cancels.
- `actual_shift_exact`: `shift a = 4079979/400000`, proved by exact rational
  arithmetic over the 17 encoded rows, with row 8 replaced by zero.
- `actualKp_lower`: every imported gain is at least 2/5.
- `actual_shifted_storage_chain`: both links
  `W q + 4079979/400000 ≥ proportionalEnergy q ≥ (1/5) Σ_i q_i²`.
- `actual_W_shifted_coercivity`: `(Σ_i q_i²)/5 ≤ W q + 4079979/400000`.
- `actual_p45_bound`: the optional block comparison with that exact shift.

The W bound has no hypotheses besides `q : Fin 6 → ℝ`. The proof of
`actual_W_eq_storage` distributes the difference of finite sums and treats
row 8 separately; it does not expand the full trigonometric expression.
Only the rational shift calculation enumerates the 17 coefficients.

For `actual_p45_bound`, the exact remaining premises are

```text
(9401/1000000) Σ_i v_i² ≤ Σ_i v_i (Σ_j M_ij v_j)
E = RouteBShiftedStorage.kinetic M v + RouteBPotentialSlice.W q.
```

The conclusion is
`RouteBShiftedStorage.p45 q v ≤ (1600000/9401)(E+4079979/400000)`.
The p45 weights remain precisely 3/2 on joints 4,5 configuration squares and
4/5 on their velocity squares (Lean indices 3,4).

This closes the constant and W identification for the *encoded* Fourier
model in PotentialSlice. It does not prove the physical DH potential equals
that encoding, Float64 execution semantics, the actual mass lower bound, or
an energy tube. It uses the imported rows directly and adds no assumed
coefficient-to-storage equality. The imported module's prior source audit
is not rerun or upgraded to a Lean proof of external file semantics.

## Reproduce the leaf only

From the workspace root in PowerShell:

```powershell
wsl.exe -d Ubuntu -- bash examples/routeb_shifted_storage/verify_actual.sh
```

The script checks the installed Lean 4.33.1 and mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474` pins and uses these exact import
directories without rebuilding them:

```text
examples/routeb_shifted_storage/output/run-pKu0JIpS
examples/routeb_potential_slice/output/run-SuGxG04V
examples/routeb_dh_power_binding/output/tube-RWfVZNvn
```

The last directory provides the transitive `StorageObstruction` import.
Mathlib dependencies come from the existing `/home/z5242/sos_lean` package
cache. Only `ActualShift.lean` is compiled, with warnings treated as errors.
Each attempt creates a fresh `output/actual-*` directory here containing the
source/script snapshots, logs, hashes, and successful compiled object.
No external sources, existing compiled objects, or other examples are changed.

## Actual compilation evidence

Successful attempt: `output/actual-GqBg6J4g/verify.log`, started at UTC
`2026-09-05T17:56:47Z`. The compiler completed with
`LEAN_COMPILE_EXIT_CODE=0` and `VERIFY_EXIT_CODE=0`, using Lean 4.33.1 and
the pinned mathlib above. All eight theorem reports in
`output/actual-GqBg6J4g/compile.log` list only
`[propext, Classical.choice, Quot.sound]`. There are no proof holes,
`sorryAx`, or custom axioms.

```text
ActualShift.lean SHA-256:
d60976ce10dc670fd93dad045c5d97fc426ae6c69036de8a3266e16e26c96579
ActualShift.olean SHA-256:
2e28e4c2b1d6834c70a314ca2545e51d6c5c8e2127739906a584131e9ae81f0c
```

The verify log also records hashes of all three imported source snapshots
and compiled objects. The current PotentialSlice source was checked to have
the same SHA-256 as its pinned snapshot:
`25e9ebe489b4f819f56e7334693d1d808e6ebd234139f659b14eb67125b846e7`.

The initial failed attempt `output/actual-fYGBJat5/` is retained. It exposed
two finite-index normalization omissions: row 8's vector lookup and equality
tests against index 8. Making the zero-frequency vector explicit and adding
`Fin.ext_iff` to the exact rational calculation resolved them. Only the
successful attempt is compilation evidence for these final theorems.
