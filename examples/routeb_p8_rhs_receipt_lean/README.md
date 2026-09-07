# Route-B P8 14-coordinate RHS receipt interface

This leaf defines a reusable receipt boundary for the `hbox` premise of
`RouteBP8PicardStep`.

The receipt contains:

- a finite indexed endpoint payload `lower upper : Fin 14 → ℝ`, with a proved
  lower-to-upper ordering field;
- an explicit `sourceHash : String` field;
- explicit rounding metadata: direction, precision in bits, arithmetic label,
  and note;
- an explicit `FullRhsBindingStatus`, whose only available constructor here is
  `open`.

`CoordinateWiseIntervalContainment` requires, for every state in the supplied
box and every `Fin 14` coordinate, the RHS to lie between the corresponding
payload endpoints.  `receipt_to_routeBP8PicardStep_hbox` converts that
proposition to the parent module's exact
`RouteBP8PicardStep.RhsIntervalPremise`.  The theorem
`receipt_usable_for_routeBP8PicardStep` feeds the converted premise into the
parent Picard-step decomposition.

This is deliberately a conditional interface.  The file does not define or
bind the deployed Julia `full_rhs!`, does not include endpoint numbers, and
does not create a receipt instance.  A source hash or rounding record is
metadata, not proof of interval containment; the `Contains` premise remains
mandatory.  Consequently the concrete Julia RHS binding is **OPEN**.

There is no `sorry`, `admit`, `axiom`, or `unsafe` declaration.  Verification
compiles this file together with a copied, pinned parent P8 module and runs a
source restriction scan.  It does not run Julia and does not use sampled RHS
data.

Run from WSL or another Bash environment with the pinned Lean installation:

```text
./verify.sh
```
