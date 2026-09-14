---
kind: review_result
review_id: review-T-P5-156-simplex-refinement-weighted-slack-covariance-liuguanyi-20260909T1302Z
task_id: T-P5-156-SIMPLEX-REFINEMENT-WEIGHTED-SLACK-COVARIANCE
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T13:02:00Z
claim_commit: 3845f17eadca051058530dbb7175c70e679b7b23
inspected_commit: 38bda676af441d55b110d303994a67b20b67ee5c
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-152-PARAMETER-DEPENDENT-CELL-SLACK-COUPLING-liuguanyi-20260909T1201Z.md
    commit: 49dd8628383fae302ddba40c7268e06046f5ca9c
  - path: agent_review_inbox/review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z.md
    commit: c9b94c1f931c76c20a0f22e428425a4d659b57bb
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: transport_signed_cell_slack_and_already_weighted_multiplier_slack_as_typed_certificate_objects_under_simplex_refinement; use_column_stochastic_pushforward_or_M_to_PtMP_congruence; do_not_reconstruct_weighted_slack_by_separately_interpolating_tau_and_cell_without_a_covariance_defect_certificate
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional ordered-field, affine-map, and quadratic-form algebra only
exit_code: n/a
---

# T-P5-156 — simplex-refinement covariance of signed weighted slack

## 0. Narrow seam and non-overlap

T-P5-152 identified the actual robust object for parameter-dependent cells as the pair

`c_lambda(m) = sum_i lambda_i c_i(m)`,

`h_lambda(m) = sum_i lambda_i tau_i c_i(m)`,

and showed that robust closure requires the implication

`c_lambda(m) >= 0  ==>  h_lambda(m) >= 0`

(or the corresponding additive-floor version).

T-P5-153 and T-P5-154 then analyze this condition on one fixed simplex representation, with T-P5-154 homogenizing the full-simplex additive-floor question into copositivity of an explicit matrix.

A source-to-math seam remains: actual uncertainty packets are often triangulated, refined, or represented by a second simplex whose vertices are themselves convex combinations of an older simplex. The certificate must therefore say which mathematical object is transported through the parameter map.

This child proves that:

1. `c` and the **already-weighted signed slack** `h=tau*c` push forward exactly through any column-stochastic refinement map;
2. the robust implication and T-P5-154 quadratic certificate transport by exact algebra, with no coordinate/conditioning tax;
3. interpolating `tau` and `c` separately and multiplying afterward is generally a different object, with an exact pairwise covariance defect;
4. that defect can have either sign and can create a false robust certificate even when the interpolated physical cell is feasible;
5. for homothetic cells there is an exact root-free two-endpoint gate deciding when the separate-product shortcut is nevertheless safe on the whole refined cell.

This does not enter T-P5-155's claimed three-vertex exact copositive-floor lane. No source admission, provenance/receipt audit, runtime/Float64 claim, coverage promotion, Lean/kernel validation, or registry mutation is performed.

---

## 1. Typed refinement map

Let the coarse uncertainty simplex have vertices `i=1,...,n`. Let the refined representation have vertices `alpha=1,...,N`.

For each refined vertex choose coarse barycentric coordinates

`p^alpha_i >= 0`,

`sum_i p^alpha_i = 1`.

Collect them into a matrix

`P in R^(n x N)`,

`P_{i alpha}=p^alpha_i`.

Thus `P` is nonnegative and column-stochastic:

**(1.1)** `P_{i alpha} >= 0`,

**(1.2)** `sum_i P_{i alpha}=1` for every `alpha`.

For a refined simplex weight `mu in Delta_N`, define the induced coarse weight

**(1.3)** `lambda := P mu`.

Then automatically

`lambda_i >= 0`,

`sum_i lambda_i = 1`.

So `P` maps the refined simplex into the coarse simplex.

The point of this theorem is not that the parameter itself has changed. `P` is only a change/refinement of its convex representation. The same `P` must be used by every source field claimed to belong to the same uncertainty point.

---

## 2. Exact pushforward theorem for signed certificate objects

Fix a state/test point `m`. For each coarse vertex let

`c_i = c_i(m)`

be the signed physical-cell slack, and let

`h_i = tau_i c_i`

be the already-weighted signed multiplier slack coming from the proved vertex gap.

Define the refined-vertex certificate objects by linear pushforward:

**(2.1)** `c_tilde_alpha := sum_i P_{i alpha} c_i`,

**(2.2)** `h_tilde_alpha := sum_i P_{i alpha} h_i`.

For refined weights `mu`, define

`c_tilde_mu := sum_alpha mu_alpha c_tilde_alpha`,

`h_tilde_mu := sum_alpha mu_alpha h_tilde_alpha`.

### Theorem A — exact refinement covariance

With `lambda=P mu`,

**(2.3)** `c_tilde_mu = c_lambda`,

**(2.4)** `h_tilde_mu = h_lambda`.

### Proof

By finite-sum associativity,

`c_tilde_mu`

`= sum_alpha mu_alpha sum_i P_{i alpha} c_i`

`= sum_i (sum_alpha P_{i alpha} mu_alpha) c_i`

`= sum_i lambda_i c_i`

`= c_lambda`.

The proof for `h` is identical.

No inverse of `P`, no simplex-coordinate solve, and no norm estimate appears.

### Corollary A1 — robust implication transports exactly

Suppose on the coarse simplex one has, for every `lambda` in the relevant domain,

`c_lambda(m)>=0  ==>  h_lambda(m)+D >=0`,

for a uniform additive floor `D>=0`.

Then for every refined `mu`,

**(2.5)** `c_tilde_mu(m)>=0  ==>  h_tilde_mu(m)+D >=0`.

The same additive floor `D` is used. Refinement itself creates no mathematical tax.

### Domain qualification

If `P Delta_N` is only a proper subset of the coarse simplex, this theorem transfers the certificate only to that subset. A refined-domain theorem cannot be promoted back to the entire coarse simplex without a coverage/surjectivity witness.

If

**(2.6)** `P Delta_N = Delta_n`,

for example because a refinement retains every original coarse vertex, then the two robust domains are the same and the sharp uniform floor is unchanged.

---

## 3. Composition law: refinement chains do not accumulate error

Suppose a second refinement uses another nonnegative column-stochastic matrix `Q` and refined-refined weights `nu`, so

`mu=Q nu`.

Then

`lambda=P Q nu`.

Because a product of nonnegative column-stochastic matrices is again nonnegative and column-stochastic, the two-stage pushforward equals the one-stage pushforward through `P Q`.

For either typed object `z=c` or `z=h`,

**(3.1)** `Push_Q(Push_P(z)) = Push_(P Q)(z)`.

Hence repeated triangulation/refinement does not create an approximation budget. Any budget appearing solely from changing barycentric representation is an adapter artifact, not a mathematical necessity.

---

## 4. Why `h` is not the same type as `tau` and `c` separately

A tempting but generally invalid adapter is:

1. interpolate the multiplier,

   `tau_tilde_alpha := sum_i p_i tau_i`,

2. interpolate the cell slack,

   `c_tilde_alpha := sum_i p_i c_i`,

3. reconstruct

   `h_sep_alpha := tau_tilde_alpha c_tilde_alpha`.

Here `p_i=P_{i alpha}` for one fixed refined vertex.

The correctly pushed certificate is instead

`h_push_alpha := sum_i p_i tau_i c_i`.

These are not equal in general.

### Theorem B — exact pairwise covariance defect

Define

**(4.1)**

`C_p(c,tau)`

`:= sum_{i<j} p_i p_j (tau_i-tau_j)(c_i-c_j)`.

Then

**(4.2)**

`h_push_alpha - h_sep_alpha = C_p(c,tau)`.

### Proof

Expanding the product gives

`h_push-h_sep`

`= sum_i p_i tau_i c_i`

`  - sum_{i,j} p_i p_j tau_i c_j`.

Symmetrizing the double sum over unordered pairs yields exactly

`sum_{i<j} p_i p_j (tau_i-tau_j)(c_i-c_j)`.

This is the usual finite weighted covariance identity, but here it is a signed proof-certificate defect, not a statistical approximation.

### Consequences

- If all `tau_i` are equal on the support of `p`, then `C_p=0`.
- If all `c_i` are equal on the support of `p` (the common-cell case), then `C_p=0`.
- More generally, separate reconstruction is exact iff `C_p=0`.
- If `C_p>=0`, then

  `h_push >= h_sep`,

  so proving `h_sep>=0` is a sound sufficient shortcut for proving `h_push>=0`.
- If `C_p<0`, then `h_sep` can be positive while the actual pushed proof slack is negative. The shortcut is then unsound.

The sign must therefore be retained until the full covariance contraction is formed. Bounding every pair by absolute value before summing discards cancellations and creates an avoidable tax.

---

## 5. Exact false-certificate regression

Use two coarse vertices and one interior refined vertex with

`p_1=p_2=1/2`,

`tau_1=2`, `tau_2=0`.

Take a homothetic scalar cell coordinate `q=Q(m)` and choose

`c_1(q)=1-2q`,

`c_2(q)=4-q`.

At the exact rational point

`q=1`,

one has

`c_1=-1`,

`c_2=3`.

Therefore the refined physical cell slack is

**(5.1)** `c_tilde=(c_1+c_2)/2=1 >=0`.

The separately interpolated multiplier is

`tau_tilde=(2+0)/2=1`,

so the invalid reconstructed weighted slack is

**(5.2)** `h_sep=tau_tilde c_tilde=1 >=0`.

A consumer using only `(tau_tilde,c_tilde)` would accept the point.

But the actual pushed vertex proof slack is

**(5.3)**

`h_push=(1/2)*2*(-1)+(1/2)*0*3=-1 <0`.

The covariance defect is exactly

`C_p=(1/2)(1/2)(2-0)(-1-3)=-2`,

and indeed

`h_push=h_sep+C_p=1-2=-1`.

Thus:

> a feasible interpolated physical cell plus a nonnegative interpolated multiplier does not imply that the convexified vertex multiplier proof remains valid.

This is a hard mathematical obstruction, not a source-format preference.

---

## 6. Homothetic whole-cell gate for the separate-product shortcut

The preceding defect depends on the state because the cell slacks do. For the homothetic family of T-P5-153, however, the dependence is only affine in the common radial quadratic coordinate.

Assume

**(6.1)** `c_i(q)=r_i-g_i q`,

with

`q=Q(m)>=0`,

`g_i>0`.

For one refined vertex with barycentric column `p`, define

`r_bar := sum_i p_i r_i`,

`g_bar := sum_i p_i g_i`.

Then

`c_tilde(q)=r_bar-g_bar q`.

Also define the two signed pairwise contractions

**(6.2)**

`A_p := sum_{i<j} p_i p_j (tau_i-tau_j)(r_i-r_j)`,

**(6.3)**

`B_p := sum_{i<j} p_i p_j (tau_i-tau_j)(g_i-g_j)`.

By Theorem B,

### Theorem C — affine covariance defect

**(6.4)**

`C_p(q)=h_push(q)-h_sep(q)=A_p-B_p q`.

Suppose `r_bar>=0` and `g_bar>0`, so the entire refined cell corresponds to

`0 <= q <= r_bar/g_bar`.

Then, provided this radial interval is attained by the state domain, the condition

`C_p(q)>=0`

for every point of the refined cell is equivalent to the two root-free endpoint gates

**(6.5)** `A_p >= 0`,

**(6.6)** `g_bar A_p - r_bar B_p >= 0`.

### Proof

`C_p(q)` is affine in `q`, so it is nonnegative on a closed interval iff it is nonnegative at both endpoints.

At `q=0`, this is `A_p>=0`.

At `q=r_bar/g_bar`, it is

`A_p-B_p r_bar/g_bar >=0`.

Since `g_bar>0`, this is equivalent without division to

`g_bar A_p-r_bar B_p>=0`.

Thus a trusted rational checker can decide whether separate `(tau,c)` interpolation is a valid lower-bound shortcut on the whole homothetic refined cell using only finite sums, products, and sign comparisons.

If the state domain does not attain the full radial interval, (6.5)-(6.6) remain sufficient but need not be necessary.

### Shared-multiplier/common-cell recovery

If `tau_i=tau` for all `i`, then `A_p=B_p=0`; the shortcut is exact.

If `(r_i,g_i)` are common across vertices, then again `A_p=B_p=0`.

This recovers the two special cases already known to be safe in T-P5-152/T-P5-153.

---

## 7. T-P5-154 matrix certificate transforms by congruence

T-P5-154 represents the coarse uniform-floor condition by a symmetric matrix `M_D` such that for coarse simplex weights `lambda`,

**(7.1)**

`lambda^T M_D lambda = Delta_lambda + g_lambda D`.

Under the refinement map `lambda=P mu`, one obtains the exact identity

**(7.2)**

`lambda^T M_D lambda`

`= mu^T (P^T M_D P) mu`.

Define

**(7.3)** `M_D^ref := P^T M_D P`.

### Theorem D — copositive refinement covariance

If `P>=0` entrywise and `M_D` is copositive, then `M_D^ref` is copositive.

### Proof

For any `mu>=0`, nonnegativity of `P` gives `P mu>=0`. Therefore

`mu^T M_D^ref mu`

`= (P mu)^T M_D(P mu)`

`>=0`.

No PSD strengthening is needed; true copositivity itself is preserved under nonnegative congruence.

### Exact-domain converse

If `P Delta_N=Delta_n`, then nonnegativity of the quadratic form on the refined simplex is equivalent to nonnegativity on the coarse simplex. Hence the sharp uniform floor is representation-invariant when the refinement covers the same uncertainty simplex.

If `P Delta_N` is a strict subset, the refined sharp floor may be smaller, which is legitimate domain restriction rather than a coordinate gain.

---

## 8. Important diagonal effect under refinement

At `D=0`, the original T-P5-153/T-P5-154 coarse matrix has zero diagonal because a coarse vertex has no pairwise mixing with itself.

After a genuine interior refinement, however,

`(P^T M_0 P)_{alpha alpha}`

`= (p^alpha)^T M_0 p^alpha`

is generally nonzero.

This diagonal is exactly the internal coarse-simplex coupling already present at the refined vertex.

Therefore one must not expect the exact pushed certificate matrix to remain in the same zero-diagonal `K_ij` parameterization after refinement.

This is another way to see why the adapter

`push tau`, `push r`, `push g`, then rebuild a new zero-diagonal pairwise matrix`

is not generally certificate-preserving. It silently discards the within-column covariance defect.

The mathematically correct options are:

1. push the signed certificate object `h` directly; or
2. push T-P5-154's homogeneous matrix by `M -> P^T M P`; or
3. provide an explicit covariance-defect theorem proving that the separately reconstructed representation is a sound lower bound.

---

## 9. Affine source semantics versus certificate semantics

There are two distinct mathematical types that a source adapter must not conflate.

### Physical affine field

If a physical source field `L(theta)` is affine in the uncertain parameter and a refined parameter vertex satisfies

`theta_tilde_alpha = sum_i p_i theta_i`,

then

`L(theta_tilde_alpha)=sum_i p_i L(theta_i)`.

So ordinary affine physical fields may be transported by `P` directly.

### Weighted proof slack

Even if both `tau(theta)` and `c(theta,m)` happen to be affine separately, their product is generally quadratic in `theta`:

`tau(theta)c(theta,m)`.

The convexified vertex proof object from T-P5-152 is

`sum_i p_i tau_i c_i`,

whereas evaluating the separately interpolated fields gives

`(sum_i p_i tau_i)(sum_i p_i c_i)`.

Theorem B is their exact difference.

Therefore `h=tau*c` should be typed as a proof-certificate quantity after multiplication, not inferred to be an affine physical source field merely because its two factors are affine.

---

## 10. Additive defect budget when exact covariance is unavailable

Sometimes a producer insists on the separately reconstructed object `h_sep` but can bound the omitted signed covariance.

If for a refined vertex or parameter cell one proves

**(10.1)** `C_p(m) >= -Xi`,

with `Xi>=0`, then

`h_push = h_sep + C_p >= h_sep-Xi`.

Consequently,

### Theorem E — one-sided covariance budget

If

`h_sep + D >=0`

and

`C_p >= -Xi`,

then

**(10.2)** `h_push + (D+Xi) >=0`.

This is the correct place to pay a refinement/reconstruction tax. It is one-sided and signed. Replacing it by

`|C_p| <= Xi`

is valid but potentially more conservative.

For a convex combination of refined vertices, if each column has `C_alpha>=-Xi_alpha`, then

`sum_alpha mu_alpha C_alpha >= -sum_alpha mu_alpha Xi_alpha`.

A uniform fallback is `Xi=max_alpha Xi_alpha`, but a weighted exact bound is sharper when the same `mu` is available.

---

## 11. Minimal theorem statements for formalization

The useful formal core can be kept independent of P5 source details.

### Lemma 1 — stochastic pushforward

Inputs:

- finite index types `I`, `A`;
- `P : I -> A -> R`;
- `0<=P i a`;
- `sum_i P i a = 1`;
- `mu a>=0`, `sum_a mu a=1`;
- families `c i`, `h i` in an ordered ring/module.

Define

`lambda i = sum_a P i a * mu a`.

Prove simplex preservation and

`sum_a mu a * sum_i P i a*c i = sum_i lambda i*c i`,

with the identical statement for `h`.

### Lemma 2 — weighted-product covariance

For `p_i>=0`, `sum p_i=1`, prove

`sum_i p_i tau_i c_i`

`- (sum_i p_i tau_i)(sum_i p_i c_i)`

`= sum_{i<j} p_i p_j (tau_i-tau_j)(c_i-c_j)`.

This is a finite-sum ring identity.

### Lemma 3 — homothetic endpoint gate

With

`C(q)=A-Bq`, `g>0`, `r>=0`,

prove

`A>=0` and `g*A-r*B>=0`

imply

`0<=q` and `g*q<=r`

imply `C(q)>=0`.

A converse is available when both radial endpoints are admissible.

### Lemma 4 — nonnegative congruence preserves copositivity

If `M` is symmetric copositive and `P` is entrywise nonnegative, prove

`P^T M P`

is copositive.

None of these lemmas requires matrix inverse, square root, spectral decomposition, singular values, or floating-point reasoning.

---

## 12. Proposed typed source packet

For an actual parameter-refinement adapter, the minimal mathematical packet should distinguish:

- `coarseParameterKey`;
- `refinedParameterKey`;
- exact rational/nonnegative refinement matrix `P`;
- column-sum witnesses `sum_i P_{i alpha}=1`;
- proof that reset fields and cell fields use the same induced coarse weight `lambda=P mu`;
- either the coarse signed certificate objects `(c_i,h_i)` or a coarse T-P5-154 matrix `M_D`;
- if reconstructing from separate `(tau,c)`, the signed covariance object `C_p` or a certified one-sided lower bound;
- for the homothetic shortcut, `(r_i,g_i,tau_i)` and the exact gates `A_p>=0`, `g_bar A_p-r_bar B_p>=0`;
- domain/image coverage: whether `P Delta_N` is the whole original uncertainty simplex or only a sub-simplex.

The adapter should not replace a parameter-map identity by approximate nearest-vertex labels or independently chosen barycentric weights for reset and cell packets.

---

## 13. Open boundaries

This mathematical child does **not** prove any of the following:

1. that the deployed uncertainty representation is in fact a simplex refinement;
2. that one actual source `P` is used consistently by reset, cell, multiplier, reference, controller, and FD packets;
3. that physical parameter fields are affine on the claimed cell;
4. that a triangulation covers the entire intended uncertainty polytope without gaps or unintended extrapolation;
5. Float64/runtime equivalence of barycentric weights or source interpolation;
6. actual source reification of `h=tau*c` rather than separate-factor reconstruction;
7. P8/flowpipe closure;
8. Lean/kernel validation;
9. independent verification by 封不觉;
10. admission/registry promotion.

All remain OPEN.

---

## 14. Recommended integration rule

The shortest safe rule is:

> **Form the signed proof object before changing uncertainty coordinates.** If `h_i=tau_i c_i` is what the vertex theorem proved, push `h` through the same nonnegative column-stochastic parameter map as `c`. Equivalently, push the T-P5-154 quadratic certificate by `M -> P^T M P`. Do not replace this by `push(tau) * push(c)` unless the covariance defect is proved zero/nonnegative or is explicitly budgeted.

This gives an exact, root-free, inverse-free bridge from source parameter refinement to the existing P5 robust-reset mathematics while preserving the distinction between physical affine fields and proof-certificate products.
