# Route-B P4 force-coordinate congruence Lean sidecar

This portable sidecar formalizes the source-independent mathematics from `agent_review_inbox/review-T-P4-018-liuguanyi-20260907T0522.md`.

The canonical P4 generalized-force residual is typed as `l_F = I_B f_B - M0_BB a_B` with `I_B = diag(1/5,1/10)`. Therefore the literal PMI nominal/acceleration-style `kc` vector `(q5/20,q4/20)` contributes `(q5/100,q4/200)` to `l_F`. The sidecar proves that map exactly, proves the division-free scalar congruence needed to reason equivalently in the nominal coordinate, and proves the mixed-coordinate force envelope `j(c+betaA)+betaF` together with an aligned extremizer.

The channel-4 corollaries freeze the exact rational identities `j=1/5`, `pF=3/5`, `pA=15`, `cA=1/20`, `cF=1/100`, and the current exact `d4`. The force-side quarter consumer is exposed with the typed mixed budget `(1/5)*betaA + betaF <= 6/25`.

Run from the repository checkout:

```bash
CI_PORTABLE=1 ./examples/routeb_p4_force_coordinate_congruence_lean/verify.sh
```

`verify.sh` locates `lake` from `PATH`, checks the pinned toolchain and `examples/local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, requires every exported theorem's `#print axioms` report, and rejects `sorryAx`.

Boundary: this sidecar does not authenticate Julia/Float64 source execution, does not prove the source checker labels the two coordinate layers correctly, does not replace generic Schur theorems, and does not close P4/M4 or mutate the verified registry. It is a theorem candidate pending independent verification and coordinator integration.
