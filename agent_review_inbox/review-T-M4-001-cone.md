---
kind: review_result
task_id: T-M4-001
source_agent: Codex
created_at: 2026-09-06T21:00:00-06:00
integration_status: pending
---

# M4 prerequisite-cone closure audit

## Scope and method

Read-only inspection of `artifacts/routeb_6dof/state.json`. The target was
the node whose `name` is `M4.block45_full_certificate`. Node IDs were resolved
from the state file, and the prerequisite cone was computed by deterministic
backward traversal over each node's explicit `dependencies` array. Levels were
then assigned bottom-up: a node with no prerequisite in the cone is level 0;
otherwise its level is one plus the maximum level of its cone prerequisites.
No status, queue, registry, or external source was changed.

Evidence checkpoint:

- state path: `artifacts/routeb_6dof/state.json`
- revision: `331`
- root_id: `b85f1ee1ef03426eaa1197ff39c6c026`
- state SHA-256: `66776aa201e93d38bc97d4ea8080f3a32e2082ab59a2c006826417460cbef16`
- target node ID: `6f06c8545bc24dc590b6e5ade85b684d`
- cone size: `9`
- maximum level: `8`

The hash was recorded from `Get-FileHash -Algorithm SHA256`.

## Complete prerequisite cone

The deterministic levels and node IDs are:

| level | node ID | name | state | direct prerequisite IDs |
|---:|---|---|---|---|
| 0 | `527611b83f6a49dda06a0d4eb711f129` | `P0.reproducibility_baseline` | open | none |
| 1 | `e25b7ff724354df58185f71eb10376e3` | `P1.bracket_decision` | open | `527611b83f6a49dda06a0d4eb711f129` |
| 2 | `94d269520f0c48c19186ee1b312ba3a3` | `P2.spectral_partition` | open | `e25b7ff724354df58185f71eb10376e3` |
| 3 | `8f7df5df39a041d7a972078830dbcee7` | `P3.strict_true_dh_bounds` | open | `94d269520f0c48c19186ee1b312ba3a3` |
| 4 | `1e7b1df1835f4deba06b11a8182f6719` | `P4.residual_schur_pmi` | open | `8f7df5df39a041d7a972078830dbcee7` |
| 5 | `9a3a7eef35b34880b85423aac67ea015` | `P5.sparse_disjunctive_sos` | open | `1e7b1df1835f4deba06b11a8182f6719` |
| 6 | `4236b22d4cd54fa4bd7cb66f458e8768` | `P6.exact_gram_interval_check` | open | `9a3a7eef35b34880b85423aac67ea015` |
| 7 | `edd8407c33f54c41867f03b46ec1e313` | `P8.independent_reachability` | open | `4236b22d4cd54fa4bd7cb66f458e8768` |
| 8 | `6f06c8545bc24dc590b6e5ade85b684d` | `M4.block45_full_certificate` | open | `9a3a7eef35b34880b85423aac67ea015`, `4236b22d4cd54fa4bd7cb66f458e8768`, `edd8407c33f54c41867f03b46ec1e313` |

## Parallel open leaves and next frontier

The complete cone has exactly one leaf under the explicit state graph:

- `527611b83f6a49dda06a0d4eb711f129` — `P0.reproducibility_baseline`

It is open. Consequently, the set of independently executable open leaves is
`{P0.reproducibility_baseline}`; there are no two or more parallel leaves in
this checkpoint. The next frontier under the strict rule “all direct cone
prerequisites are terminal (`verified`, `completed`, `closed`, or `done`)” is
the same singleton P0 node. Since P0 is not terminal, no higher node is
frontier-eligible.

This is a graph-theoretic result only. It does not say that the mathematical
work must be performed serially: the state graph currently encodes P3/P4/P8
as a single prerequisite chain, so independent mathematical work can only be
parallelized after the DAG is refined with explicit child nodes and accurate
cross-dependencies. Such refinement is outside this read-only task.

## Admission boundary

All nine nodes are `open`; no node is verified or registry-eligible. This audit
does not promote any node, alter `formal_certificate_allowed`, or close M4.
The existing true-DH binding, global coverage, residual absorption, flowpipe,
and terminal-transfer obligations therefore remain unresolved.
