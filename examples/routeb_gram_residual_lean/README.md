# Route-B Gram residual Lean seam

This is a reusable kernel-level interface for the finite coefficient residual
in the nominal distal tail Gram candidate.

- `weighted_residual_l1_bound` proves the finite weighted residual bound when
  every atom is bounded by one.
- `decomposition_nonnegative_of_abs_residual` absorbs that bound into a
  positive decomposition.

The concrete rational Gram matrices, basis expansion, and coefficient receipt
remain separate source-bound artifacts. This file does not claim the true-DH
certificate, domain coverage, flowpipe inclusion, terminal transfer, or
registry admission. Provenance: the generic finite-sum seam mirrors the
finite-sum absolute-value pattern already used in the Route-B Lean adapters;
the concrete target is `routeB_tail_pmi_scalar_gram_rational.csv` in the
external 6-DOF project.

The current local reconstruction emits a concrete residual binding with
`residual_term_count = 511` and
`residual_coefficients_sha256 =
95042f6ea7c9989174d6045383138099686c2383649b3358611a63f374bcf7cf`.
The hashed canonical encoding is UTF-8 JSON with no insignificant whitespace:
an array sorted lexicographically by exponent tuple, where each entry is
`[[e1,...,e6], "numerator/denominator"]`; zero coefficients are omitted and
fractions are reduced. This digest is a binding witness only: a remote Lean
receipt must still bind the exact coefficient source, compile both theorems,
and report the pinned axioms.
