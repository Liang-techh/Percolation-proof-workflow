---
kind: review_result
review_id: review-T-P4-012-juyangxianzun-20260907T0144
task_id: T-P4-012
source_agent: 巨阳仙尊
claimed_at: 2026-09-07T01:34:00-06:00
created_at: 2026-09-07T01:44:00-06:00
inspected_commit: 233187bd15b973d1ec14f5261189f7930bed94ed
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_by_封不觉_then_harvest_by_梁智炜_Codex
---

# T-P4-012 — remote mass-metric transfer Lean sidecar

## Scope

This pass formalizes the source-independent mathematical core of
`review-T-P4-012-youhunmozun-20260907T0130.md`. It does not identify any
abstract quadratic form with the deployed Julia/Float64 DH implementation, does
not prove a P8 distal-acceleration energy enclosure, and does not close P4/M4.

## Portable Lean artifact

Created:

- `examples/routeb_p4_remote_mass_transfer_lean/P4RemoteMassTransfer.lean`;
- `examples/routeb_p4_remote_mass_transfer_lean/README.md`;
- `examples/routeb_p4_remote_mass_transfer_lean/verify.sh`;
- `examples/routeb_p4_remote_mass_transfer_lean/lean-toolchain`.

The sidecar pins `leanprover/lean4:v4.32.0`, matching
`examples/local_fkg/lean-toolchain`. `verify.sh` contains `CI_PORTABLE=1`,
resolves `lake` from `PATH`, checks the local-FKG toolchain before compiling,
and uses no user-specific absolute path.

## Theorem decomposition

The sidecar proves the inverse-free block-PSD arithmetic seam first:

```lean
theorem remote_scaled_cross_bound_division_free
    (theta QB C QD : ℝ)
    (hpsd : 0 ≤ theta ^ 2 * QB + 2 * theta * C + QD) :
    -(theta ^ 2) * QB - QD ≤ 2 * theta * C
```

and the direct P4 consumer:

```lean
theorem remote_schur_absorption
    (theta QB C QD P d y : ℝ)
    (htheta : 0 < theta)
    (hpsd : 0 ≤ theta ^ 2 * QB + 2 * theta * C + QD)
    (hP : theta * QB ≤ P)
    (hQD : QD ≤ theta * d * y ^ 2) :
    0 ≤ P + 2 * C + d * y ^ 2
```

Thus a future typed matrix adapter only needs to supply the scaled PSD
evaluation, the comparison `theta*QB ≤ P`, and one distal-energy scalar bound;
the Lean consumer itself has no matrix inverse and no entrywise `M_BD` premise.

For the componentwise reserve route the sidecar proves:

```lean
theorem remote_component_reserve
    (U gamma c E r y : ℝ)
    (hU : 0 ≤ U) (hc : 0 ≤ c)
    (hr : r ^ 2 ≤ U * E)
    (hE : E ≤ gamma * y ^ 2)
    (hUg : U * gamma = c ^ 2) :
    |r| ≤ c * |y|
```

and exact rational specializations:

```text
U4     = 280441/2400000
gamma4 = 138240/280441
U4*gamma4 = (6/25)^2
1/100 + 6/25 = 1/4

U5     = 40147/800000
gamma5 = 48020/40147
U5*gamma5 = (49/200)^2
1/200 + 49/200 = 1/4.
```

Concrete corollaries therefore return

```text
r4^2 ≤ U4*E, E ≤ gamma4*q5^2  => |r4| ≤ (6/25)|q5|,
r5^2 ≤ U5*E, E ≤ gamma5*q4^2  => |r5| ≤ (49/200)|q4|.
```

These are still abstract conditional statements; the corrected `1/100` and
`1/200` `kc` coefficients are only arithmetic consumers here, not a fresh
source-binding claim.

## GitHub Actions focused compile

The portable sidecar was exercised by GitHub Actions at head
`63b0e2cef066b6011b55994f8ceed08d3e328a80`:

```text
workflow: Lean agent sidecars
run_id:   34096491306
job_id:   101661281423
runner:   ubuntu-24.04
Lean:     4.32.0
Lake:     5.0.0-src+8c9756b
```

The real job log records:

```text
Running examples/routeb_p4_remote_mass_transfer_lean/verify.sh
LEAN_TOOLCHAIN=leanprover/lean4:v4.32.0
...
AXIOM_AUDIT=PASS
P4_REMOTE_MASS_TRANSFER_FOCUSED_CHECK=PASS
FLOAT64_DH_SOURCE_BINDING=OPEN
P8_DISTAL_ENERGY_COVERAGE=OPEN
P4_FULL_RESIDUAL_COMPOSITION=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_remote_mass_transfer_lean/verify.sh
```

All fourteen printed theorem/constant corollary declarations depend only on

```text
[propext, Classical.choice, Quot.sound]
```

and no `sorryAx` appears in this sidecar theorem set.

The aggregate workflow job concludes `failure` only because two disjoint
portable artifacts still fail elsewhere in the same fail-closed harness:

1. `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` still has the
   known bad relative `../local_fkg` path;
2. `examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`
   still has the known unused `hκ1` warning-as-error and invalid projection from
   a disjunction, producing `sorryAx` in its zero-kappa branch.

The new T-P4-012 sidecar itself is explicitly marked `SIDECAR_RESULT=PASS` in
the same run. I did not modify the two unrelated owner lanes.

## Remaining formalization/source boundary

Still open and intentionally outside this result:

- a typed finite-dimensional bridge from the actual exact-real DH mass block
  PSD statement to the abstract `hpsd` scalar evaluation;
- Float64/source-semantic binding or a perturbation enclosure;
- same-domain P8/source proof of `a_D^T D a_D` (or a compatible surrogate)
  satisfying the needed local `y`-relative bound;
- the exact comparison between the P4 positive quadratic `P` and the physical
  local mass quadratic `QB`;
- composition with the other P4 force residual channels without double charge.

Therefore this is only a `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**. No registry, DAG parent, authoritative gate, or final conclusion was changed.
