---
kind: review_result
review_id: review-T-P5-172-low-degree-symbolic-pivot-corridor-guyuefangyuan-20260909T1737Z
task_id: T-P5-172-LOW-DEGREE-SYMBOLIC-PIVOT-CORRIDOR
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T17:37:00Z
claim_commit: ca639f69709650e80c22d44a0b3682ac38c373b6
inspected_commit: 5b6319375f07b2d8149d6523741204eb20019be1
upstream_commits:
  - f1eb76d8657edac28a04aaec289a7198a8c648d1  # T-P5-170 iterated sign-compatible pivot energy chain
  - 8caf78bf7ce97b3a727a46c12739583a12d777f7  # T-P5-171 contact/KKT pivot transport
  - 7024791953977bb79404d788d3d1246a20a37a57  # T-P5-160 degenerate support/kernel branch
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: replace_recursive_symbolic_D_expansion_by_original_principal_and_almost_principal_minor_gates; use_rank_two_floor_loading_to_cap_every_gate_degree_at_two; certify_rational_D_corridors_with_root_free_quadratic_interval_lemmas; retain_T170_fixed_candidate_chain_and_T171_contact_lift_as_consumers
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional determinant/Schur algebra; local SymPy exact-rational regression for Section 7 only
exit_code: 0 for exact symbolic regression; no Lean/kernel run
---

# T-P5-172 — low-degree symbolic pivot corridor via original minors

## 0. Verdict and exact seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-170 makes a fixed sign-compatible pivot chain an exact copositivity reduction, and T-P5-171 transports a terminal zero contact/KKT witness back to the original support. T-P5-171 correctly leaves one symbolic search issue open: if the additive floor parameter `D` is kept symbolic and one recursively forms the **scaled** reduced matrices, their displayed entries acquire higher polynomial degree, so stage sign gates appear to become increasingly expensive algebraic conditions.

For the actual P5 additive-floor pencil this degree growth is a representation artifact.

Write

`M_D = M_0 + D L_g`,

where

`L_g = (g 1^T + 1 g^T)/2`.

The loading matrix has rank at most two. This review proves that for any **fixed pivot order**:

1. every positive-pivot gate is the sign of an original principal minor of `M_D`;
2. every pivot-row sign-compatible gate is the sign of an original almost-principal minor of `M_D`;
3. every one of those minors is a polynomial in `D` of degree at most two;
4. therefore a whole symbolic pivot-order corridor is exactly a finite intersection of rational quadratic sign conditions, even though the recursively scaled matrices may display cubic, quartic, or higher positive-prefactor products;
5. nonnegativity/positivity of each quadratic on a rational interval has a root-free exact checker using only endpoint values, derivative signs, and the discriminant expression `4ac-b^2`.

Thus the T-P5-170/T-P5-171 chain does **not** require a high-degree symbolic algebraic solver for the one-parameter additive-floor search. High degree can be stripped away before the checker by returning to original minors.

No source/provenance audit, runtime/Float64 claim, Lean/kernel validation, independent re-audit, admission, or registry mutation is performed.

---

## 1. The additive-floor pencil has rank-two parameter loading

Let `n>=1`, let `g in R^n`, and let `1` denote the all-ones vector. Define

**(1.1)** `L_g := (g 1^T + 1 g^T)/2`.

Then

**(1.2)** `rank(L_g) <= 2`.

The P5 homogeneous floor matrix has the form

**(1.3)** `M_D = M_0 + D L_g`.

On the simplex `1^T lambda=1`, the loading contributes

`lambda^T (D L_g) lambda = D (1^T lambda)(g^T lambda) = D g^T lambda`,

which is exactly the additive floor term already used in T-P5-153/154 and descendants.

The rank-two fact is not merely a global matrix statement. For arbitrary row and column index sets `I,J` of the same size,

**(1.4)**

`L_g[I,J]
 = (g_I 1_J^T + 1_I g_J^T)/2`,

so the parameter-dependent columns of every square submatrix still lie in the two-dimensional span of `g_I` and `1_I`.

---

## 2. Every square minor, including almost-principal minors, has degree at most two

Let `I,J` be index lists of the same cardinality `r`, with fixed ordering. Define

**(2.1)**

`P_{I,J}(D) := det(M_D[I,J])`.

### Theorem T172-A — `rankTwoPencil_minor_degree_le_two`

For every `I,J`, there exist coefficients `c0,c1,c2` such that

**(2.2)**

`P_{I,J}(D) = c0 + c1 D + c2 D^2`.

In particular this holds not only for principal minors `I=J`, but also for the almost-principal minors needed to read Schur off-diagonal signs.

### Proof

Expand the determinant by multilinearity in the columns. In each selected column, the `D`-dependent part belongs to

`span{g_I, 1_I}`.

Any term containing `D` from three or more columns therefore has at least three chosen columns lying in a subspace of dimension at most two. Those columns are linearly dependent, so that determinant term is zero.

Hence no term of degree `D^k` with `k>=3` survives. QED.

### Relation to T-P5-160

T-P5-160 already observed degree at most two for principal determinants of this loading family. T172-A is the needed extension to **arbitrary square minors**, especially bordered/almost-principal minors. That extension is what controls pivot-row sign gates rather than only contact roots.

### Boundary

The conclusion depends on the one-parameter perturbation having rank at most two. If the deployed family is changed to include an additional independent `D`-dependent matrix not contained in this rank-two span, the degree-two conclusion must be recomputed; it must not be inherited by name.

---

## 3. Schur entries are ratios of original bordered minors

Fix an eliminated index set `P` and write, in the order `P` first,

`B := M_D[P,P]`.

Let

**(3.1)** `Delta_P(D) := det(B)`.

For two retained indices `i,j`, define the bordered minor

**(3.2)**

`Gamma_{P;i,j}(D)
 := det M_D[P ++ [i], P ++ [j]]`,

where the row order is `P` followed by `i` and the column order is `P` followed by `j`. This fixed ordering removes any hidden permutation sign.

If `Delta_P != 0`, let `S_P` denote the ordinary Schur complement after eliminating `P`.

### Theorem T172-B — `borderedMinor_eq_det_mul_schurEntry`

**(3.3)**

`Gamma_{P;i,j} = Delta_P * (S_P)_{ij}`.

For `i=j`, this is simply

**(3.4)**

`Delta_{P union {i}} = Delta_P * (S_P)_{ii}`.

### Division-free form

The identity can be stored without an inverse:

**(3.5)**

`Gamma_{P;i,j}
 = Delta_P M_{ij}
   - M_{iP} adj(B) M_{Pj}`.

When `Delta_P != 0`, (3.3) follows from `B^-1=adj(B)/Delta_P`; however a trusted checker may use (3.5) directly and never compute an inverse.

The same determinant identity is valid over exact rationals before any numerical evaluation.

---

## 4. Exact sign corridor for a fixed T-P5-170 pivot order

Fix a pivot order

`p_1, ..., p_m`.

Let

`P_k := {p_1,...,p_k}`

with `P_0=empty`. T-P5-170 recursively constructs a **scaled** current matrix, not the normalized Schur complement. Let that current matrix after `k` eliminations be `N_k`.

The only fact we need about its scale is the following.

### Lemma T172-C — `scaledReduction_is_positiveScale_schur`

Assume all previous pivot diagonals are positive. Then there exists `c_k>0` such that

**(4.1)**

`N_k = c_k S_{P_k}`.

Proof is by induction. At `k=0`, `c_0=1`. If `N_k=c_k S` and the next normalized Schur pivot is `delta>0`, then the scaled T-P5-170 reduction is

`N_{k+1}=c_k^2 delta S_{P_{k+1}}`,

so the new scale is again positive.

No explicit closed form for `c_k` is needed by the checker.

### Theorem T172-D — `fixedPivotOrder_corridor_iff_originalMinorSigns`

Assume the preceding principal determinants are positive. At stage `k`, with proposed pivot `p=p_{k+1}`:

**pivot positivity**

`(N_k)_{pp} > 0`

iff

**(4.2)** `Delta_{P_k union {p}}(D) > 0`;

and for every retained `j`,

**sign-compatible pivot edge**

`(N_k)_{pj} <= 0`

iff

**(4.3)** `Gamma_{P_k;p,j}(D) <= 0`.

### Proof

By T172-C and T172-B,

`(N_k)_{pj}
 = c_k Gamma_{P_k;p,j}/Delta_{P_k}`.

Both `c_k` and `Delta_{P_k}` are positive, so the sign is exactly the sign of the bordered minor. Taking `j=p` gives the principal-determinant ratio and proves (4.2). QED.

### Consequence: exact corridor description

A fixed pivot order is valid at parameter `D` exactly when the finite family of conditions

**(4.4)**

`Delta_{P_{k+1}}(D) > 0`

and

**(4.5)**

`Gamma_{P_k;p_{k+1},j}(D) <= 0`

holds for every stage and every retained `j`.

By T172-A, **every polynomial appearing in (4.4)-(4.5) has degree at most two**.

This is the main closure of the symbolic-`D` seam left by T-P5-171: the recursive scaled representation may become high-degree, but the mathematically equivalent sign corridor never needs polynomials above degree two.

---

## 5. Why the apparent degree explosion is only a positive-prefactor artifact

For intuition, let

`Delta_k := det M_D[P_k,P_k]`.

The normalized stage-`k` Schur entries are bordered minors divided by `Delta_k`. T-P5-170 clears the denominator at every step, and those denominator-clearing factors are themselves positive inside a valid corridor. Repeated clearing therefore multiplies later entries by products of earlier positive principal minors.

Those products can raise the displayed polynomial degree while changing **no sign**.

Thus the correct symbolic implementation rule is:

> never decide a stage sign from the fully expanded recursively scaled entry if the same sign can be read from its original bordered minor.

The former carries irrelevant positive factors; the latter is degree at most two.

This also makes symbolic expressions dramatically smaller and keeps exact rational arithmetic practical.

---

## 6. Root-free exact rational checker for a quadratic on an interval

Let

**(6.1)** `q(t)=a t^2+b t+c`

and let `L<=U` be rational endpoints.

### Theorem T172-E — `quadratic_nonneg_on_Icc_rootfree`

The condition `q(t)>=0` for every `t in [L,U]` can be decided without roots, division, or square roots by the following exhaustive cases.

1. **`a<=0`**: exact iff
   
   `q(L)>=0` and `q(U)>=0`.

2. **`a>0` and `2aL+b>=0`**: exact iff
   
   `q(L)>=0`.

3. **`a>0`, `2aL+b<0`, and `2aU+b<=0`**: exact iff
   
   `q(U)>=0`.

4. **`a>0`, `2aL+b<0<2aU+b`**: exact iff
   
   **(6.2)** `4ac-b^2>=0`.

The strict version `q>0` on the closed interval is obtained by replacing the controlling minimum inequality by `>0`.

To certify `q<=0`, apply the same theorem to `-q`.

### Algebraic proof ingredients

No calculus is required.

For the interior-vertex case,

**(6.3)**

`4a q(t) = (2at+b)^2 + (4ac-b^2)`.

For the increasing-left case,

**(6.4)**

`q(t)-q(L)
 = (t-L)(a(t+L)+b)`,

and `a(t+L)+b >= 2aL+b>=0`.

The decreasing-right case is analogous. For `a<=0`, the quadratic lies above its endpoint chord; equivalently the interpolation error is

`a(t-L)(t-U)>=0`

because both factors have opposite signs on `[L,U]` and `a<=0`.

Hence the whole fixed-order symbolic corridor can be certified by rational additions, multiplications, squares, and ordered comparisons only.

---

## 7. Exact three-dimensional regression: recursive cubic collapses to quadratic minors

Take

**(7.1)**

`M_0 = [[ 1,-3,-4],
        [-3,10,-2],
        [-4,-2,20]]`,

`g=(1,2,3)`.

Then

`M_D=M_0+D L_g`

has entries

`M11=1+D`,

`M12=-3+(3/2)D`,

`M13=-4+2D`,

`M22=10+2D`,

`M23=-2+(5/2)D`,

`M33=20+3D`.

Use the fixed pivot order `1`, then `2`.

The exact original-minor gates are

**first pivot diagonal**

**(7.2)** `Delta_1 = D+1`;

**first pivot row**

**(7.3)** `Gamma_{empty;1,2}=(3/2)D-3`,

**(7.4)** `Gamma_{empty;1,3}=2D-4`;

**second pivot diagonal**

**(7.5)**

`Delta_12 = -(1/4)D^2 + 21D + 1`;

**second pivot edge to coordinate 3**

**(7.6)**

`Gamma_{ {1};2,3}
 = -(1/2)D^2 + (25/2)D - 14`;

and the terminal scalar numerator is the original determinant

**(7.7)**

`Delta_123
 = -(73/4)D^2 + 665D - 192`.

All are degree at most two, exactly as predicted.

### Rational corridor around the sharp contact

On the rational interval

**(7.8)** `[1/4, 1/3]`,

we have

`Delta_1 >0`,

`Gamma_{empty;1,2}<0`,

`Gamma_{empty;1,3}<0`,

`Delta_12>0`,

`Gamma_{ {1};2,3}<0`.

Exact endpoint values include

`Delta_12(1/4)=399/64`,

`Delta_12(1/3)=287/36`,

`Gamma_{ {1};2,3}(1/4)=-349/32`,

`Gamma_{ {1};2,3}(1/3)=-89/9`.

Thus the pivot order is valid throughout this interval by T172-E.

Meanwhile

**(7.9)**

`Delta_123(1/4)=-1721/64 <0`,

`Delta_123(1/3)=995/36 >0`.

Its derivative surrogate

`2aD+b = 665-(73/2)D`

is positive throughout `[1/4,1/3]`, so there is exactly one root `D_*` in that interval. Conceptually,

`D_*=(1330-2 sqrt(428209))/73 ~= 0.2910464995`,

but the trusted checker never needs this radical: the rational bracket and monotonic quadratic sign proof suffice.

At `D_*`, the terminal one-dimensional core is zero while both pivots remain strictly valid. T-P5-170 therefore gives a copositive PASS and a terminal zero contact; T-P5-171 lifts that contact to the original support. Since the original additive loading is positive on every nonzero nonnegative ray (`g_i>0` here), the same contact makes every `D<D_*` fail. Hence this example has an exact sharp floor certified by the pivot chain.

### Naive recursive expansion really does raise degree

If one instead follows the raw T-P5-170 scaled matrices and eliminates the two pivots symbolically, the final displayed scalar is

**(7.10)**

`N_2(D)
 = (D+1) Delta_123(D)`

`= -(D+1)(73D^2-2660D+768)/4`,

which is cubic.

Inside the valid corridor `D+1>0`, this cubic has **exactly the same sign** as the quadratic original determinant (7.7). The extra degree is therefore pure positive-prefactor baggage, not new algebraic geometry.

This regression is the concrete reason to implement T172-D rather than recursively expanding the scaled chain.

---

## 8. First-pivot structural identity: the quadratic coefficient is rank-one negative

There is an additional useful sanity check specific to the first pivot.

Partition `g=(g_p,g_R)` and write

`h=(g_p 1+g_R)/2`.

If the pivot row is written in T-P5-170 form with

`r(D)=r_0-D h`,

then the `D^2` coefficient of the first scaled reduced matrix

`b(D)A(D)-r(D)r(D)^T`

is

**(8.1)**

`g_p L_{g_R}-h h^T`

`= -(1/4)(g_R-g_p 1)(g_R-g_p 1)^T`.

So the first reduced matrix is not an arbitrary quadratic pencil: its quadratic coefficient is negative semidefinite rank at most one. It vanishes exactly when all retained `g_i` equal the pivot weight `g_p`.

This identity is not needed for T172-D, but it is a useful producer regression and explains why homothetic/equal-weight cases are especially simple.

---

## 9. Exact obstruction and fail-closed boundaries

### 9.1 A fixed order need not remain valid globally in `D`

The original additive family is monotone on the nonnegative cone when `g_i>0`, but a **particular pivot order** need not be. A pivot off-diagonal can change sign as `D` moves. T172-D therefore certifies a semialgebraic corridor for one order; outside that corridor the dispatcher must try another order or another exact copositivity gate.

Failure of a pivot-row gate is not a mathematical FAIL of `M_D`.

### 9.2 Zero principal determinant is a real branch boundary

If some preceding `Delta_P(D)=0`, the positive-pivot Schur route is unavailable there. One must use T-P5-170's zero-pivot branch, T-P5-160's kernel logic, or another direct cone theorem. Do not divide by the vanishing minor and do not infer a sign by continuity without a separate proof.

### 9.3 Degree-two control is tied to the exact loading family

The theorem applies to `M_0+D L_g` and, more generally, to an affine one-parameter perturbation of rank at most two. Adding an independently parameterized matrix term, using a nonlinear `D`-dependence upstream, or changing the homogenization can raise the minor degree. The producer must expose the actual pencil, not merely a field named `floor`.

### 9.4 Positive `g` is not needed for the minor algebra, but is needed for sharp-floor monotonicity

T172-A through T172-D are algebraic and do not require `g_i>0`. However, the usual P5 conclusion that a zero contact at `D_*` makes every smaller `D` fail uses

`(1^T x)(g^T x)>0`

for nonzero `x>=0`. That is guaranteed by the intended `g_i>0` contract and must remain explicit.

---

## 10. Proposed source/checker packet

For a fixed candidate pivot order, the symbolic producer should **not** export recursively expanded reduced matrices as the primary sign evidence. It should export, under one exact key:

1. the original rational `M_0` and `g` (or exact coefficient witnesses for the same pencil);
2. ordered pivot index lists `P_k`;
3. each principal quadratic `Delta_{P_{k+1}}(D)`;
4. each required almost-principal quadratic `Gamma_{P_k;p_{k+1},j}(D)`;
5. coefficient triples `(a,b,c)` for those quadratics, recomputable from exact minors;
6. rational candidate intervals `[L,U]` and T172-E branch data proving the required sign throughout the interval;
7. separately, any terminal contact/root bracket and terminal-core copositivity proof consumed by T-P5-170/T-P5-171.

This packet keeps the trusted checker root-free and makes every symbolic sign gate degree at most two.

The source/coverage/runtime layers remain independent obligations.

---

## 11. Suggested Lean decomposition

The highest-value formal leaves are:

1. **`borderedMinor_eq_det_mul_schurEntry`**
   - finite symmetric matrix;
   - fixed ordered eliminated block and two retained indices;
   - preferably provide an adjugate/no-division form first.

2. **`scaledPivot_sign_iff_borderedMinor_sign`**
   - assume the prior principal determinant and current scale are positive;
   - transfer `>0` / `<=0` signs without expanding the recursive scale.

3. **`rankTwoAffinePencil_minor_degree_le_two`**
   - for a square minor of `A+D(uv^T+st^T)`;
   - determinant has no coefficient above degree two.
   - This can be formalized later if polynomial-matrix API is heavy; the checker may initially consume explicit coefficient identities generated and separately proved by `ring` for fixed dimensions.

4. **`quadratic_nonneg_on_Icc_rootfree`** and **`quadratic_pos_on_Icc_rootfree`**
   - pure `Real`/ordered-field lemmas;
   - use identities (6.3)-(6.4) and `nlinarith`;
   - these are likely the cheapest first formal targets.

5. **`fixedPivotOrder_valid_of_quadraticMinorCorridor`**
   - finite composition theorem connecting the quadratic sign packet to T-P5-170 stage hypotheses.

A practical Lean sequence is therefore: root-free scalar interval lemmas first, bordered-minor sign transport second, fixed-dimension rank-two determinant coefficients third, and only then a generic finite-dimensional polynomial theorem.

---

## 12. Requested next action

The mathematical bottleneck is now narrower than the one stated at the end of T-P5-171.

For symbolic additive-floor search:

- choose a fixed pivot order;
- compute **original** principal/almost-principal minors, not recursively expanded scaled entries;
- reduce every gate to a quadratic coefficient triple;
- use rational interval certificates from T172-E;
- at a candidate contact, return to the already-proved T-P5-170 fixed-candidate chain and T-P5-171 contact/KKT lift.

If a corridor gate changes sign, branch the pivot order there; do not interpret that event as failure of copositivity.

Actual `{M_0,g,D}` source identity, homothetic-floor binding, physical boundary attainability, runtime/Float64 semantics, domain coverage, Lean/kernel validation, 封不觉 independent verification, admission, and registry propagation all remain **open**.
