# Fixed identity multiplier for RouteB revision 46

Scope: only this directory. Reuse the frozen SignedGap/ResidualMultiplier
modules from `../routeb_signed_gap_lean/output/run-iH9FGdAL`. Verification
is pending until a successful compiler receipt is recorded.

For symmetric M,L, choose Z=I and D=2M-L. The source-bound premise
M(q)>=L is explicit, in finite-quadratic-form order. It implies D>=L
at every state where that source premise holds; no epsilon, closeness
condition, or extra bottom-block positivity test is needed.

The exact correction satisfies M delta=r. Choose z satisfying
M z=g-r+L delta. The target finite-vector identity is

    quad H (s,v) = (b-d-2g'delta-delta'Ldelta)*s^2
                   + quad D (v-s*delta).

For D>=0 this is equivalent to H>=0 iff the signed margin is nonnegative.
The constructive formula is z=M^-1 g-delta+M^-1 L delta.

The main task owns the frozen rational ansatz audit:

    R=M0^-1, delta_hat=Rr, z=Rg+(RLR-R)r.

This z is exact at M=M0. Away from M0, neither M delta_hat=r nor
M z=g-r+L delta is inferred. The exact finite-vector theorem does not
prove a frozen rational certificate, physical source binding, uniform
storage feasibility, the full-horizon budget, or J<=1.

Reproduce from the workspace root:

    wsl -d Ubuntu -- bash examples/routeb_universal_multiplier_lean/verify.sh

Every attempt first snapshots all new Lean sources, this document, the
runner, revision context, and the frozen upstream run, then hashes them
before compilation. Only the new module is compiled. Pinned Lean 4.33.1,
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474, cached dependencies only;
no Lake build/download, registry/state mutation, or broad tests.
