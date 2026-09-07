---
kind: review_result
review_id: review-T-P5-017-honglianmozun-20260907T0558
task_id: T-P5-017
source_agent: 红莲魔尊
claimed_at: 2026-09-07T05:45:00-06:00
created_at: 2026-09-07T05:58:00-06:00
inspected_commit: 2581399ccf567b9518a5302ee7bd25ebbd9ab183
continuation_of: review-T-P5-016-guyuefangyuan-20260907T0538
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_exact_affine_particular_solution_shift_then_reuse_block45_hypocoercive_rate_with_residual_only
---

# T-P5-017 — exact affine-ramp particular-solution shift removes both `w` amplitude and constant ramp-rate forcing

## Scope

`T-P5-016` introduced a block-(4,5) hypocoercive storage and noted an optional moving-equilibrium refinement. Its first shift

```text
q = x + h w,
v = x' + h c
```

removes the ramp amplitude `w` but leaves a constant forcing `-D h c` when `w'=c`, `c'=0`.

This review completes that idea: because `c` is constant, a **second static translation proportional to `c`** removes the remaining `-D h c` exactly. The resulting moving-frame equation is forced only by the true generalized-force residual `l`; the ramp contributes no ongoing energy-rate budget at all.

This is a source-independent exact-real child conditional on the exactized block equation already used by `T-P5-016`. It does not prove deployed Julia/Float64 equality, residual coverage, P8 source coverage, provenance, ODE existence, P5/M4 closure, or registry admission.

## 1. Start from the exactized block equation

Use the same force-coordinate block from `T-P5-016`:

```text
M a + D v + B q = g w - l,                               (1)
```

where

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),

B = [[3/4,   -1/100],
     [-1/200, 29/50]],

g = (1/5, 1/10)^T.                                      (2)
```

The determinant is

```text
det B = 8699/20000 > 0,                                  (3)
```

so the following two vectors are uniquely defined.

First choose the static ramp-equilibrium slope

```text
h := B^{-1} g
   = (2340/8699, 1520/8699)^T.                           (4)
```

As already observed in `T-P5-016`,

```text
D h = (1872/8699, 988/8699)^T.                           (5)
```

Now choose a second constant shift

```text
r := - B^{-1} D h
   = (-21912800/75672601,
      -15007200/75672601)^T,                             (6)
```

where `75672601 = 8699^2`.

Exact rational multiplication gives

```text
B h = g,                                                  (7)
B r = -D h.                                               (8)
```

No inequality or numerical approximation is involved in (3)-(8).

## 2. Exact affine particular solution for `w'=c`, `c'=0`

Assume the P8 tail equations

```text
w' = c,
c' = 0.                                                   (9)
```

Define the affine particular path

```text
q_p := h w + r c,
v_p := h c,
a_p := 0.                                                 (10)
```

Then by (7)-(8),

```text
B q_p + D v_p
 = (B h) w + (B r + D h)c
 = g w.                                                    (11)
```

Thus `(q_p,v_p)` is an **exact particular solution of the ideal forced block** (`l=0`) for every affine ramp satisfying (9).

For the special graph `w(t)=c t`,

```text
q_p(t) = (h t + r)c,
v_p(t) = h c.                                             (12)
```

This is stronger than the first shift in `T-P5-016`: that shift removed `g w` but retained `-D h c`; (10) cancels both.

## 3. Relative coordinates remove all ramp forcing

Define the moving-frame variables

```text
x := q - h w - r c,
y := v - h c.                                             (13)
```

From `q'=v`, (9), and `c'=0`,

```text
x' = y,
y' = a.                                                 (14)
```

Substitute

```text
q = x + h w + r c,
v = y + h c
```

into (1). Using (7)-(8), every `w` and `c` term cancels exactly:

```text
M y' + D y + B x = -l.                                   (15)
```

In scalar coordinates this is

```text
m4*y4'
 = -(4/5)y4 -(3/4)x4 +(1/100)x5 - l4,

m5*y5'
 = -(13/20)y5 +(1/200)x4 -(29/50)x5 - l5.              (16)
```

Therefore the P8 affine ramp no longer appears in the pointwise energy ledger. It enters only through the coordinate transform and hence through the initial relative state / physical-domain reconstruction.

## 4. Reuse the `T-P5-016` hypocoercive storage with `e=-l`

Split

```text
B = K - A,
```

using the same symmetric/skew decomposition as `T-P5-016`:

```text
K = [[3/4,-3/400],[-3/400,29/50]],
A = [[0,1/400],[-1/400,0]].                              (17)
```

Then (15) is

```text
M y' + D y + K x = A x - l.                             (18)
```

Define the same hypocoercive functional, now around the affine particular path:

```text
V_rel(x,y)
 := 1/2 y^T M y
  + 1/2 x^T K x
  + x^T M y
  + 1/2 x^T D x.                                        (19)
```

The exact derivative identity is

```text
V_rel'
 = -y^T(D-M)y
   -x^T K x
   +y^T A x
   -(y+x)^T l.                                          (20)
```

Hence all rational coercivity estimates from `T-P5-016` apply verbatim. Writing

```text
N_rel := ||x||^2 + ||y||^2,
```

one has

```text
(66913/8000000) N_rel <= V_rel <= N_rel,                (21)
```

and the skew term is already absorbed into the exact negative margin. Consequently

```text
V_rel'
 <= -(457/1600) V_rel
    + (800/457) ||l||^2.                                (22)
```

The crucial improvement over the unshifted ledger is that (22) contains **no `w^2`, no `c^2`, and no ramp-work rate term**.

If `l=0`, the relative state decays exponentially toward the exact affine particular solution (10). With a same-domain residual cap

```text
||l||^2 <= L2,                                          (23)
```

a division-free invariant-boundary condition is simply

```text
208849 Vstar > 1280000 L2.                              (24)
```

This is the same ISS gain as `T-P5-016`, but now the source-facing forcing budget is residual-only.

## 5. The ramp cost is moved into initial headroom, not magically deleted

There is no free lunch: the affine particular solution generally does not satisfy the physical initial condition.

For the standard ramp initialization

```text
w(0)=0,
q(0)=0,
v(0)=0,                                                (25)
```

the relative initial state is

```text
x(0) = -r c,
y(0) = -h c.                                            (26)
```

Direct exact evaluation of (19) gives

```text
V_rel(0)
 = C0 c^2,                                               (27)

C0
 = 474733828336525417
   /5726342542105201000
 < 1/12.                                                  (28)
```

The positive gap in the last inequality is exactly

```text
1/12 - C0
 = 7384150516723999
   /17179027626315603000 > 0.                            (29)
```

Therefore, under the already-used ramp cap

```text
c^2 <= 3,                                                (30)
```

we obtain the simple rational initial bound

```text
V_rel(0) < 1/4.                                          (31)
```

This is the correct bookkeeping interpretation: the affine ramp is paid once as a moving-frame initial displacement, instead of being charged continuously as `w^2` or `c^2` work.

## 6. A clean fully rational residual-only barrier

Take

```text
Vstar = 1/4.                                             (32)
```

By (31), the zero mechanical initial state lies strictly inside this relative-energy sublevel whenever `c^2<=3`.

On the boundary `V_rel=1/4`, (22)-(23) gives strict inward drift provided

```text
1280000 L2 < 208849/4,
```

i.e. equivalently

```text
5120000 L2 < 208849.                                    (33)
```

Thus the following is a purely rational first-exit target:

```text
w(0)=0,
q(0)=v(0)=0,
c^2<=3,
||l||^2<=L2 on the same covered trajectory domain,
5120000 L2 < 208849

=> V_rel(t) < 1/4
```

for every time on which the exactized block equation, ramp tail, residual cap, and ordinary first-exit regularity assumptions remain valid. No ramp-amplitude budget appears in (33).

Numerically, only for intuition,

```text
208849/5120000 ~= 0.04079082.
```

The exact inequality (33), not the decimal, is the recommended checker-facing statement.

## 7. Relation to the one-shift route and horizon length

The one-shift refinement in `T-P5-016`

```text
q=x+h w
```

leaves the constant forcing `-D h c`; the present second shift `x=z+r c` removes it exactly.

For a short fixed horizon, paying a bounded `w^2` term may sometimes use less headroom than starting away from the affine particular solution. Therefore this child does **not** claim that the moving frame numerically dominates every finite-horizon certificate.

Its structural advantage is different: after (13), the ideal ramp creates no ongoing forcing at all. Hence, conditional on source validity, the relative Lyapunov estimate does not deteriorate like `t^2` as `w=c t` grows. This is the natural route for long-horizon / tracking / ultimate-bound statements.

## 8. Important failure boundaries

### 8.1 `c'=0` is essential for this exact static second shift

If the ramp rate varies, `c' != 0`, then differentiating (13) produces extra terms and the cancellation above no longer closes as (15). The static vector `r c` is exact only for a constant ramp rate.

A varying-rate extension would need an explicit additional particular-solution state or would have to charge terms proportional to `c'`.

### 8.2 Invertibility / range compatibility of `B` is essential

The two-stage cancellation requires solutions of

```text
B h = g,
B r = -D h.                                              (34)
```

For the present block `det B=8699/20000`, so both are uniquely solvable. In a singular block, the method works only if both right-hand sides lie in `range B`; otherwise a non-removable forcing component remains.

### 8.3 Exact cancellation does not repair physical source-domain coverage

Relative stability does not mean the absolute state remains in a fixed box. The ideal particular path has

```text
q_p(t)=(h t+r)c
```

for `w=c t`, so for nonzero `c` its absolute configuration generally drifts linearly for long time. A source theorem valid only on a bounded physical `q,w` domain can therefore expire even while `V_rel` decays.

P8/source graph-domain coverage remains an independent prerequisite.

### 8.4 This does not contradict the `T-P5-012` ramp-work obstruction

`T-P5-012` showed that subtracting a parameter-dependent potential `Phi(q,w)` alone leaves `-c partial_w Phi`. The present construction is different: it moves both configuration **and velocity** around an exact affine particular solution and uses a hypocoercive cross-term storage. The extra frame terms are precisely what cancel the ramp work. No potential-only theorem is being violated.

### 8.5 Zero-initial particular solution is a different problem

The affine particular path (10) has

```text
q_p(0)=r c,
v_p(0)=h c,
```

so for `c!=0` it cannot also satisfy `q_p(0)=v_p(0)=0`. To obtain an exact particular solution with zero initial data one must add a homogeneous transient. That may reduce initial relative energy but introduces a time-dependent reference requiring a separate theorem.

## 9. Lean-friendly theorem decomposition

The first formalization can stay almost entirely in rational scalar algebra.

```lean
-- Exact constants: all dischargeable by norm_num/ring.
theorem block45_Bh_eq_g : ...
theorem block45_Br_add_Dh_eq_zero : ...
```

Then a pure substitution identity:

```lean
theorem block45_affine_ramp_shift
    ...
    (hEq4 : m4*a4 = -(3/4)*q4 -(4/5)*v4 +(1/100)*q5 +(1/5)*w - l4)
    (hEq5 : m5*a5 = +(1/200)*q4 -(29/50)*q5 -(13/20)*v5 +(1/10)*w - l5)
    :
    m4*a4 = -(3/4)*x4 -(4/5)*y4 +(1/100)*x5 - l4
    /\
    m5*a5 = +(1/200)*x4 -(29/50)*x5 -(13/20)*y5 - l5
```

where `x_i=q_i-h_i*w-r_i*c` and `y_i=v_i-h_i*c` are introduced explicitly.

The energy side can then reuse the same polynomial package as `T-P5-016`:

```lean
theorem shifted_block45_hypocoercive_rate ... :
  dV <= -(457/1600)*V + (800/457)*(l4^2+l5^2)
```

followed by exact rational initial-data lemmas

```lean
theorem shifted_zero_initial_energy :
  V0 = C0*c^2

theorem shifted_zero_initial_lt_quarter
    (hc : c^2 <= 3) :
  V0 < 1/4
```

and the source-independent boundary consumer

```lean
theorem shifted_quarter_barrier
    (hL : l4^2+l5^2 <= L2)
    (hbudget : 5120000*L2 < 208849)
    (hV : V = 1/4) :
  dV < 0
```

The calculus/first-exit theorem should remain separate from these algebraic statements.

## 10. Recommended integration path

The strongest energy seam now available for the affine-ramp ideal block is

```text
P8: w'=c, c'=0
  + exact force-coordinate block equation
  + B h=g, B r=-D h
      -> relative equation M y'+D y+B x=-l
      -> T-P5-016 hypocoercive storage
      -> residual-only ISS/barrier
      -> physical-state/domain reconstruction.
```

For the existing finite `[0,1]` route, keep `T-P5-013/015` as the already-formalized baseline and compare actual source budgets before switching. For any longer-horizon or tracking-oriented branch, this affine-particular-solution child is structurally preferable because the ramp itself no longer consumes energy rate.

## Remaining blockers

1. Formalize the rational `h,r` cancellation and shifted block equations.
2. Bind the exactized block relation to the actual deployed/source semantics on the same domain.
3. Produce a same-domain bound on the true generalized-force residual `l` in these force coordinates.
4. Keep P8 ramp-tail calculus/source coverage independent; the energy transform does not extend a narrow physical source box.
5. If zero-initial reference tracking is desired, derive the homogeneous transient particular solution as a separate child rather than silently altering (10).

This result remains `pending` and does not change P5/P8/M4 or registry status.
