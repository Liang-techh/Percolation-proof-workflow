# Attempt history

## Attempt 1 — initial exact formulation

- Scope: independent relative-eta denominator lemma plus a division-free
  direct-gate interface.
- Planned constants: `A=2002229/24000000`, `D=29/20`,
  `K=36802229/24000000`.
- No original target files touched.
- No full-project regression, LP, trajectory run, or physical source claim.

The successful or failed compiler output is preserved under `output/` by
`verify.sh`; this file is retained as the first attempt record.

## Attempt 2 — first pinned compile

- Run: `output/run-u5pj4VJR`
- Result: failed (`VERIFY_EXIT_CODE=1`).
- Diagnostics: an unused `b` parameter and an inappropriate `linarith`
  invocation for the multiplicative direct-gate term.
- No theorem was admitted; the failed source snapshot and terminal log are
  preserved.

## Attempt 3 — exact repair and successful compile

- Run: `output/run-vLUcsyKh`
- Result: `RelativeEtaDenominator_COMPILE_EXIT_CODE=0`,
  `VERIFY_EXIT_CODE=0`.
- Repair: removed the unused residual parameter and used the exact standard
  equivalence `sub_le_iff_le_add`.
- The output reports only `propext`, `Classical.choice`, and `Quot.sound`.
- No original target files, physical source bindings, registry promotions,
  or project-wide tests were touched.
