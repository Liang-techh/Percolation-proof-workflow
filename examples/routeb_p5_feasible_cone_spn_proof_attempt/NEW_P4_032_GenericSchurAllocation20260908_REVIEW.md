# Generic finite-dimensional Schur allocation

Status: `OPEN_UNCOMPILED`, source-independent mathematical child.

## Result

`NEW_P4_032_GenericSchurAllocation20260908.lean` lifts the existing 2-vector
completed-square identity to `Fin n → ℝ` for arbitrary finite `n`. It proves:

1. exact expansion of `sq (ell + r)` and `sq (ell - a r)`;
2. the combined Schur/Young identity with a single port cap `sq r ≤ W`;
3. the consumer `target ≤ beta - sq (ell+r)` from one nonnegative relaxed
   allocation;
4. `beta - lambda W - lambda/(lambda-1) * sq ell ≤
   beta - sq (ell+r)`, which is the explicit no-double-charge bridge;
5. the zero-radius finite-`lambda` boundary counterexample.

The same theorem can instantiate the 2-dimensional block-(4,5) port or the
3-dimensional block-(4,5,6) port. It remains Euclidean and source-independent:
the dense `M0_CC⁻¹` metric, DH residual identity, source/coverage, FD remainder,
flowpipe, comparator and registry gates remain external premises.

## Required next receipt

Assign a focused pinned Lean receipt to the Lean lane. It must compile this
standalone file, report the exact import/toolchain closure, exit code, all
`#print axioms`, and placeholder scan. A green receipt is only a
`compiled_candidate`; it does not close P4 or promote the verified registry.

## Mathematical use

The direct block456 target `beta_C - l_totalᵀ M0_CC⁻¹ l_total` may use this only
after a justified linear/metric transport. The theorem intentionally does not
provide that transport, so no Euclidean norm may be silently substituted for
the dense nominal metric.

