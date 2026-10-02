---
kind: review_result
review_id: review-T-P4-016-liuchuanafeng-20261002T2316Z
source_agent: 流川枫
created_at: 2026-10-02T23:16:00Z
inspected_commit: 3bc8aaa5829b53526d50d050accbfdabb600427c
claim_commit: 59f24df0c72bd11e9b30a06a739b77a8badbf579
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P4-016-liuchuanafeng-20261002T2313Z.md
  - agent_review_inbox/review-T-P4-016-kuangmanmozun-20260907T0344.md
  - src/percolation_workflow/routeb_nominal_distal_contract.py
  - scripts/check_routeb_nominal_distal_contract.py
task_id: T-P4-016
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
---

# T-P4-016 audit: tail PMI intake is a scalar/Gram candidate, not a 3x3 positivity theorem

## Question

At content commit `3bc8aaa5829b53526d50d050accbfdabb600427c`, does the in-repo nominal-distal tail contract already prove the square-root-free 3x3 PMI with the full off-diagonal `M0_BB`, with an exact polynomial identity or pinned Lean receipt that is distinct from candidate Gram data, so that `T-P4-016` can leave `open`?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The queue still marks `T-P4-016` open. The in-repo functions freeze metadata and, only when optional external CSVs are supplied, check a scalar Schur identity or exact LDL on candidate Gram blocks. Both success statuses keep `formal_certificate_allowed=false` and `registry_eligible=false`. Neither status is a proof of the 3x3 PMI, and neither is a Lean receipt.

This pass did not execute a checker. The named inputs (`routeB_physical_rational_tail_pmi_scalar.csv`, tail metadata, complete `M0_BB`) are not in this repository. No exit code is claimed. This is not `compiled_candidate`, not `verified`, and not `rejected`: the fail-closed candidate interface matches the declared intake leaf. It is not `architecture_only`: the missing objects are the external polynomial/Gram execution, the 3x3 identity itself, and the kernel receipt named in the queue.

`review-T-P4-016-kuangmanmozun-20260907T0344.md` derives an aggregate execution-remainder Schur budget and a shared-reserve counterexample. That is a different interface. It does not consume `M0_BB`, the 27-term scalar, or the 3x3 PMI, and it is not overwritten.

## Evidence inspected (read-only)

1. **Queue contract is still open.** Deliverable: exact polynomial identity, circle/domain multipliers or Lean proof, and a receipt that separates candidate Gram data from kernel verification. Forbidden: two independent component gains, floating PSD, sampled positivity, or global coverage / residual / flowpipe closure. Owner notes assign exact rational/SOS work and a pinned Lean scalar/3x3 adapter to other lanes; this review does not take those lanes.

2. **Bridge checker does not call the tail audit.** `scripts/check_routeb_nominal_distal_contract.py` blob `8cbe4eb2a0a4f1772d53abb63ac790aaf1024878` only calls `audit_routeb_nominal_distal_bridge`. A match returns `EXACT_DESCRIPTOR_BRIDGE_CANDIDATE`. That is the `T-P4-015` shape leaf, not `T-P4-016`.

3. **Tail seam is metadata plus an optional scalar identity.** `routeb_nominal_distal_contract.py` blob `b6ea54e0968d4297e1494c6989e1f12452cff6ee`. `audit_routeb_physical_rational_tail` requires frozen bridge fields including `full_MBB_12 = full_MBB_21 = 153080849893419/50000000000000000000000000000000` and tail metadata `pmi_dimension=3`, `schur_scalar_dimension=1`, `scalar_terms=27`, `scalar_max_total_cs_degree=6`, `delta_sq=1/160000`, `energy_accounting=tail_only_no_double_count`, `evidence_level=algebraic_sos_input_candidate`. The scalar CSV must have 27 terms, degree 6, and support only on exponents `e5..e10`. If both a tail polynomial CSV and a 6x6 `M0` matrix are supplied, it recomputes `rho` and compares the scalar polynomial to

```text
(1/160000) * rho * det(M_BB) - M_BB_22 * t1^2 + 2 * M_BB_12 * t1 * t2 - M_BB_11 * t2^2
```

with `M_BB` the index block `(3,4)`. A match returns `EXACT_RATIONAL_TAIL_CANDIDATE`. That is a 2x2 Schur scalar identity against a supplied polynomial. It does not assemble a 3x3 matrix, does not prove that scalar is nonnegative on the circle/domain, and does not run unless those external files are passed. Matching `pmi_dimension=3` is a string check.

4. **Gram audit is candidate LDL, not the PMI theorem.** `audit_routeb_physical_rational_gram` requires `EXPECTED_GRAM_AUDIT` with `status=PASS`, `exact_bareiss_positive=true`, `gram_blocks=14`, `max_gram_dimension=83`, `formal_certificate_allowed=false`, and `evidence_level=rigorous_numerical_tail_subcertificate_candidate`. It then runs exact LDL on each dense symmetric block and checks three equality-multiplier groups. Success is `EXACT_RATIONAL_GRAM_CANDIDATE`. The returned object still sets `formal_certificate_allowed=false` and `registry_eligible=false`. LDL positivity of supplied blocks is not the polynomial identity that those blocks reproduce the 3x3 PMI, and it is not a Lean kernel receipt. The reconstruction function that would compare coefficients is `audit_routeb_physical_rational_gram_reconstruction`; its docstring says it admits only a candidate margin and never promotes the verified registry. That function belongs to the separated `T-P4-017` leaf and is not treated here as a `T-P4-016` discharge.

5. **No execution in this pass.**

```text
command: not run
exit_code: not claimed
external_scalar_csv_sha256: not observed
external_m0_csv_sha256: not observed
external_gram_csv_sha256: not observed
lean_receipt: absent
```

## Obstruction

```text
interface: exact rational tail / Gram candidate
module: src/percolation_workflow/routeb_nominal_distal_contract.py
blob: b6ea54e0968d4297e1494c6989e1f12452cff6ee
checker_not_this_leaf: scripts/check_routeb_nominal_distal_contract.py (bridge only)
tail_status_if_inputs_match: EXACT_RATIONAL_TAIL_CANDIDATE
gram_status_if_inputs_match: EXACT_RATIONAL_GRAM_CANDIDATE
checked_only_if_external_csv_supplied: frozen M0_BB off-diagonal string, 27-term scalar support, optional 2x2 Schur scalar identity, 14-block exact LDL
not_checked_here: 3x3 PMI matrix identity, circle/domain nonnegativity, kernel verification of Gram data, pinned Lean scalar/3x3 adapter
flags: formal_certificate_allowed=false, registry_eligible=false
source_binding: not claimed
```

## Assumptions still required

- execute `audit_routeb_physical_rational_tail` on the named external scalar, metadata, and complete `M0_BB`, and record artifact hash, status, and errors;
- a separate exact identity for the square-root-free 3x3 PMI, using the full off-diagonal `M0_BB`, not two independent component gains and not the scalar Schur string alone;
- circle/domain multipliers or a pinned Lean proof, with Gram LDL kept as candidate data until a kernel receipt exists;
- do not discharge this leaf by `T-P4-017` reconstruction or by the 2026-09-07 aggregate-budget review;
- source equality, domain coverage, residual absorption, and flowpipe closure remain outside this leaf.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-016` open.
- Requested action: next owner may run the tail audit on the named external CSVs and return status, errors, and hashes. Do not treat `EXACT_RATIONAL_TAIL_CANDIDATE` or `EXACT_RATIONAL_GRAM_CANDIDATE` as verified. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not use two independent component gains as a 3x3 PMI.
- Did not treat floating PSD, sampled positivity, `status=PASS`, or `exact_bareiss_positive=true` as kernel verification.
- Did not claim global coverage, residual closure, or flowpipe closure.
- Did not invent an exit code, artifact hash, or Lean axiom list.
- Did not edit registry, state, task queue, or formal proofs.
