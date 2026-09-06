# B45-2 exact-real / conditional-Float64 seam

This is an isolated sidecar for the potential, centered-FD gradient, and
final `C*dq`/`G` error interface.  It does not import the deployed-source
comparator and does not read or write workflow state or the theorem registry.

The exact interface is six-dimensional throughout:

- `q : Fin 6 -> R` and `dq : Fin 6 -> R`;
- samples are `q + h e_k` and `q - h e_k`, represented by `qPlus`/`qMinus`;
- `h = 1/100000` and the mass regularizer is explicitly `mu = 1/1000000`.

The Float64 layer is conditional.  A machine output is represented by an
interpreted real function and enters only through value, step, derivative, or
solver-side enclosure hypotheses.  No theorem here claims that Julia's
machine `sin/cos`, FK products, finite differences, or `\` solve satisfy those
hypotheses.

The minimal IEEE-754 interface is explicit: `ieee64UnitRoundoff = 2^-53`,
and `ieee64Round x xhat` is the finite-normal binary64 relative-rounding
premise `|xhat-x| <= 2^-53 |x|`.  The
`gradient_ieee64_sample_enclosure` theorem consumes that premise at both
exact points `q +/- h e_k` and produces the potential/gradient error bound.
Normality, finiteness, and no-overflow are premises rather than hidden claims.

The final budget adds the exact FD defect and runtime defect before squaring,
so the `2 * exactErr * runtimeErr` cross term is retained.  The contraction
lemma derives a componentwise `C*dq` error from six-dimensional derivative
tensor enclosures; the gradient lemma derives the centered-FD error from the
two potential sample enclosures.  The separate deployed-source comparator
remains an upstream obligation.

## Targeted verification

From WSL, run:

```bash
./verify.sh
```

The script uses the pinned Lean 4.33.1 and the existing read-only Mathlib
cache.  It bypasses Lake and does not download, rebuild, or touch any project
state.  The generated run directory and compile receipt stay under this
sidecar's `output/` directory.
