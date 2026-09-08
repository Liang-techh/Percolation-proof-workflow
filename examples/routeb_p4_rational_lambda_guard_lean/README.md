# Route-B P4 rational common-lambda guard Lean sidecar

This portable sidecar formalizes the source-independent mathematical children
from `T-P4-039` and `T-P4-040`:

- `agent_review_inbox/review-T-P4-039-liuguanyi-20260907T1616.md`;
- `agent_review_inbox/review-T-P4-040-rational-lambda-guard-kuangmanmozun-20260907T1642.md`.

The T-P4-039 lane has four explicit Lean-facing leaves:
`young_completed_square_identity`, `young_feasible_of_rational_radius`,
`young_inner_interval_feasible`, and
`young_common_parameter_of_inner_bounds`. Their statements are division-free:
the interval is represented by cross-multiplied inequalities in `Real`; a
rational checker witness is supplied by coercion, not by an inverse in the
trusted theorem statement.

It proves:

- the exact scalar quadratic chord identity for `q(s)=P*s^2-G*s+A`;
- endpoint certification for a convex quadratic on an interval;
- a common interval consumer for an arbitrary row-index type;
- a direct `lambda`-facing version with `s=lambda-1`;
- exact left/right expansions around a nominal rational witness;
- a symmetric rounding guard from `|s-s0|<=r` plus endpoint checks;
- preservation of `lambda>1` when `r<s0`;
- one-sided source coefficient envelope domination for `s>=0`;
- a row-family source-envelope interval theorem;
- exact counterexamples showing why convexity, an explicit rounding radius, and the sign restriction on `s` matter.

The sidecar is intentionally algebraic. It does **not** prove any concrete DH
coefficient, source binding, Float64-to-real containment, P8 coverage,
trajectory invariance, P4/M4 closure, or registry admission.

## Portable verification

The verifier uses the repository-pinned `examples/local_fkg` Lake environment
and requires `lake` and `lean` on `PATH`:

```bash
bash examples/routeb_p4_rational_lambda_guard_lean/verify.sh
```

The script is marked `CI_PORTABLE=1`, so
`.github/workflows/lean-agent-sidecars.yml` executes it on GitHub-hosted CI.
It compiles with `-DwarningAsError=true`, checks every public theorem has a
`#print axioms` report, rejects `sorryAx`, and scans the Lean source for
`sorry`/`admit` placeholders.

Admission boundary: successful compilation is only a `compiled_candidate`.
待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
