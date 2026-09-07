# Anthropic FLT dependent-product subtype transport adapter

Status: `pending`; architecture-only generic infrastructure candidate.

## Selection and exact provenance

The selected declaration is the additive form
`ContinuousAddEquiv.piEquivPiSubtypeProd`, generated from
`ContinuousMulEquiv.piEquivPiSubtypeProd` in
`Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean` at fixed
commit `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`, source blob
`7829c8e30b406c8bb1dcbddf8e8d49745ec5c8ea`.  The audited source imports
`Mathlib` and the quotient module-transport definitions.  Attribution is
Apache-2.0.

The candidate is not a duplicate of the existing quotient transport sidecar:
it does not form a quotient or invoke a quotient universal property.  It is a
smaller product-reindexing leaf suitable for a typed theorem-DAG interface.
The already completed `toIntContinuousLinearEquiv` adapter is also not
duplicated.

## Exact contract

For `p : ι → Prop`, a dependent family `Y : ι → Type*` whose fibers have
topological and additive structure, and `[DecidablePred p]`, the API constructs

`((i : ι) → Y i) ≃ₜ+ ((i : {x : ι // p x}) → Y i) × ((i : {x : ι // ¬p x}) → Y i)`.

The map is the canonical restriction to the two complementary subtypes; the
inverse merges the two subtype-indexed functions.  The sidecar preserves the
upstream typed shape exactly.

## Architecture-only applicability and counterexample boundary

This leaf is useful when a theorem DAG needs to split a product-valued object
into two predicate-indexed blocks while retaining a continuous additive
equivalence.  It can organize coordinates or hypotheses, but it does not
prove that either block is nonempty, covers a physical domain, or carries a
norm/measure/Sobolev structure.

The exact counterexample boundary is the predicate `p := fun _ => False`:
the positive subtype factor is empty, while the equivalence remains valid.
Thus the existence of this transport cannot be read as a nontrivial block,
coverage, or analytic decomposition.  Any scalar-field linearity,
differentiability, boundary-condition transport, or PDE regularity must be
introduced by separate obligations.

Because this is only a typed structural leaf and offers no stronger admission
than the current candidates, it remains `architecture_only` and is not
registered as a verified theorem.

## Validation boundary

The sidecar is pending/open and uncompiled in this workspace.  No upstream
arithmetic content or local registry/shared state was modified, and no wide
regression was run.
