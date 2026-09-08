---
kind: review_result
task_id: T-P5-026
review_id: NEW_CONE_INDEX_ConcreteConsumer20260908
created_at: 2026-09-08
inspected_commit: 282de6327682b3c6aca64dfd310e9b05be163e71
status: pending
integration_status: pending
admission_label: pending
lean_validation: local_source_bundle_pass
standalone_module_imports_verified: false
concrete_K_path_bound: false
P5_closed: false
registry_eligible: false
state_mutation: false
registry_mutation: false
---

# P5-026 concrete ConeIndex consumer: source-independent only

## Scope and inspected inputs

Read `P5FeasibleConeSPN.lean`, `NEW_exact_geometry_spn.py`, the two P5-026
reviews `review-T-P5-026-guyuefangyuan-20260907T1031.md` and
`review-T-P5-026-juyangxianzun-20260907T1048.md`, and existing ConeIndex core,
checker, review and generic SignedCoverConsumer. Historical remote compile
claims in the reviews were not refreshed or adopted as current evidence.

The requested finite abstraction already exists in `NEW_CONE_INDEX_Core.lean`.
This turn does not overwrite it. It adds a typed consumer instantiation and
membership covariance, with a fresh local check of the existing core as well.
Only these three new files were written in this example directory:

- `NEW_CONE_INDEX_ConcreteConsumer20260908.lean`
- `NEW_CONE_INDEX_ConcreteConsumer20260908_check.py`
- this review.

No existing P5 file, state, registry, K_path/source artifact, Lake configuration,
or dependency cache was written. No commit, CI dispatch, or integration was run.
The worktree already contained unrelated concurrent changes; these were not
reverted or attributed to this task.

## Minimal interface and actual new contribution

The unchanged core defines:

```text
Cone = pp | nn | pnPos | pnNeg | npPos | npNeg
ConeIndex = Cone x Cone                          cardinality 36
Representative = Fin 3 x Cone                    cardinality 18
representativeFirst = [pp, pnPos, pnNeg]
flip(c4,c5) = (reverse c4, reverse c5)
indexEquiv : ConeIndex ≃ Representative x Bool
```

The involution has no fixed labels. Each representative fiber has exactly two
labels. Selection preserves the second channel only for the positive orientation;
otherwise it reverses BOTH channels. Fin-3 representative ranks correspond to
original Python cone IDs `(0,2,3)`, not `(0,1,2)`.

The new file imports the actual core and generic consumer, without duplicating
their charts or re-encoding the finite enumeration:

| New interface | Meaning |
|---|---|
| `oriented_eq_expand` | Generic oriented chart equals the concrete expanded chart. |
| `concrete_signed_cover` | Supplies the concrete real-state cover to the generic consumer. |
| `all_iff_signed` | An arbitrary state predicate requires both orientations. |
| `all_iff_even_representatives` | Exactly 18 representative tests suffice given explicit `P(-z) ↔ P(z)`. |
| `orientedCoverWitnessEquiv` | Bijection of every `(label,u)` cover witness with `(representative,Bool,u)`. |
| `member_flip_iff` | `Member (flip c) z ↔ Member c (-z)`. |
| `multiplicity_neg` | Total label membership count is even in the state. |

The witness equivalence retains the identical orthant parameter vector; it does
not choose one cone at a boundary. State coordinates remain `(x4,x5,y4,y5)` and
parameters remain `(a4,a5,b4,b5)`.

The core's arbitrary-weight sum identity retains both summands per representative.
At the origin there are still 36 covering labels, even though all chart values
are zero. This is not a partition into 18 disjoint regions and not a `Finset.image`
deduplication by specialized matrix values. Membership of a fixed label at a
fixed state is not assumed even. Only the total count is proved even by reindexing.

The new adapter is typed between the ConeIndex core and SignedCoverConsumer.
It is NOT a typed bridge to `RouteBP5FeasibleConeSPN`, its `H`, or its SPN objects.
Correspondence with that older chart table remains the existing restricted-text
arithmetic check, not validation of the old proof bodies.

## Actual verification

Lean 4.32.0 (toolchain commit `8c9756b28d64dab099da31a4c09229a9e6a2ef35`),
existing local Mathlib dependency build products, final exit 0. All seven new
printed declarations use only `[propext, Classical.choice, Quot.sound]`;
no warnings or `sorryAx`. The same invocation rechecked all core and generic
consumer declarations (26 total printed axiom reports including the seven new).

To respect the allowed-write boundary, the Python driver gathers Mathlib imports
and concatenates the three Lean bodies in memory, replacing the two local imports
by their actual source bodies. It invokes `lean --stdin` without an output flag.
No `.olean`, generated source, log or receipt is written. This checks the typed
proofs together, NOT standalone `.olean` import resolution or a Lake build.
Input hashes are frozen and rechecked after the invocation. The driver itself
does not establish provenance/authentication of the cached Mathlib environment.

Final successful invocation (repository root):

```powershell
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_ConcreteConsumer20260908_check.py --lean C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe --mathlib-packages examples/local_fkg/.lake/packages
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_check.py --self-test
```

The second command also passed: 36 left/right inverse cases each, 1296 orbit
relation pairs, 18 two-label fibers, the 36 arbitrary-weight coefficients,
169 exact boundary probes, and 11 rejected negative controls. Probes are
diagnostics; universal real-state coverage comes from the Lean proof.

During development, a Windows stdout encoding error was fixed only in the new
driver; an ambiguous `multiplicity` name was fully qualified only in the new
Lean file. The final optimized-mode invocation passed with all guards active.

SHA-256 for reproducibility:

```text
NEW_CONE_INDEX_ConcreteConsumer20260908.lean
5f50f2c68713a18d4b490573923315cb2f0a24cfafda3e281f7c1154c1d36205
NEW_CONE_INDEX_ConcreteConsumer20260908_check.py
9371d4a4ca6e2e3752a1750774724f69c585a6f6c9cd80306c42e12896cc4353
actual UTF-8 stdin source bundle
cb6b9049baff877ea5de402be2aa1c9562e034f5051eaadfbb4818ffe20eccb7
```

## Remaining boundary

No concrete K_path, source-domain envelope, actual 18 SPN certificates,
Float64/controller defect treatment, P8 coverage, ODE continuation, or P5 closure
was constructed or certified. Neither a successful finite enumeration nor this
typed source-independent adapter changes any registry or formal admission gate.
Status remains pending for review/integration.
