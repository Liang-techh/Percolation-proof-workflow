---
kind: review_result
review_id: review-T-P5-125-strong-convex-recenter-existence-honglianmozun-20260909T0455Z
task_id: T-P5-125-STRONG-CONVEX-RECENTER-EXISTENCE
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T04:55:00Z
claim_commit: ddf63672f7118e7b955e592f3e057e566549b6e2
inspected_commit: 07b6ea05936e828cd4defd5d54f5dde317db427c
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-123-radial-shaping-coercivity-split-honglianmozun-20260909T0358Z.md
    commit: 5ea34f5e5e65d5babc47a3d8ed04f578cbea7c28
  - path: agent_review_inbox/review-T-P5-124-CENTER-FORCE-MISMATCH-MIXED-COERCIVITY-guyuefangyuan-20260909T0424Z.md
    commit: c0934c14a71d4ee588ea910c018a6a5411520494
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_strong_convex_recenter_existence_then_bind_same_cell_shaped_potential_hessian_and_center_mismatch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; finite-dimensional strong-convexity, compact-minimum, and quadratic-form algebra only
exit_code: n/a
---

# T-P5-125 — strong-convex recenter existence from a root-free center-mismatch gate

## 0. Bottleneck selected

T-P5-124 gives two branches when the shaped scalar potential

`F(q) := U(q) - Psi(q)`

has nonzero center mismatch at the old anchor `q0`:

1. retain `q0`, add a constant floor `D`, and pay the unavoidable additive decay term `c D`; or
2. if a new critical point `q_*` is already known, recenter there and recover homogeneous coercivity.

The second branch was left with a genuine existence gap: `grad F(q_*)=0` was an external witness.

This review closes that mathematical gap on one certified convex ellipsoidal cell. The main result is a sharp root-free gate

**`B < 4 mu^2 R`**

which, together with a same-cell Hessian lower bound and a dual quadratic bound on the old-center force mismatch, forces a **unique interior critical point** `q_*`. It also gives the a-posteriori displacement bound

**`4 mu^2 Q(q_*-q0) <= B`**

and therefore a homogeneous recentered storage without the additive `D` floor.

No actual deployed P5 field, source packet, Float64/controller semantics, cell coverage, P8 flowpipe, Lean/kernel receipt, independent verification, admission, or registry promotion is claimed.

---

## 1. Same-cell setup

Work in a finite-dimensional real Euclidean space. Let

`Q(x) = x^T P x`

for a fixed symmetric positive-definite matrix `P`. For `R>0`, define the old-anchor ellipsoidal cell

`E_R := { q0 + x : Q(x) <= R }`.

Because `P` is positive definite, `E_R` is compact and convex.

Let `F` be `C^2` on an open neighborhood of `E_R`. Write

`b := grad F(q0)`.

Assume two quantitative packets on the **same** cell and same metric key.

### (H1) Strong Hessian lower packet

For every `z in E_R` and every vector `y`,

**`y^T Hess F(z) y >= 2 mu Q(y)`**

with `mu>0`.

The factor `2` is intentional: after the Taylor integral weight `integral_0^1 (1-s) ds = 1/2`, the resulting storage lower constant is exactly `mu`.

### (H2) Center-force dual packet

For every vector `x`,

**`<b,x>^2 <= B Q(x)`**

with `B>=0`.

The trusted theorem does not require `P^{-1}`. A source may obtain `B` from a direct PSD/dual-metric witness, but this child consumes only the inequality above.

### (H3) Root-free interior gate

**`B < 4 mu^2 R`.**

This is the only scalar comparison needed to force the new critical point to lie strictly inside the certified cell.

---

## 2. Boundary radial derivative is strictly outward

Fix any boundary displacement `x` with `Q(x)=R`. Along the chord `q0+s x`, the fundamental theorem of calculus gives

`<grad F(q0+x)-b, x>`

` = integral_0^1 x^T Hess F(q0+s x) x ds`

` >= integral_0^1 2 mu Q(x) ds`

` = 2 mu R`.

Hence

**(2.1)** ` <grad F(q0+x),x> >= <b,x> + 2 mu R`.

We claim the right side is strictly positive without taking a square root.

Suppose instead

`<b,x> + 2 mu R <= 0`.

Then `<b,x> <= -2 mu R`, so

`<b,x>^2 >= 4 mu^2 R^2`.

But the dual packet gives

`<b,x>^2 <= B R < 4 mu^2 R^2`,

a contradiction. Therefore every boundary point satisfies

**(2.2) STRICT OUTWARD RADIAL DERIVATIVE**

`<grad F(q0+x), x> > 0` whenever `Q(x)=R`.

This proof is completely root-free; the familiar norm comparison `sqrt(BR)<2muR` never needs to enter the trusted statement.

---

## 3. Existence of an interior critical point

Since `E_R` is compact and `F` is continuous, `F` attains a minimum at some `q_* in E_R`.

Assume for contradiction that the minimizer lies on the boundary. Write `q_*=q0+x_*` with `Q(x_*)=R`.

Define the one-dimensional radial restriction

`phi(t) := F(q0+t x_*)`,  `0<=t<=1`.

By (2.2),

`phi'(1)=<grad F(q_*),x_*> > 0`.

By continuity of `phi'`, for `t<1` sufficiently close to `1`, moving slightly inward decreases the value:

`phi(t) < phi(1)`.

But `q0+t x_*` lies in the interior of `E_R`, contradicting minimality of `q_*`.

Therefore the minimizer is interior. Fermat's rule gives

**(3.1) CRITICAL POINT EXISTENCE**

`grad F(q_*) = 0`,  with `Q(q_*-q0) < R`.

Thus T-P5-124's recentered branch does not need a separately guessed critical-point witness once (H1)-(H3) are available on a closed same-cell ellipsoid.

---

## 4. Uniqueness from strong monotonicity

Take any `q1,q2 in E_R` and put `d=q1-q2`. Convexity of `E_R` keeps the whole segment inside the cell, so

`<grad F(q1)-grad F(q2), d>`

` = integral_0^1 d^T Hess F(q2+s d)d ds`

` >= 2 mu Q(d)`.

If `q1!=q2`, positive definiteness of `P` gives `Q(d)>0`, hence

`<grad F(q1)-grad F(q2),d> > 0`.

Therefore `grad F` is injective on `E_R`. In particular there is at most one zero of `grad F` in the cell.

Combined with Section 3:

**(4.1) UNIQUE RECENTER**

There exists exactly one `q_* in int(E_R)` with `grad F(q_*)=0`.

This also shows the compact minimizer is the unique minimizer of `F` on `E_R`.

---

## 5. Root-free displacement bound for the new center

Write

`x_* := q_* - q0`,  `Q_* := Q(x_*)`.

Using `grad F(q_*)=0` and the same segment Hessian bound,

`-<b,x_*>`

` = <grad F(q_*)-b, x_*>`

` = integral_0^1 x_*^T Hess F(q0+s x_*)x_* ds`

` >= 2 mu Q_*`.

If `Q_*=0`, the desired bound is trivial. If `Q_*>0`, then

`4 mu^2 Q_*^2 <= <b,x_*>^2 <= B Q_*`.

Cancelling the positive scalar `Q_*` yields

**(5.1) CENTER DISPLACEMENT CERTIFICATE**

`4 mu^2 Q(q_*-q0) <= B`.

Together with `B<4mu^2R`, this independently reproduces `Q(q_*-q0)<R`.

The point is not merely qualitative existence: the same mismatch constant `B` that created T-P5-124's additive floor also quantitatively controls how far the exact equilibrium moves.

---

## 6. Homogeneous recentered coercivity with no additive floor

For any `q in E_R`, convexity keeps the segment from `q_*` to `q` inside `E_R`. Let `d=q-q_*`. Taylor's integral formula at the critical point gives

`F(q)-F(q_*)`

` = integral_0^1 (1-s) d^T Hess F(q_*+s d)d ds`

` >= integral_0^1 (1-s) 2 mu Q(d) ds`

` = mu Q(d)`.

Therefore

**(6.1) RECENTERED STORAGE COERCIVITY**

`mu Q(q-q_*) <= F(q)-F(q_*)`  for every `q in E_R`.

Thus the shaped mechanical storage

`V_*(q,v) := T(v) + F(q)-F(q_*)`

is homogeneous around the actual new center whenever the kinetic term has its usual nonnegative comparator. There is no constant floor `D`, so the specific `cD` decay debit in T-P5-124 disappears.

This does **not** say every other moving-chart, curl, forcing, controller, or hybrid term disappears; those remain separate channels. The result removes only the center-mismatch floor that arose from keeping the wrong anchor.

---

## 7. A root-free reserve for a recentered inner cell

A consumer often needs not only `q_* in E_R`, but a certified `q_*`-centered subcell that remains inside the original source cell.

Suppose a target recentered radius `r>=0` is chosen. From (5.1), define the available old-cell margin through the polynomial quantity

`Delta := 4 mu^2 (R-r) - B`.

Assume

**(7.1)** `Delta >= 0`,

**(7.2)** `Delta^2 >= 16 mu^2 B r`.

Then every `y` with `Q(y)<=r` satisfies

**(7.3)** `q_*+y in E_R`.

### Proof

Let `A:=B/(4mu^2)` only as explanatory notation; no trusted theorem needs the division. From (5.1), `Q(x_*)<=A`.

For the `P`-inner product, Cauchy-Schwarz gives

`<P x_*,y>^2 <= Q(x_*)Q(y) <= A r`.

Conditions (7.1)-(7.2) are exactly the division-free form of

`R-A-r >= 0`,

`(R-A-r)^2 >= 4 A r`.

Hence the cross term obeys

`2<Px_*,y> <= R-Q(x_*)-Q(y)`.

Therefore

`Q(x_*+y)`

` = Q(x_*)+Q(y)+2<Px_*,y>`

` <= R`.

This gives a useful downstream domain bridge: once `B,mu,R` are source-bound, a whole recentered collar can be certified without explicitly exporting the coordinate of `q_*`.

A simpler but more conservative sufficient gate is

`B + 4 mu^2 r <= 2 mu^2 R`,

obtained from `Q(x_*+y)<=2Q(x_*)+2Q(y)`.

---

## 8. Sharp threshold obstruction

The strict gate `B<4mu^2R` cannot be relaxed to `<=` if the conclusion demands an **interior** critical point.

Take one dimension with

`Q(x)=x^2`, `q0=0`, `R=1`, `mu=1`,

and

`F(x)=x^2-2x`.

Then

`F''(x)=2=2mu`,

`b=F'(0)=-2`,

so the sharp dual constant is `B=4` and

`B=4mu^2R`.

The unique critical point is

`x_*=1`,

exactly on the boundary. Hence equality does not force an interior recenter and supplies no positive source-cell reserve around it.

If instead `F(x)=x^2-3x`, then `B=9>4mu^2R` and the unique critical point is `x_*=3/2`, outside the cell entirely.

Therefore the threshold is sharp at the information level of the Hessian lower bound and center-force dual constant.

---

## 9. Why this is preferable to paying the T-P5-124 floor when the gate holds

T-P5-124's mixed same-anchor branch is valid and necessary when an exact recenter cannot be certified. But if (H1)-(H3) hold, paying a constant floor is structurally unnecessary:

- the old center mismatch `b` proves the new center cannot move farther than (5.1);
- strong convexity forces existence and uniqueness of the new critical point;
- normalization at `F(q_*)` restores homogeneous coercivity;
- the additive `cD` term caused solely by shifting the wrong-center storage is avoided.

Thus a source-facing decision rule is:

1. first test the strong-convex recenter gate `B<4mu^2R` on the same shaped potential/cell;
2. if it passes, use the recentered branch;
3. if it fails or a same-cell Hessian lower packet is unavailable, fall back to T-P5-124's mixed `D`-floor theorem rather than pretending an equilibrium exists.

This is a genuine branch selection, not an admission shortcut.

---

## 10. Candidate theorem statements

The minimal mathematical decomposition is:

### Theorem A — boundary radial positivity

From

- `Q(x)=R`, `R>0`, `mu>0`,
- `<b,x>^2 <= B Q(x)`,
- `B < 4mu^2R`,
- `<gradF(q0+x)-b,x> >= 2muQ(x)`,

conclude

`0 < <gradF(q0+x),x>`.

This is pure ordered-ring algebra after the calculus producer supplies the last premise.

### Theorem B — strong-convex ellipsoid recenter existence

For finite-dimensional `F` on compact convex `E_R`, from Theorem A on the boundary conclude existence of `q_* in int(E_R)` with `gradF(q_*)=0`. With strong monotonicity, conclude uniqueness.

### Theorem C — displacement bound

From

`gradF(q_*)=0`,

`-<b,x_*> >= 2muQ(x_*)`,

`<b,x_*>^2 <= BQ(x_*)`,

conclude

`4mu^2Q(x_*) <= B`.

### Theorem D — recentered coercivity

From `gradF(q_*)=0` and the same-cell Hessian lower packet, conclude

`mu Q(q-q_*) <= F(q)-F(q_*)`.

### Theorem E — recentered-cell inclusion reserve

From

`4mu^2 Q(x_*)<=B`, `Q(y)<=r`,

`Delta=4mu^2(R-r)-B>=0`,

`Delta^2>=16mu^2Br`,

conclude

`Q(x_*+y)<=R`.

The scalar/order leaves A, C, and most of E are suitable future Lean sidecars; the compact-minimum existence theorem should remain a separate calculus/topology layer.

---

## 11. Exact fail-closed boundaries

1. **No same-cell Hessian lower packet, no recenter existence claim.** A positive Hessian only at `q0` cannot exclude curvature loss before the boundary.
2. **No positive-definite displacement metric, no compact ellipsoid theorem.** A semidefinite `Q` can have unbounded zero-energy directions.
3. **Equality at the threshold is not enough for an interior point.** Section 8 gives an exact counterexample.
4. **The new center belongs to the old shaped scalar `F`.** A point satisfying `grad U=r` for a newly re-anchored radial potential is a different construction, as T-P5-124 already warns.
5. **Recentered coercivity does not prove actual source coverage.** The source must still bind the same physical `F`, `P`, `R`, Hessian packet, and mismatch packet on one cell.
6. **Do not double-charge center mismatch.** Once the proof actually recenters at the unique `q_*`, the old `D` floor from T-P5-124 must be removed rather than retained as another residual debit.

---

## 12. Source handoff reduced to a minimal packet

To instantiate this child on the deployed P5 problem, the producer needs only:

1. one exact shaped scalar `F=U-Psi` on a certified convex ellipsoidal cell `E_R`;
2. the cell metric `Q(x)=x^TPx` with `P>0`;
3. a same-cell Hessian lower packet `Hess F >= 2mu P`, `mu>0`;
4. the old-anchor signed mismatch `b=gradF(q0)`;
5. a dual packet `<b,x>^2<=BQ(x)`;
6. the scalar gate `B<4mu^2R`;
7. if a nontrivial recentered collar is consumed, a chosen `r` satisfying the Section 7 inclusion gates.

Once these are same-source and same-cell bound, the existence, uniqueness, displacement, and homogeneous recentered coercivity follow mathematically. Until then this result remains `pending` and must not be promoted to a physical certificate.