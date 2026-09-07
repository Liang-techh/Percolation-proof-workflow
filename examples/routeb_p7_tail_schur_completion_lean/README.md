# Route-B P7 typed 2x2 Schur completion

Task: `T-P7-002`.

This sidecar formalizes the source-independent mathematical seam identified
in `review-T-P7-001-honglianmozun-20260906T2244.md`:

- an exact 2x2 Schur completion identity;
- a robust upper bound for the inverse quadratic form under absolute-value
  bounds on the two cross coefficients;
- an absorption theorem consuming a typed bound `inverse_quadratic <= eta`
  and `eta <= tau`.

The symbols `a,b,d,u1,u2,s` are abstract. This does not prove that the
deployed seven-term P7 polynomial, its inverse block, normalization scalar,
or trajectory variable have these meanings. It also does not prove P7/P8
coverage, true-DH semantics, or M4 closure. Remote pinned Lean compilation
and independent admission review remain required.
