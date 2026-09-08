# T-P5-038 — block-(4,5) Pareto bridge Lean sidecar

This sidecar formalizes only the source-independent algebraic bridge suggested by the new T-P5-036/T-P5-037 mathematical handoff.

It consumes the two endpoint inequalities as explicit hypotheses:

- scalar endpoint (T-P5-037): `Q >= (109/200)V + (1/6)u4^2 + (1/6)u5^2`;
- anisotropic endpoint (T-P5-036): `Q >= (27/50)V + (101/500)u4^2 + (1/6)u5^2`.

For `0 <= r <= 1`, it proves the exact rational convex family

`Q >= ((109-r)/200)V + ((250+53r)/1500)u4^2 + (1/6)u5^2`,

checks the exact `r=0` and `r=1` reductions, formalizes the endpoint-margin threshold `E4 > (101/5300)Vstar`, and gives a division-free quarter-barrier first-exit theorem using the cleared checker

`300000 E4 + 1200(250+53r)E5 < (109-r)(250+53r)`.

The first-exit theorem is deliberately abstract: the endpoint certificate, exact derivative identity, same-domain residual caps, and boundary equality are all hypotheses. This file does **not** prove the real source bounds `E4,E5`, true-DH/Float64 semantics, trajectory coverage, ODE existence/continuation, endpoint integration, parent closure, or registry admission.

Run with the repository-pinned environment:

```bash
bash examples/routeb_p5_pareto_bridge_lean/verify.sh
```

The verifier locates `lake`/`lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, compiles with `-DwarningAsError=true`, prints axioms for every exported theorem, and rejects `sorryAx`.
