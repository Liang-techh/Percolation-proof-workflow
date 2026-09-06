# Positive-supply frontier receipt

Status: PASS for the independent algebraic sidecar.

Successful run: `output/run-1dUPvw7e`  
Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`  
Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`  
`-DwarningAsError=true`; cached dependencies only  
`Frontier_COMPILE_EXIT_CODE=0`; `VERIFY_EXIT_CODE=0`  
`SOURCE_RESTRICTION_CHECK=PASSED`

The exported theorem reports use only `propext`, `Classical.choice`, and
`Quot.sound`. No state, registry, original target, or broad regression was
modified.

| Artifact | SHA-256 |
|---|---|
| `Frontier.lean` | `bd35a95bceb38363c9322370d9b056d8dee3a363bee384bef4ca2f34d5bda7f0` |
| `Frontier.olean` | `48130daa1e367dbdc64b1bb19fb38c15a156a3c246eb87502726e43fe058f579` |

Classification: `COMPILED_CANDIDATE / TWO_REGIME_FRONTIER_ONLY`. This is not a
physical feasibility theorem and is not registry-promoted.
