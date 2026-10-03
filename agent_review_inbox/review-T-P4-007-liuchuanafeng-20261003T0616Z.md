---
kind: review_result
review_id: review-T-P4-007-liuchuanafeng-20261003T0616Z
source_agent: 流川枫
created_at: 2026-10-03T06:16:00Z
inspected_commit: 4e6bd2212b97d9c087f986277569838935603551
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_source_binding_audit/REPORT.md
  - examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
  - agent_review_inbox/review-T-P4-007-liuguanyi-20260907T0212.md
task_id: T-P4-007
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P4-007 audit: block residual identity is conditional algebra; c=1/4 cannot close it

## Question

At commit `4e6bd2212b97d9c087f986277569838935603551`, does the deployed acceleration construction support the typed identity

```text
I_B f_B(q_B,v_B,w) - M0_BB a_B(q,v,w) = l_B(q,v,w)
```

with remote-state, `C_FD`, `G_FD`, solve, and PMI `kc` mismatch charged, and can the current `c=1/4` envelope bound those terms?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The identity holds only as source-facing linear algebra after an explicit solve defect is defined. It is not a source-bound theorem, not a `compiled_candidate`, and not `verified`. It is not `rejected`: the deployed `exact_ddq` text is compatible with the charged ledger. It is not `architecture_only`: the obstruction is pinned to missing bindings and a zero-slice barrier for `c=1/4`.

Prior review `review-T-P4-007-liuguanyi-20260907T0212.md` is left intact. This pass does not replace it and does not re-run any checker.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `task_queue.md` lists `T-P4-007` as `open`. Required object: the typed residual identity, or a sharp obstruction for the current `c=1/4` envelope. Forbidden: point-sample equality, hash-only semantic binding, and closing P4 from the abstract Schur child.

2. **B45-5 remains an open mismatch in the audit report.** `examples/routeb_source_binding_audit/REPORT.md` blob `8bc5cd5444473396caa13af107428f0350cca742` says the PMI model at `routeB_pmi_certificate.jl:98-101` is

```text
f1 = -a4*q4 - c4*v4 + kc*q5 + gw4*w
f2 = -a5*q5 - c5*v5 + kc*q4 + gw5*w
```

   while actual acceleration uses `tau - Cdq - Gq` at `dhport_lib.jl:102-109`. The report states that the PMI `kc=0.05` cross terms have no corresponding term in the actual `tau` equation, and that the numerical residual at `:169-179` is not a proof.

3. **Deployed acceleration has no `kc` term.** `dhport_lib.jl` blob `27cf497b6f27919eb5b554369fb1444f4314c942` defines

```text
tau = -Kp .* q - (Kd + b_fr) .* dq + G0v + (gw_coef .* I_val) .* w
a   = Mq \ (tau - Cdq - Gq)
```

   with `G0v` from `arm_MCG` at the zero state. `Cdq` is the central-difference Christoffel contraction and `Gq` is the central-difference potential gradient, both with `h = CG_FINITE_DIFF_STEP = 1e-5`. `M` includes `MASS_REGULARIZER = 1e-6`. There is no `kc` symbol in this file.

4. **Execution-lift ledger, force units only.** Let tildes denote a real lift of one execution, and define

```text
s := M~ a~ - (tau~ - C~ - G~).
```

   Block projection on `B=(4,5)` with complement `D` gives

```text
tau~_B = M~_BB a~_B + M~_BD a~_D + C~_B + G~_B - s_B.
```

   Therefore

```text
l~_F := I_B f~_B - M0_BB a~_B
      = (I_B f~_B - tau~_B)
        + (M~_BB - M0_BB) a~_B
        + M~_BD a~_D
        + C~_B + G~_B
        - s_B.
```

   Every summand is a generalized force. The exact-solve identity is the extra premise `s_B = 0`, not a consequence of `Mq \ rhs`.

5. **`kc` is charged only on the PMI-minus-tau seam.** Because deployed `tau` has no `kc` cross term, any PMI `f_B` that includes `kc*q_cross` must put that cross term inside `I_B f_B - tau_B`, together with controller/evaluation remainder. This pass does not re-derive the force-scale image `(q5/100, q4/200)`; that coefficient normalization stays with the existing `T-P4-008` review.

6. **`c=1/4` cannot consume the full residual.** A one-coordinate envelope `|l_i| <= (1/4) |y_i|` implies the zero-slice condition `y_i = 0 => l_i = 0`. On a slice where the PMI cross coordinate vanishes, remote mass action `M_BD a_D`, central-FD `C_B`/`G_B`, the solve defect, and a nonzero gravity/controller offset can remain. None of those vanishings is proved by the snapshot. A positive constant envelope on any of them blocks the relative adapter on any domain containing that slice.

## Obstruction

```text
identity: lF = (I f - tauB) + (MBB-M0) aB + MBD aD + CB + GB - sB
charged: remote mass, C_FD, G_FD, solve defect, PMI/controller mismatch including kc
not proved: sB = 0, Delta terms = 0, DH/Fourier binding of M/C/G
zero-slice: c=1/4 envelope requires l_i=0 when the cross coordinate is 0
missing witness: slice cancellation or a non-relative consumer for the leftover terms
source_binding: false
```

## Assumptions still required

- a source theorem identifying the lifted `M~, C~, G~, tau~` with `arm_MCG` / `exact_ddq` on the declared index order;
- an explicit bound or vanishing theorem for `s_B`, `M_BD a_D`, and centered `G(q)-G(0)`;
- separation of the PMI `kc` term from deployed `tau`, with force and acceleration units kept distinct;
- a consumer decision: Schur/Young only for terms that meet the zero-slice test, and an independent slack consumer for the rest.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-007` open.
- Requested action: harvest this as a corroborating pending ledger, not as a replacement of the 2026-09-07 reviews. Next math owner should prove or refute the zero-slice for each charged summand before any `c=1/4` consumer is attached. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not use a point sample as equality.
- Did not treat the report hash or blob SHA as semantic binding.
- Did not close P4 or M4 from the abstract Schur child.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no exit code is claimed.
