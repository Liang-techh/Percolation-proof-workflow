---
kind: review_result
review_id: review-T-P5-201-mixed-domain-augmented-copositive-support-liuguanyi-20260910T0100Z
task_id: T-P5-201-MIXED-DOMAIN-AUGMENTED-COPOSITIVE-SUPPORT
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T01:00:00Z
claim_commit: ad5cb51680b87b473b387eb2c13603db00d445a8
inspected_commit: 16ea10686880988223ce83435ca286e6dec924c5
upstream_commits:
  - 1f9a8d60bd1f8ace3561369c96f3a18718c67569  # T-P5-198 quadratic-domain radial cap
  - 04872637e1d211b2e91bb7be8bce2894ba043624  # T-P5-199 polyhedral selector LP-dual transport
  - 12a92536fc8371342e54845225a423ad33323407  # T-P5-200 gauge-invariant signed amplitude support
  - 44f14ed1d40c4edc2a4bac8eb5851ea2dae4c55c  # T-P5-197 weighted radial cubic absorption
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_mixed_polyhedral_quadratic_support_packet; preserve_signed_physical_slope; use_augmented_copositivity_as_exact_lagrangian_checker; add_selector_gauge_pullback; route_zero_cost_recession_to_unbounded_support
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact slack-identity derivation; homogenized copositivity equivalence; convex-duality completeness under PSD+Slater; exact rational sharp regression; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-201 — mixed polyhedral + quadratic domain support via one augmented copositive packet

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-198 gives an exact support gate when the consumed selector domain is purely quadratic,

`y >= 0,   y^T P y <= rho`,

and T-P5-199 gives an exact LP-dual gate when it is purely polyhedral,

`y >= 0,   C y <= d`.

T-P5-200 then shows why a signed physical support `b^T y <= B`, especially with `b=V^T h`, should be preserved rather than replaced by a nonnegative selector majorant whenever possible.

The remaining seam explicitly left open by those reviews is the **intersection**

`F_mix := { y >= 0 : C y <= d, y^T P y <= rho }`.

The main result of this child is that the two domain descriptions can be used simultaneously with no new nonlinear optimizer in the trusted checker.

For any multipliers

`lambda >= 0`, `tau >= 0`,

define

`a := B - d^T lambda - tau rho`,

`r := C^T lambda - b`,

and the augmented symmetric matrix

`M(lambda,tau,B) := [[a, r^T/2], [r/2, tau P]]`.

If this matrix is copositive on the lifted orthant `(t,y) >= 0`, then every mixed-domain state satisfies

**`b^T y <= B`.**

The proof is the exact gap identity

**`B - b^T y`**

**`= [1;y]^T M(lambda,tau,B) [1;y]`**

**`  + lambda^T (d-Cy)`**

**`  + tau (rho-y^T P y)`.**

Thus the certificate separates into exactly three nonnegative pieces: an augmented copositive quadratic remainder, the polyhedral slack, and the quadratic-domain slack.

This is not merely a sufficient ad-hoc interpolation. In the convex regime `P >= 0` (PSD), a standard Slater condition plus a finite support bound makes this packet **complete** by convex Lagrange strong duality: some `lambda,tau` exists for every true finite bound. The certificate itself, however, is consumed only by finite exact arithmetic plus the already-existing copositivity machinery.

The construction also transports exactly from physical state coordinates and annihilates every selector-gauge direction in `ker V`; no pseudoinverse or chosen selector representation appears.

No actual P5 source matrix, cell/tube identity, Float64 enclosure, trajectory coverage, Lean/kernel receipt, independent verification, admission, or registry promotion is claimed.

---

## 1. Setup and typed mathematical contract

Let

- `y in R^p` be the nonnegative selector coefficient vector;
- `C in R^(m x p)` and `d in R^m` encode a polyhedral consumed-domain constraint `Cy<=d`;
- `P=P^T in R^(p x p)` encode a quadratic consumed-domain constraint `y^T P y<=rho`;
- `b in R^p` be the signed support functional to bound;
- `B in R` be the proposed finite upper bound.

Define

`q(y):=y^T P y`,

and

`F_mix={y>=0 : Cy<=d, q(y)<=rho}`.

For the basic sufficient theorem, no sign assumption on `b` is required. In particular the intended T-P5-200 use is

`b=V^T h`,

which generally has mixed signs even when `h^T e` is a perfectly legitimate physical amplitude slope.

The domain semantics and the support certificate must remain typed separately:

1. source/domain layer: `y>=0`, `Cy<=d`, `q(y)<=rho` on the actually consumed cell/tube;
2. mathematical certificate layer: `lambda>=0`, `tau>=0`, augmented matrix copositivity;
3. Lyapunov consumer layer: feed the proved bound `b^T y<=B` into T-P5-200/T-P5-197.

The present review proves only layer 2 and its exact bridge to layer 3, conditional on layer 1.

---

## 2. T201-A — exact mixed-domain slack decomposition

Choose arbitrary multipliers

`lambda in R^m`, `tau in R`,

with

`lambda>=0`, `tau>=0`.

Set

`a=B-d^Tlambda-tau rho`,

`r=C^Tlambda-b`,

and

`M=[[a,r^T/2],[r/2,tau P]]`.

### Theorem A — augmented copositivity implies the mixed support bound

Assume `M` is copositive:

`z>=0 -> z^T M z>=0`.

Then

`y in F_mix -> b^T y<=B`.

### Proof

For any `y`, direct expansion gives

`[1;y]^T M [1;y]`

`=B-d^Tlambda-tau rho`

` +(C^Tlambda-b)^T y`

` +tau y^T P y`.

Add the two source-domain slack terms:

`lambda^T(d-Cy)+tau(rho-y^T P y)`.

Every multiplier-dependent term cancels exactly:

`[1;y]^T M [1;y]`

` +lambda^T(d-Cy)`

` +tau(rho-y^T P y)`

`=B-b^T y`.

Now let `y in F_mix`. Then `[1;y]>=0`, so the first term is nonnegative by copositivity. The second is nonnegative because `lambda>=0` and `d-Cy>=0`. The third is nonnegative because `tau>=0` and `rho-q(y)>=0`. Therefore

`B-b^T y>=0`.

QED.

### Important structural point

This is an **identity before any inequality is applied**. Consequently a future source packet can keep exact rational slacks and contact information instead of recording only the final inequality.

At a sharp contact `y_*` with `b^T y_*=B`, every term in the identity is nonnegative and their sum is zero. Hence necessarily

`[1;y_*]^T M [1;y_*]=0`,

`lambda_i(d_i-(Cy_*)_i)=0` for all `i`,

and

`tau(rho-q(y_*))=0`.

So a sharp mixed support packet automatically carries the expected complementarity/contact information without a separate KKT solve.

---

## 3. T201-B — homogenization theorem: augmented copositivity is exactly a global Lagrangian upper bound

Define the scalar quadratic polynomial on the selector orthant

`p(y):=B-d^Tlambda-tau rho+(C^Tlambda-b)^T y+tau y^T P y`.

Then

`p(y)=B-L_lambda,tau(y)`,

where

`L_lambda,tau(y)`

`:=b^T y+lambda^T(d-Cy)+tau(rho-y^T P y)`

is the ordinary upper Lagrangian for the two consumed-domain constraints, with `y>=0` kept as the base cone rather than dualized.

### Theorem B — exact homogenized equivalence

For `M` defined above,

`M copositive`

if and only if both

1. `tau P` is copositive on `y>=0`, and
2. `p(y)>=0` for every `y>=0`.

In particular, when `tau>=0` and `P` is copositive, condition 1 is automatic, and

**`M copositive <=> L_lambda,tau(y)<=B for all y>=0`.**

### Proof

If `M` is copositive, evaluate at `(1,y)` to obtain `p(y)>=0`, and at `(0,y)` to obtain

`tau y^T P y>=0`.

Conversely assume conditions 1 and 2. For arbitrary `(t,x)>=0`:

- if `t=0`, then `(0,x)^TM(0,x)=tau x^TPx>=0`;
- if `t>0`, put `y=x/t>=0`. Homogeneity gives

`[t;x]^T M[t;x]=t^2 p(x/t)>=0`.

Thus `M` is copositive.

QED.

### Checker consequence

The producer does not need to export an optimizer of `p`. It may export `lambda,tau` and a normal P5 copositivity certificate for the finite matrix `M`. The checker reconstructs `M` and consumes it with the same trusted cone machinery already required elsewhere.

---

## 4. T201-C — convex completeness under PSD + Slater

The previous theorem is already a sound checker branch for any symmetric `P`. Completeness needs an additional convexity qualification and should not be silently assumed for a merely copositive, possibly nonconvex quadratic domain.

Assume now

`P>=0` in the ordinary PSD sense,

and assume the mixed problem has a Slater point `y_bar` satisfying

`y_bar>0`,

`C y_bar<d`,

`y_bar^T P y_bar<rho`.

Let

`v_*:=sup {b^T y : y in F_mix}`

be finite.

### Theorem C — complete multiplier representation in the convex regime

For every `B>=v_*`, there exist

`lambda>=0`, `tau>=0`

such that the corresponding augmented matrix `M(lambda,tau,B)` is copositive.

Therefore, under PSD + Slater + finite support,

**`b^T y<=B on F_mix`**

is equivalent to

**existence of a mixed augmented-copositive packet.**

### Proof sketch with the exact dependency exposed

The feasible set is convex because `P>=0`. Keep `y>=0` as the base convex domain and dualize only `Cy<=d` and `q(y)<=rho`. Slater gives zero duality gap and dual attainment for the finite optimum. Hence there exist `lambda>=0`, `tau>=0` such that

`sup_{y>=0} L_lambda,tau(y)=v_*<=B`.

Equivalently `p(y)=B-L_lambda,tau(y)>=0` for every `y>=0`. Since `tau P>=0`, Theorem B gives copositivity of `M`.

No optimizer or duality theorem is needed by the eventual trusted arithmetic checker; the completeness statement only justifies why searching for this packet loses no mathematics in the convex source regime.

### Boundary

If the source has only `P` copositive but not PSD, this completeness implication is **not claimed**. The sufficient certificate in Theorem A remains sound, but failure to find `lambda,tau,M` is then only branch failure unless an independent negative/unbounded witness is available.

---

## 5. T201-D — pure-polyhedral T-P5-199 is recovered exactly at `tau=0`

Set `tau=0`. Then

`M=[[B-d^Tlambda,(C^Tlambda-b)^T/2],[(C^Tlambda-b)/2,0]]`.

### Theorem D

This matrix is copositive if and only if

`B-d^Tlambda>=0`

and

`C^Tlambda-b>=0` entrywise.

### Proof

The lifted quadratic is

`(B-d^Tlambda)t^2+t(C^Tlambda-b)^T y`.

Copositivity at `y=0` forces the scalar constant coefficient nonnegative. If any component of `C^Tlambda-b` were negative, fix `t>0` and send the corresponding nonnegative coordinate of `y` to infinity; the form becomes negative. Thus all components are nonnegative. The converse is immediate.

These are exactly the signed T-P5-199 LP-dual conditions

`lambda>=0`,

`C^Tlambda>=b`,

`d^Tlambda<=B`.

Hence T201 is a strict extension of the existing pure-polyhedral branch, not a parallel incompatible certificate language.

---

## 6. T201-E — exact composition with the pure-quadratic T-P5-198 gate

A particularly checker-friendly sufficient subbranch can reuse T-P5-198 without invoking generic augmented copositivity discovery.

Choose `lambda>=0` and define

`s:=b-C^Tlambda`,

`R:=B-d^Tlambda`.

Assume

`s>=0`, `R>=0`,

and the T-P5-198 rank-one matrix

`R^2 P-rho s s^T`

is copositive.

Then on `y>=0`, `y^TPy<=rho`, T-P5-198 gives

`s^T y<=R`.

On the mixed domain also `Cy<=d`, so

`b^Ty=lambda^T Cy+s^Ty`

`<=lambda^Td+R=B`.

Thus the pure quadratic gate may be applied **after** a polyhedral multiplier has removed part of the signed support slope.

### Embedding into T201

When `R>0`, set

`tau:=R/(2rho)`.

The T-P5-198 rank-one inequality implies

`R/2-s^Ty+(R/(2rho))y^TPy>=0`

for every `y>=0`. A root-free verification is obtained from

`R^2 y^TPy>=rho(s^Ty)^2`

by observing

`[R(rho+q)]^2-[2rho s]^2`

`=R^2(rho-q)^2+4rho[R^2 q-rho s^2]>=0`,

where `q=y^TPy`, and both compared sides are nonnegative because `R,s,y,rho>=0`.

This scalar polynomial is exactly the T201 polynomial `p(y)` for the chosen `lambda,tau`. Hence Theorem B gives the corresponding augmented copositive matrix.

If `R=0`, T-P5-198 forces `s=0` under `s>=0`; choosing `tau=0` reduces to the pure-polyhedral packet.

### Why the general T201 packet is stronger

This compositional subbranch requires `s=b-C^Tlambda>=0`. The general augmented packet does **not**. It can preserve negative components of the residual slope and let the quadratic term absorb them exactly. This is the mixed-domain analogue of T-P5-200's instruction not to destroy signed physical cancellation by premature componentwise majorization.

---

## 7. T201-F — exact physical-coordinate pullback and selector-gauge invariance

Suppose the source-domain data are stored physically as

`e=V y`, `y>=0`,

`A e<=d`,

`e^T W e<=rho`,

and the support functional is the physical scalar

`h^T e<=B`.

Define the exact pullbacks

`C:=A V`,

`P:=V^T W V`,

`b:=V^T h`.

For fixed `lambda,tau`, define the physical lifted symmetric matrix

`M_phys := [[a,(A^Tlambda-h)^T/2],[(A^Tlambda-h)/2,tau W]]`,

with the same

`a=B-d^Tlambda-tau rho`.

Let

`T:=diag(1,V)`.

### Theorem F1 — exact congruence transport

**`M_selector = T^T M_phys T`.**

This is a literal matrix identity. No inverse of `V` is used.

Consequently for every selector state `y`,

`[1;y]^T M_selector [1;y]`

`=[1;Vy]^T M_phys [1;Vy]`.

Thus the augmented remainder depends only on the physical state represented by `y` whenever all three pullbacks are source-bound from the same `A,W,h,V` packet.

### Theorem F2 — every representation gauge lies in the lifted kernel

If

`r_g in ker V`,

then

`C r_g=0`,

`P r_g=0`,

`b^T r_g=0`,

and

`(C^Tlambda-b)^T r_g=0`.

Therefore

**`M_selector [0;r_g]=0`.**

In particular, a nonnegative gauge ray `r_g>=0`, `Vr_g=0` cannot create the coefficient-space blowup that obstructed a nonnegative majorant in T-P5-199. The mixed exact physical packet is quotient-compatible automatically.

### Typed warning

The equality `P=V^T W V` and the support pullback `b=V^T h` must be actual same-key source equalities. A numerically similar selector quadratic and a separately fitted support slope do not inherit this gauge theorem.

---

## 8. T201-G — exact zero-cost recession obstruction

The sound PASS packet above should be paired with a genuine FAIL witness rather than treating solver/search failure as mathematical failure.

Assume there exist

`y0 in F_mix`,

`r>=0`, `r!=0`,

such that

`C r<=0`,

`P r=0`,

and

`b^T r>0`.

### Theorem G1 — no finite mixed support bound exists

For every `t>=0`,

`y_t:=y0+t r>=0`,

and

`C y_t=Cy0+tCr<=d`.

Because `Pr=0` and `P=P^T`,

`q(y_t)=q(y0)+2t y0^TPr+t^2 r^TPr=q(y0)<=rho`.

Thus every `y_t` remains in `F_mix`, while

`b^T y_t=b^T y0+t b^T r -> +infinity`.

Hence no finite `B` can bound `b^T y` on the mixed domain.

### Theorem G2 — the same ray defeats every proposed T201 packet

For arbitrary `lambda>=0`, `tau>=0`, write the cross slope of the augmented matrix as

`r_M:=C^Tlambda-b`.

Then

`r_M^T r=lambda^T C r-b^T r<0`.

Since `Pr=0`, along the lifted orthant ray `(1,s r)` we obtain

`[1;sr]^T M[1;sr]`

`=a+s r_M^T r`,

which tends to `-infinity` as `s->infinity`.

Therefore **no** augmented matrix of the T201 multiplier form can be copositive.

This is a real domain/support obstruction, not a failure of a particular multiplier search.

### Boundary

The condition `Pr=0` is deliberately exact and checker-friendly. This review does not claim that every unbounded mixed support problem admits such a ray when `P` is merely copositive/nonconvex. In the PSD convex regime, standard recession analysis can sharpen this characterization, but that strengthening is not needed for the present bridge.

---

## 9. Exact rational regression — the intersection is strictly sharper than either pure route

Take

`y=(y1,y2)>=0`,

`P=I_2`, `rho=1`,

one polyhedral row

`C=[1,0]`, `d=3/5`,

and target support

`b=(1,1)`.

The mixed domain is

`y1>=0`, `y2>=0`,

`y1<=3/5`,

`y1^2+y2^2<=1`.

The point

`y_*=(3/5,4/5)`

is feasible and has

`b^T y_*=7/5`.

We show that `B=7/5` is certified exactly by T201 while neither pure branch alone proves this same sharp bound.

### Pure polyhedral branch fails to give a finite bound

If the quadratic constraint is discarded, `y2` is unbounded above. Hence T-P5-199 alone cannot certify any finite bound on `y1+y2` from `y1<=3/5`.

### Pure quadratic T-P5-198 branch rejects `B=7/5`

If the linear constraint is discarded, T-P5-198 would require

`B^2 I_2-bb^T`

to be copositive. Evaluate at `y=(1,1)`:

`y^T(B^2 I_2-bb^T)y`

`=2*(49/25)-4`

`=-2/25<0`.

Thus the pure quadratic domain also does not prove `B=7/5`.

### Mixed T201 packet closes exactly

Choose

`lambda=1/4`,

`tau=5/8`.

Then

`d lambda=3/20`,

`tau rho=5/8`,

and

`a=B-dlambda-taurho`

`=7/5-3/20-5/8`

`=5/8`.

Also

`r=C^Tlambda-b=(-3/4,-1)`.

Hence

`M=`

`[[5/8, -3/8, -1/2],`

` [-3/8, 5/8, 0],`

` [-1/2, 0, 5/8]]`.

For every lifted vector `(t,y1,y2)`, its quadratic form is

**`[t;y]^T M[t;y]`**

**`=(5/8)[(y1-(3/5)t)^2+(y2-(4/5)t)^2] >=0`.**

So `M` is actually PSD, hence certainly copositive.

Theorem A yields

`y1+y2<=7/5`

on the intersection.

At `y_*=(3/5,4/5)`, the augmented-square term vanishes, the polyhedral slack vanishes, and the quadratic slack vanishes. Therefore the exact-gap identity gives equality. Since `y_*` itself attains `7/5`, the bound is sharp.

This regression proves that the mixed packet is not just notation for choosing the better of T-P5-198 and T-P5-199. Simultaneously using both constraints can certify a strictly tighter support.

---

## 10. Relation to the T-P5-200 affine-amplitude Lyapunov branch

Suppose T-P5-200 has a genuine physical affine amplitude

`a(e)=h0+h^T e`,

with exact selector pullback

`b=V^T h`,

and a fixed-sign projected quadratic packet

`|phi(Vy)|=c^T y+y^TQy`,

`c>=0`, `Q` copositive.

T-P5-200 needs only a same-domain scalar support

`b^T y<=B`.

T201 supplies that support directly from a mixed domain via the augmented packet. Then the existing T-P5-200 identity applies unchanged:

`(h0+b^Ty)(c^Ty+y^TQy)`

`<=h0 c^Ty+y^T[(h0+B)Q+sym(bc^T)]y`.

Thus the full route is

**mixed physical cell**

`-> exact pullbacks C=AV, P=V^TWV, b=V^Th`

`-> T201 augmented support packet`

`-> scalar bound b^Ty<=B`

`-> T200 signed cubic absorption`

`-> existing T192 linear + copositivity Lyapunov checker`.

No nonnegative selector majorant is required at any point on this exact branch.

---

## 11. Minimal theorem statements for formalization

The algebraic leaves can be separated from any strong-duality theorem.

### T201-1 `mixedSupport_gap_identity`

For the definitions above,

`B-b^Ty`

`=[1;y]^TM[1;y]+lambda^T(d-Cy)+tau(rho-y^TPy)`.

This is a ring identity.

### T201-2 `mixedSupport_of_augmentedCopositive`

Assume

`y>=0`, `Cy<=d`, `y^TPy<=rho`,

`lambda>=0`, `tau>=0`,

and `M` copositive.

Then

`b^Ty<=B`.

### T201-3 `augmentedCopositive_iff_globalLagrangianBound`

Assume `tau P` copositive. Then

`M copositive`

iff

`forall y>=0, B-d^Tlambda-tau rho+(C^Tlambda-b)^Ty+tau y^TPy>=0`.

### T201-4 `tauZero_augmentedCopositive_iff_polyhedralDual`

At `tau=0`, copositivity is equivalent to

`B>=d^Tlambda` and `C^Tlambda>=b`.

### T201-5 `quadraticRankOneCap_to_augmented`

Under T-P5-198 premises, if

`R>0`, `s>=0`,

`R^2P-rho ss^T` copositive,

then with `tau=R/(2rho)`,

`[[R/2,-s^T/2],[-s/2,tau P]]`

is copositive.

The `R=0` branch should be a separate trivial lemma.

### T201-6 `physicalAugmented_pullback`

For `C=AV`, `P=V^TWV`, `b=V^Th`,

`M_selector=diag(1,V)^T M_phys diag(1,V)`.

### T201-7 `selectorGauge_mem_augmentedKernel`

If `Vr=0`, then

`M_selector [0;r]=0`.

### T201-8 `mixedZeroCostRecession_unboundedSupport`

If a feasible `y0` and `r>=0` satisfy

`Cr<=0`, `Pr=0`, `b^Tr>0`,

then for every finite `B` there exists a feasible `y` with `b^Ty>B`.

The convex completeness theorem may be formalized later behind an explicit finite-dimensional Slater/strong-duality dependency. It is not necessary for a sound PASS checker.

---

## 12. Suggested checker/source packet

A mixed-domain support certificate should keep the following fields distinct:

- `selector_state_nonnegative : y>=0` (domain semantics, not packet data);
- `polyhedral_matrix : C`;
- `polyhedral_rhs : d`;
- `quadratic_matrix : P`;
- `quadratic_radius : rho`;
- `support_slope : b`;
- `support_bound : B`;
- `linear_multiplier : lambda`;
- `quadratic_multiplier : tau`;
- `linear_multiplier_nonnegative : lambda>=0`;
- `quadratic_multiplier_nonnegative : tau>=0`;
- reconstructed `augmented_scalar : B-d^Tlambda-tau rho`;
- reconstructed `augmented_cross : C^Tlambda-b`;
- reconstructed `augmented_matrix : M`;
- `augmented_copositive_certificate` using the existing P5 cone dispatcher.

For a physical source adapter additionally retain exact equalities

- `C=A V`;
- `P=V^T W V`;
- `b=V^T h`;
- one `same_consumed_domain` identity tying `A,W,rho,h,V` to the same cell/tube key.

Do not store a pseudoinverse of `V`; it is irrelevant to the theorem and would make the packet representation-dependent.

---

## 13. Fail-closed routing rules

### PASS_MIXED_AUGMENTED_COPOSITIVE

If the same consumed domain proves

`y>=0`, `Cy<=d`, `y^TPy<=rho`,

and a packet provides `lambda>=0`, `tau>=0` with reconstructed augmented matrix `M` certified copositive, accept `b^Ty<=B` and pass the scalar support bound to T-P5-200/T-P5-197.

### PASS_COMPOSED_T198_AFTER_LINEAR_DUAL

If a `lambda` leaves a nonnegative residual slope `s=b-C^Tlambda>=0`, reuse the T-P5-198 rank-one copositivity gate on `s` and residual budget `R=B-d^Tlambda`. This is a convenient sufficient subbranch.

### MIXED_PACKET_NOT_FOUND

Failure to find `lambda,tau` is **not** a source/math FAIL in a nonconvex merely-copositive quadratic regime. Keep the branch unresolved or use another exact support method.

Under PSD + Slater, the existence theorem says a true finite bound has some packet, but a computational search can still be incomplete if the copositivity solver is incomplete; do not conflate theorem completeness with implementation completeness.

### FAIL_ZERO_COST_RECESSION

A same-domain witness

`y0 feasible`, `r>=0`, `Cr<=0`, `Pr=0`, `b^Tr>0`

is a genuine mathematical obstruction to any finite support bound and may be reported as such.

### GAUGE_RAY_IS_NOT_PHYSICAL_RECESSION

If `r>=0` and `Vr=0` under exact physical pullbacks, then `Cr=Pr=b^Tr=0`. This is a harmless representation gauge and must not be reported as physical support unboundedness.

### SOURCE_KEY_MISMATCH

A polyhedral cell from one source key and a quadratic cap from another cannot be intersected merely because their dimensions agree. The exact-gap theorem is conditional on both constraints holding simultaneously on the same consumed state set.

---

## 14. Boundaries that remain OPEN

This review does **not** prove:

1. that the actual P5 consumed cell/tube is an intersection of the declared polyhedral and quadratic domains;
2. any actual numerical `A,V,W,C,P,d,rho,h,b,B` source binding;
3. nonemptiness, trajectory inclusion, or global coverage of the mixed cell;
4. that an actual generator amplitude is exactly the T-P5-200 physical affine scalar;
5. copositivity of any actual instantiated augmented matrix;
6. completeness for a non-PSD merely-copositive `P`;
7. implementation completeness of the generic copositivity dispatcher;
8. Float64/directed-rounding/controller/PDE/ODE semantic validity;
9. P8/M4/global Route-B closure;
10. Lean/kernel compilation or axiom/placeholder checks;
11. independent verification by 封不觉;
12. admission or registry eligibility.

All remain OPEN.

---

## 15. Recommended integration/routing consequence

Insert one mixed-domain branch between source-domain extraction and T-P5-200's scalar support consumer:

1. preserve exact physical state-domain constraints rather than choosing either the polyhedral or quadratic envelope prematurely;
2. pull them to selector coordinates by `C=AV`, `P=V^TWV`, and pull the physical slope by `b=V^Th`;
3. search for nonnegative `lambda,tau` and certify the reconstructed augmented matrix copositive;
4. recover `b^Ty<=B` from the exact three-slack identity;
5. feed `B` directly to the signed T-P5-200 absorption theorem;
6. if a zero-cost recession witness appears, report the precise unbounded-support obstruction;
7. otherwise keep failure to find a packet as unresolved, not as source FAIL.

This bridge composes T-P5-198 and T-P5-199, preserves the gauge-invariant signed geometry highlighted by T-P5-200, and proves on an exact rational example that the intersection can close a sharp bound which neither pure domain description can certify alone.