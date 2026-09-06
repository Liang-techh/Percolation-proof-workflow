# B45-5 descriptor-terms adapter boundary

This sidecar packages the already compiled six-term residual decomposition and
exposes the smallest source-comparator seam needed to instantiate it.

## Definitional facts in Lean

- `q : Vec2` is ordered as `(q4,q5)`.
- `rhoKc q = (q5/100,q4/200)`.
- `rhoMgl`, `rhoMass`, `rhoRemote`, `sourceDescriptorRhs`, and the six-term
  `descriptorResidualTotal` are exact-real definitions.
- Once one exact descriptor equality is available, the residual decomposition
  is a theorem inherited from `ResidualDecomposition.lean`.

## Premises required from a source comparator

For one concrete source state, the comparator must prove both equalities about
the same `sourceBlockForce`:

1. `sourceBlockForce = expectedSourceForce q v w t`, binding block indices,
   controller constants, C/FD, G/FD, and `G0` to the exact-real force formula.
2. `sourceBlockForce = sourceDescriptorRhs t`, binding the regularized DH mass
   block split `M_BB a_B + M_BD a_D` and the returned acceleration.

The comparator must also ensure that the fields of `DescriptorResidualTerms`
are instantiated by those same source objects.  The adapter deliberately does
not accept a comparator premise for `rhoKc`: it is fixed by the nominal PMI
definition and therefore remains an explicit residual rather than a source-DH
term.

## Claims deliberately absent

There is no residual norm/domain bound, no Float64-to-real theorem, no claim
that the linear solve satisfies the exact descriptor equation, and no
reachability, PMI, or global certificate conclusion.
