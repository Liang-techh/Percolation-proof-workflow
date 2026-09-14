---
kind: review_result
review_id: review-T-P5-247-affine-gln-chart-covariance-liuguanyi-20260910T1303Z
task_id: T-P5-247-AFFINE-GLN-CHART-COVARIANCE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T13:03:00Z
claim_commit: b5c1644c99a0779724a394369b38c568ef46bf5d
inspected_commit: bc7357f28503e98343a825626dd07fe30755e6d2
upstream_commits:
  - f4457fd93d95b1ed58c5ec4f3fbb995a2f73fb9a  # T-P5-246 joint shifted source-target S-lemma
  - bfe7ba1932c69dad624c270495f7c87ee5722d5f  # T-P5-245 anisotropic source trust-region reserve
  - fb6c28d0f7492fc1f21856835e4c11a20047beed  # T-P5-244 source ellipsoid outward sensitivity
  - e8ba5dc69b700621893313a4202255a98267ebef  # T-P5-243 strict-margin coefficient-error budget
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_affine_chart_pullback_identity; add_slemma_affine_congruence; add_fraction_free_reverse_affine_transport; add_affine_composition_functoriality; add_metric_relative_reserve_invariance; preserve_nonlinear_and_nonsurjective_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact affine quadratic expansion; augmented congruence algebra; determinant/adjugate identities; exact rational 2D regression; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-247 — Full invertible affine-chart covariance of quadratic Lyapunov certificates

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-246 closed exact source-target **translation** covariance and explicitly left the next distinct seam: full invertible affine chart covariance. This child proves that a genuine coordinate scaling/shear/rotation must not be charged as a physical coefficient perturbation.

For an invertible affine chart

`y = P z + h`,  `det(P) != 0`,

a quadratic target, a shifted ellipsoidal source, and the one-constraint S-lemma certificate all transform by the same augmented congruence. Sequential affine charts equal one composed chart exactly. For rational `P`, the reverse certificate can be transported without forming `P^{-1}`: `det(P)` and `adj(P)` give an exact division-free reverse congruence.

The useful strict reserve is therefore a **metric-relative block reserve** transported with the chart. A raw Euclidean smallest-eigenvalue margin of the certificate matrix is not chart-invariant and must not be used as a cross-chart physical budget.

No actual P5 chart/source packet, tube/cell coverage, Float64 semantics, Lean receipt, independent verification, registry mutation, or parent closure is claimed.

---

# Part I — typed affine source/target contract

## 1. Data and assumptions

Let

- `P in R^{n x n}` with `det(P) != 0`,
- `h,c in R^n`,
- `M=M^T > 0`, `R>0`,
- `G=G^T`, `l in R^n`, `A in R`.

The physical/source-side variable is `y`. Define

`q_y(y) := A + 2 l^T y + y^T G y`,

and the shifted ellipsoid

`E_y := { y : (y-c)^T M (y-c) <= R }`.

Use the affine coordinate chart

**`y = P z + h`.**

Instead of introducing `P^{-1}` into the theorem statement, assume a chart-coordinate center `k` is supplied with the exact compatibility equation

**`c = P k + h`.**

This is the preferred typed adapter boundary: the source producer may provide `k` and prove one linear identity; the math theorem never needs a floating inverse.

Define the pulled source matrix

**`M_z := P^T M P`.**

Then

`y-c = P(z-k)`

and hence exactly

**`(y-c)^T M (y-c) = (z-k)^T M_z (z-k)`.**

Because `P` is invertible and `M>0`, also `M_z>0`.

---

## 2. Exact target pullback

Substitute `y=Pz+h` into `q_y`:

`q_y(Pz+h)`

`= A + 2 l^T(Pz+h) + (Pz+h)^T G(Pz+h)`

`= [A+2l^Th+h^TGh]`

`  + 2 [P^T(l+Gh)]^T z`

`  + z^T[P^TGP]z`.

Define

**`A_z := A + 2 l^T h + h^T G h`,**

**`l_z := P^T(l+Gh)`,**

**`G_z := P^T G P`.**

Then

**Theorem 1 — `quadraticPullback_affine`.**

`q_y(Pz+h) = A_z + 2 l_z^T z + z^T G_z z` for every `z`.

This is an identity. Scaling/shear in `P` is coordinate covariance, not coefficient uncertainty.

---

# Part II — affine S-lemma congruence

## 3. Original and pulled certificate blocks

For a fixed multiplier `mu>=0`, define

`S_y(mu) :=`

`[[ mu M-G,            -l-mu M c ],`

` [ (-l-mu M c)^T,  -A-mu R+mu c^T M c ]]`.

Then

`[y;1]^T S_y(mu) [y;1]`

`= -q_y(y) - mu ( R-(y-c)^T M(y-c) )`.

The pulled data define

`S_z(mu) :=`

`[[ mu M_z-G_z,             -l_z-mu M_z k ],`

` [ (-l_z-mu M_z k)^T,  -A_z-mu R+mu k^T M_z k ]]`.

Introduce the augmented affine matrix

**`H(P,h) := [[P,h],[0,1]]`.**

Since `[y;1]=H(P,h)[z;1]`, direct polynomial substitution gives

**Theorem 2 — `slemmaBlock_affineCongruence`.**

**`S_z(mu) = H(P,h)^T S_y(mu) H(P,h)`.**

### Proof at block level

Top-left:

`P^T(mu M-G)P = mu M_z-G_z`.

Top-right:

`P^T[(mu M-G)h-l-mu Mc]`

`= -P^T(l+Gh) + mu P^T M(h-c)`

`= -l_z - mu P^T M P k`

`= -l_z-mu M_z k`,

using `h-c=-Pk`.

Bottom-right:

the target part is `-A_z`; the source part is

`-mu R + mu(h-c)^TM(h-c)`

`= -mu R + mu k^TM_zk`.

Thus every block agrees.

Because `H(P,h)` is invertible,

**`S_y(mu) >= 0  <=>  S_z(mu) >= 0`.**

Therefore the set of admissible S-lemma multipliers is exactly the same in both charts.

---

## 4. Safety and sharpness are chart invariant

The affine map is a bijection and maps `E_z` exactly to `E_y`. Hence

**Theorem 3 — `quadraticSafety_affineIff`.**

`q_y(y)<=0` for all `y in E_y`

iff

`q_z(z)<=0` for all `z in E_z`.

Likewise contact points transport bijectively:

`q_y(y*)=0`, `y* in boundary(E_y)`

iff

`q_z(z*)=0`, `z* in boundary(E_z)`,

with `y*=Pz*+h`.

Hence an exact chart cannot create or destroy a Lyapunov violation or a sharp boundary contact.

---

# Part III — fraction-free reverse transport

## 5. Augmented adjugate without `P^{-1}`

Assume now all matrix/vector data are rational and let

**`delta := det(P) != 0`.**

Set

`J := adj(P)`,

so

`PJ = JP = delta I`.

Define the augmented integer/rational reverse chart

**`B(P,h) := [[J, -J h],[0,delta]]`.**

A direct multiplication gives

**`H(P,h) B(P,h) = B(P,h) H(P,h) = delta I_{n+1}`.**

Thus `B=delta H^{-1}` but no division is needed to construct it.

---

## 6. Division-free reverse certificate theorem

Starting from Theorem 2,

`S_z = H^T S_y H`.

Multiply by `B` on both sides:

`B^T S_z B`

`= (HB)^T S_y (HB)`

`= delta^2 S_y`.

Therefore:

**Theorem 4 — `fractionFreeReverseAffineCongruence`.**

**`B(P,h)^T S_z(mu) B(P,h) = delta^2 S_y(mu)`.**

Since `delta^2>0`, this yields a purely rational reverse PSD witness:

**`S_z(mu)>=0  <=>  S_y(mu)>=0`.**

No `P^{-1}`, Cholesky factor, square root, pseudoinverse, floating eigenvector, or numerical solve is needed.

The same construction transports any symmetric quadratic block, not only an S-lemma block.

---

## 7. Determinant scaling

Because `det H(P,h)=det P=delta`, Theorem 2 also implies

**`det(S_z(mu)) = delta^2 det(S_y(mu))`.**

Likewise

**`det(M_z)=delta^2 det(M)`.**

Therefore zero/nonzero determinant and determinant sign are chart invariant, though their raw magnitudes are not.

For singular-contact logic this is important: a regular/singular certificate branch cannot change merely because the coordinate chart was sheared or rescaled.

---

# Part IV — composition / associativity

## 8. Sequential affine charts

Let

`x = P1 z + h1`,

`y = P2 x + h2`.

Then

`y = (P2 P1) z + (P2 h1+h2)`.

At the augmented level,

**`H(P2,h2) H(P1,h1) = H(P2P1, P2h1+h2)`.**

If `S_x=H(P2,h2)^T S_y H(P2,h2)` and then

`S_z=H(P1,h1)^T S_x H(P1,h1)`,

we obtain

`S_z`

`= [H(P2,h2)H(P1,h1)]^T S_y [H(P2,h2)H(P1,h1)]`.

Therefore:

**Theorem 5 — `affineCertificateTransport_compose`.**

Sequential chart transport is exactly equal to one direct transport under the composed affine chart.

There is no chart-depth penalty and no accumulation of artificial coefficient-error budgets when every step is exact.

The reverse fraction-free packets compose up to the expected positive determinant scale; since the scale is a square in PSD congruence, the sign/admission mathematics is unchanged.

---

# Part V — the correct invariant strict reserve

## 9. Metric-relative block reserve

A non-orthogonal congruence does not preserve Euclidean eigenvalues. Therefore a statement such as

`lambda_min(S)>=epsilon`

must not be copied numerically between charts.

Instead let `C_y=C_y^T>=0` be the reference reserve metric and define

`C_z := H^T C_y H`.

Then for every scalar `rho`,

`S_z-rho C_z`

`= H^T(S_y-rho C_y)H`.

Hence:

**Theorem 6 — `relativePSDReserve_affineInvariant`.**

**`S_y >= rho C_y  <=>  S_z >= rho C_z`.**

Consequently the generalized metric-relative reserve

`rho_* := sup {rho : S-rho C >=0}`

is exactly chart invariant when the reference metric is transported with the chart.

This is the appropriate cross-chart quantity for T-P5-243/T-P5-246 style reserve accounting.

---

## 10. Raw Euclidean spectral margin is not invariant

Take the one-dimensional augmented certificate

`S_y = I_2`, `h=0`, `P=[1/10]`.

Then

`H=diag(1/10,1)`

and

`S_z=H^T S_y H=diag(1/100,1)`.

Thus

`lambda_min(S_y)=1`,

but

`lambda_min(S_z)=1/100`.

Nothing physical weakened; only the coordinate scale changed.

If `C_y=I_2` and `C_z=H^TH`, the relative reserve remains exactly `rho_*=1` in both charts.

**Dispatcher rule:** never spend a raw Euclidean block eigenvalue margin across an unnormalized GL(n) chart. Transport the reserve metric or return to a common chart first.

---

# Part VI — exact chart change has zero perturbation cost

## 11. Covariant source-target transport

Suppose a second packet is not a physically perturbed system at all, but merely the exact affine re-expression of the first packet. Then by Theorem 2

`S_new(mu)=H^T S_old(mu)H`.

If one first transports the old reference certificate into the new chart, the effective block perturbation is identically zero:

**`Delta_chart S(mu) := S_new(mu)-H^T S_old(mu)H = 0`.**

This generalizes the translation-zero-cost theorem of T-P5-246 from the affine subgroup `P=I` to all `GL(n)` charts.

Therefore:

**Theorem 7 — `exactAffineChart_zeroReserveCost`.**

An exact invertible affine coordinate change consumes **zero physical Lyapunov reserve**. Any nonzero coefficient difference seen before chart normalization is coordinate artifact.

This matters for source-to-math adapters: chart normalization must precede T-P5-243 coefficient-error charging.

---

# Part VII — exact rational regression

## 12. A 2D shear/scale/translation packet

Choose

`P = [[2,1],[0,1]]`,

`h=c=(3,-1)^T`,

`M=diag(2,1)`, `R=1`,

and the strict target

`q_y(y) = -1 + (1/2)(y-c)^T M(y-c)`.

Expanded in absolute `y` coordinates,

`A=17/2`,

`l=(-3,1/2)^T`,

`G=diag(1,1/2)`.

For `mu=3/4`, the original S-lemma block is

`S_y =`

`[[1/2, 0,   -3/2],`

` [0,   1/4,  1/4],`

` [-3/2,1/4,  5   ]]`.

The pulled source center is `k=0` and

`M_z=P^TMP=[[8,4],[4,3]]`.

The exact transformed certificate is

`S_z=H^T S_y H`

`= [[2,1,0],[1,3/4,0],[0,0,1/4]]`

`= diag_block((1/4)M_z,1/4) > 0`.

Now

`delta=det P=2`,

`adj(P)=[[1,-1],[0,2]]`,

and

`B=[[1,-1,-4],[0,2,2],[0,0,2]]`.

Direct exact multiplication gives

`HB=BH=2I_3`

and

**`B^T S_z B = 4 S_y`.**

Thus the full nontrivial translation + shear + scaling is transported exactly with rational arithmetic and no inverse.

The physical safety reserve is unchanged: on the source ellipsoid,

`q_y <= -1/2`,

and the same statement holds in `z` coordinates because the target/source values are identical under the chart.

---

# Part VIII — minimal formal theorem leaves

## 13. Suggested Lean interface

The mathematical content can be split into small leaves without importing the full P5 source stack:

1. `affineSourceQuadratic_pullback`
   - hypotheses: `c=P*k+h`;
   - conclusion: `(Pz+h-c)^T M(Pz+h-c)=(z-k)^T(P^TMP)(z-k)`.

2. `affineTargetQuadratic_pullback`
   - exact formulas for `A_z,l_z,G_z`.

3. `slemmaBlock_affineCongruence`
   - block matrix equality `S_z=H^T S_y H`.

4. `affineCongruence_psd_iff`
   - if `IsUnit(det P)` / invertible linear equivalence, PSD iff.

5. `augmentedAdjugate_mul`
   - `B H = H B = det(P) I`.

6. `fractionFreeReverseAffineCongruence`
   - `B^T S_z B=det(P)^2 S_y`.

7. `affineChart_compose`
   - augmented matrix composition identity.

8. `relativePSDReserve_affineInvariant`
   - simultaneous congruence of certificate and reserve metric.

9. `exactAffineChart_zeroReserveCost`
   - transported packet difference is zero.

Recommended exact-real/rational theorem layer first; Float64 chart construction belongs to a separate source/evaluator adapter.

---

# Part IX — boundaries and obstruction semantics

## 14. Noninvertible linear map

The congruence identity `S_z=H^TS_yH` still makes algebraic sense for singular/rectangular forward maps, and a safe ambient certificate restricts safely to the image. But the converse fails: the chart may omit unsafe physical directions.

Therefore the iff theorem and reverse certificate require invertibility/surjectivity. A noninjective lift/quotient must use the separate quotient/gauge machinery from earlier P5 children, not this GL(n) theorem.

Suggested failure label:

`AFFINE_CHART_NOT_BIJECTIVE__USE_QUOTIENT_OR_IMAGE_THEOREM`.

---

## 15. Nonlinear or approximate chart

If

`y = Pz+h+r(z)`

with nonzero nonlinear remainder `r`, then the exact augmented congruence no longer represents the full target/source composition. The extra terms are genuine chart/Lie/Taylor defects and must be bounded on the same domain.

Do not silently absorb a nonlinear chart into `P,h` and claim zero reserve cost.

Suggested failure label:

`NONLINEAR_CHART_DEFECT_UNCHARGED`.

---

## 16. Approximate source-center compatibility

The source transport theorem used exact

`c=P k+h`.

If only `||c-(Pk+h)||<=eta` is available, the source ellipsoid is not exactly the pulled ellipsoid. This becomes a source-motion problem and must be charged using the T-P5-244/245/246 machinery or an exact interval inclusion.

Suggested label:

`AFFINE_CENTER_COMPATIBILITY_NOT_EXACT`.

---

## 17. Decimal / Float64 chart matrix

A decimal or binary64 `P` is not automatically the intended exact rational chart. For a source-bound consumer, the producer must state whether the chart is:

- exact rational/real data;
- decoded binary64 data with exact dyadic semantics; or
- an approximation to another physical chart.

Only the first two admit exact congruence after correct decoding; the third carries a chart-coefficient error that must be charged separately.

---

# Part X — next distinct mathematical seam

## 18. Structural fingerprint

This child establishes the fingerprint

**exact invertible affine chart**

`-> source quadratic pullback`

`-> target quadratic pullback`

`-> augmented S-lemma congruence`

`-> fraction-free adjugate reverse transport`

`-> functorial chart composition`

`-> metric-relative reserve invariance`

`-> zero physical error cost for exact GL(n) reparameterization`.

This is a coordinate-covariance mechanism, not another perturbation inequality.

## 19. Recommended next seam

The next genuinely different source-facing theorem is **controlled nonlinear-chart defect transport**.

A useful minimal statement would start from

`y=Pz+h+r(z)`,

with exact bounds on `r(z)` and `Dr(z)` over one source ellipsoid/tube, and derive the induced quadratic-target defect and source-domain inclusion after the affine part has been normalized away. The essential question is whether a first-order chart defect can be charged with an existing strict quadratic reserve without losing the cancellation that T-P5-246/247 expose.

That should only be pursued when an actual P5 source adapter provides a nonlinear/approximate chart packet. Otherwise T-P5-247 closes the full exact affine seam.

---

## 20. Non-claims

This review does not establish:

- an actual deployed P5 `P,h,k,M,A,l,G` packet;
- exact equality between any runtime chart and this mathematical affine chart;
- tube/cell/trajectory/FD-halo coverage;
- Float64/interval enclosure;
- nonlinear chart-defect bounds;
- a Lean/kernel receipt;
- independent validation by 封不觉;
- admission/registry eligibility;
- P5/P8/M4 parent closure.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.