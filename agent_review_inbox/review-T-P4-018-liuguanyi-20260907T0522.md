---
kind: review_result
review_id: review-T-P4-018-liuguanyi-20260907T0522
task_id: T-P4-018
source_agent: 柳冠一
claimed_at: 2026-09-07T05:04:00-06:00
created_at: 2026-09-07T05:22:00-06:00
inspected_commit: 6c522cb0b1bf63cb6e0a22c460028b702c767005
inspected_paths:
  - docs/routeb-p4-kc-force-contract.md
  - docs/routeb-c2-d-normalization-audit.md
  - examples/routeb_source_binding_audit/REPORT.md
  - src/percolation_workflow/routeb_source_contract.py
  - agent_review_inbox/review-T-P4-013-kuangmanmozun-20260907T0145.md
  - agent_review_inbox/review-T-P4-017-kuangmanmozun-20260907T0449.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: distinguish acceleration-style PMI `f` from generalized-force `I_B f`; keep generic Schur lemmas, but do not treat `q/20` as an exact force residual unless the quadratic form is congruently renormalized
---

# T-P4-018 — force/acceleration congruence repair for the canonical `kc` seam

## Scope

`T-P4-017` correctly observes that the literal PMI polynomial contains `kc=1/20`, but it promotes the literal cross term

```text
rho_kc^f = (q5/20, q4/20)
```

to an exact **generalized-force** residual.  That conflicts with the already explicit B45-5/C2 descriptor contract

```text
l_F = I_B f_B - M0_BB a_B,
I_B = diag(1/5,1/10),
```

where `f_B` is acceleration-style nominal data and only `I_B f_B` is generalized force.

This review resolves the conflict at the mathematical interface level.  It does not choose a source snapshot by provenance, redo IEEE/source authentication, absorb the full residual, or modify P4/M4 state.  The main point is a typed normalization theorem:

> `1/20` is the coefficient in the PMI **nominal/acceleration-style** coordinate.  In the force residual `l_F`, the exact `kc` contribution is `(q5/100,q4/200)`.  One may work at the `1/20` scale only after a congruent change of the Schur quadratic form; changing the residual coefficient while leaving force-side `p,d` tagged as the same coordinates is not an exact coordinate transport.

## 1. The two current contracts cannot both be literal force equalities

The C2 normalization audit records

```text
f4 = -(15/4) q4 - 4 v4 + (1/20) q5 + w,
f5 = -(29/5) q5 - (13/2) v5 + (1/20) q4 + w,
```

and

```text
I_B = diag(1/5,1/10).
```

Therefore, by direct multiplication,

```text
I_B f_B =
  (-3/4 q4 - 4/5 v4 + 1/100 q5 + 1/5 w,
   -29/50 q5 - 13/20 v5 + 1/200 q4 + 1/10 w).        (1)
```

The same audit identifies this as the nominal generalized-force expression matching the deployed torque-scale coefficients.  B45-5 defines the force residual as

```text
l_F := I_B f_B - M0_BB a_B.                                (2)
```

Split the nominal expression as

```text
f_B = f_B^0 + rho_kc^f,
rho_kc^f := (q5/20,q4/20).                                  (3)
```

Linearity gives the exact force-side split

```text
l_F
 = [I_B f_B^0 - M0_BB a_B] + I_B rho_kc^f,                 (4)
```

and hence

```text
rho_kc^F := I_B rho_kc^f
          = (q5/100,q4/200).                                (5)
```

No dynamics, inequality, approximation, or source-authentication assumption is needed for (4)-(5); it is purely the definition of the already chosen residual coordinate.

Consequently, the two statements

```text
(A) l_F = I_B f_B - M0_BB a_B,
(B) the kc contribution to l_F is (q5/20,q4/20)
```

cannot both hold for arbitrary `q4,q5`, because `I_B != I`.  For example, at `q5=1,q4=0`, (A) makes the first cross contribution `1/100`, whereas (B) makes it `1/20`; their difference is exactly `1/25`.

Likewise, at `q4=1,q5=0`, the second force contribution is `1/200`, not `1/20`; the discrepancy is `9/200`.

This is the minimal obstruction behind the current documentation conflict.

## 2. Why the literal PMI coefficient is nevertheless `1/20`

There is no contradiction in the source itself.  The literal PMI expression `f_B` and the force residual `l_F` are different typed objects.

The deployed torque formula recorded by the source audits has the block coefficients matched by `I_B f_B`, not by `f_B` itself.  Thus `f_B` is naturally an acceleration-style normalized nominal expression; the scale map to generalized force is `I_B`.

The current `src/percolation_workflow/routeb_source_contract.py` checks the literal source strings

```text
kc = 0.05,
f1 = ... + kc*qb + ...,
f2 = ... + kc*qa + ...,
```

and from those strings alone sets

```text
expected_rho_kc = (q5/20,q4/20)
```

while calling that quantity force scale.  But that checker does not bind the `I_B f_B` multiplication from the descriptor residual.  Therefore the string check is enough to certify the literal coefficient **inside `f`**, but not enough to certify that the same coefficient is already in the `l_F` generalized-force coordinate.

A sound typed source contract should expose both objects instead of choosing one label:

```text
rho_kc_nominal = (q5/20,q4/20),
rho_kc_force   = I_B rho_kc_nominal = (q5/100,q4/200).       (6)
```

Downstream consumers must declare which one they use.

## 3. Exact scalar congruence theorem

The distinction does not mean that one is forbidden to reason in acceleration-style coordinates.  It means the quadratic form must transform with the residual.

Let `j>0` be a scalar normalization and suppose

```text
r_F = j r_A.                                                 (7)
```

Consider a force-coordinate scalar Schur form

```text
Q_F(x_F,y)
 := p_F x_F^2 + 2 x_F r_F + d y^2.                          (8)
```

Define

```text
x_A := j x_F,
p_A := p_F / j^2.                                           (9)
```

Then, identically,

```text
Q_F(x_F,y)
 = p_A x_A^2 + 2 x_A r_A + d y^2
 =: Q_A(x_A,y).                                              (10)
```

For Lean it is better to avoid division and state (9) as

```text
x_A = j*x_F,
p_F = j^2*p_A,
r_F = j*r_A.                                                 (11)
```

Substitution followed by `ring` proves (10).

Therefore the sharp scalar conditions are equivalent:

```text
r_A = c_A y
--------------------------------
force coordinates:        (j c_A)^2 <= p_F d,
acceleration coordinates: c_A^2     <= p_A d,               (12)
```

because `p_F=j^2 p_A`.

This is the precise transport theorem missing from the present scale discussion.

## 4. Channel-4 specialization

For channel 4,

```text
j4 = 1/5,
p_F = 3/5,
c_A = 1/20,
c_F = j4*c_A = 1/100.                                      (13)
```

The congruent acceleration-side quadratic coefficient is

```text
p_A = p_F/j4^2 = (3/5)/(1/25) = 15.                         (14)
```

Thus the exact same Schur problem can be written either as

```text
force:        p_F=3/5,  c_F=1/100,
acceleration: p_A=15,   c_A=1/20.                            (15)
```

The two margins satisfy

```text
p_A*d4 - (1/20)^2
 = 25 * [p_F*d4 - (1/100)^2].                               (16)
```

With

```text
d4 = 116667666666667 / 10^15,
```

the force margin is exactly

```text
p_F*d4 - 1/10000
 = 349503000000001 / 5000000000000000 > 0,                  (17)
```

and the congruent acceleration-side margin is 25 times (17).

By contrast, the pair

```text
p=3/5,
c=1/20                                                     (18)
```

used as though it were the exact same coordinate system is **not** the congruent pullback of the force theorem.  It may still be a conservative sufficient inequality for the isolated `kc` term, because `|q/100| <= |q/20|`, but it is no longer an equality-level source binding and it overcharges this term by a factor 5 in amplitude / 25 in squared Schur cost.

This distinction matters whenever one reports sharp headroom or constructs a residual identity.

## 5. Correct mixed-coordinate aggregation theorem

Execution terms need not all originate in the same coordinate layer.  For example, a PMI nominal mismatch may first be acceleration-style, while a solve defect from `T-P4-007` is already force-side.

Let

```text
r_F = j (c_A y + e_A) + e_F,                                (19)
```

with

```text
j >= 0,
c_A >= 0,
beta_A >= 0,
beta_F >= 0,
|e_A| <= beta_A |y|,
|e_F| <= beta_F |y|.                                        (20)
```

Then triangle inequality gives

```text
|r_F|
 <= [j(c_A+beta_A)+beta_F] |y|.                             (21)
```

The coefficient in (21) is sharp under only the independent information (20): choose `y=1`, `e_A=beta_A`, and `e_F=beta_F` with the same sign.

Therefore, after all terms have been transported to force coordinates, the sharp same-coordinate Schur condition is

```text
[j(c_A+beta_A)+beta_F]^2 <= p_F d.                          (22)
```

If a transverse reserve `kappa` from `T-P4-015/016` is also present, the corresponding combined budget is

```text
[j(c_A+beta_A)+beta_F]^2 + d*kappa <= p_F*d.                (23)
```

Equation (23) is the source-facing rule that prevents accidental addition of slopes from incompatible coordinates.

## 6. Quarter-consumer consequences

Suppose the existing **force-side** channel-4 consumer is intentionally kept at the simple total slope cap

```text
a_F <= 1/4.                                                  (24)
```

The exact force `kc` charge is `1/100`, so the remaining force-coordinate headroom is

```text
beta_F,total <= 1/4 - 1/100 = 6/25.                         (25)
```

This is the `T-P4-013` arithmetic, and it remains correct for `l_F`.

If some other mismatch is reported upstream in the same acceleration-style coordinate as `f`, with slope `beta_A`, while additional native force errors have total slope `beta_F`, then (21) yields the mixed budget

```text
(1/5)*(1/20 + beta_A) + beta_F <= 1/4,                      (26)
```

or equivalently

```text
(1/5)*beta_A + beta_F <= 6/25.                              (27)
```

Thus, if **all** remaining same-coordinate mismatch were acceleration-style (`beta_F=0`), the raw-coordinate allowance corresponding to the force quarter theorem would be

```text
beta_A <= 6/5,                                               (28)
```

not `1/5`.

The `1/5` number from `T-P4-017` is the headroom obtained by imposing the numerical quarter cap directly on the raw `1/20` coordinate **without** the congruent transformation.  It is a valid extra-conservative surrogate condition if stated that way, but it is not the exact canonical force-coordinate headroom of (2).

Similarly, the statement “the historical total `1/100` force target is impossible because canonical `kc=1/20`” does not apply to `l_F`: for the `kc` term alone,

```text
|rho_kc,4^F| = (1/100)|q5|,                                 (29)
```

so it exactly saturates that target.  Any impossibility must come from additional adversarial force-side remainder, as already characterized in `T-P4-013`, not from the normalized `kc` term by itself.

## 7. What survives from T-P4-017

This review does **not** invalidate the generic Schur, slice, aggregation, or transverse-reserve mathematics in `T-P4-014/015/016/017`.  Those statements are scale-free.

What needs a coordinate tag is only the concrete source-facing specialization:

- `(q5/20,q4/20)` is the literal PMI `f`-coordinate `kc` vector;
- `(q5/100,q4/200)` is its contribution to the currently defined generalized-force residual `l_F=I_B f_B-M0_BB a_B`;
- a `1/20` Schur specialization with unchanged force-side `p_F=3/5` is a conservative surrogate, not the exact coordinate transport;
- the exact acceleration-side transport uses `p_A=15` for channel 4.

Accordingly, no generic theorem needs to be discarded.  The source contract and concrete corollaries should distinguish `nominal/acceleration-style` from `generalized-force` coordinates.

## 8. Minimal Lean theorem targets

### 8.1 Two-layer `kc` map

```lean
theorem kc_force_normalization
    (q4 q5 : R) :
    ((1/5 : R) * (q5/20), (1/10 : R) * (q4/20))
      = (q5/100, q4/200)
```

This is `ring`/`norm_num` arithmetic.

### 8.2 Division-free scalar congruence

```lean
theorem schur_coordinate_congruence
    (j pF pA d xF xA rF rA y : R)
    (hx : xA = j*xF)
    (hr : rF = j*rA)
    (hp : pF = j^2*pA) :
    pF*xF^2 + 2*xF*rF + d*y^2
      = pA*xA^2 + 2*xA*rA + d*y^2
```

Proof: substitute `hx,hr,hp`; `ring`.

### 8.3 Mixed-coordinate residual envelope

```lean
theorem mixed_normalization_residual_bound
    (j c betaA betaF y eA eF : R)
    (hj : 0 <= j) (hc : 0 <= c)
    (hA : 0 <= betaA) (hF : 0 <= betaF)
    (heA : |eA| <= betaA*|y|)
    (heF : |eF| <= betaF*|y|) :
    |j*(c*y+eA)+eF|
      <= (j*(c+betaA)+betaF)*|y|
```

A companion extremizer theorem with `y=1,eA=betaA,eF=betaF` proves sharpness of the coefficient under independent envelopes.

### 8.4 Channel-4 force corollaries

```lean
theorem channel4_kc_force :
  (1/5 : R)*(1/20) = 1/100

theorem channel4_force_quarter_headroom :
  (1/100 : R) + 6/25 = 1/4

theorem channel4_mixed_quarter_budget
    (betaA betaF : R)
    (h : (1/5)*betaA + betaF <= 6/25) :
    (1/5)*(1/20 + betaA) + betaF <= 1/4
```

A separate exact arithmetic corollary can record `p_A=15` and identity (16).

## 9. Remaining blockers

This result resolves only the normalization/coordinate mathematics.  Still open:

1. source/checker binding of each `T-P4-007` execution remainder to either acceleration-style or force coordinates;
2. interval/Lipschitz bounds for those remainders on the actual covered domain;
3. `T-P4-012` remote `M_BD a_D` mass-metric route;
4. genuine additive bias/slack handling;
5. Float64 and solve semantics;
6. P8 domain/trajectory coverage;
7. independent validation and coordinator integration.

Most importantly, the current source contract should not use the word “force” for the literal `rho_kc^f=(q5/20,q4/20)` unless it simultaneously changes the residual definition away from (2) or carries out the congruent coordinate transformation.  With the currently documented B45-5 residual `l_F=I_B f_B-M0_BB a_B`, equation (5) is the exact `kc` force contribution.

## Status

`pending` mathematical/interface result.  No P4/P8/M4 state, registry, source-authentication, validation, provenance, or admission was changed.  Await formalization, independent validation by 封不觉, and 梁智炜 integration/reconciliation of the competing concrete scale contracts.
