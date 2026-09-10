---
kind: review_result
review_id: review-T-P5-270-algebraic-moving-fiber-thom-closure-kuangmanmozun-20260910T1830Z
task_id: T-P5-270-ALGEBRAIC-MOVING-FIBER-THOM-CLOSURE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T18:30:00Z
claim_commit: fa0c6e21612486f64120ed26b77f785d134a7a9c
inspected_commit: 8dff53f6d2f3db2cfc654f01e77c061ee760e8ad
upstream_commits:
  - 5334199bdb2c7b093239ffb72ffd4c759294323c # T-P5-269 moving rational fiber exact clamp
  - d062e528bc248cd24f09973dcde7cfcf7c00ffae # T-P5-266 zero-margin Sturm packet
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_selected_algebraic_endpoint_clamp; add_branch_safe_projection_atlas; add_selected_root_sign_evaluator; add_algebraic_margin_critical_resultant; reject_norm_only_branch_signs; preserve_source_binding_boundary
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact real-algebraic derivation, implicit differentiation, resultant/subresultant breakpoint analysis, rational counterexamples; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-270 — Algebraic moving fiber: branch-safe Thom / projection closure

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-269 proved that rational moving endpoints preserve the one-dimensional `q` route, but left algebraic endpoints open because a resultant or field norm multiplies all conjugate branches and therefore cannot determine the sign on the selected physical endpoint.

This child closes that mathematical seam at the exact-real level. The main result is that an algebraic moving interval

`a(q) <= s <= b(q)`,

with `a,b` specified as selected simple real roots of polynomial equations, still does **not** require a genuinely bivariate optimizer. The quadratic clamp remains the same LEFT / RIGHT / INTERIOR clamp pointwise, while all branch signs can be decided on a finite one-dimensional algebraic cell atlas in `q`. The correct object is a **selected-root sign evaluator** (isolating interval or Thom encoding + Sturm/subresultant sign determination), not the sign of a resultant.

A second new result gives an exact route to a **uniform reserve floor** on an algebraic branch. For `h(q)=H(q,a(q))`, the only interior extrema on a simple branch are among the selected common roots of

`P(q,z)=0`

and

`N_H(q,z):=H_q P_z-H_z P_q=0`.

Hence a compact-cell reserve minimum is attained at finitely many endpoint / critical algebraic candidates. This is stronger than merely deciding `h>=0`: it gives an exact finite candidate set for the sharp margin consumed downstream.

No deployed P5 algebraic endpoint packet, same-key source fiber, state realization, coverage, Float64 semantics, Lean/kernel theorem, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Fix a compact radial interval `I=[q0,q1] subset R`.

Let

`A(q,s)=A0(q)+A1(q)s-A2(q)s^2`,

with `A0,A1,A2 in Q[q]`, and set

`C(q)=K-A0(q)`,

`p(q,s)=K-A(q,s)=C(q)-A1(q)s+A2(q)s^2`.

The moving endpoints are algebraic branches:

`P_a(q,a(q))=0`,

`P_b(q,b(q))=0`,

where `P_a,P_b in Q[q,z]` are primitive in `z`. On every open branch cell considered below, the selected roots are real and simple:

`(P_a)_z(q,a(q)) != 0`,

`(P_b)_z(q,b(q)) != 0`.

The branch identity is part of the data: one may use either an isolating interval containing exactly one real root, or a Thom encoding of the selected root. This selector is not optional.

Define the endpoint derivative tests

`g_a(q)=A1(q)-2A2(q)a(q)`,

`g_b(q)=A1(q)-2A2(q)b(q)`,

and endpoint reserves

`e_a(q)=C(q)-A1(q)a(q)+A2(q)a(q)^2`,

`e_b(q)=C(q)-A1(q)b(q)+A2(q)b(q)^2`.

Also define the rational interior reserve

`F(q)=4A2(q)C(q)-A1(q)^2`.

---

## 2. Theorem A — algebraic endpoints do not change the clamp theorem

Assume at a fixed `q` that

`a(q) <= b(q)` and `A2(q)>=0`.

Then `A(q,s)<=K` for all `s in [a(q),b(q)]` is equivalent to the following exact clamp.

### LEFT

If `g_a<=0`, then safety is equivalent to

`e_a>=0`.

### RIGHT

If `g_a>0` and `g_b>=0`, then safety is equivalent to

`e_b>=0`.

### INTERIOR

If `g_a>0>g_b`, then automatically `A2>0`, and safety is equivalent to

`F>=0`.

### Proof

For fixed `q`, `p(s)=C-A1 s+A2 s^2` is convex. Its derivative is

`p'(s)=-A1+2A2 s`.

Thus `g_a=-p'(a)` and `g_b=-p'(b)`. The minimum of `p` on `[a,b]` is at `a`, at `b`, or at the unique stationary point according to exactly the three sign branches above. In the interior branch, `g_a-g_b=2A2(b-a)>0`, hence `A2>0`. At the stationary point,

`4A2 p=(2A2 s-A1)^2+F`,

so the minimum is `F/(4A2)`. No rationality of `a,b` is used. QED.

**Consequence.** The only new difficulty created by algebraic endpoints is selected-branch sign evaluation for `a<=b`, `g_a,e_a,g_b,e_b`; the inequality optimization itself is already closed.

---

## 3. Lemma B — selected-root sign evaluation is exact and branch-safe

Let `P(z),H(z) in K[z]`, where `K` is any exact real-algebraic ordered field, and let `alpha` be a selected real root of `P` represented by an isolating interval or Thom encoding.

Then `sign(H(alpha))` is decidable exactly by a terminating Sturm/subresultant procedure.

A constructive version is enough for the present checker:

1. squarefree-factor `P` and identify the factor/root carrying `alpha`;
2. compute `G=gcd(P,H)` in `K[z]`;
3. use the root selector to decide whether `alpha` is a root of `G`; if yes, `H(alpha)=0`;
4. otherwise isolate `alpha` away from all real roots of `H` by exact interval refinement; `H` has constant sign on that refined isolating interval, so the sign at any exact sample point is `sign(H(alpha))`.

Equivalent implementations may use Sturm-Habicht / signed subresultant sign determination directly from the Thom encoding.

The important statement is semantic:

**the selector identifies one real conjugate, and the sign computation is performed on that conjugate.**

No product over all conjugates is substituted for it.

---

## 4. Exact counterexample — `Res=0` does not even mean the selected branch is a contact

It is already known from T-P5-269 that the **sign** of a resultant can be opposite to the sign on the selected branch. There is a second, independent bug that matters at zero margin.

Take

`P(z)=(z-1)(z+1)`

and select the physical branch

`alpha=1`.

Let

`H(z)=z+1`.

Then

`Res_z(P,H)=0`

because `H` vanishes at the *other* conjugate `z=-1`. But on the selected branch,

`H(alpha)=2>0`.

Therefore the implication

`Res(P,H)=0 -> H(alpha)=0`

is false unless branch membership in the gcd/common-root set is checked.

This is why the zero-resultant cell must remain branch-aware; it cannot be treated as an endpoint contact automatically.

---

## 5. Theorem C — finite branch-safe projection atlas in the radial variable

Consider the finite selected-branch expressions needed by Theorem A:

`H_ga(q,z)=A1(q)-2A2(q)z`,

`H_ea(q,z)=C(q)-A1(q)z+A2(q)z^2`,

with the analogous two expressions for branch `b`.

Form a finite breakpoint family in `Q[q]` containing:

1. leading-coefficient / degree-drop polynomials for `P_a,P_b` in `z`;
2. discriminants `Disc_z(P_a)`, `Disc_z(P_b)`;
3. `Res_z(P_a,H_ga)`, `Res_z(P_a,H_ea)`;
4. `Res_z(P_b,H_gb)`, `Res_z(P_b,H_eb)`;
5. `Res_z(P_a,P_b)` for possible endpoint collisions;
6. `A2(q)` and `F(q)`;
7. if a Thom signature itself is used as the persistent branch label, the extra principal subresultant / derivative-contact polynomials needed to keep that encoding stable.

Discard identically-zero projection polynomials only after gcd/factor analysis has explained the persistent algebraic relation.

Let `J` be a connected component of `I` after removing the real roots of all nonzero breakpoint polynomials. Suppose the selected roots `a(q),b(q)` are continued from one sample point through `J` along their simple real branches.

Then throughout `J`:

- the number and order of simple real roots of each endpoint polynomial are unchanged;
- the selected branches cannot cross each other unless `Res(P_a,P_b)=0`;
- `g_a,e_a,g_b,e_b` cannot change sign without the corresponding endpoint resultant vanishing;
- `A2` and `F` cannot change sign without their own polynomial vanishing.

Therefore **the entire LEFT / RIGHT / INTERIOR clamp verdict is constant on `J`.**

### Proof idea

Simple selected roots vary continuously by the implicit-function theorem. A sign such as `H(q,a(q))` is continuous. If it changed sign inside `J`, it would vanish at some point; then `P(q,z)` and `H(q,z)` would share the selected root there, forcing the corresponding resultant to vanish, contradicting the definition of `J`. Endpoint order changes only through equality, likewise forcing `Res(P_a,P_b)=0`. QED.

### Exact algorithmic consequence

All roots of the finite projection family are real algebraic numbers and can be isolated exactly. Each open cell contains a rational sample `q*`. At this single rational sample, selected endpoint roots are ordinary real algebraic numbers over `Q`, and Lemma B decides all required signs exactly. The sign packet then applies to the whole open cell by Theorem C.

At the finitely many point cells (projection roots), evaluate the clamp directly in the corresponding real-algebraic field using the same selected-root sign machinery.

Thus the algebraic moving-fiber problem remains a **finite one-dimensional exact decision problem in `q`**.

---

## 6. Degenerate projection identities must be reduced, not ignored

A resultant may vanish identically for two very different reasons.

### Persistent selected contact

If the selected branch lies in `gcd(P,H)` over `Q(q)[z]`, then

`H(q,a(q)) identically = 0`

on that branch cell. This is a legitimate zero-margin/touching identity and should be carried as such.

### Contact only on another algebraic branch

If `gcd(P,H)` contains a different root branch but not the selected one, the selected value of `H` can stay strictly nonzero even though the resultant vanishes identically or at the current parameter. The selected root must be tested for membership in the gcd factor.

Hence the correct dispatcher on an identically-zero or zero specialized resultant is:

`factor/gcd -> selected-root membership -> ZERO on selected branch or continue with selected cofactor/sign evaluation`.

Never use

`resultant==0 -> selected reserve==0`.

---

## 7. Theorem D — exact finite candidate set for a sharp algebraic reserve floor

The preceding atlas proves nonnegativity, but downstream Schur / bootstrap consumers often need an actual reserve `eta>0`. Algebraic branches still permit an exact finite search for the sharp floor.

Let `a(q)` be a simple selected branch of

`P(q,z)=0`

on a compact cell `[u,v]`, with `P_z(q,a(q)) != 0`. Let

`h(q)=H(q,a(q))`

for `H in Q[q,z]`.

Define the **implicit critical numerator**

`N_H(q,z):=H_q(q,z) P_z(q,z)-H_z(q,z) P_q(q,z)`.

Then along the selected branch,

`h'(q)=N_H(q,a(q))/P_z(q,a(q))`.

Therefore every interior critical point of `h` lies among selected common roots of

`P(q,z)=0`,

`N_H(q,z)=0`.

Consequently the minimum of `h` on `[u,v]` is attained among the finite branch-aware candidate set:

- the two cell endpoints;
- selected real common roots of `P` and `N_H` above real roots of `Res_z(P,N_H)` in `(u,v)`;
- persistent-critical branch components detected by gcd if the resultant is identically zero.

Each candidate value is a real algebraic number and can be compared exactly by sign determination.

Thus an exact reserve floor exists as an algebraic number

`eta_* = min h(q)`

and any proposed rational reserve `eta` can be certified by the finite exact test

`h(q)-eta >= 0`

on the same atlas.

This supplies the missing bridge from branch safety to a **sharp/nonsharp constant packet** suitable for downstream budget accounting.

---

## 8. Worked exact example — an interior algebraic reserve minimum

Take

`P(q,z)=z^2-q`,

select `a(q)=+sqrt(q)`, and work on `q in [1,9]`.

Let

`H(q,z)=(z-2)^2+1/5`.

Then

`h(q)=(sqrt(q)-2)^2+1/5`.

The branch is simple since `P_z=2z>0` on this cell.

Here

`H_q=0`,

`H_z=2(z-2)`,

`P_q=-1`,

so

`N_H=2(z-2)`.

Hence the critical resultant is, up to a positive nonzero constant,

`Res_z(z^2-q, 2(z-2)) = 4(4-q)`.

The only interior critical base point is exactly

`q=4`,

where the selected root is `z=2` and

`h(4)=1/5`.

The endpoint values are larger, so the exact sharp reserve is

`eta_*=1/5`.

This illustrates why a contact-only resultant `Res(P,H)` is not enough for sharp budget extraction: `H` never vanishes here, yet the positive reserve has a genuine interior minimum detected by `Res(P,N_H)`.

---

## 9. Endpoint order and collision semantics

For two independently defined branches `a,b`, endpoint order is itself selected-root data.

On an open projection cell where `Res_z(P_a,P_b) != 0`, the continuous branches cannot collide, so the sign of `b-a` is constant and one exact sample fixes the order for the whole cell.

At a collision cell, do not silently swap labels. Evaluate the source semantics:

- if the source authorizes the unordered pair and interval endpoints may be sorted, sort explicitly and record that contract;
- if `a` and `b` have physical roles (e.g. lower/upper roots from different inequalities), a collision or order reversal requires a source-specific branch dispatch;
- if `a=b`, use the singleton-fiber endpoint evaluation rather than the nondegenerate clamp.

A failed branch-order contract is **ALGEBRAIC_ENDPOINT_LANE_NOT_APPLICABLE**, not automatically a physical counterexample.

---

## 10. Counterexample — discriminant points cannot be swallowed into one open branch

Take

`P(q,z)=z^2-q`

with selected branch `z=+sqrt(q)` for `q>0`.

At `q=0`,

`Disc_z(P)=4q=0`

and the two real branches collide. For `q<0` there is no real endpoint at all.

Any dispatcher that omits the discriminant/degree-drop boundary and simply continues a root label across `q=0` would manufacture a nonexistent real source fiber. Therefore discriminant point cells are not bookkeeping noise; they are required branch-domain boundaries.

---

## 11. Exact theorem-level fingerprint

The reusable fingerprint is

`quadratic nuisance parameter + selected algebraic moving endpoints`

`-> pointwise convex LEFT/RIGHT/INTERIOR clamp unchanged`

`-> carry isolating interval / Thom root selector`

`-> build finite q-projection set from endpoint discriminants, endpoint/contact resultants, endpoint-collision resultant, A2 and F`

`-> open q-cells: selected branch/order/sign packet constant`

`-> one rational sample per open cell + exact selected-root sign determination`

`-> projection point cells: direct algebraic evaluation`

`-> zero/identically-zero resultant: gcd + selected-root membership, never norm semantics`

`-> reserve floor: N_H=H_q P_z-H_z P_q`

`-> critical q candidates from Res_z(P,N_H) + endpoints`

`-> exact algebraic minimum / rational reserve certificate`.

This retains the one-dimensional radial architecture while allowing genuinely algebraic source fibers.

---

## 12. Minimal formalizable theorem statements

The first Lean targets should remain ordered-field / polynomial-level and avoid implementing CAD immediately.

### Leaf 1 — algebraic endpoint clamp

For arbitrary real `a<=b`, `A2>=0`, prove the LEFT/RIGHT/INTERIOR equivalence of Theorem A. This theorem contains no algebraic-number machinery.

### Leaf 2 — implicit derivative identity

Assume differentiable `P,H,a` and

`P(q,a(q))=0`, `P_z(q,a(q)) != 0`.

Prove

`d/dq H(q,a(q)) = (H_q P_z-H_z P_q)(q,a(q))/P_z(q,a(q))`.

### Leaf 3 — sign cannot change without contact

For continuous `a(q)` with `P(q,a(q))=0`, if `H(q,a(q))` is nonzero on a connected interval, its sign is constant. The resultant/subresultant layer supplies the nonvanishing certificate externally.

### Leaf 4 — branch order cannot change without collision

For continuous real branches `a,b`, if `a(q)!=b(q)` on a connected interval, `sign(b-a)` is constant.

### Leaf 5 — compact critical-point reserve principle

For differentiable `h` on `[u,v]`, every strict interior minimizer satisfies `h'=0`; instantiate Leaf 2 to reduce branch minima to `N_H=0`.

These leaves separate the analytic/ordered-field facts from the computer-algebra root-isolation implementation.

---

## 13. Fail-closed semantics

The following distinctions are mandatory.

- `Res(P,H)` sign mismatch with selected `H(alpha)`: **branch-selector bug**, not a mathematical failure of the target inequality.
- `Res(P,H)=0` because another conjugate is a contact: **OTHER_BRANCH_CONTACT**, not selected touching.
- selected `H(alpha)=0`: legitimate zero-margin cell; send to touching/Sturm exact lane.
- discriminant / degree-drop point: isolate as a branch-domain point cell; do not extrapolate the simple-root proof through it.
- selected branch ceases to be real or cannot be continued according to the source contract: **ALGEBRAIC_ENDPOINT_LANE_NOT_APPLICABLE**.
- exact negative selected reserve on a proved same-key moving source fiber: mathematical counterexample for that declared fiber; physical/source FAIL still requires state realization and source binding.
- failure of a finite-degree SOS or heuristic algebraic-number package: **CERTIFICATE_NOT_FOUND**, never mathematical FAIL.

---

## 14. Remaining obligations

Still open:

1. identify whether the deployed P5 source actually produces algebraic endpoint equations `P_a,P_b`;
2. prove the selected roots are the true same-key fiber endpoints, not an outer approximation;
3. provide branch selectors and domain cells for the actual source;
4. bind endpoint order, source key, metric, chart and nuisance parameter;
5. extract actual `A0,A1,A2,K` and prove `A2>=0` where this lane is used;
6. state/state-trajectory realization of violations;
7. cell/flowed-sheet/FD-halo/reference-halo coverage;
8. Float64/libm/interval semantics;
9. Lean/kernel formalization;
10. independent validation by 封不觉;
11. admission, registry mutation, and P5/P8/M4 parent propagation.

---

## 15. Next mathematical seam

After this child, the generic algebraic-endpoint sign problem is no longer the bottleneck. The next source-facing branch is a dichotomy:

- if actual source fibers are endpoint graphs `a(q),b(q)`, instantiate this projection atlas and extract a certified reserve floor;
- if the source instead gives a coupled semialgebraic fiber such as `P(q,s)>=0` with several disjoint `s` components, then endpoint-graph language is insufficient. The next independent mathematical child should be a **multi-component semialgebraic fiber decomposition**: exact root ordering of `P(q,·)`, component-wise quadratic clamp, and merger/split handling at discriminant cells.

That is a genuinely new geometry problem; it should not be hidden behind fictitious single-valued endpoints.