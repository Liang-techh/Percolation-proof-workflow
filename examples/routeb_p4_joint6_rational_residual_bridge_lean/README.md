# P4 joint6 rational-residual cross-multiplication Lean sidecar

Owner/source agent: **苏梦辰**.

Mathematical input: `agent_review_inbox/review-GH-MATH-P4-JOINT6-ACTUAL-RESIDUAL-liuguanyi-20260908T2010Z.md` (柳冠一).

This sidecar formalizes only the source-independent algebraic bridge for comparing an actual rational residual `N_a/D_a` with the residual consumed by the P4 contract `N_c/D_c`. The core object is the signed cross mismatch

`Q = N_a D_c - N_c D_a`,

formed before absolute-value enclosure.  The Lean leaves cover exact cross-multiplication equality, same-cell sup containment, a division-free sup gate, the quotient-difference split used for Lipschitz control, the corresponding pairwise Lipschitz bound, and the division-free Lipschitz gate.

`ResidualCSE` is dependently indexed by both a cell key and an observable/source key.  The typed adapter theorems therefore require the actual and contract CSEs to share those indices; this prevents an interface consumer from silently splicing numerator/denominator evidence from unrelated cells or observables.

## Explicit nonclaims / open boundary

This sidecar does **not** provide the missing principal compact joint6 source packet.  In particular it does not instantiate the deployed `N_a,D_a,N_c,D_c`, denominator regime, same-observable binding, numeric `E`, or Lipschitz packet for `Joint6_GetStarTheta`/`zd6`.  It does not change the `.002` baseline, parameter box, P4 parent status, checker/ledger admission, registry, Float64/FD/controller semantics, or ODE/coverage status.

The source-specific closure remains a later theorem instantiation once the principal compact-branch CSE packet is surfaced.  Even a clean compile/axiom receipt here is only a compiled candidate: **待封不觉独立验证 / 待梁智炜最终整合**.

## Focused verification

The portable verifier uses the repository-pinned local-FKG Lake environment and resolves `lake`/`lean` from `PATH`:

```bash
CI_PORTABLE=1 bash examples/routeb_p4_joint6_rational_residual_bridge_lean/verify.sh
```

It enables `-DwarningAsError=true`, scans for `sorry`/`admit`, and requires a `#print axioms` report for every exported theorem.
