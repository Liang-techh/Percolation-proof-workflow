# P3 strict weighted-cap order bridge

Status: bounded exact-real proof-attempt candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_STRICT_ORDER.lean` proves strictness for the already
assembled load order:

```text
q[jStar] < qCap[jStar]
load[jStar] > 0
q[i] <= qCap[i] for all i
  => weightedLoad(load,q) < weightedLoad(load,qCap).
```

The proof uses an explicit `Fin 6` erase decomposition of the difference sum:
the selected positive term is strict and all other terms are nonnegative.

## CapMax consumer

`capMax_consumer_strict6` consumes an existing non-strict premise

```text
capLoad(load,qCap) <= capMaxLoad(load,capMax)
```

and combines it with an existing consumer bound and the strict component gap.
It does not reprove the non-strict order bridge or capMax upper-bound
construction.

`StrictOrderContext6` keeps one common point, four layer memberships, an
explicit velocity premise, nonnegative weights, and the assembled-load/load
equality visible. These are context premises only; the strict order proof uses
the already assembled nonnegative load field.

## Boundary

No concrete source, numerical cap, physical velocity origin, rounding evidence,
coverage, admission, registry state, radius construction, or force theorem is
selected or inferred. The strict conclusion depends on the explicit positive
load, strict component gap, consumer bound, and capMax comparison premises.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

