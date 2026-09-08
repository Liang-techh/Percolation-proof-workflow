---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-ENERGY-NORMALIZATION-20260908T170235Z
task_id: GH-MATH-P4-ACTIVE-ENERGY-NORMALIZATION
source_agent: codex-block-ball-envelope-lane
created_at: 2026-09-08T17:02:35Z
integration_status: pending
admission_label: pending
status: UNIFORM_SYMBOLIC_ENVELOPE_DERIVED_SOURCE_PREMISES_OPEN
proof_status: conditional_paper_inequalities_not_kernel_verified
source_binding_proven: false
initial_bound_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
generated_numeric_bounds: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
predecessor_review: agent_review_inbox/review-GH-MATH-P4-ACTIVE-ENERGY-NORMALIZATION-20260908T165726Z.md
predecessor_sha256: ddfef47af70c8c8f120f76531d82965cd8128c9282476526fbb231bf3a6ef5df
requested_action: prove the same-source regularized mass and linear-anchor premises, then use the joint-ball envelope or direct centered bound without double charging the cross term
---

# Joint-ball envelope for T-W and the existing initial scalar

Only this new review is written. This consumes the supplied revision-804
expression identity through the hashed predecessor; no state is read or
modified. No Julia, Lean/Lake, producer, regression or numerical bound runs.
All new bounds below are symbolic conditional formulas, not certified numeric
constants or an actual initial-storage witness.

## 1. Joint-ball domain and same-source premises

Fix B=(4,5). On the CURRENT block-only X0, q_E=v_E=0 and
`||q_B||^2+||v_B||^2<=r^2`, where r is the producer's INITIAL_RADIUS.
The existing sidecar uses zero-based state slots(3,4,9,10) in order q then v.
This is a combined ball, not two independently saturated balls or a box.

The existing DeltaQ is supported at joints2/3, so its quadratic vanishes on
X0. The confirmed difference therefore restricts exactly to

```text
D(q,v):=T-W=-2*g_B^T q_B+eps*q_B^T M_BB(q)*v_B.
```

Let m>=0 be a PROVED uniform Euclidean operator upper bound for the SAME
regularized M_BB(q) on the X0 configuration projection. Let gamma>=0 satisfy
||g_B||<=gamma for the SAME source linear compensation. These are witness
parameters, not assigned values. A bound for the full regularized M also
implies the principal-block bound by coordinate projection. An unregularized
or differently configured mass bound cannot be substituted.

## 2. Rigorous uniform absolute envelope

Write a=||q_B||, b=||v_B||. Cauchy and the operator bound give

```text
|D| <= 2*gamma*a + |eps|*m*a*b.
```

Since a^2+b^2<=r^2, a<=r and 2ab<=r^2. Thus the whole closed X0 satisfies

```text
|T-W| <= delta_X,
delta_X := 2*gamma*r + |eps|*m*r^2/2.
```

This is a uniform non-strict bound. Strict initial/sublevel inclusion requires
an additional strict budget inequality; the closed-ball geometry alone does
not turn <= into <. No value of delta_X is calculated or exported.

The signed transfer directions before absolute relaxation are

```text
W=T+2*g_B^T q_B-eps*q_B^T M_BB v_B,
W<=T+delta_X,   T<=W+delta_X.
```

The minus sign on the cross term and plus sign on the compensation in W-T
are retained. When g_B=0 is actually proved, gamma can be zero in this
conditional formula; an origin value identity does not prove that premise.

If tighter correlation matters, a sufficient symbolic envelope is any value
dominating `2*gamma*a+|eps|*m*a*sqrt(r^2-a^2)` for all 0<=a<=r. No optimizer,
square-root constant or tighter numeric value is introduced. The simple
delta_X is deliberately conservative because its two summands need not
attain their maxima at the same state.

## 3. Regularizer remains in the bound

If M=M_base+mu I, the cross term is
`q_B^T M_base,BB v_B + mu*q_B^T v_B`.
The envelope m must already cover this regularizer. Alternatively, a verified
unregularized norm bound m_base and exact source mu support
`m=m_base+|mu|` as a conditional norm estimate. Do NOT add the regularizer
again after using an already regularized m. Its contribution vanishes at
the origin but not throughout X0.

## 4. Exact interface to the current scalar: two routes, not one double debit

Fresh reading of `routeB_compact_energy_storage_to_block_audit.py:44-51`
shows the existing scalar is built as

```text
u_csv = [max(h/2,m_csv/2)+eps*m_csv/2]*r^2,
```

where h, m_csv and eps are its DECLARED potential-Hessian, mass and cross-term
parameters. The cross-term allowance is already present. Their declarations
are not verified same-function bounds merely because they are rational.

### Route A: transport an independently established bound on T

If a genuine raw-value theorem gives T<=u_T on X0, then W<=u_T+delta_X.
For Z=W+b_shift, Z<=u_T+delta_X+b_shift. These are sufficient comparisons,
not claims that an added delta_X is mathematically necessary for every
initial proof. If the source theorem instead bounds the centered T-U(0),
restore U(0) as well; no Hessian theorem chooses that origin anchor.

Using u_csv as u_T REQUIRES its raw T value-level witness. The current producer
does not supply that witness. If it already bounded T with a cross-term
allowance, adding delta_X is conservative transport, not a claim of exact
cross-term cancellation or a sharp required loss.

### Route B: directly bound centered W, avoiding redundant cross-term loss

On X0 the targeted gain increment vanishes. Suppose the same-source potential
P(q_B)=U(q)+quadratic_controller(q) satisfies the anchored upper bound

```text
P(q_B)-P(0) <= (h/2)*||q_B||^2,
```

and M_BB(q)<=m*I as quadratic forms. The first premise needs the value/linear
anchor (or an independently proved anchored inequality), not just a Hessian
number. The linear compensation g_B is kept separate. Then

```text
W-U(0) <= max(h/2,m/2)*r^2 + gamma*r.
```

If g_B=0 is proved and h,m are bound to the actual source values used by
u_csv, this direct centered W upper bound is <=u_csv because the existing
eps*m/2 allowance is nonnegative. Thus a direct centered-W proof can reuse
the scalar conservatively WITHOUT adding another cross-term charge. It
does not require the generally false pointwise inequality W<=T.

If g_B is not proved zero, gamma*r must be accounted for or absorbed by a
separately verified slack. This review does not assign gamma, evaluate slack,
or claim any existing declared bound is sound.

Crucially, Route B bounds W-U(0), NOT raw W. Raw W needs the anchor restored;
Z additionally needs its existing shift. This is the remaining normalization
obstruction even when the original cross-term allowance is ample.

## 5. What is now closed mathematically, and what is still missing

The joint-ball absolute envelope and direct centered-W envelope are explicit
conditional inequalities. They refine the prior origin-only analysis and
show why “the scalar lacks a cross-term allowance” would be inaccurate:
its source formula already contains one. The missing evidence is instead:

- source-bound m/h for this regularized mass and restricted potential;
- g_B identity or a certified linear compensation envelope with correct sign;
- the raw/centered value anchor of the function actually bounded;
- the function-indexed initial inequality and consistent active threshold.

For strict inclusion use the selected target upper < the target threshold;
no such gate is evaluated here. Source expression equality, domain map and
actual storage semantics remain prerequisites. Neither the new symbolic
envelope nor existing CSV continuity constitutes VERIFIED/source admission.

Inspected paths: the predecessor review; the external storage-to-block
producer and targeted strictification declarations; workspace
`examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STORAGEIDENTITY20260907.lean`.
Only read-only inspection and paper inequalities were used. No old artifacts,
state, registry or other agent files were changed.
