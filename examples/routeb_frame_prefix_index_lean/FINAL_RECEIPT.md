# Final receipt — Route-B finite frame-prefix index leaf

Status: **PASS — generic ideal real-frame prefix candidate; Float64 binding open**

The sidecar proves, without unfolding DH matrix entries, that the six-step
source recursion is equal to an explicit seven-frame prefix list. The prefix
keeps the source multiplication order `parent * current`, and the projected
origin/axis lists therefore remain aligned with the source frame chain. This
is the lightweight indexing contract intended for downstream body leaves.

Successful pinned run: `output/run-lVHyO9Lp`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
FramePrefixIndex_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
FramePrefixIndex.lean  6A834B585E14286BF2BA1042493955C065B8A1BA2DD82B5B942A09CE9C2181A5
FramePrefixIndex.olean 60EAAB045DD51A99D497949FA07A3172574DBB3A8789573A054DDF17CEF1CA26
terminal.log           0D8150F764922191EF229DD395DB2E1A9DAA0C26E76D4062C31DDA2376FA0F53
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`. No Julia `Float64` equality or full mass-function equality is
claimed.
