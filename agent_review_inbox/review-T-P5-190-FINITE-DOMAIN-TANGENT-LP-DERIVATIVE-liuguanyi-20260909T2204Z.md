---
kind: review_result
review_id: review-T-P5-190-finite-domain-tangent-lp-derivative-liuguanyi-20260909T2204Z
task_id: T-P5-190-FINITE-DOMAIN-TANGENT-LP-DERIVATIVE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T22:04:00Z
claim_commit: 9e3b8b78e3f57d3d11d80c228bc0a1191a1de332
inspected_commit: f4307738830e6055e6cb39212d73edc6a7362bf6
upstream_commits:
  - 4c6c4ab0ae84f7e397975e6de14e8167efcd6bfa  # T-P5-186 singular PSD recession active fan
  - e5d824609fe5e899225e17adb672eac18da6883c  # T-P5-188 residual-stratum canonical compression
  - a62b347c8fd585bb8e5e77493a1b2506861d86b4  # T-P5-189 kernel-gauge Dini Lyapunov envelope
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_finite_value_parameter_cone; add_boundary_tangent_recession_gate; add_exact_right_directional_derivative; add_zero_residual_lp_derivative_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional convex quadratic, polyhedral-cone, KKT, and LP duality algebra; no Lean/kernel run
exit_code: not_applicable
---

# T-P5-190 — finite-value parameter tangent cone and exact LP directional derivative

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-189 gives a sound selection-free upper-Dini Lyapunov inequality at an active-face switch, but deliberately leaves external boundary states fail-closed. The missing issue is sharper than ordinary orthant tangency: for singular `P`, an external direction can remain inside `e>=0` while immediately turning a previously zero recession direction into a negative one, making the reduced energy `-infinity` for every positive step.

This review closes that interface mathematically.

For

`q_H(u,e)=u^T P u+2 e^T B u+e^T C e`, `u>=0`,

with `P=P^T>=0`, define the nonnegative kernel cone

`K := { d>=0 : P d=0 }`.

Using the T-P5-186 boundedness/attainment gate, the finite-value external parameter set is the polyhedral cone

**`D_fin = { e : e^T B d >=0 for every d in K }`.**

If the physical external state also satisfies `e>=0`, the actual finite domain is

**`E = R_+^p intersect D_fin`.**

At `e0 in E`, define the critical recession cone

`K_0(e0) := { d in K : e0^T B d=0 }`.

Then an external direction `v` is a genuine locally finite ray direction iff

- `v_j>=0` for every external coordinate with `(e0)_j=0`, and
- **`v^T B d>=0` for every `d in K_0(e0)`.**

Equivalently, this is exactly the polyhedral tangent cone `T_E(e0)`.

If the second condition fails, the obstruction is immediate and exact: for the violating `d`, every `t>0` has

`(e0+t v)^T B d = t v^T B d <0`,

so the inherited quadratic is unbounded below along `u+s d`. This can happen even though `e0+t v` remains in the nonnegative external orthant.

On every feasible tangent ray, the T-P5-189 upper-Dini inequality sharpens to an **exact right directional derivative**:

**`Phi'_+(e0;v) = 2 v^T C e0 + 2 min_{u in M(e0)} v^T B u`,**

where `M(e0)` is the complete orthant minimizer set of the inherited quadratic at `e0`.

Finally, T-P5-188 turns the minimization of the frozen slope into one exact LP on the zero-residual coordinates. Thus the boundary derivative can be certified by rational primal/dual equalities and inequalities; no optimizer differentiation, pseudoinverse, eigenvector, square root, or arbitrary kernel gauge is needed.

No actual Route-B/PDE source binding, physical cell/trajectory coverage, Float64 semantics, Lean/kernel verification, independent validation, admission, or registry mutation is claimed.

---

## 1. Setup and dependency boundary

Let

`P=P^T>=0`,

`B in R^(p x m)`,

`C=C^T in R^(p x p)`.

For inherited coordinates `u>=0` and external coordinates `e`, define

`F_e(u) := u^T P u + 2 e^T B u`,

`Phi(e) := inf_{u>=0} F_e(u) + e^T C e`.

Write

`b(e):=B^T e`.

This review uses, rather than re-proves, the T-P5-186 singular-PSD recession result: for a fixed `e`, `F_e` is bounded below and attains its minimum on the orthant exactly when

`b(e)^T d = e^T B d >=0`

for every

`d>=0`, `P d=0`.

All subsequent statements are finite-dimensional consequences of that gate plus T-P5-188's exact minimizer-slice theorem.

---

## 2. T190-A — finite-value parameter cone is polyhedral

Define

`K := {d in R^m : d>=0, P d=0}`.

This is a polyhedral cone because it is given by finitely many linear equalities and inequalities.

Define

`D_fin := {e in R^p : e^T B d>=0 for all d in K}`.

By T-P5-186,

**`e in D_fin` iff the inherited minimum is finite and attained.**

Since `K` is polyhedral, it is finitely generated: choose rays `d^1,...,d^N` with

`K = cone{d^1,...,d^N}`.

Then

`D_fin = intersection_r {e : e^T B d^r>=0}`.

Therefore `D_fin` is a closed polyhedral cone.

If the physical external contract also requires `e>=0`, define

`E := R_+^p intersect D_fin`.

Then `E` is again a closed polyhedral cone. This is the correct domain on which the reduced energy is a finite real-valued object.

### Interface consequence

The deployed/type-level contract should distinguish

- `external_state_nonnegative`, from
- `reduced_energy_finite`.

The first does not imply the second when `P` is singular.

---

## 3. T190-B — exact boundary tangent-cone theorem

Fix `e0 in E` and define

`K_0 := {d in K : e0^T B d=0}`.

Call these the **critical recession directions** at `e0`.

### Theorem T190-B

For a direction `v in R^p`, the following are equivalent:

1. `v in T_E(e0)`, the tangent cone of the finite physical parameter domain;
2. both conditions hold:

   **(external active coordinates)**

   `v_j>=0` whenever `(e0)_j=0`;

   **(critical recession inequalities)**

   `v^T B d>=0` for every `d in K_0`;

3. there exists `epsilon>0` such that

   `e0+t v in E`

   for every `0<=t<=epsilon`.

### Proof

Use a finite ray representation of `K`.

For every generator `d^r`, the finite-domain inequality is

`a_r(e):=e^T B d^r>=0`.

At `e0`, a generator is active exactly when `a_r(e0)=0`. A polyhedral tangent direction must satisfy

`a_r(v)=v^T B d^r>=0`

for every active generator. Inactive generators have strictly positive margin at `e0`, so their inequalities remain positive for all sufficiently small positive `t`.

The same argument applies to the external inequalities `e_j>=0`: only coordinates with `(e0)_j=0` constrain the tangent direction.

It remains to replace active generators by all of `K_0`. Since every `d in K` is a nonnegative combination of the generators and every `a_r(e0)>=0`, a combination has `e0^T B d=0` only if every generator carrying positive coefficient is itself active. Therefore nonnegativity on active generators is equivalent to

`v^T B d>=0` for every `d in K_0`.

For a polyhedron, satisfaction of all active linearized inequalities is also sufficient for the literal ray `e0+t v` to remain feasible for sufficiently small `t`. Hence (1)-(3) are equivalent. QED.

---

## 4. T190-C — sharp immediate-loss obstruction

Suppose `v` satisfies the ordinary external-orthant tangent conditions but there exists

`d in K_0`

with

`v^T B d<0`.

Then for every `t>0`,

`(e0+t v)^T B d`

`= e0^T B d + t v^T B d`

`= t v^T B d <0`.

Because `Pd=0` and `d>=0`, along any inherited state `u>=0`,

`F_{e0+t v}(u+s d)`

has asymptotic slope

`2 (e0+t v)^T B d<0`

in `s`. Hence

**`Phi(e0+t v)=-infinity` for every `t>0`.**

This is not a numerical conditioning failure and not an active-set bookkeeping failure. It is the exact boundary obstruction for the reduced-energy construction.

It also shows why T-P5-189's finite-valued Dini consumer should not be applied before this tangent-domain gate has been checked at singular boundary states.

---

## 5. T190-D — critical recession localizes to the T-P5-188 zero-residual stratum

Let `y` be any exact minimizer at `e0` and let

`r := P y + B^T e0 >=0`,

`y^T r=0`.

Use the canonical T-P5-188 partition

`I := {i : r_i=0}`,

`J := {j : r_j>0}`.

T-P5-188 gives

`M(e0) = {u : u_J=0, u_I>=0, P_II u_I=-(B^T e0)_I}`.

### Theorem T190-D

The recession cone of the complete minimizer set is exactly the critical recession cone:

**`rec M(e0) = K_0`.**

In zero-residual coordinates this is

**`K_0 = { d : d_J=0, d_I>=0, P_II d_I=0 }`.**

### Proof

First take `d in K_0`. Since `Pd=0`,

`r^T d`

`= (Py+B^T e0)^T d`

`= y^T P d + e0^T B d`

`=0`.

But `r>=0` and `d>=0`. Hence `d_j=0` on every coordinate where `r_j>0`, so `d_J=0`. Also `Pd=0` implies `P_II d_I=0`.

Conversely suppose `d_J=0`, `d_I>=0`, and `P_II d_I=0`. Extend by zero on `J`. By the T-P5-188 PSD principal-kernel lifting lemma,

`Pd=0`.

Because `r_I=0` and `d_J=0`, `r^T d=0`; therefore

`e0^T B d = r^T d-y^T P d=0`.

Thus `d in K_0`. Such a `d` preserves the affine equations and nonnegativity under `u -> u+s d`, so it is exactly a recession direction of `M(e0)`. QED.

### Consequence

The boundary tangent check can be performed after T-P5-188 entirely on the canonical zero-residual block. There is no need to enumerate a second, unrelated kernel cone.

---

## 6. T190-E — Farkas form of the boundary tangent gate

Let

`A := P_II`,

`c := (B^T v)_I`.

By T190-D, the critical-recession tangent condition is

`c^T d>=0`

for every

`d>=0`, `A d=0`.

By finite-dimensional Farkas duality, this is equivalent to existence of a free vector `lambda` such that

**`A^T lambda <= c`.**

Since `A` is symmetric,

**`A lambda <= c`.**

Equivalently, there is a nonnegative slack `s>=0` with

**`c = A lambda+s`.**

This is a very small checker packet:

- exact matrix-vector product `A lambda`;
- exact equality `c=A lambda+s`;
- entrywise `s>=0`.

No kernel basis is required.

For rational `A,c`, whenever the condition is true there is a rational Farkas witness `(lambda,s)`.

---

## 7. T190-F — exact right directional derivative on every feasible tangent ray

Assume now `v in T_E(e0)`. By T190-B, there is `epsilon>0` such that `e_t:=e0+t v` remains in `E` for `0<=t<=epsilon`, so the reduced minimum is finite and attained along the whole short ray.

Let

`M0 := M(e0)`.

Define the frozen-slope optimum

`mu(v) := min_{u in M0} v^T B u`.

This minimum is finite and attained. Indeed `M0` is a nonempty polyhedron and its recession cone is `K_0`; T190-B gives `v^T B d>=0` on every `d in K_0`, exactly the LP boundedness condition.

### Theorem T190-F

The right directional derivative exists and is

**`Phi'_+(e0;v)`**

**`= 2 v^T C e0 + 2 mu(v)`**

**`= 2 v^T C e0 + 2 min_{u in M0} v^T B u`.**

### Upper bound

Choose `u_* in M0` attaining `mu(v)`. Since `u_*` is a legal frozen inherited state for every external parameter,

`Phi(e_t)`

`<= F_{e_t}(u_*) + e_t^T C e_t`.

At `t=0`, equality holds. Therefore

`limsup_{t downarrow 0} [Phi(e_t)-Phi(e0)]/t`

`<= 2 v^T B u_* + 2 v^T C e0`

`= 2 mu(v)+2 v^T C e0`.

This is the T-P5-189 frozen-branch inequality sharpened by choosing the minimum frozen slope.

### Lower bound

For each `t>0`, choose a minimizer `u_t` of the inherited problem with **minimal support**. T-P5-186 proves that the principal block on such a minimal support `S_t` is positive definite.

There are finitely many coordinate supports. Take any sequence `t_n downarrow 0`; after passing to a subsequence, either the support is empty throughout or one fixed support `S` occurs throughout.

On a fixed nonempty support, KKT stationarity is the exact linear system

`P_SS (u_t)_S = -(B^T e_t)_S`.

Because `P_SS>0`, this solution is unique and depends continuously (indeed affinely) on `t`. Hence `u_t` stays bounded and converges to some `u_0>=0`. The KKT residual inequalities and complementarity are closed under this limit, so `u_0` is a minimizer at `e0`:

`u_0 in M0`.

Now write the inherited value `psi(e):=Phi(e)-e^T C e`. Since `u_t` minimizes at `e_t`,

`psi(e_t)`

`= F_{e0}(u_t)+2 t v^T B u_t`

`>= psi(e0)+2 t v^T B u_t`.

Therefore along the subsequence,

`liminf [psi(e_t)-psi(e0)]/t`

`>= 2 v^T B u_0`

`>= 2 mu(v)`.

Because every sequence approaching zero has such a support-stable subsequence, the global lower limit obeys the same bound. Adding the smooth derivative of `e^T C e` gives

`liminf [Phi(e_t)-Phi(e0)]/t`

`>= 2 mu(v)+2 v^T C e0`.

The upper and lower bounds agree, proving the formula. QED.

### Important interpretation

T-P5-189 says every active minimizer gives a sound upper-Dini slope. T190-F identifies the exact derivative as the **best** of those frozen slopes:

`exact one-sided slope = minimum active frozen slope`.

This remains true at a finite-domain boundary, provided the direction first passes the critical-recession tangent gate.

---

## 8. T190-G — zero-residual LP and exact rational primal/dual certificate

Use T-P5-188's representation

`M0 = {u : u_J=0, u_I>=0, A u_I=d0}`,

where

`A:=P_II`,

`d0:=-(B^T e0)_I`.

Let

`c:=(B^T v)_I`.

Then

`mu(v)` is exactly the LP

**Primal**

`min c^T x`

subject to

`A x=d0`,

`x>=0`.

Its dual is

**Dual**

`max d0^T lambda`

subject to

`A^T lambda<=c`.

The same dual-feasibility inequality appeared in T190-E as the critical-recession tangent certificate. Therefore one object serves two mathematical roles:

1. it proves the direction cannot escape to `-infinity` through a zero-cost kernel ray;
2. it gives a certified lower bound on every frozen active slope.

If producer supplies `x_*`, `lambda_*`, and slack `s_*`, checker verifies

`x_*>=0`,

`A x_*=d0`,

`s_*:=c-A^T lambda_*>=0`,

and

**`c^T x_* = d0^T lambda_*`.**

Then primal/dual weak duality plus equality proves both are optimal and

`mu(v)=c^T x_*=d0^T lambda_*`.

Hence the exact derivative is certified by

**`Phi'_+(e0;v)=2 v^T C e0+2 c^T x_*`.**

For rational `P,B,e0,v`, every finite LP above has rational primal/dual optimal witnesses. Thus exact-rational proof packets remain available even when `P_II` is singular and the minimizer set is unbounded.

No inverse, pseudoinverse, eigenvector, square root, active-selector derivative, or canonical kernel basis is needed on the trusted side.

---

## 9. Exact regressions

### 9.1 External orthant tangent is not enough

Take one inherited coordinate and two external coordinates:

`P=[0]`,

`B=[[0],[-1]]`,

`C=0`.

Let

`e0=(1,0)`,

`v=(0,1)`.

The external ray is perfectly feasible:

`e0+t v=(1,t)>=0` for every `t>=0`.

But `K=R_+`. For `d=1`,

`e0^T B d=0`,

`v^T B d=-1<0`.

Therefore

`F_{e0+t v}(u)=-2 t u`,

so for every `t>0`,

**`Phi(e0+t v)=-infinity`.**

The zero-residual block is `A=[0]`, while `c=-1`; the Farkas inequality

`A lambda<=c`

would require `0<=-1`, impossible. The tangent packet therefore rejects exactly the unsafe direction.

### 9.2 Unbounded minimizer slice can still have a finite exact derivative

Keep `P=[0]`, `C=0`, `e0=(1,0)`, `v=(0,1)`, but take

`B=[[0],[1]]`.

At `e0`, every `u>=0` is a minimizer. The minimizer set is unbounded.

Along the ray,

`F_{e0+t v}(u)=2 t u`,

whose minimum is `0` at `u=0`. Thus

`Phi'_+(e0;v)=0`.

The frozen-slope LP is

`min u` subject to `u>=0`,

with optimum `0`. Its recession slope is nonnegative, and the exact dual tangent gate is simply `0<=1`.

So unboundedness of `M(e0)` is not itself a derivative obstruction; only a **negative** slope on its recession cone is.

### 9.3 Nontrivial exact LP slope

Take

`P=[1]`, `B=[-1]`, `C=0`, `e0=1`, `v=1`.

Then

`F_e(u)=u^2-2 e u`, `u>=0`,

so near `e0=1` the minimizer is `u=e` and

`Phi(e)=-e^2`.

Hence

`Phi'_+(1;1)=-2`.

At `e0`, the zero-residual LP has

`A=[1]`, `d0=1`, `c=-1`.

Primal optimum: `x_*=1`, value `-1`.

Dual optimum: `lambda_*=-1`, with `A lambda_*=c`, value `-1`.

T190-G gives

`2 c x_*=-2`,

exactly the analytic derivative.

---

## 10. Suggested typed/formal interface

The mathematical objects should remain separated by type.

### 10.1 Finite-value domain packet

`FiniteValueConePacket`

- `P_psd`;
- inherited nonnegative-kernel recession semantics from T-P5-186;
- external state `e0`;
- proof `e0 in E`.

### 10.2 Boundary direction packet

`FiniteTangentPacket`

- external direction `v`;
- orthant active-coordinate inequalities;
- T-P5-188 zero-residual set `I,J`;
- `A=P_II` and `c=(B^T v)_I`;
- exact Farkas witness `lambda,s` with `c=A^T lambda+s`, `s>=0`.

This packet proves local finite-valuedness along the ray; it does not yet prove the derivative value.

### 10.3 Exact derivative packet

`ReducedDirectionalDerivativePacket`

extends the tangent packet with

- primal minimizer-slope witness `x_*>=0`;
- `A x_*=d0`;
- primal/dual equality `c^T x_*=d0^T lambda_*`;
- scalar derivative value

  `delta = 2 v^T C e0 + 2 c^T x_*`.

The checker only needs matrix-vector products, equalities, and entrywise order.

### 10.4 Suggested theorem leaves

- `finiteValueCone_eq_dual_nonnegKernelCone`;
- `finiteValueCone_polyhedral`;
- `tangentFiniteValueCone_iff_criticalRecession_nonneg`;
- `negativeCriticalRecession_immediate_unbounded`;
- `criticalRecession_eq_zeroResidualSliceRecession`;
- `criticalRecession_nonneg_iff_exists_farkasTransport`;
- `reducedValue_rightDirectionalDerivative_eq_minActiveSlope`;
- `zeroResidualSlopeLP_primalDual_certificate`.

The only nontrivial dependency worth keeping explicit in a first Lean decomposition is the T-P5-186 lemma that a minimal-support minimizer has a positive-definite principal block; it supplies the compact subsequence argument in the derivative lower bound without introducing pseudoinverses.

---

## 11. What remains open

This child does not provide:

1. an actual source-bound `(P,B,C)` from Route-B/PDE/Newton-Euler data;
2. proof that a physical ODE/PDE trajectory remains in the finite-value parameter cone `E`;
3. a flow/tangent theorem converting the physical vector field into the exact external direction `v` used here;
4. uniform derivative margins over a cell/polytope rather than one state/direction;
5. Float64/interval outward-rounding semantics for exact zero-residual and tangent classifications;
6. Lean/kernel compilation;
7. independent validation by 封不觉;
8. P8/M4 propagation, admission, or registry closure.

The shortest next mathematical bridge, if this lane continues, is therefore **vector-field viability for the finite-value cone**: translate `v=f(e)` or an interval/vector-field enclosure into a Nagumo-style critical-recession inequality on every active face, preferably with a finite polyhedral checker packet. That would connect this boundary derivative theorem to an actual ODE/PDE trajectory without pretending source binding has already occurred.
