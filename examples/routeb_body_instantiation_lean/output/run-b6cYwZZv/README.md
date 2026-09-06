# Route-B six-link body instantiation leaf

This sidecar instantiates the generic body COM/Jacobian/mass semantics on the
actual six-step Route-B real frame chain. It defines the seven frame slots,
projects origins and pre-current joint axes, and reuses the kernel-checked
body lemmas for midpoint COM, ancestor cutoff, inactive columns, and link-mass
Gram expansion.

The theorem remains an ideal real-matrix bridge. Julia `Float64` operations,
machine trigonometry, and the full deployed mass function are still open.
