---
kind: review_result
review_id: review-T-P5-168-three-vertex-negative-path-exact-copositivity-guyuefangyuan-20260909T1630Z
task_id: T-P5-168-THREE-VERTEX-NEGATIVE-PATH-EXACT-COPOSITIVITY
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T16:30:00Z
claim_commit: a3bce58c530988f96fdaf5c031b56ae80069b8a5
inspected_commit: 95020a4c66f81ce0711d6c0cd83a1b13305c9dc0
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION-kuangmanmozun-20260909T1540Z.md
    commit: f1c26726dcc54201ced3886d51fe0d5f40102ad4
  - path: agent_review_inbox/review-T-P5-166-negative-forest-shared-diagonal-budget-honglianmozun-20260909T1602Z.md
    commit: fec7f1ad78ecff83ef62bc6e889f63bfbca97c59
  - path: agent_review_inbox/review-T-P5-167-robust-interval-negative-component-bridge-liuguanyi-20260909T1606Z.md
    commit: 4d501806e9a3581b3fcc122b5749a212a414c5c5
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: after_negative_component_factorization_try_sign_compatible_copositive_pivot_elimination_before_negative_skeleton_or_generic_KKT; for_three_vertex_negative_path_use_exact_rootfree_scaled_gate; preserve_positive_endpoint_rescue; never_promote_negative_skeleton_failure_to_math_failure_when_positive_nonedges_remain
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact ordered-field algebra and exact rational regressions only
exit_code: n/a
---

# T-P5-168 — exact three-vertex negative-path copositivity with positive endpoint rescue

## 0. Verdict and narrow seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-165 factors a fixed symmetric copositivity problem over connected components of the strictly negative off-diagonal graph. T-P5-166 then gives an exact shared-diagonal/leaf-Schur treatment of the **negative skeleton** when that graph is a forest, but deliberately states that failure of the negative skeleton is not failure of the original mixed-sign matrix: a positive nonedge may rescue the cone quadratic form. T-P5-167 separately transports the component split to robust correlated source families by certified lower bounds.

This review closes the smallest unresolved mixed-sign component left between those lanes:

> three vertices with negative edges `1--2` and `2--3`, but a nonnegative endpoint coupling `1--3`.

The main result is stronger than a one-off 3x3 calculation. It proves an exact **copositive pivot elimination** rule whenever the eliminated pivot has nonpositive couplings to all remaining nonnegative coordinates. Positive couplings among the remaining coordinates are retained exactly instead of being discarded as in the negative-skeleton fallback. The 3-vertex path then reduces to one root-free binary gate.

No source admission, provenance/receipt audit, runtime/Float64 claim, Lean/kernel validation, independent re-audit, registry mutation, or robust interval/source reification is performed here.

---

## 1. Exact sign-compatible copositive pivot elimination

Let `b>0`. Let `y` range over a finite-dimensional nonnegative orthant. Let `A=A^T` be any real symmetric form on the `y` variables, and let `r` be componentwise nonnegative. Consider

**(1.1)**

`q(t,y) := b t^2 - 2 t <r,y> + y^T A y`,

for `t>=0`, `y>=0`.

The sign assumption `r>=0` means the pivot row has off-diagonal entries `-r_i<=0` to every retained coordinate. No sign assumption is imposed on the entries of `A`.

Define the reduced quadratic form

**(1.2)**

`R(y) := b y^T A y - <r,y>^2`,

or equivalently the reduced matrix

**(1.3)** `S := b A - r r^T`.

### Theorem A — copositive pivot iff reduced form is copositive

Under `b>0` and `r>=0`, the following are equivalent:

1. `q(t,y)>=0` for every `t>=0`, `y>=0`;
2. `R(y)>=0` for every `y>=0`.

Equivalently, the original symmetric block matrix

`[[b,-r^T],[-r,A]]`

is copositive iff `bA-r r^T` is copositive.

### Proof — sufficiency

There is the exact division-free completion identity

**(1.4)**

`b q(t,y) = (b t - <r,y>)^2 + R(y)`.

If `R(y)>=0`, then the right side is nonnegative. Since `b>0`, `q(t,y)>=0`.

### Proof — necessity without division

Fix arbitrary `y>=0`. Since `r>=0`,

`s := <r,y> >=0`.

Use the original copositive form at the nonnegative test point

**(1.5)** `(t,Y)=(s,b y)`.

Then

`<r,Y>=b s`,

and direct expansion gives

**(1.6)**

`q(s,b y)
 = b s^2 - 2 b s^2 + b^2 y^T A y
 = b R(y)`.

Copositivity gives `bR(y)>=0`; because `b>0`, `R(y)>=0`.

QED.

### Why the sign assumption matters

The theorem is not the ordinary unconstrained Schur-complement theorem disguised as copositivity. It works because the unconstrained minimizer of the pivot coordinate,

`t*=<r,y>/b`,

is automatically nonnegative on the nonnegative cone when `r>=0`.

If the pivot has a **positive** off-diagonal coefficient, exact Schur elimination can fail. For example

`M=[[1,1],[1,0]]`

is copositive because `t^2+2ty>=0` for `t,y>=0`, but unconstrained Schur elimination of the first coordinate produces the negative scalar `-1`. Thus a checker must not apply Theorem A to an arbitrary pivot row; the nonpositive-row sign gate is essential.

### Zero-pivot boundary

If one negative pivot edge is present and `b=0`, copositivity is impossible. For instance if `p>0`, the slice

`a x^2 - 2 p x t`

at any fixed `x>0` tends to `-infinity` as `t->infinity`. Hence in the negative-path application below the middle diagonal is forced to be strictly positive.

---

## 2. Exact 3x3 negative-path theorem

Consider

**(2.1)**

`M = [[ a, -p,  c],
      [-p,  b, -q],
      [ c, -q,  d]]`,

with

**(2.2)** `p>0`, `q>0`, `c>=0`.

Thus the strict negative graph is exactly the path `1--2--3`, while the endpoint pair has a nonnegative coupling.

For `x=(x1,x2,x3)>=0`, write

`Q_M(x)=x^T M x`.

Use the middle coordinate as the sign-compatible pivot. Define the three reduced scalars

**(2.3)**

`A0 := a b - p^2`,

`D0 := b d - q^2`,

`C0 := b c - p q`.

Then the exact completion identity is

**(2.4)**

`b Q_M(x)
 = (b x2 - p x1 - q x3)^2
   + A0 x1^2 + 2 C0 x1 x3 + D0 x3^2`.

This is just Theorem A with `r=(p,q)` and endpoint block `[[a,c],[c,d]]`, but it is useful to keep the explicit formula because every coefficient can be exact rational in the P5 floor matrix.

### Theorem B — exact root-free criterion

Under (2.2), `M` is copositive **iff**

**(2.5)** `b>0`,

**(2.6)** `A0>=0`,

**(2.7)** `D0>=0`,

and

**(2.8)** `C0>=0  OR  C0^2 <= A0 D0`.

No square root, inverse, eigenvalue, determinant solve, SDP, or KKT support enumeration is required by the criterion.

### Proof

Because `p>0`, copositivity forces `b>0` by the zero-pivot argument above. Then Theorem A reduces the problem exactly to copositivity of the binary form

**(2.9)**

`B(x,z)=A0 x^2 + 2 C0 x z + D0 z^2`

on `x,z>=0`.

The coordinate axes force `A0>=0` and `D0>=0`.

If `C0>=0`, all three terms in (2.9) are nonnegative.

If `C0<0` and `C0^2<=A0D0`, then whenever `A0>0`,

**(2.10)**

`A0 B(x,z)
 = (A0 x + C0 z)^2
   + (A0D0-C0^2) z^2 >=0`.

If `A0=0`, the inequality `C0^2<=A0D0` forces `C0=0`, contradicting `C0<0`; so this branch is complete.

Conversely, assume `C0<0` and `C0^2>A0D0`. If `A0>0`, the nonnegative endpoint witness

`(x,z)=(-C0,A0)`

satisfies

**(2.11)** `B(x,z)=A0(A0D0-C0^2)<0`.

If `A0=0` and `D0>0`, use `(x,z)=(D0,-C0)`; if `A0=D0=0`, use `(1,1)`. Thus failure of (2.8) always gives a concrete nonnegative reduced witness.

To lift any reduced witness `(x,z)>=0` to the original 3-vector **without division**, use

**(2.12)**

`X = (b x, p x+q z, b z) >=0`.

For this vector the square in (2.4) vanishes after common scaling, and a direct expansion yields

**(2.13)**

`Q_M(X) = b B(x,z)`.

Therefore a negative reduced witness is a genuine negative copositivity witness for `M`.

QED.

---

## 3. Determinant interpretation and the genuinely copositive-but-indefinite branch

The reduced determinant has the exact identity

**(3.1)**

`A0 D0 - C0^2 = b det(M)`.

Therefore, once `b>0`, `A0>=0`, and `D0>=0`, the hard branch `C0<0` can equivalently be checked by

**(3.2)** `det(M)>=0`.

But the other branch is important:

**(3.3)** `C0>=0`

makes the reduced endpoint cross term nonnegative on the cone, so **the determinant may be negative and the matrix may be indefinite while the matrix is still copositive**.

This is exactly the positive-rescue behavior that the negative-skeleton PSD fallback of T-P5-166 intentionally cannot capture.

A compact equivalent statement is therefore:

**(3.4)**

`M copositive`

iff

`b>0`, `ab>=p^2`, `bd>=q^2`, and

`[bc>=pq  OR  det(M)>=0]`.

The root-free `C0^2<=A0D0` form is preferable for a tiny checker because it avoids determinant expansion if the reduced coefficients are already available.

---

## 4. Exact specialization to the T-P5-154 floor matrix

At a fixed exact floor candidate `D>=0`, suppose one T-P5-165 negative component has exactly three vertices and, after applying the floor loading, its signs are

**(4.1)**

`M11 = D g1`, `M22 = D g2`, `M33 = D g3`,

with `g1,g2,g3>0`, and

**(4.2)**

`2 M12 = -s12`, `s12>0`,

`2 M23 = -s23`, `s23>0`,

`2 M13 =  t13`, `t13>=0`.

For the original T-P5-154 coefficients this means

`s12 = -(K12 + D(g1+g2))`,

`s23 = -(K23 + D(g2+g3))`,

`t13 =  K13 + D(g1+g3)`,

with the displayed sign conditions checked exactly.

Define the division-free scaled reduced gates

**(4.3)**

`A4 := 4 D^2 g1 g2 - s12^2`,

**(4.4)**

`D4 := 4 D^2 g2 g3 - s23^2`,

**(4.5)**

`C4 := 2 D g2 t13 - s12 s23`.

These are simply four times the reduced coefficients:

`A4=4A0`, `D4=4D0`, `C4=4C0`.

### Corollary C — exact P5 three-path checker

Under the sign assumptions above, the 3x3 floor block is copositive iff

**(4.6)** `A4>=0`,

**(4.7)** `D4>=0`,

and

**(4.8)** `C4>=0  OR  C4^2<=A4 D4`.

Because `s12>0` and `A4>=0`, these gates already force `D>0`, so no division or separate square-root positivity test is needed in the realized negative-path branch.

This checker uses only exact rational addition, multiplication, squaring, sign tests, and order comparisons.

### Dispatch meaning

After T-P5-165/T-P5-167 constructs a safe component partition at a fixed candidate floor:

- a 3-vertex component with strict negative path and nonnegative endpoint should be sent to Corollary C;
- **do not delete the positive endpoint term first** unless one intentionally wants the conservative T-P5-166 skeleton certificate;
- failure of the skeleton PSD check is not a mathematical FAIL for the original block;
- only failure of the exact gate above, or another genuine nonnegative negative witness, may be promoted to a mathematical FAIL.

---

## 5. Sharp rational rescue of the T-P5-166 path obstruction

T-P5-166 used the exact path skeleton

**(5.1)**

`N0 = [[1,   -3/4, 0],
       [-3/4, 1,   -3/4],
       [0,   -3/4, 1]]`.

The nonnegative vector `(1,3/2,1)` gives

**(5.2)** `x^T N0 x = -1/4`.

Now retain a positive endpoint coupling `c>=0`:

**(5.3)**

`M(c) = [[1,   -3/4, c],
         [-3/4, 1,   -3/4],
         [c,   -3/4, 1]]`.

The reduced coefficients are

**(5.4)**

`A0=D0=7/16`,

`C0=c-9/16`.

Hence Theorem B says `M(c)` is copositive exactly when

`c-9/16>=0`

or

`(c-9/16)^2 <= (7/16)^2`.

For `c>=0`, these branches combine to the sharp threshold

**(5.5)** `c>=1/8`.

At the boundary `c=1/8`,

**(5.6)**

`B(x,z) = (7/16)(x-z)^2`,

and the old witness satisfies

`(1,3/2,1)^T M(1/8)(1,3/2,1)=0`.

For every `0<=c<1/8`, the same vector gives

**(5.7)** `-1/4 + 2c <0`.

Thus the endpoint rescue threshold `1/8` is exact, not a loose sufficient constant.

### Copositive but strongly indefinite regression

Take `c=2`. Then

`C0=23/16>0`,

so Theorem B certifies copositivity immediately. Nevertheless

**(5.8)** `det M(2) = -15/8 <0`.

Therefore the matrix is indefinite. This is a concrete case where ordinary PSD, negative-skeleton PSD, and any theorem that silently replaces copositivity by PSD all fail, while the exact cone-aware pivot theorem succeeds.

---

## 6. A broader elimination strategy for mixed-sign components

Theorem A suggests a useful exact preprocessing step before generic T-P5-158/160/162 support/KKT search.

Inside one current negative component of a fixed exact matrix:

1. find a vertex `v` with strictly positive diagonal;
2. require every current off-diagonal entry from `v` to the retained coordinates to be nonpositive;
3. write those couplings as `-r`, `r>=0`;
4. replace the remaining matrix `A` by the exact scaled reduced matrix

   **(6.1)** `S=bA-r r^T`;

5. recurse on `S` if another sign-compatible pivot appears.

Every such elimination is an **iff** for copositivity, not merely a sufficient PSD reduction. Positive couplings among the retained variables survive inside `A` and can rescue the reduced form.

This strictly differs from T-P5-166's negative-skeleton route:

- negative-skeleton deletion is monotone/sufficient for the original mixed-sign matrix and exact for the forest Z-skeleton;
- sign-compatible pivot elimination is exact for the original mixed-sign matrix whenever its pivot sign condition holds.

The two are complementary. A sensible dispatcher is:

**(6.2)**

`component split -> exact sign-compatible pivot elimination -> special low-dimensional gate -> negative-skeleton sufficient certificate -> generic copositivity/KKT fallback`.

The order matters because an early skeleton deletion can destroy a positive rescue that exact pivot elimination would preserve.

### Limitation

After one elimination, entries of `S=bA-r r^T` can change sign. The theorem does not promise that a whole forest can be eliminated recursively in every order. Each subsequent pivot must re-check its own current row-sign condition. Failure of this preprocessing condition is only a dispatcher fallback, not a mathematical failure.

---

## 7. Counterexample-guided interface rules

This child fixes four fail-closed rules.

### Rule 1 — skeleton failure is not original-matrix failure

The `c=1/8` family above shows a positive nonedge can exactly repair a negative forest skeleton. A producer must not turn a failed shared-diagonal skeleton certificate into a source obstruction unless the positive remainder has also been accounted for.

### Rule 2 — pivot sign must be proved, not guessed from graph degree

A graph-theoretic leaf/center label is not enough. The pivot theorem needs the **current reduced row** to have nonpositive off-diagonal entries. Positive pivot coupling changes the constrained minimizer and invalidates the Schur iff.

### Rule 3 — do not replace `C0>=0` by determinant positivity

When `C0>=0`, the binary reduced form is automatically safe once its two diagonals are nonnegative, even if the determinant is negative. Requiring `det>=0` in that branch would manufacture false FAILs such as `c=2` above.

### Rule 4 — robust/source family handling remains T-P5-167's job

The theorem here is for one exact fixed matrix/floor candidate. If source entries are interval/correlated, first use certified family-level lower/sign information to determine which exact matrices/components are being certified. Do not replace a correlated source family by an independent Cartesian coefficient box and then interpret a false interval-hull FAIL as an actual source counterexample.

---

## 8. Suggested Lean decomposition

The proof can be formalized with very small ordered-field leaves before any matrix API is introduced.

### Leaf L1 — completion identity

Suggested statement:

`copositivePivot_completion_identity`

For real scalars/vector finite sums, prove

`b * (b*t^2 - 2*t*s + a) = (b*t-s)^2 + (b*a-s^2)`.

The fully matrix-shaped version can be layered later. This is `ring`.

### Leaf L2 — division-free necessity witness

Suggested statement:

`copositivePivot_reduced_nonneg_of_original`

Assume `0<b`, `0<=s`, and

`forall t>=0, forall scale>=0, original(t,scale)>=0`.

Instantiate `t=s`, scale `b`; conclude `0<=b*a-s^2`.

This avoids `/b` and is suitable for `nlinarith` after the ring identity.

### Leaf L3 — binary copositive root-free gate

Suggested statement:

`binary_copositive_iff_rootfree`

Prove

`(forall x z, 0<=x -> 0<=z -> 0<=A*x^2+2*C*x*z+D*z^2)`

iff

`0<=A and 0<=D and (0<=C or C^2<=A*D)`.

The sufficient hard branch uses (2.10); necessity uses the explicit rational witnesses from Section 2. No square root API is needed.

### Leaf L4 — three-path exact theorem

Suggested statement:

`negativePath3_copositive_iff`

with parameters `a b d p q c : Real`, hypotheses `0<p`, `0<q`, `0<=c`, and the exact criterion (2.5)--(2.8).

The witness lift should use the no-division map

`(x,z) -> (b*x, p*x+q*z, b*z)`.

### Leaf L5 — P5 scaled gate

Suggested statement:

`floorPath3_copositive_iff_scaledGates`

with `D>=0`, `gi>0`, `s12>0`, `s23>0`, `t13>=0`, and the exact gates

`A4>=0`, `D4>=0`, `C4>=0 or C4^2<=A4*D4`.

This should be mostly `ring_nf` plus L4 and order arithmetic.

### Optional generic finite-dimensional theorem

Only after the scalar core compiles:

`copositive_block_iff_schurScaled_of_nonpositivePivotRow`

for a finite index type, symmetric `A`, `r_i>=0`, and `b>0`.

The trusted statement can stay on the scaled matrix `bA-r r^T`, avoiding inverse and square root objects entirely.

---

## 9. Source/checker packet suggested by this result

For a fixed candidate floor after T-P5-167's safe family/component partition, a tiny source-facing exact packet is enough for this child:

- component key and vertex order `(1,2,3)`;
- exact or source-certified fixed candidate `D`;
- `g1,g2,g3>0`;
- signed exact floor-adjusted pair values `s12>0`, `s23>0`, `t13>=0`;
- exact computed `A4,D4,C4`;
- one of the two final branch witnesses:
  - `C4>=0`, or
  - `C4<0` plus `C4^2<=A4D4`;
- on FAIL, the explicit reduced/original nonnegative witness from Section 2.

The checker should **not** ask for eigenvalues, a Cholesky factor, a generic SDP, or a KKT solve for this shape.

If the component has more than three vertices, the producer may first try the generic sign-compatible pivot rule; if no valid pivot remains, fall back to the existing T-P5-166/T-P5-158/160/162 lanes.

---

## 10. Remaining obligations and admission boundary

This review proves only the exact mathematics above. It does **not** establish:

- that an actual source/floor family contains a three-vertex path component;
- exact source identity of `g_i`, `K_ij`, or floor candidate `D`;
- robust interval/correlated source sign gates beyond T-P5-167's abstract contract;
- physical/domain/trajectory coverage;
- Float64 or interval-rounding semantics;
- a Lean compile/kernel receipt;
- independent validation by 封不觉;
- registry eligibility or formal certificate admission.

Accordingly the correct state is

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.**

### Recommended next mathematical/source action

At each exact candidate floor after component factorization, dispatch by component shape. If a component is a three-vertex negative path, evaluate `(A4,D4,C4)` first. More generally, before deleting positive nonedges or launching generic support/KKT, attempt one sign-compatible copositive pivot. Preserve the positive remainder because it can be the entire reason the original mixed-sign component is safe.
