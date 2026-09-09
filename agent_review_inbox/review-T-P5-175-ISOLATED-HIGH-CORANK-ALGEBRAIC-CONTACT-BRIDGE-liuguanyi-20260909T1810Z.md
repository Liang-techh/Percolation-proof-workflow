---
kind: review_result
review_id: review-T-P5-175-isolated-high-corank-algebraic-contact-bridge-liuguanyi-20260909T1810Z
task_id: T-P5-175-ISOLATED-HIGH-CORANK-ALGEBRAIC-CONTACT-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T18:10:00Z
claim_commit: c17f16454c37de4cf16e40c0a91a34aae25fd1ab
inspected_commit: 53505fb0f54df1af5b65ed43a5d36f06316dc5f8
upstream_commits:
  - 09a09a9df2b409fedc2cac32ad483e6baa005e5c  # T-P5-174 high-corank fixed-candidate contact alternative
  - c4e82b5839bc037672c73635775399632e515406  # T-P5-172 rank-two minor / symbolic pivot corridor
  - 1b63698a429d0b2530de38e6632d29076b52e475  # T-P5-173 corank-one strict-complementarity minors
  - 8caf78bf7ce97b3a727a46c12739583a12d777f7  # T-P5-171 contact/KKT pivot transport
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_isolated_high_corank_algebraic_contact_packet; use_fraction_free_kernel_basis_and_bordered_minors; certify_quadratic_algebraic_floor_without_explicit_root; keep_persistent_high_corank_stratum_as_separate_open_branch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional determinant/adjugate algebra; exact SymPy rational-polynomial regression for Section 8
exit_code: 0 for exact symbolic regression; no Lean/kernel run
---

# T-P5-175 — isolated high-corank algebraic contact bridge

## 0. Verdict and exact seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-174 reduces a fixed higher-corank active contact to the exact linear cone problem

`A z = 0`, `z > 0`, `R z > 0`,

but explicitly leaves the symbolic-floor case open because with `A=A_D` the equation `A_D z=0` is bilinear in `(D,z)`. T-P5-172 independently proves that every square minor of the P5 additive-floor pencil is only degree at most two in `D`.

This review closes the missing bridge **when the higher-corank rank drop occurs at an isolated floor candidate**.

The central result is that one never has to solve the bilinear system in `(D,z)` directly. At an isolated candidate `alpha`:

1. `alpha` is necessarily rational or quadratic algebraic;
2. one nonsingular principal pivot minor produces a **fraction-free polynomial kernel basis**;
3. every unsatisfied active row and every inactive KKT residual of that basis is an original bordered minor, hence degree at most two in `D`;
4. the exact contact can therefore be certified by a rational minimal polynomial `p(D)`, a rational isolating interval, polynomial divisibility/remainder checks, and one **rational** coefficient vector in the kernel basis;
5. the algebraic number `alpha` and the irrational contact state never need to be represented inside the trusted checker.

The remaining genuinely different branch is a **persistent high-corank stratum**, where all rank-detecting minors vanish identically as polynomials in `D`. That is not an isolated algebraic contact and is intentionally left open.

No source/provenance audit, runtime/Float64 claim, Lean/kernel validation, independent re-audit, admission, registry mutation, or parent closure is performed.

---

## 1. Setup: the active/inactive floor pencil

Let

`M_D = M_0 + D L_g`,

with rational symmetric `M_0` and

`L_g = (g 1^T + 1 g^T)/2`.

Fix an active support `S` of size `m`, and let `T` denote the inactive indices. Write

`A_D := M_D[S,S]`,

`R_D := M_D[T,S]`.

T-P5-172 proves the following fact for this family:

> for any row set `I` and column set `J` of the same cardinality, `det M_D[I,J]` is a rational polynomial of degree at most two in `D`.

This includes principal, almost-principal, row-replacement, and bordered minors.

Suppose a real candidate `alpha` satisfies

`A_alpha >= 0`,

`rank(A_alpha)=r`,

with high corank

`k := m-r >= 2`.

The PSD premise is automatic when this active block comes from a positive-support zero contact of a globally copositive candidate, by T-P5-173. Here it is kept explicit because this review is only the contact bridge.

---

## 2. Isolated higher-corank rank drops are at most quadratic algebraic

At a rank-`r` candidate, every `(r+1) x (r+1)` minor of `A_alpha` vanishes.

### Theorem T175-A — `isolated_rank_drop_degree_le_two`

Assume there exists at least one `(r+1) x (r+1)` minor polynomial

`q(D) = det A_D[I,J]`

which is **not identically zero**.

Then:

1. `q(alpha)=0`;
2. `deg q <= 2`;
3. therefore `alpha` is rational or algebraic of degree two over `Q`;
4. the set of nearby `D` with `rank(A_D)<=r` is discrete at `alpha`.

### Proof

Rank `r` gives `q(alpha)=0`. T-P5-172 gives `deg q<=2`. A nonzero univariate polynomial of degree at most two has finitely many real roots. The minimal polynomial of `alpha` over `Q` divides `q`, so its degree is at most two. QED.

### Exact interpretation of “isolated”

For the present one-parameter family, the relevant alternative is sharp:

- if **some** `(r+1)`-minor polynomial is nonzero, every rank-`<=r` candidate is contained in a finite rational/quadratic algebraic set;
- if **all** `(r+1)`-minor polynomials vanish identically, then `rank(A_D)<=r` for every `D` and the high-corank geometry is persistent rather than isolated.

Thus the symbolic problem splits before any kernel calculation.

---

## 3. A nonsingular principal pivot exists on the PSD active block

Because `A_alpha>=0` and has rank `r`, there exists a principal index set

`P subset S`, `|P|=r`,

such that

`B_alpha := A_alpha[P,P] > 0`.

For PSD matrices this follows, for example, from a Gram representation: select `r` linearly independent Gram vectors; their principal Gram block is positive definite.

Let

`F := S \ P`, `|F|=k`,

and define polynomial blocks

`B_D := A_D[P,P]`,

`C_D := A_D[P,F]`,

`Delta(D) := det B_D`.

Then

`Delta(alpha)>0`.

By T-P5-172, `Delta(D)` has degree at most two, regardless of `r`.

The important point is that the producer only needs to identify one such pivot set `P`; no eigenbasis or pseudoinverse is required.

---

## 4. Fraction-free kernel basis

For each free index `f in F`, let `c_f(D)` denote column `f` of `C_D`. Define an active vector `z^(f)(D)` by

`z^(f)_P(D) := - adj(B_D) c_f(D)`,

`z^(f)_f(D) := Delta(D)`,

`z^(f)_{f'}(D) := 0` for `f' in F`, `f' != f`.

### Theorem T175-B — `fraction_free_kernel_pivot_rows`

For every real `D`, the pivot rows vanish identically:

`(A_D z^(f)(D))_P = 0`.

### Proof

Using `B adj(B)=det(B) I`,

`B_D[-adj(B_D)c_f] + c_f Delta`

`= -Delta c_f + Delta c_f`

`=0`.

No division and no assumption `Delta!=0` is needed for this polynomial identity. QED.

### Degree control for the state coordinates

A naive expansion of `adj(B_D)c_f(D)` appears capable of producing high degree. That is another representation artifact.

For a pivot coordinate `i in P`, the scalar

`(adj(B_D)c_f(D))_i`

is, up to the fixed column-order sign, the determinant obtained from `B_D` by replacing its `i`-th column with the active column `f`. It is therefore an original square minor of `A_D`.

Hence every coordinate of every `z^(f)(D)` has degree at most two in `D`.

This is the fraction-free analogue of Cramer's rule, but the checker never divides by `Delta`.

---

## 5. The remaining active equations are bordered minors

Take any free row `g in F`. Direct expansion gives

`(A_D z^(f)(D))_g`

`= Delta(D) A_D[g,f] - A_D[g,P] adj(B_D) A_D[P,f]`.

Define the bordered minor, using the fixed ordering `P` followed by the new index,

`Gamma^A_{g,f}(D)`

`:= det A_D[P ++ [g], P ++ [f]]`.

### Theorem T175-C — `fraction_free_active_residual_eq_bordered_minor`

`(A_D z^(f)(D))_g = Gamma^A_{g,f}(D)`.

Therefore

`deg Gamma^A_{g,f} <= 2`.

At `D=alpha`, because `rank(A_alpha)=r` and `Delta(alpha)!=0`, every such `(r+1)`-minor vanishes:

`Gamma^A_{g,f}(alpha)=0`.

Consequently each `z^(f)(alpha)` is in `ker(A_alpha)`.

Moreover the free-coordinate block of these vectors is exactly

`Delta(alpha) I_k`.

Since `Delta(alpha)!=0`, the `k` vectors are linearly independent. As `nullity(A_alpha)=k`, they form a basis of the complete active kernel.

Thus the exact kernel basis is recovered from minors alone.

---

## 6. Inactive KKT residuals are the same kind of minors

For `t in T`, define

`Gamma^R_{t,f}(D)`

`:= det M_D[P ++ [t], P ++ [f]]`.

The row set now uses the inactive row `t`, while the columns remain active.

### Theorem T175-D — `fraction_free_inactive_residual_eq_bordered_minor`

`(R_D z^(f)(D))_t = Gamma^R_{t,f}(D)`.

Again

`deg Gamma^R_{t,f} <= 2`.

Therefore both sides of the strict-contact problem are encoded by the same typed object:

> **original square minors of the rank-two floor pencil.**

There is no separate algebraic-number KKT layer.

For coefficients `c=(c_f)_{f in F}`, define

`z_c(D) := sum_f c_f z^(f)(D)`.

Then every active coordinate of `z_c(D)` and every inactive residual of `R_D z_c(D)` is a polynomial of degree at most two whenever `c` is rational.

---

## 7. Root-free exact packet at a quadratic algebraic floor

Let `p(D) in Q[D]` be the minimal polynomial of the isolated candidate `alpha`, with

`deg p in {1,2}`.

For the quadratic case, let `[L,U]` be a rational isolating interval containing exactly the chosen real root `alpha` of `p`.

The producer need not serialize `alpha` itself.

### 7.1 Exact active closure by polynomial remainder

Each active bordered residual `Gamma^A_{g,f}` has rational coefficients. Since `p` is the minimal polynomial,

`Gamma^A_{g,f}(alpha)=0`

iff

`Gamma^A_{g,f}(D) mod p(D) = 0`.

This is exact rational polynomial arithmetic.

For a candidate packet it is enough to check this divisibility for all `g,f` needed by the selected fraction-free basis.

### 7.2 Exact pivot nondegeneracy without evaluating alpha

Reduce `Delta(D)` modulo `p(D)`.

- if `deg p=1`, this is direct rational evaluation;
- if `deg p=2`, the remainder is affine, say `a+bD`.

Because `alpha in [L,U]`, a sufficient exact lower bound is

- if `b>=0`, check `a+bL>0`;
- if `b<=0`, check `a+bU>0`.

Then `Delta(alpha)>0`.

Any genuinely positive `Delta(alpha)` admits such a certificate after shrinking the rational isolating interval, so this interface is complete for strict positivity.

### 7.3 Exact state/residual positivity

Do the same for every active coordinate polynomial `q_i(D)` of `z_c(D)` and every inactive residual polynomial `s_t(D)` of `R_D z_c(D)`:

1. compute the remainder modulo `p`;
2. in the quadratic case the remainder is affine;
3. lower-bound that affine function on `[L,U]` by the appropriate rational endpoint;
4. require the lower bound to be strictly positive.

This proves

`z_c(alpha)>0`,

`R_alpha z_c(alpha)>0`

without a square root, algebraic-number comparison, eigenvector, or pseudoinverse.

### 7.4 Isolating the root itself

For a quadratic `p`, the usual rational endpoint/derivative checks suffice. For example, if `p(L)<0<p(U)` and `p'` has fixed positive sign on `[L,U]`, then exactly one root lies in the interval.

This is the same root-free polynomial-sign style already used by T-P5-172.

---

## 8. Strict feasibility implies a rational coefficient witness

At first sight, an irrational candidate `alpha` might seem to require algebraic coefficients `c_f` in the kernel basis. It does not.

### Theorem T175-E — `strict_algebraic_kernel_contact_has_rational_basis_coefficients`

Assume the fraction-free basis above is valid at `alpha` and there exists some real coefficient vector `c_0` such that

`z_{c_0}(alpha)>0`,

`R_alpha z_{c_0}(alpha)>0`.

Then there exists a **rational** coefficient vector

`c in Q^k`

with the same strict inequalities.

### Proof

Stack the active coordinates and inactive residuals into a real matrix `H_alpha` acting on the basis coefficients. The feasible set is

`Omega := { c in R^k : H_alpha c > 0 }`.

It is an open subset of `R^k`, because it is a finite intersection of strict linear half-spaces. By assumption `c_0 in Omega`, so some Euclidean ball around `c_0` lies in `Omega`. Rational vectors are dense in `R^k`; choose `c in Q^k` in that ball. QED.

### Why this matters for the interface

Even when

- the sharp floor `alpha` is irrational, and
- the physical contact state `z(alpha)` is irrational,

producer/checker exchange can remain entirely rational:

- rational polynomial `p`;
- rational isolating interval `[L,U]`;
- rational pivot/minor polynomials;
- rational coefficient vector `c`;
- rational remainder and endpoint sign checks.

The irrationality lives only in the semantic statement “the unique root of `p` in `[L,U]`”.

---

## 9. Exact rational regression: an irrational corank-two contact

This example fixes the seam with no floating assumptions.

Take the active three-coordinate loading vector

`g=(2,-2,0)`

and define

`A_D = A_0 + D L_g`,

where

`A_0 = [[ 3,-1,1],`
`       [-1, 3,1],`
`       [ 1, 1,1]]`,

`L_g = [[ 2, 0, 1],`
`       [ 0,-2,-1],`
`       [ 1,-1, 0]]`.

Thus

`A_D = [[3+2D,   -1, 1+D],`
`       [   -1, 3-2D, 1-D],`
`       [ 1+D,  1-D,   1]]`.

Let

`p(D)=D^2-2`,

and select the positive root

`alpha=sqrt(2)`

only semantically, via the rational isolating interval

`I=[7/5,10/7]`.

Indeed

`p(7/5)=-1/25<0`,

`p(10/7)=2/49>0`,

and `p'(D)=2D>0` on `I`, so there is exactly one root in `I`.

At that root,

`A_alpha = u u^T`,

with

`u=(1+alpha,1-alpha,1)`.

Hence `A_alpha>=0` and `rank(A_alpha)=1`, so its corank is two.

One nonzero rank-detecting minor is

`det A_D[{1,2},{1,2}] = -4(D^2-2) = -4p(D)`.

So the higher-corank candidate is genuinely isolated and quadratic algebraic.

Choose pivot set

`P={2}`.

Then

`Delta(D)=3-2D`.

On `I`, since `Delta` is decreasing,

`Delta(alpha) >= Delta(10/7)=1/7>0`.

The two fraction-free basis vectors are

`z^(1)(D)=(3-2D, 1, 0)`,

`z^(3)(D)=(0, D-1, 3-2D)`.

Exact multiplication gives

`A_D z^(1)(D)=(-4p(D), 0, -2p(D))`,

`A_D z^(3)(D)=(-2p(D), 0, -p(D))`.

Thus both become exact kernel vectors at the isolated root.

Now take the rational coefficient vector

`c=(1,1)`.

Then

`z_c(D)=(3-2D, D, 3-2D)`.

All active coordinates are strictly positive at the root by rational interval checks:

`3-2alpha >= 1/7>0`,

`alpha >= 7/5>0`.

Add one inactive row

`R_D=(1+D, 2-D, 0)`.

This row is compatible with the same affine floor loading, e.g. with inactive loading coordinate `g_4=0` and rational base row `(1,2,0)`.

The signed inactive residual is

`R_D z_c(D) = -3D^2+3D+3`.

Modulo `p(D)` this becomes

`3D-3`.

On the isolating interval it is increasing, so

`R_alpha z_c(alpha) >= 3*(7/5)-3 = 6/5 > 0`.

Therefore this is an exact **strict** higher-corank contact at an irrational floor, certified using only rational data.

The physical state is irrational,

`z_c(alpha)=(3-2sqrt(2), sqrt(2), 3-2sqrt(2))`,

but the coefficient packet is simply `c=(1,1)`.

This example also shows why “symbolic high corank” is not inherently a bilinear algebraic-number problem: after the fraction-free basis choice, every necessary equality is divisibility by `p` and every strict inequality is a one-dimensional rational sign check.

---

## 10. Minimal exact theorem packet

The reusable mathematical layer can be stated as follows.

### T175-A — isolated rank-drop degree

For the rank-two affine pencil, if `rank(A_alpha)=r` and some `(r+1)`-minor polynomial is nonzero, then `alpha` has algebraic degree at most two.

### T175-B — fraction-free kernel basis

For `Delta=det A[P,P]`, define

`z^(f)_P=-adj(B)A[P,f]`, `z^(f)_f=Delta`.

Then pivot rows vanish identically.

### T175-C — active bordered-minor closure

For `g,f in F`,

`(A z^(f))_g = det A[P++g, P++f]`.

### T175-D — inactive bordered-minor residual

For inactive `t`,

`(R z^(f))_t = det M[P++t, P++f]`.

### T175-E — rational coefficient density

If one real linear combination of the basis has strictly positive active coordinates and inactive residuals at `alpha`, then one rational coefficient vector does too.

### T175-F — root-free algebraic contact packet

Given:

1. rational `p(D)` of degree one or two and a rational isolating interval for `alpha`;
2. a pivot set `P` with root-free proof `Delta(alpha)>0`;
3. zero polynomial remainders modulo `p` for every active bordered residual;
4. a rational coefficient vector `c`;
5. positive interval lower bounds for every active coordinate and inactive residual remainder;

conclude

`A_alpha z_c(alpha)=0`,

`z_c(alpha)>0`,

`R_alpha z_c(alpha)>0`.

If a separate candidate-matrix copositivity PASS is available, this is a strict orthant-KKT zero contact and can be handed to T-P5-169/T-P5-171 for sharp-floor and transport consumers.

---

## 11. Suggested typed producer/checker interface

A minimal packet need only contain:

- `parameter_key`, `support_key`, `matrix_family_key`;
- rational coefficients of the affine rank-two pencil;
- active support `S`, inactive set `T`;
- rational `p(D)` and rational isolating endpoints `L,U`;
- one nonzero `(r+1)` rank-drop minor showing the isolated branch and its factor/divisibility relation to `p`;
- pivot set `P` and `Delta(D)`;
- fraction-free basis minor polynomials, or enough source entries for the checker to reconstruct them;
- exact `Gamma^A mod p = 0` checks;
- rational coefficient vector `c`;
- exact lower-bound certificates for `Delta`, active coordinates, and inactive residuals on `[L,U]`.

The checker does **not** need:

- an explicit algebraic-number object for `alpha`;
- eigenvalues/eigenvectors;
- a pseudoinverse;
- Gaussian elimination over `Q(alpha)`;
- square roots;
- floating root finding;
- a normalized contact vector.

---

## 12. Boundaries and remaining obligations

### Boundary A — persistent high-corank strata remain open

If every `(r+1)` rank-detecting minor vanishes identically as a polynomial in `D`, then `rank(A_D)<=r` for the whole parameter family. There is no isolated minimal polynomial generated by the rank drop.

That branch needs a separate common-kernel / rational-subspace / Grassmann-style transport theorem. T175 does not claim it.

### Boundary B — further rank drops inside a persistent stratum

If rank is persistently `<=r` but drops below `r` at isolated points, one may reapply the same logic using the next size of minors. The producer must explicitly state which rank stratum and pivot size are being certified; it must not silently reuse a pivot whose `Delta` vanishes at the candidate.

### Boundary C — non-strict contact

The rational-coefficient theorem relies on an **open** strict feasibility set. If some desired active coordinate or inactive residual is allowed to be exactly zero, rational density alone does not preserve the equality/face constraints. T-P5-174 already separates strict from non-strict contact; that separation remains necessary.

### Boundary D — dual obstruction at an irrational candidate

T-P5-174's fixed-candidate Gordan/Stiemke obstruction still applies semantically at `alpha`, but a dual equality witness need not admit rational coefficients. A root-free dual packet can be built over `Q(alpha)` using degree-`<2` polynomial representatives, but that is not required for the present primal strict-contact bridge and is left as a possible child.

### Boundary E — global copositivity

The contact packet does not prove that `M_alpha` is copositive away from the contact. Global PASS remains a separate T-P5-158/165/168/170-style obligation.

### Boundary F — source/runtime/formal gates

Actual source matrix binding, uncertainty/cell coverage, Float64/reification, ODE/P8/M4 semantics, Lean/kernel compilation, independent validation by 封不觉, admission, and registry mutation all remain OPEN.

---

## 13. Practical routing recommendation

The symbolic contact branch can now be split without algebraic ambiguity:

1. **corank one:** use T-P5-173 adjugate/minor gates;
2. **isolated corank >=2:** use T-P5-175 fraction-free basis + minimal-polynomial packet;
3. **persistent corank >=2:** do not force an isolated-root interface; open a separate common-kernel/stratification child;
4. after any contact packet, keep global copositivity and physical/source binding independent.

The important interface lesson is:

> **an irrational sharp floor does not require an irrational proof packet.**
>
> In the isolated higher-corank branch, exact rational polynomial data plus a rational isolating interval and a rational kernel-cone coefficient vector are sufficient.