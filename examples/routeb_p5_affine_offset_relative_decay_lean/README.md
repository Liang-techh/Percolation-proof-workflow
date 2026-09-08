# T-P5-073 affine-offset relative-decay Lean sidecar

This focused sidecar formalizes the source-independent arithmetic core extracted from 狂蛮魔尊's `T-P5-073-AFFINE-OFFSET-RELATIVE-DECAY` mathematics.

Trusted leaves:

- pure componentwise relative control forces exact zero-slice vanishing;
- exact `R=b+v*q` plus absolute bounds yields the affine envelope;
- a certified gap `delta <= |v|` absorbs additive bias by the division-free target-factor gate `beta <= (q-kappa)*delta`;
- the strict special case `beta < (1-kappa)*delta` yields `|R|<|v|`;
- finite nonnegative matrix envelopes close a strict bootstrap box under `beta_i + sum_j A_ij r_j < r_i`;
- strict budget is equivalent to positive division-free reserve, while equality has zero strict reserve;
- regressions distinguish a true transverse zero-slice obstruction from a merely positive coarse additive allowance.

Deliberately open: source/CSE polynomial divisibility, MVT/derivative infrastructure, deployed forceError/FD coefficients, Float64/controller semantics, P8 same-domain coverage, provenance/receipt/admission/re-audit, registry mutation, and P5/P8/M4 final integration.

Run with `CI_PORTABLE=1 bash verify.sh` from any working directory with `lake` and `lean` on `PATH`. The verifier consumes the pinned `examples/local_fkg` Lake environment and checks the sidecar toolchain against it.

Status after a green focused compile remains `compiled_candidate` only: 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
