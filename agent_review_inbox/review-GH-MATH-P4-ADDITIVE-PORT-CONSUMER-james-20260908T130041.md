---
kind: review_result
review_id: review-GH-MATH-P4-ADDITIVE-PORT-CONSUMER-james-20260908T130041
task_id: GH-MATH-P4-ADDITIVE-PORT-CONSUMER
source_agent: James-local-takeover
created_at: 2026-09-08T13:00:41-06:00
inspected_commit: 93792eb9312837d5a47421fcff116f131b1ebbe5
status: pending
integration_status: pending
admission_label: pending
proof_status: EXISTING_ADDITIVE_CONSUMERS_LOCATED_SOURCE_INSTANCE_OPEN
source_binding_proven: false
runtime_verified: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: supply a same-cell signed residual identity and matching-metric additive squared cap to the existing generic Schur consumer; do not overwrite the homogeneous consumer or erase bias
---

# Minimal additive-port consumer contract

## 1. Decision

There ARE existing additive-cap consumers. For block456 the shortest algebraic
route is `RouteBP4032GenericSchurAllocation20260908.combined_of_port_budget`,
with n=3 and a supplied metric transport. It accepts `sq r <= W` directly;
W need not vanish with a block coordinate. No new homogeneous-gain assumption,
synthetic example, or modification of the physical scalar consumer is needed.

This is source/interface inspection, not a compiled cross-module instance.
No current theorem, source packet or admission status is upgraded. Some files
carry historical uncompiled comments; this review does not resolve or override
their compile histories. No Lean, first-slab checker, countermodel rerun,
Monte Carlo, or regression was executed. Only this immutable review is added.

The previous remote-contract review is
`review-GH-MATH-P4-PHYSICAL-SCHUR-REMOTE-CONTRACT-james-20260908T125352.md`.
Its slab check is not rerun and is not used as an actual-port witness here.

## 2. Existing consumers: exact acceptance boundaries

Files abbreviated below are under
`examples/routeb_p5_feasible_cone_spn_proof_attempt/`, unless specified.

| Consumer | Actual input and conclusion | Additive-port suitability |
|---|---|---|
| `GenericSchurAllocation20260908.combined_of_port_budget` | lam>1, `sq r<=W`, nonnegative Schur numerator; concludes `target<=base-sq(ell+r)` | Preferred for n=3. W can be a pure additive cap. Exact residual/metric/target identities remain external. |
| `NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.joint_of_signed_defect_caps` in `routeb_p4_schur_joint_threshold_lean` | two exact scalar identities, `u<=U`, `s<=S`, `D<=Dcap`, two allocations | Keeps signed cancellation. Dcap is independently required; dual projections alone cannot determine it. |
| `RelativeAdditive.force_relative_additive` | `r=R a+MBD J eD+eB`; action bound for MBD J; ED/EB squared envelopes | Genuine relative-plus-additive force branch, but physical types are fixed B=(4,5), D=(1,2,3,6). Not a direct block456 instance. |
| `RelativeAdditive.accel_relative_additive` | `r=R a+MBD eD+eB`; action bound for MBD | Acceleration branch; do not insert J again. Same 2+4 dimensional restriction. |
| `RelativeAdditive.consume_weighted_budget` | already proved scalar `q<=weightedBudget`; affine ED/EB envelopes | Scalar conclusion is dimension-independent, but caller must first supply the correct weighted inequality. |
| `SchurPMIAbsorption.schur_pmi_margin` | affine q budget, positive slack and separately supplied `energy-q<=margin` | Keeps `biasEff` as a debit; it does not manufacture the Schur comparison. |
| `PhysicalSchurBinding.ExplicitResidualEnclosure` in `routeb_physical_schur_binding_lean` | `residual(state,y)^2<=beta^2*y^2` | NOT an additive interface. Cannot fill it from a constant W. |
| `P5MixedRelativeAdditive.residual_power_bound` / `block45_pareto_mixed_residual_decay` in `routeb_p5_mixed_relative_additive_lean` | `|l_i|<=rho_i|u_i|+b_i`, plus the fixed block45 derivative/coercivity identities | A different power/decay consumer. Norm-squared W is not b; physical channel selection and b_i^2 caps must be proved. Not a substitute for the block456 Schur target. |

The full filenames for the first five entries have prefix `NEW_P4_032_` and
suffix `.lean`; hashes are listed below. These are alternative mathematical
routes, not independent allowances to debit cumulatively.

## 3. Minimal recommended same-cell interface

Fix a source state type, a cell predicate Omega, B/D coordinate embeddings,
one configuration and nominal metric H. Choose either:

```text
direct port:    p(x) = M_BD(x) a_D(x),
forced defect:  p(x) = L(x) g_D(x),  L(x)=M_BD(x) J(x).
```

For the forced-defect branch the retained nominal term `R a_B` must already
be included in the baseline. For the direct branch it must NOT be added again
if p already includes the whole remote acceleration contribution.

Require a signed source decomposition for the actual target vector:

```text
d(x) = sigma * p(x), sigma in {+1,-1},
l_actual(x) = v_ref(x) + d(x),
P_actual(x) = beta(x) - l_actual(x)^T H l_actual(x).
```

If local/assembly defects are nonzero, include them in d or in v_ref with
their own proved identities and caps. Neither may be silently set to zero.
In the `p=L g_D` route a common baseline is `v_ref=ell+R a_B`, but that choice
still needs the actual source equality.

Supply a real linear map T and metric identity

```text
forall v, sq(T v) = v^T H v,
forall x in Omega, d(x)^T H d(x) <= Delta(x).
```

The map may be cell-specific; use the SAME map on baseline, port and total
at each application, with all identities uniform on that cell. An exact
factor/square-root or a direct metric theorem can justify it; Pi/sup norm,
unweighted Euclidean norm, current M_BB^-1 and nominal H are not interchangeable.

Then instantiate the existing generic consumer pointwise:

```text
n=3, ell=T(v_ref(x)), r=T(d(x)), W=Delta(x), base=beta(x),
lam(x)>1,
(lam-1)*(beta-target-lam*Delta) - lam*v_ref^T H v_ref >= 0.
```

Its conclusion is `target(x)<=P_actual(x)`. The three nontrivial caller
obligations are source decomposition, H-metric cap, and target allocation.
A pure additive cap is already accepted; rho<1 and energy-based absorption
are not necessary premises of this route. Nor does the conclusion by itself
establish a physical PMI theorem unless P_actual is identified with its target.

If a proved cap for the complete port already exists, use it directly as W.
Do not split/recombine solely to introduce a looser relative coefficient.

## 4. Signs: port, condensed forcing and O1 conventions differ

From `M a=F+epsilon`, remote elimination gives

```text
p_B=M_BD a_D=L(F_D+epsilon_D-M_DB a_B),
Schur(M) a_B=F_B+epsilon_B-L(F_D+epsilon_D).
```

Thus p_B has a positive definition but a negative contribution in the
condensed forcing. A norm cap is invariant under global sign reversal;
the cross term with a fixed baseline is not. Record sigma in the source
identity, not just in a comment attached to W.

`DefectConventionCore.adapt` already makes the force/O1 distinction explicit:

```text
eD_O1=F_D+epsilon_D-M_DD aD0-MDB0 a_B,
eB_O1=-epsilon_B,
rB_O1=F_B-M_BB a_B-M_BD aD0.
```

Only after the supplied balances and reference/inverse identities does its
O1 branch give `rB_O1=R a_B+L eD_O1+eB_O1`. This rB is not automatically the
positive p_B or the consumer's total residual. The adapter changes variables
as well as signs and is fixed to the 2+4 partition.

For the signed-gate alternative, use the exact same signed d and define
`u=ell^T H d`, `s=(ell+r0)^T H d`, `D=d^T H d`.
The existing gate needs both
`Pactual=beta-L0-2(c0+u)-Qactual` and `Pactual=P0-2s-D`, where
`L0=ell^T H ell`, `c0=ell^T H r0`, `Qactual=(r0+d)^T H(r0+d)`.
Provide U,S,Dcap and the exact allocations printed in that consumer.
Keeping the signed identity permits cancellation; taking an absolute cap
for safety is allowed but must not be mislabeled as the exact signed value.

## 5. Relative/additive fields, when that branch is actually needed

For the existing typed force branch take `eD=g_D` only if the proved source
identity really is `r=R a+MBD J g_D+eB`. Supply

```text
||g_D||_2^2 <= ED <= kappaD*energy+biasD,
||eB||_2^2  <= EB <= kappaB*energy+biasB,
ActionBound(MBD J,tau), ||R a||_2^2<=rhoA*energy.
```

A uniform additive force cap is the special case kappaD=0, biasD=EDcap;
it does NOT imply biasD=0. For acceleration data use the acceleration branch,
ActionBound(MBD,tau), and a bound on the actual acceleration/deviation named
by that branch's identity. Units distinguish force and acceleration defects.

`Weights` requires all three weights positive and sum(1/weight)<=1. The result is

```text
rhoEff = w0*rhoA + w1*tau^2*kappaD + w2*kappaB,
biasEff = w1*tau^2*biasD + w2*biasB,
q <= rhoEff*energy+biasEff.
```

For dense H, the action bound must concern the correctly transported operator
(e.g. T MBD J), not merely the unweighted MBD J. A 3+3 source cannot be padded
or relabeled into the fixed 2+4 physical types without a proved embedding.

`SchurPMIAbsorption` further requires delta>0, rhoEff+delta<=1 and the independent
`SchurPMIBinding.lower`. It yields `delta*energy-biasEff<=margin`; a target t
still requires `t+biasEff<=delta*energy`. Positive slack alone does not erase
the additive load. No feedback or trajectory closure is implied.

## 6. Exact witness fields still needed (proposed attachment, not implemented)

| Field | Required mathematical/source content |
|---|---|
| `cell_key`, `cell_predicate`, `embedding`, `coverage` | exact cell and state/time embedding; point membership or uniform quantified range; verified coverage if claiming a full domain |
| `configuration_key` | B/D order, units, mu and its semantics, controller/effective runtime parameters, reference and storage conventions |
| `source_pins` | mass/force/solve/reference/consumer artifact hashes, dependency and evaluator identity; execution/refinement evidence separately |
| `port_kind`, `port_identity` | distinguish MBD*aD from L*gD and prove it for the actual valuation; preserve J/remote-balance witnesses when used |
| `sign_and_total_identity` | actual sigma, baseline, local defects, actual target vector and scalar Pactual |
| `metric_identity` | H=M0_BB^-1 for this reference/order and T-metric equality, or a proved direct metric formulation |
| `additive_cap` | uniform `d^T H d<=Delta`, or separately typed operator/force caps that imply it; squared quantity and units explicit |
| `allocation` | same-cell lam>1 and Schur numerator inequality, or the signed gate's U/S/Dcap and both allocations |
| `consumer_binding` | exact consumer function, target and normalization; initial/path obligations remain separate |
| `receipt` | independent checking of the actual instantiated theorem/packet, pins and audit under existing admission rules; no inference from a review hash alone |

Hash equality is identity metadata, not a proof of any row above. Quantification
over Omega must not be replaced by a single sample, a q-only unrelated cell,
or a synthetic rational fixture. In a scalar consumer requiring all state/y
arguments, restrict to the intended admissible domain through a genuine typed
contract rather than claiming the larger quantification from cell-local data.

## 7. Minimal change recommendation and admission

Since a generic additive-W consumer exists, **do not alter existing consumers**.
The smallest future code addition is a separate same-cell source adapter with
the fields in section 6, plus its concrete typed invocation of
`combined_of_port_budget`. This review does not implement that adapter.
Generalizing the 2+4 force branch is optional, not required for the direct W path.

If callers insist on preserving the old scalar physical-PMI entry point, an
OPTIONAL separate additive variant could consume `r^2<=beta^2*y^2+B`, B>=0,
and epsilon>0, yielding

```text
p*x^2+2*x*r+d*y^2 >=
 (p-epsilon)*x^2+(d-beta^2/epsilon)*y^2-B/epsilon.
```

This is a proposed algebraic interface, not a new proved/compiled declaration.
The debit B/epsilon must remain; it is not the old nonnegativity theorem.
Do not overwrite `ExplicitResidualEnclosure.sq_le` or reinterpret its existing
receipts. No gate relaxation, registry promotion or automatic formal admission
is proposed. The whole attachment remains pending until actual witnesses and
the existing independent verification/admission requirements are satisfied.

## 8. Byte provenance inspected this turn

Prefix P = `examples/routeb_p5_feasible_cone_spn_proof_attempt/`.

| File | SHA-256 |
|---|---|
| P/NEW_P4_032_GenericSchurAllocation20260908.lean | a76375770d563f86f7de80fdea970e8d0d0fadd1ed917c262b725c7a8ba47648 |
| P/NEW_P4_032_RelativeAdditive.lean | 6db219f352aeb2fb0c5ad0985154ba65fbb7f59144a22c5b7a7ccf5e63f5eadd |
| P/NEW_P4_032_SchurPMIAbsorption.lean | f18f9fb180aefaad0dc3cd5149894d03ee111db5c45abfb86caa927df4050e3 |
| P/NEW_P4_032_DefectConventionCore.lean | 151044c8b316e1e2119eea029e0b3a71e79a78f90d180778a915a9bca7d3e034 |
| P/NEW_P4_032_BlockDefects.lean | aa1cce18e39b1b675483c9ece7cecbc1a2740c65df1846582ca57963c0a6cc51 |
| P/NEW_P4_032_DefectNormBudget.lean | 9d50b4ee96228f0b70db408e1bca7e58b4a77bbdaebebb1fb733ef66470693ad |
| P/NEW_P4_032_WeightedThreeTerm.lean | 8e339369ac522eed18e6db3e62d6d1c467aa631c563eecc7b16e725823b15600 |
| examples/routeb_physical_schur_binding_lean/PhysicalSchurBinding.lean | bf9678f8595c03006eaa2eb99a7398599468fb88f669553ea312686019558adf |
| examples/routeb_p4_schur_joint_threshold_lean/NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.lean | 91a3a598ba6c6fb0278a127c8b94a34839f74eb3cd88d46b6d2ca4d4169c5ba7 |
| examples/routeb_p5_mixed_relative_additive_lean/P5MixedRelativeAdditive.lean | 782e86afa7e20922e7dd4978d7d385cd5600b97ce44b23d4c5b6976c5c157572 |

No concrete source coefficients/caps are imported into these interfaces by this
review. Historical author labels and previous review results are unchanged.
