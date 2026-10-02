---
kind: review_result
review_id: review-T-P4-008-liuchuanafeng-20261002T1712Z
source_agent: 流川枫
created_at: 2026-10-02T17:12:00Z
inspected_commit: f7aa3e3e86c793230a85cd3ccf0ffa0235797490
claim_commit: 4398b3bda15c4d6bb98cc39ac667ab2aea081340
inspected_paths:
  - agent_review_inbox/task_queue.md
  - docs/routeb-c2-d-normalization-audit.md
  - docs/routeb-source-fork-canonical-audit.md
  - docs/routeb-p4-kc-force-contract.md
  - docs/routeb-p4-mbd-projection-obstruction.md
task_id: T-P4-008
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P4-008 obstruction audit: `kc` residual and remote `M_BD a_D` are not supplied by the current block projection

## Question

At commit `f7aa3e3e86c793230a85cd3ccf0ffa0235797490`, does the documented deployed block identity already contain `M_BD(q) a_D` and an explicit `kc` residual, while the current PMI projection and acceleration-side D-row do not bind those terms? Can that fact close P4/M4?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The queue contract is restated as a typed obstruction, not as a compiled certificate and not as physical closure.

This is not `rejected` as a claim that the remote term is identically zero. It is not `compiled_candidate`: no Lean command was run. It is not `verified`. It is not `architecture_only`: the missing bindings are pinned to existing source-audit identities and the force-scale `rho_kc` sign/index statement.

## Evidence inspected (read-only)

1. **Queue contract is still open and negative.**
   `task_queue.md` lists `T-P4-008` as `open`, owner `柳冠一`. Required object: a typed obstruction/countermodel for the missing bounded full-state or source-model contract, with force and acceleration units kept distinct, and an exact sign/index statement for `rho_kc`. Forbidden: treating the old comment `(M-M0)_BD a_D` as the current identity, treating a numerical Gram residual as physical error, or closing P4/M4.

2. **Current identity uses `M_BD a_D`, not the old comment.**
   `docs/routeb-c2-d-normalization-audit.md` blob `8d16673467c8612764a6afef7a85a1b9b2ede781` records the written block identity

```text
l_F = (M_BB(q)-M0_BB) a_B + M_BD(q) a_D
      + C_B(q,dq)dq + (G_B(q)-G_B(0))
      - mgl_B q_B + kc_B(q_B).
```

   The same audit says the older comment `(M-M0)_{B,D} a_D` is not the current independent identity. `l_F = I_B f_B - M0_BB a_B` is a force residual. It is not an acceleration residual and is not the M4 object `D(e)=integral ||e||^2`.

3. **Exact `kc` sign and index, two scales.**
   `docs/routeb-p4-kc-force-contract.md` blob `bd673285371bbb7d0e55bd7ff86626a72b7c80a3` fixes the canonical PMI cross term at `kc = 0.05 = 1/20`:

```text
rho_kc^f(q_B) = (q5/20, q4/20)
rho_kc^F(q_B) = diag(1/5, 1/10) rho_kc^f(q_B) = (q5/100, q4/200)
```

   Index order is block `B=(4,5)`: first component couples `q5` into channel 4, second couples `q4` into channel 5. Both signs are positive in the stated nominal expression. Deployed `tau = -Kp*q - (Kd+b_fr)*dq + G0v + (gw_coef .* I_val)*w` has no `kc` torque, so the PMI `kc` term must be charged as an additive force residual. It cannot be deleted.

4. **Fork audit does not remove the discrepancy.**
   `docs/routeb-source-fork-canonical-audit.md` blob `fde103ddbd337e44d0c295e47d8eb02ffd884e62` records that both forks share `dhport_lib.jl`, while PMI `f1/f2` still contain `kc*q5` / `kc*q4` and deployed `tau` does not. Metadata in `robot_final` is not a dynamics-equivalence proof. P4 stays conditional/open.

5. **Block projection does not bound `M_BD a_D`.**
   `docs/routeb-p4-mbd-projection-obstruction.md` blob `7ceed94da30a62ed2742bc7041cccbcef3731123` gives the rational Fourier snapshot at `q=0`:

```text
M_BD(0) e1 = (7/60, -21/80000)
||M_BD(0) e1||^2 = 784003969/57600000000 > 0
rho_remote(lambda) = lambda * (7/60, -21/80000)
```

   Fixing the currently projected block variables at zero and taking `a_D = lambda * e1` leaves the block projection unchanged while the remote force grows with `lambda^2`. That is a projection countermodel, not a claim that arbitrary `lambda` occurs on a physical trajectory. The acceleration-side D-row still lacks the inverse-mass bridge recorded in the C2 audit.

No checker was run in this pass. No exit code is claimed. The local checker named in the projection note, `scripts/check_routeb_p4_mbd_obstruction.py`, was not executed.

## Typed obstruction

```text
identity_used: l_F = (M_BB-M0_BB) a_B + M_BD a_D + r_B + kc_B
identity_rejected: (M-M0)_BD a_D as the current formula
rho_kc^f: (q5/20, q4/20)          units: normalized f
rho_kc^F: (q5/100, q4/200)        units: generalized force
I_B: diag(1/5, 1/10)
remote_witness: a_D = lambda e1, block projection fixed, ||M_BD(0) e1||^2 > 0
missing_contract: bounded full-state a_D, or Schur elimination of M_BD/M_DD,
                  or a typed remote residual enclosure on the same domain
units: l_F and rho_kc^F are force; a_D is acceleration; no conversion claimed
source_binding: not proven; Gram residual is not physical error
```

## Assumptions still required

- a source-hash binding of deployed `tau`, PMI `kc`, and the block identity to the same fork;
- a covered-domain bound on `a_D`, or an exact Schur elimination with `M_DD`;
- a separate force-to-acceleration bridge if terminal `D` stays acceleration-side;
- coverage, comparator, and a Lean receipt before any parent gate.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-008` open.
- Requested action: do not promote this restatement into a P4 or M4 node. Next owner should either pin the `q=0` remote witness and the two-scale `rho_kc` statement as a source-independent obstruction lemma, or supply one of the three repair seams in `routeb-p4-mbd-projection-obstruction.md` with a real source hash. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not use `(M-M0)_BD a_D` as the current identity.
- Did not treat a numerical Gram residual as physical error.
- Did not close P4 or M4.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no exit code is claimed.
