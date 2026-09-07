# O1 body-1 source theorem instantiation

Status: `OPEN_BODY_1_SOURCE_EXPANSION_LEMMAS`

This review attacks only the first body leaf.  The existing generated
`BodyTraceEvaluator` was not regenerated or reaudited.

## Concrete Lean targets

`RouteBO1PerBodyTraceAdapter.lean` now contains:

```text
h_body_1_source_entry_target :
  forall q i j,
    bodyMass (sourceContract q).origins (sourceContract q).axes
      0 (routeBMass 0) (routeBInertia 0) i j
      = bodyTraceEvaluator 0 q i j

h_body_1_expected_entry_target :
  forall q i j,
    sourceBodyMass q 0 i j =
      if i = 0 and j = 0 then 628/1875 else 0

h_body_1_trace_entry_target :
  forall q i j,
    (if i = 0 and j = 0 then 628/1875 else 0) =
      bodyTraceEvaluator 0 q i j
```

These are `Prop` definitions only.  No `h_body_1` proof, axiom, or structure
field has been added.

## Exact bridge status

The body-1 source expansion is mathematically reducible: only joint 0 is
active; the parent axis is world z; the first-step translation contributes
`(2/25)^2/4 = 1/625`; the isotropic inertia contribution is `1/3`; hence the
candidate `(0,0)` entry is `1/625 + 1/3 = 628/1875`, with all other entries
zero.  This is a proof plan, not a proof receipt.

The current Lean obstruction is the absence of compiled pointwise lemmas for
the source contract's slot-0/slot-1 origins and joint-0 parent axis after
unfolding `routeBFrameSlot`, `realDHStep`, and the prefix matrix.  The trace
side separately needs a finite-fold reduction showing that the body-1 tagged
slice reduces to the zero-frequency real coefficient.  Neither premise may be
replaced by the CSV equality or by a proposition field.

A focused Lean probe remains blocked by the local Lake manifest's Linux
mathlib path; Windows reports `Function not implemented` while attempting the
clone.  Therefore the targets remain uncompiled and unverified.

Canonical receipt:

`examples/routeb_b45_source_comparator_lean/O1_BODY_1_SOURCE_BRIDGE_RECEIPT.json`

## Hashes

```text
RouteBO1PerBodyTraceAdapter.lean
6EF2594C785BB53254D9ED4AC0C08C3D6468BB731F9C61D5D165D8CB43E8483C

BodyTraceEvaluator.lean
B9845D37B5DCD16E1F9E142CB2E4D0E5571452993E843C85AC8CD643F6BA5DEA

O1_BODY_1_SOURCE_BRIDGE_RECEIPT.json
00875C5DEA93EF14C10D39A0CC69880A4B54A1772E58C2CE0E937C7BBB0A1AC9
```
