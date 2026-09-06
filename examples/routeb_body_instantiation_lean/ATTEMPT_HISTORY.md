# Attempt history

## 2026-09-05 — run-rbr5Ms0S

Failed during module loading because the runner omitted the upstream
`MassFunctional` output directory. No state was changed.

## 2026-09-05 — run-os1dwi5g

The first source version used a dependent `List.get` accessor and had a
missing namespace qualification. The missing namespace was fixed, but the
dependent accessor caused excessive elaboration and the run was stopped after
memory growth; no theorem was admitted.

## 2026-09-05 — run-NTvbgSxi

The accessor was redesigned as a fixed `Fin 7` explicit six-prefix product,
and the duplicate expanded-entry theorem was removed. The run still exceeded
the practical narrow-leaf budget and was stopped. This sidecar remains an
uncompiled draft and is not part of the verified registry.
