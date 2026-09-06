# Route-B frame slot accessor leaf

This sidecar proves that a fixed `Fin 7` frame accessor is exactly the
corresponding `get?` slot of the recursive source frame list. It then lifts
the correspondence to source origin and axis arrays. The proof is structural
and intentionally leaves matrix multiplication and Julia `Float64` operations
opaque.
