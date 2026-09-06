# Attempt history

## 2026-09-06

- `run-qZ0JSuPZ`: initial slotwise proof left `Fin`/prefix normalization goals
  and attempted rewrites through nested products.
- `run-NeGjbpeO`: direct expansion of nested 4x4 products was stopped after it
  reached about 3.1 GB RSS; no proof artifact was accepted.
- `run-kaUnAlt6`: a finite-dimensional homogeneous-product closure was added,
  but the identity-matrix projection needed explicit `Matrix.one_apply`.
- `run-7hl40Fdl`: `homogeneous_mul` plus the seven slot cases compiled with
  warning-as-error and passed source restrictions.

No source runtime, Float64, comparator, or full-project regression claim is made.
