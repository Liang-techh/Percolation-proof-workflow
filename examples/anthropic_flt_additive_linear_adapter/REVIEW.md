# Anthropic FLT additive-to-integer-continuous-linear adapter

Status: `pending`; generic infrastructure candidate, not an FLT theorem.

## Selection and exact provenance

The selected declaration is `ContinuousAddEquiv.toIntContinuousLinearEquiv`
from `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean` at
fixed commit `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`, source blob
`7829c8e30b406c8bb1dcbddf8e8d49745ec5c8ea`.  The audited source imports
`Mathlib` and the quotient module-transport definitions.  Attribution is
Apache-2.0.

The construction was selected because it is smaller than the surrounding
quotient transport API and has no FLT-specific arithmetic content.  The
quotient candidate is intentionally not duplicated: it is already covered by
the existing quotient transport sidecar.

## Exact contract

Given additive commutative groups `M` and `M₂`, topological spaces on both,
and an additive homeomorphism `e : M ≃ₜ+ M₂`, the declaration constructs

`M ≃L[ℤ] M₂`.

The underlying function and inverse are those of `e`; the only added
structure is continuity plus the canonical integer-linear structure of an
additive equivalence.

## Applicability and counterexample boundary

This API is reusable when the target proof genuinely needs a continuous
`ℤ`-linear equivalence between topological additive groups.  It is not a
polymorphic `R`-linear transport theorem.  For example, an additive
homeomorphism between topological additive groups with no `R`-module
instances (take the identity on the discrete additive group `ℤ`) still fits
the contract and yields only `ℤ`-linear transport.  Therefore the existence
of an additive homeomorphism alone cannot be used as a witness of a real- or
complex-linear PDE coordinate change; the required scalar compatibility and
regularity must be supplied separately.

This is why the manifest is classified `light_adaptation`, even though the
sidecar mirrors the upstream definition exactly: a downstream scalar-field
use needs an explicit target-scalar obligation, and the present API does not
discharge it.

## Admission boundary

The sidecar is pending/open and uncompiled in this workspace.  It does not
prove differentiability, Sobolev regularity, boundary-condition transport,
quantitative enclosure, flowpipe validity, FLT arithmetic, or any verified
registry entry.  No registry/shared state was modified, and no wide regression
was run.
