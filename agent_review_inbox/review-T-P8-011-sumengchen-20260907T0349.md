---
kind: review_result
review_id: review-T-P8-011-sumengchen-20260907T0349
task_id: T-P8-011
source_agent: 苏梦辰
claimed_at: 2026-09-07T03:38:00-06:00
created_at: 2026-09-07T03:49:00-06:00
inspected_commit: 6f350c03ddd8a635bb14ea89461ae4e2dd9013a1
integration_status: compiled_candidate
admission_label: pending
proposed_integration_target: theorem
requested_action: independent_validate_ramp_tube_sidecar_then_bind_source_domain_and_12d_flowpipe
---

# T-P8-011 — ramp-tube / pullback-domain bridge: Lean sidecar and CI result

## Scope

This is a formalization-only follow-up consuming the mathematics in
`review-T-P8-011-guyuefangyuan-20260907T0332.md` (古月方源) and the already compiled
first-12 adapter in `examples/routeb_p8_first12_adapter_lean/`.  I did not redo
large-scale mathematical exploration.  The formalized seam is deliberately
source-independent:

- fixed-time injectivity of the exact ramp graph in `(mechanical state,c)`;
- exact graph-lift membership for a 12-state mechanical tube;
- exact pulled-back 13-state source-domain contract along `w=c*t`;
- square-only rational ramp-tail cap;
- a rational counterexample to reusing the current `|w|<=1/100` source box through
  `T=1`;
- the elementary anisotropic Lipschitz substitution from a 13-state source
  mechanical map to the explicit-time 12-state field.

Concrete Julia `full_rhs!` authentication, Float64 regularity, interval/cell
enclosure, ODE existence/continuation, actual flowpipe coverage, terminal
admission, provenance, registry mutation, and P8/M4 closure are out of scope.

## Lean artifact

New portable sidecar:

- `examples/routeb_p8_ramp_tube_transport_lean/P8RampTubeTransport.lean`
  - blob `14089ff33b220f9eaedd2e1375e86a3351d801f8`;
- `examples/routeb_p8_ramp_tube_transport_lean/verify.sh`
  - blob `06f527604349cd1c98b75d7038d26114c40d5764`;
- `examples/routeb_p8_ramp_tube_transport_lean/lean-toolchain`;
- `examples/routeb_p8_ramp_tube_transport_lean/README.md`.

The child imports `P8First12Adapter`, which already pins the typed source/adapter
seam.  `verify.sh` is marked `CI_PORTABLE=1`, resolves `lake` from `PATH`, checks
the child toolchain against `examples/local_fkg/lean-toolchain`, and compiles the
full focused dependency chain with `-DwarningAsError=true`:

1. `RouteBP8PicardStep.lean`;
2. `P8ContractAdapter.lean`;
3. `P8First12Adapter.lean`;
4. `P8RampTubeTransport.lean`.

No machine-specific Lean or Lake path is hard-coded.

## Formalized statements

### 1. Exact projection and fixed-time graph injectivity

```lean
theorem proj12_rampLift (m : State12) (c t : ℝ) :
  proj12_14 (rampLift m c t) = m

theorem rampLift_injective_mc
    {m1 m2 : State12} {c1 c2 t : ℝ}
    (h : rampLift m1 c1 t = rampLift m2 c2 t) :
    m1 = m2 ∧ c1 = c2
```

The proof reads the first twelve coordinates and the final `c` slot.  It does
not require `t!=0`; the `w=c*t` coordinate is redundant for injectivity in
`(m,c)`.

### 2. Exact graph tube and membership equivalence

```lean
def RampTube
    (B : ℝ -> ℝ -> State12 -> Prop) (C : ℝ -> Prop)
    (t : ℝ) (z : State14) : Prop :=
  exists m c, C c ∧ B t c m ∧ z = rampLift m c t

theorem rampTube_on_ramp_iff ... :
  RampTube B C t (rampLift m c t) <-> C c ∧ B t c m
```

This freezes the intended geometry: the 14-state object is an exact graph over a
12-state mechanical tube plus external parameter `c`, not a Cartesian product
with independent `w,c` boxes.

A small set-level consumer is also formalized:

```lean
theorem mechanical_coverage_lifts ... :
  (forall t, I t -> B t c (m t)) ->
  forall t, I t -> RampTube B C t (rampLift (m t) c t)
```

under the explicit parameter premise `C c`.

### 3. Pulled-back source domain

```lean
def PullbackDomain
    (D13 : State13 -> Prop) (c t : ℝ) (m : State12) : Prop :=
  D13 (pack13 m (c*t))
```

and `pullbackDomain_iff` unfolds this contract exactly.  No additional
independent `w,c` source-domain premise is introduced.

### 4. Square-only ramp-tail domain cap

```lean
theorem ramp_tail_sq_cap
    (hc : c^2 <= 3)
    (ht0 : 0 <= t) (htT : t <= T) (hT : 0 <= T)
    (hcap : 3*T^2 <= W^2) :
    (c*t)^2 <= W^2
```

The implementation uses only ordered-ring arithmetic and square nonnegativity;
there is no square-root API in this downstream theorem.

### 5. Rational obstruction to the current local `w` box

```lean
theorem current_w_box_not_T1 :
  exists c t : ℝ,
    c^2 <= 3 ∧ 0 <= t ∧ t <= 1 ∧ |c*t| > (1:ℝ)/100
```

The kernel witness is simply `c=1,t=1`.  Thus an unchanged source contract
`|w|<=1/100` cannot cover the full target family through `T=1`; this obstruction
is independent of mechanical dynamics and separate from the old source-tail
semantic mismatch.

### 6. Regularity substitution identity

```lean
theorem ramp_tail_distance (c t1 t2 : ℝ) :
  |c*t1-c*t2| = |c|*|t1-t2|
```

and the source-independent transport theorem

```lean
theorem explicitMechanical_lipschitz_transport ...
```

shows that any typed premise

```text
||M_S(pack13(x1,w1))-M_S(pack13(x2,w2))||
  <= Lm||x1-x2|| + Lw|w1-w2|
```

immediately yields

```text
||G_c(t1,m1)-G_c(t2,m2)||
  <= Lm||m1-m2|| + Lw|c||t1-t2|.
```

This is only an implication from a regularity premise.  It does **not** assert
that the real lift of the deployed Float64 program is continuous or Lipschitz.

## Real GitHub Actions result

The portable sidecar ran in real GitHub Actions:

- workflow: `Lean agent sidecars`;
- run: `34107571992`;
- job: `101696400270` (`portable-sidecars`);
- compiled head: `6f350c03ddd8a635bb14ea89461ae4e2dd9013a1`;
- Lean `4.32.0`;
- Lake `5.0.0-src+8c9756b`.

The log for this sidecar reports:

```text
AXIOM_AUDIT=PASS
P8_RAMP_TUBE_TRANSPORT_FOCUSED_CHECK=PASS
SOURCE_MECHANICAL_BINDING=OPEN
ODE_CONTINUATION=OPEN
FLOWPIPE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p8_ramp_tube_transport_lean/verify.sh
```

All nine printed theorems depend only on
`[propext, Classical.choice, Quot.sound]`; no `sorryAx` appears in this child.

The aggregate `portable-sidecars` job still concludes `failure`, but the failures
are outside this claim and are visible separately in the same real CI log:

- `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` still fails at
  `cd: ../local_fkg: No such file or directory`;
- `examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`
  still has the existing unused `hκ1`, invalid projection from a disjunction,
  and `sorryAx` in the zero-kappa branch.

I did not modify, claim, or reinterpret either unrelated artifact.

## What is now formalized versus still open

The following source-independent implication chain is now kernel-compiled:

```text
12D mechanical tube for fixed/partitioned c
  -> exact RampTube graph lift in 14D
```

and source queries may be stated on the exact pullback

```text
D13(pack13(m,c*t)).
```

This removes any formal need to independently propagate the two solved ramp tail
coordinates merely to establish the graph relation.  It does **not** provide the
actual 12D tube.

Remaining physical/formal obligations are:

1. bind concrete Julia `full_rhs!` first twelve outputs to the `sourceMechanical`
   contract from `T-P8-008`;
2. certify the source domain along `PullbackDomain`, likely by time/parameter
   cells with `w=c*t`-aware interval hulls;
3. replace or partition the current `|w|<=1/100` local box before any claim of
   coverage to `T=1`;
4. prove/consume the exact-real or execution-robust regularity premises needed
   for ODE existence/continuation;
5. produce the actual `[0,1]` 12-state mechanical flowpipe and only then use the
   graph-lift theorem;
6. compose with `T-P8-009`/terminal consumers behind the existing source,
   coverage, verification, and admission gates.

## Status

`compiled_candidate` only.  No P8/M4 final conclusion and no registry state was
changed.

**待封不觉独立验证 / 待梁智炜最终整合。**
