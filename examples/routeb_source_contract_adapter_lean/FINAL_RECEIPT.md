# Final receipt — Route-B source contract adapter

Status: **PASS — source slot origin/axis equality and body-mass lift; Julia
Float64 binding remains open**

This narrow sidecar defines a source-facing `KinematicContract` from the
verified `List.getD` frame slots and a concrete frame-slot contract. It proves
the seven source origin slots equal the frame-slot origins, the six source
joint axes equal the first six parent-frame slots, and these equalities lift to
the body mass through the contract-core congruence theorem. The `Fin 6 → Fin 7`
mapping is explicit via `prevOrigin`, matching the source semantics that joint
`j` uses the parent frame before step `j`.

Successful pinned run: `output/run-RSGGTurS`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
SourceContractAdapter_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
SourceContractAdapter.lean  58c0b15b6fceb1064f773acdb9f684dc55a021ac69a030c13e1c8b46f7b9a8dc
SourceContractAdapter.olean c1908efdfe68c5515623290fdb1808129da75a437d7d163336882282da23d5f4
terminal.log                d505c2ded193dbb69b3c26b2edb6adf771d7773289867a1ad6a9d0c6cccc88c3
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`. This is a compiled candidate, not comparator or registry
admission: the adapter still does not claim equality to Julia machine
`Float64` evaluation or the full six-body mass function.
