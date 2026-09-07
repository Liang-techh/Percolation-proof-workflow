# Route-B P5 dissipative residual-power child

This Lean sidecar formalizes the reusable scalar closure identified by
`T-P5-004`. From the already-established premise

```text
y <= -delta * x^2 + epsilon * x
```

it proves a sharp global bound, a retained-dissipation bound, a parameterized
Young family, and strict negativity above the exact threshold. It also proves
strict decay when the residual is relatively bounded by `rho < delta`.

These are exact algebraic lemmas only. The DH dynamics, coercivity constant,
residual norm bound, domain coverage, and M4 admission remain separate open
obligations.
