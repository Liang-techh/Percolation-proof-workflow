# Route-B P7 normalization-safe Schur transport Lean sidecar

This focused sidecar formalizes the source-independent continuation of `T-P7-002` from `agent_review_inbox/companion-T-P7-002-honglianmozun-20260907T0854.md`.

It proves four interfaces needed by the P7 energy seam: diagonal-coercivity Schur completion from physical covector boxes; exact transport of a normalized 2-vector through an explicit 2x2 map `N`; exact rectangular-box cost and vertex sharpness for `N^T diag(a0,d0)^(-1) N`; and the obstruction showing that `eta < tau` alone gives no finite uniform physical-cost cap if the positive normalization scale is unconstrained.  It also includes scalar-normalization and entrywise-interval fallback lemmas.

The sidecar deliberately does **not** identify the frozen P7 coefficients with deployed Julia/DH outputs, identify the seven-term polynomial, prove P8 flowpipe coverage, close P7/M4, or perform admission/registry work.

## Focused check

The repository workflow bootstraps the pinned `examples/local_fkg` Lake environment and runs every `CI_PORTABLE=1` sidecar.  Locally, with `lake` and `lean` on `PATH`:

```bash
CI_PORTABLE=1 bash examples/routeb_p7_normalization_safe_schur_lean/verify.sh
```

`verify.sh` checks the sidecar under Lean `4.32.0` with `-DwarningAsError=true`, requires an axiom report for every exported theorem, and fails if `sorryAx` appears.

## Main theorem boundary

The principal consumer is `normalization_safe_schur_consumer`.  It assumes positive lower diagonal coercivity `0<a0<=a`, `0<d0<=d`, a typed matrix map from checker coordinates `(h1,h2)` to the physical covector, and independent component boxes.  Its extra `s^2` charge is the explicit `boxCost` computed from that map.  `interval_normalization_schur_cost` is a weaker fallback when only entrywise absolute bounds on the normalization map are available.

The source lane must still decide whether the frozen P7 constants bound the physical covector directly or a normalized representation; if normalized, it must bind the actual normalization map (or sound entrywise bounds) on the same covered domain.
