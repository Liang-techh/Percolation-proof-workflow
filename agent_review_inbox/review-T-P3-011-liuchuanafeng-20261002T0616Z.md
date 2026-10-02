---
kind: review_result
review_id: review-T-P3-011-liuchuanafeng-20261002T0616Z
source_agent: 流川枫
created_at: 2026-10-02T06:16:00Z
inspected_commit: 8aa3356e76d30f9a198f5032c9d16bab284ef768
claim_commit: 91eb000662b234195a26125305233b11c85be9bd
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_mass_regularizer_lean/MassRegularizer.lean
  - examples/routeb_mass_regularizer_lean/README.md
  - examples/routeb_m33_exact_lower_lean/README.md
  - examples/routeb_block45_body_prefix_lean/README.md
  - examples/routeb_p3_mass_entry_bridge_lean/README.md
  - examples/routeb_six_body_isotropic_mass_lean/SixBodyIsotropicMass.lean
  - examples/routeb_six_body_isotropic_mass_lean/README.md
task_id: T-P3-011
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P3-011 admission probe: link-Jacobian structural lower bound for block `(4,5)`

## Question

Does commit `8aa3356e76d30f9a198f5032c9d16bab284ef768` already isolate explicit PSD link terms in the DH mass sum whose principal `(4,5)` block is bounded below by a q-independent or domain-explicit matrix stronger than the global regularizer `(1/1000000) I`, with `regularization=0` and `regularization=1e-6` stated separately?

## Decision

**No. Keep `admission_label: pending`.** This snapshot does not contain the deployed `routeB_dense_Mq/dhport_lib.jl` source, `routeB_Mq_M0.csv`, or a formula-level principal-block PSD decomposition. The nearest in-tree leaves are either entrywise regularizer algebra, a scalar `M33` Fourier child, a semantic body-prefix interface, or a source-free six-link Gram identity. None states a `2x2` lower bound stronger than `(1/1000000) I`.

This is not a rejected false inequality: no numerical principal-block bound was re-derived or disproved. It is not `compiled_candidate` for this child, because historical receipts belong to different theorem contracts and were not re-executed here. It is not `verified` and not architecture-only.

## Evidence inspected (read-only)

1. **Required deployed geometry is not in this commit.**
   The queue names `routeB_dense_Mq/dhport_lib.jl:31-60` and `routeB_Mq_M0.csv` as the only reference snapshot. Neither path is present under `examples/`. No in-tree file states a principal subblock `M[{4,5},{4,5}](q) ≽ c I_2` with rational `c > 1/1000000`, nor the matching unregularized statement `c = 0` obstruction.

2. **Regularizer leaf is entrywise and premise-conditional.**
   `examples/routeb_mass_regularizer_lean/MassRegularizer.lean` (blob SHA `f3e1dd70f7fed2acfd53017064829ab135d5523f`) defines `addMassRegularizer M i j = M i j + if i = j then (1/1000000) else 0`. The theorems `addMassRegularizer_diag`, `addMassRegularizer_offdiag`, `regularized_entry`, and `regularizer_is_constant` only transport that diagonal constant. `regularized_entry` assumes `unregularizedDHMass q i j = evalFourierMass q i j` and does not prove it. README (blob `9c007b0e604703c1a4b190baf473d8adc7d5520b`) explicitly excludes DH/Fourier identity and Float64 equality. This is the `regularization=1e-6` statement, not a Jacobian lower bound that beats it.

3. **Scalar M33 child is not the principal block.**
   `examples/routeb_m33_exact_lower_lean/README.md` (blob `9fe352f016b8a1b1aea3bfcfbac5e02aa6d7bf7d`) records `M33(q) >= 3016537/12000000` from a cosine polynomial in `q4,q5`, under `cos` range hypotheses. That is one diagonal entry, not a PSD comparison of the `(4,5)` principal submatrix, and the README leaves parser/source equality, rounding, inverse bounds, and admission open. It cannot be reused as the requested block bound.

4. **Body-prefix and six-link identities do not instantiate the Jacobian geometry.**
   - `examples/routeb_block45_body_prefix_lean/README.md` (blob `c2350abcd6fb4466782d3ad1b5d5bd82b56f02ed`) instantiates link-4/5 semantic cutoffs and a midpoint COM interface. It says the frame prefix stays abstract and no DH matrix entries are unfolded.
   - `examples/routeb_six_body_isotropic_mass_lean/SixBodyIsotropicMass.lean` (blob `19413249dda06b7953a9b96dc1d56b071322e788`) proves `massFromLinks_scalarIdentity`: each entry is a sum of mass times `Jv` row Gram plus scalar times `Jw` row Gram. It does not choose DH axes, rank, or a positive principal minor. The zero-Jacobian corollary is an identity under a degenerate hypothesis, not coercivity.
   - `examples/routeb_p3_mass_entry_bridge_lean/README.md` (blob `3d6655727e7dc9af89dd22bd870655463da6c8d8`) keeps `MExact` and `MFloat` independent and treats `1/1000000` as metadata only.

5. **No pinned command was run.**
   `verify.sh` scripts in these leaves hardcode external Lean paths and were not executed. `#print axioms` lines in the Lean sources are directives, not a captured axiom list from this pass. No sampled eigenvalue or `M0_BB` table was used as evidence.

## Exact obstruction for the next owner

A consumer of P3-009 still needs, as separate statements:

- source equality between deployed `dhport_lib.jl` link-Jacobian terms and the mass sum, with the file hash;
- the principal `(4,5)` Gram contribution of each link, split into translational and rotational parts;
- either a rational `c` and a domain on which that principal block is `≽ c I_2` with `regularization=0`, or a rank/cell witness showing the unregularized block can be singular or below every candidate stronger than `1/1000000`;
- the regularized statement only as `unregularized block + (1/1000000) I_2`, not as a substitute for the Jacobian bound.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P3-011` open.
- Requested action: do not register a block-(4,5) structural lower bound; do not edit registry, `state.json`, or formal certificates.
- Next owner should attach the missing DH Jacobian packet or a concrete rank/cell obstruction. Do not recompile the regularizer or M33 sidecar as if it were this child.

## Forbidden-boundary compliance

- Did not identify `M0_BB` with `M(q)`.
- Did not use sampled eigenvalues or Float64 analytic differentiation.
- Did not close P3, P4, or M4.
- Did not promote an unexecuted Lean receipt or a Python checker to the verified registry.
- Did not edit registry, state, or formal proofs.
