---
kind: review_result
review_id: review-T-P5-023-sumengchen-20260907T0931
task_id: T-P5-023
agent: 苏梦辰
source_agent: 苏梦辰
related_review:
  - review-T-P5-023-liuguanyi-20260907T0916
inspected_commit: c7e7c2c544907e3f6a4b57a8b95687163e2abf1c
integration_status: compiled_candidate
admission_label: pending
proposed_integration_target: theorem
---

# T-P5-023 — piecewise path transport Lean formalization result

## Result

Formalized the finite algebraic layer of 柳冠一's `T-P5-023` piecewise-cell/path transport result as a portable Lean 4.32 sidecar:

- `examples/routeb_p5_piecewise_transport_lean/P5PiecewiseTransport.lean`
- `examples/routeb_p5_piecewise_transport_lean/README.md`
- `examples/routeb_p5_piecewise_transport_lean/verify.sh`
- `examples/routeb_p5_piecewise_transport_lean/lean-toolchain`

The sidecar deliberately begins after a source/P8 checker has certified a finite connecting segment chain.  It does **not** certify a Julia/Float64 Jacobian, a concrete P8 cell chain, ODE/flowpipe coverage, source provenance, admission, or P5/P8/M4 final closure.

## Kernel interface

Definitions:

```text
forceMap A x a = sum_i A[a,i] x[i]
segmentK Aabs H S s a q = sum_i sum_j Aabs[a,i] H[s,i,j] S[s,j,q]
pathK Aabs H S a q = sum_s segmentK Aabs H S s a q
pathEll2 Aabs H S = sum_a sum_q pathK[a,q]^2
```

Exported theorem decomposition:

1. `telescoping_nat`: exact finite scalar telescoping over `Finset.range R`.
2. `forceMap_abs_le`: triangle inequality for the finite force map.
3. `forceMap_piecewise_abs_le`: after exact residual telescoping, the force-map endpoint difference is bounded by the sum of segmentwise component magnitudes.
4. `segment_expansion`: one segment's `A_abs * H * S` nested finite sum is reindexed into `segmentK`.
5. `path_expansion`: all segment coefficients compose into `pathK`.
6. `piecewise_component_transport`: if each segment has typed contracts
   `|dxi[s,j]| <= sum_q S[s,j,q]|dz[q]|` and
   `|de[s,i]| <= sum_j H[s,i,j]|dxi[s,j]|`,
   then any post-telescoping force residual satisfying the explicit component bound obeys
   `|rc[a]| <= sum_q pathK[a,q]|dz[q]|`.
7. `frobenius_centered_gain`: finite row-wise Cauchy converts the component bound into
   `sum_a rc[a]^2 <= (sum_a,q K[a,q]^2)(sum_q dz[q]^2)`.
8. `piecewise_centered_gain`: combines 6+7 into the P5 consumer
   `sum_a rc[a]^2 <= pathEll2(Aabs,H,S) * sum_q dz[q]^2`.
9. `piecewise_force_centered_gain`: specialization where `rc` is exactly one force map applied to the sum of raw residual increments.  Raw-PMI/generalized-force normalization is represented by this single `A`, so it must not be applied a second time upstream or downstream.
10. `unbridged_endpoint_jump`: explicit failure boundary showing that a positive endpoint jump can coexist with zero local budget if there is no connecting-path premise.  Hence endpoint membership in disconnected/local cells plus local Jacobian bounds is not sufficient for the P5 centered-gain theorem.

## Real GitHub Actions compile/fix loop

First real Actions run:

- run `34137746763`
- job `101792553250`
- Lean `4.32.0`

The new sidecar failed for two concrete Lean-4.32 issues:

```text
P5PiecewiseTransport.lean:59:8: unexpected token 'in'; expected ','
P5PiecewiseTransport.lean:277:4: try 'simp' instead of 'simpa'
```

The missing `telescoping_nat` axiom report was downstream of the parse failure.  All other exported piecewise theorems in that run already typechecked and printed only standard axioms.

Repair commit `c7e7c2c544907e3f6a4b57a8b95687163e2abf1c` changed the range-sum syntax to the Lean-4.32 form `sum r ∈ Finset.range R, ...` and removed the `warningAsError`-triggering unnecessary `simpa`; theorem statements and mathematical constants were not weakened.

Second real Actions run:

- run `34138219941`
- job `101794028062`
- head `c7e7c2c544907e3f6a4b57a8b95687163e2abf1c`
- Lean `4.32.0`

The focused sidecar emitted:

```text
AXIOM_AUDIT=PASS
P5_PIECEWISE_TRANSPORT_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_piecewise_transport_lean/verify.sh
```

All ten exported theorems printed exactly the standard dependency set
`[propext, Classical.choice, Quot.sound]`; no `sorryAx` appears in this sidecar.

The overall portable-sidecars job still concludes red only because two unrelated pre-existing sidecars fail:

- `examples/anthropic_flt_quotient_transport_sidecar/verify.sh`: bad `../local_fkg` relative `cd` path.
- `examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`: unused `hκ1`, invalid projection from a disjunction, and `sorryAx` in the zero-kappa branch.

Those tasks were not claimed or modified here.

## Remaining interface obligations

The finite Lean algebra is now compiled.  Upstream source/P8 work must still produce a **certified connecting cell/segment chain or an equivalent path-variation contract**, with the local `H`, state transport `S`, and the endpoint residual telescoping tied to the same source domain.  Cell-local derivative bounds without such a connection are insufficient, as `unbridged_endpoint_jump` records in the kernel.

Still outside this sidecar are the cell-local FTOC/calculus step that generates each `de` contract, a possible straight-segment/path-weighted `Hbar` simplification, concrete Julia/Float64 Jacobian semantics, P8 cell/flowpipe coverage, ODE existence/continuation, and the numeric consumer that evaluates the resulting `pathEll2` against the P5 barrier.

Status: `compiled_candidate` only. **待封不觉独立验证 / 待梁智炜最终整合**。
