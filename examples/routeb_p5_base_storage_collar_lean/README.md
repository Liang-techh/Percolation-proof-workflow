# T-P5-100 base-storage collar Lean sidecar

Owner/source agent: **苏梦辰**. Upstream mathematics: 红莲魔尊 review `T-P5-100-BASE-STORAGE-COLLAR-MATH`, commit `febe9541e36e38f5070bcb4a0ef1ffc7b7a61d41`.

This sidecar formalizes only the exact-real theorem layer requested by that review. It deliberately separates a base-state storage collar from tangent/variational semantics.

The exported leaves cover: signed energy-ledger compression; a two-channel composition step that can be folded for finite collections; the division-free `nu=c-alpha` collar compiler and inner additive gate; a 2x2 exact lifted-base-storage identity with separate nominal metric drift, base-flow Lie defect and lift defect; weighted square completion; robust lifted collar propagation; the inner-boundary inwardness consequence; affine storage normalization with the mandatory `a E + nu^2 k` budget transport; affine gate/gap covariance; and the scalar `F=x+x^3, zeta=x` nonzero-lift-defect regression.

## Typed interface boundary

The 2x2 algebra takes the triples `nma/nmb/nmc` and `bma/bmb/bmc` as already-typed caller evidence for the symmetric components of `W_t-DW[F]` and `DW[b]`. The caller must separately establish those derivative/source identities on the same outer collar. Likewise, the scalar robust theorem accepts `C0`, `Sb`, relative lift power, additive cross power and weighted-square budget only after they have been bound to one common base flow/storage/lift packet. This sidecar never identifies a variational vector with a base-state displacement by name.

## Intentionally OPEN

- actual Route-B `U_base`, `actualFlow`, `sourceTube`, `R_in/R_out` source packet;
- same-collar derivative identities for `W,F,b,zeta,e_lift`;
- deployed DH / Float64 / finite-difference / controller / solve semantics;
- source-tube/path-sheet coverage and P8 ODE continuation/flowpipe;
- theorem registry/admission and final integration.

A green compile is therefore only a `compiled_candidate`, never a source/coverage certificate.

## Focused verification

Run from a checkout that has the repo-pinned `examples/local_fkg` Lake environment:

```bash
CI_PORTABLE=1 examples/routeb_p5_base_storage_collar_lean/verify.sh
```

`verify.sh` requires `lake` and `lean` from `PATH`, checks the sidecar toolchain against the pinned Lake environment, rejects `sorry`/`admit`, compiles with warnings as errors, and requires an axiom report for every exported theorem.

**待封不觉独立验证 / 待梁智炜最终整合。**
