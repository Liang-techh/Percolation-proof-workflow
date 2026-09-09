---
kind: review_result
review_id: review-T-P5-140-multiplier-secant-optimization-honglianmozun-20260909T0908Z
task_id: T-P5-140-MULTIPLIER-SECANT-OPTIMIZATION
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T09:08:00Z
claim_commit: 38881c551dfa34f6d79045c78b26645d1013ab0e
inspected_commit: 64053c293ca65d118ed7cee07972ea40d86400c1
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-137-ELLIPSOIDAL-KNOT-RESET-MULTIPLIER-honglianmozun-20260909T0811Z.md
    commit: f4212a7463a782d219e0ee2dbcbba06f4c04b8b5
  - path: agent_review_inbox/review-T-P5-138-RANKONE-SCHUR-RESET-DECOMPOSITION-guyuefangyuan-20260909T0824Z.md
    commit: 2a86f55903249300cd2bde81f678f1e34f7493f1
  - path: agent_review_inbox/review-T-P5-139-RANGE-SOLVE-SCHUR-RESET-kuangmanmozun-20260909T0834Z.md
    commit: f0198916eb5fe1783cbeb9055031c9d9bd0dc954
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: use exact cross-metric secants to search the S-procedure multiplier; if an exact stationary range-solve witness satisfies y_star^T G y_star=4R, certify global optimality and the sharp physical contact point without inverse/sqrt; otherwise retain rational bracketing and singular hard-case boundary explicitly
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic-form algebra only
exit_code: n/a
---

# T-P5-140 — exact secant optimization of the ellipsoidal knot-reset multiplier

## 0. Narrow seam and non-overlap

T-P5-137 established the ellipsoidal reset multiplier certificate for

`W_+ - kappa W_- <= b^T x - x^T H x + C`,

on the physical cell

`x^T G x <= R`,

with `G>0`, by choosing `tau>=0` and requiring the augmented block built from

`K_tau := H + tau G`

and `E-C-tau R` to be PSD.

T-P5-138 converted the fixed-`tau` augmented block into a singular-safe rank-one domination condition. T-P5-139 then removed that rank-one PSD test whenever the producer supplies an exact range solve

`K_tau y_tau = b`.

For such a fixed multiplier the sharp block-certificate floor is characterized by

`4(E_tau-C-tau R) = b^T y_tau`.

The remaining mathematical seam is no longer the fixed-`tau` Schur algebra. It is:

> how should `tau` itself be chosen, and can the choice be certified without inverses, square roots, eigenvalue differentiation, or a black-box one-dimensional optimizer?

This child answers that seam with an exact **two-multiplier secant identity**. It preserves the cross-metric cancellation between two exact range solves and yields:

1. an exact sign test for whether increasing `tau` improves the sharp reset floor;
2. a division-free discrete convexity theorem;
3. an exact stationary-witness theorem giving the global best multiplier;
4. a quadratic gap identity to every other feasible multiplier;
5. an explicit physical contact state showing sharpness in the non-hard case;
6. a rational bracketing rule when the exact optimum is algebraic or otherwise unavailable.

No source binding, actual controller/reference extraction, coverage, Float64 semantics, Lean/kernel receipt, provenance/admission audit, registry promotion, P8 flowpipe, or P5/M4 parent closure is claimed.

---

## 1. Setup: the sharp fixed-multiplier floor

Work in a finite-dimensional real vector space. Let

- `G` be symmetric positive definite;
- `H` be symmetric;
- `b` be a fixed vector/covector under the chosen Euclidean pairing;
- `R>=0` be the ellipsoid level;
- `C` be the constant reset term.

For a multiplier `tau`, define

**(1.1)** `K_tau := H + tau G`.

Call `tau` **range-feasible** when

**(1.2)** `K_tau >= 0`

and there exists a vector `y_tau` such that

**(1.3)** `K_tau y_tau = b`.

By T-P5-139 the scalar

**(1.4)** `q_tau := b^T y_tau`

is independent of the chosen solution even when `K_tau` is singular. The sharp fixed-`tau` block floor is therefore

**(1.5)** `E_tau := C + tau R + q_tau/4`.

The trusted checker does not need to divide by four; it can retain

**(1.6)** `4(E_tau-C-tau R)=q_tau`.

The purpose of the next sections is to compare `E_tau` at different multipliers without ever introducing `K_tau^{-1}`.

---

## 2. Main identity: two exact range solves determine the floor secant

Take two range-feasible multipliers

`tau_1 < tau_2`

and write

`d := tau_2 - tau_1 > 0`,

`K_i := H + tau_i G`,

`K_i y_i = b`,

`q_i := b^T y_i`,

`s_i := y_i^T G y_i`,

`c_12 := y_1^T G y_2`.

### Theorem A — exact range-solve secant identity

One has

**(2.1)** `q_1 - q_2 = d c_12`.

Consequently the sharp floors satisfy

**(2.2)**

`4(E_2-E_1) = d (4R-c_12)`.

### Proof

Because `K_2=K_1+dG`, symmetry gives

`q_1 = b^T y_1`

`    = y_2^T K_2 y_1`

`    = y_2^T K_1 y_1 + d y_2^T G y_1`

`    = y_2^T b + d c_12`

`    = q_2 + d c_12`.

This proves (2.1). Then

`4(E_2-E_1)`

` = 4dR + q_2-q_1`

` = d(4R-c_12)`.

No inverse, generalized inverse, determinant, eigenvalue, derivative, square root, or optimization routine appears.

### Immediate decision rule

Since `d>0`, the sign of the floor change is exactly the sign of `4R-c_12`:

- if `c_12 > 4R`, then `E_2 < E_1` and increasing the multiplier improved the reset budget;
- if `c_12 = 4R`, then `E_2 = E_1`;
- if `c_12 < 4R`, then `E_2 > E_1` and the larger multiplier is worse.

Thus a producer that already computes exact rational solves at two rational candidate multipliers can compare the candidates using one exact cross quadratic form.

---

## 3. Cross-metric sandwich: the secant has an exact energy interpretation

Let

`z := y_1-y_2`.

From the two solve equations,

**(3.1)** `K_1 z = d G y_2`,

and

**(3.2)** `K_2 z = d G y_1`.

Therefore

`z^T K_1 z = d z^T G y_2 = d(c_12-s_2)`,

and

`z^T K_2 z = d z^T G y_1 = d(s_1-c_12)`.

Hence the exact identities

**(3.3)** `d(c_12-s_2) = z^T K_1 z`,

**(3.4)** `d(s_1-c_12) = z^T K_2 z`.

Because both shifted curvatures are PSD,

**(3.5)** `s_2 <= c_12 <= s_1`.

This is stronger than a generic Cauchy estimate: the cross term is not merely bounded by endpoint norms; its two gaps are exactly the energies of the solve difference in the two shifted-curvature metrics.

### Consequence: monotonicity of the metric solve norm

For any two feasible multipliers with `tau_1<tau_2`,

**(3.6)** `s_2 <= s_1`.

So `s_tau = y_tau^T G y_tau` is monotone nonincreasing along the feasible multiplier direction.

If `G>0`, `K_1>=0`, and `tau_2>tau_1`, then

`K_2 = K_1 + dG >0`.

Thus every multiplier strictly to the right of a feasible one has positive-definite shifted curvature and a unique solve. In the nonzero-`b` case the decrease is strict away from singular degeneracies because `y_1=y_2` would imply `dGy_1=0`, hence `y_1=0` and therefore `b=0`.

### Singular solution choice does not corrupt the secant

At a singular feasible left endpoint, `y_1` need not be unique. Nevertheless `q_1` is solution-independent by T-P5-139, so (2.1) shows that

**(3.7)** `c_12 = (q_1-q_2)/d`

is also solution-independent. Equivalently, if `n in ker K_1`, then

`n^T G y_2 = 0`,

because `d G y_2 = K_1(y_1-y_2)` lies in the range of `K_1`, orthogonal to its kernel.

This matters for a checker: the two-point floor comparison remains canonical even when the left range solve itself is nonunique.

---

## 4. Discrete convexity without calculus

Take three range-feasible multipliers

`tau_0 < tau_1 < tau_2`

with exact solves `y_0,y_1,y_2`. Define

`d_01=tau_1-tau_0`,

`d_12=tau_2-tau_1`,

`c_01=y_0^T G y_1`,

`c_12=y_1^T G y_2`,

`s_1=y_1^T G y_1`.

By the cross sandwich,

**(4.1)** `c_01 >= s_1 >= c_12`.

The secant identity gives

`4(E_1-E_0)/d_01 = 4R-c_01`,

`4(E_2-E_1)/d_12 = 4R-c_12`.

Hence the secant slopes are ordered:

**(4.2)**

`(E_1-E_0)/d_01 <= (E_2-E_1)/d_12`.

A division-free checker can use the equivalent polynomial inequality

**(4.3)**

`d_12 (E_1-E_0) <= d_01 (E_2-E_1)`.

Thus the sharp multiplier floor is discretely convex on the range-feasible set, proved entirely by solve equalities and PSD quadratic forms rather than differentiation of a matrix inverse.

This is the useful search fact: once a secant turns positive, all later secants cannot turn negative again; once a right-end metric norm falls below `4R`, the optimum cannot lie farther to the right.

---

## 5. Exact stationary solve gives the global optimum

The cross-metric threshold `4R` has a stronger interpretation than just a sign test.

### Theorem B — stationary range-solve global optimum

Let `tau_*` be range-feasible with an exact solve

**(5.1)** `K_* y_* = b`,

where

`K_* := H + tau_* G`.

Assume the exact scalar stationarity condition

**(5.2)** `y_*^T G y_* = 4R`.

Define

**(5.3)** `E_* := C + tau_* R + (b^T y_*)/4`.

Then for **every** other range-feasible multiplier `tau` with exact solve `K_tau y_tau=b`, one has the exact gap identity

**(5.4)**

`4(E_tau-E_*) = (y_tau-y_*)^T K_tau (y_tau-y_*)`.

Therefore

**(5.5)** `E_tau >= E_*`.

So `(tau_*,y_*)` is a globally optimal multiplier/solve pair over the whole range-feasible family.

### Proof

Set

`z := y_tau-y_*`,

`d := tau-tau_*`.

Using `K_tau y_tau=b`,

`z^T K_tau z`

` = y_tau^T K_tau y_tau`

`   - 2 y_*^T K_tau y_tau`

`   + y_*^T K_tau y_*`

` = q_tau - 2q_* + y_*^T(K_*+dG)y_*`

` = q_tau - 2q_* + q_* + d(4R)`

` = q_tau-q_* + 4dR`

` = 4(E_tau-E_*)`.

Since `K_tau>=0`, the right side is nonnegative.

This is stronger than saying a derivative vanishes. It gives the exact suboptimality gap as a physical quadratic energy.

### Root-free optimality packet

A checker does not need a derivative theorem. It only needs:

1. `K_*>=0`;
2. `K_* y_*=b`;
3. `y_*^T G y_*=4R`;
4. the fixed-`tau_*` floor equation or inequality.

Every other feasible multiplier is then dominated by the exact completion (5.4).

### Budget obstruction corollary

Suppose a downstream dwell/headroom layer allows at most reset charge `J`. If an exact stationary packet exists and

**(5.6)** `4(J-C-tau_*R) < b^T y_*`,

then `J<E_*`. By (5.5), **no other range-feasible multiplier can fit the budget either**.

This is a genuine mathematical obstruction, not a failure of a particular chosen `tau`.

Conversely, if

`4(J-C-tau_*R) >= b^T y_*`,

then `tau_*` is the best available multiplier for this exact quadratic reset envelope.

---

## 6. Physical contact state: the stationary certificate is sharp

The stationary solve also exposes the worst-case physical state directly.

Assume Theorem B and set

**(6.1)** `x_* := y_*/2`.

By stationarity,

`x_*^T G x_* = (1/4)y_*^T G y_* = R`.

Thus `x_*` lies exactly on the physical ellipsoid boundary.

Evaluate the reset quadratic

`f(x):=b^T x - x^T H x + C`.

Since `H=K_*-tau_*G` and `K_*y_*=b`,

`f(x_*)`

` = (1/2)b^T y_* - (1/4)y_*^T H y_* + C`

` = q_*/2 - (1/4)(q_* - tau_* y_*^T G y_*) + C`

` = q_*/4 + tau_*R + C`

` = E_*`.

Hence

**(6.2)** `f(x_*) = E_*`.

So when the stationarity equality is met, the multiplier certificate is not merely globally best among S-procedure multipliers: it actually touches the original physical reset objective at a concrete cell state.

Therefore if `J<E_*`, the same packet produces an explicit physical counterexample `x_*` to `f(x)<=J`.

This is especially useful for fail-closed reasoning: a negative stationary reserve cannot be repaired by trying more multipliers, Young parameters, or Schur decompositions because the physical quadratic itself violates the proposed floor.

---

## 7. Boundary optimum and rational bracketing

An exact stationary `tau_*` may be irrational, or the optimum may occur at the left edge of the feasible multiplier ray. The secant algebra still gives useful exact certificates.

### Theorem C — right-ray boundary optimality

Let `tau_0` be range-feasible, with solve `y_0`, and assume every multiplier under consideration satisfies `tau>=tau_0`. If

**(7.1)** `y_0^T G y_0 <= 4R`,

then for every range-feasible `tau>=tau_0`,

**(7.2)** `E_tau >= E_0`.

### Proof

For `tau>tau_0`, the cross sandwich gives

`c_0tau <= s_0 := y_0^T G y_0 <= 4R`.

The secant identity therefore gives

`4(E_tau-E_0)=(tau-tau_0)(4R-c_0tau)>=0`.

This remains valid when `K_0` is singular, provided the producer supplies an exact solution satisfying (7.1).

If `K_0>=0` and `G>0`, every `tau>tau_0` automatically has `K_tau>0`. To call `tau_0` the **global** feasible boundary one must still prove that no smaller allowed multiplier is range-feasible; this theorem does not infer that source/domain fact.

### Theorem D — two-sided rational optimum bracket

Let `tau_L<tau_U` be feasible rational multipliers with exact solves. If

**(7.3)** `y_L^T G y_L >= 4R`,

and

**(7.4)** `y_U^T G y_U <= 4R`,

then no feasible multiplier below `tau_L` can beat `E_L`, and no feasible multiplier above `tau_U` can beat `E_U`.

Indeed, for `tau<tau_L`, the cross sandwich gives `c_tau,L >= s_L >=4R`, hence `E_L<=E_tau`; for `tau>tau_U`, it gives `c_U,tau<=s_U<=4R`, hence `E_tau>=E_U`.

Thus every global minimizer lies in the closed bracket `[tau_L,tau_U]`, unless the feasible set itself has an earlier disconnected component (impossible for the standard affine family `K_tau=H+tau G` with `G>0`, once one feasible point is known).

This gives a deterministic rational search strategy:

1. choose rational `tau`;
2. prove `K_tau>=0` and solve `K_tau y=b` exactly;
3. compare the rational scalar `y^T G y` with `4R`;
4. move the bracket accordingly.

No algebraic number needs to enter the trusted packet unless one wants the exact optimizer itself.

---

## 8. The singular lower-boundary hard case is real and must stay explicit

At a singular feasible lower boundary, the solve `y_0` can be nonunique. The intrinsic floor scalar `q_0=b^T y_0` is unique, and every two-point cross metric is unique, but the same-point norm

`y_0^T G y_0`

can depend on the chosen nullspace representative.

Therefore the converse of Theorem C must **not** be used naively:

> finding one singular solve with `y_0^T G y_0 > 4R` does not prove that moving right improves the floor.

The safe alternatives are:

- use the canonical two-point secant `c_0tau`, which is solution-independent;
- supply a particular solve with `y_0^T G y_0<=4R`, which is sufficient for boundary optimality;
- or supply an explicit nullspace/contact witness.

### Hard-case contact witness

At a singular optimal boundary `tau_0`, block equality occurs whenever

`2x-y_0 in ker K_0`.

So a source-independent sharpness packet can supply a vector `n` with

**(8.1)** `K_0 n=0`,

**(8.2)** `(y_0+n)^T G (y_0+n)=4R`,

and set

**(8.3)** `x=(y_0+n)/2`.

Then `x` lies on the physical cell boundary and the same completion used in T-P5-139 saturates the multiplier certificate.

This is the classical singular trust-region hard case in entirely elementary quadratic-form language. It is not necessary for the upper-bound certificate, but it is necessary if one wants an explicit physical sharpness witness at a singular boundary when `y_0/2` itself lies strictly inside the cell.

The trusted consumer should therefore distinguish:

- **certificate mode:** exact range solve + floor gate is enough;
- **global multiplier optimization mode:** use secant/stationary/boundary gates above;
- **physical sharpness/counterexample mode:** additionally require the contact-state premises, especially in the singular hard case.

---

## 9. Exact rational consequence

Suppose `G,H,b,C,R` are rational and candidate multipliers `tau_i` are rational. Whenever exact Gaussian elimination returns rational solves `y_i`, all quantities below are rational:

- `q_i=b^T y_i`;
- `s_i=y_i^T G y_i`;
- `c_ij=y_i^T G y_j`;
- `4(E_j-E_i)=(tau_j-tau_i)(4R-c_ij)`;
- the discrete-convexity cross products in (4.3);
- the stationary equation `s_i=4R` when it happens at a rational point;
- the budget reserve `4(J-C-tau_iR)-q_i`.

Therefore a rational checker can search and compare multipliers without:

- matrix inversion in the theorem statement;
- pseudoinverses at singular points;
- square roots;
- eigenvalues;
- numerical derivatives;
- floating-point minimizers;
- augmented `(n+1)x(n+1)` factorization at every candidate.

The only matrix evidence needed per candidate is the already-required PSD witness for `K_tau` plus the exact solve equalities.

---

## 10. Worked rational interior optimum

Take the one-dimensional packet

`G=1`,

`H=1`,

`b=4`,

`R=1`,

`C=0`,

with `tau>=0`.

Then

`K_tau=1+tau>0`,

and the exact solve is

`y_tau=4/(1+tau)`.

The sharp floor is

`E_tau = tau + 4/(1+tau)`.

Choose

`tau_*=1`,

`y_*=2`.

Then

`K_* y_*=2*2=4=b`,

and

`y_*^T G y_*=4=4R`.

So Theorem B applies. The optimal floor is

**(10.1)** `E_*=3`.

The exact gap identity becomes

**(10.2)**

`4(E_tau-3) = (1+tau)(y_tau-2)^2 >=0`.

For example:

- `tau=0`: `y=4`, `E=4`, RHS=`1*(2)^2=4`;
- `tau=3`: `y=1`, `E=4`, RHS=`4*(-1)^2=4`.

The physical contact state is

`x_*=y_*/2=1`,

which satisfies `x_*^2=R`, and

`4x_*-x_*^2=3=E_*`.

This example shows that the stationary solve equation is exactly the missing multiplier-optimality condition; it is not merely a heuristic derivative balance.

---

## 11. Strengthening the T-P5-139 singular example

T-P5-139 used

`G=I`, `R=1`,

`H=diag(-1,1)`,

`b=(0,3)`, `C=0`.

The feasible multiplier ray begins at

`tau_0=1`,

because

`K_0=diag(0,2)>=0`,

while every `tau<1` leaves a negative first diagonal entry.

T-P5-139 supplied the exact range solve

`y_0=(0,3/2)`.

Its metric norm is

`y_0^T G y_0 = 9/4 < 4R=4`.

Therefore Theorem C proves immediately that **no larger multiplier can improve the `17/8` floor** found in T-P5-139. The earlier result was sharp at fixed `tau=1`; this child upgrades it to sharpness over the entire feasible multiplier ray.

The physical maximizer is a singular hard-case contact rather than `y_0/2`, because `y_0/2=(0,3/4)` lies inside the unit ball. One may choose a nullspace vector `n=(sqrt(7)/2,0)`, so

`K_0 n=0`,

`(y_0+n)^T(y_0+n)=4`,

and

`x=(y_0+n)/2`

lies on the unit circle and attains `17/8`. The square root is needed only to display this particular physical maximizer; the upper-bound and multiplier-optimality certificates remain rational and root-free.

This illustrates why rational certification and explicit sharpness-state construction should remain separate interfaces.

---

## 12. Minimal Lean-facing theorem split

A future Lean sidecar can stay extremely small and source-independent.

### L1 — `rangeSolve_secant`

Inputs:

- symmetric `G,H`;
- `K_i=H+tau_i G`;
- `K_i y_i=b`.

Conclusion:

`b dot y_1 - b dot y_2 = (tau_2-tau_1) * <y_1,G y_2>`.

This is pure ring algebra plus symmetry.

### L2 — `crossMetric_sandwich`

Inputs:

- L1 hypotheses;
- `tau_1<tau_2`;
- PSD of `K_1,K_2`.

Conclusions:

`<y_2,G y_2> <= <y_1,G y_2>`

and

`<y_1,G y_2> <= <y_1,G y_1>`.

Prefer proving the stronger exact identities (3.3)-(3.4).

### L3 — `sharpFloor_secant`

Define the scaled floor relation

`4(E_i-C-tau_i R)=b dot y_i`.

Conclude

`4(E_2-E_1)=(tau_2-tau_1)*(4R-<y_1,G y_2>)`.

### L4 — `stationaryFloor_global`

Inputs:

- `K_* y_*=b`;
- `<y_*,G y_*>=4R`;
- `K_tau y_tau=b`;
- PSD `K_tau`;
- scaled floor relations.

Conclusion:

`4(E_tau-E_*) = Q_{K_tau}(y_tau-y_*) >=0`.

This is the highest-value theorem: exact global optimality by one quadratic completion.

### L5 — `stationaryFloor_contact`

Inputs:

- L4 stationary hypotheses.

Set `x_*=y_*/2` and prove

`Q_G(x_*)=R`

and

`b dot x_* - Q_H(x_*) + C = E_*`.

If avoiding division by two in the statement is important, introduce `two_x=y_*` as a premise and keep all equations scaled by four.

No finite-dimensional range theorem, inverse API, calculus, or S-lemma theorem is required for these leaves.

---

## 13. Fail-closed boundaries

This child does **not** justify any of the following shortcuts:

1. **Approximate solves are not exact solves.** If `K_tau y-b !=0`, the secant and global-gap identities acquire residual terms. They must be retained and budgeted; they cannot be silently dropped.
2. **Different source keys cannot be mixed.** `G,H,b,C,R` and all candidate solves must refer to the same reset packet/cell/reference semantics.
3. **PSD is still required.** A solution of `K_tau y=b` alone does not make the Schur certificate valid if `K_tau` is indefinite.
4. **A singular solve norm is not intrinsic.** `b^T y` and two-point secants are intrinsic; `y^T G y` at a singular point can depend on the nullspace representative. Do not use the wrong converse of Theorem C.
5. **Stationarity outside the feasible multiplier set is irrelevant.** Solving `y^T G y=4R` at an indefinite `K_tau` does not certify an optimum.
6. **Rational search is not source admission.** Exact rational `tau,y` packets remain source-independent until actual deployed/reference coefficients and physical cell coverage are bound.
7. **Global multiplier optimality is not global system closure.** It optimizes only the T-P5-137 quadratic reset envelope; it does not close continuous-flow dissipation, reference coverage, FD/DH errors, P8 flowpipe, or M4.
8. **Physical contact needs its own premises in the singular hard case.** A dual-optimal singular multiplier can be sharp even when `y/2` is interior; the nullspace contact condition must not be invented.

---

## 14. Recommended next packet

For actual reset-multiplier design, the smallest high-value producer packet is now:

1. same-key rational `G,H,b,C,R`;
2. a feasible rational lower multiplier or candidate bracket;
3. for each rational candidate `tau_i`, an exact PSD witness for `K_i=H+tau_iG`;
4. exact solve rows `K_i y_i=b`;
5. exact `s_i=y_i^T G y_i` and, when comparing two candidates, `c_ij=y_i^T G y_j`;
6. if a candidate satisfies `s_i=4R`, promote it only as the **mathematical global optimizer of this reset envelope**, then test the downstream budget `J`;
7. if exact equality is unavailable, retain a rational bracket with `s_L>=4R>=s_U` and continue narrowing without floating-point optimization;
8. at a singular lower boundary, preserve the hard-case/nullspace distinction instead of forcing a positive-definite inverse model.

The main mathematical gain is that multiplier design is now an energy-completion problem rather than a black-box scalar search. The exact stationary witness does three jobs simultaneously: it chooses the globally best multiplier, gives the exact gap to every other feasible multiplier, and—outside the singular hard case—constructs the physical state that saturates the reset bound.

Current status remains `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`. No source, same-cell coverage, controller/Float64 semantics, P8 flowpipe, Lean/kernel receipt, independent verification, admission, registry, or P5/M4 parent closure is upgraded.
