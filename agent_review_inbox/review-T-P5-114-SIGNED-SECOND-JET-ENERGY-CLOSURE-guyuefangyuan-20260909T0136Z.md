---
kind: review_result
review_id: review-T-P5-114-SIGNED-SECOND-JET-ENERGY-CLOSURE-guyuefangyuan-20260909T0136Z
task_id: T-P5-114-SIGNED-SECOND-JET-ENERGY-CLOSURE
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T01:36:00Z
claim_commit: 29a27b6989be93f8c8e12e61e62c7c15e20eb118
inspected_commit: dbf0225f6825463f25c36fc78da4ada49d81850f
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET-guyuefangyuan-20260909T0030Z.md
    commit: 3072f9b62a333f96448defd626a67039adb50168
  - path: agent_review_inbox/review-T-P5-113-anchor-defect-power-absorption-honglianmozun-20260909T0057Z.md
    commit: de258fc7cb4ab6aa6df6ddf09d8ad137537c971d
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
---

# T-P5-114 — signed/correlated second-jet energy closure

## 0. Seam selected

T-P5-112 reduced the finite same-cell affine-anchor problem to one missing source-side inequality.  Along the physical anchor segment,

`M a'' = J2`,

with

`J2 = D2R[delta,delta] - D2M[delta_q,delta_q] a - 2 DM[delta_q] a'`,

and the anchor theorem consumes a uniform bound

`Q_R(J2) <= H2`.

T-P5-113 then consumes that `H2` into a Lyapunov power channel.  The still-open mathematical question is how the source/CSE layer should produce `H2` without erasing the cancellations already visible in the signed formula for `J2`.

This child gives an exact answer.  It is independent of source provenance, admission, runtime, and Lean receipts.

The main recommendation is simple:

> **form the signed second-jet vector, or at least its signed Gram expression, before intervalization.**

No coordinatewise absolute-value split is mathematically required.

---

## 1. Quadratic notation

Let `B_R` be a symmetric positive-semidefinite bilinear form and

`Q_R(x) := B_R(x,x)`.

Along one fixed point of the physical segment define

`r := D2R[delta,delta]`,

`m := D2M[delta_q,delta_q] a`,

`c := 2 DM[delta_q] a'`.

Thus

**(1.1)** `J2 = r - m - c`.

It is useful to also aggregate the two mass-side terms before bounding:

`g := m + c`,

so

**(1.2)** `J2 = r - g`.

All the identities below are pointwise on the same physical segment used by T-P5-112.

---

## 2. Smallest correlated packet: two-block signed Gram gate

From (1.2), exact quadratic expansion gives

**(2.1)**

`Q_R(J2) = Q_R(r) + Q_R(g) - 2 B_R(r,g)`.

Suppose a source/CSE certificate proves, on the whole segment,

**(2.2)** `Q_R(r) <= U_R`,

**(2.3)** `Q_R(g) <= U_G`,

**(2.4)** `L_RG <= 2 B_R(r,g)`.

Then immediately

**(2.5)**

`Q_R(J2) <= U_R + U_G - L_RG`.

Hence define

**(2.6)** `H_corr := U_R + U_G - L_RG`.

A fail-closed checker may require `0 <= H_corr` and then either use

`H2 := H_corr`

or prove a proposed rational `H2` by the single gate

**(2.7)** `H_corr <= H2`.

This is strictly more informative than separately taking norms of `r` and `g`: a positive correlation between the two terms is a *benefit* because the physical second jet subtracts them.

### Direct anchor consumption

T-P5-112 need not materialize an intermediate field named `H2`.  Combining its lower-gain theorem directly with (2.5) gives

**(2.8)**

`4 gamma Q_A(r_anchor) <= H_corr`.

Therefore a proposed anchor budget `D_anchor` passes under the exact-rational gate

**(2.9)** `H_corr <= 4 gamma D_anchor`.

This removes one unnecessary scalar layer from the certificate graph.

### Preconditioner variant

Under the T-P5-112 preconditioner packet,

`4(1-kappa)^2 Q_A(r_anchor) <= chi Q_R(J2)`,

so (2.5) yields

**(2.10)**

`4(1-kappa)^2 Q_A(r_anchor) <= chi H_corr`.

The proposed budget gate is simply

**(2.11)** `chi H_corr <= 4(1-kappa)^2 D_anchor`.

Again there is no inverse or square root.

---

## 3. Full three-term one-sided Gram packet

If the source layer cannot cheaply emit the aggregate `g=m+c`, it can preserve the exact three-term decomposition.  Expanding (1.1),

**(3.1)**

`Q_R(J2)`
` = Q_R(r) + Q_R(m) + Q_R(c)`
`   - 2 B_R(r,m)`
`   - 2 B_R(r,c)`
`   + 2 B_R(m,c)`.

This fixes the direction of every interval endpoint that a checker must consume.

Assume the six one-sided inequalities

`Q_R(r) <= U_r`,

`Q_R(m) <= U_m`,

`Q_R(c) <= U_c`,

`L_rm <= 2 B_R(r,m)`,

`L_rc <= 2 B_R(r,c)`,

`2 B_R(m,c) <= U_mc`.

Then

**(3.2)**

`Q_R(J2) <= K_signed`,

where

**(3.3)**

`K_signed := U_r + U_m + U_c - L_rm - L_rc + U_mc`.

Only the endpoint selected by the coefficient sign is needed:

- the two cross terms entering with `-` need **lower** bounds;
- the cross term entering with `+` needs an **upper** bound.

A full symmetric interval for every Gram entry is unnecessary unless useful elsewhere.

This is an exact linear scalar checker after the source has proved the six inequalities.

### Why the endpoint directions matter

Using an upper bound where a negative coefficient requires a lower bound is unsound.  In one dimension with `Q(x)=x^2`, take `r=1`, `m=-1`, `c=0`.  Then

`Q(r-m)=4`,

while `2 B(r,m)=-2`.

The true expansion is `1+1-(-2)=4`.  If one only knows the valid upper bound `2 B(r,m)<=0` and incorrectly substitutes that upper endpoint into the negative term, one obtains the false value `1+1-0=2`.

So the sign-directed endpoint rule is part of the mathematics, not a serialization detail.

---

## 4. Best source strategy: signed expression before enclosure

The two Gram packets above are modular fallbacks.  If the exact symbolic source can form

`J2 = r-m-c`

as a vector before interval/CSE enclosure, then the strongest object to bound is simply the already-signed scalar polynomial

**(4.1)** `Q_R(J2)`.

This dominates any strategy that first replaces `r,m,c` by independent absolute or norm bounds, because all algebraic cancellation is retained before over-approximation.

Thus the recommended producer hierarchy is:

1. **best:** exact `J2`, then exact `Q_R(J2)`, then one enclosure;
2. **next:** aggregate `g=m+c`, then the two-block packet `(U_R,U_G,L_RG)`;
3. **next:** the six-field one-sided three-term Gram packet;
4. **fallback only:** independent component-energy bounds with a universal PSD inequality.

This hierarchy changes only tightness.  Every level is compatible with the same T-P5-112 theorem.

---

## 5. Root-free fallback when no signed correlation is available

Sometimes the source can prove only

`Q_R(r) <= U_r`, `Q_R(m) <= U_m`, `Q_R(c) <= U_c`

with no cross information.  There is still a clean exact-rational fallback.

For every PSD quadratic form and arbitrary `x,y,z`,

**(5.1)**

`Q(x+y+z) <= 3 (Q(x)+Q(y)+Q(z))`.

A useful proof identity, avoiding square roots entirely, is

**(5.2)**

`3(Qx+Qy+Qz) - Q(x+y+z)`
` = Q(x-y) + Q(x-z) + Q(y-z)`.

The right side is nonnegative by PSD.

Apply this to `x=r`, `y=-m`, `z=-c`.  Since `Q(-v)=Q(v)`,

**(5.3)**

`Q_R(J2) <= 3(U_r+U_m+U_c)`.

Hence T-P5-112 can always consume the conservative gate

**(5.4)** `3(U_r+U_m+U_c) <= 4 gamma D_anchor`.

### The constant 3 is sharp under this information model

Again take one dimension, `Q(x)=x^2`, with

`r=1`, `m=-1`, `c=-1`.

Then each component energy is `1`, but

`J2 = 1-(-1)-(-1)=3`,

so `Q(J2)=9 = 3(1+1+1)`.

Therefore no universal coefficient smaller than `3` in front of the sum of the three independent component energies can be proved without adding correlation or unequal-weight information.

This gives a precise counterexample-guided reason to preserve Gram signs when the fallback fails.

---

## 6. Two-block weighted fallback without roots

If the source can form `g=m+c` and only knows

`Q_R(r)<=U_R`, `Q_R(g)<=U_G`,

there is a tunable rational alternative to the symmetric factor-2 bound.

For positive rationals `p,q`, PSD implies

`0 <= Q_R(q r + p g)`.

Expanding this square and eliminating the cross term in `Q_R(r-g)` gives

**(6.1)**

`p q Q_R(r-g)`
` <= (p+q) (q Q_R(r) + p Q_R(g))`.

Hence

**(6.2)**

`p q Q_R(J2) <= (p+q)(q U_R + p U_G)`.

The anchor checker can consume it directly as

**(6.3)**

`(p+q)(q U_R+p U_G) <= 4 gamma p q D_anchor`.

`p,q` are certificate tuning parameters, not physical constants.  A search layer can choose modest integers/rationals to reduce slack when `U_R` and `U_G` are very unequal; the trusted theorem never computes the square-root-optimal ratio.

For `p=q=1`, (6.2) reduces to the familiar

`Q_R(r-g) <= 2(U_R+U_G)`.

This weighted fallback is still worst-case.  Any proved signed lower bound `L_RG` should instead use the sharper section-2 gate.

---

## 7. Cell-radius homogeneous specialization

The second-jet terms are quadratic in the segment direction `delta`, so their `Q_R` energies and pairings are quartic in `delta`.  A cell producer may therefore prefer a normalized packet relative to

`Z2 := Q_Z(delta)^2 >= 0`.

For example, suppose on the whole segment it proves

`Q_R(r) <= u_r Z2`,

`Q_R(m) <= u_m Z2`,

`Q_R(c) <= u_c Z2`,

`l_rm Z2 <= 2 B_R(r,m)`,

`l_rc Z2 <= 2 B_R(r,c)`,

`2 B_R(m,c) <= u_mc Z2`.

Define

**(7.1)**

`K_corr := u_r + u_m + u_c - l_rm - l_rc + u_mc`.

Then

**(7.2)** `Q_R(J2) <= K_corr Q_Z(delta)^2`.

If the anchor cell also has

`Q_Z(delta) <= S`,

then, with `K_corr>=0`,

**(7.3)** `Q_R(J2) <= K_corr S^2`.

So the complete T-P5-112 anchor gate is

**(7.4)**

`K_corr S^2 <= 4 gamma D_anchor`.

This is exactly the earlier `K2 S^2` gate, but now `K2` is no longer a mysterious scalar: it can be built from a signed Gram enclosure and can retain cancellation.

The preconditioner version is

**(7.5)**

`chi K_corr S^2 <= 4(1-kappa)^2 D_anchor`.

All arithmetic in (7.1)-(7.5) is rational addition, multiplication, squaring, and comparison.

---

## 8. Exact information-boundary examples

### 8.1 Correlation can annihilate a huge apparent defect

In one dimension let `r=g=N`.  Then

`J2=r-g=0`

for every `N`, although

`Q(r)=Q(g)=N^2`.

The signed two-block packet has

`U_R=U_G=N^2`, `L_RG=2N^2`,

so `H_corr=0` exactly.  Any independent-energy fallback instead carries a budget proportional to `N^2`.

Thus a failure of an absolute-value/component-energy budget does **not** imply the true second-jet budget is large; it can be a pure loss-of-correlation artifact.

### 8.2 Independent energies cannot assume cancellation

Conversely, the equal-energy example in section 5 attains the worst same-sign orientation after the physical signs in `J2` are applied.  Therefore a source packet that exports only three diagonal energies contains insufficient information to justify any cancellation beyond the sharp universal fallback.

### 8.3 Pairwise intervals need not form a separately PSD endpoint matrix

The checker should consume one-sided inequalities for the *actual* Gram entries, not assemble arbitrary interval endpoints into a fake Gram matrix and demand that endpoint matrix be PSD.  Entrywise interval endpoints generally do not correspond to one simultaneously attained physical state.  Soundness comes from the proved one-sided inequalities plus the exact expansion (3.1).

A Loewner upper matrix packet is also valid if source naturally provides one, but it is a different, stronger certificate type.

---

## 9. Direct handoff to T-P5-113

T-P5-113's anchor-power channel is

`4 gamma d p_A^2 <= H2 Qd`.

Under section 2 or 3, simply substitute the correlated scalar upper bound:

**(9.1)**

`4 gamma d p_A^2 <= H_corr Qd`

or

`4 gamma d p_A^2 <= K_signed Qd`.

Therefore its two-channel discriminant theorem can use

`A1 = 4 gamma d`,

`B1 = H_corr`

without any new power proof.  In the preconditioner route it uses

`A1 = 4 d (1-kappa)^2`,

`B1 = chi H_corr`.

This child is upstream of T-P5-113's power aggregation; it does not duplicate or alter that theorem.

If a later source theorem discovers signed correlation between the *power* channels `p_ref` and `p_A`, T-P5-113 section 5 remains the appropriate downstream place to consume that distinct correlation.

---

## 10. Minimal source packet recommendation

For each same physical cell / source key, prefer one of the following mutually clear contracts.

### Contract A — direct signed scalar

- exact evaluator/identity for `J2`;
- exact chosen `Q_R`;
- certified whole-segment bound `Q_R(J2)<=H_corr` or `<=K_corr Q_Z(delta)^2`.

### Contract B — two-block Gram

- `r=D2R[delta,delta]`;
- `g=D2M[delta_q,delta_q]a + 2DM[delta_q]a'`;
- `U_R`, `U_G`, and the **lower** cross bound `L_RG<=2B_R(r,g)`;
- same-segment coverage and metric identity.

### Contract C — three-term one-sided Gram

- diagonal uppers `U_r,U_m,U_c`;
- lower cross endpoints `L_rm,L_rc`;
- upper cross endpoint `U_mc`;
- same-segment coverage and metric identity.

Only if none of these correlated packets is available should the producer fall back to independent energies and section 5/6.

Crucially, all quantities must share the same physical `(q,v,w)` segment, graph branch, normalization, and `Q_R`.  Cross terms from separately optimized cells or different metric keys cannot be combined into (2.5) or (3.2).

---

## 11. Suggested Lean decomposition

The proof can be split so that almost all new leaves are pure algebra.

```lean
-- Exact polarization/expansion leaf.
theorem quadratic_second_jet_expand
    (J r m c : V)
    (hJ : J = r - m - c) :
    Q J = Q r + Q m + Q c
          - 2 * B r m - 2 * B r c + 2 * B m c := by
  ...

-- Scalar endpoint-consumption leaf after expansion.
theorem signed_gram_upper_three
    (hq : qJ = qr + qm + qc - crm - crc + cmc)
    (hr : qr <= Ur) (hm : qm <= Um) (hc : qc <= Uc)
    (hrm : Lrm <= crm) (hrc : Lrc <= crc) (hmc : cmc <= Umc) :
    qJ <= Ur + Um + Uc - Lrm - Lrc + Umc := by
  linarith

-- Two-block version; likely the preferred integration API.
theorem signed_gram_upper_two
    (hqr : Q r <= Ur) (hqg : Q g <= Ug)
    (hcross : Lrg <= 2 * B r g) :
    Q (r-g) <= Ur + Ug - Lrg := by
  ...

-- Root-free universal fallback.
theorem quadratic_three_term_le_three_sum
    (hpsd : forall v, 0 <= Q v) :
    Q (x+y+z) <= 3 * (Q x + Q y + Q z) := by
  ...

-- Rational weighted two-block fallback.
theorem quadratic_sub_weighted_mul
    (hp : 0 < p) (hq : 0 < q) :
    p*q*Q (x-y) <= (p+q)*(q*Q x + p*Q y) := by
  ...

-- T-P5-112 composition leaf.
theorem anchor_budget_of_signed_second_jet
    (hlower : gamma * QA v <= QR (M v))
    (hgram : QR J2 <= Hcorr)
    ... :
    4*gamma*QA rAnchor <= Hcorr := by
  exact ...
```

The source-specialized theorem that defines `r,m,c` should wait for actual `D2M/D2R` extraction; the signed Gram and fallback leaves can be formalized immediately with no DH dependencies.

---

## 12. Remaining obligations / non-claims

Mathematical status: **CONDITIONAL_PASS**.

This child does **not** prove any real numerical P5 anchor budget.  Still open are:

- source-certified physical `D2M,D2R` or exact `J2` evaluator;
- same-branch `a,a'` data/enclosures needed by `m,c`;
- same-segment source/graph coverage;
- actual `Q_R` and `Q_A` identity;
- real signed Gram/direct `Q_R(J2)` enclosures;
- lower gain `gamma`, or T-P5-112's `(X,kappa,chi)` packet;
- displacement cap `S` if the normalized cell form is used;
- downstream T-P5-113 same-metric power pairing/dissipation packet;
- Float64/FD/runtime equivalence, P8 flowpipe, Lean/kernel verification, independent validator acceptance, admission, and registry promotion.

The new closure is the theorem-design result that `H2` can be produced by a **signed correlated quadratic packet**, with a precise root-free fallback and sharp information-boundary counterexamples.  Source work should therefore avoid intervalizing `D2R`, `D2M*a`, and `2DM*a'` independently before their signs are assembled.