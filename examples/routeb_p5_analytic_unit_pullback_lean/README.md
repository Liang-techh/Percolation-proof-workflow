# T-P5-064 analytic-unit pullback Lean sidecar

Agent: 巨阳仙尊

This is a source-independent Lean sidecar consuming the mathematical/interface result in `agent_review_inbox/review-T-P5-064-analytic-unit-pullback-liuguanyi-20260908T0321.md`.

It formalizes the smallest trusted seams that are useful downstream without importing source discovery into the kernel-facing layer:

- a certified positive multiplier cannot hide a zero or cancel a real contact jump;
- the exact rational worked pullback `((3-z)z^2)/((2+z)z)=((3-z)/(2+z))z`;
- the worked unit envelope `1 <= (3-z)/(2+z) <= 7/3` on `[-1/2,1/2]`;
- the exact worked-unit difference identity and rational Lipschitz constant `20/9`;
- a generic three-factor sup envelope for `U*P*R`;
- the exact three-factor telescoping identity and the T-P5-064 composition budget
  `LU*BP*MR + BU*LP*MR + BU*BP*LR`;
- a fail-closed hidden-zero regression proving that `u(z)=z`, although pointwise nonzero on a punctured interval, has no positive unit margin and yields an unbounded reciprocal near contact.

Deliberately **not** formalized here: the fully general finite-index `zpow`/valuation/parity pullback identity, deployed CSE factorization/source binding, actual rational unit enclosures from deployed code, Float64/libm/FD/controller semantics, P8 ODE/domain coverage, comparator/provenance/admission, or any P5/P8/M4 final closure.

The focused verifier is portable and uses the repository-pinned `examples/local_fkg` Lake environment. It requires `lake` and `lean` from `PATH`, checks the pinned toolchain, rejects `sorry`/`admit`, compiles with `-DwarningAsError=true`, and audits `#print axioms` output.

Run from the repository root:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_analytic_unit_pullback_lean/verify.sh
```

A successful compile is only `compiled_candidate` evidence. It remains **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.
