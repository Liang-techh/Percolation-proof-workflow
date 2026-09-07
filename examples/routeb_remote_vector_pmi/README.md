# Route-B vector remote PMI seam

`RemoteVectorPMI.lean` provides a two-dimensional, division-free Schur/PMI
adapter.  It consumes a single squared-norm enclosure for the vector remote
action and a mass-to-scale bridge:

```text
‖r_B‖² ≤ K · mass,   0 ≤ K,   mass ≤ β² y²,   K β² ≤ p d.
```

It then proves the two-dimensional PMI quadratic is nonnegative.  Keeping the
vector intact avoids charging the same `M_BD a_D` operator bound independently
to both block coordinates.  The sidecar also proves the sharp iff form: the
quadratic is nonnegative for every block vector exactly when
`‖r_B‖² <= p*d*y²`.  The theorem is source-independent and must be
compiled on the pinned GitHub Lean worker; no local Lean/Lake verification or
Route-B admission is implied.
