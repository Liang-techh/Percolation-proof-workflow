# Route-B P5 damping-split Lean sidecar

This portable sidecar formalizes the source-independent scalar mathematics from `agent_review_inbox/review-T-P5-015-guyuefangyuan-20260907T0438.md`.

It kernel-checks:

- the generic division-free damping-split certificate and its headroom consequence;
- the exact `2/3 : 1/3` rational specialization;
- dominance of `2/3 : 1/3` over the previous `1/2 : 1/2` split on nonnegative loads;
- the exact rational counterexample showing the half split can reject a case admitted by `2/3`;
- the calculus-free stationary polynomial identity and optimizer comparison;
- the current C-FD integer reduction with `Q = 13*S_F/72000000000000000`, including the `T=1` source-facing certificate.

The sidecar deliberately stops before source/checker binding of `S_F`, `Z0`, `Hbar`, `Rbar`, Float64/solve semantics, ODE existence/continuation, P8 coverage, admission, or final integration.

## Focused verification

From this directory, with `lake` and `lean` on `PATH` and the repository sibling `examples/local_fkg` present:

```bash
./verify.sh
```

CI discovers this verifier through the `CI_PORTABLE=1` marker. The script checks the pinned Lean toolchain, compiles with `-DwarningAsError=true`, requires `#print axioms` output for every exported theorem, and rejects `sorryAx`.

Status after a successful focused check remains: **待封不觉独立验证 / 待梁智炜最终整合**.
