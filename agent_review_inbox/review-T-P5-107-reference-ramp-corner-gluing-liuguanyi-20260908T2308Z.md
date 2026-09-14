---
kind: review_result
review_id: review-T-P5-107-reference-ramp-corner-gluing-liuguanyi-20260908T2308Z
task_id: T-P5-107-REFERENCE-RAMP-CORNER-GLUING
source_agent: 柳冠一
created_at: 2026-09-08T23:08:00Z
claim_commit: 976c7af8b3ef0759d37cbaf57df7f111457f6176
inspected_commit: 66c9eca2d7a9e8c9ee5cf937c6f2955bee625e33
upstream_review:
  path: agent_review_inbox/review-T-P5-106-reference-ramp-recentered-energy-honglianmozun-20260908T2256Z.md
  blob_sha: 7a8fe4d1f404a86e3695cd602f9691399fdefa52
status: CONDITIONAL_PASS_EXACT_GLUE_AND_RESET_PACKET
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize the knot-continuity/gluing leaf after T-P5-106; bind an actual continuous piecewise-affine reference input and its segment slopes only after the referenceKey is fixed
commands: none_math_derivation_only
lean_compile_status: not_run
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-107 — exact corner gluing for the position-recentered reference collar

## 0. Question

T-P5-106 proves an exact position-only recentering for

`q' = v`,

`M v' + D v + B q = g w(t)`,

with a constant center witness `B a = g`, recentered variables

`z = q-a w`, `s=v`,

and storage

`Vc(z,s) = 1/2 s^T M s + 1/2 z^T K z + z^T M s + 1/2 z^T D z`.

Its segmentwise derivative packet is

`Vc' = -Qd - w' c_s^T x`, `x=(z,s)`,

with the exact rational consequences

`Qd >= (9/10) Vc`,

`(c_s^T x)^2 <= (63/200) Qd`,

and therefore, on a segment where `(w')^2 <= S`,

`Vc' <= -(9/20) Vc + (63/400) S`.

T-P5-106 states informally that a continuous piecewise-affine ramp can be glued without a storage reset even when the slope jumps. The smallest remaining mathematical seam is to make that statement exact and to isolate what changes if the input value itself jumps.

This review closes that seam at the source-independent exact-real level.

---

## 1. Exact no-reset identity at a slope corner

Let `tau` be a knot. Assume the physical state and input value are continuous:

`q(tau+) = q(tau-)`,

`v(tau+) = v(tau-)`,

`w(tau+) = w(tau-)`.

No equality of one-sided slopes is assumed. In particular, `w'(tau-)` and `w'(tau+)` may be different.

Define on both sides

`z = q-a w`, `s=v`.

Then immediately

**(1.1)** `z(tau+) = z(tau-)`,

**(1.2)** `s(tau+) = s(tau-)`.

Because `Vc` is a fixed quadratic polynomial in `(z,s)` and contains no `w'`,

**(1.3) NO-RESET IDENTITY**

`Vc(tau+) = Vc(tau-)`.

Thus a slope discontinuity is not a hybrid reset for the position-only recentering. The derivative formula may use different slope bounds on the two adjacent open segments, but the storage value itself is glued exactly.

### Minimal theorem statement

`position_recenter_storage_continuous_at_slope_knot`

Inputs:

- fixed `a,M,D,K`;
- left/right physical states with `q+ = q-`, `v+ = v-`;
- left/right input values with `w+ = w-`.

Definitions:

`z± = q± - a*w±`, `s±=v±`, and the same quadratic `Vc`.

Output:

`z+=z-`, `s+=s-`, `Vc+=Vc-`.

This leaf is pure ring/linear algebra. It does not need differentiability or an ODE theorem.

---

## 2. Piecewise-segment collar gluing

Let

`t0 < t1 < ... < tN`

be a finite partition. Suppose `Vc:[t0,tN] -> R` is continuous on the whole interval and differentiable on every open segment `(tj,tj+1)`. On segment `j`, assume

**(2.1)** `Vc'(t) <= -nu Vc(t) + beta_j`,

with a common `nu>0`, and assume

**(2.2)** `beta_j <= nu R`

for one common collar level `R`.

Then if `Vc(t0) <= R`,

**(2.3) GLOBAL GLUING CONCLUSION**

`Vc(t) <= R` for every `t in [t0,tN]`.

### Proof

Fix one segment and put `Y=Vc-R`. From (2.1)-(2.2),

`Y' <= -nu Y`.

Hence

`d/dt [ exp(nu*(t-tj)) Y(t) ] <= 0`.

Therefore

`Y(t) <= exp(-nu*(t-tj)) Y(tj) <= 0`

throughout that segment whenever `Y(tj)<=0`.

At `tj+1`, continuity passes the same inequality to the next segment. Induction over the finite partition proves (2.3).

The important interface point is that there is **no per-knot additive debit**. The number of slope changes does not appear in the collar gate. Only the segmentwise forcing bound appears.

### Minimal theorem statement

`piecewise_dissipative_collar_glue`

Inputs:

- a finite ordered partition;
- global continuity of `V`;
- segmentwise differentiability;
- `nu>0`;
- segment inequalities `V' <= -nu*V + beta_j`;
- `beta_j <= nu*R` for all `j`;
- `V(t0)<=R`.

Output: `V<=R` on the union of all closed segments.

A Lean implementation may use an existing Gronwall/comparison lemma per segment and a finite induction. The trusted source-facing gate contains no exponential: the exponential only appears inside the proof of the generic analytic lemma.

---

## 3. Exact specialization to the T-P5-106 rational packet

T-P5-106 gives, on each differentiable ramp segment,

`nu = 9/20`,

`beta_j = (63/400) S_j`,

where `(w')^2 <= S_j`.

The segment inward condition `beta_j <= nu R` is exactly

`(63/400) S_j <= (9/20) R`.

Clearing positive denominators gives

**(3.1)** `7 S_j <= 20 R`.

Therefore a continuous piecewise-affine input with slopes `m_j` is globally collar-safe whenever

**(3.2)** `20 R >= 7 m_j^2` for every segment `j`.

Equivalently, if `Smax` is any common rational upper bound for all `m_j^2`, it is enough to check the single scalar gate

**(3.3)** `20 R >= 7 Smax`.

There is no dependence on segment duration, number of knots, or size of a slope jump. The latter is not being ignored: it is absent because `(z,s,Vc)` are continuous and the storage does not contain `w'`.

This is the exact mathematical bridge from the T-P5-106 local slope collar to a continuous piecewise-affine ramp law.

---

## 4. Why this does not replace the amplitude/domain budget

The no-reset/gluing theorem controls the invariant level around the moving center only. It does not bound the center location.

The absolute reference state still obeys the T-P5-106 value bridge

`pB(q,v) <= (67/2) Vc(z,v) + (41/200) w^2`.

Thus a valid hybrid-domain packet still needs an independent amplitude cap

`w^2 <= Wbar`.

After the global collar `Vc<=R` is glued, the absolute block budget is

**(4.1)** `pB <= (67/2)R + (41/200)Wbar`.

Slope controls invariance; amplitude controls placement. Neither typed obligation implies the other.

---

## 5. Exact obstruction when the input value jumps

Now assume the physical state is continuous at a knot but the input itself jumps by

`Delta = w+ - w-`.

Then

`z+ = z- - a Delta`, `s+=s-`.

Write

`H0 = K+D`,

`c_s = (H0 a, M a)`,

`x- = (z-,s-)`.

A direct quadratic expansion gives the exact reset identity

**(5.1) INPUT-JUMP RESET**

`Vc+ - Vc-`
` = -Delta * c_s^T x-`
`   + (Delta^2/2) * a^T H0 a`.

This is the missing counterpart of the no-reset theorem. A value jump is a genuine hybrid event and cannot be glued for free.

For the exact rational packet of T-P5-106,

**(5.2)** `a^T (K+D) a = 11275620/75672601`.

Hence

`Vc+ - Vc-`
` = -Delta*c_s^T x-`
`   + (5637810/75672601) Delta^2`.

The state-dependent signed linear term is essential. Taking absolute values before forming the exact reset would again destroy possible cancellation.

### Minimal theorem statement

`position_recenter_input_jump_energy_identity`

Inputs: symmetric `M,K,D`, fixed `a`, a physical state continuous through the event, and `Delta=w+-w-`.

Output: (5.1).

---

## 6. A new exact rational upper packet for optional jump budgeting

T-P5-106 already has

`(c_s^T x)^2 <= (63/200) Qd`.

For the same exact rational matrices `P,Q`, there is also the following useful upper comparison:

**(6.1)** `25 P - 2 Q > 0`.

Its leading principal minors are exactly

`149/4`,

`176351639/160000`,

`524415136447649/360000000000`,

`962037342549979725121/368640000000000000000`,

all strictly positive. Therefore

`2 Qd <= 25 x^T P x = 50 Vc`,

so

**(6.2)** `Qd <= 25 Vc`.

Combining with the existing slope-observable certificate gives

**(6.3)** `(c_s^T x)^2 <= (63/8) Vc`.

This is not needed for continuous ramps, but it gives a clean division-free reset interface if a future input law contains actual jumps.

Suppose before a jump

`Vc- <= R`, `R>=0`,

and introduce nonnegative rational reset auxiliaries `J,E`. If

**(6.4)** `63 Delta^2 R <= 8 J^2`,

then (6.3) implies

`|Delta*c_s^T x-| <= J`.

If in addition

**(6.5)**

`2*75672601*J + 11275620*Delta^2`
` <= 2*75672601*E`,

then (5.1) yields

**(6.6)** `Vc+ <= Vc- + E <= R+E`.

Thus an input jump can be represented by an explicit reset budget using only rational multiplication, squares, and order comparisons. No square root or matrix inverse is needed at the source-facing scalar gate.

When `Delta=0`, choose `J=E=0`; (5.1) recovers the exact zero-reset identity rather than merely a conservative inequality.

---

## 7. Interface consequences

The correct reference-ramp interface now separates three different objects:

1. **flow-segment slope packet**: on each open segment, `(w')^2<=S_j` and `20R>=7S_j`;
2. **knot packet**: continuity of `q,v,w`, which implies exact continuity of `z,s,Vc` and costs zero budget;
3. **absolute placement packet**: `w^2<=Wbar`, consumed only by the `pB`/domain bridge.

If the source law has value jumps, replace item 2 by the explicit reset identity (5.1) and, if desired, the division-free sufficient reset packet (6.4)-(6.5).

This separation matters because a slope change, an amplitude bound, and a value jump are mathematically different obligations. Charging all three through one generic disturbance norm would erase the structural cancellation proved in T-P5-106.

---

## 8. Suggested formalization decomposition

Small leaves, in order:

- `position_recenter_storage_continuous_at_slope_knot` — pure algebra;
- `piecewise_dissipative_collar_glue` — generic scalar analysis/finite induction;
- `reference_ramp_piecewise_affine_collar` — instantiate `nu=9/20`, `beta=63*S/400` and clear denominators to `7*S<=20*R`;
- `position_recenter_input_jump_energy_identity` — pure quadratic expansion;
- `reference_Qd_le_25_Vc` — pure 4x4 quadratic-form certificate;
- `reference_input_jump_division_free_reset` — scalar squares/order arithmetic.

The first, third, fourth, fifth and sixth leaves are friendly to a very small Lean algebra sidecar. The second is the only analytic gluing lemma.

---

## 9. Remaining boundaries

This review does **not** prove:

- which deployed `referenceKey` supplies the exact `M,D,B,g,a` semantics;
- that the actual P8/reference input law is continuous piecewise affine, nor its actual partition/slopes;
- any Float64/controller equality or source execution trace;
- actual `Wbar`, whole-path/tube coverage, FD/reference halo, graph lift, or flowpipe;
- Lean/kernel compilation, comparator acceptance, independent verification, admission, registry mutation, or P5/M4 closure.

The mathematical child is complete conditional on the T-P5-106 exact-real packet: continuous slope corners cost **exactly zero** storage reset, and an actual input-value jump has the exact reset formula (5.1) with an optional all-rational budget interface.
