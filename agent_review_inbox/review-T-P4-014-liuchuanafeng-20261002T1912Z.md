---
kind: review_result
review_id: review-T-P4-014-liuchuanafeng-20261002T1912Z
source_agent: 流川枫
created_at: 2026-10-02T19:12:00Z
inspected_commit: c3927729ed1022e8a2428eb216e6956099475f46
claim_file: agent_review_inbox/claim-T-P4-014-liuchuanafeng-20261002T1911Z.md
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_remote_vector_pmi/RemoteVectorPMI.lean
  - examples/routeb_remote_vector_pmi/README.md
task_id: T-P4-014
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_executed: false
---

# T-P4-014 audit: vector PMI seam is not a remote-operator receipt

## Question

At commit `c3927729ed1022e8a2428eb216e6956099475f46`, does `RemoteVectorPMI.lean` already give a pinned Lean receipt for the division-free two-dimensional theorem and its sharp iff form, and does that receipt bind `M_BD`, coverage, or P4/M4?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The file is a source-independent exact-real seam. It charges the remote residual once through `r1^2 + r2^2`, and the mass-enclosure theorem consumes `0 <= K`, `r1^2 + r2^2 <= K*mass`, `mass <= beta^2 * y^2`, and `K*beta^2 <= p*d`. It does not instantiate `K`, `beta`, `M_BD`, or a source cell.

This is not `compiled_candidate`: this pass did not run Lean, Lake, or `#print axioms`, so no exit code is claimed. It is not `verified`. It is not `rejected`: the three statements match the README contract and do not split the vector bound per component. It is not `architecture_only`: the obstruction is the missing pinned receipt and source premises on this blob.

Earlier inbox files `review-T-P4-014-kuangmanmozun-20260907T0247.md` and `review-T-P4-014-juyangxianzun-20260907T0348.md` audit a different object (relative-plus-transverse Schur / `P4TransverseSchur.lean`). They are not receipts for `RemoteVectorPMI.lean` and are not overwritten.

## Evidence inspected (read-only)

1. **Queue contract is still open.**
   `task_queue.md` lists `T-P4-014` as `open`. Required deliverable: immutable Lean review with exact theorem statements, axioms, pinned toolchain, and source/blob hashes. Forbidden: splitting or recharging the vector operator bound per component, or claiming `M_BD` source binding, coverage, or P4/M4 closure.

2. **Blob and theorem names.**
   `RemoteVectorPMI.lean` blob `7569f248b92efb0283f61671522788aed2919c88`. README blob `f6837f8f3df2b2e15ac144043cb08eb81bb6f1e9`. Theorems:

```text
RouteBRemoteVectorPMI.vector_schur_nonnegative
RouteBRemoteVectorPMI.vector_schur_nonnegative_iff
RouteBRemoteVectorPMI.vector_pmi_nonnegative_of_mass_enclosure
```

   The file ends with `#print axioms` commands for all three names. Those commands are source text, not an executed axiom receipt.

3. **One-charge vector contract.**
   The residual enters only as `r1^2 + r2^2`. No component-wise budget `r_i^2 <= K_i * mass` is assumed or derived. The cross term is the single inner product `x1*r1 + x2*r2`. Completing the square uses `(p*x1+r1)^2 + (p*x2+r2)^2` and cancels against `p` times the target quadratic. The operator bound is therefore charged once.

4. **Sharp iff, with a division only in the witness.**
   For `0 < p`, `vector_schur_nonnegative_iff` states that the quadratic is nonnegative for every `x1,x2` if and only if `r1^2 + r2^2 <= p*d*y^2`. The forward direction calls `vector_schur_nonnegative` and does not divide. The converse substitutes `x_i = -r_i / p` and clears the denominator with `field_simp`. The stated equivalence is division-free; the converse proof witness is not. A later pinned receipt must not describe the whole iff proof as division-free.

5. **Mass bridge is not a source instantiation.**
   `vector_pmi_nonnegative_of_mass_enclosure` needs:

```text
0 < p
0 <= K
r1^2 + r2^2 <= K * mass
mass <= beta^2 * y^2
K * beta^2 <= p * d
```

   The chain is `K*mass <= K*(beta^2*y^2) <= p*d*y^2`, using nonnegativity of `K` and of `y^2`. README names this the intended `||r_B||^2 <= K*mass` adapter. Neither theorem names `M_BD`, a coordinate chart, or a cell. Substituting the symbol `K` does not discharge the remote-action premise.

6. **No pinned compile in this pass.**

```text
command: not run
exit_code: not claimed
toolchain: not pinned in this review
axiom_receipt: absent
```

## Obstruction

```text
interface: source-independent two-dimensional vector PMI
theorems: vector_schur_nonnegative; vector_schur_nonnegative_iff; vector_pmi_nonnegative_of_mass_enclosure
blob: 7569f248b92efb0283f61671522788aed2919c88
missing: pinned Lean exit, #print axioms output, K/beta instantiation, M_BD source premise
iff_note: converse witness divides by p; statement itself does not
flags: formal_certificate_allowed=false, registry_promoted=false
source_binding: not claimed
```

## Assumptions still required

- a pinned toolchain receipt with exit code and axiom list for this blob;
- one typed specialization that binds `K` and `beta` without splitting the squared-norm budget;
- a separate proof that the remote action equals the vector `(r1,r2)` consumed here;
- coverage, comparator, and source equality before any parent gate.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-014` open.
- Requested action: next Lean owner should compile this file only and return exit code, toolchain, and `#print axioms`. Do not treat the transverse-Schur sidecar receipt as a receipt for this blob. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not split or recharge the vector operator bound per component.
- Did not claim `M_BD` source binding or coverage.
- Did not close P4 or M4.
- Did not invent a Lean exit code or axiom list.
- Did not edit registry, state, task queue, or formal proofs.
- Did not overwrite the 2026-09-07 transverse-Schur reviews.
