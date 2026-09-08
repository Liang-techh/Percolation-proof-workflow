---
kind: review_result
review_id: review-T-P5-083-nonlinear-step-segment-coverage-guyuefangyuan-20260908T1532Z
task_id: T-P5-083-NONLINEAR-STEP-SEGMENT-COVERAGE
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-08T15:32:00Z
claim_commit: b7ca7f986e9bc2da3721b1e19414a50928d0aacd
inspected_commits:
  - 72f430f93517ccf4bf5da5e26b29c83c56ef5e7b
  - e0551b1a078a7cffbf3275ce1fcbb52ce810ec74
  - 22ba1c3ffadf2abdb36a563de84c2f89ee6f5b35
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Insert this directly after T-P5-082. The apparently new step-segment-domain
  obligation is free whenever the nominal Euler endpoint remains in the same
  convex quadratic sublevel already certified inside the source/chart box by
  T-P5-077. Use the exact quadratic segment identity rather than introducing a
  separate coordinate speed/step-margin budget. If only a local Hessian cap is
  available, do not apply the T-P5-082 curvature estimate until this segment
  inclusion is proved. Prefer the squared Hessian packet below for a fully
  radical-free curvature budget.
---

# T-P5-083 — nonlinear Euler-segment coverage is a convexity consequence; squared curvature packet

## 0. Result in one line

T-P5-082 correctly leaves one domain premise explicit: its nonlinear-chart
curvature bound needs the Hessian cap on the whole segment

`z_t = z - t h G(z)`, `0 <= t <= 1`,

not merely at the starting point.  The first instinct is to create another
coordinatewise step-size budget.  In the P5 setting this is usually unnecessary.

If the nominal Euler endpoint

`z_E = z - h G(z)`

remains in the same root-centered quadratic sublevel as `z`, then **the entire
Euler segment remains in that sublevel automatically**, because quadratic
sublevels are convex.  T-P5-077 already supplies a radical-free gate placing
that sublevel inside the source/chart box.  Therefore the T-P5-082 Hessian cap
is valid on the whole segment with **zero additional step-domain charge**.

The key exact identity is, for any positive-semidefinite quadratic form `Q`,
any vectors `a,b`, and `0 <= t <= 1`,

**(0.1)**
`Q((1-t)a + t b)`
` = (1-t) Q(a) + t Q(b) - t(1-t) Q(a-b)`.

Hence

**(0.2)**
`Q((1-t)a+t b) <= (1-t)Q(a)+tQ(b)`.

So if

`V(z)=Q(z-z*) <= Vstar`

and a nominal corrector packet gives

**(0.3)** `V(z_E) <= q V(z)`

with merely

**(0.4)** `q V(z) <= Vstar`,

then for every `t in [0,1]`,

**(0.5)** `V(z_t) <= Vstar`.

At a full barrier level it is enough to have the familiar `0 <= q <= 1`.
No componentwise `|h G_i|` bound, no `sqrt(B_G)`, and no extra box margin is
needed for segment coverage.

There is also a cleaner fully squared curvature interface.  Suppose the chart
Hessian satisfies on the certified box `B`

**(0.6)**
`Q_W(D^2 T(u)[v,v]) <= K2 * Q_Z(v)^2`

for all `u in B`, and at the current state

**(0.7)** `Q_Z(G(z)) <= B_G`.

Then, using the exact T-P5-082 remainder

`r_curv = h^2 integral_0^1 (1-t) D^2T(z_t)[G,G] dt`,

weighted Cauchy-Schwarz on the integral gives directly

**(0.8)**
`4 Q_W(r_curv) <= K2 * h^4 * B_G^2`.

Thus a trusted exact-rational checker can certify `Q_W(r_curv) <= D_curv` from

**(0.9)** `K2 * h^4 * B_G^2 <= 4 D_curv`.

This version never needs to represent `sqrt(K2)` or an unsquared Hessian norm.
It composes directly with the additive-defect gates of T-P5-078/T-P5-081, or
with T-P5-080 when signed correlation is available.

A sharp logical obstruction is also recorded below: a Hessian cap known only at
the starting point or only on a box that the segment leaves is not enough.  For
`T(z)=z^6`, the local bound `|T''(u)|<=30` is valid on `[-1,1]`.  But starting at
`z=0` and taking `h=1, G=-2` gives endpoint `z_E=2` and exact Taylor/curvature
remainder `64`, while blindly reusing the local cap would predict at most
`(30/2)*4=60`.  So segment coverage is a real premise; convexity is what makes
it free once both endpoints are in the same certified convex set.

This result is mathematics/interface only.  It does not bind a deployed chart,
nominal contraction packet, source Hessian packet, Float64/controller/FD
implementation, P8/ODE coverage, Lean/kernel receipt, provenance, admission,
registry state, or parent closure.

---

## 1. Exact quadratic segment identity

Let `W` be symmetric positive semidefinite and

`Q(x) = x^T W x`.

For arbitrary vectors `a,b` and scalar `t`, expand

`(1-t)a + t b`.

Bilinearity and symmetry give

`Q((1-t)a+t b)`
` = (1-t)^2 Q(a) + t^2 Q(b) + 2t(1-t) <a,b>_W`.

Also

`Q(a-b)=Q(a)+Q(b)-2<a,b>_W`,

so

`2<a,b>_W = Q(a)+Q(b)-Q(a-b)`.

Substituting yields

`Q((1-t)a+t b)`
` = [(1-t)^2+t(1-t)]Q(a)`
`   + [t^2+t(1-t)]Q(b)`
`   - t(1-t)Q(a-b)`
` = (1-t)Q(a)+tQ(b)-t(1-t)Q(a-b)`.

This proves (0.1) exactly.

If `0<=t<=1`, then `t(1-t)>=0`; PSD gives `Q(a-b)>=0`, hence (0.2).
No norm, square root, eigenvalue, or inverse is used.

### Corollary 1.1 — quadratic sublevels are segment closed

Fix center `z*` and `Vstar>=0`.  Define

`E(Vstar) = {z : Q(z-z*) <= Vstar}`.

If `z0,z1 in E(Vstar)`, then every

`z_t=(1-t)z0+t z1`, `0<=t<=1`,

also lies in `E(Vstar)`.

Indeed apply (0.2) to `a=z0-z*`, `b=z1-z*`:

`Q(z_t-z*) <= (1-t)Vstar+tVstar = Vstar`.

This is the exact bridge needed by T-P5-082.

---

## 2. Nominal corrector contraction automatically covers the whole Euler segment

Let

`z_E = z-hG(z)`

and suppose an existing nominal P5 theorem gives

`V(z_E) <= q V(z)`, `q>=0`,

where

`V(u)=Q(u-z*)`.

Assume the current point satisfies

`V(z)<=Vstar`

and additionally

`q V(z)<=Vstar`.

Then `V(z_E)<=Vstar`; both endpoints are in `E(Vstar)`.  Corollary 1.1 gives

### Theorem 2.1 — nominal Euler segment stays in the same barrier

For every `t in [0,1]`,

**(2.1)**
`V(z-t h G(z)) <= Vstar`.

A convenient uniform specialization is:

- `V(z)<=Vstar`,
- `0<=q<=1`,
- `V(z_E)<=qV(z)`.

Then (2.1) follows with no state-dependent extra gate.

This theorem should consume an already-proved nominal contraction factor rather
than duplicate the T-P5-075/T-P5-078 strong-monotonicity algebra.

### Important boundary

An *actual defective* step being inside the barrier does not, by itself, prove
that the nominal endpoint `z_E` is inside it.  T-P5-082's curvature integral is
along the nominal segment, so the packet should explicitly identify which
endpoint theorem is being consumed.  In the present P5 stack the nominal
contraction factor is normally available separately, which is why the segment
coverage can be free.

---

## 3. Composition with T-P5-077 source-box containment

T-P5-077 supplies a radical-free theorem of the form

**(3.1)** `E(Vstar) subseteq B`,

where `B` is the source box on which the strong-monotonicity/Lipschitz/source
packets are valid.

Combining Theorem 2.1 with (3.1) gives immediately:

### Theorem 3.1 — Hessian-domain segment coverage from an existing invariant ball

Assume:

1. `V(z)<=Vstar`;
2. `V(z_E)<=qV(z)` and `qV(z)<=Vstar`;
3. `E(Vstar) subseteq B`.

Then for every `t in [0,1]`,

**(3.2)** `z-t hG(z) in B`.

Therefore any source theorem whose hypotheses are stated uniformly on `B`, in
particular the nonlinear-chart Hessian cap required by T-P5-082, may be used on
the whole Euler segment.

The practical point is that **there is no new coordinate-speed budget to pay**.
If T-P5-077 has already paid for a convex invariant sublevel inside the source
box and the nominal corrector preserves it, the T-P5-082 step-domain obligation
is already mathematically discharged.

---

## 4. Even weaker fallback: boxes themselves are convex

Sometimes the source adapter has no root-centered quadratic barrier but can
prove endpoint box membership directly.  Axis-aligned boxes are convex, so one
still does not need componentwise speed bounds.

Let

`B = product_i [c_i-H_i,c_i+H_i]`.

If `z in B` and `z_E in B`, then for each coordinate

`(z_t)_i = (1-t)z_i+t(z_E)_i`

is a convex combination of two points in the same interval.  Hence

### Theorem 4.1 — endpoint box membership implies full segment membership

`z,z_E in B` implies `z_t in B` for all `0<=t<=1`.

Only if endpoint membership itself is unavailable should the checker fall back
to a stronger coordinate-step condition such as

`|z_i-c_i|<=R_i`, `R_i<=H_i`,

and a radical-free squared step gate

`w_i (H_i-R_i)^2 >= h^2 B_G`

when `w_i G_i^2 <= Q_W(G)<=B_G`.

That fallback is valid, but it should not be the default because it throws away
the convexity information already present in the invariant-barrier lane.

---

## 5. A fully squared curvature theorem

T-P5-082 states the curvature bound with an unsquared Hessian constant `K_T`:

`||D^2T(u)[v,v]||_W <= K_T ||v||_Z^2`.

For exact-rational source packets it is cleaner to square this interface from
the beginning.

Assume for every segment point `u=z_t` and every relevant `v`,

**(5.1)**
`Q_W(D^2T(u)[v,v]) <= K2 * Q_Z(v)^2`,

with `K2>=0`, and suppose

**(5.2)** `Q_Z(G(z)) <= B_G`, `B_G>=0`.

Write

`H_t = D^2T(z_t)[G,G]`.

The exact curvature remainder is

`r = h^2 integral_0^1 (1-t) H_t dt`.

Use Cauchy-Schwarz for the weighted Hilbert-valued integral:

`Q_W(integral f_t dt)`
` <= (integral a_t dt) * (integral Q_W(f_t)/a_t dt)`

with the standard specialization `f_t=(1-t)H_t`, equivalently

**(5.3)**
`Q_W(integral_0^1 (1-t)H_t dt)`
` <= (integral_0^1 (1-t)dt)`
`    * (integral_0^1 (1-t)Q_W(H_t)dt)`.

Since `integral_0^1 (1-t)dt = 1/2`, (5.1)-(5.2) give

`Q_W(H_t) <= K2 * B_G^2`.

Therefore

`Q_W(integral_0^1 (1-t)H_t dt)`
` <= (1/2)*(1/2)*K2*B_G^2`
` = K2*B_G^2/4`.

Scaling by `h^2` in the vector and hence `h^4` in the quadratic form yields

### Theorem 5.1 — radical-free squared curvature budget

**(5.4)**
`4 Q_W(r_curv) <= K2 * h^4 * B_G^2`.

Thus the exact checker gate

**(5.5)** `K2*h^4*B_G^2 <= 4*D_curv`

implies

**(5.6)** `Q_W(r_curv) <= D_curv`.

No trusted square root is needed.  The source can produce `K2` directly as a
rational polynomial/interval upper bound for the squared Hessian action.

### Why this is slightly better than simply naming `K2=K_T^2`

A source checker may be able to bound the squared polynomial quantity
`Q_W(D^2T[v,v])` directly and substantially more tightly than first bounding
each absolute component, summing to an unsquared norm `K_T`, and then squaring.
So (5.1) should be treated as its own preferred source contract, not merely as a
notation change.

---

## 6. Exact obstruction: local Hessian cap without segment coverage can be false

Take the one-dimensional chart

`T(z)=z^6`.

On the certified source interval

`B=[-1,1]`,

`T''(z)=30z^4`, hence

**(6.1)** `|T''(z)| <= 30` on `B`.

Now choose

`z=0`, `h=1`, `G=-2`.

Then

`z_E=z-hG=2`,

so the segment `[0,2]` leaves `B`.  The exact second-order chart remainder is

`T(2)-T(0)-T'(0)*(2-0)`
` = 64-0-0`
` = 64`.

If one incorrectly reused the local constant `K_T=30` from `[-1,1]` despite the
segment leaving that interval, the T-P5-082 estimate would claim

`|r| <= (30/2)*1^2*|-2|^2 = 60`,

which is false because `64>60`.

This is a concrete exact-rational/polynomial regression showing that the phrase
"Hessian cap on the whole step segment" is not bureaucratic decoration.  It is
mathematically necessary.  The new contribution of T-P5-083 is that, in the
usual P5 invariant-ball situation, convexity proves that premise at zero extra
budget.

---

## 7. Recommended theorem decomposition for Lean

The minimum useful formalization is small and should remain separate from the
large nonlinear-chart differential identity.

Suggested algebraic lemmas:

1. `quadratic_convex_combo_identity`

   For symmetric PSD `W`, prove

   `Q ((1-t) • a + t • b)`
   ` = (1-t)*Q a + t*Q b - t*(1-t)*Q (a-b)`.

2. `quadratic_sublevel_segment_mem`

   From `0<=t<=1`, `Q a<=Vstar`, `Q b<=Vstar`, derive the same bound for the
   convex combination.

3. `nominal_euler_segment_mem_of_contract`

   Consume `V z<=Vstar`, `V zE<=q*V z`, `q*V z<=Vstar`; conclude every
   `z-t h G` is in the same sublevel.

4. `box_segment_mem`

   Pure coordinate fallback: endpoint membership in a product interval implies
   segment membership.

5. `curvature_sq_le_of_hessian_sq`

   Later calculus layer: combine the exact T-P5-082 integral remainder with
   squared Hessian action and the integral Cauchy bound to produce
   `4*Q_W r <= K2*h^4*B_G^2`.

The first four are source-independent and need no `Real.sqrt`.  The fifth is the
only one that needs the analytic integral/Hessian API and can be delayed if the
Lean lane wants to land the segment logic first.

---

## 8. Integration boundary / remaining obligations

This review closes only the **mathematical step-segment coverage interface** for
the nonlinear finite-step chart lane.

Still open:

- whether the deployed normalization is nonlinear at all;
- the actual nominal endpoint/contraction theorem on the same state key;
- the T-P5-077 sublevel-to-source-box packet on that same chart domain;
- a source-bound squared Hessian constant `K2`;
- a same-coordinate `B_G` packet;
- evaluator/Float64/FD/controller semantics;
- P8/ODE trajectory and physical coverage;
- Lean/kernel/comparator evidence;
- independent validation by 封不觉;
- provenance, admission, registry mutation, and P5/P8/M4 parent closure.

Admission remains **pending mathematical child**.
