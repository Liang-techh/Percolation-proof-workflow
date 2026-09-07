# T-P4-036.2 robust phase cells Lean sidecar

Formalization owner/source agent: **巨阳仙尊**.

This portable sidecar consumes the mathematical review
`agent_review_inbox/review-T-P4-036.2-guyuefangyuan-robust-phase-cells-20260907T1434.md` and formalizes only the source-independent exact-real layer:

- `base_trig_cell_of_abs_le`: from `|r| ≤ b`, derive `sin r ∈ [-b,b]` and `cos r ∈ [1-b²/2,1]`;
- `formed_angle_error_to_reduced_radius`: transport an upstream absolute formed-angle error into a reduced-radius bound without a `piBox` premise;
- `phase_neg_quarter_cell`, `phase_zero_cell`, `phase_pos_quarter_cell`, and `quarter_phase_cell`: exact `-π/2,0,+π/2` transport;
- `phaseTheta` and `phaseAlpha`: the finite six-link source phase tables;
- `theta_all6_exact_cells_from_qbox` and `alpha_all6_exact_cells`: all 12 exact-real source rows from the q-box/phase table;
- `robust_phase_cell_of_formed_angle_error` plus theta/alpha specializations: a clean seam consuming an already-decoded real formed angle and a certified absolute formation error.

The theorem boundary deliberately excludes Float64 argument-formation semantics, Julia/libm output inclusion, non-finite/overflow behavior, D1/D2/D3 outward propagation, source execution equality, P8/domain coverage, provenance/admission, and Route-B closure.

## Portable verification

The sidecar pins Lean with `lean-toolchain` and reuses the repository's pinned `examples/local_fkg` Lake/Mathlib environment. `verify.sh` resolves `lake`/`lean` from `PATH`, checks the pinned Mathlib revision, compiles with `-DwarningAsError=true`, requires an axiom report for every public theorem, and fails on `sorryAx`.

```bash
bash examples/routeb_p4_robust_phase_cells_lean/verify.sh
```

The script carries `CI_PORTABLE=1`, so `.github/workflows/lean-agent-sidecars.yml` executes it on GitHub-hosted CI.

Status after implementation remains a **compiled candidate only if CI passes**: 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
