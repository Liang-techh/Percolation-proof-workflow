---
kind: review_result
review_id: review-T-P4-013-liuchuanafeng-20261002T1815Z
source_agent: 流川枫
created_at: 2026-10-02T18:15:00Z
inspected_commit: afab0ee7ab3579059fbc04cc88938d62acca91fb
claim_commit: 72f87c5884dfea7eeb3262e3a74893866f26cd1b
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_remote_pmi_composition/RemotePMIComposition.lean
  - examples/routeb_remote_pmi_composition/README.md
task_id: T-P4-013
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_executed: false
---

# T-P4-013 audit: scalar composition seam is not a remote-action receipt

## Question

At commit `afab0ee7ab3579059fbc04cc88938d62acca91fb`, do the two theorems in `RemotePMIComposition.lean` already specialize `kappa`/`beta`, and do they constitute a pinned Lean receipt for `M_BD`, mass/source equality, coverage, or P4/M4 closure?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The file is a source-independent exact-real composition seam. Both theorems take `residual`, `kappa`, `mass`, and `beta` as parameters. The directory README names `90` only as an intended later specialization and explicitly delegates compilation and `#print axioms` to a pinned Lean worker.

This is not `compiled_candidate`: this pass did not run Lean, Lake, or `#print axioms`, so no exit code is claimed. It is not `verified`. It is not `rejected`: the statements are consistent with the declared composition contract. It is not `architecture_only`: the obstruction is the missing specialization, source premises, and pinned receipt on the current blob.

The earlier inbox file `review-T-P4-013-kuangmanmozun-20260907T0145.md` audits a different object (normalized `kc` Schur coefficients). It is not a receipt for this Lean seam and is not overwritten.

## Evidence inspected (read-only)

1. **Queue contract is still open.**
   `task_queue.md` lists `T-P4-013` as `open`. Required deliverable: immutable review with Lean exit code, theorem names, source/blob hashes, and a `kappa`/`beta` specialization note. Forbidden: treating the composition as a proof of `M_BD`, mass/source equality, coverage, or P4/M4 closure.

2. **Blob and theorem names.**
   `RemotePMIComposition.lean` blob `eb95525e426513d197fb611f88faba2553199a6f`. README blob `5cd5bc7e12f3a0057114db9e781a857d3fd558f8`. Theorems:

```text
RouteBRemotePMIComposition.residual_sq_le_of_mass_and_scale
RouteBRemotePMIComposition.pmi_nonnegative_of_mass_scaled_enclosure
```

   The file ends with `#print axioms` commands for both names. Those commands are source text, not an executed axiom receipt.

3. **Statement identity.**
   Given `residual^2 <= kappa^2 * mass` and `mass <= beta^2 * y^2`, the first theorem concludes `residual^2 <= (kappa*beta)^2 * y^2`. The step uses `kappa^2 >= 0`, left-multiplication, and `ring`. It does not assume `kappa >= 0` or `beta >= 0`; the squares absorb sign.

   The second theorem adds `0 < epsilon`, `epsilon <= p`, and `(kappa*beta)^2 / epsilon <= d`, then concludes `0 <= p*x^2 + 2*x*residual + d*y^2`. Division is guarded by `ne_of_gt hepsilon`. No `M_BD`, coordinate, cell, or source symbol appears.

4. **`kappa`/`beta` specialization note.**
   README says the intended first specialization is the conditional remote-acceleration coefficient `90`, followed by a separately proved operator/source bound for `M_BD`. Neither theorem instantiates `kappa = sqrt(90)`, `kappa^2 = 90`, or any `beta`. A later consumer must still supply:

```text
residual^2 <= kappa^2 * mass
mass <= beta^2 * y^2
0 < epsilon <= p
(kappa*beta)^2 / epsilon <= d
```

   on the same scalar channel. Substituting the name `90` without those premises does not discharge the hypotheses.

5. **No pinned compile in this pass.**

```text
command: not run
exit_code: not claimed
toolchain: not pinned in this review
axiom_receipt: absent
```

## Obstruction

```text
interface: source-independent scalar composition
theorems: residual_sq_le_of_mass_and_scale; pmi_nonnegative_of_mass_scaled_enclosure
blob: eb95525e426513d197fb611f88faba2553199a6f
missing: pinned Lean exit, #print axioms output, kappa/beta instantiation, M_BD source premise
flags: formal_certificate_allowed=false, registry_promoted=false
source_binding: not claimed
```

## Assumptions still required

- a pinned toolchain receipt with exit code and axiom list for this blob;
- one typed specialization that binds `kappa`/`beta` to a named remote budget without changing the residual;
- a separate proof that the remote action equals the scalar `residual` consumed here;
- coverage, comparator, and source equality before any parent gate.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-013` open.
- Requested action: next Lean owner should compile this file only and return exit code, toolchain, and `#print axioms`. Do not treat the README coefficient `90` as instantiated. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not treat the composition as a proof of `M_BD`.
- Did not claim mass/source equality or coverage.
- Did not close P4 or M4.
- Did not invent a Lean exit code or axiom list.
- Did not edit registry, state, task queue, or formal proofs.
