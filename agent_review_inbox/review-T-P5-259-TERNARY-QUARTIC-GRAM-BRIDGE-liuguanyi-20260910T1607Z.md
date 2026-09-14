---
kind: review_result
review_id: review-T-P5-259-ternary-quartic-gram-bridge-liuguanyi-20260910T1607Z
task_id: T-P5-259-TERNARY-QUARTIC-GRAM-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T16:07:00Z
claim_commit: 291b5dc6e55e0ed130fa37558566460f7e6ba52c
inspected_commit: 4e98955dbb11f8615fc3ee4f79df22a8e82ec66d
upstream_commits:
  - a24047e5b78cc0cabb191cfac7fab4a99deb1fec  # T-P5-258 binary quartic realized-direction SOS
  - 44b112238f3be56d3915e4c8aa4270d40a79830e  # T-P5-257 radial quotient-factor certificate
  - e41a4f7fab94f40593cdbe66ae7c23094a8e7134  # T-P5-256 structured Hessian tensor Gram majorant
  - 17e8f3fec31828ef7992411c81102b4aa1852e01  # T-P5-255 Hessian-to-Jacobian Gram reserve
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_ternary_quartic_six_parameter_Gram_bridge; add_rational_strict_Gram_corollary; add_Sym2_chart_transport; add_quaternary_nonSOS_boundary_regression
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact coefficient matching, dimension count, rational matrix identities, and hand-checkable non-SOS support argument; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-259 — Ternary-quartic exact Gram bridge and the quartic SOS boundary

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-258 closed the sharp realized-direction branch when the quotient dimension is two: the physical slack is a homogeneous binary quartic and its nonnegativity is equivalent to a one-parameter `3 x 3` Gram PSD packet.

This child closes the next exact algebraic layer for quotient dimension three.

If the realized-direction slack is a homogeneous ternary quartic with rational coefficients, then:

1. its complete Gram fiber over the quadratic monomial lift has exactly **six** free parameters;
2. by the classical Hilbert theorem for ternary quartics, physical nonnegativity is equivalent to existence of a PSD matrix in that six-parameter affine Gram fiber;
3. the entire coefficient-to-Gram map is explicit and fraction-free after multiplying the polynomial by `2`;
4. if the rational quartic is strictly positive away from the origin, a **rational positive-definite Gram witness always exists**;
5. under a rational invertible quotient-coordinate change, the certificate transports exactly by the symmetric-square representation, without whitening or floating eigenvectors;
6. this lossless route is the final exceptional quartic SOS dimension: in four variables there are rational nonnegative quartics that are not SOS. An explicit Choi-Lam-type example is proved below by a monomial-support contradiction.

No deployed P5 quotient dimension, exact factor `A`, source identity, cell/tube/trajectory coverage, Float64/interval semantics, Lean receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

# Part I — the exact six-parameter Gram fiber

## 1. Setup

Let the quotient variable be

`u=(x,y,z)^T`.

For the degree-two monomial lift use

**(1.1)**

`m(u) = [x^2, y^2, z^2, xy, xz, yz]^T`.

Write a homogeneous ternary quartic as

**(1.2)**

`p(x,y,z)`

`= a x^4 + b y^4 + c z^4`

`+ d x^3 y + e x^3 z + f x y^3 + g y^3 z + h x z^3 + i y z^3`

`+ j x^2 y^2 + k x^2 z^2 + l y^2 z^2`

`+ m x^2 y z + n x y^2 z + o x y z^2`.

There are exactly `15` quartic coefficients.

The space of symmetric `6 x 6` Gram matrices has dimension `21`, so a surjective coefficient map must have a six-dimensional kernel. The next theorem exhibits the full kernel explicitly.

## 2. Theorem 1 — complete fraction-free Gram parameterization

For arbitrary scalars `t1,...,t6`, define the symmetric matrix

**(2.1)**

`G(t) =`

`[[2a,  t1,  t2,    d,        e,        t4],`

` [ t1, 2b,   t3,    f,        t5,       g ],`

` [ t2, t3,   2c,    t6,       h,        i ],`

` [ d,  f,    t6, 2j-2t1,   m-t4,    n-t5],`

` [ e,  t5,   h,   m-t4,  2k-2t2,    o-t6],`

` [ t4, g,    i,   n-t5,    o-t6,  2l-2t3]]`.

Then identically in `x,y,z`,

**(2.2)**

`m(u)^T G(t) m(u) = 2 p(u)`.

Conversely, every symmetric Gram matrix `Q` satisfying

`m(u)^T Q m(u)=2p(u)`

is uniquely of the form `G(t)` for exactly one `t=(t1,...,t6)`.

### Proof

Coefficient matching gives the fixed entries immediately:

- `Q11=2a`, `Q22=2b`, `Q33=2c`;
- `Q14=d`, `Q15=e`, `Q24=f`, `Q26=g`, `Q35=h`, `Q36=i`.

The six duplicated degree-four monomials give the only freedom:

`x^2 y^2 = (x^2)(y^2) = (xy)^2`,

`x^2 z^2 = (x^2)(z^2) = (xz)^2`,

`y^2 z^2 = (y^2)(z^2) = (yz)^2`,

`x^2 y z = (x^2)(yz) = (xy)(xz)`,

`x y^2 z = (y^2)(xz) = (xy)(yz)`,

`x y z^2 = (z^2)(xy) = (xz)(yz)`.

Choose

`t1=Q12`, `t2=Q13`, `t3=Q23`, `t4=Q16`, `t5=Q25`, `t6=Q34`.

Matching the six duplicated coefficients then forces exactly

`Q44=2j-2t1`,

`Q55=2k-2t2`,

`Q66=2l-2t3`,

`Q45=m-t4`,

`Q46=n-t5`,

`Q56=o-t6`.

No other entries remain free. This proves both (2.2) and uniqueness.

### Minimality

The map `Sym_6 -> H_{3,4}` from symmetric Gram matrices to ternary quartics is surjective by the explicit construction above. Therefore its kernel has dimension

`21-15=6`.

Hence a generic complete Gram fiber cannot be parameterized by fewer than six scalar degrees of freedom. The six-parameter family (2.1) is dimension-minimal.

---

## 3. The six polynomial Gram gauges

The kernel is generated by the six quadratic-monomial syzygies

**(3.1)**

`(xy)^2 - x^2 y^2 = 0`,

`(xz)^2 - x^2 z^2 = 0`,

`(yz)^2 - y^2 z^2 = 0`,

`(xy)(xz) - (x^2)(yz) = 0`,

`(xy)(yz) - (y^2)(xz) = 0`,

`(xz)(yz) - (z^2)(xy) = 0`.

Thus changing `t1,t2,t3` redistributes a square monomial against the corresponding pure-product entry, while changing `t4,t5,t6` redistributes one mixed product against its alternative factorization.

This is the exact ternary analogue of the one-parameter binary Gram gauge in T-P5-258, except that the kernel is six-dimensional rather than one-dimensional.

A formal checker should treat these parameters as **Gram gauge variables**, not as physical source parameters.

---

# Part II — physical nonnegativity is exactly Gram feasibility in dimension three

## 4. Theorem 2 — ternary quartic nonnegativity iff six-parameter Gram PSD

For a real homogeneous quartic `p` in three variables, the following are equivalent:

1. `p(u)>=0` for every `u in R^3`;
2. `p` is a sum of squares of real quadratic forms;
3. there exists `t in R^6` such that

   **(4.1)** `G(t)>=0`.

### Proof

`3 -> 1` is immediate from (2.2):

`2p(u)=m(u)^T G(t)m(u)>=0`.

`2 -> 3`: if

`p=sum_r q_r(u)^2`

and each quadratic is `q_r=c_r^T m(u)`, then

`2p=m^T [2 sum_r c_r c_r^T] m`,

so the matrix `Q=2 sum_r c_r c_r^T` is PSD and, by Theorem 1, equals `G(t)` for a unique parameter vector.

`1 -> 2` is precisely the classical Hilbert exceptional case: every nonnegative **ternary quartic** is a sum of squares of quadratic forms.

Therefore (4.1) is a **lossless** certificate for this branch. It is not an S-procedure relaxation and it does not test artificial directions of `A(u)` separately from the realized state.

---

## 5. Direct connection to the T-P5-257/258 realized-direction slack

Suppose a three-dimensional quotient branch has homogeneous data

`q(u)=u^T M u`,

`w(u)=u^T W u`,

`A(u)=x A1 + y A2 + z A3`,

with rational matrices, and define

**(5.1)**

`P_kappa(u) = kappa q(u) w(u) - ||A(u)u||^2`.

Then `P_kappa` is a rational ternary quartic. Expanding its `15` coefficients and inserting them into (2.1) gives an exact six-variable spectrahedral feasibility problem:

**(5.2)**

`exists t1,...,t6 : G_kappa(t)>=0`.

By Theorem 2, (5.2) is equivalent to the true realized-direction inequality

`P_kappa(u)>=0 for all u`.

Thus for quotient dimension three, the stronger pointwise matrix gate

`A(u)^T A(u) <= kappa q(u) W`

is again unnecessary whenever the source branch truly reduces to the homogeneous ternary quartic (5.1).

As in T-P5-258, a centered positive-radius source ellipsoid does not weaken the directional question: a negative homogeneous quartic direction can be scaled arbitrarily close to the origin.

---

# Part III — exact rational serialization

## 6. Fraction-free coefficient packet

The choice `m^T G m = 2p` deliberately removes every `1/2` from the coefficient map. Therefore, if

`a,...,o,t1,...,t6`

are rational, multiply `G` by any common positive denominator `D` and obtain an integer symmetric matrix

**(6.1)** `G_int = D G`.

Because `D>0`,

`G>=0 iff G_int>=0`,

and similarly for positive definiteness.

No square root, eigendecomposition, SVD, pseudoinverse, or floating nullspace is required.

## 7. Exact PSD gates

For a supplied rational parameter vector `t`, a simple exact boundary-safe checker may use:

**(7.1)** all nonempty principal minors of `G_int` are nonnegative.

There are `2^6-1=63` such minors. This is finite and fraction-free; each determinant can be evaluated by Bareiss/fraction-free elimination.

For a strict certificate `G_int>0`, Sylvester's criterion is much cheaper:

**(7.2)** the six leading principal minors are strictly positive.

Hence the strict rational lane needs only six determinant signs once a rational `t` has been produced.

Boundary note: failure of one candidate `t` is only failure of that Gram witness. It is not a physical counterexample unless the entire six-dimensional Gram spectrahedron is proved empty or an exact state `u` with `p(u)<0` is produced.

---

## 8. Theorem 3 — rational strict margin implies rational PD Gram witness

Let `p in Q[x,y,z]` be a homogeneous quartic satisfying

**(8.1)** `p(u)>0` for every `u != 0`.

Then there exists a rational parameter vector

`t in Q^6`

such that

**(8.2)** `G(t)>0`.

### Proof

Because `p` is continuous and positive on the unit sphere, there exists a rational `epsilon>0` such that

`p(u) >= epsilon (x^2+y^2+z^2)^2`

for every `u`.

In the monomial basis (1.1),

**(8.3)**

`(x^2+y^2+z^2)^2 = m^T D0 m`,

where

`D0=diag(1,1,1,2,2,2)>0`.

The residual

`r=p-epsilon (x^2+y^2+z^2)^2`

is nonnegative. By Hilbert's ternary-quartic theorem it has a real PSD Gram matrix `Qr`.

Therefore

`Q*=2Qr + 2epsilon D0`

(after choosing the same normalization `m^T Q* m=2p`) is a real **positive-definite** Gram matrix for `2p`.

By Theorem 1 every Gram matrix for `2p` is `G(t)` for a unique `t in R^6`. The affine Gram fiber is defined over `Q`: its particular point `G(0)` and all six kernel directions are rational matrices. Rational parameter vectors are dense in `R^6`, and the positive-definite cone is open. Hence a rational `t` can be chosen sufficiently close to the real parameter of `Q*`, preserving `G(t)>0`.

This proves (8.2).

### Consequence

For a **strict** rational realized-direction reserve, exact serialization never needs an irrational Gram gauge. A rational search can in principle find a PD witness, and once found the six leading principal minors give a complete exact certificate.

This statement deliberately does **not** claim that every singular/non-strict rational ternary quartic must admit a rational PSD Gram witness in this chosen serialization. Boundary arithmetic should remain fail-closed unless an exact rational/algebraic witness is actually supplied.

---

# Part IV — quotient-coordinate covariance

## 9. Theorem 4 — symmetric-square chart transport

Let

`u=P v`,

where `P in GL_3(R)`. There is a unique `6 x 6` matrix `S2(P)` such that

**(9.1)** `m(Pv)=S2(P)m(v)`.

Every entry of `S2(P)` is a homogeneous quadratic polynomial in the entries of `P`.

If `G_u` is any Gram matrix for `2p(u)`, define

**(9.2)** `G_v = S2(P)^T G_u S2(P)`.

Then

`m(v)^T G_v m(v) = 2 p(Pv)`.

Moreover

**(9.3)**

`G_u>=0 -> G_v>=0`,

and because `P` is invertible, `S2(P)` is invertible, so in fact

`G_u>=0 iff G_v>=0`,

with the same equivalence for positive definiteness.

Thus ternary Gram feasibility is an intrinsic quotient property, not an artifact of a preferred whitening chart.

### Rational/fraction-free reverse transport

If `P` is rational, then `S2(P)` is rational. Let

`delta=det(P) != 0`, `J=adj(P)`.

Since

`P^{-1}=J/delta`

and `S2` is homogeneous of degree two,

**(9.4)**

`S2(P^{-1}) = S2(J)/delta^2`.

Therefore the reverse Gram transport can be written without division as

**(9.5)**

`delta^4 G_u = S2(J)^T G_v S2(J)`.

This is the exact `Sym^2` analogue of the adjugate chart transports already used elsewhere in the P5 chain.

No floating eigenbasis is mathematically privileged.

---

# Part V — exact low-dimensional regression

## 10. Strict rational regression

Take

**(10.1)**

`p0=(x^2+y^2+z^2)^2`.

Its coefficients are

`a=b=c=1`, `j=k=l=2`,

and all other coefficients zero.

Choose

`t1=t2=t3=t4=t5=t6=0`.

Then (2.1) gives

**(10.2)**

`G(0)=diag(2,2,2,4,4,4)>0`,

and indeed

`m^T G(0)m=2(x^2+y^2+z^2)^2`.

This is a fully rational strict witness and checks the normalization of every diagonal block in (2.1).

---

# Part VI — where the lossless quartic SOS route stops

## 11. A rational nonnegative quaternary quartic that is not SOS

Consider four variables `x,y,z,w` and the quartic

**(11.1)**

`F(x,y,z,w)`

`= x^2 y^2 + y^2 z^2 + z^2 x^2 + w^4 - 4 x y z w`.

### Nonnegativity

The four terms

`x^2 y^2`, `y^2 z^2`, `z^2 x^2`, `w^4`

are nonnegative and their product has fourth root `|xyzw|`. AM-GM gives

`x^2y^2+y^2z^2+z^2x^2+w^4 >= 4|xyzw| >= 4xyzw`.

Hence

**(11.2)** `F>=0` on `R^4`.

### Not a sum of squares of quadratic forms

Assume for contradiction

`F=sum_r q_r^2`

with homogeneous quadratic `q_r`.

Because the coefficient of `x^4` in `F` is zero, the coefficient of `x^2` in every `q_r` must vanish: the `x^4` coefficient of a sum of squares is the sum of the squares of those coefficients. The same argument removes `y^2` and `z^2` from every `q_r`.

Now inspect `x^2 w^2`. Since no `x^2` term remains in any `q_r`, its coefficient in `sum q_r^2` is the sum of squares of the `xw` coefficients. But `F` has zero `x^2w^2`, so every `xw` coefficient also vanishes. Similarly every `yw` and `zw` coefficient vanishes.

Therefore every `q_r` can contain only

`xy, yz, zx, w^2`.

But the square of a linear combination of these four monomials can never produce an `xyzw` term: such a term would require one of the forbidden pairings

`(xy)(zw)`, `(yz)(xw)`, or `(zx)(yw)`.

Hence every sum `sum q_r^2` has zero `xyzw` coefficient, contradicting the coefficient `-4` in (11.1).

Thus

**(11.3)** `F` is nonnegative but not SOS.

This supplies a concrete rational boundary: once quotient dimension reaches four, a generic homogeneous quartic realized slack cannot be declared lossless merely because no PSD quadratic Gram matrix was found.

Important scope qualification: this does **not** prove that every P5 structural slack in dimension four can realize (11.1). A special factor/product identity could still enforce SOS for a narrower source family. What fails is the dimension-only inference that was valid for ternary quartics.

---

# Part VII — minimal theorem statements for formalization

## 12. Suggested theorem interface A — coefficient map

A minimal algebraic theorem can avoid polynomial quotient machinery entirely:

`ternaryQuartic_gram_identity`

Inputs:

- coefficients `a b c d e f g h i j k l m n o : R`;
- gauges `t1 ... t6 : R`;
- `x y z : R`.

Conclusion:

`monomial6(x,y,z)^T * G(coeff,gauge) * monomial6(x,y,z)`

`= 2 * quartic15(coeff,x,y,z)`.

Proof should be `ring` after expanding the fixed matrix.

## 13. Suggested theorem interface B — PSD consumption

`ternaryQuartic_nonneg_of_gram_psd`

Assume

`G(t)>=0`.

Conclude

`p(x,y,z)>=0` for all states.

This direction is elementary and does not require formalizing Hilbert's theorem.

The reverse direction

`p>=0 -> exists t, G(t)>=0`

is the genuinely deep ternary-quartic SOS theorem. It should be kept as a named mathematical dependency until a formal library theorem or a dedicated proof is available; do not disguise it as coefficient algebra.

## 14. Suggested theorem interface C — rational strict serialization

At the exact-real mathematical layer:

`positive_ternary_quartic_exists_pd_gram`

and downstream, after a rational-density argument,

`rational_positive_ternary_quartic_exists_rational_pd_gram`.

The checker-facing packet then stores only:

- the fifteen rational quartic coefficients;
- six rational Gram gauges;
- six positive leading principal minors (or the full integer matrix from which they are recomputed).

## 15. Suggested theorem interface D — quotient chart

`ternaryGram_congr_of_linear_chart`

with

`m(Pv)=S2(P)m(v)`

and

`Gv=S2(P)^T Gu S2(P)`.

For rational reverse transport, add the adjugate identity (9.5).

---

# Part VIII — failure classifier and remaining boundaries

## 16. Exact fail-closed routing

For the ternary homogeneous branch:

- supplied `t` with `G(t)>=0` -> exact mathematical PASS for the realized quartic;
- strict supplied rational `t` with six positive leading minors -> exact strict PASS;
- one candidate `t` fails PSD -> search remains open;
- exact state `u` with `p(u)<0` -> mathematical FAIL;
- six-parameter Gram feasibility proved empty -> by Hilbert, mathematical FAIL for a ternary quartic;
- quotient dimension `>=4` and Gram search empty -> **inconclusive**, unless a special source theorem proves SOS completeness for that narrower structural family or a negative physical state is produced.

## 17. Scope boundaries

This review does not cover:

1. affine/nonhomogeneous realized slack;
2. extra unresolved kernel/cell parameters entering the fifteen coefficients;
3. off-center source regions where radial scaling no longer converts local negativity into a near-origin witness;
4. source-dependent coefficient uncertainty requiring uniform Gram parameters across a cell;
5. deployed quotient extraction and same-key `M/W/A` identity;
6. actual cell/tube/trajectory/flowpipe/stencil coverage;
7. Float64/interval semantics;
8. Lean/kernel compilation;
9. independent verification by `封不觉`;
10. admission, registry, or parent closure.

## 18. Next distinct mathematical seam

The highest-value next bridge is **uniform cell-dependent ternary Gram selection**.

If the fifteen quartic coefficients depend affinely/polynomially on a source parameter `s` over a certified cell, pointwise Hilbert feasibility gives `exists t(s)` but does not automatically give one constant rational Gram gauge or a polynomial/rational selector usable by a finite checker.

A useful next child would separate three cases:

1. one constant gauge `t` works for the whole coefficient polytope;
2. an affine/polynomial selector `t(s)` preserves PSD over the cell;
3. pointwise SOS holds but no chosen finite selector class is adequate, which must route to `INCONCLUSIVE_FROM_SELECTOR` rather than physical FAIL.

This is materially different from another fixed-coefficient Gram derivation and connects directly to the unresolved source/cell layer.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.