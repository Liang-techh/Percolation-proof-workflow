---
kind: review_result
task_id: T-P5-026
review_id: review-T-P5-026-CONE-INDEX-ORBIT-FIBER-20260914T211830Z
source_agent: Codex
agent: Codex
created_at: 2026-09-14T21:18:30Z
inspected_commit: 53e497f9d09de120db0f16da87b7d6e07e0e6e00
status: compiled_candidate
integration_status: pending
admission_label: pending
lean_actually_run: true
lean_validation: local_stdin_source_bundle_pass
lean_exit_code: 0
checker_exit_code: 0
new_axiom_reports: 10
total_axiom_reports: 48
axiom_audit: pass_allowlist
standalone_module_imports_verified: false
cached_mathlib_authenticated: false
sidecar_is_receipt: false
formal_admission_receipt_created: false
concrete_K_path_bound: false
source_coverage_verified: false
P5_closed: false
registry_eligible: false
state_mutated_by_this_task: false
registry_mutated_by_this_task: false
---

# P5 ConeIndex: fixed-state orbit fibers, preserving multiplicity

## Result and minimal interface

This adds a source-independent refinement to the existing concrete ConeIndex,
not another enumeration. The unchanged core already supplies:

- `ConeIndex = Cone × Cone` with 36 labels and a fixed-point-free simultaneous
  sign involution `flip`;
- `Representative = Fin 3 × Cone` with 18 labels, first-channel choices
  `[pp, pnPos, pnNeg]` (original Python IDs `[0,2,3]`, not `[0,1,2]`);
- `indexEquiv : ConeIndex ≃ Representative × Bool`, computable `select/expand`,
  two labels per representative, and the arbitrary-weight sum identity;
- real-state signed cover and full `(label, orthant parameter)` witness
  equivalence, retaining every closed-boundary witness.

The new module proves when orientation erasure is safe for the CARDINALITY of
a fixed-state covering support. For `C_z = {c | Member c z}` and
`R_z = {r | Member (representativeCone r) z OR
Member (flip (representativeCone r)) z}`:

| Condition | Exact statement |
|---|---|
| Any state | Opposite closed product cones both contain `z` iff `z=0`. |
| `z ≠ 0` | Representative selection restricted to `C_z` is injective. Every `r∈R_z` has exactly one covering orientation. |
| `z ≠ 0` | Label multiplicity equals `card R_z`. Different boundary representatives remain distinct. |
| `z = 0` | `card R_z=18`, but label multiplicity is `36=2*card R_z`. |

The universal formula is `multiplicity z = if z=0 then 2*card R_z else card R_z`.
An explicit origin guard proves that replacing label multiplicity by unweighted
representative-support cardinality is false there.

This does NOT assert a unique covering representative at a nonzero boundary,
does NOT drop orientation from arbitrary weighted witnesses, and does NOT make
fixed-state label membership invariant under `flip`. The full 36-to-18×Bool
witness interface remains valid everywhere. Eighteen unsigned predicate or
certificate checks still require the existing explicit evenness/invariance
premise. No specialized matrix values are deduplicated.

## New artifacts and SHA-256

Both files are under `examples/routeb_p5_feasible_cone_spn_proof_attempt/`:

| File | SHA-256 |
|---|---|
| `NEW_CONE_INDEX_OrbitFiber20260914.lean` | `4df14d1e6174b702dc9ed0d6d45c5021b9f786d0eb577b41347b404eec80ace9` |
| `NEW_CONE_INDEX_OrbitFiber20260914_check.py` | `6a1a35e4402de8c72115ed737824711a4607b505ec356bad73aed81df5d17d4d` |

The ten new audited declarations in `RouteBP5ConeIndexOrbitFiber` are:
`coordinates_neg`, `opposite_member_iff_zero`,
`representative_injective_on_members`, `orbit_member_iff`, `unique_orientation`,
`coveringRepresentatives_nonempty`, `multiplicity_eq_support_card`,
`origin_support_card`, `exact_multiplicity_formula`, and
`origin_orientation_erasure_loses_multiplicity`.

These sidecar files are source artifacts, NOT receipts. This immutable review
records the execution observed in this task; it does not substitute for an
authenticated comparator/admission receipt or authorize registry promotion.

## Actual focused verification

Executed locally, not inferred from a predecessor review:

```powershell
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_OrbitFiber20260914_check.py --lean C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe --mathlib-packages examples/local_fkg/.lake/packages
```

- Actual Lean: `4.32.0`, `x86_64-w64-windows-gnu`, toolchain commit
  `8c9756b28d64dab099da31a4c09229a9e6a2ef35`.
- Final Lean exit code **0**; checker exit code **0**, `result: pass`.
- **10 new / 48 total** printed axiom reports. The checker parses every report
  and permits only `propext`, `Classical.choice`, `Quot.sound`. All ten new
  declarations use that allowed set. Final output has no warning or `sorryAx`.
- The first development run was rejected by the checker's warning gate for an
  unused `or_comm` simp argument. Only the new Lean file was corrected; the
  final invocation above passed without suppressing that gate.
- Exact UTF-8 stdin bundle SHA-256:
  `385d8b8fa7a5502193e682e9749986f3284fcfac72e3ef5abc625782db38b32c`.

The driver concatenates complete pinned sources, in dependency order:
Core, InverseCover20260908, SignedCoverConsumer, ConcreteConsumer20260908,
then OrbitFiber20260914. Local imports are replaced in memory by these bodies;
Mathlib imports are retained. `lean --stdin` is called without an output flag.
No generated Lean source, `.olean`, log, receipt, cache or registry file is
written by the checker. Guards remain active under `python -O`.

This verifies elaboration/kernel checking of that SOURCE BUNDLE against the
existing cached Mathlib environment. It does **not** verify standalone local
module imports, a Lake build, dependency-cache authentication, CI provenance,
or formal admission. No full regression or SPN fixture/search was run.

Pinned unchanged inputs (same example directory; rechecked after Lean):

| Input | SHA-256 |
|---|---|
| `P5FeasibleConeSPN.lean` | `fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824` |
| `NEW_exact_geometry_spn.py` | `263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42` |
| `NEW_CONE_INDEX_Core.lean` | `b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602` |
| `NEW_CONE_INDEX_InverseCover20260908.lean` | `2e4a6dfaca0d564e3fbf3407c6c68b31776c1fced30687d4c8e81e6b90d740c0` |
| `NEW_CONE_INDEX_SignedCoverConsumer.lean` | `ea9a87281e096caf2e3b082a31dd0fbb00efc85016376dbd8ad735b39d41f4b8` |
| `NEW_CONE_INDEX_ConcreteConsumer20260908.lean` | `5f50f2c68713a18d4b490573923315cb2f0a24cfafda3e281f7c1154c1d36205` |

The old `P5FeasibleConeSPN.lean` proof attempt and `NEW_exact_geometry_spn.py`
were read and hashed, NOT executed as part of the bundle. The generic sidecar
at `examples/routeb_p5_feasible_cone_spn_lean/P5FeasibleConeSPN.lean` was also
inspected, not compiled in this task. No new typed adapter to either old P5
theorem namespace, its `H`, or its SPN certificate objects is asserted.

## Reviewed context and unchanged admission boundary

Read the mathematical review
`agent_review_inbox/review-T-P5-026-guyuefangyuan-20260907T1031.md`, the formal
handoff `agent_review_inbox/review-T-P5-026-juyangxianzun-20260907T1048.md`,
and the existing inverse-cover/ConcreteConsumer reviews. Their historical
execution claims were not reused as this task's current verification evidence.

Only the two new source files above and this new review were written by this
task. Existing P5 files, state, registry, K_path/source artifacts, and previous
reviews were not modified. The worktree already had unrelated changes,
including `artifacts/routeb_6dof/state.json`; those were left untouched. Other
agents were active concurrently, so repository-wide changes are not attributed
to this task.

Still absent from this result: concrete source-bound `K_path`, same-domain
residual/Jacobian envelope, actual 18 SPN witnesses, Float64/controller/solve
defect handling, source coverage, P8 continuation/flowpipe, and P5 closure.
This remains a source-independent compiled candidate, pending independent
review/integration, with `registry_eligible: false`.
