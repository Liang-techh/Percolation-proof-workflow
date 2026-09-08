# T-P5-071 signed two-cycle Lean sidecar

Agent/source_agent: **巨阳仙尊**.

This portable sidecar formalizes the source-independent kernel-facing leaves from 狂蛮魔尊's `T-P5-071-SIGNED-TWO-CYCLE-CONTACT` review:

- unsigned two-cycle elimination and strict small-gain injectivity;
- source-cleared determinant-style inverse budgets without division;
- opposite-orientation composition -> antitone scalar cycle;
- unit one-sided and absolute coercivity of `G(s)=s-phi(s)` for antitone `phi`;
- a denominator-free scalar perturbation consumer for negative feedback;
- strict-monotone zero-location lemmas used by source-sign -> root-orientation adapters;
- linear regressions separating same-orientation unit-gain obstruction from arbitrarily large negative-feedback gains.

The trusted core **does not** prove the T-P5-071 interval fixed-point/existence theorem, continuity or construction of the deployed root maps, concrete source sign/orientation binding, exact source cross-variation exporters, Float64/libm/controller/FD semantics, P8 same-domain ODE coverage, admission, registry mutation, or P5/P8/M4 final closure. Failure of both the opposite-orientation branch and the strict unsigned small-gain branch remains `NOT_APPLICABLE`, not a proof of noninvertibility.

Run from a GitHub CI environment that already provides the repository's pinned `examples/local_fkg` Lake environment:

```bash
CI_PORTABLE=1 examples/routeb_p5_signed_two_cycle_lean/verify.sh
```

Expected policy: `lake` and `lean` must be on `PATH`; no host-specific absolute tool path is used.
