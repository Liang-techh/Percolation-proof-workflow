# B45-1.g q=0 mass bridge receipt

Status: PASS

Successful run: `output/run-iIbVmSPE`

- Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`
- `MassZeroBridge_COMPILE_EXIT_CODE=0`
- `VERIFY_EXIT_CODE=0`
- external audit: `output/audit-20260905T221316Z/result.json`

| Artifact | SHA-256 |
|---|---|
| `MassZeroBridge.lean` | `6dcc3103b9a6b9f69ba66fb5649835a28797cd94dce69f6fd53aabe7f839b219` |
| `MassZeroBridge.olean` | `ff8a1e54a1516bfb19aafaff2783098fffbbd4b0d405e7c8067e696ce2989bca` |
| source CSV | `a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8` |

The external checker re-aggregates 610 CSV rows with exact rationals, verifies
the frozen q=0 payload and regularized M0 payload, and records that Lean does
not read the CSV. The kernel proves the finite matrix equality and entrywise
corollary. This is an exact q=0 bridge only: full q-dependent DH/Fourier
binding, Float64 semantics, PSD, and reachability remain open.
