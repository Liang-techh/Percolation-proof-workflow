---
kind: review_result
task_id: T-P5-026
review_id: review-T-P5-026-ORBITFIBER-SPN-DAG-20260914T212915Z
source_agent: Codex
agent: Codex
created_at: 2026-09-14T21:29:15Z
inspected_commit: e5f3f7ec984511e5eec1fc17ff9cb17a652e00ec
reviewed_candidate: NEW_CONE_INDEX_OrbitFiber20260914
status: compiled_candidate
integration_status: pending
admission_label: pending
lean_actually_run: true
lean_validation: local_stdin_source_bundle_pass
lean_exit_code: 0
checker_exit_code: 0
new_axiom_reports: 8
total_axiom_reports: 67
axiom_audit: pass_allowlist
standalone_module_imports_verified: false
cached_mathlib_authenticated: false
admission_verified: false
sidecar_is_receipt: false
theorem_DAG_mutated: false
concrete_K_path_bound: false
source_coverage_verified: false
P5_closed: false
registry_eligible: false
state_mutated_by_this_task: false
registry_mutated_by_this_task: false
---

# OrbitFiber review: shortest conditional SPN bridge and weighted audit lane

## Conclusion

The fixed-state multiplicity result is sound as a label-count interface, but
does not itself transport an SPN certificate. The shortest pointwise proof
retains the two oriented charts and supplies a shared representative quadratic
gap identity. No multiplicity factor is needed in that proof.

Two source-independent children are now implemented for DAG review, NOT inserted
into the DAG: the direct 18-certificate consumer and an optional, exactly
multiplicity-preserving weighted-gap equivalence. These are typed against the
existing GENERIC P5 sidecar, not merely proposed pseudocode.

## Direct child: `eighteen_spn_envelope`

All new declarations live in `RouteBP5ConeIndexSPNBridge`. Write

```text
G(z) = mu*Q(z) - RouteBP5FeasibleConeSPN.absEnvelope K (L z) z
T(r,b,u) = RouteBP5ConeIndex.chart (expand (r,b)) u
r : Representative = Fin 3 × Cone            -- 18 labels
b : Bool                                    -- both orientations
u : Fin 4 → Real, Orthant u
```

The minimal additional identity at the consumer boundary is:

```text
hgap : forall r b u, Orthant u -> G(T(r,b,u)) = quad (H r) u
```

Together with `H r = S r + N r` entrywise, `IsPSD (S r)`, and entrywise
nonnegative `N r`, the child proves `forall z, absEnvelope K (L z) z <= mu*Q(z)`.
It instantiates the existing `global_abs_envelope_of_spn` with index
`Representative × Bool`, concrete `T`, and `H/S/N` lifted by first projection.
`signed_representative_cover` supplies its cover premise. Thus only 18 sets of
matrix data are used while both chart orientations remain explicitly covered.

The smaller upstream obligations that construct `hgap` are:

1. `hrep : forall r u, Orthant u -> G(chart (representativeCone r) u) = quad (H r) u`.
2. `heven : forall z, G(-z) = G(z)`.

`signed_gap_of_even` combines these, preserving the SAME nonnegative `u` under
global chart reversal. `p5_gap_even` discharges the scalar evenness from
`Q(-z)=Q(z)` and `L(-z)=-L(z)`, using the existing P5 absolute-envelope theorem.
It does not assume residual, membership, or source-code sign invariance.

`residual_power_of_envelope` then attaches the existing component residual
power bound, retaining the explicit premise
`forall a, abs(r a) <= rowEnvelope K z a`. No actual residual/source envelope is
constructed. Neither `mu<1` nor a trajectory/decay conclusion is asserted.

## Optional child: `envelope_iff_weighted_nonneg`

Let `C_z` be all covering LABELS and `R_z` the covering ORBIT support, where an
orbit is included if either of its two orientations contains `z`. For an
arbitrary same-state scalar function `G`, the new `weighted_gap_factor` proves:

```text
sum_c (if Member c z then G(z) else 0) = kappa(z) * G(z)
kappa(z) = if z=0 then 2*card(R_z) else card(R_z)   -- Nat cast to Real
```

This explicitly consumes OrbitFiber's `exact_multiplicity_formula`.
Coverage gives `kappa(z)>0`; `weighted_gap_nonneg_iff` therefore proves that the
sum is nonnegative iff `G(z)` is nonnegative, without division by a count.
`envelope_iff_weighted_nonneg` substitutes the ACTUAL generic P5 `p5Gap` into
that equivalence. This is the precise typed attachment of fixed-state
multiplicity to P5 if a later checker/DAG lane aggregates over covering labels.
It is not an independent proof that the weighted sum is nonnegative.

## Three boundaries that must remain separate

| Boundary | Valid conclusion | Invalid shortcut |
|---|---|---|
| `z=0` | 18 covering orbits but 36 covering labels. Weighted bookkeeping retains factor 2. | Replace the origin's label count by 18. |
| `z!=0` | One covering orientation per covering orbit; different boundary orbits may still overlap. | Infer that the positive representative chart contains `z`, or that every weight is orientation invariant. |
| Weighted witnesses | Full reindexing to `(r,b,u)` preserves arbitrary weights; replacing both orientations by one weight needs an explicit value-transport identity. | Use uniqueness of `b` to identify `W(flip c,u)` with `W(c,u)`. |

For a concrete guard against the last shortcut, take `c=(nn,pp)` and
`z=(-1,1,-1,1)=chart c (1,1,1,1)`. The selected representative is `(pp,nn)`
with orientation `true`. The weight `W(c,u)=1` for true orientation and `0`
for false orientation has value 1 at the covering label and 0 at its positive
representative. Geometry does not identify these values. Likewise the
non-even predicate `z[0]>=0` holds on all 18 positive representative charts
but fails at this state. These are guards against invalid generic inferences,
NOT counterexamples to the actual P5/SPN claim.

If a weighted sum uses `W(c,coordinates c z)`, the sufficient same-state binding
is `W(c,u)=G(chart c u)` on admissible witnesses. In an SPN implementation it is
the exact gap identity that provides this binding. Matrix invariance
`H(flip c)=H(c)` is another sufficient way to reuse a quadratic certificate
at the same `u`; it still does not make `Member (flip c) z` equal `Member c z`.

The direct SPN path includes `u=0` in its gap contract. `signed_gap_origin`
proves `G(0)=0` from that contract, using `chart c 0=0` and `quad H 0=0`.
Thus no extra numerical origin budget is added. If a future interface checks
only nonzero states, it must separately prove the origin case; evenness or
the number 18 alone cannot do so. The count factor 2 is bookkeeping, not a
doubling of `mu` in the pointwise inequality.

## Proposed DAG edges and exact remaining leaf

Suggested child names below are proposals only; no node/registry was created.

| Proposed child | Implemented theorem / required incoming edges |
|---|---|
| `P5_SIGNED_REP_GAP` | `p5_gap_even` plus `signed_gap_of_even`; needs even `Q`, odd `L`, and the typed `hrep` identity. |
| `P5_18_SPN_CONSUMER` | `eighteen_spn_envelope`; needs signed cover, signed gap, and 18 conditional SPN premises; reuses generic P5 `global_abs_envelope_of_spn`. |
| `P5_WEIGHTED_GAP_AUDIT` | `envelope_iff_weighted_nonneg`; depends on OrbitFiber factor correction and covering-label nonemptiness, not on a concrete gain. |
| `P5_COMPONENT_POWER_CONSUMER` | `residual_power_of_envelope`; needs direct envelope and the independently supplied component residual bound. |

The shortest main path is signed gap -> 18-SPN consumer -> component power.
The weighted audit is a separate optional branch, not a required dependency
of the direct SPN consumer.

The remaining source-independent binding leaf is the fully typed `hrep` above
for the frozen physical `L`, `P/Q`, representative charts and constructed `H`.
The older proof-attempt file contains `cone_gap_identity`/`H_flip` statements,
but its Cone/chart objects are a separate namespace-level implementation.
This task has NOT imported and transported those concrete objects.

Import origin is important: both existing `P5FeasibleConeSPN.lean` files declare
the `RouteBP5FeasibleConeSPN` namespace and overlapping names. The new bridge
explicitly targets `examples.routeb_p5_feasible_cone_spn_lean.P5FeasibleConeSPN`.
It does not bundle the homonymous file in `proof_attempt`. The generic P5
consumer has an arbitrary index type, so no Cone equivalence is needed to
connect the NEW core to that consumer. A separate frozen-gap leaf remains
necessary to instantiate its physical polynomial data. Restricted-text Python
agreement cannot replace this typed identity.

Only after that conditional mathematical attachment, actual `K_path`, same-domain
component envelopes and 18 SPN witnesses can instantiate a source-bound claim.
This review supplies none of those inputs and no source/P8/ODE/P5 closure.

## Actual verification and immutable artifacts

New files under `examples/routeb_p5_feasible_cone_spn_proof_attempt/`:

| File | SHA-256 |
|---|---|
| `NEW_CONE_INDEX_SPNBridge20260914.lean` | `da9eba42c611d31e019dbdf4a1f4d06bb7d4e82c5cbdf9c138d98f3278dae10a` |
| `NEW_CONE_INDEX_SPNBridge20260914_check.py` | `3f2f80e6744e4c8c24d032469418165f78596952bc147f2ebce04b6941124fe7` |

Actual final command, from the repository root:

```powershell
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_SPNBridge20260914_check.py --lean C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe --mathlib-packages examples/local_fkg/.lake/packages
```

Final Lean/checker exit codes were 0. All 8 new declarations and 67 total
printed axiom reports passed the allowlist `{propext, Classical.choice,
Quot.sound}`. No final warning or `sorryAx`. The invocation rechecked the
OrbitFiber source and its dependencies as well as the full generic P5 sidecar.
Development failures were confined to the new file: missing classical
decidability, broad finite-sum simplification timeout, and an under-instantiated
function-negation rewrite. These were repaired with a local classical instance,
explicit `Nat.cast_sum`/order lemmas, and an explicitly applied P5 theorem.
No heartbeat limit increase or warning/axiom gate suppression was used.

The exact UTF-8 source bundle SHA-256 is
`080a33c45d982a4b51df006abfa03ac5d5653d37fde315c0b282ada9aa31a7c1`.
The driver pins all existing Lean inputs, substitutes complete source bodies
in memory for mapped imports, invokes `lean --stdin`, and rechecks input hashes
afterward. No `.olean`, generated Lean file, log, receipt, dependency cache or
registry artifact is written. It runs correctly with Python assertions disabled.

Pinned source dependencies, relative to the example directory:

| File | SHA-256 |
|---|---|
| `NEW_CONE_INDEX_Core.lean` | `b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602` |
| `NEW_CONE_INDEX_InverseCover20260908.lean` | `2e4a6dfaca0d564e3fbf3407c6c68b31776c1fced30687d4c8e81e6b90d740c0` |
| `NEW_CONE_INDEX_SignedCoverConsumer.lean` | `ea9a87281e096caf2e3b082a31dd0fbb00efc85016376dbd8ad735b39d41f4b8` |
| `NEW_CONE_INDEX_ConcreteConsumer20260908.lean` | `5f50f2c68713a18d4b490573923315cb2f0a24cfafda3e281f7c1154c1d36205` |
| `NEW_CONE_INDEX_OrbitFiber20260914.lean` | `4df14d1e6174b702dc9ed0d6d45c5021b9f786d0eb577b41347b404eec80ace9` |
| `../routeb_p5_feasible_cone_spn_lean/P5FeasibleConeSPN.lean` | `8a2206d22747bc7c24be65e2d87b31fc23f94e769525a62aabad97326e5385e7` |

This is local elaboration/kernel checking of the source bundle against the
existing Lean 4.32.0/Mathlib environment. Standalone module imports, Lake build,
cached dependency authentication and admission were NOT verified. The local
checker and sidecar are NOT an admission receipt. Status remains compiled
candidate/pending independent review, never registry eligible here.

Read the OrbitFiber candidate and its preceding immutable review, both existing
P5 source variants, and the existing signed-cover/core interfaces. Only the two
new source files and this review were written in this continuation. Previous
reviews, existing P5/ConeIndex files, state, registry and K_path/source artifacts
were not modified by this task; concurrent worktree changes were left alone.
