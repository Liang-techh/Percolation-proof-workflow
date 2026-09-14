---
kind: review_result
review_id: review-T-P5-207-copositive-error-polar-cuts-honglianmozun-20260910T0248Z
task_id: T-P5-207-COPOSITIVE-ERROR-POLAR-CUTS
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T02:48:26Z
claim_commit: 8cc835a42fa0cc7465c6bb3bcb52754e8b9669a8
inspected_commit: c31aff28cb5c8632cc62948235f253dc579aeb98
upstream_commits:
  - 37f9f4fb4865e4bd61b0541636f46ba622d17ca7  # T-P5-204 support-slack Lyapunov margin
  - f3c7325dd1cb49f0e93523c11bed546502e77981  # T-P5-205 copositive reference reserve extraction
  - 35e841a7aa73ffe7f41c586f0409d0a5f4948201  # T-P5-206 multi-support error allocation
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_error_witness_halfspace_theorem; add_strict-reference-polar-form; add_zero-energy-face-gate; add_rational-failure-cut; add_anchor-witness-ray-sandwich
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact homogeneous quadratic identities; finite-dimensional convex polarity; rational-density strict witness argument; exact 2x2 copositive regression; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-207 — exact polar cuts for simultaneous Lyapunov support-error budgets

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-206 gives a sound **inner approximation** of the simultaneous support-error safe region by taking convex/downward hulls of already-certified safe anchors. What is still missing is the mathematically dual object: a cheap **outer approximation** and exact FAIL witness that says why a proposed support-error vector cannot fit inside the remaining Lyapunov energy.

This child closes that seam.

For one common selector/source key, let

`C(Delta) = C0 - sum_k Delta_k Q_k`,

where `C0` and all `Q_k` are symmetric copositive and `Delta>=0`. For every selector state `y>=0`, define

`c0(y)=y^T C0 y`,

`q_k(y)=y^T Q_k y`,

`q(y)=(q_1(y),...,q_m(y))`.

Then the exact safe region is the intersection of witness halfspaces

**`E = intersection_{y>=0} {Delta>=0 : Delta · q(y) <= c0(y)}`.**

Thus every nonnegative state `y` is not merely a copositivity witness: it is a linear cut in support-error space. If a candidate `Delta` violates that cut, the same `y` is an explicit negative-energy direction for `C(Delta)`.

When `C0` is strictly copositive on the normalized orthant, division by the reference energy is legitimate and the whole safe region is exactly the polar of a compact ratio body:

**`E = {Delta>=0 : sup_{r in R} Delta·r <= 1}`**, 

`R = conv { q(y)/c0(y) : y>=0, y!=0 }`.

When `C0` has zero-energy directions, the division-free theorem remains valid and exposes an additional exact zero-face compatibility gate: any error coordinate that loads a zero-reference-energy direction must be forced to zero unless its debit also vanishes there.

For rational matrices and a rational unsafe candidate `Delta`, every strict copositivity failure admits a **rational** nonnegative witness, hence a rational linear cut. Combining these outer witness cuts with T-P5-206 safe anchors yields a two-sided certificate for a requested error ray. If a safe-anchor lower bound and one witness-cut upper bound meet at the same rational scale, the true joint error threshold is proved exactly without solving a global optimization problem.

No actual P5 matrix values, source/selector binding, physical coverage, Float64 enclosure, Lean/kernel proof, independent verification, admission, registry promotion, or parent closure is claimed.

---

## 1. Common-key energy setup

Fix one selector sector and one source/configuration key. Assume

- `C0 in Sym_n` is copositive;
- `Q_1,...,Q_m in Sym_n` are copositive;
- `Delta in R_+^m` is the vector of support-cap overestimates already isolated by T-P5-200/T-P5-204.

Define

`C(Delta):=C0-sum_k Delta_k Q_k`.

For `y>=0`, define scalar energies

`c0(y):=y^T C0 y >=0`,

`q_k(y):=y^T Q_k y >=0`.

Then

**`y^T C(Delta)y = c0(y)-Delta·q(y)`.**

The Lyapunov-safe simultaneous error set is

`E := {Delta>=0 : C(Delta) is copositive}`.

All statements below are homogeneous in `y`; one may therefore normalize to

`Sigma := {y>=0 : 1^T y = 1}`

without changing any condition on a nonzero witness.

---

## 2. T207-A — exact witness-halfspace representation

For every nonzero `y>=0`, define the closed halfspace

`H_y := {Delta>=0 : Delta·q(y) <= c0(y)}`.

### Theorem

**`E = intersection_{y>=0, y!=0} H_y`.**

Equivalently it is enough to intersect over `y in Sigma`.

### Proof

By definition,

`Delta in E`

iff

`y^T C(Delta)y >=0` for every `y>=0`

iff

`c0(y)-Delta·q(y)>=0` for every `y>=0`

iff

`Delta·q(y)<=c0(y)` for every `y>=0`.

That is exactly membership in every `H_y`. Homogeneity gives the normalized version. QED.

### Consequence: exact FAIL cut

If some `y>=0` satisfies

`Delta·q(y) > c0(y)`,

then

`y^T C(Delta)y < 0`.

So the same state simultaneously supplies

1. a concrete negative Lyapunov-energy witness for the proposed support budget; and
2. a linear separating cut `Delta'·q(y)<=c0(y)` obeyed by **every** truly safe `Delta'`.

This is the outer counterpart of T-P5-206's safe-anchor inner certificate.

---

## 3. T207-B — strict-reference polar body

Assume now that `C0` is **strictly copositive** on nonzero nonnegative states. Since `Sigma` is compact and `c0` is continuous, there exists

`mu0 := min_{y in Sigma} c0(y) > 0`.

Therefore the ratio map

`r(y):=q(y)/c0(y) in R_+^m`

is continuous on `Sigma`.

Let

`R0 := {r(y): y in Sigma}`

and

`R := conv(R0)`.

Because `R0` is compact in finite dimension, `R` is compact.

### Polar theorem

**`E = {Delta>=0 : sup_{r in R} Delta·r <= 1}`.**

Equivalently,

**`E = R^circ_1 intersection R_+^m`**

for the level-one polar `R^circ_1={Delta: Delta·r<=1 for all r in R}`.

### Proof

For `y in Sigma`, T207-A gives

`Delta·q(y)<=c0(y)`.

Since `c0(y)>0`, divide by it:

`Delta·r(y)<=1`.

A linear functional has the same supremum on a set and on its convex hull, so requiring this for all `r(y)` is equivalent to

`sup_{r in R} Delta·r<=1`.

QED.

### Structural meaning

The simultaneous support-error problem is exactly a convex polarity problem:

- state directions generate the **ratio body** `R`;
- admissible support errors form its level-one polar;
- a dangerous state direction is a supporting hyperplane of the error budget.

T-P5-206's anchor hull approximates `E` from inside; a finite witness library approximates it from outside.

---

## 4. T207-C — zero-reference-energy face

Strict copositivity of `C0` is useful but is not required for the division-free theorem. Define the normalized zero-energy set

`Z0 := {z in Sigma : c0(z)=0}`.

For any `z in Z0`, T207-A requires

`Delta·q(z)<=0`.

But `Delta>=0` and every component of `q(z)` is nonnegative. Therefore safety is equivalent on this face to

**`Delta·q(z)=0` for every `z in Z0`.**

In particular, define

`J_bad := {k : exists z in Z0 with q_k(z)>0}`.

### Zero-face gate

Every safe `Delta` must satisfy

**`Delta_k=0` for every `k in J_bad`.**

### Proof

Choose `k in J_bad` and a corresponding `z` with `q_k(z)>0`. If `Delta_k>0`, then

`Delta·q(z) >= Delta_k q_k(z) >0=c0(z)`,

contradicting T207-A. QED.

After imposing those forced zero coordinates, the remaining positive-reference-energy directions still contribute the ratio inequalities

`Delta·q(y)/c0(y)<=1`, `c0(y)>0`.

No division by zero is ever needed.

### Important boundary

The zero-face gate is necessary but not by itself sufficient. Ratios can become arbitrarily restrictive along sequences with `c0(y)->0+`. The exact theorem remains the full halfspace intersection of T207-A.

---

## 5. T207-D — rational strict failure witnesses

Assume `C0,Q_k`, and the proposed `Delta` all have rational entries.

Suppose `Delta` is unsafe. Then there exists a real `y>=0`, `y!=0`, with

`f(y):=c0(y)-Delta·q(y)<0`.

Normalize `y` into `Sigma`. Since `f` is a polynomial and the inequality is strict, there is an open relative neighborhood of `y` in `Sigma` on which `f<0` remains true.

Rational points are dense in every face of the rational simplex `Sigma`. Hence there exists

`y_Q in Sigma intersection Q^n`

with

**`c0(y_Q)-Delta·q(y_Q)<0`.**

### Rational-cut corollary

Every strict failure of a rational candidate has a rational witness cut

**`Delta'·q(y_Q) <= c0(y_Q)`**

that excludes the candidate exactly.

The trusted checker needs only rational matrix-vector multiplication and an exact sign comparison. It does not need an eigenvector or numerical minimizer.

### What is not claimed

This density argument proves existence of a rational strict witness; it does not prescribe a polynomial-time search algorithm for finding one. A numerical copositivity solver may propose the witness, after which rational reconstruction plus exact sign checking is sufficient.

---

## 6. T207-E — finite witness outer polyhedron

Let `W={w^(1),...,w^(N)}` be any finite library of nonnegative witness states. Define

`O_W := {Delta>=0 : Delta·q(w^(j)) <= c0(w^(j)) for j=1,...,N}`.

Then directly from T207-A,

**`E subseteq O_W`.**

Thus `O_W` is a rational polyhedral **outer approximation** whenever the matrices and witness states are rational.

This has a safe fail-closed interpretation:

- if a proposed `Delta` violates one stored cut, it is rigorously unsafe;
- if it satisfies every stored cut, it is only **not yet disproved**;
- passing a finite witness library must never be relabeled as global copositivity unless another theorem closes the gap.

Every newly discovered negative-energy witness monotonically shrinks `O_W` while preserving `E subseteq O_W`.

---

## 7. T207-F — inner-anchor / outer-witness ray sandwich

Fix a requested error profile `d>=0`, `d!=0`, and define the true ray threshold

`theta(d):=sup{t>=0 : t d in E}`.

### Outer bound from one witness

For any `w>=0` with

`d·q(w)>0`,

T207-A implies every safe scale satisfies

`t <= c0(w)/(d·q(w))`.

Hence

**`theta(d) <= theta_out(w;d):=c0(w)/(d·q(w))`.**

If `c0(w)=0<d·q(w)`, then `theta(d)=0` immediately.

For a finite witness library,

`theta(d) <= min_j theta_out(w^(j);d)`

over those witnesses with positive denominator.

### Inner bound from T-P5-206

Suppose T-P5-206's safe-anchor LP supplies a rational certificate that

`t_in d`

lies below a convex combination of certified safe anchors. Then

**`t_in d in E`**, hence

**`t_in <= theta(d)`.**

Therefore

**`t_in <= theta(d) <= t_out`.**

This is an exact two-sided Lyapunov support-budget bracket built from two finite rational packets.

---

## 8. T207-G — finite exactness when contact meets a safe anchor

The previous sandwich becomes an exact threshold certificate if the two sides meet.

Assume

1. a T-P5-206 anchor certificate proves `t_* d in E`; and
2. a nonnegative witness `w` satisfies

`d·q(w)>0`

and

**`c0(w)=t_* d·q(w)`.**

### Contact theorem

Then

**`theta(d)=t_*`.**

### Proof

The safe-anchor certificate gives `theta(d)>=t_*`.

For any `t>t_*`, the same witness gives

`w^T C(td) w`

`= c0(w)-t d·q(w)`

`= (t_*-t)d·q(w)`

`<0`.

Therefore no `t>t_*` is safe, so `theta(d)<=t_*`. QED.

### Root-free rational form

If `t_*=p/q` with `p>=0,q>0`, exact contact can be checked without division as

**`q c0(w)=p d·q(w)`.**

Then the complete threshold packet consists only of

- the existing T-P5-206 rational safe-anchor weights;
- one rational witness `w>=0`;
- `d·q(w)>0`;
- the cross-multiplied contact equality.

No generalized eigenvalue, square root, inverse, pseudoinverse, or optimization result needs to enter the trusted packet.

---

## 9. T207-H — exact curved regression: the safe region need not be polyhedral

It is important not to overinterpret either the anchor polytope or a finite witness polyhedron as the true geometry.

Take

`C0 = [[1,0],[0,1]]`,

`Q1 = [[1,0],[0,0]]`,

`Q2 = [[0,1],[1,0]]`.

Both debit matrices are copositive on `R_+^2` because

`y^T Q1 y = x^2>=0`,

`y^T Q2 y = 2xy>=0`.

For `Delta=(a,b)>=0`,

`C(Delta) = [[1-a,-b],[-b,1]]`.

Its energy is

`q_Delta(x,y)=(1-a)x^2-2bxy+y^2`.

For fixed `x>0`, write `t=y/x>=0`. Then

`q_Delta/x^2 = (1-a)-2bt+t^2`

`= (t-b)^2 + 1-a-b^2`.

Therefore the exact copositive condition is

**`a+b^2<=1`.**

So the simultaneous safe region is

**`E={(a,b)>=0 : a+b^2<=1}`**, 

a genuinely curved set.

At a boundary point with rational `b`, the state

`w=(1,b)`

is an exact contact witness because

`w^T C(a,b) w = 1-a-b^2=0`.

For any candidate with `a+b^2>1`, the same formula gives a strict negative witness whenever `w=(1,b)` is used for that candidate.

### Consequence

There is no general theorem that a finite anchor library or a finite witness library will exactly recover the whole safe region. The correct safe architecture is two-sided:

- anchors provide certified inner geometry;
- witness cuts provide certified outer geometry;
- exactness is declared only when the two meet on the queried profile or a separate global theorem closes the set.

---

## 10. T207-I — cutting-plane routing without false promotion

A practical exact-arithmetic loop for a fixed source/selector key is now:

1. Keep T-P5-206 safe anchors `A_safe`.
2. Keep T207 rational failure witnesses `W_fail`.
3. For a desired profile `d`, solve the anchor LP to get a safe lower scale `t_in`.
4. Evaluate all witness cuts to get an unsafe-side upper scale `t_out`.
5. If `t_in=t_out` exactly, emit the T207-G threshold certificate.
6. If a candidate between the bounds is directly proved copositive, add it as a new safe anchor.
7. If it is disproved, rationalize/check the negative state and add the resulting witness cut.

Every step preserves

**`inner_safe_region subseteq E subseteq outer_witness_region`.**

A solver timeout or inconclusive midpoint test simply leaves a nonzero bracket. It is not evidence of safety or failure.

No finite-termination theorem is claimed for a general curved `E`.

---

## 11. Relationship to T-P5-204/205/206

### T-P5-204

T204 gives the scalar/generalized-copositive threshold for support-cap slack and identifies zero-slack obstructions. T207 lifts the same pointwise energy principle to the full multi-error space and records each violating state as a reusable linear cut.

### T-P5-205

A positive reference reserve from T205 can make `C0` strictly copositive relative to the chosen physical gauge. In that corridor T207-B's compact polar body is particularly clean. T207 does not assume that such a reserve always exists; T207-C handles zero-reference-energy directions explicitly.

### T-P5-206

T206 gives **safe anchors / inner approximation**. T207 gives **failure witnesses / outer approximation**. They are dual in use but disjoint in proof:

- T206 certifies safety from convex combinations of known-safe matrices;
- T207 certifies failure from one state direction and globally characterizes safety as the intersection of all such state cuts.

Neither result replaces the other.

---

## 12. Candidate theorem statements

### Candidate A — `copositive_error_region_eq_witness_intersection`

If `C0,Q_k` are symmetric copositive and `C(Delta)=C0-sum Delta_k Q_k`, then for `Delta>=0`,

`Copositive(C(Delta))`

iff

`forall y>=0, Delta·q(y)<=c0(y)`.

### Candidate B — `strict_reference_error_region_polar`

If additionally `C0` is strictly copositive on the normalized orthant, then the safe error region equals the level-one polar of `conv{q(y)/c0(y)}` intersected with the nonnegative error orthant.

### Candidate C — `zero_reference_energy_forces_zero_error_coordinate`

If `z>=0`, `c0(z)=0`, and `q_k(z)>0`, then every safe `Delta` satisfies `Delta_k=0`.

### Candidate D — `rational_unsafe_error_has_rational_state_witness`

For rational `C0,Q_k,Delta`, if `C(Delta)` is not copositive, there exists rational `y>=0`, `y!=0`, with `y^T C(Delta)y<0`.

### Candidate E — `safe_anchor_contact_witness_exact_ray_threshold`

If `t_* d` is certified safe and some `w>=0` satisfies `c0(w)=t_* d·q(w)` with `d·q(w)>0`, then `t_*` is the exact safe threshold along ray `d`.

---

## 13. Boundaries remaining OPEN

This review does **not** prove:

1. actual source-bound `C0,Q_k` for P5;
2. actual selector/cell identity or same-key coverage;
3. that `C0` is strictly copositive for any real sector;
4. a finite witness set that globally represents a curved safe region;
5. finite termination of the anchor/cut refinement loop;
6. an efficient algorithm for discovering a rational witness, beyond exact checking once proposed;
7. Float64 or interval enclosure of candidate witnesses/caps;
8. controller, ODE, PDE, trajectory, or physical-source semantics;
9. Lean/kernel compilation or independent 封不觉 verification;
10. admission, registry eligibility, or parent theorem closure.

All remain external/pending.

---

## 14. Structural fingerprint

The new energy structure is

**`reference Lyapunov energy`**

`minus`

**`support-error debit`**

`=> state-wise linear inequality in error coordinates`

`=> exact witness halfspaces`

`=> strict-reference polar body / zero-energy compatibility face`

`=> rational negative-energy cuts`

`=> T206 inner anchors + T207 outer witnesses`

`=> exact ray threshold when safe contact and failure cut meet`.

This is a useful separation of responsibilities: the support solver proposes error budgets, the Lyapunov layer supplies safe anchors and dangerous state cuts, and the trusted consumer only checks rational quadratic evaluations plus finite linear inequalities.