---
kind: task_claim
task_id: T-P4-036-MATH-FK-TELESCOPE
parent_task_id: T-P4-036
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-08T04:18:00-06:00
status: claimed
admission_label: pending
base_commit: 220fd8e3ad4e5525f0f7e53724a96fd16e58a7a0
---

# Claim — exact-real DH link/FK telescoping bound

The previously claimed `T-P4-036-MATH-12ROW-PHASE-CANCEL` target is already materially covered by the earlier `T-P4-036.2` all-12 phase-cell review and its compiled Lean sidecar. I therefore do not repeat that proof.

This child takes the next smallest mathematical step inside the still-open finite-DH propagation leaf: for the standard real DH transform, derive a phase-independent exact Frobenius difference identity for one link and a rational square bound for a finite product of links. The goal is to turn per-angle real-lift errors into a compact exact-real FK/frame perturbation budget without intervalizing every trig entry independently.

Scope is mathematics only. No Float64/libm semantics, deployed source identity, COM/Jacobian/M/C/G propagation, P8 coverage, receipt/provenance, admission, or registry mutation is claimed. This does not overlap `T-P4-022`, which is the generic matrix-action Frobenius consumer; here the new content is the DH-specific exact norm identity and product telescoping constant.
