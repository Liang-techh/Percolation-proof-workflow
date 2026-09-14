---
kind: review_result
review_id: review-T-P5-250-thick-affine-tube-equality-multiplier-honglianmozun-20260910T1352Z
task_id: T-P5-250-THICK-AFFINE-TUBE-EQUALITY-MULTIPLIER
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T13:52:00Z
claim_commit: 9d849a0b910c01ee81ddf5bc97746b98ccff32cd
inspected_commit: 7ea565a4d4b7347fc49ddd697f526962a20dc9ba
upstream_commits:
  - 90206be9153fffcb2d5363624794346e4879dc8c  # T-P5-249 rectangular affine image/equality multiplier
  - a25de2d6e01b16133af9dc40d46efcfef6731ef8  # T-P5-247 affine GL(n) covariance
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_weighted_thick_tube_slemma; add_tube_taxed_equality_multiplier_lmi; add_metric_reserve_schur_charge; preserve_eta_zero_and_two_constraint_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact quadratic/S-lemma algebra; weighted support completion; Schur complement; rational one-dimensional regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-250 — Thick affine-tube equality multiplier and metric-aware Lyapunov debit

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-249 proved that an unrestricted matrix equality multiplier is free on the exact affine image `C ξ=0`, where `ξ=[y;1]`. The smallest distinct extension is a weighted thick tube

`(C ξ)^T W (C ξ) <= eta^2`, `W>0`, `eta>0`.

The equality term is now nonzero. This child gives:

1. an exact one-tube S-lemma criterion for the previously free equality multiplier;
2. a direct fraction-free LMI containing no inverse or square root;
3. a compositional Schur reserve charge that separates tube radius from multiplier strength in the correct metric;
4. an exact scalar optimization of that reserve charge when a common reserve metric is available;
5. a sharp 1D regression showing the threshold is genuinely linear in `eta` and that zero exact-image reserve may be destroyed by every positive tube thickness;
6. a fail-closed boundary explaining why this does **not** make the two-constraint `source ellipsoid ∩ tube` problem lossless in general.

No actual P5 source/tube packet, trajectory coverage, Float64 semantics, Lean receipt, independent validation, admission or registry mutation is claimed.

---

# Part I — exact tube-taxed equality multiplier

## 1. Abstract lifted slack

Let `y in R^n` and use augmented coordinates

`ξ := [y;1] in R^N`, `N=n+1`.

Let

`C in R^{r x N}`, `W=W^T>0`.

Write the weighted residual

`e(y):=C ξ`.

The thick affine tube is

`T_eta := { y : e(y)^T W e(y) <= eta^2 }`.

Let `B=B^T in R^{N x N}` denote the **unlifted quadratic slack** whose nonnegativity is required. In a downstream Lyapunov application, `B` may already contain a fixed source S-lemma multiplier or another previously certified quadratic subtraction. Thus the local mathematical question is simply

`ξ^T B ξ >= 0 on T_eta`.

Suppose T-P5-249's exact-image lift supplied `Y in R^{r x N}` such that

`S := B + C^T Y + Y^T C >= 0`.

On `Cξ=0`, `ξ^TBξ=ξ^TSξ`, so `Y` is free. On a thick tube,

`ξ^T B ξ = ξ^T S ξ - 2 e(y)^T Y ξ`,

and the second term must be paid for.

Let `E:=e_N e_N^T`, where `e_N` is the final coordinate vector. Since the augmented slice has `ξ_N=1`,

`ξ^T E ξ = 1`.

Define the tube quadratic

`g(y) := eta^2 - e(y)^T W e(y)`

`       = ξ^T (eta^2 E - C^T W C) ξ`.

Assume strict tube Slater:

there exists `y0` with `g(y0)>0`.

For the intended thickening of a nonempty affine image this is automatic for every `eta>0`, because an exact image point has `Cξ=0`.

---

## 2. Main theorem: exact one-tube S-lemma

**Theorem 1 — `thickTube_equalityMultiplier_iff`.**

Under strict tube Slater, the following are equivalent:

(A) `ξ^T B ξ >=0` for every `y in T_eta`;

(B) there exists `tau>=0` such that

`L(tau) := B + tau C^T W C - tau eta^2 E >=0`;

(C) using the exact-image lifted matrix `S=B+C^TY+Y^TC`, there exists `tau>=0` such that

**`L_Y(tau) := S + tau C^T W C - C^T Y - Y^T C - tau eta^2 E >=0`.**

### Proof

The implication `(B) -> (A)` is direct. For `g(y)>=0`,

`ξ^T B ξ`

`= ξ^T L(tau) ξ + tau g(y)`

`>=0`.

Conversely, `(A)` plus strict feasibility of the single quadratic inequality `g(y)>=0` is precisely the lossless one-constraint S-lemma, hence some `tau>=0` satisfies

`ξ^T[B-tau(eta^2E-C^TWC)]ξ >=0`

for every `y`, which is equivalent to the global augmented PSD matrix in (B). Substituting

`B=S-C^TY-Y^TC`

gives (C). QED.

This is the exact mathematical meaning of **“the equality multiplier is taxed by tube thickness.”** The tax is not an arbitrary Euclidean error radius: it uses the actual normal residual `Cξ` and the declared weight `W`.

---

## 3. Important domain interpretation

If `B` already came from a fixed source-energy multiplier, e.g.

`B = -Q - mu G_source`, `mu>=0`,

where `G_source(y)>=0` defines the source ellipsoid, then `L(tau)>=0` proves the desired target on

`source ∩ T_eta`.

However, Theorem 1 is lossless for **`B>=0 on the whole tube`**, not automatically for the original two-constraint implication involving both source and tube. If the target is safe only because source and tube cooperate, a joint two-quadratic multiplier problem remains. Failure of this one-tube packet is therefore not a physical FAIL for the two-constraint problem.

Suggested fail-closed label:

`FIXED_SOURCE_MULTIPLIER_TUBE_PACKET_INCONCLUSIVE__JOINT_TWO_QUADRATIC_SEARCH_REQUIRED`.

---

# Part II — exact weighted support completion

## 4. Completing the normal residual

For `tau>0`, the multiplier/tube part admits the exact identity

`tau C^T W C - C^T Y - Y^T C`

`= (C-tau^{-1}W^{-1}Y)^T (tau W) (C-tau^{-1}W^{-1}Y)`

`  - tau^{-1} Y^T W^{-1} Y`.

Therefore

`L_Y(tau)`

`= S - tau eta^2 E - tau^{-1}Y^TW^{-1}Y`

`  + (C-tau^{-1}W^{-1}Y)^T(tau W)(C-tau^{-1}W^{-1}Y)`.

This separates the exact tube tax into:

- a scalar/affine-slice debit `tau eta^2 E`;
- a metric dual debit `tau^{-1}Y^TW^{-1}Y`;
- a nonnegative residual square which should **not** be discarded when exactness matters.

The weighted dual metric `W^{-1}` is forced by the support function of the residual ellipsoid; replacing it by an ambient Euclidean norm is generally weaker.

---

## 5. Compositional reserve gate

Dropping only the final nonnegative square yields a clean sufficient packet:

**Theorem 2 — `thickTube_metricReserve_sufficient`.**

If some `tau>0` satisfies

**`S - tau eta^2 E - tau^{-1}Y^T W^{-1}Y >=0`,**

then `L_Y(tau)>=0`, hence `B>=0` on the entire thick tube.

This sufficient gate can itself be checked without `W^{-1}` or division by `tau`. By the Schur complement,

`S - tau eta^2 E - tau^{-1}Y^T W^{-1}Y >=0`

is equivalent to

**`R(tau):=[[S-tau eta^2 E, Y^T],[Y, tau W]] >=0`**

because `tau W>0`.

Thus for rational `S,Y,W,eta^2,tau`, the reserve packet is a purely rational PSD check. No square root, pseudoinverse, eigenvector or numerical support maximization is required.

The gate is exact whenever the dropped square vanishes, i.e. when

`Y=tau W C`.

More generally it is intentionally compositional rather than claimed lossless: the exact checker should prefer `L_Y(tau)>=0`; the Schur reserve packet is useful when a downstream budget ledger wants a source-independent debit.

---

# Part III — optimized common-metric budget

## 6. Relative reserve constants

Suppose a downstream proof owns a PSD reserve metric `R=R^T>=0` and exact rational/nonnegative constants `rho,alpha,beta` satisfying

`S >= rho R`,

`E <= alpha R`,

`Y^TW^{-1}Y <= beta R`.

Then for every `tau>0`,

`S - tau eta^2E - tau^{-1}Y^TW^{-1}Y`

`>= [rho - tau eta^2 alpha - beta/tau] R`.

The scalar debit is

`phi(tau)=tau eta^2 alpha + beta/tau`.

If `alpha>0`, `beta>0`, its exact infimum over `tau>0` is

**`inf phi = 2 eta sqrt(alpha beta)`**

at

`tau_* = sqrt(beta)/(eta sqrt(alpha))`.

Hence a sufficient metric-relative survival gate is

**`rho >= 2 eta sqrt(alpha beta)`.**

For strict margin `rho>2eta sqrt(alpha beta)` and rational input data, a rational `tau` can always be chosen sufficiently close to `tau_*` to preserve strict positivity; therefore the trusted artifact need not store an irrational optimizer.

Degenerate cases are simpler:

- `beta=0`: the equality multiplier vanishes in the `W`-dual metric, so the dual debit disappears;
- `alpha=0`: on the represented subspace the affine normalization direction costs no reserve, and one should retain the full matrix packet rather than divide by `alpha`.

This scalarization is **not** a replacement for the exact matrix LMI. It is a portable energy-budget corollary.

---

# Part IV — sharp rational regressions

## 7. Sharp 1D thickening threshold

Take scalar physical coordinate `x`, augmented `ξ=(x,1)`,

`C=[1,0]`, `W=[1]`, so the tube is `|x|<=eta`.

Let `m>0`, `k>0`, and choose

`S=[[0,0],[0,m]]`,

`Y=[0,k]`.

Then

`C^TY+Y^TC=[[0,k],[k,0]]`,

so

`B=S-C^TY-Y^TC=[[0,-k],[-k,m]]`.

Thus

`ξ^TBξ = m-2kx`.

On the exact image `x=0`, the slack is `m>0`. On the thick tube,

`min_{|x|<=eta}(m-2kx)=m-2k eta`.

Therefore safety holds **iff**

**`eta <= m/(2k)`.**

Now apply Theorem 1:

`L_Y(tau)=[[tau,-k],[-k,m-tau eta^2]]`.

PSD requires

`tau(m-tau eta^2)-k^2 >=0`.

The determinant is a concave quadratic in `tau`, maximized at

`tau=m/(2eta^2)`,

with maximum

`m^2/(4eta^2)-k^2`.

Hence the exact LMI reproduces precisely the physical threshold

`eta<=m/(2k)`.

For this regression the reserve Schur charge is also exact:

`m - tau eta^2 - k^2/tau >=0`,

whose optimal debit is `2k eta`.

So the linear-in-`eta` budget is not an artifact of Young's inequality; it is the true support cost in this branch.

---

## 8. Zero-reserve obstruction: every positive tube can fail

Use the same `C,W`, but set

`S=0`, `Y=[0,1]`.

Then

`B=[[0,-1],[-1,0]]`,

and

`ξ^TBξ=-2x`.

On the exact image `x=0`, the slack is exactly zero, so the exact equality theorem passes.

For **every** `eta>0`, however, the allowed point `x=eta` gives

`ξ^TBξ=-2eta<0`.

Thus an equality multiplier supported only by semidefinite contact can have **zero thickening radius**. There is no theorem of the form “exact-image safety automatically extends to some positive tube” without an additional reserve/transversality assumption.

The exact LMI exposes the same obstruction:

`L_Y(tau)=[[tau,-1],[-1,-tau eta^2]]`.

Its lower-right entry is negative for every `tau>0`; `tau=0` leaves an indefinite cross matrix. Hence no certificate exists.

This is the precise failure boundary requested by T-P5-249.

---

# Part V — relation to exact equality and singular limit

## 9. `eta=0` is not obtained by blindly invoking the strict S-lemma

When `eta=0`, the tube constraint becomes

`e^TWe<=0`,

which is equivalent to the exact equality `e=0`, but strict Slater is lost. T-P5-249's unrestricted equality-multiplier theorem is the correct exact branch.

A finite scalar `tau` normal penalty can fail at semidefinite contact even though a free matrix equality multiplier succeeds; T-P5-249 already supplied that obstruction. Therefore the `eta downarrow 0` limit of the thick-tube scalar multiplier must not be used to replace the exact equality theorem. In sharp cases the required `tau` may diverge as `eta->0`.

Dispatcher:

- `eta=0`: use T-P5-249 exact equality-multiplier/image theorem;
- `eta>0` and strict tube Slater: use the present one-tube S-lemma;
- approximate/nonquadratic residual sets: this theorem does not apply without another enclosure argument.

---

# Part VI — candidate theorem statements

## 10. Candidate library statements

### Candidate A

`thickTube_equalityMultiplier_iff`

Inputs:

- symmetric `B,S`;
- residual matrix `C`;
- `W>0`, `eta>0`;
- multiplier matrix `Y` with `S=B+C^TY+Y^TC`;
- strict tube Slater.

Conclusion:

`(forall y, (Cξ)^TW(Cξ)<=eta^2 -> ξ^TBξ>=0)`

iff

`exists tau>=0, S+tau C^TWC-C^TY-Y^TC-tau eta^2E >=0`.

### Candidate B

`thickTube_metricReserve_sufficient`

If `tau>0` and

`[[S-tau eta^2E,Y^T],[Y,tau W]]>=0`,

then the thick-tube safety conclusion holds.

### Candidate C

`thickTube_commonMetric_budget`

Given `S>=rho R`, `E<=alpha R`, `Y^TW^{-1}Y<=beta R`, a sufficient survival condition is

`rho>=2eta sqrt(alpha beta)`.

For strict rational margin, there exists a rational `tau>0` certifying the Schur reserve block.

---

# Part VII — structural fingerprint

## 11. New fingerprint

`exact affine-image equality multiplier`

`-> residual thickening Cξ in weighted ellipsoid`

`-> free equality term becomes bilinear normal/tangent debit`

`-> one-tube lossless S-lemma`

`-> exact L_Y(tau) PSD gate`

`-> weighted completion in W/W^{-1}`

`-> optional Schur reserve block`

`-> optimized O(eta) metric budget`

`-> zero-reserve contact may have zero admissible thickness`.

This is a genuine Lyapunov/energy mechanism: the tube radius and equality multiplier interact through a dual metric pair rather than through a coarse ambient norm.

---

# Part VIII — exact boundaries and non-claims

## 12. Boundaries

1. **Joint source+tube losslessness is not claimed.** Two independent quadratic inequalities do not in general inherit the one-constraint lossless S-lemma. The present packet is exact for the fixed quadratic slack `B` over the full tube and therefore compositional for source∩tube.

2. **`eta=0` uses T-P5-249.** Strict Slater disappears; do not infer the exact equality result by setting `eta=0` in the present theorem.

3. **`W` must be positive definite in the reserve-completion branch.** The exact LMI `L_Y(tau)` itself still makes algebraic sense for `W>=0`, but `W^{-1}`/Schur support statements do not. Semidefinite `W` requires quotient/range handling.

4. **Actual residual semantics remain open.** No claim is made that a P5 nonlinear chart defect, FD halo error, Newton–Euler graph residual or trajectory tube is exactly represented by this `C,W,eta` packet.

5. **No coverage upgrade.** A tube certificate is a conditional inequality on the declared tube, not proof that trajectories or stencils remain in it.

---

## 13. Next distinct seam

The clean next mathematical seam is the **semidefinite normal metric / partial tube** case:

`W>=0` with nontrivial `ker(W)`.

Then some residual directions are unpenalized, so the correct criterion should split `range(W)` from `ker(W)`, derive a hard annihilation/range gate for the equality multiplier on unbounded residual directions, and only then apply the present weighted S-lemma on the quotient. This is structurally parallel to the earlier signed-lineality/range obstructions, but now occurs in the affine-tube normal bundle.

An alternative actual-source-driven seam is a genuinely coupled `source ellipsoid ∩ thick tube` packet. That should be attempted only if the real P5 source supplies both quadratics, because generic two-constraint S-procedure losslessness is false.

---

## 14. Non-claims

This review does not establish:

- actual P5 `C,W,eta,Y,S` source identity;
- source/tube/trajectory/FD-halo coverage;
- a lossless generic two-quadratic S-procedure;
- Float64 or interval semantics;
- a Lean/kernel receipt;
- independent verification by 封不觉;
- admission or registry eligibility;
- P5/P8/M4 parent closure.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.