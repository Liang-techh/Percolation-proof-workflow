---
kind: review_result
review_id: review-GH-MATH-P5-103-REFERENCE-PACKET-PRODUCER-liuchuanafeng-20261004T2012Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-04T20:12:00Z
claimed_at: 2026-10-04T20:10:00Z
inspected_commit: 3f11c617dbb252822676bb716d3cae4a3c839230
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-P5-103-REFERENCE-BINDING-PACKET-SPEC-20260914-Sartre.md
  - agent_review_inbox/review-P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING-20260914-Sartre.md
  - agent_review_inbox/review-GH-MATH-P5-103-REFERENCE-L2-IDENTITY-liuchuanafeng-20261004T1812Z.md
  - agent_review_inbox/review-GH-MATH-P5-103-TRAJECTORY-PROMOTION-GATE-liuchuanafeng-20261004T1912Z.md
task_id: GH-MATH-P5-103-REFERENCE-PACKET-PRODUCER
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
packet_instantiated: false
producer_present: false
proposed_integration_target: documentation
requested_action: harvest_pending_missing_packet_producer_do_not_instantiate_reference
---

# GH-MATH-P5-103-REFERENCE-PACKET-PRODUCER: packet v1 is specified, exporter is absent

## Question

At commit `3f11c617dbb252822676bb716d3cae4a3c839230`, does the repository contain a same-context actual/reference exporter that fills `context.json`, `reference.json`, and `samples.jsonl` under packet schema `routeb-p5-reference-binding-v1`, or only a specification with missing fields?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The producer task is open and fail-closed. The v1 contract is written. No producer file, no three payload files, and no selected reference exist in the inspected tree. This poll does not invent `qbar0=vbar0=0` or `lbar=0`.

This is not `rejected`: no packet bytes were submitted, so there is no hash mismatch, index swap, or wrong residual type to reject. It is not `verified` or `compiled_candidate`: no Lean, Julia, validator, or exporter was run. It is not `architecture_only`: the schema already names the required fields; the blocker is the missing instance.

Roster text still marks 流川枫 unavailable for new dispatch. This file is an inbox-only poll result and does not rewrite that roster, prior authorship, or the Lean/L2/L3 lanes.

## Evidence inspected (read-only)

1. **Release boundary.** `task_queue.md` section `2026-09-14 — next GitHub release batch after revision 890` assigns `GH-MATH-P5-103-REFERENCE-PACKET-PRODUCER` to find or implement a same-context actual/reference exporter against packet v1, and to return exact missing/rejected fields if no instance exists. Compiled candidates and source-independent lemmas cannot enter the verified registry.

2. **Contract exists; instance does not.** `review-P5-103-REFERENCE-BINDING-PACKET-SPEC-20260914-Sartre.md` (blob `f546779f965c67d28110e8d0818be749a8698a9e`) is `SPECIFICATION_ONLY_REFERENCE_UNSELECTED` with `actual_packet_instantiated: false`. It requires three UTF-8 payloads, `context.json`, `reference.json`, `samples.jsonl`, with no default values. Its section 7 says the packet, validator, source-export wrapper, and L1–L3 proofs were not created in that round.

3. **Tree has no producer artifacts.** At the inspected commit, the repository tree has the Sartre specification and later inbox polls, and no path matching `context.json`, `reference.json`, `samples.jsonl`, or a packet-producer module. Inbox names for this task id are only this claim and this review.

4. **Prior binding already records the missing reference.** `review-P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING-20260914-Sartre.md` (blob `f81056cf27d619a9f521d951e772aa22a1ecc067`) reports `MISSING_ACTUAL_REFERENCE_CONTEXT`. Recorded hashes, not recomputed in this poll:

```text
routeB_export_traj.jl 35EBE806A46273068AF1AF937C0C0152378D6889024EC5586BF3C7AABD30ECCF
routeB_state_samples.csv AC0839DA41C789D0F951E814ECF7789E87E8EA1B423AE5520E404022A96B2191
routeB_traj_all.csv 634E9FF32CFCD91DB757F0942ADE8DE1F913C0A50DD0FEDB964AF9C09B53AF7F
routeB_export_manifest.toml 5B61D624F4F6060DA8C33A51FA7982BEF8206D2C3924BABB512440DEFAD89187
```

Those actual exports are not a paired reference. `routeB_traj_all.csv` stores actual `l2=norm(lv)^2`, which the spec rejects as a signed force residual. The export manifest does not record a reference output hash.

5. **Sibling polls do not create a producer.** The 2026-10-04 L2 poll keeps the subtraction identity pending. The L3 poll keeps trajectory promotion pending. Neither file adds `context.json`, `reference.json`, or `samples.jsonl`.

## Missing and rejected fields

Fail-closed class for the absent instance: `pending / MISSING_REFERENCE_FIELD` and `pending / INCOMPLETE_CONTEXT`. No submitted packet is `rejected`.

```text
producer_module: MISSING
context.json: MISSING
  schema routeb-p5-reference-binding-v1: MISSING
  source evaluatorPath/entryPoint/sha256: MISSING in packet
  dependencies including dhport_lib and M0 hashes: MISSING
  producer sourcePath/sha256/runId/runtimeVersion/numericEncoding: MISSING
  configurationValues / Mref parsing / forcing law evidenceRef: MISSING
reference.json: MISSING
  mode descriptor_reference|full_source_reference: UNSELECTED
  selection provenanceRef/initialTime/initialState/timeDomain: MISSING
  qbar0/vbar0: MISSING; must not be defaulted to 0 or copied from actual
  lbarLaw: MISSING; must not be defaulted to 0
  full6InitialState / remote reference state: MISSING if full_source_reference
  trajectoryEvidenceRef: absent => no trajectory admission
samples.jsonl: MISSING
  paired actual q6/v6/a6/l[2] and reference qbarB/vbarB/abarB/lbar[2]: MISSING
  signedResidual = l-lbar: MISSING
  contextKey/referenceKey content hashes: MISSING because payloads are absent
wrong_residual_type: not submitted; existing l2/vbar2 must not be renamed into r
packet_instantiated: false
source_binding_proven: false
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `GH-MATH-P5-103-REFERENCE-PACKET-PRODUCER` open.
- Requested action: harvest this as a pending missing-producer obstruction. Do not treat the Sartre specification, actual CSV rows, or `l2` as a filled packet. Do not close P5. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not implement an exporter, choose a zero reference, copy actual initial data, or set `lbar=0`.
- Did not claim L1 source equality, L2 defect bounds, or L3 interval witnesses.
- Did not rerun trajectories, Lean, Julia, MATLAB, or a validator; no exit code is claimed.
- Did not edit registry, state, task queue, roster, or formal proofs.
