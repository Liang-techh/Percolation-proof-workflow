---
kind: review_result
review_id: review-T-P5-113-anchor-defect-power-absorption-honglianmozun-20260909T0057Z
task_id: T-P5-113-ANCHOR-DEFECT-POWER-ABSORPTION
source_agent: 红莲魔尊
created_at: 2026-09-09T00:57:00Z
claim_commit: 5951185d58e60dc19894f55690987ccc79eba539
inspected_commit: 25b713f9fce3a7a007038782c5e6dd852b28b526
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-110-approximate-reference-recentering-honglianmozun-20260908T2358Z.md
    blob_sha: 9ff5e8d7a7fbce4888aa9759c1d2117924cac16a
  - path: agent_review_inbox/review-T-P5-111-flow-domain-recenter-design-liuguanyi-20260909T0003Z.md
    blob_sha: 785a287900b6de8db4252ad9853d9902544e726a
  - path: agent_review_inbox/review-T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET-guyuefangyuan-20260909T0030Z.md
    blob_sha: 5eaefc8d90e09be23c7ccb56182d022a25e80185
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize the two-channel root-free discriminant leaf, then instantiate only after a same-metric power-pairing/dissipation packet binds the T-P5-112 anchor remainder to the P5 energy ledger
commands: exact algebraic derivation; local Fraction sanity check only; no Lean compile or source execution
lean_compile_status: not_run
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-113 — same-cell affine-anchor defect -> Lyapunov power absorption

## 0. New mathematical seam

T-P5-112 gives a finite same-cell affine-anchor error for an implicit graph,
without explicit inversion.  In its direct lower-gain form, if

`r_A = alpha(z1) - alpha(z0) - Dalpha(z0)[z1-z0]`,

then

**(0.1)** `4 gamma Q_A(r_A) <= H2`, with `gamma>0`.

T-P5-110/T-P5-111, on the other hand, already give a centered reference-power
channel and a Lyapunov dissipation `Qd`.  The missing interface is not another
anchor remainder theorem: it is the power theorem that tells the energy ledger
how to consume `r_A` without converting it to coordinatewise absolute caps and
without introducing an arbitrary independent Young split for every channel.

This review closes that pure mathematics child.  It has two parts:

1. a same-metric anchor-defect power transfer;
2. a sharp, square-root-free two-channel aggregation gate for combining that
   power with the existing recentered-reference power.

No source, runtime, coverage, Lean, comparator, or admission result is claimed.

---

## 1. Anchor remainder as a power channel

Let `u` be the velocity/multiplier paired with the graph error in the actual
energy identity, and define

`p_A := <u,r_A>`.

Do **not** assume Euclidean Cauchy unless the physical consumer is Euclidean.
Instead require an explicit compatible quadratic pairing packet:

**(1.1)** `p_A^2 <= Q_U(u) * Q_A(r_A)`.

Assume the same Lyapunov ledger has a dissipation comparison

**(1.2)** `d * Q_U(u) <= Qd`, with `d>0`.

Combining (0.1), (1.1), and (1.2) gives the division-free power inequality

**(1.3)**

`4 gamma d * p_A^2 <= H2 * Qd`.

Proof: multiply (1.1) by `4 gamma d`, use
`4 gamma Q_A(r_A)<=H2` and `d Q_U(u)<=Qd`.  All factors are nonnegative.
No inverse, square root, coordinatewise norm conversion, or scalar acceleration
cap is needed.

### Budget-level corollary

If T-P5-112 has already been consumed into a proposed rational budget

`Q_A(r_A) <= D_A`,

then the smaller interface is simply

**(1.4)** `d * p_A^2 <= D_A * Qd`.

The direct form (1.3) is preferable when the checker wants to avoid introducing
`D_A` or division by `4 gamma`.

### Preconditioner form

T-P5-112 also gives, under its approximate-left-inverse packet,

`4(1-kappa)^2 Q_A(r_A) <= chi H2`.

The corresponding power theorem is

**(1.5)**

`4 d (1-kappa)^2 p_A^2 <= chi H2 Qd`.

Again no reciprocal of `chi`, `d`, or `1-kappa` is required in the trusted
statement.

---

## 2. Root-free sharp aggregation of two squared power channels

The next lemma is source-independent and is the main new reusable result.
Let

`Q >= 0`, `A0>0`, `A1>0`, `B0>=0`, `B1>=0`, `T>=0`,

and suppose two signed powers satisfy

**(2.1)** `A0 p0^2 <= B0 Q`,

**(2.2)** `A1 p1^2 <= B1 Q`.

Define the cross-margin numerator

**(2.3)**

`Delta := T*A0*A1 - B0*A1 - B1*A0`.

Assume the two polynomial gates

**(2.4)** `0 <= Delta`,

**(2.5)** `4*B0*B1*A0*A1 <= Delta^2`.

Then

**(2.6)**

`(p0+p1)^2 <= T Q`.

This is exactly the two-channel worst-case aggregation condition, but written
without square roots and without dividing by `A0 A1`.

### Proof

From (2.1)-(2.2),

`A0*A1*p0^2 <= B0*A1*Q`,

`A0*A1*p1^2 <= B1*A0*Q`.

It remains to control the signed cross term.  Multiplying (2.1) and (2.2)
gives

`A0*A1*p0^2*p1^2 <= B0*B1*Q^2`.

Hence

`(2*A0*A1*p0*p1)^2`
` <= 4*B0*B1*A0*A1*Q^2`
` <= Delta^2 Q^2`.

Because `Delta Q>=0`, this implies

**(2.7)** `2*A0*A1*p0*p1 <= Delta Q`.

If `p0 p1<=0`, (2.7) is immediate; if `p0 p1>0`, it follows by comparing the
nonnegative squares above.  Adding the two diagonal estimates and (2.7),

`A0*A1*(p0+p1)^2`
` <= (B0*A1+B1*A0+Delta)Q`
` = T*A0*A1*Q`.

Since `A0*A1>0`, cancellation of the positive common factor proves (2.6).

### Sharpness / information boundary

Write formally `C0=B0/A0` and `C1=B1/A1`.  If one were allowed square roots,
the worst same-sign saturation is

`T_sharp = (sqrt(C0)+sqrt(C1))^2`.

Conditions (2.4)-(2.5) are exactly its denominator-cleared version:

`T-C0-C1 >= 0`,

`(T-C0-C1)^2 >= 4 C0 C1`.

Thus, given only the two independent squared envelopes (2.1)-(2.2), this gate
cannot be improved.  Equality is approached/attained when both channels saturate
with the same sign.  Any better bound must use extra signed correlation, not a
cleverer Young parameter.

This matters here because the T-P5-110 reference forcing and T-P5-112 anchor
remainder are distinct mathematical channels: splitting each into its own
`theta_j,beta_j` is unnecessary bookkeeping when only their separate squares
are known.

---

## 3. Exact specialization to T-P5-110 + T-P5-112

Let `p_ref` denote the recentered-reference power from T-P5-110.  That child
provides, for `eta>0`,

**(3.1)**

`eta * p_ref^2 <= (1+eta) L_eta(a) * Qd`.

Let the affine-anchor power `p_A` satisfy (1.3):

**(3.2)**

`4 gamma d * p_A^2 <= H2 * Qd`.

Instantiate the generic lemma with

`A0 = eta`,

`B0 = (1+eta)L_eta(a)`,

`A1 = 4 gamma d`,

`B1 = H2`.

For a desired total squared-power coefficient `T`, define

**(3.3)**

`Delta_A`
` := 4 eta gamma d T`
`    - 4 gamma d (1+eta)L_eta(a)`
`    - eta H2`.

Then the completely division-free sufficient-and-sharp gate is

**(3.4)** `0 <= Delta_A`,

**(3.5)**

`16 eta gamma d (1+eta)L_eta(a) H2 <= Delta_A^2`.

Under (3.4)-(3.5),

**(3.6)** `(p_ref+p_A)^2 <= T Qd`.

No `sqrt(H2)`, `sqrt(L_eta)`, inverse mass, or per-channel Young allocation is
present in the trusted gate.

### Preconditioner specialization

If T-P5-112 is consumed through

`4(1-kappa)^2 Q_A(r_A) <= chi H2`,

replace

`A1 = 4 d (1-kappa)^2`,

`B1 = chi H2`.

The same two scalar polynomial conditions then apply verbatim.  This keeps the
approximate-left-inverse packet algebraically separated from the energy ledger.

---

## 4. From total square to Lyapunov collar

Choose `0<=theta<1`, `beta>=0` and put

**(4.1)** `T = 4 theta beta`.

If the discriminant gate from section 3 holds with this `T`, then

`(p_ref+p_A)^2 <= 4 theta beta Qd`.

Since

`(theta Qd + beta)^2 - 4 theta beta Qd`
` = (theta Qd-beta)^2 >= 0`,

and `theta Qd+beta>=0`, we obtain

**(4.2)**

`p_ref+p_A <= theta Qd + beta`.

Therefore any energy identity/inequality of the form

**(4.3)** `Vdot <= -Qd + p_ref + p_A`

immediately yields

**(4.4)** `Vdot <= -(1-theta)Qd + beta`.

If, on the same collar/domain key,

**(4.5)** `Qd >= lambda V`, with `lambda>0`,

then with `nu=(1-theta)lambda>0`,

**(4.6)** `Vdot <= -nu V + beta`.

Thus the T-P5-100/T-P5-096 inward-collar gate is simply

**(4.7)** `beta <= nu R_in`.

The new anchor remainder does not require a new first-exit architecture.  It
enters exactly once through the combined power coefficient.

### Fully expanded direct gate

With `T=4 theta beta`, section 3 becomes

`Delta_A`
` = 16 eta gamma d theta beta`
`   - 4 gamma d (1+eta)L_eta(a)`
`   - eta H2`,

and the two checks are

**(4.8)** `Delta_A >= 0`,

**(4.9)**

`Delta_A^2 >= 16 eta gamma d (1+eta)L_eta(a) H2`.

Together with

**(4.10)** `beta <= (1-theta)lambda R_in`,

these are a pure polynomial/rational interface from the two upstream squared
packets to the collar.

---

## 5. Signed-correlation refinement: where further improvement can come from

The discriminant gate is sharp only under the information model in which the
cross sign between `p_ref` and `p_A` is unknown.  If source/math can prove a
correlated signed packet directly, preserve it.

Suppose, in addition to (2.1)-(2.2), one has

**(5.1)**

`2*A0*A1*p0*p1 <= Bx Q`.

Then expansion gives immediately

`A0*A1*(p0+p1)^2`
` <= (B0*A1+B1*A0+Bx) Q`.

Hence the single linear gate

**(5.2)**

`B0*A1+B1*A0+Bx <= T*A0*A1`

implies `(p0+p1)^2<=TQ`.

`Bx` may be strictly smaller than the worst-case discriminant cross allowance,
and may even be negative.  Thus a true nonlinear/structural cancellation between
the reference forcing and the graph-anchor defect should be consumed here,
not erased by separate norms first.

This is the only way to beat the section-2 worst-case constant without adding
new information.

---

## 6. Rational sanity witness

A small exact example confirms the denominator-cleared gate is non-vacuous.
Take

`eta=1`, `gamma=1`, `d=1`, `L_eta=1/16`, `H2=1/4`,

so

`A0=1`, `B0=1/8`, `A1=4`, `B1=1/4`.

Choose `theta=1/2`, `beta=3/16`; then `T=3/8` and

`Delta = 3/4`.

The discriminant check is exact:

`Delta^2 = 9/16 > 1/2`

while

`4 B0 B1 A0 A1 = 1/2`.

Therefore `(p0+p1)^2 <= (3/8)Q`, hence

`p0+p1 <= (1/2)Q + 3/16`.

This is only a theorem sanity witness; it is not a Route-B source constant.

---

## 7. Exact obstructions and fail-closed boundaries

### 7.1 No positive dissipation comparison, no anchor-power budget

The T-P5-112 state/graph error bound alone does not control energy power.
If `Q_A(r_A)=1` but `u=t` is unconstrained and `Qd=0`, then

`p_A=t`

grows without bound.  A positive same-domain comparison such as
`d Q_U(u)<=Qd` (or an independent state/multiplier cap) is indispensable.

### 7.2 Metric mismatch is not harmless

`Q_A` in T-P5-112 and the dual form appearing in the power pairing must be the
same metric, or connected by an explicit comparator.  A Euclidean bound cannot
be silently consumed as a moving mass-metric bound, and a metric at the anchor
cannot be silently reused at the target state.

### 7.3 Double-counting guard

If the same affine-anchor defect is already included inside the T-P5-110
`p_ref`/`L_eta(a)` source decomposition, it must **not** be added again as
`p_A`.  The present theorem is for a genuinely separate remainder channel.
The source-facing packet must identify the decomposition

`total extra power = p_ref + p_A`

with disjoint semantics, or instead supply one direct total-power square/cross
packet.

### 7.4 Second-jet coverage remains upstream

This review does not weaken T-P5-112's requirement that `H2` cover the whole
physical anchor-to-target path.  Anchor-only curvature, an independent trig-lift
segment, sampling, or pointwise nonsingularity cannot instantiate (0.1).

### 7.5 Worst-case aggregation intentionally ignores helpful correlation

If (5.1) is available, using (3.4)-(3.5) is valid but possibly conservative.
Conversely, without any cross information, claiming a coefficient below the
section-2 discriminant boundary is false: same-sign saturating scalar channels
provide the counterexample.

---

## 8. Candidate theorem statements

Recommended source-independent leaves:

1. `anchor_defect_power_sq_transport`

   Inputs:
   `pairSq <= QU*QA`, `d*QU<=Qd`, `4*gamma*QA<=H2`, nonnegativity.

   Output:
   `4*gamma*d*pairSq <= H2*Qd`.

2. `two_power_square_aggregate_discriminant`

   Inputs:
   `A0>0`, `A1>0`, `B0,B1,Q,T>=0`,
   `A0*p0^2<=B0*Q`, `A1*p1^2<=B1*Q`,
   `Delta>=0`, `4*B0*B1*A0*A1<=Delta^2`,
   `Delta=T*A0*A1-B0*A1-B1*A0`.

   Output:
   `(p0+p1)^2<=T*Q`.

3. `two_power_square_aggregate_of_signed_cross`

   Consume direct `2*A0*A1*p0*p1<=Bx*Q` and the linear coefficient gate (5.2).

4. `anchor_reference_power_to_collar`

   Specialize `A0=eta`, `B0=(1+eta)L_eta`,
   `A1=4 gamma d`, `B1=H2`, `T=4 theta beta`, then compose with
   `Qd>=lambda V` and `beta<=(1-theta)lambda R_in`.

The first three are pure real algebra/order theorems.  The fourth must keep the
physical decomposition and same-domain metric identities as explicit premises.

---

## 9. Smallest real source packet still missing

To instantiate this child in the actual P5 chain, the source/consumer owners
must provide, all under the same relevant cell/reference/storage key:

1. the T-P5-112 finite anchor remainder packet (`gamma,H2` or the preconditioner variant);
2. the exact physical statement identifying where `r_A` enters the energy equation;
3. the multiplier `u` and a squared pairing inequality
   `(<u,r_A>)^2 <= Q_U(u)Q_A(r_A)`;
4. a positive dissipation comparison `d Q_U(u)<=Qd`;
5. confirmation that this anchor channel is not already included in
   T-P5-110's `p_ref/L_eta`;
6. the existing T-P5-110 `eta,L_eta(a)` packet and T-P5-111 selected recenter/domain packet;
7. the collar rate `Qd>=lambda V`, levels, and actual flow/path coverage.

If a direct signed cross packet between the two powers exists, provide it and
use section 5 instead of the worst-case discriminant gate.

---

## 10. Status / non-claims

Mathematical child: **CONDITIONAL_PASS**.

Closed here:

- inverse-free transfer from the T-P5-112 affine-anchor quadratic remainder to
  an energy-power square;
- sharp root-free aggregation of that channel with the T-P5-110 reference
  power;
- direct polynomial collar gates;
- signed-correlation refinement and an exact double-counting boundary.

Still open and intentionally not claimed:

- actual source identity for the anchor power channel;
- actual compatible `Q_A/Q_U/Qd` metric binding and positive `d`;
- actual `gamma/H2` or preconditioner numeric packet;
- same-cell path/graph/FD/reference coverage;
- selected recenter/jump/dwell instantiation;
- Float64/controller/runtime equivalence;
- Lean compile/kernel receipt;
- comparator/admission/registry or parent P5/P8 closure.
