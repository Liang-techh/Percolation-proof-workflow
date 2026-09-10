---
kind: review_result
review_id: review-T-P5-203-psd-sharp-polar-schur-dual-honglianmozun-20260910T0148Z
task_id: T-P5-203-PSD-SHARP-POLAR-SCHUR-DUAL
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T01:48:00Z
claim_commit: 548b5bd37c3cddacce7220a5922411e6bfa6e339
inspected_commit: 039f1bc768f35a4285fae56fe36de976b7a4c266
upstream_commits:
  - 12a92536fc8371342e54845225a423ad33323407  # T-P5-200 gauge-invariant affine-amplitude cubic absorption
  - 269f249537b6bd41557c1287022bb507d78f2a1b  # T-P5-201 mixed-domain augmented copositive support
  - f7b0684409c15797d12d7b92496ac0dfc124809f  # T-P5-202 PSD mixed-domain recession/polar gate
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_psd_sharp_reduced_dual; add_root_free_prescribed_bound_packet; add_rational_strict_margin_completeness; bypass_generic_copositive_search_on_psd_slater_corridor
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact PSD Cauchy-Schwarz derivation; orthant quadratic KKT/Schur completion; scalar tau minimization; rational-polyhedron density argument; exact regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-203 — PSD sharp polar/Schur dual and root-free rational support packet

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-202 proved that, for the PSD mixed domain

`F = { y >= 0 : C y <= d, y^T P y <= rho }`,

support finiteness has an exact linear recession/polar alternative, and that any polar witness

`lambda >= 0`,

`C^T lambda + P nu - b >= 0`

produces the constructive family

`B_tau = d^T lambda + tau rho + (nu^T P nu)/(4 tau)`, `tau>0`.

The open quantitative question was whether optimizing this family merely gives a convenient nonsharp cap or actually recovers the sharp support value.

This child proves the stronger statement.

For `P=P^T>=0` and `rho>0`, define

`J(lambda,nu) := d^T lambda + sqrt(rho * nu^T P nu)`

on the polar-feasible set

`lambda >= 0`,

`alpha := C^T lambda + P nu - b >= 0`.

Then:

1. every such pair gives a valid support bound;
2. the square root can be removed completely from a prescribed-`B` trusted packet;
3. under the same ordinary convex Slater condition used for the PSD completeness corridor of T-P5-201, the exact support is

   **`sup_F b^T y = inf J(lambda,nu)`**;

4. equivalently, optimizing T-P5-202's completed-square family over `lambda,nu,tau` is sharp, not merely sufficient;
5. for rational data, every **strict rational margin** `B > sup_F b^T y` has a fully rational, root-free certificate;
6. an exact sharp rational packet need not exist because the sharp support itself can be irrational even for one-dimensional rational data.

Thus, on the PSD + Slater corridor, the generic augmented-copositivity search of T-P5-201 is mathematically unnecessary for the support subproblem: one can use a polar linear system plus one PSD seminorm/SOC-type inequality. T-P5-201 remains necessary outside this corridor and remains the correct general mixed-domain fallback.

No actual P5 source matrix, same-cell identity, domain nonemptiness/coverage, Float64 enclosure, controller/PDE/ODE semantics, Lean/kernel proof, independent verification, admission, or registry promotion is claimed.

---

## 1. Setup

Let

- `P=P^T in R^(p x p)` be ordinary PSD;
- `C in R^(m x p)`;
- `d in R^m`;
- `rho >= 0`;
- `b in R^p`.

Write

`q_P(x) := x^T P x`

and

`F := { y in R^p : y>=0, C y<=d, q_P(y)<=rho }`.

The support value is

`s_* := sup { b^T y : y in F }`.

The intended T-P5-200 application has `b=V^T h`, so `b` may have mixed signs. No entrywise sign assumption on `b` or `nu` is used in the basic certificate.

---

## 2. T203-A — PSD seminorm Cauchy-Schwarz without a square root factorization

### Lemma

For every symmetric PSD `P` and all real vectors `x,z`,

**`(x^T P z)^2 <= (x^T P x)(z^T P z)`.**

### Proof

For every real scalar `t`, PSD gives

`0 <= (x+t z)^T P (x+t z)`

`= q_P(x) + 2t x^T P z + t^2 q_P(z)`.

If `q_P(z)>0`, the discriminant of this quadratic in `t` is nonpositive:

`4(x^T P z)^2 - 4 q_P(x) q_P(z) <= 0`.

If `q_P(z)=0`, T-P5-202's PSD-null lemma gives `Pz=0`, so `x^TPz=0` and the same inequality is trivial.

QED.

### Why this lemma matters here

A trusted checker does **not** need a Cholesky factor, a matrix square root, an eigenbasis, or a pseudoinverse. It can consume only the rational quadratic forms `x^TPx`, `z^TPz`, and `x^TPz`.

---

## 3. T203-B — root-free prescribed-`B` support certificate

### Theorem

Assume `P>=0`, `rho>=0`, and choose real `lambda,nu,B` satisfying

`lambda >= 0`,

`alpha := C^T lambda + P nu - b >= 0` entrywise.

Define the residual scalar

`s := B - d^T lambda`.

If

**`s >= 0`**

and

**`s^2 >= rho * q_P(nu)`,**

then every `y in F` satisfies

**`b^T y <= B`.**

### Proof

From the polar inequality,

`b = C^T lambda + P nu - alpha`.

Hence for `y in F`,

`b^T y`

`= lambda^T C y + y^T P nu - alpha^T y`

`<= d^T lambda + y^T P nu`,

because `lambda>=0`, `Cy<=d`, `alpha>=0`, and `y>=0`.

By T203-A,

`(y^T P nu)^2 <= q_P(y) q_P(nu) <= rho q_P(nu) <= s^2`.

Since `s>=0`, this implies

`y^T P nu <= |y^T P nu| <= s`.

Therefore

`b^T y <= d^T lambda + s = B`.

QED.

### Trusted packet

For rational source data and rational proposed `B`, a PASS packet contains only

- rational `lambda>=0`;
- rational `nu`;
- exact check `C^Tlambda + Pnu - b >=0`;
- exact check `s=B-d^Tlambda>=0`;
- exact check `s^2 >= rho*(nu^TPnu)`.

This uses only rational add/multiply/order. There is no square root in the checker.

---

## 4. T203-C — exact orthant Schur/KKT elimination for fixed `lambda,tau`

Fix `tau>0` and a vector

`ell := b - C^T lambda`.

Consider the concave orthant quadratic

`Phi_tau(ell) := sup_{y>=0} [ ell^T y - tau q_P(y) ]`.

### Theorem

In extended-real form,

**`Phi_tau(ell)`**

**`= inf { q_P(nu)/(4tau) : Pnu - ell >= 0 }`.**

If the right feasible set is empty, both sides are `+infinity`.

### Weak direction by exact square completion

Take any `nu` with

`beta := Pnu-ell >=0`.

For every `y>=0`,

`q_P(nu)/(4tau) - [ell^Ty - tau q_P(y)]`

`= tau (y - nu/(2tau))^T P (y - nu/(2tau)) + beta^T y`

`>=0`.

Thus

`Phi_tau(ell) <= q_P(nu)/(4tau)`.

Taking the infimum over feasible `nu` gives one inequality.

### Reverse direction by orthant KKT

Assume `Phi_tau(ell)<+infinity`. Equivalently, the convex quadratic program

`min_{y>=0} [ tau q_P(y) - ell^T y ]`

is bounded below. A finite-dimensional convex quadratic bounded below on a polyhedron attains its minimum. The orthant has a strict interior point, so the usual KKT conditions are exact.

Let `y_*` be a minimizer. Then there is `mu>=0` with

`2tau P y_* - ell - mu = 0`,

`mu_i (y_*)_i = 0` for every `i`.

Set

**`nu_* := 2tau y_*`.**

Then

`Pnu_* - ell = mu >=0`,

so `nu_*` is feasible for the right-hand problem. Complementarity yields

`ell^T y_* = 2tau q_P(y_*)`.

Therefore

`Phi_tau(ell)`

`= ell^T y_* - tau q_P(y_*)`

`= tau q_P(y_*)`

`= q_P(nu_*)/(4tau)`.

Hence equality holds.

### Infinite branch

If no `nu` satisfies `Pnu-ell>=0`, the Farkas alternative for the cone

`{ r>=0 : Pr=0 }`

produces `r>=0`, `Pr=0`, and `ell^Tr>0`. Along `y=t r`,

`ell^T y - tau q_P(y) = t ell^T r -> +infinity`.

Thus the extended-value equality is exact on both finite and infinite branches.

### Structural point

The T-P5-202 square packet is not merely a Young inequality. For fixed `lambda,tau`, minimizing its `nu` variable computes the **exact** orthant quadratic Lagrange envelope.

---

## 5. T203-D — eliminate `tau`: exact seminorm dual

Assume now **`rho>0`**.

For fixed polar-feasible `(lambda,nu)`, write

`q := q_P(nu) >=0`.

T-P5-202 gives

`B_tau = d^Tlambda + tau rho + q/(4tau)`.

### Scalar minimization

For `q>0`, AM-GM or one-variable differentiation gives

**`inf_{tau>0} [tau rho + q/(4tau)] = sqrt(rho q)`,**

with unique minimizer

**`tau_* = (1/2) sqrt(q/rho)`.**

For `q=0`, the infimum is `0`. Since PSD implies `q=0 -> Pnu=0`, the same polar constraint becomes the pure polyhedral condition

`C^Tlambda-b>=0`,

so this limiting case is exactly the `tau=0` branch of the ordinary Lagrange dual.

Therefore define

**`J(lambda,nu) := d^Tlambda + sqrt(rho q_P(nu))`**

on

`K_pol := { (lambda,nu) : lambda>=0, C^Tlambda + Pnu - b >=0 }`.

The fully reduced dual value is

**`theta_* := inf_{K_pol} J(lambda,nu)`.**

### Weak duality

T203-B immediately implies

**`s_* <= theta_*`.**

Indeed every feasible `(lambda,nu)` gives the support bound `J(lambda,nu)` in real arithmetic.

---

## 6. T203-E — sharpness under the PSD Slater corridor

Assume:

1. `P>=0`;
2. `rho>0`;
3. there exists a strict feasible point `y_bar>0` with

   `C y_bar < d`,

   `q_P(y_bar) < rho`;

4. the support value `s_*` is finite.

These are the ordinary finite-dimensional convex Slater hypotheses already used for the PSD completeness corridor in T-P5-201.

### Theorem

Under these assumptions,

**`s_* = theta_*`**

that is,

**`sup_{y in F} b^T y`**

**`= inf_{lambda>=0, C^Tlambda+Pnu-b>=0}`**

**`[ d^Tlambda + sqrt(rho * nu^T P nu) ]`.**

### Proof

The Lagrangian for the primal support problem is

`L(y;lambda,tau)`

`= b^Ty + lambda^T(d-Cy) + tau(rho-q_P(y))`

with `lambda>=0`, `tau>=0`, and `y>=0` retained as the primal domain.

Hence the Lagrange dual function is

`g(lambda,tau)`

`= d^Tlambda + tau rho`

`  + sup_{y>=0} [(b-C^Tlambda)^T y - tau q_P(y)]`.

For `tau>0`, T203-C eliminates the inner supremum exactly as

`inf_{Pnu-(b-C^Tlambda)>=0} q_P(nu)/(4tau)`.

For `tau=0`, the inner supremum is finite exactly when

`C^Tlambda-b>=0`,

and then its value is zero; this is the `q_P(nu)=0` limiting/pure-polyhedral branch.

Therefore the full Lagrange dual value equals

`inf_{lambda,nu,tau>0}`

`[ d^Tlambda + tau rho + q_P(nu)/(4tau) ]`

with `lambda>=0` and `C^Tlambda+Pnu-b>=0`, together with the included pure-polyhedral limit.

Eliminating `tau` by Section 5 gives exactly `theta_*`.

By convex Slater strong duality, the primal support value equals the Lagrange dual value. Hence

`s_*=theta_*`.

QED.

### Consequence for T-P5-201

On this PSD + Slater corridor, the support subproblem never needs a generic copositivity search merely to recover a sharp real bound. The sharp value is already the optimum of a linear-polar + PSD-seminorm dual.

T-P5-201 remains the correct route when:

- `P` is not ordinary PSD;
- Slater/convex regularity is unavailable for a desired completeness claim;
- one is consuming a more general augmented copositive packet not reducible to this PSD seminorm form.

---

## 7. T203-F — there is an optimal nonnegative `nu` on the sharp KKT branch

The reduced theorem allows arbitrary signed `nu`, which is useful for weak certificates. But the KKT construction in T203-C gives more.

Whenever `tau>0` and the dual inner problem is finite, an optimal witness can be chosen as

`nu_*=2tau y_*`.

Because `y_*>=0`,

**`nu_*>=0`.**

Thus, under the Slater sharpness theorem, the dual optimum may be searched with `nu>=0` without changing the optimal value, while keeping the more permissive signed-`nu` formulation for certificate consumption.

At a nondegenerate sharp contact with `q_P(nu_*)>0`, the scalar `tau` optimum also satisfies

`q_P(nu_*) = 4 tau_*^2 rho`.

Since `nu_*=2tau_* y_*`, this gives

**`q_P(y_*)=rho`.**

So whenever the quadratic support term is genuinely active, the sharp primal contact lies on the quadratic boundary, exactly as expected from complementary slackness.

---

## 8. T203-G — rational strict-margin completeness

Assume now that

`P,C,d,b,rho,B`

are all rational, `P>=0`, `rho>0`, the Slater hypotheses of Section 6 hold, and

**`B > s_*`.**

### Theorem

There exist **rational** `lambda,nu` such that, with

`s=B-d^Tlambda`,

all of the following hold exactly:

`lambda>=0`,

`C^Tlambda+Pnu-b>=0`,

`s>0`,

**`s^2 > rho * q_P(nu)`.**

Hence every strict rational support margin has a fully rational T203-B certificate.

### Proof

By `theta_*=s_*<B`, choose a real polar-feasible pair `(lambda_0,nu_0)` with

`J(lambda_0,nu_0)<B`.

The polar-feasible set

`K_pol={lambda>=0, C^Tlambda+Pnu-b>=0}`

is a rational polyhedron. Rational points are dense in every nonempty face of a rational polyhedron. Therefore `(lambda_0,nu_0)` can be approximated arbitrarily closely by rational points `(lambda,nu)` that remain in `K_pol`.

The map

`(lambda,nu) -> d^Tlambda + sqrt(rho q_P(nu))`

is continuous. Choose the rational approximation close enough that

`d^Tlambda + sqrt(rho q_P(nu)) < B`.

Set the rational number

`s=B-d^Tlambda`.

Then

`s > sqrt(rho q_P(nu)) >=0`,

hence

`s^2 > rho q_P(nu)`.

QED.

### Practical consequence

For a trusted exact-rational consumer, it is unnecessary to represent the possibly irrational optimum. Choose any rational `B` with enough downstream Lyapunov margin, and certify it by the strict root-free inequality.

This is precisely the regime needed by T-P5-200 cubic absorption: downstream closure usually needs a safe rational cap, not symbolic ownership of the exact algebraic optimum.

---

## 9. T203-H — exact relation to the T-P5-202 `tau` family

For fixed polar-feasible `(lambda,nu)` with `rho>0`, `q=q_P(nu)>0`,

`B_tau - [d^Tlambda + sqrt(rho q)]`

`= tau rho + q/(4tau) - sqrt(rho q)`

`= ( sqrt(tau rho) - sqrt(q)/(2sqrt(tau)) )^2`

`>=0`.

Equivalently,

`B_tau` is sharp for that `(lambda,nu)` exactly at

`tau=(1/2)sqrt(q/rho)`.

Thus the apparent looseness of T-P5-202 is entirely the price of a nonoptimal scalar completion parameter once `(lambda,nu)` are fixed. There is no additional hidden PSD-copositivity gap.

If the optimal `tau` is irrational, a rational `tau` packet can approximate but need not attain the exact optimum. T203-B avoids this representational issue by checking only

`s^2 >= rho q`.

---

## 10. Exact regressions

### Regression A — one-dimensional quadratic cap, irrational sharp value

Take

`p=1`, `P=[1]`, `rho=2`, `b=1`,

with no additional `C y<=d` constraints.

Then

`F={y>=0:y^2<=2}`

and the exact support is

**`s_*=sqrt(2)`.**

The polar condition is simply

`nu>=1`.

Hence

`J(nu)=sqrt(2)*|nu|`,

whose minimum is attained at `nu=1`, giving exactly `sqrt(2)`.

T-P5-202's family is

`B_tau=2tau+1/(4tau)`

with minimum `sqrt(2)` at

`tau=1/(2sqrt(2))`, which is irrational.

Therefore rational input data can have an irrational sharp support. An exact sharp **rational** bound packet cannot exist simply because the correct bound is not rational.

Nevertheless every rational `B>sqrt(2)` has the rational root-free certificate

`nu=1`,

`s=B`,

`B^2>2`.

This exactly demonstrates the distinction between sharp real completeness and strict-margin rational completeness.

### Regression B — polyhedral branch dominates

Take `p=1`, `P=[1]`, `rho=4`, `b=1`, and the additional constraint

`0<=y<=1`,

encoded by `C=[1]`, `d=1`.

The exact support is `1`, even though the quadratic-only support would be `2`.

Choose

`lambda=1`, `nu=0`.

Then

`C^Tlambda+Pnu-b=0`

and

`J=1`.

So the reduced dual automatically selects the pure-polyhedral `tau=0` branch when that is sharper.

### Regression C — quadratic branch dominates

Use the same data but set `d=10`. Then the polyhedral bound is inactive and the exact support is `2`.

Choose `lambda=0`, `nu=1`:

`Pnu-b=0`,

`J=sqrt(4)=2`.

Thus the same dual formulation switches cleanly between the linear and quadratic active mechanisms.

---

## 11. Candidate theorem statements

### T203-1 `psd_seminorm_cauchy_schwarz_sq`

For symmetric PSD `P`,

`(x^T P z)^2 <= (x^T P x)(z^T P z)`.

### T203-2 `mixedPSD_root_free_support_bound`

If

`lambda>=0`,

`C^Tlambda+Pnu-b>=0`,

`s=B-d^Tlambda>=0`,

`s^2>=rho*(nu^TPnu)`,

then

`y>=0 -> Cy<=d -> y^TPy<=rho -> b^Ty<=B`.

### T203-3 `orthant_psd_quadratic_schur_dual`

For `tau>0`,

`sup_{y>=0} [ell^Ty-tau y^TPy]`

`= inf_{Pnu-ell>=0} (nu^TPnu)/(4tau)`

in extended-real form.

### T203-4 `mixedPSD_support_reduced_dual`

Under PSD + strict Slater + finite support + `rho>0`,

`sup_F b^Ty`

`= inf_{lambda>=0, C^Tlambda+Pnu-b>=0}`

`[d^Tlambda+sqrt(rho*(nu^TPnu))]`.

### T203-5 `mixedPSD_strict_rational_support_packet`

For rational data satisfying T203-4, every rational `B` strictly above the support admits rational `lambda,nu` satisfying the root-free T203-2 packet with strict final square margin.

### T203-6 `mixedPSD_tau_family_exact_infimum`

Under the same corridor, the infimum of T-P5-202's

`d^Tlambda+tau rho+(nu^TPnu)/(4tau)`

over polar witnesses and `tau>0`, plus the pure-polyhedral limiting branch, equals the exact support.

---

## 12. Suggested checker routing

For an actual same-source mixed packet with `P` certified ordinary PSD:

1. verify domain nonemptiness and the actual consumed `C,P,d,rho,b` key;
2. run T-P5-202's positive-recession LP first; if feasible, return true support-unbounded obstruction;
3. otherwise solve the reduced convex dual

   `min d^Tlambda + sqrt(rho nu^TPnu)`

   subject to

   `lambda>=0`, `C^Tlambda+Pnu-b>=0`;

4. for a trusted rational PASS at a proposed rational `B`, do **not** import the square root result; instead emit rational `lambda,nu` and verify

   `s=B-d^Tlambda>=0`,

   `s^2>=rho*(nu^TPnu)`;

5. feed the resulting exact rational support bound into T-P5-200;
6. only if `P` is not PSD, or the required convex/Slater completeness corridor is unavailable, fall back to T-P5-201's generic augmented-copositive route.

This removes a generic copositivity search from the PSD support corridor while preserving fail-closed semantics elsewhere.

---

## 13. Fail-closed labels

### `PASS_PSD_ROOT_FREE_SUPPORT_BOUND`

A same-domain PSD packet has rational `lambda,nu,B` satisfying the exact T203-B inequalities.

### `PASS_PSD_SHARP_DUAL_REAL`

PSD + strict Slater + finite support are established and the reduced seminorm dual is used as a sharp real characterization.

### `PASS_PSD_STRICT_RATIONAL_MARGIN`

A rational `B>s_*` is accompanied by a rational root-free packet with strict square margin.

### `SHARP_VALUE_ALGEBRAIC_NOT_RATIONAL`

The real sharp support is known but is not rational; do not require a rational packet to equal it exactly. Use a rational strict upper margin.

### `PSD_SLATER_COMPLETENESS_NOT_AVAILABLE`

The root-free packet remains a sound sufficient certificate, but do not claim sharp-dual completeness. Route to T-P5-201 or another exact fallback if sharpness is required.

### `PSD_GATE_NOT_APPLICABLE`

`P` is not certified ordinary PSD. Do not use T203-A/C/D. Return to the general copositive/nonconvex mixed-domain machinery.

---

## 14. Boundaries remaining OPEN

This review does not prove:

1. that the actual P5 selector/domain matrix `P` is ordinary PSD;
2. that actual `C,P,d,rho,b` are source-bound to one cell/tube/runtime key;
3. actual nonemptiness, strict Slater, trajectory membership, or global coverage;
4. the numerical value of the real P5 support optimum;
5. that any resulting cap is small enough for the final T-P5-200 Lyapunov margin;
6. Float64/directed-rounding or solver-certificate extraction semantics;
7. controller/PDE/ODE/source-evaluator correctness;
8. Lean/kernel compilation or axiom checks;
9. independent verification by 封不觉;
10. admission, registry, P5/P8/M4, or global Route-B closure.

All remain open.

---

## 15. New structural fingerprint

The mathematical chain is now

**PSD mixed domain**

`-> recession polar gate`

`-> orthant quadratic KKT`

`-> exact Schur/completed-square elimination`

`-> scalar tau minimization`

`-> sharp PSD-seminorm support dual`

`-> root-free squared rational certificate`

`-> gauge-preserving T-P5-200 cubic absorption`.

The central point is that the support optimization and the trusted certificate should be separated: the optimizer may use a square root/SOC representation, while the proof packet consumed downstream can remain entirely rational and division/root free.

---

## 16. Next mathematical seam

After T203, the next useful energy question is no longer whether the PSD mixed support cap can be made sharp in principle. It can.

The remaining physically relevant seam is **margin sensitivity**: how a support error `Delta B` propagates through the T-P5-200 quadratic debit

`D_B=(h0+B)Q+sym(b c^T)`

and therefore through the cone-wise Lyapunov decay margin of T-P5-192.

A useful next child would derive an exact monotonic/threshold law in `B` (or `Delta B`) for the final copositivity/decay gate, so a source-side support solver knows how much rational slack is affordable before cubic absorption destroys the desired `gamma`. That task is disjoint from source provenance and from T203's support duality itself.