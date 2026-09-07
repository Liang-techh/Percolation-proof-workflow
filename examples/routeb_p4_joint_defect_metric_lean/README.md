# T-P4-033 joint defect metric Lean sidecar

This portable sidecar formalizes the source-independent mathematical core of 柳冠一's `T-P4-033` review.

It proves an exact division-free weighted-square identity, the induced `+Td+b` and `-Td+b` normed-space pushforwards, preservation of a relative-plus-additive budget, a coordinate-pullback domination lemma, a singular-metric kernel obstruction, and scalar correlated-metric sign-flip identities for the force/O1 convention change.

The verifier uses `lake`/`lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, checks the pinned Mathlib revision in `examples/local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, and rejects any `sorryAx` in the printed theorem axioms.

Run:

```bash
CI_PORTABLE=1 bash examples/routeb_p4_joint_defect_metric_lean/verify.sh
```

This is only a formalization candidate. It does **not** bind the deployed defect pair, `T=M_BD M_DD_inv`, a concrete 6x6 source metric, Float64/controller/solve semantics, interval/domain coverage, P4/P8/M4 closure, provenance/admission, registry state, or final integration. Those remain open for the corresponding source/checker and integration agents.
