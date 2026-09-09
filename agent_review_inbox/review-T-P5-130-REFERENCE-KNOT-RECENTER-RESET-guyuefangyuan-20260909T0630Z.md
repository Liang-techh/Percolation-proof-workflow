---
kind: review_result
review_id: review-T-P5-130-reference-knot-recenter-reset-guyuefangyuan-20260909T0630Z
task_id: T-P5-130-REFERENCE-KNOT-RECENTER-RESET
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T06:30:00Z
claim_commit: 059a581140cf62946017798da46788b0ff5efa4c
inspected_commit: 037289456fd1dd877a7c46218bd578418f7e8529
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-108-hybrid-jump-dwell-recovery-guyuefangyuan-20260908T2320Z.md
    commit: e503f25e58a101782ae16dbdf4a128a7f1e2da59
  - path: agent_review_inbox/review-T-P5-127-MOVING-RECENTER-ENVELOPE-TRACKING-guyuefangyuan-20260909T0530Z.md
    commit: 8771585ea270185eaecabbcbef960b0fb2579a87
  - path: agent_review_inbox/review-T-P5-128-ROOT-FREE-ELLIPSOID-SUM-AND-CENTER-TRACKING-kuangmanmozun-20260909T0538Z.md
    commit: 274afb22d19b47aa467684899cdb6017c88c4bd9
  - path: agent_review_inbox/review-T-P5-129-MOVING-CHART-CENTER-TRACKING-COVARIANCE-liuguanyi-20260909T0615Z.md
    commit: 7bfca9b203efb1e1f27f218ecffd572d222ca58d
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_reference_knot_reset_and_multiplicative_headroom_step_then_bind_one_same_key_pre_post_reference_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional Taylor/strong-convexity/order algebra only
exit_code: n/a
---

# T-P5-130 — reference-knot recenter reset and multiplicative dwell recovery

## 0. Narrow seam selected

T-P5-127 treats a continuously moving strongly-convex potential-gap storage

`W(t,q) = F(t,q) - F(t,q_*(t))`

and shows that continuous center motion is already represented by the explicit-time term; one must not add a second independent `q_*dot` debit.

T-P5-128 and T-P5-129 then sharpen continuous center tracking and moving-chart geometry.

A different case remains at a genuine **reference/potential knot** where the storage definition itself changes discontinuously from a pre-knot potential `F-` to a post-knot potential `F+`. The physical state `q` can remain continuous while the critical center and potential-gap storage both jump.

This review proves the smallest exact reset interface for that event and connects it to T-P5-108's rational dwell recovery. The new feature is that a recentering knot generally produces both:

1. a multiplicative reset tax on the old storage; and
2. an additive center-relocation/reset floor.

The resulting headroom recurrence is therefore strictly more general than T-P5-108's `V+ <= V- + E` case.

No actual reference schedule, source packet, controller semantics, coverage, Float64 receipt, P8 flowpipe, Lean compile, independent verification, admission, or registry promotion is claimed.

---

## 1. Pre/post potential-gap storages

Work on one common convex physical cell. Let `Q(x)=x^T P x` for a fixed SPD matrix `P`.

At one reference knot let

`F-(q)` = pre-knot shaped potential,

`F+(q)` = post-knot shaped potential.

Let their critical centers be

`grad F-(q-) = 0`,

`grad F+(q+) = 0`.

Define the nonnegative potential-gap storages

`W-(q) := F-(q) - F-(q-)`,

`W+(q) := F+(q) - F+(q+)`.

Write

`DeltaF := F+ - F-`.

The physical state `q` is held fixed while evaluating the instantaneous storage reset.

### Exact reset identity

Add and subtract `F+(q-)` and `F-(q-)`:

`W+(q)-W-(q)`

` = [DeltaF(q)-DeltaF(q-)] + C+`,

where

`C+ := F+(q-) - F+(q+)`.

Thus

**(1.1)**

`W+ = W- + [DeltaF(q)-DeltaF(q-)] + C+`.

This identity is exact. It separates two genuinely different objects:

- the state-dependent change of potential around the old center;
- the post-potential energy saved by relocating from the old center `q-` to the new center `q+`.

If `F+` is strongly convex on the common cell and `q+` is its critical point there, then `C+>=0`.

---

## 2. Root-free bound for the center-relocation cost

Assume post-knot strong convexity on the whole segment from `q-` to `q+`:

**(2.1)**

`y^T Hess F+(z) y >= 2*mu*Q(y)`, `mu>0`.

Let

`delta := q+ - q-`,

`g := grad F+(q-)`.

Since `grad F-(q-)=0`, this is also

`g = grad DeltaF(q-)`.

Strong convexity gives

`F+(q+) >= F+(q-) + <g,delta> + mu Q(delta)`.

Therefore

**(2.2)**

`C+ <= -<g,delta> - mu Q(delta)`.

Assume a dual quadratic bound at the old center:

**(2.3)**

`<g,y>^2 <= B Q(y)`

for the needed directions, in particular for `y=delta`, with `B>=0`.

Put `a=<g,delta>` and `q0=Q(delta)`. Then `a^2<=B q0` and (2.2) reads

`C+ <= -a-mu q0`.

For `q0>0`, multiply the desired inequality by `q0` and use

`q0 [B + 4 mu a + 4 mu^2 q0]`

` = (B q0-a^2) + (a+2 mu q0)^2 >= 0`.

Hence

`4 mu(-a-mu q0) <= B`.

If `q0=0`, (2.3) forces `a=0`, while (2.2) and `C+>=0` force `C+=0`.

Therefore:

### Theorem A — center relocation cost

**(2.4)**

`4*mu*C+ <= B`.

No inverse Hessian, square root, eigenvalue, or division appears in the trusted statement.

Thus an exact rational reset budget `Ec>=0` is certified by the single gate

**(2.5)**

`B <= 4*mu*Ec`,

which implies `C+<=Ec`.

This is the discrete-knot analogue of T-P5-127's root-free center-tracking estimate, but now the quantity controlled is the **potential relocation cost**, not only the center displacement.

---

## 3. State-dependent change around the old center

Let

`x := q-q-`.

Taylor's formula along the physical segment `q- + s x` gives

**(3.1)**

`DeltaF(q)-DeltaF(q-)`

` = <g,x> + Integral_0^1 (1-s) x^T DeltaH(q-+s x) x ds`,

where

`DeltaH := Hess F+ - Hess F-`.

Assume the pre-knot storage controls displacement:

**(3.2)**

`m Q(x) <= W-(q)`, `m>0`.

Assume a one-sided signed Hessian-jump bound on the whole physical segment:

**(3.3)**

`x^T DeltaH(q-+s x) x <= 2*ell*Q(x)` for every `s in [0,1]`.

Then the integral remainder satisfies

`Integral_0^1 (1-s) ... ds <= ell Q(x)`.

Choose rational/nonnegative `eta` and check

**(3.4)**

`ell <= m*eta`.

Using (3.2), the quadratic jump contribution is then at most

`eta W-`.

### Linear jump contribution

From the same dual packet (2.3),

`<g,x>^2 <= B Q(x)`.

Choose `alpha>0`, `El>=0` and check the root-free gate

**(3.5)**

`B <= 4*m*alpha*El`.

Then

**(3.6)**

`<g,x> <= alpha W- + El`.

A purely algebraic proof is enough. If `<g,x><=0`, the result is immediate. Otherwise (2.3), (3.2), and (3.5) imply

`<g,x>^2 <= 4 alpha El W-`.

But

`(alpha W- + El)^2 - 4 alpha El W-`

` = (alpha W- - El)^2 >= 0`,

and both sides being compared are nonnegative.

Therefore (3.1)-(3.6) yield

**(3.7)**

`DeltaF(q)-DeltaF(q-) <= (alpha+eta) W- + El`.

---

## 4. Complete knot reset theorem

Combine the exact identity (1.1), the relocation gate (2.5), and (3.7).

Define

`kappa := 1 + alpha + eta`,

`E := El + Ec`.

Then:

### Theorem B — reference-knot recenter reset

Under the same-cell assumptions above and gates

`B <= 4*mu*Ec`,

`B <= 4*m*alpha*El`,

`ell <= m*eta`,

we have

**(4.1)**

`W+(q) <= kappa W-(q) + E`.

The checker-facing packet can therefore be entirely rational once source has supplied `m,mu,B,ell` and chosen `alpha,eta,El,Ec`.

Unlike T-P5-108's additive-only reset, a changing potential generally gives `kappa>1`. The multiplicative term is not cosmetic: it represents the state-dependent change in the storage definition at the knot.

---

## 5. Sharp translation example: the additive floor is real

Consider one dimension with `Q(x)=x^2` and

`F-(x)=mu*x^2`,

`F+(x)=mu*(x-a)^2`,

where `mu>0`, `a!=0`.

Then

`q-=0`, `q+=a`,

`W-(x)=mu*x^2`,

`W+(x)=mu*(x-a)^2`.

The Hessians are identical, so

`ell=0`, `eta=0`.

At the old center

`g=-2 mu a`,

and the exact dual constant is

`B=4 mu^2 a^2`.

The relocation cost is

`C+=mu a^2 = B/(4 mu)`,

so Theorem A is exactly saturated.

Now ask for a reset inequality with a prescribed multiplicative factor `1+alpha`, `alpha>0`:

`W+(x) <= (1+alpha)W-(x)+E` for all `x`.

The required additive budget is the maximum of

`W+-(1+alpha)W-`

` = mu a^2 - 2 mu a x - alpha mu x^2`.

The maximum occurs at `x=-a/alpha` and equals

**(5.1)**

`E_min = mu a^2 (1 + 1/alpha)`.

Our two gates give exactly

`Ec_min = B/(4mu) = mu a^2`,

`El_min = B/(4*m*alpha) = mu a^2/alpha`,

because here `m=mu`.

Hence

`Ec_min+El_min = E_min`.

So the apparent twofold use of the center-gradient defect `B` is not an artifact of separate Young inequalities. Under this information model it is **sharp**: one piece pays relocation of the minimum, and the other pays the state-dependent linear reset around the old center.

This also proves a hard obstruction:

> if the reference center jumps (`a!=0`), no finite uniform purely homogeneous reset `W+<=kappa W-` can hold for any finite `kappa`, because at the old center `W-(q-)=0` while `W+(q-)=mu a^2>0`.

A genuine center jump therefore requires an additive reset floor unless one changes the event semantics or proves a special signed cancellation from richer source structure.

---

## 6. Generalized positive-excess reset

T-P5-108 works with the positive excess above a continuous-flow base collar `R0`:

`A(W) := max(W-R0,0)`.

Suppose a knot satisfies the new multiplicative/additive reset

`W+ <= kappa W- + E`,

with

`kappa>=1`, `E>=0`, `R0>=0`.

Since

`W- <= R0 + A(W-)`,

we obtain

`W+ - R0`

` <= kappa A(W-) + (kappa-1)R0 + E`.

The right side is nonnegative, so taking positive parts gives

### Theorem C — excess reset with multiplicative tax

**(6.1)**

`A+ <= kappa A- + J0`,

where

**(6.2)**

`J0 := (kappa-1)R0 + E`.

This identifies a second cost that does not appear in additive-only T-P5-108: even if `E=0`, a multiplicative storage change consumes `(kappa-1)R0` units of positive-excess budget relative to the old base collar.

---

## 7. Exact rational dwell recovery with `kappa>1`

Assume a continuous dwell of duration `h` before the next knot satisfies the T-P5-108 rational excess-decay certificate

**(7.1)**

`P * A- <= QN * A0`,

where

`P := (N+nu*h)^N`,

`QN := N^N`,

`N>=1`, `nu>0`, `h>=0`.

Assume the post-event headroom invariant starts with

`A0<=H`, `H>=0`.

Then (7.1) and Theorem C give

`A+ <= kappa*(QN/P)*H + J0`.

Avoid division by checking directly:

### Theorem D — multiplicative hybrid headroom gate

**(7.2)**

`kappa*QN*H + P*J0 <= P*H`.

Under positivity of `P`, this implies

**(7.3)**

`A+<=H`.

Equivalently, after substituting (6.2), the single exact gate is

**(7.4)**

`P * ((kappa-1)R0 + E)`

` <= (P-kappa*QN) * H`.

For `kappa=1`, this reduces exactly to T-P5-108:

`P E <= (P-QN)H`.

Thus T-P5-108 is the additive-reset boundary case of the present theorem.

### Specialization to `nu=9/20`

Using the integer-scaled factors from T-P5-108,

`P20 := (20*N + 9*h)^N`,

`Q20 := (20*N)^N`,

the gate is

**(7.5)**

`kappa*Q20*H + P20*((kappa-1)R0+E) <= P20*H`.

For `N=1`, this is

**(7.6)**

`(20+9h)*((kappa-1)R0+E)`

` <= (9h - 20*(kappa-1))*H`.

Hence a visible necessary condition for any positive reset room at `N=1` is

`9h >= 20*(kappa-1)`.

This is the rational-certificate version of the intuitive requirement that continuous contraction during the dwell must first recover the multiplicative storage expansion before it can recover additive reset energy.

---

## 8. Structural obstruction: zero dwell cannot repair a true multiplicative reset

At `h=0`, the rational flow factors satisfy `P=QN`.

Then (7.2) becomes

`kappa*P*H + P*((kappa-1)R0+E) <= P*H`.

After removing the positive common factor,

`(kappa-1)(H+R0) + E <= 0`.

For `kappa>1` with any positive headroom/base radius, or for `E>0`, this is impossible.

Therefore no proof-search tuning can hide a genuine storage-definition jump at zero dwell. A schedule with arbitrarily rapid reference knots needs one of the following:

1. a storage representation whose knot reset has `kappa=1,E=0` by exact signed semantics;
2. a nonzero minimum dwell;
3. a varying headroom schedule rather than a fixed invariant collar;
4. stronger signed pre/post potential information that reduces the reset before absolute bounding.

This is a mathematical obstruction, not a source/provenance issue.

---

## 9. Interaction with T-P5-107 input-value jumps

T-P5-107 already distinguishes a continuous slope corner from a genuine input-value jump and derives a physical storage reset budget for the latter.

The present theorem concerns a different typed object: a **change in the potential-gap/recentered storage definition** at a reference knot.

If, in the actual implementation, the controller input jump and the pre/post potential change are generated by the same `referenceKey`, they must not automatically be charged as two unrelated resets. The source lane should first derive one same-key exact pre/post storage identity and then decide whether T-P5-107's `E_input` and the present `(kappa,E)` are:

- two provably independent components that add;
- two descriptions of the same physical reset, in which case adding them would double-count; or
- partially correlated signed terms that should be combined before intervalization.

The mathematics here intentionally leaves that semantic binding open.

---

## 10. Coverage obligations exposed

The reset theorem needs more than endpoint values.

To consume (2.1), (3.1), and (3.3), source/coverage must bind one common knot packet containing at least:

- pre/post `referenceKey` and knot time/order;
- `F-`, `F+`, their critical centers `q-`, `q+`;
- one common physical `Q`/normalization;
- post strong-convexity constant `mu` along `q- -> q+`;
- pre coercivity `m Q(q-q-) <= W-(q)` on the reset source region;
- old-center gradient mismatch `g=grad F+(q-)=grad DeltaF(q-)` and dual bound `B`;
- signed Hessian-jump upper bound `ell` along every segment `q- -> q` used by the reset region;
- proof that these physical segments remain inside the same certified cell/domain;
- the continuous-flow base collar/rate `(R0,nu)` and actual dwell for the next headroom step.

For a moving nonlinear chart, these should first be formulated in physical coordinates or transported with the already established exact chart semantics. A chart-space straight segment must not silently replace the required physical segment unless path equivalence/coverage is proved.

---

## 11. Suggested Lean leaves

The useful order is to formalize the scalar algebra before any calculus/source specialization.

### Leaf 1 — center relocation algebra

```lean
theorem center_relocation_cost
    (mu B q a C : ℝ)
    (hmu : 0 < mu) (hB : 0 <= B) (hq : 0 <= q)
    (hdual : a^2 <= B*q)
    (hCnonneg : 0 <= C)
    (hC : C <= -a - mu*q) :
    4*mu*C <= B := by
  ...
```

The proof can split `q=0` / `q>0`; the positive branch uses

`(B*q-a^2) + (a+2*mu*q)^2 >= 0`.

### Leaf 2 — linear knot absorption

```lean
theorem knot_linear_absorption
    (m B alpha El Qx W p : ℝ)
    (hm : 0 < m) (ha : 0 < alpha)
    (hEl : 0 <= El) (hQ : 0 <= Qx) (hW : 0 <= W)
    (hcoer : m*Qx <= W)
    (hdual : p^2 <= B*Qx)
    (hgate : B <= 4*m*alpha*El) :
    p <= alpha*W + El := by
  ...
```

### Leaf 3 — multiplicative excess reset

```lean
theorem positive_excess_after_affine_reset
    (kappa E R0 Wm Wp : ℝ)
    (hk : 1 <= kappa) (hE : 0 <= E) (hR : 0 <= R0)
    (hreset : Wp <= kappa*Wm + E) :
    max (Wp-R0) 0 <=
      kappa * max (Wm-R0) 0 + (kappa-1)*R0 + E := by
  ...
```

### Leaf 4 — multiplicative hybrid headroom step

```lean
theorem hybrid_headroom_step_affine
    (P QN kappa H R0 E A0 Am Ap : ℝ)
    (hP : 0 < P) (hQN : 0 <= QN)
    (hk : 1 <= kappa) (hH : 0 <= H)
    (hflow : P*Am <= QN*A0)
    (hA0 : A0 <= H)
    (hjump : Ap <= kappa*Am + (kappa-1)*R0 + E)
    (hgate : kappa*QN*H + P*((kappa-1)*R0+E) <= P*H) :
    Ap <= H := by
  ...
```

The full Taylor/strong-convexity theorem can be added later once the source packet fixes the finite-dimensional calculus representation.

---

## 12. Result and next mathematical/source action

**Result:** `CONDITIONAL_PASS / pending mathematical child`.

The new closed mathematical interface is:

1. exact reference-knot reset identity (1.1);
2. root-free center-relocation gate `B <= 4 mu Ec`;
3. root-free state-dependent reset gates `B <= 4 m alpha El` and `ell <= m eta`;
4. affine reset `W+ <= (1+alpha+eta)W- + El+Ec`;
5. exact multiplicative dwell/headroom gate (7.2)/(7.5);
6. a sharp translation example proving the additive floor and the two `B`-charges are genuine under the present information model.

The highest-value next source task is now very concrete: bind one actual pre/post reference-knot packet under the same key and determine whether the real schedule has (i) continuous potential with only slope changes, (ii) a genuine center/potential jump, or (iii) a correlated controller+potential jump requiring one combined signed reset identity.

Still open and not claimed here: actual source binding, same-cell segment coverage, real knot/dwell values, controller/FD/Float64 semantics, P8 flowpipe, Lean/kernel closure, independent verification by 封不觉, admission, and registry promotion.
