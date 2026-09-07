---
kind: review_result
task_id: T-P3-001
source_agent: Codex
created_at: 2026-09-07T02:07:29Z
integration_status: pending
---

# T-P3-001 review: single-entry true-DH source bridge

## Scope and inspected evidence

Inspected:

- `docs/routeb-p3-next-concrete-child.md`
- `examples/routeb_p3_mass_entry_bridge_lean/MassEntryBridge.lean`
- `examples/routeb_p3_mass_entry_bridge_lean/README.md`
- `examples/routeb_p3_mass_entry_bridge_lean/REPORT.md`
- latest local receipt `examples/routeb_p3_mass_entry_bridge_lean/output/run-36AKCyjA/verify.log`

The latest receipt reports Lean 4.32.0, pinned `examples/local_fkg/lean-toolchain`,
`MASS_ENTRY_BRIDGE_COMPILE_EXIT_CODE=0`, `FOCUSED_CHECK=PASS`, only standard
axioms (`propext`, `Classical.choice`, `Quot.sound`), and
`REGISTRY_MUTATION=false`. A short local hash check confirms the current
`MassEntryBridge.lean` is `4cb56ec8964039e736eaba1f2b4591a7c51c366e44c551bb5f8016eb4736b89c`,
matching the latest receipt. The earlier failed runs contain linter/type/
`sorryAx` failures and are retained as history, not evidence of success.

The P3 document records the current external source hashes, including
`dhport_lib.jl=aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`
and `routeB_interval_bounds.jl=7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f`.
Those hashes are provenance inputs from the document; this review did not
rerun Julia or alter the external project.

## Judgment

The smallest *conditional* source-to-interval contract is implemented and
compiled. In Lean, `MExact` and `MFloat` are independent parameters;
`mass_entry_float64_to_exact_interval` consumes `ExactDHInterval`, box
membership, an authenticated trace equality, and receipt interval membership.
It then derives machine-value membership and exact-model box membership.

The actual canonical Julia/DH bridge is **not yet implementable from the
available receipt alone**. The Lean structure stores source/trace hashes and a
proof-bearing `finiteNormalNoOverflow` field, but no concrete IEEE operation
trace, rounding witness, Julia execution artifact, exact-DH evaluator
agreement proof, or interval checker output is bound into the theorem. Thus
the receipt proves only the abstract contract after those facts are supplied
as premises. The current external interval code and CSV payload cannot fill
that gap by sampling or decimal reification.

## Smallest next child

Implement one fixed rational box and one fixed `(i,j)` entry with a separate,
machine-readable receipt containing:

1. canonical source/parameter/box/regularizer/precision hashes;
2. deterministic Julia runtime and platform identity;
3. an IEEE-754 operation trace (including `sin`/`cos`, multiplication,
   accumulation, and directed interval endpoint witnesses);
4. a checker proving the trace evaluates to the recorded Float64 value;
5. an exact-real DH evaluator agreement obligation and an interval-soundness
   receipt.

The Lean side should then instantiate the existing abstract theorem. Until
items 4–5 are independently checked, retain the theorem as conditional.

## Admission boundary

Classification: `COMPILED_CANDIDATE` only; integration status: `pending`.

This result must not enter the verified theorem registry, must not close
`P3.strict_true_dh_bounds`, and does not change `formal_certificate_allowed`.
The unresolved obligations remain canonical Julia/DH semantic binding,
Float64 operation semantics, exact evaluator agreement, all-entry extension,
global box coverage, residual absorption, P8 flowpipe, terminal transfer,
comparator, and full pinned Lean/CI verification.

## Proposed workflow integration

Documentation/DAG metadata only: attach this review to
`P3.child.mass_entry_float64_to_exact_interval` as a compiled conditional
attempt, preserve the failed receipt history, and schedule the fixed-box
IEEE/exact-evaluator bridge as the next frontier leaf. No authoritative state,
registry, or external source was modified.
