# Route-B P4 execution residual Lean sidecar

This sidecar formalizes the source-independent theorem decomposition from
`agent_review_inbox/review-T-P4-007-liuguanyi-20260907T0212.md`.

It isolates the algebra that must remain true when the deployed Float64 solve
is lifted to real numbers:

1. `block_tau_from_solve_defect` fixes the sign convention for
   `solveDefect = M*a - (tau-C-G)`;
2. `block_residual_with_solve_defect` proves the block generalized-force
   residual identity with the explicit `-solveDefect_B` term;
3. `block_residual_exact_solve` shows the older exact-solve identity is only a
   specialization obtained from the explicit zero-defect premise;
4. `centered_reference_split` and
   `centered_reference_split_with_model` formalize the runtime/reference
   centering identity, so a reference-point evaluation offset is charged as
   `delta(q)-delta(q0)` rather than twice as independent bias; and
5. `relative_envelope_zero_slice` plus its pointwise/obstruction forms prove
   that any envelope `|l| <= k|y|` necessarily forces `l=0` wherever `y=0`.

The sidecar deliberately keeps `M_BB*a_B`, `M_BD*a_D`, controller terms, and
runtime remainders as typed abstract vectors. It does **not** prove Float64
error bounds, DH source equality, the remote-mass energy premise, P8 coverage,
full P4 residual absorption, M4 closure, or registry admission.

## Focused verification

The repository workflow `.github/workflows/lean-agent-sidecars.yml` can run this
artifact because `verify.sh` contains `CI_PORTABLE=1`. The script resolves
`lake` from `PATH`, reuses the repository-pinned sibling `examples/local_fkg`
Lake environment, checks its toolchain against this sidecar's
`lean-toolchain`, compiles with `-DwarningAsError=true`, and checks the printed
axiom reports for `sorryAx` or compile errors.

From the repository root:

```bash
bash examples/routeb_p4_execution_residual_lean/verify.sh
```

A focused compile establishes only a `compiled_candidate` for the abstract
algebra. Independent validation belongs to `封不觉`; harvesting and final
integration belong to `梁智炜（Codex）`.
