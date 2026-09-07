# T-P5-034 exact 15/16 block-(4,5) SOS Lean sidecar

Formalization-only sidecar for `agent_review_inbox/review-T-P5-034-honglianmozun-20260907T1701.md`.

It freezes the exact source-independent block-(4,5) scalar forms `V45` and `Q45` and checks:

- the weighted nine-square identity `Q45 - (15/16)V45 = SOS`;
- coercivity `Q45 >= (15/16)V45`;
- the exact rational witness showing the rounded-up `47/50` bound is false;
- the residual-coupled ledger `Vdot <= -(15/32)V + (17/10)L2`;
- the `Vstar=1/4` division-free gate `1088 L2 < 75`;
- the `Kc=1/12` incremental gate `272 mu + 3264 nu < 75`;
- the exact improvement factor `125/124` over T-P5-033 and ultimate coefficient `272/75`.

The sidecar intentionally does **not** establish source residual binding, Julia/Float64/true-DH execution semantics, first-exit/ODE continuation, P8 same-domain trajectory coverage, provenance/admission, registry mutation, or final P5/M4 integration.

Run from a checkout containing the pinned `examples/local_fkg` Lake environment:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_block45_15_16_sos_lean/verify.sh
```

`verify.sh` resolves `lake` and `lean` from `PATH`, compares the sidecar toolchain with the repository Lake environment, compiles with `-DwarningAsError=true`, requires an axiom report for every exported theorem, and rejects any `sorryAx` occurrence.

Status after a successful focused compile is only `compiled_candidate`: 待封不觉独立验证 / 待梁智炜最终整合。
