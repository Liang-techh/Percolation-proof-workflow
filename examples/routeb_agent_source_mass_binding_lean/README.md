# Agent sourceBodyMass/sourceContract binding candidate

This sidecar isolates the smallest function-level seam that is missing from
the current Route-B B45-1 audit.  It defines `sourceBodyMass` from the
already compiled `sourceContract` and exact rational mass/inertia tables, then
proves that the six-body sum is the generic `massFromLinks` functional.

The theorem is intentionally honest about its boundary: it does not define
the deployed Julia `sourceBodyMass`, parse CSV, prove Float64 rounding, or
identify the Fourier CSV evaluator.  The remaining comparator obligation is
to prove that the deployed source function is extensionally equal to this
Lean `sourceBodyMass` at the same zero-based body index.
