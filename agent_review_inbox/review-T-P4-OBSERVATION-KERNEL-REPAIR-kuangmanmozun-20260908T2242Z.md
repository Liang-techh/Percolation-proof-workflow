---
kind: review_result
review_id: review-T-P4-OBSERVATION-KERNEL-REPAIR-kuangmanmozun-20260908T2242Z
task_id: T-P4-OBSERVATION-KERNEL-REPAIR
source_agent: 狂蛮魔尊
created_at: 2026-09-08T22:42:00Z
claim_commit: a2aede004586b188cd368373f177842dc0261178
inspected_commit: 11ce5556cc5adf8e980ac0be97f7cd63918458d5
status: CONDITIONAL_PASS_WITH_SHARP_REPAIR_GATE
integration_status: pending
admission_label: pending
proof_status: SOURCE_INDEPENDENT_MATHEMATICS_ONLY
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
registry_mutation: false
state_mutation: false
---

# T-P4-OBSERVATION-KERNEL-REPAIR — exact repair of a rank-deficient defect observation

## 1. Question and result

The immediately preceding actual-source review proved the negative statement needed to
fail closed: two independent scalar observations of a three-dimensional defect cannot
by themselves bound an SPD energy `D=d^T H d`, because the observation map has a
nontrivial kernel.

This child answers the next mathematical question:

> What is the **minimal additional information** that repairs that obstruction, and
> what exact gate should a future block-(4,5,6) source packet satisfy?

The answer is sharp.

Let

```text
H = H^T > 0,                 d in R^n,
L : R^n -> R^m,              N : R^n -> R^k,
T d := (L d, N d).
```

Then a finite uniform `H`-energy cap from squared observation caps exists **if and only
if** the combined observation has no invisible direction:

```text
ker L ∩ ker N = {0}.                         (KERNEL-GATE)
```

Equivalently, the stacked matrix `T` has full column rank.  In finite dimension this
is equivalent to positive definiteness of

```text
G := L^T L + N^T N = T^T T.
```

For trusted arithmetic one does not need an eigenvalue or square root.  It suffices to
supply a rational `C >= 0` and the PSD witness

```text
C * (L^T L + N^T N) - H  >=  0.              (PSD-CAP)
```

Then every `d` satisfying

```text
||L d||^2 <= U,
||N d||^2 <= V
```

obeys the division-free bound

```text
d^T H d <= C * (U + V).                      (ENERGY-CAP)
```

Conversely, if `(KERNEL-GATE)` fails, no finite bound depending only on `U,V` can hold,
even at `U=V=0`.

Thus the correct repair to the present block456 obstruction is not specifically
"recover all six upstream variables".  For the **quadratic defect cap alone**, it is
enough to add any source-certified observation that kills the old nullspace, together
with a quantitative PSD comparison.  Full `y=X z_A` remains necessary only if another
consumer needs that stronger source identity.

No actual source packet is claimed here.

## 2. Exact iff theorem

### Theorem A — finite-energy observability iff the common kernel is trivial

Let `H` be SPD on `R^n`, and let `L,N` be linear maps.  Define

```text
Q(d) := ||L d||^2 + ||N d||^2.
D(d) := d^T H d.
```

The following are equivalent.

1. `ker L ∩ ker N = {0}`.
2. `Q(d)>0` for every `d != 0`.
3. There exists a finite `C>0` such that `D(d) <= C Q(d)` for every `d`.
4. There exists a finite `C>0` such that
   `C(L^T L+N^T N)-H` is PSD.

**Proof.**

`1 -> 2`: if `Q(d)=0`, both nonnegative squares vanish, hence `Ld=Nd=0`; the
common-kernel assumption gives `d=0`.

`2 -> 3`: on the Euclidean unit sphere the continuous function `Q` has a positive
minimum `mu>0`, while `D` has a finite maximum `M`; hence
`D(d)<=M ||d||^2 <= (M/mu)Q(d)`.  This is only an existence proof; the consumer does
not need to compute `M/mu`.

`3 <-> 4`: expand the quadratic form

```text
d^T [ C(L^T L+N^T N)-H ] d = C Q(d)-D(d).
```

`3 -> 1`: if nonzero `v` lies in the common kernel, then `Q(tv)=0` for every `t`
while `D(tv)=t^2 D(v)>0`, contradiction.

This is the exact structural boundary.  It strengthens the previous rank-deficiency
obstruction from a negative result into a necessary-and-sufficient repair criterion.

## 3. Rank-two / one-scalar specialization in dimension three

Now let `n=3` and suppose the existing observation `L` has rank exactly `2`.  Its
kernel is one-dimensional; choose any nonzero generator `v` with `L v=0`.  Let the
new observation be one scalar

```text
N d = c^T d.
```

Then

```text
ker L ∩ ker N = {0}
    iff
c^T v != 0.                                  (ONE-SCALAR-GATE)
```

So **one scalar is mathematically sufficient**, but only if it actually sees the old
invisible direction.

This is also necessary.  If `c^T v=0`, the same ray `d=t v` remains invisible and
`D(tv)` is unbounded.

For the current block456 source problem this gives a precise design rule:

- a third row/projection that is a linear combination of the two existing observations
  has zero value;
- any third same-source linear observable transverse to the old kernel can repair the
  information deficit;
- after that qualitative rank test, a quantitative PSD-cap witness is still required.

A mere `det != 0` or nonzero third component is therefore not enough for a useful
numerical budget: conditioning matters.

## 4. Quantitative sharpness: an almost-invisible third row can be arbitrarily expensive

Take the exact rational model

```text
H = I_3,
L d = (d1,d2),
c = (1,0,epsilon),      epsilon != 0.
```

The third scalar is

```text
t = d1 + epsilon*d3.
```

The combined map is injective for every `epsilon != 0`, so the qualitative kernel gate
passes.  But on the old invisible ray `d=(0,0,z)`,

```text
L d = 0,
t = epsilon*z,
D = z^2 = t^2 / epsilon^2.
```

Hence any universal coefficient multiplying the third-observation square must be at
least `1/epsilon^2`.  With the rational choice `epsilon=1/100`, the required factor is
at least `10000`.

This rules out a dangerous shortcut:

> `rank(stacked observation)=3` is enough to prove finiteness, but it is **not** a
> quantitative reserve certificate.

The future source packet must expose either a rational inverse/left-inverse bound or a
PSD comparison such as `(PSD-CAP)`; otherwise a nearly dependent third row can consume
arbitrarily large Schur margin.

## 5. Exact reconstruction from three independent scalar observations

There is an even sharper route when exactly three independent scalar observations are
available.

Let `T` be an invertible `3 x 3` observation matrix and

```text
y = T d.
```

Instead of invoking a matrix inverse primitive, let the certificate provide a rational
matrix `U` and exact identities

```text
U T = I,
T U = I.
```

Then `d=U y`, so the full defect energy is **exactly**

```text
D = d^T H d
  = y^T K y,
K := U^T H U.                                 (EXACT-RECONSTRUCTION)
```

There is no Cauchy/Young loss and no condition-number factor beyond what is already
encoded in the exact matrix `K`.

Therefore a future block456 producer does not necessarily need to emit `D` as a fourth
independent quantity.  It may instead emit three same-key linearly independent scalar
observations, plus an exact rational left/right inverse for their stacked map.  The
consumer can reconstruct the intended `H`-energy exactly by
`(EXACT-RECONSTRUCTION)`.

This is a strict refinement of the preceding source-obstruction handoff: "third
independent defect direction" can be turned into a complete typed energy producer.

## 6. Exact box cap: eight vertices, no spectral norm

Suppose the three observation intervals are certified as

```text
|y1| <= b1,
|y2| <= b2,
|y3| <= b3,
```

and `K=U^T H U` is PSD.  The convex quadratic `y^T K y` attains its maximum over the
box at a vertex.  Thus the exact box cap is

```text
D <= max_{sigma_i in {-1,+1}}
       (sigma .* b)^T K (sigma .* b).         (VERTEX-CAP)
```

Only eight exact-rational evaluations are needed in dimension three.  This preserves
signed cross terms and is generally tighter than replacing `K` by an operator norm or
bounding each cross term independently.

A Lean/checker implementation can avoid `max` over an abstract finite set by accepting
one rational `Dcap` and checking the eight inequalities

```text
vertexEnergy(sigma) <= Dcap.
```

Because the quadratic is convex in each coordinate separately (`K_ii>=0`), repeatedly
pushing each coordinate to an endpoint proves the vertex claim.

For nonsymmetric intervals `[li,ui]`, the same argument uses the eight ordinary box
vertices.

## 7. Specialization to the current symbolic block456 metric

The immediately preceding source review records the symbolic candidate

```text
H =
[[ 50003000000/5000400003, 0,                   -50000000000/5000400003],
 [ 0,                        4000000/200739,       0],
 [-50000000000/5000400003,   0,                   350003000000/5000400003]].
```

If a future same-source packet genuinely supplies the three **actual defect
coordinates** `(d4,d5,d6)` with symmetric bounds

```text
|d4|<=b4, |d5|<=b5, |d6|<=b6,
```

then `T=I_3`, and the exact vertex maximum reduces to

```text
Dcap =
  (50003000000/5000400003) * b4^2
+ (4000000/200739)          * b5^2
+ (350003000000/5000400003)* b6^2
+ (100000000000/5000400003)* b4*b6.            (BLOCK456-BOX-CAP)
```

The final cross term is positive because the maximizing vertex takes `d4` and `d6`
with opposite signs, matching the negative `H46` entry.

This formula is **conditional only**.  The current two-row payload is not yet an actual
`(d4,d5)` producer, and the current source review reports controller-coefficient
omissions.  `(BLOCK456-BOX-CAP)` must not be attached to those old rows by name alone.

Nevertheless, it identifies a materially smaller mathematical source target: after
repairing the two existing rows, one correctly typed same-key `d6` interval is enough
to produce the full 3D energy cap for this metric.  A six-dimensional upstream box is
not mathematically necessary for this particular consumer.

## 8. Counterexamples that should be kept as regressions

### C1 — redundant third row does not repair the kernel

```text
H=I,
L(d)=(d1,d2),
c=(1,1,0),
d=t e3.
```

All three scalar observations vanish for every `t`, but `D=t^2` is unbounded.

Expected status: `REJECT_REDUNDANT_THIRD_OBSERVATION`.

### C2 — full rank with arbitrarily bad quantitative reserve

```text
H=I,
L(d)=(d1,d2),
c=(1,0,1/100).
```

The combined map is invertible, yet the old-kernel ray forces an energy coefficient at
least `10000` relative to the third scalar square.

Expected status: `RANK_PASS_QUANTITATIVE_CAP_STILL_REQUIRED`.

### C3 — canonical good repair

```text
H=I,
L(d)=(d1,d2),
c=e3.
```

Then `D=d1^2+d2^2+d3^2` exactly.  The repair has unit reserve.

Expected status: `PASS_EXACT_RECONSTRUCTION`.

These three examples separate **dimension**, **conditioning**, and **energy
reconstruction**; a future checker should not collapse them into one boolean rank test.

## 9. Minimal formalization leaves

Recommended source-independent Lean leaves:

```text
common_kernel_trivial_iff_stacked_sq_positive
energy_le_of_psd_stacked_observation_cap
no_energy_cap_of_common_kernel_nontrivial
rank_two_scalar_repair_of_kernel_pairing_ne_zero
stacked_observation_energy_exact_of_two_sided_inverse
quadratic_box_le_of_all_vertex_le
```

The first production-facing theorem should use cleared matrix/quadratic hypotheses:

```text
0 <= C,
PSD (C * (L^T L + N^T N) - H),
||L d||^2 <= U,
||N d||^2 <= V
------------------------------------------------
d^T H d <= C*(U+V).
```

No square roots, singular values, divisions, or floating eigenvalue calculations are
needed in the trusted consumer.

For the 3-observation exact route, avoid a generic inverse API if inconvenient: accept
`U` plus `UT=I` and `TU=I`, define `K=U^T H U`, and prove the quadratic identity by
`ring`/matrix algebra.

## 10. Boundary and next step

This child is a mathematical `CONDITIONAL_PASS` only.

It does **not** prove that the repository currently has the required third source row,
that the existing rows 4/5 equal the intended defect coordinates, that `H` is bound to
the deployed runtime, or that any path/FD/Float64 domain is covered.

The useful next source-side question is now exact and small:

1. repair/reify the two existing actual defect observations under one source key;
2. produce one third same-key scalar linear observation;
3. prove that its stacked map with the first two has trivial kernel **quantitatively**,
   preferably by a rational two-sided inverse or `(PSD-CAP)` witness;
4. then compute `D` by exact reconstruction/8-vertex evaluation instead of requesting a
   separate coarse norm cap.

If no third observation sees the old nullspace, the prior impossibility theorem remains
final for that packet.
