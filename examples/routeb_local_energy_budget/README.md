# Local reference kinetic / PD storage budget

This leaf uses the requested exact reference masses and local PD coefficients.
It proves pointwise algebra and conditional energy/output bounds. It introduces
no source-specific axioms and does not identify an external robot implementation.
All edits and compile products are confined to this new example directory.

**Compiled successfully** on 2026-09-05 with the pinned environment.
See [VERIFICATION.md](VERIFICATION.md) for the successful run and all three
retained failed attempts.

## Storage, derivative, and total mismatch

```text
m44 = 350003/3000000       m55 = 200739/4000000
VB  = (m44/2)*v4^2 + (m55/2)*v5^2 + (3/10)*q4^2 + (1/4)*q5^2

m44*a4 = -(3/5)*q4 - (4/5)*v4 + (1/5)*w + e4
m55*a5 = -(1/2)*q5 - (13/20)*v5 + (1/10)*w + e5
```

VB contains constant-reference kinetic energy and the local PD position
quadratic. It does **not** contain gravitational potential. The meaning of `e`
is the **total reference-block force mismatch**, including mass error, remote
coupling acceleration, gravity, and FD/Float64 effects. It is not merely a tiny
finite-difference truncation residual. Matching these premises to actual dynamics
remains an external identification obligation.

`derivative_identity` proves the following equality for the explicit chain-rule
expression `m44*v4*a4 + m55*v5*a5 + (3/5)*q4*v4 + (1/2)*q5*v5`:

```text
dVB = -(4/5)*v4^2 - (13/20)*v5^2
      + (1/5)*v4*w + (1/10)*v5*w + v4*e4 + v5*e5.
```

`derivative_budget` takes an explicit equality between a supplied `dVB` and
that chain-rule expression, along with the two dynamics premises, and proves

```text
dVB <= (17/520)*w^2 + e4^2/(8/5) + e5^2/(13/10).
```

The half-damping split is exposed as an exact four-square remainder in
`half_damping_identity`. Each axis spends half its damping on `w` and half on
`e`. The input coefficients add to `1/40 + 1/130 = 17/520`.
No differentiability theorem or time integration is asserted by this algebraic
derivative statement.

## Initial state and output comparisons

`full12Ball x` means the zero-centered squared Euclidean full-state norm is
at most `9/400`. The explicit state order is `(q1,...,q6,v1,...,v6)`, so the
block projection uses zero-based `Fin 12` indices `3,4,9,10`.

The proved chain is

```text
full12Ball x
  => q4^2+q5^2+v4^2+v5^2 <= 9/400
  => VB0 <= (3/10)*(9/400) = 27/4000.
```

For arbitrary real block coordinates the leaf also proves

```text
p         = (3/2)*(q4^2+q5^2) + (4/5)*(v4^2+v5^2)
          <= (6400000/200739)*VB
qterminal = 3*(q4^2+q5^2) + 2*(v4^2+v5^2)
          <= (16000000/200739)*VB.
```

The terminal expression is a separate weighted quadratic, not the symbol `q`
for a coordinate. Both comparison constants are governed by the v5 coefficient.
For the exact cap `27/4000 + 17/520 + 1/10 = 7251/52000`, Lean verifies

| Output | Exact cap-derived bound | Required strict threshold |
| --- | --- | --- |
| p | `3867200/869869` | `< 28/5` (5.6) |
| qterminal | `9668000/869869` | `< 12` |

`outputs_of_cap` proves both strict conclusions together from `VB <= cap`.

## Explicit next obligation

`cap_of_energy_ledger` is a conditional interface: given

```text
VB(t) <= VB(0) + (17/520)*inputEnergy(t) + residualEnergy(t),
VB(0) <= 27/4000,
inputEnergy(t) <= 1,
residualEnergy(t) <= 1/10,
```

it proves `VB(t) <= cap`. Its scalar energy quantities have to be identified
externally. In the intended T=1 application they mean

```text
inputEnergy(t)    = integral_0^t w(s)^2 ds
residualEnergy(t) = integral_0^t [(5/8)*e4(s)^2 + (10/13)*e5(s)^2] ds.
```

The main next obligation is a justified bound on this **total** residual energy,
uniformly for the intended trajectories and times in `[0,1]`, along with the
actual dynamics/derivative identification, regularity, and integrated energy
comparison. The inequality `residualEnergy <= 1/10` is a premise, **not proved**.
Neither is an actual trajectory cap asserted. A pointwise residual bound and an
integrated residual-energy bound must not be conflated.

The optional `routeb_dh_power_binding/EnergyTube.lean` was inspected but is not
imported or modified; this leaf remains independent of its global storage
coefficient and analytic dependency chain. No global shifted-storage/output
comparison is used.

## Direct cached verification

```powershell
wsl -d Ubuntu -- bash '/mnt/c/Users/z5242/Desktop/重构版/工作流/examples/routeb_local_energy_budget/verify.sh'
```

The verifier uses the direct Lean 4.33.1 binary and cached libraries in
`/home/z5242/sos_lean`, checking Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`. Warnings are errors. Each invocation
retains exact source/script snapshots and real compile/verification logs in its
own `output/run-*` directory. No broad tests, solver runs, dependency downloads,
or Lake builds are performed.
