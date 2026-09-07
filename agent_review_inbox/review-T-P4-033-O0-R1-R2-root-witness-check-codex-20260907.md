# T-P4-033 O0-R1/R2 — root-witness check from existing data

Date: 2026-09-07  
State context: revision 504 at the final read-only check (the review was
started from the user-reported revision 502)  
Status: `CONDITIONAL_ROOT_WITNESS_ONLY`  
Scope: check whether existing exact-rational source/metric fields can produce
a root witness for `rho_r`, and whether the same data produces `epsilon_R`.
No existing ledger is consumed and no O0 closure is claimed.

## Result

The square-root arithmetic can be completed conservatively, but no actual
same-key child is consumable. The port data provides a squared bound for one
normalized map, not a keyed baseline/perturbation pair.

## Exact root witnesses available as candidates

`routeB_compact_port_frobenius_ledger.csv` records the exact rational squared
candidate for the left-output normalized map `T=R*B_up^(-1/2)`:

- eta 2.7: `g_27=4227/500000`;
- eta 5.6: `g_56=34547/1000000`.

These are not passed as `rho_r`. Exact rational upper-root witnesses can,
however, be constructed:

```text
rho_27 := 9195/100000,
rho_27^2 - g_27 = 321/400000000 > 0;

rho_56 := 1859/10000,
rho_56^2 - g_56 = 1181/100000000 > 0.
```

Thus, if a future receipt proves that the corresponding `g_eta` is the
baseline `R_r` bound under the canonical key, these rationals are valid
`rho_r` witnesses. They are only arithmetic witnesses now: the source ledger
labels itself a rigorous-numerical candidate, and the workflow node remains
open/unverified.

## Metric check

The exact metric constants in the compact interface are

```text
B_up = diag(1402217/12000000, 200739/4000000).
```

For this exact matrix, a valid lower bound is

```text
beta = 200739/4000000,
s = 1/5,
s^2 = 1/25 <= beta,
beta - 1/25 = 1018475/100000000 > 0.
```

So `s=1/5` is a valid exact square-root witness **provided** the receipt binds
this exact `B_up` to the same normalized map and source/state key. It is not a
proof that the current artifact's metric metadata is authoritative. The
pointwise `M_BB(q5)` and nominal `M0_BB` weighted ledgers remain different
metrics and cannot be substituted for this `B_up` contract.

## Missing `epsilon_R`

No existing exact source/metric artifact supplies a map difference

```text
R_delta = R_f - R_r
```

or a bound of the required form

```text
||R_delta*a_B||_2 <= epsilon_R*sqrt(a_B^T*B_up*a_B).
```

The Frobenius CSV has `rho2_frobenius_upper` and metric variants such as
`rho2_m0_upper`/`rho2_mass_upper`, but none is an `R_f-R_r` bound. The
`rho2_m0` and mass columns also represent different output metrics, not a
perturbation residual. Consequently no exact `epsilon_R` can be derived from
the current `g_27` or `g_56`.

The non-identifiability is already visible in one dimension: with `R_r=1/2`
and the same baseline bound `rho_r=1/2`, choosing `R_f=R_r` gives
`epsilon_R=0`, while choosing `R_f=-R_r` gives the sharp difference
`epsilon_R=1`. The baseline squared ledger alone cannot distinguish these
cases.

## O0-R1 dependency obstruction

The current source-side files do not attach an authoritative exact-real
inverse receipt for `K` to this port candidate. Under the current API,
`proves_exact_real_bound` defaults to `false`; hence a numeric DD inverse
ledger cannot be used to derive `K_f`, `DeltaK`, or the three-term `U_R`.
Without those exact-real outputs, a resolvent-derived `epsilon_R` is blocked
even if the root witnesses above are accepted arithmetically.

## Minimum actual child still required

To turn the candidate roots into a consumable child, provide one cell or
explicitly uniform domain receipt containing:

1. the canonical `source_key` and `state_key` shared by exact/Float64 `mu`,
   FD/force scales, block coordinates, rounding mode, `B_up`, and all bounds;
2. `proves_exact_real_bound=true`, exact `K`, exact `epsilon_A`, and
   `epsilon_A*K<1`, or a direct exact-real `U_R` receipt;
3. a proof that `g_eta` bounds the actual baseline `R_r`, then the rational
   root witness `rho_eta` above (or a tighter exact rational root);
4. an exact same-key bound for `R_f-R_r`, yielding `epsilon_R` directly or
   via the same-key `s=1/5` conversion;
5. the typed physical identity `R_port*a_B=r_B` if the child is to be called
   physical.

The exact-root part is therefore not the remaining mathematical blocker. The
minimum blocker is an authoritative, same-key `R_f-R_r` enclosure (and, for a
resolvent-derived enclosure, the exact-real `K` receipt). Until those arrive,
return `PENDING/OBSTRUCTION`, never `rho_r`/`epsilon_R` as verified inputs.
