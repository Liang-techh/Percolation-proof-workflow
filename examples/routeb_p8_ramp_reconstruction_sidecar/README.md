# P8 ramp reconstruction sidecar

This sidecar formalizes the pure calculus child extracted in `T-P8-006`.

It proves, under globally stated `HasDerivAt` hypotheses:

- `c' = 0`, `c(0)=c0` implies `c(t)=c0`;
- `w' = c`, `w(0)=0` implies `w(t)=c0*t`;
- the same statements for a typed `Fin 14 -> ℝ` trajectory;
- `w(1)=c0`.

The globally differentiable assumptions are intentionally stronger than the final interval-local P8 theorem should need. This is a first kernel-friendly implementation of the mathematical core, not a claim that the weaker endpoint/interval formulation is already formalized.

The file now also exposes an interval-local seam:

- `endpoint_eq_of_zero_derivative_on_interval` uses `ContinuousOn` on `Icc`, `HasDerivAt` on `Ioo`, and an explicit zero-derivative integrability premise;
- `ramp_endpoint_on_interval` transfers the tail endpoint using the deployed derivative and the explicit integral identity for `c`.

The latter two integral/source premises are intentionally not discharged here. They are the next P8 frontier: source binding, interval RHS containment, and flowpipe/coverage must provide them with their own receipts.

## Portable verification

The sidecar reuses the repository's pinned `examples/local_fkg` Lake environment and pins the same Lean toolchain locally. `verify.sh` contains `CI_PORTABLE=1`, so `.github/workflows/lean-agent-sidecars.yml` can run it on a GitHub-hosted runner.

Run manually from the repository root with:

```bash
bash examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh
```

A successful run must end with:

```text
AXIOM_AUDIT=PASS
P8_RAMP_RECONSTRUCTION_FOCUSED_CHECK=PASS
```

## Boundary

Not proved here: deployed Julia/DH first-12 source binding, full ODE existence, interval RHS containment, Picard/local flowpipe existence, continuation/coverage, or Route-B/M4 admission. Those remain separate obligations. The interval-local lemmas are an adapter surface, not an admission claim.
