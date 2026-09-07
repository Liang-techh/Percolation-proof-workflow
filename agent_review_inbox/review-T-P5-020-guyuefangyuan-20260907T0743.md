---
kind: review_result
review_id: review-T-P5-020-guyuefangyuan-20260907T0743
task_id: T-P5-020
source_agent: 古月方源
agent: 古月方源
claimed_at: 2026-09-07T07:32:00-06:00
created_at: 2026-09-07T07:43:00-06:00
inspected_commit: 06c1f2528e2146221f10596a69b92921ccaff9e4
continuation_of:
  - review-T-P5-018-guyuefangyuan-20260907T0634
  - review-T-P5-019-honglianmozun-20260907T0702
related_reviews:
  - review-T-P5-009-liuguanyi-20260907T0606
  - review-T-P5-019-liuguanyi-20260907T0730
  - review-T-P4-007-liuguanyi-20260907T0212
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_centered_small_gain_and_anchor_barrier_then_source_bind_a_same_domain_increment_or_jacobian_bound
---

# T-P5-020 — centered residual small-gain and nominal-anchor split for the block-(4,5) tube

## 0. Result in one sentence

The `T-P5-018` incremental hypocoercive tube and the `T-P5-019` direct residual metric admit a stronger two-lane residual architecture than a single absolute `L2` box: split the actual-minus-nominal residual into a **centered state increment** plus a **nominal-anchor bias**.  The centered branch is absorbed multiplicatively whenever its squared state gain `ell2` satisfies a rational small-gain inequality, while only the anchor branch is charged to the ultimate/invariant tube.  A source checker can certify the centered gain from a same-domain Jacobian/Frobenius bound for smooth exact-real components.

No Float64/source binding, P8 flowpipe coverage, ODE continuation, provenance/admission, P5/P8/M4 closure, or registry promotion is claimed.

---

## 1. Inputs already available from T-P5-018 / T-P5-019

Use the incremental block variables

```text
x = q_B - qbar_B,
y = v_B - vbar_B,
N = ||x||^2 + ||y||^2,
u = x + y.
```

For the exact-rational hypocoercive storage `V` and dissipation quadratic `Q`, the previous mathematical/Lean children provide

```text
V' = -Q - u^T r,                                      (1)
Q >= (457/800) N,                                     (2)
Q >= (457/672) V,                                     (3)
5 ||u||^2 <= 17 Q.                                    (4)
```

Equation (4) is the newly formalized direct residual metric from `T-P5-019`.

The point of this child is not to improve (4) further.  It changes how the physical residual `r` should be split before (4) is consumed.

---

## 2. Exact nominal-anchor decomposition

Let the actual generalized-force mismatch be a state-dependent map `l(t,z)`, where `z=(q_B,v_B)` for the block, and let the nominal model carry a possibly different residual map `n(t,zbar)`.  Then the actual-minus-nominal residual has the exact identity

```text
r(t)
 = l(t,z) - n(t,zbar)
 = [l(t,z) - l(t,zbar)] + [l(t,zbar) - n(t,zbar)].     (5)
```

Define

```text
r_c := l(t,z) - l(t,zbar),                            (centered branch)
b   := l(t,zbar) - n(t,zbar).                         (anchor branch)
```

Then simply

```text
r = r_c + b.                                          (6)
```

This decomposition is algebraically exact and has two useful boundary cases:

1. If the nominal dynamics uses the same residual map as the actual dynamics at the nominal state, then `b=0`; only a centered increment remains.
2. If the nominal dynamics is the exact-real ideal model with `n=0`, then `b=l(t,zbar)`; only the residual **along the nominal flowpipe** must be paid as an additive anchor, while state variation away from the nominal path can be absorbed by a Lipschitz small-gain argument.

A state-independent bias inside `l` cancels from `r_c` but, for an ideal nominal model, remains once in `b`.  Thus this split does not magically erase a real implementation bias; it prevents paying the same state-varying residual as a full absolute box over the entire actual tube.

---

## 3. Centered residual small-gain theorem

Assume on one common first-exit domain that

```text
||r_c||^2 <= ell2 * N,                                (7)
ell2 >= 0.                                             (8)
```

By (2),

```text
N <= (800/457) Q,
```

hence

```text
||r_c||^2 <= (800/457) ell2 Q.                        (9)
```

By Cauchy and the direct metric (4),

```text
|u^T r_c|^2
 <= ||u||^2 ||r_c||^2
 <= (17/5) Q * (800/457) ell2 Q
 = (2720/457) ell2 Q^2.                               (10)
```

Now choose any rational checker parameter `mu` satisfying

```text
0 <= mu < 1,                                          (11)
2720 * ell2 <= 457 * mu^2.                            (12)
```

Because `Q>=0`, (10)-(12) imply

```text
|u^T r_c| <= mu Q.                                    (13)
```

This is the key small-gain bridge.  It has no square root in the trusted/checker-facing premise.

### Pure centered case

If `b=0`, then from (1), (6), and (13),

```text
V' <= -(1-mu) Q
   <= -(457/672)(1-mu) V.                             (14)
```

Thus a true centered state-increment residual below the threshold gives **strict exponential contraction with no ultimate additive floor**.

The information-theoretic threshold exposed by this route is

```text
2720 * ell2 < 457.                                    (15)
```

For exact rational certification one need not introduce `sqrt(2720*ell2/457)`; the checker can search for any rational `mu<1` satisfying (12).  A convenient fixed corollary is `mu=1/2`:

```text
10880 * ell2 <= 457                                   (16)
```

which yields

```text
V' <= -(457/1344) V.                                  (17)
```

The adaptive rational `mu` route is recommended because it retains more decay when the centered gain is small.

---

## 4. Mixed centered + anchor first-exit barrier

Assume in addition a same-domain anchor bound

```text
||b||^2 <= B2,                                        (18)
B2 >= 0.                                               (19)
```

At a candidate boundary `V=Vstar`, combine (13) with (1):

```text
V'
 <= -Q + |u^T r_c| + |u^T b|
 <= -(1-mu) Q + |u^T b|.                              (20)
```

By Cauchy and (4),

```text
|u^T b|^2 <= (17/5) Q B2.                             (21)
```

Since (3) gives `Q >= (457/672)Vstar`, a sufficient condition for

```text
|u^T b| < (1-mu) Q
```

is

```text
(17/5) B2 < (1-mu)^2 * (457/672) Vstar.               (22)
```

Clearing denominators gives the particularly clean checker-facing barrier

```text
2285 * (1-mu)^2 * Vstar > 11424 * B2.                 (23)
```

Under (11)-(12) and (23), every point on `V=Vstar` has

```text
V' < 0.                                                (24)
```

This is stronger for first-exit purposes than first converting everything to one absolute `L2` budget.  The centered state-dependent part consumes a dimensionless fraction `mu` of the dissipation; only the nominal-anchor residual enters the additive barrier.

### Existing common physical margin

`T-P5-018` gives the common position/velocity margin choice

```text
Vstar = (117/4880) sigma^2.                            (25)
```

Substitution into (23) reduces exactly to

```text
17823 * (1-mu)^2 * sigma^2 > 3716608 * B2.             (26)
```

For the quarter barrier `Vstar=1/4`, (23) becomes

```text
2285 * (1-mu)^2 > 45696 * B2.                         (27)
```

When `mu=0`, (23), (26), and (27) reduce to the direct-metric additive barriers already exposed by `T-P5-019`; the new theorem is therefore a strict extension rather than a competing constant ledger.

---

## 5. Optional ISS ledger for the mixed case

For a time-uniform anchor bound, one can also retain a standard differential ISS inequality.  Let `g=1-mu>0`.  From (21) and Young with reserve `g`,

```text
|u^T b| <= (g/2) Q + (17/(10 g)) B2.                  (28)
```

Then

```text
V' <= -(g/2) Q + (17/(10 g)) B2
   <= -(457 g/1344) V + (17/(10 g)) B2.               (29)
```

The asymptotic gain is

```text
11424 / (2285 g^2),                                   (30)
```

so its invariant-boundary condition is exactly (23).  For first-exit certification, however, the square comparison in Section 4 is cleaner because it avoids division by `g` entirely.

---

## 6. Source-facing Jacobian / Frobenius sufficient condition

The centered premise (7) can be produced from a genuine same-domain increment theorem rather than from an absolute affine envelope.

Consider a time-dependent but state-smooth residual component

```text
E(t,z) : R^4 -> R^2,
z=(x4,x5,y4,y5),
```

and assume that for fixed `t` the segment joining `zbar` and `z` remains in a convex certified domain.  Suppose uniform derivative bounds hold on that segment/domain:

```text
|partial_j E_i(t,zeta)| <= J_ij,                      (31)
J_ij >= 0,
```

for `i=1,2`, `j=1,...,4`.  Define the squared Frobenius bound

```text
JF2 := sum_{i=1}^2 sum_{j=1}^4 J_ij^2.                (32)
```

Applying the one-dimensional fundamental theorem of calculus along the segment and Cauchy row by row gives

```text
||E(t,z)-E(t,zbar)||^2 <= JF2 * ||z-zbar||^2.         (33)
```

Thus (7) holds with

```text
ell2 = JF2.                                            (34)
```

A direct checker target is therefore

```text
2720 * JF2 <= 457 * mu^2,
0 <= mu < 1.                                          (35)
```

This is intentionally Frobenius-based rather than spectral-norm-based: it is conservative but requires only eight scalar derivative intervals, finite sums, squares, and rational arithmetic.  If a tighter certified operator norm is available, it can replace `JF2` without changing the downstream theorem.

### Important Float64 boundary

The Jacobian route is naturally suited to smooth exact-real DH/analytic/FD model components.  A raw IEEE-754 execution map can have rounding discontinuities, so a derivative bound for the underlying real formula does **not** by itself certify (33) for the Float64 lift.  Float64/solve/controller remainders must either:

- receive an independent centered-increment theorem that accounts for rounding; or
- remain in the additive anchor/box branch `B2`.

This is exactly compatible with the semantic decomposition in `T-P4-007`: smooth exact-real state variation can be routed to the centered branch, while `DeltaM/DeltaC/DeltaG/delta_ctrl/solve_defect` are kept separate until a source theorem decides whether each has a centered gain or only an additive box.

---

## 7. Why the current affine FD envelope alone is insufficient

`T-P5-019` (柳冠一) correctly shows that an absolute affine envelope

```text
|E_i(z)| <= s_i * cap(z) + b_i
```

is enough for the **additive** tube consumer.  It does not imply the centered increment bound

```text
|E_i(z)-E_i(zbar)| <= L_i ||z-zbar||.                 (36)
```

In particular, the positive offset `b_i` cannot simply be cancelled algebraically unless the source theorem proves that it is a common state-independent contribution to the actual error map.  `T-P5-009` already supplied the generic obstruction to deriving homogeneous gain from a positive-offset absolute envelope.

Therefore this child does not replace the `T-P5-019` absolute-box adapter.  It gives a second, potentially much tighter route **if** the source/checker can prove a true centered increment or Jacobian contract.

---

## 8. Why this can materially tighten the P8 tube

The current absolute-box route pays the worst-case residual over the entire actual first-exit domain:

```text
||r||^2 <= L2_abs.
```

The anchor split instead pays

```text
state variation  -> dimensionless small-gain mu,
nominal-path bias -> B2.                              (37)
```

If the residual map varies smoothly but has a nonzero offset, `B2` can be evaluated only on the nominal flowpipe, while the off-nominal variation is absorbed by (12).  This can be much smaller than a single absolute box over the full tube and is structurally aligned with the `nominal flowpipe + residual tube` architecture of `T-P5-018`.

It also creates a useful source-checker priority order:

```text
1. Try to certify a centered increment/Jacobian gain for each smooth residual component.
2. Route components satisfying (35) into the small-gain branch.
3. Evaluate the remaining additive component only on the nominal tube and combine it into B2.
4. Check (23) or (26) for the final first-exit barrier.
```

No step permits an absolute positive-offset envelope to be silently reclassified as a centered gain.

---

## 9. Lean-friendly theorem decomposition

The algebraic core needs no matrix library if it consumes the existing `T-P5-019` metric and `T-P5-018` coercivity facts.

Recommended atomic statements:

```lean
-- Exact algebraic anchor split.
theorem residual_anchor_split
    (lAct lAnchor lNom : R2) :
    lAct - lNom = (lAct - lAnchor) + (lAnchor - lNom) := ...

-- Cauchy + direct metric + state-to-Q conversion.
theorem centered_power_sq_bound
    (zc Q N Rc2 ell2 : ℝ)
    (hQ : 0 <= Q)
    (hQN : (457/800 : ℝ) * N <= Q)
    (hRc : Rc2 <= ell2*N)
    (hz : zc^2 <= (17/5 : ℝ)*Q*Rc2) :
    457*zc^2 <= 2720*ell2*Q^2 := ...

-- Rational small-gain absorption, no sqrt.
theorem centered_absorb_of_mu
    (zc Q ell2 mu : ℝ)
    (hQ : 0 <= Q) (hmu : 0 <= mu)
    (hz : 457*zc^2 <= 2720*ell2*Q^2)
    (hgain : 2720*ell2 <= 457*mu^2) :
    |zc| <= mu*Q := ...

-- Pure contraction.
theorem centered_residual_contraction
    ...
    (hmu1 : mu < 1)
    (hQV : (457/672 : ℝ)*V <= Q) :
    Vdot <= -(457/672 : ℝ)*(1-mu)*V := ...

-- Division-free mixed first-exit barrier.
theorem centered_anchor_barrier_inward
    ...
    (hmu1 : mu < 1)
    (hQV : (457/672 : ℝ)*Vstar <= Q)
    (hAnchorSq : zb^2 <= (17/5 : ℝ)*Q*B2)
    (hbar : 11424*B2 < 2285*(1-mu)^2*Vstar) :
    Vdot < 0 := ...

-- Existing common-margin specialization.
theorem centered_anchor_common_margin
    ...
    (hbar : 3716608*B2 < 17823*(1-mu)^2*sigma^2) :
    Vdot < 0 := ...
```

The Jacobian-to-Frobenius step is better left as a separate calculus/adapter theorem because it needs a path/FToC interface; the pointwise small-gain algebra above can be formalized immediately and independently.

---

## 10. Precise remaining obligations

This result leaves the following genuinely open:

1. **Centered source binding:** prove (7) for one or more actual residual components on the same P8 first-exit domain.  Current absolute FD envelopes do not suffice.
2. **Float64 semantics:** decide which runtime/solve terms admit a centered increment theorem and which must remain additive.
3. **Nominal-anchor bound:** certify `B2` along the nominal flowpipe for the chosen nominal residual convention.
4. **Convex-domain/path condition:** a Jacobian proof needs the actual-nominal segment to remain in the domain where derivative intervals are valid.
5. **P8 nominal flowpipe and margins:** `sigma` and same-domain coverage remain external premises.
6. **ODE first-exit calculus:** the pointwise inward theorem still needs the standard continuation/first-exit wrapper.
7. **No parent closure:** P5/P8/M4 and registry admission remain unchanged.

## 11. Recommended next seam

The highest-value source-side experiment is now very specific: on the block-(4,5) first-exit box, compute interval bounds for the state Jacobian of the **smooth exact-real part** of the residual and form the eight-term rational `JF2`.  If a rational `mu<1` satisfies

```text
2720 JF2 <= 457 mu^2,
```

route that smooth part to the centered branch.  Keep Float64/solve/controller pieces in the additive anchor branch until separately certified, and then test the final division-free barrier

```text
17823 (1-mu)^2 sigma^2 > 3716608 B2.
```

This is the smallest source-to-math target that can turn the current residual tube from a pure absolute-ISS enclosure into a genuine contraction-plus-anchor certificate.
