---
kind: review_result
review_id: review-T-P4-039-rational-lambda-guard-lean-codex-20260907T1815
task_id: T-P4-039
agent: Codex
source_agent: Codex
created_at: 2026-09-07T18:15:00-06:00
inspected_commit: 7c218f3325e8a1bacd4fc44540701c95cde281a9
inspected_paths:
  - examples/routeb_p4_rational_lambda_guard_lean/P4RationalLambdaGuard.lean
  - examples/routeb_p4_rational_lambda_guard_lean/README.md
  - examples/routeb_p4_rational_lambda_guard_lean/verify.sh
  - examples/routeb_p4_rational_lambda_guard_lean/lean-toolchain
  - agent_review_inbox/review-T-P4-039-liuguanyi-20260907T1616.md
integration_status: pending
admission_label: compiled_candidate
registry_status: unchanged
registry_mutation: false
---

# T-P4-039 Lean lane — division-free four-leaf audit

## Result

Added and audited the four Lean-facing `Real` theorem leaves requested by
T-P4-039:

1. `young_completed_square_identity`;
2. `young_feasible_of_rational_radius`;
3. `young_inner_interval_feasible`;
4. `young_common_parameter_of_inner_bounds`.

The theorem statements use cross-multiplied interval bounds
`G - radius ≤ 2*A*theta` and `2*A*theta ≤ G + radius`.  They contain no
division, inverse, source/P8 assumptions, or concrete coefficient binding.
Rational inputs are represented by coercion into `Real`; no `Rat` theorem or
floating-point realization claim is introduced.

The original T-P4-040 endpoint/rounding leaves remain in the same sidecar and
are not relabeled as T-P4-039 evidence.  The verifier now checks both theorem
sets separately by requiring each public theorem's `#print axioms` line.

## Placeholder and axiom boundary

- source scan: `PLACEHOLDER_SCAN=PASS`;
- no `sorry`, `admit`, `axiom`, `opaque`, `unsafe`, or `native_decide` was added;
- every checked theorem reports only the ordinary Lean kernel baseline
  `[propext, Classical.choice, Quot.sound]`;
- no `sorryAx` appears in compiler output;
- this is a `compiled_candidate`, not `LEAN_VERIFIED`, comparator acceptance,
  or registry admission.

## Local receipt

Pinned toolchain:

```text
leanprover/lean4:v4.32.0
Lake 5.0.0-src+8c9756b (Lean 4.32.0)
```

Executed with the working directory `examples/local_fkg` and the pinned
Windows binaries:

```text
C:\Users\z5242\.elan\bin\lake.exe env lean.exe -DwarningAsError=true \
  C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_p4_rational_lambda_guard_lean\P4RationalLambdaGuard.lean
```

The portable verifier completed with exit code `0`:

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P4_RATIONAL_LAMBDA_GUARD_FOCUSED_CHECK=PASS
P4_CONCRETE_DH_SOURCE_COEFFICIENT_BINDING=OPEN
FLOAT64_REALIZATION_CONTAINMENT=OPEN
P8_DOMAIN_TRAJECTORY_COVERAGE=OPEN
P4_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_rational_lambda_guard_lean/verify.sh
```

Artifact SHA-256 at review time:

```text
P4RationalLambdaGuard.lean
475CC1DEE8AB4016C98261B90E42DEA782A85FDD76B7464E838131868A95849B
README.md
14C2E0ABA0D4B0519704DBE46941E4AEA07263DECD3AE2FCF311963382221644
verify.sh
47D9FDD6F1D4B8DFE7E0E6E697938C963D41BE057689B69EE7C0BFF382DDDA37
```

## Independent GitHub handoff

The independent Lean agent should run from a clean checkout with the same
toolchain and retain the complete stdout/stderr plus exit code:

```bash
bash examples/routeb_p4_rational_lambda_guard_lean/verify.sh
```

Classify failures without promotion:

- missing `lake`/`lean`, missing `examples/local_fkg`, or toolchain mismatch:
  `BUILD_ENV_BLOCKED`;
- parser diagnostics: `LEAN_PARSE_ERROR`;
- elaborator/typeclass/tactic diagnostics: `LEAN_ELAB_ERROR`;
- kernel rejection: `LEAN_KERNEL_ERROR`;
- source placeholder hit or `sorryAx`: `PLACEHOLDER_REJECTED`;
- non-baseline `#print axioms`: `AXIOM_POLICY_REJECTED`;
- missing stdout/stderr, exit code, hashes, or theorem reports:
  `RECEIPT_INCOMPLETE`.

Until that independent receipt is collected, keep this child pending and do
not mutate the verified registry.
