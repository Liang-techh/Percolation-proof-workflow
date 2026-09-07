---
kind: review_result
review_id: review-T-P5-011-honglianmozun-20260907T0155
task_id: T-P5-011
source_agent: 红莲魔尊
claimed_at: 2026-09-07T01:46:00-06:00
created_at: 2026-09-07T01:55:00-06:00
inspected_commit: eb4a9b9bad03a0c6c8e00b79fef20e2d5862c950
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_squared_cubic_energy_barrier_and_generate_single_fourier_scalar_SF
---

# T-P5-011 — Lyapunov self-bootstrap for the central-FD cubic lane

## Scope

This pass composes the strongest currently available P5/P3 mathematics rather
than asking P8 for an independent velocity box:

1. `T-P5-008` supplies the storage-renormalized energy ledger in which the
   `1e-6 I` mass regularizer belongs to kinetic storage and the frozen-potential
   gravity FD term is conservative rather than an additive force bias.
2. `T-P3-008` supplies the exact-real central-FD tensor remainder
   `|R[k,i,j]| <= mu[k,i,j]`, with a global rational Fourier formula
   `mu = h^2 c/6`, `h=1/100000`.
3. `T-P5-010` supplies the squared cubic-power estimate
   `P_C^2 <= Lambda A^3`, where `A` is the diagonal damping quadratic.

The new question is:

> Can the modified Lyapunov storage itself provide the local velocity/energy
> radius needed to absorb the cubic C-FD term, so that a separate P8 velocity
> box is not logically necessary for this one lane?

Yes. A regularizer-based kinetic coercivity estimate plus a square-only barrier
argument gives a self-consistent forward-invariant energy sublevel. The
resulting source-facing exact-real interface can be compressed further to one
rational Fourier scalar instead of 216 separate `mu[k,i,j]` values.

This review does not prove the true-DH/Fourier semantic binding, Float64
rounding bounds, ODE existence/coverage, controller/solve bias closure, or any
admission/provenance claim.

## Inputs inspected

- `review-T-P5-008-honglianmozun-20260906T2348.md` — modified storage and
  reduced P5 ledger;
- `review-T-P5-010-youhunmozun-20260907T0026.md` — cubic-power squared
  certificate and local small-gain obstruction;
- `review-T-P3-008-guyuefangyuan-20260907T0141.md` — exact source index map,
  central-FD tensor remainder, and Fourier `O(h^2)` bound;
- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_analytic_fourier_dynamics_probe.py`
  — exact definition of `derivative_error` with `FD_H=1/100000`;
- `examples/routeb_supply_core/RouteBSupplyCore.lean` as quoted by P5-010 —
  damping coefficients
  `[13/10, 11/10, 19/20, 4/5, 13/20, 1/2]`.

## 1. Damping quadratic and modified energy

Let

```text
A(v) := sum_i d_i v_i^2,
```

with the current exact damping coefficients. Their maximum is

```text
d_max = 13/10.                                               (1)
```

Write the storage from `T-P5-008` abstractly as

```text
V_tilde = T_eps(v,q) + W(q,w),                               (2)
```

where

```text
T_eps = 1/2 v^T (Mhat(q)+eps I) v,
eps = 1/1000000,
```

and `W` includes the storage-renormalized potential/controller terms.

The exact-real DH mass `Mhat` is PSD because it is a sum of Jacobian Gram
terms. Therefore

```text
T_eps >= eps/2 * ||v||^2.                                   (3)
```

Suppose on the declared proof domain we have any lower bound

```text
W(q,w) >= W_min.                                             (4)
```

Shift the storage by a constant:

```text
Z := V_tilde - W_min.                                        (5)
```

The derivative is unchanged, while `(3)`--`(4)` imply

```text
Z >= T_eps >= eps/2 ||v||^2.                                (6)
```

Since `A <= d_max ||v||^2`,

```text
A(v) <= K Z,
K := 2 d_max / eps.                                          (7)
```

With the current exact constants,

```text
K = 2*(13/10)/(1/1000000) = 2600000.                        (8)
```

Thus even the bare `1e-6` regularizer gives a global exact-real
velocity-to-storage coercivity theorem. It is conservative, but it is enough to
close a bootstrap if the FD cubic constant is sufficiently small.

Important: no claim is made here that the current non-kinetic storage has
already been source-bound to a proved `W_min`. A constant shift is harmless to
`V_dot`, so a future domain-specific lower bound is all that is needed; the
potential/controller part need not literally be nonnegative as written.

## 2. Square-only cubic absorption from an energy barrier

Take the squared C-FD power estimate from `T-P5-010`:

```text
P_C^2 <= Lambda A^3,
Lambda >= 0.                                                 (9)
```

Let `g>=0` denote the damping margin remaining after every already-relative
power term has been charged. For example, if

```text
P_rel <= kappa_R A,
0 <= kappa_R < 1,
```

then

```text
g := 1-kappa_R > 0.                                         (10)
```

Assume at one state

```text
A >= 0,
Z >= 0,
A <= K Z,
Lambda K Z <= g^2.                                          (11)
```

Then

```text
P_C^2
 <= Lambda A^3
 =  (Lambda A) A^2
 <= (Lambda K Z) A^2
 <= g^2 A^2.                                                 (12)
```

Because both `|P_C|` and `g A` are nonnegative, comparison of squares yields

```text
|P_C| <= g A.                                                (13)
```

No square root and no division are needed. This is the minimal algebraic
consumer that the formalization lane should implement first.

There is also a strict version. If

```text
Lambda K Z < g^2,
A > 0,
```

then

```text
|P_C| < g A.                                                 (14)
```

Hence the cubic mismatch is strictly dominated by the remaining damping at
every nonzero velocity inside the strict energy barrier.

## 3. Lyapunov derivative closure

After the storage renormalization of `T-P5-008`, suppose the remaining ledger
has the form

```text
Z_dot
 <= -A + P_C + P_rel + P_bias,                               (15)
```

with

```text
P_rel <= kappa_R A,
P_bias <= 0,
0 <= kappa_R < 1.                                            (16)
```

Set `g=1-kappa_R`. Under the barrier `(11)`, `(13)` gives

```text
Z_dot
 <= -g A + P_C
 <= -g A + |P_C|
 <= 0.                                                       (17)
```

Under the strict barrier and `A>0`, equation `(14)` gives

```text
Z_dot < 0.                                                   (18)
```

Thus the central-FD cubic term does not need an externally declared velocity
box if the current Lyapunov sublevel itself implies `(11)`.

## 4. First-exit / self-bootstrap theorem

Fix an energy cap `Z_star>=0` satisfying

```text
Lambda K Z_star <= g^2.                                     (19)
```

Assume along a differentiable trajectory that the source/ledger hypotheses
needed for `(15)`--`(16)`, the coercivity `A<=KZ`, and the cubic estimate `(9)`
hold whenever `Z<=Z_star`. If

```text
Z(0) <= Z_star,                                              (20)
```

then the sublevel

```text
Z(t) <= Z_star                                               (21)
```

is forward invariant for as long as the trajectory remains in the other
source/domain hypotheses.

Proof: on the whole sublevel `Z<=Z_star`, `(19)` implies `(11)`, so `(17)`
gives `Z_dot<=0`. A first exit through `Z=Z_star` would require the storage to
increase from a value at most `Z_star`, contradicting the one-sided
nonincrease on the sublevel. Equivalently, apply the mean-value theorem on the
first crossing interval.

If `(19)` and `(20)` are strict, then `Z(t)<Z_star` is retained and `(18)` gives
strict dissipation whenever `A(t)>0`.

This is the missing bootstrap composition between the local cubic theorem and a
Lyapunov proof: the radius is generated by the same storage whose derivative is
being controlled.

## 5. One scalar Fourier certificate is enough for this P5 route

`T-P3-008` gives for each derivative tensor entry

```text
mu[k,i,j] = h^2/6 * c[k,i,j],                                (22)
```

where

```text
c[k,i,j]
 := sum_nu (|Re a_ij,nu|+|Im a_ij,nu|) |nu_k|^3             (23)
```

is a nonnegative rational number computed from the frozen exact mass Fourier
CSV.

`T-P5-010` defines

```text
Lambda
 := 1/4 * sum_{k,i,j} mu[k,i,j]^2/(d_k d_i d_j).             (24)
```

Substituting `(22)` gives the exact compression

```text
Lambda = h^4/144 * S_F,                                      (25)
```

with the single rational Fourier scalar

```text
S_F
 := sum_{k,i,j} c[k,i,j]^2/(d_k d_i d_j).                    (26)
```

Therefore P5 does **not** need 216 separate rational `mu` values once the
power-level route is chosen. A source/checker artifact may generate the 216
values for diagnostics, but the theorem consumer can ingest just `S_F` plus a
proof/check that it was computed from the bound tensor.

For the deployed nominal step

```text
h = 1/100000,
h^4 = 1/10^20.                                               (27)
```

Combining `(8)` and `(25)` gives the exact rational identity

```text
Lambda K
 = [13 / 72000000000000000] * S_F.                           (28)
```

Hence the energy-barrier condition `(19)` can be written in a completely
square-root-free, division-free form:

```text
13 * S_F * Z_star
 <= 72000000000000000 * g^2.                                 (29)
```

This is a particularly useful interface for Lean/exact arithmetic. It converts
all exact-real Fourier FD mathematics needed by this P5 bootstrap into one
nonnegative rational scalar `S_F`.

The `h^4` factor also explains why the conservative regularizer-only
`K=2600000` does not automatically make this route useless: `Lambda K` carries
an exact prefactor of about `1.80556e-16` times `S_F`. A concrete margin still
requires computing `S_F`; no numerical closure is claimed before that value is
source-bound.

## 6. Robust extension for an additional cubic execution remainder

`T-P3-008` correctly keeps the Julia Float64 gap separate. If a future IEEE
lane proves another cubic-power bound

```text
P_ieee^2 <= Lambda_ieee A^3,                                 (30)
```

then one may combine it with the analytic FD cubic without square roots using

```text
(P_C + P_ieee)^2
 <= 2 P_C^2 + 2 P_ieee^2
 <= 2 (Lambda + Lambda_ieee) A^3.                            (31)
```

Thus the same barrier theorem applies after replacing

```text
Lambda -> 2 (Lambda + Lambda_ieee).                          (32)
```

This is not claimed for the current runtime yet; it is the correct theorem
shape if the operation-level remainder is eventually shown to vanish cubically
with velocity. If the runtime produces a genuine additive power bias instead,
it must stay in the ultimate-bound/bias lane and cannot be hidden in `(32)`.

## 7. Failure boundaries

This pass rules out several unnecessary or invalid requirements:

1. **A separate P8 velocity box is not mathematically necessary for the C-FD
   cubic lane** if a storage lower bound `W>=W_min` and initial energy cap close
   `(19)`--`(20)`. P8 is still needed for the other state/domain and source
   coverage obligations.
2. **The 216 `mu[k,i,j]` values are not all needed by the final P5 theorem.**
   The exact-real energy consumer can use the one rational aggregate `S_F`.
3. **A positive additive bias cannot be repaired by this bootstrap.** If
   `P_bias>0` can remain at `A=0`, then `(17)` fails at zero velocity and P5
   reverts to the P5-004 ultimate-bound architecture unless that bias is
   separately eliminated or made state-relative.
4. **No damping margin means no cubic barrier.** If `kappa_R>=1`, then `g<=0`
   and the present strict-decay route is unavailable regardless of how small
   `Lambda` is.
5. **Exact-real PSD/coercivity is not Float64 admission.** Equation `(7)` uses
   the exact mechanical PSD structure plus the exact `eps I` regularizer; the
   deployed execution still needs its semantic/rounding bridge.

## 8. Lean-friendly theorem package

The highest-value first sidecar is purely algebraic:

```lean
theorem cubic_square_absorption_from_energy_barrier
    (A Z PC Lambda K g : Real)
    (hA : 0 <= A) (hZ : 0 <= Z)
    (hLambda : 0 <= Lambda) (hK : 0 <= K) (hg : 0 <= g)
    (hcoerce : A <= K*Z)
    (hcubic : PC^2 <= Lambda*A^3)
    (hbarrier : Lambda*K*Z <= g^2) :
    |PC| <= g*A
```

and the strict version

```lean
theorem cubic_square_strict_absorption_from_energy_barrier
    ...
    (hApos : 0 < A)
    (hbarrier : Lambda*K*Z < g^2) :
    |PC| < g*A
```

Then a scalar ledger consumer:

```lean
theorem cubic_energy_barrier_dissipation
    (A Zdot PC PR PB Lambda K kappaR : Real)
    ...
    (hledger : Zdot <= -A + PC + PR + PB)
    (hrel : PR <= kappaR*A)
    (hbias : PB <= 0)
    (hgain : 0 <= kappaR ∧ kappaR < 1)
    (hcoerce : A <= K*Z)
    (hcubic : PC^2 <= Lambda*A^3)
    (hbarrier : Lambda*K*Z <= (1-kappaR)^2) :
    Zdot <= 0
```

The exact constant specialization should be separate:

```text
K = 2600000,
Lambda = S_F/(144*10^20),
Lambda*K = 13*S_F/72000000000000000.
```

A later calculus child may formalize first-exit invariance; it should not be
mixed with the source-independent square algebra.

## What remains open

- Compute and freeze the exact rational scalar `S_F` from the current Fourier
  mass payload, or equivalently generate the `mu` tensor and reduce it to
  `(26)`.
- Bind the frozen Fourier mass function to the exact-real DH mass on the needed
  source domain (`B45-1` / semantic source lane).
- Bound the Float64 `dM/cijk/36-term` execution gap and classify it as cubic,
  relative, or genuine bias.
- Establish a lower bound `W_min` for the modified non-kinetic storage on the
  intended P8/first-exit domain and record the initial shifted energy `Z(0)`.
- Close controller/solve residuals sufficiently to obtain a genuine
  `kappa_R<1` and `P_bias<=0` (or move remaining positive bias to the
  ultimate-bound branch).
- ODE existence, P8 state/domain coverage, source semantics, validation,
  admission, and final M4 integration remain independent.

## Recommended next action

1. Exact source/checker lane: generate the one rational scalar `S_F` from the
   current frozen mass CSV using `(23)` and `(26)`. This is smaller than asking
   P5 to carry 216 tensor constants.
2. Formalization lane: implement the square-only theorem `(11)`--`(13)` and the
   exact arithmetic reduction `(28)`--`(29)` as a tiny portable sidecar.
3. Energy/source lane: obtain `W_min` on the same first-exit domain and evaluate
   whether the initial shifted storage satisfies `(29)` after the remaining
   relative gain `g` is fixed.
4. Keep any Float64 execution remainder and any positive controller/solve bias
   explicit; do not use the exact-real `h^4` barrier to hide them.

This result remains `pending`. It is a mathematical Lyapunov composition
lemma, not P5/P8/M4 closure.
