# Signed energy-gap derivative and affine residual multiplier

Scope: only this new directory is owned. Revision45 of
`artifacts/routeb_6dof/state.json`, the prefix checkpoint report, and
`examples/routeb_J_strategy/SIGNED_WORK.md` were read and snapshotted.
No registry/state writes, broad tests, dependency builds/downloads, numerical
certificate synthesis, or external-project edits were performed.

## Mathematical result

All vectors are real finite functions and all matrix products and quadratic
forms are actual finite sums. The dimension is generic; take n=6 for the
physical variables and m=14 for the augmented state.

`SignedGap.lean` defines

    Sgap(t) = (1/2) v(t)' M0 v(t) - (1/2) v(t)' M(t) v(t)
              - (U(t) - Uzero - (1/2) q(t)' H0 q(t)).

`hasDerivAt_bilinear` differentiates the finite double sum by product and sum
rules. `hasDerivAt_kinetic` combines its two velocity terms using symmetry.
`hasDerivAt_signedGap` proves the real derivative

    HasDerivAt Sgap (v' M0 (a-a0) - v' eta) t.

Here the prime on v in displayed linear algebra denotes transpose, not a
time derivative. The proof uses qdot=v, vdot=a, the derivative of each mass
entry, the actual potential derivative, actual force balance, and nominal
acceleration at the same state with the same drive. The Coriolis force is
the explicit Christoffel tensor contraction. Its exact power identity is
imported from the cached `ChristoffelPower` proof, not hypothesized. No
scalar kinetic-power equality or gap-derivative equality is assumed.

`hasDerivAt_signedGap_from_source` further obtains both mass and potential
time derivatives from `HasFDerivAt` source-space premises by chain rules.
Its tensor is explicitly bound to the derivative of the same M(q) used in
force balance. `implemented_actual_balance` reuses `DHPowerBinding`'s
finite-precision/FD/solve defect definition. `same_state_residual` reuses
`CoupledResolvent` and gives M delta = r with eta already included once.

Sgap, its potential remainder, and the eventual storage remain signed.
Uzero may be set to U(0); its value has no effect on the derivative.

## Affine 7x7 certificate

`ResidualMultiplier.lean` defines the actual (n+1)-square finite matrix

    A = [ b-d-2 z'r,           -(g+Z'r-Mz)' ;
          -(g+Z'r-Mz),          Z'M+MZ-L   ].

For symmetric M, `affine_quadratic_expansion` proves

    (1,delta)' A (1,delta)
      = b-(d+2g'delta)-delta'Ldelta
        +2(z+Z delta)'(M delta-r).

`affine_residual_cancellation` proves the last term vanishes from the
component equations M delta=r. `affine_dissipation_fin6` then yields

    delta'Ldelta + (d+2g'delta) <= b

from an explicit premise `forall x : Fin 7 -> Real, 0 <= quad A x`.
`affine_dissipation_of_test_vector` needs only nonnegativity at (1,delta).
`homogeneous_matrix` specializes z=0 to the original S6. Neither inverse
existence nor positive storage is needed for these implications. The
nonnegativity predicate is literally quadratic-form nonnegativity; no
unproved built-in PSD conversion is hidden. Symmetry of L, if desired for
the standard symmetric-PSD formulation or energy interpretation, is a
separate source/certificate property, not needed for the cancellation.

The main task reports a source-bound affine coefficient audit at
`../routeb_affine_multiplier/output/run-20260905T202634Z-e39dc9a3`.
Its local-jet witness distinguishes affine from homogeneous multipliers.
This leaf neither reruns that audit nor claims a global storage from it;
constructive inverse/congruence equivalence remains with the main task.
The Lean implication above is independent of that numerical/symbolic audit.

## Storage and integrated interfaces

`IntegratedBudget.lean` proves actual FTC interval-integral versions of
the signed-work identity and its differentiable scalar-weighted version.
`hasDerivAt_signed_storage` differentiates Y'P(t)Y+k(t)S(t).
`hasDerivAt_augmented_storage` uses Ydot=F+B delta and derives its S5 form,
with F=A14 Y as the intended specialization:

    d = Y'Pd Y + 2 Y'P F + kdot S - k v'eta,
    g = B'P Y + (k/2) M0 v,
    Vdot = d + 2 g'delta.

`augmented_affine_dissipation` composes that derivative with the affine
matrix condition to bound delta'Ldelta + deriv V t. The hS premise at
this modular assembly point is supplied by the signedGap derivative
theorems, not an independent scalar energy assumption.

`integrated_dissipation` uses interval-integral monotonicity and the FTC
to derive integral ell + V(t)-V(0) <= integral supply.
`PrefixCertificate` exposes continuity, interior derivatives,
integrability, pointwise dissipation, and a lower storage bound at the
particular stopping endpoint. `prefix_budget` combines those with the
initial upper bound and supply budget. `signed_budget_prefix_bootstrap`
reuses the cached compact first-hit theorem: certificate data need hold
only on prefixes strictly below cap, with a uniform margin < cap.
Terminal-only storage bounds do not satisfy that interface.

## Concrete unmet physical premises

1. Bind the actual DH mass field and potential to the real functions in
   `hasDerivAt_signedGap_from_source`, including source derivatives DM, DU,
   the tensor convention, and symmetry of M, M0, H0. The generic theorem
   does not certify CSV coefficients, DH source extraction, or that M0/H0
   equal the intended nominal mass/potential Hessian.
2. Provide a real trajectory with the stated kinematics and actual force
   balance. Bind a0 to the full nominal acceleration evaluated at the
   current q,v, with the identical controller/disturbance drive. A nominal
   reference trajectory in place of that same-state acceleration is not
   sufficient.
3. Bind eta to all chosen source, controller/parameter, FD, Float64, and
   solve defects with the displayed sign. The imported identity is exact
   algebra for real-valued inputs; it does not certify a floating solver,
   supply eta bounds, or justify setting eta=0. The same eta appears once
   in r, and contributes -k v'eta in d. Regularity/integrability of eta and
   its work terms is still open for the intended implementation.
4. The main derivative statements are all-point `HasDerivAt` results.
   The FTC inequality variant needs derivatives at every interior point,
   continuity at endpoints, and integrability. This is stronger than an
   almost-everywhere or sampled numerical-trajectory statement. An
   absolutely-continuous/AE adapter, treatment of step changes/solver
   interpolation, and the real trajectory semantics are not proved here.
5. Instantiate P,k,B,A14 and their derivatives, and certify the affine
   matrix quadratic form on every required state/source cell. The main
   task's pointwise jet witness supplies no global differentiable P,k.
   No multiplier or numerical certificate has been synthesized here.
6. Establish the original full12 initial-ball and ramp-family upper
   storage bound, a lower storage bound at every possible prefix endpoint,
   and the uniform strict supply budget. Also establish coverage, the
   continuity of the integral cost used in the bootstrap, existence and
   continuation up to the requested horizon. The bootstrap acts on a
   supplied interval; it is not an ODE existence theorem.

Consequently actual-DH J<=1, the original full-horizon outputs, global
storage feasibility, and registry admission remain unproved by this leaf.

## Reproduction and evidence

From the workspace root in PowerShell:

    wsl -d Ubuntu -- bash examples/routeb_signed_gap_lean/verify.sh

Only the three new Lean modules are compiled, with warningAsError=true.
The executable is the pinned WSL Lean 4.33.1; Mathlib commit is checked as
`0df444a360eaa60ab8c11dca51a86af692955474`. Mathlib and package dependencies
are read from `/home/z5242/sos_lean/.lake/packages`; local leaf oleans are
copied from existing caches. The script invokes no Lake build or download.

Each attempt has a new `output/run-*` directory with pre-run source/report
snapshots, copied cached oleans, SHA256 manifest, complete compiler stdout
and stderr, actual commands, and exit codes in `terminal.log`. Failed
attempts are retained, including their failed proof axiom reports; those
are not verification receipts. See `ATTEMPT_HISTORY.md` for outcomes and
the final source-to-olean receipt.
