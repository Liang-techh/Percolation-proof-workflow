# Final compilation receipt

Successful run: `output/run-iH9FGdAL`.
Complete terminal log: `output/run-iH9FGdAL/terminal.log`.
Start/end UTC: 2026-09-05T20:36:09Z / 2026-09-05T20:37:50Z.
All module compile exit codes and VERIFY_EXIT_CODE: 0.
Options: `-DwarningAsError=true`, explicit run root and olean outputs.
Lean: 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6.
Mathlib: 0df444a360eaa60ab8c11dca51a86af692955474, cached dependencies only.

| Module | Source SHA256 | Olean SHA256 |
| --- | --- | --- |
| SignedGap | d4b9bcb69d69502527e48252eb54102a4acc4e83cff4a1412438cf1240d0b061 | 498aed10c67f6988066d16fa510bcfde461be3be0b6cb546ed326b4a56c4300e |
| ResidualMultiplier | 14f9e4bf32931e1c4b1215dff2a01ecd696828e3a9c8910e1e4b9fcb5cc3d9c8 | 72d43da8ba07fbda9f27521a27dfca950e2ff2e72b386d9df7126da72860d5b3 |
| IntegratedBudget | 280bc557901e0e777768fb5d45792813b6f5436e44f1de65ea7cc23f1be8293c | 0e12f19e34e9c0d34ef17fd0d15cac1742f1add50eade83debe63a0881a84b1e |

Terminal log SHA256:
`2f8cdc797d0dd06c59a3ea8df818023c2d235a116406c0d5fa0e9f9747c66677`.

The current source hashes were compared with the successful run's frozen
source files and all matched. The compile log prints dependencies only on
propext, Classical.choice and Quot.sound. There are no sorry/admit/custom
axiom declarations in the delivered new Lean sources. The cached local
module oleans and input snapshots have their pre-run hashes in
`output/run-iH9FGdAL/before_run.sha256`.

Primary handoff declarations, namespace `RouteBSignedGap`:

- `hasDerivAt_signedGap_from_source`: true source-space chain rules and
  finite-sum kinetic differentiation, with exact Christoffel power reuse.
- `affine_quadratic_expansion`, `affine_dissipation_fin6`: explicit affine
  7x7 form and its finite-vector nonnegative premise.
- `hasDerivAt_augmented_storage`, `augmented_affine_dissipation`: S5
  derivative assembly and affine gate composition.
- `integrated_signed_work`, `integrated_weighted_work`,
  `signed_budget_prefix_bootstrap`: real interval integrals and the uniform
  prefix budget interface.

These are compiled conditional mathematics. The physical source bindings,
eta bounds and regularity, AE trajectory adapter, state/source-cell matrix
certificates, uniform initial/prefix bounds, and ODE continuation remain
open as documented in README. No registry/state writes or physical
full-horizon certificate claim were made.
