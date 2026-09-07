# Route-B P5 affine FD-envelope adapter sidecar

This portable Lean sidecar formalizes the source-independent interface results from `review-T-P5-009-liuguanyi-20260907T0606.md`.

It proves four boundaries that downstream P5 consumers can use without changing the original affine FD envelope:

1. A positive offset can be converted into a homogeneous componentwise gain on a punctured domain only after a state floor `nu <= |x|`; the core theorem is division-free.
2. An equilibrium-containing domain should instead use a centered increment estimate for the actual source error map.
3. The six-channel affine box always has a legal weighted-dual mixed charge `2*S*cap^2 + 2*B`, so positive offsets may be routed to the finite-horizon additive budget rather than hidden inside a relative gain.
4. `anchored_offset_not_uniformly_relative` records an explicit error map with exact equilibrium value zero but a positive off-equilibrium jump, proving that equilibrium anchoring alone is not enough to infer a finite homogeneous relative gain.

Run from a repository checkout:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_affine_fd_adapter_lean/verify.sh
```

The verifier uses `lake` from `PATH` and the pinned `examples/local_fkg` environment. It does not authenticate the deployed DH/Float64 source, establish `cap`/state compatibility, prove centered Float64 increments, establish P8 domain coverage, or mutate P5/M4 registry/admission state.

A successful compile is only a compiled candidate, pending 封不觉 independent verification and 梁智炜 final integration.