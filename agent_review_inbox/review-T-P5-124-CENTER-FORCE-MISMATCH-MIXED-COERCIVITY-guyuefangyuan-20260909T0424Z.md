---
kind: review_result
review_id: review-T-P5-124-center-force-mismatch-mixed-coercivity-guyuefangyuan-20260909T0424Z
task_id: T-P5-124-CENTER-FORCE-MISMATCH-MIXED-COERCIVITY
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T04:24:00Z
claim_commit: ab544f53bbb9a546353173ce84adf4cd5dc14abd
inspected_commit: 5ea34f5e5e65d5babc47a3d8ed04f578cbea7c28
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-121-APPROXIMATE-CONSERVATIVE-CURL-DEFECT-guyuefangyuan-20260909T0332Z.md
    commit: a47987998ab1760fc4e3f626ab13fb9c58194682
  - path: agent_review_inbox/review-T-P5-122-CURL-METRIC-PULLBACK-CLOSURE-kuangmanmozun-20260909T0342Z.md
    commit: 1ad2545fbe4175bed3808d77c49b533cded84b88
  - path: agent_review_inbox/review-T-P5-123-radial-shaping-coercivity-split-honglianmozun-20260909T0358Z.md
    commit: 5ea34f5e5e65d5babc47a3d8ed04f578cbea7c28
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_mixed_center_force_coercivity_then_bind_same_cell_center_mismatch_and_curl_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic-form and Lyapunov algebra only
exit_code: n/a
---

# T-P5-124 — center-force mismatch: mixed coercivity, additive floor, and exact recenter alternative

## 0. Bottleneck selected

T-P5-123 proves that the radial shaping construction has the exact value split

`2 W(q) = 2 B_U(q;q0) + 2 <b,x> - I_sym(x)`,

where

`x=q-q0`,

`b=grad U(q0)-r(q0)`,

and

`I_sym(x)=integral_0^1 (1-s) x^T(Dr+Dr^T)(q0+s x)x ds`.

If `b=0`, a symmetric-sector bound gives homogeneous coercivity of the shaped storage. T-P5-123 also proves a hard obstruction when `b!=0`: after normalizing `W(q0)=0`, no positive homogeneous bound `m Q_X(x)<=W(q)` can hold in a neighborhood of `q0`, because the shaped storage has a nonzero linear derivative there.

The remaining mathematical branch is therefore not another exact-center theorem. It is:

> if the center-force mismatch is quantitatively small but genuinely nonzero, what exact root-free certificate converts it into a controlled nonhomogeneous storage floor, and how does that floor interact with the approximate-curl small-gain lane from T-P5-121?

This review gives a sharp answer. The key result is a three-gate theorem with only rational products and order:

`2(m+eps)+kappa <= 2a`,

`B <= 4 eps D`,

`K_curl <= 16 m alpha theta d`.

The first two produce `m Q_X(x) <= W(q)+D`; the third absorbs the curl remainder. The constant shift `D` then appears as an unavoidable additive term `cD` in any derivative ledger containing `-cW`. This is the correct mixed branch; it does not pretend that the original anchor is still an equilibrium.

No deployed P5 field, source packet, domain coverage, Float64/controller semantics, P8 flowpipe, Lean/kernel receipt, independent verification, admission, or registry promotion is claimed.

---

## 1. Same-cell setup inherited from T-P5-123

Let `Q(x)=Q_X(x)>=0` be the physical displacement quadratic form.

Assume the same radial segment and same signed force field as T-P5-123, with

**(1.1)** `a Q(x) <= B_U(q;q0)`,

and the same signed symmetric-sector path budget

**(1.2)** `I_sym(x) <= kappa Q(x)`.

Write the center-force mismatch power as

**(1.3)** `p_b(x) := <b,x>`,  `b=grad U(q0)-r(q0)`.

The exact T-P5-123 value identity gives

`2 W = 2 B_U + 2 p_b - I_sym`,

hence from (1.1)-(1.2),

**(1.4)**

`2 W >= (2a-kappa) Q + 2 p_b`.

Instead of demanding `b=0`, assume a typed dual quadratic estimate

**(1.5) CENTER-MISMATCH DUAL BOUND**

`p_b(x)^2 <= B Q(x)`

for all relevant `x`, with `B>=0`.

This is the right source-facing object. It does not require an inverse metric in the trusted theorem. A producer may obtain `B` from a direct PSD block, a dual-metric witness, or a signed finite-dimensional calculation, but this child consumes only (1.5).

---

## 2. Root-free one-sided Young lemma with a pre-budgeted floor

The elementary scalar lemma needed below is deliberately written without division or square roots.

### Lemma 2.1 — center mismatch one-sided absorption

Let `Q,B,eps,D>=0`, `eps>0`, and `p` satisfy

`p^2 <= B Q`,

`B <= 4 eps D`.

Then

**(2.1)**

`p >= -eps Q - D`.

### Proof

Suppose instead that `p < -eps Q-D`. Then `-p>eps Q+D>=0`, so

`p^2 > (eps Q+D)^2`.

But

`(eps Q+D)^2 - 4 eps D Q = (eps Q-D)^2 >=0`,

therefore

`p^2 > 4 eps D Q >= B Q`,

contradicting `p^2<=BQ`.

Every trusted check is a polynomial/order statement. The familiar quantity `B/(4 eps)` never needs to be computed.

---

## 3. Main mixed coercivity theorem

Choose rational/scalar parameters

`m>0`, `eps>0`, `D>=0`

satisfying the two gates

**(3.1) CURVATURE RESERVE GATE**

`2(m+eps)+kappa <= 2a`,

and

**(3.2) CENTER FLOOR GATE**

`B <= 4 eps D`.

Then (1.4) and (3.1) imply

`W >= (m+eps)Q + p_b`.

Lemma 2.1 gives `p_b>=-eps Q-D`, hence

**(3.3) MIXED COERCIVITY**

`m Q_X(q-q0) <= W(q)+D`.

If the full shaped storage is

`S(q,v)=T(v)+W(q)`

with `T(v)>=d_v Q_V(v)>=0`, define the shifted storage

**(3.4)** `V := S + D`.

Then

**(3.5)**

`V >= m Q_X(q-q0) + d_v Q_V(v) >=0`.

This is the correct substitute for the impossible same-center statement `mQ_X<=W` when `b!=0`.

### Important semantics

Adding `D` does **not** make `q0` a critical point or local minimizer of `W`. It merely supplies a nonnegative storage baseline large enough to dominate the unmatched linear term. The gradient remains

`grad W(q0)=b`.

Thus this theorem respects the T-P5-123 center obstruction rather than evading it by renaming a constant.

---

## 4. Sharpness of the floor gate

The center-floor condition is sharp at the information level of `(1.5)`.

Take one dimension,

`Q(x)=x^2`,

and the exact shaped lower model

`W(x)=(m+eps)x^2-beta x`,

so `p_b=-beta x` and the sharp dual constant is

`B=beta^2`.

The desired shifted comparator is

`m x^2 <= W(x)+D`,

or equivalently

`0 <= eps x^2-beta x+D`.

Its minimum occurs at `x=beta/(2eps)` and equals

`D-beta^2/(4eps)`.

Therefore the comparator holds for every `x` **iff**

`beta^2 <= 4 eps D`,

i.e. exactly (3.2).

Consequently no theorem using only the quadratic mismatch information `p_b^2<=BQ` can universally replace the factor `4` by a larger favorable constant or demand a smaller `D` for fixed `eps`.

---

## 5. Coupling to T-P5-121 approximate-curl power

Now assume the derivative ledger is written for the **unshifted** full shaped storage `S`:

**(5.1)**

`Sdot <= -c S - d Q_V(v) + p_n + p_other`,

where `c>0`, `d>0`,

`p_n=<v,n>`

is the nonconservative radial remainder from T-P5-121.

Assume the same physical-cell curl packet

**(5.2)** `4 Q_F(n) <= K_curl Q_X(x)`,

and compatible power pairing

**(5.3)** `p_n^2 <= Q_V(v) Q_F(n)`.

Because `V=S+D`, (5.1) becomes the exact shifted ledger

**(5.4)**

`Vdot <= -c V - d Q_V(v) + p_n + cD + p_other`.

From (3.5), `m Q_X(x)<=V`. Therefore T-P5-121's root-free absorption applies unchanged if there exist `alpha,theta` with

`0<=alpha<c`, `0<=theta<1`,

and

**(5.5) CURL SMALL-GAIN GATE**

`K_curl <= 16 m alpha theta d`.

It yields

`p_n <= alpha V + theta d Q_V(v)`,

so

**(5.6) MIXED CENTER+CURL LEDGER**

`Vdot <= -(c-alpha)V -(1-theta)d Q_V(v) + cD + p_other`.

This is the central theorem of the child.

### Fully root-free certificate packet

The source-independent trusted scalar consumer can therefore be reduced to

1. `2(m+eps)+kappa <= 2a`,
2. `B <= 4 eps D`,
3. `K_curl <= 16 m alpha theta d`,
4. `m>0`, `eps>0`, `0<=alpha<c`, `0<=theta<1`.

No square root, inverse metric, eigenvalue, or division is needed after the quadratic premises are supplied.

T-P5-122 may first transport the physical curl constant into a chart metric. In that case the transported constant simply replaces `K_curl` in gate 3; the center-mismatch comparator must use the same displacement/storage metric key as the transported curl consumer.

---

## 6. Ultimate-tube closure

If the remaining signed terms have a certified upper bound

`p_other <= P`,

with `P>=0`, then (5.6) gives

`Vdot <= -(c-alpha)V -(1-theta)dQ_V + (cD+P)`.

Let `R0>=0`. The exact rational boundary gate

**(6.1)**

`cD + P <= (c-alpha) R0`

implies that on `V=R0`,

`Vdot <= -(1-theta)d Q_V <=0`.

With the already separate first-exit / outer-collar / same-tube coverage theorem, this makes `V<=R0` a candidate invariant/ultimate tube.

The additive floor is therefore not an admission failure by itself. It changes the conclusion from homogeneous convergence to a zero-centered storage into convergence/invariance relative to a nonzero storage tube.

---

## 7. Why the derivative pays exactly `cD`

If the available derivative theorem contains the term `-cS`, then shifting the storage by a constant has the algebraic identity

`-cS = -c(V-D) = -cV+cD`.

Thus `cD` is not a loose Young-inequality artifact. It is exactly the price of reusing the same decay ledger after the constant shift.

A source may avoid this particular charge only by providing a stronger derivative statement whose dissipation is expressed independently of the storage zero level, or by actually recentering at a critical point and proving a new coercive storage there. One cannot simply add `D` and keep the old conclusion `Vdot<=-cV+...`.

### Exact scalar obstruction

Take any trajectory for which the unshifted inequality is an equality `Sdot=-cS`. For `V=S+D`, necessarily

`Vdot=-cV+cD`.

Therefore a theorem that replaces the shifted right-hand side by `-cV` for `D>0` is false even before curl, controller, or numerical defects are introduced.

---

## 8. Coercivity-floor versus curl-gain tradeoff

Define conceptually the maximum homogeneous curvature available before paying center mismatch as

`mu0 := a-kappa/2`.

The trusted checker need not form this quotient; it is only useful for analysis.

The mixed gates require

`m+eps <= mu0`,

while the curl gate requires

`K_curl <= 16 m alpha theta d`.

For `B>0`, any finite center-floor certificate has `eps>0`, hence necessarily `m<mu0`. Therefore a necessary condition for this particular mixed branch is

**(8.1)**

`K_curl < 16 mu0 alpha theta d`.

Equivalently, using the unhalved symmetric margin,

`K_curl < 8 (2a-kappa) alpha theta d`.

If the curl constant already saturates the entire available homogeneous curvature margin, there is no remaining `eps` with which to absorb a nonzero center mismatch.

Conversely, choosing larger `m` improves the curl allowance but leaves smaller `eps`, which by the sharp gate `B<=4epsD` forces a larger additive floor `D`. Choosing smaller `m` reduces the floor but weakens the curl small-gain allowance. This is a genuine certificate-design Pareto tradeoff, not a numerical tuning accident.

A search layer may tune rational `(m,eps,D,alpha,theta)`; the trusted theorem still checks only the polynomial gates above.

---

## 9. Exact recenter alternative when a new critical-point witness exists

The mixed branch is necessary only when one insists on retaining the old anchor while `b!=0`. A stronger source may instead provide an actual critical point of the shaped scalar potential.

Let

`F(q):=U(q)-Psi(q)`

for the already constructed scalar radial potential `Psi`. Suppose a point `q_*` in the certified cell satisfies

**(9.1)** `grad F(q_*)=0`.

Assume the segment from `q_*` to `q` remains in a region where the symmetric Hessian obeys the direct matrix/quadratic lower bound

**(9.2)**

`y^T Hess F(z) y >= 2 mu Q_X(y)`

for all relevant `z,y`, with `mu>0`.

Taylor's integral formula gives

`F(q)-F(q_*)`

` = integral_0^1 (1-s) (q-q_*)^T Hess F(q_*+s(q-q_*))(q-q_*) ds`,

so

**(9.3) RECENTERED COERCIVITY**

`mu Q_X(q-q_*) <= F(q)-F(q_*)`.

This branch has no additive center floor because the storage is genuinely recentered at a critical point, not merely shifted by a constant at a noncritical anchor.

### Quantitative displacement of the new center

Let `x_*=q_*-q0` and `b=grad F(q0)`; for the radial construction, this is exactly the T-P5-123 center mismatch at `q0`.

If the Hessian lower bound (9.2) also covers the segment `q0 -> q_*`, then

`-<b,x_*> >= 2 mu Q_X(x_*)`.

If the same dual mismatch bound gives

`<b,x_*>^2 <= B Q_X(x_*)`,

then, whenever `Q_X(x_*)>0`, squaring yields

**(9.4)**

`4 mu^2 Q_X(x_*) <= B`.

For `Q_X(x_*)=0` the inequality is automatic. Thus the center mismatch also gives a root-free a-posteriori metric bound on how far a certified new critical point can move.

This does **not** prove existence of `q_*`; existence and same-cell coverage remain independent obligations.

### Re-anchoring the radial construction is a different operation

If a source instead gives a point `q_*` satisfying `grad U(q_*)=r(q_*)`, one may rebuild the radial potential with anchor `q_*` and rerun T-P5-123/T-P5-121. That new potential and its curl remainder need not equal the old `Psi` and `n`; the two operations must not be conflated in a typed interface.

---

## 10. Further obstructions

### 10.1 No positive curvature reserve, no domain-independent quadratic shifted coercivity

If the post-shaping quadratic reserve vanishes, a linear center mismatch cannot be absorbed into a finite global quadratic comparator merely by adding a constant.

In one dimension take

`W(x)=-x`.

For any finite `D` and any `m>0`, the inequality

`m x^2 <= W(x)+D=D-x`

fails for sufficiently large positive `x`.

A bounded cell may still permit a cell-specific absolute floor, but then the bound is a domain-radius certificate rather than the source-independent curvature/mismatch theorem proved here.

### 10.2 A constant shift does not restore equilibrium semantics

Even when (3.3) holds,

`grad(W+D)(q0)=b`.

Therefore no proof may use `V=W+D` as if its zero or minimizer were at `q0`. The theorem certifies a storage lower bound and an ultimate-tube ledger only.

### 10.3 Center mismatch and curl are independent first-jet sectors

`b` is a zero-order force/storage mismatch at the anchor. `K_curl` measures the antisymmetric first derivative along the cell. Either can vanish while the other is arbitrarily large. They need separate source fields and separate gates; a small curl constant cannot certify center balance.

---

## 11. Suggested Lean theorem decomposition

The best first Lean leaves are pure scalar/order algebra and do not need calculus.

### Leaf A — one-sided floor absorption

Suggested shape:

`center_mismatch_ge_neg_epsQ_sub_D`

Premises:

- `0 <= Q`, `0 <= B`, `0 < eps`, `0 <= D`,
- `p^2 <= B*Q`,
- `B <= 4*eps*D`.

Conclusion:

`-eps*Q-D <= p`.

The contradiction proof in section 2 should be friendly to `nlinarith` after exposing `(eps*Q-D)^2>=0`.

### Leaf B — mixed coercivity scalar closure

`mixed_center_coercivity`

Premises:

- `2*W >= (2*a-kappa)*Q + 2*p`,
- `p^2 <= B*Q`,
- `2*(m+eps)+kappa <= 2*a`,
- `B <= 4*eps*D`,
- sign premises.

Conclusion:

`m*Q <= W+D`.

### Leaf C — shifted decay identity/closure

`shifted_storage_decay`

From

`Sdot <= -c*S - d*Qv + pn + Pother`

and `V=S+D`, derive

`Vdot <= -c*V-d*Qv+pn+c*D+Pother`.

### Leaf D — combined center+cURL small gain

`mixed_center_curl_small_gain`

Consume Leaf B plus the already source-independent T-P5-121 power premises and gate `K<=16*m*alpha*theta*d` to produce (5.6).

### Later calculus leaf

`critical_point_hessian_lower_implies_recentered_coercivity`

should be postponed until the scalar theorem and source packet are stable.

---

## 12. Source-facing packet

For a real same-cell P5 instantiation, the least ambiguous packet is:

1. the same shaped storage convention `U-Psi` and anchor `q0`;
2. exact center mismatch covector `b=grad U(q0)-r(q0)`;
3. a typed direct dual bound `p_b(x)^2<=B Q_X(x)` on the intended displacement metric;
4. the T-P5-123 base Bregman constant `a` and signed symmetric-sector budget `kappa` on the same radial cell;
5. rational candidate `(m,eps,D)` satisfying gates (3.1)-(3.2);
6. the T-P5-121/122 curl constant in the **same** displacement/storage metric key and the same-cell power pairing;
7. nominal derivative constants `(c,d)` and any remaining `p_other<=P` ledger;
8. outer-collar / radial-segment / chart coverage for every object actually consumed.

If a recentered branch is desired instead, additionally bind a concrete `q_*`, `grad F(q_*)=0`, the segment coverage, and a Hessian lower packet for the same shaped scalar `F`. Do not substitute a point satisfying `grad U=r` unless the radial potential is explicitly rebuilt around that point.

Producer priority should be:

- preserve `b` as a signed covector and form its dual quadratic action before intervalizing;
- keep the symmetric Jacobian sector and skew/curl sector separate as T-P5-123 requires;
- use direct pulled-back metric gates from T-P5-122 when possible;
- only then tune rational `m,eps,D,alpha,theta`.

---

## 13. Status and exact open boundary

Result: **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending**.

This child proves the previously open nonhomogeneous center-force branch at the source-independent mathematical level:

- nonzero center mismatch can be absorbed by the sharp root-free gate `B<=4epsD`;
- the remaining homogeneous displacement margin is `m`, paid through `2(m+eps)+kappa<=2a`;
- the curl lane then uses `K_curl<=16m alpha theta d`;
- the shifted derivative ledger necessarily acquires the additive term `cD`;
- a genuine critical-point recenter can remove that floor, but existence/coverage of the new center is an independent obligation.

Still open and explicitly **not** claimed here:

- actual deployed `b`, `B`, `a`, `kappa`, `K_curl`, `(c,d)`, or `P` source binding;
- same-cell/radial/whole-chart coverage;
- a real critical-point witness `q_*` or proof of its existence;
- explicit-time `Psi_t`, moving-anchor, frame-power, controller, FD, Float64/runtime, or P8 semantics;
- Lean/kernel compilation and proof receipt;
- independent verification by 封不觉;
- admission, registry, or parent P5 closure.
