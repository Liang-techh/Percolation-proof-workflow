---
kind: review_result
review_id: review-T-P4-032-exact-cell-lambda-codex-20260907T232742
task_id: T-P4-032
agent: Codex-P4-math-lane
source_agent: Codex-P4-math-lane
created_at: 2026-09-07T23:27:42-06:00
inspected_commit: be2fe41ccfd46f6361dd2f58adaa367ea9351029
inspected_paths:
  - agent_review_inbox/README.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ExactCellLambdaConsumer.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ExactCellLambdaConsumer.review.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SameSourceConsumerPacket.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHProducerBaseBridge.lean
  - examples/routeb_p4_rational_lambda_guard_lean/P4RationalLambdaGuard.lean
related_tasks:
  - T-P4-038
  - T-P4-039
  - T-P4-040
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.same_source_exact_cell_lambda_consumer
requested_action: review the same-source envelope and common-rational-lambda interface as pending mathematical evidence; require independent elaboration and real source inequalities before any stronger claim; do not promote registry status
---

# Same-source rational charges to one scalar target

Question: how can the line-9 source lane consume the rational common-lambda guard without replacing missing DH source inequalities by coefficient slack or sampled values?

This result adds a typed interface and proof attempt. It does not instantiate a concrete DH envelope family, run Lean/Lake, evaluate a solver, or change workflow/registry state. The inspected commit identifies the surrounding checkout; the new artifact hashes below identify the actual workspace files, regardless of whether the coordinator has committed them yet.

## Source-bound envelope contract

For one source key/domain, fixed force coordinates and common rational target t>0, `SameSourceCharges` requires a proved cell cover and, on every cell i:

`||l_base(x)||²≤A_i`, `||port(x)||²≤P_i`, `t+D_i≤b_base(x)`.

The rational A_i and P_i are squared-force upper charges. A_i is NOT the producer acceleration metric A_up. P_i is the uninflated port charge. D_i is the base budget AFTER reserving t.

`chargesFromProducer` constructs the P_i bound from the existing same-source `RowSourceEvidence` and `rhoSq*A_up(x)≤P_i`. `DHProducerBaseBridge.rowEvidenceFromProducer` can supply that evidence only under its explicit matrix, descriptor, operator-bound and domain premises. The source identities and A_i/D_i inequalities remain open.

## Scaled Young and rational guard

For s=lambda−1>0, the exact identity behind `scaled_young` is

`(s+1)||u||²+s(s+1)||v||²-s||u+v||²=||u-sv||²≥0`.

For G_i=D_i−A_i−P_i,

`q_i(s)=P_i*s²-G_i*s+A_i=(s+1)A_i+s(s+1)P_i-sD_i`.

`RationalGuard` stores rational 0<a≤b and exact rational endpoint checks q_i(a)≤0, q_i(b)≤0 for all rows. The code invokes the existing `RouteBP4RationalLambdaGuard.common_lambda_interval`, using P_i≥0 for convexity. One rational s in the common interval then yields, via the proved cell cover,

`0<t≤b_base(x)-||l_base(x)+port(x)||²` throughout the source domain.

The kernel argument needs no finiteness assumption; a finite checker may use Fin n. It never replaces a cover by a sample set or a common s by unrelated rowwise witnesses. At s=1 it recovers 2A_i+2P_i≤D_i. General-s feasibility does not imply the older fixed-theta=1 Allocation record.

`source_floor_to_P4` instead consumes the source floor directly with the existing `P4Binding`: q equals the total squared force residual, nominal=nu*b_base, gain*beta=nu>0, and the correctly directed P4 lower comparison. The P4 target is nu*t, not automatically t. Optional front decomposition and richer SourceView bindings remain separate.

## Exact target-reservation counterexample

Let u=v=(1,0), b_base=4 and t=1. Then A=P=1 and the actual residual square is 4, leaving margin 0. Incorrectly setting D=4 gives q(1)=0; the correct D=3 gives q(1)=1>0. `forgetting_target_counterexample` encodes both exact evaluations and failure of target=1. This is an algebraic interface counterexample, not a demonstrated physical trajectory state.

## Remaining real-DH boundary

One must still identify the actual force decomposition and storage normalization, include any nonzero distal/local/FD defects, establish same-cell A_i/P_i/D_i inequalities, and prove the intended source/trajectory domain is covered. In particular, the producer's four-angle domain is not automatically the block-p domain. A branch name, hash string, positive external coefficient slack or guarded lambda supplies none of these facts.

## Evidence and checks

- Read-only source/signature inspection and manual algebra review were performed. Public interfaces include `SameSourceCharges`, `chargesFromProducer`, `scaled_young`, `guard_allocation_identity`, `guard_at_rational`, `same_source_scalar_floor`, `rational_common_source_target`, `source_floor_to_P4`, `shift_one_identity` and `forgetting_target_counterexample`.
- PowerShell text scan of the new Lean file: 0 proof-placeholder declarations/tokens and 0 trailing-whitespace lines; command exit code 0.
- `git diff --check -- <new Lean> <paired review>`: exit code 0. At the initial check both were untracked, so the separate text scan was the meaningful whitespace check.
- `Get-FileHash -Algorithm SHA256` for the five files below: exit code 0.
- No Lean/Lake, verifier, GitHub CI query, solver or regression was run. Imports/elaboration/axioms for this module are unverified. No compiled or source-verified claim is made.

| Artifact | SHA-256 |
|---|---|
| `NEW_P4_032_ExactCellLambdaConsumer.lean` | `b4f99ab8b9ced4dfb09fdc5ab1344ac8b7271363ed3af7e06bf2f696da5b8122` |
| paired `.review.md` | `d9c4152262c7002bc70318609ca63131c70abdf93cfdb745432da06ee1345f1e` |
| `NEW_P4_032_SameSourceConsumerPacket.lean` | `8c49603aa1c2193a5440026474d8ddc4b90e3a308c7c32ac862ace7b8c1a160e` |
| `NEW_P4_032_DHProducerBaseBridge.lean` | `94cc1f34d87d376309b750e95811fe0d13a4386fea872dba9b967b0421f73e94` |
| `P4RationalLambdaGuard.lean` | `6a79d222697632e2a54ff7fc6954bfc63eb39bfc92187649514ef88123673636` |

Disposition: retain as **pending / OPEN_UNCOMPILED** mathematical interface evidence. No registry promotion or concrete P4/physical-DH closure.
