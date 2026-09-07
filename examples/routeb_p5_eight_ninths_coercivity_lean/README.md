# Route-B P5 exact 8/9 coercivity Lean sidecar

This portable sidecar formalizes the source-independent algebra from
`agent_review_inbox/review-T-P5-032-honglianmozun-20260907T1253.md`.

It freezes the exact block-(4,5) `eps=1` storage `V` and dissipation `Q`, proves
the explicit nine-square identity for `Q-(8/9)V`, derives `Q >= (8/9)V`, and
then exposes the sharpened `4/9` ISS coefficient, `153 L2 < 40 Vstar` barrier,
`Kc=1/12` parameter-tube gate `153 mu + 1836 nu < 40`, the T-P5-031
`U/W/p/q` downstream specialization, and a square-root-free slack-feasibility
necessity diagnostic.

The sidecar deliberately does **not** authenticate a source residual/gain
table, Julia/DH/Float64 execution semantics, P8 same-domain coverage, ODE
first-exit/continuation, provenance/admission, registry state, or final P5/P8/M4
integration.

Run from a repository checkout with the pinned sibling `examples/local_fkg`
Lake environment:

```bash
CI_PORTABLE=1 examples/routeb_p5_eight_ninths_coercivity_lean/verify.sh
```

`verify.sh` resolves `lake` and `lean` from `PATH`, checks the local-fkg
`lean-toolchain` pin, compiles with `-DwarningAsError=true`, requires every
public theorem to emit a `#print axioms` report, and fails if `sorryAx` appears.

Admission boundary: a successful compile is only a `compiled_candidate`.
待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
