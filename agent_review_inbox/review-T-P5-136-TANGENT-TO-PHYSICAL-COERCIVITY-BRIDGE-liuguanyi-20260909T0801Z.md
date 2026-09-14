---
kind: review_result
review_id: review-T-P5-136-tangent-to-physical-coercivity-bridge-liuguanyi-20260909T0801Z
task_id: T-P5-136-TANGENT-TO-PHYSICAL-COERCIVITY-BRIDGE
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T08:01:00Z
claim_commit: 037f1d212fc77fb869de1629d4b66c58d679c277
inspected_commit: cc73f3fdc46f582c396f93bd4c4b73927fb647cf
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-132-BOUNDED-CELL-KNOT-RESET-honglianmozun-20260909T0658Z.md
    commit: a521dbad9a0c1dac213ed61e745dff9c2c54cc4f
  - path: agent_review_inbox/review-T-P5-134-NONLINEAR-KNOT-TANGENT-REMAINDER-ABSORPTION-guyuefangyuan-20260909T0732Z.md
    commit: 18b13382a2a71d0d985071c63287909a25284478
  - path: agent_review_inbox/review-T-P5-135-PHYSICAL-SECANT-RADIUS-NO-CURVATURE-TAX-kuangmanmozun-20260909T0743Z.md
    commit: 31f635c582323ac71285d878c50674e94229941e
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_root_free_relative_secant_distortion_then_transport_tangent_coercivity_and_physical_covector_dual_into_existing_physical_knot_reset_consumer
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact quadratic-form and scalar polynomial algebra only
exit_code: n/a
---

# T-P5-136 — tangent-storage to physical-reset coercivity bridge

## 0. Narrow seam

T-P5-135 proved that the sharp T-P5-131/132 physical reset consumer should keep the physical secant

`x = T(c+xi)-T(c) = y+r`

and the physical quadratic quantity

`Qx = Q(x)`

whenever physical coercivity

`m Qx <= Wm`

and the physical covector dual inequality

`p^2 <= B Qx`,  `p=<g,x>`,

are already available. Under those stronger premises there is no reason to split `<g,x>` into tangent and remainder pieces or to pay the T-P5-134 `tau` linear-remainder tax.

The open interface boundary in T-P5-135 section 10.1 is important in practice: a normalized producer may know only a tangent-storage estimate

`m_t q <= Wm`,  `q=Q(y)`,

not yet the physical coercivity premise. T-P5-134 has a two-sided secant/tangent sandwich, but it packages a certificate `0<=delta<=1`; its lower side therefore encounters the genuine `H R<4` nonfolding/small-remainder barrier.

For **coercivity transport** only the upper side is needed. The upper distortion has no such smallness barrier. This child isolates its sharp root-free form, removes the auxiliary `delta`, and shows that one rational relative-distortion witness simultaneously:

1. transports tangent storage coercivity into the physical coercivity required by T-P5-131/132;
2. supplies the physical bounded-cell radius required by T-P5-132;
3. can be paired with an inverse-free matrix PSD certificate for the physical covector dual bound, thereby recovering the no-`tau` physical reset lane from a weaker tangent-storage packet.

No actual chart/source packet, same-cell coverage, Float64/controller semantics, P8 flowpipe, Lean/kernel receipt, independent verification, admission, registry, or parent-gate promotion is claimed.

---

## 1. Secant packet

Let `P` be symmetric positive definite and write

`Q(u) := u^T P u`,

`B_P(u,v) := u^T P v`.

Let

`x := y+r`,

`q := Q(y)`,

`rho := Q(r)`,

`c := B_P(y,r)`.

Assume

**(1.1)** `0 <= q <= R`, with `R>=0`,

and the T-P5-134 second-order chart packet

**(1.2)** `4*rho <= H*q^2`, with `H>=0`.

Gram positivity gives

**(1.3)** `c^2 <= q*rho`.

The target is now a **relative** secant bound

`Qx <= Lambda*q`,

not merely a cell radius `Qx<=Rx`.

---

## 2. Sharp root-free relative upper distortion

Choose `Lambda` and define

**(2.1)**

`D := 4*(Lambda-1) - H*R`.

Check only

**(2.2)** `D >= 0`,

**(2.3)** `D^2 >= 16*H*R`.

Then:

### Theorem A — root-free relative secant upper bound

**(2.4)**

`Q(y+r) <= Lambda * Q(y)`.

### Proof

If `q=0`, then (1.2) gives `rho=0`; positive definiteness gives `y=r=0`, so the conclusion is trivial.

Assume `q>0`. From (1.2) and `q<=R`,

`4*rho <= H*q^2 <= H*R*q`.

Hence

**(2.5)** `4*rho <= H*R*q`.

From Gram positivity,

`c^2 <= q*rho <= (H*R/4) q^2`.

We claim

**(2.6)** `8*c <= D*q`.

If `c<=0`, this follows from `D*q>=0`. If `c>0`, then

`(8*c)^2 = 64*c^2 <= 16*H*R*q^2 <= D^2*q^2 = (D*q)^2`.

Both `8*c` and `D*q` are nonnegative, so `8*c<=D*q`.

Now

`4*Qx = 4*q + 8*c + 4*rho`

`       <= 4*q + D*q + H*R*q`

`       = 4*Lambda*q`.

Thus `Qx<=Lambda*q`.

The trusted statement uses only quadratic-form nonnegativity, multiplication, squaring, addition, and order. No square root, division, matrix inverse, eigenvalue, singular value, or Young parameter is required.

---

## 3. Sharpness and exact interpretation

For interpretation only, the least possible real uniform factor under (1.1)-(1.3) is

`Lambda_min = (1 + sqrt(H*R)/2)^2`.

The checker never needs this expression. Conditions (2.2)-(2.3) are exactly its branch-safe root-free form.

Sharpness follows already in one dimension with `Q(u)=u^2`: take `q=R` and choose positive aligned `r` saturating

`4*rho = H*R^2`.

Then

`Q(y+r)/Q(y) = Lambda_min`.

A rational equality regression is

`R=1`, `H=9`, `y=1`, `r=3/2`.

Then

`q=1`, `rho=9/4`, `Qx=25/4`.

Take

`Lambda=25/4`.

Then

`D = 4*(25/4-1)-9 = 12`,

`D^2 = 144 = 16*9*1`,

and (2.4) is equality.

This is the same large-curvature example used by T-P5-135 to show that physical-radius certification remains meaningful when `H R>4`. The new point is that the **relative upper** distortion also remains perfectly valid there.

---

## 4. Why the `H R<4` barrier is irrelevant for upper coercivity transport

T-P5-134's two-sided packet chooses `delta` with

`rho <= delta^2 q`

and then uses

`(1-delta)^2 q <= Qx <= (1+delta)^2 q`.

A positive lower factor needs `delta<1`; with only `4rho<=Hq^2` on `q<=R`, this indeed forces a smallness condition comparable to `H R<4`.

But the upper identity itself has no such restriction. For every `delta>=0`,

`delta * [(1+delta)^2 q - Qx]`

` = Q(r-delta*y) + (1+delta)*(delta^2 q-rho)`,

so whenever `rho<=delta^2 q`, the upper bound is sound even for `delta>1`.

Theorem A is the same fact after eliminating the auxiliary square-root-like `delta` and replacing it by the directly consumable rational factor `Lambda`. Therefore:

**upper secant transport has no information-theoretic `H R<4` barrier; only lower secant transport does.**

This distinction is exactly what the coercivity bridge needs.

---

## 5. Tangent coercivity -> physical coercivity without division

Assume a tangent-storage packet gives

**(5.1)** `m_t*q <= Wm`, with `m_t>0`.

After Theorem A, choose any rational `m_x>0` satisfying

**(5.2)**

`Lambda * m_x <= m_t`.

Then

`m_x*Qx <= m_x*Lambda*q <= m_t*q <= Wm`.

Hence:

### Theorem B — physical coercivity transport

**(5.3)**

`m_x * Qx <= Wm`.

This is exactly premise (1.1) of T-P5-132, now recovered from a weaker tangent-storage contract.

The producer may regard `m_t/Lambda` as the optimal real choice, but the trusted checker need never divide. It accepts a proposed positive rational `m_x` and verifies only `Lambda*m_x<=m_t`.

### Exact large-curvature regression

Continue the rational example

`R=1`, `H=9`, `Lambda=25/4`.

If

`q <= Wm`

so `m_t=1`, choose

`m_x=4/25`.

Then

`Lambda*m_x = 1 = m_t`,

hence

`(4/25) Qx <= Wm`.

At the equality witness `Qx=25/4`, `q=Wm=1`, this is exact.

Thus even though the T-P5-134 **lower** sandwich cannot use a certificate `delta<=1` when `H R=9`, tangent storage can still be transported to a valid physical coercivity theorem. The price is a weaker coercivity constant, not failure of the interface.

---

## 6. One relative-distortion witness also supplies the physical radius

From

`Qx <= Lambda*q`

and

`q<=R`,

immediately

**(6.1)**

`Qx <= Rx`, with `Rx := Lambda*R`.

Therefore the same `Lambda` witness can feed both physical premises needed downstream:

- T-P5-131/132 coercivity through Theorem B;
- T-P5-132 bounded-cell radius through `Rx=Lambda R`.

This is not a weaker replacement for T-P5-135's sharp radius theorem. It is the same sharp information written relatively.

Indeed define T-P5-135's radius discriminant

`D_rad := 4*(Rx-R)-H*R^2`.

With `Rx=Lambda R`,

**(6.2)**

`D_rad = R * D`.

For `R>0`, the radius square gate

`D_rad^2 >= 16*H*R^3`

is exactly

`R^2 D^2 >= 16*H*R^3`,

hence equivalent to

`D^2 >= 16*H*R`.

For `R=0`, (1.1)-(1.2) already force `Qx=0`.

So a producer that needs both coercivity transport and a bounded reset cell should export **one** relative-distortion certificate `Lambda`, not independently optimize `Lambda` and `Rx`.

---

## 7. Physical covector dual without inverse or chart splitting

T-P5-135's second structural premise is

`p^2 <= B Qx`,  `p=<g,x>`.

If the physical metric `P` and physical covector column `g` are available, this theorem can be certified globally by a single matrix PSD condition.

Assume

**(7.1)** `B>=0`,

**(7.2)**

`B*P - g*g^T >= 0`  as a symmetric matrix.

Then for every physical displacement `u`,

`u^T(BP-gg^T)u >= 0`,

so

### Theorem C — inverse-free physical dual certificate

**(7.3)**

`<g,u>^2 <= B * Q(u)`.

In particular, for the exact nonlinear secant `u=x`,

**(7.4)** `p^2 <= B Qx`.

For rational `P,g,B`, the source/checker boundary can therefore remain exact-rational matrix arithmetic. There is no need to compute `P^{-1}`, a dual norm, a matrix square root, an eigenvalue, or a singular value.

This is deliberately a **physical covector** certificate. If the source has only a tangent covector `J0^T g` but has not bound the physical `g` or the same physical metric `P`, (7.2) cannot be inferred by type erasure. That weaker case remains fail-closed and may require T-P5-134's tangent/remainder route.

---

## 8. Main adapter theorem: tangent packet -> physical T-P5-132 packet

Combine the preceding leaves.

Assume under one immutable knot/chart/storage identity:

1. `x=y+r`, `q=Q(y)`, `Qx=Q(x)`;
2. `0<=q<=R`, `R>=0`;
3. `4Q(r)<=H q^2`, `H>=0`;
4. `D=4(Lambda-1)-H R >=0`;
5. `D^2>=16 H R`;
6. tangent storage coercivity `m_t q<=Wm`, `m_t>0`;
7. proposed physical coercivity constant `m_x>0` with `Lambda*m_x<=m_t`;
8. physical covector packet `g`, `B>=0`, `BP-gg^T>=0`;
9. the existing T-P5-130/131 physical reset envelope
   `Wp <= Wm + p + ell Qx + C0`, with `p=<g,x>`;
10. the existing center-relocation scalar premise `4*mu*C0<=B`, `mu>0`.

Then the adapter derives

**(8.1)** `m_x Qx <= Wm`,

**(8.2)** `p^2 <= B Qx`,

**(8.3)** `Qx <= Lambda R`.

Therefore T-P5-132 may be instantiated directly with

`m := m_x`,

`R_x := Lambda R`,

`A_x := m_x*(kappa-1)-ell`.

The sharp physical reset theorem then proceeds exactly as written, including its interior/boundary branch logic and root-free boundary polynomial gate.

### What chart curvature now costs

Under this adapter, chart nonlinearity is charged in two places only:

- degradation from `m_t` to `m_x` through `Lambda*m_x<=m_t`;
- expansion of the physical radius from `R` to `Lambda R`.

There is **no separate linear remainder tax `tau`** because the signed physical work `p=<g,x>` is never split.

This is strictly preferable to the tangent-only T-P5-134 fallback whenever the physical `P,g` packet is available and the weakened `m_x` still leaves useful reset headroom.

---

## 9. Interaction with the reset headroom `A`

The physical reset coefficient becomes

`A_x = m_x*(kappa-1)-ell`.

Thus this bridge does not claim that nonlinear charts are free: if `Lambda` is large, the strongest certifiable `m_x` may be much smaller than `m_t`, and `A_x` may decrease or even become nonpositive.

However this loss has a precise meaning: it is a **coercivity distortion**, not a separate fictitious force or linear-remainder budget.

If `A_x>0`, T-P5-131's global/interior branch may still apply. If `A_x<=0`, T-P5-132 remains mathematically usable because the physical radius `R_x=Lambda R` is finite and its boundary branch explicitly handles `A<=0`.

So large chart curvature should not automatically force a return to the tangent `tau` architecture. The correct decision is:

1. compute/certify the relative upper distortion `Lambda`;
2. transport `m_t` to a physical `m_x`;
3. retain the physical signed work with Theorem C;
4. let the existing T-P5-132 branch logic decide whether the resulting `A_x` is interior-positive or boundary-dominated.

---

## 10. Why this is stronger than merely exporting a physical radius

T-P5-135's `Qx<=Rx` theorem is sufficient for the bounded-cell reset only if physical coercivity already exists.

A radius cap by itself does **not** imply

`m_x Qx <= Wm`.

The relative theorem `Qx<=Lambda q` does. That is the exact interface distinction:

- absolute radius transport answers: “where can the physical secant lie?”
- relative upper distortion answers: “how much physical quadratic energy can one unit of tangent quadratic energy produce?”

The latter is the missing lemma needed to move a storage lower bound from tangent coordinates to the physical secant state.

---

## 11. Fail-closed boundaries

### 11.1 No lower secant theorem is claimed

Theorem A is upper-only. It does not imply

`a q <= Qx`

for any positive `a` when `H R` is large. Indeed if the allowed remainder can satisfy `r=-y`, then `x=0` while `q>0`.

Therefore this child must not be used to infer chart injectivity, a lower metric distortion, or normalized critical-point uniqueness.

### 11.2 Physical dual semantics remain typed

The matrix condition `BP-gg^T>=0` requires the **same physical metric `P` and physical covector `g`** that define `Qx` and `p` in the reset envelope. A bound on `J0^T g`, a Euclidean norm of some coefficient vector, or a differently normalized metric is not interchangeable without another theorem.

### 11.3 Tangent storage must be the same pre-knot storage

The premise `m_t q<=Wm` must use the same `Wm` appearing in the reset envelope. A geometric tangent bound for an unrelated Lyapunov function does not transport T-P5-132 coercivity.

### 11.4 Whole-segment curvature packet remains necessary

The source of `4Q(r)<=Hq^2` is still T-P5-134's whole-segment Hessian-action theorem. Endpoint/anchor Hessian data alone do not justify this remainder estimate.

### 11.5 Source and runtime semantics are untouched

Nothing here proves that deployed Float64/controller/reference code realizes `T`, `P`, `g`, `Wm`, or the same knot state. Those remain separate source/coverage/runtime obligations.

---

## 12. Recommended formalizable leaves

A minimal Lean split is:

1. `secant_upper_distortion_root_free`
   - premises `Q y<=R`, `4*Q r<=H*(Q y)^2`, `H>=0`, `R>=0`;
   - `D=4*(Lambda-1)-H*R`, `D>=0`, `D^2>=16*H*R`;
   - conclusion `Q(y+r)<=Lambda*Q(y)`.

2. `tangent_coercivity_to_physical_secant`
   - consumes leaf 1, `m_t*Q(y)<=Wm`, `0<m_x`, `Lambda*m_x<=m_t`;
   - concludes `m_x*Q(y+r)<=Wm`.

3. `covector_dual_of_psd`
   - symmetric PSD premise `B*P-g*g^T>=0`;
   - concludes `(g^T u)^2<=B*(u^T P u)` for all `u`.

4. `relative_distortion_implies_radius`
   - `Qx<=Lambda*q`, `q<=R`;
   - concludes `Qx<=Lambda*R`.

5. `tangent_packet_to_bounded_physical_reset`
   - packages leaves 1-4 into the exact premise surface expected by T-P5-132;
   - no source or admission fields inside the mathematical theorem.

A useful regression should instantiate

`R=1`, `H=9`, `Lambda=25/4`, `m_t=1`, `m_x=4/25`

and verify equality on `y=1`, `r=3/2`.

---

## 13. Typed source packet and next seam

The minimal same-key producer packet is now:

- `storageKey`, `knotKey`, `chartKey`, `physicalMetricKey`, `physicalCovectorKey`;
- physical `P` and `g`;
- exact secant decomposition `x=y+r` with `y=J0 xi`;
- tangent radius `q<=R`;
- whole-segment second-order packet `4Q(r)<=Hq^2`;
- rational `Lambda` with the two root-free distortion gates;
- tangent storage coercivity `m_t q<=Wm`;
- rational `m_x>0` with `Lambda*m_x<=m_t`;
- rational `B>=0` with exact PSD certificate `BP-gg^T>=0`;
- the already-defined physical reset envelope and center-relocation constant.

If this packet is available, the actual nonlinear chart no longer needs a separate tangent linear-remainder budget: it can feed the sharp physical T-P5-132 consumer directly with `m_x` and `R_x=Lambda R`.

The highest-value next mathematical/source question is therefore narrow: **does the actual knot packet expose one physical metric/covector pair `(P,g)` consistent with the reset envelope, and one tangent-storage coercivity bound for the same `Wm`?** If yes, this bridge supplies the missing cross-coordinate theorem. If no, T-P5-134 remains the sound weaker fallback.

---

## 14. Status

Mathematical results established in this review:

- sharp root-free relative upper secant distortion: **proved**;
- no `H R<4` smallness requirement for upper-only transport: **proved**;
- tangent-storage -> physical coercivity transport via one multiplication gate: **proved**;
- one relative-distortion witness simultaneously gives the sharp physical radius: **proved**;
- inverse-free physical covector dual theorem from `BP-gg^T>=0`: **proved**;
- composition into the T-P5-132 physical reset premise surface: **proved conditionally on typed packet premises**;
- sharp rational large-curvature equality regression: **provided**.

Still open:

- actual same-key `P/g/T/J0/Wm` source packet;
- actual tangent coercivity and physical covector PSD witness;
- whole-segment chart/Hessian source coverage;
- Float64/controller/reference/FD semantics;
- P8 flowpipe/domain coverage;
- Lean/kernel verification;
- independent verification by 封不觉;
- admission, registry, and any P5/M4 parent promotion.

Final status: **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source semantics**.
