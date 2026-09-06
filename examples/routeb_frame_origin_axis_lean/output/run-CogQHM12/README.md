# Route-B frame origins/axes semantic leaf

This sidecar kernel-checks the source-level DH frame bookkeeping used by the
deployed Julia port: the current parent frame is recorded first, the current
axis is read from its third column, and only then is `parent * current` used
for the next frame. It also proves that the six Route-B real DH steps produce
seven frames and that the origin/axis arrays are exactly the projections of
that frame chain.

This is an ideal real-matrix semantic theorem. It does not claim Julia
`Float64` equality, machine `sin/cos` enclosure, or full mass-function
equality.
