---
kind: review_result
review_id: review-T-P5-035-liuguanyi-20260907T1714
task_id: T-P5-035
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-07T17:04:00-06:00
created_at: 2026-09-07T17:14:00-06:00
inspected_commit: 8e7c19582ab77d1f0939af5567c3b54f1aee38e2
inspected_paths:
  - agent_review_inbox/review-T-P5-022-liuguanyi-20260907T0820.md
  - agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md
  - agent_review_inbox/review-T-P5-034-honglianmozun-20260907T1701.md
source_hashes:
  T-P5-022: b52b7a9c9026cae0bbead03bf87682447f3276c4
  T-P5-028: 6dc334aa54505646f336916e225c8aa508bddf35
  T-P5-034: 7a5b47ec4d6556a8a41df04619a77ae9d09b74dc
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_exact_3_over_125_storage_coercivity_and_use_it_as_the_typed_Euclidean_gain_to_V_gain_adapter_between_T-P5-022_028_and_T-P5-034
---

# T-P5-035 — exact `V >= (3/125)||z||^2` closes the Euclidean/source-gain -> P5 energy-gain interface

## 0. Result

The newest `T-P5-034` improves the dissipation-side inequality to

```text
Q >= (15/16) V,
V' <= -(15/32)V + (17/10)||l||^2,
```

but the source/Jacobian bridge from `T-P5-022` naturally emits a Euclidean centered gain

```text
||r_c||^2 <= ell2 ||delta z||^2,
delta z = (delta x4, delta x5, delta y4, delta y5).
```

The missing interface is a lower coercivity theorem for the *same frozen storage `V`*.  For the exact block-(4,5) storage used in `T-P5-034`, one has the fully rational identity

```text
V(z) >= (3/125) ||z||^2.                                (0.1)
```

This immediately yields the typed transport

```text
||r_c||^2 <= (125/3) ell2 V(delta z).                   (0.2)
```

Thus a source checker that already emits `ell2` can feed the new `T-P5-034` V-based barrier/tube consumer without inventing a new spectral norm or numerical eigenvalue.

For the incremental common-frame tube, if the source supplies

```text
||Delta l||^2 <= ell2 ||delta z||^2 + nu (delta c)^2,
```

then `T-P5-034`'s `Kc=1/12` gate is implied by the exact division-free condition

```text
34000 ell2 + 9792 nu < 225.                             (0.3)
```

In particular, for common ramp parameter (`delta c=0`) the centered source-gain threshold is simply

```text
ell2 < 9/1360.                                          (0.4)
```

No source identity, Float64 theorem, flowpipe/coverage fact, ODE continuation, Lean/kernel receipt, or admission is claimed here.

---

## 1. Frozen storage

Use exactly the storage from `T-P5-034`:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
K = [[3/4,    -3/400],
     [-3/400, 29/50]],

V
 := (1/2) y^T M y
  + (1/2) x^T K x
  + x^T M y
  + (1/2) x^T D x,

x=(x4,x5), y=(y4,y5).                                   (1.1)
```

In coordinate order `z=(x4,x5,y4,y5)`, direct expansion is

```text
V =
    (31/40) x4^2
  + (123/200) x5^2
  - (3/400) x4 x5
  + (350003/3000000) x4 y4
  + (200739/4000000) x5 y5
  + (350003/6000000) y4^2
  + (200739/8000000) y5^2.                              (1.2)
```

The identity below is for exactly this coordinate convention.  It must not be transplanted to a differently normalized force/state block without an explicit coordinate theorem.

---

## 2. Exact seven-square coercivity certificate

Exact rational expansion gives

```text
V - (3/125)(x4^2+x5^2+y4^2+y5^2)
=
    (1891747/3000000) x4^2
  + (1409/800000)     x5^2
  + (62003/12000000)  y4^2
  + (1359/80000000)   y5^2

  + (350003/3000000) (x4 + (1/2)y4)^2
  + (468391/800000)  (x5 + (3/70)y5)^2
  + (3/800)           (x4-x5)^2.                        (2.1)
```

Every coefficient is strictly positive.  Hence

```text
V >= (3/125)(x4^2+x5^2+y4^2+y5^2).                     (2.2)
```

Equivalently,

```text
||z||^2 <= (125/3) V.                                   (2.3)
```

This is deliberately an explicit SOS-style scalar identity: no eigenvalue API, matrix inverse, square root, or floating PSD check is needed.

### Independent exact check

I expanded the right side of (2.1) with exact rational arithmetic and subtracted the frozen polynomial (1.2); the normalized residual is identically zero.  All numbers in (2.1) are exact rationals.

A useful structural way to see the certificate is that the two difficult storage cross terms are paid by

```text
(350003/3000000)(x4+y4/2)^2,
(468391/800000)(x5+3y5/70)^2,
```

while the small `x4-x5` coupling is paid by `(3/800)(x4-x5)^2`; the four remaining diagonal margins stay positive.

---

## 3. Nearby failure boundary: do not round the constant upward to `121/5000`

The certified `3/125 = 0.024` is close to the true weakest Euclidean direction.  A simple exact rational state already disproves the tempting rounded-up constant `121/5000 = 0.0242`.

Take

```text
z0 = (x4,x5,y4,y5) = (0, -1/24, 0, 1).                 (3.1)
```

Then

```text
||z0||^2 = 577/576,
V(z0)    = 2310629/96000000,                            (3.2)
```

and

```text
V(z0) - (121/5000)||z0||^2
  = -49813/288000000 < 0.                               (3.3)
```

Equivalently,

```text
V(z0)/||z0||^2
  = 6931887/288500000
  ~= 0.024027338 < 0.0242.                              (3.4)
```

So any source adapter that silently replaces `3/125` by `0.0242` is unsound for the frozen storage.  I do **not** claim `3/125` is sharp; (3.3) is only a nearby exact upper obstruction.

---

## 4. Main typed bridge: `T-P5-022 ell2 -> T-P5-034 mu`

`T-P5-022` proves a source-coordinate/Jacobian transport of the form

```text
||r_c||^2 <= ell2 ||delta z||^2                         (4.1)
```

provided the source/state map, Jacobian envelope, force normalization and path/cell premises are supplied.

Assume the `delta z` in (4.1) is exactly the coordinate vector on which the incremental/centered storage is evaluated:

```text
Vd := V(delta z).                                        (4.2)
```

Then (2.3) gives

```text
||r_c||^2
 <= ell2 ||delta z||^2
 <= (125/3) ell2 Vd.                                    (4.3)
```

Therefore the V-based centered-gain coefficient can be chosen as

```text
mu := (125/3) ell2.                                      (4.4)
```

This is the missing mathematical adapter.  It is valid only when the state-coordinate identity in (4.2) is typed and proved; a source norm in a different ordering/scaling cannot be re-labelled as `Vd`.

### Common-ramp specialization via `T-P5-028`

`T-P5-028` already proves that at fixed time, if actual and nominal trajectories share the same ramp parameter `c`, then

```text
Delta q4 = Delta x4,
Delta q5 = Delta x5,
Delta v4 = Delta y4,
Delta v5 = Delta y5,
Delta w  = 0,
Delta c  = 0.                                            (4.5)
```

Hence in the common-`c` mode the Euclidean source displacement in the four active mechanical coordinates is exactly the `delta z` consumed by (2.1)-(2.3); no extra coordinate norm factor is needed.  Large source Jacobian columns in `w/c` still cost zero centered gain because those displacement rows are zero, exactly as in `T-P5-022/028`.

If `delta c != 0`, the rank-one/parameter correction of `T-P5-028` must remain explicit; it cannot be hidden inside (4.4).

---

## 5. Incremental tube composition: exact source-facing gate

Suppose the source/path lane proves the joint incremental squared bound

```text
||Delta l||^2
 <= ell2 ||delta z||^2 + nu (delta c)^2,
ell2 >= 0,
nu   >= 0.                                               (5.1)
```

By (2.3),

```text
||Delta l||^2
 <= (125/3)ell2 Vd + nu (delta c)^2.                    (5.2)
```

Thus in `T-P5-034` notation one may take

```text
mu = (125/3)ell2.                                        (5.3)
```

The new `15/16` incremental barrier with `Kc=1/12` requires

```text
272 mu + 3264 nu < 75.                                  (5.4)
```

Substituting (5.3) and clearing the only denominator gives the exact source-facing condition

```text
34000 ell2 + 9792 nu < 225.                             (5.5)
```

No optimization variable remains.

### Common-parameter centered tube

When `delta c=0` / `nu=0`, (5.5) reduces to

```text
34000 ell2 < 225,
```

i.e.

```text
ell2 < 9/1360.                                          (5.6)
```

This is a concrete exact target for a `T-P5-022/023` source Jacobian checker.  It says precisely how small the Euclidean centered squared gain must be before the newest `T-P5-034` energy tube can consume it.

---

## 6. Separate centered gain plus anchor bias: updated rational discriminant

`T-P5-022` also allows the source lane to produce a separate anchor bound

```text
||b||^2 <= B2,                                           (6.1)
```

rather than a joint total residual-square bound.  In that case one must **not** silently write

```text
||r_c+b||^2 <= ell2||z||^2+B2;
```

that omits the cross term.  The correct bridge uses a Young parameter `theta>0`:

```text
||r_c+b||^2
 <= (1+theta)||r_c||^2 + (1+1/theta)||b||^2.            (6.2)
```

On the quarter-energy boundary `V=1/4`, (2.3) gives

```text
||r_c||^2 <= (125/12) ell2.                             (6.3)
```

Let

```text
A := (125/12) ell2,
B := B2,
T := 75/1088,                                            (6.4)
```

where `T` is exactly the total squared-residual allowance from `T-P5-034` at `V=1/4`.

A `theta>0` satisfying

```text
(1+theta)A + (1+1/theta)B < T                           (6.5)
```

exists exactly when the quadratic

```text
A theta^2 - (T-A-B) theta + B < 0                       (6.6)
```

has a positive feasible point.  Define the fully cleared rational margin

```text
R := 225 - 34000 ell2 - 3264 B2.                        (6.7)
```

For `ell2>0`, a sufficient-and-exact real feasibility test is

```text
R > 0,
R^2 > 443904000 ell2 B2.                                (6.8)
```

Indeed `T-A-B = R/3264`, and

```text
4AB = (125/3) ell2 B2,
3264^2 * (125/3) = 443904000.                           (6.9)
```

A purely rational witness is the quadratic vertex

```text
theta_bal = R / (68000 ell2),                           (6.10)
```

which is positive under (6.8) and makes (6.6) strictly negative.  Thus the checker does not need a square root even though (6.8) is a discriminant condition.

Boundary cases are simple:

```text
ell2 = 0  -> require B2 < 75/1088,
B2   = 0  -> require ell2 < 9/1360.                     (6.11)
```

This section is an updated source-to-energy adapter for the new `15/16` consumer.  It should not replace a sharper direct `K_path`/orthant consumer if one is available.

---

## 7. Source-domain consequence of the quarter barrier

The coercivity theorem also gives a clean domain transport.  Any state satisfying

```text
V(z) <= 1/4                                              (7.1)
```

necessarily satisfies

```text
||z||^2 <= 125/12.                                      (7.2)
```

Hence every active coordinate obeys the squared cap

```text
x4^2, x5^2, y4^2, y5^2 <= 125/12.                      (7.3)
```

This is not a flowpipe or coverage theorem; it is only a one-way mathematical implication useful when a source Jacobian/cell certificate is already valid on a Euclidean region containing that ball.  The converse is false in general and must not be used to infer `V<=1/4` from the same Euclidean cap.

---

## 8. Minimal theorem surfaces

The pure algebraic kernel child can be tiny:

```text
theorem block45_V_minus_3_125_normSq_sos
    (x4 x5 y4 y5 : R) :
    V45 x4 x5 y4 y5
      - (3/125) * (x4^2+x5^2+y4^2+y5^2)
      =
        (1891747/3000000) * x4^2
      + (1409/800000) * x5^2
      + (62003/12000000) * y4^2
      + (1359/80000000) * y5^2
      + (350003/3000000) * (x4+y4/2)^2
      + (468391/800000) * (x5+(3/70)*y5)^2
      + (3/800) * (x4-x5)^2 := by
  ring
```

followed by

```text
theorem block45_V_ge_3_125_normSq :
  (3/125) * (x4^2+x5^2+y4^2+y5^2) <= V45 x4 x5 y4 y5 := by
  rw [block45_V_minus_3_125_normSq_sos]
  positivity
```

and the interface corollary

```text
theorem euclidean_centered_gain_to_V_gain
    (hV : (3/125) * N <= Vd)
    (hr : r2 <= ell2 * N)
    (hell : 0 <= ell2) :
    r2 <= (125/3) * ell2 * Vd := ...
```

A second small arithmetic theorem can encode

```text
272*((125/3)*ell2) + 3264*nu < 75
<- 34000*ell2 + 9792*nu < 225.                          (8.1)
```

The centered+anchor discriminant (6.8) should be a separate theorem so the main coercivity leaf stays source-independent.

---

## 9. Failure boundaries / remaining obligations

1. The theorem uses exactly the frozen `V45` coordinate convention.  A differently scaled state needs a new coordinate congruence/transport theorem.
2. `T-P5-022`'s `ell2` is consumable only if its source path/cell/Jacobian premises are valid on the same first-exit/incremental domain.
3. The common-ramp zero rows are valid only under the `T-P5-028` common-parameter premise.  Parameter mismatch must remain in the `nu`, rank-one `K_eff`, expanded-state, or additive/transverse lane.
4. Separate anchor bias must use (6.2) or a stronger joint source metric; simply adding squared caps is mathematically invalid.
5. Float64/controller/solve discontinuities are not made differentiable by this bridge.
6. `3/125` is certified, not claimed sharp.  `121/5000` is explicitly false by (3.3).
7. ODE existence, continuation, flowpipe coverage, true-DH/source equality, concrete `H/S/A/K_path`, Lean compile/axiom audit, comparator, provenance admission, P5/P8/M4 closure and registry state remain open.

## 10. Requested integration action

Add `V >= (3/125)||z||^2` as a source-independent child next to the `T-P5-034` `Q >= (15/16)V` leaf, then expose only the typed adapter

```text
ell2_Euclidean -> mu_V = (125/3) ell2_Euclidean.
```

For the incremental `Kc=1/12` route, let source checkers target

```text
34000 ell2 + 9792 nu < 225.
```

For the one-trajectory centered-plus-anchor route, use the fail-closed rational discriminant

```text
R = 225 - 34000 ell2 - 3264 B2,
R > 0,
R^2 > 443904000 ell2 B2,
```

with rational witness `theta_bal=R/(68000 ell2)` when `ell2>0`.  Keep all results `pending` until normal Lean/source/coverage/integration gates run.
