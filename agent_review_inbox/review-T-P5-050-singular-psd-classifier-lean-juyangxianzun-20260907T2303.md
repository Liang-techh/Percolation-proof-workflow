---
kind: review_result
review_id: review-T-P5-050-singular-psd-classifier-lean-juyangxianzun-20260907T2303
task_id: T-P5-050
agent: 巨阳仙尊
source_agent: 巨阳仙尊
math_source_agent: 狂蛮魔尊
math_source_review: review-T-P5-050-kuangmanmozun-20260907T2238
integration_status: compiled_candidate
admission_label: pending
registry_mutation: false
---

# T-P5-050 — singular PSD classifier Lean formalization / CI repair result

## Result

Consumed 狂蛮魔尊's pivot-free singular-PSD classification and implemented the source-independent algebraic core as a portable Lean sidecar:

- `examples/routeb_p5_singular_psd_classifier_lean/P5SingularPSDClassifier.lean`
- `examples/routeb_p5_singular_psd_classifier_lean/README.md`
- `examples/routeb_p5_singular_psd_classifier_lean/verify.sh`

The formalized scope is the singular symmetric `2x2` quadratic/affine classifier under `p >= 0`, `s >= 0`, `p*s-q^2 = 0`: adjugate/kernel identities, incompatibility numerator, pivot-free trace completion, the compatible nonzero-rank completion bound, explicit incompatible kernel-ray unboundedness, the trace-zero/zero-matrix branch, and the exhaustive finite-upper-bound classifier. This is algebraic/formalization evidence only; it does not bind deployed P5 coefficients or physical/runtime semantics.

## Repair cycle

The initial sidecar reached GitHub Actions but exposed two genuine Lean proof-shape issues. They were repaired without weakening theorem statements.

Final repair commit:

`64cbcfed5f1fae24efb5639ed1e4837e7177c0e9`

The repair in `singular_incompatible_unbounded` replaced a brittle `nlinarith` use of the adjugate-bias identity with an explicit `calc` plus `ring`/`rw`, so the scaled kernel-ray bias is normalized deterministically. In `singular_psd_finite_upper_bound_iff`, the trace-zero branch now explicitly forms `htau0 : trace2 p s = 0 := htau.symm` before invoking the zero-matrix theorem, fixing the equality-orientation mismatch.

This closes the intended `数学 -> Lean -> CI -> 修复 -> 再 Lean` loop for this sidecar.

## GitHub-hosted compile evidence

Workflow: `.github/workflows/lean-agent-sidecars.yml`

- run: `34188767386`
- job: `101942323905`
- head SHA: `64cbcfed5f1fae24efb5639ed1e4837e7177c0e9`
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`
- repository-pinned local-FKG toolchain: `leanprover/lean4:v4.32.0`

Focused lane output:

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P5_SINGULAR_PSD_CLASSIFIER_FOCUSED_CHECK=PASS
PIVOT_FREE_SINGULAR_CLASSIFIER=true
SOURCE_FLOAT64_BINDING=OPEN
P8_ODE_COVERAGE=OPEN
P5_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_singular_psd_classifier_lean/verify.sh
```

The shared portable-sidecars job is red because several unrelated historical lanes still fail. The T-P5-050 lane itself is explicitly `SIDECAR_RESULT=PASS`; this review does not claim the aggregate workflow is green.

## Public theorem / axiom audit

The focused run printed axiom sets for all 19 public theorem targets below. Every target depends only on the standard set `[propext, Classical.choice, Quot.sound]`; none contains `sorryAx`.

1. `RouteBP5SingularPSD.adjugate_kernel_first`
2. `RouteBP5SingularPSD.adjugate_kernel_second`
3. `RouteBP5SingularPSD.incompatibility_norm_identity`
4. `RouteBP5SingularPSD.trace_completion_identity`
5. `RouteBP5SingularPSD.singular_compatible_trace_identity`
6. `RouteBP5SingularPSD.singular_compatible_completion_cleared`
7. `RouteBP5SingularPSD.singular_compatible_completion`
8. `RouteBP5SingularPSD.compatible_range_first`
9. `RouteBP5SingularPSD.compatible_range_second`
10. `RouteBP5SingularPSD.singular_incompatibility_norm`
11. `RouteBP5SingularPSD.singular_incompatible_adjnumerator_pos`
12. `RouteBP5SingularPSD.singular_adjugate_kernel_quadratic`
13. `RouteBP5SingularPSD.singular_adjugate_kernel_ray_quadratic`
14. `RouteBP5SingularPSD.adjugate_kernel_bias`
15. `RouteBP5SingularPSD.singular_incompatible_unbounded`
16. `RouteBP5SingularPSD.zero_trace_diagonals`
17. `RouteBP5SingularPSD.zero_matrix_of_psd_singular_trace_zero`
18. `RouteBP5SingularPSD.zero_matrix_nonzero_bias_unbounded`
19. `RouteBP5SingularPSD.singular_psd_finite_upper_bound_iff`

The last theorem is the formal dispatcher seam: under singular PSD diagonal assumptions, existence of a global finite upper bound is equivalent to either the nonzero-rank compatible branch or the zero-matrix/zero-bias branch. It must not be interpreted as a deployed P5 certificate until concrete coefficients and source semantics are separately bound.

## Open boundaries

Still open and intentionally not claimed here:

- deployed/source coefficient binding for `p,q,s,b4,b5`;
- true-DH and Float64/controller/solve semantics;
- same-domain P8 trajectory / ODE coverage;
- positive-definite T-P5-044 layer and the dispatcher that selects positive-definite versus singular branches;
- P5/P8/M4 final composition;
- provenance/admission and any registry mutation.

A whole-workflow red status caused by other sidecars is not a blocker for recording this focused candidate, but those failures are not repaired or reclassified by this review.

## Status

`compiled_candidate` only.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
