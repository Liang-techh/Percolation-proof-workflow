---
kind: review_result
review_id: review-T-P5-232-coupled-fiber-conditional-schur-reduction-guyuefangyuan-20260910T0928Z
task_id: T-P5-232-COUPLED-FIBER-CONDITIONAL-SCHUR-REDUCTION
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T09:28:00Z
claim_commit: e7a6402187be82d4a4c58ae1271d3274b7b35d81
inspected_commit: d21c940c4d61ed3e03e60aef7b697682f762838a
upstream_commits:
  - f91212c7b6b45b35e88e2a71c17b712b363c480d  # T-P5-231 anisotropic kernel-fiber scaling
  - 95fc7a17795dda55ed0f493d5588c573ef84151d  # T-P5-230 curved ellipsoid trust-region
  - 575e296e13600ee0aa7b043dde8dd3b0f97b2ca1  # T-P5-229 bounded flat-fiber support
  - db655d40ee23d1c71f03f46eb20d112d0553b2fa  # T-P5-228 fiber-sign radical annihilation
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_conditional_distance_exact_reduction; add_conditional_curvature_second_schur_gate; add_graph_induced_curvature_radical_classifier; preserve_exact_inner_outer_fiber_semantics
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic/support mathematics only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-232 — coupled-fiber conditional Schur reduction

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-231 gave the exact semidefinite-curvature decomposition

`sup q_t = A t^2 + 2t h_{K_N(t)}(b_N)`

under a genuine direct-product assumption between the curved `range(H)` fiber and the flat `ker(H)` fiber, with the curved Schur center independently admissible. Its handoff correctly warned that a coupled source fiber must not be replaced silently by that product.

This child removes that product assumption exactly.

The central result is that an arbitrary coupled fiber is governed not by a naked support function, but by a **support-minus-conditional-distance** functional. If realizing a nominally flat kernel displacement forces motion in the negatively curved range coordinates, that conditional distance induces a second quadratic curvature on the kernel coordinates. Consequently an apparent T-P5-231 `O(t)` / `t^(1+p)` obstruction can disappear completely: the coupled problem may become quadratic-order Schur absorption.

The genuinely flat directions are therefore not simply `ker(H)`. After source coupling is imposed, they are the directions in `ker(H)` that also lie in the radical of the induced conditional curvature.

No actual P5 source fiber, same-cell/tube coverage, Float64 enclosure, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. General semidefinite setup

Let the gauge space split orthogonally as

`E = R orthogonal_sum N`,

with symmetric `H>=0`,

`R = range(H)`, `N = ker(H)`.

Write a gauge coordinate as `alpha=u+z`, `u in R`, `z in N`, and decompose

`b=b_R+b_N`.

Choose the unique `x in R` satisfying

`H x = b_R`.

For physical amplitude `t>0`, consider

`q_t(u,z) = t^2 c + 2t <b_R,u> + 2t <b_N,z> - <u,H u>`.

Set

`A := c + <b_R,x> = c + <x,Hx>`.

Completion of the curved square gives the pointwise identity

**`q_t(u,z) = t^2 A + 2t <b_N,z> - <u-tx, H(u-tx)>`.**

This identity is the only input needed below.

---

## 2. Exact arbitrary-coupling reduction

Let `F_t subset R x N` be the actual admissible fiber. It need not be a product, convex, symmetric, or a graph.

For each kernel coordinate `z`, define the conditional curved slice

`U_t(z) := {u in R : (u,z) in F_t}`

and the extended conditional distance

`delta_t(z) := inf_{u in U_t(z)} <u-tx,H(u-tx)>`,

with `delta_t(z)=+infinity` when `U_t(z)` is empty.

### Theorem A — `coupledFiber_sup_eq_supportMinusConditionalDistance`

For every `t>0`,

**`sup_{(u,z) in F_t} q_t(u,z)`**

**`= t^2 A + sup_z [ 2t <b_N,z> - delta_t(z) ]`.**

### Proof

For fixed `z`, the only `u`-dependent term in the completed-square identity is

`-<u-tx,H(u-tx)>`.

Therefore

`sup_{u in U_t(z)} q_t(u,z)`

`= t^2 A + 2t<b_N,z> - inf_{u in U_t(z)} <u-tx,H(u-tx)>`.

Taking the supremum over all `z` proves the identity. No minimizer or compactness is required; ordinary extended-real `sup/inf` is enough. QED.

### Recovery of T-P5-231

If

`F_t = U_t x K_N(t)`

and the curved Schur center `tx` belongs to `U_t`, then `delta_t(z)=0` for every `z in K_N(t)`. Theorem A becomes exactly

`sup q_t = t^2 A + 2t h_{K_N(t)}(b_N)`.

Thus T-P5-231 is the zero-conditional-distance special case, not the generic coupled case.

---

## 3. Conditional curvature produces a second Schur gate

The exact function `delta_t` may be complicated, but a source may be able to prove a quadratic lower envelope.

Assume there is a symmetric PSD matrix/operator `R_N>=0` on `N` such that for every admissible `(u,z) in F_t`,

**`<u-tx,H(u-tx)> >= <z,R_N z>`.**

Equivalently, `delta_t(z)>=z^T R_N z` on the projected fiber.

### Theorem B — `conditionalCurvature_rangeSchur_upper`

If `b_N in range(R_N)` and a producer supplies `y` satisfying

`R_N y = b_N`,

then for every admissible `(u,z)`,

**`q_t(u,z) <= t^2 (A + <b_N,y>)`.**

Hence if

`A + <b_N,y> <= 0`,

the entire coupled fiber is safe; if the inequality is strict, a strict quadratic reserve remains.

### Proof

By the conditional-curvature lower bound,

`q_t(u,z) <= t^2 A + 2t<b_N,z> - <z,R_N z>`.

Using `R_N y=b_N`, complete the second square:

`2t<b_N,z>-<z,R_Nz>`

`= t^2 <y,R_Ny> - <z-ty,R_N(z-ty)>`

`= t^2 <b_N,y> - <z-ty,R_N(z-ty)>`

`<= t^2 <b_N,y>`.

QED.

### Why this is stronger than the flat support bound

A naked outer box or product model discards the compulsory curved displacement hidden in `delta_t`. Theorem B keeps that displacement as negative energy. A source can therefore certify a quadratic Lyapunov gate even when the projection of the fiber onto `N` has fixed nonshrinking radius.

The trusted packet needs only:

1. `R_N>=0`;
2. the pointwise conditional-curvature inequality;
3. an exact solve `R_N y=b_N`;
4. the scalar sign `A+b_N^T y<=0`.

No pseudoinverse is required.

---

## 4. Exact graph coupling and induced curvature

A particularly important source contract is an exact linear graph:

**`u = t x + L z`,**

with `L : N -> R`.

Then

`delta_t(z) = <Lz,H Lz>`

and the induced kernel curvature is

**`R_L := L^* H L >=0`.**

Therefore the full fiber problem becomes exactly

**`q_t = t^2 A + 2t <b_N,z> - <z,R_L z>`.**

This is a second Schur problem on the old kernel coordinates.

### Theorem C — `graphFiber_inducedRadical_eq_ker`

Because `Lz in R=range(H)` and `H` is positive definite on `R`,

**`ker(R_L) = ker(L)`.**

### Proof

`z^T R_L z = <Lz,H Lz>`.

The right side is zero iff `Lz=0`, since `H|_R` is positive definite. For PSD `R_L`, zero quadratic value is equivalent to membership in its kernel. QED.

### Structural consequence

The truly flat subspace after coupling is

**`N_flat = ker(L)`,**

not all of `N=ker(H)`.

If `L` is injective, the apparent flat kernel is completely curved by the source constraint. Every kernel forcing direction is then Schur-absorbable at quadratic order, subject only to the finite-domain/trust-region gate.

If `L` has a kernel, only the component of `b_N` visible on `ker(L)` retains the T-P5-229/231 support obstruction.

---

## 5. Recursive range/kernel decomposition on the induced curvature

Let

`N = range(R_L) orthogonal_sum ker(R_L)`

and write

`b_N = b_c + b_f`.

Choose `y in range(R_L)` with

`R_L y = b_c`.

For `z=z_c+z_f`,

`2t<b_N,z>-z^T R_L z`

`= t^2 <b_c,y> - <z_c-ty,R_L(z_c-ty)> + 2t<b_f,z_f>`.

Therefore, if the source fiber in these *second-stage* coordinates is a genuine product and contains `ty` in the curved factor, then

**`sup q_t = t^2 (A+<b_c,y>) + 2t h_{K_f(t)}(b_f)`.**

This is exactly the T-P5-231 theorem one level deeper.

The correct dispatcher is therefore recursive:

`H range/kernel split`

`-> impose actual source coupling`

`-> induced curvature R_L`

`-> R_L range/kernel split`

`-> only then apply flat support/exponent logic to ker(R_L)`.

A checker that applies flat support logic immediately to all of `ker(H)` can be arbitrarily conservative and can manufacture a false source-level FAIL when the supposed kernel displacement is not independently realizable.

---

## 6. Sharp scaling law for graph-coupled shrinking fibers

The T-P5-231 critical exponent `p=1` changes interpretation once induced curvature is positive definite.

Assume `R_L>0` on `N`, `b_N!=0`, and

`K_t = t^p K`,

where `K` is compact and contains a neighborhood of `0`. Consider

`Phi(t) := sup_{z in K_t} [2t b_N^T z - z^T R_L z]`.

Let `y=R_L^{-1} b_N`.

### Theorem D — graph-coupled exponent trichotomy

#### D1. `p<1`

For sufficiently small `t`, the unconstrained Schur maximizer

`z_*=t y`

belongs to `t^p K`, since

`t y / t^p = t^(1-p) y -> 0`.

Hence exactly

**`Phi(t)=t^2 b_N^T y`**

for all sufficiently small `t`.

So the large/shrinking-slower-than-linear fiber does **not** create a subquadratic obstruction; the negative induced curvature clips the optimizer at amplitude `O(t)`.

#### D2. `p=1`

Writing `z=t xi` gives the exact formula

**`Phi(t)=t^2 sup_{xi in K} [2b_N^T xi - xi^T R_L xi]`.**

This is a dimensionless trust-region/convex quadratic gate.

#### D3. `p>1`

Writing `z=t^p xi`,

`Phi(t)=sup_{xi in K} [2 t^(1+p)b_N^T xi - t^(2p) xi^T R_L xi]`.

Since `2p>1+p`,

**`Phi(t)=2 h_K(b_N) t^(1+p) + O(t^(2p))`.**

Thus the fiber is so small that curvature is higher order; the remaining effect is the same support term as in the flat theory, but now it is already higher than quadratic order.

### Comparison with T-P5-231

For a genuinely flat product fiber, T-P5-231 found `p<1` to be fatal because `t^(1+p)` dominates `t^2`.

For an injectively graph-coupled fiber, this child finds:

- `p<1`: exact quadratic Schur order;
- `p=1`: exact quadratic trust-region order;
- `p>1`: higher-order support leakage.

So the product assumption is mathematically decisive. The source geometry can reverse the apparent `p<1` obstruction.

---

## 7. Exact rational regression: coupling removes a false flat-fiber FAIL

Take one curved coordinate `u`, one nominally flat coordinate `z`, with

`H=1`, `b_R=0`, `b_N=1`, `c=-2`.

Then

`q_t(u,z) = -2t^2 + 2tz - u^2`.

### Product fiber

Let

`F_t^prod = {(u,z): u=0, |z|<=1}`.

Then

`sup q_t = -2t^2 + 2t >0`

for every `0<t<1`. This is the T-P5-229/231 flat support obstruction.

### Coupled graph fiber

Instead impose the exact source relation

`u=z`, `|z|<=1`.

Then

`q_t = -2t^2 + 2tz - z^2`.

For `0<t<=1`, the maximizer is `z=t`, and

**`sup q_t = -t^2 <0`.**

The projected `z` interval is identical in the two models. The only difference is the compulsory curved displacement. Replacing the coupled graph by the product projection therefore changes a safe exact instance into an apparent small-amplitude failure.

This is not a minor numerical conservatism; it changes the asymptotic order from `O(t)` to `O(t^2)`.

---

## 8. Exact rational regression: only the coupling radical remains dangerous

Take one curved coordinate and two kernel coordinates,

`H=1`, `L=[1,0]`, `b_N=(0,1)`, `c=-2`.

The graph is

`u=z_1`, `|z_1|<=1`, `|z_2|<=1`.

Then

`R_L = diag(1,0)`,

`ker(R_L)=span(e_2)=ker(L)`.

The quadratic is

`q_t=-2t^2 + 2t z_2 - z_1^2`.

Choosing `z_1=0,z_2=1` gives

`q_t=-2t^2+2t>0`

for `0<t<1`.

Thus coupling does not magically remove every flat obstruction. It removes exactly the directions that are forced into curved range motion; the residual radical `ker(L)` must still be handled by support/exponent logic.

---

## 9. Inner / exact / outer fiber semantics

The conditional-distance viewpoint makes approximation direction explicit.

If `F_actual subset F_outer`, then

`sup_{F_actual} q_t <= sup_{F_outer} q_t`.

Therefore an outer coupled-fiber packet can certify **PASS** when its upper bound is nonpositive, but a positive outer supremum is not a physical FAIL.

If `F_inner subset F_actual`, then

`sup_{F_inner} q_t <= sup_{F_actual} q_t`.

Therefore an explicit positive witness in an inner/exact source fiber certifies **FAIL**.

Likewise, a lower bound on conditional distance,

`delta_actual(z) >= z^T R_N z`,

is a PASS-oriented certificate because it supplies extra negative curvature. It cannot by itself prove a FAIL. A FAIL needs an upper bound on the actual conditional cost together with an actual/inner realizable `z`, or a concrete source witness `(u,z)`.

This distinction must remain typed in any producer/checker interface.

---

## 10. Suggested source packet

A useful source producer should not export only the marginal kernel radius. For each same-key cell/tube it should try to export one of:

1. **exact graph:** `u-tx=Lz`;
2. **conditional-curvature lower packet:** a rational PSD `R_N` and a proof/certificate that
   `<u-tx,H(u-tx)> >= z^T R_N z` on the actual fiber;
3. **exact/inner flat residual packet:** a realizable family in the radical of the induced curvature for FAIL analysis.

For exact graph data, the downstream algebra is finite:

`R_L=L^T H L`, range test for `b_N`, exact solve `R_L y=b_N`, and one scalar quadratic reserve. Only if the range test fails does the support/exponent branch remain necessary.

This is substantially sharper than exporting independent coordinate boxes for `u` and `z`.

---

## 11. Lean decomposition

The first formalization should stay finite-dimensional and avoid pseudoinverses.

Suggested leaves:

1. `semidefinite_split_completedSquare`
   - assumptions `Hx=b_R`, `Hz=0`;
   - prove the pointwise completed-square identity.

2. `coupledFiber_sup_eq_supportMinusConditionalDistance`
   - set-level `sup`/`inf` theorem for arbitrary fiber slices.

3. `conditionalCurvature_rangeSchur_upper`
   - assumptions `R>=0`, `Ry=b`, and conditional quadratic lower bound;
   - conclude the quadratic upper bound.

4. `graphFiber_inducedCurvature_psd`
   - prove `L^T H L>=0`.

5. `graphFiber_inducedRadical_eq_ker`
   - with `range(L) subset range(H)` / positive definiteness on the curved subspace, prove `ker(L^T H L)=ker(L)`.

6. `graphFiber_secondSchur_completedSquare`
   - exact identity using an explicit solve `R_L y=b_c`.

7. Two tiny rational regression lemmas for Sections 7 and 8.

The asymptotic scaling theorem can be formalized later; the exact algebraic core above already gives a sound source/checker seam.

---

## 12. Remaining obligations

This child does **not** prove that the actual P5 fiber is a graph, a product, or satisfies any particular conditional-curvature lower bound. The following remain open and must stay explicit:

- actual same-key P5 source relation between curved and kernel lift coordinates;
- whether the source fiber is exact, inner, or outer;
- same-cell/tube and trajectory coverage;
- actual amplitude variable and source dilation law;
- rational/interval enclosure for `H,L,R_L,b_N` under deployed Float64 semantics;
- exact range solve / strict reserve for concrete instances;
- Lean implementation and pinned compile;
- independent validation by 封不觉;
- admission / registry / parent closure.

The mathematical advance is the removal of T-P5-231's product assumption at the theorem level and the identification of **conditional induced curvature** as the correct object deciding whether an apparent kernel direction is genuinely flat.