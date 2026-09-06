# Final receipt

Status: PASS

Successful run: `output/run-TIbpu6FN`  
Log: `output/run-TIbpu6FN/terminal.log`  
Start/end UTC: `2026-09-05T21:27:55Z` / `2026-09-05T21:28:03Z`  
Command: Lean 4.33.1 with `-DwarningAsError=true` and explicit `--root`; cached imports only.  
Lean commit: `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`  
Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`  
Compile exit: `0`  
Snapshot check: `SNAPSHOT_HASHES_UNCHANGED=true`

## Hashes

| Artifact | SHA-256 |
| --- | --- |
| current `OriginQuadratic.lean` | `f7ff884197da4d21c0d45e639779948c794134b85d490314f012c1812c915ea0` |
| frozen run source | `f7ff884197da4d21c0d45e639779948c794134b85d490314f012c1812c915ea0` |
| `OriginQuadratic.olean` | `42106f99ded794503a116f69f51733decc5882b6bd1b0ba4b631114909c544dd` |
| `terminal.log` | `87466f89a0ec581a22520fd26be6531033deec52d381cad19e16810875d6a74d` |
| `before_run.sha256` | `7685e9933304ff456fad6dc49d73dddc18a09d58241b5c289dac906139808e35` |
| pinned Lean executable | `38fcb4b987cc8e00c8e669795de0d14f1a08cf882fb6177a2b230035baaf4290` |

## Axiom audit

`#print axioms` for all four exported structural theorems reports only:

```text
propext, Classical.choice, Quot.sound
```

No `sorry`, `admit`, or custom `axiom` declaration occurs in the delivered
Lean source. Scope is limited to this new directory; no state, existing leaf,
or archive was written.
