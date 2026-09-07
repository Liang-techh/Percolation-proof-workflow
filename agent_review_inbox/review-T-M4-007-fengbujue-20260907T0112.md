---
kind: review_result
review_id: review-T-M4-007-fengbujue-20260907T0112
task_id: T-M4-007
source_agent: 封不觉
created_at: 2026-09-07T01:12:00-06:00
integration_status: pending
admission_label: compiled_candidate
review_of: review-T-M4-007-sumengchen-20260907T0018
inspected_commit: f4654e3612bbe2f17628bffd2b58fa7c9097aadd
proposed_integration_target: theorem
requested_action: harvest_as_pending_metadata_only
---

# T-M4-007 independent final gate — pure tail-budget transfer

## Verdict

**`compiled_candidate` confirmed. No M4/registry promotion.**

The source-independent arithmetic child is semantically correct, the exact rational identity is correct, and the unchanged sidecar blob is independently observed compiling in the GitHub-hosted pinned Lean environment with no `sorryAx` and only standard Mathlib axioms.

This validation does **not** cover the ramp integral, a physical same-domain `rhoBar` bound, P7 source binding, P8 existence/flowpipe/coverage, terminal `L/g` source premises, or any M4 parent admission.

## Provenance / immutable artifact

Reviewed result:

- `review-T-M4-007-sumengchen-20260907T0018.md`
- mathematical parent: `review-T-M4-006-daai-xianzun-20260906T2346.md`

Exact sidecar blobs, unchanged at inspected commit `f4654e3612bbe2f17628bffd2b58fa7c9097aadd`:

- `M4TailBudgetTransfer.lean`: `88737af4367e435e5d5e0752af04b3b601488352`
- `verify.sh`: `16da37d85e96c777ed420904959f9ea66fad0e24`
- `lean-toolchain`: `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`
- toolchain value: `leanprover/lean4:v4.32.0`

The verifier is portable: `CI_PORTABLE=1`, repository-relative Lake root, `lake` discovered from PATH, toolchain equality check, `-DwarningAsError=true`, explicit axiom-report checks, and fail-closed rejection of Lean errors / `sorryAx`.

## Theorem semantics audit

The formalized constants are exactly:

```text
oldGate   = 4483/2000
newGate   = 1401/625
tailScale = 160000
```

and the exact identity

```text
4483/2000 + 16/160000 = 1401/625
```

is correct.

`tail_budget_transfer` exactly formalizes the elementary ledger implication

```text
Dtail <= rhoBar/160000,
Dbase + rhoBar/160000 <= newGate
=> Dbase + Dtail <= newGate.
```

`old_gate_plus_tail_of_rho_le_16` correctly drops the mathematical parent's extra `0 <= rhoBar` premise: that premise is not logically required for the pure implication because division is by the fixed positive `160000`. Physical source lanes may still naturally establish nonnegativity of an actual `rhoBar`; its absence here is not a theorem weakness or hidden physical claim.

`tail_budget_from_slack` is also correct as a pure transitive inequality. Its comment calls `Delta` a nonnegative allowance, but the theorem does not need `0 <= Delta` logically; no downstream physical interpretation should infer nonnegativity unless supplied separately.

Crucial scope boundary: **the sidecar does not formalize `ramp_tail_integral_bound`**. Therefore the cross-branch mathematical step

```text
rho(t), s(t)=c*t, c^2<=3
=> Dtail <= rhoBar/160000
```

remains outside this compiled child. The Lean result begins only after `hDtail` has been supplied.

## GitHub Actions evidence

I independently inspected decoded GitHub-hosted logs from run/job:

```text
run_id   = 34092184909
job_id   = 101647828389
head_sha = f4654e3612bbe2f17628bffd2b58fa7c9097aadd
runner   = ubuntu-24.04
Lean     = 4.32.0
Lake     = 5.0.0-src+8c9756b
```

The job log shows the exact unchanged M4 sidecar blob path executing before aggregate failure elsewhere:

```text
Running examples/routeb_m4_tail_budget_transfer_lean/verify.sh
LEAN_TOOLCHAIN=leanprover/lean4:v4.32.0
RouteBM4TailBudgetTransfer.tail_budget_transfer
  -> [propext, Classical.choice, Quot.sound]
RouteBM4TailBudgetTransfer.old_gate_plus_rho16_exact
  -> [propext, Classical.choice, Quot.sound]
RouteBM4TailBudgetTransfer.old_gate_plus_tail_of_rho_le_16
  -> [propext, Classical.choice, Quot.sound]
RouteBM4TailBudgetTransfer.tail_budget_from_slack
  -> [propext, Classical.choice, Quot.sound]
AXIOM_AUDIT=PASS
M4_TAIL_BUDGET_TRANSFER_FOCUSED_CHECK=PASS
PHYSICAL_RHOBAR_BINDING=OPEN
P8_FLOWPIPE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_m4_tail_budget_transfer_lean/verify.sh
```

Thus focused script exit code is `0`; the aggregate portable-sidecars step exits `1` only because other independent sidecars fail. The shared workflow explicitly records each per-sidecar PASS/FAIL before failing the aggregate job, so the focused M4 compile evidence is valid.

## Admission boundary / unresolved blockers

1. **Ramp integral theorem open:** no kernel proof yet connects the P8 ramp and time-varying `rho(t)` to `Dtail <= rhoBar/160000`.
2. **Physical `rhoBar` source binding open:** no same-domain source theorem yet supplies the relevant normalization/multiplier bound, in particular the useful `rhoBar <= 16` target.
3. **P7 typed/source binding open:** the abstract tail charge has not been established as the deployed Schur tail on the same trajectory.
4. **P8 flowpipe/existence/coverage open.**
5. **Terminal source premises open:** the `L/g` consumer and total residual ledger still need same-domain source/receipt/coverage evidence.
6. **M4/registry admission not satisfied:** this arithmetic sidecar cannot alter the authoritative M4 gate or register a physical theorem.

The integrator currently has an explicit `TASK_TARGETS["T-M4-007"]` fail-closed mapping to `M4.block45_full_certificate`, so this review may be harvested as pending metadata. At validation time, no processed marker for the original T-M4-007 review was yet discoverable; that is a harvest-timing fact, not a proof blocker.

## Minimal return tasks

- **To the formal/math interface lane:** prove the interval/ramp integral bridge separately, with explicit integrability/measurability or an equivalent exact bound; do not fold it silently into this arithmetic child.
- **To the P7/source lane:** supply the same-domain physical `rhoBar` bound and typed tail identification.
- **To the P8 lane:** supply existence/continuation/coverage for the trajectory on which the ramp and tail bound are consumed.
- **To 梁智炜:** harvest this as pending metadata only; no authoritative M4 gate or registry change is justified.

## Final gate label

```text
pure arithmetic theorem semantics: PASS
GitHub-hosted Lean/kernel compile: PASS (focused path)
#print axioms: PASS; standard Mathlib axioms only
portable toolchain/provenance: PASS
ramp-integral bridge: OPEN
physical rhoBar/source binding: OPEN
P8 flowpipe/domain coverage: OPEN
M4/registry admission: NOT SATISFIED
```

**Final admission label: `compiled_candidate`.**
