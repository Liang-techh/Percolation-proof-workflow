---
kind: review_result
review_id: review-T-P5-031-guyuefangyuan-20260907T1224
task_id: T-P5-031
source_agent: 古月方源
agent: 古月方源
claimed_at: 2026-09-07T12:22:00-06:00
created_at: 2026-09-07T12:24:00-06:00
inspected_commit: 9b3384dbc4545d7cec73357319f1d5325520b68d
inspected_paths:
  - agent_review_inbox/review-T-P5-030-honglianmozun-20260907T1205.md
  - agent_review_inbox/review-T-P5-020-guyuefangyuan-20260907T0743.md
continuation_of:
  - review-T-P5-030-honglianmozun-20260907T1205
  - review-T-P5-020-guyuefangyuan-20260907T0743
related_reviews:
  - review-T-P5-018-guyuefangyuan-20260907T0634
  - review-T-P5-019-honglianmozun-20260907T0702
  - review-T-P5-026-guyuefangyuan-20260907T1031
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_square_only_physical_increment_gain_to_mu_nu_bridge_and_have_the_source_lane_supply_same_domain_force_normalized_incremental_gains_before_consuming_the_T_P5_030_parameter_tube
---

# T-P5-031 — physical incremental gains imply the `mu/nu` envelope for the moving-frame parameter tube

## 0. Result in one sentence

`T-P5-030` reduced ramp-parameter contraction to the source-facing premise

```text
||Dl||^2 <= mu * Vd + nu * dc^2.                         (0.1)
```

The missing bridge can be made completely rational and square-only.  If a source checker supplies nonnegative component gains for the **physical** block differences `(dq4,dq5,dv4,dv5,dw,dc)`, then the exact moving-frame identities transport those gains to two scalars `U,W >= 0`.  Any nonnegative slack pair `p,q` satisfying

```text
p*q >= U*W                                                (0.2)
```

gives

```text
||Dl||^2 <= (U+p) * Vd + (W+q) * dc^2.                   (0.3)
```

Thus the entire `T-P5-030` tube condition can be checked directly by the two division-free inequalities

```text
p*q >= U*W,
11424*(U+p) + 137088*(W+q) < 2285.                       (0.4)
```

No square root is needed in the trusted consumer.  Moreover, before searching `p,q`, the bridge has an exact scalar feasibility obstruction: with

```text
R := 2285 - 11424*U - 137088*W,
```

there exists a real slack pair passing (0.4) iff

```text
R > 0,
R^2 > 6264373248 * U*W.                                  (0.5)
```

For rational source gains, a checker can simply emit a nearby rational `p,q` and verify (0.4); it need not formalize the square-root optimizer behind (0.5).

This is source-independent mathematics.  It does not supply the gain table, prove Float64 Lipschitz continuity, prove P8 coverage, or promote P5/M4.

---

## 1. Exact moving-frame transport reused from T-P5-030

Use the two-trajectory notation of `T-P5-030`:

```text
X = x1-x2,
Y = y1-y2,
dc = c1-c2,
Vd = the incremental hypocoercive storage.
```

For the physical block coordinates, the moving frame gives exactly

```text
dq_i := q1_i-q2_i = X_i + (h_i*t+r_i)*dc,
dv_i := v1_i-v2_i = Y_i + h_i*dc,
dw   := w1-w2       = t*dc.                              (1.1)
```

The exact constants are

```text
h4 = 2340/8699,
h5 = 1520/8699,

r4 = -21912800/75672601,
r5 = -15007200/75672601.                                 (1.2)
```

On `0 <= t <= 1`, both affine factors remain negative:

```text
r4+h4 = -1557140/75672601 < 0,
r5+h5 = -1784720/75672601 < 0.                            (1.3)
```

Since `h4,h5>0`, `r_i+h_i*t` increases monotonically but stays negative.  Hence the exact endpoint bounds are

```text
|h4*t+r4| <= A4 := 21912800/75672601,
|h5*t+r5| <= A5 := 15007200/75672601.                     (1.4)
```

Also

```text
|h4| = 2340/8699,
|h5| = 1520/8699,
|t| <= 1.                                                 (1.5)
```

Therefore, with `d := |dc|`, (1.1) implies

```text
|dq4| <= |X4| + A4*d,
|dq5| <= |X5| + A5*d,
|dv4| <= |Y4| + h4*d,
|dv5| <= |Y5| + h5*d,
|dw|  <= d.                                               (1.6)
```

Nothing in this step assumes source smoothness; it is only the exact coordinate transform.

---

## 2. Source-facing physical incremental gain contract

Let `Dl=(Dl_4,Dl_5)` be the **already force-normalized** residual difference consumed by `T-P5-030`.  Suppose a source/evaluator theorem supplies, on the same typed domain, nonnegative gains

```text
k[a,q4], k[a,q5], k[a,v4], k[a,v5], k[a,w], k[a,c] >= 0   (2.1)
```

for `a in {4,5}`, with

```text
|Dl_a|
 <= k[a,q4]*|dq4|
  + k[a,q5]*|dq5|
  + k[a,v4]*|dv4|
  + k[a,v5]*|dv5|
  + k[a,w] *|dw|
  + k[a,c] *|dc|.                                         (2.2)
```

`k[a,c]` is optional.  It is zero when the residual map has no direct ramp-rate input after the exact moving-frame/source adapter.  It is kept explicit so that an actual source contract never has to hide a direct parameter dependence inside a state gain.

Substitute (1.6).  Define the centered state part

```text
S_a
 := k[a,q4]*|X4|
  + k[a,q5]*|X5|
  + k[a,v4]*|Y4|
  + k[a,v5]*|Y5|,                                         (2.3)
```

and the deterministic parameter gain

```text
G_a
 := k[a,q4]*A4
  + k[a,q5]*A5
  + k[a,v4]*h4
  + k[a,v5]*h5
  + k[a,w]
  + k[a,c].                                               (2.4)
```

All terms in (2.4) are nonnegative.  Then

```text
|Dl_a| <= S_a + G_a*d.                                    (2.5)
```

For a general horizon `0<=t<=T`, replace `A_i` by any certified bound for `|h_i*t+r_i|`, replace the `k[a,w]` term by `T*k[a,w]`, and leave the rest unchanged.  The `T=1` form above is the current Route-B specialization.

### Boundary of this contract

Equation (2.2) must cover every source input on which `Dl` actually depends.  If other mechanical coordinates vary and affect `Dl`, their differences must either be added as extra gain channels with their own moving/tube support bounds or be separately fixed/bounded by a theorem.  This review does **not** silently drop the other ten mechanical coordinates.

---

## 3. Convert the centered component gains to one `U*Vd` budget

`T-P5-030` reuses the sharp coordinate supports

```text
X4^2 <= alpha4 * Vd,
X5^2 <= alpha5 * Vd,
Y4^2 <= beta4  * Vd,
Y5^2 <= beta5  * Vd,                                     (3.1)
```

with exact positive rationals

```text
alpha4 = 9438522000000 / 6764044380739,
alpha5 = 34399976000000 / 20292133142217,

beta4  = 43887777300000000000 / 2367435825391792217,
beta5  = 56414160640000000000 / 1357807504945166121.     (3.2)
```

For nonnegative `u1,...,u4`,

```text
(u1+u2+u3+u4)^2 <= 4*(u1^2+u2^2+u3^2+u4^2).              (3.3)
```

Apply (3.3) to (2.3), then use (3.1):

```text
S_a^2 <= U_a * Vd,                                        (3.4)
```

where

```text
U_a := 4 * (
    k[a,q4]^2 * alpha4
  + k[a,q5]^2 * alpha5
  + k[a,v4]^2 * beta4
  + k[a,v5]^2 * beta5).                                  (3.5)
```

Define

```text
U := U_4 + U_5,
W := G_4^2 + G_5^2.                                      (3.6)
```

Then

```text
S_4^2 + S_5^2 <= U*Vd.                                   (3.7)
```

The factor `4` in (3.3) is only a convenient default, not a structural loss.  A sharper all-rational variant chooses positive rational weights `omega_j` with `sum_j omega_j=1` and uses

```text
(sum_j u_j)^2 <= sum_j u_j^2 / omega_j.                  (3.8)
```

Then (3.5) may be replaced by

```text
U_a(omega)
 := sum_j k[a,j]^2 * c_j / omega_j,                      (3.9)
```

where `c=(alpha4,alpha5,beta4,beta5)`.  A checker can search rational `omega`; the trusted theorem only checks positivity, `sum omega=1`, and the resulting rational inequality.  The uniform choice `omega_j=1/4` recovers (3.5).

---

## 4. Main square-only bridge: one product inequality replaces square roots

From (2.5),

```text
||Dl||^2
 <= (S_4+G_4*d)^2 + (S_5+G_5*d)^2
 = A + 2*d*C + W*d^2,                                    (4.1)
```

where

```text
A := S_4^2+S_5^2,
C := S_4*G_4 + S_5*G_5.                                  (4.2)
```

By (3.7),

```text
A <= U*Vd.                                                (4.3)
```

Cauchy on the two residual channels gives

```text
C^2 <= (S_4^2+S_5^2)*(G_4^2+G_5^2)
    <= U*W*Vd.                                            (4.4)
```

Now choose any

```text
p >= 0,
q >= 0,
p*q >= U*W.                                             (4.5)
```

I claim

```text
2*d*C <= p*Vd + q*d^2.                                   (4.6)
```

This can be proved without division or square roots.  All quantities on both sides are nonnegative, and (4.4)-(4.5) give

```text
C^2 <= p*q*Vd.                                           (4.7)
```

Then

```text
(p*Vd + q*d^2)^2 - (2*d*C)^2
 = (p*Vd - q*d^2)^2
   + 4*d^2*(p*q*Vd - C^2)
 >= 0.                                                    (4.8)
```

Since both compared quantities are nonnegative, (4.8) implies (4.6).

Combining (4.1), (4.3), and (4.6):

```text
||Dl||^2
 <= (U+p)*Vd + (W+q)*d^2
 =  (U+p)*Vd + (W+q)*dc^2.                               (4.9)
```

Therefore the exact source-to-`T-P5-030` assignment is

```text
mu := U+p,
nu := W+q.                                                (4.10)
```

### Theorem 4.1 — physical gain to moving-frame residual envelope

Under (1.1), the physical incremental contract (2.2), the coordinate supports (3.1), nonnegativity of the gains/storage, and (4.5), equation (4.9) holds.

This is the central new bridge.

---

## 5. Direct `1/12` parameter-tube gate

`T-P5-030` proves the convenient boundary is inward when

```text
11424*mu + 137088*nu < 2285.                              (5.1)
```

Using (4.10), the source checker no longer needs to manufacture `mu,nu` indirectly.  It may instead emit `U,W,p,q` and check

```text
p >= 0,
q >= 0,
p*q >= U*W,
11424*(U+p) + 137088*(W+q) < 2285.                        (5.2)
```

Every quantity in (5.2) can be an exact rational.  Once (5.2) and the remaining `T-P5-030` ODE/first-exit hypotheses are supplied, the existing conclusion

```text
Vd < dc^2/12                                              (5.3)
```

follows for the parameter cell.

This bridge does not duplicate the `T-P5-026/029` SPN path.  Those children consume a direct **power** envelope and preserve the full component geometry.  `T-P5-031` is specifically the norm-square consumer needed by `T-P5-030`; it should be used only on the parameter-tube branch.

---

## 6. Exact feasibility obstruction for the slack allocation

The two slack variables in (5.2) have a sharp scalar feasibility test over the reals.

Set

```text
A0 := 11424,
B0 := 137088 = 12*A0,
R  := 2285 - A0*U - B0*W.                                (6.1)
```

The remaining conditions are

```text
p,q >= 0,
p*q >= U*W,
A0*p+B0*q < R.                                            (6.2)
```

### Necessity

If (6.2) holds, then `R>0`.  Also

```text
(A0*p+B0*q)^2 >= 4*A0*B0*p*q >= 4*A0*B0*U*W.             (6.3)
```

Since `A0*p+B0*q<R`,

```text
R^2 > 4*A0*B0*U*W.                                       (6.4)
```

The exact integer factor is

```text
4*A0*B0 = 6264373248.                                    (6.5)
```

Hence failure of either

```text
R > 0,
R^2 > 6264373248*U*W                                     (6.6)
```

is a genuine obstruction to this aggregated `U/W` bridge; no choice of Young/slack split can rescue it.

### Sufficiency over the reals

If `U*W>0`, the weighted product constraint has the minimum weighted cost

```text
min_{p*q>=U*W} (A0*p+B0*q)
 = 2*sqrt(A0*B0*U*W),                                    (6.7)
```

attained at

```text
p_* = sqrt(B0*U*W/A0),
q_* = sqrt(A0*U*W/B0).                                   (6.8)
```

Thus (6.6) is also sufficient for a real pair satisfying (6.2).  When `U*W=0`, take `p=q=0` and only `R>0` remains.

The trusted checker does **not** need (6.7)-(6.8).  Because the desired inequalities are strict and the source data are rational, it can search a nearby rational pair and submit only (5.2).  Equations (6.6) are mainly a fast counterexample-guided diagnostic: if they fail, tighten the gain table or the weighted state bound before spending effort on a `p,q` search.

---

## 7. Relation to T-P5-020 and source Jacobians

`T-P5-020` already identified the correct qualitative split: smooth centered variation should be charged as a small gain, while true execution/anchor effects must not be silently forced into that branch.

`T-P5-031` supplies the missing ramp-parameter transport for that idea.  A smooth exact-real source residual can obtain the nonnegative gains in (2.2), for example, from same-domain interval bounds on the relevant partial derivatives followed by a segment/mean-value theorem.  The resulting `K_phys` then enters (2.3)-(3.6), while the affine ramp offsets enter only through `G_a`.

The following boundary is essential:

- a Jacobian bound for the smooth exact-real residual does not automatically bound the real-lift of a Float64 implementation;
- a Float64 rounding/solve/controller difference that can jump across an execution threshold may fail to admit a uniform Lipschitz gain as `dc -> 0`;
- such a term requires its own incremental execution theorem, a cell-local discrete argument, or a different additive/absolute tube.  It cannot simply be inserted into `k[a,*]` because a pointwise absolute error bound is not an incremental gain.

This is exactly the scaling obstruction already exposed by `T-P5-030`: a fixed positive difference floor cannot certify a tube whose diameter vanishes like `dc^2`.

---

## 8. Lean-friendly theorem decomposition

No ODE API is needed for this child.  The smallest useful formal pieces are:

```text
four_term_weighted_square
```

Inputs: `omega_j>0`, `sum omega=1`.
Output:

```text
(sum_j u_j)^2 <= sum_j u_j^2/omega_j.
```

A fixed four-term/no-division corollary may simply prove (3.3).

```text
moving_frame_physical_increment_gain
```

Inputs: the exact identities (1.1), `0<=t<=1`, exact endpoint bounds (1.4), nonnegative source gains, and (2.2).
Output: (2.5) with exact `G_a`.

```text
aggregate_centered_gain_bound
```

Inputs: (3.1), nonnegative gains.
Output: (3.7) with either the fixed `U` in (3.5)-(3.6) or the weighted version (3.9).

```text
product_slack_cross_bound
```

Minimal scalar statement:

```text
0<=V, 0<=d, 0<=C, 0<=U, 0<=W,
C^2 <= U*W*V,
0<=p, 0<=q,
U*W <= p*q
------------------------------------------------
2*d*C <= p*V + q*d^2.
```

Proof should use the square identity (4.8), avoiding division and square roots.

```text
physical_gain_to_mu_nu_envelope
```

Inputs: (2.5), (3.7), (4.5).
Output:

```text
||Dl||^2 <= (U+p)*Vd + (W+q)*dc^2.
```

```text
parameter_tube_gain_gate
```

Inputs: the previous theorem and

```text
11424*(U+p)+137088*(W+q)<2285.
```

Output: the exact `mu/nu` premise expected by the already formalized `T-P5-030` ledger/boundary theorem.  The first-exit/ODE wrapper remains a separate consumer.

An optional diagnostic theorem can formalize the necessity direction of (6.6); the existence direction is not required for the kernel path because the checker can submit explicit rational `p,q`.

---

## 9. Remaining open obligations

Still open, explicitly:

1. derive a real source-bound, force-normalized incremental gain table satisfying (2.2) on the same P8/first-exit domain;
2. include every residual-dependent state coordinate rather than silently treating the block as isolated;
3. establish incremental semantics for Float64 `dM/cijk/accumulation`, linear solve, and controller/reference arithmetic, or keep those pieces out of the shrinking parameter tube;
4. provide the center/nominal trajectory and absolute P8 source-domain coverage;
5. provide ODE existence/continuation and the first-exit wrapper that consumes the already proved inward boundary;
6. independent validation by 封不觉 and final integration by 梁智炜.

No provenance/receipt/admission work was performed in this child.  No registry, state, P5, P8, or M4 final status is changed.

Current status: `pending mathematical child`; 待封不觉独立验证 / 待梁智炜最终整合。
