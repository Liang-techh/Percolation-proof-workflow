---
kind: review_result
review_id: review-T-P5-202-psd-mixed-domain-recession-polar-gate-kuangmanmozun-20260910T0131Z
task_id: T-P5-202-PSD-MIXED-DOMAIN-RECESSION-POLAR-GATE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T01:31:00Z
claim_commit: fe68a10181738b3b01ca2475d3ecf873f43940c9
inspected_commit: 68fa17749cb25678e126aa7927def3cd59dfaaf3
upstream_commits:
  - 04872637e1d211b2e91bb7be8bce2894ba043624  # T-P5-199 polyhedral selector LP-dual transport
  - 12a92536fc8371342e54845225a423ad33323407  # T-P5-200 gauge-invariant signed amplitude absorption
  - 269f249537b6bd41557c1287022bb507d78f2a1b  # T-P5-201 mixed-domain augmented copositive support
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_psd_mixed_recession_exact_characterization; add_linear_polar_finiteness_precheck; add_constructive_rational_augmented_packet; preserve_nonpsd_fallback
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact recession-cone derivation; cone-polar/Farkas alternative; PSD Young completion; rational PASS/FAIL regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-202 — PSD mixed-domain recession/polar gate and constructive rational support packet

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-201 gives an exact mixed-domain support certificate for

`F = { y >= 0 : C y <= d, y^T P y <= rho }`

through nonnegative multipliers `lambda,tau` and copositivity of one lifted matrix. It also records one sufficient unbounded-support witness

`r >= 0, C r <= 0, P r = 0, b^T r > 0`.

The remaining mathematical seam is to decide whether this ray condition is merely a useful obstruction or the exact recession test in the convex PSD regime, and whether support finiteness can be screened before invoking a generic copositivity search.

This child proves both points.

Assume throughout this review that

`P = P^T >= 0`

in the ordinary PSD sense and that `F` is nonempty.

Then the exact recession cone is

**`rec(F) = { r >= 0 : C r <= 0, P r = 0 }`.**

Consequently a linear support `b^T y` is bounded above on `F` iff there is no ray in this cone with positive `b`-slope. By the finite-dimensional cone-polar/Farkas alternative, this is equivalent to the existence of

`lambda >= 0`, `nu in R^p`

such that

**`alpha := C^T lambda + P nu - b >= 0`**

entrywise.

This is a purely linear feasibility gate: no quadratic optimizer, no pseudoinverse, and no generic copositivity search are needed merely to decide whether a finite support bound exists.

More strongly, from any such polar witness and any scalar `tau > 0`, define

**`B_tau := d^T lambda + tau rho + (nu^T P nu)/(4 tau)`.**

Then every `y in F` satisfies

**`b^T y <= B_tau`.**

The corresponding T-P5-201 augmented matrix is automatically copositive by an explicit PSD-square plus nonnegative-cross decomposition. Thus the PSD branch admits a root-free, rational, constructive PASS packet whenever the linear polar gate succeeds.

This strengthens T-P5-201 only at the level of **existence of some finite bound**. It does not claim that `B_tau` is the sharp support value, nor does it remove T-P5-201's sharper prescribed-`B`/strong-duality route when a tight constant is required.

No actual P5 source matrices, cell/tube identity, nonemptiness/coverage receipt, Float64 enclosure, Lean/kernel proof, independent verification, admission, or registry promotion are claimed.

---

## 1. Setup

Let

- `P=P^T in R^(p x p)` be PSD;
- `C in R^(m x p)`;
- `d in R^m`;
- `rho in R`;
- `b in R^p`.

Define

`F := { y in R^p : y>=0, C y<=d, y^T P y<=rho }`.

Assume `F` is nonempty.

The relevant support problem is

`sup { b^T y : y in F }`.

The intended T-P5-200 application is `b=V^T h`, but no selector-map assumption is needed for the mathematics below.

---

## 2. T202-A — PSD null quadratic implies actual kernel membership

### Lemma

If `P=P^T>=0` and

`r^T P r = 0`,

then

**`P r = 0`.**

### Elementary proof without spectral decomposition

For any `x` and real `t`, PSD gives

`0 <= (r+t x)^T P (r+t x)`

`= 2 t x^T P r + t^2 x^T P x`,

because `r^TPr=0`.

If `x^TPr != 0`, choosing `t` with sufficiently small magnitude and opposite sign makes the linear term dominate the quadratic term and gives a negative value, contradiction.

Therefore `x^TPr=0` for every `x`, hence `Pr=0`.

This lemma is the exact place where ordinary PSD enters the recession theorem.

---

## 3. T202-B — exact recession cone of the mixed PSD domain

### Theorem

Assume `F` is nonempty and `P>=0`. Then

**`rec(F) = K := { r : r>=0, C r<=0, P r=0 }`.**

Here `r in rec(F)` means

`y+t r in F`

for every `y in F` and every `t>=0`.

### Proof: `K subset rec(F)`

Take `r>=0`, `Cr<=0`, `Pr=0`, and any `y in F`.

For `t>=0`:

1. `y+t r>=0`;
2. `C(y+t r)=Cy+t Cr<=d`;
3. because `Pr=0`,

   `(y+t r)^T P(y+t r)`

   `= y^TPy + 2t y^TPr + t^2 r^TPr`

   `= y^TPy <= rho`.

Hence `y+t r in F`, so `r in rec(F)`.

### Proof: `rec(F) subset K`

Take `r in rec(F)` and choose one `y0 in F`.

Since `y0+t r>=0` for all `t>=0`, every coordinate of `r` must be nonnegative.

Since

`C y0 + t C r <= d`

for all `t>=0`, every row must satisfy `Cr<=0`.

Finally

`q(t):=(y0+t r)^T P(y0+t r)`

`=y0^TPy0 + 2t y0^TPr + t^2 r^TPr`

is bounded above by `rho` for every `t>=0`.

PSD gives `r^TPr>=0`. If `r^TPr>0`, the `t^2` term drives `q(t)` to `+infinity`, contradiction. Hence `r^TPr=0`, and T202-A gives `Pr=0`.

Therefore `r in K`.

QED.

### Structural consequence

T-P5-201's zero-cost ray test is not merely sufficient in the PSD branch. Its conditions are exactly the recession directions of the consumed mixed domain.

---

## 4. T202-C — exact support-finiteness criterion

### Theorem

Under the same assumptions, the following are equivalent:

1. `sup_{y in F} b^T y < +infinity`;
2. every `r>=0` with `Cr<=0` and `Pr=0` satisfies `b^Tr<=0`;
3. there exist `lambda>=0` and `nu in R^p` such that

   **`C^T lambda + P nu - b >= 0`**

   entrywise.

### `1 -> 2`

If some `r in K` had `b^Tr>0`, choose any `y0 in F`. T202-B gives

`y0+t r in F`

for all `t>=0`, while

`b^T(y0+t r)=b^Ty0+t b^Tr -> +infinity`,

contradicting finite support.

### `2 <-> 3`: cone polar / Farkas form

Let

`K={r>=0, Cr<=0, Pr=0}`.

Its negative polar is

`K^circ={b : b^Tr<=0 for all r in K}`.

The constraints defining `K` are linear. Standard finite-dimensional Farkas duality gives

`K^circ`

`={C^Tlambda + Pnu - alpha : lambda>=0, alpha>=0, nu arbitrary}`.

Thus `b in K^circ` iff there are `lambda>=0`, `nu` such that

`alpha=C^Tlambda+Pnu-b>=0`.

### `3 -> 1`: constructive proof

This direction is proved quantitatively in T202-D below and does not require any abstract support theorem.

---

## 5. T202-D — constructive rational support bound

Assume

`lambda>=0`

and

`alpha:=C^Tlambda+Pnu-b>=0`.

Then

`b=C^Tlambda+Pnu-alpha`.

For every `y in F`, because `y>=0`, `alpha>=0`, `lambda>=0`, and `Cy<=d`,

`b^Ty`

`=lambda^T Cy + nu^T P y - alpha^T y`

`<=lambda^T d + nu^T P y`.

Fix any `tau>0`.

PSD of `P` gives the exact square inequality

`0 <= (2 tau y - nu)^T P (2 tau y - nu)`

`=4 tau^2 y^TPy - 4 tau nu^T P y + nu^T P nu`.

Therefore

`nu^T P y <= tau y^TPy + (nu^TPnu)/(4 tau)`

`<= tau rho + (nu^TPnu)/(4 tau)`.

Hence

**`b^T y <= B_tau`**

with

**`B_tau = d^Tlambda + tau rho + (nu^TPnu)/(4 tau)`.**

This is an ordinary exact-real inequality requiring only PSD, linear signs, and scalar positivity.

### Rational certificate consequence

If `C,P,d,b,rho` are rational and the linear polar system is feasible, it has a rational feasible point `(lambda,nu)` because it is a rational polyhedral feasibility problem. Choosing any rational `tau>0` produces a fully rational `B_tau`.

Thus the PSD branch can always produce a finite rational support cap without square roots whenever finite support is possible.

The scalar `tau` may later be optimized or simply chosen from a small rational search grid. Tightness is a design issue, not a soundness issue.

---

## 6. T202-E — explicit construction of the T-P5-201 augmented copositive packet

Recall the T-P5-201 augmented matrix

`M(lambda,tau,B)`

`=[[B-d^Tlambda-tau rho, (C^Tlambda-b)^T/2],`

`  [(C^Tlambda-b)/2, tau P]]`.

Take the polar witness from T202-C/D and choose

`B=B_tau=d^Tlambda+tau rho+(nu^TPnu)/(4tau)`.

Then

`B-d^Tlambda-tau rho=(nu^TPnu)/(4tau)`,

and

`C^Tlambda-b=alpha-Pnu`.

For any lifted orthant vector `(t,y)>=0`, direct expansion gives

`[t;y]^T M [t;y]`

`=(nu^TPnu)/(4tau) t^2`

` + t(alpha-Pnu)^T y`

` + tau y^TPy`.

Regroup:

**`[t;y]^T M [t;y]`**

**`= (1/(4tau)) (2tau y-t nu)^T P (2tau y-t nu)`**

**`  + t alpha^T y`.**

Both terms are nonnegative because

`P>=0`, `tau>0`, `t>=0`, `alpha>=0`, `y>=0`.

Therefore

**`M(lambda,tau,B_tau)` is copositive.**

### Important checker consequence

In this PSD subbranch, a generic copositivity dispatcher is unnecessary after the linear polar witness has been found. The checker can validate the explicit decomposition:

1. verify `P>=0` by its existing PSD certificate;
2. verify `lambda>=0`;
3. reconstruct `alpha=C^Tlambda+Pnu-b` and verify `alpha>=0`;
4. verify `tau>0`;
5. reconstruct `B_tau`;
6. optionally reconstruct the augmented matrix and check the identity above.

The lifted matrix is certified by a PSD square plus an entrywise-nonnegative orthant cross term.

This is stronger computationally than asking a generic copositivity solver to rediscover the same structure.

---

## 7. T202-F — exact theorem of alternatives for a fail-closed pre-screen

Because the recession system is homogeneous, a positive support ray can be normalized.

If

`r>=0`, `Cr<=0`, `Pr=0`, `b^Tr>0`,

then after rescaling one may impose

**`b^Tr>=1`.**

Therefore the PSD mixed-domain branch admits an exact rational linear alternative:

### FINITE side

Find

`lambda>=0`, `nu`

with

`C^Tlambda+Pnu-b>=0`.

Then construct `B_tau` by T202-D.

### UNBOUNDED side

Find

`r>=0`, `Cr<=0`, `Pr=0`, `b^Tr>=1`.

Then any nonempty `F` has

`sup_F b^Ty=+infinity`.

These two systems cannot both be feasible:

if the FINITE witness holds and `r` satisfies the ray constraints, then

`b^Tr`

`<=lambda^T Cr + nu^TPr`

`<=0`,

contradicting `b^Tr>=1`.

Finite-dimensional Farkas duality says one of the two alternatives holds.

Thus in the PSD regime, `MIXED_PACKET_NOT_FOUND` can be refined substantially:

- if the UNBOUNDED ray LP succeeds, report a genuine mathematical obstruction;
- if the FINITE polar LP succeeds, a rational support packet exists constructively;
- only solver/integration/source failures remain unresolved.

---

## 8. Sharp rational regression: unbounded selector set but exact finite support

Take

`P = [[1,0],[0,0]]`,

`rho=1`,

no additional `C y<=d` rows,

and

`b=(1,-1)`.

Then

`F={y1>=0,y2>=0 : y1^2<=1}`.

The set is unbounded because `y2` is free in the positive direction, but

`b^Ty=y1-y2<=1`.

The exact support is `1`, attained at `(1,0)`.

Choose

`nu=(1,0)`,

`lambda` empty,

so

`Pnu-b=(1,0)-(1,-1)=(0,1)=alpha>=0`.

Choose

`tau=1/2`.

Then

`nu^TPnu=1`,

and T202-D gives

`B_tau=(1/2)*1 + 1/(4*(1/2))=1`.

So the constructive bound is sharp in this regression.

The lifted augmented matrix is

`M = [[1/2,-1/2,1/2],`

`     [-1/2,1/2,0],`

`     [1/2,0,0]]`.

For `(t,y1,y2)>=0`,

`[t;y]^T M[t;y]`

`= (1/2)(t-y1)^2 + t y2 >=0`.

This exhibits explicitly how an unbounded coefficient direction can be harmless for a signed support functional.

---

## 9. Exact unbounded regression

Keep

`P=diag(1,0)`, `rho=1`,

but take

`b=(0,1)`.

Then

`r=(0,1)`

satisfies

`r>=0`, `Pr=0`, and `b^Tr=1`.

Hence the support is unbounded:

`b^T(0,t)=t -> +infinity`.

The polar system correctly has no solution because the second coordinate of `Pnu` is always zero, so

`Pnu-b`

has second coordinate `-1` and cannot be entrywise nonnegative.

This is a minimal PASS/FAIL regression pair for the future checker.

---

## 10. Decisive boundary: PSD cannot be weakened to mere copositivity

Consider

`P = [[1,-1,1],`

`     [-1,1,1],`

`     [1,1,0]]`.

For `y>=0`,

`y^TPy=(y1-y2)^2+2y3(y1+y2)>=0`,

so `P` is copositive.

But it is not PSD; for example

`x=(1,1,-1)`

gives

`x^TPx=-4`.

Take `rho=0` and no polyhedral rows. Then

`r=(1,1,0)>=0`

satisfies

`r^TPr=0`,

and every `t r` remains feasible because

`(tr)^T P(tr)=0`.

Thus `r` is a genuine recession direction.

However

`Pr=(0,0,2) != 0`.

In fact this `P` is nonsingular, so `ker(P)={0}`. A checker that replaced the true non-PSD recession analysis by the PSD condition `Pr=0` would miss the ray completely.

Taking

`b=(1,1,0)`

makes

`b^Tr=2>0`,

so the support is genuinely unbounded even though the false `ker(P)` recession test sees no nonzero ray.

Therefore:

**ordinary PSD is an essential gate for T202-B through T202-F.**

If `P` is only copositive, failure of the PSD gate must route back to T-P5-201's general copositive/semialgebraic branch. It is not a mathematical FAIL by itself.

---

## 11. Relation to T-P5-199, T-P5-200, and T-P5-201

### T-P5-199

T-P5-199 handles a purely polyhedral bound by LP duality. T202 shows that after adding a PSD quadratic cap, the **finiteness** question is still reducible to one linear polar system because the only quadratic recession directions are exactly `ker(P)`.

### T-P5-200

T-P5-200 wants a finite signed physical support bound `b^Ty<=B` to absorb an affine-amplitude cubic defect. T202 supplies such a rational `B` whenever the mixed PSD domain has no positive `b` recession ray.

Because `b` may be signed, this remains compatible with T-P5-200's gauge-preserving route and does not require replacing `b` by a nonnegative selector majorant.

### T-P5-201

T-P5-201 supplies the general augmented-copositive certificate and discusses completeness under PSD + Slater for a prescribed finite support bound.

T202 adds two narrower facts:

1. for deciding **whether any finite bound exists**, PSD + nonempty domain is enough; no Slater condition is needed;
2. once the linear polar witness exists, one can construct a rational `B_tau` whose augmented matrix has an explicit copositive decomposition, so a generic copositivity search is unnecessary for this nonsharp existence branch.

T202 does **not** prove that a requested/sharp `B` admits the same square-form packet. If the downstream Lyapunov budget needs a tighter constant than the constructive `B_tau`, retain the full T-P5-201 optimization/strong-duality route.

---

## 12. Suggested checker routing

For an actual same-source mixed packet with `P` certified PSD:

1. prove the consumed domain is nonempty;
2. solve the rational UNBOUNDED ray LP

   `r>=0, Cr<=0, Pr=0, b^Tr>=1`;

3. if feasible, return `FAIL_POSITIVE_RECESSION_SUPPORT_UNBOUNDED` with the exact ray;
4. otherwise solve the dual polar LP

   `lambda>=0, C^Tlambda+Pnu-b>=0`;

5. choose rational `tau>0` and form

   `B_tau=d^Tlambda+tau rho+(nu^TPnu)/(4tau)`;

6. validate the exact PSD-square identity from T202-E;
7. feed `B_tau` to T-P5-200;
8. if `B_tau` is too loose for final Lyapunov closure, use it only as a finiteness witness and continue to T-P5-201 for a sharper mixed-domain support certificate.

This ordering distinguishes three logically different events that were previously easy to conflate:

- true support unboundedness;
- finite support with an easy nonsharp rational cap;
- finite support whose useful sharp constant still requires the stronger augmented optimization.

---

## 13. Suggested formal theorem statements

### T202-1 `psd_quad_eq_zero_implies_mulVec_eq_zero`

For symmetric PSD `P`,

`r^T P r=0 -> P r=0`.

### T202-2 `mixedPSD_recession_iff`

For nonempty

`F={y>=0 : Cy<=d, y^TPy<=rho}`

with `P>=0`,

`r in rec(F) <-> r>=0 and Cr<=0 and Pr=0`.

### T202-3 `mixedPSD_support_polar_iff`

Under the same assumptions,

`sup_F b^Ty < +infinity`

iff there exist `lambda>=0`, `nu` with

`C^Tlambda+Pnu-b>=0`.

The reverse direction may be stated constructively via T202-4 rather than through extended-real support APIs.

### T202-4 `mixedPSD_polar_constructive_bound`

If

`lambda>=0`,

`alpha=C^Tlambda+Pnu-b>=0`,

`tau>0`,

then every `y in F` satisfies

`b^Ty <= d^Tlambda+tau rho+(nu^TPnu)/(4tau)`.

### T202-5 `mixedPSD_constructed_augmented_copositive`

With `B_tau` above, the T-P5-201 augmented matrix is copositive, witnessed by

`[t;y]^T M[t;y]`

`=(1/(4tau))(2tau y-t nu)^T P(2tau y-t nu)+t alpha^T y`.

### T202-6 `mixedPSD_positive_recession_unbounded`

If `F` is nonempty and

`r>=0`, `Cr<=0`, `Pr=0`, `b^Tr>0`,

then for every real `B` there exists `y in F` with `b^Ty>B`.

---

## 14. Fail-closed labels

### `PASS_PSD_MIXED_POLAR_FINITE_SUPPORT`

PSD, nonempty same-domain semantics, and a valid polar witness are present. A rational finite bound `B_tau` may be constructed.

### `FAIL_PSD_MIXED_POSITIVE_RECESSION`

A same-domain exact ray satisfies

`r>=0`, `Cr<=0`, `Pr=0`, `b^Tr>=1`.

This is a genuine mathematical obstruction to any finite support cap.

### `PSD_MIXED_POLAR_BOUND_TOO_LOOSE`

A finite constructive bound exists but does not leave enough downstream Lyapunov margin. This is not support unboundedness; route to the sharper T-P5-201 mixed optimization.

### `PSD_GATE_NOT_APPLICABLE`

`P` is not certified ordinary PSD. Do not use `Pr=0` as the recession characterization. Route to the general copositive/nonconvex branch.

### `MIXED_DOMAIN_NONEMPTY_NOT_PROVEN`

The theorem of support finiteness is not consumed until the actual same-key mixed domain is known nonempty. An empty nominal packet must not be turned into a physical PASS.

---

## 15. Boundaries remaining OPEN

This review does not prove:

1. that any actual P5 quadratic matrix `P` is PSD on the consumed selector packet;
2. that actual `C,P,d,rho,b` come from one source/cell/tube key;
3. actual nonemptiness or trajectory/domain coverage;
4. a sharp support value for the real P5 packet;
5. usefulness of the nonsharp `B_tau` for the final decay margin;
6. Float64 or directed-rounding semantics;
7. controller/PDE/ODE/source-evaluator correctness;
8. Lean/kernel compilation or axiom checks;
9. independent verification by 封不觉;
10. admission, registry, P5/P8/M4, or global Route-B closure.

All remain open.

---

## 16. Next mathematical seam

After T202, the next useful inequality question is no longer “is the support finite?” in the PSD branch. That question has a linear exact alternative.

The remaining quantitative bottleneck is **how tight a rational cap must be for the downstream cubic absorption**.

A natural next child is to optimize the constructive family

`B_tau(lambda,nu)=d^Tlambda+tau rho+(nu^TPnu)/(4tau)`

over polar witnesses while preserving rational certificates, and compare that value with the full T-P5-201 augmented optimum. If a simple active-set or Schur reduction closes the gap, the generic copositivity solver can be bypassed on a much larger PSD corridor; if not, an explicit gap example will identify where the stronger mixed packet is genuinely necessary.
