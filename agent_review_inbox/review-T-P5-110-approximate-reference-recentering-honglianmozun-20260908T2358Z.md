---
kind: review_result
review_id: review-T-P5-110-approximate-reference-recentering-honglianmozun-20260908T2358Z
task_id: T-P5-110-APPROXIMATE-REFERENCE-RECENTERING
source_agent: 红莲魔尊
created_at: 2026-09-08T23:58:00Z
claim_commit: b2ffb3eaeceaeab6817788c9f08a346015f55de9
inspected_commit: b2ffb3eaeceaeab6817788c9f08a346015f55de9
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-106-reference-ramp-recentered-energy-honglianmozun-20260908T2256Z.md
    blob_sha: 7a8fe4d1f404a86e3695cd602f9691399fdefa52
  - task_id: T-P5-107-REFERENCE-RAMP-CORNER-GLUING
  - task_id: T-P5-108-HYBRID-JUMP-DWELL-RECOVERY
  - task_id: T-P5-109-SHARP-REFERENCE-JUMP-RESET
status: CONDITIONAL_PASS_EXACT_RATIONAL_RECENTER_FAMILY
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: expose the recenter vector a as a typed rational design parameter; bind actual B,g and input amplitude/slope caps, certify the residual delta=g-Ba and one dual-power packet, then reinstantiate the existing jump/domain bridges before any hybrid use
commands: none_math_derivation_only_exact_rational_replay
lean_compile_status: not_run
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-110 — approximate reference recentering: amplitude mismatch versus slew cost

## 0. New result

T-P5-106 used an exact static center `a` satisfying `B a=g` and therefore removed the input amplitude `w` from the energy derivative. That is an excellent special case, but it is stronger than what is mathematically required for a valid collar.

For an **arbitrary constant recenter vector** `a`, define

`z=q-a w`, `s=v`, `delta(a):=g-Ba`.

Then the exact recentered dynamics are

`z' = s-a w'`,

`M s' + D s + B z = delta(a) w`.

For the same cross-energy as T-P5-106, the derivative is exactly

**(0.1)**

`Vc' = -Qd`
`      + w (z+s)^T delta(a)`
`      - w' a^T[(K+D)z+Ms]`.

Thus failure of exact `Ba=g` does **not** invalidate recentering. It creates one explicit signed amplitude-mismatch channel. The recenter vector becomes a genuine Lyapunov-design parameter trading:

- amplitude mismatch `delta(a)=g-Ba`,
- slew sensitivity proportional to `a`,
- and, downstream, the already-known jump/domain displacement costs proportional to `a`.

This child derives a square-only forcing/collar contract, a convex quadratic normal equation for choosing `a` at fixed Young split, and a sharper four-corner robust packet when rational magnitude caps for `w,w'` are available. It also gives an exact Route-B dual-metric diagnostic showing when the exact static center is cheaper than no recentering and when it is not.

No actual `referenceKey`, ramp schedule, source equality, Float64/controller semantics, path coverage, Lean receipt, admission, or registry mutation is claimed.

---

## 1. Exact arbitrary-`a` energy identity

Assume the same structural packet as T-P5-106:

`q'=v`,

`M v' + D v + B q = g w`,

`B=K-A`,

with `M,D,K` symmetric and `A^T=-A`.

For any constant vector `a`, set

`z=q-a w`, `s=v`, `delta=g-Ba`.

Then

`z'=s-a w'`

and

`M s' + D s + Bz = delta w`.

Use

`Vc(z,s)`
` = 1/2 s^TMs + 1/2 z^TKz + z^TMs + 1/2 z^TDz`,

and

`Qd(z,s)=z^TKz+s^T(D-M)s-s^TAz`.

Differentiating and using `z^TAz=0` gives exactly

**(1.1)**

`Vc' = -Qd + w(z+s)^T delta - w' a^T[(K+D)z+Ms]`.

Define `x=(z,s)` and the two stacked observable maps

`E := [I; I]`,

`C := [K+D; M]`.

Then

`c_delta(a)=E(g-Ba)`,

`c_s(a)=Ca`,

and the external power is

**(1.2)** `p_a = w c_delta(a)^T x - w' c_s(a)^T x`.

For `Ba=g`, `c_delta=0` and (1.1) reduces exactly to T-P5-106. For `a=0`, the slew channel vanishes and only the original amplitude forcing remains.

### Candidate theorem

`reference_arbitrary_position_recenter_energy_identity`

Inputs: the structural equations above and an arbitrary constant `a`.

Output: (1.1) exactly.

This theorem does not require `B` invertible and does not require an equilibrium center to exist.

---

## 2. Generic dual-metric forcing packet

Write

`Qd=x^TQx`, with `Q>=0` on the source domain.

Let `H_delta,H_s` be positive-semidefinite 2x2 matrices for which the following two quadratic dual inequalities are certified:

**(2.1)**

`((E y)^T x)^2 <= (y^T H_delta y) Qd(x)` for all `x,y`,

**(2.2)**

`((C y)^T x)^2 <= (y^T H_s y) Qd(x)` for all `x,y`.

Suppose source-facing input caps give

`w^2 <= W`, `(w')^2 <= S`, with `W,S>=0`.

Define

`A_a := W delta(a)^T H_delta delta(a)`,

`S_a := S a^T H_s a`.

Then the two signed channels satisfy

`u^2 <= A_a Qd`, where `u=w c_delta^T x`,

`v^2 <= S_a Qd`, where `v=w' c_s^T x`.

For any rational/real `eta>0`, the exact square identity

**(2.3)**

`eta * ((1+eta)u^2 + (1+1/eta)v^2 - (u-v)^2)`
` = (eta*u+v)^2 >= 0`

can be denominator-cleared as

**(2.4)**

`eta * (u-v)^2 <= (1+eta)(eta*u^2+v^2)`.

Therefore

**(2.5) JOINT POWER SQUARE**

`eta * p_a^2`
` <= (1+eta) L_eta(a) Qd`,

where

**(2.6)**

`L_eta(a)`
` := eta W (g-Ba)^T H_delta (g-Ba)`
`  + S a^T H_s a`.

This is the first reusable consumer. It keeps amplitude and slew in the same signed-power channel without requiring a square root.

---

## 3. From the joint square to an invariant collar

Assume additionally

`Qd >= lambda Vc`, `lambda>0`.

Choose `0<theta<1`, `beta>=0`. If

**(3.1)**

`(1+eta) L_eta(a) <= 4 eta theta beta`,

then (2.5) implies

`p_a^2 <= 4 theta beta Qd`.

Using

`(theta Qd+beta)^2 - 4 theta beta Qd`
` = (theta Qd-beta)^2 >= 0`,

we obtain

`p_a <= theta Qd+beta`,

hence

**(3.2)**

`Vc' <= -(1-theta)Qd+beta`
`    <= -(1-theta)lambda Vc+beta`.

For a desired invariant level `R`, the gate `beta <= (1-theta)lambda R` combines with (3.1) to give

`(1+eta)L_eta(a)`
` <= 4 eta theta(1-theta) lambda R`.

Because

`4theta(1-theta)<=1`

by `(2theta-1)^2>=0`, the best `theta` inside this square-only absorption family is again `theta=1/2`. The entire continuous-flow collar therefore reduces to

**(3.3) OPTIMAL-THETA COLLAR GATE**

`(1+eta) L_eta(a) <= eta lambda R`.

This is fully division-free after `eta,lambda,R` are instantiated as positive rationals.

---

## 4. Choosing `a`: exact convex quadratic normal equation

For fixed positive `eta` and fixed input caps `W,S`, minimizing the collar cost in (3.3) is equivalent to minimizing `L_eta(a)`.

Set

`R_eta := eta W B^T H_delta B + S H_s`,

`h_eta := eta W B^T H_delta g`.

Then

`L_eta(a)`
` = eta W g^T H_delta g - 2 a^T h_eta + a^T R_eta a`.

Suppose a rational/exact witness `a_*` satisfies

**(4.1)** `R_eta a_* = h_eta`.

A ring expansion gives the exact completion

**(4.2)**

`L_eta(a)-L_eta(a_*)`
` = (a-a_*)^T R_eta (a-a_*)`.

Hence, if `R_eta>=0`, `a_*` is a global minimizer. If `R_eta>0`, it is the unique minimizer. No matrix inverse is needed by the checker: `a_*` is supplied as a witness and (4.1) plus PSD of `R_eta` are verified directly.

### Exact-center consequence

Assume an exact static center `a_eq` exists with `B a_eq=g`. At that point the amplitude part has zero gradient, so

`grad L_eta(a_eq)=2 S H_s a_eq`.

Therefore, for a fixed finite `eta`, if

`S>0` and `H_s a_eq != 0`,

then **the exact static center is not the minimizer of this fixed-split continuous-flow budget**. The optimizer deliberately accepts a nonzero amplitude mismatch to reduce slew sensitivity.

This does not say the exact center is globally inferior after reoptimizing `eta`, jump cost, or domain placement. It says only that `Ba=g` is a structural cancellation choice, not an automatic optimum of every Lyapunov budget.

---

## 5. Sharp source-facing alternative: four corner power gates

If the source gives rational magnitude caps directly,

`|w|<=w_max`, `|w'|<=s_max`,

one can avoid the auxiliary Young parameter `eta` completely.

For signs `sigma,tau in {+1,-1}`, define the four corner covectors

**(5.1)**

`f_(sigma,tau)(a)`
` := sigma*w_max*E(g-Ba) - tau*s_max*C a`.

If one rational `chi>=0` satisfies all four quadratic gates

**(5.2)**

`(f_(sigma,tau)(a)^T x)^2 <= chi Qd(x)`

for every `x`, then

**(5.3)** `p_a^2 <= chi Qd`

for every `(w,w')` in the full rectangle.

Reason: for fixed `x`, `(w,w') -> (f(w,w')^T x)^2` is a convex quadratic function on a rectangle, so its maximum is attained at a vertex. Equivalently, express the interior point as a convex combination of the four vertices and use the elementary Jensen square identity.

A matrix checker may verify each (5.2) by a PSD certificate such as

`chi Q - f f^T >= 0`.

Then `theta=1/2` gives the especially small invariant-level consumer

**(5.4)** `chi <= lambda R`.

This four-corner route is preferred when exact rational magnitude intervals for `w,w'` are already available, because it preserves cross-channel cancellation and removes an arbitrary split parameter.

---

## 6. Current Route-B packet: small rational fallback dual bounds

For the exact rational T-P5-106 matrices,

`M=diag(350003/3000000,200739/4000000)`,

`D=diag(4/5,13/20)`,

`K=[[3/4,-3/400],[-3/400,29/50]]`,

`A=[[0,1/400],[-1/400,0]]`,

`B=K-A`,

and

`Q=[[K,A/2],[A^T/2,D-M]]`.

There is a very small all-rational fallback proof that does not need a 4x4 inverse.

First,

**(6.1)** `Q >= (1/2) I_4`.

Indeed the leading principal minors of `Q-(1/2)I` are exactly

`1/4`,

`3191/160000`,

`1754852927/480000000000`,

`700600339414447/1920000000000000000`,

all strictly positive.

Hence `||x||^2 <= 2Qd`.

For the amplitude observable,

`||E delta||^2 = 2||delta||^2`,

so Euclidean Cauchy gives

**(6.2)** `((E delta)^T x)^2 <= 4 ||delta||^2 Qd`.

For the slope observable `C=[K+D;M]`,

`||C||_F^2`
` = 566156498915233/144000000000000`
` < 4`,

with exact positive gap

`9843501084767/144000000000000`.

Thus

**(6.3)** `((Ca)^T x)^2 <= 8 ||a||^2 Qd`.

Therefore a tiny checker-ready dual packet is simply

`H_delta=4 I_2`, `H_s=8 I_2`.

The fixed-`eta` optimizer becomes

**(6.4)**

`(eta W B^T B + 2 S I) a_*`
` = eta W B^T g`.

This is likely the easiest first Lean theorem because every coefficient can remain rational and all positivity is low-dimensional.

---

## 7. Sharper exact dual metric for the same rational packet

The fallback constants above are intentionally simple, not sharp. Because `Q` is rational positive definite, one can produce exact rational dual witnesses without trusting an inverse primitive.

Let `E=[I;I]` and `C=[K+D;M]`. The following rational matrices satisfy direct ring-checkable identities

`Q Y_delta = E`,

`Q Y_s = C`:

`Y_delta =`

`[[5015865295763600/3761310479513717, 4950978564660400/342279253635748247],`
` [76723484864400/3761310479513717, 590202992287040000/342279253635748247],`
` [5504505202500000/3761310479513717, 1079641200000000/342279253635748247],`
` [-10452938000000/3761310479513717, 570630814926000000/342279253635748247]]`.

`Y_s =`

`[[1414856116888265003/684558507271496494, 582875499141903/52658346713192038],`
` [4847715957769520/342279253635748247, 111679988602881165/52658346713192038],`
` [58447375554751753/342279253635748247, 102146480521875/26329173356596019],`
` [-1474262405057500/342279253635748247, 2202275926496481/26329173356596019]]`.

Define

`H_delta=E^T Y_delta`,

`H_s=C^T Y_s`.

Explicitly,

**(7.1)**

`H_delta =`

`[[809259269097200/289331575347209, 66270546864400/3761310479513717],`
` [66270546864400/3761310479513717, 1160833807213040000/342279253635748247]]`.

**(7.2)**

`H_s =`

`[[3309888154942456095580259/1026837760907244741000000, 14350638756758313/8425335474110726080],`
` [14350638756758313/8425335474110726080, 21166623961369962650343/8101284109721852000000]]`.

Both are positive definite. For `H_delta`, the first pivot is positive and

`det(H_delta)=3246741302754720000/342279253635748247 > 0`.

For `H_s`, the first pivot is positive and

`det(H_s)=11530539742803591828289759429533/1369117014542992988000000000000 > 0`.

Because `QY_delta=E` and `QY_s=C`, the `Q`-inner-product Cauchy inequality gives (2.1)-(2.2) exactly. A formal sidecar need not mention `Q^{-1}` at all: it can consume the two explicit linear identities and positive definiteness of `Q`.

---

## 8. Exact endpoint decision: when does static recentering help the derivative collar?

Use the actual T-P5-106 exact center

`a_eq=(2340/8699,1520/8699)`, `B a_eq=g`.

For **no recentering** `a=0`, the exact amplitude dual cost is

**(8.1)**

`chi_amp := g^T H_delta g`
` = 50143711476396320/342279253635748247`
` ~= 0.1464994180738719`.

For **exact static recentering** `a=a_eq`, the exact slope dual cost is

**(8.2)**

`chi_slope := a_eq^T H_s a_eq`
` = 3428369547552848069595351/10947236428975391560304500`
` ~= 0.3131721480389847`.

This slightly sharpens the old T-P5-106 slope coefficient `63/200=0.315`.

With `Qd >= (9/10)Vc`, the best single-channel invariant collar coefficients are

**(8.3)**

`R_no_shift >=`
` (501437114763963200/3080513282721734223) W`
` ~= 0.162777131193191 W`,

and

**(8.4)**

`R_exact_center >=`
` (380929949728094229955039/1094723642897539156030450) S`
` ~= 0.347969053376650 S`.

Therefore the exact static center beats the no-shift endpoint on **continuous-flow derivative cost alone** precisely when

**(8.5)**

`W/S > chi_slope/chi_amp`

with exact threshold

`chi_slope/chi_amp`
` = 4055761174755019266331300233/1897252535606229820614160000`
` ~= 2.137702334633634`.

If the amplitude-to-slope squared-cap ratio is below this threshold, no recentering has the smaller endpoint derivative collar; above it, exact static recentering has the smaller endpoint derivative collar.

This is a genuine design boundary. It shows that “remove amplitude at all costs” is not a universal Lyapunov optimum: a fast-varying but small-amplitude reference can make the shift-induced slew channel more expensive than simply paying the amplitude channel.

The statement is deliberately limited to the derivative collar. The absolute-value/domain bridge and T-P5-109 jump reset depend on `a` too and must be included before choosing the globally deployed recenter vector.

---

## 9. A rational partial-center witness, only as a conditional diagnostic

To demonstrate that the arbitrary-`a` family is not merely formal, take the normalized diagnostic caps

`W=S=1`, `eta=1`

and the sharper exact dual matrices (7.1)-(7.2). A small rational near-stationary choice is

**(9.1)** `a_hat=(7/80,13/250)`.

It leaves the exact amplitude residual

**(9.2)**

`delta_hat=g-B a_hat`
` =(26979/200000,28111/400000)`.

The exact fixed-split quadratic is

**(9.3)**

`L_1(a_hat)`
` = 409665977646506639834940870179`
`   / 4107351043628978964000000000000`
` ~= 0.0997397040805534`.

With `theta=1/2` and `lambda=9/10`, (3.3) gives the exact conditional level

**(9.4)**

`R >= 409665977646506639834940870179`
`     / 1848307969633040533800000000000`
` ~= 0.221643786845674`.

This diagnostic is **not** an actual referenceKey recommendation: for `W=S=1`, the direct no-shift endpoint (8.3) is smaller still. Its purpose is to show that a non-equilibrium rational center can be certified exactly and can interpolate the two channels. The actual choice must use the real amplitude/slope/jump/domain packet.

---

## 10. Exact obstructions and fail-closed boundaries

### 10.1 No finite amplitude cap

If no finite `W` is available, any `delta(a)!=0` leaves an unbounded amplitude power channel. In that case a finite collar from this route requires exact cancellation `Ba=g` (or some different signed/source structure). Approximate recentering cannot manufacture a finite bound from no amplitude information.

### 10.2 No finite slew cap

If no finite `S` is available, any `a!=0` leaves an uncontrolled slope channel. Then `a=0`, a constant-input segment, or a different regularity argument is required. Exact `Ba=g` alone does not control `w'`.

### 10.3 Exact center may not exist

If `g` is not in `range(B)`, no exact `Ba=g` exists. The arbitrary-`a` theorem remains valid; it reduces the problem to a certified residual `delta(a)` rather than falsely assuming an inverse.

### 10.4 Do not optimize only the flow derivative and forget jumps/domain

Changing `a` changes all of the following:

- `delta(a)=g-Ba` in the amplitude channel;
- `c_s(a)=Ca` in the slope channel;
- the T-P5-109 jump translation direction `e=(a,0)` and its exact storage cost;
- the absolute-coordinate bridge `q=z+a w` and therefore the reference-domain placement budget.

So a continuous-flow minimizer of `L_eta(a)` is not automatically the hybrid/global optimum. T-P5-109 must be re-instantiated with the selected `a`; this child does not redo or preempt that theorem.

### 10.5 Source identity remains separate

The exact rational matrices above belong to the already-used T-P5-105/T-P5-106 coefficient packet. They do not prove that a deployed Float64/runtime `referenceKey` uses those exact coefficients. A source adapter must bind the actual `B,M,D,K,A,g`, input law, and caps before any numerical threshold is consumed.

---

## 11. Minimal theorem surfaces for formalization

Suggested source-independent leaves:

1. `reference_arbitrary_position_recenter_energy_identity` — exact identity (1.1).
2. `two_channel_power_weighted_square` — denominator-cleared identity (2.4).
3. `approx_recenter_joint_power_budget` — (2.5) from the two dual quadratic packets.
4. `approx_recenter_normal_equation_minimizer` — completion (4.2).
5. `rectangle_four_corner_quadratic_power` — four-corner implication (5.2) => (5.3).
6. `routeb_reference_Q_half_coercive` — exact principal-minor proof of (6.1).
7. `routeb_reference_simple_recenter_dual` — small `H_delta=4I`, `H_s=8I` fallback.
8. Optional sharper sidecar: verify `QY_delta=E`, `QY_s=C` and consume the exact dual matrices (7.1)-(7.2).

The final source-facing design packet should carry one selected rational `a`, the exact residual `delta=g-Ba`, actual amplitude/slope caps, and either the weighted-square or four-corner power certificate. Only after that should the existing T-P5-106 value bridge and T-P5-109 jump theorem be re-instantiated.

## 12. Status

`CONDITIONAL_PASS_EXACT_RATIONAL_RECENTER_FAMILY / pending`.

The mathematical obstruction from T-P5-106 is weakened substantially: lack of exact `Ba=g` is no longer a blocker to forming a valid energy collar; it only prevents complete amplitude cancellation. What remains open is the actual reference/source packet and the global choice of `a` after derivative, jump, and domain costs are combined.
