# B45-2 targeted receipt

Status: **PASS — isolated exact-real / conditional-Float64 seam compiled**

Date: 2026-09-06 UTC

## Scope

- six-dimensional `q : Fin 6 -> R` and `dq : Fin 6 -> R`;
- exact centered samples `q + h e_k`, `q - h e_k` with `h = 1/100000`;
- explicit regularized-mass seam with `mu = 1/1000000`;
- potential-value enclosure and centered-FD gradient enclosure;
- explicit finite-normal binary64 interface with `u = 2^-53`, including the
  two-sample potential-to-gradient bridge;
- optional interpreted step `hhat`, with a separate step-rounding term;
- derivative-tensor enclosure for the final `C*dq` contraction;
- exact-FD plus runtime `C*dq/G` defect budget, with the cross term retained
  before division by `2*D`.

Machine evaluation, deployed DH/source equality, Float64 trigonometry,
parameter conversion, solver residual, and trajectory semantics remain
conditional premises or open obligations.  No deployed-source comparator is
imported or redefined here.

## Compile evidence

Command:

```text
lean -DwarningAsError=true --root=examples/routeb_b45_2_float64_seam_lean \
  -o output/run-PP41eMJr/Float64Seam.olean Float64Seam.lean
```

Pinned environment:

- Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`;
- output: `output/run-PP41eMJr/`;
- axiom reports: 14;
- unexpected proof axioms: none;
- `sorryAx`: absent.

Input SHA-256:

```text
110b03541f571fadb38d878c6642996857bf1d0933724ae73fb8e25f2d5b4bd7  Float64Seam.lean
3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71  lean-toolchain
6c4cf41f76be0f7a25f18dcc6fe30cc4f1a55aedb85a19bf1848af74b3b9256f  verify.sh
```

Output SHA-256:

```text
7b3cdcb041bd84f007e01d3bbb796d68c5fe5e5c47e8a811cb74851ea4d7ddcb  output/run-PP41eMJr/Float64Seam.olean
60ef3ac567484801863e7f3c45219b0f73a61546188e3618324764bfccb9bafd  output/run-PP41eMJr/compile.log
```

The targeted run did not invoke the main workflow, modify state or registry,
or run the full regression suite.
