---
kind: review_result
review_id: review-T-P5-134-nonlinear-knot-tangent-remainder-absorption-guyuefangyuan-20260909T0732Z
task_id: T-P5-134-NONLINEAR-KNOT-TANGENT-REMAINDER-ABSORPTION
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T07:32:00Z
claim_commit: b75352bd0ca4a5b01378c91ffcfcf655da51df3f
inspected_commit: 60275eaef8b3a98cd4eaa28c6ac85d552020e498
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-130-REFERENCE-KNOT-RECENTER-RESET-guyuefangyuan-20260909T0630Z.md
    commit: 7c48ca222df55971d46c3a1ec6b37cdd5aba27c9
  - path: agent_review_inbox/review-T-P5-131-SHARP-PARAMETER-FREE-KNOT-RESET-kuangmanmozun-20260909T0642Z.md
    commit: bd54dbc6226fb2eeafcac3d233a709148af4b96f
  - path: agent_review_inbox/review-T-P5-132-BOUNDED-CELL-KNOT-RESET-honglianmozun-20260909T0658Z.md
    commit: a521dbad9a0c1dac213ed61e745dff9c2c54cc4f
  - path: agent_review_inbox/review-T-P5-133-REFERENCE-KNOT-CHART-SWITCH-COVARIANCE-liuguanyi-20260909T0710Z.md
    commit: 4eec908f938ea1e30e5f381d254c62b5e1b45ae1
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_root_free_tangent_secant_sandwich_and_bind_actual_same_key_C2_chart_remainder_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact quadratic-form, scalar-order, and FTC/Jensen algebra only
exit_code: n/a
---

# T-P5-134 — nonlinear knot tangent-remainder absorption

## 0. Narrow seam

T-P5-133 proves that at a nonlinear chart switch the true physical secant displacement is

`x = T(c+xi)-T(c) = Jbar(xi) xi`,

not the anchor tangent `J0 xi`.  It also isolates the exact remainder

`r = x - J0 xi = Integral_0^1 (1-s) D^2T(c+s xi)[xi,xi] ds`.

That review correctly says that a producer using only `J0` must charge this remainder.  The missing mathematical interface is: **how much does the remainder cost in the already-sharp T-P5-130/131/132 knot-reset envelope, and can the cost remain relative rather than becoming a coarse additive floor?**

This review closes exactly that seam.  The main result is that a genuinely second-order chart remainder can be converted into a root-free rational reduction of the reset curvature headroom.  The conversion needs a same-cell tangent-radius cap only to keep the secant/tangent metric distortion away from collapse.  The linear mismatch remainder is already second order and can be absorbed without that radius.

No actual chart/source binding, controller semantics, Float64/FD, P8 coverage, Lean receipt, independent verification, admission, or registry promotion is claimed.

---

## 1. Start from the physical sharp reset envelope

Let `P` be SPD and write

`Q(u) := u^T P u`,

`B_P(u,v) := u^T P v`.

At one reference knot retain the physical T-P5-130 envelope

**(1.1)**

`Wp <= Wm + p + ell*Qx + C`,

where

`Qx := Q(x)`,

`p := <g,x>`.

Assume the physical pre-knot coercivity

**(1.2)** `m*Qx <= Wm`, with `m>0`,

and choose the desired reset factor

**(1.3)** `kappa >= 1`.

Define, exactly as T-P5-131,

**(1.4)**

`A := m*(kappa-1)-ell`.

Then

**(1.5)**

`Wp-kappa*Wm <= p - A*Qx + C`.

This step is deliberately performed in physical coordinates **before** any tangent approximation.  Consequently this child does not need to replace the physical coercivity theorem by a new tangent coercivity theorem.

Assume also the physical dual and relocation packets

**(1.6)** `<g,u>^2 <= B*Q(u)` for all relevant `u`, with `B>=0`,

**(1.7)** `4*mu*C <= B`, with `mu>0`.

---

## 2. Exact tangent/secant decomposition

Let

`y := J0*xi`,

`r := x-y`.

Define

`q := Q(y)`,

`rho := Q(r)`,

`c := B_P(y,r)`,

`p0 := <g,y>`,

`pr := <g,r>`.

Then exactly

**(2.1)** `x=y+r`,

**(2.2)** `Qx=q+2*c+rho`,

**(2.3)** `p=p0+pr`.

The dual packet (1.6) gives

**(2.4)** `p0^2 <= B*q`,

**(2.5)** `pr^2 <= B*rho`.

The point is to reduce (1.5) to a new scalar envelope in `(q,p0)` while charging the secant remainder once and only once.

---

## 3. Root-free secant/tangent metric sandwich

Suppose a relative remainder parameter `delta` satisfies

**(3.1)** `0 <= delta <= 1`,

**(3.2)** `rho <= delta^2*q`.

Then

### Lemma A — exact quadratic sandwich

**(3.3)**

`(1-delta)^2*q <= Qx <= (1+delta)^2*q`.

The usual proof would invoke a norm triangle inequality and square roots.  Here there is a cleaner polynomial proof.

For `delta>0`, the lower difference satisfies the exact identity

**(3.4)**

`delta * [Qx-(1-delta)^2*q]`

` = Q(r+delta*y) + (1-delta)*(delta^2*q-rho) >= 0`.

Likewise the upper difference satisfies

**(3.5)**

`delta * [(1+delta)^2*q-Qx]`

` = Q(r-delta*y) + (1+delta)*(delta^2*q-rho) >= 0`.

For `delta=0`, (3.2) and SPD imply `r=0`, hence `Qx=q`.

Thus the trusted leaf uses only quadratic-form nonnegativity, multiplication, and order.  No square root or inverse is required.

### Sharpness

The factors are information-theoretically sharp.  If `r=-delta*y`, then the lower bound is equality; if `r=+delta*y`, the upper bound is equality.  No smaller symmetric distortion factor follows from only (3.2).

---

## 4. Second-order chart remainder producer and the sharp `1/4`

T-P5-133 gives

`r = Integral_0^1 (1-s) h(s) ds`,

where

`h(s) := D^2T(c+s*xi)[xi,xi]`.

Suppose a whole-segment source theorem gives the correlated Hessian-action bound

**(4.1)**

`Q(h(s)) <= H*q^2`

for every `s in [0,1]`, with `H>=0` and the same anchor-tangent energy `q=Q(J0 xi)`.

Weighted quadratic Jensen/Cauchy gives

`Q(r)`

` <= (Integral_0^1 (1-s) ds) * Integral_0^1 (1-s) Q(h(s)) ds`

` <= (1/2)*(H*q^2/2)`.

Therefore

### Lemma B — second-order remainder energy

**(4.2)**

`4*rho <= H*q^2`.

The factor `1/4` is sharp.  In one dimension take

`T(z)=z+(d/2)z^2`, `c=0`, `J0=1`.

Then `D^2T=d` is constant and

`r=(d/2)xi^2`,

so `4*rho=d^2*xi^4=H*q^2` with `H=d^2`.

Thus improving `1/4` requires extra signed/variation information about the chart Hessian; it cannot be obtained from the uniform action cap (4.1) alone.

---

## 5. Convert the quartic remainder to a relative metric distortion

Suppose the same tangent cell supplies

**(5.1)** `q <= R`, with `R>=0`.

Choose rational `delta` satisfying (3.1) and the single root-free gate

**(5.2)**

`H*R <= 4*delta^2`.

Then from (4.2),

`4*rho <= H*q^2 <= H*R*q <= 4*delta^2*q`,

hence (3.2).

So the complete metric-distortion producer needs only

`4*rho <= H*q^2`,

`q<=R`,

`H*R<=4*delta^2`.

All quantities can remain rational.  `delta` is merely a certificate tuning parameter; no checker-side square root of `H*R` is needed.

---

## 6. The linear chart remainder is cheaper: no radius is needed

The same second-order packet already gives a purely relative bound for `pr=<g,r>`.

From (2.5) and (4.2),

`4*pr^2 <= B*H*q^2`.

Choose `tau>=0` and check

**(6.1)**

`B*H <= 4*tau^2`.

Then

### Lemma C — linear remainder absorption

**(6.2)**

`pr <= tau*q`.

Proof: if `pr<=0`, the result is immediate since `tau*q>=0`.  If `pr>0`, (6.1) gives

`4*pr^2 <= 4*tau^2*q^2`,

and both sides have nonnegative square roots conceptually; equivalently, positive quantities comparable by squares give `pr<=tau*q`.  The theorem statement and source gate contain no square root.

Unlike the secant/tangent metric distortion, this step uses **no radius `R`**.  The reason is structural: `r=O(|xi|^2)` and the linear functional of `r` is therefore already `O(q)`.

The constant is sharp for the retained scalar information: in one dimension the dual inequality and (4.2) can both saturate, giving `pr/q = sqrt(BH)/2`.

---

## 7. Main theorem: chart nonlinearity becomes an effective-headroom tax

Return to

`Wp-kappa*Wm <= p-A*Qx+C`.

There are two sign branches for `A`.

### Branch I: `A>=0`

Use the lower sandwich (3.3):

`-A*Qx <= -A*(1-delta)^2*q`.

Together with `p=p0+pr` and Lemma C,

**(7.1)**

`Wp-kappa*Wm`

` <= p0 - [A*(1-delta)^2-tau]*q + C`.

Define

**(7.2)**

`Ahat := A*(1-delta)^2 - tau`.

Then the nonlinear physical reset has been reduced to exactly the T-P5-131 scalar form

**(7.3)**

`Wp-kappa*Wm <= p0-Ahat*q+C`,

with

`p0^2<=B*q`, `4*mu*C<=B`.

### Branch II: `A<=0`

Now `-A>=0`, so the upper sandwich is the sound direction:

`-A*Qx <= -A*(1+delta)^2*q`.

Define

**(7.4)**

`Ahat := A*(1+delta)^2 - tau`.

The same reduced envelope (7.3) follows.

### Theorem D — nonlinear tangent-remainder reduction

Under (1.1)-(1.7), the exact chart decomposition, the whole-segment second-order packet (4.2), tangent radius (5.1), and rational gates

`0<=delta<=1`,

`H*R<=4*delta^2`,

`tau>=0`,

`B*H<=4*tau^2`,

set

`A=m*(kappa-1)-ell`

and define `Ahat` by (7.2) if `A>=0`, or by (7.4) if `A<=0`.

Then (7.3) is valid.

This is the key closure: **chart nonlinearity need not be charged as an additive reset floor.  It first reduces the quadratic headroom from `A` to `Ahat`.**  Only the already-existing T-P5-131/132 scalar reset theorem decides whether an additive floor is then necessary.

The affine limit is exact: `H=0` permits `delta=tau=0`, hence `Ahat=A`, recovering T-P5-133 affine covariance with no tax.

---

## 8. Direct composition with T-P5-131

Because (7.3) has exactly the T-P5-131 scalar shape, its sharp global checker can be reused unchanged with `Ahat` in place of `A`.

If

**(8.1)** `Ahat>=0`,

and

**(8.2)**

`Ahat*(4*mu*E-B) >= B*mu`,

then

### Corollary E — global nonlinear-chart knot reset

**(8.3)**

`Wp <= kappa*Wm + E`.

For `B>0`, (8.2) automatically forces `Ahat>0`.  For `B=0`, the exact endpoint `Ahat=0,E=0` remains valid.

No new Young allocation is introduced: the only chart-side certificate knobs are `delta` and `tau`, both checked by square-cleared rational inequalities.

---

## 9. Direct composition with T-P5-132 bounded-cell branch

The reduced scalar state is now the **tangent energy** `q`, and the same packet already has `q<=R`.  Therefore T-P5-132 can be applied directly to `(q,p0,Ahat,R)`; one does not need to reconstruct or overapproximate the physical radius `Qx` first.

For the interior branch, if

`0<Ahat`

and

`B<=4*Ahat^2*R`,

use the T-P5-131 product gate (8.2).

For the boundary branch, if

`Ahat<=0`

or

`4*Ahat^2*R<=B`,

define

**(9.1)**

`S := 4*mu*E - B + 4*mu*Ahat*R`.

Then the exact T-P5-132 gates

**(9.2)** `S>=0`,

**(9.3)** `S^2>=16*mu^2*B*R`

imply again

`Wp<=kappa*Wm+E`.

This is particularly useful when chart nonlinearity pushes a formerly-positive physical `A` to `Ahat<=0`: a finite tangent cell can still rescue the reset exactly through the already-proved bounded-cell theorem.

---

## 10. Why the radius obligation cannot be deleted from second-order metric control

A second-order remainder bound by itself does **not** imply any globally positive lower comparison between the physical secant energy and the anchor-tangent energy.

Take one dimension on `z>=0`, `P=1`, and the smooth injective chart

**(10.1)**

`T(z)=z/(1+c*z)`, with `c>0`.

At the anchor `0`, `J0=1`, so

`y=z`, `q=z^2`.

The exact remainder is

`r=T(z)-z = -c*z^2/(1+c*z)`.

Hence

`rho = c^2*z^4/(1+c*z)^2 <= c^2*q^2`,

so the quartic packet (4.2) holds globally with, for example, `H=4*c^2`.

But

**(10.2)**

`Qx/q = [T(z)^2]/z^2 = 1/(1+c*z)^2 -> 0`

as `z->infinity`.

Therefore for every proposed constant `lambda>0`, the claim

`lambda*q <= Qx`

fails somewhere despite the uniform second-order remainder law.  Equivalently, when `A>0`, no theorem can retain a fixed positive fraction of `A` globally from the quartic remainder packet alone.

A bounded tangent radius, or an independently certified relative remainder `rho<=delta^2 q` with `delta<1`, is mathematically necessary to prevent secant collapse.  This is not a provenance or implementation issue.

Note that `T'(z)=1/(1+c*z)^2>0`; the obstruction is not created by a fold or a singular chart on the positive ray.

---

## 11. A stronger cancellation-preserving optional lane

The exact remainder in (1.5) can also be written

**(11.1)**

`p-A*Qx`

` = p0-A*q + <g-2*A*P*y,r> - A*rho`.

This identity is worth preserving in the producer.  The generic theorem above bounds the linear `pr` and metric distortion separately because those are available from the scalar packet `(B,H,R)`.

If an actual source/CSE lane can directly enclose the **combined signed remainder**

`<g-2*A*P*y,r> - A*rho`,

or its one-sided Gram data, that correlated packet can replace the generic `(delta,tau)` tax and may be much sharper.  In particular, a producer should form (11.1) before intervalizing whenever possible; separately taking absolute values of `pr`, `B_P(y,r)`, and `rho` can destroy cancellation.

This is a recommendation for the next source adapter, not a claim that such a packet currently exists.

---

## 12. Minimal Lean theorem decomposition

Recommended order:

1. `quadratic_secant_lower_of_remainder`
   - premises `0<=delta<=1`, `Q r <= delta^2*Q y`;
   - conclusion `(1-delta)^2*Q y <= Q (y+r)`;
   - use identity (3.4).

2. `quadratic_secant_upper_of_remainder`
   - same premises;
   - conclusion `Q(y+r) <= (1+delta)^2*Q y`;
   - use identity (3.5).

3. `second_order_chart_remainder_quarter`
   - FTC/Jensen leaf producing `4*Q r <= H*q^2` from the whole-segment Hessian-action cap.

4. `linear_remainder_absorb_quadratic`
   - from `pr^2<=B*rho`, `4*rho<=H*q^2`, `B*H<=4*tau^2`, prove `pr<=tau*q`.

5. `nonlinear_knot_tangent_reduction_pos`
   - `A>=0` branch, conclusion (7.1).

6. `nonlinear_knot_tangent_reduction_neg`
   - `A<=0` branch, conclusion using (7.4).

7. Thin specializations invoking the already-proved T-P5-131 and T-P5-132 scalar leaves with `Ahat`.

Leaves 1,2,4,5,6 are finite-dimensional/polynomial order algebra.  Only leaf 3 needs calculus/integration infrastructure.

---

## 13. Typed source contract suggested by this child

For a nonlinear normalized-only knot adapter, bind under one immutable knot/chart/reference identity:

- physical knot and pre/post reference keys from T-P5-130/133;
- physical SPD metric `P` and physical reset constants `m,B,mu,ell`;
- old-center coordinate `c`, state offset `xi`, anchor Jacobian `J0`;
- tangent energy `q=Q(J0 xi)` and tangent-cell cap `q<=R`;
- exact/validated `C^2` segment coverage `c+s xi`, `0<=s<=1`;
- Hessian-action producer for `Q(D^2T(c+s xi)[xi,xi])<=H*q^2`;
- rational `delta,tau` with `H*R<=4*delta^2` and `B*H<=4*tau^2`;
- branch sign for `A=m(kappa-1)-ell` and the derived `Ahat`;
- then the existing T-P5-131/132 scalar reset gate.

If the source can form the correlated expression (11.1) directly, prefer that over the generic separate tax.

The full nonlinear pullback Hessian connection term identified by T-P5-133 remains a separate obligation if a producer attempts to derive `ell` in normalized coordinates.  This child does **not** authorize dropping that term.  The cleanest lane is still to certify `ell` physically and use the present theorem only for secant/tangent state displacement.

---

## 14. Boundaries and non-claims

Still open:

1. actual deployed chart classification and `chartKey`;
2. same-knot physical state/reference binding;
3. actual whole-segment `D^2T` evaluator and `H`;
4. actual tangent radius `R` and coverage proving the segment stays in the certified chart cell;
5. source-bound physical `m,B,mu,ell` and relocation packet;
6. nonlinear pullback-Hessian connection evidence if `ell` is not kept physical;
7. controller/reference jump coupling and possible combined signed reset identity;
8. Float64/FD/controller/solve semantics;
9. P8 flowpipe and physical/reference/FD halo;
10. Lean/kernel receipt;
11. independent verification by 封不觉;
12. admission/registry/formal-certificate promotion.

Accordingly the status remains `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.

---

## 15. Integration recommendation

The mathematical consumer can now be organized in three layers:

1. **physical reset geometry** — T-P5-130/131/132;
2. **chart gluing/covariance** — T-P5-133;
3. **nonlinear tangent fallback** — this T-P5-134, used only when the producer cannot keep the exact physical secant but can certify a `C^2` remainder.

For affine charts, layer 3 collapses to zero cost.  For nonlinear charts, the trusted additional gates are just

`H*R <= 4*delta^2`,

`B*H <= 4*tau^2`,

plus the sign-selected definition of `Ahat`, after which the existing sharp T-P5-131/132 checker is reused unchanged.

This preserves the exact physical theorem as the canonical route while giving a sound, quantitative fallback for anchor-tangent implementations.
