---
kind: review_result
review_id: review-T-P3-009-liuchuanafeng-20261019T0811Z
source_agent: 流川枫
created_at: 2026-10-19T08:11:37Z
inspected_commit: afedcc27cf8cd2fc5569c2c286a9b1d917f5453b
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P3-009-liuchuanafeng-20260907T1514.md
  - examples/routeb_source_binding_audit/REPORT.md
  - examples/routeb_source_binding_audit/snapshots/original_target/routeB_Mq_M0.csv
  - examples/routeb_source_binding_audit/SHA256SUMS.csv
admission_label: pending
---

# T-P3-009 review — block-(4,5) positive-block and inverse bounds (audit)

## Question inspected
Whether current inbox/source snapshots already supply a rational lower bound for the covered block-(4,5) matrix `M(q)_BB` and corresponding upper bounds on its inverse entries, suitable for consuming downstream Schur children, or whether a cell/source mismatch prevents it.

## Evidence
Read-only inspection of the existing bounded source-binding audit (REPORT.md, SHA 8bc5cd5444473396caa13af107428f0350cca742) and the frozen `routeB_Mq_M0.csv` snapshot.

Key facts from REPORT.md:
- CSV mass at q=0 + 1e-6 I equals the literal Lean `M0` entry-for-entry (derived exact arithmetic).
- Full functional identity `M_FD(q) = EvalFourier(...) + 1e-6 I = mass_matrix(q; reg=1e-6)` remains OPEN (B45-1). No theorem binds DH transform order, parent-axis, COM, rotational convention, and regularizer for all q in the domain.
- PMI certificate loads only constant `M0` and introduces `kc` cross terms absent from the actual `tau` equation (B45-5 mismatch flag).
- Classification table explicitly marks "Full `M(q)` = Lean/source Fourier evaluator" as OPEN and "PMI block model = actual block dynamics" as OPEN / MISMATCH FLAG.
- No eigenvalue/LDL route or domain-restricted rational lower bound for the variable block-(4,5) is present; sampled or constant `M0_BB` cannot be substituted.

`routeB_Mq_M0.csv` provides only the single numerical point (approximately the regularized M at zero), not an interval or functional bound.

No commands were executed (read-only document audit). No source hashes beyond the REPORT and CSV contents already recorded in the snapshot manifest were recomputed.

## Boundary respected
Did not treat constant `M0_BB` as `M(q)`, did not promote sampled values to global bounds, did not close P3/P4/M4, and did not modify registry, state, or formal proofs.

## Proposed integration
Target: documentation / frontier metadata only.
Requested action: record as pending obstruction. The rational lower-bound / inverse-upper-bound package for covered block-(4,5) is not supplied by current snapshots. Next required child is the open B45-1 full-mass reconstruction (or an explicit domain restriction that makes a constant or interval bound valid) before any Schur consumer can treat the bound as available.

admission_label: pending
