---
kind: review_result
review_id: review-T-P5-243-strict-margin-coefficient-error-budget-liuguanyi-20260910T1208Z
task_id: T-P5-243-STRICT-MARGIN-COEFFICIENT-ERROR-BUDGET
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T12:08:00Z
claim_commit: 85a45be9a3b374f4f0836b1f66887806a37c7511
inspected_commit: 5fb084ea18cfc53e895912f734bacd5dff23e6b7
upstream_commits:
  - aa8124d17a0bfbed3572ed7cd3c20cdbe924964e  # T-P5-242 two-dimensional fiber cubic S-lemma elimination
  - 73e5febae1d3ac2733d7bdea067fc244e2f551d1  # corrected T-P5-239 rank-one two-cap fiber/secular bridge
  - 56fdaebc2c0ca45fce1791923abb8311a54e14f9  # T-P5-240 quotient rank-one pivot transport
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_fixed_multiplier_vertical_reserve; add_metric_coefficient_error_packet; add_psd_reserve_transfer; add_division_free_discriminant_budget; add_congruence_invariance; preserve_source_domain_float64_and_admission_gates
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact block-matrix algebra, metric completed square, adjugate Schur slack, rational discriminant analysis, exact rational regression; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-243 — Strict-margin coefficient-error budget from one fixed S-lemma multiplier

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-242 leaves a practical strict-margin seam: once a rational regular S-lemma multiplier has already certified one ellipsoidal fiber, a source/support solver should be told how much outward coefficient error in `A,l,G` can be tolerated **without rerunning the cubic multiplier/root partition**.

This child gives an exact answer in a source metric.

The core result is a PSD reserve-transfer identity. A fixed regular base multiplier gives an explicit vertical Lyapunov reserve

`epsilon = N/d`,

where `d=det(lambda M-G)` and `N` is the fraction-free Schur numerator. A perturbation packet is summarized by

- a one-sided scalar error `Delta A <= a`;
- a one-sided metric quadratic error `Delta G <= gamma M` in Loewner order;
- an inverse-free dual-energy witness `M x = Delta l`, `beta = Delta l^T x`.

For any `theta>0`, the perturbation consumes exactly the explicit budget

`eta(theta)=a+(gamma+theta)R+beta/theta`.

If `eta(theta)<=epsilon`, then the perturbed target has an explicit S-lemma certificate at the updated multiplier

**`lambda' = lambda + gamma + theta`.**

No cubic root, eigensystem, optimizer, or re-partition is needed.

Moreover, existence of such a `theta` is decided by one **division-free discriminant**. For rational data the witness `theta` can itself be chosen rational, including the equality case. The whole transfer is invariant under exact quotient-basis congruence.

No actual P5 source pair, FD/DH coefficient enclosure, tube/cell/trajectory coverage, Float64 execution semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

# Part I — fixed-multiplier vertical reserve

## 1. Base ellipsoidal fiber

Let

`M in S_{++}^n`, `R>0`,

and define the source ellipsoid

`E := { y : y^T M y <= R }`.

Let the affine-quadratic Lyapunov debit be

`q(y) := A + 2 l^T y + y^T G y`,

with `G=G^T`.

Fix one multiplier `lambda>=0` and put

`K := lambda M-G`,

`c := -A-lambda R`,

`S_lambda := [[K,-l],[-l^T,c]]`.

For every `y`,

`[y;1]^T S_lambda [y;1]`

`= -q(y)-lambda(R-y^T M y)`.

Hence `S_lambda>=0` implies `q<=0` on `E`.

The strict regular branch used here assumes

**`K>0`.**

This is exactly the branch T-P5-242 says can be chosen with a rational multiplier whenever a rational-data target has a strict compact safety margin.

## 2. Fraction-free Schur reserve

Set

`d := det K > 0`,

`J := adj(K)`,

and

**`N := d*c - l^T J l`.**

Assume

**`N>0`.**

Since `K^{-1}=J/d`, define

`epsilon := N/d`

`= c-l^T K^{-1}l >0`.

Then

**Theorem A — `fixedMultiplier_verticalReserve`.**

`S_lambda - epsilon e e^T >=0`, where `e` is the last coordinate vector. Consequently

**`q(y) <= -epsilon` for every `y in E`.**

### Proof

The top-left block is `K>0`. Its Schur complement in

`S_lambda-epsilon e e^T`

is

`c-epsilon-l^T K^{-1}l = 0`.

Therefore the block matrix is PSD. For `y in E`,

`-q(y)-lambda(R-y^TMy)-epsilon >=0`.

Because `lambda>=0` and `R-y^TMy>=0`,

`q(y)<=-epsilon`.

QED.

### Why `N` is the useful trusted quantity

For rational `K,l,c`, both `d` and `N` are rational and require no inverse. A checker only needs an exact PD witness for `K`, the adjugate identity, and the scalar sign `N>0`.

The reserve comparison below can be cleared of the remaining division by `d` entirely.

---

# Part II — inverse-free metric packet for coefficient errors

## 3. Perturbed target

Let

`q_tilde(y) = q(y) + r(y)`,

where

`r(y) := Delta A + 2 Delta l^T y + y^T Delta G y`,

and `Delta G` is symmetric.

Assume a source/error producer supplies exact scalars `a>=0`, `gamma>=0`, a vector `x`, and a scalar `beta` satisfying

1. **scalar one-sided enclosure**

   `Delta A <= a`;

2. **quadratic one-sided metric enclosure**

   `gamma M-Delta G >=0`;

3. **linear dual-energy witness**

   `M x = Delta l`;

4. **dual-energy identity**

   `beta = Delta l^T x`.

Because `M>0` and `M x=Delta l`,

`beta=x^T M x>=0`,

and `beta=0` iff `Delta l=0`.

No inverse or square root appears in this packet.

## 4. Exact metric completed square

For every `theta>0`, every `y`, and every scalar `s`,

`theta y^T M y - 2 s Delta l^T y + (beta/theta)s^2`

`= theta (y-(s/theta)x)^T M (y-(s/theta)x) >=0`.

Taking `s=1` gives

`2 Delta l^T y <= theta y^T M y + beta/theta`.

Together with the one-sided scalar and quadratic bounds,

`r(y)`

`<= a + (gamma+theta)y^T M y + beta/theta`.

Therefore on the source ellipsoid,

**`r(y) <= eta(theta)`**, where

**`eta(theta) := a+(gamma+theta)R+beta/theta`.**

This is the natural coefficient-error debit measured in the same metric as the source cap.

## 5. Perturbation S-lemma block without invoking the S-lemma

Define

`tau := gamma+theta`,

and

`T_theta := [[tau M-Delta G, -Delta l],[-Delta l^T, eta(theta)-Delta A-tau R]]`.

Because

`eta(theta)-Delta A-tau R`

`= (a-Delta A)+beta/theta`,

we have the exact decomposition

`T_theta`

`= [[gamma M-Delta G,0],[0,a-Delta A]]`

`  + [[theta M,-Delta l],[-Delta l^T,beta/theta]]`.

The first summand is PSD by assumptions 1–2. The second summand is PSD by the completed-square identity above. Hence

**`T_theta>=0`.**

Equivalently, this is a direct exact certificate that

`r(y)<=eta(theta)` on `E`.

No appeal to a numerical trust-region solver is needed.

---

# Part III — PSD reserve transfer and updated multiplier

## 6. Main composition theorem

Assume the base packet of Part I and perturbation packet of Part II. If some `theta>0` satisfies

**`eta(theta) <= epsilon`,**

then put

**`lambda' := lambda+gamma+theta`.**

Define the perturbed S-lemma block

`S_tilde(lambda')`

`:= [[lambda' M-(G+Delta G), -(l+Delta l)],`

`    [-(l+Delta l)^T, -(A+Delta A)-lambda' R]]`.

Then

**Theorem B — `coefficientError_reserveTransfer`.**

`S_tilde(lambda')>=0`.

Hence

**`q_tilde(y)<=0` for every `y^TMy<=R`.**

### Exact PSD identity

Let `E0=e e^T` on the final homogeneous coordinate. Then

`S_tilde(lambda')`

`= (S_lambda-epsilon E0)`

`  + [[gamma M-Delta G,0],[0,a-Delta A]]`

`  + [[theta M,-Delta l],[-Delta l^T,beta/theta]]`

`  + (epsilon-eta(theta)) E0`.

Every summand is PSD.

This is stronger than merely bounding the perturbed objective pointwise: it constructs the **new certificate matrix and the new multiplier explicitly**.

### Interface consequence

A source/support solver that perturbs `A,l,G` does not need to rerun T-P5-242's cubic partition. It may consume a previously frozen regular multiplier `lambda`, submit `(a,gamma,x,beta,theta)`, and the checker updates the multiplier by the scalar rule

`lambda' = lambda+gamma+theta`.

---

# Part IV — division-free admissible-error gate

## 7. Clear the base denominator

Recall

`epsilon=N/d`.

Define the remaining reserve after scalar and quadratic errors by

**`E_num := N - d(a+gamma R)`.**

For `theta>0`, the gate `eta(theta)<=epsilon` is equivalent to

`a+gamma R+theta R+beta/theta <= N/d`.

Multiplying by the positive `d*theta` gives the completely division-free quadratic inequality

**`d R theta^2 - E_num theta + d beta <= 0`.**

Thus a producer may simply submit a rational `theta>0` and the checker evaluates this polynomial inequality exactly.

## 8. Eliminate `theta`: square-free discriminant gate

Assume `beta>0`. Because `d>0` and `R>0`, the quadratic in `theta` opens upward and has positive constant term.

There exists a real `theta>0` satisfying the budget iff

**`E_num>0`**

and

**`Delta_budget := E_num^2 - 4 d^2 R beta >=0`.**

This is a root-free, square-root-free exact criterion.

### Proof

The roots, when real, have product

`beta/R>0`

and sum

`E_num/(dR)`.

Therefore both roots are positive exactly when `E_num>0`. A feasible interval exists exactly when the discriminant is nonnegative.

QED.

## 9. Zero-linear-error branch

If `beta=0`, then positive definiteness of `M` implies `Delta l=0`.

In that case the Young block is unnecessary. One may set

`tau=gamma`

and use only

`[[gamma M-Delta G,0],[0,a-Delta A]]>=0`.

The exact budget gate reduces to

**`E_num>=0`.**

If `E_num>0`, one may also choose any sufficiently small rational `theta>0`; if `E_num=0`, use the zero-cross branch directly rather than introducing an artificial positive `theta`.

## 10. Rational witness theorem

Suppose all base and error-packet data are rational.

If `beta>0`, `E_num>0`, and `Delta_budget>=0`, then there exists a **rational** `theta>0` satisfying the division-free quadratic gate.

- If `Delta_budget>0`, the feasible root interval has nonempty interior; choose any rational point inside it.
- If `Delta_budget=0`, the unique root is

  `theta = E_num/(2 d R)`,

  which is rational.

Therefore the updated multiplier

`lambda'=lambda+gamma+theta`

can remain rational even at the sharp boundary of this error-summary budget.

This is useful operationally: strict source rounding/error budgets do not force the checker into the ordered quadratic extension used by T-P5-242's exact cubic-boundary classifier.

---

# Part V — sharpness of the `(a,gamma,beta)` summary

## 11. Information-theoretic worst case

The metric completed square implies

`sup_{y^TMy<=R} 2 Delta l^T y = 2 sqrt(R beta)`.

Indeed, if `beta>0`, equality is attained by

`y_* = sqrt(R/beta) x`,

because

`y_*^T M y_* = R`

and

`Delta l^T y_* = sqrt(R beta)`.

If only the summary facts

`Delta A<=a`, `Delta G<=gamma M`, `M x=Delta l`, `beta=Delta l^T x`

are retained, then the worst admissible perturbation can saturate all three bounds simultaneously:

`Delta A=a`, `Delta G=gamma M`, and the above `Delta l` direction.

Its maximum perturbation debit is exactly

**`a+gamma R+2 sqrt(R beta)`.**

Hence the error-summary threshold is sharp: no theorem using only `(a,gamma,beta)` can guarantee a smaller universal debit.

The square-free discriminant condition is exactly the rationalized form of

`epsilon >= a+gamma R+2 sqrt(R beta)`.

### Important failure semantics

If `Delta_budget<0`, the **summary packet is insufficient for universal PASS**. This is not automatically a mathematical FAIL for the actual perturbation unless an actual reachable `y` and actual coefficients realize a violating direction. A narrower source-correlated perturbation may still be safe.

This distinction should remain explicit in the dispatcher.

---

# Part VI — quotient/chart invariance

## 12. Exact congruence transport

Let `y=T z` with invertible exact `T`. Transport

`M' = T^T M T`,

`G' = T^T G T`,

`Delta G' = T^T Delta G T`,

`l'=T^T l`,

`Delta l'=T^T Delta l`.

If `M x=Delta l`, define

`x' := T^{-1}x`.

Then

`M' x' = Delta l'`,

and

`beta' = Delta l'^T x' = beta`.

Also

`gamma M'-Delta G' = T^T(gamma M-Delta G)T`,

so the Loewner error gate is preserved.

For the base regular block,

`K'=T^T K T`.

Hence

`d' = det(T)^2 d`.

The vertical Schur reserve itself is invariant:

`epsilon' = c-l'^T K'^{-1}l' = epsilon`.

Consequently

`N' = d' epsilon = det(T)^2 N`,

and

`E_num' = det(T)^2 E_num`.

Therefore

`Delta_budget'`

`= E_num'^2 - 4 d'^2 R beta'`

`= det(T)^4 Delta_budget`.

Thus the signs of `E_num` and `Delta_budget`, the dual energy `beta`, the admissible-error decision, and the physical reserve `epsilon` are all exact quotient/chart invariants.

**Theorem C — `coefficientErrorBudget_congruenceInvariant`.**

The T-P5-243 budget may be checked in any exact quotient basis. No whitening, orthonormal basis, or floating eigenvectors are mathematically privileged.

This is the adapter-facing bridge needed to connect T-P5-240's quotient transport to T-P5-242's fixed fiber certificate.

---

# Part VII — exact rational regression

## 13. Base strict certificate inherited from the T-P5-242 tangent example

Take

`M=I_2`, `R=1`,

`G=diag(1,0)`,

`l=(1/4,0)`,

`A=-8/5`.

Use the rational multiplier

`lambda=5/4`.

Then

`K=diag(1/4,5/4)`,

`d=5/16`,

`J=diag(5/4,1/4)`,

`c=7/20`.

Moreover

`l^T J l = 5/64`,

so

`N = d c-l^T J l`

`= 7/64-5/64`

`= 1/32`.

Therefore

**`epsilon=N/d=1/10`.**

The true base maximum is indeed `-1/10`, attained at `(1,0)`.

## 14. Rational coefficient perturbation

Take

`Delta A=1/100`,

`Delta G=(1/100) I_2`,

`Delta l=(1/100,0)`.

Choose the exact summary

`a=1/100`,

`gamma=1/100`,

`x=(1/100,0)`,

`beta=1/10000`.

Then

`M x=Delta l`,

`gamma M-Delta G=0`.

The remaining fraction-free reserve is

`E_num`

`= 1/32 - (5/16)(1/100+1/100)`

`= 1/40`.

The square-free budget discriminant is

`Delta_budget`

`= (1/40)^2 - 4(5/16)^2(1)(1/10000)`

`= 3/5120 >0`.

Choose the rational Young parameter

`theta=1/100`.

Then

`eta(theta)`

`= 1/100 + (1/100+1/100) + (1/10000)/(1/100)`

`= 1/25 < 1/10 = epsilon`.

The updated multiplier is

**`lambda'=127/100`.**

The perturbed target is

`q_tilde(x,y)`

`= -159/100 + (13/25)x + (101/100)x^2 + (1/100)y^2`.

Its exact certificate block is

`S_tilde(127/100)`

`= [[13/50, 0, -13/50],`

`   [0, 63/50, 0],`

`   [-13/50, 0, 8/25]]`.

The nontrivial `2x2` principal determinant is

`(13/50)(8/25)-(13/50)^2 = 39/2500>0`,

so the block is positive definite.

On the unit disk the true maximum occurs at `(1,0)` and equals

`-159/100 + 52/100 + 101/100 = -3/50`.

This exactly equals the base margin `-1/10` plus the worst perturbation debit `1/25`; the transfer has not hidden a sign error.

## 15. Saturating obstruction example

Keep the same base packet but take

`Delta A=0`, `Delta G=0`, `Delta l=(1/10,0)`.

Then `beta=1/100`, while the base reserve is only `epsilon=1/10`.

The summary worst-case debit is

`2 sqrt(R beta)=1/5 > 1/10`.

At the actual reachable point `(1,0)`, the base target equals `-1/10` and the perturbation contributes `+1/5`, so

`q_tilde(1,0)=+1/10>0`.

Thus the discriminant obstruction can correspond to a genuine Lyapunov failure, not merely a proof artifact. The dispatcher must nevertheless distinguish this explicit witness from the generic `summary insufficient` case of Part V.

---

# Part VIII — suggested formal interface

## 16. Minimal theorem statements

Suggested theorem/interface names:

- `fixedMultiplier_verticalReserve`
- `metricLinearError_completedSquare`
- `metricCoefficientError_psdPacket`
- `coefficientError_reserveTransfer`
- `coefficientErrorBudget_divisionFree`
- `coefficientErrorBudget_discriminantIff`
- `coefficientErrorBudget_rationalTheta`
- `coefficientErrorBudget_congruenceInvariant`

A minimal trusted packet can avoid matrix inverses entirely:

1. base `lambda`, `K`, `d`, `J`, `N`;
2. exact proof/check that `K>0`, `K*J=d I`, and `N=d*c-l^T J l>0`;
3. perturbation `a,gamma,x,beta` with `Delta A<=a`, `gamma M-Delta G>=0`, `M x=Delta l`, `beta=Delta l^T x`;
4. either a rational `theta>0` satisfying

   `d R theta^2-E_num theta+d beta<=0`,

   or the square-free existence gate plus a generated rational witness;
5. updated multiplier `lambda'=lambda+gamma+theta`.

The checker may optionally verify the final `S_tilde(lambda')>=0` as a redundant regression, but the decomposition theorem makes that full recomputation mathematically unnecessary.

## 17. Dependencies

This child uses only:

- T-P5-242's existence/use of a regular fixed S-lemma certificate in the strict-margin branch;
- T-P5-240's exact quotient-congruence viewpoint;
- elementary Schur-complement/adjugate algebra;
- a one-line `M`-metric completed square;
- scalar quadratic discriminant arithmetic.

It does not consume provenance receipts, admission state, or Lean compilation.

## 18. Failure / non-applicability boundary

This theorem must fail closed or route elsewhere when:

1. `M` is not positive definite. Then the dual-energy witness may have kernel/range obstructions and the source fiber may be noncompact; route to the earlier semidefinite kernel machinery.
2. `R<=0`. `R=0` is the singleton fiber and should use the trivial point check; `R<0` is source-feasibility logic.
3. the chosen base multiplier has singular `K`. The strict branch should first move to a regular multiplier as in T-P5-242; do not divide by `det K=0`.
4. coefficient errors are not expressed in the **same centered quotient coordinates and same source branch** as the base certificate.
5. `Delta G<=gamma M` or `Delta A<=a` is inferred from samples rather than an exact/interval source bound.
6. only an outer summary `(a,gamma,beta)` is known and the discriminant gate fails. This is `INCONCLUSIVE_FROM_SUMMARY`, not an actual FAIL unless a concrete violating source/reachable witness is supplied.
7. the perturbation changes the source cap `M,R`, the common center, equality constraints, or the outer rank-one branch itself. Those are domain/geometry perturbations, not target-coefficient perturbations and require a separate bridge.
8. Float64/FD/DH rounding has not been outwardly enclosed into exact `Delta A,Delta l,Delta G`; decimal optimizer output is not an exact packet.

## 19. Structural fingerprint

The new reusable fingerprint is

**strict regular S-lemma certificate -> fraction-free vertical Schur reserve -> one-sided metric coefficient-error packet -> inverse-free dual-energy completed square -> PSD reserve sum -> explicit updated multiplier -> division-free scalar quadratic -> square-free discriminant budget.**

It converts T-P5-242 from an exact classifier into a robust, compositional certificate consumer.

## 20. What remains open

Still open and not claimed here:

- actual same-key P5 extraction of `Delta A,Delta l,Delta G` from support-cap rounding or FD/DH remainder budgets;
- exact proof of a source-specific `gamma M-Delta G>=0` and `Delta A<=a`;
- actual quotient/common-center/source-cap identity from T-P5-239/240;
- cell/tube/trajectory coverage and branch coverage;
- perturbations of `M,R`, equality constraints, or the source center;
- Float64/interval coefficient enclosure;
- Lean/kernel formalization and independent validation by 封不觉;
- admission, registry mutation, or any P5/P8/M4 parent closure.

## 21. Next smallest mathematical seam

The next source-facing seam is to turn an actual FD/DH/support rounding packet into the exact one-sided metric summaries used here:

`Delta A<=a`, `Delta G<=gamma M`, `M x=Delta l`, `beta=Delta l^T x`.

The next non-source-facing extension is **domain/cap sensitivity**: allow simultaneous outward perturbation of the source ellipsoid `(M,R)` and prove a reserve-transfer theorem that distinguishes target-coefficient debit from domain enlargement. That extension should not be merged into the present theorem because changing the source cap also changes the multiplier penalty itself.