# Route-B body COM/Jacobian mass leaf

This sidecar makes the source-audited body semantics explicit: midpoint COM
between consecutive origins, pre-current parent axes, cross-product
translational columns, angular columns, and the `j <= body` ancestor cutoff.
It proves inactive columns vanish and expands each body contribution into the
link-mass Gram form already used by the full mass-functional composition leaf.

This remains an ideal semantic interface.  It does not yet bind the origins and
axes to the Julia frame function or prove Float64/full-q Fourier equality.
