# Exact derivation and scope boundary

## Matrix and projection

The current exact Q used by the Route-B storage construction is

```text
Q = diag(3, 8, 95/7, 165/7, 45, 90),
Q[1,2] = Q[2,1] = -5.
```

For `u=e4+e5`, the off-diagonal block is disjoint from the selected
coordinates.  Its expanded quadratic form is

```text
q'Qq = 3 q0² + 8 q1² + (95/7)q2² + (165/7)q3²
       + 45 q4² + 90 q5² - 10 q1 q2.
```

The first three terms involving coordinates 1 and 2 are nonnegative after
the exact completion

```text
8 q1² - 10 q1 q2 + (95/7)q2²
 = 8(q1 - (5/8)q2)² + (585/56)q2².
```

Thus

```text
(165/7) q3² + 45 q4² <= q'Qq.
```

The selected two-dimensional Cauchy inequality has the exact rational slack

```text
(32/495)*((165/7)x² + 45y²) - (x+y)²
 = (11x - 21y)² / 231 >= 0.
```

Combining the two inequalities gives

```text
(eta3 + eta4)² <= (32/495) epsilon_Q²
```

whenever `eta'Qeta <= epsilon_Q²`.  With `epsilon_Q >= 0`, taking square
roots gives the exported absolute projection bound

```text
|eta3 + eta4| <= sqrt(32/495) epsilon_Q.
```

The witness `eta=(0,0,0,21s,11s,0)` attains equality, so the constant is
sharp for this Q and this direction.

## What this does not prove

The scalar in the existing supply leaf is `etaU = u dot eta_vec`.  This leaf
now supplies the exact physical projection interface, but it only supplies
an absolute bound proportional to `epsilon_Q`.  It does not imply

```text
|etaU| <= kappa rho
```

unless an additional source theorem proves equilibrium vanishing and a
state-relative error estimate, for example `epsilon_Q <= c*rho`, or directly
proves `|u dot eta_vec| <= kappa*rho`.  The absolute bound remains compatible
with a fixed nonzero eta at `rho=0`, so it does not by itself repair the
small-rho denominator obstruction.

## Verification scope

The Lean file is an exact real algebra theorem with the current Q payload.
It does not import Julia or Float64 semantics, prove the physical source
implementation, prove Q positive definite beyond the selected domination
identity, close the relative-eta frontier, prove uniform feasibility, or
promote anything to the verified theorem registry.
