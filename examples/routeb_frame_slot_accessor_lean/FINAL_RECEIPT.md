# Final receipt — Route-B frame slot accessor

Status: **PASS — source frame/origin/axis slot bridge; Float64 binding open**

The sidecar proves that a fixed `Fin 7` prefix accessor is exactly the
corresponding `List.getD` slot of the recursive Route-B source frame list. It
also lifts the result to the source origin and axis arrays. The proof keeps DH
matrix entries opaque and preserves the source `parent * current` structure.

Successful pinned run: `output/run-4RJoHvpZ`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
FrameSlotAccessor_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
FrameSlotAccessor.lean  f497bd1f45fae4dd385f4d0f46df79252c92e5cd027b29d5dc55011f91525c31
FrameSlotAccessor.olean 89be6d796b4564c3d84778eb7649772313403bb998184fb1ae028bb177e93af9
terminal.log             5116fd9e56ca89ae366f5acf7f80e2cb5704c2c7e05256dd6eb90495320cfff7
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`. No Julia `Float64` equality, enclosure, or full mass identity
is claimed.
