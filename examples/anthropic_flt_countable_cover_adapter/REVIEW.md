# Anthropic FLT countable-cover topology adapter

Status: `pending`; direct-reuse non-number-theoretic API candidate.

## Exact provenance and declaration

The selected upstream declaration is
`TopologicalSpace.secondCountableTopology_of_countable_cover'` in
`Definitions/Def_Mathlib_Topology_Bases.lean`, pinned at commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef` and source blob
`0a0f162c947cce45653a7762a500392803c0bb36`. The audited source imports
`Mathlib`; repository attribution is Apache-2.0.

## Applicability

The exact contract requires a topological target `α`, a countable index sort
`ι`, a topological family `U i` with `SecondCountableTopology (U i)`, maps
`f i : U i → α` that are `Topology.IsOpenEmbedding`, and a hit witness
`∀ a, ∃ i u, f i u = a`. The conclusion is only
`SecondCountableTopology α`.

The sidecar is classified `direct_reuse` because the theorem is already a
standard generic topological API. Its possible use in local region/chart
bookkeeping is an adaptation, not a quantitative interval, box, or flowpipe
result.

## Boundary

`sampled_patch_missing_target_point` shows that one sampled patch can omit a
target point, so sample membership cannot replace the hit witness. Open
embedding and second-countability also do not provide numerical enclosure,
coverage of a physical state domain, or theorem admission. The sidecar is
pending/open, uncompiled, and not entered into the verified registry.

No upstream arithmetic content or local registry/state was modified; no wide
regression was run.
