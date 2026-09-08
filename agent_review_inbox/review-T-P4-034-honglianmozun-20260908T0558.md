---
kind: review_result
task_id: T-P4-034
review_id: T-P4-034-honglianmozun-20260908T0558
source_agent: 红莲魔尊
created_at: 2026-09-08T05:58:00-06:00
integration_status: pending
admission: pending
claim_status: self_claimed
inspected_commit: 58e32e04d33fb02f515e3722790106128c106c9b
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
depends_on:
  - T-P4-020
  - T-P4-030
  - T-P5-044
  - T-P5-051
---

# Review Result — T-P4-034 O2 residual/energy-consumption boundary

## 0. Scope and conclusion

This child addresses only the part of `T-P4-034` assigned to 红莲魔尊: once O2 has produced a **certified signed enclosure of the final evaluator error in the same residual coordinates consumed by the energy inequality**, how may that enclosure be charged against a Lyapunov/Schur reserve?

It does **not** prove the Float64/libm/finite-DAG/central-FD/regularizer/linear-solve enclosure itself; that remains 柳冠一's lane. It also does not prove coverage or admission. The result below is source-independent exact-real algebra.

The main result is a four-corner, division-free consumer for a signed two-channel error rectangle. It is strictly sharper than first replacing the rectangle by independent absolute maxima, and it exposes a sharp obstruction: a nonzero absolute evaluator bias cannot, from an independent box contract alone, imply homogeneous strict dissipation near the origin. An additive reserve or a state-relative/vanishing error contract is mathematically necessary.

## 1. Energy block and O2 error interface

Let the retained two-channel energy curvature be

`H = [[p,q],[q,s]]`

with

`p > 0`, `Delta := p*s-q^2 > 0`.

For multiplier/state coordinates `u=(x,y)` define

`D_H(u) := p*x^2 + 2*q*x*y + s*y^2`.

Let O2 eventually bind the **final force/residual evaluator error**

`e=(e4,e5)`

to the signed rectangle

`L4 <= e4 <= U4`, `L5 <= e5 <= U5`

on one certified source/state box. The affine error power is

`P_err(u,e) := -(e4*x + e5*y)`.

For the dual quadratic define

`N_H(e4,e5) := s*e4^2 - 2*q*e4*e5 + p*e5^2`.

Because `Delta>0` and `p>0`, `H` and `adj(H)` are positive definite.

## 2. Exact retained-dissipation completion

Fix `theta>0`. Put

`z1 := 2*theta*(p*x+q*y)+e4`,
`z2 := 2*theta*(q*x+s*y)+e5`.

Two exact polynomial identities are

`p * (s*z1^2 - 2*q*z1*z2 + p*z2^2)`
`  = (p*z2-q*z1)^2 + Delta*z1^2`,

and

`s*z1^2 - 2*q*z1*z2 + p*z2^2`
`  = 4*theta*Delta*(theta*D_H(u) + e4*x + e5*y) + N_H(e4,e5)`.

Hence the left side is nonnegative and therefore

`-theta*D_H(u) - (e4*x+e5*y)`
`  <= N_H(e4,e5)/(4*theta*Delta)`.

Equivalently, for `0 < theta <= 1`,

**`-D_H(u) - e·u`
`<= -(1-theta) D_H(u) + N_H(e)/(4 theta Delta)`.**

The charge is sharp for fixed `e` if exactly the fraction `1-theta` of the original curvature is required to remain: equality in the completion is attained at

`u = -(1/(2*theta)) H^{-1} e`.

This is the correct mathematical boundary between O2's additive evaluator uncertainty and a dissipative energy consumer. O2 supplies `e`; the energy theorem decides how much curvature is spent.

## 3. Exact signed-rectangle consumer: four corners suffice

A major practical point is that O2 should not discard signs prematurely.

For fixed `e5`, `N_H(e4,e5)` is a convex quadratic in `e4` with leading coefficient `s>0`; for fixed `e4` it is a convex quadratic in `e5` with leading coefficient `p>0`. The elementary one-dimensional interpolation identity

`(1-t) f(a) + t f(b) - f((1-t)a+t*b)`
`= A*t*(1-t)*(b-a)^2 >= 0`

holds for every quadratic `f(r)=A*r^2+B*r+C` with `A>=0` and `0<=t<=1`.

Applying it successively in `e4` and `e5` proves

**`N_H(e4,e5) <= max N_H(c)` over the four rectangle corners**

`c in {(L4,L5),(L4,U5),(U4,L5),(U4,U5)}`.

Therefore a completely division-free robust gate is:

for each of the four corners `c`, prove

**`N_H(c) <= 4*theta*Delta*kappa`.**

Then for every O2 error point in the whole signed rectangle and every energy state `u`,

**`-D_H(u)-e·u <= -(1-theta)D_H(u)+kappa`.**

This is finite exact-rational arithmetic once O2 has exported rational outward endpoints. There is no square root, eigenvalue, solver status, or sampling step in the consumer.

### Why keeping signed endpoints matters

Take `p=s=1`, `q=1/2`, so `Delta=3/4`, and suppose O2 proves the one-sided box

`0 <= e4 <= 1`, `0 <= e5 <= 1`.

Then

`N_H(e)=e4^2-e4*e5+e5^2`,

and every corner has `N_H<=1`. Thus the exact rectangle charge is

`kappa = 1/(3*theta)`.

If one first forgets signs and uses only `|e4|<=1`, `|e5|<=1`, the standard absolute cross-term estimate gives

`N_H <= 1 + 1 + 1 = 3`,

hence `kappa=1/theta`, a factor-three loss. Signed O2 intervals can therefore preserve real Lyapunov margin.

## 4. Direct first-exit gate

Suppose the already-proved exact-real energy ledger has the form

`Vdot <= -c*V - D_H(u) - e·u + beta`,

with `c>0`, and a first-exit boundary is `V=Vstar`.

If `0<theta<=1`, `c*Vstar > beta`, and every O2 rectangle corner satisfies the strict gate

**`N_H(corner) < 4*theta*Delta*(c*Vstar-beta)`,**

then the four-corner theorem gives some `kappa < c*Vstar-beta`, and therefore on the exit boundary

`Vdot < -(1-theta)D_H(u) <= 0`.

Thus O2 may feed a barrier proof through a finite list of exact corner inequalities. This is only a **consumer** theorem: the O2 source lane must still prove that every deployed evaluator error on every certified box lands in the declared rectangle.

## 5. Sharp obstruction: absolute evaluator bias cannot yield homogeneous decay

A nonzero absolute evaluator enclosure is qualitatively different from a state-relative error.

Fix any nonzero `e0`. From the independent box contract alone the term

`-D_H(u)-e0·u`

cannot be nonpositive for all sufficiently small `u`. Indeed take

`u=-t*e0`, `t>0`.

Then

`-D_H(-t e0)-e0·(-t e0)`
`= -t^2 D_H(e0) + t ||e0||^2`.

Because `D_H(e0)>0`, this is strictly positive whenever

`0 < t < ||e0||^2 / D_H(e0)`.

Consequently:

**an O2 rectangle that permits a nonzero state-independent evaluator bias cannot, by itself, prove a homogeneous strict Lyapunov inequality through the origin.**

One must do at least one of the following:

1. spend an actual additive reserve / first-exit margin, as above;
2. prove a stronger state-relative or vanishing contract `e(u)->0` with a quantitative rate;
3. preserve source correlation showing that the nonzero points of the raw rectangle are impossible near the energy origin.

This is an exact obstruction, not a weakness of Young's inequality.

It also explains the relation to `T-P4-020`: that child gives the sharp joint Schur budget once an additive scalar envelope `B` is already known. The present child is disjoint: it gives a signed two-channel rectangle-to-energy consumer and identifies when O2 can or cannot legitimately create such an additive charge.

## 6. Coordinate/type boundary: solve error is not automatically force error

O2's raw outputs include `M`, central-FD `C/G`, `tau`, and a linear solve. The energy pairing must consume an error in the **same physical residual coordinates** as its multiplier.

In particular, a certified acceleration/solve error enclosure

`e_a = ddq_float - ddq_exact`

cannot be silently used as a force-residual enclosure. A source-side bridge such as

`e_F = M * e_a`

(or the actual deployed residual identity, including all other coefficient errors) must be proved on the same box and with the correct operation/source key.

The obstruction is already visible in one dimension: if `e_a=1` but the mass coefficient is only known to be an arbitrary positive `m`, then `e_F=m` and the sharp additive charge scales like `m^2`. No finite energy charge follows from `|e_a|<=1` alone without a mass/operator enclosure.

Likewise, an interval for each raw primitive `Delta M`, `Delta C`, `Delta G`, `Delta tau`, and solve error is not yet the final residual interval unless the finite-DAG composition into the residual has itself been outwardly enclosed. This is precisely where the O2 source semantics must stop and the energy consumer may begin.

## 7. Orientation boundary inherited from T-P4-030

The global Route-B port/gain convention remains relevant before worst-case completion. If the whole residual error vector is globally negated, `e -> -e`, then `N_H(-e)=N_H(e)`, so the final quadratic additive charge is unchanged. But the unsquared power `e·u` flips sign when the co-state/multiplier is held fixed, exactly as in `T-P4-030`.

Therefore an O2 receipt should identify whether its final error rectangle is expressed in port or gain residual coordinates. A global sign change may be transported by `[L,U] -> [-U,-L]`; it must not be ignored in an unsquared source identity merely because the later worst-case quadratic charge happens to be even.

## 8. Singular boundary

The four-corner theorem above intentionally assumes `Delta>0`. At a rank-one PSD boundary `Delta=0`, a finite affine charge exists only if **every allowed error lies in `Range(H)`**, equivalently has no component along `ker(H)`; this is the singular compatibility condition proved in the earlier affine-energy classification.

A genuine two-dimensional O2 rectangle cannot be contained in a one-dimensional range. Thus if the retained energy curvature becomes singular while O2 still exports an area-positive error box, no finite global affine completion exists. The checker must fail closed or use a stronger correlated error set; it must not obtain a singular result by substituting `Delta=0` into the positive-definite corner gate.

## 9. Candidate theorem statements

Suggested exact-real children, all source-independent:

1. `o2_error_power_retained_dissipation_completion_2x2`
   - hypotheses `0<p`, `0<Delta`, `0<theta`;
   - conclusion `-theta*D_H(u)-e·u <= N_H(e)/(4*theta*Delta)`;
   - proof from the two square identities above.

2. `dual_quadratic_rectangle_le_corners`
   - hypotheses `L4<=e4<=U4`, `L5<=e5<=U5`, `0<p`, `0<s`;
   - four corner upper bounds imply `N_H(e)<=K`.

3. `o2_signed_rectangle_energy_consumer`
   - combines (1) and (2), preferably in division-free form
     `N_H(corner) <= 4*theta*Delta*kappa`.

4. `o2_signed_rectangle_first_exit_gate`
   - consumes `c*Vstar>beta` and the strict four-corner inequalities.

5. `absolute_evaluator_bias_blocks_homogeneous_decay`
   - explicit witness `u=-t e0` for nonzero `e0`.

6. `solve_error_requires_force_metric_bridge`
   - a typed/documentation-level theorem/interface, not a numerical source claim: acceleration and force errors remain distinct until a same-box mass/residual map is supplied.

The algebraic core should be amenable to `ring`, square nonnegativity, and `nlinarith`; no matrix inverse is required if the adjugate/SOS form is used.

## 10. What remains open

This review does not establish any actual numerical `L4,U4,L5,U5` for deployed `dhport_lib.jl`, does not prove raw Float64 operations are outwardly enclosed, does not bind the central-FD shift or `1e-5` rounding semantics, does not prove the solve-conditioning leaf, and does not prove box coverage. It also does not identify acceleration error with force residual error.

The next source-side handoff needed from O2 is therefore small and explicit: for each certified box and a fixed source/hash/orientation key, export an outward **final residual-error rectangle in the energy consumer's force coordinates** (or a stronger correlated set). Once that object exists, the four exact corner gates above are sufficient to turn it into a rigorous Lyapunov additive charge without further Float64 reasoning.

Admission remains `pending`; no registry or parent closure is claimed.
