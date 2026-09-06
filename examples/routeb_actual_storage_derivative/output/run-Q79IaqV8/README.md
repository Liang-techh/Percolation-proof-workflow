# Actual storage derivative composition

Owned scope: only this new directory. The completed universal multiplier leaf
and the actual-energy positivity leaf are read-only dependencies. No state,
registry, archive, numerical runs, dependency builds, or broad tests.

Verification is pending. The runner imports successful frozen ActualStorage
run-ZWEIdfZ8 (completed 2026-09-05T21:11:05Z), checks its receipt and olean
hashes, and checks its sources match the current positivity leaf. It uses
pinned Lean 4.33.1, cached Mathlib, warningAsError=true, prospective snapshots,
full compiler output and exit codes. All failed attempts are retained.

Reproduce from the workspace root:

    wsl -d Ubuntu -- bash examples/routeb_actual_storage_derivative/verify.sh

The proof imports the ACTUAL W0 and storageV definitions, fixed rational M0/H0,
and the literal M0_symmetric/H0_symmetric proofs from ReferenceMass. K,D,G
remain explicit source parameters. Physical q4 is Lean q 3.

With S=K+H0, qdot=v, vdot=a0+delta, M0 a0=-S q-Dv+G w, the result is

    W0dot = -v'Sq-v'Dv+v'G w+(14/75)q4v4+v'eta.

delta_cancellation expands actual finite sums to cancel v'M0 delta from the
nominal kinetic derivative and the signed-gap derivative. The modular theorem
accepts the previous signed-gap derivative. The full source theorem DERIVES it
using the cached hasDerivAt_signedGap_from_source: finite kinetic power and
Christoffel cancellation, mass/potential chain rules, actual force balance,
and the same-state nominal balance. No final W0 derivative is a hypothesis.

SourceAt lists the kinematics, source derivatives DM/DU, tensor and gradient
bindings, actual mass symmetry, actual force equation (with eta once), and
the explicit nominal equation. It contains no gap or storage derivative field.
The fixed reference symmetry is reused, not assumed for an arbitrary M0.

For V=f W0+sum pi qi^2+h c^2, the product and finite-sum derivative is

    Vdot = f' W0+f W0dot+sum(pi' qi^2+2 pi qi vi)+h' c^2,

assuming c'=0. This applies to the imported storageV itself. The theorem
hasDerivAt_storageV_from_source composes the source proof of W0dot directly.
Both rates contain no explicit delta channel. Eta and its signed work remain.

Exact external K,D,G coefficients and physical meanings of M,U, source
derivatives, forces/eta, and trajectories remain source premises. No defect
bound, coefficient feasibility, dissipation inequality, integration, or
full-horizon J<=1 is inferred. The main task handles state and archiving.
