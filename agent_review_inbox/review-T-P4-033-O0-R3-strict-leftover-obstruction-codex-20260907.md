# T-P4-033 O0-R3 — strict-positive-leftover exact receipt search

Date: 2026-09-07  
Observed state: revision 508  
Scope: same-key exact-Fourier one-cell R3 only; no consumer call, registration,
or O0 closure.

## Result

No consumable same-key receipt exists for the triple

```text
(weighted baseline rho_r, remaining margin m_r, theta).
```

The exact-Fourier key currently supplies the factor-2 weighted perturbation
only. The state and inbox search found no authoritative fields named or
equivalent to `weighted_baseline.rho_r`,
`schur_baseline.remaining_margin_m_r`, or a fixed exact `theta` under that
same source/state/metric key.

## Key and available perturbation

```text
source_key = routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)
state_key  = routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity
```

The accepted factor-2 adapter provides, in the left-output Euclidean metric,

```text
epsilon := epsilon_R^(2,weighted)
 = 10884976891854242252555776013990910667449238154978439 /
   106656554159567228416987083730445236164580900447719948854959486481478400000
```

with `B_up = diag(1402217/12000000, 200739/4000000)` and `s=1/5`. The
source bound remains induced-infinity and the output metric is Euclidean-2;
these norm tags must not be collapsed.

## Exact strict arithmetic required by the new API

For exact `rho_r >= 0`, `epsilon >= 0`, `theta > 0`, and exact baseline
remaining margin `m_r`, the only valid leftover is

```text
lambda = 1 + 1/theta
charge = lambda * ((rho_r + epsilon)^2 - rho_r^2)
       = lambda * (2*rho_r*epsilon + epsilon^2)
m_f = m_r - charge.
```

Strict R3 requires

```text
m_r > lambda * (2*rho_r*epsilon + epsilon^2),
equivalently m_f > 0.
```

The lower-level arithmetic helper's nonnegative leftover result is not enough
for this API; equality `m_f=0` is a strict-margin failure.

## Exact arithmetic obstruction

The available exact `epsilon` alone cannot decide strict positivity. Even
fixing `theta=1` and `rho_r=0`, two exact rational margin choices are both
compatible with every currently supplied perturbation fact:

```text
charge = 2*epsilon^2.

Case A: m_r = epsilon^2       => m_f = -epsilon^2 < 0.
Case B: m_r = 3*epsilon^2     => m_f =  epsilon^2 > 0.
```

Thus no strict leftover theorem follows from the current perturbation receipt.
Likewise, an unbound `rho_r` changes the charge by the exact term
`2*lambda*rho_r*epsilon`; an unbound candidate margin cannot be repaired by
repeating square-root arithmetic.

## Rejected candidates

The exact-Fourier Frobenius CSV exposes squared candidates such as
`4227/500000` and `34547/1000000`, plus unkeyed candidate `theta/charge/margin`
columns. They do not prove the actual weighted baseline statement for `R_r`,
do not carry this canonical source/state key, and cannot be passed as `rho_r`
or `m_r`. The previously constructed rational roots `9195/100000` and
`1859/10000` remain arithmetic witnesses only, not baseline receipts.

## Minimal receipt that would make R3 consumable

Under the exact key above, provide all of:

1. `rho_r >= 0` and a theorem/interval receipt proving
   `forall a_B, ||R_r a_B||_2 <= rho_r*sqrt(a_B^T*B_up*a_B)`; a squared bound
   must include an exact upper-root witness;
2. one fixed exact `theta > 0` and `lambda = 1+1/theta`;
3. an authoritative exact `m_r > 0` representing the baseline Schur margin
   after the baseline charge, in the same normalization and cell;
4. exact arithmetic proving
   `lambda*((rho_r+epsilon)^2-rho_r^2) < m_r`, with returned `m_f > 0`;
5. unchanged source/state/norm/orientation equality, and `R_port*a_B=r_B` if
   the result is to be called physical.

Until then the exact status is

```text
OPEN_FAIL_CLOSED:
same_key_weighted_baseline_rho_r_missing;
same_key_remaining_margin_m_r_missing;
same_key_theta_missing;
strict_positive_leftover_undetermined.
```

```text
main_state_modified = false
registry_promoted = false
schur_margin_consumed = false
```
