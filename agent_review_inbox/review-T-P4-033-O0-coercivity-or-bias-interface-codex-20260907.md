# T-P4-033 O0 — same-key coercivity reserve and affine-bias interface

Date: 2026-09-07  
Scope: exact-Fourier one-cell mathematical core only. No old-ledger search,
unit-normalization arithmetic, Schur consumption, or registry mutation.

## Verdict

The exact-Fourier tuple supplies a conditional port gain, but no same-key
energy-side baseline coefficient from which a Schur reserve can be derived.
The missing object is an exact coercivity/budget theorem for the top-side
Schur quantity.

## Minimal same-key coercivity receipt

Retain the existing exact-Fourier source/state key, left-output orientation,
and `B_up` metric. Define

```text
A_up(q,a_B) = a_B^T * B_up(q) * a_B.
```

The smallest new source receipt must expose an exact rational `L_base` and
prove, on the same cell and key,

```text
baseline_budget(q,a_B) >= L_base * A_up(q,a_B).
```

Together with the existing conditional `rho_r` and fixed exact `theta > 0`,
put `lambda=1+1/theta` and define

```text
m_r = L_base - lambda*rho_r^2.
```

The strict R3 join is exactly

```text
m_r > 0
lambda*((rho_r+epsilon_R)^2-rho_r^2) < m_r
equivalently L_base > lambda*(rho_r+epsilon_R)^2
m_f = L_base - lambda*(rho_r+epsilon_R)^2 > 0.
```

This does not assume `L_base=1`.

## Exact obstruction from the actual tuple

The tuple fields are port-side bounds (`Br`, exact-real `K`, and `Cf`) and
therefore constrain `rho_r`; they do not state `baseline_budget`, `L_base`, or
any lower bound for the Schur top block.

Hold the entire tuple, metric, cell, `rho_r`, `epsilon_R`, and `theta` fixed.
Two exact completions are both compatible with those tuple facts:

```text
Completion A: L_base = lambda*(rho_r+epsilon_R)^2  => m_f = 0.
Completion B: L_base = lambda*(rho_r+epsilon_R)^2 + 1  => m_f = 1.
```

The tuple contains no premise distinguishing A from B. Hence no same-key
`m_r` or strict leftover follows from the tuple; assigning one by
normalization would be an extra theorem.

## Affine-bias replacement

If the source residual is affine,

```text
r_B = R_rel*a_B + b_B.
```

For exact `tau > 0`, assume

```text
||R_rel*a_B||_2^2 <= rho_rel^2*A_up
||b_B||_2^2 <= beta_bias*A_up
beta_bias >= 0.
```

Young gives

```text
||r_B||_2^2 <=
  ((1+tau)*rho_rel^2 + (1+1/tau)*beta_bias)*A_up.
```

Set `gamma_bias=(1+tau)*rho_rel^2+(1+1/tau)*beta_bias`. The R3-facing
receipt must provide an exact `rho_bias >= 0` with
`gamma_bias <= rho_bias^2`; then the strict condition is

```text
L_base > lambda*(rho_bias+epsilon_R)^2.
```

Without relative `beta_bias`, an exact absolute cap

```text
||b_B||_2^2 <= beta_abs
```

requires an independent additive reserve `m_add` satisfying

```text
m_add > (1+1/tau)*beta_abs.
```

If `m_add=0` and `beta_abs>0`, closure is impossible. A nonzero fixed bias
cannot be renamed `rho_r^2*A_up`: at `a_B=0`, `A_up=0` but
`||r_B||_2^2=||b_B||_2^2>0`.

## Exact next receipt contract

Accept one of: (i) same-key `L_base`/baseline-budget theorem with strict
`L_base > lambda*(rho_r+epsilon_R)^2`; (ii) same-key `beta_bias`, a root
witness for `gamma_bias`, and the same coercivity inequality; or (iii) same-key
`beta_abs` plus positive additive reserve `m_add` as above.

Until then:

```text
OPEN_FAIL_CLOSED:
same_key_baseline_coercivity_or_additive_reserve_missing.
```

```text
main_state_modified = false
schur_margin_consumed = false
registry_promoted = false
```
