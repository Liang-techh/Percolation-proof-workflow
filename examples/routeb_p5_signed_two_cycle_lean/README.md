# T-P5-071 signed two-cycle companion Lean sidecar

Agent/source_agent: **巨阳仙尊**.

Concurrency note: while this lane was being built, **苏梦辰** independently committed the main `T-P5-071` formalization at `examples/routeb_p5_signed_two_cycle_contact_lean/`. To avoid duplicate ownership, this path is now explicitly a **companion**. Its unique integration-facing scope is the base-parameter `D` transport left open by the main sidecar, plus a source-cleared negative-feedback transport that does not introduce the unsigned determinant reserve `Delta = mu1*mu2-C12*C21`.

The companion theorem cluster contains:

- `negative_feedback_parameter_transport_x1/x2`: from a unit-coercive opposite-orientation scalar inverse, an outer slope charge and an inner parameter charge, derive
  `X1 <= Z1 + a*Z2 + (p+a*q)*D` and
  `X2 <= b*Z1 + Z2 + (q+b*p)*D`;
- `cleared_negative_feedback_parameter_transport_x1/x2`: the corresponding division-free source-cleared numerators, with no `Delta > 0` hypothesis;
- `negative_feedback_scalar_budget`: denominator-free perturbation of an antitone scalar cycle;
- local support/regression lemmas for antitone composition/coercivity, unsigned fallback elimination, strict small-gain injectivity, source-cleared unsigned budgets, root-sign orientation leaves, and same-vs-opposite-orientation linear behavior.

The overlapping support lemmas are not a competing claim against 苏梦辰's main sidecar; they keep this companion independently compilable and make the `D`-transport seam kernel-local.

The trusted core **does not** prove the T-P5-071 interval fixed-point/existence theorem, continuity or construction of deployed root maps, concrete source sign/orientation/slope-variation binding, exact source exporters, Float64/libm/controller/FD semantics, P8 same-domain ODE coverage, admission, registry mutation, or P5/P8/M4 final closure. Failure of both the opposite-orientation branch and strict unsigned small-gain fallback remains `NOT_APPLICABLE`, not a proof of noninvertibility.

Run from a GitHub CI environment that already provides the repository's pinned `examples/local_fkg` Lake environment:

```bash
CI_PORTABLE=1 examples/routeb_p5_signed_two_cycle_lean/verify.sh
```

Expected policy: `lake` and `lean` must be on `PATH`; no host-specific absolute tool path is used.
