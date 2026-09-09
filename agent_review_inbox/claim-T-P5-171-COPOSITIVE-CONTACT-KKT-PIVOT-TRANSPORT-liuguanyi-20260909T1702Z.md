---
type: review_claim
review_id: RVW-T-P5-171-COPOSITIVE-CONTACT-KKT-PIVOT-TRANSPORT-LGY-20260909T1702Z
task_id: T-P5-171-COPOSITIVE-CONTACT-KKT-PIVOT-TRANSPORT
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T17:02:00Z'
lease_expires_at: '2026-09-09T18:02:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-170-iterated-sign-compatible-pivot-energy-chain-honglianmozun-20260909T1657Z, review-T-P5-169-sharp-floor-contact-localization-kuangmanmozun-20260909T1640Z, review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909]'
---
# Review Claim — copositive contact/KKT transport through pivot reduction

## Scope
Close the support-stationarity seam between T-P5-170 and the sharp-floor/support-kernel machinery of T-P5-159/T-P5-169. Prove that a terminal nonnegative zero contact of a certified copositive core carries the exact cone-KKT/complementarity conditions, and that the division-free T-P5-170 backward pivot lift transports those conditions to the original matrix without re-solving a KKT system.

## Route
1. Prove the finite-dimensional cone fact: if `M` is copositive, `z>=0`, and `z^T M z=0`, then `Mz>=0` and `z_i(Mz)_i=0` coordinatewise; on the positive support, the principal block has `M_SS z_S=0`.
2. For one sign-compatible pivot `M=[[b,-r^T],[-r,A]]`, `S=bA-r r^T`, prove the exact vector identity `M(r^T z, b z)=(0,Sz)` in addition to the known quadratic lift.
3. Iterate the identity through a T-P5-170 pivot chain and show terminal complementarity, FAIL gradients, and full-kernel contacts transport exactly to the original coordinates.
4. State the active-support consequence: a terminal zero contact yields an explicit positive principal-kernel witness for the lifted original support, so determinant/root sharpness checks need not re-run support KKT in the unreduced dimension.
5. Record the strict-complementarity boundary: an eliminated pivot can lift with zero coordinate and zero gradient, so strict inactive inequalities / uniqueness of the active set are not preserved automatically.

No provenance/receipt/admission work, no Lean compile, no runtime/Float64 claim, and no registry mutation.