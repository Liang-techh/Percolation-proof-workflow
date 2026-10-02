---
kind: review_result
review_id: review-T-P3-016-liuchuanafeng-20261002T0312Z
source_agent: 流川枫
created_at: 2026-10-02T03:12:00Z
inspected_commit: 24a91ab030bbf70df48ab1aa4f47722a7f6f2074
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_m33_exact_lower_lean/M33LowerBound.lean
  - examples/routeb_m33_exact_lower_lean/check_exact_lower.py
  - examples/routeb_m33_exact_lower_lean/README.md
  - examples/routeb_m33_exact_lower_lean/verify.sh
  - examples/routeb_m33_exact_lower_lean/lean-toolchain
task_id: T-P3-016
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P3-016 admission probe: exact M33 rational lower-bound lemma

## Question

Does commit `24a91ab030bbf70df48ab1aa4f47722a7f6f2074` already contain a consumable pinned receipt for `RouteBM33ExactLower.m33_lower_bound`, with the factorized cosine-box proof, exact rational arithmetic, and an upstream M33 formula-hash binding that a P3 mass-bound child could use?

## Decision

**No. Keep `admission_label: pending`.** The algebraic sidecar is present and its rational identity checks out, but this pass has no pinned Lake/Mathlib receipt, and the Lean statement does not itself bind the upstream Fourier/source hash.

This is not a rejected false inequality, and it is not architecture-only: the theorem statement and a pre-Lean `Fraction` check exist. It is also not `compiled_candidate` or `verified`, because `verify.sh` was not executed against a matching Lake root.

## Evidence inspected (read-only)

1. **In-tree sidecar, not an upstream source artifact.**
   `examples/routeb_m33_exact_lower_lean/` contains `M33LowerBound.lean` (blob SHA `4a04e469dd9c884a6897b52b716bf092c50431a8`), `check_exact_lower.py` (`e31f074a3c29a61b17488f4ffcc8f6792629b789`), `README.md` (`9fe352f016b8a1b1aea3bfcfbac5e02aa6d7bf7d`), `verify.sh` (`b057c255aef9e6f28da378b3b5da2f5761a7a6bd`), and `lean-toolchain` (`94b9f495baff80fd9cb44aad8f4762cb3b2066fe`, text `leanprover/lean4:v4.32.0`).
   The named upstream artifact `task_routeb_source_fourier_binding_current` is cited only in the README. It is not a file in this sidecar, so this review does not re-prove parser/source equality.

2. **Theorem contract is the cosine-box algebraic child only.**
   Public theorem: `RouteBM33ExactLower.m33_lower_bound`.
   Hypotheses: `-1 ≤ u ≤ 1` and `-1 ≤ x ≤ 1`.
   Conclusion: `(3016537 : ℝ) / 12000000 ≤ m33 u x`, where
   `m33 u x = 12159703/48000000 + 399/200000 * u + 147/3200000 * (x + (2*u^2 - 1) - x*(2*u^2 - 1))`.
   The file comment identifies `u = cos(q5)`, `x = cos(2*q4)`, `cos(2*q5) = 2*u^2 - 1`. Those substitutions are not hypotheses of the theorem. The proof is `ring` plus `nlinarith` after factoring `(u+1)` times a nonnegative inner term. No `sorry` or `admit` appears in the file. `#print axioms m33_lower_bound` is a directive, not a captured axiom list.

3. **Statement mismatch before P3 consumption.**
   README writes `M33(q) >= 3016537/12000000` and records canonical source `routeB_dense_Mq/dhport_lib.jl` SHA-256 `AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936`.
   The Lean theorem does not mention `M33`, `q`, that SHA, or the upstream artifact. Queue scope requires binding the upstream M33 formula hash without promoting the upstream checker. That binding is absent from the theorem statement. A future consumer must keep formula equality, Float64/libm rounding, all-entry mass coercivity, and coverage as separate obligations.

4. **Pre-Lean rational check passed; pinned Lean did not run.**
   Replayed `check_exact_lower.py` logic with Python `Fraction` only:
   - polynomial identity `m33 - lower = (u+1) * (399/200000 - 2*(147/3200000)*(1-u)*(1-x))` holds;
   - endpoint relation `A - B + C = 3016537/12000000` holds;
   - inner gap `B - 8*C = 651/400000 > 0` holds.
   Exit code of that replay: `0`. Status string: `PASS`. This is the script's own pre-Lean consistency check, not a kernel proof.
   `verify.sh` exits 2 unless `LAKE_ROOT` (default `examples/local_fkg`) has a lakefile and the same toolchain. This environment has no `lake` binary and no `examples/local_fkg`. No `#print axioms` output, no `sorry` scan of elaborated terms, and no compile exit code are claimed.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P3-016` open.
- Requested action: do not register `m33_lower_bound` as a P3 mass bound; do not edit registry, `state.json`, or formal certificates.
- Next owner for the missing receipt remains the pinned Lean slot: run `verify.sh` against a v4.32.0 Lake root, capture exit code, `#print axioms`, and a placeholder scan, then attach the upstream formula hash as an explicit hypothesis or a separate source-binding child.

## Forbidden-boundary compliance

- Did not infer the M33 source formula from the lower-bound lemma.
- Did not treat the algebraic child as Float64/libm semantics.
- Did not claim all-entry mass coercivity, inverse bounds, flowpipe coverage, or P3/formal-gate opening.
- Did not edit registry, state, or formal proofs.
