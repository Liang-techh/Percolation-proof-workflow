---
kind: review_result
review_id: review-T-P5-154-uniform-additive-simplex-floor-kuangmanmozun-20260909T1233Z
task_id: T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T12:33:00Z
claim_commit: 6854e794e940249366a854a6a5b61479829872db
inspected_commit: 5d3bf8beefe1ef1534901db6d0612d3f5e496ab8
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING-guyuefangyuan-20260909T1223Z.md
    commit: 64a4676b364a81dd196864d7677be2ee587e22c6
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_uniform_additive_floor_as_copositive_quadratic_form; never_promote_pairwise_edge_repairs_to_full_simplex_sufficiency; use_exact_rational_PSD_as_a_sound_fast_path_and_explicit_simplex_witnesses_as_fail_closed_obstructions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact ordered-field/quadratic-form algebra only
exit_code: n/a
---

# T-P5-154 — uniform additive simplex floor is a copositivity problem

## 0. Narrow seam and non-overlap

T-P5-153 exactly closes the **zero-additive-floor** question for homothetic centered cells by the pairwise signs

`K_ij=(tau_i-tau_j)(r_i g_j-r_j g_i)`.

It also observes that if a pair has `K_ij<0`, any uniform additive repair must pay a positive floor, and gives a midpoint edge lower bound. It intentionally does **not** solve the exact uniform floor over the whole uncertainty simplex.

This child attacks only that remaining inequality problem. It proves:

1. the exact full-simplex uniform-floor condition is copositivity of one explicit rational symmetric matrix;
2. pairwise/edge repair checks are not sufficient once three or more uncertainty vertices interact;
3. a three-vertex all-rational counterexample passes every edge exactly but fails at the simplex barycenter;
4. a complete symmetric `N`-vertex family has a sharp closed-form floor, showing a genuine multiway tax;
5. exact rational PSD is a sound root-free fast path, and is sharp on that symmetric family, but PSD failure is not a mathematical failure of the true copositive condition.

No source/admission/provenance audit, receipt work, runtime/Float64 claim, registry mutation, or independent validation is performed.

---

## 1. T-P5-153 additive-repair form

Keep the homothetic notation of T-P5-153. For simplex weights

`lambda_i >= 0`, `sum_i lambda_i = 1`,

define

`g_lambda = sum_i lambda_i g_i`,

with every `g_i>0`, and

`Delta_lambda = sum_{i<j} lambda_i lambda_j K_ij`.

T-P5-153 gives the exact identity

`g_lambda (h_lambda + D)
 = (Delta_lambda + g_lambda D) + b_lambda c_lambda`,

with `g_lambda>0`, `b_lambda>=0`.

Hence a single uniform additive floor `D>=0` is sufficient over the whole simplex if

**(1.1)** `Delta_lambda + g_lambda D >= 0`

for every simplex weight.

If the cell boundary `c_lambda=0` is attainable for every relevant `lambda`, then (1.1) is also necessary for a uniform additive repair. Thus the exact mathematical problem is to understand the minimum of the left side over the simplex.

---

## 2. Homogeneous quadratic matrix

For a fixed candidate `D`, define a symmetric `N x N` matrix `M_D` by

**(2.1)** `M_D[i,i] = D g_i`,

and for `i<j`,

**(2.2)**

`2 M_D[i,j] = K_ij + D(g_i+g_j)`.

Then for every simplex vector `lambda`,

### Theorem A — exact homogenization

**(2.3)**

`lambda^T M_D lambda = Delta_lambda + g_lambda D`.

Proof:

`lambda^T M_D lambda`

`= sum_i D g_i lambda_i^2
   + sum_{i<j} [K_ij + D(g_i+g_j)] lambda_i lambda_j`

`= Delta_lambda
   + D [sum_i g_i lambda_i^2
        + sum_{i<j}(g_i+g_j)lambda_i lambda_j]`.

The bracket equals

`(sum_i g_i lambda_i)(sum_j lambda_j)=g_lambda`

because `sum_j lambda_j=1`. This proves (2.3).

The same identity can be written without imposing `sum lambda=1`:

**(2.4)**

`x^T M_D x
 = (sum_i x_i) D (sum_i g_i x_i)
   + sum_{i<j} K_ij x_i x_j`.

For `x>=0`, `x != 0`, normalize `lambda=x/(sum x)`. Therefore sign on the simplex is equivalent to sign on the whole nonnegative orthant.

---

## 3. Exact condition = copositivity

Recall: a symmetric real matrix `M` is copositive when

`x>=0 ==> x^T M x >=0`.

### Theorem B — exact uniform-floor criterion

Assume `g_i>0` and `D>=0`. Then

**(3.1)**

`Delta_lambda + g_lambda D >=0` for every simplex weight `lambda`

if and only if

**(3.2)** `M_D` is copositive.

The forward implication follows from homogeneous rescaling (2.4); the reverse implication is immediate by taking `x=lambda`.

Consequently, under the same boundary-attainability assumption used for necessity in T-P5-153,

> the exact minimum uniform additive floor is the least `D>=0` for which `M_D` is copositive.

This is the correct full-simplex object. The zero-floor case is special because `M_0` has zero diagonal; then a negative off-diagonal entry is already exposed by a two-coordinate nonnegative vector, so T-P5-153's pairwise sign test is exact. Once `D>0`, positive diagonal loading can hide each pair individually while several negative pair couplings still cooperate in the simplex interior.

---

## 4. Three-vertex counterexample: every edge passes, interior fails

Take three vertices with exact rational data

**(4.1)** `g_1=g_2=g_3=1`,

**(4.2)** `K_12=K_13=K_23=-4`,

and test the candidate uniform floor

**(4.3)** `D=1`.

For any edge, say `lambda=(t,1-t,0)`,

`Delta+gD = 1-4t(1-t)`

`= (2t-1)^2 >=0`.

So **every two-vertex restriction is certified exactly**, with equality at its midpoint.

But at the simplex barycenter

`lambda=(1/3,1/3,1/3)`,

one has

`g=1`,

`Delta=-4*(3/9)=-4/3`,

and therefore

**(4.4)** `Delta+gD = -1/3 <0`.

Equivalently,

`M_1 = [[1,-1,-1],[-1,1,-1],[-1,-1,1]]`,

whose every `2 x 2` principal block is PSD, yet

`(1,1,1) M_1 (1,1,1)^T = -3`.

Thus:

### Corollary C — edge repair is not a simplex repair

For `N>=3`, checking that the candidate additive floor works on every uncertainty edge is **not sufficient** for full-simplex robust closure.

This directly limits how T-P5-153 equation (7.4) may be used: pairwise midpoint bounds are exact lower bounds from violating edges, but their maximum cannot be promoted to the exact uniform floor without an additional multiway theorem.

---

## 5. Sharp complete symmetric family

The preceding example belongs to a family with an exact closed form.

Assume

**(5.1)** `g_i=g>0` for all `i`,

and

**(5.2)** `K_ij=-kappa` for every `i<j`, with `kappa>=0`.

Then for every simplex weight,

`g_lambda=g`,

and

`Delta_lambda = -kappa sum_{i<j} lambda_i lambda_j`.

Use

`(sum_i lambda_i)^2
 = sum_i lambda_i^2 + 2 sum_{i<j}lambda_i lambda_j`

and `sum lambda_i=1` to obtain

**(5.3)**

`Delta_lambda = -(kappa/2)(1-sum_i lambda_i^2)`.

By the elementary Cauchy inequality

`1=(sum_i lambda_i)^2 <= N sum_i lambda_i^2`,

so

`sum_i lambda_i^2 >= 1/N`,

with equality at the barycenter `lambda_i=1/N`.

Therefore

### Theorem D — sharp `N`-way floor

The exact uniform additive floor is

**(5.4)**

`D_* = kappa (N-1) / (2 g N)`.

Indeed,

`Delta+gD >= gD - kappa(N-1)/(2N)`,

so `D>=D_*` is sufficient, and the barycenter makes equality at `D=D_*`, proving necessity.

This is a genuine multiway effect. Restricting to any one edge gives the exact two-vertex floor

**(5.5)** `D_edge = kappa/(4g)`.

Hence

**(5.6)** `D_*/D_edge = 2(N-1)/N`.

For every `N>=3`, the full-simplex floor is strictly larger than every edge floor; as `N` grows the gap approaches a factor of `2`.

The concrete counterexample in Section 4 is `N=3`, `g=1`, `kappa=4`, so

`D_edge=1`,

while

**(5.7)** `D_*=4/3`.

---

## 6. Rational PSD fast path

Copositivity is the exact condition, but a trusted checker does not need to solve a generic copositivity problem before using the result.

### Theorem E — PSD sufficient certificate

If the exact rational matrix `M_D` satisfies

**(6.1)** `M_D >= 0` in Loewner order,

then `M_D` is copositive, hence `D` is a valid uniform additive floor.

This is root-free at the theorem interface. A producer may clear positive denominators and provide any exact rational PSD witness already accepted elsewhere in the project: LDL, matrix-SOS, principal-minor proof in a dimension where that is sound, or a direct Gram factor.

Important fail-closed rule:

> `M_D` not PSD does **not** imply that the uniform floor is invalid.

PSD is only a fast sufficient lane; the exact target is copositivity on the nonnegative orthant.

### Sharpness on the complete symmetric family

At the exact floor (5.4), `M_D` becomes

**(6.2)**

`M_{D_*} = (kappa/2) [ I - (1/N) 11^T ]`.

Indeed its diagonal entries are `kappa(N-1)/(2N)` and its off-diagonal entries are `-kappa/(2N)`.

For any real `x`,

`x^T M_{D_*} x
 = (kappa/2) [sum_i x_i^2 - (1/N)(sum_i x_i)^2] >=0`

by Cauchy. Thus the PSD fast path is **exact** on this nontrivial multiway family; it closes at the same sharp `D_*` found by direct simplex optimization.

This is useful operationally: one should try exact rational PSD before invoking any more expensive copositive-specific reasoning.

---

## 7. A cheaper but weaker coefficient gate

Expanding (2.3) gives

`Delta+gD
 = sum_i D g_i lambda_i^2
   + sum_{i<j}[K_ij+D(g_i+g_j)]lambda_i lambda_j`.

Therefore the purely scalar conditions

**(7.1)** `D>=0`,

**(7.2)** `K_ij + D(g_i+g_j) >=0` for every pair,

are sufficient.

They make every degree-two barycentric coefficient nonnegative. This route is extremely easy to check but can be much looser than PSD. In the `N=3`, `g=1`, `kappa=4` family it requires `D>=2`, whereas the sharp floor is only `4/3`.

Recommended hierarchy for a rational checker is therefore:

1. exact zero-floor pair signs from T-P5-153 when `D=0`;
2. exact rational PSD of `M_D` for a proposed positive uniform floor;
3. coefficientwise gate only as a last very cheap sufficient fallback;
4. if these fail, preserve the problem as copositivity rather than declaring mathematical failure.

---

## 8. Explicit negative witnesses are decisive

Although PSD failure is inconclusive, a nonnegative rational vector is a complete finite obstruction to a proposed `D`.

If a producer finds rational `x_i>=0`, not all zero, with

**(8.1)** `x^T M_D x <0`,

then normalize

`lambda=x/(sum_i x_i)`.

Homogeneity gives

`Delta_lambda+g_lambda D <0`.

If the corresponding homothetic cell boundary is attainable, T-P5-153's identity then produces a true boundary point where

`h_lambda + D <0`.

So the source-facing fail-closed interface can be completely exact:

- PSD witness => certified sufficient floor;
- rational nonnegative negative-direction witness => certified insufficient floor;
- neither => `NOT_CERTIFIED`, not `FAIL`.

The Section 4 witness is simply `x=(1,1,1)`.

---

## 9. Structural complexity note

The copositive reduction is not cosmetic. In the equal-`g` graph-structured subfamily

`K_ij=-kappa` on graph edges and `K_ij=0` on nonedges,

the exact floor is

`D_*=(kappa/g) max_{lambda in simplex} sum_{ij in E} lambda_i lambda_j`.

By the classical Motzkin-Straus identity, this maximum equals

`(1/2)(1-1/omega(G))`,

where `omega(G)` is the clique number. Thus arbitrary-dimension exact uniform-floor computation already contains a standard combinatorial hard problem.

This observation is not needed by any theorem above and should not be used as a formal certificate. Its architectural purpose is narrower: do not expect a universal exact `O(N^2)` pairwise scalar formula for positive additive floors in the fully general homothetic family. The zero-floor miracle of T-P5-153 does not persist after diagonal loading.

---

## 10. Minimal Lean theorem surface

The useful source-independent leaves are small.

### Leaf 1 — `uniformAdditive_homogenize`

For finite weights with `sum lambda=1`, prove the scalar identity

`lambda^T M_D lambda = Delta_lambda + D*g_lambda`

from the entry definitions (2.1)--(2.2).

This is finite-sum/ring algebra.

### Leaf 2 — `uniformAdditive_of_psd`

Assume `0<=lambda_i`, `sum lambda=1`, and `M_D` PSD. Conclude

`0 <= Delta_lambda + D*g_lambda`.

This is Leaf 1 plus the PSD quadratic-form inequality.

### Leaf 3 — `threeVertex_edgePass_interiorFail`

Prove exactly:

- `1-4*t*(1-t)=(2*t-1)^2 >=0` for `0<=t<=1`;
- at `lambda=(1/3,1/3,1/3)`, the same three-pair system gives `-1/3`.

This is a tiny regression theorem preventing future pairwise-floor misuse.

### Leaf 4 — `completeNegativePair_floor`

For `N>0`, simplex weights, `g>0`, `kappa>=0`, prove

`sum_i lambda_i^2 >= 1/N`

and then

`-kappa sum_{i<j}lambda_i lambda_j + g*D >=0`

under

`2*g*N*D >= kappa*(N-1)`.

The statement can be kept division-free. Equality at uniform rational weights proves sharpness when `N` is represented in a field supporting the corresponding rational scalar.

### Leaf 5 — `nonnegativeWitness_refutes_uniformFloor`

From `x>=0`, `sum x>0`, and `x^T M_D x<0`, normalize to a simplex vector and derive a failed additive gate. This packages explicit counterexamples separately from any copositivity decision procedure.

No leaf requires matrix inverse, pseudoinverse, square root, eigensystem, deployed source identity, or a generic copositivity solver.

---

## 11. Source/checker-facing packet

After T-P5-153 has produced exact same-key data

`{g_i,r_i,tau_i,K_ij}`,

a uniform additive consumer should carry

`(uncertaintyKey, cellSlackFamilyKey, D, M_D)`

with exact identities (2.1)--(2.2).

Recommended producer behavior:

1. if all `K_ij>=0`, use zero floor and stop;
2. otherwise choose a rational candidate `D` from the downstream available budget;
3. build exact rational `M_D`;
4. first attempt exact PSD/LDL;
5. if PSD fails, search for a small-support rational nonnegative negative direction;
6. if a negative direction is found, record its support and exact deficit as a genuine obstruction;
7. if no witness is found, leave the floor `NOT_CERTIFIED_BY_PSD` rather than inventing a pairwise closure.

For symmetric or otherwise structured families, derive a specialized exact theorem before invoking generic copositivity machinery.

---

## 12. Failure branches and boundaries

This child does **not** justify any of the following:

- taking the maximum of T-P5-153 pairwise midpoint deficits as a full-simplex floor;
- treating all `2 x 2` principal restrictions of `M_D` as sufficient when `N>=3`;
- declaring a floor false merely because `M_D` has a negative eigenvalue;
- using graph/clique complexity observations as source or theorem admission evidence;
- omitting the boundary-attainability assumption when converting a negative additive gate into a physical boundary counterexample;
- mixing separately normalized vertex cell slacks with a different interpolated `cellSlackFamilyKey`.

The result is mathematical only. Actual deployed `{g_i,r_i,tau_i}`, homothetic source identity, same barycentric weights, cell/domain coverage, runtime rounding, Lean compilation, independent validation, and P5 parent closure all remain open.

---

## 13. Requested handoff

The next useful mathematical/source action is now sharply separated:

- if the deployed family is homothetic and a uniform additive budget is available, build `M_D` and try exact rational PSD first;
- if PSD fails, do not fall back to edge-only logic; instead search for a rational nonnegative negative direction or a specialized copositive theorem for the actual low dimension/structure;
- preserve the Section 4 three-vertex regression permanently in any checker that offers a "pairwise additive repair" mode;
- only after the actual same-key `{g_i,r_i,tau_i}` packet is available should numerical floor optimization be attempted.

The key new obstruction is structural: **zero-floor robust closure is pairwise in the homothetic family, but positive uniform additive repair is genuinely multiway.**