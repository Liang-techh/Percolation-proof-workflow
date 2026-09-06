# Final receipt — Route-B mass functional composition leaf

Status: **PASS — compiled candidate; source binding still open**

The sidecar proves the finite-dimensional composition step needed by B45-1:

* `weightedGram_congruent` lifts pointwise Jacobian/weight equality to a Gram
  matrix equality;
* `linkMass_congruent` combines translational mass and rotational inertia;
* `massFromLinks_congruent` closes the finite six-link sum;
* `ideal_mass_eq_fourier_of_linkwise` exposes the remaining source adapter as
  explicit linkwise hypotheses;
* `regularized_mass_eq_fourier` preserves equality under the exact diagonal
  regularizer.

Successful pinned run: `output/run-pVaCVj2p`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
MassFunctional_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SNAPSHOT_HASHES_UNCHANGED=true
```

Hashes:

```text
MassFunctional.lean  E9B90D46B70E5CFAD03A1DA34B6FBC369751A791FD40A867424921E8AC63A
MassFunctional.olean 946CDCB566546BFF92524869673ABFEB627587217979995B41FDDB0D1CC3EF8D
terminal.log         37A729BCDA3D9E980B3618A1AD46824E719B0F8BC79E8DC755DFFE55BC6AD446
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`.  No `sorry`, `admit`, custom axiom, CSV reader, Julia binding,
or Float64 enclosure is used.  Therefore this receipt does not promote the
full mass identity or the formal certificate.
