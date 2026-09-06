# Route-B P8 first-exit/domain closure — minimal Lean decomposition

Status: `COMPILED_CONDITIONAL_DECOMPOSITION__CONCRETE_P8_OPEN`

## Result

`FirstExitBridge.lean` strictly compiles under Lean `v4.33.1` with the pinned
local Mathlib path. It contains no `sorry`, `admit`, or user-declared axiom.
The reported foundational axioms are `propext`, `Classical.choice`, and
`Quot.sound`.

The theorem decomposition is intentionally conditional. It proves the logical
assembly needed by P8 without pretending that a concrete Route-B ODE or
flowpipe has already supplied the premises.

## Exact separation of obligations

### 1. Domain-local analytic estimate

`LocalCertificate domain conclusion trajectory T` says only:

```text
for t in [0,T], domain(trajectory(t)) -> conclusion(trajectory(t)).
```

`localCertificate_of_domainSafe` applies it globally only after a separate
`DomainSafeThrough` proof. Thus a source bound valid on a box is never used to
prove membership in that same box by assumption.

### 2. First-exit topology and limit passage

`FirstExitAttainment` is an explicit premise producing an attained boundary
time from a hypothetical failure of domain safety. Its witness records domain
membership only on strict earlier prefixes.

`PrefixLimitMargin` is separate. A concrete adapter must prove that estimates
valid before the exit persist at the candidate exit, using the required
continuity or absolute-continuity argument. `BoundarySeparated` then supplies
the strict contradiction. The theorem `domainSafeThrough_of_firstExit` merely
composes these three facts.

### 3. ODE continuation

`ContinuationCriterion` is not derived from domain membership. It must be
instantiated from a concrete existence/uniqueness and extension theorem, such
as local Lipschitzness together with compact containment. Only then does
`existsThrough_of_domainSafe_and_continuation` conclude availability through
the target horizon.

### 4. P8 assembly

`p8_firstExit_domain_continuation_assembly` returns:

- domain safety through the horizon;
- the domain-local conclusion on the whole horizon;
- solution availability through the horizon.

Every first-exit, prefix-limit, boundary-separation, local-certificate, and
continuation hypothesis remains visible in its type.

## Why the current probe is not a proof

The inspected P8 local probe has `T=0.001`, radius `0.001`, 35 reachsets, and
`coverage_complete=false`; it is not the original full-X0, ramp-input,
`T=1` contract. `ProbeMayDischarge` requires both
`coverageComplete = true` and the closure claim. The compiled theorem
`coverageFalse_probe_cannot_discharge` proves that a false-coverage receipt
cannot pass this gate.

## Concrete premises still open

The Lean assembly does not establish:

- full 12-state initial inclusion and the ramp-input lift for `T=1`;
- a source-bound maximal continuous/AC Route-B solution;
- attained first exit for every relevant domain face;
- strict same-prefix bounds for joint limits, remote states, inverse guards,
  and implementation-semantics conditions;
- local-Lipschitz/compact-containment continuation through `T=1`;
- complete flowpipe/partition coverage or terminal transfer.

Accordingly `coverage=false`, `coverage_complete=false`, and
`formal_certificate_allowed=false` remain mandatory.

## Verification and mutation boundary

Strict command:

```powershell
lake env lean -DwarningAsError=true .\FirstExitBridge.lean
```

The exact output is retained in `compile_strict.log`; hashes and provenance are
in `CHECK_RESULT.json`. No Julia, solver, or regression suite was run. This task
created files only under `examples/routeb_first_exit_bridge_lean/` and did not
edit state, registry, canonical source, or any pre-existing file.

During final verification, unrelated concurrent worktree changes appeared in
`src/percolation_workflow/math_frontier.py`,
`src/percolation_workflow/scheduler.py`, and
`tests/test_math_bottleneck_dispatch.py`; they were not touched by this task.
