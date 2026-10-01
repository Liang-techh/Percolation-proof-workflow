---
kind: review_result
review_id: T-P4-029-LIUCHUANAFENG-20261001T1418Z
task_id: T-P4-029
source_agent: 流川枫
created_at: 2026-10-01T08:18:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 6bc95ebd56577c2a1317db2c58ee6d79ed195d01
---

# T-P4-029 audit: Float64 evaluator enclosure is still open

## Exact question

Does the recorded port formula

```text
R_port(q) = -M_BD(q) * M_DD(mu, q)^(-1) * (M_DB(q) - M0_DB)
```

with `B=(4,5)`, `D=(1,2,3,6)`, `mu=1/1000000`, have a per-certified-box enclosure tying the exact-real/interval evaluator to deployed `dhport_lib.jl` Float64 `M,C_fd,G_fd,tau`/solve, while preserving `M_BD*a_D` and the force scale `q5/100, q4/200`? If not, return the fail-closed obstruction and the still-required primitive lemmas.

## Inspected commit / paths

- Commit: `6bc95ebd56577c2a1317db2c58ee6d79ed195d01`.
- `agent_review_inbox/task_queue.md` — `T-P4-029` still `status: open`. The card names `P5_COMPACT_DH_FOURIER_SOURCE_SEMANTICS_AUDIT.md`, `P5_COMPACT_EXACT_REAL_MODEL_BOUNDARY.md`, and local receipt `SOURCE_FORMULA_PRESENT_CONTROLLER_MISMATCH_AND_FLOAT64_ENCLOSURE_OPEN`.
- Those two named audit files are not in this tree (`docs/` and `artifacts/` were listed). Their absence is recorded; it is not treated as a disproof of the formula.
- In-repo boundary used instead:
  - `docs/routeb-dh-source-coefficient-binding-next.md` (blob `963ab5fdccc55f8852afd18fdb7625c97d55693d`), admission `P3_REAL_DH_COEFFICIENT_BINDING = PENDING`, `float64_bridge: open`, `finite_difference_bridge: open`, `solve_bridge: out_of_scope`.
  - `docs/routeb-p4-o2-minimal-proof-chain.md` (blob `aef9eeba421a5a3ed836b2cc9ec596ad4885e1e9`). Source anchor hash recorded there is `AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936` for frozen `dhport_lib.jl`; operation-schedule hash `58209B231ED2BD1662B74B95CBBE5EE206AB1911BFDF03C8AED99C1BFF80C7C1`. The same doc says those hashes identify statements, not a numerical enclosure.
- Inbox tree at the same commit: no prior `claim-T-P4-029-*` or `review-T-P4-029-*`.
- No Lean compile, checker, or Julia run was executed. Exit code: not applicable.

## Provenance receipt (what is actually in-repo)

The coefficient-binding note records a read-only inspection of external `dhport_lib.jl` and gives SHA-256 `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`, matching the O2 chain anchor. It also records:

- default regularizer `1/1000000` on the diagonal, outside the 610 Fourier CSV rows;
- central difference `C/G` at `h=1e-5` in `dhport_lib.jl:73-99`;
- solve `Mq \ (tau-Cdq-Gq)` at `dhport_lib.jl:102-109`;
- `Matrix{Float64}` / `sin` / `cos` at the DH step, with no per-operation IEEE semantics.

The task-queue harvest already separates the static force-scale identity `diag(1/5,1/10)*(q5/20,q4/20)=(q5/100,q4/200)` from deployed `tau` equality. This review does not re-prove that identity and does not treat it as a Float64 enclosure.

The external `dhport_lib.jl` itself is not in this repository, so line-level formula equality was not re-read from source bytes in this pass.

## Typed adapter target (not admitted)

Smallest Lean/source interface still required, with premises external:

```text
structure PortMapTrace where
  mu : ℚ
  qBox : Fin 6 → RatInterval
  Mbd Mdd Mdb M0db : RatIntervalMatrix
  rB aB aD : RatIntervalVec
  sourceKey runtimeKey : String

theorem port_adapter_conditional
    (tr : PortMapTrace)
    (hmu : tr.mu = 1/1000000)
    (hsrc : tr.sourceKey = canonicalDhportKey)
    (henc : float64BlocksContained tr)
    (hinv : ddInverseSound tr)
    (hform : rB_eq_Rport_aB tr) :
    contains rB (R_port * a_B) ∧ contains (M_BD * a_D) (explicitDistalTerm tr)
```

`R_gain = -R_port` may appear only inside a norm-square bound. The adapter must not also assert `M_DD*v + DeltaM_DB*a_B = 0` and `r_B = R_gain*a_B` as the same residual equation. No such theorem is compiled here.

## Primitive lemmas still missing

1. Exact-real DH / Fourier mass map equal to the frozen 610-row payload (still pending in the coefficient note).
2. Regularizer bridge `M = M_hat + (1/1000000) I` under the same unregularized base, including the `D=(1,2,3,6)` principal block.
3. Certified-box invertibility of `M_DD(mu,q)` and an outward enclosure of the inverse or solve residual, not a solver-status flag.
4. Identity of `M0_DB` with the same `(mu,q)` convention as `M_DB`; missing nominal base is an open witness, not zero by default.
5. Float64/libm `sin`/`cos`, rounded add/mul, and source-order matrix accumulation enclosures (O2 `.1`–`.4`).
6. Central-difference remainder for `C_fd`/`G_fd` at `h=1e-5`, separate from the exact Coriolis/gravity map.
7. Force-scale and `tau` composition enclosure; the rational scale identity does not enclose deployed `tau`.
8. Explicit retention of `M_BD*a_D` in the residual consumer, distinct from the Schur port action `R_port*a_B`.
9. Per-certified-box coverage. One cell, a source hash, or a BigFloat sample does not discharge the box partition.

## Explicit non-admissions

- Not proved: source-text agreement of the recorded `R_port` formula with deployed `dhport_lib.jl`.
- Not proved: per-box Float64 enclosure of `M`, `C_fd`, `G_fd`, `tau`, or the linear solve.
- Not proved: exact-real evaluation is authoritative for the deployed controller.
- Not proved: controller/damping semantics match the factorized source.
- Not proved: P4 parent closure, flowpipe, or registry promotion.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the in-repo record is a fail-closed obstruction. The named compact audits are absent, the coefficient note leaves `float64_bridge` open, and the O2 chain treats the `dhport_lib.jl` hash as an identifier rather than an enclosure. No kernel theorem was produced.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction on `T-P4-029`. Do not close the parent.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Next child, out of scope here: place the missing `P5_COMPACT_*` audits in-repo with hashes, then a single certified-box trace for `M_DD` invertibility and `R_port*a_B`. A green interval print remains diagnostic until the primitive lemmas above are discharged.

## Unresolved blockers

1. `P5_COMPACT_DH_FOURIER_SOURCE_SEMANTICS_AUDIT.md` and `P5_COMPACT_EXACT_REAL_MODEL_BOUNDARY.md` are not in this commit.
2. External `dhport_lib.jl` bytes were not re-hashed in this pass; only previously recorded SHA-256 values were read.
3. No pinned Lean receipt for the conditional port adapter.

## Response / handoff

流川枫 claimed open `T-P4-029` and recorded a pending fail-closed boundary: source-level formula notes and hashes do not enclose deployed Float64 `M/C_fd/G_fd/tau`/solve, and the required port adapter `R*a_B=r_B` remains an uncompiled target. No registry or formal-proof edit.
