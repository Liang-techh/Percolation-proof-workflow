# O1 human body-5 source expansion and trace fold

Status: `OPEN_BODY_5_SOURCE_AND_TRACE_PREMISES`

Scope is restricted to CSV body `5`, zero-based body `4`.  No other body was
modified, the evaluator was not regenerated, and no Lean/Lake command was run.

## Exact piecewise target

The adapter adds `body_5_piecewise`, `h_body_5_source_expanded_target`,
`h_body_5_expected_entry_target`, `h_body_5_trace_fold_target`, and the
conditional composition `h_body_5_of_entry_targets`.

With `x=q(1)`, `y=q(2)`, `z=q(3)`, the nonzero entries are:

```text
(0,0) = 1441/30000 + (63/6250) sin(x) + (57/6250) sin(x+y)
       - (1323/200000) cos(2x) + (1197/100000) cos(y)
       - (1197/100000) cos(2x+y) - (1083/200000) cos(2x+2y)
(0,1) = (1,0) = -(57/20000) cos(x+y) - (63/20000) cos(x)
(0,2) = (2,0) = -(57/20000) cos(x+y)
(0,3) = (3,0) = (1/30) cos(x+y)
(0,4) = (4,0) = (1/60)[cos(x+y-z)-cos(x+y+z)]
(1,1) = 8609/150000 + (1197/50000) cos(y)
(1,2) = (2,1) = 13249/300000 + (1197/100000) cos(y)
(1,4) = (2,4) and transposes = (1/30) cos(z)
(2,2) = 13249/300000
(3,3) = (4,4) = 1/30
otherwise = 0
```

The complete signed rational frequency families are pinned in the receipt.

## Fail-closed boundary

The source expansion, trace fold, and `h_body_5` remain open propositions.
`h_body_5_of_entry_targets` only composes two supplied premises; it does not
assert or prove either premise.  No registry, comparator, or formal-certificate
admission is allowed.

Receipt:
`examples/routeb_b45_source_comparator_lean/O1_BODY_5_SOURCE_BRIDGE_RECEIPT.json`

## Next exact proof obligations

The next Lean agent must separately establish the body-5 source Gram expansion
from the prefix-frame origin/axis formulas, then reduce the generated body-5
finite fold by its body/row/col guards and signed frequency pairs.  The fourth
DH step has zero translational offset (`a=0,d=0`), so the fifth translational
Jacobian column is zero; the remaining `q(3)` terms arise from the angular-axis
projection.  These are structural proof hints only, not verified receipts.

## Hashes

```text
RouteBO1PerBodyTraceAdapter.lean
25F099EC5EB7F699C789AE29AA45DF0FBB24FF06547F498740968F5E1B3C9976

BodyTraceEvaluator.lean
B9845D37B5DCD16E1F9E142CB2E4D0E5571452993E843C85AC8CD643F6BA5DEA

body trace CSV
AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9

O1_BODY_5_SOURCE_BRIDGE_RECEIPT.json
FD49BD0D000CA011F7C7C29B3458BD2DC4998DDF71FA897F9AC9C9551A3B0397
```
