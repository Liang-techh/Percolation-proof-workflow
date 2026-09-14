---
kind: review_result
review_id: review-T-P5-123-radial-shaping-coercivity-split-honglianmozun-20260909T0358Z
task_id: T-P5-123-RADIAL-SHAPING-COERCIVITY-SPLIT
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T03:58:00Z
claim_commit: 83e7a6fd0c5c5b04d014f45c66c22dd489885bd8
inspected_commit: f8f23ce20b9978a2a4745bad9a11cb50d6e4d478
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-119-conservative-bias-power-storage-shaping-honglianmozun-20260909T0257Z.md
    commit: 31f9508aab519f8af557803999942934063c5eb1
  - path: agent_review_inbox/review-T-P5-120-MOVING-CHART-CONSERVATIVE-POWER-PULLBACK-liuguanyi-20260909T0302Z.md
    commit: 282c801638022fcb40220e1f92f44f3ec0a3993d
  - path: agent_review_inbox/review-T-P5-121-APPROXIMATE-CONSERVATIVE-CURL-DEFECT-guyuefangyuan-20260909T0332Z.md
    commit: a47987998ab1760fc4e3f626ab13fb9c58194682
  - path: agent_review_inbox/review-T-P5-122-CURL-METRIC-PULLBACK-CLOSURE-kuangmanmozun-20260909T0342Z.md
    commit: 1ad2545fbe4175bed3808d77c49b533cded84b88
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_radial_value_sym_skew_split_and_bind_same_cell_base_potential_force_jet_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional radial integral, quadratic-form, and Lyapunov small-gain derivation only
exit_code: n/a
---

# T-P5-123 — radial storage-shaping coercivity from the symmetric Jacobian sector

## 0. Bottleneck selected

T-P5-119 establishes that an exactly conservative signed force channel can be moved into the Lyapunov storage instead of being paid as a generic disturbance. T-P5-121 then extends this to an approximately conservative field by using the radial potential

`Psi(q) = integral_0^1 <r(q0+s(q-q0)), q-q0> ds`

and paying only the skew-Jacobian/curl remainder. T-P5-122 transports that curl remainder through nonlinear-chart metrics without introducing square roots or inverses.

One premise is still structurally exposed: after subtracting `Psi`, the new storage must remain positive/coercive. T-P5-121 assumes a comparator of the form

`m Q_X(q-q0) <= V`,

but does not derive it from the same force jet that generated `Psi`.

This review closes that source-independent mathematical seam. The main point is an exact symmetric/skew split of the **same** Jacobian path:

- the symmetric part of `Dr` controls how much curvature is removed from storage;
- the skew part of `Dr` controls the nonconservative power remainder from T-P5-121;
- a large skew Jacobian by itself costs **zero** storage coercivity;
- a nonzero center mismatch appears as an uncancellable linear term and cannot be repaired by an additive normalization constant.

The result gives a root-free joint gate connecting storage admissibility directly to the curl small-gain theorem.

No deployed P5 source field, physical cell, Float64/controller semantics, P8 coverage, Lean receipt, provenance/admission, independent verification, or registry promotion is claimed.

---

## 1. Setup and exact radial value identity

Work in a finite-dimensional real configuration space. Let `Omega` be star-shaped with respect to an anchor `q0`. For a target point `q in Omega`, write

`x = q-q0`,
`z_s = q0+s x`, `0<=s<=1`,
`r_s = r(z_s)`,
`A_s = Dr(z_s)`.

Assume `r` is `C^1` on every such radial segment.

Define the same radial potential used in T-P5-121:

**(1.1)**

`Psi(q) := integral_0^1 <r_s,x> ds`.

Let `r0=r(q0)`. By the fundamental theorem of calculus,

`r_s = r0 + integral_0^s A_tau x d tau`.

Substitute this into (1.1) and exchange the order of integration:

`Psi(q)`
` = <r0,x> + integral_0^1 integral_0^s x^T A_tau x d tau ds`
` = <r0,x> + integral_0^1 (1-tau) x^T A_tau x d tau`.

Hence the exact value identity is

**(1.2) RADIAL POTENTIAL VALUE IDENTITY**

`Psi(q) = <r0,x> + integral_0^1 (1-s) x^T A_s x ds`.

Because `x^T(A_s-A_s^T)x=0`, only the symmetric part contributes:

**(1.3)**

`2 Psi(q)`
` = 2<r0,x> + integral_0^1 (1-s) x^T(A_s+A_s^T)x ds`.

This is independent of any conservativity assumption. It is a pure radial identity for the constructive potential.

---

## 2. Exact complementarity with the T-P5-121 curl remainder

T-P5-121 proves for the same radial construction that

**(2.1)**

`n(q) := r(q)-grad Psi(q)`
`      = integral_0^1 s (A_s-A_s^T)x ds`.

Compare (1.3) and (2.1):

- storage **value** uses `(1-s)(A_s+A_s^T)`;
- nonconservative **gradient defect** uses `s(A_s-A_s^T)`.

Thus the same first-jet packet naturally splits into two independent signed consumers.

### Structural fingerprint

For radial storage shaping, do **not** first bound `||Dr||` and reuse that number everywhere. The symmetric and skew sectors have different mathematical roles and different signs.

A pure skew field can have arbitrarily large `||Dr||` while changing the radial storage by exactly zero. Conversely, a symmetric destabilizing component can consume storage curvature even though its curl defect is exactly zero.

This split is the force-field analogue of preserving nonlinear cancellation before intervalization.

---

## 3. Base potential and the exact center-compatibility condition

Let `U(q)` be the configuration part of the pre-shaped Lyapunov storage. Define

`g0 := grad U(q0)`.

Instead of assuming `q0` is already a critical point of `U`, keep the linear term explicit. Define the Bregman-type centered remainder

**(3.1)**

`B_U(q;q0) := U(q)-U(q0)-<g0,x>`.

Now define the shaped configuration storage normalized at the anchor:

**(3.2)**

`W(q) := [U(q)-Psi(q)] - [U(q0)-Psi(q0)]`.

Since `Psi(q0)=0`, combining (1.2) with (3.1) gives the exact decomposition

**(3.3) SHAPED-STORAGE VALUE SPLIT**

`W(q)`
` = B_U(q;q0)`
`   + <g0-r0,x>`
`   - integral_0^1 (1-s) x^T A_s x ds`.

Equivalently, using only the symmetric part,

**(3.4)**

`2 W(q)`
` = 2 B_U(q;q0)`
`   + 2<g0-r0,x>`
`   - integral_0^1 (1-s) x^T(A_s+A_s^T)x ds`.

The exact same-center compatibility condition is therefore

**(3.5) CENTER FORCE BALANCE**

`g0 = r0`.

When (3.5) holds, the linear term vanishes and the shaped potential starts quadratically at the anchor.

### Why a constant normalization cannot replace (3.5)

The gradient of the shaped storage at the anchor is

`grad W(q0)=g0-r0`.

Adding any constant `C` changes neither this gradient nor the local minimizer. Therefore, if `g0-r0 != 0`, no additive normalization can make `q0` a local minimum of the shaped storage.

More explicitly, choose a direction `h` with `<g0-r0,h><0`. Then

`W(q0+epsilon h)=epsilon<g0-r0,h>+o(epsilon)<0`

for sufficiently small positive `epsilon` after normalizing `W(q0)=0`.

Hence no homogeneous inequality

`m Q_X(q-q0) <= W(q)` with `m>0`

can hold on any neighborhood of `q0`.

This is a force/storage center obstruction, distinct from T-P5-117's anchor-displacement center mismatch. The source packet must either prove (3.5), recenter the storage at the new equilibrium, or route the unmatched center force through a genuinely nonhomogeneous/additive branch.

For the common case in which the original normalized energy already has `g0=0`, condition (3.5) reduces to the simple requirement

`r(q0)=0`.

---

## 4. Root-free coercivity theorem from a symmetric-sector upper bound

Let

`Q_X(x)=x^T P_X x`

with `P_X` symmetric PSD.

Assume the base configuration storage has the lower Bregman bound

**(4.1)**

`a Q_X(x) <= B_U(q;q0)`

for some real/rational `a`.

Assume center force balance (3.5).

There are two useful source interfaces for the symmetric part.

### 4.1 Direct integrated symmetric budget

Suppose the source proves the signed path bound

**(4.2)**

`integral_0^1 (1-s) x^T(A_s+A_s^T)x ds <= kappa Q_X(x)`.

Then (3.4) immediately yields

**(4.3)**

`W(q) >= (a-kappa/2) Q_X(x)`.

Therefore any proposed `m>0` satisfying the scalar gate

**(4.4) ROOT-FREE STORAGE GATE**

`2m + kappa <= 2a`

obeys

**(4.5)**

`m Q_X(q-q0) <= W(q)`.

The trusted consumer only checks additions, multiplications, and order. No inverse metric, square root, generalized eigenvalue, or optimizer is required.

`kappa` need not be nonnegative. If the symmetric force derivative is restoring in the sign convention of `U-Psi`, the signed path budget may have `kappa<0`, in which case shaping **increases** the storage margin.

### 4.2 Uniform same-cell matrix gate

A simpler but potentially more conservative producer can certify, on the whole radial cell,

**(4.6)**

`2 kappa P_X - (Dr(z)+Dr(z)^T) >= 0`  for every relevant `z`.

Then for `z=z_s`,

`x^T(A_s+A_s^T)x <= 2 kappa Q_X(x)`.

Since `integral_0^1 (1-s) ds = 1/2`, (4.2) follows exactly:

`integral_0^1 (1-s) x^T(A_s+A_s^T)x ds`
` <= kappa Q_X(x)`.

Thus the same scalar gate (4.4) applies.

For rational polynomial/affine producers, (4.6) is an exact rational PSD target. It is deliberately a bound on the **symmetric derivative**, not on `Dr^T Dr` or a spectral norm of the full Jacobian.

---

## 5. Adding kinetic energy / full Lyapunov storage

Let the full pre-shaped storage have a nonnegative velocity part `T(v)` satisfying

**(5.1)** `d_v Q_V(v) <= T(v)`,

with `d_v>=0` and `Q_V` PSD.

Normalize the full shaped storage as

**(5.2)**

`V(q,v) := T(v) + W(q)`.

Under (4.1)-(4.4),

**(5.3)**

`V(q,v) >= m Q_X(q-q0) + d_v Q_V(v)`.

This supplies exactly the displacement comparator assumed by the homogeneous approximate-conservative small-gain lane of T-P5-121.

Nothing in this theorem claims a derivative inequality for `V`; it is an admissibility/coercivity bridge. The derivative ledger remains a separate premise and must use the same shaped storage convention.

---

## 6. Joint symmetric/curl closure with T-P5-121

Assume now that the derivative ledger for this same shaped storage has the T-P5-121 form

**(6.1)**

`Vdot <= -c V - d Q_V(v) + <v,n> + p_other`,

with `c>0`, `d>0`, and the same radial nonconservative remainder `n` from (2.1).

Suppose the curl packet gives

**(6.2)**

`4 Q_F(n) <= K_curl Q_X(x)`,

and the compatible power pairing gives

**(6.3)**

`<v,n>^2 <= Q_V(v) Q_F(n)`.

T-P5-121 shows that if

`K_curl <= 16 m alpha theta d`

with `0<=alpha<c`, `0<=theta<1`, then

`<v,n> <= alpha V + theta d Q_V(v)`

and hence

`Vdot <= -(c-alpha)V -(1-theta)d Q_V(v)+p_other`.

Using the **maximal coercivity margin produced by this review**,

`m_* = a-kappa/2 = (2a-kappa)/2`,

we obtain the direct joint gate

**(6.4) SYM/CURL JOINT SMALL-GAIN GATE**

`K_curl <= 8 (2a-kappa) alpha theta d`,

with the required positivity condition

**(6.5)** `2a-kappa > 0`.

This is a single source-independent design relation between the two pieces of the same Jacobian:

- `kappa` is the signed symmetric-sector curvature debit;
- `K_curl` is the skew-sector action budget;
- `2a-kappa` is the storage margin remaining after shaping.

As the destabilizing symmetric sector approaches the base storage curvature, the allowable curl budget shrinks to zero. A negative/restoring symmetric sector enlarges the allowable curl budget.

### Parameter-free half-reserve specialization

Choosing

`alpha=c/2`, `theta=1/2`

gives the easy checker gate

**(6.6)**

`K_curl <= 2 (2a-kappa) c d`.

Then

**(6.7)**

`Vdot <= -(c/2)V -(d/2)Q_V(v) + p_other`.

This specialization is useful when the coordinator wants a fixed rational split and does not want to optimize `alpha,theta`.

---

## 7. Sharpness of the one-half storage debit

The factor `1/2` in `(a-kappa/2)` cannot be improved under only the uniform symmetric-sector bound.

Take one dimension with anchor `q0=0`,

`r(x)=kappa x`,

so `Dr=kappa`, and let

`Q_X(x)=x^2`.

Then the uniform matrix gate (4.6) is exact, and the radial potential is

`Psi(x)=integral_0^1 kappa s x^2 ds = (kappa/2)x^2`.

If the base potential remainder is exactly

`B_U=a x^2`,

then the shaped potential is exactly

`W=(a-kappa/2)x^2`.

Thus no universal theorem based only on `a` and the uniform symmetric bound `kappa` can replace `kappa/2` by a smaller debit.

---

## 8. Pure-skew counterexample: full Jacobian norm is the wrong storage quantity

Take two dimensions and

`J0 = [[0,-1],[1,0]]`,

`r_K(x)=K J0 x`

for an arbitrary `K>0`.

Then

`Dr_K = K J0`,
`Dr_K + Dr_K^T = 0`.

The radial potential is exactly

`Psi(x)=integral_0^1 <KJ0(sx),x> ds = 0`

because `x^T J0 x=0`.

Therefore this arbitrarily large Jacobian costs **zero storage coercivity**.

On the other hand, T-P5-121 gives

`n(x)=KJ0 x`,

so the entire channel remains as a nonconservative/curl power term.

Any producer that first replaces `Dr` by a full operator-norm bound proportional to `K` and then debits that number from storage would manufacture an arbitrarily large false curvature penalty. This is exactly why the symmetric/skew split must occur before norm enclosure.

---

## 9. Pure-symmetric specialization recovers exact conservative shaping

For an affine field

`r(x)=b+A x`,

the radial identities become

**(9.1)**

`Psi(x)=b^T x + (1/2)x^T A x`
`      = b^T x + (1/4)x^T(A+A^T)x`,

and

**(9.2)**

`n(x)=(1/2)(A-A^T)x`.

If `A=A^T`, then `n=0`: there is no curl budget at all, and the only issue is whether subtracting the conservative quadratic keeps the storage positive.

For a quadratic base potential

`U(x)=U(0)+g0^T x + (1/2)x^T K x`,

with center balance `g0=b`, the shaped potential is exactly

**(9.3)**

`W(x)=(1/2)x^T(K-A)x`.

Thus the T-P5-119 affine theorem is recovered as the zero-curl specialization of the present radial theorem. The present result extends the same logic to nonlinear fields using only a same-ray symmetric-sector cap.

---

## 10. Time-dependent force fields

Let `r=r(t,q)` and optionally `U=U(t,q)`. Apply the preceding analysis at each fixed time.

If, on the same certified spacetime tube,

`grad_q U(t,q0)=r(t,q0)`

and the Bregman lower bound plus symmetric-sector cap are uniform, then the instantaneous shaped storage remains uniformly coercive with the same `m`.

However, as T-P5-120/T-P5-121 already show, the derivative ledger also contains the schedule term coming from the time derivative of the pulled/radial potential. This review does **not** erase that term.

Therefore the typed responsibilities are separate:

1. spatial symmetric jet -> storage coercivity;
2. spatial skew jet -> nonconservative power small-gain;
3. explicit time dependence / moving anchor -> schedule-power budget.

A producer must not use a spatial coercivity certificate to silently discharge `Psi_t`.

---

## 11. Moving-chart boundary

T-P5-120 shows that conservative force power is a pulled-back work one-form, and T-P5-122 gives a root-free metric transport for the skew/curl action.

The present coercivity theorem is most naturally proved in the authoritative physical configuration cell before chart pullback. If a normalized-coordinate consumer needs

`m_z Q_Z(z-z0) <= V(t,z)`,

it still needs a **lower** displacement transport from physical shaped distance to the normalized metric. That is a different order direction from T-P5-122's upper curl-action transport factors.

So the following are not interchangeable:

- upper tangent/covector factors used to transport curl action;
- lower metric factor needed to transport storage coercivity.

No chart inverse should be inferred implicitly. A direct normalized PSD/inclusion witness is preferable when available.

---

## 12. Source-facing packet

A real P5 producer that wants to combine T-P5-119/121/122 with this child should bind, under one common physical cell/tube key:

1. the base configuration storage/potential `U` and anchor `q0`;
2. the exact signed force field `r` that is being removed from the power ledger;
3. center values `g0=grad U(q0)` and `r0=r(q0)` plus the exact equality `g0=r0` (or an explicit recentering branch);
4. a Bregman lower bound `a Q_X <= U-U(q0)-<g0,q-q0>`;
5. `A=Dr` on the entire radial segment/cell;
6. either the direct integrated symmetric budget (4.2) or the uniform PSD gate `2kappa P_X-(A+A^T)>=0`;
7. the skew/curl action packet used by T-P5-121 and, if charted, the T-P5-122 metric transport;
8. a no-double-count statement: the symmetric contribution already absorbed into `Psi` is not also charged as a generic residual norm;
9. if time dependent, a separate schedule-power packet for `Psi_t`;
10. if a normalized chart is used, a separate lower storage-metric transport/inclusion witness.

The preferred producer should preserve both signed packets:

`SYM: integral (1-s) x^T(A+A^T)x`

and

`SKEW: integral s(A-A^T)x` / its quadratic action bound.

Collapsing them into one unsigned `||Dr||` envelope loses the main structural benefit.

---

## 13. Candidate theorem statements for formalization

Suggested source-independent leaves:

```text
radial_potential_value_identity:
  Psi(q) = <r(q0),x>
           + integral_0^1 (1-s) * <x, Dr(q0+s*x) x> ds.

radial_potential_value_symmetric_part:
  2*Psi(q) = 2*<r(q0),x>
             + integral_0^1 (1-s) * <x,(Dr+Dr^T)x> ds.

shaped_storage_center_gradient:
  grad (U-Psi)(q0) = grad U(q0) - r(q0).

shaped_storage_coercive_of_radial_sym_cap:
  g0=r0 ->
  a*QX(x) <= B_U ->
  integral (1-s)<x,(Dr+Dr^T)x> <= kappa*QX(x) ->
  2*m+kappa <= 2*a ->
  m*QX(x) <= (U-Psi)(q)-(U-Psi)(q0).

uniform_sym_psd_implies_radial_sym_cap:
  (forall z on radialSegment, 2*kappa*P_X-(Dr(z)+Dr(z)^T) >= 0)
  -> radial symmetric budget <= kappa*QX(x).

shaped_center_requires_force_balance:
  localMinAt q0 (U-Psi) -> grad U(q0)=r(q0).

sym_curl_joint_small_gain:
  storage hypotheses above ->
  4*QF(n)<=Kcurl*QX(x) ->
  pairing/dissipation hypotheses ->
  Kcurl <= 8*(2*a-kappa)*alpha*theta*d ->
  Vdot <= -(c-alpha)V -(1-theta)d*QV + p_other.
```

For Lean, the highest-value first leaves are the exact radial value identity, the center-gradient identity, and the quadratic scalar consequence `2m+kappa<=2a`. The calculus/integral layer can stay separate from the finite-dimensional PSD consumer.

---

## 14. Failure boundaries / non-claims

This review is a `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending` result only.

The following remain open and must fail closed:

- no actual P5 source field `r` or base potential `U` has been bound;
- no proof currently establishes `grad U(q0)=r(q0)` for the deployed source convention;
- no same-cell/radial-segment symmetric Jacobian packet has been provided;
- no actual rational `a,kappa,m` or matrix PSD witness has been supplied;
- the T-P5-121 curl packet and T-P5-122 chart metric packet remain source-independent until bound to deployed semantics;
- if `g0-r0!=0`, homogeneous same-center coercivity is impossible after any additive normalization; a recentered or nonhomogeneous branch is required;
- if `2a-kappa<=0`, the available information does not certify a positive displacement margin after shaping even if the curl is zero;
- a small curl bound does not imply a safe symmetric sector, and a safe symmetric sector does not imply small curl;
- the storage coercivity theorem does not discharge explicit time dependence `Psi_t`, moving-anchor terms, or frame-power semantics;
- no Float64/FD/controller/runtime, P8 flowpipe, Lean/kernel, independent verifier `封不觉`, admission, or registry claim is made.

The mathematical progress is the exact decomposition showing that **storage admissibility and nonconservative dissipation should consume different signed halves of the same force Jacobian**, together with the sharp root-free storage margin `m <= a-kappa/2` and the direct joint curl gate `K_curl <= 8(2a-kappa) alpha theta d`.
