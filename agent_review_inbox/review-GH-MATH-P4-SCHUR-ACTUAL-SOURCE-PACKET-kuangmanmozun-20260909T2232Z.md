---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-PACKET-kuangmanmozun-20260909T2232Z
task_id: GH-MATH-P4-SCHUR-ACTUAL-SOURCE-PACKET
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T22:32:00Z
claim_commit: 20810eea625a4895f7fe5677f4420b52d74c5c38
inspected_head: 4af485b80eb5a6eccd484c9da86236a52162b791
inspected_upstream:
  - 20d05498e72774e2009a2e5a0d03b684e388050e
  - b1ea7a04716bef9ce4aa70a32879b997b85047ff
  - 79dc40e790939ce9b8260d8a3569ce8c4f44f0fd
  - 196aa849e029c84327b6acfcba19c945a74753c9
status: BLOCKED_WITH_EXACT_SOURCE_PACKET_OBSTRUCTION
result_class: mathematical-interface-and-counterexample-child
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
registry_mutation: false
state_mutation: false
requested_action: source/CSE lane should emit one same-key block456 defect packet, preferably d4,d5,w6 with w6=350003*d6-50000*d4 before intervalization, plus exact H/source identity; if only raw coordinate boxes are available, the exact rational raw-box fallback below is sufficient but weaker
---

# GH-MATH-P4-SCHUR-ACTUAL-SOURCE-PACKET — final mathematical packet decision

## 1. Result

The directed task can now be closed as a **mathematically complete packet specification with an exact source obstruction**, but not as an instantiated physical/source certificate.

The current repository contains all of the following mathematical ingredients:

1. an exact rational candidate for the block-(4,5,6) origin metric inverse `H=M0_CC^-1`;
2. a proof that two observed defect directions, or two Schur scalar projections, cannot control the full three-dimensional SPD energy;
3. the sharp transformed third coordinate
   `w6 = 350003*d6 - 50000*d4`,
   for which the block456 energy diagonalizes exactly;
4. a source-independent rational residual comparison interface for the principal joint-6 branch.

What is still absent is the one object this task was assigned to consume: an **actual same-key source packet** binding the physical/configuration defect to `d=(d4,d5,d6)` (or directly to `d4,d5,w6`) together with source identity of the exact metric.  The available joint-6 residual bridge explicitly stops before instantiating the principal compact source expression, so it cannot be spliced into the Schur packet as if it were a measured third coordinate.

Therefore no numerical `Delta_H`, `u`, `s`, or deployed Schur cap is honestly source-bound in this task.  The correct status is fail-closed `BLOCKED_WITH_EXACT_SOURCE_PACKET_OBSTRUCTION`, not `PASS` and not an admission/registry result.

This review adds one producer-facing mathematical refinement not needed in the earlier obstruction reviews: **if the source producer cannot emit the correlated scalar `w6` but can emit independent rational absolute caps on the raw coordinates, there is still an exact sharp rational box cap.**  Thus there are now two mathematically valid producer routes rather than one.

## 2. Exact metric and transformed-coordinate route

The source-reification lane proposes

```text
H =
[[ 50003000000/5000400003,  0,                    -50000000000/5000400003],
 [ 0,                        4000000/200739,         0],
 [-50000000000/5000400003,   0,                     350003000000/5000400003]].
```

Write

```text
h11 =  50003000000/5000400003,
h22 =  4000000/200739,
h13 = -50000000000/5000400003,
h33 =  350003000000/5000400003.
```

Then

```text
D = d^T H d
  = h11*d4^2 + h22*d5^2 + 2*h13*d4*d6 + h33*d6^2.
```

The exact completed-square coordinate is

```text
w6 := 350003*d6 - 50000*d4,
```

and the exact identity is

```text
D
 = (3000000/350003) * d4^2
 + (4000000/200739) * d5^2
 + (1000000/1750155002250009) * w6^2.
```

Hence a same-key producer packet

```text
d4^2 <= U4,
d5^2 <= U5,
w6^2 <= Uw,
w6 = 350003*d6 - 50000*d4
```

implies

```text
D <=
  (3000000/350003) * U4
+ (4000000/200739) * U5
+ (1000000/1750155002250009) * Uw.
```

Because `(d4,d5,d6) -> (d4,d5,w6)` is invertible, this cap is sharp if the three transformed-coordinate quadratic caps are otherwise independent.  No square root, eigendecomposition, floating inverse, or nonlinear optimizer is needed by the checker.

## 3. New fallback theorem — exact sharp cap from raw rational absolute boxes

Suppose instead that the actual source lane can only prove independent symmetric raw-coordinate bounds

```text
|d4| <= a4,
|d5| <= a5,
|d6| <= a6,
```

with `a4,a5,a6 >= 0` rational and all three bounds referring to the same defect/configuration key.

### Theorem — exact block456 raw-box maximum

For every such `d`,

```text
D <= D_raw(a4,a5,a6),
```

where

```text
D_raw(a4,a5,a6)
 := h11*a4^2
  + h22*a5^2
  + h33*a6^2
  + 2*(-h13)*a4*a6.
```

Since `h13<0`, this is explicitly

```text
D_raw
 = (50003000000/5000400003)*a4^2
 + (4000000/200739)*a5^2
 + (350003000000/5000400003)*a6^2
 + (100000000000/5000400003)*a4*a6.
```

This bound is **sharp over the independent symmetric raw box**.

### Proof

The diagonal terms satisfy

```text
d4^2 <= a4^2,
d5^2 <= a5^2,
d6^2 <= a6^2.
```

For the only cross term,

```text
2*h13*d4*d6
 <= 2*|h13|*|d4|*|d6|
 <= 2*|h13|*a4*a6.
```

Adding the four bounds proves the upper bound.

Sharpness is attained by any corner with

```text
|d4|=a4,
|d5|=a5,
|d6|=a6,
sign(d4) = -sign(d6),
```

because `h13<0`, so the cross term is then exactly `+2|h13|a4a6`.  Thus no smaller uniform constant follows from independent raw absolute caps alone.  QED.

### Consequence

A source producer does **not** strictly need `w6` if it already has rational absolute boxes for the same `d4,d5,d6`.  However the transformed `w6` route can be materially tighter because it retains the negative `d4/d6` correlation before intervalization.  The raw-box theorem is therefore a valid fail-safe route, not the preferred tight route.

## 4. Squared-cap-only fallback without square roots

Sometimes the producer exports only rational quadratic caps

```text
d4^2 <= U4,
d5^2 <= U5,
d6^2 <= U6
```

and does not export rational absolute radii.  The sharp independent-box formula would contain `sqrt(U4*U6)` and is no longer purely rational in general.

For any rational `eta>0`, Young's inequality gives

```text
2*|d4*d6| <= eta*d4^2 + eta^(-1)*d6^2.
```

Hence the entirely rational sufficient cap

```text
D <=
  (h11 + (-h13)*eta) * U4
+ h22 * U5
+ (h33 + (-h13)/eta) * U6.
```

The checker may keep `eta=p/q>0` rational and clear the positive denominator rather than perform floating division.  This route is generally nonsharp, but it gives a deterministic source-compatible cap when the producer exposes only squared caps and cannot form `w6`.

The exact sharp raw-box cap and the transformed-coordinate cap should not be conflated: the first assumes independent raw coordinate boxes; the second assumes independent boxes after the correlated affine transform.  They are different information models.

## 5. Exact information obstruction that remains

The mathematical source obstruction is now narrow.

A packet containing only rows/directions 4 and 5 cannot certify a finite full block456 energy cap.  More generally, if `H` is SPD on `R^3` and the source observation map `L:R^3->R^m` has rank `<3`, choose nonzero `v in ker L`; then `d=t v` keeps all observed quantities fixed at zero while

```text
d^T H d = t^2 * v^T H v -> infinity.
```

Therefore none of the following can substitute for the missing third independent information:

- two raw defect rows only;
- the two scalar Schur projections `u` and `s` only;
- a source-independent theorem about a possible joint-6 rational residual;
- a separately reconstructed `H` with no same-source defect binding.

The later joint-6 bridge is useful once the actual principal compact CSE appears, but its own review explicitly records that the concrete `N_a,D_a` source object was not available.  It is therefore not legal evidence that the current Schur packet already contains `d6` or `w6`.

## 6. Minimal same-key packet that closes this task downstream

One immutable producer record is sufficient if it freezes one `source_key/configuration_key/domain_key` and provides either Route A or Route B below.

### Route A — preferred correlated packet

```text
1. defect identity/order: d=(d4,d5,d6) is the intended block456 defect;
2. exact affine CSE: w6=350003*d6-50000*d4, formed before intervalization;
3. rational same-domain caps: d4^2<=U4, d5^2<=U5, w6^2<=Uw;
4. exact metric source identity: K=M0_CC for the same C=(4,5,6), H=K^-1;
5. if the Schur consumer needs them, same-key ell,r0 and exact definitions
   u=ell^T H d, s=(ell+r0)^T H d.
```

Then the trusted scalar checker computes the exact rational `Delta_H` in section 2.

### Route B — raw-box fallback

Replace items 2–3 by same-key rational absolute caps

```text
|d4|<=a4, |d5|<=a5, |d6|<=a6.
```

Then the checker uses the exact sharp `D_raw` from section 3.

### Optional Route C — squared-cap-only fallback

If only `U4,U5,U6` are available, freeze rational `eta>0` and use the Young cap from section 4.

None of these routes requires a six-dimensional `y=Xz_A` box if the producer supplies `d` directly with an exact source identity.  Conversely, if the producer chooses the `y` route, it must provide enough same-key information to prove `d=Ay+b` (or `d=J_d z_A+b`) on all three active defect directions.

## 7. Formalizable theorem statements

The mathematical leaves can be stated without source-specific names.

```text
raw_box_metric_cap:
  h11>=0 -> h22>=0 -> h33>=0 -> h13<=0 ->
  |x|<=a -> |y|<=b -> |z|<=c ->
  h11*x^2 + h22*y^2 + 2*h13*x*z + h33*z^2
    <= h11*a^2 + h22*b^2 + h33*c^2 - 2*h13*a*c.

raw_box_metric_cap_sharp:
  0<=a -> 0<=b -> 0<=c -> h13<0 ->
  the preceding upper bound is attained at (a,b,-c).

squared_cap_metric_young:
  eta>0 -> x^2<=U4 -> y^2<=U5 -> z^2<=U6 ->
  D(x,y,z)
    <= (h11-h13*eta)U4 + h22*U5 + (h33-h13/eta)U6
  when h13<=0.
```

For the concrete block456 constants, all coefficient signs and equalities reduce to exact rational normalization.

## 8. Failed branches / nonclaims

- **Failed branch: infer `D` from `u,s`.** Impossible in 3D without a third independent constraint; rank-deficient observation lemma gives an unbounded counterexample family.
- **Failed branch: splice the principal joint-6 bridge as actual `d6`.** The bridge is still source-independent because its concrete principal `N_a,D_a` packet is missing.
- **Failed branch: use an unrelated matching-metric CSV packet.** Same shape/positive definiteness does not establish identity with `M0_CC^-1` for the defect packet.
- **Failed branch: intervalize `d4,d6` separately and claim the transformed cap.** Once the correlation is discarded, only the raw-box/Young fallback is justified.

This review does not establish source completeness, actual interval caps, Float64/directed-rounding soundness, Lean/kernel compilation, coverage, verifier approval, admission, registry mutation, or parent P4/M4 closure.

## 9. Next step

The next useful work is no longer another Schur algebra proof.  A source/CSE producer must emit one of Routes A–C under one immutable configuration/domain key.  Route A is preferred because it is sharp and rational; Route B is an exact rational fallback if raw absolute boxes already exist.  Until such a packet lands, this directed task should remain closed as a documented source obstruction rather than stay indefinitely `CLAIMED` or be re-run as generic Schur algebra.
