---
kind: review_result
review_id: review-T-P4-002-liuchuanafeng-20261003T0312Z
source_agent: 流川枫
created_at: 2026-10-03T03:12:00Z
inspected_commit: 4405a23ed0eed8657d139fcbc0935d1dbe01857e
claim_commit: 2a11d5360dc8567b685c5371bbabb4bc334f5af9
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P4-002-liuchuanafeng-20261003T0310Z.md
  - agent_review_inbox/review-T-P4-002-one-channel.md
  - examples/routeb_p4_next_child/P4RationalSchurAbsorption.lean
  - examples/routeb_p4_next_child/REPORT.md
  - docs/routeb-c2-d-normalization-audit.md
task_id: T-P4-002
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
---

# T-P4-002 audit: channel-4 Schur consumer is not a true-DH residual envelope

## Question

At content commit `4405a23ed0eed8657d139fcbc0935d1dbe01857e`, does the exact Schur leaf identify a smallest executable source-binding witness for `d`, `p`, and the actual channel-4 residual, or does the decimal audit still stop short of DH equality?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The queue still marks `T-P4-002` open. The Lean leaf is an exact-real algebraic consumer of an abstract residual premise. The rational `d` is a spelling of the exported decimal `0.116667666666667`. Neither object is a true-DH residual envelope, and neither is overwritten here.

This is not `rejected`: the algebraic margin is positive and the prior focused report records a kernel pass. It is not `compiled_candidate`: this pass did not compile. It is not `verified`. It is not `architecture_only`: the missing object is an executable source receipt for the residual premise, not only a missing wrapper.

## Evidence inspected (read-only)

1. **Queue contract is still open.** Scope is one Schur channel and the smallest executable witness for `d`, `p`, and the actual residual. Deliverable is a checker/Lean boundary, a normalization map, and a receipt contract. Forbidden: using the decimal audit as DH equality, or closing P4 globally.

2. **Exact consumer, source-independent.** `examples/routeb_p4_next_child/P4RationalSchurAbsorption.lean` blob `d85c2e1c258a88355b076ac5cce322180eb827ad` defines

```text
p = 3/5
ell = 1/100
d = 116667666666667 / 10^15
quadratic(x,y) = p x^2 + 2 ell x y + d y^2
```

`exact_schur_margin` is `0 < p*d - ell^2`. The exact difference is

```text
p*d - ell^2 = 349503000000001 / 5000000000000000 > 0.
```

`residual_absorption` assumes `residual^2 <= ell^2 * y^2` and spends Young parameter `epsilon = 1/100`. The leftover diagonal budgets are `p - 1/100 = 59/100` and `d - ell^2/(1/100) = 106667666666667/10^15`. The file header says no DH, Float64, coverage, or trajectory premise is introduced.

3. **Historical compile is not reused as this pass's receipt.** `examples/routeb_p4_next_child/REPORT.md` blob `a0cc002c7bdccd97f71aa07c31093b6bef6977ac` records a 2026-09-06 focused `lake env lean` with `exit_code = 0` and axioms `[propext, Classical.choice, Quot.sound]` for `exact_schur_margin`, `exact_schur_nonnegative`, and `residual_absorption`. It also says the rational `d` is only a reification of the exported decimal, coverage remains false, and the Julia SOS coefficients are runtime-generated. This pass did not rerun that command and does not claim a new exit code.

4. **Normalization map keeps force and acceleration apart.** `docs/routeb-c2-d-normalization-audit.md` blob `8d16673467c8612764a6afef7a85a1b9b2ede781` records deployed `a = M(q) \ rhs`, `I_B = diag(1/5, 1/10)`, `M0_BB = diag(0.116667666666667, 0.05018475)`, and `l_F = I_B f_B - M0_BB a_B` as a generalized-force residual. Channel 4 is the first diagonal entry: `I4 = 1/5` and the decimal spelling of `M0[4,4]` is the same rational used as `d`. `M0_BB != I_B`, so the two scales are not interchangeable. `l4` cannot be renamed to an acceleration residual `e_A`. An acceleration-side `D` still needs a separate mass or inverse-mass bridge.

5. **Prior one-channel review is preserved, not closed.** `agent_review_inbox/review-T-P4-002-one-channel.md` blob `e2a0b3c4114f6e84712c3809574d0a05a0f3e09d` proposes a zero-state channel-4 receipt and records decimal spelling and Float64 value checks as PASS while `true_dh_mass_equality = PENDING`. That file is not a pinned Julia execution trace. A receipt copied from the CSV, or a decimal-text equality, still fails the executable-witness bar stated there.

6. **No checker execution in this pass.**

```text
command: not run
exit_code: not claimed
lean_receipt: historical REPORT only; not rerun
julia_zero_point_trace: absent
```

## Obstruction

```text
algebraic_consumer: residual^2 <= (1/100)^2 y^2 implies the channel-4 quadratic stays nonnegative
schur_margin: p*d - ell^2 = 349503000000001 / 5000000000000000
young_debit: epsilon = 1/100 from p; d debit = 1/100
d_spelling: 116667666666667/10^15 = exported decimal 0.116667666666667
missing_executable_witness:
  pinned Julia bits for M0[4,4], rhs4, a4, f4, l4 at one declared point
  source SHA-256, mass_regularizer=1e-6, fd_step=1e-5, runtime pin
  explicit identity l4 = (1/5)*f4 - M0[4,4]*a4
  a theorem that the executed residual satisfies residual^2 <= y^2/10000
    on a stated cell, not at one sample
flags: formal_certificate_allowed=false, registry_promoted=false
source_binding: not claimed
```

## Assumptions still required

- the residual in `residual_absorption` must be identified with force-side `l4`, not with `a4` or `e_A`;
- `d` may enter the consumer only as the declared rational spelling until a Float64-to-real outward theorem exists;
- `p = 3/5` remains an interface coefficient, not a deployed-source equality;
- one zero-point trace, even if later emitted, does not give a cell envelope;
- channel 5 and `M0[5,5]` stay outside this child.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-002` open.
- Requested action: keep the algebraic consumer and the decimal spelling as separate inputs. Do not harvest the 2026-09-06 decimal/Float64 spelling checks as true-DH equality. The next child is a pinned one-point receipt, then a fixed-cell force-side enclosure. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not treat the decimal audit as DH equality.
- Did not close P4 or M4.
- Did not rename `l4` to an acceleration residual.
- Did not invent an exit code, source hash, or Lean axiom list for this pass.
- Did not edit registry, state, task queue, or formal proofs.
- Did not overwrite `review-T-P4-002-one-channel.md`.
