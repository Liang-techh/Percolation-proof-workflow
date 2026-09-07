---
kind: review_result
review_id: review-T-P5-018-guyuefangyuan-20260907T0634
task_id: T-P5-018
source_agent: 古月方源
claimed_at: 2026-09-07T06:24:00-06:00
created_at: 2026-09-07T06:34:00-06:00
inspected_commit: 0de32f05818c7f2e283e021375b9c2e9bfe5b860
continuation_of:
  - review-T-P5-016-guyuefangyuan-20260907T0538
  - review-T-P5-017-honglianmozun-20260907T0558
related_reviews:
  - review-T-P5-009-liuguanyi-20260907T0606
  - review-T-P4-019-kuangmanmozun-20260907T0550
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_incremental_block45_hypocoercive_tube_and_use_it_as_a_nominal_flowpipe_plus_residual_domain_bootstrap_interface
---

# T-P5-018 — incremental hypocoercive tube: cancel any common ramp/forcing, start with zero tracking energy, and bootstrap source-domain margin

## 0. Result in one sentence

The affine particular-solution shift of `T-P5-017` is not needed if P8 can provide **any nominal trajectory driven by the same input**: subtracting actual and nominal block-(4,5) equations cancels the entire common forcing identically, for arbitrary time dependence, and the `T-P5-016` hypocoercive storage becomes a residual-only incremental Lyapunov tube with zero initial energy when the two trajectories start together.

This gives a new P5/P8 seam:

```text
nominal flowpipe with physical-domain margin
+ same-domain bound on actual-minus-nominal generalized-force residual
+ incremental hypocoercive tube
=> actual block stays inside the physical domain.
```

No source binding, provenance, Float64 equality, ODE existence, registry admission, or P5/P8/M4 closure is claimed here.

## 1. Common forcing cancels without an affine-ramp assumption

Use the exactized constant reference block already isolated in `T-P5-016`:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
B = [[3/4,   -1/100],
     [-1/200, 29/50]].
```

Let an actual trajectory and a nominal trajectory satisfy, pointwise on the same time interval,

```text
M q''    + D q'    + B q    = f(t) - l(t),              (1)
M qbar'' + D qbar' + B qbar = f(t) - lbar(t),           (2)
```

where `f(t)` is **the same forcing in both equations**. It can be `g w(t)` as in the Route-B block, but nothing below requires `w'=c`, `c'=0`, affine time dependence, or even invertibility of `B`.

Define

```text
x := q-qbar,
y := q'-qbar',
r := l-lbar.                                             (3)
```

Subtracting (2) from (1) gives the exact incremental dynamics

```text
x' = y,
M y' + D y + B x = -r.                                  (4)
```

This is the key structural fact. Every common input disappears before any inequality is used.

### Route-B specialization

For the deployed-force ledger one normally takes

```text
f(t) = g w(t),
g = (1/5,1/10)^T.
```

If the nominal reference is ideal (`lbar=0`), then `r=l`, so the incremental system consumes only the true generalized-force residual. If a future nominal model has its own certified remainder, the theorem consumes only the mismatch `l-lbar`.

This is stronger than the static affine shift of `T-P5-017` in one important direction: **common-forcing cancellation holds for arbitrary `w(t)` and does not require `c'=0`.** The affine shift remains useful when one wants a closed-form nominal path without separately propagating a nominal ODE.

## 2. Reuse the symmetric/skew decomposition

As in `T-P5-016`, write

```text
B = K - A,

K = [[3/4,-3/400],[-3/400,29/50]],
A = [[0,1/400],[-1/400,0]],                              (5)
```

with `K` symmetric and `A` skew-symmetric. Then (4) is

```text
M y' + D y + K x = A x - r.                             (6)
```

Define the incremental hypocoercive storage

```text
Vd(x,y)
 := 1/2 y^T M y
  + 1/2 x^T K x
  + x^T M y
  + 1/2 x^T D x.                                        (7)
```

The exact completion is

```text
Vd
 = 1/2 (y+x)^T M (y+x)
   + 1/2 x^T H x,
H := K + D - M.                                         (8)
```

Differentiating (7) along (6) gives

```text
Vd'
 = -y^T(D-M)y
   -x^T K x
   +y^T A x
   -(y+x)^T r.                                          (9)
```

Thus the entire P8/common-input contribution has disappeared from the energy derivative.

## 3. Existing dissipation margin, plus a sharper upper norm constant

The rational estimates from `T-P5-016` give

```text
y^T(D-M)y + x^T K x >= (229/400)(||x||^2+||y||^2),     (10)

y^T A x <= (1/800)(||x||^2+||y||^2).                   (11)
```

Let

```text
N := ||x||^2+||y||^2.
```

Then

```text
Vd' <= -(457/800) N + |(x+y)^T r|.                     (12)
```

`T-P5-016` used the convenient upper bound `Vd<=N`. For the present tube interface it is worthwhile to keep one more rational digit of structure. Since

```text
M <= mmax I,
mmax = 350003/3000000,
K <= (303/400) I,
D <= (4/5) I,
```

and, coordinatewise,

```text
x^T M y <= 1/2 x^T M x + 1/2 y^T M y,
```

we obtain

```text
Vd
 <= mmax ||y||^2
    + (mmax/2 + 303/800 + 2/5)||x||^2

 =  (350003/3000000)||y||^2
  + (5022503/6000000)||x||^2.                           (13)
```

Both coefficients are strictly below `21/25`; for the larger one the exact gap is

```text
21/25 - 5022503/6000000 = 17497/6000000 > 0.           (14)
```

Hence the clean improved equivalence is

```text
Vd <= (21/25) N.                                        (15)
```

This slightly strengthens every residual-to-energy barrier below without changing the storage.

## 4. Residual-only ISS inequality

By Cauchy and `||x+y||^2 <= 2N`,

```text
|(x+y)^T r| <= sqrt(2N) ||r||.
```

Using the square/Young split already employed in `T-P5-016`, with exactly half of the `457/800` dissipation retained,

```text
|(x+y)^T r|
 <= (457/1600)N + (800/457)||r||^2.                    (16)
```

Combining (12), (15), and (16),

```text
Vd'
 <= -(457/1600)N + (800/457)||r||^2
 <= -(457/1344)Vd + (800/457)||r||^2.                  (17)
```

The rate `457/1344` comes from

```text
(457/1600) * (25/21) = 457/1344.
```

Compared with the previous convenient `V<=N` consumer, the storage-to-state refinement reduces the ultimate/barrier residual gain from

```text
1280000/208849
```

to

```text
1075200/208849.                                         (18)
```

No approximation is needed in the proof.

### Division-free barrier

Assume on the same covered domain

```text
||r||^2 <= L2.                                          (19)
```

On a boundary `Vd=Vstar`, (17) is strictly inward whenever

```text
208849 Vstar > 1075200 L2.                              (20)
```

Therefore, under the standard differentiability/first-exit hypotheses, an initial state with `Vd(0)<Vstar` cannot cross outward through that boundary while (1)-(2) and (19) remain valid.

This is an additive-residual consumer. Positive FD offsets such as those classified in `T-P5-009` do **not** need to be dishonestly converted into `rho |v|`; once a source lane produces a genuine two-channel bound, they may enter `L2` directly.

## 5. Matching initial conditions eliminate the headroom cost of the affine shift

If actual and nominal trajectories start from the same mechanical state,

```text
q(0)=qbar(0),
q'(0)=qbar'(0),                                          (21)
```

then

```text
x(0)=0,
y(0)=0,
Vd(0)=0.                                                 (22)
```

This is a major difference from the affine particular path of `T-P5-017`, whose relative initial energy is nonzero for `c!=0`. Here the nominal path can be chosen to satisfy the **same physical initial condition** as the actual path, so the entire Lyapunov budget is available for model/source residual rather than initial reference mismatch.

The cost is shifted elsewhere: one must propagate or otherwise certify the nominal trajectory. That is naturally a P8 task, not a P5 residual-power task.

## 6. Much sharper component tube bounds from the completed square

For a domain bootstrap, an energy bound must be converted back to coordinate error. The coarse full-state constant from `T-P5-016` is not needed.

### 6.1 Two exact matrix lower bounds

The mass satisfies

```text
M >= (1/20) I,                                          (23)
```

because

```text
350003/3000000 - 1/20 = 200003/3000000 > 0,
200739/4000000 - 1/20 = 739/4000000 > 0.
```

For `H=K+D-M`, its diagonal entries are

```text
H44 = 4299997/3000000,
H55 = 4719261/4000000,
H45 = H54 = -3/400.
```

Using `-2ab <= a^2+b^2` on the cross term gives

```text
H >= (117/100) I.                                       (24)
```

Indeed the two post-cross coefficients exceed `117/100` by exactly

```text
767497/3000000,
9261/4000000,
```

respectively.

Therefore (8) implies

```text
Vd >= (1/40)||y+x||^2 + (117/200)||x||^2.              (25)
```

In particular,

```text
||x||^2 <= (200/117)Vd.                                 (26)
```

### 6.2 A direct velocity bound, not a triangle-inequality bound

The following scalar identity is exact:

```text
(1/20)(y+x)^2 + (117/100)x^2
 = (117/2440)y^2
   + (61/50)(x + (5/122)y)^2.                           (27)
```

Apply it coordinatewise to (25). This yields

```text
Vd >= (117/4880)||y||^2,                                (28)
```

hence

```text
||y||^2 <= (4880/117)Vd.                                (29)
```

This is substantially tighter than first bounding `y=(y+x)-x` by a triangle inequality.

Thus a sublevel `Vd<=Vstar` gives immediately

```text
x_i^2 <= (200/117)Vstar,
y_i^2 <= (4880/117)Vstar                                (30)
```

for each block coordinate `i=4,5`.

## 7. Nominal-flowpipe margin -> actual source-domain bootstrap

Suppose a nominal P8 flowpipe is certified inside a shrunken physical box, with block-coordinate margins `sq>0`, `sv>0`:

```text
|qbar_i(t)| <= Q_i - sq,
|qbar'_i(t)| <= V_i - sv,
```

and the full source/residual theorem is valid whenever the actual state is inside the larger box `|q_i|<=Q_i`, `|v_i|<=V_i`.

If one chooses `Vstar` so that

```text
200 Vstar <= 117 sq^2,                                  (31)
4880 Vstar <= 117 sv^2,                                 (32)
```

then (30) and the triangle inequality ensure that `Vd<Vstar` keeps the actual block coordinates inside the larger box.

Combined with the residual barrier (20), this gives a standard first-exit bootstrap: before the hypothetical first domain exit, the residual premise is valid; the residual premise makes the error-energy boundary inward; therefore the coordinate error cannot consume the available margin and the exit cannot occur through block 4 or 5.

### One common margin

For a single margin `s>0` on all four block coordinates, take

```text
Vstar := (117/4880) s^2.                                (33)
```

This automatically satisfies both (31) and (32). The residual condition (20) becomes the completely division-free certificate

```text
24435333 s^2 > 5246976000 L2.                           (34)
```

because

```text
208849*117 = 24435333,
1075200*4880 = 5246976000.
```

So a source/checker lane can work entirely with rational squared margins: no square root is needed in the trusted arithmetic core.

## 8. Why this seam is useful for P8

The current P8 route has two different difficulties:

1. propagate a trajectory/flowpipe over the time interval;
2. account for DH/FD/Float64/solve mismatch while staying inside the domain on which those mismatch bounds are valid.

The incremental theorem separates them cleanly. A possible future proof architecture is

```text
(A) propagate a nominal exact-real 12D mechanical system;
(B) prove the nominal block-(4,5) coordinates retain explicit domain margin;
(C) source-bind the actual-minus-nominal generalized-force residual and prove ||r||^2<=L2 on the full domain;
(D) use (20)/(31)/(32), or the one-margin certificate (34), to get a self-consistent actual tube;
(E) combine with independent lanes for the other coordinates and terminal transfer.
```

This can be preferable to propagating every execution/model uncertainty directly through the P8 interval ODE, because the residual uncertainty is paid by a dissipative energy tube rather than by repeated interval wrapping.

This review does **not** claim that the current nominal flowpipe, margin, or source-bound `L2` already exists. It identifies the exact mathematical contract that would make such a split sound.

## 9. Relation to nearby reviews

### `T-P5-017`

No conflict. `T-P5-017` constructs an explicit affine particular solution and therefore avoids a separate nominal ODE, at the price of nonzero initial relative energy and the assumption `c'=0`. `T-P5-018` instead permits an arbitrary nominal trajectory with matching initial data. Its common forcing cancels even for non-affine inputs.

### `T-P5-009`

The positive-offset obstruction remains correct for a **homogeneous velocity-relative** consumer. The present theorem supplies an honest alternative destination: after actual source binding, additive offsets may contribute to the squared residual budget `L2` instead of being forced into `rho |v|`.

### `T-P4-019`

A genuinely additive execution error may be impossible to absorb in a zero-slack pointwise Schur certificate. That does not imply it is unusable globally: if it can be bounded as part of the generalized-force residual mismatch, `T-P5-018` can consume it as an ISS/tube forcing. P4 Schur closure and P5 incremental energy are therefore complementary consumers rather than substitutes.

## 10. Failure boundaries

1. **Same forcing is essential.** If actual and nominal equations use different input signals, their difference appears as an additional forcing and must be added to `r`.
2. **Same reference block is essential for the exact subtraction used here.** Differences in mass/damping/stiffness must either be included in the generalized-force residual or handled by a separate incremental coefficient-variation theorem.
3. **Residual coverage must be on the same physical domain.** A point sample or positive-offset audit is not a uniform `L2` theorem.
4. **The tube only controls block 4/5.** Other mechanical coordinates and `w` still need their own P8/source-domain coverage.
5. **Nominal propagation is not proved here.** The theorem trades the explicit affine reference for a nominal flowpipe obligation.
6. **First-exit/ODE regularity remains separate.** Equations (20) and (34) are algebraic inward-boundary certificates, not by themselves a calculus theorem.
7. **No source semantics are inferred from the frozen rational coefficients.** The constant-block identity is conditional on the source-facing residual ledger that defines `l` relative to this reference block.

## 11. Lean-friendly theorem decomposition

The first formalization can be small and source-independent.

### Difference identity

```lean
theorem common_forcing_difference
    (m4 m5 d4 d5 b44 b45 b54 b55 : ℝ)
    (q4 q5 v4 v5 a4 a5 q4n q5n v4n v5n a4n a5n : ℝ)
    (f4 f5 l4 l5 ln4 ln5 : ℝ)
    (hA4 : m4*a4 + d4*v4 + b44*q4 + b45*q5 = f4-l4)
    (hN4 : m4*a4n + d4*v4n + b44*q4n + b45*q5n = f4-ln4)
    ... :
    m4*(a4-a4n) + d4*(v4-v4n)
      + b44*(q4-q4n) + b45*(q5-q5n)
      = -(l4-ln4) := by
  linarith
```

### Rational storage bounds

```lean
theorem block45_incremental_V_upper :
  Vd x4 x5 y4 y5 <= (21/25) * N x4 x5 y4 y5

theorem block45_incremental_x_bound :
  (117/200) * (x4^2+x5^2) <= Vd x4 x5 y4 y5

theorem block45_incremental_y_bound :
  (117/4880) * (y4^2+y5^2) <= Vd x4 x5 y4 y5
```

The velocity theorem can be proved using the exact identity (27), so no square roots are needed.

### Residual-only rate and barrier

```lean
theorem block45_incremental_rate
    (hpow : dV <= -(457/800)*N + absPower)
    (hdual : absPower <= (457/1600)*N + (800/457)*L2)
    (hVupper : V <= (21/25)*N) :
    dV <= -(457/1344)*V + (800/457)*L2

theorem block45_incremental_boundary_inward
    (hL : r4^2+r5^2 <= L2)
    (hbudget : 1075200*L2 < 208849*Vstar)
    (hboundary : V = Vstar) :
    dV < 0
```

### Domain-margin corollary

```lean
theorem block45_common_margin_budget
    (hs : 0 < s)
    (hL : r4^2+r5^2 <= L2)
    (hbudget : 5246976000*L2 < 24435333*s^2)
    ... :
    -- boundary V = (117/4880)s^2 is inward,
    -- and the resulting sublevel gives |x_i|<s, |y_i|<s.
    ...
```

Keep the trajectory/first-exit theorem separate from this algebraic package.

## 12. Recommended next work

1. A formalization Agent can implement the four pure algebraic pieces: common-forcing subtraction, `V<=21/25 N`, the `117/4880` velocity lower bound, and the division-free boundary certificate.
2. P8 can consider a **nominal-flowpipe + shrunken-domain margin** output rather than forcing the full execution uncertainty into every Picard box.
3. The source/checker lane should target an actual same-domain two-channel residual mismatch certificate `r4^2+r5^2<=L2`; the positive FD offsets identified in `T-P5-009` may honestly enter this additive budget.
4. Only after both nominal margin and `L2` exist should the coordinator test certificate (34) numerically/rationally. Until then this remains a mathematical child, not physical closure.

## Admission boundary

```text
mathematical_incremental_identity = derived
rational_tube_constants           = derived
source_bound_L2                    = OPEN
nominal_flowpipe_margin            = OPEN
first_exit_calculus                = OPEN
full_12D_domain_coverage           = OPEN
P5/P8/M4 admission                 = unchanged
registry                           = unchanged
```
