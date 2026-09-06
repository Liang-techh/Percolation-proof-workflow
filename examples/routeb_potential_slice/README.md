# Actual coefficient table to negative storage configuration

`PotentialSlice.lean` encodes all 17 Gaussian-rational potential CSV rows in
their original order and the six actual rational proportional gains. It proves
the exact slice identity for the full encoded potential and transfers the
existing scalar obstruction to `no_global_nonnegative_W` and a negative
configuration at `q=![0,1/10,0,0,0,0]`.

`output/run-SuGxG04V/verify.log` records successful offline Lean 4.33.1
compilation with warnings as errors. `source_evidence.json` records the exact
CSV-field/Kp audit, input hashes and imported proof-object hashes. Both
conjugate rows are counted once; all imaginary parts are zero.

This closes the coefficient-to-slice seam. It does not prove that a DH
kinematic/derivative implementation equals this Fourier model, nor enclose
Float64 evaluation. It invalidates the unshifted-energy nonnegativity shortcut,
not the original block-(4,5) safety/terminal goal or the saved polynomial V.

Reproduce with `bash examples/routeb_potential_slice/verify.sh` in the existing
WSL environment. The script reuses the successful StorageObstruction object,
does not download dependencies, and writes fresh run evidence only here.
