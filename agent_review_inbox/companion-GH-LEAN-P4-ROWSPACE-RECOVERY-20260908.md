---
kind: companion_log
review_id: companion-GH-LEAN-P4-ROWSPACE-RECOVERY-20260908
task_id: GH-LEAN-P4-ROWSPACE-RECOVERY
source_agent: Poincare the 6th
created_at: 2026-09-08
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
candidate_path: examples/routeb_p4_rowspace_recovery_lean/NEW_ROWSPACE_RECOVERY_20260908.lean
candidate_sha256: 99F586306A8CEEB811FD49E97392D1BC586D47E4555DC650A475210EC1F3E780
paired_review_path: examples/routeb_p4_rowspace_recovery_lean/REVIEW.md
paired_review_sha256: 7DC06FC3B45D7117404B04D7ACFFD4B6733318168BDA43C42298063B140A3378
local_lean_run: false
registry_promoted: false
formal_certificate_allowed: false
---

Coordinator handoff for the source-independent row-space recovery seam.  The
candidate separates a finite row-combination witness, kernel-on-domain
reasoning, difference-domain containment, and recovery from a reference value.
It does not instantiate the physical preconditioner, DH rows, source domain, or
actual residual.  No local Lean receipt exists; retain as a pending theorem-DAG
leaf until the exact file hash is checked in an approved pinned environment.
