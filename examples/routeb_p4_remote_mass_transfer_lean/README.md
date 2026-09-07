# Route-B P4 remote mass-metric transfer Lean sidecar

This sidecar formalizes only the source-independent theorem decomposition from
`agent_review_inbox/review-T-P4-012-youhunmozun-20260907T0130.md`.

It contains four layers:

1. `remote_scaled_cross_bound_division_free`: the scaled block-PSD cross-term
   inequality, stated without matrix inverses or division;
2. `remote_schur_absorption`: a direct consumer showing that a local positive
   quadratic plus one distal-energy budget absorbs the remote cross term;
3. `remote_component_reserve`: a square-to-absolute-value adapter for a single
   force component; and
4. exact rational channel-4/channel-5 constants for the corrected
   force-coordinate `kc` bookkeeping:
   `U4=280441/2400000`, `U5=40147/800000`,
   `gamma4=138240/280441`, `gamma5=48020/40147`.

The sidecar deliberately does **not** prove that deployed Julia/Float64 mass
matrices satisfy the abstract PSD premise, does not bind `M_BD a_D` to the
source execution, does not prove a P8 bound on distal acceleration energy, and
does not close the remaining P4 residual channels or M4.

## Focused verification

The repository workflow `.github/workflows/lean-agent-sidecars.yml` runs this
artifact because `verify.sh` contains `CI_PORTABLE=1`. The script resolves
`lake` from `PATH`, reuses the pinned sibling `examples/local_fkg` Lake
environment, checks that its toolchain matches this directory's
`lean-toolchain`, compiles with `-DwarningAsError=true`, and checks all printed
axiom reports for `sorryAx` or unexpected compile errors.

From the repository root:

```bash
bash examples/routeb_p4_remote_mass_transfer_lean/verify.sh
```

A successful focused run establishes only a Lean `compiled_candidate` for the
abstract mathematics. Independent validation belongs to `封不觉`; harvesting
and final integration belong to `梁智炜（Codex）`.
