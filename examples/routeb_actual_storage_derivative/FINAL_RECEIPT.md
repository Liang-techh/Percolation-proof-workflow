# Actual storage derivative: final receipt

PASS: output/run-UX1mucoR/terminal.log, 2026-09-05T21:17:48Z to 21:18:58Z.
ActualStorageDerivative_COMPILE_EXIT_CODE=0; VERIFY_EXIT_CODE=0.
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6;
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474; warningAsError=true.
One new module compiled, cached imports only. Pre-run manifest unchanged;
delivered source matches the successful snapshot. All four attempts retained.
All six printed axiom reports use only propext, Classical.choice, Quot.sound.
No sorry, admit, or custom axiom occurs in the delivered Lean source.

| Successful run file | SHA256 |
| --- | --- |
| ActualStorageDerivative.lean | 9f5f7019214f30960072c336f9aafd098d1747a05ed3d282f223744eb3e8fcbc |
| ActualStorageDerivative.olean | c566b7d4d3e1e57236276e90cf309bd4e72409fc30f545377c7cc6ad1c95ec18 |
| terminal.log | 7c715021ed8e23ad7cbf245ae05d1ad9a80750b8cd52597f360e4d325d617800 |
| before_run.sha256 | 317b955851d06c4d652fda8c418cc0260af0321e8e9b8a3911f1a2bf460ad8c3 |

Imports: ActualStorage final run-ZWEIdfZ8, including its successful cached
ReferenceMass and SignedGap run-iH9FGdAL. The runner checks successful receipts,
published olean hashes and current upstream source equality before compilation.
The complete upstream snapshot is frozen under each attempt's upstream/.

Namespace RouteBActualStorageDerivative; main entry points:

- hasDerivAt_W0_from_source: real derivative of the imported W0 using literal
  M0/H0 symmetry, cached signed-gap source/kinetic proofs, and explicit finite
  delta_cancellation. It proves W0dot=-v'(K+H0)q-v'Dv+v'G w+14q4v4/75+v'eta.
- hasDerivAt_position_sum: actual six-term derivative sum(pi' qi^2+2pi qi vi).
- hasDerivAt_storageV_from_source: real derivative of imported storageV,
  f'W0+f W0dot+sum(pi' qi^2+2pi qi vi)+h'c^2, with c'=0. It invokes the
  W0 source theorem; neither final derivative identity is assumed.

SourceAt explicitly retains kinematics, source mass/potential derivatives,
tensor/gradient bindings, actual mass symmetry, actual force balance and
M0a0=-(K+H0)q-Dv+G w. Exact external K,D,G coefficients and physical eta/source
bindings remain premises. The rates have no explicit delta term; eta work
remains. This closes derivative composition, not coefficient feasibility,
dissipation, integration or J<=1. Only this new directory was written;
no other leaf changes, state/registry writes, archives, or broad tests.
