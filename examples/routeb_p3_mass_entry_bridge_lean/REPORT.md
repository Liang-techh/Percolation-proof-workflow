# Route-B P3 single-entry bridge report

Status: **COMPILED_CANDIDATE — conditional only**

The focused theorem `mass_entry_float64_to_exact_interval` compiles under the
pinned local FKG Lean environment. It consumes four explicit premises:

1. the exact-real DH entry is contained on the chosen rational box;
2. the sampled input lies in that box;
3. the receipt value is the interpreted Float64 entry;
4. the authenticated receipt value lies in the interval.

It returns both the machine-entry containment and the exact-real box
containment. The source hash, operation trace hash, runtime and finite-normal
proof are carried by the receipt structure, but this sidecar intentionally
does not validate their external provenance or prove Julia/exact evaluator
equality.

The receipt status is therefore pending/conditional, not `VERIFIED`. No
verified registry, persistent state, external source, or Route-B admission flag
was changed. Full P3 coverage, all 36 entries, IEEE operation semantics,
canonical DH binding, and downstream P4/P8/M4 obligations remain open.

Focused command:

```text
./verify.sh
```

The script checks Lean 4.32.0 from `examples/local_fkg/lean-toolchain`, rejects
proof-hole/unsafe escape tokens, requires zero `sorryAx`, and audits the four
printed theorem axiom reports.

Latest focused receipt (2026-09-07 local run):

- output: `output/run-VJHd35nB`
- `MASS_ENTRY_BRIDGE_COMPILE_EXIT_CODE=0`
- `FOCUSED_CHECK=PASS`
- OLean SHA-256: `a11e7cfecd6668afb134e68b6dd208473ff9bddb47cd0379f0c78891cfb462e7`
- compile log SHA-256: `21a3cf765e9dd2ccc2d497b2e4706c04d7ef6f5bcf93094a26a180ed35a30f83`
- axiom audit: only `propext`, `Classical.choice`, `Quot.sound`
- `CONDITIONAL_SOURCE_BRIDGE=OPEN`; `REGISTRY_MUTATION=false`
