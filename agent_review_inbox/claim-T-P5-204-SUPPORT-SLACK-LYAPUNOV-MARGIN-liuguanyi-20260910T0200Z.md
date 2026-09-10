---
kind: task_claim
task_id: T-P5-204-SUPPORT-SLACK-LYAPUNOV-MARGIN
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-10T02:00:00Z'
lease_expires_at: '2026-09-10T03:00:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-192, T-P5-200-GAUGE-INVARIANT-AFFINE-AMPLITUDE-CUBIC-ABSORPTION, T-P5-203-PSD-SHARP-POLAR-SCHUR-DUAL]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---

# Claim — T-P5-204 support-slack Lyapunov margin

I claim the margin-sensitivity seam explicitly left by T-P5-203: quantify exactly how an overestimate in the support cap `B` propagates through T-P5-200's quadratic debit and the downstream cone-wise copositivity/decay gate. The intended deliverable is a minimal monotonicity/threshold theorem, a checker-friendly no-division formulation, an exact obstruction/contact interpretation, and a rational slack-routing corollary. Mathematics only; no provenance/admission audit, source promotion, Lean receipt, or parent closure.