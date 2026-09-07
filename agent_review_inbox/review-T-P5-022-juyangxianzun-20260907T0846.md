---
kind: review_result
review_id: review-T-P5-022-juyangxianzun-20260907T0846
task_id: T-P5-022
source_agent: 巨阳仙尊
agent: 巨阳仙尊
claimed_at: 2026-09-07T08:30:00-06:00
created_at: 2026-09-07T08:46:00-06:00
upstream_review: review-T-P5-022-liuguanyi-20260907T0820.md
inspected_commit: af350193a4b9a16e7a2bf27fe2b9d857c3047d88
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_then_coordinator_harvest_without_source_or_registry_promotion
---

# T-P5-022 — Lean formalization of coordinate-aware centered-gain / anchor transport

## Result

The finite-sum mathematical adapter from 柳冠一's `T-P5-022` review is now a
portable Lean 4.32.0 sidecar:

```text
examples/routeb_p5_coordinate_transport_lean/
  P5CoordinateTransport.lean
  README.md
  lean-toolchain
  verify.sh
```

The sidecar compiles in the real GitHub pinned environment with
`-DwarningAsError=true`, emits axiom reports for every public theorem, and its
focused verifier reports

```text
AXIOM_AUDIT=PASS
P5_COORDINATE_TRANSPORT_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_coordinate_transport_lean/verify.sh
```

This is a formalized algebraic adapter only.  It does not establish a concrete
source Jacobian, Float64 increment theorem, P8 flowpipe/domain coverage, ODE
continuation, P5/P8/M4 closure, or registry admission.

## Inspected mathematical input

Upstream review:

```text
agent_review_inbox/review-T-P5-022-liuguanyi-20260907T0820.md
```

The mathematical contract is the source-to-consumer chain

```text
|dxi_j| <= sum_k S[j,k] |dz_k|
|de_i|  <= sum_j H[i,j] |dxi_j|
|rc_a|  <= sum_i Aabs[a,i] |de_i|

K[a,k] = sum_i sum_j Aabs[a,i] H[i,j] S[j,k]
ell2    = sum_a sum_k K[a,k]^2
```

followed by the centered-gain consumer

```text
sum_a rc_a^2 <= ell2 * sum_k dz_k^2.
```

For an anchor box `|braw_i| <= c_i`, the second interface is

```text
b_a = sum_i A[a,i] braw_i
C_a = sum_i |A[a,i]| c_i
B2  = sum_a C_a^2

sum_a b_a^2 <= B2.
```

## Lean theorem decomposition

The sidecar defines the typed finite tables and exposes the following public
lemmas.

### Transport table and reindexing

```lean
transportedK
transportEll2
anchorRow
anchorB2
forceMap
```

```lean
transportedK_nonneg
```

proves that nonnegative `Aabs`, `H`, and `S` tables give nonnegative transported
entries `K[a,k]`.

```lean
transport_expansion
```

is the pure finite-sum distributivity/reindexing identity

```text
sum_i Aabs[a,i] *
  (sum_j H[i,j] * (sum_k S[j,k] * |dz_k|))
=
sum_k K[a,k] * |dz_k|.
```

### Component source contract -> transported row bound

```lean
component_transport
```

consumes only the already-typed component contracts and proves

```text
|rc_a| <= sum_k K[a,k] |dz_k|.
```

The proof is finite-sum monotonicity plus `transport_expansion`; no calculus,
matrix inverse, square root, or operator norm appears in this theorem.

### Frobenius squared-gain consumer

```lean
frobenius_centered_gain
```

uses Mathlib's finite Cauchy inequality row by row and proves

```text
sum_a rc_a^2
<=
(sum_a sum_k K[a,k]^2) * (sum_k dz_k^2).
```

The composed theorem

```lean
transported_jacobian_centered_gain
```

therefore directly produces the `ell2` shape consumed by `T-P5-020` /
`T-P5-021` from the source-facing component contracts.

### Force-map anchor transport

```lean
forceMap_abs_le
force_map_anchor_box_to_B2
```

formalize the arbitrary finite force map and component anchor box.  The latter
proves exactly

```text
sum_a forceMap(A,braw)_a^2
<=
anchorB2(|A|,c).
```

No explicit `c_i >= 0` theorem argument is needed after the stronger source
premise `|braw_i| <= c_i` is supplied: the row bound itself proves the required
nonnegativity.  Keeping that sign premise out of the public theorem avoids a
redundant interface and passes `warningAsError` without disabling the linter.

### Route-B force-coordinate arithmetic

The following exact rational lemmas are also compiled:

```lean
raw_pmi_channel4_square_scale
raw_pmi_channel5_square_scale
channel4_double_normalization_factor
channel5_double_normalization_factor
```

They record

```text
(x/5)^2  = x^2/25
(x/10)^2 = x^2/100
```

and prove that accidentally applying the same normalization a second time
charges another factor `1/25` or `1/100`.  These are arithmetic guardrails for
the typed `raw_pmi_force` versus `generalized_force` distinction; they do not
claim which tag a concrete source object has.

## Interface minimization found during formalization

The upstream source contract naturally emits `S[j,k] >= 0`.  Once the actual
state inequality

```text
|dxi_j| <= sum_k S[j,k] |dz_k|
```

has already been proved, however, entrywise nonnegativity of `S` is not needed
by `component_transport` or by the final squared-gain theorem.  It is therefore
kept only in `transportedK_nonneg` as a checker-facing sanity lemma rather than
as a redundant hypothesis on the main consumer.

This is an interface simplification only; it does not authorize a source
checker to emit an untyped or semantically invalid `S`.

## GitHub Actions evidence

Compiled head:

```text
af350193a4b9a16e7a2bf27fe2b9d857c3047d88
```

Lean sidecar blob:

```text
examples/routeb_p5_coordinate_transport_lean/P5CoordinateTransport.lean
blob sha: 83e91c93ac6c2af4ff57c4752bdfec3d5a28071e
```

Workflow/job:

```text
Lean agent sidecars
run: 34134033353
job: 101780888665
runner: ubuntu-24.04
Lean: 4.32.0
Lake: 5.0.0-src+8c9756b
Mathlib revision used by local_fkg: 81a5d257c8e410db227a6665ed08f64fea08e997
```

The log for this sidecar contains all eleven axiom reports and then:

```text
AXIOM_AUDIT=PASS
P5_COORDINATE_TRANSPORT_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_coordinate_transport_lean/verify.sh
```

Every printed theorem in this sidecar depends only on

```text
[propext, Classical.choice, Quot.sound]
```

and no `sorryAx` occurs in this sidecar.

The shared workflow job is nevertheless red because other independent lanes
still fail.  In the same real log:

1. `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` still enters
   the wrong relative `../local_fkg` path;
2. `examples/routeb_p5_weighted_dual_residual_lean/verify.sh` still has the
   unused `hκ1`, invalid projection from a disjunction, and corresponding
   `sorryAx` in its zero-κ branch.

Neither failure is in `T-P5-022`; this round did not preempt those owners.

## Portable verification contract

`verify.sh` contains `CI_PORTABLE=1`, resolves both `lake` and `lean` from
`PATH`, compares its local `lean-toolchain` against
`examples/local_fkg/lean-toolchain`, invokes

```text
lake env lean -DwarningAsError=true P5CoordinateTransport.lean
```

and fails if an expected axiom report is absent or if `sorryAx` appears.
There is no machine-specific absolute path.

## What remains outside this sidecar

The following are still open physical/source obligations and must not be
silently imported into this compiled theorem:

1. the actual consumer-to-source state ordering/scaling and same-domain
   component transport matrix `S`;
2. a force-coordinate tag and the corresponding `A`, applied exactly once;
3. certified exact-real Jacobian/increment bounds `H`, or a direct centered
   increment theorem for non-smooth Float64/controller/solve pieces;
4. nominal-anchor component boxes on the same nominal flowpipe;
5. routing of every non-block source coordinate as common, transported,
   expanded-consumer, or additive/transverse;
6. P8 nominal flowpipe/domain coverage, initial-state binding, ODE
   existence/continuation, and deployed source semantics.

In particular, the finite-sum theorem intentionally starts after the FTOC /
Jacobian-to-increment step.  It does not turn a smooth exact-real derivative
bound into a theorem about a discontinuous lifted IEEE rounding map.

## Admission boundary

`compiled_candidate` only.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.  No P5/P8/M4 or registry
status is changed by this result.
