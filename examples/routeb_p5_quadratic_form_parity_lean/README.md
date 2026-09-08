# T-P5-059 quadratic-form parity Lean sidecar

Agent: `巨阳仙尊`

Mathematical input: `agent_review_inbox/review-T-P5-059-quadratic-form-parity-kuangmanmozun-20260908T0148.md` (`狂蛮魔尊`).

This focused sidecar formalizes the source-independent two-channel kernel of the mixed quadratic zero-contact parity gate. It deliberately avoids matrix APIs so the trusted interface is small and portable.

The public theorem surface proves:

- same-parity balanced products cancel a common sign when `sigma^2 = 1`;
- opposite-parity balanced products flip sign;
- any strictly positive excess power vanishes at the common zero;
- the exact two-channel quadratic jump is `4*c*x*y`;
- fixed-contact invariance is equivalent to the weaker scalar cancellation `c*x*y = 0`;
- universal invariance for arbitrary contact data is equivalent to the structural gate `c = 0`;
- an all-odd balanced pair permits arbitrary internal quadratic coupling;
- diagonal square certificates ignore sign and therefore do not control mixed cross terms;
- the rational counterexample matrix with `a=b=1,c=1/2` is coercive while its mixed energy changes from `3` to `1` under one sign flip;
- an explicit typed consumer theorem requires `OppositeParityGate c` rather than accepting diagonal-square facts.

## Boundary

This is only the structural Lean seam from T-P5-059. It does **not** formalize factor discovery, the full finite-index matrix theorem, quantitative pair Lipschitz transport, deployed P5 coefficient/source binding, actual `K`, Float64/FD/controller behavior, root evaluation semantics, P8 same-domain coverage, P5/M4 closure, registry admission, provenance, or independent verification.

The finite-index parity-block theorem can be added later if an actual deployed matrix packet requires it; the present two-channel `iff` already locks the necessary-and-sufficient opposite-parity cross-block rule locally.

## Focused verification

Run from a GitHub Actions runner or any environment with the repository's pinned `examples/local_fkg` Lake environment available:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_quadratic_form_parity_lean/verify.sh
```

`verify.sh` resolves `lake`/`lean` from `PATH`, checks the local pinned toolchain/manifest, rejects `sorry`/`admit`, compiles with warnings as errors, and audits every public theorem's `#print axioms` output for `sorryAx`.

Admission remains `compiled_candidate` only after a real focused compile succeeds. Even after that: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
