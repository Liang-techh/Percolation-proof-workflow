---
kind: review_result
review_id: review-T-P5-272-multiconstraint-semialgebraic-fiber-arrangement-liuguanyi-20260910T1901Z
task_id: T-P5-272-MULTICONSTRAINT-SEMIALGEBRAIC-FIBER-ARRANGEMENT
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T19:01:00Z
claim_commit: 2fb141f6ad5863c4c52e7c7528e31a0f5510b17e
inspected_commit: 51b169287280752164a02827b76340dd797ef57b
upstream_commits:
  - 28be4ab630470caae390cfef4b534a0c96091076 # T-P5-271 multicomponent semialgebraic fiber decomposition
  - 796fdbafb703dd97bb6841632091174aac469e68 # T-P5-270 algebraic moving fiber Thom closure
  - 5334199bdb2c7b093239ffb72ffd4c759294323c # T-P5-269 moving rational fiber exact clamp
  - bcebee5554c3a98dbe3a716407a21586f6367839 # T-P5-268 concave quadratic parameter clamp
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_common_boundary_factor_arrangement; add_boolean_truth_cell_dispatch; add_boundary_truth_vector; add_closure_safe_continuous_clamp; preserve_strict_and_equality_semantics
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact algebraic/sign-topology derivation and rational counterexamples only; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-272 — Multi-constraint one-dimensional semialgebraic fiber arrangement

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-271 reduced a fiber defined by one inequality `P(q,s)>=0` to a finite `q`-atlas. The genuinely new issue is that a real source adapter may expose several polynomial predicates simultaneously, with strict/weak inequalities, equalities, unions, and conjunctions. Individual root atlases are not enough: two boundary roots from different predicates may cross, changing which predicate supplies the active endpoint, and a boundary point may be admitted or rejected by the Boolean formula independently of the truth on either adjacent strip.

This child proves a common-arrangement theorem for **any finite Boolean formula in polynomial sign atoms with one fiber variable**. After a finite exceptional projection set in `q` is removed, all boundary roots admit one common ordered algebraic arrangement. Every open strip has a constant full sign vector; every root graph has a constant boundary truth vector including all simultaneous zero atoms arising from shared factors. Hence the source fiber has a fixed combinatorial decomposition on each regular `q`-cell. Universal continuous Lyapunov safety reduces exactly to selected strip closures plus graph-only components, so the existing algebraic quadratic clamp can be reused without replacing the source by a convex hull or a general two-variable optimizer.

No actual P5 Boolean formula, source key, cell, evaluator, clipping interval, state realization, trajectory/FD-halo coverage, Float64 semantics, Lean/kernel proof, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Source formula and common factor basis

Let `I=[q0,q1]` and `[L,U]` be compact rational intervals. Let

`P_1(q,s),...,P_m(q,s) in Q[q,s]`

and let `Phi` be a finite Boolean formula built from atoms

`P_i ⋈ 0`, where `⋈ in {>,>=,=,<=,<}`.

The source fiber is

`F_q={s in [L,U] : Phi(q,s) is true}`.

Identically zero `P_i` are removed first by replacing their atom by its constant truth value. For every remaining polynomial, view it as a polynomial in `s`, extract the `q`-content, and refine all squarefree factors across the whole family into one common pairwise-coprime basis over `Q(q)[s]`:

`P_i(q,s)=c_i(q) product_{a=1}^N F_a(q,s)^(m_{ia})`,

where `m_{ia}>=0`, each `F_a` is squarefree in `s`, and distinct `F_a,F_b` are coprime over `Q(q)[s]`.

This common basis is essential. If the same algebraic factor occurs in several source predicates, a root of that factor makes all corresponding `P_i` vanish simultaneously; treating the predicates independently would falsely interpret this as a collision of unrelated root branches.

---

## 2. Finite exceptional q-set

After clearing all harmless rational-function denominators, define `Sigma subset I` to contain every real zero in `I` of every nonzero projection polynomial needed for:

1. denominator or content sign changes `c_i(q)=0`;
2. leading coefficient in `s` of a common factor `F_a` vanishing;
3. `disc_s(F_a)=0`;
4. `Res_s(F_a,F_b)=0` for `a!=b`;
5. `F_a(q,L)=0` or `F_a(q,U)=0` when the evaluation is not identically zero;
6. any extra coefficient polynomial used by the Lyapunov quadratic dispatcher, for example `A2(q)` if curvature branch changes must be synchronized with the same atlas.

Persistent identities `F_a(q,L)≡0` or `F_a(q,U)≡0` are not declared infinitely exceptional; they are represented as persistent constant boundary branches.

Because the common factors are squarefree and pairwise coprime over `Q(q)[s]`, the relevant discriminants and pairwise resultants are nonzero rational functions before specialization. Therefore `Sigma` is finite.

The complement `I\Sigma` is a finite union of connected open intervals `J`. Points in `Sigma`, together with the outer endpoints of `I`, are retained as exact zero-dimensional `q` cells.

---

## 3. Theorem A — common ordered-root arrangement

Fix one connected regular cell `J subset I\Sigma`.

### Statement

All real roots in `[L,U]` of all common factors can be labeled globally on `J` as

`alpha_1(q)<...<alpha_r(q)`

such that:

- every `alpha_k` is continuous real-algebraic and real analytic on `J`;
- each branch belongs to one fixed common factor `F_{a(k)}`;
- no two branches collide or exchange order on `J`;
- no nonpersistent branch crosses `L` or `U` on `J`;
- if `m_{i,a(k)}>0`, then `P_i(q,alpha_k(q))=0` for every `q in J`;
- if `m_{i,a(k)}=0`, then `P_i(q,alpha_k(q))` is nonzero and has constant sign on the connected graph of `alpha_k`.

### Proof

On `J`, the leading coefficient and discriminant of every `F_a` are nonzero. Hence every specialized real root of every factor is simple, so the implicit-function theorem gives a unique local analytic root graph. Pairwise resultants are nonzero, so roots of two distinct common factors cannot meet. Roots of the same factor cannot meet because its discriminant is nonzero. Thus local graphs continue uniquely across the connected interval and cannot exchange order. Boundary-evaluation projection polynomials prevent a nonpersistent root from entering or leaving `[L,U]`.

If `m_{i,a(k)}>0`, the factorization gives exact vanishing of `P_i` on that graph. Otherwise `P_i` is a continuous nonzero function on the connected graph. Its sign is therefore constant. This proves the full statement.

---

## 4. Theorem B — strip sign vectors are constant

Augment the root list by `alpha_0(q)=L` and `alpha_{r+1}(q)=U`, merging persistent boundary-root identities rather than duplicating them. For each nonempty open strip

`S_k={(q,s): q in J, alpha_k(q)<s<alpha_{k+1}(q)}`,

define the sign vector

`sigma_k=(sign P_1,...,sign P_m) in {-,+}^m`.

### Claim

`sigma_k` is constant throughout `S_k`. Therefore the truth value of every atom and of the whole Boolean formula `Phi` is constant on `S_k`.

### Proof

No common boundary factor vanishes inside `S_k`, and no content factor `c_i` vanishes on `J`. Thus no `P_i` can vanish in the connected strip. A continuous nonzero real function has constant sign on a connected set. Boolean evaluation depends only on this sign vector, so its truth is constant.

This means one certified sample point per strip determines the whole source truth on that strip.

---

## 5. Theorem C — parity update across one root branch

Suppose `alpha_k` belongs to common factor `F_a`. Let `sigma_-` and `sigma_+` be the sign vectors on the immediately left and right strips, when those strips exist.

For every source polynomial `P_i`:

- if `m_{ia}=0`, its sign is unchanged across the branch;
- if `m_{ia}>0` is even, its sign is unchanged;
- if `m_{ia}` is odd, its sign flips.

Equivalently,

`sign_+(P_i)=(-1)^(m_{ia}) sign_-(P_i)`

for all nonzero side values.

### Proof

Locally, because `F_a` has a simple root,

`F_a(q,s)=(s-alpha_k(q)) h(q,s)`

with `h` nonzero near the graph. Every other common factor and every `c_i` is also nonzero there. Hence

`P_i=(s-alpha_k)^(m_{ia}) H_i`

with `H_i` continuous and nonzero. Crossing the graph changes only the sign of the first factor, exactly when `m_{ia}` is odd.

Thus after one initial strip sign vector is certified, all neighboring strip sign vectors can be propagated by an exact finite parity mask rather than re-solved numerically.

---

## 6. Theorem D — boundary truth vector is constant

For each root graph `G_k={(q,alpha_k(q)):q in J}`, define its exact boundary valuation as follows.

For each `P_i`:

- if `m_{i,a(k)}>0`, record `P_i=0`;
- otherwise record the constant nonzero sign from Theorem A.

Call the resulting vector

`beta_k in {-,0,+}^m`.

### Claim

The Boolean truth value `Phi(beta_k)` is constant on the entire root graph.

This is the critical datum for strict and equality atoms. For example, at a zero of `P_i`, the atoms `P_i>0` and `P_i<0` are false, `P_i>=0`, `P_i<=0`, and `P_i=0` are true. No neighboring-strip sign can substitute for this boundary evaluation.

---

## 7. Theorem E — exact Boolean cylindrical decomposition

On a regular cell `J`, the source set

`F={(q,s): q in J, L<=s<=U, Phi(q,s)}`

is exactly the union of:

- those open strips `S_k` whose strip truth is true;
- those root graphs `G_k` whose boundary truth is true;
- selected constant clipping-boundary graph pieces at `L,U` according to the same atom evaluation.

No other source geometry occurs on `J`.

Consequently, for every fixed `q in J`, `F_q` has a **fixed combinatorial incidence pattern**: the identities and order of all candidate endpoints are unchanged, and whether each open interval and each intervening boundary point is admitted is unchanged.

Connected components can therefore be reconstructed by a finite adjacency rule:

- a true root graph joins its true left/right strips;
- a false root graph separates the two sides even if both adjacent strips are true;
- a true root graph with both adjacent strips false is a graph-only singleton component in each fixed fiber;
- a false strip contributes no points, regardless of neighboring graph truth.

This is precisely the information lost by taking a convex hull or by storing only endpoint numbers without the active source predicate.

---

## 8. Theorem F — continuous Lyapunov safety can use strip closures exactly

Let `p(q,s)` be continuous on `J x [L,U]`; in the deployed application it is the quadratic slack

`p(q,s)=K-A(q,s)`.

For every selected open strip `S_k`, let

`cl_J(S_k)={(q,s): q in J, alpha_k(q)<=s<=alpha_{k+1}(q)}`

where the boundary graphs are understood by continuity even if the Boolean source formula excludes them.

### Claim

`p>=0` on the selected source set over `J`

if and only if both conditions hold:

1. `p>=0` on `cl_J(S_k)` for every selected open strip `S_k`;
2. `p>=0` on every selected root graph not adjacent to any selected open strip, and on any selected isolated clipping-boundary graph not covered by a selected strip closure.

### Proof

The reverse implication is immediate because the source is contained in this union of closures and selected graph-only pieces.

For the forward implication, fix a selected open strip. If `p>=0` on the strip, continuity gives `p>=0` at every limiting boundary point of that strip, so `p>=0` on its closure. Any selected graph not incident to a selected strip is not obtained as such a limit and therefore must be checked separately. These are exactly the extra pieces in condition 2.

### Consequence

Strict source inequalities do **not** force a new open-interval optimizer for continuous Lyapunov safety. Every nonempty selected open strip may be checked with the existing closed algebraic endpoint clamp from T-P5-268/269/270. However the boundary truth vector must still be retained because it decides whether a graph-only component exists and whether a purported counterexample at a boundary is an actual source state or merely a limiting point.

---

## 9. Quadratic clamp reuse

Take

`A(q,s)=A0(q)+A1(q)s-A2(q)s^2`,
`p=K-A`.

On every selected open strip closure `[alpha_k(q),alpha_{k+1}(q)]`, the existing branch logic applies:

- convex slack / concave target: LEFT, RIGHT, or INTERIOR branch as in T-P5-268;
- algebraic moving endpoints: eliminate endpoint values and derivative signs against the defining boundary factors as in T-P5-270;
- if two endpoint roots come from different source polynomials, no extra optimizer is needed because their order is fixed on `J`; the pairwise resultant was already placed into `Sigma`.

For graph-only components `s=alpha_k(q)`, safety is the one-dimensional algebraic sign condition

`p(q,alpha_k(q))>=0`,

checked with the selected-root/Thom encoding of that branch.

Hence a finite Boolean source formula in one fiber variable still reduces the Lyapunov check to a finite **one-dimensional `q` dispatcher**.

---

## 10. Why pairwise resultants between different predicates are essential

Consider

`I=[-1/2,1/2]`, `s in [-1,1]`,

and the conjunctive source formula

`Phi := (s-q>=0) AND (s+q>=0) AND (1-s>=0)`.

The fiber is

`F_q=[|q|,1]`.

The two lower-bound root branches are `s=q` and `s=-q`. Each is simple for every `q`, so individual discriminants detect nothing. Their order switches at `q=0`, where

`Res_s(s-q,s+q)=2q=0`.

For `q<0`, the active lower endpoint is `-q`; for `q>0`, it is `q`. Therefore a dispatcher that partitions only by individual discriminants can attach the wrong source identity to the endpoint. The common pairwise-resultant arrangement creates the necessary point cell `q=0` and keeps the active-boundary identity fixed on both neighboring open cells.

---

## 11. Strict-boundary weakification is unsound

It is tempting to replace strict atoms by weak ones before building the fiber. This is unsound even though strip closures are safe for a continuous target.

Take `s in [-1,1]` and

`Phi := (s>0) AND (-s>0)`.

The true source fiber is empty. Replacing `>` by `>=` produces the singleton `{0}`.

Let the Lyapunov slack be the continuous constant `p(s)=-1`. Universal safety `p>=0` on the true fiber is vacuously true, while it fails on the weakified fiber.

The distinction with Theorem F is exact:

- taking the closure of an **already selected nonempty open strip** preserves continuous universal safety;
- changing the Boolean atom truth at a boundary can create a new graph-only component that was not the closure of any selected strip.

Therefore the adapter must retain the exact boundary truth vector `beta_k`; strict/weak/equality semantics cannot be erased.

---

## 12. Shared factors are not pairwise collisions

Suppose two predicates contain the same factor `F(q,s)`. Then `Res_s(P_1,P_2)` may vanish identically and is useless as an exceptional projection polynomial. The correct preprocessing is the common factor basis of Section 1.

A branch of `F=0` is one geometric boundary graph carrying a multiplicity vector

`(m_{1F},...,m_{mF})`.

Its strip sign update is the parity vector

`((-1)^(m_{1F}),...,(-1)^(m_{mF}))`,

and its boundary truth vector sets precisely those atoms with positive multiplicity to zero.

Thus shared factors are handled structurally, while resultants are reserved for collisions between **distinct coprime common boundary factors**.

---

## 13. Exceptional q-point cells

At every `q*=Sigma`, the regular arrangement is intentionally discarded. Specialize the original Boolean formula directly:

`Phi_{q*}(s)`.

Some source polynomials may drop degree or become identically zero in `s`; some distinct regular root branches may merge; strict and equality predicates can change the status of the merged point. The fiber

`F_{q*}={s in [L,U]: Phi_{q*}(s)}`

is then solved as an exact one-variable semialgebraic sign problem.

This direct point-cell rule is necessary. A source state can exist only at a merger point even when every neighboring regular fiber is empty, for example an equality atom `P(q,s)=0` whose real roots appear only at a discriminant-zero specialization.

Universal safety on the full compact `q` interval is therefore the conjunction of all regular-cell checks and all point-cell checks.

---

## 14. Minimal theorem statement

A compact reusable statement is:

> **Finite Boolean fiber arrangement theorem.** Let `Phi(q,s)` be any finite Boolean formula in atoms `P_i(q,s) ⋈ 0` with `P_i in Q[q,s]` and `⋈ in {>,>=,=,<=,<}`, restricted to a compact rational box `I x [L,U]`. After removing identically zero atoms and refining the family into a common pairwise-coprime squarefree factor basis with multiplicity vectors, there exists a finite algebraic set `Sigma subset I` such that on each connected component `J` of `I\Sigma`: (i) all real boundary roots admit a common strictly ordered analytic algebraic labeling; (ii) every open strip between consecutive roots has a constant full sign vector and hence constant Boolean truth; (iii) every root graph has a constant `{- ,0,+}` boundary valuation and hence constant Boolean truth; and (iv) the fixed-fiber source sets have one fixed combinatorial incidence pattern. For every continuous slack `p`, nonnegativity on the source over `J` is equivalent to nonnegativity on the closures of all Boolean-true open strips plus all Boolean-true graph cells not incident to a true strip. Exceptional `q` values are checked by direct specialization.

This is the exact cross-layer bridge needed to reuse one-dimensional algebraic Lyapunov clamps under a general finite Boolean source description.

---

## 15. Fraction-free / exact packet

A source-facing exact packet need only serialize algebraic data; no floating eigenvectors or nonlinear optimizer are needed:

- common factors `F_a in Q[q,s]`;
- multiplicity matrix `m_{ia}`;
- content/sign polynomials `c_i(q)`;
- nonzero discriminants, pairwise resultants, leading coefficients, and clipping-boundary evaluations defining `Sigma`;
- selected-root encodings for each common root branch on each regular cell;
- one rational sample sign vector on each regular cell (or one initial strip plus parity propagation);
- exact Boolean syntax tree / atom comparison types;
- the resulting strip truth bits and root-graph truth bits;
- point-cell specialized Boolean packets.

The mathematical checker can verify sign propagation and the Lyapunov leaves without evaluating floating roots.

---

## 16. Suggested formalization leaves

The useful Lean-level leaves are small ordered-field/topological facts rather than a monolithic CAD implementation:

1. `pow_sign_crossing_parity`: `(s-a)^m h(s)` with nonzero continuous `h` flips sign across `a` iff `m` is odd;
2. `boolean_eval_of_sign_vector`: equal atom valuations imply equal formula truth;
3. `nonzero_continuous_sign_constant_on_connected`: a continuous nonvanishing real map on a connected set has fixed sign;
4. `continuous_nonneg_open_implies_closure`: continuous `p` nonnegative on a nonempty open interval is nonnegative on its closed interval closure;
5. `finite_union_nonneg_iff`: nonnegativity on a finite union iff nonnegative on every selected piece;
6. `ordered_roots_no_collision_keep_order`: pairwise noncolliding continuous root graphs preserve strict order on a connected interval.

Squarefree refinement, resultant projection, root isolation, and Thom encodings may remain external certified preprocessing until a pinned algebraic-number implementation is chosen.

---

## 17. Fail-closed semantics

The dispatcher must distinguish:

- no root collision but endpoint source identity changes would require a pairwise resultant zero: **COMMON_RESULTANT_POINT_CELL_REQUIRED**;
- strict/weak/equality boundary truth omitted: **BOUNDARY_TRUTH_UNSPECIFIED**, never infer from neighboring strips;
- shared factor treated as an ordinary pairwise collision: **COMMON_FACTOR_REFINEMENT_REQUIRED**;
- selected nonempty open strip checked on its closure for a continuous Lyapunov slack: mathematically exact, not an outer-relaxation downgrade;
- Boolean formula weakified before decomposition: **UNSOUND_BOOLEAN_WEAKIFICATION**;
- selected graph with no adjacent selected strip: **GRAPH_ONLY_COMPONENT**, must be checked directly;
- root arrangement or sign certificate unavailable: **CERTIFICATE_NOT_FOUND**, never mathematical FAIL;
- negative witness for an exact declared Boolean fiber: mathematical failure of that declared fiber; physical/source FAIL still requires actual source binding and state realization.

---

## 18. Remaining obligations

Still open:

1. determine the actual P5 source predicate syntax and whether the fiber is truly one-dimensional after the chosen quotient/chart;
2. bind all `P_i`, Boolean connectives, strict/weak/equality atom semantics, `q,s,[L,U]`, metric/chart, and source key to the same evaluator;
3. prove clipping interval validity and all parameter-domain restrictions;
4. produce the actual common squarefree factor basis and multiplicity matrix;
5. produce exact projection polynomials and selected-root encodings;
6. bind actual Lyapunov `A0,A1,A2,K` to the same source/cell;
7. prove any use of strip closure is applied only to a continuous target on a genuinely selected nonempty strip;
8. state/trajectory realization of any negative witness;
9. cell/flowed-sheet/FD-halo/reference-halo coverage;
10. Float64/libm/interval semantics;
11. Lean/kernel formalization of the small leaves;
12. independent validation by 封不觉;
13. admission, registry mutation, and P5/P8/M4 parent propagation.

---

## 19. Next mathematical seam

Finite Boolean geometry in **one** fiber variable is now reduced to a finite common arrangement. The next genuinely different source geometry is not “more Boolean predicates” but a fiber with **two continuous variables**, for example

`F_q={(s,t): P_i(q,s,t) ⋈ 0}`.

A full CAD jump would be expensive and would obscure the Lyapunov structure. The next useful mathematical child should therefore be structure-sensitive: identify when the two-variable source fiber is triangular/graph-like, e.g.

`s in F_q`, `t in [a(q,s),b(q,s)]`,

or when one variable enters the Lyapunov target quadratically with source endpoints algebraic in the other. Then one can eliminate the inner variable by the existing exact clamp and remain with a one-dimensional algebraic outer problem. A theorem giving exact conditions for this **nested-fiber elimination** would extend source coverage without invoking general bivariate optimization.