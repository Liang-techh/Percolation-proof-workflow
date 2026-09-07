---
kind: review_result
review_id: review-T-P4-013-kuangmanmozun-20260907T0145
task_id: T-P4-013
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T01:38:00-06:00
created_at: 2026-09-07T01:45:00-06:00
inspected_commit: 9f20a58b491398bd83957898ae3db7ae2f12e2ff
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_normalization_aware_shifted_residual_schur_and_use_force_coordinate_constants_downstream
---

# T-P4-013 — normalization-aware `kc` sharp Schur budget and the exact remaining-residual allowance

## Scope

`T-P4-011` computed the Schur/Young cost of the raw PMI-coordinate cross term

```text
rho_kc^f = (q5/20, q4/20),
```

while the newer typed bridge `T-P4-008` proves that the actual P4 generalized-force residual

```text
l_F := I_B f_B - M0_BB a_B,
I_B = diag(1/5,1/10),
```

contains instead

```text
rho_kc^F = I_B rho_kc^f = (q5/100, q4/200).                  (1)
```

This pass recomputes the sharp inequality budget after that normalization and derives the exact robust composition theorem for adding other same-coordinate residual terms. It is deliberately disjoint from the already-claimed `T-P4-012` remote `M_BD a_D` mass-metric task.

Inputs inspected:

- `review-T-P4-008-liuguanyi-20260907T0120.md` for the typed normalization (1) and the full remote-action obstruction;
- `review-T-P4-011-kuangmanmozun-20260907T0046.md` for the earlier raw-coordinate Schur calculation;
- `examples/routeb_p4_sharp_schur_sidecar/P4SharpSchur.lean` for the exact theorem
  `forall x, 0 <= p*x^2 + 2*x*r + d*y^2  <->  r^2 <= p*d*y^2` when `p>0`.

No source semantic binding, remote-action bound, P8 coverage, Lean validation, admission, or final P4/M4 closure is claimed.

## 1. Normalization changes the sharp coefficients by factors 25 and 100 in squared budget

For channel 4, once the Schur coordinate is typed as `y=q5`, the generalized-force `kc` residual is

```text
r4 = y/100.                                                  (2)
```

Thus the necessary-and-sufficient sharp Schur coefficient condition is

```text
1/10000 <= p4*d4.                                           (3)
```

For channel 5, with `y=q4`,

```text
r5 = y/200,                                                  (4)
```

and the sharp condition is

```text
1/40000 <= p5*d5.                                           (5)
```

Compare this with the raw-coordinate requirement `1/400 <= p*d` from `T-P4-011`: applying `I_B` reduces the squared `kc` charge by exactly `25` in channel 4 and `100` in channel 5.

Therefore the statement in `T-P4-011` that the old `1/100` residual target is numerically too small is true only for the raw `f` coordinate. It does **not** transfer to the P4 force residual `l_F`. In generalized-force coordinates, channel 4 `kc` alone exactly matches coefficient `1/100`, while channel 5 is only `1/200`.

This is a mathematical consequence of the typed normalization, not a choice of a more favorable constant.

## 2. Exact block-4 margin after the force normalization

The existing abstract block-4 constants are

```text
p4 = 3/5,
d4 = 116667666666667 / 10^15.
```

Hence

```text
p4*d4 - 1/10000
 = 349503000000001 / 5000000000000000
 > 0.                                                        (6)
```

So the normalized `kc` contribution uses only about `0.14%` of the available squared Schur budget:

```text
(1/10000)/(p4*d4) ~= 0.00142856.
```

The exact completion is

```text
p4*x^2 + 2*x*(y/100) + d4*y^2
 = (p4*x+y/100)^2/p4
   + (d4 - 1/(10000*p4))*y^2,                               (7)
```

with consumed diagonal cost

```text
1/(10000*p4) = 1/6000,
```

and remaining coefficient

```text
d4 - 1/6000
 = 349503000000001 / 3000000000000000
 > 0.                                                        (8)
```

A particularly simple Young choice is `eps=1/100`:

```text
2*x*(y/100) >= -(1/100)x^2 -(1/100)y^2.                     (9)
```

Thus any channel with `p>=1/100` and `d>=1/100` absorbs this normalized cross term. For the current block-4 constants the retained coefficients are

```text
p4-1/100 = 59/100,
d4-1/100 = 106667666666667 / 10^15,
```

both strictly positive.

## 3. The exact robust composition theorem: `kc + other residual`

The more useful downstream statement is not `kc` alone. Let

```text
r = c*y + e,
c >= 0,
beta >= 0,
|e| <= beta*|y|.                                            (10)
```

Then by the triangle inequality

```text
|r| <= (c+beta)|y|.                                         (11)
```

Moreover `(c+beta)` is the **smallest possible universal coefficient** under only (10): choose `y=1` and `e=beta` to attain equality. Therefore, for `p>0`, the sharp scalar Schur theorem gives the robust iff

```text
[for every y,e with |e|<=beta|y|, and every x,
  0 <= p*x^2 + 2*x*(c*y+e) + d*y^2]

iff

(c+beta)^2 <= p*d.                                          (12)
```

The reverse direction is (11) plus the sharp Schur theorem. Necessity follows by the same-sign extremizer `y=1,e=beta` and minimizing in `x`.

This is the right interface for combining the typed `kc` contribution with independent same-coordinate force errors. It avoids hiding a triangle inequality inside an arbitrary total residual constant.

Lean-friendly version without square roots:

```lean
theorem shifted_residual_schur
    (p d c beta x y e : R)
    (hp : 0 < p) (hc : 0 <= c) (hbeta : 0 <= beta)
    (he : |e| <= beta*|y|)
    (hbudget : (c+beta)^2 <= p*d) :
    0 <= p*x^2 + 2*x*(c*y+e) + d*y^2
```

and a separate extremizer theorem proving sharpness of the coefficient `c+beta`.

## 4. Exact residual headroom under the existing `1/4` consumer

The compiled abstract block-4 sidecar already accepts any total residual satisfying coefficient `1/4`. For the actual force-coordinate channel-4 `kc`, `c=1/100`. Therefore the largest independent other-residual coefficient that can be certified solely by triangle inequality while preserving the `1/4` envelope is exactly

```text
beta4 <= 1/4 - 1/100 = 6/25.                                (13)
```

Indeed

```text
1/100 + 6/25 = 1/4.
```

So the clean corrected source target is

```text
|e_other,4| <= (6/25)|q5|
------------------------------------------------
|q5/100 + e_other,4| <= (1/4)|q5|.                          (14)
```

This is materially less restrictive than the raw-coordinate target from `T-P4-011`, which left only `1/5` coefficient headroom after charging `1/20`.

For channel 5, the normalized `kc` coefficient is `1/200`; if a future channel-5 Schur consumer also allows total coefficient `1/4`, the analogous headroom would be

```text
beta5 <= 1/4 - 1/200 = 49/200.                              (15)
```

That last statement is only a coefficient arithmetic interface; this review does not assert that the physical channel-5 `p5*d5` has already been source-bound to the quarter condition.

## 5. Precise status of the historical `1/100` total residual target

The normalization gives a more nuanced conclusion than either “the old target works” or “the old target fails.”

### Channel 4

Here `kc` itself has coefficient exactly `1/100`. Therefore it **saturates** a total envelope

```text
|r_total| <= (1/100)|y|.                                    (16)
```

If the only information on an additional residual is

```text
|e| <= beta|y|
```

with any `beta>0`, then no universal proof of (16) is possible: choose `y=1,e=beta` with the same sign as `kc`. This gives

```text
|1/100 + beta| > 1/100.                                     (17)
```

Thus the historical target is valid for the normalized `kc` term **alone**, but leaves zero adversarial headroom for any separately bounded same-sign residual. To reuse it for the full channel one must prove either `e=0` or a correlation/sign/cancellation theorem, not merely a positive magnitude envelope.

### Channel 5

Here `kc=1/200` leaves exactly `1/200` coefficient headroom under a `1/100` total target. Under only separate absolute bounds, the condition

```text
|e| <= (1/200)|y|                                           (18)
```

is sufficient and sharp for retaining the old total coefficient.

This sharply identifies why blindly restoring the old `1/100` artifact is still unsafe even though the normalization fixes the earlier scale mismatch.

## 6. Local-state norm improves by a sharp factor 25

From (1),

```text
||rho_kc^F||^2
 = q5^2/10000 + q4^2/40000.                                 (19)
```

Since

```text
Pstate = (3/2)(q4^2+q5^2) + (4/5)(v4^2+v5^2),
```

we have the sharp operator-norm inequality

```text
||rho_kc^F||^2 <= (q4^2+q5^2)/10000
                <= Pstate/15000.                            (20)
```

The constant `1/15000` is sharp from this information alone: take `q4=0`, `v4=v5=0`, and `q5 != 0`.

Therefore on the local PMI sublevel `Pstate<=28/5`,

```text
||rho_kc^F||^2 <= 7/18750.                                  (21)
```

The raw-coordinate bound in `T-P4-011` was `7/750`; (21) is exactly `25` times smaller, matching the largest singular value `||I_B||=1/5` at squared level.

Under only the joint limits `|q4|,|q5|<=pi`,

```text
||rho_kc^F||^2 <= pi^2/8000.                                (22)
```

Again, local sublevel and joint-limit bounds are different domains and should not be mixed.

## 7. What this fixes and what remains open

Mathematically fixed here:

1. generalized-force sharp coefficients are `1/100` and `1/200`, not `1/20`;
2. the raw-coordinate claim “old `1/100` target is too small for kc” does not apply to `l_F`;
3. channel 4 normalized `kc` alone saturates the historical `1/100` total target but fits the `1/4` consumer with exact independent residual headroom `6/25`;
4. the robust `kc + other` Schur condition is exactly `(c+beta)^2<=p*d` under only a separate magnitude envelope;
5. the local squared-norm budget is `<=Pstate/15000`, hence `<=7/18750` on `Pstate<=28/5`.

Still open and deliberately not taken over:

- `T-P4-012`: the remote `M_BD a_D` term and its mass-metric absorption;
- source binding for the other terms in the `T-P4-008` decomposition;
- whether each P4 Schur auxiliary `y` is exactly the physical cross coordinate after normalization;
- whether other residual terms are same-coordinate/relative, additive, or correlated with `kc`;
- Float64/source semantic binding, P8 coverage, and P4/M4 admission.

## Recommended next action

1. Formalization lane: implement the generic `shifted_residual_schur` theorem and the concrete channel-4 `beta<=6/25` corollary; no square roots are required.
2. P4 source lane: report the residual decomposition in generalized-force coordinates and target the *remaining* channel-4 relative envelope `|e_other,4|<=(6/25)|q5|` if the existing quarter consumer is retained.
3. Do not revive the historical `1/100` total target for channel 4 unless the non-kc remainder is proved zero or a signed/correlated cancellation is available; the normalized `kc` term already saturates that target.
4. Keep `T-P4-012` independent: a successful remote mass-metric bound must still be converted into a same-coordinate/Schur-compatible form before it can consume the coefficient headroom above.

Admission remains `pending`; this is a mathematical inequality correction/bridge only, awaiting any formalization, independent validation, and 梁智炜 integration.
