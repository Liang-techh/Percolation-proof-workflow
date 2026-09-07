# Route-B P4 next child: exact rational Schur/PMI absorption

This directory contains one independently checkable exact-real child theorem:

* `exact_schur_margin` proves the strict rational Schur margin for the current
  block-4 scalar data `p=3/5`, `ell=1/100`, and the exact rational spelling of
  the exported `M0[4,4]` decimal;
* `exact_schur_nonnegative` proves the associated quadratic form is
  nonnegative for every real pair;
* `residual_absorption` consumes an explicit pointwise envelope
  `residual² ≤ ell² y²` and proves the same PMI remains nonnegative.

The child deliberately does not claim DH/Float64 source equality, global
partition coverage, inverse-mass bounds, continuous residual integration, or
M4 closure. The force/acceleration distinction from
`docs/routeb-c2-d-normalization-audit.md` is therefore preserved.

Run `verify.sh` for a focused Lean kernel check.
