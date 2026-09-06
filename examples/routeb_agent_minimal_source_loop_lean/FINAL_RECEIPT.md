# Final receipt — Route-B minimal source loop

Status: **PASS — pinned Lean compiled candidate; not registry-admitted**

`RouteBMinimalSourceLoop.lean` is an independent Mathlib-only formalization of
the finite six-body accumulation used by the Julia `mass_matrix` loop. It proves
the finite body sum, equality with generic `massFromLinks`, explicit cutoff
vanishing, and the rotated-isotropic inertia expansion. It does not claim
Julia/Float64 implementation equivalence or source comparator acceptance.

Pinned environment:

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
COMPILE_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
MAIN_DAG_STATE_UNCHANGED=true
```

The four theorem axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`; no `sorry`, `admit`, or declared axiom is present.

Successful run: `output/run-GKVqBwZa`

```text
RouteBMinimalSourceLoop.lean  82a8d0d7c7e6ea7ab8867d4c1113cdff23b146b441a9c08442a9b187594480d6
RouteBMinimalSourceLoop.olean ADAAB00BBD19F242DF0D147C59F06620C8EF55ED401266CADC8E521FC7F3A5C2
terminal.log                  81F6F8E7C92E6B899254DE79A3DCEF51684AAF3AA5A2BFA55CFB7E1FAF2B30C1
```
