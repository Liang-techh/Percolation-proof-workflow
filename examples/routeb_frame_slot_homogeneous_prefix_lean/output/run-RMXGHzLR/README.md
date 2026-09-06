# Route-B frame-slot to homogeneous-prefix adapter

This Mathlib-only sidecar closes the narrow ideal-real shape gap between the
source-oriented `routeBFrameSlot` accessor and the abstract `homogeneousPrefix`
used by the prefix projection lemmas.  It reuses the successful concrete-step
homogeneous theorem and does not unfold or reinterpret the Julia Float64
evaluator.

The result is a compiled candidate only until the source comparator accepts the
corresponding definitions.
