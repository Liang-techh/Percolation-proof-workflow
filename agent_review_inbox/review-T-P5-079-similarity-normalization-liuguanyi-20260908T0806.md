---
kind: review_result
review_id: review-T-P5-079-similarity-normalization-liuguanyi-20260908T0806
task_id: T-P5-079-SIMILARITY-NORMALIZATION
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T08:06:00-06:00
claim_commit: 9c64f802352405144b36baeec96d2b438cd7aa9c
inspected_commits:
  - 48c78207c758636227a8bb3f5be2e1f6c247e6c4
  - f2769764ff5a9c983114c3de525808be97eb98c7
  - 22ba1c3ffadf2abdb36a563de84c2f89ee6f5b35
  - f0d1df5605088ee79b7416d61af04cf78c2d2f65
inspected_paths:
  - agent_review_inbox/review-T-P5-074-weighted-strong-monotone-scc-guyuefangyuan-20260908T0700.md
  - agent_review_inbox/review-T-P5-076-weighted-gram-lipschitz-liuguanyi-20260908T0716.md
  - agent_review_inbox/review-T-P5-077-anchor-localized-invariant-ball-guyuefangyuan-20260908T0731.md
  - agent_review_inbox/review-T-P5-078-mixed-relative-additive-corrector-kuangmanmozun-20260908T0752.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Insert this as the coordinate-normalization bridge around the weighted P5 SCC
  packet. If source coordinates are affinely normalized, transport the residual
  covariantly and the quadratic weight by congruence before consuming
  T-P5-074/076/077/078. Preserve the theorem-level quadratic-form certificate;
  do not rerun an equal-charge Gershgorin row test after anisotropic scaling.
  If residual output coordinates are normalized independently from state
  coordinates, expose the resulting preconditioner explicitly.
---

# T-P5-079 — affine similarity normalization of the weighted SCC certificate

## 0. Result in one line

The weighted strong-monotonicity, weighted squared-Lipschitz, root-localization,
and damped-corrector packets developed in T-P5-074/076/077/078 are exactly
coordinate invariant under an invertible affine state normalization, but only
if the residual is transformed covariantly and the metric is transported by
congruence.

Let

`x = c + S z`

with invertible real matrix `S`, and suppose the physical residual/vector field
`F_x` and normalized residual `F_z` satisfy the exact same-point identity

**(0.1)** `F_x(c + S z) = S F_z(z)`.

Let `W_x` be a fixed symmetric positive-definite weight and define

**(0.2)** `W_z = S^T W_x S`.

Then for every pair `z,y`, writing `x=c+Sz`, `x'=c+Sy`,

**(0.3)** `Q_{W_z}(z-y) = Q_{W_x}(x-x')`,

**(0.4)**
`<F_z(z)-F_z(y), z-y>_{W_z}`
` = <F_x(x)-F_x(x'), x-x'>_{W_x}`,

and

**(0.5)**
`Q_{W_z}(F_z(z)-F_z(y))`
` = Q_{W_x}(F_x(x)-F_x(x'))`.

Consequently the *same numerical constants* `mu` and `Lambda` transport in
both directions:

`<Delta F_x, Delta x>_{W_x} >= mu Q_{W_x}(Delta x)`

iff

`<Delta F_z, Delta z>_{W_z} >= mu Q_{W_z}(Delta z)`,

and

`Q_{W_x}(Delta F_x) <= Lambda Q_{W_x}(Delta x)`

iff

`Q_{W_z}(Delta F_z) <= Lambda Q_{W_z}(Delta z)`.

No spectral recomputation is mathematically needed after normalization.

Likewise the exact damped corrector

`x_plus = x - h F_x(x)`

is conjugate to

`z_plus = z - h F_z(z)`

with the *same* scalar step `h`. Therefore the quadratic factors and barrier
constants used in T-P5-075/077/078 are invariant when all packets are
transported through the same `(S,W_z)` chart.

Two interfaces are unsafe:

1. keeping the old weight after anisotropic state scaling; and
2. scaling residual/output coordinates independently from state coordinates
   and then feeding that independently scaled residual directly to the
   corrector theorem.

Both errors already fail in exact rational 1D/2D examples below.

This is a mathematics/interface child only. It does not bind any deployed SCC,
source normalization, Float64/FD/controller/solve implementation, physical
coverage, P8/ODE trajectory, Lean/kernel receipt, provenance, admission,
registry mutation, or parent closure.

---

## 1. Fixed-metric affine chart and exact quadratic identities

For a symmetric positive-definite matrix `W`, write

`Q_W(v) = v^T W v`,

`<u,v>_W = u^T W v`.

Let `S` be invertible and set

`T(z)=c+Sz`.

The affine offset `c` disappears from differences:

`T(z)-T(y)=S(z-y)`.

Define the transported weight

`W_z=S^T W_x S`.

Then for any vector `v`,

**(1.1)**
`Q_{W_z}(v)`
` = v^T S^T W_x S v`
` = Q_{W_x}(Sv)`.

This is the basic congruence identity. Positive definiteness is also preserved:
for `v != 0`, invertibility gives `Sv != 0`, hence

`Q_{W_z}(v)=Q_{W_x}(Sv)>0`.

Now assume the residual covariance (0.1). For `Delta z=z-y`,

`Delta F_x = F_x(Tz)-F_x(Ty)`
` = S(F_z(z)-F_z(y))`
` = S Delta F_z`.

Therefore

**(1.2)**
`<Delta F_z,Delta z>_{W_z}`
` = Delta F_z^T S^T W_x S Delta z`
` = <S Delta F_z,S Delta z>_{W_x}`
` = <Delta F_x,Delta x>_{W_x}`,

and

**(1.3)**
`Q_{W_z}(Delta F_z)=Q_{W_x}(Delta F_x)`.

No inverse appears in these checker-facing identities. Although analytically
one may write `F_z=S^{-1} F_x∘T`, a source adapter can instead certify the
multiplication-only identity `F_x∘T=S F_z`.

### Theorem 1.1 — strong-monotonicity similarity equivalence

Suppose `B_z` is a domain and `B_x=T(B_z)`. Under (0.1)-(0.2), for any real
`mu`,

`<F_x(x)-F_x(y),x-y>_{W_x} >= mu Q_{W_x}(x-y)`

for every `x,y in B_x` iff

`<F_z(z)-F_z(w),z-w>_{W_z} >= mu Q_{W_z}(z-w)`

for every `z,w in B_z`.

The same `mu` is used on both sides.

### Theorem 1.2 — squared-Lipschitz similarity equivalence

Under the same assumptions, for any real `Lambda`,

`Q_{W_x}(F_x(x)-F_x(y)) <= Lambda Q_{W_x}(x-y)`

on `B_x` iff

`Q_{W_z}(F_z(z)-F_z(w)) <= Lambda Q_{W_z}(z-w)`

on `B_z`.

Again, the same `Lambda` is used on both sides.

These two equivalences are the exact source-to-math normalization bridge for
T-P5-074 and T-P5-076.

---

## 2. Exact corrector conjugacy and preservation of the Lyapunov packet

Suppose the physical exact step is

**(2.1)** `x_plus = x - h F_x(x)`.

Write `x=c+Sz` and use (0.1):

`x_plus`
` = c+Sz-h S F_z(z)`
` = c+S(z-hF_z(z))`.

Hence

### Theorem 2.1 — damped corrector similarity identity

**(2.2)** `z_plus = z - h F_z(z)`

is exactly conjugate to (2.1), with no rescaling of `h`.

If `x_star=c+S z_star` is a root, then by invertibility of `S`,

`F_x(x_star)=0` iff `F_z(z_star)=0`.

Moreover

**(2.3)**
`Q_{W_x}(x-x_star)=Q_{W_z}(z-z_star)`.

Thus a root-centered Lyapunov level `Vstar` is numerically the same scalar in
both coordinates.

If the anchor is `x0=c+S z0`, then

**(2.4)**
`Q_{W_x}(F_x(x0)) = Q_{W_z}(F_z(z0))`.

Therefore the T-P5-077 anchor-residual scalar `B0` is also invariant. In
particular, its localization gate

`mu^2 Q(c_anchor-x_star) <= B0`

transports without changing either `mu` or `B0`.

The T-P5-075 exact-corrector factor

`q_h = 1 - 2 h mu + h^2 Lambda`

is therefore unchanged, and so are the T-P5-078 relative/additive gates when
the defect vectors themselves obey the same covariance as the residual. A
normalized defect packet in a different codomain metric is **not** automatically
the same uncertainty class; Section 7 gives the required repair.

---

## 3. Jacobian congruence: one source derivative packet survives normalization

Assume differentiability and differentiate

`F_x(c+Sz)=S F_z(z)`.

Writing

`J_x = D F_x(c+Sz)`, `J_z=D F_z(z)`,

we obtain the exact intertwining identity

**(3.1)** `J_x S = S J_z`.

Define the T-P5-074 symmetric object

`A_x = W_x J_x + J_x^T W_x`

and the T-P5-076 Gram object

`H_x = J_x^T W_x J_x`.

In normalized coordinates define

`A_z = W_z J_z + J_z^T W_z`,

`H_z = J_z^T W_z J_z`.

Using `W_z=S^T W_x S` and (3.1),

**(3.2)**
`A_z = S^T A_x S`,

and

**(3.3)**
`H_z = S^T H_x S`.

Thus both of the quadratic matrices needed by T-P5-074/076 transform by the
*same congruence*.

### Corollary 3.1 — Loewner gates preserve the constants

For any `mu,Lambda`,

**(3.4)** `A_x >= 2 mu W_x` iff `A_z >= 2 mu W_z`,

and

**(3.5)** `H_x <= Lambda W_x` iff `H_z <= Lambda W_z`.

Proof: subtract the right-hand side and use

`A_z-2mu W_z = S^T(A_x-2mu W_x)S`,

`Lambda W_z-H_z = S^T(Lambda W_x-H_x)S`.

An invertible congruence preserves positive semidefiniteness in both
directions.

The interface point is important: if an exact source Jacobian certificate was
already proved in one chart, a second spectral/operator-norm computation in a
normalized chart is mathematically redundant. The adapter only needs the exact
intertwining and congruence identities.

---

## 4. Positive diagonal/rational specialization

The most useful source form is a positive diagonal scale

`S=diag(s_1,...,s_n)`, `s_i>0`,

and a diagonal weight

`W_x=diag(w_1,...,w_n)`, `w_i>0`.

Then

**(4.1)** `w_i^z = w_i s_i^2`.

The Jacobian intertwining (3.1) is entrywise

**(4.2)** `J_x[i,j] s_j = s_i J_z[i,j]`.

No division is required to check this identity.

For the symmetric packet,

**(4.3)**
`A_z[i,j] = s_i s_j A_x[i,j]`.

For the Gram packet,

**(4.4)**
`H_z[j,k] = s_j s_k H_x[j,k]`.

Because all `s_i` are positive, every signed cancellation already present in
`A_x[i,j]` or `H_x[j,k]` is preserved. Hence the preferred source order is

`signed physical polynomial`
` -> exact multiplication by s_i s_j`
` -> enclosure`,

not

`absolute values of primitive Jacobian entries`
` -> scale`
` -> rebuild cross terms`.

This is the same correlation-preserving principle used by T-P5-074 and
T-P5-076, now made coordinate invariant.

---

## 5. The theorem is invariant; a naive equal-charge row certificate is not

T-P5-076 uses a convenient sufficient row/Gershgorin-style certificate. One
must distinguish the **quadratic-form theorem** from this particular
coordinate-wise sufficient proof.

Suppose in the physical chart

`H_x[j,j] <= a_j`,

`|H_x[j,k]| <= c_jk`,

and

**(5.1)** `a_j + sum_{k!=j} c_jk <= Lambda w_j`.

Then for every physical coordinate vector `u`, T-P5-076 gives

`u^T H_x u <= Lambda sum_j w_j u_j^2`.

After diagonal scaling, set `u=S v`. Immediately

**(5.2)**
`v^T H_z v`
` = (Sv)^T H_x(Sv)`
` <= Lambda sum_j w_j s_j^2 v_j^2`
` = Lambda v^T W_z v`.

So the certificate transports exactly at the quadratic-form level.

Equivalently, in the pairwise proof one uses the scaled Young identity

**(5.3)**
`2 s_j s_k |v_j v_k| <= s_j^2 v_j^2 + s_k^2 v_k^2`.

This preserves the original charges `c_jk`.

### Obstruction 5.1 — rerunning the naive row test after scaling can falsely reject

Take

`W_x=I`,

`H_x=[[2,9/10],[9/10,2]]`,

`Lambda=29/10`.

The original equal-charge row gate is sharp:

`2+9/10 = 29/10`.

Now choose

`S=diag(10,1)`.

Then

`W_z=diag(100,1)`,

`H_z=S^T H_x S=[[200,9],[9,2]]`.

By congruence, the exact theorem

`H_z <= (29/10) W_z`

is valid.

However, if one forgets that the old row proof must be transported and simply
reruns the equal-charge test on the transformed entries, row 2 asks for

`2+9 <= 29/10`,

which is false.

Thus **the coordinate-wise row certificate itself is not a tensorial object**.
The safe adapter is to transport the already certified quadratic form, or to
use (5.3) with the original unscaled pair charges. Re-enclosing transformed
entries and assigning each cross term equally can create an artificial
obstruction after anisotropic normalization.

The same statement holds for a lower symmetric/strong-monotonicity row proof:
transport the base pair charges through `u=S v`; do not assume the same naive
post-scaling diagonal-dominance format remains sharp.

---

## 6. Obstruction: keeping the old weight changes the mathematical problem

A common normalization bug is to scale coordinates but continue using the old
Euclidean/diagonal weight as if the metric were unchanged.

Consider the exact rational Jacobian

**(6.1)**
`J_x=[[1,1],[-1,1]]`, `W_x=I`.

Then

`J_x+J_x^T=2I`,

`J_x^T J_x=2I`.

So the physical packet has exactly

`mu=1`, `Lambda=2`.

Choose

`S=diag(3,1)`.

From `J_x S=S J_z`,

**(6.2)**
`J_z=[[1,1/3],[-3,1]]`.

With the correct transported metric

`W_z=diag(9,1)`,

one obtains exactly

**(6.3)**
`W_z J_z+J_z^T W_z = 2 W_z`,

**(6.4)**
`J_z^T W_z J_z = 2 W_z`.

Thus `mu=1`, `Lambda=2` are preserved as the theorem predicts.

If instead one incorrectly freezes the normalized metric at `I`, then

`J_z+J_z^T=[[2,-8/3],[-8/3,2]]`.

For the exact rational vector `v=(1,1)`,

**(6.5)**
`v^T(J_z+J_z^T)v = -4/3 < 0`.

So even nonnegative monotonicity fails in the wrong metric.

This is not a harmless conservative weakening: it is a different mathematical
statement. Depending on the direction of the coordinate change, a frozen
metric can either discard a valid certificate or make an unrelated normalized
certificate look stronger than the intended physical one. The adapter must
bind the metric transformation explicitly.

---

## 7. Independent residual/output scaling produces a preconditioned corrector

The covariance (0.1) is essential. Source code often normalizes state and
residual/output channels with different diagonal scales. Let

`x=c+S z`

but define an exported residual `G` through

**(7.1)** `F_x(c+Sz)=D G(z)`

for another invertible scale `D`.

Then the physical update

`x_plus=x-hF_x(x)`

becomes

**(7.2)**
`z_plus = z - h R G(z)`,

where

`R=S^{-1}D`.

Hence the map to which T-P5-074/076/075 should be applied is

**(7.3)** `Phi(z)=R G(z)`,

not `G(z)`, unless `D=S` (or another separately proved identity makes
`R G=G`).

A trusted checker need not calculate an inverse: the source adapter may expose
an exact matrix `R` satisfying

**(7.4)** `S R=D`,

and then certify `Phi=R G`. For positive diagonal rational scales, this can be
written denominator-free as

**(7.5)** `s_i Phi_i = d_i G_i`.

### Exact 1D obstruction

Take

`F_x(x)=x`, `S=2`, `D=1`, `c=0`.

Then `x=2z` and the independently scaled exported residual is

`G(z)=F_x(2z)=2z`.

But the true normalized residual is

`F_z(z)=S^{-1}F_x(2z)=z`.

Therefore the physical step is

`z_plus=(1-h)z`,

while a consumer that incorrectly feeds `G` directly into the corrector theorem
models

`z_plus=(1-2h)z`.

At `h=3/2`, the true normalized step has factor `-1/2` and is a strict
contraction, while the incorrectly modeled step has factor `-2` and expands.
The discrepancy is purely a missing coordinate interface; no interval or
floating-point issue is involved.

Thus independent codomain normalization must be represented as an explicit
preconditioner in the mathematical contract.

---

## 8. Domain and box transport

The secant theorems require the *same physical domain* after changing charts.
The exact domain relation is

**(8.1)** `B_x = c + S B_z`.

Affine maps preserve convexity. Therefore the convex-segment assumption used by
T-P5-076 transports automatically if (8.1) is exact.

For diagonal positive `S`, a centered normalized box

`|z_i-z0_i| <= H_i^z`

maps to the physical axis-aligned box

**(8.2)** `|x_i-x0_i| <= s_i H_i^z`.

The T-P5-077 root-centered Lyapunov ball itself does not need coordinate-wise
re-derivation, because

`Q_{W_z}(z-z_star)=Q_{W_x}(x-x_star)`.

But its *box containment gate* must use halfwidths belonging to the chosen
chart. A source packet may either transport the physical halfwidths by (8.2) or
transport the already proved containment theorem as a set inclusion. Mixing
physical halfwidths with normalized weights is not type-correct.

---

## 9. Minimal typed mathematical contract

A source-to-math normalization packet can be very small.

### Core affine packet

1. exact chart: `x = c + S z`;
2. invertibility (or positive diagonal nonzero entries) of `S`;
3. physical weight `W_x`;
4. transported weight identity `W_z = S^T W_x S`;
5. residual covariance `F_x(c+Sz)=S F_z(z)` on the same mapped cell.

### Optional differential packet

6. `J_x(c+Sz) S = S J_z(z)`.

This is enough to transport both the symmetric and Gram source certificates by
(3.2)-(3.3).

### Independent output-normalization packet

If the source exports `G` with `F_x=D G`, also require

7. an explicit preconditioner `R` with `S R=D`;
8. the consumer field `Phi=R G`.

Do not pass `G` directly to the SCC theorem unless `R=I` has been proved.

For a positive diagonal rational chart, the checker-facing equalities are only
products:

`w_i^z = w_i s_i^2`,

`J_x[i,j] s_j = s_i J_z[i,j]`,

`A_z[i,j]=s_i s_j A_x[i,j]`,

`H_z[j,k]=s_j s_k H_x[j,k]`,

and, when needed, `s_i Phi_i=d_i G_i`.

No square root, eigenvalue, or inverse is required by the trusted arithmetic
layer.

---

## 10. Suggested Lean decomposition

The first formalization pass can stay almost entirely finite-dimensional and
algebraic.

Suggested leaves:

1. `quadraticForm_congruence`
   - `Q_{SᵀWS}(v)=Q_W(Sv)`.

2. `weighted_pairing_similarity`
   - from `DeltaFx=S*DeltaFz`, `DeltaX=S*DeltaZ`, prove pairing equality.

3. `strongMonotone_similarity_iff`
   - same `mu` under an affine bijection.

4. `sqLipschitz_similarity_iff`
   - same `Lambda` under the same chart.

5. `corrector_step_similarity`
   - `T(z-hFz)=T(z)-hFx(Tz)` under covariance.

6. `jacobian_sym_congruence`
   - from `Jx*S=S*Jz`, prove `Az=SᵀAxS`.

7. `jacobian_gram_congruence`
   - from the same intertwining, prove `Hz=SᵀHxS`.

8. `scaled_young_pair`
   - `2*s*t*|a*b| <= s^2*a^2+t^2*b^2` for nonnegative `s,t`.

9. `gram_row_certificate_under_diagonal_similarity`
   - transport the T-P5-076 base row certificate without rerunning a naive
     transformed Gershgorin test.

10. `independent_codomain_scaling_requires_preconditioner`
    - from `Fx=D*G`, `S*R=D`, derive the normalized step with `R*G`.

The first seven are sufficient for the main theorem. The row-certificate and
independent-output leaves are interface hardening and can remain separate.

---

## 11. Boundaries deliberately left open

This review does **not** prove any of the following:

- that a deployed P5 SCC actually uses an affine normalization `x=c+Sz`;
- that its residual implementation satisfies `F_x∘T=S F_z` exactly;
- that its Jacobian source satisfies `J_x S=S J_z` on the whole cell;
- that physical and normalized source boxes are the exact images of one another;
- any Float64/outward-rounding, FD, controller, linear-solve, or evaluator
  defect bound;
- root existence for a deployed SCC;
- P8/ODE/first-exit trajectory coverage;
- Lean/kernel compilation or independent validation;
- comparator/admission/registry mutation.

The theorem also does **not** cover a nonlinear chart `x=T(z)` with
state-dependent Jacobian, nor a moving/time-dependent scale `S(t)`. In those
cases extra derivative/connection terms appear in Jacobians or dynamics and
must be exposed explicitly; silently applying this fixed affine similarity
result would be unsound.

Likewise a state-dependent Lyapunov metric `W(x)` is outside this result. Here
`W_x` and `W_z` are fixed quadratic weights related by one constant
congruence.

---

## 12. Proposed downstream use

The safe chain is:

`physical/source chart`
` -> exact affine normalization packet (S,c)`
` -> residual covariance / optional Jacobian intertwining`
` -> W_z=S^T W_x S`
` -> transport strong-monotonicity + Gram quadratic certificates`
` -> reuse same mu, Lambda, B0, Vstar and h`
` -> T-P5-075/077/078 corrector and invariant-ball consumers`.

If the source uses separate state and output scales, insert

`G -> Phi=R G`, `S R=D`

before the weighted SCC packet.

The principal mathematical rule is therefore:

**normalize the state, residual, and metric as one covariant object; do not
normalize each interface independently and hope the old Lyapunov constants
still mean the same thing.**
