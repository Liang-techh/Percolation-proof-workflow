# P4 next-child report

## Result

`EXACT_RATIONAL_SCHUR_ABSORPTION = VERIFIED` by the pinned Lean kernel.

Actual focused verification (2026-09-06, Windows):

```text
cwd = examples/local_fkg
command = C:\Users\z5242\.elan\bin\lake.exe env lean -DwarningAsError=true \
  C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_p4_next_child\P4RationalSchurAbsorption.lean
exit_code = 0
'RouteBP4NextChild.exact_schur_margin' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP4NextChild.exact_schur_nonnegative' depends on axioms: [propext, Classical.choice, Quot.sound]
'RouteBP4NextChild.residual_absorption' depends on axioms: [propext, Classical.choice, Quot.sound]
AXIOM_AUDIT = PASS (no sorryAx, admit, or custom axiom)
```

`verify.sh` reproduces the same focused check and exits nonzero with
`BUILD_ENV_BLOCKED` if no `lake` executable can be found.

The closed child is a reusable algebraic consumer for a future P4 receipt:
an exact residual envelope with `beta=1/100` is sufficient for the concrete
block-4 scalar PMI channel. It is not a physical certificate because the
premise is intentionally abstract.

## Boundary

The current external P4 artifact still reports `coverage_complete=false` and
the positive-origin Schur row as unknown. The Julia SOS coefficients are also
runtime-generated and are not a fixed rational Gram witness. Consequently
`P4.residual_schur_pmi`, M4, and the verified theorem registry remain open.

The exact rational `d` is only a reification of the exported decimal
`0.116667666666667`; it is not a proof that the Float64/DH computation equals
that rational. That source-binding theorem remains the next frontier.
