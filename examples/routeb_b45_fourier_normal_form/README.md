# B45-1.1/B45-1.2 Fourier single-step normal form

This sidecar contains only a small reusable algebraic Lean interface. It does
not bind the original Julia `Float64` implementation to Lean `Real`, and it
does not claim a mass, residual, coverage, or reachability certificate.

`FourierNormalForm.lean` compiles the single-step DH matrix entries after
replacing `cos(q+offset*pi/2)` and `sin(q+offset*pi/2)` by the formal Laurent
atoms `fourierCos eps z` and `fourierSin eps z`. The source-specific phase and
DH constants are recorded as exact rational definitions.  It now also proves
the six exact phase identities for `z = Complex.exp (Complex.I * (q : ℂ))`,
using only the pinned Mathlib complex-exponential and unit-norm lemmas.

This remains a single-step semantic bridge: it is not yet a Julia `Float64`
binding, a multi-step product theorem, or a full mass-matrix certificate.
