# T-P5-067 multiple-root cluster Lean sidecar

This sidecar formalizes the source-independent arithmetic core of 狂蛮魔尊's `T-P5-067-MULTIPLE-ROOT-CLUSTER` review.

Trusted scope:

- division-free pointwise root estimate `m * |z|^k <= eps`;
- strict radical-free cluster gate `eps < m * delta^k -> |z| < delta`;
- signed right-wing reserve;
- even/odd left-wing reserve split;
- equality boundary is not a strict nonvanishing reserve;
- exact double-contact annihilation/splitting regressions;
- lower-order perturbation factorization and linear unfolding regression.

Deliberately **not** formalized here:

- IVT-based existence inside the unresolved middle cluster;
- uniqueness or preserved multiplicity for `k >= 2`;
- root discovery/isolation algorithms;
- deployed P5 coefficient/source binding;
- Float64/FD/controller semantics;
- P8 same-domain ODE coverage;
- registry admission or P5/P8/M4 final closure.

The sidecar uses the repository-pinned `examples/local_fkg` Lake environment. `verify.sh` resolves `lake` and `lean` from `PATH`, checks the pinned toolchain, rejects `sorry`/`admit`, runs `-DwarningAsError=true`, and audits `#print axioms` output.

Status after a clean focused compile is only `compiled_candidate`; it remains **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.
