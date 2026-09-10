---
kind: review_result
task_id: T-P5-205-COPOSITIVE-REFERENCE-RESERVE-EXTRACTION
review_id: R-T-P5-205-COPOSITIVE-REFERENCE-RESERVE-EXTRACTION-GUYUEFANGYUAN-20260910T0222Z
agent: 古月方源
source_agent: 古月方源
completed_at: '2026-09-10T02:31:00Z'
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
claim_path: agent_review_inbox/claim-T-P5-205-COPOSITIVE-REFERENCE-RESERVE-EXTRACTION-guyuefangyuan-20260910T0222Z.md
claim_commit: d0c08b13de44607c49ab1f8b3b4ce894152e9cb4
derived_from:
  - T-P5-192
  - T-P5-203-PSD-SHARP-POLAR-SCHUR-DUAL
  - T-P5-204-SUPPORT-SLACK-LYAPUNOV-MARGIN
scope: mathematics_only
---

# T-P5-205 — Copositive reference-reserve extraction

## 0. Goal and boundary

T-P5-204 leaves a quantitative seam: the deployed/slack correction can only be absorbed if the *actual* T-P5-192 reference-sector certificate carries a positive, checker-consumable reserve. A PASS at zero reserve only proves nonincrease and cannot be silently upgraded to a positive Lyapunov margin.

This child supplies an exact cone-pullback reserve equivalence, a rational no-division packet, a compositional mismatch budget, and counterexamples that fix two unsafe shortcuts. It does **not** claim that the current source artifacts already provide the required matrices or a positive numerical reserve.

## 1. Physical cone and pullback notation

Let the physical sector/cone be finitely generated as

`K = { e = V y : y >= 0 }`,

with a fixed same-key generator matrix `V`. Let the T-P5-192 reference derivative quadratic be represented by a symmetric matrix `G_ref`, with the sign convention that the desired reference inequality is

`e^T G_ref e <= 0`.

Let the Lyapunov/energy quadratic used by the downstream mismatch budget be

`E(e) = e^T H e`,

with symmetric `H`. Define the cone pullbacks

`A := - V^T G_ref V`,

`B :=   V^T H V`.

Thus reference nonincrease is exactly copositivity of `A` on the nonnegative orthant, while nonnegativity of the Lyapunov energy on the physical sector is copositivity of `B`.

Throughout, `Cop(M)` means

`y^T M y >= 0` for every `y >= 0`.

No PSD replacement is intended: all statements below are orthant/cone statements.

## 2. Exact reserve equivalence

### Theorem 2.1 — cone reserve iff one loaded copositivity gate

For every scalar `eta >= 0`, the following are equivalent:

1. for every `e in K`,
   `e^T G_ref e <= - eta e^T H e`;
2. `Cop(A - eta B)`.

### Proof

Write `e=Vy`, `y>=0`. Then

`- e^T G_ref e - eta e^T H e`

`= y^T[-V^T G_ref V - eta V^T H V]y`

`= y^T(A-eta B)y`.

Therefore the physical-sector reserve inequality for every `e=Vy` is exactly the orthant copositivity condition. No inverse, eigenvalue, square root, normalization, or optimizer is introduced. QED.

### Corollary 2.2 — rational no-division reserve packet

Let `p>=0`, `q>0` be rationals (or exact integers after clearing denominators), and let `eta=p/q`. Then

`Cop(A-eta B)  <=>  Cop(q A - p B)`.

Hence a producer can export the reserve as the exact tuple

`(A, B, p, q, certificate_for_Cop(qA-pB))`

without any trusted division.

## 3. Reserve monotonicity and sharp reserve

Assume `Cop(B)`. If `Cop(A-eta0 B)` for some `eta0>=0`, then every `eta` with `0<=eta<=eta0` also passes, because

`A-eta B = (A-eta0 B) + (eta0-eta) B`,

and both summands are copositive.

Thus the feasible reserve set is downward closed. Existing exact copositivity machinery can therefore bracket a rational reserve without introducing generalized eigenvalue code.

If the baseline `Cop(A)` is already known, the sharp abstract reserve is

`eta_* = inf { (y^T A y)/(y^T B y) : y>=0, y^T B y>0 }`.

Directions with `y^T B y=0` do not constrain `eta` provided the baseline `Cop(A)` holds there. The checker need not evaluate this ratio; it is only the variational interpretation of the loaded-copositivity gate.

## 4. A normalized two-certificate packet with no division

Let `J := 1 1^T`, so for `y>=0`,

`y^T J y = (1^T y)^2`.

Choose exact rationals `m>0`, `U>0` and verify

`Cop(A - m J)`,                                           (lower dissipation certificate)

`Cop(U J - B)`.                                           (upper energy certificate)

Then

`U A - m B`

`= U(A-mJ) + m(UJ-B)`

is copositive. Therefore the reference certificate carries the positive reserve

`eta = m/U`.

This is useful when the source can cheaply certify a normalized lower bound for the reference dissipation and a normalized upper bound for the Lyapunov energy. The trusted checker can keep the pair `(m,U)` cross-multiplied and never form `m/U`.

The lower certificate `Cop(A-mJ)` is especially strong on the orthant: every nonzero `y>=0` has `1^T y>0`, so it gives a genuinely positive normalized reference dissipation.

## 5. Exact composition with T-P5-203 / T-P5-204 mismatch

The most useful no-division form does not require scalarizing the deployed correction too early.

Let `C` be the symmetric pullback matrix of the total same-key mismatch/slack correction, with the convention that the final desired inequality requires

`y^T(A-C)y >= 0` for all `y>=0`.

Suppose a source reserve packet gives

`Cop(qA-pB)`

with `p>=0`, `q>0`. If the downstream adapter separately proves the cone budget

`Cop(pB-qC)`,

then

`q(A-C) = (qA-pB) + (pB-qC)`

is copositive, hence `Cop(A-C)`.

### Theorem 5.1 — reserve-currency composition

`Cop(qA-pB)` and `Cop(pB-qC)` with `q>0` imply `Cop(A-C)`.

This is an exact algebraic seam between a T-P5-192 reference reserve and a T-P5-203/T-P5-204 correction packet. It preserves the full quadratic shape of `C`; cancellation need not be discarded by first replacing `C` with a scalar multiple of `B`.

### Scalar slack specialization

If T-P5-204 gives the simpler bound `C <=_cop sigma B`, i.e.

`Cop(sigma B-C)`,

and `sigma <= p/q`, then, assuming `Cop(B)`, the budget closes. A division-free sufficient check is simply

`p - q sigma >= 0`.

For the normalized `(m,U)` packet of Section 4, a scalar correction `sigma B` is absorbed whenever

`U sigma <= m`.

Indeed

`U(A-sigma B) = (UA-mB) + (m-U sigma)B`,

and both terms on the right are copositive.

This is the recommended checker-facing inequality for any T-P5-204 support/slack quantity already reduced to a rational scalar `sigma` multiplying the same Lyapunov form.

## 6. Obstruction: zero-reserve PASS does not imply positive reserve

Take

`A = diag(1,0)`,

`B = I_2`,

on `R_+^2`.

Then `A` is copositive, so the zero-reserve reference inequality passes. But for every `eta>0`, with `y=(0,1)`,

`y^T(A-eta B)y = -eta < 0`.

Hence the sharp reserve is exactly `eta_*=0` even though `B` is positive definite.

**Implementation consequence:** an existing T-P5-192 boolean PASS at `eta=0` is not evidence for any positive T-P5-204 decay budget. A positive reserve must be separately certified by `qA-pB`, by the `(m,U)` packet, or by another exact quantitative certificate.

## 7. Obstruction: generator-ray checks are not enough

A finitely generated cone does **not** reduce a quadratic reserve ratio to independent checks on its generating rays.

Take the full orthant with `V=I_2`,

`A = [[1,-9/10],[-9/10,1]]`,

`B = I_2`.

On each coordinate generator, the apparent reserve ratio is `1`. But for `y=(1,1)`,

`y^T A y = 1/5`,

`y^T B y = 2`,

so the reserve ratio is only `1/10`.

Moreover

`A-(1/10)B = (9/10) [[1,-1],[-1,1]]`

is PSD and hence copositive, so the true sharp reserve is exactly `1/10`.

**Implementation consequence:** do not compute a reserve as the minimum of per-generator ray margins. Cross terms can reduce the interior margin by an order of magnitude. The correct finite checker object remains `Cop(qA-pB)`.

## 8. Strict-decay qualification

A positive scalar reserve `eta>0` yields

`e^T G_ref e <= -eta E(e)`.

It yields *strict* negativity for every nonzero physical `e` only if `E(e)>0` for every nonzero `e in K`. Copositivity of `B` alone is not enough; one needs strict copositivity/coercivity of the Lyapunov form on the physical cone (or an equivalent source certificate).

Example: `A=B=diag(1,0)` admits reserve `eta=1`, but both sides vanish on the nonzero ray `(0,1)`. Therefore downstream code must not turn `eta>0` into a global strict-contraction claim without a positive-energy premise.

## 9. Recommended producer / checker contract

For each exact same-key physical selector/sector, the source-side producer should attempt, in this order:

1. Export `V`, `G_ref`, and `H`, then form exact pullbacks `A=-V^T G_ref V`, `B=V^T H V`.
2. Reuse the existing copositivity lane to certify `Cop(qA-pB)` for an explicit rational candidate `p/q>0`.
3. If direct loaded copositivity is awkward, attempt the normalized pair `Cop(A-mJ)` and `Cop(UJ-B)` and retain `(m,U)` instead of a floating quotient.
4. Preserve a matrix-shaped downstream correction `C` whenever available and check `Cop(pB-qC)` directly. Only scalarize to `sigma B` when the source/adapters naturally provide such a bound.
5. If the best certified candidate is `p=0`, report **zero quantitative reserve**. Do not fabricate a positive margin from baseline nonincrease.
6. If a candidate reserve fails, retain the exact nonnegative witness `y` from the copositivity checker as a counterexample for source/sector refinement.

## 10. Suggested Lean leaves

The proof surface can be kept small and mostly algebraic before introducing large matrix APIs:

- `pullback_reserve_iff_copositive`
  - substitution `e=Vy` and `ring`.
- `copositive_sub_smul_mono`
  - if `B` and `A-eta0 B` are copositive and `0<=eta<=eta0`, then `A-eta B` is copositive.
- `normalized_twoCertificate_reserve`
  - from `Cop(A-mJ)` and `Cop(UJ-B)` derive `Cop(UA-mB)`.
- `reserve_currency_compose`
  - from `Cop(qA-pB)` and `Cop(pB-qC)` derive `Cop(q(A-C))`.
- `no_positive_reserve_of_zero_dissipation_positive_energy`
  - if some `y>=0` has `A[y]=0` and `B[y]>0`, no `eta>0` can pass.
- a `norm_num` regression for the `[[1,-9/10],[-9/10,1]]` example showing why generator-only margin checks are unsound.

The first four leaves require only closure of copositive forms under addition and nonnegative scalar multiplication plus ring identities.

## 11. What remains open

This child does **not** close the parent deployment chain. Still required:

- actual same-key extraction of `V`, `G_ref`, `H` from the T-P5-192 source artifact;
- an explicit positive rational `p/q` or `(m,U)` that passes for the real physical sector;
- the actual T-P5-203/T-P5-204 mismatch matrix/scalar and a same-key budget comparison;
- sector/trajectory coverage and any boundary-face bookkeeping;
- Float64 / interval enclosure and source-rounding obligations;
- Lean/kernel implementation and independent verification by 封不觉;
- registry/admission/provenance closure by the designated lanes.

## 12. Verdict

`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.

The mathematical seam is closed: a positive reference reserve is exactly a loaded copositivity certificate, admits an exact rational no-division representation, and composes additively with the downstream mismatch/slack matrix. The remaining blocker is no longer conceptual: the real T-P5-192 source must instantiate a positive rational reserve and the real downstream correction must fit inside it.