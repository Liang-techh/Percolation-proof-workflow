---
kind: review_result
review_id: review-T-P3-017-liuchuanafeng-20261002T0414Z
source_agent: 流川枫
created_at: 2026-10-02T04:14:00Z
inspected_commit: a22508cc5b6dceba914b79b2457e2cf0266b9bf7
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_six_body_isotropic_mass_lean/SixBodyIsotropicMass.lean
  - examples/routeb_six_body_isotropic_mass_lean/README.md
  - examples/routeb_six_body_isotropic_mass_lean/FINAL_RECEIPT.md
  - examples/routeb_six_body_isotropic_mass_lean/ATTEMPT_HISTORY.md
  - examples/routeb_six_body_isotropic_mass_lean/verify.sh
  - examples/routeb_isotropic_link_mass_lean/IsotropicLinkMass.lean
  - examples/routeb_isotropic_link_mass_lean/FINAL_RECEIPT.md
  - examples/routeb_isotropic_inertia_lean/IsotropicInertia.lean
  - examples/routeb_isotropic_inertia_lean/README.md
task_id: T-P3-017
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P3-017 admission probe: rotational prefix mass lower-bound lift

## Question

Does commit `a22508cc5b6dceba914b79b2457e2cf0266b9bf7` already contain the external exact-checker packet `P3.rotational_prefix_mass_lower_bound` / `routeB_compact_rotational_mass_lower_certificate.csv`, and a statement that turns six positive principal minors into `M(q) ⩾ 9401/1000000 I` from isotropic inertia and unit DH-axis semantics?

## Decision

**No. Keep `admission_label: pending`.** The named certificate and predicate are absent from this snapshot. The nearest in-tree Lean children are source-free algebraic identities. They do not state the numerical lower bound, the six principal minors, q-independence, or unit DH-axis semantics.

This is not a rejected false inequality: the bound was not re-derived and was not disproved. It is not `compiled_candidate` for this child, because the historical receipts belong to different theorem contracts and were not re-executed here. It is not `verified` and not architecture-only.

## Evidence inspected (read-only)

1. **Required source packet is not in this commit.**
   Queue scope names `P3.rotational_prefix_mass_lower_bound` and `routeB_compact_rotational_mass_lower_certificate.csv`. No path under `examples/` matches `rotational_prefix`, `compact_rotational`, `mass_lower`, or `9401`. GitHub code search for those identifiers in this repository returned no hits (`incomplete_results` may hide matches, so absence is also checked against the recursive `examples/` tree at this commit). Principal-minor values and the certificate source hash therefore cannot be reported from this snapshot.

2. **Nearest algebraic child does not state the lift.**
   `examples/routeb_six_body_isotropic_mass_lean/SixBodyIsotropicMass.lean` (blob SHA `19413249dda06b7953a9b96dc1d56b071322e788`) proves:
   - `massFromLinks_scalarIdentity`: under `inertia k = scalarIdentity (scalar k)`, the `(i,j)` entry of `massFromLinks` equals the six-link sum of `mass k * Jv` row Gram plus `scalar k * Jw` row Gram;
   - `massFromLinks_scalarIdentity_congruent`: if every `Jv` and `Jw` entry is zero, that entry is zero.
   Neither theorem mentions `M(q)`, `9401/1000000`, principal minors, DH axes, or a prefix map. The zero-Jacobian corollary is an identity under a degenerate hypothesis, not a coercivity lower bound. No `sorry` or `admit` appears in this file. `#print axioms` is a directive, not a captured axiom list from this pass.

3. **Upstream identities are rotation/Gram reductions only.**
   - `RouteBIsotropicInertia.rotated_isotropic_eq` (blob `c0bf5d80f6f2017665224449e78c48697f28eb15`): if `R` has orthonormal rows, `R * (s I) * Rᵀ = s I`. It does not instantiate a DH axis or a numerical inertia.
   - `RouteBIsotropicLinkMass.linkMass_scalarIdentity` (blob `d634530e851e2ea43424902eb2227a2b535df521`): entrywise `linkMass` splits into translational mass Gram plus scalar rotational Gram. It does not choose the six link scalars or prove positivity.
   README files explicitly leave concrete Jacobian and Float64 source bindings open.

4. **Historical receipts are not this child's proof.**
   `FINAL_RECEIPT.md` for the six-body leaf records a prior pinned run `output/run-ialqen55` with Lean 4.33.1, Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`, compile exit 0, and `FULL_MASS_BINDING=OPEN`. `verify.sh` hardcodes `/home/z5242/sos_lean` and `/home/z5242/.elan/.../v4.33.1` and was not executed in this pass. The recorded content hash `6b918d4d...` was not recomputed here. Those receipts do not mention the `9401/1000000` threshold or the missing CSV.

## Assumptions still required before the numerical lift

A future consumer must keep these separate; none is discharged here:

- source equality between the missing CSV / `P3.rotational_prefix_mass_lower_bound` and the DH mass formula;
- isotropic scalar inertia for each of the six links, with the exact scalars named;
- unit DH-axis semantics and the exact six-link prefix-map inequality;
- q-independence of the six principal minors, plus the exact minor values;
- the matrix comparison that turns those minors into `M(q) ⩾ 9401/1000000 I`;
- exclusion of translational-only, Coriolis, inverse, and flowpipe readings.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P3-017` open.
- Requested action: do not register a prefix-mass lower bound; do not edit registry, `state.json`, or formal certificates.
- Next owner should attach the missing certificate (hash, six principal-minor values, q-domain) or record a concrete obstruction that the external checker never entered this repository. The pinned Lean slot should not compile the six-body identity again as if it were this child.

## Forbidden-boundary compliance

- Did not use the historical receipt or any checker as Float64 evidence.
- Did not add translational or Coriolis semantics to the identity theorems.
- Did not claim inverse, flowpipe, or P3/formal-gate closure.
- Did not promote a Python checker or an unexecuted Lean run to the verified registry.
- Did not edit registry, state, or formal proofs.
