---
kind: review_result
review_id: review-T-P5-262-rational-amgm-metric-bridge-guyuefangyuan-20260910T1652Z
task_id: T-P5-262-RATIONAL-AMGM-METRIC-BRIDGE
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T16:52:00Z
claim_commit: 2d4cfbc440f7e9972fa99a760e294e4a6fe7ccae
inspected_commit: 982685b0a3563da90931388be24fe95a476968be
upstream_commits:
  - f17933375d1275a5ad9ecff9bf810d0678e5c113  # T-P5-261 matched-metric polarization
  - b8a204dc8c3ae93128534689cbeb5aa5d8d9b925  # T-P5-260 uniform cell Gram selection
  - a24047e5b78cc0cabb191cfac7fab4a99deb1fec  # T-P5-258 binary realized-direction SOS
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_rational_AMGM_bridge_identity; add_mixedMetric_canonicalPolarization_transport; add_direct_Loewner_bridge_packet; add_spectralSandwich_optimized_distortion; add_fractionFree_distortion_gate; add_affineCell_vertex_bridge; add_metric_mismatch_regressions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact quadratic identities, Loewner-order transport, one-variable optimization, rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-262 — Rational AM-GM bridge for mixed-metric polarization

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-261 proves that canonical symmetric polarization is lossless when the two radial metrics coincide (or are proportional), but its generic nonmatching fallback loses the full condition ratio `beta/alpha` under a sandwich

`alpha W <= M <= beta W`.

This child gives a strictly sharper, completely rational bridge for the nonmatching branch. The central observation is that no matrix square root or geometric mean is required: for every positive scalar `t`, the auxiliary metric

`J_t := t^2 M + W`

satisfies the exact scalar identity

**(0.1)**

`(u^T J_t u)^2 - 4 t^2 (u^T M u)(u^T W u)`

`= [t^2 (u^T M u) - (u^T W u)]^2 >= 0`.

Therefore a mixed radial quartic can be embedded into one matched quadratic square, T-P5-261 can be applied there without loss, and only then is the bridge transported back to the original two metrics.

The resulting packet is exact-rational whenever `t,M,W` and the submitted Loewner comparison constants are rational. Under only `alpha W <= M <= beta W`, optimizing this AM-GM bridge improves the worst-case distortion from

`beta/alpha`

to the infimum

**(0.2)** `[(1 + sqrt(beta/alpha))/2]^2`.

For every strict rational budget above that infimum, a rational `t` exists, so the checker can remain entirely rational. The infimum is sharp **for this one-parameter AM-GM bridge family**; it is not claimed to be the universal sharp mixed-metric polarization constant for every particular `F,M,W`.

No actual deployed P5 metric pair, factor, source cell, tube/trajectory coverage, Float64/interval semantics, Lean receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

# Part I — setup and the exact AM-GM bridge

## 1. Setup

Let

`M=M^T>0`, `W=W^T>0`

be two SPD matrices on the same quotient coordinates. Write

`q_M(u)=u^T M u`,

`q_W(u)=u^T W u`.

Let `F : R^n -> R^m` be a homogeneous quadratic vector map, and let `S` be its unique symmetric bilinear polarization:

`F(u)=S(u,u)`.

Define the canonical linear factor in the second slot

`A_sym(u)v := S(u,v)`.

Assume the realized-direction scalar packet

**(1.1)**

`||F(u)||^2 <= kappa q_M(u) q_W(u)`

for every `u`, with `kappa>=0`.

The arbitrary-factor warning from T-P5-261 remains in force: all matrix statements below concern the canonical symmetric factor `A_sym`, or the doubled fraction-free symmetrization, not an arbitrary gauge-equivalent factor `A(u)` satisfying only `A(u)u=F(u)`.

---

## 2. Lemma 1 — fraction-free scalar bridge identity

For any `t>0`, define

**(2.1)** `J_t := t^2 M + W`.

Then for every `u`,

**(2.2)**

`q_{J_t}(u)^2 - 4 t^2 q_M(u) q_W(u)`

`= [t^2 q_M(u)-q_W(u)]^2`.

### Proof

Put `x=q_M(u)` and `y=q_W(u)`. Then

`q_{J_t}(u)=t^2 x+y`,

and

`(t^2x+y)^2-4t^2xy=(t^2x-y)^2`.

No commutativity assumption on `M,W` is involved; the identity occurs after evaluation on the same physical direction `u`.

Consequently,

**(2.3)** `4t^2 q_M(u)q_W(u) <= q_{J_t}(u)^2`.

Combining (1.1) and (2.3),

**(2.4)**

`||F(u)||^2 <= [kappa/(4t^2)] q_{J_t}(u)^2`.

This is now exactly the matched-metric situation of T-P5-261.

---

# Part II — canonical polarization through the bridge

## 3. Theorem 1 — mixed metric to one matched metric

Under the setup above, for every `t>0`,

**(3.1)**

`4t^2 A_sym(u)^T A_sym(u)`

`<= kappa q_{J_t}(u) J_t`

for every `u`.

### Proof

Equation (2.4) is a diagonal quadratic-map estimate in the single SPD metric `J_t`. Applying the matched-metric polarization equivalence of T-P5-261 with constant `kappa/(4t^2)` gives

`A_sym(u)^T A_sym(u)`

`<= [kappa/(4t^2)] q_{J_t}(u)J_t`.

Multiply by `4t^2>0`.

### Why this matters

The bridge does not first replace `M` by a crude scalar multiple of `W`. It postpones metric comparison until **after** the lossless canonical polarization step. That is exactly where T-P5-261's `beta/alpha` fallback was leaving avoidable slack.

---

## 4. Theorem 2 — direct rational Loewner bridge packet

Fix `t>0`. Suppose positive scalars `p,q` satisfy the two Loewner inequalities

**(4.1)** `J_t <= p M`,

**(4.2)** `J_t <= q W`.

Then

**(4.3)**

`A_sym(u)^T A_sym(u)`

`<= kappa [pq/(4t^2)] q_M(u) W`

for every `u`.

### Proof

From (4.1),

`q_{J_t}(u) <= p q_M(u)`.

From (4.2),

`J_t <= qW`.

Therefore

`q_{J_t}(u)J_t <= pq q_M(u)W`.

Insert this in (3.1) and divide by `4t^2`.

### Exact-rational checker form

A checker does not need generalized eigenvalues. A producer may submit rational

`t>0`, `p>0`, `q>0`, `C>=0`

and verify

**(4.4)** `pM-J_t >= 0`,

**(4.5)** `qW-J_t >= 0`,

**(4.6)** `pq <= 4t^2 C`.

Then the checker concludes directly

**(4.7)**

`A_sym(u)^T A_sym(u) <= kappa C q_M(u)W`.

All matrices and scalar inequalities can be rational/fraction-free. No matrix square root, matrix geometric mean, SVD, pseudoinverse, floating rank tolerance, or numerical eigensystem is required.

This direct `(t,p,q,C)` packet is preferable to first extracting global spectral sandwich constants when actual matrix structure admits tighter rational Loewner bounds.

---

## 5. Doubled canonical factor

If a producer starts from a coefficient tensor for an arbitrary linear factor, first purge the antisymmetric input-slot syzygy exactly as in T-P5-261. Let

`Ahat_sym(u)=2A_sym(u)`

be the doubled symmetric factor.

Then (3.1) becomes

**(5.1)**

`t^2 Ahat_sym(u)^T Ahat_sym(u)

`<= kappa q_{J_t}(u)J_t`,

and (4.7) becomes

**(5.2)**

`Ahat_sym(u)^T Ahat_sym(u)`

`<= 4 kappa C q_M(u)W`.

Thus coefficient symmetrization and mixed-metric bridging can both remain denominator-free at the serialized theorem layer.

---

# Part III — spectral-sandwich specialization

## 6. Corollary 1 — explicit bridge from `alpha W <= M <= beta W`

Assume

**(6.1)** `0<alpha<=beta`,

**(6.2)** `alpha W <= M <= beta W`.

Then

`W <= alpha^(-1) M`,

so

**(6.3)**

`J_t=t^2M+W <= (t^2+1/alpha)M`.

Also

**(6.4)**

`J_t <= (beta t^2+1)W`.

Hence Theorem 2 applies with

`p(t)=t^2+1/alpha`,

`q(t)=beta t^2+1`.

The distortion is

**(6.5)**

`C(t)=p(t)q(t)/(4t^2)`

`= [beta t^2 + 1 + beta/alpha + 1/(alpha t^2)]/4`.

Therefore

**(6.6)**

`A_sym(u)^T A_sym(u)`

`<= kappa C(t) q_M(u)W`.

This is valid for every positive `t`.

---

## 7. Theorem 3 — optimal distortion inside the AM-GM bridge family

Let

`r:=beta/alpha >=1`.

Then

**(7.1)**

`inf_{t>0} C(t) = (1+r+2sqrt(r))/4`

`= [(1+sqrt(r))/2]^2`.

The optimum occurs at

**(7.2)** `t^4=1/(alpha beta)`.

### Proof

From (6.5),

`4C(t)=1+r+beta t^2+1/(alpha t^2)`.

By AM-GM,

`beta t^2+1/(alpha t^2) >= 2sqrt(beta/alpha)=2sqrt(r)`.

Equality holds exactly when

`beta t^2=1/(alpha t^2)`,

that is `t^4=1/(alpha beta)`.

Equivalently,

**(7.3)**

`C(t)-C_*`

`= (1/4)[sqrt(beta)t - 1/(sqrt(alpha)t)]^2 >=0`,

where `C_*=[(1+sqrt(r))/2]^2`.

### Comparison with T-P5-261's generic fallback

T-P5-261 gives the safe factor `r=beta/alpha`.

For `r>1`,

`C_*<r`,

because

`4(r-C_*) = 3r-1-2sqrt(r)`

`= (sqrt(r)-1)(3sqrt(r)+1)>0`.

At `r=1`, `C_*=1`, consistently recovering the proportional-metric no-loss limit at the real optimization level.

Thus the AM-GM bridge strictly improves the condition-ratio budget whenever the two-metric sandwich is genuinely nontrivial.

### Scope of sharpness

The word “optimal” here refers only to the one-parameter bridge family

`J_t=t^2M+W`

combined with the interval-derived comparison constants (6.3)-(6.4).

This does **not** prove that `C_*` is the universally smallest possible constant for every particular mixed-metric quadratic map. Actual `F` can have additional cancellation, and direct Loewner bounds in Theorem 2 can also beat the interval-only estimate.

---

## 8. Rational approximation and the exact checker boundary

Even when `alpha,beta` are rational, the real optimizer (7.2) need not be rational because it involves a fourth root.

This is not an obstacle for exact serialization.

The map `t -> C(t)` is continuous on `(0,infinity)`, and positive rationals are dense. Therefore for every rational target `Cbar` satisfying

**(8.1)** `Cbar>C_*`,

there exists a rational `t>0` with

**(8.2)** `C(t)<Cbar`.

The producer can search over rational `t` and submit the finite `(t,p,q,Cbar)` packet of Theorem 2. Thus no algebraic number needs to appear in the checker.

If the exact real optimum happens to use rational `t`, it may of course be attained exactly.

### Important proportional branch rule

When `M=cW` exactly, use T-P5-261's direct proportional-metric theorem, which gives the exact factor `1` with no need to approximate the optimizer. The AM-GM bridge is a fallback for genuine mismatch, not a replacement for exact proportionality detection.

---

## 9. Root-free planning test for a desired interval-only budget

Although an actual rational bridge witness should still be serialized through `(t,p,q)`, one can test whether a proposed scalar budget `Cbar` lies above the real AM-GM infimum without evaluating a square root.

For rational `alpha,beta,Cbar>0`, define

**(9.1)** `T := 4 alpha Cbar - alpha - beta`.

Then

**(9.2)** `Cbar >= C_*`

if and only if

**(9.3)** `T>=0`

and

**(9.4)** `T^2 >= 4 alpha beta`.

### Proof

`Cbar>=C_*` is equivalent to

`4alpha Cbar >= alpha+beta+2sqrt(alpha beta)`.

Move the rational terms to the left. Since both sides after the move must be nonnegative, squaring is lossless and yields (9.3)-(9.4).

This pair is useful as a root-free **budget-planning gate**. For final exact rational serialization at a strict budget, one still supplies a rational bridge `t` as in Theorem 2.

---

# Part IV — exact rational regression

## 10. Regression — `alpha=1/16`, `beta=1`

Take the metric mismatch used in T-P5-261's same-constant counterexample:

`W=I`,

`M=diag(1,1/16)`.

Then

`alpha=1/16`, `beta=1`, `r=16`.

T-P5-261's generic condition-ratio fallback gives distortion

`C_old=16`.

For the present bridge, the real optimizer satisfies

`t^4=16`,

so the rational choice

**(10.1)** `t=2`

is exactly optimal.

Then

`J=4M+W`,

`p=t^2+1/alpha=4+16=20`,

`q=beta t^2+1=5`.

Hence

**(10.2)**

`C_new=pq/(4t^2)=100/16=25/4`.

So the exact rational bridge improves the generic distortion

`16 -> 25/4`.

For the concrete map from T-P5-261,

`F(x,y)=(x^2,xy)`,

one has the scalar packet

`||F||^2 <= q_M q_W`

with `kappa=1`. At `u=(0,1)`, the canonical matrix factor requires at least `C>=4` from that single direction, while the universal interval bridge gives `25/4`. This illustrates both facts simultaneously:

1. the new bridge is dramatically sharper than `16`;
2. it is still a structural universal bound, not necessarily the particular map's sharp mixed-metric constant.

---

## 11. Counterexample boundary — universal same-constant transport is false

The T-P5-261 rational counterexample already shows that one cannot simply replace the mixed scalar product by the same-constant canonical matrix gate when metrics differ.

With

`F(x,y)=(x^2,xy)`,

`W=I`,

`M=diag(1,1/16)`,

one has

`||F(u)||^2 <= q_M(u)q_W(u)`

for every `u`, but at `u=(0,1)`

`A_sym(u)^T A_sym(u)=diag(1/4,0)`

whereas

`q_M(u)W=(1/16)I`.

Thus factor `C=1` fails.

The present child therefore does not seek an impossible universal same-constant representation under arbitrary mismatch. It instead gives a tunable exact-rational path between the proportional branch and low-dimensional realized-quartic/SOS branches.

---

# Part V — parameter-cell transport

## 12. Corollary 2 — one bridge over an affine parameter cell

Let `s` vary in a convex polytope `P`. Suppose

`M(s)` and `W(s)` are affine symmetric matrix families,

and are SPD on `P`.

Fix rational scalars `t>0,p>0,q>0,C>=0`, and define

`J_t(s)=t^2M(s)+W(s)`.

The matrix families

`pM(s)-J_t(s)`

and

`qW(s)-J_t(s)`

are affine in `s`.

Therefore the uniform Loewner conditions

`J_t(s)<=pM(s)`,

`J_t(s)<=qW(s)`

for all `s in P`

are exactly reduced to checking them at the vertices of `P`.

If additionally `pq<=4t^2C`, then every parameter value inherits the same mixed-metric polarization overhead `C`.

### Proof

An affine symmetric matrix family evaluated at a convex combination of vertices is the same convex combination of the vertex matrices. The PSD cone is convex. Necessity follows by evaluating at each vertex; sufficiency follows by convexity.

### Relation to T-P5-260

T-P5-260 gives finite vertex/corner transport for parameter-dependent ternary Gram selectors. The present corollary is a different high-dimensional route: when a rational bridge metric is enough, the **bridge itself** can be certified uniformly by finitely many vertex PSD checks. No ternary Gram selector is needed merely to control metric mismatch.

This does not prove the scalar realized-direction premise (1.1) uniformly; that remains a separate source-facing obligation.

---

# Part VI — decision layer

## 13. Recommended dispatcher

For an actual same-key quotient packet with a homogeneous quadratic vector remainder `F` and two SPD radial metrics `M,W`, the mathematical dispatcher should be:

1. **Canonicalize factor first.** Purge antisymmetric input-slot syzygies and work with `A_sym` / `Ahat_sym`.
2. **Exact proportionality check.** If `M=cW`, use T-P5-261 at factor `1`.
3. **Direct rational bridge search.** Try rational `t,p,q` with
   `J_t=t^2M+W`, `J_t<=pM`, `J_t<=qW`; charge `pq/(4t^2)`.
4. **Uniform sandwich fallback.** If only `alpha W<=M<=beta W` is available, tune rational `t` near the optimum (7.2), giving overhead arbitrarily close to `C_*`.
5. **Low-dimensional exact quartic route.** If the bridge still spends too much reserve and quotient dimension is 2 or 3, use T-P5-258/259 realized-direction SOS/Gram machinery rather than declaring physical failure.
6. **Generic higher-dimensional route.** A failed bridge is only a failure of this sufficient matrix representation, not a proof that the scalar radial inequality is false.

This keeps the cheap high-dimensional positive class in front while preserving the exact low-dimensional escape hatches.

---

# Part VII — Lean-facing decomposition

## 14. Suggested small theorem statements

### Lemma A — scalar AM-GM bridge identity

For symmetric quadratic forms `M,W` and scalar `t`,

`q (t^2 M + W) u ^ 2 - 4*t^2*(q M u)*(q W u)`

`= (t^2*q M u - q W u)^2`.

This is ring algebra.

### Lemma B — mixed radial to matched radial

Assuming `t>0`, `kappa>=0`, and

`||F u||^2 <= kappa*(q M u)*(q W u)`,

prove

`||F u||^2 <= (kappa/(4*t^2))*(q (t^2 M+W) u)^2`.

### Lemma C — bridge canonical polarization

Consume Lemma B and T-P5-261's matched-metric polarization theorem to obtain

`4*t^2 * gram (A_sym u) <= kappa*(q J u) • J`.

### Lemma D — two-Loewner transport

Assuming

`J<=pM`, `J<=qW`,

prove

`q J u • J <= p*q*(q M u) • W`.

No inverses are required.

### Lemma E — rational bridge packet

Combine C and D with `p*q<=4*t^2*C` to conclude

`gram (A_sym u) <= kappa*C*(q M u) • W`.

### Lemma F — spectral sandwich bridge

From `alpha W<=M<=beta W`, prove

`J_t <= (t^2+1/alpha)M`

and

`J_t <= (beta*t^2+1)W`.

A fraction-free version should multiply through by positive `alpha` rather than normalize by division.

### Lemma G — root-free budget test

For positive `alpha,beta,C`, with

`T=4*alpha*C-alpha-beta`,

prove that

`T>=0` and `T^2>=4*alpha*beta`

imply

`C >= (1+beta/alpha+2*sqrt(beta/alpha))/4`.

This lemma is optional for the first rational checker implementation because the `(t,p,q)` witness path avoids square roots entirely.

### Lemma H — affine-cell vertex PSD transport

For affine symmetric matrix map `L(s)` over a finite polytope, vertex PSD implies PSD on every convex combination. Instantiate it twice for `pM-J` and `qW-J`.

---

# Part VIII — remaining obligations

## 15. What this child does not close

The following remain open and must not be inferred from this result:

- actual P5 same-key reification of `M,W,F`;
- proof that the deployed factor has been canonicalized rather than carrying an invisible syzygy;
- actual scalar realized-direction inequality (1.1);
- actual rational `(t,p,q,C)` packet for deployed cells;
- proof that `M,W` are SPD on the relevant quotient/source domain;
- source/cell/tube/trajectory/FD-halo coverage;
- Float64/interval enclosure and reserve-floor accounting;
- Lean compile/kernel receipt;
- independent verification by 封不觉;
- admission, registry mutation, or parent P5 closure.

Failure of a bridge PSD comparison is **not** physical FAIL. It only means this sufficient high-dimensional matrix lane is too coarse for that packet; retain T-P5-258/259 and direct realized-direction routes.

---

## 16. Next mathematical seam

The clean next question is whether the one-parameter arithmetic bridge can be enlarged without losing exact rational checkability.

One candidate is a structured auxiliary SPD metric `J` satisfying a directly certified quartic domination

`q_J(u)^2 >= 4 q_M(u)q_W(u)`

or an equivalent low-rank/tensor identity, together with `J<=pM` and `J<=qW`. If such `J` can exploit eigenspace alignment or block structure, it may beat the scalar `t` bridge while remaining high-dimensional and rational.

A second, more source-facing seam is to bind actual P5 quotient metrics and determine whether direct rational `(t,p,q)` comparisons already fit inside the current Lyapunov reserve. Only if the present `C_*`-level overhead is still too large is a more elaborate mixed-metric polarization theorem justified.

Until such source data are bound, this child remains mathematical infrastructure only.
