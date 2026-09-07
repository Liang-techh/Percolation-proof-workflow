---
kind: review_result
review_id: review-T-P5-030-honglianmozun-20260907T1205
task_id: T-P5-030
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T11:56:00-06:00
created_at: 2026-09-07T12:05:00-06:00
inspected_commit: f08cd54cf56d8f375b7d176267617ffa209214f6
continuation_of:
  - review-T-P5-017-honglianmozun-20260907T0558
  - review-T-P5-019-honglianmozun-20260907T0702
related_reviews:
  - companion-T-P5-017-honglianmozun-20260907T1640
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_incremental_moving_frame_parameter_tube_then_bind_only_if_source_supplies_incremental_residual_envelope
---

# T-P5-030 — moving-frame incremental contraction gives a rational ramp-parameter cell tube

## 0. Result in one sentence

The affine moving frame of `T-P5-017` has a stronger consequence than single-trajectory stability: for two trajectories with constant ramp rates `c1,c2`, subtracting each trajectory's **own** exact affine particular solution removes the ramp parameter from the difference equation completely. The only inputs left are the initial mismatch proportional to `dc := c1-c2` and the true residual difference `Dl := l1-l2`.

Combining that exact cancellation with the direct residual metric of `T-P5-019` gives a checker-friendly incremental tube. If the source can prove on the same domain

```text
||Dl||^2 <= mu * Vd + nu * dc^2,
mu >= 0, nu >= 0,
11424*mu + 137088*nu < 2285,
```

then the rational tube

```text
Vd < dc^2 / 12
```

is invariant under the usual first-exit hypotheses for `dc != 0`, because the standard equal-physical-state initialization already satisfies the strict initial bound. This turns a `c`-cell width into explicit pairwise `q/v/w` diameter bounds without charging the absolute ramp amplitude.

This is mathematics only. It does not create the incremental residual envelope, source/Float64 semantics, ODE continuation, flowpipe coverage, or parent admission.

## 1. Two exactized block trajectories

For `i=1,2`, use the same exact force-coordinate block equation as `T-P5-017`:

```text
M vi' + D vi + Bphys qi = g wi - li,                     (1)
qi' = vi,
wi' = ci,
ci' = 0.                                                  (2)
```

The exact constants are

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),

Bphys = [[3/4,   -1/100],
         [-1/200, 29/50]],

g = (1/5,1/10)^T.
```

As in `T-P5-017`, define

```text
h = (2340/8699, 1520/8699)^T,

r = (-21912800/75672601,
     -15007200/75672601)^T,
```

so that exactly

```text
Bphys h = g,
Bphys r = -D h.                                          (3)
```

For each trajectory introduce its own moving frame

```text
xi := qi - h wi - r ci,
yi := vi - h ci.                                         (4)
```

Then `(1)-(3)` give

```text
xi' = yi,
M yi' + D yi + Bphys xi = -li.                           (5)
```

The important point is that **no `ci` appears in (5)**.

## 2. Exact difference equation: the ramp parameter disappears

Set

```text
X := x1-x2,
Y := y1-y2,
Dl := l1-l2,
dc := c1-c2.                                             (6)
```

Subtracting (5) gives the exact incremental system

```text
X' = Y,
M Y' + D Y + Bphys X = -Dl.                              (7)
```

Thus the ideal affine-ramp family is conjugate, by the parameter-dependent translation (4), to one common autonomous block. In particular, there is no forcing term proportional to `dc`, `t*dc`, `c1`, or `c2` in the relative equation itself.

This distinction matters. If one instead compares both physical trajectories in a single frame built at a fixed nominal `c0`, a deterministic term `g(c-c0)t` appears. Using each trajectory's own exact particular solution is the coordinate choice that exposes the true incremental cancellation.

## 3. Reuse the T-P5-019 hypocoercive difference energy

Write

```text
Bphys = K - A,

K = [[3/4,-3/400],[-3/400,29/50]],
A = [[0,1/400],[-1/400,0]].                              (8)
```

Apply the same storage as `T-P5-017/019` to `(X,Y)`:

```text
Vd(X,Y)
 := 1/2 Y^T M Y
  + 1/2 X^T K X
  + X^T M Y
  + 1/2 X^T D X.                                        (9)
```

`T-P5-019` proves, for any residual entering exactly as in (7),

```text
Vd' <= -(457/1344) Vd + (17/10) ||Dl||^2.               (10)
```

Therefore the two-trajectory problem needs no new dissipation calculation. It only needs an **incremental** source bound for `Dl`.

## 4. Exact initial parameter-mismatch energy

Assume the standard equal physical initialization

```text
q1(0)=q2(0)=0,
v1(0)=v2(0)=0,
w1(0)=w2(0)=0.                                          (11)
```

Then from (4),

```text
X(0) = -r dc,
Y(0) = -h dc.                                            (12)
```

Because (9) is homogeneous quadratic,

```text
Vd(0) = C0 * dc^2,                                       (13)
```

with exactly the same constant computed in `T-P5-017`:

```text
C0 = 474733828336525417
     /5726342542105201000
   < 1/12.                                                (14)
```

Hence

```text
Vd(0) < dc^2/12                                          (15)
```

for every `dc != 0`; for `dc=0`, the initial difference energy is exactly zero.

The ramp-parameter width is therefore paid once as a quadratic initial displacement in the common moving-frame dynamics.

## 5. Incremental residual envelope and exact rational parameter tube

An absolute residual cap such as `||li||^2 <= L2` is not the right object for a shrinking parameter-cell diameter: it generally leaves a nonzero forcing price as `dc -> 0`.

The natural source-facing incremental contract is instead

```text
||Dl||^2 <= mu * Vd + nu * dc^2,                        (16)
mu >= 0,
nu >= 0.                                                  (17)
```

Here `mu` charges the state-dependent residual variation and `nu` charges direct ramp-parameter variation. Their physical units are whatever is required by the already normalized force-coordinate block; the theorem does not silently identify raw source forces with `Dl`.

Substituting (16) into (10) gives

```text
Vd'
 <= -[(457/1344) - (17/10)mu] Vd
    + (17/10) nu dc^2.                                  (18)
```

For a generic tube

```text
Vd = Kc * dc^2,
```

the boundary derivative is strictly negative for `dc != 0` whenever

```text
11424*mu < 2285,                                         (19)
(2285 - 11424*mu) * Kc > 11424*nu.                      (20)
```

These are exactly (18) after clearing denominators; no exponential, square root, or floating constant is needed.

### Clean specialization `Kc = 1/12`

Because the exact initial coefficient already satisfies `C0<1/12`, take

```text
Kc = 1/12.                                               (21)
```

Then (19)-(20) collapse to the single sufficient condition

```text
11424*mu + 137088*nu < 2285.                             (22)
```

Indeed, with `mu,nu>=0`, (22) automatically implies (19), and on
`Vd=dc^2/12`, (18) becomes strictly negative for every nonzero `dc`.

Consequently, under ordinary continuity/first-exit assumptions and while (1)-(2) plus (16) remain valid on the covered domain,

```text
Vd(t) < dc^2/12                                          (23)
```

throughout the interval for every pair with `dc != 0` and equal physical initial data (11).

For the ideal residual-free block, simply set

```text
mu=0, nu=0.
```

Then (22) is automatic and (23) is an immediate incremental contraction tube.

## 6. Failure boundary: an absolute residual cap cannot yield a vanishing parameter diameter

The scaling in (16) is not cosmetic.

Suppose all that is known is

```text
||Dl||^2 <= Lconst
```

with some fixed positive `Lconst`, independent of `dc` and `Vd`. Then (10) only gives an ultimate energy of order `Lconst`, not order `dc^2`. As `dc -> 0`, no uniform estimate of the form

```text
Vd <= Kc * dc^2
```

can follow from that information alone.

The zero-width slice makes the obstruction explicit. At `dc=0`, a model that permits `X=Y=0` but also permits a nonzero independent `Dl` does not define a shrinking parameter family at all: the residual channel can separate two otherwise identical trajectories. Therefore a source-side parameter-cell contraction certificate must prove that the **difference residual vanishes with the difference state/parameter**, e.g. through (16), a componentwise Lipschitz equivalent, or a stronger exact cancellation.

This does not invalidate the absolute residual gates from `T-P5-019/024`; those are appropriate for one-trajectory invariant-energy barriers. It only says they are insufficient for a pairwise cell-diameter theorem.

## 7. Transport the relative tube back to physical pairwise diameters

Under the ramp graph `wi(t)=ci t`, the physical differences are

```text
q1-q2 = X + dc (h t+r),
v1-v2 = Y + h dc,
w1-w2 = t dc.                                            (24)
```

The sharp coordinate support constants already derived in the `T-P5-017` companion are

```text
X4^2 <= alpha4 Vd,
X5^2 <= alpha5 Vd,
Y4^2 <= beta4 Vd,
Y5^2 <= beta5 Vd,                                       (25)
```

where

```text
alpha4 = 9438522000000 / 6764044380739,
alpha5 = 34399976000000 / 20292133142217,

beta4 = 43887777300000000000 / 2367435825391792217,
beta5 = 56414160640000000000 / 1357807504945166121.     (26)
```

Combining (23)-(26) yields a direct parameter-cell diameter seam.

For any horizon `0<=t<=T`, define

```text
Ai(T) := max(|ri|, |hi*T+ri|).                           (27)
```

If a parameter cell gives the pairwise bound

```text
dc^2 <= Delta2,                                          (28)
```

then the relative and deterministic square budgets are

```text
Xqi = alpha_i * Delta2 / 12,
Yqi = Ai(T)^2 * Delta2,

Xvi = beta_i * Delta2 / 12,
Yvi = hi^2 * Delta2.                                     (29)
```

The square-root-free two-term envelope from the previous `T-P5-017` companion can therefore certify any desired physical pairwise squared diameter `Dqi` by

```text
Dqi - Xqi - Yqi > 0,
4*Xqi*Yqi < (Dqi-Xqi-Yqi)^2,                             (30)
```

and similarly for velocity with `(Xvi,Yvi,Dvi)`.

For the ramp coordinate itself,

```text
(w1-w2)^2 <= T^2 * Delta2.                               (31)
```

Equations (29)-(31) are pairwise **diameter** bounds. They do not prove that the absolute cell center is inside a source box; that center/coverage problem remains separate.

## 8. Very small rational `T=1` diameter corollary

For `T=1`, the affine-center maxima are the same endpoint values already checked in the prior companion:

```text
A4(1)=|r4|,
A5(1)=|r5|.                                              (32)
```

If the tube (23) holds, the elementary bound `(a+b)^2 <= 2a^2+2b^2` gives a deliberately simple rational consumer:

```text
(q1_4-q2_4)^2 < (401/1000) dc^2,
(q1_5-q2_5)^2 < (181/500)  dc^2,

(v1_4-v2_4)^2 < (13/4) dc^2,
(v1_5-v2_5)^2 < 7 dc^2,

(w1-w2)^2 <= dc^2.                                      (33)
```

The four strict coefficient checks are exact-rational consequences of (25), `Vd<dc^2/12`, and the values of `h,r`; the decimals are not needed in the trusted statement.

Thus a checker that partitions `c` into cells can convert a pairwise `dc^2` budget directly into conservative physical `q/v/w` diameters using only rational multiplication. If the cell is represented by a center and half-width `delta`, then pairwise `dc^2<=4 delta^2`; (33) can be consumed after that substitution.

The discriminant criterion (30) remains the sharper route when the actual source-box slack is tight; (33) is the smaller formal interface.

## 9. What this does and does not solve for P8/source coverage

This result helps with **parameter-cell width propagation**, not absolute source coverage.

It can support a split-domain workflow of the form

```text
c-cell width
 -> incremental residual envelope (16)
 -> moving-frame tube (23)
 -> q/v/w pairwise cell diameter (29)-(33)
 -> combine with independently certified cell center trajectory/domain.
```

It does not repair the earlier whole-family obstruction for a fixed tiny `w` box. Even if every cell has small diameter, the absolute center still follows `w_center(t)=c_center*t`. A source domain with `|w|<=0.01` cannot cover a cell whose center has already left that interval merely because the cell diameter is small.

Likewise, no source-side `mu,nu` are provided here. If the deployed residual includes Float64/solve/controller artifacts whose difference does not satisfy (16), the parameter contraction theorem remains conditional.

## 10. Lean-friendly theorem decomposition

The new math can be formalized without ODE or matrix APIs.

Recommended atomic statements:

```text
moving_frame_two_parameter_difference
```

Input: two scalar-coordinate copies of the exact block equations plus `Bphys*h=g` and `Bphys*r=-D*h`.
Output: the two equations in (7). Pure `ring`/`linarith` substitution.

```text
block45_parameter_difference_initial_energy
```

Input: `X0=-r*dc`, `Y0=-h*dc`.
Output: `Vd0=C0*dc^2` and `C0<1/12`. Exact `norm_num`/`ring_nf`.

```text
incremental_residual_parameter_ledger
```

Input:

```text
dV <= -(457/1344)V + (17/10)L2,
L2 <= mu*V + nu*dc2.
```

Output (18). Pure linear arithmetic.

```text
parameter_twelfth_tube_boundary
```

Input:

```text
mu>=0, nu>=0,
dc2>0,
11424*mu + 137088*nu < 2285,
V=dc2/12,
```

plus the previous ledger.
Output: `dV<0`.

```text
block45_parameter_diameter_T1
```

Input: `Vd<=dc2/12` plus coordinate-support hypotheses.
Output the five squared bounds (33). The coefficient checks are exact rational arithmetic.

The first-exit/calculus wrapper should remain separate. No theorem in this child needs to assert ODE existence, uniqueness, or flowpipe inclusion.

## 11. Dependencies and remaining open items

Consumes only:

- exact moving-frame constants/identities from `T-P5-017`;
- the direct incremental residual ledger from `T-P5-019`;
- the sharp coordinate support constants from the existing `T-P5-017` companion;
- the abstract ramp graph `w=ct` when transporting back to physical coordinates.

Still open:

- a source-derived incremental residual envelope `(16)` with typed force coordinates;
- Float64 `dM/cijk/accumulation`, solve, controller, and reference-difference semantics;
- the nominal/center cell trajectory and absolute source-domain inclusion;
- ODE existence/continuation and interval flowpipe coverage;
- P5/P8/M4 closure, provenance/admission, registry integration.

The immediate source-side question is now precise: instead of only reporting an absolute `||l||^2` cap, determine whether the deployed residual map admits a same-domain difference bound of the form

```text
||l(z1,c1)-l(z2,c2)||^2 <= mu*Vd(z1,z2) + nu*(c1-c2)^2.
```

If it does, the single rational gate `(22)` decides whether the convenient `1/12` parameter tube closes.

Current status: `pending mathematical child`; 待封不觉独立验证 / 待梁智炜最终整合。
