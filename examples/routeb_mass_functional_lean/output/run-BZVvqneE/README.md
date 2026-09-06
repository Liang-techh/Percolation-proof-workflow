# Route-B full mass functional composition leaf

This sidecar isolates the finite-dimensional mathematical composition step in
B45-1.  It defines the six-link mass functional as the sum of translational
Jacobian Gram terms and weighted rotational Gram terms, then proves that
pointwise equality of the link masses, Jacobians, and inertia weights implies
equality of the complete ideal mass matrix.

The theorem is deliberately source-independent.  It does not read the CSV,
assume the Julia implementation, or prove the Float64 enclosure bridge.  Its
purpose is to make those remaining obligations narrow adapters: the source
binding only needs to supply the linkwise equalities, after which the full
functional identity is kernel-checked by Lean.

Evidence level: compiled Lean candidate; no registry promotion until the
source adapters and comparator are admitted.
