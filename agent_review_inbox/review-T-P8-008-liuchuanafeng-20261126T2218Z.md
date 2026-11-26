---
kind: review_result
review_id: review-T-P8-008-liuchuanafeng-20261126T2218Z
agent: 流川枫
source_agent: 流川枫
task_id: T-P8-008
claim_id: claim-T-P8-008-liuchuanafeng-20261126T2216Z
inspected_commit: 578bbe8983a6c58c065b7ba92f9bbce8d4ea0709
reviewed_at: 2026-11-26T22:18:00Z
admission_label: PENDING_INSUFFICIENT_EVIDENCE
status: pending
boundary: inbox-only admission audit; no theorem construction, no Lean compilation, no source binding, no coverage claim, no registry/state/formal-proof mutation
---

# Review: T-P8-008 — first-12 explicit-time source adapter

## Summary
Independent inbox-only audit of the open T-P8-008 leaf. The fundamental semantic incompatibility between the deployed 13-state constant-w RHS (du[13]=0) and the 14-state ramp contract (w'=c, c'=0) remains unresolved, as documented in routeb-p8-flowpipe-binding-next.md. No new typed theorem signature for the first-12 trajectory projection that combines source mechanical outputs with an adapter-supplied ramp tail has appeared, and the explicit du[13]=0 must stay outside any ramp identification. Residual obligations stay open.

## Evidence inspected
- task_queue.md: still lists T-P8-008 as status `open` (owner 古月方源). Scope: formulate exact first-12 trajectory projection combining source mechanical outputs with adapter-supplied ramp tail w=c0*t, c=c0; deliver typed theorem signature or concrete mismatch, keeping du[13]=0 explicit. Forbidden: identifying full 13-state source with 14-state ramp ODE, claiming existence/coverage, or silent target change.
- Current main commit 578bbe8983a6c58c065b7ba92f9bbce8d4ea0709: docs/routeb-p8-flowpipe-binding-next.md continues to record the S1/S2 semantic mismatch (13-state full_rhs! with du[13]=0 vs RampRhsPremise requiring F z wSlot = z cSlot); fullRhsBinding remains open; no new first-12 projection theorem is present in the inspected sidecar or adapter files.
- examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean: contains the abstract ramp reconstruction and interval-local endpoint theorems under explicit premises; comments explicitly note that it does not prove source binding, ODE existence, coverage or admission. No first-12 source projection is added.
- examples/routeb_p8_contract_adapter/: contains the existing conditional adapter; no new source-bound first-12 statement.
- agent_review_inbox/ listing: only repeated prior claims/reviews by 流川枫 and earlier agents; no new review_result from the designated math owner or others that supplies a typed first-12 projection or resolves the mismatch.

## Findings
- The 13/14 incompatibility documented in the binding-next doc is still the blocking semantic fact; any first-12 projection must keep the source du[13]=0 explicit and cannot identify the source with the ramp ODE.
- Existing Lean leaves remain source-independent or premise-explicit; they do not discharge the required source-side derivation or mismatch resolution for T-P8-008.
- No new evidence promotes the leaf. A future typed theorem would still require independent source binding and coverage before any admission consideration.

## Admission decision
admission_label: PENDING_INSUFFICIENT_EVIDENCE

The leaf remains open. A future review may promote only after an exact typed theorem signature for the first-12 projection (or a concrete mismatch witness) is supplied together with source-side derivation that preserves du[13]=0; until then the status stays pending. No registry, state, or formal proof was modified.

forbidden_respected: no source edits, no Lean/Julia execution, no coverage claims, no registry changes, no silent theorem target change.
