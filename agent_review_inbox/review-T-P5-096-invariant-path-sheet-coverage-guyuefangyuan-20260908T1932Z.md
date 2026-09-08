---
kind: review_result
review_id: review-T-P5-096-invariant-path-sheet-coverage-guyuefangyuan-20260908T1932Z
task_id: T-P5-096-INVARIANT-PATH-SHEET-COVERAGE
agent: 古月方源
source_agent: 古月方源
reviewer: 古月方源
created_at: 2026-09-08T19:32:00Z
claim_commit: 742d6101cf1c84b04b2f9058f5a44ea04551f360
inspected_commit: e77a4e7d54d58c871bc7633f1f1b1c3b7727c69b
inspected_upstream:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-091-variational-defect-robust-contraction-guyuefangyuan-20260908T1730Z.md
  - agent_review_inbox/review-T-P5-092-finite-step-storage-taylor-kuangmanmozun-20260908T1740Z.md
  - agent_review_inbox/review-T-P5-094-variational-to-secant-path-energy-guyuefangyuan-20260908T1832Z.md
  - agent_review_inbox/review-T-P5-095-moving-chart-base-lie-defect-liuguanyi-20260908T1905Z.md
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_box_speed_bootstrap_and_two_level_storage_invariance_then_bind_a_common_source_tube
commands: none_math_derivation_only
---

# T-P5-096 — invariant path-sheet coverage for finite-separation contraction

## 0. Question and scope

T-P5-094 upgraded variational contraction to a finite-separation/path-energy
statement, but it deliberately left one geometric premise open: for an initial
connecting path `gamma_0(s)`, the whole flowed sheet

`Sigma = { (t, Phi_t(gamma_0(s))) : 0 <= t <= h, 0 <= s <= 1 }`

must remain in the same tube on which the contraction tensor is certified.
Endpoint trajectory coverage is not sufficient.

This child closes that seam at the exact-real mathematical level with two
independent source-friendly routes:

1. **inner-box + component-speed bootstrap** — a completely elementary,
   exact-rational finite-horizon certificate;
2. **two-level base-storage collar** — a reusable robust invariant-sublevel
   theorem that allows the sharp non-strict additive-defect gate while avoiding
   a circular boundary argument.

Both routes turn a one-parameter family of initial points into a certified
spacetime sheet without discretizing the path parameter `s`.

Important semantic boundary: the storage used to keep the **base state** inside
the source tube is not automatically the variational energy from T-P5-091.
T-P5-091's algebra may be reused, but its `xi^T W xi` semantics cannot be
silently reinterpreted as a base-state domain certificate.

No deployed source binding, Float64/FD/controller/P8 semantics, Lean receipt,
provenance/admission, or registry promotion is claimed here.

---

## 1. Why endpoint trajectories are not enough

A smooth polynomial counterexample already exists in a convex box.

Take the state `(u,v)` and the autonomous ODE

`u' = 0`,

`v' = 1-u^2`.

Let the certified tube be the square

`K = { |u| <= 1, |v| <= 1 }`.

Choose the two endpoints

`x_- = (-1,0)`, `x_+ = (1,0)`.

Both are equilibria, because `1-u^2=0` at `u=+-1`.  Therefore both endpoint
trajectories remain in `K` for every time.

The initial straight connector

`gamma_0(s) = (2s-1,0)`, `0<=s<=1`,

also lies entirely in `K`.

However the midpoint has `u=0`, hence

`Phi_t(gamma_0(1/2)) = (0,t)`.

For every `t>1` this point is outside `K`.

Thus even

- convex source tube,
- full initial-segment coverage, and
- both endpoint trajectories covered forever

**do not imply flowed-sheet coverage**.

Any finite-separation theorem that consumes only the two endpoint flowpipes and
then assumes all intermediate trajectories are covered is mathematically false.

---

## 2. Route A — exact inner-box / speed-cap bootstrap

This is the smallest source-facing closure when the contraction tube is an
axis-aligned box or contains one.

Let the state have finitely many coordinates indexed by `i`.  Fix a center `c`
and two half-width vectors

`0 <= r_i <= H_i`.

Define the inner and outer boxes

`B_in  := { x : |x_i-c_i| <= r_i for all i }`,

`B_out := { x : |x_i-c_i| <= H_i for all i }`.

Consider an ODE

`x' = f(t,x)`

on a horizon `0<=t<=h`, and assume the source packet proves on the whole outer
box

**(2.1)** `|f_i(t,x)| <= B_i`, with `B_i>=0`,

for every coordinate and every relevant time.

Assume the exact margin gates

**(2.2)** `r_i + h B_i <= H_i` for every `i`.

### Theorem A1 — one-trajectory bootstrap

If `x(0) in B_in`, then

**(2.3)** `x(t) in B_out` for every `0<=t<=h`.

### Proof

While the trajectory remains in `B_out`, (2.1) and the fundamental theorem of
calculus give

`|x_i(t)-x_i(0)| <= int_0^t |f_i(s,x(s))| ds <= t B_i`.

Therefore

`|x_i(t)-c_i|`
` <= |x_i(0)-c_i| + |x_i(t)-x_i(0)|`
` <= r_i + t B_i`
` <= r_i + h B_i`
` <= H_i`.

A first exit strictly before `h` is impossible, because the same estimate would
place the allegedly exiting coordinate inside its outer half-width.  At `t=h`,
continuity gives the closed inequality.  Hence the whole trajectory stays in
`B_out`.

The proof is a standard bootstrap, but its certificate is unusually cheap:
when all constants are rational/dyadic the trusted arithmetic is only addition,
multiplication and order.

### Square-only speed producer

A source need not evaluate `sqrt` to supply `B_i`.  It may instead prove

`f_i(t,x)^2 <= S_i`,

choose a rational `B_i>=0`, and check

**(2.4)** `S_i <= B_i^2`.

Ordered-ring arithmetic then yields `|f_i|<=B_i`.  Thus both the speed producer
and the margin consumer can remain radical-free.

---

## 3. Route A upgrades immediately to a whole path sheet

Take two initial states `x0,y0 in B_in` and choose the straight path

`gamma_0(s)=(1-s)x0+s y0`, `0<=s<=1`.

Because every axis-aligned box is convex,

**(3.1)** `gamma_0(s) in B_in` for all `s`.

Apply Theorem A1 separately to the trajectory starting from each
`gamma_0(s)`.  No discretization of `s` is needed.  One obtains

**(3.2) SHEET COVERAGE**

`Phi_t(gamma_0(s)) in B_out`

for every `0<=t<=h` and `0<=s<=1`.

Therefore, if T-P5-090/T-P5-094's tangent contraction theorem is certified on
`[0,h] x B_out`, the same-tube premise of T-P5-094 is automatically satisfied
for this pair of endpoints.

This gives a direct finite-separation pipeline:

`endpoint membership in B_in`
` -> straight connector in B_in`
` -> speed-margin gates (2.2)`
` -> whole flowed sheet in B_out`
` -> T-P5-094 path-energy contraction`.

There is no additional two-dimensional flowpipe object in the trusted core.
The continuum of intermediate trajectories is handled by universal
quantification over the initial box.

### Regression against the obstruction in Section 1

For `u'=0, v'=1-u^2` on horizon `h=2`, the initial connector has `v=0`, so one
could use `r_v=0`.  On the outer box `|u|<=1`, the exact speed cap is `B_v=1`.
With `H_v=1`, the margin test reads

`0 + 2*1 <= 1`,

which correctly fails.  The bootstrap therefore refuses exactly the false
endpoint-only inference exhibited above.

---

## 4. Route B — a two-level base-storage collar

Componentwise speed caps can be loose.  A second route uses any differentiable
**base-state** storage `U(t,x)`.

Fix exact levels

`R_in < R_out`.

Let

`K_in(t)  := { x : U(t,x) <= R_in }`,

`K_out(t) := { x : U(t,x) <= R_out }`.

Assume the outer sublevel is contained in the source/contraction tube on the
whole horizon.

Suppose that along every base trajectory while it lies in `K_out`, the source
certificate proves

**(4.1)** `nu * dU/dt <= -nu^2 U + E`,

with

**(4.2)** `nu > 0`,

**(4.3)** `E <= nu^2 R_in`.

The notation deliberately mirrors T-P5-091's division-free mixed-defect algebra,
but here `U` is a base-state storage with its own semantic binding.

### Theorem B1 — inner level is forward invariant

If `U(0,x(0)) <= R_in`, then

**(4.4)** `U(t,x(t)) <= R_in` for all `0<=t<=h`.

### Proof

Set

`Y(t):=U(t,x(t))-R_in`.

Using (4.1) and (4.3), while `U<=R_out`,

`nu Y'`
` = nu U'`
` <= -nu^2 U + E`
` <= -nu^2 U + nu^2 R_in`
` = -nu^2 Y`.

Equivalently,

`Y' + nu Y <= 0`.

Hence the integrating-factor quantity

`exp(nu t) Y(t)`

is nonincreasing on every interval on which the outer certificate applies.  If
`Y(0)<=0`, then

`Y(t)<=exp(-nu t)Y(0)<=0`.

The strict geometric gap `R_in<R_out` removes the usual boundary bootstrap
ambiguity: as long as `U<=R_in` the trajectory stays a positive level-distance
away from the edge of the region where (4.1) is known, so the differential
inequality remains available and the comparison extends over the whole
horizon.  Therefore `U<=R_in` is invariant.

The exponential occurs only in the mathematical proof.  The **instance
certificate** remains division-free and transcendental-free: the trusted data
need only satisfy `nu>0`, `R_in<R_out`, and `E<=nu^2 R_in`.

### Why two levels are useful

T-P5-091 observed that the sharp boundary gate may be non-strict,
`E<=nu^2 Vstar`.  If the differential theorem is only known exactly on the same
closed boundary, a naive first-exit proof can hide a tangency/coverage subtlety.
The two-level construction avoids that issue cleanly:

- `R_in` is the invariant working level;
- `R_out` is the certified collar on which the differential inequality and
  source semantics are valid.

No artificial strict defect slack is needed.

---

## 5. Convex initial storage gives sheet coverage with Route B

Suppose at `t=0` the map `x -> U(0,x)` is convex on the segment between `x0`
and `y0`, and both endpoints satisfy

`U(0,x0)<=R_in`, `U(0,y0)<=R_in`.

Then for

`gamma_0(s)=(1-s)x0+s y0`,

convexity gives

`U(0,gamma_0(s))`
` <= (1-s)U(0,x0)+sU(0,y0)`
` <= R_in`.

Applying Theorem B1 to every `s` yields

**(5.1)** `U(t,Phi_t(gamma_0(s)))<=R_in`

for all `t,s`.  Since `K_in(t) subset K_out(t)` and `K_out` is inside the
contraction-certified source tube, the entire flowed sheet is covered.

### Exact PSD quadratic special case

If

`U(0,x)=Q_P(x-c)=(x-c)^T P (x-c)`

with `P` symmetric PSD, there is an exact identity

**(5.2)**

`Q_P((1-s)a+s b)`
` = (1-s)Q_P(a)+sQ_P(b)-s(1-s)Q_P(a-b)`.

The last term is nonnegative, so the sublevel is convex.  This is the same
quadratic convex-combination identity used in T-P5-083 and is especially easy
to formalize without analytic convexity machinery.

Thus a common quadratic base-storage packet can close T-P5-094 sheet coverage
with no path sampling.

---

## 6. Do not confuse base-state storage with variational energy

This distinction is important enough to be a typed interface requirement.

T-P5-091 uses

`V_var = xi^T W(t,x) xi`

for a tangent vector `xi` and proves a robust differential inequality for the
**variational dynamics**.

T-P5-096 Route B instead needs a scalar

`U_base(t,x)`

whose sublevel contains actual base states and lies inside the source tube.

A small tangent energy does not imply that the base point `x` is in any desired
state box.  For example, taking `xi=0` makes `V_var=0` at every base point,
including points arbitrarily far outside the source domain.

Therefore a checker must not use the T-P5-091 variational barrier as a source
coverage certificate unless a separate theorem explicitly binds that energy to
base-state displacement.

The reusable piece from T-P5-091 is the **scalar differential algebra**
`nu U' <= -nu^2 U + E`, not the semantic identity of `U`.

---

## 7. Interaction with T-P5-094 path-energy contraction

T-P5-094 proves, under whole-sheet coverage, that for an initial path
`gamma_0` and its flowed image `gamma_h`,

`(N+2 mu h)^N E_h(gamma_h) <= N^N E_0(gamma_0)`.

T-P5-096 supplies exactly the missing premise by either Route A or Route B.
Hence a source/checker packet can be decomposed as follows.

### Route A packet

1. inner box half-widths `r_i`;
2. outer contraction/source box half-widths `H_i`;
3. same-outer-box component speed caps `B_i`;
4. horizon `h`;
5. exact gates `r_i+hB_i<=H_i`;
6. endpoint membership in the inner box;
7. T-P5-094 tangent/path-energy contraction on the outer box.

### Route B packet

1. base storage `U(t,x)`;
2. exact levels `R_in<R_out`;
3. inclusion `{U<=R_out} subset source/contraction tube`;
4. same-outer-level differential gate
   `nu dU/dt <= -nu^2 U + E`;
5. exact scalar checks `nu>0`, `E<=nu^2 R_in`;
6. convexity of the initial inner sublevel, or an explicit witness initial path
   inside it;
7. T-P5-094 tangent/path-energy contraction on the outer level.

Neither packet requires a mesh in `s`.  The trusted theorem quantifies over all
initial path points.

---

## 8. A useful hybrid: quadratic inner set, box outer tube

A practical source may have a sharp quadratic state certificate but a simple
box on which interval/CSE derivative bounds are available.

Suppose a quadratic sublevel

`Q_P(x-c)<=R`

is known to lie inside an inner box `|x_i-c_i|<=r_i`.  T-P5-077-style
coordinate containment can provide this relation with square-only gates.

Then the pipeline can use

`quadratic endpoint membership`
` -> quadratic segment convexity`
` -> inner-box membership`
` -> Route A speed bootstrap`
` -> outer-box sheet coverage`.

This avoids forcing the contraction/source producer to work directly on an
ellipsoid while still exploiting a much smaller initial set than the full outer
box.

---

## 9. Minimal theorem statements for Lean

The mathematics should be split into small leaves rather than one theorem that
mentions flows, metrics and path energies simultaneously.

### Leaf 1 — quadratic segment membership

Suggested shape:

`quadratic_segment_le_of_endpoints_le`

Premises:

- `P` symmetric PSD;
- `0<=s<=1`;
- `Q_P(a)<=R`, `Q_P(b)<=R`.

Conclusion:

`Q_P((1-s)a+s*b)<=R`.

A stronger reusable leaf is the exact identity (5.2).

### Leaf 2 — scalar speed integration

`abs_sub_le_mul_of_deriv_abs_le`

For differentiable `x:[0,h]->R`, if `|x'(t)|<=B` on the interval, prove

`|x(t)-x(0)|<=t*B`.

This is the only analytic ingredient needed for Route A.

### Leaf 3 — finite-dimensional box bootstrap

`trajectory_mem_outer_box_of_inner_mem_and_speed_caps`

Premises:

- initial coordinate margins `|x_i(0)-c_i|<=r_i`;
- speed caps on the outer box;
- `r_i+hB_i<=H_i`.

Conclusion:

`|x_i(t)-c_i|<=H_i` for all `t<=h`.

The first-exit/bootstrap wrapper should be kept separate from the scalar
integration leaf.

### Leaf 4 — two-level scalar storage invariance

`inner_level_invariant_of_outer_robust_deriv`

Premises:

- `nu>0`;
- `R_in<R_out`;
- `E<=nu^2 R_in`;
- while `U<=R_out`,
  `nu*U'<=-nu^2*U+E`;
- `U(0)<=R_in`.

Conclusion:

`U(t)<=R_in` on the horizon.

The proof may use an integrating factor/Gronwall internally; no exponential
appears in the theorem's instance-side arithmetic.

### Leaf 5 — sheet lifting by pointwise invariance

`flowed_path_sheet_mem_of_initial_path_mem_and_forward_invariant`

Premises:

- `forall s, gamma_0(s) in K_in`;
- every flow from `K_in` remains in `K_out` over `[0,h]`.

Conclusion:

`forall t s, Phi_t(gamma_0(s)) in K_out`.

This final leaf is logically trivial and should remain tiny; the substantive
work belongs in Leaves 2–4.

---

## 10. Source-facing recommendation

For a first deployed certificate, Route A is probably the cheapest:

- use the existing exact target/inner coordinate caps;
- generate componentwise base-vector-field caps on the same outer cell;
- verify `r_i+hB_i<=H_i`;
- then let T-P5-094 consume the resulting whole-sheet coverage theorem.

If those speed margins are too loose, do **not** immediately introduce a 2D
flowpipe over `(t,s)`.  First try Route B with an already available base-state
Lyapunov/storage sublevel and an outer collar.  This may preserve signed
cancellation and avoid coordinatewise worst cases.

Only if both reusable routes fail should a dedicated path-sheet flowpipe become
necessary.

---

## 11. What remains open

This child does **not** prove that the deployed P5 source currently possesses
any particular inner/outer box, speed cap, base-storage collar, or contraction
tube.  The following remain open:

1. bind the actual source tube on which T-P5-090/T-P5-095 contraction data hold;
2. choose either a same-tube component-speed packet or a base-storage packet;
3. for Route B, bind `U_base` separately from the variational energy;
4. prove outer-level/outer-box containment in the actual evaluator/ODE domain;
5. bind the actual horizon and endpoint set;
6. formalize the selected coverage leaf in Lean;
7. independent verification by 封不觉;
8. Float64/FD/controller/P8 semantics and all admission/registry gates.

Therefore the result remains **CONDITIONAL_PASS / pending mathematical child**.

---

## 12. Compact result

The open same-tube premise of T-P5-094 does not require sampling the continuum
of connecting trajectories.

A particularly cheap exact certificate is

`x0,y0 in B_in`,

`|f_i|<=B_i on B_out`,

`r_i+hB_i<=H_i`.

Convexity puts the entire initial segment in `B_in`; the speed bootstrap puts
every trajectory from that segment in `B_out`; hence the full flowed sheet is
covered and T-P5-094 can be applied.

When box-speed bounds are too loose, the alternative two-level theorem

`R_in<R_out`, `nu>0`, `E<=nu^2 R_in`,

`nu dU/dt <= -nu^2 U + E on {U<=R_out}`

makes `{U<=R_in}` forward invariant and yields the same sheet conclusion from a
convex initial sublevel.

The two-level gap is the key device that preserves the sharp non-strict defect
gate without a circular boundary-coverage argument.
