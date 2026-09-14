---
kind: review_result
review_id: review-T-P5-122-curl-metric-pullback-closure-kuangmanmozun-20260909T0342Z
task_id: T-P5-122-CURL-METRIC-PULLBACK-CLOSURE
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T03:42:00Z
claim_commit: 223c6b0e1284cdb7c09f899522ec72daff9dd7d9
inspected_commit: 4c6efc29afe287bf3fee2ea6aaa5cf92efd7929a
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-120-MOVING-CHART-CONSERVATIVE-POWER-PULLBACK-liuguanyi-20260909T0302Z.md
    commit: 282c801638022fcb40220e1f92f44f3ec0a3993d
  - path: agent_review_inbox/review-T-P5-121-APPROXIMATE-CONSERVATIVE-CURL-DEFECT-guyuefangyuan-20260909T0332Z.md
    commit: a47987998ab1760fc4e3f626ab13fb9c58194682
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_direct_and_factored_curl_metric_pullback_then_bind_same_cell_chart_metric_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; finite-dimensional quadratic-form/PSD algebra and exact counterexamples only
exit_code: n/a
---

# T-P5-122 — root-free metric transport for approximate curl under a nonlinear chart

## 0. Bottleneck selected

T-P5-120 establishes the correct object type for a physical force: under a chart `x=T(t,z)` its generalized components are the covector pullback `J^T r`, not a tangent-vector transform.

T-P5-121 then proves the exact curl pullback identity

`S_z = J^T S_x J`,

where `S_x = Dr-Dr^T`, and obtains a physical same-cell action bound of the form

`Q_F(S_x delta_x) <= K_curl Q_X(delta_x)`.

The remaining inequality seam is quantitative:

> What exact, root-free certificate transports this physical skew-action bound into a normalized/chart metric, and when is a factored chart constant genuinely necessary rather than an artifact of norm bounding?

This review gives:

1. the direct pulled-back PSD gate, which is the tight target when the source can expose `J` and `S_x` together;
2. a fully factored, inverse-free gate using one tangent metric transport and one covector metric transport;
3. a proof that the product of the two transport factors is information-theoretically sharp under only those separate envelopes;
4. an anisotropic counterexample showing that the factored product can nevertheless be arbitrarily more conservative than the direct pulled-back gate;
5. the correct finite-displacement/secant version for the radial remainder from T-P5-121, including a counterexample showing that an endpoint Jacobian bound cannot be substituted for segment coverage;
6. the exact small-gain ledger obtained after the metric transport.

No deployed source packet or chart/domain coverage is asserted.

---

## 1. Typed quadratic-form setup

Work at one fixed time and one fixed chart point unless explicitly discussing a segment.

Let physical tangent increments be `delta_x in R^n` and normalized tangent increments be `eta in R^k`. Let

`J : R^k -> R^n`

be the chart Jacobian.

A physical curl/skew action is a covector-valued linear map

`S_x : R^n -> R^n`,

with `S_x^T=-S_x` in the chosen physical coordinate basis. T-P5-121 gives the normalized pulled-back skew action

**(1.1)**

`S_z = J^T S_x J : R^k -> R^k`.

Keep four quadratic forms distinct:

`Q_X(delta_x) = delta_x^T P_X delta_x`,

`Q_F(f) = f^T R_F f`,

`Q_Z(eta) = eta^T P_Z eta`,

`Q_G(g) = g^T R_G g`,

where the matrices are symmetric PSD. Positive definiteness may be imposed by a concrete consumer, but the algebra below only needs PSD plus the displayed matrix inequalities.

`Q_X` and `Q_Z` measure tangent/displacement objects. `Q_F` and `Q_G` measure force/covector objects. Their roles must not be interchanged merely because the coordinate dimensions happen to match.

Assume the physical curl-action certificate

**(1.2)**

`K P_X - S_x^T R_F S_x >= 0`  (PSD),

with `K>=0`.

Equivalently,

`Q_F(S_x delta_x) <= K Q_X(delta_x)`

for every physical increment.

---

## 2. Direct pulled-back gate: no condition-number loss is intrinsically required

The strongest normalized certificate available from the actual pulled-back matrices is simply

**(2.1) DIRECT CURL PULLBACK PSD GATE**

`K_z P_Z - S_z^T R_G S_z >= 0`,

where

`S_z=J^T S_x J`.

Then for every normalized tangent increment `eta`,

**(2.2)**

`Q_G(S_z eta) <= K_z Q_Z(eta)`.

This is just the quadratic form of (2.1), but it is the correct source-facing target because it preserves every signed/orientation cancellation inside `J^T S_x J` before taking a norm or interval envelope.

Expanded without introducing an inverse or square root, the matrix to certify is

**(2.3)**

`K_z P_Z - J^T S_x^T J R_G J^T S_x J >= 0`.

If all matrices and `K_z` are rational, this can be consumed by any exact rational PSD witness already accepted by the finite-dimensional infrastructure. No spectral norm, Cholesky square root, or Jacobian inverse is mathematically required.

---

## 3. Factored root-free transport theorem

Sometimes the producer cannot certify (2.3) directly and instead exposes separate metric comparison packets. Let `mu_X, mu_F >=0` satisfy

**(3.1) tangent transport**

`mu_X P_Z - J^T P_X J >= 0`,

and

**(3.2) covector transport**

`mu_F R_F - J R_G J^T >= 0`.

These mean respectively

`Q_X(J eta) <= mu_X Q_Z(eta)`,

and

`Q_G(J^T f) <= mu_F Q_F(f)`.

Then the following root-free closure is immediate.

### Theorem 3.1 — factored curl metric pullback

From (1.2), (3.1), and (3.2),

**(3.3)**

`mu_F * mu_X * K * P_Z - S_z^T R_G S_z >= 0`.

Hence

**(3.4)**

`Q_G(S_z eta) <= mu_F mu_X K Q_Z(eta)`

for every `eta`.

### Proof

Using `S_z=J^T S_x J`,

`S_z^T R_G S_z`

`= J^T S_x^T J R_G J^T S_x J`.

By (3.2),

`J R_G J^T <= mu_F R_F`,

so congruence by `S_x J` gives

`S_z^T R_G S_z <= mu_F J^T S_x^T R_F S_x J`.

By (1.2),

`S_x^T R_F S_x <= K P_X`,

therefore

`S_z^T R_G S_z <= mu_F K J^T P_X J`.

Finally (3.1) gives

`S_z^T R_G S_z <= mu_F mu_X K P_Z`.

Every step is a PSD congruence/order step. There is no division and no hidden invertibility assumption.

---

## 4. Why two chart factors really appear

The two appearances of `J` in `S_z=J^T S_x J` are not notation noise. One acts on the tangent input, and the other pulls the physical covector back to normalized coordinates.

The separate-factor product in (3.4) cannot be universally improved if the checker knows only (1.2), (3.1), and (3.2).

Take dimension two with Euclidean metrics

`P_X=R_F=P_Z=R_G=I`,

let

`S_x = a [[0,-1],[1,0]]`,

and choose the conformal chart Jacobian

`J=s I`, `s>0`.

Then the exact physical constant is

`K=a^2`,

while the sharp tangent and covector transport constants are both

`mu_X=mu_F=s^2`.

The pulled curl is

`S_z=s^2 S_x`,

so its exact squared action constant is

**(4.1)**

`K_z=s^4 a^2=mu_F mu_X K`.

Thus a rule that pays only one factor `s^2` is false even for a static linear conformal chart.

### Isolating the tangent-side factor

Keep `J=sI`, `P_X=P_Z=R_F=I`, but take

`R_G=s^(-2) I`.

Then the covector comparison is exact with `mu_F=1`, while `mu_X=s^2`. The pulled action satisfies

`Q_G(S_z eta)=s^2 a^2 ||eta||^2`.

So dropping `mu_X` undercounts by the factor `s^2`.

### Isolating the covector-side factor

Instead take `P_Z=s^2 I`, all force metrics Euclidean. Then `mu_X=1`, `mu_F=s^2`, and relative to `Q_Z` the pulled action again needs the factor `s^2`. Dropping `mu_F` is equally unsound.

These examples also show why tangent and covector metric types must remain explicit in a formal interface.

---

## 5. But the factored product may be arbitrarily conservative

Sharpness of the product under *separate envelopes* does not mean the factored gate is always close to the direct gate.

Take again dimension two, Euclidean metrics, and the unit skew matrix

`S_x=[[0,-1],[1,0]]`.

Let

`J_M = diag(M,1/M)`, with `M>=1`.

The sharp separate Euclidean transport constants are

`mu_X=mu_F=M^2`.

The factored theorem therefore returns

`K_z <= M^4`.

However, two-dimensional skew forms transform by determinant, and here `det J_M=1`. Directly,

**(5.1)**

`J_M^T S_x J_M = S_x`.

Therefore the exact direct constant in (2.1) is

**(5.2)** `K_z=1`.

The ratio between the factored bound and the direct bound is `M^4`, which is unbounded.

This is the main practical conclusion of this child:

> form the signed matrix `J^T S_x J` first whenever possible, and only then certify its quadratic action. Multiplying independent Jacobian/operator caps can destroy all 2-form orientation cancellation.

A failed factored gate is therefore not a mathematical FAIL for the pulled curl. It means only `NOT_CERTIFIED_BY_FACTORED_METRIC_TRANSPORT`; the direct PSD lane remains open.

---

## 6. Radial remainder transport is different from pointwise curl-action transport

T-P5-121 constructs its radial remainder in **physical configuration space**:

`n_x(q) = integral_0^1 s S_x(q0+s(q-q0))(q-q0) ds`,

and proves

**(6.1)**

`4 Q_F(n_x(q)) <= K Q_X(q-q0)`.

At `q=T(z)`, the normalized residual covector is

`n_z(z)=J(z)^T n_x(T(z))`.

For this already-integrated remainder, only the covector transport factor is needed pointwise. From (3.2),

**(6.2)**

`4 Q_G(n_z(z)) <= mu_F K Q_X(T(z)-q0)`.

There is no reason to pay `mu_X` here unless one also wants to replace the finite physical displacement by a normalized displacement bound.

This distinction avoids a common double charge:

- transporting the **curl operator** `S_x` to `S_z` uses one tangent factor and one covector factor;
- transporting the **already formed physical radial remainder** uses the covector factor only, while its finite displacement remains the actual physical secant.

---

## 7. Correct finite-displacement/secant gate

Assume the physical anchor is represented by `q0=T(z0)`. If a producer has a finite-displacement bound

**(7.1)**

`Q_X(T(z)-T(z0)) <= mu_sec Q_Z(z-z0)`,

then (6.2) immediately gives

**(7.2)**

`4 Q_G(n_z(z)) <= mu_F K mu_sec Q_Z(z-z0)`.

This is the correct chart-domain radial-remainder constant.

### Uniform tangent bound implies a secant bound only with segment coverage

Suppose the straight normalized segment

`z_s=z0+s(z-z0)`, `0<=s<=1`,

lies in the chart domain and (3.1) holds with the same `mu_X` for every `z_s`. Since

`T(z)-T(z0)=integral_0^1 J(z_s)(z-z0) ds`,

quadratic Jensen yields

`Q_X(T(z)-T(z0))`

`<= integral_0^1 Q_X(J(z_s)(z-z0)) ds`

`<= mu_X Q_Z(z-z0)`.

Therefore under **whole-segment** tangent coverage one may take

**(7.3)** `mu_sec=mu_X`.

Again, no square root is required.

---

## 8. Hard counterexample: endpoint Jacobian is not a secant certificate

The segment qualifier in Section 7 is necessary.

In one dimension on `[0,1]`, for any `N>0`, define the smooth injective chart

**(8.1)**

`T_N(z)=z+N(2z-z^2)`.

Its derivative is

`T_N'(z)=1+2N(1-z)>0`,

so it is a valid monotone chart on the interval. At the endpoint `z=1`,

**(8.2)** `T_N'(1)=1`.

Thus an endpoint-only tangent comparison would allow `mu_X=1` in Euclidean metrics.

But relative to the anchor `z0=0`,

**(8.3)**

`T_N(1)-T_N(0)=1+N`.

Hence the finite-displacement ratio is

`Q_X(T_N(1)-T_N(0))/Q_Z(1-0)=(1+N)^2`,

which is unbounded with `N`.

Therefore an endpoint Jacobian cap cannot replace a secant/whole-segment chart bound in the radial remainder theorem. This obstruction is independent of source provenance or numerical precision.

---

## 9. Root-free small-gain ledger after chart transport

There are two useful branches.

### 9.1 Physical-displacement storage comparator

Suppose the reshaped storage satisfies

**(9.1)** `m_X Q_X(T(z)-q0) <= V`, `m_X>0`,

and the normalized residual work pairing has

**(9.2)** `<u,n_z>^2 <= Q_U(u) Q_G(n_z)`.

For a **static** chart, or for the generalized-power part after the frame term has been separately accounted for, (6.2) gives

`4 m_X Q_G(n_z) <= mu_F K V`.

Thus if the nominal ledger reserves

`-cV-d Q_U(u)`,

and one chooses losses `alpha>=0`, `delta_d>=0` with `alpha<c`, `delta_d<d`, then the division-free gate

**(9.3)**

`mu_F K <= 16 m_X alpha delta_d`

implies

**(9.4)**

`<u,n_z> <= alpha V + delta_d Q_U(u)`.

This is T-P5-121's scalar discriminant closure with the exact covector transport charge inserted.

### 9.2 Normalized-displacement storage comparator

If instead

`m_Z Q_Z(z-z0) <= V`

and (7.1) holds, then (7.2) yields the gate

**(9.5)**

`mu_F K mu_sec <= 16 m_Z alpha delta_d`.

Under the whole-segment uniform tangent hypothesis, `mu_sec` may be replaced by `mu_X`.

This makes the bookkeeping transparent: the tangent chart factor belongs to converting a finite physical displacement into normalized displacement; it is not automatically owed when the storage already controls the physical displacement.

---

## 10. Moving-chart obstruction: generalized power alone is not the physical work

For a time-dependent chart, T-P5-120 gives

`v = T_t + J u`.

The curl remainder therefore contributes

**(10.1)**

`n_x^T v = n_z^T u + n_x^T T_t`.

Sections 2–9 do not authorize dropping the second term.

The failure is immediate: take `u=0`, `n_x !=0`, and choose `T_t=n_x`. Then

`n_z^T u=0`

while

`n_x^T v=||n_x||^2>0`.

Thus a moving-chart consumer has two honest choices:

1. close the nonconservative work directly in physical velocity variables, where no artificial chart split is introduced; or
2. retain an explicit signed/bounded frame-power packet for `n_x^T T_t` in addition to the generalized-force small-gain gate.

A certificate for only `J^T n_x` cannot be promoted to a certificate for total physical curl-defect power.

---

## 11. Formalizable theorem statements

A minimal theorem family is:

### `curl_action_pullback_direct`

Assume symmetric PSD `P_Z,R_G`, define `S_z=J^T S J`, and assume

`K_z P_Z - S_z^T R_G S_z` is PSD.

Then

`Q_G(S_z eta) <= K_z Q_Z(eta)`.

### `curl_action_pullback_factored`

Assume

`K P_X-S^T R_F S >=0`,

`mu_X P_Z-J^T P_X J >=0`,

`mu_F R_F-J R_G J^T >=0`,

with nonnegative scalar constants. Then

`mu_F mu_X K P_Z-(J^T S J)^T R_G(J^T S J) >=0`.

### `physical_radial_remainder_covector_transport`

Assume

`4Q_F(n_x)<=K Q_X(x)`

and

`Q_G(J^T f)<=mu_F Q_F(f)`.

Then

`4Q_G(J^T n_x)<=mu_F K Q_X(x)`.

### `uniform_tangent_transport_implies_secant`

On a straight covered segment, if

`Q_X(J(z_s)eta)<=mu_X Q_Z(eta)`

for all `s in [0,1]`, then

`Q_X(T(z1)-T(z0))<=mu_X Q_Z(z1-z0)`.

### `chart_curl_small_gain_cleared`

Assume

`4m Q_G(n)<=Kbar V`,

`p^2<=Q_U Q_G(n)`,

and

`Kbar<=16m alpha delta_d`.

Then

`p<=alpha V+delta_d Q_U`.

The last theorem contains only products, squares, and order after the quadratic premises are provided.

---

## 12. Source-facing packet and recommended order

For a real P5 source, the least lossy packet is:

1. same-cell physical skew matrix/action `S_x=Dr-Dr^T` for the actual force/covector field;
2. exact chart Jacobian `J` at the same point and same object ordering;
3. explicit physical tangent/force and normalized tangent/covector quadratic metrics;
4. preferably a direct PSD witness for (2.3);
5. if direct PSD is unavailable, the three factored PSD witnesses (1.2), (3.1), (3.2);
6. for the radial remainder, the physical anchor and star-shaped physical segment from T-P5-121;
7. if replacing physical displacement by normalized displacement, a secant packet (7.1) or a whole-normalized-segment uniform tangent packet, not an endpoint Jacobian sample;
8. for a moving chart, the residual frame-power term `n_x^T T_t` or a decision to close work in physical velocity variables.

Recommended order is **signed matrix first, metric envelope second**. In particular, form `J^T S_x J` before intervalizing independent Jacobian factors whenever source semantics permit it.

---

## 13. Failure semantics

The following statuses must remain distinct:

- direct PSD gate passes: normalized curl action is certified at the stated matrix/source premises;
- factored gate passes: normalized curl action is certified, possibly conservatively;
- factored gate fails but direct gate not checked: `NOT_CERTIFIED_BY_FACTORED_METRIC_TRANSPORT`, not mathematical FAIL;
- endpoint tangent bound only: insufficient for radial finite-displacement replacement;
- moving chart without frame-power packet: insufficient for total physical work;
- no same-cell physical skew-action/source semantics: source-binding obstruction, not repaired by this theorem.

---

## 14. Open boundaries / non-claims

T-P5-122 is **CONDITIONAL_PASS / pending mathematical child** only.

Still open:

- actual deployed same-cell `S_x=Dr-Dr^T` source binding;
- actual rational `P_X,R_F,P_Z,R_G,J` packet and PSD witnesses;
- chart/radial segment coverage needed for any finite-displacement replacement;
- actual moving-chart frame-power budget if `T_t !=0`;
- actual values showing whether the direct gate or factored gate has useful reserve;
- Float64/FD/controller effects, P8 flow coverage, Lean/kernel receipt, provenance/admission, registry, and parent P5/M4 closure.

No such gate is upgraded here.

---

## 15. Bottom line

Approximate curl is a pulled-back 2-form. Quantitatively, the safe factored rule is

`K_z <= mu_F mu_X K`,

with one factor for tangent transport and one for covector transport, and that product is genuinely sharp if those are the only available envelopes.

But it can be catastrophically loose: the area-preserving anisotropic example `J=diag(M,1/M)` has factored cost `M^4` while the exact pulled curl is unchanged. Therefore the strongest practical lane is the direct rational PSD certificate for `J^T S_x J`.

For the already integrated radial remainder, do not automatically pay both factors: covector pullback costs `mu_F`; converting the physical anchor displacement to normalized coordinates costs a **secant** factor, which requires whole-segment information. Endpoint Jacobian control is not enough.
