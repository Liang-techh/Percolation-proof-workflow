---
kind: review_result
review_id: review-T-P5-210-common-zero-second-order-critical-cone-threshold-kuangmanmozun-20260910T0334Z
task_id: T-P5-210-COMMON-ZERO-SECOND-ORDER-CRITICAL-CONE-THRESHOLD
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T03:34:00Z
claim_commit: 3474a1b3c2c60adcf1c2bae64b4651f0855ff4f3
inspected_commit: d1c18ea1361c2716894d8c85893abfa2c2aaa35a
upstream_commits:
  - 84f4d490036164a8a7654c2781f7dea8864cb695  # T-P5-208 ray-threshold contact/support bridge
  - 9b453f8e99d0736e55393d6458036b8a3658a17c  # T-P5-209 weak-reference residual-contact threshold
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_bicritical_cone; add_second_order_exact_endpoint_certificate; add_common_zero_local_ray_ceiling; route_bicritical_mixed_block_to_T178_T180; retain_global_copositivity_gate
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact quadratic expansion on orthant tangent cone; copositive zero-contact residual algebra; rational 2x2 counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-210 — common-zero second-order critical-cone threshold

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-209 closes the first-order weak-reference branch: if a zero-debit-energy contact `z` has an inactive row with endpoint residual zero but positive debit residual, every larger ray parameter immediately violates copositivity by a one-sided coordinate perturbation. It explicitly leaves the case with no usable first-order debit residual to a second-order critical/tangent reduction.

This child supplies that reduction and, slightly more generally, does not require `Qz=0` componentwise. The right object is a **bi-critical orthant cone**: tangent directions must annihilate both the endpoint contact residual and the debit residual. On that cone the first-order terms of both quadratic forms vanish, so both forms become ordinary nonnegative quadratic forms. A positive-debit zero of the endpoint quadratic on this cone is then an exact sharp-threshold certificate.

The resulting dispatcher is genuinely two-level:

1. T-P5-209: first-order inactive residual saturation;
2. T-P5-210: second-order bi-critical quadratic saturation.

The second level is not a heuristic KKT test. It gives an explicit negative orthant witness for every parameter strictly beyond the certified endpoint.

No actual P5 source matrices/profile, selector/cell/tube binding, global coverage, Float64 enclosure, Lean/kernel proof, independent 封不觉 verification, admission, registry promotion, or parent closure is claimed.

---

## 1. Setup

Let `C,Q` be real symmetric `n x n` matrices and define the nonnegative ray pencil

`M(t) := C - t Q`, `t>=0`.

Assume `Q` is copositive. Fix a candidate `t_*>=0` for which

`H := M(t_*)`

is copositive.

Let `z>=0`, `z!=0`, satisfy the two zero-energy conditions

`z^T H z = 0`,

`z^T Q z = 0`.

Because `H` and `Q` are copositive zero contacts, the standard one-sided contact lemma gives

`a := H z >= 0`,

`b := Q z >= 0`,

and complementarity gives

`z_i a_i = z_i b_i = 0` for every `i`.

In particular both residual vectors vanish on the positive support

`S := supp(z)`.

The ordinary tangent cone of the nonnegative orthant at `z` is

`T_+(z) := {v : v_i is arbitrary for i in S, and v_j>=0 for j notin S}`.

Define the **bi-critical cone**

`K(H,Q;z) := {v in T_+(z) : a^T v = 0 and b^T v = 0}`.

Since `a,b>=0`, and inactive tangent components are nonnegative, this can equivalently be written coordinatewise as

- `v_S` arbitrary;
- `v_j=0` whenever `j notin S` and `a_j>0` or `b_j>0`;
- `v_j>=0` on the remaining inactive rows where `a_j=b_j=0`.

Thus there is no hidden nonlinear tangent geometry: `K(H,Q;z)` is a rational polyhedral mixed signed/orthant cone whenever `H,Q,z` are rational.

---

## 2. T210-A — exact orthant critical-cone lemma

### Lemma

For every `v in T_+(z)`, there exists `eps_0>0` such that

`z + eps v >=0`

for every `0<=eps<=eps_0`.

For `v in K(H,Q;z)`, the quadratic expansions are exactly

`(z+eps v)^T H (z+eps v) = eps^2 v^T H v`,

`(z+eps v)^T Q (z+eps v) = eps^2 v^T Q v`.

Consequently

**`v^T H v >=0` and `v^T Q v >=0` for every `v in K(H,Q;z)`.**

### Proof

On coordinates where `z_i=0`, tangent feasibility gives `v_i>=0`. On coordinates where `z_i>0`, choose `eps_0` small enough that every negative `v_i` remains dominated by `z_i`.

Now expand:

`(z+eps v)^T H(z+eps v)`

`= z^THz + 2 eps (Hz)^T v + eps^2 v^T H v`

`= eps^2 v^T H v`,

because `z^THz=0` and `a^Tv=0`. The left side is nonnegative by copositivity of `H`, hence `v^THv>=0`.

The proof for `Q` is identical, using `z^TQz=0` and `b^Tv=0`.

QED.

### Why both critical equalities are needed

A tangent direction with `a^Tv>0` has a positive first-order endpoint-energy buffer. A direction with `b^Tv>0` changes the debit at first order. Such directions do not belong to the pure second-order problem. Dropping either equality mixes the T-P5-209 first-order mechanism back into the quadratic term and can produce false sharpness certificates; Regression 2 below gives an explicit example for the endpoint-residual equality.

---

## 3. T210-B — exact second-order sharp-threshold certificate

### Theorem

Assume:

1. `H=M(t_*)` is copositive;
2. `Q` is copositive;
3. `z>=0`, `z!=0`;
4. `z^T H z=0`;
5. `z^T Q z=0`;
6. there exists `v in K(H,Q;z)` such that
   - `v^T H v=0`,
   - `v^T Q v>0`.

Then **`t_*` is the exact endpoint of the safe ray**

`T := {t>=0 : M(t) is copositive}`.

Equivalently,

- `M(s)` is copositive for every `0<=s<=t_*`;
- `M(s)` is not copositive for every `s>t_*`.

### Safe side

For `0<=s<=t_*`,

`M(s)=H+(t_*-s)Q`.

Both summands are copositive, so `M(s)` is copositive.

### Unsafe side

Fix `s>t_*` and put `delta:=s-t_*>0`. Then

`M(s)=H-delta Q`.

Because `z^THz=z^TQz=0`,

`z^T M(s) z=0`.

Because `v` is bi-critical,

`z^T M(s)v = a^Tv - delta b^Tv = 0`.

Finally,

`v^T M(s)v`

`= v^T H v - delta v^T Qv`

`= -delta v^TQv <0`.

Choose any sufficiently small `eps>0` with `x_eps:=z+eps v>=0`. Then

`x_eps^T M(s)x_eps`

`= eps^2 v^T M(s)v <0`.

Hence `M(s)` is not copositive.

QED.

### Structural meaning

T-P5-209 proves sharpness when the first derivative in an inactive orthant direction flips sign. T210-B proves sharpness when **all relevant first derivatives vanish and the second derivative flips sign**. The witness is still finite-dimensional and exact: it is the nearby orthant state `z+eps v`.

---

## 4. T210-C — common-zero branch and a local second-order ray ceiling

The branch highlighted explicitly by T-P5-209 is the stronger condition

`Qz=0`.

Suppose now `C,Q` are both copositive and

`z^TCz=0`,

`Qz=0`.

Let

`a:=Cz>=0`.

Since `Qz=0`, for every ray parameter `t`,

`M(t)z=Cz=a`.

Therefore the first-order critical cone is independent of `t`:

`K_z := {v in T_+(z) : a^Tv=0}`.

For every `v in K_z`, both

`c(v):=v^TCv >=0`,

`q(v):=v^TQv >=0`.

Every globally safe parameter `t` must satisfy

`c(v)-t q(v)>=0`

for every `v in K_z`.

Thus every `v in K_z` with `q(v)>0` gives the exact local upper bound

**`t <= c(v)/q(v)`.**

Define

`tau_2(z) := inf { c(v)/q(v) : v in K_z, q(v)>0 }`,

with `tau_2(z)=+infinity` if there is no such direction.

Then

**`T subset [0,tau_2(z)]`.**

If a safe candidate `t_*` admits a direction `v in K_z` with

`c(v)=t_* q(v)` and `q(v)>0`,

then T210-B applies and `t_*` is the exact global ray endpoint.

This is the second-order analogue of T-P5-209's finite family of first-order residual ratios. Unlike the rowwise first-order ceiling, `tau_2` is generally a generalized quadratic quotient on a mixed cone and need not be rational or attained without additional nondegeneracy. No such attainment is silently claimed here.

---

## 5. T210-D — block form and reuse of the existing mixed-critical checker

Let `S=supp(z)`. In the common-zero branch `Qz=0`, define the zero endpoint-residual inactive set

`I := {j notin S : (Cz)_j=0}`

and the blocked set

`J := {j notin S : (Cz)_j>0}`.

Then every `v in K_z` has the form

`v=(u,y,0_J)`,

with

`u in R^S`,

`y in R_+^I`.

For any symmetric matrix `R`, the restricted quadratic form is

`v^T Rv`

`= u^T R_SS u + 2 y^T R_IS u + y^T R_II y`.

Therefore the second-order endpoint object is **exactly the signed-active / one-sided-inactive mixed quadratic block already studied in T-P5-178 and simplified in the corank-one case by T-P5-180**.

No new cone solver is required. The intended routing is:

1. build `S,I,J` from the exact contact residuals;
2. freeze `J` to zero;
3. send `(R_SS,R_IS,R_II)` for `R=H` and `R=Q` to the existing mixed-critical representation;
4. search for a common critical direction with `h(v)=0<q(v)`;
5. once global copositivity of `H` is independently certified, use T210-B for exact ray sharpness.

This routing is important because a signed active direction must not be encoded as an ordinary orthant coordinate without a valid signed split / range elimination. The earlier mixed-block theorems already contain those gates.

---

## 6. T210-E — division-free rational endpoint packet

Suppose the candidate is rational

`t_*=p/r`, with `p>=0`, `r>0`,

and define the scaled endpoint matrix

`H_r := rC-pQ = r H`.

A source/checker packet may verify:

1. `H_r` is copositive;
2. `Q` is copositive;
3. `z>=0`, `z!=0`;
4. `z^T H_r z=0`;
5. `z^T Q z=0`;
6. `v in T_+(z)`;
7. `(H_r z)^T v=0`;
8. `(Qz)^T v=0`;
9. `v^T H_r v=0`;
10. `v^T Qv>0`.

Then `p/r` is the exact ray endpoint.

All equalities and inequalities are polynomial/rational except the separate copositivity premises. No division by `r`, no generalized eigenvalue, no inverse, no square root, and no normalization of `v` is required.

If `z,v,C,Q,p,r` are rational, the entire second-order contact witness is rational. If the true critical direction is algebraic, this child does **not** claim that a rational exact witness must exist; that case should retain the existing root-free/algebraic isolation machinery rather than round the direction numerically.

---

## 7. Regression 1 — genuine second-order endpoint with no first-order debit residual

Take

`C = [[0,0],[0,1]]`,

`Q = [[0,0],[0,1]]`.

Then

`M(t)=diag(0,1-t)`.

The exact safe interval is plainly

`T=[0,1]`.

At `t_*=1`,

`H=M(1)=0`.

Choose

`z=e_1`,

`v=e_2`.

Then

`Hz=0`,

`Qz=0`,

`z^THz=z^TQz=0`,

`v^THv=0`,

`v^TQv=1>0`.

There is no first-order T-P5-209 debit residual because `Qz=0` componentwise. Nevertheless T210-B gives exact sharpness. For every `s>1`, the nearby witness `z+eps e_2` has energy

`-(s-1)eps^2<0`.

This is the minimal clean regression proving that the second-order branch is not cosmetic.

---

## 8. Regression 2 — endpoint-residual criticality cannot be dropped

Let

`H = [[0,1],[1,1]]`,

`Q = [[0,0],[0,1]]`,

and view `H` as the candidate matrix at `t_*=0`, so

`M(s)=H-sQ = [[0,1],[1,1-s]]`.

Both `H` and `Q` are copositive. Take

`z=e_1`.

Then

`z^THz=0`,

`Qz=0`,

but

`Hz=e_2`.

Now choose the tangent direction

`v=(-1/2,1)`.

For small positive `eps`, `z+eps v>=0`. Moreover

`v^T H v=0`,

`v^T Qv=1>0`.

If one omitted the critical equality `(Hz)^Tv=0`, these two quadratic equalities would falsely appear to certify that `t_*=0` is sharp.

But in fact

`(Hz)^Tv=1>0`,

and

`M(s)` remains copositive for every `0<=s<=1` because its orthant quadratic form is

`2xy+(1-s)y^2>=0`.

Thus the candidate `0` is not the endpoint. The positive first-order endpoint residual buffers the negative second-order perturbation.

**Conclusion:** `v^THv=0<v^TQv` is not enough; the tangent direction must also lie in the endpoint critical cone.

---

## 9. Regression 3 — zero debit energy cannot certify sharpness

Take

`H = [[0,0],[0,1]]`,

`Q = [[0,0],[0,1]]`,

again at candidate `t_*=0`.

Let

`z=e_1`, `v=e_1`.

Then

`Hz=Qz=0`,

`v` is bi-critical,

`v^THv=0`,

but also

`v^TQv=0`.

The pencil

`M(s)=diag(0,1-s)`

remains copositive for every `0<=s<=1`.

Therefore a second-order endpoint contact with zero debit energy does not move under the ray and cannot prove sharpness. The strict gate `v^TQv>0` is essential.

---

## 10. Formalizable theorem statements

### T210-F1 — critical quadratic nonnegativity

`critical_quadratic_nonneg_of_copositive_zero_contact`

Given symmetric copositive `R`, `z>=0`, `z^TRz=0`, and a tangent direction `v in T_+(z)` with `(Rz)^Tv=0`, prove

`v^TRv>=0`.

The proof is the exact one-parameter expansion of `z+eps v`.

### T210-F2 — second-order exact ray endpoint

`second_order_critical_contact_exact_ray_endpoint`

Given symmetric `H,Q`, `t_*>=0`, with `H` and `Q` copositive, assume

- `z>=0`, `z!=0`;
- `z^THz=0`;
- `z^TQz=0`;
- `v in T_+(z)`;
- `(Hz)^Tv=0`;
- `(Qz)^Tv=0`;
- `v^THv=0`;
- `v^TQv>0`.

For `M(s):=H+(t_*-s)Q`, prove

- `Copositive(M(s))` for `0<=s<=t_*`;
- `not Copositive(M(s))` for every `s>t_*`.

The unsafe proof may explicitly construct a sufficiently small `eps>0` such that `z+eps v>=0` and then show its quadratic energy is negative.

### T210-F3 — common-zero critical ceiling

Given copositive `C,Q`, `z>=0`, `z^TCz=0`, `Qz=0`, and

`K_z=T_+(z) intersect (Cz)^perp`,

prove that every safe `t` satisfies

`v^TCv >= t v^TQv`

for every `v in K_z`.

This theorem should avoid defining an infimum if the formal library does not need it; the pointwise ratio-free inequality is the stronger checker-facing form.

---

## 11. Fail-closed routing

A checker using this child should distinguish:

- **FIRST_ORDER_SHARP:** T-P5-209 finds `(Hz)_j=0<(Qz)_j`;
- **SECOND_ORDER_SHARP:** no chosen first-order witness is used, but T210-B finds a bi-critical `v` with `v^THv=0<v^TQv`;
- **SECOND_ORDER_GATE_NOT_APPLICABLE:** no such exact `v` has been certified;
- **GLOBAL_SAFE_SIDE_OPEN:** the local contact data are present but `H` has not been globally certified copositive.

The latter two are not mathematical FAIL states. In particular, failure to find a bi-critical zero direction does not prove that the ray can be extended: a different contact state can become active, or the relevant critical quotient can have an algebraic/non-attained limiting mechanism.

Likewise, the mixed-critical reduction must not promote local nonnegativity on `K(H,Q;z)` into global copositivity of `H`.

---

## 12. What this closes and what remains open

This child closes the specific mathematical seam left by T-P5-209 when first-order residual contact does not provide the ray endpoint:

**zero-energy endpoint contact -> bi-critical orthant cone -> second-order positive-debit contact -> exact ray sharpness.**

It also supplies an exact local ceiling in the componentwise common-zero branch `Qz=0` and shows that the required cone is precisely the previously developed signed-active/one-sided-inactive mixed block, so the result composes with T-P5-178/T-P5-180 rather than creating a new solver architecture.

Still open, intentionally:

- actual P5 `C,Q,z,v` source binding and same-key identity;
- discovery/attainment of the generalized critical quotient when no exact rational `v` is already available;
- global copositivity of the endpoint matrix;
- support/cell/tube coverage;
- Float64/interval semantics;
- Lean implementation and independent 封不觉 verification;
- admission/registry/parent propagation.

The smallest next mathematics child, if the actual pipeline reaches this branch, is a **corank-one critical-block scalarization**: combine T-P5-180's anchor Schur reduction with the pair `(H,Q)` to turn `v^THv=0<v^TQv` into bordered-determinant / Schur remainder signs on the zero-residual inactive block. That can be attacked without touching source provenance.