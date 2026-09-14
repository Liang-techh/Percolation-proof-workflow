---
kind: review_result
review_id: RVW-P4-SCHUR-ACTUAL-SOURCE-NEXT-GYFY-20260909T1123Z
task_id: GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT
source_agent: 古月方源
created_at: 2026-09-09T11:40:00Z
claim_commit: 315dc07e683cb11526d853fa012c0b0abcb90b80
inspected_commit: 315dc07e683cb11526d853fa012c0b0abcb90b80
inspected_paths:
  - agent_review_inbox/review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT-guyuefangyuan-20260908T2230Z.md
  - agent_review_inbox/review-GH-MATH-P4-BLOCK456-SOURCE-REIFICATION-codex-20260908T091914.md
  - agent_review_inbox/review-GH-MATH-P4-BLOCK456-MATCHING-METRIC-BUDGET-codex-20260908.md
status: CONDITIONAL_PASS_MATHEMATICAL_REFINEMENT
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
registry_mutation: false
state_mutation: false
proposed_integration_target: P4.block456.actual_source_schur.third_direction_residual
requested_action: source/CSE lane should generate the same-key affine scalar w6=350003*d6-50000*d4 before intervalization, together with d4,d5 caps and the exact H/source identity; do not reconstruct D from u/s and do not substitute the unrelated matching-metric CSV packet
---

# GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT — sharp third-direction source contract

## 1. Result

The previous round established a genuine information-theoretic obstruction: rows 4 and 5, or any two scalar Schur observations, cannot by themselves cap the three-dimensional positive-definite block456 energy

```text
D = d^T H d,
C=(4,5,6).
```

This round does **not** retract that obstruction.  It sharpens it using the exact rational block456 metric candidate already frozen by the source-reification lane.

For this particular `H=M0_CC^{-1}`, one does not need an arbitrary third raw coordinate box.  There is a unique H-orthogonalized third scalar (after normalizing the coefficient of `d6`) that removes every remaining cross term:

```text
r6 := d6 - (50000/350003) d4.
```

Equivalently, without division inside the source producer,

```text
w6 := 350003*d6 - 50000*d4 = 350003*r6.
```

The exact block456 quadratic form diagonalizes in `(d4,d5,w6)`.  Therefore a same-key source packet consisting only of exact identities/caps for `d4`, `d5`, and `w6` is sufficient to generate an independent sharp `D` cap.  A raw `d6` interval is not mathematically necessary if the signed affine combination `w6` can be produced directly.

This is a **mathematical source-interface refinement**, not actual source closure.  The repository still lacks the same-key actual packet proving the required affine identities/caps and the source identity of `H`.  The separately claimed `GH-MATH-P4-SCHUR-ACTUAL-SOURCE-PACKET` lane remains owned by 狂蛮魔尊; this review does not duplicate or pre-empt that producer work.

## 2. Exact metric used

The source-reification review proposes the exact rational inverse

```text
H =
[[ 50003000000/5000400003,  0,                    -50000000000/5000400003],
 [ 0,                        4000000/200739,         0],
 [-50000000000/5000400003,  0,                     350003000000/5000400003]].
```

Write

```text
h11 =  50003000000/5000400003,
h22 =  4000000/200739,
h13 = -50000000000/5000400003,
h33 =  350003000000/5000400003.
```

Then

```text
D = h11*d4^2 + h22*d5^2 + 2*h13*d4*d6 + h33*d6^2.
```

All identities below are exact rational algebra.  They do not use a floating-point eigenvalue, a numerical inverse, or a square root.

## 3. Exact completed-square identity

Because

```text
-h13/h33 = 50000/350003
```

and

```text
h11 - h13^2/h33 = 3000000/350003,
```

we have the exact identity

```text
D
 = (3000000/350003) * d4^2
 + (4000000/200739) * d5^2
 + (350003000000/5000400003)
     * (d6 - (50000/350003)*d4)^2.
```

Using `w6=350003*d6-50000*d4`, this becomes the division-free producer-facing form

```text
D
 = (3000000/350003) * d4^2
 + (4000000/200739) * d5^2
 + (1000000/1750155002250009) * w6^2,
```

where

```text
1750155002250009 = 5000400003 * 350003.
```

The three coefficients are strictly positive.

A second exact decomposition, useful as a regression identity, is

```text
D
 = (50003000000/5000400003)
     * (d4 - (50000/50003)*d6)^2
 + (4000000/200739) * d5^2
 + (3000000/50003) * d6^2.
```

The two decompositions are algebraically identical.

## 4. Minimal same-key `D` producer theorem

Assume one physical/source key supplies the exact same defect vector `d=(d4,d5,d6)` and nonnegative caps

```text
d4^2 <= U4,
d5^2 <= U5,
w6^2 <= U6,
w6 = 350003*d6 - 50000*d4.
```

Then the completed-square identity gives

```text
D <= Delta_H(U4,U5,U6),
```

with

```text
Delta_H(U4,U5,U6)
 := (3000000/350003) * U4
  + (4000000/200739) * U5
  + (1000000/1750155002250009) * U6.
```

This is the smallest source-facing theorem needed to repair the rank-deficient observation in the previous round.  The trusted consumer needs only exact rational multiplication/addition and order comparison.

### Sharpness under independent transformed-coordinate caps

The map

```text
(d4,d5,d6) -> (d4,d5,w6)
```

is invertible because the coefficient of `d6` in `w6` is `350003 != 0`.  Every corner of an independent symmetric box in `(d4,d5,w6)` is therefore realizable by a unique physical `d`.

Since the exact energy is diagonal with positive coefficients in these coordinates, the bound above is the exact maximum over

```text
|d4| <= sqrt(U4),
|d5| <= sqrt(U5),
|w6| <= sqrt(U6)
```

whenever those square roots are only semantic notation for the symmetric quadratic caps.  No smaller uniform coefficient can be obtained from these three independent quadratic caps alone.

The checker itself does not need to compute any square root.

## 5. Why this is the mathematically natural third scalar

Normalize a candidate third scalar as

```text
t_q := d6 - q*d4.
```

Substitute `d6=t_q+q*d4` into `D`.  The cross coefficient between `d4` and `t_q` is

```text
2*(h33*q + h13).
```

It vanishes if and only if

```text
q = -h13/h33 = 50000/350003.
```

Hence `r6=d6-(50000/350003)d4` is the **unique normalized third scalar that H-orthogonalizes the missing direction from the observed d4 direction**.  The integer-scaled `w6` has the same property.

This matters for interval production.  If `d4` and `d6` are separately intervalized first and only then combined, the negative cross correlation can be lost.  Producing `w6` from the exact affine source expression before intervalization preserves the cancellation selected by the actual metric.

This is a statement about algebraic decoupling, not a claim that `w6` always has the narrowest numerical interval under every possible correlated enclosure method.

## 6. Direct connection to `d=A y+b`

Suppose the desired actual source identity eventually has

```text
d = A*y + b,
```

with rows `A4,A5,A6` and offsets `b4,b5,b6` in block456 order.  Then the new scalar is itself an exact affine source observable:

```text
w6
 = 350003*d6 - 50000*d4
 = (350003*A6 - 50000*A4) * y
   + (350003*b6 - 50000*b4).
```

Therefore the producer does **not** need to first construct a full box for all of `d` and then compute `D`.  It is enough to prove, under the same configuration/source/domain key,

```text
d4 = A4*y+b4,
d5 = A5*y+b5,
w6 = (350003*A6-50000*A4)*y + (350003*b6-50000*b4),
```

and generate the three quadratic caps `U4,U5,U6` from those exact signed affine rows.

This can reduce the amount of source information required relative to the previous round's conservative request for a complete six-dimensional `y` box: only the coordinates of `y` that are active in `A4`, `A5`, or `350003*A6-50000*A4` must be bounded for this `D` producer.  If the last signed row cancels some previously unobserved directions exactly, those directions need not be bounded merely to reconstruct `d6` separately.

Conversely, if any unobserved `y` direction survives in one of these three affine rows and remains unbounded, this theorem does not close the source packet.

## 7. Exact necessity of a genuine third direction

The refinement does not remove the old rank obstruction.

Let the currently observed raw rows be

```text
L0(d) = (d4,d5).
```

Then `ker L0 = span(e6)`.  Add any third scalar

```text
t(d) = a*d4 + b*d5 + c*d6.
```

The augmented observation `(d4,d5,t(d))` is injective if and only if `c != 0`.

- If `c=0`, `e6` remains in the kernel.  Scaling `t*e6` makes `D` arbitrarily large because `H` is positive definite.  No finite uniform `D` cap can follow.
- If `c!=0`, the three observations determine `d` uniquely, hence a finite quadratic bound can in principle be obtained from finite observation bounds.

Our `w6` uses `c=350003`, so it is a genuine third direction.  Moreover it is the particular direction that diagonalizes the exact `H` energy.

This provides a typed fail-closed rule for future adapters: a purported third scalar whose `d6` coefficient vanishes cannot repair the source-dimension obstruction, regardless of how small its interval is.

## 8. Sharp fallback if source only exposes raw coordinate boxes

If source production can only prove symmetric raw bounds

```text
|d4| <= a,
|d5| <= b,
|d6| <= c,
a,b,c >= 0,
```

then the completed-square identity yields the exact symmetric-box maximum

```text
D <=
  (3000000/350003) * a^2
  + (4000000/200739) * b^2
  + (350003000000/5000400003)
      * (c + (50000/350003)*a)^2.
```

It is sharp: choose `|d4|=a`, `|d5|=b`, `|d6|=c` and choose the signs of `d4,d6` oppositely, which maximizes `|d6-(50000/350003)d4|`.

This fallback is mathematically safe but usually inferior to directly intervalizing `w6`, because it discards any source correlation between rows 4 and 6.

## 9. Separation from `u` and `s`

The assignment asks for separated Schur outputs

```text
u = <ell,d>_H,
s = <ell+r0,d>_H,
D = d^T H d.
```

The previous obstruction remains decisive: `D` must not be reconstructed from only `u` and `s` in a three-dimensional SPD metric.  This review gives an economical independent `D` producer, not a way to eliminate that independence requirement.

Once `d=A y+b` is source-bound, the best pattern is to form **all three signed affine observables before intervalization**:

```text
u(y),
s(y),
w6(y),
```

plus the raw/orthogonal rows needed for `U4,U5`.  Their intervals may then be consumed separately under one source/configuration/domain key.  Do not infer `D` from the `u/s` intervals.

## 10. Relation to the existing matching-metric `rho2_m0_upper` lane

The matching-metric review has a different conditional object:

```text
r_C^T H r_C <= gamma_k * a_C^T P_k a_C.
```

If its historical producer/source/domain/rounding identities are eventually validated, it already supplies a whole-vector H-energy cap for that **homogeneous remote port** `r_C` and does not need the present coordinate decomposition.

The present theorem addresses the actual signed-affine defect lane `d=A y+b`.  The two packets must not be spliced merely because they use the same 3x3 `H`; their residual identities and source keys are separate obligations.  In particular, the serialized `rho2_m0_upper` values remain conditional because their producer hash/source/rounding/domain binding is still open.

## 11. Suggested Lean leaves

The first theorem should be purely algebraic and source-independent.

```lean
-- schematic constants specialized to the exact block456 metric
 theorem block456_H_complete_square
   (d4 d5 d6 : Real) :
   h11*d4^2 + h22*d5^2 + 2*h13*d4*d6 + h33*d6^2
     = (3000000/350003 : Real)*d4^2
       + (4000000/200739 : Real)*d5^2
       + (350003000000/5000400003 : Real)
           *(d6-(50000/350003 : Real)*d4)^2 := by
   norm_num [h11,h22,h13,h33]
   ring
```

A division-free consumer leaf can use `w6` directly:

```lean
 theorem block456_H_cap_of_residualized_caps
   (d4 d5 d6 U4 U5 U6 D : Real)
   (hw : w6 = 350003*d6 - 50000*d4)
   (hD : D = block456Quad d4 d5 d6)
   (h4 : d4^2 <= U4)
   (h5 : d5^2 <= U5)
   (h6 : w6^2 <= U6) :
   D <= (3000000/350003 : Real)*U4
      + (4000000/200739 : Real)*U5
      + (1000000/1750155002250009 : Real)*U6 := by
   -- rewrite by the exact identity, then positivity + linarith/nlinarith
```

A small structural obstruction theorem should also be retained:

```lean
 theorem third_observation_with_zero_d6_coefficient_cannot_cap
   (H : ...) (hHpd : PositiveDefinite H)
   (a b : Real) :
   -- observations d4,d5,a*d4+b*d5 leave e6 in the kernel,
   -- hence no finite uniform H-energy cap exists.
```

The generalized Schur-complement identity for an arbitrary SPD block can be added later; the specialized rational identity is the highest-value first leaf because it pins the actual source metric convention and is trivial for the kernel to check.

## 12. Remaining obligations / status

This review closes only the **mathematical question of what minimum third-direction information is sufficient once the recorded exact H is accepted**.

Still open:

1. actual same-key source identity `d=A y+b`;
2. actual affine rows/offsets and exact signed producer for `d4,d5,w6`;
3. finite source-valid caps `U4,U5,U6` on the same physical cell/domain;
4. source reification proving the deployed/reference `M0_CC` and inverse semantics equal the recorded rational `KQ/HQ` rather than merely an algebraically valid candidate;
5. separate same-key `u` and `s` source outputs if the Schur consumer uses them;
6. source/runtime/Float64/interval semantics and physical coverage;
7. Lean/kernel receipt if this child is formalized;
8. independent validation by 封不觉;
9. admission/registry/final P4 propagation.

Accordingly the task remains `pending` at parent/source level.  The new contribution is the exact sharp source contract

```text
(d4^2 <= U4) + (d5^2 <= U5) + ((350003*d6-50000*d4)^2 <= U6)
    ==> d^T H d <= Delta_H(U4,U5,U6),
```

and the proof that this third scalar is the unique normalized H-orthogonalized completion of the currently missing block456 direction.
