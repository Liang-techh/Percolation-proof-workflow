# P5-103 initial reference Lean bridge

This sidecar formalizes only the source-independent kernel seams extracted from
柳冠一's `P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING` review.

Included:

- explicit D/B typed partition for the P5 weighted budget;
- `hybridBudget_eq_full_of_block_match`;
- exact initial-ball arithmetic `<= 27/800 < 28/5`;
- deterministic same-source anchor reconstruction and `anchor = self`;
- centered residual zero at the initial matched anchor;
- the explicit boundary that anchor equality alone leaves `obs x - lbar` as the
  bias until a nominal graph theorem identifies `lbar`;
- `nominalResidual_eq_zero_of_graph`, which consumes rather than invents the
  nominal graph equality;
- a pointwise acceleration counterexample showing that q/v/input alone do not
  determine the nominal residual.

Not formalized here:

- the deployed six-coordinate ordering/source projection into the D/B split;
- a real `referenceKey` or reference-generator source binding;
- linear-ODE existence/uniqueness for all times;
- actual `qbar/vbar/lbar` trajectory or flowpipe data;
- Float64/controller/DH semantics, P8 coverage, comparator/admission, registry,
  or P5/M4 final closure.

The verifier is portable for the repository CI convention.  It finds `lake` and
`lean` from `PATH`, checks the sidecar toolchain against the pinned
`examples/local_fkg` Lake environment and its `lake-manifest.json`, scans for
`sorry`/`admit`, compiles with `-DwarningAsError=true`, and requires an axiom
report for every public theorem.

Even a clean compile remains `compiled_candidate` evidence only: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
