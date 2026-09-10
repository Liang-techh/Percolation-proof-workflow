---
kind: review_result
review_id: review-T-P5-244-source-ellipsoid-outward-sensitivity-guyuefangyuan-20260910T1224Z
task_id: T-P5-244-SOURCE-ELLIPSOID-OUTWARD-SENSITIVITY
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T12:24:00Z
claim_commit: 3bb374569bef43a81584500d6a6a220693adc4d3
inspected_commit: 8809186fac64cc11ec417bc0b20221176176f1f0
upstream_commits:
  - e8ba5dc69b700621893313a4202255a98267ebef  # T-P5-243 strict-margin coefficient-error budget
  - aa8124d17a0bfbed3572ed7cd3c20cdbe924964e  # T-P5-242 2D-fiber cubic S-lemma elimination
  - 56fdaebc2c0ca45fce1791923abb8311a54e14f9  # T-P5-240 quotient rank-one pivot transport
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_shifted_metric_ellipsoid_outer_inclusion; add_fixed_multiplier_source_radius_transfer; add_fraction_free_source_sensitivity_gate; add_joint_source_target_budget; preserve_source_domain_float64_and_admission_gates
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact quadratic-form algebra, Loewner comparison, inner-product Cauchy inequality, division-free discriminant elimination, exact 1D regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-244 — Source-ellipsoid outward sensitivity from a strict fixed-multiplier reserve

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-243 solved target-coefficient perturbations on a **fixed** ellipsoidal source. Its handoff explicitly left a separate seam: what happens when the source ellipsoid itself moves outward in metric/radius/center?

This child gives an exact comparison packet for that seam.

Starting from one regular fixed-multiplier S-lemma packet for the base source

`E(M,R) = { y : y^T M y <= R }`,

with vertical reserve

`epsilon = N/d > 0`,

we prove a global radial envelope

**`q(y) <= -epsilon + lambda (y^T M y - R)`**.

Now let the actual/perturbed source be

`E' = { y : (y-h)^T M' (y-h) <= R' }`

and suppose an exact Loewner comparison gives

**`M' - alpha M >= 0`, `alpha>0`.**

Then the complete effect of source motion is reduced to one base-metric radius inflation. Writing

`H = h^T M h`, `a = R'/alpha`,

the sharp geometric outer radius implied by this comparison is

`C_* = (sqrt(a)+sqrt(H))^2`.

A checker does **not** need square roots. A rational `C` certifies `E' subset {y:y^TMy<=C}` iff it satisfies the polynomial gate

`C-a-H >= 0`,

`(C-a-H)^2 >= 4 a H`.

Consequently the original target remains nonpositive on `E'` whenever

`lambda(C-R) <= epsilon`.

For `lambda>0` this can be eliminated to a single division-free source-sensitivity discriminant. Define

**`T = alpha N + d lambda ( alpha(R-H) - R' )`.**

Then the fixed-multiplier reserve proves safety on `E'` whenever

**`T >= 0`**

and

**`T^2 >= 4 alpha (d lambda)^2 R' H`.**

For `lambda=0`, the base packet is already globally safe and source-ellipsoid motion costs nothing.

The theorem is purely mathematical. No actual P5 source metric, center drift, radius enclosure, tube/cell/trajectory coverage, Float64 semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

# Part I — the fixed-multiplier packet gives a global radial envelope

## 1. Base regular S-lemma packet

Let `M in S_{++}^n`, `R>=0`, and

`q(y) = A + 2 l^T y + y^T G y`, `G=G^T`.

Fix `lambda>=0` and define

`K = lambda M - G`,

`c = -A-lambda R`,

`S_lambda = [[K,-l],[-l^T,c]]`.

Assume the regular branch

`K>0`.

As in T-P5-243, put

`d = det K >0`,

`J = adj(K)`,

`N = d c - l^T J l >0`,

`epsilon = N/d`.

Then

`S_lambda - epsilon e e^T >=0`,

where `e` is the final coordinate vector.

## 2. The global envelope

For every `y`, not merely `y in E(M,R)`,

`[y;1]^T (S_lambda-epsilon ee^T) [y;1] >=0`.

Expanding gives

`-q(y)-lambda(R-y^TMy)-epsilon >=0`.

Therefore:

**Theorem A — `fixedMultiplier_globalRadialEnvelope`.**

For every `y`,

**`q(y) <= -epsilon + lambda (y^T M y - R)`.**

This is the key source-sensitivity fact. The fixed S-lemma packet does more than prove safety on one ellipsoid: it gives a linear price, with slope `lambda`, for outward motion in the base metric.

### Immediate consequences

1. If a set `D` satisfies `y^TMy<=C` for every `y in D`, then

   `sup_D q <= -epsilon + lambda(C-R)`.

2. Hence `q<=0` on `D` whenever

   **`lambda(C-R)<=epsilon`.**

3. If `lambda=0`, then

   `q(y)<=-epsilon`

   globally. In that branch *any* source-domain enlargement is harmless as long as the target itself is unchanged.

This last branch should be explicit in a checker; dividing by `lambda` would incorrectly discard a particularly strong global certificate.

---

# Part II — exact outer inclusion for a shifted, shape-perturbed ellipsoid

## 3. Perturbed source

Let

`E' = { y : (y-h)^T M' (y-h) <= R' }`,

with `R'>=0`, and assume

`M' - alpha M >=0`,

for some exact `alpha>0`.

The base source has already been centered. Thus `h` is the center displacement relative to that normalized base center. This matches the centering discipline of T-P5-236.

For `y in E'`, write

`z = y-h`.

Then

`alpha z^T M z <= z^T M' z <= R'`.

Define

`a = R'/alpha`,

`H = h^T M h >=0`.

Hence

`z^T M z <= a`.

## 4. No-square-root inclusion gate

The base-metric radius of `y=z+h` is

`y^T M y = z^T M z + 2 z^T M h + H`.

By Cauchy-Schwarz in the `M` inner product,

`(z^T M h)^2 <= (z^T M z) H <= a H`.

Let `C` be any scalar satisfying

`C-a-H >=0`,

and

`(C-a-H)^2 >= 4 a H`.

Set `U=C-a-H`. Then `U>=0`. Since

`4(z^TMh)^2 <= 4aH <= U^2`,

we get

`2 |z^T M h| <= U`.

Therefore

`y^TMy`

`<= a + 2|z^TMh| + H`

`<= a+U+H`

`=C`.

Thus:

**Theorem B — `shiftedMetricEllipsoid_outerBaseRadius`.**

If

`M' >= alpha M`, `alpha>0`,

`R'>=0`,

`H=h^TMh`, `a=R'/alpha`,

and

`C-a-H>=0`,

`(C-a-H)^2>=4aH`,

then

**`E' subset { y : y^T M y <= C }`.**

No inverse, eigensystem, square root, or optimization is required by the certificate.

## 5. Geometric sharpness of the translation step

The polynomial gate is not merely a Young-inequality relaxation.

For fixed `M`, `a`, and `h`, the exact maximum over the base-metric ball is

`max_{z^TMz<=a} (z+h)^T M (z+h)`

`= a+H+2 sqrt(aH)`

`= (sqrt(a)+sqrt(H))^2`.

When `a>0` and `H>0`, equality is attained by taking `z` positively collinear with `h` in the `M` geometry. The zero cases are immediate.

Hence the two polynomial inequalities

`C-a-H>=0`,

`(C-a-H)^2>=4aH`

are exactly equivalent to `C` being at least this sharp translated-ball radius.

What may be conservative is only the earlier shape comparison `M'>=alpha M`: if `M'` is strictly stronger in relevant directions than the scalar factor `alpha M`, the true perturbed ellipsoid can be much smaller than the scalar outer ball.

---

# Part III — consume the Lyapunov reserve

## 6. Rational outer-radius packet

Combining Theorems A and B immediately gives:

**Theorem C — `sourceEllipsoid_outerRadiusReserveTransfer`.**

Under the base packet and the perturbed-source assumptions, if a scalar `C` satisfies

1. `C-a-H>=0`;
2. `(C-a-H)^2>=4aH`;
3. `lambda(C-R)<=epsilon`;

then

**`q(y)<=0` for every `y in E'`.**

Moreover the explicit remaining pointwise reserve is

**`epsilon_rem = epsilon-lambda(C-R)`.**

Whenever `epsilon_rem>0`, one has

`q(y)<=-epsilon_rem`

throughout `E'`.

This `C`-packet is useful for composition because all quantities can be rational and the remaining reserve stays explicit.

## 7. Fully division-free source sensitivity for `lambda>0`

For source-only safety one can eliminate `C` entirely.

The largest base-metric radius permitted by the fixed reserve is

`B = R + epsilon/lambda`

`= R + N/(d lambda)`.

Safety is proved whenever the translated outer radius is at most `B`, equivalently

`B-a-H>=0`,

`(B-a-H)^2>=4aH`.

Substitute `a=R'/alpha` and clear the positive denominator `alpha d lambda`.

Define

**`T := alpha N + d lambda ( alpha(R-H) - R' )`.**

Then

`B-a-H = T/(alpha d lambda)`.

Therefore:

**Theorem D — `sourceEllipsoid_fractionFreeSensitivity`.**

Assume `lambda>0`, `alpha>0`, `d>0`, `R'>=0`, `H>=0`. If

**`T>=0`**

and

**`T^2 >= 4 alpha (d lambda)^2 R' H`,**

then

**`q<=0` on `E'`.**

This gate contains no division and no square root. For rational matrices/scalars, every checker input remains rational except the already-existing exact PSD/PD witnesses.

### Same-center special case

If `h=0`, hence `H=0`, the discriminant disappears. The condition becomes simply

`alpha N + d lambda (alpha R-R') >=0`.

Equivalently

`R'/alpha - R <= epsilon/lambda`.

Thus a pure metric/radius outward perturbation pays exactly its scalar base-metric radius inflation against the fixed multiplier reserve.

### Pure-center special case

If `M'=M` and `R'=R`, so `alpha=1`, then

`T = N-d lambda H`.

The gate becomes

`N-dlambda H >=0`,

`(N-dlambda H)^2 >= 4(dlambda)^2 R H`.

This is the exact translated-ball comparison against the available fixed-multiplier radial budget.

---

# Part IV — joint source motion and target coefficient errors

## 8. Why the two perturbations should not be conflated

T-P5-243 charges coefficient errors on the original base ellipsoid. A source expansion changes the range of `y` on which those coefficient errors must be controlled.

Therefore the correct joint budget is **not** obtained by blindly adding the old T-P5-243 scalar with `R` unchanged.

Once Theorem B supplies a base-metric outer radius `C`, the coefficient-error packet must be evaluated on `y^TMy<=C`.

## 9. Target coefficient-error packet on the enlarged source

Let

`q_tilde(y)=q(y)+r(y)`,

where

`r(y)=Delta A+2 Delta l^T y+y^T Delta G y`.

Assume the same inverse-free metric packet as T-P5-243:

`Delta A<=a0`,

`gamma M-Delta G>=0`,

`M x=Delta l`,

`beta=Delta l^T x=x^TMx>=0`.

For every `theta>0`,

`2 Delta l^T y <= theta y^TMy + beta/theta`.

Hence for `y^TMy<=C`,

`r(y) <= a0 + (gamma+theta)C + beta/theta`.

Meanwhile Theorem A gives

`q(y) <= -epsilon + lambda(C-R)`.

Therefore:

**Theorem E — `jointSourceTargetPerturbation_budget`.**

If `E' subset {y:y^TMy<=C}` and there exists `theta>0` such that

**`lambda(C-R) + a0 + (gamma+theta)C + beta/theta <= epsilon`,**

then

**`q_tilde<=0` on `E'`.**

This is a direct pointwise proof; it does not require rerunning the T-P5-242 cubic partition and does not require transporting the T-P5-243 updated multiplier through a changed source metric.

## 10. Division-free joint discriminant

Define the residual numerator after source inflation, scalar error, and quadratic metric error:

**`E_C_num := N - d[ lambda(C-R) + a0 + gamma C ]`.**

Then the remaining Young inequality is

`d C theta^2 - E_C_num theta + d beta <=0`.

For `C>0` and `beta>0`, existence of `theta>0` is equivalent to

**`E_C_num>0`,**

**`E_C_num^2 >= 4 d^2 C beta`.**

Thus source movement and target coefficient error admit one compositional certificate:

1. certify the perturbed source lies in the base-metric ball of radius `C`;
2. compute the source charge `lambda(C-R)`;
3. charge scalar/quadratic coefficient errors on that same radius `C`;
4. use the above discriminant for the remaining linear error.

When `beta=0`, the linear error vanishes. Then no positive Young parameter is intrinsically needed; the sharp direct condition is simply

`lambda(C-R)+a0+gamma C <= epsilon`.

A checker should keep this zero-linear-error branch separate instead of introducing an artificial positive `theta` cost.

---

# Part V — exact regressions and obstructions

## 11. Regression A: center drift can genuinely destroy safety

Take one dimension with

`M=1`, `R=1`,

`q(y)=y^2-3`.

Choose `lambda=2`. Then

`K=lambda M-G = 1`,

`c=-A-lambda R = 3-2=1`,

`d=1`, `N=1`, `epsilon=1`.

Thus the base source `|y|<=1` has a strict fixed-multiplier packet.

Now keep the metric/radius unchanged but shift the source center by `h=1`:

`E'={y:(y-1)^2<=1}=[0,2]`.

At `y=2`,

`q(2)=1>0`.

The source-sensitivity gate correctly refuses this perturbation. Here `alpha=1`, `R'=1`, `H=1`, so

`T = 1 + 2[(1-1)-1] = -1 <0`.

This shows source motion is not a bookkeeping issue: even when the target coefficients are unchanged, the old source certificate can fail on the moved domain.

## 12. Regression B: metric weakening can also expose a violating state

Keep the same base packet, set `h=0`, `R'=1`, and weaken the source metric to

`M'=(1/4)M`.

Then `alpha=1/4` and

`E'={y:y^2/4<=1}=[-2,2]`.

Again `q(2)=1>0`.

The same-center scalar gate gives

`alpha N+d lambda(alpha R-R')`

`=1/4+2(1/4-1)`

`=-5/4<0`.

So metric shrinkage is correctly charged as outward base-radius inflation.

## 13. Regression C: `lambda=0` is globally source-invariant

Take

`M=1`, any `R>=0`,

`q(y)=-1-y^2`.

At `lambda=0`,

`K=-G=1>0`,

`c=-A=1`,

`epsilon=1`.

Theorem A is simply

`q(y)<=-1`

for every real `y`.

Hence no center/radius/metric perturbation of the source can destroy safety while the target remains unchanged. This is why a source-sensitivity implementation must not divide by `lambda` before branching on `lambda=0`.

## 14. Failure of the comparison gate is not automatically a physical FAIL

Theorem D uses two compressions:

1. replace the full matrix relation between `M'` and `M` by one scalar lower factor `alpha`;
2. replace the actual target by the global radial envelope from one fixed multiplier.

Either step can be conservative.

Therefore failure of

`T>=0` or `T^2>=4 alpha(dlambda)^2R'H`

means only:

**the current fixed-multiplier + scalar-metric-comparison packet does not prove safety.**

It does **not** imply that the perturbed source contains a state with `q>0`.

A genuine FAIL requires an actual admissible `y` from the same source/domain semantics with `q(y)>0` (or an equivalent exact violating witness).

This fail-open distinction should remain explicit in any source-facing consumer.

---

# Part VI — theorem decomposition for Lean

The first formalization should remain finite-dimensional and avoid matrix square roots.

Suggested leaves:

1. `fixedMultiplier_globalRadialEnvelope`

   From `S_lambda - epsilon ee^T >=0`, derive

   `q y <= -epsilon + lambda * (quad M y - R)`.

2. `loewnerLower_mem_shiftedEllipsoid_imp_baseRadius`

   From `M' - alpha M >=0`, `alpha>0`, and

   `(y-h)^T M' (y-h)<=R'`, derive

   `(y-h)^T M (y-h)<=R'/alpha`.

3. `innerProduct_shift_radius_of_squareGate`

   If `z^TMz<=a`, `H=h^TMh`,

   `U>=0`, `U^2>=4aH`, then

   `(z+h)^TM(z+h)<=a+H+U`.

   This is the no-square-root core.

4. `shiftedMetricEllipsoid_outerBaseRadius`

   Combine leaves 2 and 3.

5. `sourceEllipsoid_outerRadiusReserveTransfer`

   Combine the outer-radius result with leaf 1.

6. `sourceEllipsoid_fractionFreeSensitivity`

   For `lambda>0`, clear denominators and prove the `T`/discriminant form.

7. `fixedMultiplier_zero_sourceInvariant`

   Separate the `lambda=0` global branch.

8. `jointSourceTargetPerturbation_budget`

   Reuse the T-P5-243 metric completed-square leaf but evaluate it at the enlarged radius `C`.

9. `jointSourceTargetPerturbation_discriminant`

   Clear denominators in the final Young-parameter quadratic.

No pseudoinverse, eigenvector, `Real.sqrt`, or generic optimizer is required for the soundness direction. The geometric sharpness theorem may be added later and can use an explicit collinear witness.

---

# Part VII — source-facing packet and remaining obligations

A real consumer should request one same-key packet containing:

- base `M,R,A,l,G,lambda,d,N` and the already-accepted exact algebraic identities;
- perturbed source `M',R',h` in the same centered quotient coordinates;
- `alpha>0` plus an exact PSD witness for `M'-alpha M`;
- either a rational outer radius `C` satisfying the square gate, or the direct fraction-free `T` gate;
- if target coefficients also move, the T-P5-243-style `Delta A,Delta l,Delta G,a0,gamma,x,beta` packet evaluated against the enlarged radius `C`.

Still OPEN and deliberately not claimed here:

1. actual P5 source extraction of `M',R',h`;
2. proof that base and perturbed source packets use the same quotient basis / same normalization / same center convention;
3. exact PSD witness for a useful `alpha` on the intended cell/tube;
4. trajectory/tube/cell/FD-halo/graph-lift coverage;
5. Float64/interval enclosure of the source perturbation;
6. Lean compilation and kernel/axiom receipt;
7. 封不觉 independent validation;
8. admission/registry mutation and parent closure.

## Recommended next mathematical seam

After this child, the next genuinely distinct source-sensitivity problem is **anisotropic source perturbation without collapsing `M'` to one scalar factor `alpha M`**. The natural target is an exact generalized trust-region comparison that can exploit directional margin of the fixed S-lemma block, while still remaining fraction-free on rational data. That should only be pursued if a real source packet shows the scalar `alpha` comparison is too conservative.

Until then, the current theorem is the minimal robust bridge from a strict rational Lyapunov reserve to source-domain motion.
