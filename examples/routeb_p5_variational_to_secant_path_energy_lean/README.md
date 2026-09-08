# T-P5-094 variational-to-secant path-energy Lean sidecar

Agent/source_agent: 巨阳仙尊.

This portable sidecar consumes only the mathematical review `T-P5-094-VARIATIONAL-TO-SECANT-PATH-ENERGY` and formalizes a deliberately small trusted core that does not require a full Riemannian-manifold or ODE-flow API.

Implemented leaves:

- `one_step_rational_decay_from_integral_packet`: exact division-free one-step consequence of an integrated derivative inequality plus the monotonicity-derived integral lower bound.
- `relative_rate_one_step_from_integral_packet`: the same leaf for an effective signed rate `mu-rho`.
- `finite_sum_path_energy_contraction`: pointwise weighted contraction implies contraction of a finite path-energy quadrature/sum.
- `quadratic_midpoint_jensen_of_psd_direction`: exact midpoint Jensen identity/inequality for a 2x2 quadratic form, assuming nonnegativity in the difference direction.
- `two_sample_secant_packet`: a minimal finite-sample Jensen consumer combining two tangent bounds into a secant-style averaged bound.
- `raw_normalized_chord_sq_expands`: exact nonlinear-chart counterexample showing normalized Euclidean chord expansion under `Psi(z)=2z`.
- `pullback_tangent_contracts`: exact pulled-back metric contraction for `M(z)=1/z^4`, preserving the physical factor `1/4`.

Deliberately OPEN: deriving the integral packet from differentiability/FTC, arbitrary-`N` equal-partition induction, Bochner/integral Jensen, full `C^1` Jacobian-to-secant theorem, path infimum/geodesic APIs, same-tube path-sheet coverage, chart path lifting, deployed source binding, Float64/FD/controller semantics, P8 flowpipe/ODE coverage, registry/admission.

`verify.sh` is `CI_PORTABLE=1`, resolves `lake`/`lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, requires the pinned `examples/local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, scans placeholders, audits `#print axioms`, and rejects `sorryAx`.

A green compile is only `compiled_candidate`: 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
