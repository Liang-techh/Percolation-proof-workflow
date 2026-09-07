# Route-B P4 transverse Schur reserve sidecar

This focused Lean sidecar formalizes the positive part of `T-P4-014` from 狂蛮魔尊.

It contains four layers:

1. `decomposed_residual_abs_bound`: `r = c*y + e + b` with `|e| <= beta|y|` and `|b| <= gamma|z|` gives the mixed envelope `(c+beta)|y| + gamma|z|`.
2. `transverse_gap_identity` and `transverse_square_budget`: the division-free identity behind the sharp reserve condition `d*gamma^2 <= (p*d-a^2)*h`.
3. `schur_from_square_budget` and `relative_plus_transverse_schur`: completion of the square in the Schur variable without division or square roots in the hypotheses.
4. Exact block-4 arithmetic for `p4=3/5`, `d4=116667666666667/10^15`, `c=1/100`, `beta=6/25`, including the integer checker condition
   `583338333333335*gamma^2 <= 37503000000001*h`.

Run from a repository checkout with the pinned `examples/local_fkg` Lake environment available:

```bash
CI_PORTABLE=1 bash examples/routeb_p4_transverse_schur_reserve_lean/verify.sh
```

The sidecar deliberately does not bind `DeltaM`, `DeltaC`, `DeltaG`, controller rounding, or solve defects to a specific transverse coordinate. It also does not mutate P4/M4 admission or registry state. The explicit sharpness extremizer from the mathematical review remains a separate optional theorem.

Status after compilation should be reported only as a compiled candidate, pending 封不觉 independent verification and 梁智炜 final integration.