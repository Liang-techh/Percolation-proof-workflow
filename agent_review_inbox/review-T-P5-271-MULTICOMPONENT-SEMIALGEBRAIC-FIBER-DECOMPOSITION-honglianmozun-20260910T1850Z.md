---
kind: review_result
review_id: review-T-P5-271-multicomponent-semialgebraic-fiber-decomposition-honglianmozun-20260910T1850Z
task_id: T-P5-271-MULTICOMPONENT-SEMIALGEBRAIC-FIBER-DECOMPOSITION
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T18:50:00Z
claim_commit: e90ec477593fda8e9d0aa464d3b92a3ac17b2ab8
inspected_commit: dca236762bf7fa0687e0d6fbcaf030d895561a92
upstream_commits:
  - 796fdbafb703dd97bb6841632091174aac469e68 # T-P5-270 algebraic moving fiber Thom closure
  - 5334199bdb2c7b093239ffb72ffd4c759294323c # T-P5-269 moving rational fiber exact clamp
  - bcebee5554c3a98dbe3a716407a21586f6367839 # T-P5-268 concave quadratic parameter clamp
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_parity_aware_semialgebraic_fiber_atlas; add_multicomponent_quadratic_clamp; add_discriminant_point_cell_dispatch; reject_convex_hull_fiber_relaxation; preserve_source_binding_boundary
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact real-algebraic/squarefree-factor derivation, sign-topology proof, quadratic energy clamp, rational counterexamples; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-271 — Multi-component semialgebraic fiber decomposition for Lyapunov quadratic clamps

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-270 closes selected algebraic endpoint graphs `a(q),b(q)` on simple-root cells, but explicitly leaves a different geometry open: a source fiber may be declared implicitly by one polynomial inequality

`F_q := { s in [L,U] : P(q,s) >= 0 }`

and may contain several disjoint intervals, moving singleton branches, mergers, or splits.

This child proves that for a **single polynomial inequality in one fiber variable**, the geometry is still reducible to a finite one-dimensional `q` atlas. On every regular `q` cell the real roots of a parity-aware squarefree factorization form ordered algebraic branches, the sign topology of `P(q,.)` is fixed, and `F_q` is a fixed combinatorial union of interval components and possibly isolated even-multiplicity root branches. The signed quadratic Lyapunov debit is then checked component by component with the existing LEFT/RIGHT/INTERIOR clamp, plus a singleton evaluation rule.

At discriminant / degree-drop / resultant cells one must **not** extrapolate the regular-cell branch description. Those finitely many `q` values are exact point cells and are solved directly as univariate algebraic sign problems. This is essential: an isolated feasible state can live only on a discriminant point and be invisible on every neighboring open cell.

A second exact obstruction is proved: replacing a disconnected fiber by its convex hull is not a harmless source relaxation. It can create a false Lyapunov failure arbitrarily far from the true source components.

No actual P5 source polynomial, same-key fiber, state realization, trajectory/cell/FD-halo coverage, Float64 semantics, Lean/kernel proof, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let

`I=[q_0,q_1] subset R`, `L<U`,

with rational endpoints for the serialized packet, and let

`P(q,s) in Q[q,s]`, `P != 0`.

The source fiber is

**(1.1)** `F_q = { s in [L,U] : P(q,s) >= 0 }`.

The energy / Lyapunov upper envelope is

**(1.2)** `A(q,s)=A0(q)+A1(q)s-A2(q)s^2`,

with `A0,A1,A2 in Q[q]`, and the desired safety gate is

**(1.3)** `A(q,s) <= K` for every `q in I` and every `s in F_q`.

Write the slack

**(1.4)** `p(q,s)=K-A(q,s)=C(q)-A1(q)s+A2(q)s^2`,

where `C=K-A0`.

Unlike T-P5-268/269/270, this review does **not** assume that the entire fiber is one interval or that `A2>=0` globally. Curvature sign changes can be added to the same finite `q` partition.

---

## 2. Why ordinary squarefree reduction is unsound for an inequality fiber

For an equality `P=0`, replacing `P` by its squarefree part preserves the zero set. For a sign condition `P>=0`, it generally does **not** preserve the feasible set.

Example:

`P(s)=(s-1)^2`.

Then `P>=0` is true for every `s`, whereas the squarefree part `s-1>=0` keeps only `s>=1`.

Therefore a correct fiber atlas must remember root **multiplicity parity**, not merely the union of distinct roots.

Over `Q(q)[s]`, take the squarefree factorization

**(2.1)** `P(q,s)=c(q) product_{j=1}^d F_j(q,s)^j`,

where each nonconstant `F_j` is squarefree in `s` and the `F_j` are pairwise coprime over `Q(q)`.

The exponent `j` is part of the source geometry. Crossing a simple real root belonging to `F_j` flips the sign of `P` iff `j` is odd.

This parity datum is the first new structural gate.

---

## 3. Finite exceptional projection set

Clear the rational-function denominators in (2.1). Define an exceptional set `Sigma subset I` containing the real zeros in `I` of every nonzero projection polynomial required for any of the following events:

1. a denominator in the squarefree factorization vanishes;
2. the leading coefficient in `s` of some `F_j` vanishes (degree drop);
3. `disc_s(F_j)=0` (a root inside that factor ceases to be simple);
4. `Res_s(F_i,F_j)=0` for `i!=j` (roots from different multiplicity factors collide);
5. `F_j(q,L)=0` or `F_j(q,U)=0` when that evaluation is not identically zero (a moving root crosses a clipping boundary);
6. `A2(q)=0` when `A2` is not identically zero (quadratic curvature changes sign).

Identically vanishing boundary evaluations are treated symbolically as persistent boundary-root factors rather than as an infinite exceptional set.

Because the squarefree factors are pairwise coprime over `Q(q)` and squarefree in `s`, their discriminants and pairwise resultants are nonzero rational functions before specialization. After clearing denominators, only finitely many real zeros occur on compact `I`.

Hence

**(3.1)** `I \ Sigma = J_1 union ... union J_N`

is a finite union of open intervals.

The points of `Sigma`, together with `q_0,q_1`, are retained as zero-dimensional `q` cells.

---

## 4. Theorem A — ordered algebraic root atlas on every regular q-cell

Fix one connected open cell `J subset I\Sigma`.

### Claim

All real roots in `[L,U]` of all factors `F_j(q,.)` can be labeled

**(4.1)** `alpha_1(q) < alpha_2(q) < ... < alpha_m(q)`

for `q in J`, such that:

- each `alpha_r` is a continuous real-algebraic branch and is real analytic on `J`;
- each branch belongs to one fixed factor `F_{j(r)}`;
- the multiplicity of `alpha_r` as a root of `P(q,.)` is the fixed integer `j(r)`;
- no two branches collide on `J`;
- no branch crosses `L` or `U` on `J` unless it is a persistent boundary branch already factored symbolically.

### Proof

On `J`, the leading coefficient and discriminant of every `F_j` are nonzero. Therefore every specialized root is simple and the number of real roots is locally constant. At each real root, `(F_j)_s != 0`, so the implicit function theorem gives a unique local analytic root graph.

Pairwise resultants are nonzero on `J`, hence a root of `F_i` cannot meet a root of `F_j` for `i!=j`. A root of one factor cannot meet another root of the same factor because its discriminant is nonzero. Thus local root graphs continue uniquely across the connected cell and cannot exchange order. Boundary-evaluation projection polynomials prevent a nonpersistent branch from crossing `L` or `U`.

The factor label and exponent are therefore constant along each branch. QED.

---

## 5. Theorem B — sign topology and component type are constant on a regular cell

Insert the constant clipping walls as

`beta_0=L`, `beta_{m+1}=U`,

and let the internal `beta_r` be the ordered root branches `alpha_r` that lie in `(L,U)`.

The open vertical strips

**(5.1)** `S_r = { (q,s): q in J, beta_r(q)<s<beta_{r+1}(q) }`

are connected and contain no zero of `P`. Therefore `sign P` is constant on each strip.

At a root branch `alpha_r` of multiplicity `j(r)`, the sign relation across the branch is

**(5.2)** `sign(P_right)=(-1)^{j(r)} sign(P_left)`.

Thus:

- odd multiplicity roots switch feasible/infeasible side;
- even multiplicity roots preserve the side sign.

Because equality is included in `P>=0`, there is one additional component type that a single-interval endpoint model misses:

**isolated moving singleton.**

If the two adjacent strips both satisfy `P<0` and `j(r)` is even, then

**(5.3)** `{alpha_r(q)}`

is itself a feasible connected component for every `q in J`.

Therefore, on a regular cell, `F_q` has a constant combinatorial decomposition into a finite ordered family consisting only of:

1. closed interval components `[a_k(q),b_k(q)]`, whose endpoints are `L`, `U`, or selected algebraic root branches;
2. singleton components `{c_k(q)}` arising from an isolated even-multiplicity zero.

The number and type of components are fixed throughout `J`.

### Exact sign initialization

It is enough to determine the sign of `P` in one strip at one exact sample `q* in J`; all other strip signs follow by (5.2). Equivalently one may use an exact selected-root sign evaluator / Sturm-Habicht sign determination as in T-P5-270.

No floating root ordering is required.

---

## 6. Theorem C — exact component-wise Lyapunov clamp

Fix `q` and one interval component `[a,b] subset F_q`.

We want

**(6.1)** `p(q,s)>=0` for every `s in [a,b]`.

There are two curvature regimes.

### 6.1 Convex slack: `A2(q)>0`

Then `p(s)=C-A1 s+A2 s^2` is strictly convex. Define

`g_a=A1-2A2 a`,

`g_b=A1-2A2 b`,

`E_a=p(a)`, `E_b=p(b)`,

`F=4A2 C-A1^2`.

The exact T-P5-268/270 clamp applies:

- LEFT: if `g_a<=0`, safety on this component iff `E_a>=0`;
- RIGHT: if `g_a>0` and `g_b>=0`, safety iff `E_b>=0`;
- INTERIOR: if `g_a>0>g_b`, safety iff `F>=0`.

All signs involving algebraic `a,b` are selected-branch signs, never resultant signs.

### 6.2 Concave or affine slack: `A2(q)<=0`

Then `p` is concave (affine at equality). A concave function on `[a,b]` lies above the chord joining its endpoint values, hence

**(6.2)** `p(s)>=min(p(a),p(b))` for every `s in [a,b]`.

Therefore

**(6.3)** `p>=0 on [a,b]  <=>  p(a)>=0 and p(b)>=0`.

So no stationary-point denominator is needed in this regime.

### 6.3 Singleton component

For a singleton `{c(q)}` the exact condition is simply

**(6.4)** `p(q,c(q))>=0`.

This singleton rule is necessary even when every neighboring open strip is infeasible.

### 6.4 Union rule

If

`F_q = C_1(q) disjoint_union ... disjoint_union C_M(q)`,

then

**(6.5)** `p>=0 on F_q  <=>  p>=0 on every C_k(q)`.

Equivalently the true fiber reserve is

**(6.6)** `r(q)=min_k r_k(q)`,

where `r_k` is the exact interval minimum from the clamp above or the singleton value.

No cross-component convexification is legitimate.

---

## 7. Theorem D — finite exact q-dispatcher on a compact interval

Start from the regular projection partition `I\Sigma` of Section 3. Refine each open cell by the finitely many selected-branch contact events needed by the quadratic clamp:

- `g_a=0`, `g_b=0` for interval endpoints;
- endpoint reserve contacts `p(q,a(q))=0`, `p(q,b(q))=0`;
- singleton reserve contacts `p(q,c(q))=0`;
- rational interior reserve contact `F(q)=0`;
- critical-point resultants/subresultants used to extract a strict reserve floor when a branch reserve must be minimized in `q`.

T-P5-270 already proves that selected algebraic branch signs are constant between their branch-aware contact cells and that their extrema reduce to exact algebraic endpoint/critical candidates.

Hence every regular source-topology cell admits a finite exact LEFT/RIGHT/INTERIOR/ENDPOINT/SINGLETON dispatcher.

For every exceptional `q*=Sigma`, evaluate the specialized univariate polynomial

**(7.1)** `P(q*,s)`

over the exact real-algebraic coefficient field `Q(q*)`, isolate/order its real roots in `[L,U]`, build the true sign components directly, and apply the same one-variable quadratic clamp to those components.

Therefore the full compact safety statement (1.3) is equivalent to a **finite family of exact real-algebraic sign checks**. There is no mathematical need for a generic bivariate numerical optimizer in the one-polynomial/one-fiber-variable branch.

This is a specialized cylindrical decomposition, but only the one-dimensional projection/root-ordering structure required by the Lyapunov packet is retained.

---

## 8. Exact obstruction 1 — convex-hull replacement can create a false Lyapunov FAIL

Take a q-independent fiber polynomial

**(8.1)** `P(s)=(s^2-1)(4-s^2)`

on `[-2,2]`, with source condition `P(s)>=0`.

Then

**(8.2)** `F=[-2,-1] union [1,2]`.

Take

**(8.3)** `A(s)=2-s^2`, `K=1`,

so

`p(s)=K-A=s^2-1`.

On the true source fiber, `|s|>=1`, hence

**(8.4)** `p(s)>=0` everywhere on `F`.

Thus the exact Lyapunov gate passes.

But the convex hull is `conv(F)=[-2,2]`, and at the artificial gap point `s=0`,

**(8.5)** `p(0)=-1<0`.

Therefore replacing a disconnected source fiber by its convex hull turns a true PASS into a false FAIL.

The gap can be made arbitrarily costly by replacing `A` with `M+1-s^2` and `K=1`; the true fiber remains safe after scaling the root threshold appropriately while the artificial center debit grows with `M`.

**Conclusion:** a multi-component source fiber must be preserved component-wise whenever signed nonlinear cancellation matters.

---

## 9. Exact obstruction 2 — discriminant point cells cannot be skipped

Consider

**(9.1)** `P(q,s)=-(q^2+s^2)`

on `I=[-1,1]`, `s in [-1,1]`, with source condition `P>=0`.

For every `q!=0`,

**(9.2)** `F_q=emptyset`.

At the discriminant point `q=0`,

**(9.3)** `F_0={0}`.

Now take the slack to be the constant

**(9.4)** `p(q,s)=-1`.

Every open q-cell away from zero is vacuously safe because the fiber is empty. Nevertheless the actual source point `(0,0)` violates the Lyapunov inequality.

Thus a dispatcher that analyzes only regular open cells and treats discriminant points as removable measure-zero events is mathematically unsound for universal safety.

The zero-dimensional q cells are not bookkeeping; they may carry genuine isolated feasible states.

---

## 10. Exact obstruction 3 — ignoring multiplicity parity changes the source set

Take

`P(s)=-(s^2-1)^2`.

Then `P>=0` holds only at `s=+-1`, two singleton source components.

The ordinary squarefree part is `s^2-1`; its nonnegative set is `(-infinity,-1] union [1,infinity)`, which is entirely different.

Thus for an inequality source packet:

**(10.1)** root locations alone are insufficient;

**(10.2)** multiplicity parity is part of the physical/source geometry;

**(10.3)** isolated even-multiplicity roots must remain representable as singleton components.

This is why the factorization in Section 2 retains the exponent `j`.

---

## 11. Reserve-floor consequence

Suppose an open regular cell has components `C_k(q)` and component reserve functions `r_k(q)` from Section 6.

Then

**(11.1)** `r_global = min_{q in closure(J)} min_k r_k(q)`

is attained because the source fiber restricted to the compact closure is semialgebraic/compact after the exceptional endpoint cells are restored.

On any branch where `r_k(q)=H(q,alpha(q))` for a selected simple algebraic root `P_branch(q,alpha)=0`, T-P5-270 gives the exact critical numerator

**(11.2)** `N_H = H_q (P_branch)_s - H_s (P_branch)_q`.

Interior extrema occur only at selected common roots of

`P_branch=0`, `N_H=0`.

On an INTERIOR clamp branch the reserve is rational in `q` (`F/(4A2)` when `A2>0`), so ordinary exact univariate critical-point isolation applies.

Therefore the multi-component extension does not destroy exact reserve extraction: it changes only the finite outer minimum over source components and singular q point cells.

---

## 12. Structural fingerprint

The new fingerprint is:

`single polynomial source inequality in one fiber variable`

`-> parity-aware squarefree factorization over Q(q)`

`-> finite projection set (degree drop / discriminant / inter-factor resultant / clipping contact / curvature switch)`

`-> ordered selected algebraic roots on each regular q-cell`

`-> sign strips + multiplicity-parity propagation`

`-> interval components + isolated even-multiplicity singleton components`

`-> component-wise Lyapunov quadratic clamp`

`-> exact algebraic point-cell checks at mergers/splits`

`-> finite one-dimensional safety / reserve dispatcher`.

This keeps the same fundamental architecture as T-P5-268/269/270 while removing the fictitious assumption that the source fiber is connected.

---

## 13. Candidate theorem statements for later formalization

The formal leaves should remain separated from computer-algebra implementation.

### Leaf 1 — concave/affine endpoint minimum

For real `a<=b` and quadratic

`p(s)=C-A1 s+A2 s^2`

with `A2<=0`, prove

`(forall s in [a,b], 0<=p(s)) <=> 0<=p(a) and 0<=p(b)`.

### Leaf 2 — union safety

For a finite family of sets `C_k`, prove

`p>=0 on union_k C_k <=> forall k, p>=0 on C_k`.

This trivial ordered-set leaf is the exact reason components can be checked independently without convexifying them.

### Leaf 3 — parity sign crossing

If a continuous function near `a` factors as

`P(s)=(s-a)^m h(s)`, `h(a)!=0`,

prove that the signs on the two sides differ iff `m` is odd.

### Leaf 4 — isolated even-multiplicity feasible root

If `P(a)=0`, `P<0` on both punctured sides of `a`, then `{a}` is a connected component of `{P>=0}` locally.

### Leaf 5 — regular-cell root order invariance

For finitely many continuous root branches with pairwise noncollision on a connected interval, their strict order is constant.

### Leaf 6 — exceptional point necessity

Universal safety over a finite cell decomposition is the conjunction of safety on all positive-dimensional cells and all zero-dimensional point cells.

The squarefree factorization, resultant projection and exact root isolation may remain external certified preprocessing until a pinned algebraic-number implementation exists.

---

## 14. Fail-closed semantics

The following distinctions are mandatory.

- No dominant single interval because the source has several components: **MULTICOMPONENT_FIBER**, not a mathematical failure.
- Convex-hull outer interval fails while every true component passes: **HULL_RELAXATION_FALSE_FAIL**; preserve the disconnected fiber.
- A regular-cell root atlas reaches a discriminant/resultant/degree-drop point: **SINGULAR_Q_POINT_CELL_REQUIRED**, not branch extrapolation.
- An even-multiplicity isolated root is feasible only by equality: keep a **SINGLETON_COMPONENT**; do not discard it as measure zero.
- Exact source fiber empty on a cell: the universal inequality there is vacuous, but this does not remove neighboring/isolated point cells.
- Exact negative reserve on a proved same-key component: mathematical counterexample for that declared fiber; physical/source FAIL still requires source binding and state realization.
- Root isolation / CAD / selected-sign certificate not found: **CERTIFICATE_NOT_FOUND**, never mathematical FAIL.
- Replacing `P` by its ordinary squarefree part in a sign inequality without parity metadata: **UNSOUND_SOURCE_TRANSFORM**.

---

## 15. Remaining obligations

Still open:

1. determine whether deployed P5 actually exposes a source fiber of the form `P(q,s)>=0` or an equivalent polynomial Boolean formula;
2. bind `P`, `q`, `s`, `[L,U]`, metric/chart and source key to the same actual evaluator;
3. prove the compact clipping interval is source-valid and not merely sampled;
4. produce the actual squarefree multiplicity packet and exact projection polynomials;
5. provide selected-root encodings on every regular cell and exact specialized point-cell packets;
6. extract the actual `A0,A1,A2,K` and bind them to the same source/cell;
7. state/state-trajectory realization of any negative witness;
8. cell/flowed-sheet/FD-halo/reference-halo coverage;
9. Float64/libm/interval semantics;
10. Lean/kernel formalization of ordered-field leaves;
11. independent validation by 封不觉;
12. admission, registry mutation and P5/P8/M4 parent propagation.

---

## 16. Next mathematical seam

For **one** polynomial inequality in **one** fiber variable, disconnected components and merger/split point cells are now mathematically reduced to a finite q-atlas.

The next genuinely new geometry is a Boolean/conjunctive semialgebraic fiber, for example

`F_q={s in [L,U]: P_1(q,s)>=0, ..., P_r(q,s)>=0}`,

or mixed signs/equalities. Then component boundaries may come from different polynomials, and active-boundary identity can switch where two boundary roots cross. The natural next child is a **multi-constraint one-dimensional fiber arrangement theorem**: use pairwise resultants between all boundary polynomials, build a common ordered root arrangement, evaluate the Boolean sign formula strip-by-strip, and retain singleton equality components.

That would still avoid general two-variable optimization while matching a much broader class of actual source descriptions.