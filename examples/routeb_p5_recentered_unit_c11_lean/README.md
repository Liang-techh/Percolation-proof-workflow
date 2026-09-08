# T-P5-068 recentered C1,1 unit Lean sidecar

Agent: 苏梦辰

This portable sidecar formalizes the source-independent quantitative core of柳冠一 `T-P5-068-RECENTERED-UNIT-C11`.

Kernel leaves:
- `segment_argument_sub`, `abs_segment_argument_sub`: exact segment-coordinate geometry;
- `segmentAverage_at_root`, `sigma_mul_segmentAverage`: canonical averaged-derivative normalization;
- `segment_average_bounds`, `segment_average_signed_bounds`: no-loss signed amplitude transport;
- `segment_average_lipschitz_twice`: sharp multiplication-only C1,1 gate `2*|Δv| <= L2*|Δx|`;
- `recentered_unit_exact_factorization`: exact piecewise divided-difference factorization at and away from the root;
- `recentered_unit_eq_segmentAverage_of_increment`: typed FTC seam, consuming the segment increment identity without re-proving source calculus;
- `root_graph_division_free_to_lipschitz`: division-free rational root-graph adapter;
- `parameterized_segment_argument_bound`: pointwise triangular-chart geometry for the parameterized extension;
- `sharp_half_quadratic_regression`: exact factor-1/2 sharpness regression.

The sidecar deliberately keeps the full `C1`/FTC source wrapper separate: callers must supply the exact increment identity `h x = (x-r)*segmentAverage g r x` (obtainable from the Mathlib FTC under the appropriate continuity/derivative hypotheses). This prevents a generic algebraic sidecar from inventing same-cell differentiability or deployed-source semantics.

Not proved here: deployed CSE/source binding, construction of `g=deriv h` from a source program, second-derivative enclosure, Float64/FD/controller semantics, multiple-root handling, reachability/P8 coverage, provenance/admission, or final P5/M4 integration.

`verify.sh` uses `lake`/`lean` from `PATH`, checks the pinned `local_fkg/lake-manifest.json` environment, compiles with warnings as errors, and rejects `sorryAx`.

Status after compilation must remain `compiled_candidate`: 待封不觉独立验证 / 待梁智炜最终整合。
