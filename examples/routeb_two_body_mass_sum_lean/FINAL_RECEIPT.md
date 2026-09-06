# Final receipt — Route-B two-body mass sum

Status: **PASS — block-(4,5) finite mass-sum interface; six-body and Float64
binding remain open**

The sidecar defines the sum of the body-3 and body-4 contract mass
contributions and proves its entrywise equality between the source slot
contract and the frame contract, reusing the verified single-body leaves.

Successful pinned run: `output/run-jYZomeB7`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
TwoBodyMassSum_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
TwoBodyMassSum.lean  22b681e4d7bb0672c223b08973d9e82101161fb7e9556863b50d12d0321b8ba5
TwoBodyMassSum.olean 79b5a1111a92c75a6da279abbe7041a7a0c9f814dd85bd91543f222a98fb8b1c
```

Only standard logical axioms occur in the axiom reports. No six-body source
equality, Float64 enclosure, or comparator admission is claimed.
