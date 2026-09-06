# Attempt history

## Initial semantic-bridge attempt — 2026-09-05

The prior leaf stopped at formal Laurent atoms and did not identify
`z = Complex.exp (Complex.I * q)`.  The current attempt adds the smallest
exact bridge for phases `1`, `Complex.I`, and `-Complex.I`, using
`Complex.exp_ofReal_mul_I`, `Complex.norm_exp_I_mul_ofReal`, and
`Complex.inv_eq_conj`.  No `sorry`, `admit`, or nonstandard axiom is used.

The source is intentionally compiled before any receipt is updated.  If the
attempt fails, its exact source and terminal log must remain under `output/`
and this record must be extended with the Lean error and next lemma.

### Repair of initial attempt — `run-rq9auBSp`

The pinned compile failed with exit code 1.  The exact errors were:

* linter error at the `hnorm` proof: `try 'simp' instead of 'simpa'`;
* unknown identifiers `map_ofReal` and `conj_I`;
* the conjugate expansion remained unsolved because the qualified
  `Complex.conj_ofReal`/`Complex.conj_I` facts were not supplied;
* after unfolding the local `z`, `rw` could no longer find `z⁻¹`;
* the failed attempt consequently exposed `sorryAx` in the unproved theorem.

The next lemma is the same phase bridge with the inverse/conjugate rewrite
performed before expanding the local abbreviation.  The failed source and
terminal log are preserved in `output/run-rq9auBSp/`.

### Definition-expansion repair — `run-cWJtOsnq`

The pinned compile again exited with code 1.  The qualified conjugation
lemmas and the `hnorm` proof now elaborated, but `rw [hinv]` failed because
the target still contained the opaque definitions `fourierCos` and
`fourierSin`; no explicit occurrence of `z⁻¹` existed yet.  The next repair
is to unfold only those two definitions first, then apply the already-proved
`z⁻¹ = conj z`, `conj z = ...`, and `z = ...` rewrites.  The exact source and
terminal log are preserved in `output/run-cWJtOsnq/`.

### Phase-algebra repair — `run-xPRde7mZ`

This compile reached only the residual algebraic goals
`Complex.I ^ 2 * Complex.sin ↑q = -Complex.sin ↑q` and its negated
counterpart.  The definition expansion and all `starRingEnd` rewrites were
successful.  The next minimal repair supplies Mathlib's exact
`Complex.I_sq` identity to `norm_num`; the failed source and terminal log
remain under `output/run-xPRde7mZ/`.

### Explicit `I²` repair — `run-dOUIXAZr`

The `Complex.I_sq` rewrite did not fire in the residual normal form, leaving
the same two goals.  The exact failed source and log are preserved under
`output/run-dOUIXAZr/`.  The next repair expands `pow_two` and uses the
actual Mathlib multiplication lemma `Complex.I_mul_I` directly.

### Ring-normal-form repair — `run-mJJajsJ4`

The explicit `pow_two`/`I_mul_I` simplification reduced the target but did
not normalize nested products inside the conjunction.  The exact remaining
target is preserved in `output/run-mJJajsJ4/`.  The next minimal repair is
`ring_nf` followed by the same exact `I²` identities.

### Linter-only repair — `run-ZjTISuSp`

The phase bridge itself closed, but warnings-as-errors rejected the final
`simp` because `Complex.I_mul_I` was unused after `ring_nf`; the exact log is
preserved in `output/run-ZjTISuSp/`.  The final repair removes only that
unused argument and retains `Complex.I_sq`.
