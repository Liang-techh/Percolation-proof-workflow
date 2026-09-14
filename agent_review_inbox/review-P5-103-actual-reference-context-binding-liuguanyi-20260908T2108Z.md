---
kind: review_result
review_id: review-P5-103-actual-reference-context-binding-liuguanyi-20260908T2108Z
task_id: P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING
source_agent: 柳冠一
created_at: 2026-09-08T21:08:00Z
inspected_commit: febe9541e36e38f5070bcb4a0ef1ffc7b7a61d41
status: INITIAL_REFERENCE_IDENTITY_BRIDGE_PROVED_GENERAL_TIME_INSTANCE_MISSING
integration_status: pending
admission_label: pending
actual_reference_packet_found: false
initial_match_bridge_closed: true
canonical_zero_residual_reference_math: true
general_time_qbar_vbar_bound: false
referenceKey_source_binding: false
lbar_source_binding: false
source_binding_proven: false
lean_run: false
lake_run: false
producer_run: false
registry_mutated: false
formal_certificate_allowed: false
P5_closed: false
requested_action: bind either a canonical nominal-reference generator with same initial block state and same input/context, or provide a real paired nominal output packet; do not require stored qbar/vbar at t0 once initial identity is proved
---

# P5-103 — actual reference context: no paired source packet found; initial-time reference can be reduced to an identity theorem

## 0. Result

梁智炜 revision 874 asked specifically for a same-context
`qbarB/vbarB/referenceKey/lbar` packet, or an exact missing-field report.
The current GitHub-tracked source inspections still do **not** contain such a
paired packet.  In particular, the actual residual evaluator exposes the
formula `nominal_f` but not a selected nominal trajectory; the actual trajectory
export is block-only and unpaired; the compact file whose name contains
`nominal` is a remote-acceleration descriptor reference, not nominal block
position/velocity; and T-P5-018 is a conditional same-forcing theorem, not an
instantiated source reference.

There is nevertheless a useful mathematical reduction that removes an
unnecessary source obligation at the **initial time**: if the nominal reference
is selected by the same initial block state and same input/model spec, then the
hybrid anchor budget at `t0` equals the ordinary full-state budget exactly.  No
separate stored numerical `qbarB(t0),vbarB(t0)` is needed.  A second theorem
shows how a canonical zero-residual nominal reference may be generated from a
linear block ODE, so a whole nominal trajectory can be identified by a compact
reference spec rather than by a pre-exported table.

This does **not** recover general-time `qbarB(t),vbarB(t)` from the actual output,
and it does not turn `nominal_f` into a deployed source theorem.  General-time
centering remains pending until either a reference generator is source-bound or
a paired nominal output/flowpipe is supplied.

## 1. Evidence boundary: what is and is not present

The following already-recorded actual-source inspections were re-read:

1. `review-P5-098-ANCHOR-BUDGET-INSTANTIATION-20260908T202703Z.md`:
   `routeB_descriptor_residual_interface.jl` contains `nominal_f` and the full
   actual `M\\R` residual evaluator, but no `qbar/vbar` initial data, nominal
   solution table, `referenceKey`, or `lbar` table.  Its origin regression row
   fixes only actual `q=v=0,w=0`.
2. The same review records that `routeB_export_traj.jl` exports actual block
   `q4,q5,dq4,dq5` (plus aggregate fields), not paired nominal block states and
   not the remote eight coordinates needed for a general-time hybrid budget.
3. `routeB_compact_nominal_descriptor_interface.csv` uses "nominal" for the
   remote acceleration/reference elimination; it is not a selected
   `qbarB/vbarB` trajectory.
4. `review-P5-CENTERED-ANCHOR-INSTANTIATION-20260908T200937Z.md` gives a valid
   conditional anchor construction once `qbarB/vbarB/lbar` are selected, but
   explicitly leaves that actual reference identity open.
5. `review-T-P5-018-guyuefangyuan-20260907T0634.md` supplies the mathematical
   same-forcing incremental equation and the optional ideal `lbar=0` route, but
   its same-initial-state premise is not itself source data.
6. `NEW_REVIEW_P5_EXACT_DH_CELL_SOURCE_JET_CONTRACT_20260908.md` adds exact
   `M,DM,R,DR` coefficient extraction for an analytic cell; it does not add a
   nominal trajectory/reference key or `lbar` instance.

Therefore the exact missing fields in the present committed evidence are:

```text
ReferenceContextInstance:
  contextKey        -- model/controller/input/state-map semantics identity
  referenceKey      -- identity of the selected nominal-reference construction
  t0
  qbarB0, vbarB0    -- OR a proof they equal the selected actual block initial data
  referenceLaw      -- nominal block ODE / graph used after t0
  inputIdentity     -- same w/input law as the actual centered consumer
  lbarLaw           -- zero-residual law, or an independently certified lbar(t)
```

For a general time `t`, either `qbarB(t),vbarB(t)` (or certified enclosures) must
be evaluable from `referenceLaw/referenceKey`, or an actual paired nominal
output/flowpipe must be supplied.  A string/hash key alone cannot supply the
mathematical state.

## 2. Bridge lemma A — initial hybrid budget is exactly the full budget

Let `B={4,5}` and `D={1,2,3,6}`.  Use the P5-098 full-state weights

```text
pFull(q,v) = (3/2) sum_{i=1}^6 q_i^2 + (4/5) sum_{i=1}^6 v_i^2,
pD(q,v)    = (3/2) sum_{i in D} q_i^2 + (4/5) sum_{i in D} v_i^2,
pB(qB,vB)  = (3/2) sum_{i in B} q_i^2 + (4/5) sum_{i in B} v_i^2.
```

### Theorem `hybridBudget_eq_full_of_block_match`

Assume at the selected initial time

```text
qbarB = projB(q),
vbarB = projB(v).
```

Then, by a literal partition of the finite sums,

```text
pD(q,v) + pB(qbarB,vbarB) = pFull(q,v).                 (A1)
```

No dynamics, source equality, matrix inverse, or numerical approximation is
used.  Thus the already-recorded initial-ball fact

```text
sum_i (q_i^2+v_i^2) <= (3/20)^2 = 9/400
```

implies

```text
pD(actual0)+pB(nominal0)
  = pFull(actual0)
  <= (3/2)*(9/400)
  = 27/800
  < 28/5.                                                (A2)
```

The exact slack is `4453/800` as in P5-098.  The important interface change is
that the source lane need not export four duplicate nominal numbers at `t0` if
it can instead prove the stronger and cleaner identity

```text
referenceInitialBlock = actualInitialBlock.             (A3)
```

This turns P5-098's conditional arithmetic into a reusable theorem consumer;
it does **not** prove that the deployed reference generator actually chooses
(A3).

## 3. Bridge lemma B — initial centered anchor is the actual point

Use the P5 centered-anchor map: preserve all remote/context coordinates and
replace only `(qB,vB)` by `(qbarB,vbarB)`, then recompute graph-dependent fields
from the same deterministic source semantics.

### Theorem `anchor_eq_self_of_initial_block_match`

If (A3) holds and the graph-dependent fields are defined by the same functional
source/unique graph at identical primitive inputs, then

```text
anchor(X0) = X0.                                         (B1)
```

Consequently for the centered residual

```text
rc(X) := l(X)-l(anchor(X)),
```

we have

```text
rc(X0)=0.                                                 (B2)
```

This is stronger than merely asserting `z(X0)=0`: it records the required
same-source/determinism premise that makes the recomputed acceleration and
residual equal.  It still does **not** imply the bias vanishes.  With
`bias=l(anchor)-lbar`, (B1) only gives

```text
bias(X0)=l(X0)-lbar(t0).                                  (B3)
```

Hence setting `lbar=0` requires a separate reference-law theorem.

## 4. Bridge lemma C — canonical zero-residual nominal reference exists and is unique

The T-P5-018 nominal block equation has the form

```text
M qbar'' + D qbar' + B qbar = g w(t),                    (C1)
```

with constant 2x2 matrices and positive diagonal `M`.  More generally this
argument applies to whichever exact semantics is selected for `Mref` and the
source nominal coefficients; it does not identify the Float64 execution with a
particular rational idealization.

Let `zbar=(qbar,vbar)`.  Since `M` is invertible, (C1) is the first-order system

```text
zbar' = A zbar + b w(t),                                 (C2)
A = [[0,I],[-M^{-1}B,-M^{-1}D]],
b = [0,M^{-1}g].
```

For continuous `w`, the variation-of-constants formula

```text
zbar(t)
 = exp(A(t-t0)) z0
   + integral_{t0}^t exp(A(t-s)) b w(s) ds               (C3)
```

is a global solution, and standard linear-ODE uniqueness makes it the only
solution with initial state `z0`.  In particular, if the reference initial
state is chosen as the actual block initial state, the tuple

```text
RefSpec = (exact model semantics, input law w, t0, actual qB0, actual vB0)
```

mathematically determines a unique nominal block trajectory.  Two candidate
references with the same `RefSpec` are equal for all common times.  Therefore a
`referenceKey` need not encode/export a whole trajectory: it may identify this
`RefSpec`, provided the source/workflow proves that the key really denotes it.

Define the nominal residual with the same sign convention as T-P5-018,

```text
lbar(t) := g w(t) - (M qbar'' + D qbar' + B qbar).       (C4)
```

Then (C1) gives exactly

```text
lbar(t)=0 for every t.                                    (C5)
```

So there are two legitimate interface branches:

```text
canonical-zero-residual branch:
  referenceKey -> RefSpec
  qbar/vbar := unique solution of (C1) with the keyed initial data
  lbar := 0 by (C5)

external-nominal-remainder branch:
  referenceKey -> externally selected qbar/vbar/lbar law
  lbar must remain an explicit source-bound function
```

The current committed source/output trail proves neither branch is the deployed
selection.  It only exposes enough formulas to make the first branch a precise
mathematical construction once the coordinator chooses/binds it.

### Division-free source-facing variant

The trusted source contract does not need to store `M^{-1}`.  It may carry the
graph form

```text
qbar' = vbar,
M vbar' = g w - D vbar - B qbar,                         (C6)
```

plus positive diagonal/non-singularity of `M`.  Equation (C5) then follows by
substitution.  Matrix inversion is only a proof-of-existence device, not a
checker operation.

## 5. Why the missing fields are real: two exact obstructions

### 5.1 A vector-field formula does not select a reference

Even the scalar zero-forcing system `q''=0` has both

```text
qbar_1(t)=0,
qbar_2(t)=1
```

as zero-residual solutions.  Therefore a `nominal_f`/ODE formula and input law
without initial/reference identity do not determine `qbar/vbar`.  The missing
`referenceKey` or equivalent initial-data selection is mathematically
essential, not bookkeeping noise.

### 5.2 Pointwise qbar/vbar do not determine lbar

At one time, fixing `qbar,vbar,w` does not fix the residual in

```text
lbar = g w - M abar - D vbar - B qbar
```

unless the nominal acceleration/graph law is also fixed.  Different `abar`
produce different `lbar` at the same point.  Thus an output table containing
only `qbar/vbar` would still be insufficient for the nonzero-remainder branch;
`lbar=0` is valid only after binding the zero-residual reference law.

## 6. Minimal typed contract recommended downstream

```text
structure NominalReferenceSpec where
  contextKey       : ContextKey
  referenceKey     : ReferenceKey
  t0               : Real
  qB0 vB0          : Vec2
  sameInput         : InputLawIdentity
  modelIdentity     : NominalModelIdentity
  initialBinding    : qB0 = actual_qB(t0) /\ vB0 = actual_vB(t0)

structure CanonicalNominalReference extends NominalReferenceSpec where
  qbar vbar        : Real -> Vec2
  graph            : forall t, qbar'(t)=vbar(t) /\
                     M*vbar'(t)=g*w(t)-D*vbar(t)-B*qbar(t)
  initial          : qbar(t0)=qB0 /\ vbar(t0)=vB0
```

Derived fields/theorems rather than duplicated inputs:

```text
lbar_zero                  -- from graph
reference_unique_same_spec -- from linear ODE uniqueness
hybrid_budget_initial_eq   -- from initialBinding
anchor_initial_eq_self     -- with same-source graph determinism
centered_residual_initial_zero
```

If the workflow instead consumes an external nominal trajectory, replace
`graph/lbar_zero` by an explicit `qbar/vbar/lbar` source packet and a
`referenceKey` binding theorem.  Do not mix the two branches.

Suggested Lean leaves:

```text
hybridBudget_eq_full_of_block_match
anchor_eq_self_of_block_match
nominalResidual_eq_zero_of_graph
nominalReference_unique_of_same_initial
```

The first and third are finite-sum/algebra leaves and should be very small.  The
ODE uniqueness leaf can be postponed if the source exports a reference; it is
mathematically useful only for the canonical-generator branch.

## 7. Remaining boundary

This review closes a **mathematical/interface reduction**, not the actual
reference source binding.  Still open:

- proof that deployed/current P5 chooses the canonical zero-residual reference,
  or a real paired nominal output packet;
- binding of `referenceKey` to model semantics, input law and initial data;
- general-time evaluation/enclosure of qbarB/vbarB;
- if not canonical zero-residual, actual lbar(t) and its equation;
- source/Float64 reification for the actual residual evaluator and Mref;
- same-domain/path/FD halo, P8 flowpipe, Lean/kernel, independent verification,
  comparator/admission and registry.

The exact actionable next source witness is therefore smaller than
"export an entire nominal trajectory": for initial-budget closure, provide the
same-context identity `nominalInitialBlock = actualInitialBlock`; for general
centering, additionally bind a canonical reference generator key (or export a
paired nominal state/remainder packet).  Until one of those is present, P5-103
remains pending rather than falsely filling qbar/vbar/lbar with zero.
