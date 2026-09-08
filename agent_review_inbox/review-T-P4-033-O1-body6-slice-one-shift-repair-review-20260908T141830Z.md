---
kind: review_result
review_id: review-T-P4-033-O1-body6-slice-one-shift-repair-review-20260908T141830Z
task_id: T-P4-033-O1-body6-slice
source_agent: codex-body6-math-lane
created_at: 2026-09-08T14:18:30Z
integration_status: pending
status: OPEN_UNCOMPILED
compile_status: OPEN_UNCOMPILED
lean_receipt_status: missing
admission_label: pending
proposed_integration_target: metadata_only
requested_action: review_single_shift_repair_composition_then_obtain_focused_post_repair_Lean_receipts
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ONESHIFTREPAIR20260908.lean
artifact_sha256: a468140373c9fe43b52a3b3e0e15a5a773a437b44361c6b1898ba93af312649b
companion_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ONESHIFTREPAIR20260908.review.md
companion_sha256: b1ec9ecb3de3c9354d13f0135bfad0a41e0822c03eb3b8f1095805656638f89e
---

# BODY6 bounded single-shift repair review

This is advisory evidence for the existing BODY6 task only. The new leaf
and reviewed dependency composition remain **OPEN_UNCOMPILED / pending**.
No registry promotion, proof-obligation closure or state integration is requested.

## Independent arithmetic interface and counterexample

The new 47-line leaf imports only Mathlib. It is an independent arithmetic
consumer; it does not import or certify the pending BODY6 dependency chain.
Its scalar interface is s <= a+beta, g = s+B and (a+beta)+B <= bar,
implying g <= bar. Its typed path interface additionally requires whole-path
membership in D(t), projection of D(t) into Q, and the value identity on Q.

The repaired PATHDOMAINPROJECTION source only commutes cap+B into B+cap.
The aligned consumer's source cap remains a+beta and its shifted budget
remains (a+beta)+B <= bar. Static inspection therefore finds one use of B,
not a second shift. This does not certify caller-supplied a/beta values or
their storage normalization.

The exact saturated counterexample takes B=4079979/400000, s=0, g=B,
cap=0 and bar=B. The single-shift cap holds, while g+B <= bar is false.
A double charge would falsely reject this valid cap; it does not provide
missing source or path evidence.

## Unclosed source, path and Lean dependencies

- No active Alignment instance or identification of the actual source storage
  with the encoded storage is supplied; mass and remainder identities remain
  external premises.
- No actual initial-set cap, starting-point membership, integrated-growth
  estimate or uniform growth budget is supplied. IntegratedGrowth is an
  assumption, not a newly derived trajectory estimate.
- No actual whole-path domain inclusion, configuration projection instance,
  ODE/flowpipe proof or continuous-PDE claim is supplied.
- The new leaf has no Lean compilation or kernel/axiom receipt.
- No successful post-repair PATHDOMAINPROJECTION receipt was established.
  INITIALPATHCAPS, ACTUALSTORAGEALIGN and ALIGNEDPATHCAPCONSUMER still need
  dependency-aware focused compilation before any compiled-chain claim.

The inspected receipt
`review-T-P4-033-O1-body6-slice-lean-receipt-codex-20260908T052153.md`
records a pre-repair PATHDOMAINPROJECTION elaboration failure and an
INITIALPATHCAPS import blockage. It is not post-repair success evidence.
The current repaired PATHDOMAINPROJECTION SHA-256 inspected here is
`557a732c06cf774e49e75a811e1a01c910617ec011e0f84e5de72f0919a16f5b`.
The companion review pins the other inspected sources and historical receipt.

ACTUALSTORAGEALIGN.aligned_path_cap_transfer_attempt contains the same
add_le_add_right/trans spelling as the historical failed site. This is a
static elaboration risk for a future focused check, not a new observed
compiler failure. The aligned consumer uses the shifted-value lemma, but
the entire imported module must still elaborate.

## Validation and boundaries

Only bounded source/receipt inspection and read-only envelope/hash checks
were performed. No Lean/Lake, source audit script, broad regression or inbox
integrator ran. Existing leaves, receipts, registry and state were not edited
by this review. All source/path premises and post-repair compilation remain open.
