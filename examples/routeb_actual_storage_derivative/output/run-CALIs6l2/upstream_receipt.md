# Revision47 handoff receipt

Status: concrete storage shape, exact M0 upper bound, initial bounds and
polynomial-family nonnegativity/terminal theorems compiled successfully.

Final run: `output/run-ZWEIdfZ8/terminal.log`, ended 2026-09-05T21:11:05Z.
ActualStorage compile exit 0; verifier exit 0; pre-run snapshot hashes unchanged.
ReferenceMass was reused from its successful exit-0 compilation in
`output/run-EQMuJx15/terminal.log`, with source equality checked before reuse.
Both use Lean 4.33.1, warningAsError=true, cached Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`. No new dependency builds or downloads.

Every printed final theorem dependency is a subset of
`{propext, Classical.choice, Quot.sound}`. No sorry/admit/custom axiom occurs
in either current Lean source. All six actual attempts remain on disk.

ReferenceMass source SHA256:
`b77e00ab3cf236edc143fa963aba362a8279f2ca6caecaf5277726fac0c91607`

ReferenceMass olean SHA256 (also the final run's copied cache):
`9e84474ff4d5aa440e9dcf1054e0f22b645fa6e645f42cd351e58e9057e70d43`

ActualStorage olean SHA256:
`7b3f8836286e56b7b306faf5bca26338752a16b1c271a2b6eb51a524bd05ae97`

ActualStorage source SHA256:
`c20c900ca09039dc7c37c247d071c058a58dd7ca419a4865f2c1f7f29f6a01aa`

The final run's `before_run.sha256` records both exact source hashes and all
pre-run inputs; current source hashes were independently compared with the
final source snapshots after compilation.

## Main-agent entry points

- `M0_le_identity`: actual finite v'M0v <= sum vi^2, from rational DSOS.
- `W0_source_energy`: exact signed-gap to actual-energy/remainder identity,
  with H, U and Uzero bindings explicit.
- `W0_nonneg`: actual mass quadratic-form PSD plus q4^2<=56/15 and source bindings.
- `W0_initial_upper`: full12 ball plus explicit Sgap>=-3/10000 implies
  W0<=231/20000.
- `storageV_initial_upper`: V<=9 beta/400+3f/10000+3h under the stated beta bounds.
- `synthesisV_nonneg_on_P`, `synthesisV_terminal`, `synthesisV_initial_upper`:
  concrete nonnegative-coefficient powers (1-t)^j, j>=1; suitable for Pauli's
  LP coefficient selection. No LP candidate is assumed or synthesized here.

Exact absolute row sums (all strictly below 1):
`1887427/2000000, 11224907/12000000, 7144697/12000000,
250001/1000000, 615649/4000000, 50001/1000000`.
The final source audit matches all 36 M0 and H0 Lean entries to the coupled
reference and reconstructs them from the snapshotted rational CSVs.

## Not discharged

External physical/DH/implemented source identification; actual M(q) PSD and
physical domain coverage; initial full12 ball and c^2<=3; the entire-ball
Sgap>=-3/10000 rational audit premise; eta identification/bounds/work;
kinematics, source differentiability, nominal/actual force balance and trajectory
semantics needed for derivative composition. The new-family derivative and
exact g=0 composition are assigned to the separate agent owning
`examples/routeb_actual_storage_derivative/`; this leaf adds no derivative files.
No dissipation, integration,
existence/continuation, coefficient feasibility or physical J<=1 claim follows
without that additional work. See README for the detailed boundary.

Only this owned directory was written. No registry/state writes or full regression.
