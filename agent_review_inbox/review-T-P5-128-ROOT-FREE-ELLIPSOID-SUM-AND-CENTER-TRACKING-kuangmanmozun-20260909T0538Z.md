---
kind: review_result
review_id: review-T-P5-128-root-free-ellipsoid-sum-and-center-tracking-kuangmanmozun-20260909T0538Z
task_id: T-P5-128-ROOT-FREE-ELLIPSOID-SUM-AND-CENTER-TRACKING
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T05:38:00Z
claim_commit: 7671b2812f4cb890e3cf8980370606d8fdb5e74a
inspected_commit: 15f9c282aba85dbc10417416fe68973cb8ee10c8
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-125-STRONG-CONVEX-RECENTER-EXISTENCE-honglianmozun-20260909T0455Z.md
    commit: 119338bc1d5cc8ab789ce2bc9f55fd656dba3c29
  - path: agent_review_inbox/review-T-P5-127-MOVING-RECENTER-ENVELOPE-TRACKING-guyuefangyuan-20260909T0530Z.md
    commit: 8771585ea270185eaecabbcbef960b0fb2579a87
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_root_free_quadratic_sum_cap_and_replace_auxiliary_pq_center_tracking_gate_then_bind_actual_temporal_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact quadratic-form/order algebra only
exit_code: n/a
---

# T-P5-128 — sharp root-free ellipsoid-sum closure and tuning-free center tracking

## 0. Bottleneck selected

T-P5-127 closes moving-center drift with the bound

`4 mu^2 Q(q_*(t1)-q_*(t0)) <= G01`

and then keeps the new center inside an outer ellipsoid through an auxiliary weighted-sum gate using arbitrary positive tuning parameters `p,q`.

That gate is valid, but it leaves an avoidable proof-search knob and has an endpoint hole at exact equality when one of the two radius budgets vanishes. The same geometry already appears in T-P5-125's recentered-collar inclusion, where a root-free discriminant was written directly.

This review extracts the common sharp theorem once and specializes it back to center tracking. The result uses only addition, multiplication, squaring, and order comparisons. It has no square root, division, eigenvalue, inverse, or auxiliary Young parameter in the trusted statement.

This is a mathematical child only. No actual temporal source, reference schedule, chart, FD/controller semantics, coverage, Lean receipt, independent verification, admission, or registry promotion is claimed.

---

## 1. General quadratic-sum problem

Let `P` be symmetric positive definite and

`Q(x) := x^T P x`.

Let `S>0`, and suppose two vectors `a,b` satisfy

**(1.1)** `Q(a) <= A`,

**(1.2)** `S Q(b) <= G`,

with `A>=0`, `G>=0`.

We want a universal condition implying

**(1.3)** `Q(a+b) <= R`.

Define the polynomial slack

**(1.4)** `D := S (R-A) - G`.

The proposed gate is

**(1.5)** `D >= 0`,

**(1.6)** `D^2 >= 4 S A G`.

These two inequalities are the root-free form of the exact Minkowski-radius condition, but the proof below never introduces a square root.

---

## 2. Root-free proof of the quadratic-sum theorem

Write

`u := Q(a)`, `v := Q(b)`, `c := a^T P b`.

Quadratic Cauchy-Schwarz gives

**(2.1)** `c^2 <= u v`.

Now define the actual leftover before paying the cross term:

`E := S (R-u-v)`.

Using `u<=A` and `Sv<=G`,

`E`
` = [S(R-A)-G] + S(A-u) + (G-Sv)`
` = D + S(A-u) + (G-Sv)`.

Therefore

**(2.2)** `E >= D >= 0`.

Moreover,

`E^2 >= D^2 >= 4 S A G`.

Since `u<=A` and `Sv<=G`,

`S^2 u v <= S A G`.

Hence

**(2.3)** `E^2 >= 4 S^2 u v >= 4 S^2 c^2`.

If `c<=0`, then already

`Q(a+b)=u+v+2c <= u+v <= R`

because `E>=0`.

If `c>0`, both `E` and `2Sc` are nonnegative, so (2.3) implies

`E >= 2 S c`.

Thus

`S(R-u-v) >= 2Sc`,

and because `S>0`,

`R >= u+v+2c = Q(a+b)`.

Therefore:

### Theorem A — root-free quadratic-sum cap

If `Q(a)<=A`, `S Q(b)<=G`, `A,G>=0`, `S>0`, and

`D=S(R-A)-G >=0`,

`D^2 >= 4 S A G`,

then

**`Q(a+b) <= R`.**

No tuning parameter is needed.

---

## 3. Sharpness at the information level

The gate is not merely sufficient. For a nontrivial SPD space, the universal worst case under only (1.1)-(1.2) is attained when `a` and `b` are collinear in the same `P` direction and both budgets saturate.

In explanatory square-root notation only, the worst possible value is

`(sqrt(A) + sqrt(G/S))^2`.

Conditions (1.5)-(1.6) are exactly the root-free polynomial encoding of

`R >= (sqrt(A)+sqrt(G/S))^2`.

Thus if either polynomial condition fails, a same-direction one-dimensional realization violates the desired universal cap.

An exact rational regression avoids all irrational constants:

`S=1`, `A=1`, `G=4`, `a=1`, `b=2`.

Then the true worst-case sum energy is

`Q(a+b)=9`.

At `R=9`,

`D=9-1-4=4`,

`D^2=16=4*S*A*G`,

so the gate is exactly on the boundary and the physical inequality is exactly saturated.

At `R=899/100`,

`D=399/100`,

`D^2=159201/10000 < 160000/10000 = 4*S*A*G`,

while the same exact vectors still give `Q(a+b)=9>899/100`.

Therefore the discriminant threshold cannot be reduced under the present information model.

---

## 4. Relation to the T-P5-127 weighted `p,q` gate

T-P5-127 Section 4 uses positive `p,q` and checks

`(p+q)(S q A + p G) <= S p q R`.

With `t=p/q>0`, this becomes

`S A (1+1/t) + G(1+t) <= S R`.

For `A>0` and `G>0`, minimizing over `t>0` gives exactly the same sharp universal threshold as Theorem A. Thus the weighted gate is mathematically capable of reaching the optimum when an optimal tuning ratio is available.

However, the tuning-free discriminant has two advantages:

1. the checker does not need to search, optimize, or carry `p,q`;
2. it closes exact endpoint cases that no finite positive `p,q` can certify.

### Endpoint hole 1

Take

`S=1`, `A=0`, `G=1`, `R=1`.

Theorem A gives

`D=0`, `D^2=0`,

so the exact universal statement `Q(a+b)<=1` holds because `a=0` and `Q(b)<=1`.

But the weighted gate becomes

`p(p+q) <= p q`,

hence `p^2<=0`, impossible for any finite `p>0`.

### Endpoint hole 2

Take

`S=1`, `A=1`, `G=0`, `R=1`.

Again Theorem A passes exactly, while the weighted gate becomes

`q(p+q)<=pq`,

hence `q^2<=0`, impossible for finite `q>0`.

So the old gate is a sound sufficient family, but its finite-positive parameterization misses sharp equality at degenerate endpoints. This is a certificate-policy limitation, not a mathematical failure of the ellipsoid inclusion.

---

## 5. Direct specialization to T-P5-127 moving-center tracking

Use

`S := 4 mu^2`,

`a := q_*(t0)-c`,

`b := q_*(t1)-q_*(t0)`.

T-P5-127 supplies

`Q(a) <= R_in`,

`S Q(b) <= G01`.

Set

**(5.1)** `D_center := 4 mu^2 (R_out-R_in) - G01`.

Then the tuning-free finite-time tracking gate is

**(5.2)** `D_center >= 0`,

**(5.3)** `D_center^2 >= 16 mu^2 R_in G01`.

These imply

**(5.4)** `Q(q_*(t1)-c) <= R_out`.

This strictly improves the certificate interface of T-P5-127 Section 4: no `p,q` need be selected or source-bound.

If a positive certified collar `tau>0` is desired, simply replace `R_out` by `R_out-tau` in (5.1)-(5.3). Then the conclusion strengthens to

`Q(q_*(t1)-c) <= R_out-tau`,

which leaves an explicit rational reserve for chart/FD/source-segment coverage.

---

## 6. Direct time-step gate from a temporal-gradient envelope

T-P5-127 also notes that a time-strip dual bound may yield

`G01 <= h^2 Gdot`,

where `h=t1-t0`.

Theorem A can consume this upper envelope directly. Define

**(6.1)** `D_h := 4 mu^2 (R_out-R_in) - h^2 Gdot`.

A fully polynomial sufficient step-size condition is

**(6.2)** `D_h >= 0`,

**(6.3)** `D_h^2 >= 16 mu^2 R_in h^2 Gdot`.

Then the critical center remains in the outer ellipsoid over that two-time update, subject to the same source-valid time strip and same-cell hypotheses used to obtain the temporal-gradient packet.

This statement does not make the temporal packet sharp: conservatism in `Gdot` or in the time integral remains source-side. It only removes additional geometric/Young slack after `G01` has been bounded.

---

## 7. T-P5-125 collar theorem is the same lemma

T-P5-125 Section 7 has

`4 mu^2 Q(q_*-q0) <= B`

and wants every offset `y` with `Q(y)<=r` to satisfy

`Q((q_*-q0)+y) <= R`.

Apply Theorem A with

`S=4mu^2`, `A=r`, `G=B`, `a=y`, `b=q_*-q0`.

Then

`D = 4mu^2(R-r)-B`,

and the generic gate becomes exactly

`D>=0`,

`D^2 >= 16 mu^2 B r`.

Thus T-P5-125's recentered-collar inclusion and T-P5-127's moving-center tracking are not separate inequality patterns. They are one reusable quadratic-sum theorem with different semantic labels.

This is useful for formalization: one algebraic Lean leaf can serve both branches and prevents future coefficient drift.

---

## 8. Multi-knot / piecewise-reference recursion

For a piecewise reference schedule, suppose a sequence of center increments `b_k` satisfies

`S Q(b_k) <= G_k`

under one common metric/strong-convexity key on each certified transition.

Starting from a radius certificate `Q(a_0)<=R_0`, choose rational radii `R_1,...,R_N` such that for every step

`D_k := S(R_{k+1}-R_k)-G_k >=0`,

`D_k^2 >= 4 S R_k G_k`.

Then repeated application of Theorem A gives

`Q(a_0+b_0+...+b_{N-1}) <= R_N`.

No square-root accumulation and no per-step Young tuning parameter is required. If the bounds are saturated by collinear same-direction increments, the recursion is also worst-case sharp at each step.

This is the natural continuous-segment companion to the existing hybrid jump/dwell lane: smooth recenter motion can be tracked by the discriminant recursion, while actual discontinuous reference knots remain jump events and should continue to use the separate exact jump translation theorem.

---

## 9. Failure modes and semantic boundaries

### 9.1 Dropping the branch guard is unsound

The square condition alone is insufficient because squaring loses the sign of the leftover.

For example take `S=1`, `A=1`, `G=1`, `R=0`.

Then

`D=-2`, `D^2=4=4SAG`.

The squared condition passes, but with `a=b=1`,

`Q(a+b)=4>0=R`.

Therefore `D>=0` is mandatory.

### 9.2 Exceeding the gate is not a source failure

If a concrete source packet fails (5.2)-(5.3), that proves only

`NOT_CERTIFIED_BY_ROOT_FREE_QUADRATIC_SUM_GATE`

unless one also has a realizable source state whose two displacements align sufficiently to violate the outer radius. The theorem is sharp for the information class `(A,G)` but may be conservative for an actual source that contains signed correlation or directional restrictions.

### 9.3 Signed correlation can beat the universal cap

If source provides a direct upper bound

`a^T P b <= C`

with useful sign, the exact consumer should use

`Q(a+b) <= A + G/S + 2C`

(or a cleared-denominator equivalent) rather than discarding the correlation and using the worst-case Cauchy alignment. Theorem A is the correct fallback only when no stronger signed cross packet exists.

### 9.4 No coverage is created

The new gate combines two already-valid quadratic envelopes. It does not prove that the old center, new center, full chord, temporal strip, chart image, FD halo, or physical trajectory lies in the domain where those envelopes were established.

---

## 10. Minimal theorem statements for formalization

### Theorem A — `quadratic_sum_cap_root_free`

Assume an SPD quadratic form `Q`, `S>0`, `A>=0`, `G>=0`,

`Q a <= A`,

`S * Q b <= G`,

`D = S*(R-A)-G`,

`0 <= D`,

`4*S*A*G <= D^2`.

Then

`Q (a+b) <= R`.

### Theorem B — `critical_center_two_time_tracking_root_free`

Assume

`Q(q0-c)<=Rin`,

`4*mu^2*Q(q1-q0)<=G01`,

`mu>0`,

`D=4*mu^2*(Rout-Rin)-G01`,

`0<=D`,

`16*mu^2*Rin*G01<=D^2`.

Then

`Q(q1-c)<=Rout`.

### Theorem C — `critical_center_tracking_with_reserve`

Same as Theorem B after replacing `Rout` by `Rout-tau`; conclude

`Q(q1-c)<=Rout-tau`.

### Theorem D — `piecewise_center_radius_recursion`

Inductively consume Theorem A over a finite list of increments and certified radii.

The best implementation strategy is to prove Theorem A once in an abstract real inner-product/quadratic setting, then make B/C/D thin specializations.

---

## 11. Source-facing consequence

For the actual P5 moving-reference lane, the source packet does not need to invent rational `p,q` tuning witnesses. It should instead provide, under one reference/chart/cell key:

1. `mu>0` and the same metric `Q` used by the strong-Hessian theorem;
2. the old-center radius `R_in` relative to the fixed cell anchor;
3. the two-time temporal-gradient packet `G01`, or a time-strip packet giving `G01<=h^2 Gdot`;
4. the desired outer radius `R_out` and optional reserve `tau`;
5. same-cell/time-strip coverage for the premises themselves.

The trusted consumer then checks only the two polynomial inequalities (5.2)-(5.3), or their `tau` version.

If these fail, the next useful mathematical question is not another Young tuning search. It is whether source can provide signed alignment information between the old center offset and the new center drift, or a smaller same-key `G01`.

---

## 12. Final disposition

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending.**

The moving-center geometry now has a sharp tuning-free closure:

`D = 4mu^2(Rout-Rin)-G01`,

`D>=0`,

`D^2>=16mu^2 Rin G01`

implies

`Q(q_*(t1)-c)<=Rout`.

The same generic theorem exactly subsumes T-P5-125's recentered-collar discriminant, exposes the mandatory nonnegative branch guard, and removes the exact-endpoint holes of T-P5-127's finite-positive `p,q` certificate family. A reserve version and a piecewise-reference recursion follow without new analytic assumptions.

No actual source binding, domain coverage, Float64/controller semantics, Lean/kernel verification, independent review, admission, registry eligibility, or P5/P8 parent closure is upgraded by this result.