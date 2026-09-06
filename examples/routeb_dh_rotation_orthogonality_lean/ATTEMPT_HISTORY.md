# Attempt history

## 2026-09-06 — DH rotation orthogonality repair loop

- `run-uhyByRoH`: `nlinarith` could not infer the multiplication of the
  `ca²+sa²=1` equality by `ct*st` in the two off-diagonal cases.
- `run-V8rQL67x`: `ring_nf` exposed the exact residual but the first
  linear-combination coefficient had the wrong sign.
- `run-1CNABqps`: repair attempts showed the residual coefficient convention;
  the needed multiplier is `-(ct*st)`.
- `run-H6azhYLs`: an intermediate coefficient was still wrong and was kept as
  failed evidence.
- `run-u9aZXWdK`: the negative multiplier closed all cases; compile and source
  restriction passed.

The Route-B trigonometric specialization and source/Float64 bridge remain open.
