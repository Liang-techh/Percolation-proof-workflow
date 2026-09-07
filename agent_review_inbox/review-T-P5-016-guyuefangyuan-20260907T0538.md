---
kind: review_result
review_id: review-T-P5-016-guyuefangyuan-20260907T0538
task_id: T-P5-016
source_agent: 古月方源
claimed_at: 2026-09-07T05:23:00-06:00
created_at: 2026-09-07T05:38:00-06:00
inspected_commit: f6642ddfcb3907e9098b134e1c589972d23f1bc4
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_hypocoercive_block45_storage_and_use_it_as_an_optional_P5_infinite_horizon_consumer_after_source_binding
---

# T-P5-016 — block-(4,5) hypocoercive storage: exact rational decay and additive-residual barrier

## Scope and motivation

`T-P5-013` proved a useful finite-horizon Lyapunov barrier, but also isolated a genuine obstruction: the available kinetic dissipation `A(v)` only satisfies an upper relation `A <= K Z`; it does not lower-bound total mechanical storage because one may have `v=0`, positive configuration energy, and therefore zero instantaneous damping. Hence an additive ramp/nonconservative work budget cannot be upgraded to a uniform infinite-horizon estimate from that energy alone.

This review attacks exactly that obstruction. The idea is to add a standard but here **fully rational and source-facing** hypocoercive cross term, so position energy is converted into velocity damping through the second-order equation itself.

Two levels are separated throughout:

1. a generic constant-mass second-order theorem, independent of Route-B constants;
2. a concrete exact-rational specialization to the frozen block-(4,5) PMI coefficient model.

The latter uses the literal frozen source expression in
`examples/routeb_source_binding_audit/snapshots/original_target/routeB_pmi_certificate.jl` together with the exactized reference block from `T-P3-010`. It is **not** a claim that Julia Float64 execution, the current live source, or the full physical DH residual has already been semantically bound. `T-P4-018` independently confirms the required force normalization: the literal `kc=1/20` in `f_B` becomes `(q5/100,q4/200)` after multiplication by `I_B=diag(1/5,1/10)`.

No provenance, receipt, admission, P8 coverage, IEEE error bound, ODE existence, or P5/M4 closure is claimed.

## 1. Generic hypocoercive identity

Consider a constant-mass second-order system

```text
M q'' + D q' + K q = A q + e,
```

with `v=q'`, where `M,D,K` are symmetric, `M` is positive definite, and `A` is skew-symmetric. For any scalar `eps`, define

```text
V_eps(q,v)
 := 1/2 v^T M v
  + 1/2 q^T K q
  + eps q^T M v
  + eps/2 q^T D q.                                    (1)
```

Differentiating and substituting the equation gives

```text
V_eps'
 = - v^T (D-eps M) v
   - eps q^T K q
   + v^T A q
   + (v+eps q)^T e.                                    (2)
```

The cancellation is exact: the derivative of `eps q^T M v` contributes
`eps v^T M v + eps q^T M q''`, while the derivative of
`eps/2 q^T D q` contributes `eps q^T D v`; these cancel the `D v` term after inserting `M q''`.

The same functional has the exact completion

```text
V_eps
 = 1/2 (v+eps q)^T M (v+eps q)
   + 1/2 q^T (K + eps D - eps^2 M) q.                 (3)
```

Thus positivity requires a restoring-force premise, not merely damping:

```text
M > 0,
K + eps D - eps^2 M > 0.                               (4)
```

This is the structural repair of the `T-P5-013` obstruction. It creates a full-state storage whose derivative contains a negative configuration term as well as velocity damping.

## 2. Exactized frozen block-(4,5) equation

The frozen PMI source has, for axes `(4,5)`,

```text
f4 = -(15/4) q4 - 4 v4 + (1/20) q5 + w,
f5 = -(29/5) q5 - (13/2) v5 + (1/20) q4 + w.
```

With the force normalization from the C2/B45 contract

```text
I_B = diag(1/5,1/10),
```

this becomes

```text
I4 f4 = -(3/4)q4 -(4/5)v4 +(1/100)q5 +(1/5)w,
I5 f5 = +(1/200)q4 -(29/50)q5 -(13/20)v5 +(1/10)w.    (5)
```

Let the exactized `q=0` reference mass block from `T-P3-010` be

```text
M = diag(m4,m5),
m4 = 350003/3000000,
m5 = 200739/4000000.                                  (6)
```

For the generalized-force residual

```text
l := I_B f_B - M a_B,
```

(5) is equivalently

```text
M a + D v + Kdiag q = J q + g w - l,                  (7)
```

with

```text
D     = diag(4/5,13/20),
Kdiag = diag(3/4,29/50),
J     = [[0,1/100],[1/200,0]],
g     = (1/5,1/10)^T.                                  (8)
```

Split the nonsymmetric cross-stiffness into

```text
S := (J+J^T)/2 = [[0,3/400],[3/400,0]],
A := (J-J^T)/2 = [[0,1/400],[-1/400,0]],               (9)
K := Kdiag-S = [[3/4,-3/400],[-3/400,29/50]].          (10)
```

Then the exactized block equation is

```text
M a + D v + K q = A q + e,
e := g w - l.                                           (11)
```

The symmetric part of the cross coupling is therefore genuine storage; only the tiny skew component `A` remains nonconservative.

## 3. Choose eps=1: exact block storage and derivative

Set `eps=1` in (1):

```text
V(q,v)
 = 1/2 v^T M v
 + 1/2 q^T K q
 + q^T M v
 + 1/2 q^T D q.                                        (12)
```

Using (2), (11), and `q^T A q=0`,

```text
V'
 = -v^T(D-M)v
   -q^T K q
   +v^T A q
   +(v+q)^T e.                                         (13)
```

The completed-square form is

```text
V
 = 1/2 (v+q)^T M (v+q)
   + 1/2 q^T(K+D-M)q.                                  (14)
```

Everything in (12)-(14) is exact rational algebra once the two scalar block equations (7) are assumed.

## 4. Exact rational coercivity constants

The symmetric stiffness satisfies the global bounds

```text
(229/400) ||q||^2 <= q^T K q <= (303/400) ||q||^2.     (15)
```

A direct proof uses `2 xy <= x^2+y^2` and `-2xy <= x^2+y^2` on the cross term `-(3/200) q4 q5`.

The velocity coefficients are

```text
4/5 - m4  = 2049997/3000000,
13/20-m5 = 2399261/4000000,                             (16)
```

and both are larger than `229/400`. Also

```text
K + D - M >= (3317497/3000000) I,                      (17)
```

while the minimum mass coefficient is

```text
m_min = 200739/4000000.                                (18)
```

Using the exact scalar SOS identity

```text
(v+q)^2 + q^2 - (1/3)(v^2+q^2)
 = (1/6) ((2v+3q)^2 + q^2) >= 0,                       (19)
```

coordinatewise in (14), one gets the full-state lower bound

```text
V >= (m_min/6)(||q||^2+||v||^2)
  = (66913/8000000) N,                                 (20)
N := ||q||^2+||v||^2.
```

For the upper bound, use `2 q_i v_i <= q_i^2+v_i^2`, the mass maximum

```text
m_max = 350003/3000000,
```

and the upper stiffness bound in (15). The largest resulting configuration coefficient is

```text
(303/400 + 4/5 + 350003/3000000)/2
 = 5022503/6000000 < 1,                                (21)
```

while the velocity coefficient is at most `m_max<1`. Hence

```text
V <= N.                                                (22)
```

Thus `V` is a genuine positive-definite full-state storage with a completely explicit rational norm equivalence.

## 5. Exact unforced decay despite the skew cross coupling

The skew term in (13) is

```text
v^T A q = (1/400)(v4 q5 - v5 q4).                      (23)
```

Two applications of Young's inequality give the one-sided bound

```text
v^T A q <= (1/800) N.                                  (24)
```

By (15)-(16), the negative quadratic part of (13) is at least

```text
v^T(D-M)v + q^T K q >= (229/400) N.                    (25)
```

Therefore

```text
V' <= -(457/800) N + (v+q)^T e.                       (26)
```

In the exact ideal block (`w=0`, `l=0`, hence `e=0`), (22) yields

```text
V' <= -(457/800) V.                                    (27)
```

So, conditional on the block model holding along the trajectory, this 4-state linear block has an exact rational exponential Lyapunov rate `457/800`. This is much stronger than the original kinetic-only energy estimate: it controls configuration energy even at instants where `v=0`.

## 6. Additive residual / ramp forcing: an infinite-horizon scalar consumer

The same theorem admits a nonzero `e`. Since

```text
||v+q||^2 <= 2N,
```

for any `eta>0`,

```text
|(v+q)^T e|
 <= eta N + (1/(2 eta)) ||e||^2.                       (28)
```

Take exactly

```text
eta = 457/1600.
```

Combining (26), (28), and `V<=N` gives

```text
V' <= -(457/1600) V + (800/457) ||e||^2.              (29)
```

Hence a uniform same-domain bound

```text
||e||^2 <= Ebar                                         (30)
```

produces the standard ultimate estimate

```text
V(t)
 <= exp(-(457/1600)t) V(0)
    + (1280000/208849) Ebar
      * (1-exp(-(457/1600)t)),                          (31)
```

provided the differential inequality remains valid on the whole interval. The exact asymptotic gain is therefore

```text
1280000/208849 ~= 6.12883.                              (32)
```

For a first-exit/barrier consumer one does not need exponentials. If

```text
208849 Vstar > 1280000 Ebar,                            (33)
```

then the derivative is strictly negative on the boundary `V=Vstar`. Under the ordinary continuity/differentiability hypotheses this prevents outward first exit from that sublevel. This is a division-free rational target suitable for Lean/checker use.

This is the promised repair of the `T-P5-013` infinite-time obstruction: additive work is no longer accumulated linearly forever; the cross-term storage converts restoring force into a full-state negative drift.

## 7. Separate the P8 ramp and the P4 residual

Here

```text
e = g w - l,
||g||^2 = (1/5)^2 + (1/10)^2 = 1/20.                  (34)
```

The crude but source-independent split

```text
||g w-l||^2 <= (1/10) w^2 + 2||l||^2                 (35)
```

turns (29) into

```text
V'
 <= -(457/1600)V
    + (80/457) w^2
    + (1600/457)||l||^2.                               (36)
```

If the P8 ramp has `w=c t`, `c^2<=3`, `0<=t<=1`, then `w^2<=3`; a uniform residual cap `||l||^2<=L2` gives the exact rational barrier condition

```text
208849 Vstar > 384000 + 2560000 L2.                    (37)
```

This specialization is intentionally conservative. A future source theorem may exploit correlation between `w` and `l`, or first shift to the moving ramp equilibrium, to reduce the cost. Equation (37) is useful because it is already a pure rational checker target.

### Optional moving-equilibrium refinement

For the unsymmetrized stiffness

```text
B := Kdiag-J
 = [[3/4,-1/100],[-1/200,29/50]],
det B = 8699/20000 > 0,                                (38)
```

one has the exact ramp equilibrium slope

```text
h := B^{-1} g = (2340/8699, 1520/8699).                (39)
```

Writing `q=x+h w`, `v=x'+h c` for an affine ramp `w'=c`, `w''=0` removes the `w` amplitude from the ideal linear equation and leaves the constant forcing

```text
-D h c - l,
D h = (1872/8699, 988/8699).                            (40)
```

Its squared coefficient is

```text
||D h||^2 = 4480528/75672601 ~= 0.05921.               (41)
```

This may be a better infinite-horizon P8/P5 interface than paying `w^2` directly, but it changes coordinates and should be a separate child if the coordinator wants it. The main theorem (29) does not depend on this refinement.

## 8. Sharp failure boundaries / counterexamples

### 8.1 Restoring stiffness is necessary

The hypocoercive route cannot be obtained from damping alone. In one dimension take

```text
q' = v,
v' = -d v,
d>0.
```

Every state `(q0,0)` is an equilibrium. Therefore no positive-definite full-state storage can satisfy a strict estimate `V' <= -lambda V` with `lambda>0` on all states: at `(q0,0)`, `q0!=0`, the vector field and `V'` vanish while `V>0`.

So a positive restoring-force/coercivity premise is mathematically necessary; this is exactly the missing ingredient identified in `T-P5-013`.

### 8.2 The nonsymmetric cross coupling cannot simply be called potential

`J` is not symmetric. Treating all of `Jq` as a gradient would be false. Its skew component (9) has nonzero circulation and survives in power as (23). The present route does not hide that defect; it pays it explicitly by `1/800 N`.

### 8.3 Hypocoercivity does not repair source/domain gaps

Equations (27)-(37) are conditional on the block relation (7)/(11) and on a uniform residual bound on the same trajectory domain. They do not prove:

- that the frozen exactized `M0` relation equals Julia Float64 execution;
- that the full DH residual `l` satisfies a particular cap;
- that the P8 ramp source box covers `[0,1]`;
- that IEEE/controller/solve remainders vanish;
- ODE existence or continuation outside the covered source domain.

If the source/domain premise ends at a finite exit time, the differential inequality ends there too.

## 9. Minimal Lean theorem package

A source-independent formalization should avoid matrices initially and encode the two coordinates directly.

Define exact constants

```lean
m4 : ℝ := 350003/3000000
m5 : ℝ := 200739/4000000
```

and assume the two exactized residual equations

```text
m4*a4 = -(3/4)q4 -(4/5)v4 +(1/100)q5 +(1/5)w - l4,
m5*a5 = +(1/200)q4 -(29/50)q5 -(13/20)v5 +(1/10)w - l5.
```

Suggested child statements:

```lean
-- Pure algebra after differentiating the polynomial storage.
theorem block45_hypocoercive_derivative_identity ... :
  dV = -((4/5-m4)*v4^2 + (13/20-m5)*v5^2)
       -(3/4*q4^2 + 29/50*q5^2 - 3/200*q4*q5)
       +(1/400)*(v4*q5-v5*q4)
       +(v4+q4)*((1/5)*w-l4)
       +(v5+q5)*((1/10)*w-l5)

-- Norm equivalence, all constants rational.
theorem block45_V_lower :
  (66913/8000000) * (q4^2+q5^2+v4^2+v5^2) <= V

theorem block45_V_upper :
  V <= q4^2+q5^2+v4^2+v5^2

-- Pointwise decay/ISS-like inequality.
theorem block45_hypocoercive_rate ... :
  dV <= -(457/1600)*V
        +(800/457)*(e4^2+e5^2)

-- Division-free barrier specialization.
theorem block45_barrier
    (hE : e4^2+e5^2 <= Ebar)
    (hbudget : 1280000*Ebar < 208849*Vstar)
    (hV : Vstar <= V) :
    dV < 0
```

The first three are polynomial/rational and should be amenable to `ring_nf` plus `nlinarith`/square-nonneg lemmas. A later calculus theorem may integrate (29); it should remain separate from the algebraic sidecar.

## 10. Recommended next action

1. Formalization lane: encode the four pure algebra/norm/barrier lemmas above as a tiny portable sidecar. No source semantics are needed.
2. P4/source lane: provide a same-domain force residual cap for `l`, or a structured split. The hypocoercive theorem can consume a constant bias, so it does **not** require every term to vanish with velocity.
3. P8/source lane: if the target remains finite horizon `[0,1]`, either use (37) after source coverage is repaired or consider the moving-equilibrium transform (39)-(41) to replace `w` amplitude by constant ramp-rate forcing.
4. Coordinator: keep this as an optional P5 route. It should not replace the already compiled finite-horizon `T-P5-013/015` path unless the restoring-force/source block assumptions are actually easier to bind.

The main mathematical gain is that the old statement “additive work prevents infinite-time closure” is now refined: it is true for the kinetic-only storage, but **false once a restoring-force-compatible hypocoercive cross term is available**. For the exactized frozen block-(4,5), that cross term yields the explicit decay constant `457/800` and the additive-residual barrier `208849 Vstar > 1280000 Ebar`.
