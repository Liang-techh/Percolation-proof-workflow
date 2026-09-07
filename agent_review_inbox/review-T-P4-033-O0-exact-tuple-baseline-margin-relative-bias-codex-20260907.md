# T-P4-033 O0 — exact-Fourier tuple baseline construction and margin boundary

Date: 2026-09-07  
Scope: mathematical core only; exact-Fourier one-cell key, no old-ledger
search, no Schur consumption, no registry admission.

## Constructive result

The real exact-Fourier tuple can produce a conditional weighted baseline gain.
Let

```text
R_r(q) = -M_BD(q) * M_DD(mu_exact,q)^(-1) * DeltaM_DB(q)
```

under the explicit same-key port-map identity and the zero off-diagonal
regularizer-shift premise. The tuple supplies, in one induced-infinity norm,

```text
||M_BD||_infinity <= Br
||M_DD(mu_exact)^(-1)||_infinity <= K
||DeltaM_DB||_infinity <= Cf.
```

Submultiplicativity therefore gives the exact unweighted baseline bound

```text
U_r = Br*K*Cf
  = 307877874565159207113609223771373 /
    88466548932015686688434020800000000.
```

Using the already compiled Fin-2 output factor and the same metric root
`s=1/5`, the conditional weighted Euclidean baseline witness is

```text
rho_r = 2*U_r/s = 10*U_r
  = 307877874565159207113609223771373 /
    8846654893201568668843402080000000.
```

The exact theorem interface required for this construction is

```text
forall a_B,
  ||R_r(q) a_B||_2 <= rho_r * sqrt(a_B^T*B_up*a_B)
```

for every q in the declared exact-Fourier cell. This is still conditional on
the typed definition of `R_r`, the exact-real authority of `K`, and the
same-key induced-infinity submultiplicativity chain.

## Conditional exact theta/margin calculation

Choose the exact rational value

```text
theta = 1,
lambda = 1 + 1/theta = 2.
```

If, in addition, a same-key normalized baseline budget of exactly `1` is
proved, with no other uncharged term, then the baseline remaining margin would
be the exact rational candidate

```text
m_r^unit = 1 - 2*rho_r^2
 = 39036862614056869268384562327979703376965752490585807296058625694871 /
   39131651399703629175019294625928027986209692974274163200000000000000
 > 0.
```

For the already accepted same-key perturbation `epsilon_R`, the strict post-
charge leftover under this additional unit-budget premise is

```text
m_f^unit = 1 - 2*(rho_r + epsilon_R)^2
 = 44803170958565974244104611264818695759805381025392128881467231870512947837498295972583918816113 /
   44911961416709949048557505500291830721283968962590630715724431652772514650274717400445556640625
 > 0.
```

Equivalently, the exact strict inequality is

```text
m_r^unit > 2*((rho_r + epsilon_R)^2 - rho_r^2)
```

and it holds for these displayed rationals. This calculation is a conditional
mathematical branch, not an admitted receipt: the exact-Fourier tuple contains
no proof that the normalized baseline budget is `1`, nor any same-key
`m_r` field representing the actual physical Schur reserve.

## Minimal obstruction to a consumable m_r

The tuple has matrix/resolvent/coupling bounds but no energy-side premise of
the form

```text
baseline_budget >= L_base * A_up,
L_base - lambda*rho_r^2 = m_r,
m_r > 0.
```

Without `L_base` (or a direct authoritative `m_r`), the expression
`1-2*rho_r^2` is an invented normalization and cannot be passed to the strict
R3 API. The missing receipt must also bind the port map to the physical
residual if the result is intended to be physical:

```text
R_port*a_B = r_B.
```

Therefore the strongest current status is

```text
CONDITIONAL_RHO_R_AND_THETA_CONSTRUCTED;
STRICT_M_R_NOT_CONSUMABLE;
OBSTRUCTION_MISSING_BASELINE_COERCIVITY_OR_EXACT_MARGIN.
```

## Relative-residual / explicit-bias fallback

If the source can prove only an affine residual decomposition

```text
r_B = R_r*a_B + b_r,
```

then a homogeneous `rho_r` interface is false whenever `b_r != 0` and
`a_B=0`, because its right side is zero. The exact replacement is, for every
`tau > 0`,

```text
||r_B||_2^2
 <= (1+tau)*rho_rel^2*A_up
    + (1+1/tau)*||b_r||_2^2,
```

from `||R_r*a_B||_2^2 <= rho_rel^2*A_up`. To absorb the bias into the same
homogeneous metric, a separate exact same-key premise is required:

```text
||b_r||_2^2 <= beta_bias*A_up,
```

which yields the effective squared gain

```text
rho_eff^2 = (1+tau)*rho_rel^2 + (1+1/tau)*beta_bias.
```

Otherwise `||b_r||_2^2` must remain an explicit additive budget and cannot be
renamed `rho_r^2*A_up`. This is the minimal relative-residual/bias rewrite;
it does not manufacture a Schur margin.

## Required next exact receipt

To turn the conditional construction into a consumable strict child, provide
under the exact-Fourier source/state/metric/orientation key:

1. the typed `R_r` identity and exact-real `K` authority;
2. either an exact normalized `L_base`/coercivity theorem or direct exact
   `m_r > 0` after baseline charge;
3. exact `theta > 0` and
   `m_r > (1+1/theta)*((rho_r+epsilon_R)^2-rho_r^2)`;
4. if the physical residual is affine, the exact `b_r` or relative bias cap
   above, plus the physical map identity.

No old Float64 ledger, `rho_F^2`, or unkeyed candidate margin is used here.

```text
main_state_modified = false
registry_promoted = false
schur_margin_consumed = false
```
