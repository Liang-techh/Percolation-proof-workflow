---
kind: review_result
review_id: review-T-P4-015-liuchuanafeng-20261002T2013Z
source_agent: 流川枫
created_at: 2026-10-02T20:13:00Z
inspected_commit: 386bb041aaf6f49187e1ddec3bc30ceeee080cd6
claim_commit: 83ec888634e62f40cabc407b5a6cd199ff555be0
inspected_paths:
  - agent_review_inbox/task_queue.md
  - scripts/check_routeb_nominal_distal_contract.py
  - src/percolation_workflow/routeb_nominal_distal_contract.py
task_id: T-P4-015
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
---

# T-P4-015 audit: nominal distal bridge intake is a shape candidate, not the required port theorem

## Question

At content commit `386bb041aaf6f49187e1ddec3bc30ceeee080cd6`, does the in-repo nominal distal contract already bind `a_D = S*y + r_hat*z/rho`, the reduced descriptor equation, and the retained `M_BD*S*y` port, with exact evidence for the rational direction, `rho`, the retained polynomial, and the full `M0_BB` tail PMI, so that `T-P4-015` can leave `open`?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The queue still marks `T-P4-015` open. The dedicated checker only compares two external CSV shapes to frozen metric dictionaries. A matching shape returns `EXACT_DESCRIPTOR_BRIDGE_CANDIDATE` and still leaves `formal_certificate_allowed=false` and `registry_eligible=false`. That status is not a proof of the acceleration split, not a proof of the retained port, and not a Lean receipt.

This pass did not execute the checker. Default inputs live outside this repository (`../6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`). No exit code is claimed. This is not `compiled_candidate`, not `verified`, and not `rejected`: the fail-closed interface matches the declared intake leaf. It is not `architecture_only`: the missing objects are the external CSV execution, the split/port identity itself, and the tail PMI evidence named in the queue.

`review-T-P4-015-liuguanyi-20260907T0326.md` derives a slice-Lipschitz transport into a Schur consumer. That is a different interface. It is not a receipt for this descriptor-bridge leaf and is not overwritten.

## Evidence inspected (read-only)

1. **Queue contract is still open.** Required deliverable: exact source/interval/Lean evidence for the rational direction, `rho`, the retained polynomial, and the full `M0_BB` tail PMI. Forbidden: replacing the retained port by a coarse `||a_D||` bound, treating artifact shape as proof, or claiming global coverage. Local progress note on the same entry says the two CSV contracts are checked and the tail scalar/Gram/reconstruction lane is recorded separately; source execution and pinned Lean remain open. This review does not treat that note as a certificate.

2. **Checker blob.** `scripts/check_routeb_nominal_distal_contract.py` blob `8cbe4eb2a0a4f1772d53abb63ac790aaf1024878`. It reads only
   - `routeB_compact_dh_nominal_distal_bridge_audit.csv`
   - `routeB_compact_nominal_descriptor_interface.csv`
   hashes their concatenated bytes, copies a `controller_source_sha256` field if present, and calls `audit_routeb_nominal_distal_bridge`. Exit `0` is returned only when status is `EXACT_DESCRIPTOR_BRIDGE_CANDIDATE`; otherwise exit `2`. The module docstring says it audits the CSV pair. It does not load the retained polynomial, `rho`, or `M0_BB`.

3. **Bridge audit contract.** `routeb_nominal_distal_contract.py` blob `b6ea54e0968d4297e1494c6989e1f12452cff6ee`. The file docstring says the checker validates exact artifact shape and provenance and does not prove the polynomial inequalities or source semantics. `audit_routeb_nominal_distal_bridge`:
   - requires audit fields including `split_identity_exact=true`, `inverse` not present as a proved substitution, `formal_certificate_allowed=false`, four nominal/reduced rows, and two retained-port rows;
   - requires interface fields `block_B=4;5`, `block_D=1;2;3;6`, `inverse_substitution=false`, plus the three equation strings `M_DD(q)^(-1)*(b_D-M0_DB*a_B)`, `M_DD(q)*v+DeltaM_DB(q)*a_B=0`, and `r_B-M_BD(q)*v=0`;
   - checks coordinate order only;
   - returns `EXACT_DESCRIPTOR_BRIDGE_CANDIDATE` when those strings match.

   Matching `split_identity_exact=true` is an input-shape check. It does not expand `a_D = S*y + r_hat*z/rho` or show that the retained port is `M_BD*S*y` rather than a second charge of the same remote action. The nominal equation string still writes an inverse, while `inverse_substitution=false` is only a flag. The flag does not by itself prove the reduced equation avoided inverse substitution.

4. **Tail objects are declared beside this leaf, not discharged by it.** The same module freezes bridge constants used by a different audit: `r_hat=0,1,-6377/6250,0`, `rho=10616159325566083327957/39062500000000000000000`, `retained_polynomial_terms=46`, and `full_MBB_12=full_MBB_21=153080849893419/50000000000000000000000000000000`, with `evidence_level=algebraic_subcertificate`. `audit_routeb_physical_rational_tail` can recompute `rho` and a scalar Schur identity from optional tail/M0 inputs, and still returns only `EXACT_RATIONAL_TAIL_CANDIDATE` with certificate flags false. That function is not called by the T-P4-015 checker. Its existence does not close the retained-port or tail-PMI deliverable of this task.

5. **No execution in this pass.**

```text
command: not run
exit_code: not claimed
external_audit_csv_sha256: not observed
external_interface_csv_sha256: not observed
controller_source_sha256: not observed
lean_receipt: absent
```

## Obstruction

```text
interface: exact descriptor-bridge CSV shape candidate
checker: scripts/check_routeb_nominal_distal_contract.py
audit: audit_routeb_nominal_distal_bridge
blobs: 8cbe4eb2a0a4f1772d53abb63ac790aaf1024878; b6ea54e0968d4297e1494c6989e1f12452cff6ee
checked: audit/interface metric equality and block order (4,5) / (1,2,3,6)
not_checked_here: a_D=S*y+r_hat*z/rho expansion, retained M_BD*S*y non-double-count, rho identity, 46-term retained polynomial, full M0_BB tail PMI, pinned Lean
adjacent_only: EXPECTED_BRIDGE / audit_routeb_physical_rational_tail
flags: formal_certificate_allowed=false, registry_eligible=false
source_binding: not claimed
```

## Assumptions still required

- run the existing checker on the named external CSVs and record artifact hash, copied source hash, status, and errors;
- a separate exact identity for `a_D = S*y + r_hat*z/rho` and for the retained port `M_BD*S*y`, with an explicit non-double-count ledger against the reduced equation;
- do not discharge `rho`, the retained polynomial, or the `M0_BB` tail PMI by the bridge-shape status; those remain on the tail audit / reconstruction lane;
- a pinned Lean receipt before any parent promotion;
- source equality, domain coverage, and comparator gates remain outside this leaf.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-015` open.
- Requested action: next owner may execute `scripts/check_routeb_nominal_distal_contract.py` and return the printed JSON plus exit code. Do not treat `EXACT_DESCRIPTOR_BRIDGE_CANDIDATE` as verified. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not replace the retained port by a coarse `||a_D||` bound.
- Did not treat CSV shape, `split_identity_exact=true`, or `inverse_substitution=false` as a proof.
- Did not claim global coverage, source binding, or Route-B closure.
- Did not invent an exit code, artifact hash, or Lean axiom list.
- Did not edit registry, state, task queue, or formal proofs.
