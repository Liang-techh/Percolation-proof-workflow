# Fixed identity multiplier for RouteB revision 46

Scope: only this directory. Reuse the frozen SignedGap/ResidualMultiplier
modules from `../routeb_signed_gap_lean/output/run-iH9FGdAL`. All delivered
theorems passed Lean 4.33.1 with warningAsError=true in
`output/run-76aeLbcO` (2026-09-05T21:01:25Z). Source hashes match the
successful pre-compilation snapshot; all printed axiom dependencies are
only propext, Classical.choice, Quot.sound. See `FINAL_RECEIPT.md`.

For symmetric M,L, choose Z=I and D=2M-L. The source-bound premise
M(q)>=L is explicit, in finite-quadratic-form order. It implies D>=L
at every state where that source premise holds; no epsilon, closeness
condition, or extra bottom-block positivity test is needed.

The exact correction satisfies M delta=r. Choose z satisfying
M z=g-r+L delta. The target finite-vector identity is

    H = [b-d-2z'r, -(g+r-Mz)'; -(g+r-Mz), 2M-L],
    quad H (s,v) = (b-d-2g'delta-delta'Ldelta)*s^2
                   + quad D (v-s*delta).

For D>=0 this is equivalent to H>=0 iff the signed margin is nonnegative.
The constructive formula is z=M^-1 g-delta+M^-1 L delta.
`CONSTRUCTIVELOSSLESS` implements that formula with an explicit right
inverse R of the actual M. `psd_iff_margin` and `affine7x7_lossless` need
only the two displayed vector equations, with no inverse premise.
No theorem takes the congruence identity as a hypothesis.

`finite_quadratic_coercivity` transfers c*dot(x,x)<=quad L x to D with
the same c. Choose c>0 for quantitative coercivity; `D_positive` transfers
strict positivity for every nonzero finite vector directly. A globally
source-bound M(q)>=L yields the bound at every q via `global_coercivity`.

The main task owns the frozen rational ansatz audit:

    R=M0^-1, delta_hat=Rr, z=Rg+(RLR-R)r.

This z is exact at M=M0. Away from M0, neither M delta_hat=r nor
M z=g-r+L delta is inferred. The exact finite-vector theorem does not
prove a frozen rational certificate, physical source binding, uniform
storage feasibility, the full-horizon budget, or J<=1.

## Centered noncontractive source gate

For any center h (which need not solve M h=r), define

    ec = g+r-Mz-Dh,
    mhat = margin(L,g,h,b,d)+2(z+h)'(Mh-r).

`affine_center_identity` derives from finite sums, using symmetric M,L,

    quad H(s,v) = quad K(s,v-sh),   K=[mhat,-ec';-ec,D].

With dM=M0-M and the two frozen equations M0h=r, M0z=g+Lh-r,
`frozen_center_error` and `frozen_center_margin` give exactly

    ec = dM(2h+z),
    mhat = b-d-2g'h-h'Lh-2(z+h)'dM h.

`centered_dual_sos` proves the finite completion for A=D:

    quad K(s,y) = quad(D-L)y + quad L(y-sQec)
                  + s^2*(mhat-ec'Qec).

It needs symmetry of L and L(Qec)=ec; a genuine Q=L^-1 supplies this
equation. `affine_centered_dual_bound` combines this identity with the
derived recentering and D>=L to certify the entire actual affine matrix
from mhat>=ec'Qec. It has NO inverse premise on M, no contraction parameter,
no epsilon, and no assumption that the frozen center is the actual delta.
The actual source mass order and nonnegativity of L remain explicit.
`frozen_affine_dual_bound` exposes the final scalar condition directly in
dM,h,z and composes both frozen equations with the complete affine gate.
The main task owns source coefficient binding and the rational ansatz audit.

Reproduce from the workspace root:

    wsl -d Ubuntu -- bash examples/routeb_universal_multiplier_lean/verify.sh

Every attempt first snapshots all new Lean sources, this document, the
runner, revision context, and the frozen upstream run, then hashes them
before compilation. Only the new module is compiled. Pinned Lean 4.33.1,
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474, cached dependencies only;
no Lake build/download, registry/state mutation, or broad tests.
