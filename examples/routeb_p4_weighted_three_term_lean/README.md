# P4 weighted three-term focused Lean sidecar

This sidecar is owned by **苏梦辰** for task `GH-LEAN-P4-032-weighted-three-term`.

It performs a pinned, focused compile of
`examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_WeightedThreeTerm.lean`
inside the repository's `examples/local_fkg` Lake environment.  It does not
supply a source identity, numerical operator certificate, trajectory coverage,
Float64 semantics, admission, or P4/M4 integration.

The target deliberately keeps `DistalForceDefect` and `DistalAccelDefect`
distinct.  The focused check fails closed on Lean warnings, missing axiom
reports, `sorryAx`, or source-level `sorry`/`admit` placeholders.

Run from a shell with `lake` and `lean` on `PATH`:

```bash
bash examples/routeb_p4_weighted_three_term_lean/verify.sh
```

Status after a green focused check remains only a compiled candidate: **待封不觉独立验证 / 待梁智炜最终整合**.
