# Anthropic FLT registry / graph adapter

Status: `pending`; advisory architecture adapter only.

## Selection and classification

The selected candidate is the upstream docs-site pipeline:

```text
extract.py -> graphdata.py -> render.py -> selfcheck.py
```

The FLT infra audit classifies this as reusable graph/registry structure rather
than theorem content. The local classification is `light_adaptation`: the
separation of extraction, graph computation, rendering, and output selfcheck is
portable, but the local manifest, DAG, frontier, comparator, and registry
schemas are different and must be bound explicitly.

The related challenge/solution/FinalCheck pattern is retained only as an
admission seam: statement identity, permitted axioms, final check, and
comparator evidence are separate fields. It is not treated as a verified FLT
proof.

## Provenance

Source provenance is pinned to
`upstream/anthropics-fermats-last-theorem` commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`, with the audited paths recorded in
the manifest. The audit reports Apache-2.0 attribution, Lean 4.33.1, and
Mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d`.

## Typed boundary

`GraphManifest` retains provenance, stage/landmark nodes, typed edge kinds,
source/graph/selfcheck hashes, and the three registry states. `edgeRefsValid`
and `graphMetadataComplete` are structural predicates only. The interface
requires explicit `PromotionEvidence` before a verified/formal-allowed state
can be stated; metadata completeness or rendered reachability cannot satisfy
that evidence by themselves.

No upstream theorem body was copied, no local registry/state/frontier was
mutated, and no FLT arithmetic or PDE claim is made. This sidecar remains
pending and uncompiled; no broad regression was run.
