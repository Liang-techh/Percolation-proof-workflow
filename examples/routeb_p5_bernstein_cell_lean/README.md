# T-P5-052 correlated Bernstein cell gate — Lean sidecar

This portable sidecar formalizes the source-independent trusted core requested by `review-T-P5-052-guyuefangyuan-20260907T2334`:

- exact monomial-to-Bernstein identities for degree 2 and degree 3 on `[0,1]`;
- nonnegative-control consumers;
- exact dyadic de Casteljau left/right half identities;
- control nonnegativity preservation under half subdivision;
- the endpoint-only unsoundness regression `1-5t+5t^2`;
- a positive polynomial with a negative coarse Bernstein control, enforcing the fail-closed `SUBDIVIDE/UNDECIDED` interpretation;
- a generic typed bridge that feeds certified `Rtr`/`Rdet` values into an already-proved two-remainder consumer without re-proving the 2x2 affine completion.

The sidecar intentionally does **not** formalize the optional eventual-subdivision theorem for all strictly positive cubic polynomials. That compactness/derivative analysis is not required by the trusted checker core. It also does not establish deployed source polynomiality, Float64/FD/controller semantics, multidimensional coverage, P8 ODE coverage, P5/M4 closure, or registry admission.

Run with:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_bernstein_cell_lean/verify.sh
```

Admission boundary: `compiled_candidate` only after pinned Lean compilation and axiom audit; then **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.
