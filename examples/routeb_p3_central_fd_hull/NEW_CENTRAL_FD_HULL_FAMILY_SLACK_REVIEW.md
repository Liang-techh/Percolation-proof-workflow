# P3 family-level strict slack consumer

Status: conditional exact-real proof-attempt candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_FAMILY_SLACK.lean` consumes, at one common point, three
upstream facts:

```text
selected gap <= capLoad - weightedLoad
0 < selected gap
capLoad <= capMaxLoad.
```

`family_strict_slack6` proves both the quantitative slack

```text
weightedLoad + selectedGap <= capMaxLoad
```

and the strict consequence `weightedLoad < capMaxLoad`.
`family_strict_slack_consumer6` then adds an existing consumer bound by
transitivity.

## Same-point contract

`FamilySlackContext6` carries `muBar`, component radius, cap vector, load,
velocity, weight, capMax, one common point, and four layer-membership premises.
The componentization equality and all nonnegativity/velocity premises remain
explicit fields. The strict theorem does not infer a concrete cap from a
radius or infer domain agreement from naming.

## Missing-premise obstruction

If no family-to-concrete cap relation supplies `hOrder`, `hGapLower`, or
`hCapMax`, this leaf cannot produce strict slack; the result remains
conditional. Likewise, if the four layer facts are not established at the same
point, the context cannot be specialized soundly. No fallback numerical or
physical fact is inserted.

No source, numerical value, rounding evidence, coverage, admission, registry,
or Lean compilation claim is made. No local Lean/Lake command was run.

