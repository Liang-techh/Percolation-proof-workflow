kind: review_result
result_id: REV-T-P5-123-20260909T0435Z-kuangmanmozun
source_agent: 狂蛮魔尊
target_task_id: T-P5-123-PARAMETRIC-JET-CONSISTENCY-AND-TAYLOR-HALF
repository: Liang-techh/Percolation-proof-workflow
branch: main
commit_scope: agent_review_inbox/NEW_REVIEW_P5_SAME_CELL_GRAPH_JET_ADDITIVE_CONTRACT_20260908.md; agent_review_inbox/NEW_REVIEW_P5_GRAPH_JET_IFT_AND_INVERSE_FREE_HCAP_20260908.md
decision: REQUEST_CHANGES
review_scope: >-
  Mathematical closure only. Determine what a uniform quadratic same-cell graph-jet remainder actually forces at the parameterized base state, derive the sharp second-order Taylor coefficient when M2 is a Hessian supremum, transport it into the existing metric/quartic envelope, and exhibit exact counterexamples for omitted parametric affine jets and basepoint-only Hessian control.
passed_checks:
  - Uniform O(||eta||^2) remainder forces exact zero-order eta-jet matching for every admitted parameter w.
  - Uniform O(||eta||^2) remainder forces exact first-order eta-jet matching for every admitted parameter w.
  - Whole-chord D_eta^2 bound yields the sharp integral-Taylor coefficient 1/2.
  - Compatible output-metric cap converts the sharp norm remainder into a factor-1/4 quartic metric cap.
  - Whole-cell quadratic-to-linear reduction follows after a certified rho(eta)^2 <= R_cell^2 bound.
  - Counterexamples exclude missing w-dependent constant/linear eta terms and basepoint-only Hessian certification.
failed_checks:
  - Current source packet does not yet state that the proposed reduced linearization exactly equals the parameterized zero/first eta jet g(0,w)+D_eta g(0,w) eta for every admitted w.
  - Current symbol M2 is not yet semantically pinned down as either a Hessian supremum or an already-integrated Taylor-remainder coefficient; applying the 1/2 factor without this distinction risks double charging or double improvement.
  - A basepoint Hessian value alone is insufficient; whole same-cell chord coverage for the Hessian envelope is still required.
required_actions:
  - Preserve w as a fixed parameter when taking the eta Taylor expansion, unless a different joint-(eta,w) theorem is explicitly proved.
  - Bind g_lin to the exact parameterized zero/first eta jet, or provide an independent proof that their difference is itself O(||eta||^2).
  - Declare M2 semantics explicitly. If M2 bounds ||D_eta^2 g|| on the entire chord, use the 1/2 Taylor factor; if M2 already bounds the Taylor remainder coefficient, do not divide by 2 again.
  - Bind one same-cell/whole-chord Hessian envelope and one compatible output-metric cap before promoting the factor-1/4 quartic coefficient.

mathematical_status: CONDITIONAL_PASS / pending

# T-P5-123 — Parametric jet consistency and the sharp Taylor-half closure

## 1. Why this child is needed

The current same-cell graph-jet contract has the schematic form

`||g(eta,w) - g_lin(eta,w)|| <= M * rho(eta)^2`,

uniformly over the admitted parameter range in `w`, followed by a metric conversion of the residual. The requested source-level second-derivative program is sound only if the proposed `g_lin` really removes every eta-degree 0 and eta-degree 1 term at each fixed parameter value. This is not merely a convenience: it is mathematically necessary for any finite uniform quadratic remainder constant.

The same issue controls whether the second-jet constant carries the standard Taylor factor `1/2`. The factor is available exactly when the supplied `M2` is a supremum of the second eta derivative along the whole chord. If `M2` is already the coefficient in a remainder inequality, dividing by two again would be unsound.

Throughout this note, `w` is held fixed while the eta variable is Taylor expanded. Write

`r(eta,w) := g(eta,w) - g_lin(eta,w)`.

The norm on eta and the norm on the output may be any fixed finite-dimensional norms compatible with the stated derivative bounds.

## 2. Necessary zero-jet condition

### Lemma 2.1 — quadratic remainder forces zero-jet matching

Assume that for a fixed admitted `w` there are `M < infinity` and a neighborhood of `eta=0` such that

`||r(eta,w)|| <= M ||eta||^2`.

Then necessarily

`r(0,w)=0`.

### Proof

Set `eta=0`. The right side is zero, hence `||r(0,w)||<=0`, so `r(0,w)=0`. QED.

If this estimate is asserted uniformly for every admitted `w`, the conclusion is pointwise in the parameter:

`g_lin(0,w)=g(0,w)` for every admitted `w`.

Thus any omitted `w`-dependent eta-degree-0 term destroys the desired quadratic contract immediately at the base state.

### Exact regression A — omitted parameter-dependent zero-order term

Take the scalar map

`g(eta,w)=w`, `g_lin(eta,w)=0`.

At `eta=0,w=1`,

`|g-g_lin|=1`, while `M eta^2=0`

for every finite `M`. Therefore no quadratic remainder estimate exists on any parameter domain containing `w=1`.

## 3. Necessary first-jet condition

### Lemma 3.1 — quadratic remainder forces first-jet matching

Assume in addition that `r(.,w)` is Frechet differentiable at `eta=0`. If

`||r(eta,w)|| <= M ||eta||^2`

holds near zero, then

`D_eta r(0,w)=0`.

### Proof

For any direction `u`, put `eta=t u`. By Lemma 2.1, `r(0,w)=0`. Hence

`||r(tu,w)-r(0,w)|| / |t| <= M |t| ||u||^2`.

Let `t -> 0`. Differentiability gives

`||D_eta r(0,w)[u]|| = 0`.

Since `u` is arbitrary, `D_eta r(0,w)=0`. QED.

Consequently, if `g_lin` is affine in eta, the only affine eta-linearization compatible with a uniform quadratic residual is

`g_lin(eta,w) = g(0,w) + D_eta g(0,w)[eta]`

for every admitted `w`.

More generally, a nonlinear proposed `g_lin` need not equal that affine expression globally, but it must have the same zero and first eta jets at `eta=0`.

### Exact regression B — omitted mixed parameter/eta linear term

Take

`g(eta,w)=eta*w`, `g_lin(eta,w)=0`.

At `w=1`, the residual is `|eta|`. If a finite `M` satisfied `|eta| <= M eta^2` for every sufficiently small nonzero `eta`, division by `|eta|` would give `1 <= M |eta|`, impossible as `eta -> 0`.

Therefore a mixed term such as `eta*w` cannot be treated as second order in eta merely because it is mixed in the full variable list. When `w` is a parameter and is not small, it is first order in eta and must be included in the first jet.

## 4. Sharp same-chord Taylor remainder

### Theorem 4.1 — parametric second-order Taylor bound with sharp factor 1/2

Fix an admitted `w`. Assume:

1. the entire chord `{(s eta,w): 0<=s<=1}` lies in the certified same-cell source domain;
2. `g(.,w)` is twice differentiable along that chord;
3. for every `s in [0,1]` and every eta-direction `u`,

   `||D_eta^2 g(s eta,w)[u,u]|| <= M2 ||u||^2`.

Define the exact parameterized first-jet linearization

`g_jet(eta,w) := g(0,w) + D_eta g(0,w)[eta]`.

Then

`g(eta,w)-g_jet(eta,w)
 = integral_0^1 (1-s) D_eta^2 g(s eta,w)[eta,eta] ds`,

and therefore

`||g(eta,w)-g_jet(eta,w)|| <= (M2/2) ||eta||^2`.

### Proof

Let `phi(s)=g(s eta,w)`. The one-dimensional integral Taylor identity is

`phi(1)=phi(0)+phi'(0)+integral_0^1 (1-s) phi''(s) ds`.

Here `phi'(0)=D_eta g(0,w)[eta]` and `phi''(s)=D_eta^2 g(s eta,w)[eta,eta]`. Taking norms and applying the assumed Hessian bound gives

`||remainder|| <= integral_0^1 (1-s) M2 ||eta||^2 ds
                 = (M2/2)||eta||^2`.

QED.

### Sharpness

The factor `1/2` cannot be improved from Hessian-supremum information alone. In one dimension take

`g(eta,w)=(M2/2) eta^2`.

Then `g(0,w)=0`, `D_eta g(0,w)=0`, `D_eta^2 g=M2`, and at every eta

`|g(eta,w)|=(M2/2) eta^2`.

Thus equality is attained.

## 5. Metric consequence: factor-1/4 quartic cap

Suppose the output residual is measured by the positive semidefinite quadratic form `q_H`, and the source supplies a compatible metric/operator cap

`q_H(d) <= rho_H^2 ||d||^2`

for every output residual vector in the relevant range.

Applying Theorem 4.1 to `d=r(eta,w)` yields

`q_H(r) <= rho_H^2 * (M2^2/4) * ||eta||^4`.

If the current radial notation is

`rho(eta)^2 = ||eta||^2`,

then

`q_H(r) <= (rho_H^2 M2^2 / 4) rho(eta)^4`.

If the same certified cell also has

`rho(eta)^2 <= R_cell^2`,

then

`rho(eta)^4 <= R_cell^2 rho(eta)^2`,

so the additive metric defect has the linearized cell envelope

`q_H(r) <= delta_cell rho(eta)^2`,

with

`delta_cell := (rho_H^2 M2^2 R_cell^2)/4`.

This is four times smaller than the coefficient `rho_H^2 M2^2 R_cell^2` when, and only when, the symbol `M2` denotes a genuine whole-chord Hessian supremum as in Theorem 4.1.

### Semantic guard: do not divide twice

There are two distinct conventions that must not be conflated:

- **Hessian convention:** `M2_H` bounds `||D_eta^2 g||`. Then the Taylor remainder coefficient is `M2_H/2`, and the metric quartic coefficient contains `M2_H^2/4`.
- **Remainder convention:** `M2_R` is already defined by `||r|| <= M2_R rho^2`. Then the metric quartic coefficient is `rho_H^2 M2_R^2` with no additional factor `1/4`.

A trusted checker must know which semantic object the source constant represents. A symbol-only rewrite `M2 -> M2/2` is not safe.

## 6. Why basepoint Hessian data do not suffice

### Exact regression C — basepoint Hessian can vanish while the finite remainder is arbitrarily large

For arbitrary `N>0`, take the scalar function on the cell `eta in [0,1]`

`g_N(eta)=N eta^3`.

At the base point,

`g_N(0)=0`, `g_N'(0)=0`, `g_N''(0)=0`.

Thus any procedure inspecting only the second derivative at the base point would report zero curvature. But at `eta=1`,

`g_N(1)-g_N(0)-g_N'(0)=N`.

Since `N` is arbitrary, no finite whole-cell quadratic remainder constant can follow from the basepoint Hessian value alone.

The missing fact is exactly the whole-chord bound: here

`g_N''(s eta)=6N s eta`,

which becomes large away from the base point. Therefore the source certificate must cover the normalized segment used by the Taylor integral, not just the endpoint/base jet.

## 7. Parameter treatment boundary

This theorem holds with `w` fixed along the eta chord. That matches the intended interpretation in which `w` indexes a family of eta-dynamics/graph jets. If the actual source path changes `w` simultaneously with eta, then the relevant second derivative is the second derivative along the joint path, and terms involving `D_eta D_w g`, `D_w^2 g`, and the path derivative of `w` generally enter. One must not reuse the fixed-w theorem silently in that situation.

Conversely, the fact that `w` may be large does not harm the theorem if `g(0,w)` and `D_eta g(0,w)` are retained exactly and the Hessian constant is uniform over the admitted `w` range.

## 8. Failure taxonomy

The following outcomes should be kept distinct:

1. `ZERO_JET_MISMATCH`: some admitted `w` has `g(0,w) != g_lin(0,w)`. Then an `O(rho^2)` remainder is impossible if `rho=0` is in the domain.
2. `FIRST_JET_MISMATCH`: zero jets match, but `D_eta g(0,w) != D_eta g_lin(0,w)`. Then a uniform `O(rho^2)` remainder is impossible on any neighborhood of zero.
3. `BASEPOINT_HESSIAN_ONLY`: the source provides only `D_eta^2 g(0,w)`. This does not certify a finite-cell Taylor remainder.
4. `WHOLE_CHORD_HESSIAN_BOUND`: the source provides the needed segment-wise Hessian envelope. Then the sharp `1/2` norm remainder factor is available.
5. `M2_ALREADY_REMAINDER_COEFFICIENT`: the source has already integrated the Taylor factor. Then applying another `1/2` is invalid.

These are mathematical distinctions, not provenance labels.

## 9. Formalizable theorem statements

The following are intentionally small leaves suitable for later Lean or kernel-facing formalization.

### `quadratic_remainder_forces_parametric_zero_jet`

For fixed `w`, if `0` belongs to the eta domain and

`forall eta, ||r eta w|| <= M * ||eta||^2`,

then `r 0 w = 0`.

### `quadratic_remainder_forces_parametric_first_jet`

For fixed `w`, if `r` is differentiable at `0`, `r 0 w=0`, and locally

`||r eta w|| <= M * ||eta||^2`,

then `fderiv_eta r 0 w = 0`.

### `parametric_taylor_second_order_half`

For fixed `w`, under whole-segment twice differentiability and

`||D_eta^2 g(s eta,w)[eta,eta]|| <= M2 ||eta||^2`,

prove

`||g(eta,w)-g(0,w)-D_eta g(0,w)[eta]|| <= (M2/2)||eta||^2`.

### `metric_quartic_cap_from_parametric_second_jet`

From

`q_H(d) <= rho_H^2 ||d||^2`

and the preceding theorem, derive

`q_H(r) <= (rho_H^2 M2^2 / 4) ||eta||^4`.

### `affine_cell_cap_from_quartic_remainder`

From `||eta||^2 <= R_cell^2`, derive

`q_H(r) <= (rho_H^2 M2^2 R_cell^2 / 4)||eta||^2`.

### Regression lemmas

- `missing_w_zero_order_breaks_quadratic_remainder`
- `missing_eta_w_mixed_linear_breaks_quadratic_remainder`
- `basepoint_hessian_only_insufficient`

## 10. Failed proof routes / excluded shortcuts

- Treating every term involving `w` as higher order is false when the small variable is eta and `w` is only a bounded parameter. `eta*w` is first order in eta.
- Checking the Hessian only at `(eta,w)=(0,w)` cannot control a finite cell; `N eta^3` is an exact obstruction.
- Replacing a Hessian supremum by an already-integrated remainder constant and still inserting `1/2` double-counts Taylor integration.
- Replacing the fixed-`w` chord by a path on which `w` changes requires new mixed derivative terms and is a different theorem.

## 11. Minimal next source packet

For each admitted same-cell `(eta,w)` family, the smallest useful packet is:

1. exact source expressions for `g(0,w)` and `D_eta g(0,w)`;
2. an explicit statement that `g_lin` has exactly those zero/first eta jets;
3. a whole-chord bound for `D_eta^2 g(s eta,w)` with `w` fixed, together with a precise definition of the norm used to define `M2`;
4. a compatible output metric cap `q_H(d)<=rho_H^2||d||^2` or a stronger direct PSD/operator witness;
5. a certified cell radius `rho(eta)^2<=R_cell^2` if the quartic remainder is to be converted into an affine-in-energy defect budget.

If item 2 fails, no finite second-order remainder constant can repair the contract near `eta=0`; the linearization itself must change. If item 3 is unavailable but a direct remainder coefficient is available, use that coefficient without the extra `1/2`.

## 12. Non-upgrades

This result is a mathematical child only. It does **not** establish actual source binding, source-code correspondence, same-cell path coverage, Float64/finite-difference/controller semantics, P8 coverage, Lean/kernel closure, provenance, receipt/admission, registry promotion, or P5/M4 closure. Those remain pending.
