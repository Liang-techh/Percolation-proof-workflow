---
kind: review_result
review_id: review-T-P5-135-physical-secant-radius-no-curvature-tax-kuangmanmozun-20260909T0743Z
task_id: T-P5-135-PHYSICAL-SECANT-RADIUS-NO-CURVATURE-TAX
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T07:43:00Z
claim_commit: 70ebc31bb236df32e7f34edd1e104692b88c166b
inspected_commit: 35a0d7c09d9aa52580e20f3afd5b81218b25139f
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-128-ROOT-FREE-ELLIPSOID-SUM-AND-CENTER-TRACKING-kuangmanmozun-20260909T0538Z.md
    commit: 274afb22d19b47aa467684899cdb6017c88c4bd9
  - path: agent_review_inbox/review-T-P5-131-SHARP-PARAMETER-FREE-KNOT-RESET-kuangmanmozun-20260909T0642Z.md
    commit: bd54dbc6226fb2eeafcac3d233a709148af4b96f
  - path: agent_review_inbox/review-T-P5-132-BOUNDED-CELL-KNOT-RESET-honglianmozun-20260909T0658Z.md
    commit: a521dbad9a0c1dac213ed61e745dff9c2c54cc4f
  - path: agent_review_inbox/review-T-P5-133-REFERENCE-KNOT-CHART-SWITCH-COVARIANCE-liuguanyi-20260909T0710Z.md
    commit: 4eec908f938ea1e30e5f381d254c62b5e1b45ae1
  - path: agent_review_inbox/review-T-P5-134-NONLINEAR-KNOT-TANGENT-REMAINDER-ABSORPTION-guyuefangyuan-20260909T0732Z.md
    commit: 18b13382a2a71d0d985071c63287909a25284478
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_sharp_tangent_to_physical_secant_radius_leaf_and_prefer_direct_physical_reset_consumer_when_physical_dual_coercivity_are_available
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact quadratic-form and scalar polynomial algebra only
exit_code: n/a
---

# T-P5-135 — sharp physical-secant radius and no-curvature-tax reset lane

## 0. Narrow seam

T-P5-133 identifies the correct nonlinear displacement

`x = T(c+xi)-T(c) = y+r`,

with anchor tangent

`y = J0 xi`

and second-order remainder `r`. T-P5-134 then gives the sharp same-segment remainder-energy estimate

`4 Q(r) <= H Q(y)^2`

and, for a tangent-cell radius `Q(y)<=R`, converts it to a relative sandwich using auxiliary `delta,tau`. That route is sound, but under the **physical** packet already assumed in T-P5-134 it can pay a large avoidable price: it splits the physical linear term `<g,x>` into tangent and remainder pieces and replaces the physical quadratic reserve `A Q(x)` by a tangent reserve `Ahat Q(y)`.

The key observation is that T-P5-131/132 are already the sharp consumers of the physical pair

`Qx = Q(x)`, `p=<g,x>`.

Therefore, whenever the producer retains the physical coercivity and physical dual inequality assumed by T-P5-134, there is no mathematical reason to reduce `A` at all. The only chart-side quantity needed by the bounded-cell branch is an **upper bound on the physical secant radius**. This child derives the sharp root-free radius conversion directly from `Q(y)<=R` and `4Q(r)<=H Q(y)^2`.

No actual chart/source binding, same-cell coverage, controller/FD/Float64 semantics, P8 flowpipe, Lean receipt, independent verification, admission, registry, or parent-gate promotion is claimed.

---

## 1. Abstract same-metric secant packet

Let `P` be SPD and write

`Q(u) := u^T P u`,

`B_P(u,v) := u^T P v`.

Set

`x := y+r`,

`q := Q(y)`,

`rho := Q(r)`,

`c := B_P(y,r)`.

Then exactly

`Qx := Q(x) = q + 2c + rho`.

Assume

**(1.1)** `0 <= q <= R`, with `R>=0`,

and the T-P5-134 second-order remainder packet

**(1.2)** `4*rho <= H*q^2`, with `H>=0`.

By quadratic Cauchy/Gram positivity,

**(1.3)** `c^2 <= q*rho`.

The problem is to certify `Qx<=Rx` without `sqrt(HR)`, without a relative lower sandwich, and without imposing `HR<=4`.

---

## 2. Sharp root-free tangent-to-physical radius theorem

Define

**(2.1)**

`D := 4*(Rx-R) - H*R^2`.

Check only

**(2.2)** `D >= 0`,

**(2.3)** `D^2 >= 16*H*R^3`.

Then:

### Theorem A — sharp physical secant radius

**(2.4)** `Q(y+r) <= Rx`.

### Direct proof

From (1.1)-(1.2),

`4*rho <= H*q^2 <= H*R^2`.

Also from (1.3),

`c^2 <= q*rho <= R*(H*R^2/4) = H*R^3/4`.

We claim

**(2.5)** `8*c <= D`.

If `c<=0`, this is immediate from `D>=0`. If `c>0`, then

`(8c)^2 = 64 c^2 <= 16 H R^3 <= D^2`,

and both `8c` and `D` are nonnegative, so `8c<=D`.

Therefore

`4 Qx = 4q + 8c + 4rho`

` <= 4R + D + H R^2`

` = 4Rx`.

Hence `Qx<=Rx`.

The trusted statement uses only quadratic-form nonnegativity, multiplication, squaring, addition, and order. No square root, division, inverse, eigenvalue, or Young parameter is needed.

### Relation to T-P5-128

This theorem is also the exact specialization of T-P5-128's root-free ellipsoid-sum gate after observing

`4Q(r) <= H q^2 <= H R^2`.

Take its parameters `A0=R`, `S=4`, `G=H R^2`. Its discriminant becomes exactly

`D=4(Rx-R)-HR^2`,

`D^2>=16HR^3`.

The direct proof above is included so the new chart leaf need not depend on a higher-level center-tracking theorem.

---

## 3. Sharpness of the radius gate

For interpretation, the least possible real upper radius is

`Rx,min = (sqrt(R) + (sqrt(H)/2) R)^2`

`       = R + (H/4)R^2 + sqrt(H R^3)`.

The checker never needs this expression. Conditions (2.2)-(2.3) are its root-free branch-safe form.

The bound is information-theoretically sharp under only (1.1)-(1.3). In one dimension with `Q(u)=u^2`, choose positive aligned `y,r` saturating

`y^2=R`,

`4r^2=H R^2`.

Then `Q(y+r)=Rx,min`.

A fully rational regression is

`R=1`, `H=1`, `y=1`, `r=1/2`.

Then

`q=1`, `rho=1/4`, `Qx=9/4`.

At `Rx=9/4`,

`D = 4*(9/4-1)-1 = 4`,

`D^2=16=16HR^3`.

Any `Rx<9/4` is falsified by the same witness. Thus the radius conversion itself has no slack to recover unless the source supplies signed information on `B_P(y,r)` or a smaller direct secant envelope.

---

## 4. The physical reset packet should stay physical

Retain the T-P5-130/131/134 physical reset premises

**(4.1)** `m*Qx <= Wm`, with `m>0`,

**(4.2)** `p^2 <= B*Qx`, where `p=<g,x>` and `B>=0`,

**(4.3)** `4*mu*C <= B`, with `mu>0`,

**(4.4)** `Wp <= Wm + p + ell*Qx + C`,

and choose `kappa>=1`.

Define exactly as T-P5-131

**(4.5)**

`A := m*(kappa-1)-ell`.

Then the same physical derivation gives

**(4.6)**

`Wp-kappa*Wm <= p - A*Qx + C`.

Crucially, the chart identity `x=y+r` does not change (4.1)-(4.6). If (4.1) and (4.2) are genuinely physical statements for the actual secant `x`, then neither `p` nor `A Qx` needs to be decomposed into tangent plus remainder pieces.

This leads to the main improvement.

---

## 5. Global branch: chart nonlinearity costs exactly zero

Assume the T-P5-131 global gate

**(5.1)** `A>=0`,

**(5.2)** `A*(4*mu*E-B) >= B*mu`.

Then directly from (4.1)-(4.6), T-P5-131 yields

### Theorem B — no-curvature-tax global nonlinear-chart reset

**(5.3)** `Wp <= kappa*Wm + E`.

No premise involving `H`, `R`, `delta`, or `tau` is needed.

This is not because the chart remainder vanished. It is because T-P5-131 already optimized over **all physical states** satisfying `p^2<=B Qx`. Replacing `x` by `y+r` and then bounding the two pieces separately can only discard correlation that the physical theorem did not need to discard.

Therefore, under the physical assumptions (4.1)-(4.4), the T-P5-134 effective-headroom reduction

`A -> Ahat`

is a sound fallback for a tangent-only consumer, but it is not a necessary mathematical tax for the global reset theorem.

---

## 6. Bounded-cell branch: chart nonlinearity only inflates the radius

Suppose the actual source is normalized-only for the cell radius, so it knows `q<=R` and (1.2), but does not directly know a physical `Qx<=Rphys` certificate.

First choose rational `Rx` satisfying Theorem A. Then the complete T-P5-132 checker applies **with the original physical `A` unchanged** and with `Rx` as the physical radius.

### Interior branch

If

`0<A`

and

`B <= 4*A^2*Rx`,

use the same T-P5-131 product gate

`A*(4*mu*E-B) >= B*mu`.

### Boundary branch

If

`A<=0`

or

`4*A^2*Rx <= B`,

define

**(6.1)**

`Sx := 4*mu*E - B + 4*mu*A*Rx`.

Check

**(6.2)** `Sx>=0`,

**(6.3)** `Sx^2 >= 16*mu^2*B*Rx`.

Then

### Theorem C — sharp bounded physical-secant reset from tangent radius

**(6.4)** `Wp <= kappa*Wm + E`.

Thus the nonlinear chart enters the sharp reset consumer only through the smallest certified physical secant radius `Rx`. It does **not** independently tax the dual linear term and the quadratic curvature headroom.

---

## 7. Strict regression: the split `delta/tau` tax can be very loose

Take the scalar values

`A=1`, `B=1`, `R=1`, `H=1`.

The sharp secant-radius theorem gives

`Rx=9/4`.

For the state-dependent physical expression

`p-A Qx`,

with `p^2<=Qx`, the exact worst value on `0<=Qx<=9/4` is

`1/4`.

Indeed the unconstrained maximum of `sqrt(s)-s` occurs at `s=1/4`, which lies inside the physical radius.

Now compare the T-P5-134 split lane. Its smallest real choices are

`delta=1/2` from `HR<=4delta^2`,

`tau=1/2` from `BH<=4tau^2`.

Hence

`Ahat = A*(1-delta)^2 - tau`

`     = 1/4 - 1/2`

`     = -1/4`.

The reduced tangent envelope is then

`p0 - Ahat*q = p0 + q/4`,

which, under `p0^2<=q` and `q<=1`, permits the value

`1 + 1/4 = 5/4`.

So the tangent/remainder split inflates the retained state-dependent charge from the true sharp `1/4` to `5/4` in this exact rational example. There is no contradiction: T-P5-134 is sound; the example shows that the split can destroy a factor-five amount of cancellation even before relocation is charged.

---

## 8. Stronger coverage regression: remove the artificial `HR<=4` smallness barrier

T-P5-134's lower secant/tangent sandwich requires a certificate `0<=delta<=1` together with

`HR <= 4delta^2`.

Therefore that particular lower-sandwich lane cannot run when `HR>4`.

The physical-radius theorem has no such smallness requirement.

Take the exact rational chart example

`T(z)=z+(3/2)z^2`, `c=0`, `xi=1`, `P=1`.

Then

`y=1`, `r=3/2`, `x=5/2`,

`R=1`, `H=9`,

and

`Qx=25/4`.

Theorem A certifies the sharp radius `Rx=25/4` because

`D=4*(25/4-1)-9=12`,

`D^2=144=16*9`.

The chart is not folding on the segment: `T'(z)=1+3z>0` for `0<=z<=1`.

Now choose an abstract sharp bounded-reset packet

`A=-1`, `B=1`, `mu=1`.

The T-P5-132 boundary floor at `Rx=25/4` is exactly

`E = 1/4 + 5/2 + 25/4 = 9`.

In cleared form,

`Sx = 4E-B+4A Rx = 36-1-25 = 10`,

`Sx^2=100=16*B*Rx`.

The one-dimensional aligned witness `g=1`, `x=5/2`, `C=1/4` saturates the state/relocation charge:

`p-AQx+C = 5/2 + 25/4 + 1/4 = 9`.

Hence this is an exact equality regression for the new lane. The `delta<=1` sandwich has no legal certificate here (`delta` would need at least `3/2`), while the physical-radius route remains finite and sharp.

---

## 9. Why this does not invalidate T-P5-134

T-P5-134 solves a different fallback problem: **what if the consumer insists on reducing everything to anchor-tangent variables `(q,p0)`?** In that representation the lower/upper secant sandwich and the linear remainder tax are legitimate.

The new theorem says that this reduction should not be performed when the upstream packet already contains the stronger physical structure used by T-P5-131/132:

- physical coercivity `m Qx<=Wm`;
- physical dual inequality `<g,u>^2<=B Q(u)` applicable to the actual secant `u=x`;
- the physical reset envelope in `p=<g,x>` and `Qx`.

With those premises, `x` is the right state variable and the tangent chart is only a producer for a physical **radius cap** when a bounded-cell theorem needs one.

So the recommended precedence is:

1. exact/direct physical secant packet if available;
2. physical packet + sharp tangent-to-secant radius conversion (this child);
3. only if the consumer truly lacks physical coercivity/dual semantics, fall back to T-P5-134's `Ahat` tangent reduction;
4. if a signed combined remainder `<g-2APy,r>-A Q(r)` is available, use that correlated lane before separate absolute-value taxes.

---

## 10. Fail-closed boundary: when the no-tax theorem is NOT allowed

Two assumptions are structural.

### 10.1 Tangent coercivity is not physical coercivity

If the source knows only

`m q <= Wm`

but not

`m Qx <= Wm`,

then the derivation of `-A Qx` from `-(kappa-1)Wm` is unavailable. For example, with `q=1` and aligned `r=y`, one has `Qx=4q`; a tangent coercivity certificate does not imply the physical one with the same `m`.

In that situation the original `A` must not be preserved without an additional secant/coercivity transport theorem.

### 10.2 Separate tangent dual bounds are not a physical dual theorem

If the producer has only

`p0^2<=B q`

and an independent bound on the remainder action, but no theorem implying

`p^2=<g,x>^2<=B Qx`

for the same physical metric/covector, then the linear remainder cannot be silently deleted. A `tau`-type charge or a signed combined-remainder packet is then genuinely needed.

Therefore this child is a stronger lane **under the physical T-P5-134 assumptions**, not a license to infer physical semantics from unrelated normalized caps.

---

## 11. Formalizable theorem leaves

A minimal Lean decomposition is:

1. `secant_radius_root_free`
   - SPD quadratic form `Q`;
   - premises `Q y<=R`, `4*Q r<=H*(Q y)^2`;
   - define `D=4*(Rx-R)-H*R^2`;
   - premises `D>=0`, `D^2>=16*H*R^3`;
   - conclusion `Q(y+r)<=Rx`.

2. `physical_reset_ignores_chart_split_global`
   - takes the existing physical T-P5-131 premises directly;
   - conclusion uses the original `A=m(kappa-1)-ell`;
   - no chart variables occur in the conclusion or gate.

3. `physical_reset_from_tangent_radius_bounded`
   - composes leaf 1 with T-P5-132;
   - uses `Rx` in the branch test and boundary discriminant;
   - retains original `A` and `B`.

The only quadratic-form identity additionally needed by leaf 1 is Gram/Cauchy positivity

`B_P(y,r)^2 <= Q(y)Q(r)`.

No calculus is needed in this child; the calculus remains isolated in T-P5-134's producer of `4Q(r)<=Hq^2`.

---

## 12. Typed source contract and next step

For the stronger lane, bind under one immutable knot/chart/reference identity:

- physical `P`, physical `m,B,mu,ell`, and the exact physical reset-envelope semantics;
- `chartKey`, anchor `c`, tangent `J0`, displacement `xi`;
- `y=J0 xi`, exact secant relation `x=T(c+xi)-T(c)=y+r`;
- tangent radius `Q(y)<=R`;
- whole-segment second-order action packet yielding `4Q(r)<=H Q(y)^2`;
- a rational `Rx` satisfying the two root-free radius gates.

The highest-value next source action is therefore **not** to search for smaller `delta,tau` first. It is to decide whether the actual knot packet really retains physical coercivity and the physical dual norm theorem for the secant state. If yes, export `Rx` and keep the original `A`. If no, T-P5-134 remains the sound fallback and its taxes are real relative to the weaker interface.

A further mathematical improvement would require signed information on `B_P(y,r)` or on the combined remainder. Without such information, Theorem A's physical radius is already sharp.

---

## 13. Status

This is a mathematical child only.

- exact root-free tangent-radius -> physical-secant-radius gate: **proved**;
- sharpness and rational equality regressions: **proved**;
- global no-curvature-tax composition under physical T-P5-131 assumptions: **proved**;
- bounded-cell composition through T-P5-132 with original `A`: **proved**;
- actual same-key chart/source packet: **not bound**;
- actual physical coercivity/dual availability at the current normalized-only knot: **not established here**;
- Lean/kernel verification: **not run**;
- source/coverage/Float64/controller/P8/admission/registry/P5-M4 promotion: **not claimed**.

Final status: **CONDITIONAL_PASS / pending source semantics**.