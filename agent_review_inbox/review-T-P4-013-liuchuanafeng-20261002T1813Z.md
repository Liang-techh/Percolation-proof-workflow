---
kind: review_result
review_id: review-T-P4-013-liuchuanafeng-20261002T1813Z
source_agent: 流川枫
created_at: 2026-10-02T18:13:00Z
inspected_commit: afab0ee7ab3579059fbc04cc88938d62acca91fb
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_remote_pmi_composition/RemotePMIComposition.lean
task_id: T-P4-013
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P4-013 audit: scalar PMI composition is a parameter theorem, not a remote binding

## Question

At commit `afab0ee7ab3579059fbc04cc88938d62acca91fb`, do the two theorems in `RemotePMIComposition.lean` already compose a proved remote mass budget into the scalar Schur envelope used by P4, or do they only state a source-independent inequality under unbound `kappa`/`beta` premises?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The file states two real-scalar composition theorems. Their hypotheses are parameters. Nothing in the file instantiates `M_BD(q) a_D`, a mass source, coverage, or a P4 residual node.

This is not `rejected`: the stated implications are the intended composition shape and no counterexample to those implications was found by inspection. It is not `compiled_candidate`: no Lean command was run, so there is no exit code. It is not `verified`. It is not `architecture_only`: the obstruction is the missing source specialization of the named premises.

## Evidence inspected (read-only)

1. **Queue contract is still open.**
   `task_queue.md` lists `T-P4-013` as `open`. Required object: compile the two source-independent composition theorems and record exact statements, pinned toolchain, and `#print axioms`, plus a specialization note for `kappa`/`beta`. Forbidden: treating the composition as a proof of `M_BD`, mass/source equality, coverage, or P4/M4 closure.

2. **Blob and theorem names.**
   Path `examples/routeb_remote_pmi_composition/RemotePMIComposition.lean`, blob `eb95525e426513d197fb611f88faba2553199a6f`. Namespace `RouteBRemotePMIComposition`. Theorems:
   - `residual_sq_le_of_mass_and_scale`
   - `pmi_nonnegative_of_mass_scaled_enclosure`
   The file ends with `#print axioms` for both names. Those commands are source text only; their kernel output was not captured.

3. **Statement shape.**
   The first theorem takes `residual, kappa, mass, beta, y : ℝ` and assumptions
   `residual ^ 2 ≤ kappa ^ 2 * mass` and `mass ≤ beta ^ 2 * y ^ 2`, and concludes
   `residual ^ 2 ≤ (kappa * beta) ^ 2 * y ^ 2`.
   The second adds `0 < epsilon`, `epsilon ≤ p`, and `(kappa * beta) ^ 2 / epsilon ≤ d`, and concludes
   `0 ≤ p * x ^ 2 + 2 * x * residual + d * y ^ 2`.
   The module docstring says the physical/source premises are intentional parameters.

4. **Placeholder scan (text only).**
   No `sorry`, `admit`, `axiom`, or `opaque` declaration appears in the blob. Proof steps use `sq_nonneg`, `mul_le_mul_of_nonneg_left`, `ring`, `field_simp`, and `linarith`. Imports are `Mathlib.Data.Real.Basic` and `Mathlib.Tactic`. This scan is not a kernel axiom print.

5. **Specialization note for `kappa`/`beta`.**
   The composition replaces the pair `(kappa, mass)` and `(beta, y)` by the product scale `kappa * beta` on `y`. A later owner may instantiate `kappa` only from a proved remote-action bound `residual ^ 2 ≤ kappa ^ 2 * mass`, and `beta` only from a proved mass-to-PMI-scale bound `mass ≤ beta ^ 2 * y ^ 2`, with the same `mass` and the same `y` as the Schur slot. Empty names, a block-only remote bound, or a numeric token do not supply those premises. The second theorem also needs a positive `epsilon` already known to sit under `p` and to dominate `(kappa * beta) ^ 2 / epsilon` by `d`. None of those witnesses are in this file.

## Commands

```text
lean/lake: not run
exit code: not claimed
pinned toolchain: not claimed
#print axioms output: not claimed
```

## Obstruction

```text
interface: residual_sq_le_of_mass_and_scale ; pmi_nonnegative_of_mass_scaled_enclosure
premises: residual^2 ≤ kappa^2 * mass ; mass ≤ beta^2 * y^2 ; 0 < epsilon ≤ p ; (kappa*beta)^2 / epsilon ≤ d
missing: source witness for kappa/beta/mass/residual, pinned Lean receipt, axiom print, coverage
source_binding: not claimed
flags: formal_certificate_allowed=false, registry_eligible=false
```

## Assumptions still required

- a pinned Lean invocation of this file, with toolchain, exit code, stdout/stderr, and the actual `#print axioms` output;
- one remote-action receipt that proves the `kappa` premise without a block-only bound;
- a matching mass-scale receipt for the same `mass` and Schur coordinate `y`;
- an `epsilon` margin already admitted by the P4 residual node;
- coverage and comparator gates before any parent close.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-013` open.
- Requested action: do not treat these theorems as `M_BD` or mass/source equality. Next Lean owner should return a pinned receipt; a mathematics owner should supply one specialized `(kappa, beta)` pair or the missing witness. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not treat the composition as a proof of `M_BD`, mass/source equality, coverage, or P4/M4 closure.
- Did not claim a compile, axiom set, or exit code.
- Did not close P4 or M4.
- Did not edit registry, state, task queue, or formal proofs.
