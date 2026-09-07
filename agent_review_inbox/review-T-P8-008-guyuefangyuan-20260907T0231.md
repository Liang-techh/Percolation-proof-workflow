---
kind: review_result
review_id: review-T-P8-008-guyuefangyuan-20260907T0231
task_id: T-P8-008
source_agent: 古月方源
claimed_at: 2026-09-07T02:23:00-06:00
created_at: 2026-09-07T02:31:00-06:00
inspected_commit: 99f771cdc8d1aaf2e12ed23b91c9d6b79097208d
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_first12_ramp_elimination_adapter_then_bind_source_mechanical_outputs
---

# T-P8-008 — exact first-12 source projection, ramp elimination, and the unavoidable tail-repair seam

## Scope

This pass resolves the mathematical part of the coordinator-assigned first-12 explicit-time source adapter.  The deployed source is kept exactly as documented: a 13-state field with mechanical outputs in slots `0..11` and literal tail derivative `du[13]=0`.  The adapter is allowed to supply the mathematical ramp tail `w'=c`, `c'=0`, but is **not** allowed to relabel that repaired tail as a source output.

Inspected inputs:

- `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean`, blob `11c8e23a52128e56b65a76024285c45a9070414d`;
- `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean`, blob `0bcac8908b2492ae72279ef0cd05b2d6634bc3a9`;
- `examples/routeb_p8_explicit_time_sidecar/RouteBP8ExplicitTimeSidecar.lean`, blob `0afc58327d9ba0c50143c436d79b13712761c41e`;
- `examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean`, blob `6baf8643631297c0ec33e59d7a224e8fcc1e7319`;
- `docs/routeb-p8-flowpipe-binding-next.md`, blob `c3d9dbf3aa7d1e9fdf4f0583f83c47fcdde83ae0`;
- `review-T-P8-009-sumengchen-20260907T0118.md`, whose interval-local ramp theorem already gives `w(t)=c0*t`, `c(t)=c0` on `[0,1]` for a lifted trajectory under the typed tail derivative hypotheses.

No ODE existence, interval enclosure, flowpipe coverage, Float64 source equality, receipt/provenance, admission, or registry claim is made.

## 1. Minimal typed objects

Let

```text
X12 := R^12,
X13 := R^13 = (mechanical 12, w),
X14 := R^14 = (mechanical 12, w, c).
```

Write

```text
pack13(m,w) := (m,w),
proj12_13(x) := x[0..11],
proj12_14(z) := z[0..11].
```

Let the deployed exact mathematical source interface be an arbitrary field

```text
S : X13 -> X13.
```

For the current source, the separate source fact is

```text
sourceTailZero(S) :  S(x)_w = 0   for every x.                 (1)
```

Nothing below assumes that the 13th source output is a ramp derivative.

Define the source-authenticated mechanical projection

```text
M_S(x) := proj12_13(S(x)) in X12.                              (2)
```

For a fixed external ramp coefficient `c`, eliminate `w` analytically and define the 12-state nonautonomous mechanical field

```text
G_S,c(t,m) := M_S(pack13(m,c*t)).                              (3)
```

This is the smallest explicit-time object that can honestly be called source-derived: every one of its 12 outputs is literally a source mechanical output evaluated at the same `(q,dq,w)` state, with only the input value `w=c*t` supplied by the ramp adapter.

## 2. Exact state-level bridge to the existing 14-state `timeLift`

The existing adapter `P8ContractAdapter.timeLift` can consume the autonomous source by taking

```text
G(t,x) := S(x).
```

Its 14-state field is then

```text
L_S(z)[0..11] = M_S(forgetTail(z)),
L_S(z)_w       = z_c,
L_S(z)_c       = 0.                                          (4)
```

Let the existing ramp state be

```text
R(m,c,t) := rampLift(m,c,t) = (m,c*t,c).                     (5)
```

There are two exact algebraic identities:

```text
forgetTail(R(m,c,t)) = pack13(m,c*t),                         (6)
```

and therefore

```text
proj12_14(L_S(R(m,c,t))) = G_S,c(t,m).                        (7)
```

Moreover the two tail components are exactly

```text
L_S(R(m,c,t))_w = c,
L_S(R(m,c,t))_c = 0.                                         (8)
```

Equivalently, if

```text
tangentRamp(g,c) := (g,c,0) in X14,
```

then the complete vector-field identity is

```text
L_S(R(m,c,t)) = tangentRamp(G_S,c(t,m), c).                  (9)
```

This is the key P8 bridge.  It requires no ODE theorem, no interval argument, and no source-tail reinterpretation.

### Proof

Equation (6) is coordinatewise from the definitions of `forgetTail` and `rampLift`: slots `0..11` are `m`, slot 12 is `c*t`.  Substitution into the first 12 branches of `timeLift` gives (7).  The branch definitions at slots 12 and 13 give (8).  Extensionality over `Fin 14` gives (9).

## 3. Trajectory equivalence after eliminating the ramp tail

Let `m : I -> X12` be a coordinatewise differentiable mechanical path on an interval `I` and define

```text
z(t) := R(m(t),c,t).                                          (10)
```

The derivative of (10), coordinatewise, is

```text
z'(t) = tangentRamp(m'(t),c).                                (11)
```

Combining (9) and (11) gives the exact equivalence

```text
z'(t)=L_S(z(t))
      <=>
m'(t)=G_S,c(t,m(t)).                                         (12)
```

Thus the 14-state lifted ramp dynamics and the 12-state explicit-time mechanical dynamics are the **same trajectory equation after exact elimination of the two tail coordinates**.  No uniqueness assumption is required for this pointwise equivalence.

This also composes directly with T-P8-009 in the reverse direction.  Suppose a typed 14-state solution of `L_S` has initial tail `w(0)=0`, `c(0)=c0` and satisfies the interval-local regularity hypotheses of T-P8-009.  Then on `[0,1]`,

```text
c(t)=c0,
w(t)=c0*t.                                                   (13)
```

Let `m(t)=proj12_14(z(t))`.  Equation (6) becomes

```text
forgetTail(z(t)) = pack13(m(t),c0*t),                         (14)
```

and projecting the first 12 solution equations gives exactly

```text
m'(t)=G_S,c0(t,m(t)).                                        (15)
```

So T-P8-009 plus the algebraic theorem (9) already supplies the complete mathematical trajectory projection.  The remaining P8 source question is only whether the concrete Julia mechanical outputs instantiate `M_S` on the same semantics/domain.

## 4. A 13-state repaired field, and why it must not be confused with the source

For compatibility with the existing explicit-time 13-state sidecar, define a repaired field

```text
R_S,c(x) := pack13(M_S(x), c).                               (16)
```

It preserves the source mechanical outputs exactly:

```text
proj12_13(R_S,c(x)) = proj12_13(S(x)).                        (17)
```

while replacing only the derivative of the `w` coordinate by the adapter value `c`.

Under the actual source-tail fact (1), the difference is exactly one-dimensional:

```text
R_S,c(x) - S(x) = c * e_w,                                   (18)
```

where `e_w` is the 13th coordinate basis vector.

Hence

```text
R_S,c = S   <=>   c=0.                                       (19)
```

For every intended nonzero perturbation parameter, the repaired 13-state field is **not** the deployed source.  It is an adapter that preserves all 12 source mechanical equations and changes exactly one tail equation.

This gives a sharper version of the existing incompatibility statement: the semantic edit needed to pass from the literal 13-state source to a ramp-compatible 13-state system is precisely the rank-one tail update `c e_w`; nothing in slots `0..11` needs to change.

## 5. Direct obstruction to a full 13-state source trajectory with nonzero ramp

Suppose one tries instead to claim that

```text
y(t)=pack13(m(t),c*t)
```

is a trajectory of the literal source `S`.  Its tail derivative is `c`, whereas (1) requires the source tail derivative to be `0`.  Therefore

```text
[y'(t)=S(y(t)) at even one differentiability point] -> c=0.  (20)
```

So no theorem covering the intended family `c^2<=3` may demand full 13-coordinate source equality.  This is a mathematical obstruction, not a missing receipt or a weak enclosure.

The correct source contract is first-12 equality only.

## 6. Source-specific mechanical form

The documented source has

```text
S(q,v,w)[q slots] = v,
S(q,v,w)[v slots] = acc(q,v,w),
S(q,v,w)[w slot] = 0.                                       (21)
```

Substituting (3), the repaired explicit-time system is therefore exactly

```text
q'(t) = v(t),
v'(t) = acc(q(t),v(t),c*t).                                  (22)
```

This is the clean mathematical target for the P8 interval/flowpipe lane.  It uses the real source acceleration function at the real source state `(q,v,w=c*t)`; it does not invent a 14th source input or ask the source to evolve `w`.

## 7. Recommended Lean theorem package

A minimal source-independent formalization should avoid a heavy ODE API and prove the algebra first.

```lean
abbrev State12 := Fin 12 -> R
abbrev State13 := Fin 13 -> R

def pack13 (m : State12) (w : R) : State13 := ...
def proj12_13 (x : State13) : State12 := ...
def sourceMechanical (S : State13 -> State13) (x : State13) : State12 :=
  proj12_13 (S x)

def explicitMechanical (S : State13 -> State13) (c t : R) (m : State12) : State12 :=
  sourceMechanical S (pack13 m (c*t))
```

First algebraic lemma:

```lean
theorem forgetTail_rampLift
    (m : State12) (c t : R) :
    forgetTail (rampLift m c t) = pack13 m (c*t)
```

Main vector-field seam, stated coordinatewise if a `tangentRamp` helper is undesirable:

```lean
theorem timeLift_first12_on_ramp
    (S : State13 -> State13) (m : State12) (c t : R) (i : Fin 12) :
    timeLift (fun _ x => S x) t (rampLift m c t) (embed12_14 i)
      = explicitMechanical S c t m i
```

```lean
theorem timeLift_tail_on_ramp
    (S : State13 -> State13) (m : State12) (c t : R) :
    timeLift (fun _ x => S x) t (rampLift m c t) wSlot = c /\
    timeLift (fun _ x => S x) t (rampLift m c t) cSlot = 0
```

Source-tail repair:

```lean
def repair13 (S : State13 -> State13) (c : R) (x : State13) : State13 :=
  pack13 (sourceMechanical S x) c

theorem repair13_preserves_first12 ...

theorem repair13_eq_source_iff_c_zero
    (S : State13 -> State13)
    (hzero : forall x, S x wSlot13 = 0) :
    repair13 S c = S <-> c = 0
```

For trajectory consumers, use coordinatewise `HasDerivWithinAt` on `[0,1]` to match T-P8-009 rather than introducing a full ODE solution structure.  The final theorem can state that the first-12 derivative equations of a lifted solution are equivalent to `explicitMechanical S c0 t` after T-P8-009 supplies (13).

## 8. What this closes and what remains open

Closed mathematically:

1. exact first-12 source projection after the substitution `w=c*t`;
2. exact vector-field identity between the 14-state `timeLift` on a ramp state and the explicit-time 12-state mechanical field;
3. trajectory-level equivalence after ramp elimination;
4. precise characterization of the 13-state repair as a one-coordinate update;
5. proof that the literal zero-tail source cannot itself carry a nonzero ramp trajectory.

Still open:

- instantiate `S[0..11]` by the concrete Julia `full_rhs!` mechanical outputs with the same DH/FD/solve semantics;
- prove the concrete source evaluation is enclosed on every required cell;
- ODE existence/regularity and continuation;
- `[0,1]` flowpipe coverage;
- terminal downstream physical premises and P8/M4 admission.

## Recommended next action

Formalization lane: implement the four tiny algebraic lemmas above, reusing the existing `timeLift`, `rampLift`, and T-P8-009 interval theorem.  Source lane: bind only the 12 mechanical outputs of `full_rhs!` to `M_S`; keep the literal source tail theorem `S_w=0` as a separate fact.  Flowpipe lane should certify (22), not the impossible full 13-state equation with `w'=0` and `w=c*t` simultaneously.

This result remains `pending`: it is the mathematical source/adapter seam, not source authentication or flowpipe closure.
