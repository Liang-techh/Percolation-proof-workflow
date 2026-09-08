---
kind: review_result
task_id: T-P5-026-CONE-INDEX-INVERSE-COVER
created_at: 2026-09-08
inspected_commit: ce7163d1f6ca10435136894d4484ac78de1fb68d
status: pending
integration_status: pending
lean_validation: local_stdin_source_bundle_pass
standalone_module_imports_verified: false
concrete_K_path_bound: false
source_coverage_verified: false
P5_closed: false
registry_eligible: false
---

# Concrete ConeIndex: inverse coordinates and finite membership fibers

## Result and write boundary

The existing `NEW_CONE_INDEX_Core.lean` already supplies the concrete finite
index, free global-sign involution, representative selection, and generic
multiplicity-preserving cover. This increment imports that actual core rather
than replacing its enumeration. It adds an exact inverse and a finite-label
membership interface, including parameter uniqueness per label.

Only three new files were written by this task, all in this example directory:

- `NEW_CONE_INDEX_InverseCover20260908.lean`
- `NEW_CONE_INDEX_InverseCover20260908_check.py`
- `NEW_CONE_INDEX_InverseCover20260908_REVIEW.md` (this review)

No existing P5 file, state, registry, K_path/source artifact, dependency cache,
Lake configuration, or prior review was edited by this task. No commit,
integration, CI dispatch, producer, or certificate search was run. Concurrent
changes to other paths, including state and shared scripts, were visible in
the shared worktree; they are not this task's changes and were not reverted.

## Read inputs and inherited minimal interface

Read `P5FeasibleConeSPN.lean`, `NEW_exact_geometry_spn.py`, the original
P5-026 mathematical and formalization reviews listed in the hash table below,
and the existing ConeIndex core/consumer reviews. Historical remote compile
claims were not adopted as current verification of the old P5 files.

The inherited interface, freshly checked together with this increment, is:

```text
ConeIndex = Cone × Cone                         card 36
Representative = Fin 3 × Cone                   card 18
representativeFirst = [pp, pnPos, pnNeg]
flip(c4,c5) = (reverse c4, reverse c5)
indexEquiv : ConeIndex ≃ Representative × Bool
```

`false` is the representative, `true` reverses BOTH channels. The rank in
`Fin 3` corresponds to original Python IDs `(0,2,3)`, not `(0,1,2)`.
The core proves both inverse laws, no fixed labels, two labels per orbit,
unique signed selection, and arbitrary-weight sum preservation. It does not
require matrix values at different representative labels to be distinct.

## New concrete inverse and cover interface

The inverse table is exactly the existing rational checker's `J` table:

| Channel label | a(x,y) | b(x,y) |
|---|---|---|
| pp | x | y |
| nn | -x | -y |
| pnPos | -y | x+y |
| pnNeg | x | -x-y |
| npPos | -x | x+y |
| npNeg | y | -x-y |

`coordinates c z` interleaves these into `(a4,a5,b4,b5)`, for state order
`(x4,x5,y4,y5)`. Both compositions with the core's actual `chart` are proved
identities on all real vectors, without a positivity assumption.

The new consumer-facing results are:

- `chartEquiv`, `parameter_unique`: for a fixed label, the chart is a
  bijection of real vectors and its parameter is unique.
- `member_iff_coordinates`: `Member c z ↔ Orthant (coordinates c z)`.
  Membership therefore has four explicit weak inequalities, including zeros.
- `witnessLabelEquiv`: all `(label, parameter)` witnesses at a state are in
  bijection with all covering labels. Its inverse restores the unique exact
  parameter; no boundary label is removed.
- `memberLabelEquiv`: covering labels are in bijection with covering
  `(representative, Bool)` labels, using the core's actual `select/expand`.
- `coveringLabels_spec`, `coveringLabels_nonempty`, `coveringLabels_card`:
  the finite filter is exactly membership, is nonempty at every real state,
  and has cardinality equal to the core's `multiplicity`.
- `inverse_cover_multiplicity`: that cardinality equals the sum of the two
  coordinate-test indicators for EACH of 18 representatives.
- `origin_coveringLabels_card`: the origin retains all **36** labels.

`coveringLabels` filters the finite INDEX set, not an image of chart or matrix
values. Parameter uniqueness per label must not be mistaken for uniqueness of
the state's label. Real membership uses classical decidability in Lean; no
executable exact-real comparison oracle is claimed. The Python rational tests
are executable, but are not a compiled extraction of this Lean definition.

Dropping Bool still requires an independent sign-invariance premise for the
particular consumer, as in the existing core/consumer. At fixed nonzero `z`,
`Member (flip c) z` need not equal `Member c z`. A specific negative control
at `z=(1,1,1,1)`, `c=(pp,pp)` catches that invalid shortcut.

## Actual focused verification

Final command from the repository root, exit 0:

```powershell
python -B -O examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_InverseCover20260908_check.py --lean C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe --mathlib-packages examples/local_fkg/.lake/packages
```

Lean 4.32.0, executable commit `8c9756b28d64dab099da31a4c09229a9e6a2ef35`.
The driver combines the actual core and new file in memory, replacing the local
import by the core's body and preserving Mathlib imports, then invokes
`lean --stdin`. No `.olean`, generated Lean bundle, log, or receipt is written.
This is elaboration/kernel validation of the combined source in the existing
cached environment, NOT standalone module import resolution or a Lake build.
It does not independently authenticate/rebuild the Mathlib cache.

All 12 new axiom reports and 16 inherited core reports contain only
`propext`, `Classical.choice`, `Quot.sound`; no warnings or `sorryAx` in the
final invocation. Earlier development failures in dependent-subtype rewriting,
classical-if elaboration and a looping simplification were corrected only in
the new file. The final driver also enforces an axiom whitelist.

The optimized Python invocation passed:

- Literal-only reading of the old Python geometry (no execution/import).
- Restricted linear-expression parsing of the new Lean inverse branches;
  exact equality with the reviewed `J` table and both inverse identities on
  all 36 product matrices. This text check is not a Lean parser or typed
  cross-namespace binding.
- 36 signed labels, 18 representative pairs, and 625 rational state probes
  preserving every label and its exact parameter.
- Probe multiplicity histogram `{1:144, 2:288, 4:144, 6:24, 12:24, 36:1}`.
- Five rejected controls: wrong inverse sign, missing orientation, duplicate
  label, value deduplication at the origin, fixed-state sign invariance.

The rational probes are diagnostics, not the universal real-cover proof.
All pinned input hashes were checked before and after the final invocation.

## SHA-256

The first five paths are relative to this example directory; the last three
are relative to the repository root. Hashes cover actual bytes.

| File | SHA-256 |
|---|---|
| P5FeasibleConeSPN.lean | fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824 |
| NEW_exact_geometry_spn.py | 263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42 |
| NEW_CONE_INDEX_Core.lean | b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602 |
| NEW_CONE_INDEX_InverseCover20260908.lean | 2e4a6dfaca0d564e3fbf3407c6c68b31776c1fced30687d4c8e81e6b90d740c0 |
| NEW_CONE_INDEX_InverseCover20260908_check.py | fb1f60af7bd565a00adbd913614dcc202a9fc2052daf9f7c6aed69f87b6b1904 |
| agent_review_inbox/review-T-P5-026-guyuefangyuan-20260907T1031.md | 3bfcba88dfdd26e7ab6766bf3b5c97303f675ad422cbc237e72f020df3c63f73 |
| agent_review_inbox/review-T-P5-026-juyangxianzun-20260907T1048.md | 7014ac45022170a555617a8bfa821b83edbe9f0bf69cc643894b826f18e3ff36 |
| agent_review_inbox/review-T-P5-026-concrete-consumer-20260908.md | ffda93600daf410accc13a266f466a9bc08c297b00985738d327b6ab64d589ee |

UTF-8 stdin bundle SHA-256:
`437228e76a70765f2f91529f8369cc5faad64e9fcd895f43ff5f1c5a8913989a`.

## Remaining boundary

This is a typed extension of `RouteBP5ConeIndex`, not a typed adapter to the
old `RouteBP5FeasibleConeSPN.H` or its SPN certificates. It supplies no concrete
K_path, same-domain residual envelope, actual 18 SPN witnesses, Float64 defect
treatment, P8 flowpipe coverage, or ODE continuation. No P5 closure or registry
admission follows. Integration/review status remains pending.
