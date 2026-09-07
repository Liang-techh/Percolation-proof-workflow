---
kind: review_result
review_id: review-T-P5-010-fengbujue-20260907T0107
task_id: T-P5-010
source_agent: 封不觉
created_at: 2026-09-07T01:07:00-06:00
integration_status: pending
admission_label: compiled_candidate
review_of: review-T-P5-010-juyangxianzun-20260907T0047
inspected_commit: f4654e3612bbe2f17628bffd2b58fa7c9097aadd
proposed_integration_target: theorem
requested_action: coordinator_harvest_as_pending_metadata_only
---

# T-P5-010 independent final gate — cubic small-gain sidecar

## Verdict

**`compiled_candidate` confirmed. No P5/M4 promotion.**

I independently checked the theorem statements, the portable verifier, the pinned Lean/Lake environment, the GitHub-hosted job, the decoded job log, and the source/hash boundary. The focused sidecar itself really compiled on GitHub Actions and its exported theorem set is zero-`sorryAx` with only the standard Mathlib axioms. The aggregate workflow is red only because other portable sidecars fail; this path is explicitly recorded as `SIDECAR_RESULT=PASS` in the real job log.

The result is nevertheless only a source-independent consumer layer. It does **not** prove the deployed central-FD tensor bound, the P8 velocity/energy sublevel coverage, controller/solve bias closure, or any physical P5/M4 parent theorem.

## Version / provenance chain

Reviewed formalization result:

- `agent_review_inbox/review-T-P5-010-juyangxianzun-20260907T0047.md`
- formalized source commit: `f4654e3612bbe2f17628bffd2b58fa7c9097aadd`
- mathematical parent: `review-T-P5-010-youhunmozun-20260907T0026.md`

Exact sidecar blobs at the compiled commit:

- `examples/routeb_p5_cubic_small_gain_lean/P5CubicSmallGain.lean`
  - Git blob `cf8577b62ee1a0b1f202f2f9f041d960631377f5`
- `examples/routeb_p5_cubic_small_gain_lean/verify.sh`
  - Git blob `6f0235f5c94ae5354e006bf4131572ff373a2141`
- `examples/routeb_p5_cubic_small_gain_lean/lean-toolchain`
  - Git blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`
  - value `leanprover/lean4:v4.32.0`

The sidecar toolchain matches `examples/local_fkg/lean-toolchain` at the same commit. The reused Lake environment is repository-pinned: its `lake-manifest.json` fixes Mathlib at `81a5d257c8e410db227a6665ed08f64fea08e997` and the workflow separately checks out `anthropics/formal-math` at `795efb86f191735c5481675763537cfb4ff37e55`.

`verify.sh` is portable for the unified CI lane: it contains `CI_PORTABLE=1`, discovers `lake` from `PATH`, checks toolchain identity, uses a repository-relative Lake root, runs `lean -DwarningAsError=true`, requires an axiom report for each declaration, and rejects `sorryAx`, Lean errors, and missing modules.

## Independent theorem-statement audit

### 1. `scaled_young_division_free`

Statement:

```text
2 ai aj x y <= aj^2 x^2 + ai^2 y^2
```

This is exactly the square identity consequence `(aj*x-ai*y)^2 >= 0`; no positivity assumptions are required. It is a valid reusable algebra kernel, but by itself it is **not** the six-dimensional tensor/row-weight certificate from the mathematical parent.

### 2. `cubic_relative_small_gain`

Statement:

```text
dE <= -A + PC + PR + PB
PC <= kC*A
PR <= kR*A
=> dE <= -(1-kC-kR)*A + PB
```

Semantics are correct. The formal theorem intentionally needs fewer hypotheses than the explanatory mathematical review: nonnegativity of `A`, `kC`, `kR` and `kC+kR<1` are unnecessary for this non-strict algebraic composition itself.

### 3. `cubic_relative_small_gain_strict`

The theorem adds exactly the assumptions needed for strict decay at the consumer level:

```text
A > 0,
kC+kR < 1,
PB <= 0,
```

plus the previous power upper bounds. No independent `kC>=0` / `kR>=0` premise is mathematically needed for this implication once `PC<=kC*A` and `PR<=kR*A` are supplied.

### 4. `cubic_absorption_of_energy_sublevel`

Statement:

```text
0 <= A,
0 <= Lambda,
0 <= kappa,
PC^2 <= Lambda*A^3,
A <= R^2,
Lambda*R^2 <= kappa^2
=> |PC| <= kappa*A
```

This is semantically correct and matches the square-root-free consumer proposed by the mathematical review. Important boundary: the sidecar **assumes** `PC^2 <= Lambda*A^3`; it does not formalize the weighted Cauchy-Schwarz derivation from the actual central-FD tensor envelope. Therefore this theorem does not verify the mathematical review's tensor formula for `Lambda` or any deployed value of `Lambda,R,kappa`.

### 5. `nonzero_cubic_ray_not_globally_quadratic_absorbable`

The Lean theorem correctly proves that for fixed nonzero scalar cubic coefficient `c` and positive quadratic coefficient `a`, no finite real `kappa` can dominate `|c| t^3` by `kappa*a*t^2` for every `t>=0`.

This is a genuine one-ray scaling obstruction and is sufficient once a physical/mathematical lane has identified a nonzero cubic ray. It is **not** by itself the fully general theorem about every nonzero homogeneous cubic form on `R^6`; that general conclusion still requires selecting a ray `v0` with nonzero cubic value.

## GitHub Actions kernel evidence

Unified workflow:

```text
.github/workflows/lean-agent-sidecars.yml
```

Directly inspected run/job:

```text
run_id   = 34092184909
job_id   = 101647828389
head_sha = f4654e3612bbe2f17628bffd2b58fa7c9097aadd
runner   = ubuntu-24.04
job      = portable-sidecars
job conclusion = failure (aggregate)
```

The job log confirms checkout of exactly `f4654e3612bbe2f17628bffd2b58fa7c9097aadd`, checksum-verified Elan installation, Lean `4.32.0`, Lake `5.0.0-src+8c9756b`, and Mathlib revision `81a5d257c8e410db227a6665ed08f64fea08e997`.

Relevant decoded log block:

```text
Running examples/routeb_p5_cubic_small_gain_lean/verify.sh
LEAN_TOOLCHAIN=leanprover/lean4:v4.32.0
... six declarations depend on axioms [propext, Classical.choice, Quot.sound] ...
AXIOM_AUDIT=PASS
P5_CUBIC_SMALL_GAIN_FOCUSED_CHECK=PASS
FD_TENSOR_SOURCE_BINDING=OPEN
P8_VELOCITY_SUBLEVEL_COVERAGE=OPEN
CONTROLLER_SOLVE_BIAS_CLOSURE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_cubic_small_gain_lean/verify.sh
```

No `sorryAx` appears in this sidecar's theorem set.

The aggregate job failure does not invalidate the focused result. The same log identifies unrelated failures in:

- `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` — bad relative Lake path;
- `examples/routeb_p5_weighted_dual_residual_lean/verify.sh` — its own Lean/linter/projection errors including `sorryAx` in that separate theorem set.

The workflow at this commit deliberately runs all `CI_PORTABLE=1` scripts, emits a per-sidecar `SIDECAR_RESULT`, and only fails the aggregate step after collecting all focused results. Thus `SIDECAR_RESULT=PASS` for this path is valid kernel-facing evidence despite the overall red job.

Observed command semantics / exit evidence for this sidecar are therefore:

```text
bash examples/routeb_p5_cubic_small_gain_lean/verify.sh
focused exit code = 0  (witnessed by the workflow `if bash "$script"; then ... PASS` branch)
aggregate portable-sidecars step exit code = 1 due to other sidecars
```

## Admission / DAG boundary

The following gates remain open and prevent any stronger label:

1. **FD tensor source binding:** no same-domain theorem yet binds deployed central-FD Christoffel mismatch to the `PC^2 <= Lambda*A^3` premise or to a concrete tensor/matrix certificate.
2. **Domain coverage:** no P8/first-exit proof yet supplies the same-domain velocity box or energy sublevel `A <= R^2` needed by the local cubic absorber.
3. **Bias closure:** controller/solve/additive power bias is not yet proved nonpositive/zero on the same domain; therefore the strict consumer cannot be instantiated physically.
4. **Parent dependency closure:** the abstract consumer does not close P5, M4, flowpipe, source semantics, receipt freshness, or the verified registry.
5. **Integrator provenance:** at review time, current `scripts/integrate_agent_reviews.py` has no `TASK_TARGETS["T-P5-010"]` mapping, so the deterministic inbox integrator will not create a processed marker for this task until the coordinator explicitly maps it. This is a harvest/provenance issue, not a kernel failure.

## Minimal return tasks

- **To the P3/source lane:** prove the exact deployed central-FD tensor-error contract or a coordinate-weighted certificate that supplies the premise consumed by this sidecar; do not substitute samples or hash equality for semantic binding.
- **To the P8/coverage lane:** provide the same-domain velocity/energy sublevel used to instantiate `A <= R^2` (or a coordinate box for the alternate matrix certificate).
- **To the P5 bias lane:** close `PB <= 0` / zero-bias under explicit deployed hypotheses, or retain the ultimate-bound architecture instead of claiming strict decay.
- **To 梁智炜:** if T-P5-010 is to be harvested by the deterministic integration pass, add a fail-closed `TASK_TARGETS` mapping to the P5 node as pending metadata only. Do not promote the registry from this review.

## Final gate label

```text
mathematical consumer semantics: PASS
GitHub-hosted Lean/kernel compile: PASS (focused path)
#print axioms: PASS; standard Mathlib axioms only
portable provenance/toolchain pin: PASS
FD tensor/source binding: OPEN
same-domain coverage: OPEN
controller/solve bias closure: OPEN
P5/M4/registry admission: NOT SATISFIED
```

**Final admission label: `compiled_candidate`.**
