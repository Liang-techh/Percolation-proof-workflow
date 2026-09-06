# Attempt history

`run-sHvKnSgi` failed with `lean.dependsOnNoncomputable` because the real
regularizer definition uses noncomputable real division. The source was repaired
by adding a scoped `noncomputable section`; the failed log is retained.
