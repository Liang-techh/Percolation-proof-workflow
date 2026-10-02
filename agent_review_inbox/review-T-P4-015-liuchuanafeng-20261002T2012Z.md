---
kind: review_result
review_id: review-T-P4-015-liuchuanafeng-20261002T2012Z
source_agent: 流川枫
created_at: 2026-10-02T20:12:00Z
inspected_commit: 61282c16bac0d8c6de2cb8d72b1f5cc4cc268844
claim_commit: 64073a5df44234df2ffd51e115a79e1825ec85f6
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

# T-P4-015 audit: nominal distal CSV shape is not a descriptor binding

## Question

At commit `61282c16bac0d8c6de2cb8d72b1f5cc4cc268844`, does the in-repo nominal distal contract already prove `a_D = S*y + r_hat*z/rho`, the reduced descriptor equation, and the retained `M_BD*S*y` port, with exact source, interval, or Lean evidence that can enter the verified registry?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The queue still marks `T-P4-015` open. `audit_routeb_nominal_distal_bridge` is a fail-closed string/shape intake for two external CSV contracts. Its dataclass defaults `formal_certificate_allowed=False` and `registry_eligible=False`, and the module docstring says the checker validates artifact shape and provenance only. It does not prove the polynomial identities or source semantics.

This pass did not execute the checker. The default inputs live outside this repository (`../6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`). No exit code is claimed. This is not `compiled_candidate`, not `verified`, and not `rejected`: the in-repo interface matches the declared shape leaf. It is not `architecture_only`: the missing objects are the external payload execution, an exact identity for `a_D = S*y + r_hat*z/rho`, the retained-port polynomial, and a pinned Lean receipt.

`review-T-P4-015-liuguanyi-20260907T0326.md` audits a slice-Lipschitz routing from execution remainders to Schur reserves. It is not a receipt for this nominal distal CSV contract and is not overwritten. The optional `rho` / `M0_BB` scalar identity inside `audit_routeb_physical_rational_tail` belongs to the disjoint `T-P4-016` leaf and is not closed here.

## Evidence inspected (read-only)

1. **Queue contract is still open.** Required deliverable: exact source/interval/Lean evidence for the rational direction, `rho`, the retained polynomial, and the full `M0_BB` tail PMI, binding `a_D = S*y + r_hat*z/rho`, the reduced descriptor equation, and the retained `M_BD*S*y` port without inverse substitution or double-counting. Forbidden: replacing the retained port with a coarse `||a_D||` bound, treating the artifact shape as proof, or claiming global coverage.

2. **Checker blob.** `scripts/check_routeb_nominal_distal_contract.py` blob `8cbe4eb2a0a4f1772d53abb63ac790aaf1024878`. It reads `routeB_compact_dh_nominal_distal_bridge_audit.csv` and `routeB_compact_nominal_descriptor_interface.csv`, hashes their concatenated bytes, copies a `controller_source_sha256` field if present, and calls the audit. Exit `0` is returned only when status is `EXACT_DESCRIPTOR_BRIDGE_CANDIDATE`; otherwise exit `2`. The script does not compute `S`, `rho`, or a port polynomial.

3. **Audit contract.** `routeb_nominal_distal_contract.py` blob `b6ea54e0968d4297e1494c6989e1f12452cff6ee`. `RouteBNominalDistalBridgeAudit` defaults both certificate flags to false, and `audit_routeb_nominal_distal_bridge` never sets them true. The function:
   - requires audit fields including `status=DH_NOMINAL_DISTAL_BRIDGE_AUDIT`, four full/nominal/reduced rows, two retained port rows, `split_identity_exact=true`, and `formal_certificate_allowed=false`;
   - requires interface fields `block_B=4;5`, `block_D=1;2;3;6`, `inverse_substitution=false`, `nominal_remote_equation=M_DD(q)^(-1)*(b_D-M0_DB*a_B)`, `v_descriptor_equation=M_DD(q)*v+DeltaM_DB(q)*a_B=0`, and `force_port_equation=r_B-M_BD(q)*v=0`;
   - rejects coordinate orders other than `(4, 5)` and `(1, 2, 3, 6)`;
   - returns `EXACT_DESCRIPTOR_BRIDGE_CANDIDATE` only when those string mismatches are empty.

   Matching `split_identity_exact=true` or `inverse_substitution=false` is an input-shape check. It is not a proof of `a_D = S*y + r_hat*z/rho`, not a proof that the retained port avoids double-counting, and not a kernel certificate. The recorded remote equation still writes `M_DD(q)^(-1)*...`; the flag `inverse_substitution=false` does not by itself discharge inverse substitution.

4. **Declared constants are not consumed by this leaf.** `EXPECTED_BRIDGE` records `r_hat=0,1,-6377/6250,0`, `rho=10616159325566083327957/39062500000000000000000`, 46 retained polynomial terms, and off-diagonal `M0_BB` entries, but `audit_routeb_nominal_distal_bridge` does not read those fields. They are checked only if a later tail audit is given both the tail polynomial and an `M0` matrix. That check is outside this claim.

5. **No execution in this pass.**

```text
command: not run
exit_code: not claimed
external_payload_sha256: not observed
source_sha256: not observed
lean_receipt: absent
```

## Obstruction

```text
interface: nominal distal descriptor CSV shape candidate
checker: scripts/check_routeb_nominal_distal_contract.py
audit: audit_routeb_nominal_distal_bridge
blobs: 8cbe4eb2a0a4f1772d53abb63ac790aaf1024878; b6ea54e0968d4297e1494c6989e1f12452cff6ee
missing: in-repo payload execution, exact a_D=S*y+r_hat*z/rho identity, retained M_BD*S*y polynomial, pinned Lean receipt
not_discharged_by_string_match: inverse_substitution=false, split_identity_exact=true
flags: formal_certificate_allowed=false, registry_eligible=false
source_binding: not claimed
adjacent_leaf_not_closed: T-P4-016 rho/M0_BB identity
```

## Assumptions still required

- run the checker on the named external CSVs and record artifact/source hashes and the printed error list;
- prove, rather than echo, `a_D = S*y + r_hat*z/rho` and the retained `M_BD*S*y` port on the same source;
- keep inverse elimination and energy double-counting as separate obligations;
- a pinned Lean receipt for the rational direction, `rho`, and the retained polynomial;
- source equality, domain coverage, and comparator gates before any parent promotion.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-015` open.
- Requested action: next owner may execute the existing checker and return the printed JSON plus exit code. Do not treat `EXACT_DESCRIPTOR_BRIDGE_CANDIDATE` as verified. Do not edit registry, `state.json`, or formal certificates. Do not replace the retained port with a coarse `||a_D||` bound.

## Forbidden-boundary compliance

- Did not treat artifact shape as a proof of the distal identity or the retained port.
- Did not replace the retained port with a coarse `||a_D||` bound.
- Did not claim global coverage, residual closure, or source binding.
- Did not invent an exit code, payload hash, or Lean axiom list.
- Did not close `T-P4-016` or overwrite the existing slice-Lipschitz review.
- Did not edit registry, state, task queue, or formal proofs.
