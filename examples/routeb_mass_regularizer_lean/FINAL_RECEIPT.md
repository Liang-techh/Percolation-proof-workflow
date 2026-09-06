# Exact mass regularizer leaf receipt

Status: PASS

Successful run: `output/run-8qHz1Tiv`

- Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`
- `-DwarningAsError=true`
- `MassRegularizer_COMPILE_EXIT_CODE=0`
- `VERIFY_EXIT_CODE=0`
- `SNAPSHOT_HASHES_UNCHANGED=true`

| Artifact | SHA-256 |
|---|---|
| `MassRegularizer.lean` | `cd8dafa426a77d867e541f6855b71e58157d383bbbfa214a2712235bf851528b` |
| `MassRegularizer.olean` | `f3b2566f78df4e9a4bbdbba7a7f58319c6c4b5315fe57e87a80cb343af18667a` |

The leaf proves exact entrywise diagonal/off-diagonal regularizer semantics,
the composition with an explicit unregularized DH/Fourier equality premise, and
the fact that the off-diagonal regularizer contribution is zero. It does not
prove the DH/Fourier equality, the Float64 bridge, mass PSD, or `J <= 1`.
The exported theorem axiom reports contain only `propext`, `Classical.choice`,
and `Quot.sound`.
