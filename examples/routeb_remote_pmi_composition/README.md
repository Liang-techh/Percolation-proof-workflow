# Route-B remote budget to PMI composition

`RemotePMIComposition.lean` is a source-independent Lean seam for the P4
repair.  It proves two exact-real steps:

1. a remote-action bound `residual² <= kappa² * mass` plus a scale bridge
   `mass <= beta² * y²` yields `residual² <= (kappa*beta)²*y²`;
2. that composed envelope and the scalar Schur budget imply nonnegativity of
   the P4 quadratic.

The intended first specialization is the conditional remote-acceleration
budget coefficient `90`, followed by a separately proved operator/source bound
for `M_BD`.  No deployed DH binding, domain coverage, or registry admission is
present here.  Compilation and `#print axioms` are delegated to the pinned
GitHub Lean worker; no local Lean/Lake claim is made.
