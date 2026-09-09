---
kind: review_result
review_id: review-T-P5-192-cone-selector-lyapunov-margin-honglianmozun-20260909T2250Z
task_id: T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T22:50:00Z
claim_commit: 7eeec1e2fa53dfc26244750cdd31d27c11417b7f
inspected_commit: 980d3ed8a24cc7cf2d0ee60bafb50e2edcc5ea36
upstream_commits:
  - 2cef444f49ae94b85815734cf4376812b76f824a  # T-P5-185 piecewise active-face Schur fan
  - a62b347c8fd585bb8e5e77493a1b2506861d86b4  # T-P5-189 kernel-gauge Dini envelope
  - ed292584c6b459fff851a0fbc6f54bf4087cb7a0  # T-P5-190 exact tangent derivative
  - ef1dfbc4779541e30d02843b282cdd9e892912a2  # T-P5-191 affine finite-cone viability
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_selector_cone_decay_packet; reuse_fixed_copositivity_checker; add_affine_drift_linear_gate; add_seam_safe_dini_comparison
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional convex quadratic/KKT algebra, cone-generator pullback, Dini comparison; rational 2x2 hand regression; no Lean/kernel run
exit_code: not_applicable
---

# T-P5-192 — finite selector-cone Lyapunov margin and exact copositive pullback

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-189 proves that an orthant-minimized quadratic Lyapunov envelope may be nonsmooth at active-face switches but still admits a frozen-minimizer upper-Dini bound. T-P5-190 sharpens the pointwise derivative and T-P5-191 gives a finite viability packet for the external finite-value cone. The remaining energy-method question is how to turn finitely many exact minimizer selectors into a **uniform negative derivative margin** without differentiating the optimizer map and without requiring the selector cones themselves to be dynamically invariant.

This review gives that bridge.

For

`q_H(u,e)=u^T P u+2 e^T B u+e^T C e`, `u>=0`, `P=P^T>=0`, `C=C^T`,

let

`Phi(e)=min_{u>=0} q_H(u,e)`

on a finite-value external cone `E`.

Suppose `E` is covered by finitely many polyhedral cones `C_alpha`, and on each cone there is a **linear exact KKT selector**

`u=Y_alpha e`.

Then on `C_alpha` define the branch-energy matrix

`Q_alpha := Y_alpha^T P Y_alpha + Y_alpha^T B^T + B Y_alpha + C`,

and for affine external dynamics

`e' = A e + c`

define

`G_alpha := B Y_alpha + C`,

`L_alpha := A^T G_alpha + G_alpha^T A`.

For every current state `e in C_alpha`, regardless of whether `A e+c` points into another selector cone,

`Phi(e)=e^T Q_alpha e`

and T-P5-189 gives the seam-safe bound

**`D^+ Phi(e) <= e^T L_alpha e + 2 c^T G_alpha e`.**

Therefore a target rate `gamma>=0` is certified on that selector cone by two independent homogeneous gates:

**quadratic gate**

`e^T (L_alpha+2 gamma Q_alpha)e <=0` for all `e in C_alpha`,

and **constant-drift first-order gate**

`c^T G_alpha e <=0` for all `e in C_alpha`.

If `C_alpha=cone(V_alpha)`, these become exact finite algebraic packets:

**`-V_alpha^T (L_alpha+2 gamma Q_alpha) V_alpha` is copositive,**

and

**`V_alpha^T G_alpha^T c <=0` entrywise.**

Thus the same fixed rational copositivity machinery developed earlier for T-P5-158 and its fast paths can be reused directly for Lyapunov derivative margins.

If all selector cones in a finite cover pass and T-P5-191 (or another trajectory theorem) keeps `e(t)` inside the finite-value cone, then globally

**`D^+ Phi(e(t)) <= -2 gamma Phi(e(t))`,**

so

**`Phi(e(t)) <= exp(-2 gamma t) Phi(e(0))`.**

No optimizer derivative and no active-face switching regularity are required.

---

## 1. Setup and exact selector contract

Let

`P=P^T>=0`, `B in R^(p x m)`, `C=C^T`.

For inherited state `u>=0` and external state `e`, set

`q(u,e)=u^T P u+2 e^T B u+e^T C e`.

Let `E` be a cone on which the minimum is finite and attained. T-P5-190 gives one construction of such an `E`; T-P5-191 gives a trajectory-level invariance checker when the external field is affine.

Fix a polyhedral selector cone `C_alpha subseteq E` and a matrix `Y_alpha` such that for every `e in C_alpha`, with

`y=Y_alpha e`,

all three KKT conditions hold:

1. `y>=0`;
2. `r:=P y+B^T e>=0`;
3. `y^T r=0`.

Since `P>=0`, the inherited problem is convex. These KKT conditions are therefore sufficient and necessary for `y` to be a global orthant minimizer. Hence

`Y_alpha e in M(e)`

for every `e in C_alpha`.

This contract is exactly what T-P5-185/186 active-face constructions are designed to produce. The present child does not rebuild those fans.

---

## 2. T192-A — exact branch-energy quadratic

For one selector `Y=Y_alpha`, define

`Q := Y^T P Y+Y^T B^T+B Y+C`.

This matrix is symmetric.

For every `e in C_alpha`,

`q(Y e,e)=e^T Q e`.

Since `Y e` is an exact minimizer,

**`Phi(e)=e^T Q e`.**

This identity is a value statement only. It does not assert that `Phi` is differentiable across overlaps of different selector cones; T-P5-189 gives explicit counterexamples to such a claim.

The advantage of keeping `Q` in the unsimplified symmetric form above is that no global matrix complementarity identity such as `Y^T(PY+B^T)=0` is needed. Pointwise KKT on the cone is enough.

---

## 3. T192-B — frozen external slope is one symmetric quadratic plus one linear term

Let the external dynamics be affine:

`f(e)=A e+c`.

For a fixed current minimizer `y=Y e`, T-P5-189 gives

`D^+ Phi(e) <= 2 f(e)^T(B y+C e)`.

Define

`G:=B Y+C`.

Then

`B y+C e=G e`,

so

`2 f(e)^T G e`

`=2(Ae+c)^T G e`

`=e^T(A^T G+G^T A)e+2c^T G e`.

Define the symmetric frozen derivative matrix

**`L:=A^T G+G^T A`.**

Therefore, for every `e in C_alpha`,

**`D^+ Phi(e) <= e^T L e+2c^T G e`.**

### Important seam fact

The vector `f(e)` does **not** need to lie in the tangent cone of `C_alpha`.

The selector cone is only used to certify that `Y e` is a minimizer at the current state. The frozen-state Dini argument remains valid if the actual trajectory immediately crosses into a different active-face cone. Only the global finite-value domain `E` must remain viable.

This is the main reason the certificate is safe at active-face switching seams.

---

## 4. T192-C — target decay rate on one selector cone

Fix `gamma>=0`.

On `C_alpha`, because `Phi(e)=e^T Q e`, it is sufficient to require

`e^T L e+2c^T G e <= -2 gamma e^T Q e`.

Equivalently,

**`e^T M e+2 ell^T e <=0`**

for every `e in C_alpha`, where

`M:=L+2 gamma Q`,

`ell:=G^T c`.

Because `C_alpha` is a cone, this mixed degree inequality separates **exactly** into two gates:

1. `e^T M e<=0` for every `e in C_alpha`;
2. `ell^T e<=0` for every `e in C_alpha`.

### Proof of exact separation

Sufficiency is immediate by addition.

For necessity, fix any `r in C_alpha` and apply the mixed inequality to `e=t r`, `t>0`:

`t^2 r^T M r+2t ell^T r<=0`.

Divide by `t`:

`t r^T M r+2 ell^T r<=0`.

Let `t downarrow 0`; this gives

`ell^T r<=0`.

Now divide the original inequality by `t^2`:

`r^T M r+(2/t)ell^T r<=0`.

Alternatively, after the linear gate is already known, let `t -> infinity`; any `r^T M r>0` would eventually violate the inequality. Hence

`r^T M r<=0`.

Since `r` was arbitrary, both gates are necessary.

### Structural meaning

A constant affine drift is a first-order effect near the cone vertex; it cannot be hidden inside a quadratic Lyapunov margin. The first-order sign must be paid separately.

---

## 5. T192-D — exact generator pullback to ordinary copositivity

Let a selector cone be finitely generated:

`C_alpha=cone(V_alpha)`.

Every `e in C_alpha` has the form

`e=V_alpha xi`, `xi>=0`.

For the quadratic gate,

`e^T M e=xi^T(V_alpha^T M V_alpha)xi`.

Therefore

`e^T M e<=0` for every `e in C_alpha`

iff

**`-V_alpha^T M V_alpha` is copositive.**

This is exact even if the generator representation is redundant or nonunique.

For the linear gate,

`ell^T e=(V_alpha^T ell)^T xi`.

Hence

`ell^T e<=0` for every `e in C_alpha`

iff

**`V_alpha^T ell<=0` entrywise.**

Substituting `M=L_alpha+2 gamma Q_alpha` and `ell=G_alpha^T c` gives the trusted-side packet:

### `SelectorConeLyapunovMarginPacket(alpha,gamma)`

- rational generator matrix `V_alpha`;
- rational selector `Y_alpha` with exact KKT validity on its cone;
- rational `P,B,C,A,c`;
- `Q_alpha=Y_alpha^T P Y_alpha+Y_alpha^T B^T+B Y_alpha+C`;
- `G_alpha=B Y_alpha+C`;
- `L_alpha=A^T G_alpha+G_alpha^T A`;
- exact copositivity of

  **`R_alpha(gamma):=-V_alpha^T(L_alpha+2 gamma Q_alpha)V_alpha`;**

- exact sign

  **`V_alpha^T G_alpha^T c<=0`.**

The copositivity subproblem is exactly the fixed rational problem already closed mathematically by T-P5-158, with lower-cost PSD/Z/forest/pivot fast paths available from later children. No new nonlinear optimizer is needed here.

---

## 6. T192-E — finite-cover seam-safe Lyapunov theorem

Assume:

1. `E` is forward invariant for the actual external trajectory;
2. `E` is covered by finitely many selector cones:

   `E subseteq union_alpha C_alpha`;

3. on every `C_alpha`, `Y_alpha e` satisfies the exact KKT selector contract;
4. every selector cone passes the T192-D packet at the same `gamma>=0`;
5. `Phi` is finite and continuous on `E` (as supplied by the preceding convex-quadratic framework).

Then along every trajectory in `E`,

**`D^+ Phi(e(t)) <= -2 gamma Phi(e(t))`.**

### Proof

At a current state `e`, choose any `alpha` with `e in C_alpha`. The current selector `Y_alpha e` is an exact minimizer. T192-B gives

`D^+ Phi(e)<=e^T L_alpha e+2c^T G_alpha e`.

The cone packet gives

`e^T L_alpha e+2c^T G_alpha e<=-2 gamma e^T Q_alpha e`.

T192-A gives

`e^T Q_alpha e=Phi(e)`.

Hence the desired Dini inequality follows.

No compatibility of derivatives between overlapping cones is needed. No optimizer selection needs to be continuous. No selector cone needs to be invariant.

---

## 7. T192-F — exponential energy comparison

Assume `gamma>0` and `Phi>=0` on `E`.

From T192-E,

`D^+ Phi(t)<=-2 gamma Phi(t)`.

Set

`W(t)=exp(2 gamma t) Phi(t)`.

The upper Dini derivative satisfies

`D^+ W(t)<=0`.

Hence `W` is nonincreasing and

**`Phi(e(t))<=exp(-2 gamma t) Phi(e(0))`.**

If a separate coercivity packet gives lower/upper state bounds on `Phi`, this can be converted into state-norm decay. That coercivity is a distinct obligation and is not assumed here.

---

## 8. Exact nonsmooth regression: the T-P5-189 kink still admits rate 1

Take

`P=[[1,1],[1,1]]`,

`B=-I_2`,

`C=I_2`.

For `e>=0`, T-P5-189 showed

**`Phi(e1,e2)=min(e1,e2)^2`.**

This is genuinely nondifferentiable on the positive seam `e1=e2>0`.

Use two selector cones:

`C_1={e1>=e2>=0}=cone{(1,0),(1,1)}`,

`C_2={e2>=e1>=0}=cone{(0,1),(1,1)}`.

On `C_1`, choose

`Y_1=[[1,0],[0,0]]`,

so `u=(e1,0)` is an exact minimizer.

On `C_2`, choose

`Y_2=[[0,0],[0,1]]`,

so `u=(0,e2)` is an exact minimizer.

Take homogeneous stable dynamics

`A=-I_2`, `c=0`.

For cone 1, exact algebra gives

`Q_1=diag(0,1)`,

`G_1=diag(0,1)`,

`L_1=diag(0,-2)`.

At `gamma=1`,

`L_1+2 Q_1=0`.

For cone 2,

`Q_2=diag(1,0)`,

`G_2=diag(1,0)`,

`L_2=diag(-2,0)`,

and again

`L_2+2 Q_2=0`.

Thus both generator-pulled copositivity matrices are exactly zero and the drift gate is vacuous. Therefore

**`D^+ Phi=-2 Phi`**

along the flow, including the nondifferentiable seam.

The full quadratic is smooth; the reduced Lyapunov function is kinked; yet the finite cone-selector packet certifies the exact decay rate without selecting a differentiable optimizer.

---

## 9. Exact affine-drift obstruction: viability is not decay

Take the scalar reduced energy

`Phi(e)=e^2` on `E=R_+`,

with affine dynamics

`e'=-e+1`.

The cone is forward invariant. In T-P5-191 notation,

`N=[1]`, `A=[-1]`, `c=[1]`, `Lambda=[-1]`,

so

`N A=Lambda N`,

`N c=1>=0`.

Thus the **viability packet passes exactly**.

For the Lyapunov packet take `Y=0`, `B=0`, `C=1`. Then

`Q=1`, `G=1`, `L=-2`.

At target `gamma=1`, the quadratic gate is perfect:

`L+2 gamma Q=0`.

But the first-order drift gate is

`c G e=e>0` for `e>0`,

so it fails.

Indeed

`d/dt Phi=2e(-e+1)`,

which is positive for `0<e<1`.

This pins the logical boundary:

**forward invariance of the finite-value cone does not imply decay of a zero-centered homogeneous Lyapunov energy.**

A nonzero constant drift must either satisfy the T192 linear gate on every selector cone, lie entirely in a zero-energy direction, or be handled by a shifted/ISS-type storage theorem. It cannot be silently absorbed into the quadratic rate matrix.

A stronger scaling obstruction follows immediately: if `Phi` is positive on the drift ray `c` and the trajectory starts at the cone vertex, then `e(t)=t c+O(t^2)` gives `Phi(e(t))=t^2 Phi(c)+o(t^2)>0`, whereas a global estimate `Phi(t)<=exp(-2 gamma t)Phi(0)=0` would force `Phi(t)=0`. Thus a coercive zero-centered storage cannot have global exponential decay under nonzero inward constant drift.

---

## 10. Failure boundaries

### 10.1 Missing selector coverage

If a physical state in `E` lies in no certified selector cone, the theorem says nothing there. Sampling or generic KKT existence is not a substitute for a finite cover proof.

### 10.2 Selector KKT is pointwise, not merely matrix-shaped

A guessed matrix `Y_alpha` is not valid merely because it solves one stationarity equation. The cone must guarantee

`Y_alpha e>=0`,

`P Y_alpha e+B^T e>=0`,

and complementarity for every `e` in that cone.

### 10.3 Copositivity only after generator pullback

The correct quadratic object is

`-V_alpha^T(L_alpha+2 gamma Q_alpha)V_alpha`.

Requiring `-(L_alpha+2 gamma Q_alpha)` to be PSD on the full ambient space is only a stronger sufficient test and can lose valid cone-local decay.

### 10.4 Cone switching is not a blocker

A trajectory may cross from `C_alpha` to `C_beta`. No active-face derivative matching is required because the proof uses the current frozen minimizer and the upper Dini derivative.

### 10.5 Finite-value-domain viability remains separate

If the external trajectory can leave `E`, T-P5-190 shows the inherited minimum may become `-infinity`. T192 does not repair that; T-P5-191 or another trajectory/domain theorem must keep the state inside the finite-value cone.

### 10.6 Source binding and physical coverage remain external

This child does not identify actual Route-B/PDE matrices `P,B,C,A,c`, prove a physical selector fan, or certify an actual trajectory domain.

---

## 11. Candidate theorem statements

### Theorem `selectorCone_dini_decay_of_kkt`

Given `P>=0`, a cone `C=cone(V)`, an exact linear KKT selector `Y` on `C`, affine dynamics `f(e)=Ae+c`, and `gamma>=0`, if

`-V^T(L+2 gamma Q)V`

is copositive and

`V^T G^T c<=0`,

then for every `e in C`,

`D^+ Phi(e;f(e))<=-2 gamma Phi(e)`.

### Theorem `finiteSelectorCover_dini_decay`

If finitely many selector cones cover a forward-invariant finite-value domain and every cone satisfies the preceding theorem with the same `gamma`, then the reduced envelope satisfies the global upper-Dini decay inequality.

### Theorem `finiteSelectorCover_exponential_energy_decay`

Under nonnegativity of `Phi` and `gamma>0`, the preceding Dini inequality implies

`Phi(e(t))<=exp(-2 gamma t)Phi(e(0))`.

### Lemma `affineConeMixedDegree_nonpos_iff`

For a cone `C`, symmetric `M`, and vector `ell`,

`e^T M e+2 ell^T e<=0` for all `e in C`

iff both

`e^T M e<=0` and `ell^T e<=0` for all `e in C`.

This scaling lemma is the exact reason the constant drift gate cannot be hidden inside the quadratic gate.

---

## 12. Recommended checker order

For each selector cone:

1. verify exact KKT selector inequalities/equalities on the cone;
2. build exact rational `Q_alpha,G_alpha,L_alpha`;
3. check `V_alpha^T G_alpha^T c<=0`;
4. build `R_alpha(gamma)=-V_alpha^T(L_alpha+2 gamma Q_alpha)V_alpha`;
5. run cheap PSD/Z/forest/pivot copositivity fast paths where applicable;
6. if necessary, use T-P5-158's exact support-KKT copositivity fallback;
7. only after every selector cone passes, combine with an independent finite-value-domain viability packet.

This keeps optimizer switching, viability, derivative negativity, source identity, and formal admission as separate proof obligations.

---

## 13. What remains open

This child does not provide:

1. actual source-bound `P,B,C,A,c` or a Route-B/PDE key;
2. a source-bound finite selector cover `C_alpha,Y_alpha,V_alpha`;
3. physical trajectory/domain coverage;
4. construction of the largest admissible `gamma` across all cones;
5. a shifted/ISS storage theorem for the common case where nonzero affine drift fails the first-order gate;
6. Float64/interval outward-rounding semantics;
7. Lean/kernel compilation;
8. independent validation by 封不觉;
9. admission, registry, P8, or M4 propagation.

A mathematically useful next child, **only after an actual selector/source packet exists**, is rate optimization: each cone gives an affine matrix pencil in `gamma`, and the global certified rate is the minimum cone-wise copositive threshold. Without actual matrices, abstract rate optimization would add machinery without reducing the current source obstruction.