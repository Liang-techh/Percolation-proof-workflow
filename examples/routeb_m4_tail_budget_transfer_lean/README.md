# T-M4-007 — pure M4/P7 tail-budget transfer

This sidecar formalizes the elementary exact-real budget implications extracted
from `review-T-M4-006-daai-xianzun-20260906T2346.md`.

It proves:

- `tail_budget_transfer`: any `Dtail <= rhoBar/160000` may replace the coarse
  tail allowance if `Dbase + rhoBar/160000 <= 1401/625`;
- `old_gate_plus_rho16_exact`: the exact identity
  `4483/2000 + 16/160000 = 1401/625`;
- `old_gate_plus_tail_of_rho_le_16`: the old-gate corollary;
- `tail_budget_from_slack`: a reusable generic slack form.

Evidence boundary: this is pure arithmetic. It does **not** prove the ramp
integral, a physical `rhoBar`, P7 source binding, P8 existence/coverage, terminal
`L/g` premises, M4 admission, or registry promotion.

Run `./verify.sh` in a checkout with the repository's pinned
`examples/local_fkg` Lake environment available. The verifier locates `lake`
from `PATH`, checks the local toolchain pin, and is registered for the shared
portable GitHub Actions workflow through `CI_PORTABLE=1`.

Even after a successful compile/axiom check, status remains: **待封不觉独立验证 /
待梁智炜最终整合**.
