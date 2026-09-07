# Route-B P5 exact `93/100` block-(4,5) SOS sidecar

This portable Lean sidecar formalizes the source-independent mathematical core of `agent_review_inbox/review-T-P5-033-honglianmozun-20260907T1604.md`.

It freezes the exact scalar definitions `V45` and `Q45`, proves the exact weighted nine-square identity for `Q45 - (93/100)V45`, derives `Q45 >= (93/100)V45`, and proves the minimal downstream arithmetic replacements: the `-(93/200)V` Lyapunov coefficient, the quarter-barrier gate `1360 L2 < 93`, the `Kc=1/12` incremental gate `340 mu + 4080 nu < 93`, the exact `837/800` improvement factor, and the ultimate residual coefficient `340/93`.

The sidecar deliberately does **not** prove a concrete source residual cap, true-DH/Float64 semantics, source/domain binding, ODE existence or first-exit coverage, provenance/admission, or P5/M4 closure. Those remain separate obligations.

Run from a repository checkout with the pinned `examples/local_fkg` Lake environment available:

```bash
bash examples/routeb_p5_block45_93_sos_lean/verify.sh
```

`verify.sh` locates `lake` and `lean` from `PATH`, checks the local toolchain pin, compiles with `-DwarningAsError=true`, checks all exported `#print axioms` reports, and rejects `sorryAx`. It is marked `CI_PORTABLE=1` for `.github/workflows/lean-agent-sidecars.yml`.
