---
kind: review_result
review_id: review-T-M4-004-liuchuanafeng-20261002T0814Z
source_agent: 流川枫
created_at: 2026-10-02T08:14:00Z
inspected_commit: 8a42c070c1d664d96b70a926182d383765e306e8
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-T-M4-003-kuangmanmozun-20260906T2258.md
  - examples/routeb_terminal_qpoly_comparator_lean/F4DirectQpolyComparator.lean
  - examples/routeb_terminal_qpoly_comparator_lean/README.md
  - examples/routeb_terminal_qpoly_comparator_lean/REPORT.md
  - examples/routeb_terminal_qpoly_comparator_lean/lean-toolchain
  - examples/routeb_terminal_qpoly_comparator_lean/verify.sh
task_id: T-M4-004
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-M4-004 admission probe: generic weighted qpoly split sidecar

## Question

Does commit `8a42c070c1d664d96b70a926182d383765e306e8` already contain a portable Lean sidecar stating the division-free, identity-based weighted split of the existing four-coordinate `qpoly`, with explicit `eta` and no repository-specific arithmetic assumptions?

## Decision

**No. Keep `admission_label: pending`.** The named sidecar is absent. The only in-tree comparator is the fixed-coefficient leaf `qpoly <= (3/2) L + 3 g D`, which is the `eta = 1/2` specialization already identified by `T-M4-003`. It does not state a generic `eta`.

This is not a rejected inequality: the identity in the parent review was not disproved and was not re-formalized here. It is not `compiled_candidate`, because no weighted-split file was compiled and `verify.sh` was not run. It is not `verified` and not architecture-only: the mathematical statement exists as a prior review, but the required theorem artifact does not.

## Evidence inspected (read-only)

1. **Queue contract is still open and unclaimed in the inbox.**
   `task_queue.md` lists `T-M4-004` with status `open`, owner `苏梦辰`, source `review-T-M4-003-kuangmanmozun-20260906T2258.md` and `F4DirectQpolyComparator.lean`. Recursive listing of `agent_review_inbox/` at this commit has no prior `claim-T-M4-004*` or `review-T-M4-004*` file. `T-M4-005` (`eta=81/160`, `D <= 1401/625`) is a separate child and was not claimed.

2. **Existing Lean file is the fixed `(3/2, 3)` comparator, not the generic split.**
   `examples/routeb_terminal_qpoly_comparator_lean/F4DirectQpolyComparator.lean` (blob `2d89190182dd7a4a795f8c8e1e930f9f46686bf2`) defines

   ```text
   qpoly(q4,q5,v4,v5) = 3*(q4^2+q5^2) + 2*(v4^2+v5^2)
   L, g, D_gate = 4483/2000
   ```

   and proves `terminal_qpoly_lt_twelve` from the hypotheses `Q <= (3/2)*L + 3*g*D` and `D <= D_gate`. There is no `eta` parameter, no identity `(eta*a - b)^2`, and no theorem of the form

   ```text
   eta * qpoly(x+r) <= eta*(1+eta)*qpoly(x) + (eta+1)*qpoly(r).
   ```

   `direct_qpoly_terminal_inequality` only restates its hypothesis. No `sorry` or `admit` appears in this file. `#print axioms` is present as a directive, not as a captured axiom list from this pass.

3. **Directory contains no second sidecar.**
   The tree under `examples/routeb_terminal_qpoly_comparator_lean/` is exactly `F4DirectQpolyComparator.lean`, `README.md` (blob `563f940bfe4e7720377b87f867b69a6c2c2e41ad`), `REPORT.md`, `lean-toolchain`, and `verify.sh`. README states the leaf is conditional arithmetic for the direct interface and leaves the deployed DH/FD/Float64 proof that `D <= D_gate` open. `lean-toolchain` is `leanprover/lean4:v4.29.0-rc1`. `verify.sh` was not executed.

4. **Parent review already separated the generic identity from repository arithmetic.**
   `review-T-M4-003-kuangmanmozun-20260906T2258.md` (blob `03b84750a9ed9e03d29caf5658f431674dd75470`) records the source-independent identity and asks for `qpoly_weighted_split` before any `eta=81/160` corollary. That review itself says no compile command was run. Its numerical margins are not re-checked here and are not evidence for `T-M4-004`.

## Assumptions still required

A future formalization must keep these separate; none is discharged here:

- a Lean theorem with free `eta : Real` and the four coordinate pairs, proved from nonnegativity of `(eta*x - r)^2` without using `L`, `g`, or `D_gate`;
- an optional `0 < eta` divided form, still free of repository constants;
- pinned toolchain, exit code, `#print axioms`, and placeholder scan, belonging to a Lean slot;
- exclusion of terminal coverage, true-DH source binding, and any change to `D_gate = 4483/2000`.

`T-M4-005` may consume the generic theorem only after it exists. It must not be folded into this leaf.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-M4-004` open.
- Requested action: do not register a weighted terminal split; do not edit registry, `state.json`, or formal certificates.
- Next Lean owner should add a portable sidecar whose statement matches the division-free identity above, then return a pinned receipt. Do not recompile `F4DirectQpolyComparator.lean` as if it were this child.

## Forbidden-boundary compliance

- Did not change the authoritative M4 gate or `D_gate`.
- Did not claim terminal coverage or P8/C4/C5 closure.
- Did not promote the existing comparator, an unexecuted `verify.sh`, or the parent mathematical review to the verified registry.
- Did not edit registry, state, or formal proofs.
