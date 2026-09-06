# Bounded residual-budget falsification, not a certificate

The original six-axis Julia `arm_MCG` and Float64 solve are read-only inputs.
RK4 integrates all twelve state coordinates and the total reference-force cost
`R'=e4^2/(8/5)+e5^2/(13/10)` over T=1. It is neither interval reachability nor
the exporter's discrete stepping algorithm. All results are E1 numerical only.

Eight axis/origin initial cases at 400 steps gave a maximum R of
0.00984855512579 (q2=0.149, ramp c=1.7). Refining only that case to 800 steps
gave 0.00984855512551. Agreement does not bound integration or rounding error.

`linear_direction.py` uses rational Fourier M(0) plus the source's 1e-6
diagonal regularizer and the rational potential Hessian to construct an
exact-real model linearization. The first run correctly failed its reference
mass assertion because the CSV has no regularizer; source inspection of
`build()` and `mass_matrix()` established where to add it. No source was changed.
Gauss-Legendre quadrature, matrix exponentials and the trust-region direction
are floating point and un-enclosed. The linearized predicted R=0.01367956 and
set-wide numerical screen 0.01417223 are NOT nonlinear upper bounds.

The single selected full12 direction (norm=0.149, c=1.7), evaluated by the
original nonlinear Julia-FD dynamics with 800 RK4 steps, yielded:

- R(1)=0.0100229985895;
- maximum sampled p=0.10152929;
- terminal qpoly=0.24623045.

This is nine distinct initial cases and one refinement, not an exhaustive
search. No budget violation was found; R<=0.1 for the original full initial
ball and ramp family remains OPEN. The unstable linear mode (spectral abscissa
about 1.93462) is not ignored and is not a finite-time counterexample.

Reproduction: Julia `--startup-file=no -O1 screen.jl 400`; the refined axis
case uses `screen.jl 800 2`. The adversarial case uses
`screen.jl 800 9 linear_output/candidate.csv`. Python needs numpy and scipy;
`linear_direction.py` refuses to overwrite its existing output directory.
Every Julia run retains its script snapshot, source hash, metadata and sampled
trajectories in a fresh directory. No further numerical campaign is scheduled.
