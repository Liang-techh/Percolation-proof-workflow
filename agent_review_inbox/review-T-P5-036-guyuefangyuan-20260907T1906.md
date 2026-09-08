---
kind: review_result
review_id: review-T-P5-036-guyuefangyuan-20260907T1906
task_id: T-P5-036
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T18:23:00-06:00
created_at: 2026-09-07T19:06:00-06:00
inspected_commit: e352e72d92eb6dfd19bd275ccf0a44c699bdc5a2
continuation_of:
  - review-T-P5-035-guyuefangyuan-20260907T1728
related_reviews:
  - review-T-P5-031-guyuefangyuan-20260907T1224
  - review-T-P5-037-honglianmozun-pending
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_componentwise_joint_reserve_and_weighted_residual_completion_then_feed_real_same_domain_componentwise_source_bounds
---

# T-P5-036 — anisotropic componentwise residual reserve for frozen block-(4,5)

## 0. Result in one line

Continue with exactly the frozen block-(4,5) Lyapunov pair from `T-P5-035`.  Put

```text
u4 := x4 + y4,
u5 := x5 + y5.
```

The previous joint certificate was

```text
Q >= (27/50) V + (1/6) u4^2 + (1/6) u5^2.
```

The first residual direction has materially more reserve than the second.  An exact rational strengthening is

```text
Q >= (27/50) V + (101/500) u4^2 + (1/6) u5^2.          (0.1)
```

Thus the two residual components should not be collapsed to one scalar `L2` before the Lyapunov consumer.  From the exact derivative

```text
V' = -Q - u4*l4 - u5*l5,
```

one obtains the componentwise ISS bound

```text
V' <= -(27/50) V + (125/101) l4^2 + (3/2) l5^2.        (0.2)
```

If same-domain source bounds give `l4^2 <= E4`, `l5^2 <= E5`, then at the existing `Vstar=1/4` a division-free strict first-exit gate is

```text
25000 E4 + 30300 E5 < 2727.                            (0.3)
```

For a residual entirely in component 4, the admissible squared residual rises from the isotropic `9/100` to `2727/25000`; this is an exact factor

```text
(2727/25000)/(9/100) = 303/250 = 1.212,
```

i.e. **21.2% more component-4 residual capacity**, with no new physical/source assumption.  The component-5-only threshold is unchanged.

The diagonal coefficient `101/500 = 0.202` is also already extremely close to the exact maximum possible while the component-5 reserve is fixed at `1/6`: the exact critical coefficient is about `0.2020579837`, so the remaining diagonal-slice room is only about `0.0287%` relative.

This child is deliberately disjoint from `T-P5-037`: 红莲魔尊 owns the scalar/isotropic coupled-completion lane; `T-P5-036` preserves residual-component anisotropy.

---

## 1. Frozen forms and the new residual metric

Use the same exact rational matrices and storage as `T-P5-035`:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
K = [[3/4,    -3/400],
     [-3/400, 29/50]],
A = [[0, 1/400],
     [-1/400, 0]].

V := (1/2) y^T M y
   + (1/2) x^T K x
   + x^T M y
   + (1/2) x^T D x,

Q := y^T(D-M)y + x^T K x - y^T A x.
```

In coordinate order

```text
z := (x4,x5,y4,y5),
```

define

```text
R36 := Q - (27/50)V - (101/500)(x4+y4)^2 - (1/6)(x5+y5)^2.   (1.1)
```

The symmetric matrix of `R36 = z^T H36 z` is exactly

```text
H36 =
[[ 259/2000,              -219/40000,          -23350027/100000000,        1/800 ],
 [ -219/40000,             2437/30000,         -1/800,                    -216259859/1200000000 ],
 [ -23350027/100000000,   -1/800,               134949619/300000000,       0 ],
 [ 1/800,                  -216259859/1200000000, 0,                        503518441/1200000000 ]].  (1.2)
```

All entries are exact rationals derived solely from the already-frozen `V,Q`; no source table, floating eigenvalue, solver objective, or numerical fit enters (1.2).

---

## 2. Exact positivity certificate

The four leading principal minors of `H36` are

```text
Delta1 = 259/2000,

Delta2 = 50350757/4800000000,

Delta3 = 64392553543361789
         /225000000000000000000,

Delta4 = 1399534174605692185573043249
         /14400000000000000000000000000000000.        (2.1)
```

Every numerator and denominator in (2.1) is strictly positive.  Hence Sylvester's criterion gives `H36 > 0`, proving (0.1).

For a Lean route that avoids importing a numerical spectral argument, here is an exact rational `LDL^T` factorization.  Write `H36 = L D L^T`, with

```text
L =
[[ 1, 0, 0, 0 ],
 [ -219/5180, 1, 0, 0 ],
 [ -23350027/12950000,
   -17283467739/125876892500,
   1, 0 ],
 [ 5/518,
   -55994878481/25175378500,
   -3396173013973188801/4121123426775154496,
   1 ]],
```

and diagonal

```text
D11 = 259/2000,
D22 = 50350757/621600000,
D33 = 64392553543361789/2360191734375000000,
D44 = 1399534174605692185573043249
      /4121123426775154496000000000000.                (2.2)
```

All four pivots are positive.  Therefore `z^T H36 z` is literally a positive rational sum of four squares `(L^T z)_i^2`.  This is the recommended kernel-facing representation if a general Sylvester theorem is inconvenient.

---

## 3. Exact componentwise residual completion

Let the force-normalized residual components entering the derivative be `l4,l5`.  The first coordinate uses the exact square identity

```text
(101/500) u4^2 + u4*l4 + (125/101) l4^2
  = (101*u4 + 250*l4)^2 / 50500
  >= 0.                                                 (3.1)
```

The second coordinate uses

```text
(1/6) u5^2 + u5*l5 + (3/2) l5^2
  = (u5 + 3*l5)^2 / 6
  >= 0.                                                 (3.2)
```

Combining (0.1), (3.1), and (3.2) with

```text
V' = -Q - u4*l4 - u5*l5
```

gives the exact source-independent consumer

```text
V' <= -(27/50)V
      + (125/101) l4^2
      + (3/2) l5^2.                                    (3.3)
```

Compared with `T-P5-035`, which charges `(3/2)(l4^2+l5^2)`, the coefficient of `l4^2` falls from `3/2` to `125/101`; the `l5^2` charge is unchanged.  The ratio

```text
(3/2)/(125/101) = 303/250 = 1.212                      (3.4)
```

is the same 21.2% directional capacity improvement seen at the barrier.

If only a total norm bound is available, one may always use

```text
(125/101)l4^2 + (3/2)l5^2 <= (3/2)(l4^2+l5^2),
```

so this consumer is never worse than the old scalar consumer.  The gain appears exactly when the source lane preserves component information.

---

## 4. One-trajectory first-exit gate

Assume same-domain componentwise bounds

```text
l4^2 <= E4,
l5^2 <= E5,
E4,E5 >= 0.                                             (4.1)
```

Then (3.3) is strictly inward at `V=Vstar` whenever

```text
(125/101)E4 + (3/2)E5 < (27/50)Vstar.                  (4.2)
```

Clearing denominators gives the pure-rational gate

```text
6250 E4 + 7575 E5 < 2727 Vstar.                        (4.3)
```

For the existing quarter barrier `Vstar=1/4`, this becomes

```text
25000 E4 + 30300 E5 < 2727.                            (4.4)
```

Sanity checks:

```text
E5 = 0  => E4 < 2727/25000 = 0.10908,
E4 = 0  => E5 < 2727/30300 = 9/100.
```

The old isotropic gate is `E4+E5 < 9/100`.  Hence the new feasible region strictly contains the old triangle and stretches the component-4 intercept by factor `303/250`.

No statement here supplies `E4,E5`; they remain source/domain obligations.

---

## 5. Incremental parameter tube

For difference dynamics, keep the two source components separate.  Assume

```text
(Dl4)^2 <= mu4*Vd + nu4*dc^2,
(Dl5)^2 <= mu5*Vd + nu5*dc^2,                          (5.1)
```

with all `mu_i,nu_i >= 0`.  Applying (3.3) to the difference system gives

```text
Vd' <= -[27/50 - (125/101)mu4 - (3/2)mu5] Vd
       +[(125/101)nu4 + (3/2)nu5] dc^2.                (5.2)
```

On the existing parameter boundary

```text
Vd = (1/12) dc^2,
```

a strict inward condition is

```text
(125/101)(mu4 + 12 nu4)
  + (3/2)(mu5 + 12 nu5)
  < 27/50.                                              (5.3)
```

Clearing denominators gives

```text
6250 (mu4 + 12 nu4)
 + 7575 (mu5 + 12 nu5)
 < 2727.                                                (5.4)
```

If the source layer collapses the two components before reaching this theorem, (5.4) collapses back to the scalar `T-P5-035` gate.  Therefore the useful source-facing representation is a four-number table `(mu4,nu4,mu5,nu5)`, not only aggregate `(mu,nu)`.

---

## 6. Exact near-optimality in the diagonal slice

The coefficient `101/500` was not chosen by a floating fit.  Consider the entire one-parameter diagonal family

```text
H(h) := Q - (27/50)V - h*u4^2 - (1/6)*u5^2.            (6.1)
```

Its `4x4` determinant is exactly affine in `h`:

```text
det H(h)
 = [4877007676788744113042095643249
    - 24136673973337318915131300000000*h]
   /14400000000000000000000000000000000.              (6.2)
```

Hence any PSD certificate in this diagonal slice must satisfy

```text
h <= hcrit,

hcrit := 4877007676788744113042095643249
         /24136673973337318915131300000000
       ~= 0.20205798372120995.                          (6.3)
```

At `h=hcrit`, the first three leading principal minors are still strictly positive:

```text
3124299745372577107323930306751
 /24136673973337318915131300000000,

474513320177488114152453542332207
 /45256263700007472965871187500000000,

39103040487615782657168706718585609
 /139027242086422956951156288000000000000,              (6.4)
```

while the determinant is exactly zero.  Thus the critical matrix is PSD singular, and `hcrit` is the exact endpoint of this fixed-`u5` diagonal lane.

The certified simple rational

```text
h0 = 101/500 = 0.202
```

satisfies

```text
hcrit - h0
 = 1399534174605692185573043249
   /24136673973337318915131300000000
 > 0,                                                   (6.5)
```

and the relative endpoint gap is only

```text
hcrit/h0 - 1
 = 1399534174605692185573043249
   /4875608142614138420856522600000
 ~= 0.0002870481,                                       (6.6)
```

i.e. about **0.0287%**.  So there is essentially no value in continuing to tune only the `u4^2` coefficient while holding the `u5^2` reserve at `1/6`.

For a nearby explicit rational counterexample, take

```text
hbad = 203/1000,
zbad = (x4,x5,y4,y5) = (11,13,6,6).                    (6.7)
```

Then exact evaluation gives

```text
zbad^T H(hbad) zbad = -1848397/15000000 < 0.           (6.8)
```

Therefore the universal strengthening with `203/1000*u4^2` is false.  This is a genuine global quadratic obstruction, not a floating eigenvalue warning.

---

## 7. What this changes in the P5 route

The useful consumer order is now

```text
same-domain source residual
  -> preserve component-4/component-5 squared budgets
  -> T-P5-036 weighted componentwise consumer
  -> only collapse to scalar L2 if the source cannot keep components separate.
```

This matters because the frozen block is intrinsically anisotropic: the first residual direction has about 21% more available work reserve at the same `27/50 V` decay allocation.  Destroying that information before the Lyapunov layer leaves certified margin on the table.

This child does **not** replace the more general `T-P5-026` cone/SPN lane.  If a source checker can preserve signed cross-correlation or a full `2x2` residual metric, SPN/direct-power certificates may still do better.  `T-P5-036` is the smallest exact componentwise adapter that already beats the scalar norm route and has a nearly sharp diagonal coefficient.

It also does not overlap `T-P5-037`: that child optimizes a scalar/isotropic completion, whereas (0.1) fixes the same decay coefficient `27/50` and extracts direction-specific residual reserve.

---

## 8. Suggested Lean decomposition

Recommended small theorems:

```text
block45_componentwise_joint_reserve
```

Explicitly expand the frozen rational `V,Q` and prove

```text
(27/50)*V
 + (101/500)*(x4+y4)^2
 + (1/6)*(x5+y5)^2
 <= Q.
```

For a kernel-friendly proof, encode the rational `LDL^T` data in (2.2) and finish from four `sq_nonneg` facts; do not invoke numerical eigenvalues.

```text
componentwise_residual_completion_101_500
```

Prove directly from the two square identities (3.1)-(3.2):

```text
-(101/500)*u4^2 - (1/6)*u5^2 - u4*l4 - u5*l5
 <= (125/101)*l4^2 + (3/2)*l5^2.
```

```text
block45_componentwise_iss
```

Compose the derivative identity with the two preceding lemmas.

```text
block45_componentwise_quarter_barrier
```

Pure arithmetic corollary consuming `l4^2<=E4`, `l5^2<=E5`, `25000 E4 + 30300 E5 < 2727`.

```text
block45_componentwise_incremental_tube
```

Consume (5.1) and the division-free gate (5.4).

Optional obstruction theorem:

```text
block45_componentwise_203_over_1000_counterexample
```

At the explicit rational state `(11,13,6,6)`, normalize the quadratic and prove (6.8) by `norm_num`.

The exact `hcrit` determinant identity is mathematically useful but not required for the first integration; the small rational counterexample already prevents accidental over-strengthening.

---

## 9. Dependencies and open boundaries

Depends on:

- the frozen exact-real block-(4,5) `V,Q` definitions already used by `T-P5-035`;
- the exact derivative identity `V' = -Q - (x+y)^T l` on the same mathematical model.

Still open, and deliberately not claimed here:

- true source binding of `l4,l5` on the same P8/first-exit domain;
- Float64/FD/solve/controller semantics and any execution-vs-exact-real error;
- construction of `E4,E5` or `(mu4,nu4,mu5,nu5)` from the deployed source;
- full 12-coordinate mechanical closure;
- ODE existence/continuation and first-exit calculus;
- P8 absolute flowpipe/domain coverage;
- Lean compile/axiom receipt;
- provenance/admission/registry/P5/P8/M4 closure.

Integration status therefore remains strictly **pending**.
