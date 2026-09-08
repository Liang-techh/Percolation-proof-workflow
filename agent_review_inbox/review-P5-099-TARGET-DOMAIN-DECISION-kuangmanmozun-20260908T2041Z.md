---
kind: review_result
review_id: P5-099-TARGET-DOMAIN-DECISION-kuangmanmozun-20260908T2041Z
task_id: P5-099-TARGET-DOMAIN-DECISION
source_agent: 狂蛮魔尊
created_at: "2026-09-08T20:41:00Z"
inspected_commit: "779fdc3871384f23a1a06153b9fa0bf44b6c7e38"
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_TargetCaps.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_TargetCellInclusion20260908.lean
  - agent_review_inbox/review-P5-TARGET-REPAIR-MINIMAL-20260908-Sartre.md
  - agent_review_inbox/review-P5-PARAMETER-FEASIBILITY-ENVELOPE-20260908-Sartre.md
admission_label: pending
status: mathematical_obstruction_with_sharp_pointwise_repair_threshold
formal_certificate_allowed: false
registry_eligible: false
---

# P5-099 — exact witness is inside the current broad target domain; sharp pointwise target/beta thresholds

## 1. Question and decision

梁智炜 assigned this lane to decide whether the exact full-graph witness

`x_* : q=0, v=0, w=1`

can be excluded by the intended target domain, and, if not, to give the smallest exact target/beta correction forced by that point.

**Decision:** under the currently formalized broad target-domain envelopes, the witness cannot be excluded. It lies strictly inside the q/v ellipsoid and inside every stated disturbance cap. Therefore any universal nonnegative target over that broad domain is mathematically false if the previously harvested exact source witness is retained. Excluding the point requires a new, explicitly narrower physical/reachable-domain predicate together with a coverage proof; it cannot be obtained by relabeling GrowthCaps, the full ellipsoid, a ramp law, a finite-difference halo, or a path cover.

At this point the direct target value is exactly

`P_* = b-h = -G < 0`.

Hence the sharp **intrinsic** pointwise repair is an added beta charge of at least `G` (or an equally large weakening of the target floor). Any Schur/Young consumer that keeps the original split pays additional proof slack; those larger thresholds are listed below.

This is a mathematical/domain decision only. It does not promote source binding, coverage, Lean/kernel status, P5/M4, registry, or admission.

## 2. Exact domain membership

The current target sidecar defines

`GrowthCaps(x) : |q_j|<=5/2, |v_j|<=15, |w|<=2`,

and the coverage-driver full ellipsoid

`fullP(x) = (3/2) sum q_j^2 + (4/5) sum v_j^2`.

The theorem `full_ellipsoid_caps` consumes `fullP(x)<=28/5` and `w^2<=3`.
For `x_*=(q=0,v=0,w=1)` we have, by exact arithmetic,

`fullP(x_*) = 0 < 28/5`,

`w_*^2 = 1 < 3`,

`|w_*| = 1 < 2`.

Thus `x_*` is not a boundary accident: it has strict reserve in all displayed q/v/disturbance inequalities. In particular no tightening of the already-derived coordinate consequences of the same ellipsoid can remove it.

The ramp sidecar also does not remove the point. `rampState` uses `w=amplitude*time`. Choosing `amplitude=1` and `time=1` gives `w=1`, with `amplitude^2=1<=3` and `0<=time<=1`. The theorem correctly keeps an independent domain/cover premise `D` and `cover`; therefore a *specific* reachable-set theorem could still exclude this realization, but no such exclusion follows from the present cap/ramp algebra itself.

Consequently the only mathematically legitimate exclusion route is a new theorem of the form

`D_physical(x) -> x != x_*`

(or a stronger quantitative separation), plus a proof that the final theorem is quantified only over `D_physical`. A restriction such as a smaller disturbance interval, a special ramp schedule, or a reachable-flow subset changes the theorem/domain and must be propagated through coverage. FD halo/path/derivative-cover predicates are evaluator-support sets and cannot be used as a silent physical-domain exclusion.

## 3. Frozen source value at the witness

Use the previously harvested exact source packet at `q=v=0,w=1`:

- `r_*=0`;
- `ell_*=lTotal_*=k`;
- `H=M_CC(0)^-1` is the fixed positive definite matching metric;
- `h = k^T H k`;
- `S = |a_C|^2` for the source acceleration;
- frozen beta value `b = S/100 + 1/20`.

The exact rational gap is

`G = h-b`

with

`G = 908496145006016245606224697730990370520062591844085847627884168761717525947223 / 6758722017363098327650876161130774484190251396262627754497272897204629481055540`.

Hence `G>11/100` (numerically about `0.1344183327`, only for orientation), and

`P_* = beta_* - lTotal_*^T H lTotal_* = b-h = -G < 0`.

This is a direct target failure before Young, Schur, Q-search, determinant, adjugate, or port-cap relaxation. Therefore no choice of Q, lambda, residual split, or sharper port estimate can prove the unchanged statement `P>=0` on any domain containing `x_*`.

## 4. Sharp intrinsic target/beta correction

Let the displayed target require `P_new(x_*) >= t_*`, and let the only change at the witness be an additional beta charge `g_*`, so `P_new=P_old+g_*`. Then

`P_new(x_*) >= t_*  <->  g_* >= G+t_*`.

This is necessary and sufficient at the point and is sharp. Equality gives `P_new(x_*)=t_*`; any smaller charge fails at the exact witness. In particular for the existing nonnegative target `t_*=0`,

**sharp intrinsic pointwise beta increment:** `g_* >= G`.

Equivalently, if beta is frozen and the conclusion is weakened to `P_old >= -tau_*`, the sharp floor change is `tau_* >= G`. A strict positive target/reserve requires strict `g_*>G+t_*` relative to the desired strict margin.

If beta is parameterized by a common acceleration coefficient `p_a` and disturbance coefficient `p_w`, with q/v monomials vanishing at this witness,

`beta_*(p_a,p_w)=p_a*S+p_w`,

then the exact target half-space is

`p_a*S + p_w >= h+t_*`.

Thus changing q/v beta coefficients alone can never repair this witness.

For the currently frozen `p_w=1/20`, the exact minimum new acceleration coefficient for the direct target is

`p_a >= (h-1/20+t_*)/S`.

At `t_*=0` this lies strictly between `49363/10^6` and `49364/10^6`. The current `p_a=1/100` therefore fails the exact target at this point.

For frozen `p_a=1/100`, the exact minimum new disturbance coefficient is

`p_w >= h-S/100+t_*`,

which at `t_*=0` lies strictly between `184418/10^6` and `184419/10^6`.

These are pointwise necessities, not full-cell sufficiency statements.

## 5. If the existing Schur/Young proof route is retained

The direct target threshold `G` is the information-theoretic minimum. A fixed proof decomposition may require more budget.

Define

`Gamma = 2h-b`

and let `d>0` be the existing global-cap expression evaluated at the witness (even though the true port residual is zero there). Exact prior arithmetic gives

`Gamma = 2385725165280437386413665293324305992717331018379028255833360562921055025947223 / 6758722017363098327650876161130774484190251396262627754497272897204629481055540`,

so `Gamma>31/100` (about `0.3529846558`). The old-cap lambda=2 threshold is

`Gamma_old = Gamma + 2d`,

with `1/2 < Gamma_old < 3/5` (about `0.5181338044`).

Therefore, for the original split and `lambda=2`:

- with the sharp point cap `Delta_*=0`, an added beta charge must satisfy `g_* >= Gamma+t_*`;
- if the old global cap value `d` is retained, `g_* >= Gamma+2d+t_*`.

For `p_w=1/20`, the corresponding minimum `p_a` values are exactly

`(2h-1/20)/S`  for cap zero,

`(2h+2d-1/20)/S` for the old cap,

lying respectively in `(113369,113370)/10^6` and `(161731,161732)/10^6` at `t_*=0`.

This clarifies the earlier `p_a=3/25` candidate: `3/25=0.12` is large enough for the **pointwise lambda=2, cap-zero** inequality, but is too small if the old cap `d` is retained. It is also not a full-domain certificate.

If one is allowed to re-split the same total residual optimally, the completed-square lower bound is exactly `h`; hence the best possible compensated split returns to the intrinsic `Bavail>=h`, i.e. the beta increment `G`. It cannot do better because the total residual energy `h` is invariant under the split. This proves that Q/lambda/split search cannot erase the intrinsic deficit.

## 6. Sharp obstruction / counterexample logic

The point `x_*` itself is the counterexample to any universal claim over the broad target domain:

1. `x_*` satisfies the displayed domain inequalities with strict reserve.
2. The exact source graph gives `P(x_*)=-G<0`.
3. Therefore `forall x in D_broad, P(x)>=0` is false whenever `D_broad` contains the full-ellipsoid/disturbance point.

This obstruction is stronger than a failed optimizer or sampled negative value: it survives arbitrarily large Q, exact zero port cap, and arbitrary compensated residual splitting unless the target/beta statement changes.

A proposed new domain that excludes only this point is not automatically useful. To preserve a universal physical theorem, the exclusion must be justified by a source/reachability invariant. For example, `|w|<1` excludes `w=1` but also removes a portion of the currently allowed input set; without a physical coverage theorem this is a statement change, not a repair.

## 7. Lean-friendly theorem statements

The mathematical leaf can be formalized without square roots.

### Domain leaf

```text
def witness : State := { q := 0, velocity := 0, disturbance := 1, time := 1 }

theorem witness_in_full_target :
  fullP witness <= 28/5 /\ witness.disturbance^2 <= 3 /\ GrowthCaps witness
```

All goals reduce to exact rational normalization.

### Direct target necessity

```text
theorem witness_beta_increment_necessary
    (G g t Pold : Real)
    (hG : Pold = -G) (hnew : Pold + g >= t) :
    G + t <= g
```

and conversely `G+t<=g` gives the pointwise target.

### Coefficient half-space

```text
theorem witness_beta_coeff_necessary
    (S h pa pw t : Real) (hS : 0 < S)
    (htarget : pa*S + pw - h >= t) :
    h + t <= pa*S + pw
```

No division is needed in the trusted consumer; coefficient threshold division can remain an optional corollary.

### Fixed lambda=2 proof-route debit

```text
theorem witness_lambda2_budget
    (h b d g t : Real)
    (hbudget : b + g >= 2*h + 2*d + t) :
    (2*h - b) + 2*d + t <= g
```

Again this is linear arithmetic after the exact source scalars are supplied.

## 8. Failure branches explicitly closed

- **Increase Q / solve a larger SDP:** cannot change `P_*=-G`.
- **Tune lambda only:** proof slack can change, direct target cannot.
- **Use exact zero port residual:** removes cap slack but leaves `G`.
- **Redistribute `ell+r`:** optimal compensated split has unavoidable charge `h`; it cannot make the frozen `b<h` feasible.
- **Increase q/v beta weights:** their monomials are zero at `q=v=0`.
- **Recenter the residual without compensation:** certifies a different residual/target and needs a new source theorem.
- **Call the point non-ramp:** `amplitude=time=1` realizes `w=1` under the currently displayed ramp algebra.
- **Use FD/path halo as a domain exclusion:** wrong quantifier/type; evaluator support is not a physical reachable-set theorem.
- **Treat `3/25` as global repair:** it passes only one pointwise relaxed configuration and fails the old-cap configuration; no all-cell/source/coverage result follows.

## 9. Requested next action

The coordinator now has a binary mathematical choice:

1. **Keep the current broad intended domain and original target.** Then the frozen target is rejected by the exact witness. To continue, explicitly fund at least `G` of pointwise beta/target charge (and the larger proof-route debit if the original Schur split/cap is retained), followed by a new full-domain/source proof.
2. **Keep the target unchanged.** Then provide a new source/reachability theorem that excludes `x_*` from the final physical quantifier and propagate that narrower domain through path/derivative/FD/graph coverage. Merely changing a cap label is insufficient.

Until one of those two statement-level choices is made and source/coverage is supplied, this lane remains `pending`; no formal-certificate or registry effect is justified.
