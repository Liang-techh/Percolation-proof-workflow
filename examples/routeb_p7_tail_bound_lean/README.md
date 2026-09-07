# Route-B P7 exact rational tail bound

This sidecar proves the final scalar arithmetic for the physical seven-term
tail bound, using the exact rational constants emitted by the independent
checker in the external Route-B project.

The checked conclusions are:

```text
eta(qmax = 13/50) < 1/160000
eta(qmax = 3/8)   < 1/160000
```

The sidecar is intentionally not a physical-source theorem. It does not prove
that the Julia Float64 trajectory is represented by the polynomial, that the
tail absorbs the full residual, or that P7/P8/M4 has global coverage. Those
obligations remain open and are recorded in the persistent Route-B state.

The pinned local environment is Lean 4.32.0 from `examples/local_fkg`.
