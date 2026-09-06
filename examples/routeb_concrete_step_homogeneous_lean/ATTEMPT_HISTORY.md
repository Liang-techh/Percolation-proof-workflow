# Attempt history

## 2026-09-06

- `run-yBVdGcm3`: dependency path was incomplete (`FrameRecursion.olean` was
  not yet included); no compilation claim was made.
- `run-ZBZY9WRv`: the minimal generic frame-shape proof and concrete bottom-row
  specialization compiled successfully. Peak RSS was about 5.2 GB because
  the source-level `RealDHStep` definition was elaborated; future adapters
  should consume this olean instead of expanding the source again.

No Julia runtime, Float64, comparator, or full-project regression claim is made.
