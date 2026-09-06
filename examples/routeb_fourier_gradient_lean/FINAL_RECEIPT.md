# Final receipt — Route-B Fourier potential gradient leaf

Status: **PASS — compiled candidate; deployed source binding still open**

The sidecar defines a finite Fourier potential and proves:

* `phaseLine_at`: coordinate-line phase at the base point equals the original
  phase;
* `hasDerivAt_phaseLine`: its exact coordinate derivative is the corresponding
  frequency;
* `hasDerivAt_fourier_row`: each Fourier row has the exact cosine derivative;
* `hasDerivAt_fourierPotential_coordinate`: the finite row sum has the stated
  coordinate gradient;
* `deployed_gradient_of_functional_identity`: a functional identity reduces a
  deployed zero-gradient claim to the Fourier gradient equality.

Successful pinned run: `output/run-weWkW1WN`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
FourierGradient_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SNAPSHOT_HASHES_UNCHANGED=true
```

Hashes:

```text
FourierGradient.lean  2BF64904920F1EF6A46CD79D5BA10B14320F60347448BD55BECC5C27FE29EFEB
FourierGradient.olean 5955F79DBAF7667FA1106CF8F93905CF77D18C355C7A53890BFBDF2DB5F3AC87
terminal.log          575E88FD7748C20F0218131B5F4DF69E793DCABC2B6357BA806DA5995FD345A3
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`; there is no `sorry`, `admit`, or custom axiom.  This leaf does
not prove equality to the Julia potential, central finite-difference C/G
semantics, or a Float64 rounding enclosure, so it is not registry-verified.
