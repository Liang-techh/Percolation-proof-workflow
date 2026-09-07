---
kind: task_claim
task_id: T-P5-025
source_agent: 柳冠一
agent: 柳冠一
claimed_at: 2026-09-07T10:04:00-06:00
inspected_commit: fc37dceca16f676ca0bc7864444899a3d83533f1
continuation_of:
  - review-T-P5-023-liuguanyi-20260907T0916
  - review-T-P5-024-kuangmanmozun-20260907T0945
---

# T-P5-025 claim — direct componentwise transported-gain to P5 dissipation bridge

I claim a new disjoint interface-math child: preserve the full nonnegative transported component matrix `K_path` from T-P5-023 instead of immediately collapsing it to the Frobenius scalar `ell2_path`, and derive a finite exact-rational orthant certificate implying the P5 coupling bound `|(x+y)^T r_c| <= mu Q` directly.

Boundary: source-independent algebra/interface mathematics only. No Lean implementation, source/Jacobian verification, P8 coverage, provenance/audit, admission, or parent closure. T-P5-024 Lean formalization is already owned elsewhere and will not be duplicated.
