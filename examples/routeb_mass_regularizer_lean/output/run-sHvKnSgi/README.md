# Route-B exact mass regularizer leaf

This leaf proves only the kernel-checked entrywise semantics of the exact real
regularizer `(1/1000000) I` and its composition with an explicit unregularized
mass/Fourier equality premise. It does not assert the unresolved DH/Fourier
identity or any Float64 equality.

The successful run, if present, is recorded under `output/` and must use the
pinned Lean/Mathlib environment. The theorem is a candidate input to B45-1.e/f
and to the constant-regularizer part of B45-4; it is not a physical source
binding and is not promoted to the verified registry by this leaf alone.
