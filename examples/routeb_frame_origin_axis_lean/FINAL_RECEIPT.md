# Final receipt — Route-B frame origin/axis semantic leaf

Status: **PASS — ideal real-frame semantic candidate; Julia Float64 binding open**

The sidecar kernel-checks the source bookkeeping used by `fk_frames(q)`:

* the current frame is recorded before the current DH multiplication;
* the current joint axis is the third column of the parent frame;
* the next frame is `parent * current`;
* origin and axis arrays are projections of the recursive frame chain;
* six Route-B steps give seven frames, including the initial world frame.

Successful pinned run: `output/run-H0sN55iL`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
FrameOriginAxis_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
FrameOriginAxis.lean  8F8D3333C9D4FF2E5A4A3CF25FA1C11BA6C6C719B10598F8B0E03162C524EF39
FrameOriginAxis.olean A4B70EA5D3249A2AC90E0D73596EBB7B4493535BF2F2F817437E620C66A64BB5
terminal.log         0F8CE8D23EC41ADF7CB33F37B6ED7F6A94CBEAC574CBD58B273E5D71502DAAAF
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`. This does not claim machine `Float64` equality, trigonometric
enclosures, or the full mass-function equality.
