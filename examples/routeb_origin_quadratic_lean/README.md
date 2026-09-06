# Route-B origin quadratic Lean leaf

This leaf contains reusable, model-independent structural rejection lemmas.

- `negSemidefinite_of_originQuadraticLittleO`: a symmetric finite-dimensional
  quadratic form bounded by `ε * ‖x‖²` for every `ε > 0` is nonpositive.
- `negSemidefinite_of_negatedQuadraticPlusQuartic`: the scaled condition
  `-q_N(x) + ε R(x) ≥ 0` for every `ε > 0` implies `q_N(x) ≤ 0`; `ε` is the
  squared scale, so no limit or square-root analysis is needed.
- `neg_not_quadNonnegative_zero_diagonal_offdiag`: a symmetric 2×2 matrix
  with zero diagonal and nonzero off-diagonal cannot become
  `QuadNonnegative` after negation.
- `neg_not_quadNonnegative_q6_v6_block`: the concrete zero-diagonal,
  nonzero-coupling instance.

Verification is isolated to this directory. Run `bash verify.sh` from WSL;
the script uses cached Lean 4.33.1/Mathlib only, enables warnings-as-errors,
creates a prospective pre-run hash snapshot, and retains every `output/run-*`
directory. This leaf does not write project state, existing leaves, or archives.
