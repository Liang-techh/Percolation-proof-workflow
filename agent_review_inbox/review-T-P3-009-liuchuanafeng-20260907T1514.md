---
kind: review_result
review_id: review-T-P3-009-liuchuanafeng-20260907T1514
source_agent: 流川枫
created_at: 2026-09-07T15:14:00-06:00
inspected_commit: c23cbeddeec80a1cec2375cc73d0548ef2ec100d
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_source_binding_audit/REPORT.md
  - examples/routeb_source_binding_audit/SHA256SUMS.csv
  - examples/routeb_source_binding_audit/snapshots/original_target/routeB_pmi_certificate.jl
  - examples/routeb_source_binding_audit/snapshots/original_target/routeB_Mq_M0.csv
  - examples/routeb_source_binding_audit/snapshots/current_exact/ReferenceMass.lean
integration_status: pending
admission_label: pending
---

# T-P3-009 audit: block-(4,5) positivity / inverse bounds

## Question

Does the current repository snapshot already contain an exact rational lower bound for the *covered* block-(4,5) positive matrix `M_BB(q)` and corresponding inverse-entry upper bounds suitable for `T-P7-002` / the P4 sharp Schur child?

## Decision

**No.** The only exact 2x2 object in-tree is a frozen *reference* block `M0_BB` assembled from diagonal entries of a constant `M0`, not a proved enclosure of the deployed `M(q)` on a covered q-box. Inverse-entry bounds for the actual covered block are therefore not admissible from this snapshot.

`admission_label: pending` — obstruction / missing source-functional identity, not a rejected false claim and not architecture-only speculation.

## Evidence inspected (read-only)

1. **PMI source uses constant `M0`, then drops off-diagonals.**
   `routeB_pmi_certificate.jl` sets `ja, jb = 4, 5`, loads `routeB_Mq_M0.csv` as `Float64`, and builds
   `M0_BB = [M0[ja, ja] 0.0; 0.0 M0[jb, jb]]`.
   That is an explicit structural choice: even the CSV off-diagonal `M0[4,5]` (order `1e-18` Float64 noise) is replaced by exact `0`. The same file then uses only `M11 = M0_BB[1,1]` and `M22 = M0_BB[2,2]` as scalar denominators in the PMI residual map. This is not a theorem that `M_BB(q)` is diagonal, positive-definite, or bounded below on the declared `q_lim` box.

2. **CSV `M0` is a decimal snapshot, not a proved `M(q)` identity.**
   Snapshot `routeB_Mq_M0.csv` (sha256 `28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40`, 654 bytes per `SHA256SUMS.csv`) records 1-based entries
   `M0[4,4] ≈ 0.116667666666667`, `M0[5,5] ≈ 0.05018475`, `M0[4,5] ≈ 3.06e-18`.
   `REPORT.md` B45-1 states the functional identity
   `M_FD(q) = EvalFourier(...) + 10^{-6} I = mass_matrix(q)` is **OPEN**. Only the reconstruction `CSV mass at q=0 = Lean M0` is derived-exact.

3. **Lean `M0` gives an exact *candidate* 2x2 at q=0, nothing more.**
   `ReferenceMass.lean` (physical axes 4,5 = `Fin` 3,4) has
   `M0[3,3] = 350003/3000000`, `M0[3,4] = 0`, `M0[4,3] = 0`, `M0[4,4] = 200739/4000000`.
   These rationals match the CSV diagonals and the PMI zero-off-diagonal pattern.
   Existing Lean theorems (`M0_symmetric`, `rowAbs_lt_one`, `M0_dsos_identity`, `M0_le_identity`) bound the *full 6x6 reference* `M0` from above by `I`; they do **not** produce a lower bound on the 2x2 block of `M(q)`, nor any inverse-entry bound.
   `reference.json` flags recorded in `REPORT.md`: `Lean_compiled=false`, `physical_DH_identification_proved=false`, `Float64_binding_proved=false`.

4. **Candidate arithmetic that must not be promoted.**
   *If* one illicitly identified the covered block with this frozen diagonal `M0_BB`, the matrix would be SPD with
   `det = (350003/3000000)*(200739/4000000)` and inverse diagonals
   `3000000/350003` and `4000000/200739`.
   That calculation is recorded only as a *counterfactual*: the task explicitly forbids treating constant `M0_BB` as `M(q)` without proof. No LDL/eigenvalue certificate for `M_BB(q)` on a covered cell exists in the inspected tree.

5. **PMI model mismatch remains orthogonal and blocking for consumers.**
   `REPORT.md` B45-5: PMI block model injects `kc=0.05` cross terms that are absent from deployed `tau` in `dhport_lib.jl:102-109`. Even a future exact `M_BB(q)` bound would not by itself license P4 Schur consumption of the current PMI residual.

## What would close this leaf (not done here)

- A source-bound identity or interval enclosure of `M_BB(q)` on an explicit covered q-box, with index/order ledger and regularizer `10^{-6}` charged.
- Then an exact rational (or Lean) lower bound `M_BB(q) 〈 λ I` or LDL witness, plus inverse-entry upper bounds.
- Separate semantic adapter if the consumer still uses `M0` diagonals and zero off-diagonals.

## Integration target and requested action

- Target: documentation / DAG metadata only. Keep `T-P3-009` open.
- Requested action: do **not** promote any `M0_BB` inverse candidate; do **not** touch registry, `state.json`, or formal certificates.
- Next smallest math child remains B45-1 (full `M(q)` reconstruction) or a single-cell exact `M_BB(q)` enclosure that does not assume `M(q)=M0`.

## Commands / hashes

- Inspected commit: `c23cbeddeec80a1cec2375cc73d0548ef2ec100d`
- No Lean/Julia/checker executed in this pass (GitHub-only read of pinned snapshots).
- Snapshot hashes: as in `examples/routeb_source_binding_audit/SHA256SUMS.csv`.
- Exit code: n/a (documentation audit).

## Forbidden-boundary compliance

- Did not treat `M0_BB` as `M(q)`.
- Did not use sampled eigenvalues as global bounds.
- Did not claim P3/P4/M4 closure.
- Did not edit registry / state / formal proofs.
