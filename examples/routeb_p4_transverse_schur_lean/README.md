# T-P4-014 transverse Schur Lean sidecar

This portable sidecar formalizes the inequality core from `agent_review_inbox/review-T-P4-014-kuangmanmozun-20260907T0247.md`.

It contains: (1) the same-coordinate plus transverse residual absolute-value composition; (2) the division-free exact Schur reserve identity and square budget; (3) the final P4 nonnegative quadratic consumer; (4) the additive-bias-with-explicit-slack specialization; (5) a division-free polynomial witness showing failure when the transverse reserve budget is violated; and (6) the exact block-4 rational corollary `583338333333335*gamma^2 <= 37503000000001*h`.

The sidecar is pinned to Lean 4.32.0 and reuses `examples/local_fkg/`, including its pinned `lake-manifest.json`. `verify.sh` locates `lake` from `PATH`, checks toolchain and manifest presence, compiles with `-DwarningAsError=true`, and rejects `sorryAx`/compile errors from the focused log. It is marked `CI_PORTABLE=1` for `.github/workflows/lean-agent-sidecars.yml`.

It deliberately does **not** bind `DeltaM/DeltaC/DeltaG/delta_ctrl/solveDefect` to a transverse coordinate, identify an actual positive `h*z^2` reserve in the deployed certificate, prove Float64/IEEE bounds, or modify P4/M4/registry status.

Run from the repository root with:

```bash
bash examples/routeb_p4_transverse_schur_lean/verify.sh
```

Admission remains pending: 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
