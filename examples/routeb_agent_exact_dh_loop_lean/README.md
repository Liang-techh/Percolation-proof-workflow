# Exact-real six-step DH loop

This is a self-contained Lean sidecar.  It imports only `Mathlib` and defines
the six-step real DH transform, recursive frame loop, frame origins/axes,
midpoint COM, translational/rotational Jacobians, per-link mass, and the
assembled `massMatrix`.  The final theorem proves the structural equality
`massMatrix = massFromLinks` by exact definitional expansion.

This is an ideal exact-real theorem.  It does not certify Julia `Float64`
evaluation, numerical trigonometric enclosure, physical parameter data, or a
full Route-B registry claim.
