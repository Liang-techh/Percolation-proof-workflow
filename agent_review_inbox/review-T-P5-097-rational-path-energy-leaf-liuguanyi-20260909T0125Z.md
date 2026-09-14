---
kind: review_result
review_id: review-T-P5-097-rational-path-energy-leaf-liuguanyi-20260909T0125Z
task_id: T-P5-097-RATIONAL-PATH-ENERGY-LEAF
agent: 柳冠一
source_agent: 柳冠一
reviewer: 柳冠一
created_at: 2026-09-09T01:25:00Z
claim_commit: c56b776bc27ae4facaa3a28e702b40d36b5ad0d4
inspected_commit: 256d083bcaaccd7dc78ace48a123d9d39da3b8f6
inspected_paths:
  - agent_review_inbox/review-T-P5-094-variational-to-secant-path-energy-guyuefangyuan-20260908T1832Z.md
  - agent_review_inbox/task_queue.md
upstream_blob_sha: 71273ffdaaa15cbee2f1783660abd066b46881c6
task_queue_blob_sha: dc78918afd223c77b3b9ad0f3326076855f1c3d3
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: consume_as_source_independent_connector_and_piecewise_rational_decay_leaves; keep_sheet_source_binding_and_Lean_separate
commands: none_math_derivation_only
---

# T-P5-097 — rational path-energy leaf: one-sheet connector sandwich and heterogeneous rational decay

## 0. Bottleneck

T-P5-094 already proves the core moving-metric statement: a variational decay theorem can be integrated along a flowed connector, and an equal-step rational factor can replace `exp(-2 mu h)`.  Its infimum-energy theorem, however, is naturally stated by taking an infimum over admissible initial paths.  At the source/interface layer this can become unnecessarily strong: proving that *every* admissible connector can be flowed through the same certified sheet family is often much harder than certifying one canonical connector.

This child gives a source-independent bridge that needs only **one flowed connector sheet**, plus a rational certificate that this connector is not too expensive relative to the initial infimum energy.  It also replaces the equal-rate/equal-time slicing by a heterogeneous exact-rational product, so local contraction margins can be retained instead of collapsed to one global minimum.

No source reification, Float64/FD/controller semantics, P8 flowpipe, Lean/kernel receipt, admission, provenance audit, or registry change is claimed.

## 1. Minimal composition leaf: certified connector implies finite-separation contraction

Let `E_0(gamma)` and `E_h(gamma_h)` be the initial/final path energies from T-P5-094, and let

`D_0(x,y) = inf E_0(gamma)`,

`D_h(Phi_h x, Phi_h y) = inf E_h(eta)`

for the chosen admissible path classes.

Assume one connector `gamma` from `x` to `y` is certified and its flowed image `gamma_h = Phi_h o gamma` is admissible at the final time.  Let exact nonnegative scalars `A,B,C,D` satisfy `A>0`, `C>0` and

**(1.1) path-flow certificate**

`A E_h(gamma_h) <= B E_0(gamma)`,

**(1.2) connector-quality certificate**

`C E_0(gamma) <= D D_0(x,y)`.

Because the final infimum is no larger than the energy of the displayed final path,

`D_h(Phi_h x,Phi_h y) <= E_h(gamma_h)`.

Multiplying only by positive scalars and chaining the inequalities gives the fully division-free theorem

**(1.3) ONE-SHEET FINITE-SEPARATION LEAF**

`A C D_h(Phi_h x,Phi_h y) <= B D D_0(x,y)`.

Thus an all-path initial lifting hypothesis is not logically necessary.  A single source-bound connector sheet is enough once its initial suboptimality is certified.

A useful additive variant is also immediate.  If `E_0(gamma) <= D_0(x,y)+eps`, then

**(1.4)** `A D_h <= B D_0 + B eps`.

Therefore a merely approximate geodesic produces an explicit additive path-selection debit; it must not be reported as homogeneous contraction unless `eps=0` or an independent relative-gap theorem converts it to (1.2).

## 2. Rational connector-quality certificate from a metric sandwich

The remaining question is how to obtain (1.2) without solving a geodesic problem.

Let `K` be a convex initial-state region, let `W_0(z)` be the state-dependent initial metric, and let `W_*` be one fixed symmetric PSD reference matrix.  Suppose exact scalars `m,M` satisfy

`m > 0`, `M >= 0`,

and throughout **the full admissible initial path region `K`**,

**(2.1)** `m Q_{W_*}(v) <= Q_{W_0(z)}(v) <= M Q_{W_*}(v)`

for every `z in K` and tangent vector `v`.

For `x,y in K`, choose the straight connector

`gamma_*(s)=y+s(x-y)`.

Convexity keeps `gamma_*` inside `K`.  Its energy obeys

`E_0(gamma_*) <= M Q_{W_*}(x-y)`.

For any admissible `eta:[0,1]->K` joining `y` to `x`, the lower sandwich and quadratic Jensen/Cauchy give

`E_0(eta)`
` >= m integral_0^1 Q_{W_*}(eta'(s)) ds`
` >= m Q_{W_*}( integral_0^1 eta'(s) ds )`
` =  m Q_{W_*}(x-y)`.

Taking the infimum over `eta` yields

`D_0^K(x,y) >= m Q_{W_*}(x-y)`.

Combining the upper straight-path and lower infimum bounds gives the exact, division-free connector certificate

**(2.2) STRAIGHT-CONNECTOR SANDWICH**

`m E_0(gamma_*) <= M D_0^K(x,y)`.

No inverse metric, square root, geodesic solver, exponential, or eigenvalue is part of the trusted theorem.

Combining (2.2) with (1.1) gives the main bridge:

**(2.3) ONE-SHEET METRIC-SANDWICH CONTRACTION**

`A m D_h(Phi_h x,Phi_h y) <= B M D_0^K(x,y)`.

This is the exact source-independent contract I recommend downstream: source/coverage needs one straight initial connector, one flowed sheet, and quadratic-form sandwich constants `m,M`; it does **not** need to enumerate/flow every admissible initial path.

### Boundary that must remain explicit

The lower bound in (2.1) must hold on the whole path class used to define `D_0^K`, not merely on the straight segment.  If the infimum is allowed to escape into a region where the metric is much smaller, a segment-only lower bound cannot imply (2.2).  The safe typed object is therefore a restricted path domain `K` (or another path class with an independently proved global lower sandwich).

## 3. Heterogeneous exact-rational time slicing

T-P5-094 gives the equal-rate/equal-step rational decay.  The same proof works without flattening local rates.

Let

`0=t_0 < t_1 < ... < t_n=h`, `Delta_k=t_{k+1}-t_k >= 0`.

Assume for every strand parameter `s` of the **same certified flowed connector sheet**, and for `t in [t_k,t_{k+1}]`,

**(3.1)** `d/dt V_s(t) <= -2 nu_k V_s(t)`, with `nu_k >= 0`.

The one-step argument of T-P5-094 gives

`(1+2 nu_k Delta_k) V_s(t_{k+1}) <= V_s(t_k)`.

Multiplying over `k` gives

**(3.2)**

`[product_k (1+2 nu_k Delta_k)] V_s(h) <= V_s(0)`.

Because the product is independent of `s`, integration along the connector yields

**(3.3) HETEROGENEOUS PATH-ENERGY DECAY**

`[product_k (1+2 nu_k Delta_k)] E_h(gamma_h) <= E_0(gamma_0)`.

This retains time-local contraction margins.  For example, two half-intervals with exact rates `nu_0=0`, `nu_1=2` give factor `1*(1+2)=3`, whereas collapsing to the global minimum `min nu_k=0` would certify no decay at all.

### 3.1 Pure integer/rational checker leaf

Write exact nonnegative rationals

`nu_k = a_k/b_k`, `Delta_k = c_k/d_k`, with `b_k,d_k > 0`.

Define

`P_num = product_k (b_k d_k + 2 a_k c_k)`,

`P_den = product_k (b_k d_k)`.

Then (3.3) is exactly equivalent to the denominator-cleared gate

**(3.4)** `P_num E_h <= P_den E_0`.

A relative/signed variational defect from T-P5-091 may be consumed by setting `nu_k=mu_k-rho_k` after separately checking `mu_k>=rho_k`.  No exponential, division, square root, spectral norm, or matrix inverse is required by the checker.

Combining (3.4) and the straight-connector sandwich gives a fully rational finite-separation leaf:

**(3.5)** `P_num * m * D_h <= P_den * M * D_0^K`.

## 4. Minimal typed contract

A practical source-independent packet can be kept very small:

1. `PathDomain K` and endpoints `x,y`, with `segment(x,y) subset K`;
2. fixed reference quadratic form `W_*`;
3. exact `m>0, M>=0` and the uniform quadratic sandwich (2.1) on the initial path class;
4. one connector `gamma_*` and one flowed sheet `gamma_t(s)` with endpoint/flow identities;
5. a finite time partition `t_k` and exact effective rates `nu_k>=0` valid uniformly in `s` on each time slab;
6. the standard T-P5-094 variational-energy identity on that same sheet.

Trusted output is only (3.5).  The packet intentionally separates:

- **geometry**: segment/path-domain membership;
- **metric comparison**: `m W_* <= W_0(z) <= M W_*` as quadratic forms;
- **flow-sheet coverage**: the one actual connector sheet;
- **differential contraction**: local `nu_k`;
- **rational arithmetic**: products in (3.4).

## 5. Suggested formal theorem leaves

Suggested small formal interfaces, without claiming they are already in Lean:

- `pathEnergy_lower_of_metricSandwich`
- `straightPathEnergy_upper_of_metricSandwich`
- `straightConnector_relativeInfimumBound`
- `oneSheet_finiteSeparation_of_connectorBound`
- `rationalDecay_piecewiseRates`
- `pathEnergyDecay_piecewiseRates`
- `oneSheet_metricSandwich_rationalContraction`

The algebraic final leaf should have no matrix inverse or transcendental operation in its statement.

## 6. Open obligations / non-claims

Still OPEN and not upgraded by this review:

- actual source binding for `W_0`, `W_*`, `m,M`, endpoints, path domain, and local `nu_k`;
- proof that the chosen straight connector and its **whole flowed sheet** remain in the derivative/contraction-certified tube;
- if `D_0` is defined over a larger path class than `K`, a lower metric sandwich on that larger class or an explicit restriction theorem;
- state/time-dependent final metric source semantics and any chart/source binding;
- Float64/FD/controller/solve semantics, P8 flowpipe/halo coverage, Lean/kernel verification, independent validation, admission, and registry.

Status is therefore `CONDITIONAL_PASS / pending`: the mathematical connector and rational checker decomposition are closed, but no deployed P5/P8 parent is closed.
