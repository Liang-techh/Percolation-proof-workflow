# Route-B P5 weighted dual residual sidecar

Task: `T-P5-007`
Agent: `臭屁猪`

This sidecar formalizes the source-independent damping-weighted implication

```text
dualSq(r) <= kappa^2 * dampedSq(v)
```

into retained dissipation, together with the exact `kappa = 0` boundary and a
generic additive-force-error counterexample. It does **not** bind deployed DH,
FD, solve, source hashes, domain coverage, or P5/M4 admission.

Portable verification:

```bash
bash examples/routeb_p5_weighted_dual_residual_lean/verify.sh
```

The verifier is registered with `.github/workflows/lean-agent-sidecars.yml`
through `CI_PORTABLE=1` and uses the repository-pinned Lean 4.32.0 local-FKG
Lake environment.

A successful compile remains `待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合`.
