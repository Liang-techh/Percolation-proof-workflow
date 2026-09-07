---
kind: review_result
review_id: review-T-P8-011-guyuefangyuan-20260907T0332
task_id: T-P8-011
source_agent: 古月方源
claimed_at: 2026-09-07T03:26:00-06:00
created_at: 2026-09-07T03:32:00-06:00
inspected_commit: c07975f77438377e047e93b29b144c73379ef87c
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_ramp_tube_transport_and_pullback_domain_then_use_12d_explicit_time_flowpipe_as_P8_coverage_object
---

# T-P8-011 — ramp-eliminated flowpipe transport, exact domain pullback, and regularity bridge

## Scope

`T-P8-008` proved the pointwise source/adapter seam: after substituting `w=c*t`, the first 12 coordinates of the 14-state ramp lift are exactly the explicit-time mechanical field, while the literal source tail remains separate.  The new formalization sidecar now contains that algebra.  The next mathematical gap is between this trajectory identity and an actual P8 flowpipe/continuation statement.

This review proves a source-independent bridge that keeps the flowpipe in 12 mechanical dimensions plus an external parameter `c`, and lifts it to the existing 14-state ramp representation only as an exact graph.  It also derives the exact necessary ramp-coordinate domain condition and a quantitative Lipschitz transport theorem for future ODE existence/continuation work.

Inspected inputs:

- `review-T-P8-008-guyuefangyuan-20260907T0231.md`;
- `examples/routeb_p8_first12_adapter_lean/P8First12Adapter.lean`, blob `f16e15e9f7d54f20d2f0827b45b2561acc2d5305`;
- `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean`, blob `11c8e23a52128e56b65a76024285c45a9070414d`;
- `examples/routeb_p8_interval_ramp_lean/P8IntervalRamp.lean`, blob `0904bd9510ccc672436459caa40d827c879bba07`;
- `examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean`, blob `6baf8643631297c0ec33e59d7a224e8fcc1e7319`;
- `docs/routeb-p8-flowpipe-binding-next.md`, blob `c3d9dbf3aa7d1e9fdf4f0583f83c47fcdde83ae0`.

No Julia semantic binding, interval enclosure, ODE existence theorem, source receipt, coverage certificate, admission, or registry update is claimed.

## 1. The correct flowpipe object after ramp elimination

Use the `T-P8-008` notation

```text
State12 = R^12,
pack13(m,w) = (m,w),
G_c(t,m) = sourceMechanical(S, pack13(m,c*t)),
rampLift(m,c,t) = (m,c*t,c).
```

Let `C(c)` be an admissible parameter predicate, in the current parent

```text
C(c) :<=> c^2 <= 3.
```

Let

```text
B(t,c,m)
```

be any mechanical flowpipe predicate.  It may be an interval box, zonotope, polynomial enclosure, first-exit sublevel, or any other certified set; no geometry is needed for the theorem.

Define the exact ramp graph tube

```text
RampTube(B,C,t,z)
  :<=> exists m c,
      C(c) and B(t,c,m) and z = rampLift(m,c,t).                (1)
```

This is not the Cartesian product of a mechanical box with independent `w` and `c` intervals.  It retains the exact relations

```text
w = c*t,
c = constant.                                                  (2)
```

That distinction matters because the current 14-state Picard parent otherwise pays wrapping error in two coordinates whose dynamics are already solved exactly.

## 2. `rampLift` is injective in the data that matter

For every fixed `t`,

```text
rampLift(m1,c1,t) = rampLift(m2,c2,t)
  -> m1=m2 and c1=c2.                                         (3)
```

Proof: the first 12 coordinates are exactly `m`, and slot 13 (zero-based) is exactly `c`; no assumption on `t` is needed.  The `w` coordinate is therefore redundant for recovering the pair `(m,c)`.

Consequently membership of a ramp state in (1) is unambiguous: if

```text
z = rampLift(m,c,t),
```

then

```text
RampTube(B,C,t,z) <=> C(c) and B(t,c,m).                       (4)
```

This is the minimal set-level projection theorem needed by a flowpipe adapter.

## 3. Mechanical flowpipe coverage lifts exactly to the 14-state ramp tube

Fix an admissible `c` and a mechanical path `m(t)`.  Define

```text
z(t) := rampLift(m(t),c,t).                                    (5)
```

Suppose on a time set `I`

```text
B(t,c,m(t))                                                    (6)
```

holds for every `t in I`.  Then immediately from (1)

```text
RampTube(B,C,t,z(t))                                           (7)
```

for every `t in I` whenever `C(c)`.

Now add the trajectory hypothesis from `T-P8-008`:

```text
m'(t) = G_c(t,m(t)).                                           (8)
```

The exact vector-field identity already proved there gives

```text
z'(t) = timeLift(S)(t,z(t))                                   (9)
```

with the adapter-owned tail `w'=c`, `c'=0`.  Therefore a certified flowpipe for the 12-state explicit-time mechanical system lifts to a certified flowpipe for the existing 14-state ramp system without any new dynamical enclosure in the two tail coordinates.

Conversely, if a lifted trajectory is known to satisfy the ramp reconstruction hypotheses of `T-P8-009`, then on `[0,1]`

```text
z(t) = rampLift(proj12(z(t)),c0,t),                            (10)
```

and (4) projects any `RampTube` coverage statement back to the mechanical tube.  Thus, restricted to the ramp manifold, the two flowpipe notions are equivalent; the 14-state representation is a graph lift of the 12-state nonautonomous one, not a genuinely larger dynamical problem.

### Consequence for P8

A future P8 interval engine does not need to propagate independent interval states for `w` and `c`.  It can certify

```text
m' = G_c(t,m)                                                   (11)
```

for external `c`, then attach the exact tail `(c*t,c)` by theorem.  The existing 14-state structural consumers can remain unchanged downstream.

## 4. The source domain must be pulled back along the ramp graph

Let

```text
D13(x)
```

be the domain on which a source-side semantic/enclosure theorem for the 13-state field is valid.  The correct domain for the explicit-time field is not an arbitrary 14-dimensional box.  It is the pullback

```text
Dpull(c,t,m) :<=> D13(pack13(m,c*t)).                          (12)
```

For a mechanical tube `B`, the exact source-domain compatibility obligation is

```text
forall t c m,
  Time(t) -> C(c) -> B(t,c,m) -> D13(pack13(m,c*t)).           (13)
```

Once (13) holds, every source evaluation used by `G_c` is inside the certified source domain.  There is no separate mathematical obligation to enclose arbitrary `(w,c)` pairs that violate `w=c*t`.

This is a strict improvement over a Cartesian 14-state contract: source certification may still use boxes internally, but it only needs boxes that cover the ramp graph over each time/parameter cell.

## 5. Exact ramp-coordinate width theorem

Suppose the source theorem is valid only when

```text
|w| <= W,     W >= 0,                                         (14)
```

and the proof horizon is

```text
0 <= t <= T,  T >= 0,                                         (15)
```

for the full parameter family

```text
c^2 <= 3.                                                      (16)
```

Because `w=c*t`, the sharp universal requirement is

```text
forall c,t, c^2<=3 and 0<=t<=T -> |c*t|<=W.                   (17)
```

For `W,T>=0`, (17) is equivalent to the square condition

```text
3*T^2 <= W^2.                                                  (18)
```

### Sufficiency

From `c^2<=3` and `0<=t<=T`,

```text
(c*t)^2 = c^2*t^2 <= 3*T^2 <= W^2.
```

Since `W>=0`, this gives `|c*t|<=W`.

### Necessity

Take `c=sqrt(3)` and `t=T`.  Then `c^2=3`, so (17) gives

```text
sqrt(3)*T <= W,
```

and squaring yields (18).

Hence at the target `T=1`, a single symmetric source domain for the whole ramp family must reach at least

```text
W >= sqrt(3).                                                  (19)
```

A rational but slightly wider sufficient cap is `W=2`, using the already formalized consequence `c^2<=3 -> |c|<=2`.

## 6. Concrete obstruction to the current `w in [-0.01,0.01]` local box

The P8 flowpipe-binding document records the current local box

```text
w in [-1/100, 1/100].                                         (20)
```

This cannot cover the target family on `[0,1]`, independently of all mechanical dynamics.  The fully rational witness is

```text
c=1,  c^2=1<=3,
t=1,
w=c*t=1 > 1/100.                                              (21)
```

More generally, with the admissible fixed parameter `c=1`, the ramp exits (20) for every

```text
t > 1/100.                                                     (22)
```

Therefore any claim that one unchanged `|w|<=0.01` source box supports uniform P8 coverage beyond `T=0.01` is mathematically false.  The target `T=1` requires either

1. a wider source-certified `w` domain;
2. time/parameter partitioning with graph-aware `w=c*t` bounds; or
3. direct explicit-time source enclosures that evaluate `w=c*t` without promoting `w` to an independently boxed state.

This obstruction is separate from the old `du[13]=0` mismatch; `T-P8-008` fixed the semantic adapter, while (21) is a domain-coverage obstruction that remains afterward.

## 7. Quantitative regularity transport for Picard/continuation

The next ODE question is whether the explicit-time field `G_c` satisfies a local regularity contract once the exact-real source field does.  There is a direct theorem.

Assume the source mechanical map satisfies, on the pulled-back domain, an anisotropic Lipschitz bound

```text
||M_S(pack13(m1,w1)) - M_S(pack13(m2,w2))||
  <= Lm*||m1-m2|| + Lw*|w1-w2|,                              (23)
```

with `Lm,Lw>=0`.  Then for a fixed `c`, substituting `w=c*t` gives

```text
||G_c(t1,m1)-G_c(t2,m2)||
  <= Lm*||m1-m2|| + Lw*|c|*|t1-t2|.                          (24)
```

Proof: apply (23) to `w1=c*t1`, `w2=c*t2` and use

```text
|c*t1-c*t2| = |c|*|t1-t2|.
```

Two useful corollaries are immediate.

For fixed time,

```text
||G_c(t,m1)-G_c(t,m2)|| <= Lm*||m1-m2||.                     (25)
```

So ramp elimination does not worsen the spatial Lipschitz constant at all.

For the full current parameter family, `c^2<=3` implies `|c|<=2`, hence the rational uniform bound

```text
||G_c(t1,m1)-G_c(t2,m2)||
  <= Lm*||m1-m2|| + 2*Lw*|t1-t2|.                            (26)
```

Thus any exact-real source theorem providing (23) automatically supplies the continuity-in-time and local-Lipschitz-in-state shape used by standard Picard-Lindelof/continuation theorems.  The hard future work is obtaining the source-domain constants and proving the trajectory stays inside that domain, not reconstructing regularity from scratch after the ramp substitution.

### Important execution-semantics boundary

Equation (23) must be a theorem about a genuinely exact-real/smooth semantic source map, or a direct incremental theorem about the deployed execution semantics.  A real lift of a Float64 program is not automatically differentiable or continuous because rounding creates discontinuities.  Therefore one must not differentiate the Float64 execution map symbolically and call the result a source Lipschitz proof.  If execution error is retained, it needs its own incremental enclosure or perturbation/solution-robustness theorem.

## 8. Parameter/time slabs give graph-aware source boxes

Suppose on one cell

```text
|c| <= C,
0 <= t <= t1.                                                 (27)
```

Then the ramp graph obeys

```text
|w| = |c*t| <= C*t1.                                         (28)
```

Thus a sequence of time/parameter cells can generate source `w` bounds mechanically from (28).  If the parameter interval is signed and narrower than `[-C,C]`, the four corner products of the `c` interval and the time interval give the exact interval hull of `c*t` because multiplication is bilinear and extrema occur at corners of a rectangle.

This suggests a much cheaper enclosure interface than treating `w` and `c` as independent interval variables: each flowpipe cell stores `(time interval, c interval, mechanical box)`, and computes the admissible `w` interval from their product.  The mathematical source query remains 13-state, exactly matching the deployed source input shape.

## 9. Lean-friendly theorem decomposition

A source-independent sidecar can remain elementary and avoid committing to a full ODE API.

```lean
-- Fixed-time injectivity of the exact ramp graph.
theorem rampLift_injective_mc
    {m1 m2 : State12} {c1 c2 t : R}
    (h : rampLift m1 c1 t = rampLift m2 c2 t) :
    m1 = m2 /\ c1 = c2

-- Exact set-level graph lift.
def RampTube
    (B : R -> R -> State12 -> Prop)
    (C : R -> Prop) (t : R) (z : State14) : Prop :=
  exists m c, C c /\ B t c m /\ z = rampLift m c t

theorem rampTube_on_ramp_iff ... :
  RampTube B C t (rampLift m c t) <-> C c /\ B t c m

-- Pulled-back source domain.
def PullbackDomain
    (D13 : State13 -> Prop) (c t : R) (m : State12) : Prop :=
  D13 (pack13 m (c*t))

-- Square-only domain cap, avoiding sqrt in the consumer.
theorem ramp_tail_sq_cap
    (hc : c^2 <= 3) (ht0 : 0 <= t) (htT : t <= T)
    (hT : 0 <= T) (hcap : 3*T^2 <= W^2) :
    (c*t)^2 <= W^2

-- Exact rational obstruction for the currently documented local w box.
theorem current_w_box_not_T1 :
    exists c t, c^2 <= 3 /\ 0 <= t /\ t <= 1 /\
      |c*t| > (1:R)/100

-- Source anisotropic Lipschitz -> explicit-time Lipschitz.
theorem explicitMechanical_lipschitz_transport ...
```

The first four statements are pure algebra/order and can be formalized independently of source binding.  A later ODE sidecar may consume the final regularity theorem together with a Mathlib local-existence theorem, but should not be mixed into this child until the exact domain and semantic source are frozen.

## 10. What this changes in the shortest P8 chain

The earlier P8 chain had an apparent need to build a genuine 14-dimensional flowpipe after the source-contract repair.  The present result sharpens it to

```text
first-12 source binding
  -> explicit-time 12D RHS enclosure on PullbackDomain
  -> 12D mechanical flowpipe/continuation for each c-cell
  -> exact RampTube graph lift (this review)
  -> existing 14D terminal/ramp consumers.                    (29)
```

The two tail coordinates no longer need independent Picard propagation.  This does not remove the real hard gates: the concrete source mechanical outputs, interval soundness, existence/continuation, cell coverage to `T=1`, and downstream terminal physics remain open.

## Recommended next actions

1. Formalization lane: add a small portable sidecar for `rampLift_injective_mc`, `RampTube`, `rampTube_on_ramp_iff`, `PullbackDomain`, and the rational `current_w_box_not_T1` obstruction.  Keep ODE APIs out of the first pass.
2. P8 source/checker lane: stop generating independent `w,c` endpoint dynamics; for each `(time,c)` cell compute the source input `w` hull from `w=c*t` and certify only the 12 mechanical outputs of the 13-state source.
3. Regularity lane: for the exact-real DH/FD/solve semantic field, obtain an anisotropic mechanical/`w` Lipschitz enclosure of the form (23).  Then (24)--(26) give the explicit-time regularity needed by a future local-existence/continuation theorem.
4. Coverage planning: do not reuse the current `|w|<=1/100` local source box past `T=1/100` for the full family; either widen or partition it.

This result remains `pending`: it is a mathematical flowpipe/domain bridge, not a P8/M4 closure or verification result.
