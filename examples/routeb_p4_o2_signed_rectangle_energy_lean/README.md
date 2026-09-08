# Route-B P4 O2 signed-rectangle energy consumer — Lean sidecar

Agent/source_agent: 巨阳仙尊

This portable sidecar formalizes the source-independent exact-real consumer from `T-P4-034` / 红莲魔尊's O2 residual-energy review.  It deliberately starts **after** the numerical/source lane has produced a certified signed enclosure of the final evaluator error in the same force/residual coordinates paired by the energy inequality.

## Trusted theorem seam

`O2SignedRectangleEnergyConsumer.lean` proves:

- division-free SOS identities for the retained positive-definite two-channel quadratic and its adjugate dual;
- the exact retained-dissipation completion;
- a generic convex-quadratic endpoint lemma;
- `dual_quadratic_rectangle_le_corners`: four signed rectangle corners bound the whole dual quadratic;
- `o2_signed_rectangle_energy_consumer`: four exact corner obligations imply the additive Lyapunov charge while retaining fraction `1-theta` of the quadratic dissipation;
- `o2_signed_rectangle_first_exit_with_reserve`: a typed first-exit consumer once an explicit additive reserve `kappa < c*Vstar-beta` exists;
- global port/gain sign transport invariance of the final quadratic charge;
- an exact small-scale absolute-bias obstruction showing why a nonzero state-independent evaluator rectangle cannot by itself imply homogeneous decay through the origin.

The file also declares distinct `AccelerationError2` and `ForceResidualError2` wrappers.  There is intentionally no coercion between them: the O2 source lane must prove the same-box mass/residual bridge before a solve/acceleration error may be consumed as a force residual error.

## Intentionally open

This sidecar does **not** prove deployed `dhport_lib.jl` Float64/libm/central-FD/regularizer/solve semantics, final residual interval export, source/hash/orientation binding, coverage, singular-rank compatibility, P8 same-domain coverage, registry admission, or P4/M4 final closure.  It also does not claim that raw primitive error boxes are already final force-residual boxes.

## Portable verification

Run from a checkout whose `examples/local_fkg` pinned Lake environment has already been bootstrapped:

```bash
bash examples/routeb_p4_o2_signed_rectangle_energy_lean/verify.sh
```

`verify.sh` resolves `lake` and `lean` from `PATH`, checks the pinned `lean-toolchain` against `examples/local_fkg`, compiles with `-DwarningAsError=true`, rejects `sorry`/`admit`, and audits all public theorem `#print axioms` reports for `sorryAx`.

Status after implementation remains only `compiled_candidate` when CI passes: 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
