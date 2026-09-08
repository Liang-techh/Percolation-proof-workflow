---
kind: review_result
review_id: review-T-P5-057-radical-factor-cancel-liuguanyi-20260908T0122
task_id: T-P5-057-RADICAL-FACTOR-CANCEL
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T01:06:00-06:00
created_at: 2026-09-08T01:22:00-06:00
claim_commit: 1e233bde42458bf8c555c3151caad729dd2d406e
inspected_commit: 14d23250b895fd0d0471ca40db72207d0fd62429
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-056-honglianmozun-20260908T0100.md
  - agent_review_inbox/review-T-P5-056-zero-contact-factor-kuangmanmozun-20260908T0043.md
  - agent_review_inbox/review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a removable-radical / vanishing-order bridge between exact zero-contact factor certificates and the eta-Lipschitz source packet; do not require a false positive lower bound for the original radicand when a certified common square factor can be cancelled
---

# T-P5-057 — removable radical factor and vanishing-order bridge

## 0. Bottleneck

The latest radical eta-Lipschitz child correctly proves that a generic primitive

`u(eta) = G(eta) / sqrt(A(eta))`

needs a strict positive radicand margin if it is treated as a black-box radical node. It also records the exact obstruction `A(eta)=eta`: `sqrt(A)` is only 1/2-Holder at zero.

Separately, the exact zero-contact child shows that a nonnegative rational polynomial of degree at most three can expose an interior double-root factor exactly, e.g.

`A(t) = (t-r)^2 L(t)`.

Those two results leave one source-to-math gap: a touching-zero radicand is not automatically singular if the numerator shares the correct algebraic factor. The correct interface must distinguish true singularity from a removable common-factor singularity before asking for a positive lower bound on `A`.

This review gives that bridge and a complete vanishing-order classification for the common-factor packet.

No deployed-source, Float64/libm, factor-discovery, coverage, Lean-compilation, comparator, registry, or admission claim is made.

---

## 1. Exact common-factor identity

Let `m >= 1`, `q >= 0` be integers and suppose on one mathematical cell

`A = h^(2m) * S`,

`G = h^q * J`,

with `S > 0`.

Because

`h^(2m) = |h|^(2m)`,

we have the exact principal-square-root identity

**(1.1)** `sqrt(A) = |h|^m * sqrt(S)`.

Hence at every point with `h != 0`,

**(1.2)**

`G/sqrt(A) = sign(h)^q * |h|^(q-m) * J/sqrt(S)`.

This identity is the whole bridge. The singular behavior is controlled by the difference between the numerator order `q` and the half-radicand order `m`, not by the fact that `A` itself reaches zero.

The source checker therefore should not immediately reject a zero lower bound for `A`. It should first ask whether an exact factor packet `(h,m,q,S,J)` exists.

---

## 2. Vanishing-order classification

Write

`Vred := J/sqrt(S)`.

Assume only that `Vred` stays bounded near a zero of `h`.

### 2.1 Under-cancelled case: `q < m`

Then (1.2) contains the negative power

`|h|^(-(m-q))`.

There is no generic bounded extension theorem. Exact negative control:

`h(t)=t`, `S=1`, `J=1`, `m=1`, `q=0`

gives

`G/sqrt(A)=1/|t|`,

which diverges at zero.

So `q<m` must remain fail-closed unless an additional numerator-vanishing witness is supplied. If such a witness exists, the correct action is to refactor `G` and increase `q`; it must not be hidden inside a numerical interval bound.

### 2.2 Balanced case: `q = m`

Equation (1.2) becomes

**(2.1)** `G/sqrt(A) = sign(h)^m * Vred` for `h != 0`.

There are two sound removable lanes.

1. **`m` even.** Then `sign(h)^m=1` on both sides, so the unique natural extension is simply

   **`u_ext = Vred`**.

   No sign condition on `h` is needed.

2. **`m` odd but `h` has a fixed sign on the cell.**
   - if `h >= 0`, use `u_ext=Vred`;
   - if `h <= 0`, use `u_ext=-Vred`.

The important obstruction is the missing third case: if `m` is odd and the cell contains a genuine sign change of `h`, there is no generic continuous extension. Exact example:

`A(t)=t^2`, `G(t)=t`, `S=J=1`, `m=q=1`.

For `t != 0`,

`G/sqrt(A)=t/|t|=sign(t)`.

The two one-sided limits are `-1` and `+1`.

Thus **one numerator zero cancels the blow-up but not necessarily the sign jump**. A two-sided cell may need to be split at the exact zero, or it needs an additional vanishing witness in the numerator.

### 2.3 Over-cancelled case: `q > m`

Let

`k := q-m >= 1`.

Define the scalar factor

`psi(h) = sign(h)^q * |h|^k` for `h != 0`,

and set `psi(0)=0`.

Then `psi` is continuous for every parity of `q`, so

**(2.2)** `u_ext := psi(h) * Vred`

is a continuous removable extension whenever `Vred` is bounded/continuous.

In particular, no fixed-sign condition on `h` is required once the numerator vanishes at least one order more strongly than the square-root denominator.

This gives the sharp qualitative trichotomy:

`q<m`  -> generic blow-up possible;

`q=m`  -> bounded, but odd balanced order may retain a sign jump;

`q>m`  -> zero-contact is generically removable.

---

## 3. Exact Lipschitz control of the over-cancelled factor

The previous section is not only topological. It gives a quantitative source contract.

Let `k=q-m>=1`. Assume on the same cell

`|h| <= H`,

`|h(eta)-h(eta0)| <= Lh * |eta-eta0|`,

with `H >= 0`, `Lh >= 0`.

For either possible parity form of `psi`, one has the scalar power bound

**(3.1)**

`|psi(h)-psi(h0)| <= k * H^(k-1) * |h-h0|`.

Hence

**(3.2)**

`Lip_eta(psi(h)) <= k * H^(k-1) * Lh`,

and

**(3.3)** `|psi(h)| <= H^k`.

Now suppose the reduced numerator has

`|J| <= MJ`,

`|Delta J| <= LJ |Delta eta|`.

Define the reduced numerator

`K := psi(h) * J`.

Then exact product transport gives

**(3.4)** `|K| <= MK := H^k * MJ`,

**(3.5)**

`|Delta K| <= LK |Delta eta|`,

where one valid exact bound is

**`LK := H^k * LJ + k * H^(k-1) * Lh * MJ`.**

This is source-friendly: it uses only amplitude/variation data and integer powers. The zero of `h` does not create any denominator in this step.

For the balanced removable lanes (`q=m`, even `m` or fixed-sign `h`), simply take `K=+J` or `K=-J`, so `MK=MJ` and `LK=LJ`.

---

## 4. Reduced radical Lipschitz theorem: charge only the residual radicand

After the exact cancellation above, every removable lane has the form

`u_ext = K / sqrt(S)`

with `S` the **residual radicand**.

This is the key source-to-math payoff: the positive-margin obligation belongs to `S`, not to the original touching-zero radicand `A=h^(2m)S`.

Assume

`S >= mu^2 > 0`,

`|Delta S| <= LS |Delta eta|`,

`|K| <= MK`,

`|Delta K| <= LK |Delta eta|`.

Then the existing normalized-radical two-point algebra applies verbatim to the reduced packet and yields

**(4.1)**

`|Delta u_ext| <= [LK/mu + MK*LS/(2*mu^3)] |Delta eta|`.

Equivalently, the division-free scaled form is

**(4.2)**

`2*mu^3 |Delta u_ext| <= (2*mu^2*LK + MK*LS) |Delta eta|`.

Crucially, neither bound contains a lower bound for `A`. `A` may equal zero on the cell.

This is exactly the missing exception to the generic positive-radicand-margin rule: a certified common factor moves the margin requirement from `A` to `S`.

---

## 5. Radical-free squared P5 consumer

If the downstream P5 ledger prefers squared gains, use an exact rational lower bound

`S >= s0 > 0`

instead of introducing `mu=sqrt(s0)`.

For any rational `theta>0`, the reduced packet satisfies

**(5.1)**

`4*theta*s0^3 * |Delta u_ext|^2`

`<= (1+theta) * (4*theta*s0^2*LK^2 + MK^2*LS^2) * |Delta eta|^2`.

All constants in (5.1) can remain exact rational if the source factor packet and variation bounds are rational.

For `q>m`, substitute the explicit values

`MK = H^k MJ`,

`LK = H^k LJ + k H^(k-1)Lh MJ`.

For the balanced removable lanes, substitute `MK=MJ`, `LK=LJ`.

Thus a future source checker can hand the result directly to the existing squared residual / correlated perturbation lane without ever manufacturing a fake `A>=epsilon>0` premise.

---

## 6. Direct bridge from the zero-contact factor certificate

The low-degree zero-contact result makes this especially concrete.

Suppose an exact factor certificate gives

`A(t) = (t-r)^2 * L(t)`

with

`L(t) >= s0 > 0`

on a cell.

Take

`h=t-r`, `m=1`, `S=L`.

Now the numerator order determines the correct source branch.

### 6.1 Numerator does not vanish: `G=J`

This is `q=0<m=1`.

If `J(r) != 0`, the primitive behaves like `1/|t-r|`; no uniform bounded/Lipschitz certificate exists across the contact.

### 6.2 Numerator vanishes once: `G=(t-r)J`

This is the balanced odd case `q=m=1`:

`G/sqrt(A) = sign(t-r) * J/sqrt(L)`.

If `r` is an interior point and the cell straddles `r`, a nonzero `J(r)` produces a jump. The correct repair is one of:

1. split the cell exactly at the rational root `r` and use the two fixed-sign reduced lanes;
2. prove an additional numerator zero and refactor to `q>=2`;
3. provide a separate special cancellation theorem strong enough to control the two-sided limit.

At an endpoint, or on any one-sided cell where `t-r` has fixed sign, the same `q=1` factor is already removable.

### 6.3 Numerator vanishes at least twice: `G=(t-r)^q J`, `q>=2`

Now `q>m`, so the extension is continuous automatically. For the first over-cancelled case `q=2`,

`G/sqrt(A) = |t-r| * J/sqrt(L)`

away from the root and extends by zero at `t=r`.

Therefore the zero-contact factor checker and radical eta-Lipschitz checker can be composed with a small deterministic decision tree rather than fighting each other.

---

## 7. Why absolute-value intervalization must happen after factor analysis

The balanced odd example also exposes an interface-ordering bug.

If source algebra has

`A=t^2`, `G=t`,

then exact factor analysis sees `m=q=1` and immediately exposes the sign-jump boundary.

If a checker first replaces `G` by `|G|<=|t|` and treats only magnitudes, it can no longer distinguish

`G=t`

from

`G=|t|`.

But these lead to different normalized primitives:

`t/sqrt(t^2)=sign(t)`,

`|t|/sqrt(t^2)=1`

for `t!=0`.

Thus the signed common factor must be extracted **before** absolute-value enclosure. This is the radical analogue of the signed `k45+k54` rule in the correlated P5 matrix lane: early absolute values can destroy the exact cancellation/sign information needed by the mathematical consumer.

---

## 8. Minimal typed mathematical contract

A useful source packet is small:

```text
RadicalFactorPacket
  m q : Nat
  h S J : cell -> Real
  A G : cell -> Real
  hA : A = h^(2m) * S
  hG : G = h^q * J
  hSpos : s0 <= S, 0 < s0
```

Then add exactly one branch witness:

- `q>m` plus `(H,Lh,MJ,LJ,LS)` bounds; or
- `q=m`, `Even m`; or
- `q=m` plus a fixed-sign witness for `h` on the cell.

The checker should reject `q<m` unless a stronger numerator-factor witness is supplied, and it should not silently accept `q=m` with odd `m` on a sign-changing cell.

Factor discovery itself need not be trusted. A CAS/source generator may propose `h,m,q,S,J`; the trusted theorem only verifies the exact identities and the branch inequalities.

---

## 9. Suggested minimal theorem statements

The formalization can stay modular.

1. `sqrt_even_power_factor`
   - assumptions: `0 <= S`;
   - conclusion: `sqrt (h^(2*m) * S) = |h|^m * sqrt S`.

2. `balanced_radical_cancel_even`
   - assumptions: `0<S`, `h!=0`, `q=m`, `Even m`, exact factor identities;
   - conclusion: `G/sqrt(A) = J/sqrt(S)`.

3. `balanced_radical_cancel_of_nonneg_factor`
   - assumptions: `0<S`, `0<h` (or a same-sign cell theorem), `q=m`;
   - conclusion: `G/sqrt(A)=J/sqrt(S)`.

4. `overvanishing_factor_lipschitz`
   - assumptions: `k>=1`, `|h|<=H`, `Lip h<=Lh`;
   - conclusion for the extended `psi`: amplitude `<=H^k` and Lipschitz `<=k H^(k-1)Lh`.

5. `reduced_radical_squared_gain`
   - consume `(s0,MK,LK,LS,theta)` and prove (5.1).

A practical Lean split should avoid formalizing a global `sign`-power API first. Prove the two parity forms of `psi` separately (`|h|^k` and `sign(h)|h|^k`) or specialize initially to the physically likely `m=1` case.

---

## 10. Boundaries that remain open

This review does **not** prove that the deployed evaluator actually has such a factor packet. The following remain open:

- exact source/CSE identities producing `A=h^(2m)S` and `G=h^qJ`;
- whether the source uses an algebraically cancelled expression or evaluates an IEEE `0/0` at a contact point;
- exact factor/root discovery and source-key binding;
- interval proofs of `S>=s0>0`, `|h|<=H`, and the variation constants;
- Float64/libm/outward-rounding semantics;
- centered/full residual and parameter-key compatibility;
- first-exit / trajectory / P8 coverage;
- Lean compile/axiom receipt, independent verification, comparator and admission.

If the deployed implementation literally evaluates `G/sqrt(A)` at `A=0`, this mathematical removable extension does not by itself prove execution equivalence. A source semantic adapter must show that the executed branch agrees with the cancelled/extended formula or excludes the contact point.

---

## 11. Requested integration

Record this as a `pending mathematical/interface child` between the exact zero-contact factor lane and the radical eta-Lipschitz/source-perturbation lane.

The main reusable conclusion is:

> A zero radicand does not require a fake positive lower bound when the source supplies an exact common-factor certificate. The correct gate is the numerator-vs-half-radicand vanishing order. After sound cancellation, all Lipschitz and squared-gain charges belong to the residual positive radicand `S`; under-cancelled and odd balanced sign-changing cases remain explicit obstructions.
