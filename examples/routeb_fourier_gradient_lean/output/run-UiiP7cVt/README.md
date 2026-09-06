# Route-B Fourier potential gradient leaf

This sidecar proves the analytic coordinate-gradient formula for a finite
Fourier potential.  It differentiates the exact finite row sum along a single
joint-coordinate line and obtains the corresponding component of the
Fourier-gradient evaluator.

The result is source-independent and does not identify the deployed Julia
potential, its central finite-difference implementation, or Float64 values.
Those remain explicit B45-2 source-adapter obligations.  No registry promotion
is made by this leaf.
