---
kind: review_result
review_id: review-T-P5-258-binary-quartic-realized-direction-sos-honglianmozun-20260910T1554Z
task_id: T-P5-258-BINARY-QUARTIC-REALIZED-DIRECTION-SOS
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T15:54:00Z
claim_commit: 7c533a103f11e89d61fbb4f2bda77d9f6c3c3e82
inspected_commit: 5b0589984c84c68dfff19190410c947d7cd95185
upstream_commits:
  - 44b112238f3be56d3915e4c8aa4270d40a79830e  # T-P5-257 radial quotient-factor certificate
  - e41a4f7fab94f40593cdbe66ae7c23094a8e7134  # T-P5-256 structured Hessian tensor Gram majorant
  - 17e8f3fec31828ef7992411c81102b4aa1852e01  # T-P5-255 Hessian-to-Jacobian Gram reserve
  - 598db594c600e1999d4ddf12cb0fb23df4ffbd70  # T-P5-254 shared-quotient Jacobian leakage
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_two_dimensional_syzygy_gauge_lemma; add_binary_quartic_one_parameter_Gram_certificate; add_fraction_free_principal_minor_checker; add_strict_rational_multiplier_corollary; add_unbounded_matrix_gate_conservatism_regression
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact polynomial algebra and hand-checkable rational PSD regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-258 — Binary-quartic realized-direction SOS certificate

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-257 isolates the sharp remaining radial/realized-direction obligation after quotient factorization:

`u(theta)^T [kappa q(theta) W - A(theta)^T A(theta)] u(theta) >= 0`.

Its sufficient matrix replacement

`A(theta)^T A(theta) <= kappa q(theta) W`

can still be much stronger, because it tests every artificial vector against `A(theta)`, whereas the energy identity only tests the vector realized by the same state.

This child closes an exact low-degree branch: **quotient dimension two, homogeneous quadratic source/storage factor, and quotient factor `A(u)` linear in `u`.** In this branch the true energy remainder is a homogeneous binary quartic. Its nonnegativity is equivalent to one scalar parameter making a `3 x 3` Gram matrix PSD. No operator-norm relaxation is needed.

There is also an exact structural reason for the gap. In two quotient coordinates, every polynomial perturbation of `A` invisible to `A(u)u` is a Koszul/syzygy gauge multiple of `(-u2,u1)`. The matrix gate charges that invisible gauge, while the realized energy does not. A rational one-parameter family below makes the matrix-gate loss arbitrarily large while the scalar Lyapunov polynomial is unchanged.

No actual deployed P5 Hessian/factor packet, source identity, cell/tube/trajectory coverage, Float64/interval semantics, Lean receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

# Part I — realized-direction gauge

## 1. Setup

Write the two quotient coordinates as

`u=(x,y)^T`.

Let `A(u)` be a polynomial `k x 2` matrix and define the contracted nonlinear vector

`F(u) := A(u) u`.

Only `F` occurs in the sharp radial debit:

`||F(u)||^2 <= kappa q(u) (u^T W u)`.

Consequently `A` is not unique.

## 2. Theorem 1 — complete two-dimensional polynomial syzygy gauge

Let `K` be a field of characteristic different from two (in particular `Q` or `R`). For polynomial matrices

`A,A' in K[x,y]^(k x 2)`,

the following are equivalent:

1. `A'(u)u = A(u)u` identically;
2. there exists a polynomial column `h(u) in K[x,y]^k` such that

   **(2.1)** `A'(u)-A(u) = h(u) [-y, x]`.

Thus the realized energy depends only on the quotient class

`A mod <[-y,x]>`.

### Proof

Set `B=A'-A`. Row by row, write `B_j=(b1,b2)`. The identity `B_j u=0` is

`x b1 + y b2 = 0`.

Hence `x b1 = -y b2`. Since `x` and `y` are coprime in the UFD `K[x,y]`, `y` divides `b1`; write `b1=-yh`. Substitution gives `y(-xh+b2)=0`, hence `b2=xh`. Therefore

`B_j=h[-y,x]`.

Doing this for every output row gives (2.1). The converse is immediate because

`[-y,x] [x,y]^T = 0`.

This is exact polynomial algebra; there is no norm, projector, pseudoinverse, or numerical nullspace.

## 3. Corollary — canonical symmetric polarization for linear `A`

Suppose one output row of `A` is linear:

`a(u)=[alpha x + beta y, gamma x + delta y]`.

Then

`a(u)u = alpha x^2 + (beta+gamma)xy + delta y^2`.

The unique symmetric-polarized representative is

**(3.1)**

`a_sym(u)=[alpha x + ((beta+gamma)/2)y, ((beta+gamma)/2)x + delta y]`.

Moreover

`a-a_sym = ((gamma-beta)/2)[-y,x]`.

Hence the antisymmetric coefficient is a pure realized-direction gauge. A checker may remove it exactly before building the scalar quartic. It must not interpret a large antisymmetric coefficient as Lyapunov leakage merely because the stronger matrix gate sees it.

Important boundary: symmetric polarization removes the *obvious* syzygy gauge but does not in general make the matrix inequality equivalent to the realized scalar inequality. The exact scalar quartic test below remains the sharp branch.

---

# Part II — the realized energy is a binary quartic

## 4. Homogeneous two-dimensional branch

Assume rational symmetric matrices

`M=M^T`, `W=W^T`,

and a quotient factor linear in `u`:

**(4.1)** `A(u)=x A1 + y A2`,

with rational `A1,A2 in Q^(k x 2)`.

Let

`q(u)=u^T M u`.

Define the exact realized-direction slack

**(4.2)**

`P_kappa(x,y)
 = kappa (u^T M u)(u^T W u) - ||A(u)u||^2`.

For rational `kappa`, this is a homogeneous binary quartic with rational coefficients. Expand uniquely as

**(4.3)**

`P_kappa(x,y)=a x^4+b x^3 y+c x^2 y^2+d x y^3+e y^4`.

The sharp Lyapunov obligation on any centered positive-radius ellipsoid is exactly

**(4.4)** `P_kappa(x,y)>=0 for all real (x,y)`.

Why the source radius disappears in this homogeneous branch: if a nonzero direction violates (4.4), scaling that direction toward the origin puts a violating point in every centered source neighborhood. Conversely global nonnegativity obviously implies source-local nonnegativity. Thus for homogeneous degree four, a centered source cap gives no weaker directional problem.

This equivalence is specific to the homogeneous branch. Affine offsets, extra kernel parameters, or off-center source sets are handled separately in the boundary section.

---

# Part III — exact one-parameter Gram certificate

## 5. Theorem 2 — binary quartic nonnegativity iff one `3 x 3` Gram is PSD

For the quartic (4.3), define for a scalar parameter `tau`

**(5.1)**

`G(tau) =
 [[2a,        b,          tau],
  [ b,   2(c-tau),         d],
  [tau,        d,          2e]]`.

Let

`z=[x^2,xy,y^2]^T`.

Then for every `tau`, exactly

**(5.2)** `P_kappa(x,y) = (1/2) z^T G(tau) z`.

Furthermore,

**(5.3)**

`P_kappa>=0 on R^2  <=>  exists tau in R such that G(tau)>=0`.

### Proof of the identity

Expanding `z^T G z` gives

`2a x^4 + 2b x^3y + [2tau+2(c-tau)]x^2y^2 + 2d xy^3 + 2e y^4`,

which is `2P_kappa`.

### Proof of sufficiency

If `G(tau)>=0`, factor it over the reals as a Gram matrix. Then `(1/2)z^TGz` is a sum of squares of homogeneous quadratics, hence nonnegative.

### Proof of necessity

Every nonnegative homogeneous binary quartic is a sum of squares of real homogeneous quadratics. An elementary route is enough here:

- factor the real binary form into real linear factors and irreducible real quadratic factors;
- every real linear factor occurs with even multiplicity, otherwise the sign changes across its zero line;
- every remaining nonnegative quadratic factor is a sum of two squares of real linear forms;
- repeatedly use the two-squares product identity

  `(p^2+q^2)(r^2+s^2)=(pr-qs)^2+(ps+qr)^2`.

Thus `P=r1^2+...+rm^2` with quadratic `ri`. Writing each `ri` in the basis `z=(x^2,xy,y^2)` gives a PSD Gram matrix `Q` satisfying `P=z^TQz`. The coefficient equations force

`Q11=a`, `2Q12=b`, `Q22+2Q13=c`, `2Q23=d`, `Q33=e`.

There is exactly one free scalar, say `Q13=tau/2`, and `2Q=G(tau)`. Hence some real `tau` satisfies (5.3).

This is a lossless certificate for this branch, not an SOS relaxation.

---

# Part IV — fraction-free checker

## 6. Principal-minor packet

For rational `a,b,c,d,e,tau`, the condition `G(tau)>=0` can be checked by exact rational principal minors. The seven nontrivial gates are

**1 x 1:**

`2a >= 0`,

`2(c-tau) >= 0`,

`2e >= 0`.

**2 x 2:**

**(6.1)** `4a(c-tau)-b^2 >= 0`,

**(6.2)** `4ae-tau^2 >= 0`,

**(6.3)** `4e(c-tau)-d^2 >= 0`.

**3 x 3:**

**(6.4)**

`det G(tau)
 = 2[tau^3-c tau^2+(bd-4ae)tau+(4aec-a d^2-e b^2)] >= 0`.

For a real symmetric `3 x 3` matrix, nonnegativity of all principal minors is necessary and sufficient for PSD. Therefore the entire sharp two-dimensional realized-direction problem reduces to **one scalar semialgebraic feasibility problem of degree at most three**, plus linear/quadratic side gates.

No eigenvector, square root, operator norm, pseudoinverse, or floating minimization is mathematically necessary.

If the implementation prefers an LDL/Schur checker, the same matrix `G(tau)` can be consumed there; (6.1)-(6.4) are simply a transparent fraction-free packet.

## 7. Theorem 3 — strict rational margin gives a rational Gram witness

Assume `a,b,c,d,e in Q` and

**(7.1)** `P_kappa(u)>0 for every u!=0`.

Then there exists **rational** `tau` such that

**(7.2)** `G(tau)>0`.

### Proof

On the unit circle, the positive quartic `P` has a strictly positive minimum. The quartic

`H0=x^4+x^2y^2+y^4=z^T I z`

is also strictly positive away from zero. Hence for sufficiently small real `epsilon>0`,

`P-epsilon H0 >=0`.

By Theorem 2, `P-epsilon H0` has a PSD Gram `Q0`. Therefore `P` has the positive definite Gram

`Q0+epsilon I >0`.

All Gram matrices representing the same binary quartic lie on the affine one-parameter family `G(tau)/2`, so there exists a real `tau0` with `G(tau0)>0`. Positive definiteness is open, and the rationals are dense; choosing rational `tau` sufficiently close to `tau0` preserves `G(tau)>0`. Since the quartic coefficients are rational, this gives a fully rational strict certificate.

Thus an actual strict Lyapunov margin in this branch is not forced to serialize an algebraic Gram parameter. Only a sharp non-strict boundary may require an algebraic witness or a separate exact boundary argument.

---

# Part V — strict separation from the quotient matrix gate

## 8. Rational family with arbitrarily large conservatism

Take

`M=W=I_2`,

`q(u)=x^2+y^2`,

one output (`k=1`), and for a rational parameter `N` define

**(8.1)**

`A_N(u)=[x-Ny, Nx+y]`.

This decomposes exactly as

**(8.2)**

`A_N(u) = [x,y] + N[-y,x]`.

The second term is the syzygy gauge from Theorem 1, so

**(8.3)**

`F_N(u)=A_N(u)u=x^2+y^2=q(u)`

for every `N`.

Therefore the sharp realized-direction constant is

**(8.4)** `kappa_radial^*=1`.

Indeed

`||F_N(u)||^2=q(u)^2 = q(u)(u^T W u)`.

Now inspect the stronger matrix gate. Since `A_N` is a row vector,

`A_N A_N^T
 =(x-Ny)^2+(Nx+y)^2
 =(1+N^2)(x^2+y^2)
 =(1+N^2)q(u)`.

Thus `A_N^T A_N` has eigenvalues

`0` and `(1+N^2)q(u)`.

Consequently

**(8.5)**

`A_N(u)^T A_N(u) <= kappa q(u) I_2`

holds for all `u` iff

**(8.6)** `kappa >= 1+N^2`.

So

**(8.7)**

`kappa_matrix^*/kappa_radial^* = 1+N^2`,

which is unbounded as `|N|` grows.

This proves that the remaining conservatism after T-P5-257 is not merely a small constant-factor artifact. The matrix packet can lose an arbitrarily large amount of Lyapunov reserve by charging a direction that is exactly invisible after contraction with the physical quotient state.

## 9. Strict rational PASS while the matrix gate FAILS

To avoid relying on a zero-margin equality case, choose `N=10` and `kappa=2`.

The exact realized slack is

`P_2=q^2=(x^2+y^2)^2`

so

`a=1, b=0, c=2, d=0, e=1`.

Choose rational `tau=0`. Then

**(9.1)** `G(0)=diag(2,4,2)>0`.

Hence the sharp realized-direction certificate has a strict positive quartic margin.

But the matrix gate would require

`kappa >= 1+10^2 = 101`,

while `kappa=2`. Its least eigenvalue along the charged row direction equals

`(2-101)q=-99q<0`

for every nonzero state. Thus the exact scalar certificate strictly PASSes while the stronger matrix gate very strongly FAILs.

This is a pure rational regression suitable for a trusted checker or a small Lean sidecar.

---

# Part VI — theorem statement for downstream use

## 10. Candidate theorem: `binary_quartic_realized_direction_iff_gram`

A source-independent theorem can be stated as follows.

**Inputs**

- rational/real `2 x 2` symmetric `M,W`;
- linear matrix pencil `A(u)=xA1+yA2`;
- scalar `kappa`;
- exact quartic coefficients `a,b,c,d,e` satisfying expansion (4.3).

**Conclusion**

The realized-direction inequality

`||A(u)u||^2 <= kappa (u^TMu)(u^TWu)` for every real `u`

is equivalent to existence of `tau` for which `G(tau)>=0`.

For a rational executable certificate, `tau` is supplied explicitly and the checker proves the coefficient identity plus the seven principal-minor inequalities. The forward existential direction is mathematical architecture; the backward direction is the small trusted certificate consumer.

## 11. Candidate theorem: `two_coordinate_syzygy_gauge`

If polynomial `B: K^2 -> K^(k x 2)` satisfies

`B(u)u=0` identically,

then there exists polynomial `h:K^2->K^k` with

`B(u)=h(u)[-u2,u1]`.

This is useful before any norm comparison: it lets the generator normalize away exact energy-invisible gauge terms rather than asking a matrix majorant to pay for them.

## 12. Minimal checker route

For a concrete two-dimensional quotient cell/family, the mathematical hot path becomes:

`T-P5-257 exact quotient factor F=A(u)u`

`-> remove/check polynomial syzygy gauge if desired`

`-> exact quartic coefficient expansion`

`-> search one scalar tau`

`-> serialize rational tau when strict margin exists`

`-> check G(tau) principal minors exactly`

`-> consume sharp kappa in T-P5-254/255 leakage/energy budget`.

This replaces a pointwise `2 x 2` operator PSD inequality by one exact quartic Gram packet whose test vectors are exactly the physical realized directions.

---

# Part VII — failure boundaries

## 13. What this theorem does not cover

1. **Extra ambient/kernel variables.** If `A=A(u,z,s)` or `q=q(u,z)` depends on parameters not determined by the two quotient coordinates, freezing those parameters gives a binary quartic but does not by itself prove uniformity over the parameter set. A separate coefficient/SOS/domain certificate is required.

2. **Affine/nonhomogeneous factor.** If `A` has a constant term or the source/target is translated, the slack is not a homogeneous binary quartic. Homogenizing introduces another variable and changes the certificate class; do not silently reuse this `3 x 3` packet.

3. **Off-center source region.** The scaling argument in Section 4 uses a centered neighborhood of the origin. On a truncated/off-center region, global binary-form nonnegativity can be stronger than the requested local property.

4. **Dimension greater than two.** The one-parameter `3 x 3` Gram family is special to homogeneous binary quartics. It must not be generalized by assuming every higher-dimensional nonnegative quartic has the same SOS property.

5. **Sharp boundary rationality.** The strict-margin corollary guarantees rational `tau`; this review does not claim that every non-strict rational PSD quartic necessarily arrives with a rational positive-semidefinite Gram witness through the chosen serialization route.

6. **Source binding.** Nothing here identifies deployed `D/M/W/A`, proves a Hessian factorization from Julia/DH, or proves the source ellipsoid/trajectory remains in the required region.

## 14. Exact failure classifier

For a supplied rational `tau`, failure of one principal minor means only **that particular Gram witness fails**. It is not a mathematical counterexample until the one-dimensional feasible set in `tau` is proved empty or a direct state `u` with `P_kappa(u)<0` is produced.

Conversely, a matrix-gate failure is never by itself a radial failure: the family (8.1) shows the gap can be arbitrarily large.

This preserves fail-closed routing:

- `G(tau)>=0` for some serialized `tau` -> exact scalar PASS for this homogeneous binary branch;
- candidate `tau` fails -> search/partition remains open;
- scalar quartic negative at an exact state -> mathematical FAIL;
- matrix gate fails but scalar quartic unresolved -> **do not propagate FAIL**.

---

# Part VIII — dependency and next seam

## 15. Dependencies consumed

This child uses only the mathematical outputs of:

- T-P5-257: factor-before-Gram and the exact realized-direction quotient obligation;
- T-P5-256/255/254 only as downstream motivation for how the resulting `kappa` enters the nonlinear leakage budget.

It does not consume their source/coverage claims, because those remain open.

## 16. What this closes

For a source-like packet satisfying the stated two-coordinate homogeneous assumptions, the final realized-direction inequality is no longer forced through the stronger matrix PSD majorant. It has a lossless degree-four certificate with one scalar Gram parameter, and strict rational margins admit fully rational certificates.

The syzygy theorem also identifies the exact algebraic gauge responsible for potentially unbounded operator-norm overcharging.

## 17. What remains independent

Still open:

- actual deployed quotient dimension and exact factor `A`;
- exact `M/W` source identity and same-key convention;
- parameter/cell dependence of a deployed factor;
- cell/tube/trajectory/flowpipe/stencil coverage;
- Float64/interval semantics;
- Lean/kernel compilation;
- independent verification by `封不觉`;
- admission, registry, or P5/P8/M4 parent closure.

## 18. Next distinct mathematical seam

The natural next structural boundary is quotient dimension `r=3` with homogeneous quartic slack. In that case the realized polynomial is a **ternary quartic**. Classical real algebra says nonnegative ternary quartics are also SOS of quadratics, but the Gram space is now a `6 x 6` affine family rather than the single-parameter binary packet. A useful next child would derive the exact coefficient-to-Gram linear map, identify a low-dimensional/fraction-free PSD serialization, and then state explicitly where the lossless SOS property stops in higher quotient dimension. That would extend the sharp realized-direction route without falling back to the conservative matrix gate.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**. No provenance/receipt/admission upgrade or parent closure is asserted.