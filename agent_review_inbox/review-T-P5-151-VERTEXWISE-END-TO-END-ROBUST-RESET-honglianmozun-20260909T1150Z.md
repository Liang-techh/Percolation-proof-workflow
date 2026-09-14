---
kind: review_result
review_id: review-T-P5-151-vertexwise-end-to-end-robust-reset-honglianmozun-20260909T1150Z
task_id: T-P5-151-VERTEXWISE-END-TO-END-ROBUST-RESET
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T11:50:00Z
claim_commit: 80e7ebd6c7d8e4e183b487dca94e5c7f4185f4d3
inspected_commit: c23a72cb79099f36724f327011bf628c20a8186e
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-148-SEMIDEFINITE-CELL-CROSS-RESIDUAL-SCHUR-CAP-honglianmozun-20260909T1059Z.md
    commit: 6daae6877be6f6d19d2263d170c21b6d090ba1e8
  - path: agent_review_inbox/review-T-P5-149-INEXACT-AUGMENTED-RANGE-SOLVE-CAP-liuguanyi-20260909T1110Z.md
    commit: 506928de79dd6f2d24cb40b29655909fd5819032
  - path: agent_review_inbox/review-T-P5-150-SEMIDEFINITE-RESIDUAL-POLYTOPE-CLOSURE-kuangmanmozun-20260909T1130Z.md
    commit: 834eabbae175186f1f9e82ff501f9c55f581d65d
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: allow_parameter_vertex_specific_augmented_residual_caps_and_vertex_specific_cell_multipliers_to_be_carried_to_a_common_scalar_reset_floor_before_robustification; use_shared_Sigma_only_as_an_optional_intermediate; preserve_exact_range_compatibility_at_each_vertex; when_exact_range_solves_and_lossless_vertex_multipliers_are_available_take_the_maximum_of_vertex_floors_as_the_sharp_robust_floor
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic, convex-hull, and Lyapunov/reset algebra only
exit_code: n/a
---

# T-P5-151 — vertexwise end-to-end robust reset

## 0. Narrow seam and non-overlap

T-P5-148 gives an augmented Schur cap for one fixed semidefinite residual map. T-P5-149 allows inexact solves for that fixed map. T-P5-150 then treats a polytope of residual maps but deliberately requires one shared matrix cap `Sigma` if robustification is performed at the augmented-residual stage.

T-P5-150 explicitly notes that parameter-dependent caps may be retained if a downstream theorem supports them. This review closes exactly that downstream seam.

The main point is:

> for a scalar reset/Lyapunov budget on one fixed physical quotient cell, one does not need a shared matrix cap before taking the robust maximum.

Because the original residual expression is affine in the uncertainty parameter, robustification can be postponed until after each uncertainty vertex has been pushed through its own nullspace completion and its own bounded-cell multiplier. The final common object is only one scalar reset floor `E`.

This can be strictly sharper than every route that first forces all vertices through a shared Loewner cap.

No deployed source binding, interval-runtime semantics, provenance/admission audit, coverage claim, Lean/kernel result, or registry mutation is made.

---

## 1. Setup

Let

- `A=A^T >= 0` be the semidefinite uncontrolled-direction metric;
- `m in R^d` be the positive-metric quotient coordinate;
- `G=G^T > 0` and `R>=0` define the common physical cell

  `m^T G m <= R`;

- `xi(m) := (1,m) in R^(d+1)`;
- `P=conv{v_1,...,v_N}` be a nonempty finite uncertainty polytope;
- `Q(theta)` be affine on `P`, with `Q_j:=Q(v_j)`;
- the parameter-independent quotient/base reset quadratic be

  `q_0(m) := C_0 + b_0^T m - m^T H_0 m`.

For the uncontrolled variable `e`, define the full reset envelope

**(1.1)**

`f_theta(e,m)`

`:= q_0(m) + e^T Q(theta) xi(m) - e^T A e`.

For each fixed state `(e,m)`, `f_theta(e,m)` is affine in `theta`.

The robust goal is one scalar `E` such that

**(1.2)**

`f_theta(e,m) <= E`

for every `theta in P`, every `e`, and every `m` with `m^T Gm<=R`.

---

## 2. First theorem: robust scalar floor is vertexwise exactly

### Theorem A — convex-hull scalar reset reduction

For any real `E`, the following are equivalent:

1. `f_theta(e,m)<=E` for every `theta in P`, every `e`, and every physical `m`;
2. `f_{v_j}(e,m)<=E` for every vertex `j`, every `e`, and every physical `m`.

### Proof

`1 => 2` is immediate because every vertex lies in `P`.

For `2 => 1`, write

`theta = sum_j lambda_j v_j`,

with `lambda_j>=0` and `sum_j lambda_j=1`.

Affineness of `Q` gives

`Q(theta)=sum_j lambda_j Q_j`.

The base quadratic and the term `-e^T A e` are independent of `theta`, so

**(2.1)**

`f_theta(e,m)=sum_j lambda_j f_{v_j}(e,m)`.

Each vertex value is at most `E`; therefore their convex combination is at most `E`.

QED.

### Exact supremum consequence

Whenever the suprema are interpreted in the extended real sense,

**(2.2)**

`sup_{theta in P, e, m^TGm<=R} f_theta(e,m)`

`= max_j sup_{e, m^TGm<=R} f_{v_j}(e,m)`.

The inequality `<=` follows from Theorem A applied above every common upper bound; the reverse inequality follows because every vertex is admissible.

Thus the sharp robust scalar floor is the maximum of the sharp vertex floors. A shared matrix cap is not mathematically necessary for scalar reset closure.

---

## 3. Vertex-specific augmented caps are enough

For each vertex `j`, let a symmetric matrix

`Sigma_j = [[alpha_j, g_j^T/2], [g_j/2, S_j]]`

satisfy the fixed-vertex augmented block gate

**(3.1)**

`[[4A, -2Q_j], [-2Q_j^T, 4Sigma_j]] >= 0`.

Equivalently, for all `e,m`,

**(3.2)**

`e^T Q_j xi - e^T A e <= xi^T Sigma_j xi`

`= alpha_j + g_j^T m + m^T S_j m`.

Define the vertex-reduced quotient coefficients

**(3.3)** `C_j := C_0 + alpha_j`,

**(3.4)** `b_j := b_0 + g_j`,

**(3.5)** `H_j := H_0 - S_j`.

Then

**(3.6)**

`f_{v_j}(e,m) <= C_j+b_j^T m-m^T H_j m`.

Crucially, `Sigma_j` is allowed to depend on `j`. No common Loewner upper bound is required.

This already consumes the inexact fixed-vertex caps allowed by T-P5-149.

---

## 4. Each uncertainty vertex may use its own physical-cell multiplier

For each vertex `j`, choose a scalar

`tau_j >= 0`

and define

**(4.1)** `K_j := H_j + tau_j G`.

Assume

**(4.2)** `K_j >= 0`

and provide any exact range solve

**(4.3)** `K_j y_j = b_j`.

Define the vertex floor

**(4.4)**

`E_j := C_j + tau_j R + (1/4) b_j^T y_j`.

Then for every physical `m`,

**(4.5)**

`E_j - (C_j+b_j^Tm-m^T H_jm)`

`= tau_j (R-m^T Gm)`

`  + (m-y_j/2)^T K_j (m-y_j/2)`

`>=0`.

Therefore every vertex admits its own multiplier, its own quotient completion, and its own scalar floor.

There is no reason to force `tau_1=...=tau_N`.

---

## 5. Main theorem: end-to-end vertexwise robust reset

### Theorem B — vertex-specific Schur + vertex-specific multiplier + one common scalar floor

Assume for every vertex `j`:

1. the augmented residual block (3.1) holds with its own `Sigma_j`;
2. `tau_j>=0`;
3. `K_j=H_j+tau_jG>=0`;
4. `K_j y_j=b_j`;
5. one common scalar `E` satisfies `E>=E_j`.

Then for every `theta in P`, every `e`, and every `m` with `m^TGm<=R`,

**(5.1)**

`f_theta(e,m) <= E`.

### Proof

Every vertex satisfies `f_{v_j}<=E_j<=E` by (3.6) and (4.5). Apply Theorem A.

QED.

This theorem is already useful with nonminimal/inexact `Sigma_j` produced by T-P5-149.

---

## 6. Stronger exact-gap theorem with range-factored residuals

The cleanest case is when every vertex is exactly range-compatible with `A`.

Assume for each vertex an exact solve

**(6.1)** `A X_j = Q_j`.

Define the intrinsic fixed-vertex cap

**(6.2)**

`Sigma_j^* := (1/4) X_j^T A X_j`.

This is independent of the chosen representative `X_j` modulo `ker A` and is the fixed-vertex minimal cap from T-P5-148.

For every `e,m`, one has the exact square completion

**(6.3)**

`e^T Q_j xi - e^T A e`

`= xi^T Sigma_j^* xi`

`  - (e-X_j xi/2)^T A(e-X_j xi/2)`.

Partition `Sigma_j^*` as in section 3 and define `C_j,b_j,H_j` accordingly.

Assume also the vertex multiplier data of section 4 and let

`E >= max_j E_j`.

For `theta=sum_j lambda_j v_j`, the following exact decomposition holds:

**(6.4)**

`E-f_theta(e,m)`

`= sum_j lambda_j [`

`    (E-E_j)`

`  + (e-X_j xi/2)^T A(e-X_j xi/2)`

`  + tau_j(R-m^TGm)`

`  + (m-y_j/2)^T K_j(m-y_j/2)`

`  ]`.

Every term is nonnegative on the physical cell.

So the robust proof is a convex combination of vertex-specific Lyapunov/reset gaps. It never constructs a shared matrix `Sigma`.

---

## 7. Sharpness when the fixed-vertex multiplier is lossless

For one strictly feasible ellipsoidal constraint `m^TGm<R` with `G>0` and `R>0`, the classical one-constraint S-lemma makes the scalar multiplier representation lossless for a quadratic upper-bound problem.

Therefore, if each vertex uses a sharp/lossless multiplier and the exact range solve (6.1), then each `E_j` equals the actual vertex supremum and Theorem A gives

**(7.1)**

`E_* = max_j E_j`

as the sharp robust scalar reset floor.

The trusted theorem above does not need the S-lemma: (6.4) is a direct sufficient certificate. The S-lemma is only the interpretation that the vertex certificates can, in the standard strict ellipsoid setting, be chosen without loss.

---

## 8. Strict separation example: shared `Sigma` can overcharge irreducibly

This example shows that T-P5-151 is not merely a reformulation of T-P5-150.

Take

`A=[1]`,

`G=[1]`,

`0<R<=1`,

`q_0(m)=0`,

`xi=(1,m)`.

Let the uncertainty segment have two vertices

**(8.1)** `Q_1=[2,0]`,

**(8.2)** `Q_2=[0,2]`.

For vertex 1,

`f_1(e,m)=2e-e^2`.

Its exact maximum over `e` is

**(8.3)** `1`.

For vertex 2,

`f_2(e,m)=2em-e^2`.

Its exact maximum over `e` is

**(8.4)** `m^2 <= R`.

Hence Theorem A gives the exact robust floor

**(8.5)**

`E_* = max(1,R)=1`.

### Vertexwise certificate

Take exact solves

`X_1=[2,0]`, `X_2=[0,2]`.

Then

**(8.6)** `Sigma_1^*=diag(1,0)`,

**(8.7)** `Sigma_2^*=diag(0,1)`.

Vertex 1 uses `tau_1=0` and gives `E_1=1`.

Vertex 2 has reduced quadratic `m^2`; using `tau_2=1` gives `K_2=0` and `E_2=R`.

Thus T-P5-151 certifies `E=1` exactly.

### Any shared matrix cap costs at least `1+R`

Suppose instead one insists on one shared symmetric

`Sigma=[[a,c],[c,d]]`

that dominates both exact fixed-vertex caps:

`Sigma-Sigma_1^* >=0`,

`Sigma-Sigma_2^* >=0`.

The first PSD condition forces

**(8.8)** `a>=1`.

The second forces

**(8.9)** `d>=1`.

On the two physical boundary points `m=+sqrt(R)` and `m=-sqrt(R)`, the larger shared-cap value is

`max_{sign=+/-} [1, sign sqrt(R)] Sigma [1; sign sqrt(R)]`

`= a+dR+2|c|sqrt(R)`

`>= 1+R`.

Therefore every shared-cap-first route pays at least

**(8.10)** `E_shared >= 1+R`,

while the exact robust floor is `1`.

For the rational choice

**(8.11)** `R=1/4`,

T-P5-151 gives exact floor `1`, whereas every shared matrix cap incurs at least

**(8.12)** `5/4`.

This is a strict 25% overcharge caused solely by demanding one Loewner cap before using the bounded physical state geometry.

The geometric reason is clear: vertex 1 spends only the constant component of `xi`, while vertex 2 spends only the `m` component. A shared matrix must reserve both simultaneously even though the final robust scalar maximum only needs the worse vertex at each uncertainty extreme.

---

## 9. Relation to T-P5-150

T-P5-150 remains fully correct and useful. Its shared `Sigma` theorem is the right interface when:

- a downstream consumer genuinely requires one uncertainty-independent quadratic matrix cap;
- one wants to collapse uncertainty before seeing the physical quotient cell;
- or a producer already exposes a convenient common PSD cap.

T-P5-151 adds a sharper option when the downstream goal is only a scalar reset/Lyapunov budget on a fixed cell:

1. keep each uncertainty vertex separate;
2. perform fixed-vertex semidefinite elimination;
3. perform the bounded-cell multiplier separately at each vertex;
4. take only the maximum scalar floor at the end.

The shared matrix cap becomes optional rather than mandatory.

---

## 10. Finiteness and fail-closed boundaries

### 10.1 Kernel leakage is still fatal

T-P5-151 does not bypass the range obstruction.

If for any vertex `j`

`range(Q_j) not subseteq range(A)`,

there exist `k in ker A` and `xi` with `k^TQ_jxi !=0`. Taking `e=tk` with the favorable sign sends the vertex reset to `+infinity`.

Therefore the robust scalar floor is also infinite.

So vertexwise downstream robustification is sharper than a shared cap only after every active vertex is finitely controllable.

### 10.2 The physical cell must be common across uncertainty

The convex-combination identity (2.1) is evaluated at the same `(e,m)` and the same admissible cell.

If `G`, `R`, or the state domain depends on `theta`, the vertex argument does not by itself prove robust closure over a parameter-dependent feasible set.

### 10.3 The original reset map must be affine in the uncertainty description

The theorem applies to an exact convex-hull/affine residual packet.

A nonlinear parameterization, an interval cloud without convex-hull proof, or sampled runtime points cannot be substituted silently.

### 10.4 Vertex-specific caps cannot be averaged first unless the parameter weights are retained

The proof uses each vertex cap only inside its own vertex inequality and takes a scalar common floor afterward.

It does not claim that `sum lambda_j Sigma_j` is a parameter-independent shared cap, nor that one of the `Sigma_j` dominates the others.

### 10.5 A vertex-specific multiplier is not a physical controller parameter

`tau_j` is a proof multiplier for one uncertainty vertex. Unless separately sourced, it must not be interpreted as a deployed controller or runtime scheduling quantity.

---

## 11. Checker-friendly theorem surface

A future exact checker does not need matrix inverses or square roots.

For every vertex `j`, it may receive either:

### Route A — direct vertex cap

- `Q_j`;
- symmetric `Sigma_j`;
- PSD block

  `[[4A,-2Q_j],[-2Q_j^T,4Sigma_j]] >=0`;

- partition `(alpha_j,g_j,S_j)`;
- `tau_j>=0`;
- `K_j=H_j+tau_jG >=0`;
- exact solve `K_j y_j=b_j`;
- scalar comparison `E>=C_j+tau_jR+b_j^Ty_j/4`.

### Route B — exact range-factored vertex

- exact solve `A X_j=Q_j`;
- form `4Sigma_j=X_j^TAX_j` exactly;
- then the same quotient multiplier packet.

No global `Sigma`, no common `tau`, no inverse, no generalized eigenvalue, and no square root is required.

If fractions are undesirable, multiply the final scalar gate by 4:

**(11.1)**

`4E >= 4C_j + 4tau_j R + b_j^T y_j`.

---

## 12. Candidate theorem statements

### Leaf A — affine vertex scalar reduction

Assumptions:

- `lambda_j>=0`, `sum lambda_j=1`;
- `Q=sum lambda_j Q_j`;
- for all `j`, `f_j(e,m)<=E`.

Conclusion:

`f_Q(e,m)<=E`.

Proof: exact convex combination.

### Leaf B — one vertex reset completion

Assumptions:

- fixed block cap (3.1);
- `m^TGm<=R`;
- `tau>=0`;
- `K=H+tau G>=0`;
- `Ky=b`;
- `4E>=4C+4tau R+b^Ty`.

Conclusion:

`f(e,m)<=E`.

Proof: augmented residual PSD gap plus cell multiplier square completion.

### Leaf C — exact range-factored vertex gap

Assumptions:

- `AX=Q`;
- quotient multiplier assumptions as above.

Conclusion: the exact two-square-plus-cell-slack identity obtained by combining (6.3) and (4.5).

### Leaf D — robust vertex family

Assumptions:

- `theta` is a convex combination of finite vertices;
- every vertex satisfies Leaf B with the same scalar `E` but arbitrary vertex-specific `Sigma_j,tau_j,y_j`.

Conclusion:

`f_theta(e,m)<=E`.

---

## 13. Structural fingerprint

This child suggests a reusable Lyapunov/reset fingerprint:

**affine uncertainty + fixed state cell + scalar final budget => delay robustification until after vertexwise energy completion.**

Premature matrix robustification can force incompatible directions to be paid simultaneously. If the final consumer only needs a scalar supremum, the mathematically natural order is

1. uncertainty vertex;
2. signed/nullspace energy completion;
3. bounded-cell Lyapunov multiplier;
4. scalar vertex floor;
5. maximum over vertices.

This is the same general principle seen elsewhere in the repository: preserve signed/directional structure until the last consumer that actually needs a scalar envelope.

---

## 14. Open boundaries after this child

Still open:

- actual same-key source/runtime uncertainty polytope;
- proof that the deployed residual family is affine and lies in the stated convex hull;
- exact source identities tying all `Q_j` to the same semidefinite `A`;
- actual common quotient cell `G,R` and same-cell coverage;
- actual reset/Lyapunov base coefficients `C_0,b_0,H_0`;
- construction of source-derived vertex caps or exact range solves;
- exact/rational PSD and range receipts for the chosen vertex multipliers;
- Float64/directed-rounding semantics;
- time-dependent/reference-knot composition beyond one fixed reset cell;
- Lean/kernel formalization and independent validation by 封不觉;
- provenance/admission/registry/P5 parent closure.

This review only proves the mathematics needed to consume a future robust source packet more sharply. It does not assert that the current deployed source already provides such a packet.

---

## 15. Requested handoff

The shortest useful producer packet for this route is

`(cellKey, resetKey, A, G, R, C0, b0, H0, {Q_j})`

plus, for each uncertainty vertex `j`, either

- a direct augmented PSD cap `Sigma_j`, or
- an exact range solve `A X_j=Q_j`,

and then a vertex-specific quotient packet

`(tau_j, K_j, y_j, E_j)`

with

`K_j=H_j+tau_jG>=0`,

`K_j y_j=b_j`.

The final robust consumer needs only

**`E >= E_j` for all vertices.**

If this vertexwise scalar floor is materially smaller than every available shared-`Sigma` route, it should be preferred for the reset/Lyapunov consumer. A shared matrix cap should be retained only when a later theorem truly requires a common matrix object.