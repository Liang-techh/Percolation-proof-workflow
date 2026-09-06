# Relative-eta denominator leaf receipt

Status: PASS — compiled candidate, source-unbound

Successful run: `output/run-vLUcsyKh`

Pinned environment:

- Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`
- `-DwarningAsError=true`
- cached dependencies only

Compiler result:

```text
RelativeEtaDenominator_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SNAPSHOT_HASHES_UNCHANGED=true
```

The successful leaf proves:

```text
rho > 0, 0 <= tau <= 1, |etaU| <= kappa*rho,
kappa < 36802229/24000000
  => rho*(rho*(A + tau*D) - tau*etaU) > 0,
```

for exact rational `A=2002229/24000000` and `D=29/20`. It also proves the
division-free equivalence
`directGate <-> E <= b + a1 * denominator`.

The exported theorem reports contain only the standard axioms
`propext`, `Classical.choice`, and `Quot.sound`. The source contains no
`sorry` or `admit`.

| Artifact | SHA-256 |
|---|---|
| `RelativeEtaDenominator.lean` | `7205581770ed544f2d41608982600583a78b98e6606ae1ffde6d70639619bb73` |
| `RelativeEtaDenominator.olean` | `ccce9f3aebca9225a5c9a42d1b06890a4036123aba3ad838225a5bb6ba1753c0` |
| `terminal.log` | `9d70bd631662b665c22955dd312296b82b67dd1755e96cdce5a672e18cd343d6` |

## Scope boundary

`etaU` and the relative bound are abstract hypotheses. This leaf does not
prove physical DH source binding, the relative bound from implementation
semantics, uniform feasibility, continuation, reachability, or `J <= 1`.
It is not promoted to the verified theorem registry and does not change
`formal_certificate_allowed=false`.

The failed first compile remains at `output/run-u5pj4VJR/` and is documented
in `ATTEMPT_HISTORY.md`.
