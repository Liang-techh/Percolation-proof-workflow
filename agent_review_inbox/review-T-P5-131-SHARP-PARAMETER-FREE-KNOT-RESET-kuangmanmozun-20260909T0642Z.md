---
kind: review_result
review_id: review-T-P5-131-sharp-parameter-free-knot-reset-kuangmanmozun-20260909T0642Z
task_id: T-P5-131-SHARP-PARAMETER-FREE-KNOT-RESET
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T06:42:00Z
claim_commit: 08f9d9c605a208d9c3032a2bd72cd2894b79813f
inspected_commit: 7c48ca222df55971d46c3a1ec6b37cdd5aba27c9
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-130-REFERENCE-KNOT-RECENTER-RESET-guyuefangyuan-20260909T0630Z.md
    commit: 7c48ca222df55971d46c3a1ec6b37cdd5aba27c9
  - path: agent_review_inbox/review-T-P5-128-ROOT-FREE-ELLIPSOID-SUM-AND-CENTER-TRACKING-kuangmanmozun-20260909T0538Z.md
    commit: 274afb22d19b47aa467684899cdb6017c88c4bd9
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_parameter_free_reset_leaf_then_bind_actual_same_key_reference_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact scalar/quadratic-form algebra only
exit_code: n/a
---

# T-P5-131 — sharp parameter-free reference-knot reset

## 0. Narrow seam

T-P5-130 proves a sound reference-knot reset by introducing four auxiliary budget variables

`alpha > 0`, `eta >= 0`, `El >= 0`, `Ec >= 0`,

with

`kappa = 1 + alpha + eta`,

`B <= 4 mu Ec`,

`B <= 4 m alpha El`,

`ell <= m eta`.

That interface is useful, but for a fixed physically meaningful multiplicative reset factor `kappa` it still leaves an artificial budget-allocation problem. It also throws away a favorable signed Hessian jump when `ell < 0`, because `eta` is constrained to be nonnegative.

This review analytically eliminates `alpha, eta, El, Ec`. The resulting checker gate is root-free, division-free, sharp under exactly the scalar information retained by T-P5-130, and endpoint-safe. It also eliminates the additive reset budget from the subsequent dwell/headroom step.

No actual reference schedule, source reification, same-cell coverage, controller/FD/Float64 semantics, P8 flowpipe, Lean receipt, independent verification, admission, or registry promotion is claimed.

---

## 1. Abstract reset envelope inherited from T-P5-130

Let `Qx >= 0` denote the physical displacement quadratic energy `Q(q-q-)`. Let

`Wm := W-(q)`,

`Wp := W+(q)`.

T-P5-130's exact reset identity plus its one-sided Taylor bound and center-relocation estimate reduce the calculus to the following scalar premises.

Assume

**(1.1) pre-knot coercivity**

`m Qx <= Wm`, with `m > 0`.

Let

`p := <g,q-q->`.

Assume the dual packet

**(1.2)**

`p^2 <= B Qx`, with `B >= 0`.

Let `C` denote the center-relocation contribution. T-P5-130 proves

**(1.3)**

`4 mu C <= B`, with `mu > 0`.

Let `ell` be the signed one-sided Hessian-jump coefficient on the physical segment. The complete reset envelope is

**(1.4)**

`Wp <= Wm + p + ell Qx + C`.

Important: `ell` is signed. A negative `ell` is useful curvature and should not be replaced by zero unless the source packet has already lost the sign.

Choose the desired multiplicative reset factor

`kappa >= 1`.

Define the **curvature headroom**

**(1.5)**

`A := m (kappa-1) - ell`.

The quantity `A` is the exact quadratic reserve left after paying the signed Hessian jump.

---

## 2. A root-free sharp linear-minus-quadratic lemma

The key scalar subproblem is to control

`p - A Qx`

from only

`Qx >= 0`, `p^2 <= B Qx`, `A >= 0`.

When `A > 0`, the sharp bound is

**(2.1)**

`4 A (p - A Qx) <= B`.

This needs no square root. If `Qx=0`, (1.2) forces `p=0`, so (2.1) is immediate. If `Qx>0`, use the exact identity

**(2.2)**

`Qx * [B - 4 A p + 4 A^2 Qx]`

` = (B Qx - p^2) + (p - 2 A Qx)^2 >= 0`.

Since `Qx>0`, the bracket is nonnegative, which is exactly (2.1).

This is the same completed-square geometry that sits underneath Young's inequality, but here the tuning parameter has already been optimized away.

---

## 3. Main theorem: no `alpha/eta/El/Ec`

Assume (1.1)-(1.4), `kappa>=1`, `E>=0`, and define `A` by (1.5).

Check only the two polynomial gates

**(3.1)**

`A >= 0`,

and

**(3.2)**

`A * (4 mu E - B) >= B mu`.

Then

### Theorem A — parameter-free reference-knot reset

**(3.3)**

`Wp <= kappa Wm + E`.

### Proof

Because `kappa-1>=0`, coercivity gives

`-(kappa-1) Wm <= -m(kappa-1) Qx`.

Combining with (1.4),

**(3.4)**

`Wp - kappa Wm <= p - A Qx + C`.

There are two branches.

#### Branch B=0

From `p^2 <= B Qx=0`, `p=0`. From `4 mu C <= 0` and `mu>0`, `C<=0`. With `A>=0`, (3.4) gives

`Wp-kappa Wm <= -A Qx + C <= 0 <= E`.

So the exact endpoint `A=0,B=0,E=0` is valid.

#### Branch B>0

Gate (3.2), together with `mu>0` and `A>=0`, forces `A>0`. By (2.1),

`4 A (p-A Qx) <= B`.

Multiply by `mu` and add `A*(4 mu C <= B)`:

**(3.5)**

`4 mu A (p-A Qx+C) <= B(mu+A)`.

But (3.2) is exactly

`4 mu A E >= B(A+mu)`.

Therefore

`p-A Qx+C <= E`.

Together with (3.4), this proves (3.3).

The trusted statement requires only addition, multiplication, squaring/order premises already present upstream, and two new scalar polynomial comparisons. There is no square root, division, inverse Hessian, eigenvalue, or Young parameter.

---

## 4. Equivalent minimum additive floor and information-theoretic sharpness

For interpretation only, if `B>0` and `A>0`, gate (3.2) is equivalent to

**(4.1)**

`E >= E_min := B/(4A) + B/(4mu)`

` = B(A+mu)/(4 mu A)`.

The two terms have the same physical meanings identified in T-P5-130:

- `B/(4mu)` pays relocation of the post-knot minimum;
- `B/(4A)` pays the worst state-dependent linear mismatch after the signed Hessian jump has consumed part of the multiplicative reserve.

The new result is not claiming those two effects disappear. It proves that their **optimal total** can be checked without introducing four auxiliary allocations.

### Sharp scalar-envelope witness

Fix any `B>0`, `A>0`, `m>0`, `mu>0`, and choose `kappa,ell` so that `A=m(kappa-1)-ell`. Set

`Qx = B/(4 A^2)`,

`Wm = m Qx`,

`p = B/(2A)`,

`C = B/(4mu)`,

and take (1.4) at equality.

Then

`p^2 = B Qx`,

`4mu C = B`,

and

**(4.2)**

`Wp-kappa Wm = B/(4A) + B/(4mu) = E_min`.

Hence no smaller universal additive floor can be proved from only (1.1)-(1.4). The gate is sharp for the retained information model.

---

## 5. Exact quadratic-potential saturation example

The sharpness is not merely an abstract scalar construction. A genuine one-dimensional strongly-convex potential family saturates it.

Let

`Q(x)=x^2`,

`F-(x)=m x^2`,

`F+(x)=mu x^2 + g x`,

where

`m>0`, `mu>0`, and define

`ell := mu-m`.

Then

`q-=0`,

`q+=-g/(2mu)`,

`B=g^2`,

`W-(x)=m x^2`,

`W+(x)=mu x^2 + g x + g^2/(4mu)`.

The Hessian jump is exactly `2ell`, post strong convexity is exactly `2mu`, and the relocation bound is saturated.

For any `kappa>=1`, define

`A=m(kappa-1)-ell`.

Then exactly

**(5.1)**

`W+(x)-kappa W-(x)`

` = g x - A x^2 + B/(4mu)`.

If `A>0`, the maximum occurs at `x=g/(2A)` and equals (4.1). Thus Theorem A is sharp even inside the intended potential-gap geometry.

### Concrete rational regression

Take

`m=1`, `ell=-1/2`, `mu=1/2`, `g=1`, `B=1`, `kappa=1`.

Then

`A=1/2`,

and Theorem A gives the exact minimum

`E=1`.

Indeed

`W-(x)=x^2`,

`W+(x)=(1/2)x^2+x+1/2`,

so

**(5.2)**

`W+(x)-W-(x) = -(1/2)x^2+x+1/2 <= 1`,

with equality at `x=1`.

This example matters because T-P5-130's parameterization forces

`kappa=1+alpha+eta > 1`

whenever `alpha>0` and `eta>=0`. It therefore cannot hit this valid `kappa=1` branch. The signed negative Hessian jump supplies enough quadratic reserve to absorb the linear mismatch without any multiplicative tax above one.

---

## 6. Relation to the T-P5-130 split

When `ell>=0` and

`kappa > 1 + ell/m`,

T-P5-130 can attain the same optimum by choosing

`eta = ell/m`,

`alpha = kappa-1-ell/m = A/m`,

`Ec = B/(4mu)`,

`El = B/(4m alpha) = B/(4A)`.

So Theorem A is the **analytic elimination** of the optimal T-P5-130 allocation in that branch, not a contradiction to it.

The new gate is strictly stronger in two important endpoint/sign regimes:

1. if `ell<0`, it preserves the favorable signed curvature instead of truncating it through `eta>=0`;
2. if `B=0,A=0`, it certifies the exact endpoint with `E=0`, whereas the old `alpha>0` split only approaches that endpoint.

---

## 7. Hard obstructions: why the `A` branch cannot be deleted

The nonnegative curvature-headroom condition is structural, not checker decoration.

### 7.1 `A<0`: quadratic blow-up

Take the quadratic family of Section 5 with `g=0`, hence `B=0`. Then

`W+-kappa W- = -A x^2`.

If `A<0`, this is unbounded above on the valid convex domain `R`. Therefore no finite uniform additive `E` follows from the present envelope information.

### 7.2 `A=0,B>0`: linear blow-up

In the same family with `g!=0`,

`W+-kappa W- = g x + B/(4mu)`.

This is unbounded above. Hence when `B>0`, finite global closure requires **strict** `A>0`; Theorem A obtains that strictness automatically from (3.2).

### 7.3 bounded-cell caveat

These are information-theoretic obstructions for the current envelope, which contains no independent radius cap. If an actual source packet additionally proves

`Qx <= Rcell`,

then an `A<=0` branch may still be closable by a radius-dependent estimate. Such a repair is a different theorem and must carry the same-cell radius as an explicit premise. The present obstruction must not be upgraded to an impossibility claim for every bounded physical cell.

---

## 8. Eliminate `E` from the subsequent dwell/headroom gate

T-P5-130 next combines an affine reset with a rational dwell certificate. Its checker gate has the form

**(8.1)**

`kappa QN H + P((kappa-1)R0 + E) <= P H`,

where `P>0`, `QN>=0`, `H>=0`, `R0>=0` and the flow packet proves

`P Am <= QN A0`, `A0<=H`.

For a fixed `kappa`, define the available additive reset capacity

**(8.2)**

`J := P H - kappa QN H - P(kappa-1)R0`.

Instead of selecting `E` and then testing (8.1), check the following **division-free combined gates**:

**(8.3)**

`J >= 0`,

**(8.4)**

`A >= 0`,

**(8.5)**

`A * (4 mu J - B P) >= B mu P`.

These gates are exactly Theorem A evaluated at the largest additive reset amount permitted by the dwell step, `E=J/P`, with the denominator cleared. Therefore they certify that some nonnegative reset floor fits inside the available dwell headroom, and the T-P5-130 hybrid step closes.

For `B>0,A>0`, the combined condition is also sharp under the same independent-envelope model: the reset needs at least `E_min`, while the dwell gate permits at most `J/P`; (8.5) is exactly the cleared inequality

`J/P >= E_min`.

Thus a checker can now scan only the semantically meaningful scalar `kappa`. It no longer needs to tune `alpha,eta,El,Ec,E`.

With T-P5-130's integerized dwell notation, simply substitute its exact rational/integer `P,QN` (for example `P20,Q20`) into (8.2)-(8.5). No new transcendental arithmetic is introduced.

---

## 9. Lean-friendly theorem shape

The mathematical core should be formalized first as a scalar leaf, independent of the potential calculus:

```lean
-- Schematic statement; names/types can be adapted to the existing sidecar.
theorem knot_reset_parameter_free
    (m mu B ell kappa E Qx Wm Wp p C : ℝ)
    (hm : 0 < m) (hmu : 0 < mu)
    (hB : 0 <= B) (hE : 0 <= E) (hQ : 0 <= Qx)
    (hk : 1 <= kappa)
    (hcoer : m*Qx <= Wm)
    (hdual : p^2 <= B*Qx)
    (hreloc : 4*mu*C <= B)
    (hreset : Wp <= Wm + p + ell*Qx + C)
    (hA : 0 <= m*(kappa-1)-ell)
    (hgate :
      (m*(kappa-1)-ell) * (4*mu*E-B) >= B*mu) :
    Wp <= kappa*Wm + E := by
  ...
```

A useful helper leaf is the root-free identity from Section 2:

```lean
theorem linear_minus_quadratic_root_free
    (A B Qx p : ℝ)
    (hA : 0 < A) (hB : 0 <= B) (hQ : 0 <= Qx)
    (hdual : p^2 <= B*Qx) :
    4*A*(p-A*Qx) <= B := by
  ...
```

The proof should explicitly split `Qx=0` versus `Qx>0` and use

`Qx*(B-4*A*p+4*A^2*Qx)
 = (B*Qx-p^2)+(p-2*A*Qx)^2`.

This avoids importing square-root or norm machinery.

A second thin specialization can encode (8.2)-(8.5) for the hybrid dwell consumer. No actual source constants should be hard-coded into the mathematical leaf.

---

## 10. Result and next action

**Result: `CONDITIONAL_PASS / pending mathematical child`.**

The closed mathematical interface is now:

1. retain T-P5-130's actual calculus/source premises through the scalar reset envelope (1.1)-(1.4);
2. choose only the semantic multiplicative factor `kappa>=1`;
3. compute `A=m(kappa-1)-ell`;
4. for a standalone reset, check `A>=0` and `A(4mu E-B)>=Bmu`;
5. for reset+dwell, compute `J=PH-kappa QN H-P(kappa-1)R0` and check `J>=0`, `A>=0`, `A(4mu J-BP)>=Bmu P`;
6. preserve the exact endpoint `B=0,A=0` and the favorable `ell<0` branch;
7. if `A<0` or `A=0<B`, do not call the current envelope globally closed unless an explicit bounded-cell radius or richer signed correlation is added.

Highest-value next source step remains disjoint from this review: bind one actual same-key pre/post reference packet and provide exact `m,mu,B,ell` plus the real dwell data. Once those numbers exist, the new gate reduces the reset feasibility test to a one-scalar rational search in `kappa`.

Still open and explicitly not claimed: actual source binding, same-cell segment coverage, real knot/reference semantics, controller/FD/Float64 effects, P8 flowpipe, Lean/kernel compile, independent verification by 封不觉, admission, registry eligibility, or P5/M4 parent closure.
