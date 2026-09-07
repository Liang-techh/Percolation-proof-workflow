# O1 bodyTraceEvaluator — typed 7-leaf follow-up

Status: `OPEN_H_BODY_PROOFS_UNCOMPILED`

## Result

The 727-row body trace now has a generated Lean transport definition at
`examples/routeb_b45_source_comparator_lean/BodyTraceEvaluator.lean`.
Each `BodyTraceRow` retains `body`, `row`, `col`, six-coordinate `frequency`,
and real/imaginary `RationalTag` numerator/denominator fields.  The concrete
`bodyTraceEvaluator` is a finite exact fold over these tagged rows, followed by
the real cosine/sine lift.

The adapter
`examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyTraceAdapter.lean`
defines `fourierBodyFromTrace` and six explicit propositions
`h_body_1` through `h_body_6`.  They are direct source-versus-generated-
evaluator targets; no `h_body` premise is stored in a structure and no proof is
asserted.

## Boundary

The generated Lean and adapter are not compiled.  A focused `lake env lean`
probe was blocked because the local Lake manifest points at a Linux mathlib
path and attempted a Windows-incompatible clone (`Function not implemented`).
Thus neither syntax compilation nor any of the six exact DH equalities is
verified here.

The only remaining mathematical obligations are the six source-bound proofs:

```text
forall q i j, sourceBodyMass q (bodyIndex : Fin 6) i j
  = fourierBodyFromTrace bodyIndex q i j
```

for `bodyIndex = 0,...,5`, under the existing source/state/mu/q key.  The
receipt deliberately records these as open and rejects premise-field or
data-level equality substitution.

## Immutable hashes

```text
body trace CSV
AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9

generate_body_trace_evaluator.py
79664A62EFD9A021F52A13FC7F5DCD545DCA602DEB0FFFEC8CA5B6E96C00DC83

BodyTraceEvaluator.lean
B9845D37B5DCD16E1F9E142CB2E4D0E5571452993E843C85AC8CD643F6BA5DEA

RouteBO1PerBodyTraceAdapter.lean
2D48D0767C0C6A432A3592FDB85651D2CBD440DA63A0E0E6653CAE6FE96A20D9

O1_BODY_TRACE_EVALUATOR_RECEIPT.json
4BCF7BE771A9C29FADAF177B65853E697C3617F898D5B87DC26686AA98D6F62D
```
