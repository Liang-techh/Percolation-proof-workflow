---
kind: review_result
review_id: review-T-P5-185-piecewise-active-face-orthant-schur-fan-honglianmozun-20260909T2055Z
task_id: T-P5-185-PIECEWISE-ACTIVE-FACE-ORTHANT-SCHUR-FAN
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T20:55:00Z
claim_commit: d4fcf792f51ee10a4a12c0def7d31d1f650e3165
inspected_commit: 019fb0c240e6532d03d2921451e5fdc03edb876b
upstream_commits:
  - aa8d1c1c47b9c5fedf6f5bb86691b6b6f89b7646  # T-P5-183 complementary orthant Schur transport
  - 038a8508822dd9f0603d2b8374191c91430d3686  # T-P5-182 orthant-feasible PSD-block Schur descent
  - a851e8ba5abd1fbb8578d668f9c00a14eeb2b879  # T-P5-184 PSD Z-matrix monotone range solve
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_piecewise_active_face_transport; add_pd_active_set_schur_fan; route_global_T183_gap_to_cellwise_cone_reduction
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic/KKT algebra; exact rational regression
exit_code: 0 for hand-checked exact identities; no Lean/kernel run
---

# T-P5-185 — piecewise active-face orthant Schur fan

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-183 proved a lossless one-sided Schur reduction when one global linear transport

`Y >= 0`, `R := P Y + B^T >= 0`, `Y^T R = 0`

works for every retained external direction `e >= 0`. Its remaining-obligation list explicitly leaves open the case in which no such global complementary transport exists and asks for a sound cone/active-face subdivision rather than unsound columnwise stacking.

This review closes that mathematical seam.

The key point is that global entrywise signs on `Y` and `R` are stronger than the energy argument actually needs. For a fixed external direction `e`, the completion only needs the **pointwise** conditions

`Y e >= 0`, `R e >= 0`, `(Y e)^T (R e) = 0`.

Therefore different external cones may use different inherited active faces and different linear transports. On each cone the full constrained energy has an exact reduced quadratic value. A finite cone cover then gives a global iff theorem.

When the inherited block `P` is positive definite, such a finite cover exists automatically: enumerate inherited active faces. The external orthant is partitioned/covered by finitely many rational polyhedral KKT cones, and on each cone the Lyapunov/copotivity energy is exactly one quadratic form. This is an **active-face Schur fan**.

This is strictly stronger than T-P5-183's single-global-transport branch. An exact rational example below has no global complementary linear transport at all, but two cones give an exact global proof.

No actual source identity, support/contact binding, domain/path coverage, Float64/controller semantics, Lean/kernel verification, independent validation, admission, registry mutation, P8/M4, or parent closure is claimed.

---

## 1. Setup

Let

`P=P^T in R^{m x m}`, `P >= 0`,

`B in R^{p x m}`,

`C=C^T in R^{p x p}`,

and define

`H = [[P, B^T], [B, C]]`.

For inherited coordinates `u in R_+^m` and retained external coordinates `e in R_+^p`, write

`q_H(u,e) = u^T P u + 2 e^T B u + e^T C e`.

For any linear transport matrix `Y in R^{m x p}`, define

`R := P Y + B^T`,

`K := C - Y^T P Y`.

The algebraic identity from T-P5-183 is

**(1.1)**

`q_H(u,e)`

`= (u-Y e)^T P (u-Y e)`

`  + 2 u^T R e`

`  + e^T K e`.

The new content is to use this identity **regionally** rather than requiring one `Y` to satisfy global matrix complementarity.

---

## 2. T185-A — pointwise complementary transport gives the exact constrained energy

### Theorem

Fix one `e >= 0`. Suppose a matrix `Y` satisfies

**(2.1)** `Y e >= 0`,

**(2.2)** `R e >= 0`, where `R=P Y+B^T`,

**(2.3)** `(Y e)^T(R e)=0`.

Then

**(2.4)**

`min_{u >= 0} q_H(u,e) = e^T K e`,

where `K=C-Y^T P Y`.

In particular, the minimum is attained at

**(2.5)** `u_*(e)=Y e`.

### Proof

For arbitrary `u>=0`, (1.1), PSD of `P`, and `R e>=0` give

`q_H(u,e) >= e^T K e`,

because

`(u-Ye)^T P(u-Ye) >= 0`

and

`u^T R e >=0`.

The point `u=Ye` is feasible by (2.1). Substituting it into (1.1) gives

`q_H(Ye,e)`

`= 0 + 2 (Ye)^T(Re) + e^T K e`

`= e^T K e`

by (2.3). Thus the lower bound is attained exactly. QED.

### Energy interpretation

The first term is the inherited dissipative square. The second term is the one-sided KKT work. Complementarity says the proposed minimizer pays no KKT work. Nothing in this proof requires `Y>=0` or `R>=0` entrywise as matrices; only their action on the current external direction matters.

---

## 3. T185-B — cone-wise exact reduction

Let `C_alpha` be any cone contained in `R_+^p`. Give it its own transport `Y_alpha` and define

`R_alpha=P Y_alpha+B^T`,

`K_alpha=C-Y_alpha^T P Y_alpha`.

Assume that for **every** `e in C_alpha`,

**(3.1)** `Y_alpha e >=0`,

**(3.2)** `R_alpha e >=0`,

**(3.3)** `(Y_alpha e)^T(R_alpha e)=0`.

Then by T185-A,

**(3.4)**

`min_{u>=0} q_H(u,e)=e^T K_alpha e`

for every `e in C_alpha`.

Hence on one cell/cone,

**(3.5)**

`q_H(u,e)>=0 for all u>=0,e in C_alpha`

iff

`e^T K_alpha e>=0 for all e in C_alpha`.

The FAIL direction is constructive: if `e in C_alpha` has `e^T K_alpha e<0`, then

**(3.6)** `(u,e)=(Y_alpha e,e)`

is an exact nonnegative negative-energy witness for the full block.

---

## 4. T185-C — finite cone cover gives a global iff

Suppose finitely many cones

`{C_alpha}_{alpha in A}`

cover the retained external orthant:

**(4.1)** `R_+^p = union_alpha C_alpha`.

On each cone assume the pointwise transport packet (3.1)-(3.3).

Then

### Main theorem `copositive_iff_piecewiseComplementaryTransport`

**(4.2)**

`H is copositive`

iff

for every `alpha`, `K_alpha` is nonnegative on `C_alpha`.

### Proof

For any `e>=0`, choose a cone containing it. T185-B computes the exact constrained minimum over `u>=0`. Thus the full quadratic is nonnegative for all `(u,e)>=0` exactly when every regional reduced minimum is nonnegative. QED.

### Overlap consistency

The cones need not form a disjoint partition. If `e` belongs to two valid cones `C_alpha,C_beta`, then both reduced values equal the same physical constrained minimum, so automatically

**(4.3)** `e^T K_alpha e=e^T K_beta e`.

No extra gluing equation is mathematically necessary on overlaps.

---

## 5. T185-D — fixed inherited face packet

The pointwise complementarity conditions become particularly cheap when a cone is assigned one inherited active face.

Let

`F subseteq {1,...,m}`

be the transported/positive inherited coordinates and let `J=F^c`.

A sufficient exact packet on a cone `C_alpha` is

**(5.1)** `(Y_alpha e)_J = 0` for all `e in C_alpha`,

**(5.2)** `(R_alpha e)_F = 0` for all `e in C_alpha`,

**(5.3)** `(Y_alpha e)_F >=0` for all `e in C_alpha`,

**(5.4)** `(R_alpha e)_J >=0` for all `e in C_alpha`.

Then `Y_alpha e` and `R_alpha e` are nonnegative and have disjoint supports, so

`(Y_alpha e)^T(R_alpha e)=0`

automatically.

This is the regional version of T-P5-183's row-separation theorem. The crucial difference is that the face is allowed to depend on the external cone.

---

## 6. T185-E — finitely generated rational cones have a finite exact checker

Suppose a cone is supplied by generators

`C_alpha = cone(v_1,...,v_s)`

with each `v_j>=0`.

Because (5.1)-(5.4) are linear equalities/inequalities in `e`, it is enough to verify them on the generators:

**(6.1)** `(Y_alpha v_j)_J=0`,

**(6.2)** `(R_alpha v_j)_F=0`,

**(6.3)** `(Y_alpha v_j)_F>=0`,

**(6.4)** `(R_alpha v_j)_J>=0`

for `j=1,...,s`.

Every nonnegative conic combination then inherits the same gates.

If `V_alpha=[v_1 ... v_s]`, cone-restricted nonnegativity of the reduced quadratic also has the exact pullback

**(6.5)**

`e^T K_alpha e>=0 for all e in C_alpha`

iff

`lambda^T(V_alpha^T K_alpha V_alpha)lambda>=0 for all lambda>=0`.

Thus, once an exact ray/generator representation is available, the remaining regional quadratic obligation is an ordinary copositivity problem for

**(6.6)** `V_alpha^T K_alpha V_alpha`.

For rational `P,B,C,Y_alpha,V_alpha`, every trusted check in this packet is rational arithmetic plus the already-existing copositivity layer. No square root, eigenvector, pseudoinverse, floating tolerance, or nonlinear optimizer is required by the transport theorem itself.

---

## 7. T185-F — positive-definite inherited energy automatically yields a finite active-face fan

The previous theorems assume a valid cone cover is supplied. In the important strict-energy branch, the cover exists canonically.

Assume now

**(7.1)** `P>0` in the ordinary positive-definite sense.

For each inherited face `F subseteq {1,...,m}`, let `J=F^c`. Since every principal block `P_FF` is positive definite, define the unique face transport

**(7.2)** `Y_F[F,:] := -P_FF^{-1} B_F^T`,

**(7.3)** `Y_F[J,:] := 0`.

Define its residual

`R_F := P Y_F+B^T`.

By construction,

**(7.4)** `(R_F)[F,:]=0`,

and

**(7.5)** `(R_F)[J,:]=P_JF Y_F[F,:]+B_J^T`.

Now define the external KKT cone

**(7.6)**

`C_F := {e>=0 : (Y_F e)_F>=0 and (R_F e)_J>=0}`.

The other two fixed-face conditions are matrix identities, so every `e in C_F` satisfies T185-D.

### Theorem `pd_activeFaceFan_covers_orthant`

**(7.7)**

`R_+^p = union_{F subseteq [m]} C_F`.

### Proof

Fix arbitrary `e>=0`. Consider the strictly convex coercive quadratic program

**(7.8)**

`min_{u>=0} [u^T P u + 2 e^T B u]`.

Positive definiteness gives a unique minimizer `u_*`.

Let

`F={i:(u_*)_i>0}`, `J=F^c`.

The KKT conditions for the nonnegative orthant are

**(7.9)** `r_*:=P u_*+B^T e>=0`,

**(7.10)** `(u_*)_i(r_*)_i=0` for every `i`.

Hence

`(r_*)_F=0`, `(u_*)_J=0`.

The active equations are therefore

`P_FF (u_*)_F+B_F^T e=0`.

Since `P_FF` is invertible,

**(7.11)** `(u_*)_F=Y_F[F,:] e`.

The inactive KKT inequalities give

**(7.12)** `(R_F e)_J=(r_*)_J>=0`.

Thus `e in C_F`. Since `e` was arbitrary, the cones cover the whole external orthant. QED.

### Exact regional value

Define

**(7.13)** `K_F:=C-Y_F^T P Y_F`.

Then for every `e in C_F`,

**(7.14)**

`min_{u>=0} q_H(u,e)=e^T K_F e`.

Therefore

### Corollary `pd_block_copositive_iff_activeFaceFan`

**(7.15)**

`H copositive`

iff

for every inherited face `F`, `K_F` is nonnegative on `C_F`.

There are at most `2^m` face cones; empty cones may be discarded.

---

## 8. Piecewise-quadratic Lyapunov envelope

Under `P>0`, define the constrained inherited-energy value function

`Phi(e):=min_{u>=0} q_H(u,e)`.

T185-F gives the exact formula

**(8.1)**

`Phi(e)=e^T K_F e` whenever `e in C_F`.

Thus `Phi` is a continuous piecewise-quadratic homogeneous degree-two function on the external orthant, with polyhedral active-set cells.

The continuity here does not require a separate analytic proof: on any overlap, Section 4 already shows the regional quadratics equal the same unique constrained minimum.

This is the relevant Lyapunov/energy structural fingerprint:

> **strict inherited dissipation + orthant constraint -> finite KKT fan -> exact piecewise quadratic reduced energy.**

One should not pay a global unsigned envelope merely because the active inherited face changes with direction.

---

## 9. Rationality in the positive-definite branch

If `P` and `B` are rational and `P>0`, every principal `P_FF` is nonsingular rational. Hence every face solve

`P_FF Y_F[F,:]=-B_F^T`

has a rational solution matrix.

Consequently:

- every `Y_F` is rational;
- every residual matrix `R_F` is rational;
- every cone `C_F` is a rational polyhedral cone;
- every reduced `K_F` is rational when `C` is rational.

A producer can therefore enumerate faces using exact Gaussian elimination and exact linear inequalities. The theorem does not require an LCP solver to be trusted. An LCP/QP routine may be used as an untrusted discovery accelerator, but exact rational face equations are sufficient evidence for the mathematical layer.

---

## 10. Exact strict separation — no global T183 transport, but a two-cone fan is exact

Take one inherited variable and two external variables:

`P=[1]`,

`B^T=[1,-1]`,

`C=[[1,-1],[-1,1]]`.

Write

`d:=e_1-e_2`.

Then for `u,e_1,e_2>=0`,

**(10.1)**

`q_H(u,e)=u^2+2ud+d^2=(u+d)^2>=0`.

So the full block is copositive.

### Why no single global T-P5-183 complementary transport exists

Here `Y` and `R` each have one inherited row. For nonnegative matrices, T-P5-183's global condition `Y^TR=0` forces row separation: either

- `Y=0`, or
- `R=0`.

If `Y=0`, then

`R=B^T=[1,-1]`,

which is not entrywise nonnegative.

If `R=0`, then

`Y=-B^T=[-1,1]`,

which is not entrywise nonnegative.

Thus the single-global-transport branch fails genuinely.

### Cone 1: boundary-active inherited face

Let

**(10.2)** `C_+={e>=0:e_1>=e_2}`.

Choose

`Y_+=0`, `R_+=[1,-1]`.

For `e in C_+`,

`Y_+e=0`,

`R_+e=d>=0`,

so pointwise complementarity holds. The reduced matrix is

`K_+=C`,

and

**(10.3)** `e^T K_+ e=d^2`.

The exact constrained minimizer is `u=0`.

### Cone 2: transported inherited face

Let

**(10.4)** `C_-={e>=0:e_2>=e_1}`.

Choose

`Y_-=[-1,1]`.

This matrix is **not** entrywise nonnegative, which is precisely why global T-P5-183 cannot use it. But on `C_-`,

**(10.5)** `Y_-e=e_2-e_1=-d>=0`.

Moreover

`R_-=Y_-+B^T=0`.

Since

`Y_-^T Y_- = [[1,-1],[-1,1]]=C`,

the reduced matrix is

**(10.6)** `K_-=0`.

Thus the exact constrained minimum on `C_-` is zero, achieved at

`u=e_2-e_1`.

The two cones cover the external orthant. Hence T185-C proves the full copositivity of (10.1) exactly even though the global T183 packet is impossible.

### Structural lesson

**Failure of a global complementary transport is not a mathematical obstruction. It may only mean that the inherited active face depends on the external direction.**

Regional transport matrices need not be entrywise nonnegative; they only need to map their own cone into the inherited orthant.

---

## 11. Boundary A — singular PSD blocks are not automatically covered by the PD fan theorem

The general cellwise theorem T185-A through T185-E only requires `P>=0` and remains valid for singular `P` whenever valid cone transports are supplied.

However T185-F deliberately assumes `P>0`. If `P` is singular:

- some `P_FF` may be singular;
- the constrained minimizer may be nonunique;
- a face equation may require a range-compatibility condition;
- a nullspace recession direction can make the value `-infinity` for some external directions;
- a canonical linear face transport may not exist without additional gauge/range data.

Therefore one must not claim automatic finite-face construction from T185-F in the singular branch. Route singular faces through the existing kernel/range/recession machinery (T-P5-174/T-P5-178/T-P5-182/T-P5-184) or a later dedicated parametric singular-face theorem.

---

## 12. Boundary B — a partial cone list is only a partial theorem

If supplied cones cover only a strict subset of `R_+^p`, then the regional reductions certify only that subset. No global copositivity conclusion follows.

For the automatic PD fan, enumerating all inherited faces proves coverage mathematically by T185-F. If a producer prunes faces, it must justify that the remaining cones still cover the target external cone/domain.

Coverage of this **mathematical external orthant** must also not be confused with the repository's physical source/domain/path coverage gate; the latter remains external.

---

## 13. Boundary C — generator checks do not solve the reduced copositivity obligation by themselves

Verifying face feasibility on cone generators closes the transport/KKT part only.

The reduced condition

`e^T K_F e>=0 on C_F`

is still a quadratic cone problem. With a generator representation it becomes ordinary copositivity of `V_F^T K_F V_F`, but that copositivity still needs an existing mathematical certificate/checker such as the T-P5-155/T-P5-158 family or another structural fast path.

Do not label an active-face cone PASS merely because its KKT inequalities are valid.

---

## 14. Boundary D — per-column complementarity remains unsound

T-P5-183's warning remains fully active. One cannot solve each external basis column separately, obtain different inherited supports, and then stack those columns into one global `Y` without controlling mixed directions.

T185 fixes this by making the **external region itself part of the theorem**. A face/transport is valid only on a cone where its pointwise linear KKT signs and complementarity hold for every direction in that cone.

Thus the correct replacement for unsound column stacking is not “different columns, same region”; it is **different active faces on different cones**.

---

## 15. Checker-facing packet

### General regional packet

For each cone/cell `alpha`, provide under one exact reduced key:

1. `P=P^T>=0`, `B`, `C=C^T`;
2. exact cone description `C_alpha subseteq R_+^p`;
3. exact `Y_alpha`;
4. `R_alpha=P Y_alpha+B^T`;
5. proof/check that `Y_alpha e>=0` on `C_alpha`;
6. proof/check that `R_alpha e>=0` on `C_alpha`;
7. proof/check that `(Y_alpha e)^T(R_alpha e)=0` on `C_alpha`;
8. `K_alpha=C-Y_alpha^T P Y_alpha`;
9. cone-restricted copositivity certificate for `K_alpha`.

Together with an exact cover of the target external cone, this gives a global iff.

### Fixed-face rational packet

For a finitely generated cone `C_alpha=cone(V_alpha)` and inherited face `F`, it is enough to check generatorwise

- `(Y_alpha V_alpha)_J=0`;
- `(R_alpha V_alpha)_F=0`;
- `(Y_alpha V_alpha)_F>=0`;
- `(R_alpha V_alpha)_J>=0`;

then check copositivity of

`V_alpha^T K_alpha V_alpha`.

### Positive-definite automatic packet

If `P>0`, enumerate all `F`, solve

`P_FF Y_F[F,:]=-B_F^T`, `Y_F[J,:]=0`,

construct

`C_F={e>=0:Y_F[F,:]e>=0, (P_JF Y_F[F,:]+B_J^T)e>=0}`,

and check the corresponding reduced quadratic on each nonempty cone. T185-F supplies the cover theorem.

---

## 16. Suggested Lean theorem decomposition

Good first leaves are exact identities and finite-dimensional cone statements.

### `pointwiseOrthantTransport_value`

Assume `P` PSD, `e>=0`, `Ye>=0`, `Re>=0`, `dot (Ye) (Re)=0`, `R=PY+B^T`.

Prove the lower bound for all `u>=0` and equality at `u=Ye`.

### `copositiveOn_iff_reducedOn_of_pointwiseTransport`

Lift the previous result to a predicate on one external cone.

### `copositive_iff_of_finiteTransportCover`

Assume a finite family of cones covers the external orthant and each cone has the pointwise packet. Reduce full copositivity to regional reduced nonnegativity.

### `fixedFaceTransport_of_generatorGates`

For a finitely generated cone, prove generatorwise linear gates imply pointwise complementarity on the full cone.

### `copositiveOn_coneGenerators_iff`

Prove restricted nonnegativity of `K` on `cone(V)` iff ordinary copositivity of `V^T K V`.

### `pd_activeFaceFan_cover`

For finite-dimensional positive-definite `P`, formalize existence/uniqueness of the orthant quadratic minimizer and show every `e>=0` lies in at least one face cone.

The review itself has no Lean receipt and should not be promoted on theorem text alone.

---

## 17. Recommended routing

For an inherited one-sided block after T-P5-179/T-P5-182:

1. first try T-P5-184 if the inherited PSD block is a Z-matrix and the exact nonnegative right-hand-side sign corridor applies;
2. otherwise try T-P5-183's single global complementary transport, because it is cheapest when it exists;
3. if the global transport fails because active rows change with external direction, **do not declare failure** and do not stack per-column LCP witnesses;
4. if `P>0`, invoke T185-F and enumerate the finite inherited active-face fan;
5. if `P>=0` is singular, use T185-A-E only with supplied valid regional transports and route the construction/range/recession issue to the singular kernel machinery;
6. reduce each regional quadratic via cone generators to the existing copositivity dispatcher;
7. only after all regions covering the target cone pass may the mathematical block be called closed.

---

## 18. Remaining obligations

Still open:

1. actual same-key production of the `P,B,C` block for the physical P5 path;
2. deciding whether the actual inherited block is PD, singular PSD, Z-matrix, or outside these fast corridors;
3. if using the PD fan, exact construction and pruning/nonemptiness of the actual face cones;
4. cone-restricted copositivity certificates for every surviving reduced `K_F`;
5. singular-PSD automatic fan construction, if the actual block is singular and global T183/T184 do not close it;
6. physical source identity, domain/path coverage, Float64/controller/FD semantics, P8/M4;
7. Lean/kernel compilation and theorem/axiom receipt;
8. independent validation by 封不觉;
9. admission/registry integration.

The mathematical child remains

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.**