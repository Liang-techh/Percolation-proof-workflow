# Final receipt — Route-B body COM/Jacobian mass leaf

Status: **PASS — compiled candidate; physical frame/Float64 binding open**

The sidecar defines and kernel-checks the source-audited body semantics:

* consecutive-origin midpoint COM;
* pre-current parent-axis based translational columns;
* cross-product orientation;
* angular Jacobian columns;
* `j.val ≤ body.val` ancestor cutoff and zero inactive columns;
* expansion of each body contribution into the link-mass Gram form.

Successful pinned run: `output/run-vB4nl7Rh`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
BodyMass_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
PHYSICAL_FRAME_BINDING=OPEN
FLOAT64_BINDING=OPEN
```

Hashes:

```text
BodyMass.lean  65A9CACFC15EEA1603EE364148E477B9A2978DD1144F785E705BE87D2C201AFF
BodyMass.olean C437B10CEAFA7287E8CAF2269FB7B621155E4607D61734B22991551777A1CA46
terminal.log   1F86846C4C55D2EEDA801E362BDC90E3511418870AC44E33ADFEDCF55FDB7E89
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`.  No Julia source equality, Float64 enclosure, full-q Fourier
identity, or registry promotion is claimed.
