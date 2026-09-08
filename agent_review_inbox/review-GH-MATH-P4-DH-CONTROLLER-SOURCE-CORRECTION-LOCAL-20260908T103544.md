---
kind: review_result
review_id: review-GH-MATH-P4-DH-CONTROLLER-SOURCE-CORRECTION-LOCAL-20260908T103544
task_id: GH-MATH-P4-DH-CONTROLLER-SOURCE-CORRECTION
source_agent: Codex-controller-polynomial-readonly-audit
created_at: "2026-09-08T10:35:44-06:00"
inspected_commit: d9aee5bb2e4f08526947c2a712821472bd73862a
integration_status: pending
admission: pending
admission_label: pending
status: CONFIRMED_CONTROLLER_POLYNOMIAL_OMISSION
merge_decision: reject_current_payload_as_complete_DH_preconditioned_equation
source_binding_proven: false
external_files_modified: false
payload_rewritten: false
producer_executed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
requested_action: preserve the current payload as historical; separately authorize a versioned controller-key correction and independent coefficient audit before any source use
---

# DH controller polynomial: exact omission and minimal repair specification

## Conclusion

The current direct preconditioned-force builder omits nonlocal controller
monomials from rows4/5. This is an expression-level defect, not merely a missing
source proof or an overly conservative bound. The exported support confirms
the omission. Current payload must not be merged as the complete equation
printed in its own metadata.

This review is immutable and is the only file added. No external project,
producer, checker or payload is modified or executed. No full regression,
numerical bound generation, Lean/Julia run or source admission.

External root P:

C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized

## 1. Frozen source equation and signs

The relevant dhport_lib.jl declarations and exact_ddq expression are:

    tau = -Kp .* q - (Kd + b_fr) .* dq + G0v
          + (gw_coef .* I_val) .* w
    returned acceleration = Mq \ (tau - Cdq - Gq).

This is Float64 code, not a theorem that an exact real equation holds.
For the producer's analytic chart define k_j=Kp_j, d_j=Kd_j+b_fr_j,
g_j=GwI_j and g0_j=analytic G_j(0), with a fixed scalar w.
The ideal coefficient lists used by the DH builders are:

    k=(1,4/5,7/10,3/5,1/2,2/5)
    d=(13/10,11/10,19/20,4/5,13/20,1/2)
    g=(1,1/2,3/10,1/5,1/10,1/20).

For physical one-based row i, the complete intended analytic preconditioned
residual polynomial is

    P_i = sum_j X_ij [
            sum_k (M_jk(q)+epsilon*delta_jk)*a_k
            + sum_l sum_k C_jlk(q)*dq_l*dq_k
            + G_j(q)
            + k_j*q_j + d_j*dq_j - g_j*w - g0_j
          ],
    epsilon=1/1000000.

Here M is the unregularized analytic mass chart loaded by the producer;
epsilon is added once. The corresponding controller contribution is

    C_i = sum_j X_ij*k_j*q_j + sum_j X_ij*d_j*dq_j
          - (sum_j X_ij*g_j)*w - sum_j X_ij*g0_j.

The q/dq signs are POSITIVE because the residual subtracts tau.
The w and g0 signs are NEGATIVE. q_j and dq_j retain the input coordinate j,
not output row i. Off-diagonal X entries are signed and must not be replaced
by absolute values.

P_i=0 is still an independent actual-acceleration/source obligation; the formula
alone defines a polynomial. Analytic C/G and analytic g0 do not equal the
central-FD runtime quantities merely because controller gains agree.

## 2. Exact source of the discrepancy

P/robot_formal_v1/exact_checks/build_preconditioned_force_balance_identity_dh.py
lines69–70, inside for a in range(6), currently contain

    add(poly, ("q", i + 1), X[i][a] * kp[a] if a == i else Q(0))
    add(poly, ("dq", i + 1), X[i][a] * (kd[a] + bfr[a]) if a == i else Q(0))

Python i,a are zero-based. Two independent issues occur together:
the serialized coordinate is pinned to i+1, and every a!=i contribution is zeroed.
Thus current controller contribution is only

    C_bad_i = X_ii*k_i*q_i + X_ii*d_i*dq_i
              - (sum_j X_ij*g_j)*w - sum_j X_ij*g0_j.

Holding all other producer branches unchanged, the exact correction is

    Delta_i = sum_(j!=i) X_ij*(k_j*q_j+d_j*dq_j)
    C_i = C_bad_i + Delta_i
    P_complete_i = P_bad_i + Delta_i.

No error norm or numerical approximation is used in these identities.
If the complete residual equals zero at some source point, the bad one would
equal -Delta_i there, not automatically zero. If the bad residual were forced
to zero instead, the complete one would equal Delta_i.

The expression discrepancy is independent of any separate correctness audit
of mass/C/G branches. This turn does not certify those branches in full.

## 3. Current payload corroboration and obstruction

Fresh structural reads of the current payload give:

| Output row | Stored q coordinate keys | Stored dq coordinate keys | Same X row's nonzero-token columns |
|---|---|---|---|
| 4 | 4 only | 4 only | 1,2,3,4,5,6 |
| 5 | 5 only | 5 only | 1,2,3,4,5,6 |

All k_j and d_j in the inspected lists are nonzero. Consequently each missing
j!=i coefficient is genuinely nonzero for the stored X. The existing
half_active full-state candidate does not impose all remote q_j/dq_j=0.

A smallest formal-polynomial obstruction is the q1 coefficient:
for i=4 or5 it should be X_i1*k1=X_i1, whereas the current q-kind map has
coefficient zero for that key. A dq1 coefficient is likewise absent.
This is a coefficient mismatch in the declared independent-coordinate chart,
not a sampled acceleration, a trajectory counterexample or a claim that other
source constraints are satisfied. Taking a formal nonzero q1 assignment
exhibits the same Delta discrepancy without proving reachability.

The adjacent centered builder
P/robot_formal_v1/exact_checks/build_force_balance_bridge_dh.py lines75–76
already writes

    q_coeff  = [X[i][j]*kp[j] for j in range(6)]
    dq_coeff = [X[i][j]*damp[j] for j in range(6)].

Its current controller_rows for output4/5 each have six q and six dq coefficients.
That is consistent with the intended controller formula, but it does not
authenticate the entire centered source equation. The centered payload cannot
silently repair the direct payload merely by being listed beside it.

## 4. Minimal repair — specification only, NOT applied

For the current two-row producer, the minimal code change is exactly:

    add(poly, ("q", a + 1), X[i][a] * kp[a])
    add(poly, ("dq", a + 1), X[i][a] * (kd[a] + bfr[a]))

Both the key and the gate must change:
- Removing only a==i incorrectly sums six coefficients into q_i/dq_i.
- Changing only the key still discards all remote coefficients.
- Changing only the outer row loop to range(6) exports the same defective
  diagonal-only controller rule for six rows.
- Multiplying the assembled controller by X a second time is not a correction.

Keep w/g0 signs and common scalar disturbance semantics; retain signed summation.
For the present X, a correctly repaired q/dq-kind map would each contain all
six coordinate keys per selected output row. Do not edit old support counts
or status fields by hand to simulate that result.

A separately authorized implementation should create a new versioned payload
with corrected producer/checker identity, not silently replace the historical
one. Preserve old hashes and record supersession/provenance. Any downstream
normal form, bound or certificate consuming the old byte identity needs an
explicit dependency audit; this review does not assert which downstream
outputs were actually regenerated or affected.

The source currently names centered_split_reference=force_balance_bridge_v1.json
(the historical branch), despite being the DH controller builder. Any proposed
comparison against force_balance_bridge_dh_v1.json must bind that exact DH
reference and hash explicitly; a filename change itself is no proof.

## 5. Small independent checks required before reopening

No checker was run in this task. Inspection of
check_preconditioned_force_balance_identity_dh.py shows checks of status,
controller-source hash and coefficient lists, output row IDs and two support
counts. It does not compare all controller monomial coefficients or prove the
actual residual vanishes. An OK marker from that checker would not detect
this missing-controller issue.

A focused future audit, without broad regression, should:

1. Independently form the expected controller coefficient map indexed by
   (output i, kind q/dq, input j) as X_ij*k_j and X_ij*d_j.
2. Compare every exact coefficient against the serialized polynomial;
   check all twelve q/dq keys per output and reject missing/wrong-coordinate terms.
3. Verify the signed difference new-old equals Delta_i, with unchanged
   mass/C/G/regularizer/w/g0 branches rather than relying on term counts.
4. Compare the controller-only result with the same-hash DH centered row
   coefficient arrays; do not derive the oracle by repeating the faulty loop.
5. Retain row4/5 scope. All6 export and actual source equations are separate
   tasks; this two-line repair cannot establish them.
6. Independently supply actual-source/analytic/FD/runtime alignment and any
   assembly/solve/model defect before asserting P_i(source acceleration)=0.

In particular, no corrected polynomial, syntactic equation label, successful
producer run or source hash match is itself source admission.
The obstruction is confirmed; repair remains unimplemented.

## 6. Exact paths and SHA-256

All paths below are relative to the explicitly fixed external root P.
Each raw SHA was recomputed in this turn.

| Path | SHA-256 |
|---|---|
| robot_formal_v1/exact_checks/build_preconditioned_force_balance_identity_dh.py | 925F3818146E7E4154BFF07EF16CC6C93DB8609AE15BE20A8551B4F15DCA1C5F |
| robot_formal_v1/exact_checks/build_force_balance_bridge_dh.py | A5082A12D267380A01D9E9C7965FBF17FA7FDB62C2D963110DA38A192470AA15 |
| robot_formal_v1/exact_checks/check_preconditioned_force_balance_identity_dh.py | D05BCE02B5ACA1D8B018255B5E813E4C98FD7E04B98A4336F9926CC372512389 |
| robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json | E0969AADE062FE7C7648A655EA95282E8FD27F9EB7D47C3FFC1B38E33C920F48 |
| robot_formal_v1/interval_bounds/force_balance_bridge_dh_v1.json | 3045EA1923148C90C8473C8402C7522E99EEDA2C1590A494322CA3950D76A107 |
| robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |
| routeB_dense_Mq/dhport_lib.jl | AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936 |

Audit performed: source reads, targeted JSON key/list inspection, raw hashes,
and symbolic sign/index reasoning. No numerical bounds or physical test states
were generated; no production file or payload was rewritten.

