---
kind: review_result
review_id: review-T-P5-058-guyuefangyuan-20260908T0120
task_id: T-P5-058-QUADRATIC-RADICAL-CANCEL
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-08T01:18:00-06:00
created_at: 2026-09-08T01:20:00-06:00
claim_commit: 224d5e288c7f90a59c246522f81570cd6f2371b3
parent_task: T-P5-057-RADICAL-FACTOR-CANCEL
parent_review: review-T-P5-057-radical-factor-cancel-liuguanyi-20260908T0122
parent_commit: 34a6cdd4f58a91ff22847fc041a9695637813751
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a square-only radical-cancellation consumer which removes the balanced odd sign obstruction whenever downstream mathematics needs only the pointwise quadratic magnitude; keep centered/signed consumers on the T-P5-057 parity-sensitive lane
---

# T-P5-058 — parity-free quadratic radical cancellation

## 0. Bottleneck and non-overlap

`T-P5-057` classifies the signed normalized primitive

`u = G / sqrt(A)`

under an exact common-factor packet

`A = h^(2m) S`, `G = h^q J`, `S>0`.

Its sharp obstruction is the balanced odd case `q=m` when `h` changes sign: `u` can jump even though the blow-up is removed. That obstruction is real for signed or centered residual consumers.

However, several energy/majorant interfaces ultimately consume only a pointwise square such as `u^2`, `b_i^2`, or a diagonal quadratic magnitude. In that narrower lane the sign is algebraically irrelevant. This review isolates the exact theorem, supplies radical-free rational variation bounds, and gives an explicit negative control showing why it must **not** be reused for centered differences.

This is source-independent mathematics only. It does not overlap the currently claimed `T-P5-056` Lean work and makes no source/Float64/coverage/provenance/admission claim.

---

## 1. Exact square cancellation

Assume integers `m>=1`, `q>=0` and, on one real cell,

`A = h^(2m) S`,

`G = h^q J`,

`S>0`.

At every point with `h != 0`, we have `A>0`, so

`u^2 = (G/sqrt(A))^2 = G^2/A`.

Therefore

`u^2 = h^(2q) J^2 / (h^(2m) S)`.

If `q=m+k` with `k>=0`, exact cancellation gives

**(1.1)** `u^2 = h^(2k) J^2 / S`  for `h != 0`.

Define the **quadratic reduced primitive** on the entire cell by

**(1.2)** `W := h^(2k) J^2 / S`.

Then `W=u^2` wherever the original radical quotient is defined, while `W` itself is defined at `h=0` because `S>0`.

The decisive point is that (1.2) contains neither a square root nor `sign(h)`.

### Balanced case `q=m`

Here `k=0`, so

**(1.3)** `W = J^2/S`.

This extension is valid for **every parity of `m`** and does not require `h` to have fixed sign. In particular, the balanced odd sign jump from `T-P5-057` disappears for a pointwise square-only consumer.

### Over-cancelled case `q>m`

Here `k>=1`, so

`W = h^(2k) J^2/S`.

The factor `h^(2k)` is an ordinary even polynomial factor. Hence `W` extends through every zero/sign change of `h`, and in fact vanishes at such a zero whenever `J,S` stay finite with `S>0`.

### Under-cancelled case `q<m`

Squaring does **not** rescue insufficient numerator order. With `h(t)=t`, `S=J=1`, `m=1`, `q=0`,

`u^2 = 1/t^2`,

which diverges at zero. Thus the quadratic lane has the sharp generic threshold

**`q>=m`**,

whereas the signed two-sided continuous lane of `T-P5-057` can require strictly more information in the balanced odd case.

---

## 2. Pointwise radical-free energy bound

Let `q=m+k`, `k>=0`, and assume on the cell

`|h| <= H`,

`|J| <= MJ`,

`S >= s0 > 0`.

Since `W>=0`, (1.2) gives immediately

**(2.1)** `W <= H^(2k) MJ^2 / s0`.

Equivalently, the division-free rational form is

**(2.2)** `s0 * W <= H^(2k) MJ^2`.

For the balanced case `k=0`, this becomes simply

**(2.3)** `s0 * W <= MJ^2`.

Thus if a P5 consumer needs only a raw squared magnitude `u^2 <= E`, a factor packet with `q>=m` can discharge that magnitude without any lower bound on the original radicand `A`. Only the residual factor `S` needs a positive lower bound.

No square root or parity branch enters (2.2).

---

## 3. Radical-free two-point Lipschitz bound for the square itself

The same cancellation gives a useful variation theorem for consumers that need `W(eta)` to vary regularly but still do not need the signed primitive `u`.

Assume two points `eta,eta0` in the same cell satisfy

`|h|, |h0| <= H`,

`|h-h0| <= Lh |eta-eta0|`,

`|J|, |J0| <= MJ`,

`|J-J0| <= LJ |eta-eta0|`,

`S,S0 >= s0 > 0`,

`|S-S0| <= LS |eta-eta0|`.

Write `Delta eta = eta-eta0`.

For `k>=1`, the integer-power identity gives

`|h^(2k)-h0^(2k)| <= 2k H^(2k-1) |h-h0|`.

Also

`|J^2-J0^2| <= 2 MJ |J-J0|`,

and

`|1/S - 1/S0| <= |S-S0|/s0^2`.

Using the telescoping decomposition

`W-W0`

`= (h^(2k)-h0^(2k)) J^2/S`

`  + h0^(2k) (J^2-J0^2)/S`

`  + h0^(2k) J0^2 (1/S-1/S0)`,

we obtain

**(3.1)** for `k>=1`,

`|W-W0| <= CW |Delta eta|`,

with

`CW = 2k H^(2k-1)Lh MJ^2/s0`

`   + H^(2k) [2 MJ LJ/s0 + MJ^2 LS/s0^2]`.

For the balanced case `k=0`, the first term vanishes and no `h` regularity is needed:

**(3.2)**

`|W-W0| <= [2 MJ LJ/s0 + MJ^2 LS/s0^2] |Delta eta|`.

A checker that wants to avoid all divisions can use the equivalent scaled forms

**(3.3)** for `k>=1`,

`s0^2 |W-W0|`

`<= [2k H^(2k-1)Lh MJ^2 s0`

`   + H^(2k)(2 MJ LJ s0 + MJ^2 LS)] |Delta eta|`,

and

**(3.4)** for `k=0`,

`s0^2 |W-W0| <= (2 MJ LJ s0 + MJ^2 LS) |Delta eta|`.

If the source envelope data are rational, every constant in (2.2), (3.3), and (3.4) is exact rational. No `sqrt`, numerical root, eigenvalue, sign split, or floating optimization is required.

---

## 4. Strict enlargement over the signed balanced-odd lane

The new lane is not merely a cosmetic rewrite. Consider the exact rational model

`h(t)=t`, `m=q=1`, `J=1`, `S=1`.

Then

`A=t^2`, `G=t`.

For `t!=0`,

`u(t)=t/|t|=sign(t)`.

So the signed primitive has no continuous extension across zero. This is exactly the balanced odd obstruction of `T-P5-057`.

But the quadratic reduced primitive is

**(4.1)** `W(t)=u(t)^2=1` for `t!=0`,

and the exact extension is simply

**(4.2)** `W(t)=1` for all `t`.

Hence the square-only lane has Lipschitz constant **zero** on this example, while the signed lane is discontinuous.

This is a genuine enlargement of the certifiable mathematical region for consumers that only use pointwise quadratic magnitude.

---

## 5. Critical obstruction: do not use `W` for centered signed residuals

The previous example also gives the exact negative control needed to prevent an unsound transport.

For every `eps>0`,

`u(eps)=1`, `u(-eps)=-1`,

so

**(5.1)** `(u(eps)-u(-eps))^2 = 4`.

But

**(5.2)** `W(eps)-W(-eps)=0`.

Therefore variation of `W=u^2` gives no control on the centered signed quantity `(Delta u)^2` across a sign-changing balanced root. In fact there is no finite constant `C` satisfying

`(u(eps)-u(-eps))^2 <= C |2eps|^2`

for all sufficiently small `eps`, because the left side stays `4` while the right side tends to zero.

So the consumer split must be explicit:

- **safe quadratic lane:** pointwise `u^2`, `|u|^2`, diagonal bias-square or energy magnitude;
- **unsafe to replace:** `u`, `Delta u`, `(Delta u)^2`, signed cross terms, or any consumer whose algebra depends on relative sign across points/components.

Those centered/signed consumers remain on the parity-sensitive `T-P5-057` lane and may require exact root splitting, fixed sign, or an additional numerator zero.

This distinction should be encoded in the type/interface rather than left as a prose convention.

---

## 6. Source/checker decision rule

Given an exact factor packet

`A=h^(2m)S`, `G=h^q J`, `S>=s0>0`,

the checker can use the following fail-closed decision tree.

1. If the downstream object is signed or centered, use `T-P5-057` unchanged.
2. If the downstream object is pointwise square-only:
   - if `q<m`, fail closed or refactor `G` to expose additional numerator zeros;
   - if `q>=m`, set `k=q-m` and replace the radical node by the exact rational primitive
     `W=h^(2k)J^2/S`;
   - use (2.2) for pointwise energy, or (3.3)/(3.4) if variation of the square itself is needed.
3. Do **not** infer implementation safety at the zero from the mathematical extension. A deployed evaluator that still computes the original `0/0` expression must be rewritten/bound to the cancelled expression before source admission.

This separates three previously conflated questions: algebraic magnitude removability, signed continuity, and executable source identity.

---

## 7. Suggested Lean theorem decomposition

Keep this sidecar smaller than the generic radical package. A practical decomposition is:

1. `normalized_square_eq_ratio`
   - assumptions: `0<A`;
   - conclusion: `(G / Real.sqrt A)^2 = G^2/A`.

2. `normalized_square_factor_cancel`
   - parameterize `q=m+k` to avoid Nat subtraction;
   - assumptions: `S>0`, `h!=0`;
   - conclusion:
     `(h^(m+k)*J / Real.sqrt(h^(2*m)*S))^2 = h^(2*k)*J^2/S`.

3. `balanced_square_extension_no_parity`
   - `k=0` specialization;
   - conclusion away from the root is `J^2/S`, with no parity/fixed-sign hypothesis.

4. `cancelled_square_pointwise_bound`
   - prove division-free `s0*W <= H^(2*k)*MJ^2` from amplitude hypotheses.

5. `cancelled_square_two_point_bound_zero`
   - `k=0`, theorem (3.4).

6. `cancelled_square_two_point_bound_pos`
   - `k>=1`, theorem (3.3), using the standard Nat-power difference estimate.

7. Regression theorem `balanced_odd_signed_jump_square_constant`
   - instantiate `h=t`, `m=q=1`, `J=S=1`;
   - square extension is constant although the signed quotient changes sign.

8. Regression theorem `centered_square_not_controlled_by_square_variation`
   - same model; record `(u eps-u (-eps))^2=4` while `W eps-W (-eps)=0` for `eps>0`.

The trusted consumer should expose whether it asks for `PointwiseSquare` or `CenteredSignedDifference`; this prevents the square-only theorem from being accidentally applied to the wrong semantic object.

---

## 8. Dependencies and remaining gaps

Depends mathematically on the exact factor packet interface of `T-P5-057` and, upstream, on a source-side/zero-contact mechanism capable of producing `A=h^(2m)S`, `G=h^qJ` with `S>=s0>0` on the same cell.

Still open and **not claimed here**:

- whether the real CSE/source graph contains such a same-key factor packet;
- whether the relevant P5 consumer is truly pointwise-square-only or instead centered/signed;
- exact source identity for the cancelled expression at `h=0`;
- Float64/libm and `0/0` execution semantics;
- cell coverage / P8 ODE continuation;
- Lean compilation, axiom audit, comparator, receipt/provenance;
- registry or P5/P8/M4 admission.

Status remains **pending mathematical child**.
