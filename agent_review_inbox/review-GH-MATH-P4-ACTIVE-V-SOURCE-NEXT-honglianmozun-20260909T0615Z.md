kind: review_result
task_id: GH-MATH-P4-ACTIVE-V-SOURCE-NEXT
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T06:15:00Z
status: BLOCKED_WITH_EXACT_SOURCE_VALUE_BINDING_OBSTRUCTION
claim_commit: adc4cbc2ff740e7a79f536f0707fcde52f844db5
scope: actual runtime/source active-V identity, additive normalization, and same initial_storage_upper binding

# Verdict

The source-form energy ledger is mathematically identifiable, but the current committed repository still does **not** identify which value-level function is the deployed/runtime active `V`, nor does it bind the recorded `initial_storage_upper` to that same selected function/run.

This is now a precise value-normalization obstruction, not a derivative-identity obstruction:

- the committed convention result has `runtime_observation = null`, `source_binding_proven = false`, and `active_function_selected = null`;
- the certificate-indexed initial witness explicitly has `historical_producer_function_binding = None`, `same_run_event_binding = None`, `consumer_function_identity = None`, and `runtime_initial_bound_proven = False`;
- the exact five-point obstruction rejects an exact `sameStorage` edge between the degree-4 certificate polynomial and the same-K energy slice of degree at most 2, while explicitly leaving unrelated initial inequalities untouched;
- the barrier consumer syntactically reads the scalar metric `initial_storage_upper`, but that selector equality does not identify the function whose value is being bounded.

Therefore I cannot honestly instantiate the existing `Body6SliceActualStorage` bridge as the **actual deployed storage** without one new source/value witness. I do not change the active V, threshold, or stored upper.

# Repository/source facts consumed

1. `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907.lean` defines the source-form saved ledger

   `V_saved(q,qd) = KE_6(qd) + U_quad_6(q) + U3_6(q) + U4_6(q) + Ua_6(q)`.

   Its abstract `actualSourceStorageID` is a theorem from an assumed equality for an abstract `V_act`; it is not a producer selector for the deployed runtime function.

2. `examples/routeb_active_v_function_envelope/NEW_CONVENTION_RESULT.json` remains `pending` and says explicitly

   `runtime_observation = null`,
   `source_binding_proven = false`,
   `active_function_selected = null`.

   It records the scalar consumer value

   `U_recorded = 492033745203 / 25600000000000`,

   but deliberately does not select among raw, shifted, centered, or cross-term conventions.

3. `examples/routeb_active_v_function_envelope/NEW_CONVENTION_REVIEW.md` distinguishes, on the pinned ideal same-K slice,

   - raw `W`,
   - shifted `Z = W + c`,
   - centered `F = W - a`,
   - cross-term variants,

   and states that no actual active runtime V follows without source binding. It also notes that the barrier script reads `V0 = initial_storage_upper` while using value-level coercivity/cap/threshold consumers, so a constant shift cannot be ignored merely because derivatives agree.

4. `examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.py` proves a certificate-indexed ideal initial upper, but deliberately returns

   `historical_producer_function_binding = None`,
   `same_run_event_binding = None`,
   `consumer_function_identity = None`,
   `source_binding_proven = False`,
   `runtime_initial_bound_proven = False`.

5. `examples/routeb_active_v_function_envelope/NEW_CONVENTION_identity_obstruction.json` gives an exact finite-difference witness showing that the degree-4 certificate slice cannot equal any degree-<=2 same-K energy slice at all five tested points. It also records `same_run_initial_upper_binding = null`.

# Mathematical closure obtained this round

## 1. Constant-shift ambiguity is invisible to derivative identities

Let `V_act, V_saved : X -> R` and suppose for some constant `c`

`V_act(x) = V_saved(x) + c` for every state `x`.

Along every differentiable trajectory `x(t)`, whenever the two derivatives are defined,

`d/dt V_act(x(t)) = d/dt V_saved(x(t))`.

Hence no Lie-derivative identity, dissipation identity, or energy-power rewrite can determine `c`.

This formally separates two typed obligations:

- derivative equality / energy identity;
- value normalization / active-function identity.

The first cannot discharge the second.

## 2. One exact shared anchor equality kills the whole constant ambiguity

Assume in addition there is one source-identified anchor state `x0` with

`V_act(x0) = V_saved(x0)`.

Evaluating the shift relation at `x0` gives

`V_saved(x0) = V_saved(x0) + c`,

hence

**`c = 0`**,

and therefore

**`V_act(x) = V_saved(x)` for every x`.**

This is the smallest exact mathematical bridge if the only remaining ambiguity is an additive constant.

Lean-shaped candidate statement:

```lean
theorem constantShift_eq_zero_of_anchor
    (Vact Vsaved : X -> Real) (c : Real)
    (hshift : forall x, Vact x = Vsaved x + c)
    (x0 : X)
    (hanchor : Vact x0 = Vsaved x0) :
    c = 0 := by
  have h := hshift x0
  linarith

theorem active_eq_saved_of_anchor
    (Vact Vsaved : X -> Real) (c : Real)
    (hshift : forall x, Vact x = Vsaved x + c)
    (x0 : X)
    (hanchor : Vact x0 = Vsaved x0) :
    forall x, Vact x = Vsaved x := by
  have hc : c = 0 := constantShift_eq_zero_of_anchor Vact Vsaved c hshift x0 hanchor
  intro x
  simpa [hc] using hshift x
```

No inverse, square root, spectral theorem, or runtime evaluation is needed.

## 3. Exact cap transport under a known shift

If

`V_act = V_saved + c`, 

then for every initial state `x0` and every scalar cap `U_act`,

**`V_act(x0) <= U_act  <->  V_saved(x0) <= U_act - c`.**

Equivalently, if source proves

`V_saved(x0) <= U_saved`,

then the corresponding active cap is

**`U_act = U_saved + c`.**

Thus an unchanged numeric `initial_storage_upper` is valid across the shift only after proving `c=0`; otherwise the cap must be rebased by the same constant. The same statement applies to every value-level threshold/sublevel constant consumed downstream.

Candidate theorem:

```lean
theorem shifted_initial_upper
    (hshift : Vact x0 = Vsaved x0 + c)
    (hupper : Vsaved x0 <= U) :
    Vact x0 <= U + c := by
  linarith
```

and conversely with `Uact-c`.

## 4. Sharing the same upper number does NOT identify the normalization

A tempting but invalid inference is

`V_saved(x0) <= U` and `V_act(x0) <= U`

therefore `V_act = V_saved` or `c=0`.

Counterexample:

`V_saved(x0) = 0`, `U = 1`, `c = 1/2`, `V_act = V_saved + 1/2`.

Then both

`V_saved(x0) <= 1`

and

`V_act(x0) <= 1`

hold, while `c != 0` and the functions differ everywhere by `1/2`.

Therefore the repository's scalar selector

`initial_storage_upper = 492033745203/25600000000000`

cannot by itself serve as an anchor/normalization witness. It is an inequality target, not a pointwise function identity.

## 5. Stronger obstruction: the existing certificate polynomial cannot silently be declared the same saved energy

The committed finite exact witness restricts the certificate polynomial to

`t=0, q4=s`, all other q/v coordinates zero,

at five rational points `s = -3/20, -3/40, 0, 3/40, 3/20` with fourth-difference weights `[1,-4,6,-4,1]`.

Its fourth difference is nonzero under both committed interpretations, whereas every polynomial of degree at most 2 has zero fourth difference. Thus the certificate slice cannot agree with the same-K degree-<=2 energy slice at all five points.

Consequently the missing bridge cannot be repaired by merely renaming `routeB_certificate_V.csv` as `V_saved`. A genuine producer relation is required: equality to the actual selected runtime V, or an explicit transformation with every value-level consumer transported consistently.

# Smallest admissible source packet that would close this task

One of the following two forms is sufficient.

### Exact pointwise selector form

Provide a source-identified runtime/deployed function `V_active` and prove on the actual required state/path domain

**`V_active(x) = V_saved(x)`**

with the same `M/U/g/gains/regularizer/state/time` interpretation, plus bind the recorded `initial_storage_upper` to that same `V_active` and initial-set/run identity.

### Explicit constant-shift form

Provide a source-identified `V_active`, a single exact scalar `c`, and prove

**`V_active(x) = V_saved(x) + c`**

on the required domain. Then either:

- provide one exact shared anchor equality, which forces `c=0`; or
- keep `c` and rebase every value-level consumer, beginning with
  `U_active = U_saved + c`.

The same rule must be applied to threshold/sublevel constants. Derivative-only theorems may be reused unchanged, but value-level coercivity, initial inclusion, first-exit thresholds, and p_B-to-V comparisons are not automatically invariant under a shift.

# Candidate typed bridge

A source-facing interface can make the distinction explicit:

```text
ActiveVValueBinding :=
  V_active                 : State -> R
  shift                    : R
  active_eq_saved_shift    : forall x in Domain,
                                V_active x = V_saved x + shift
  initial_state_set        : Set State
  saved_initial_upper      : R
  saved_initial_bound      : forall x in Initial,
                                V_saved x <= saved_initial_upper
  active_initial_upper     : R
  active_cap_rebase        :
                                active_initial_upper = saved_initial_upper + shift
```

If a source anchor proves `shift=0`, this collapses to the simpler exact `Body6SliceActualStorage` equality and the numeric upper may remain unchanged. If not, the shift stays visible and the cap/threshold arithmetic is forced to move with it.

# Failure boundary / no overclaim

- No deployed/runtime active-function selector was found in the committed evidence inspected here.
- No same-run event binding ties `routeB_certificate_V.csv`, `initial_storage_upper`, and the actual consumer evaluation to one selected function.
- The certificate-indexed ideal initial inequality is not promoted to a runtime initial theorem.
- I did not alter the active V formula, threshold `1`, `initial_storage_upper`, controller, state map, source artifacts, or registry.
- No admission, receipt, generic provenance audit, re-audit, Lean/Lake run, Julia run, runtime replay, or registry promotion was performed.

# Remaining obligation

The narrow remaining source obligation is now exactly:

**identify the deployed `V_active` value function and bind it pointwise to `V_saved` (or to `V_saved+c` with exact `c`), then bind `initial_storage_upper` to that SAME function/run with the cap transported by the same normalization.**

Until that witness exists, the correct status is pending/blocked at value-level source identity even though the energy derivative algebra can be reused conditionally.
