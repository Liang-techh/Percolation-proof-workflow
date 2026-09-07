# Companion result — moving-frame energy to absolute source-box transport

- task_id: `T-P5-017`
- parent_review: `review-T-P5-017-honglianmozun-20260907T0558.md`
- agent: `红莲魔尊`
- source_agent: `红莲魔尊`
- role: math / Lyapunov / energy-interface bridge
- status: `pending`
- integration_status: `待封不觉独立验证 / 待梁智炜最终整合`

This is a continuation of my own `T-P5-017` moving-frame result, not a new task claim. It does not touch the active `T-P5-024/025/026` leases.

## 1. Goal

`T-P5-017` proves a useful relative-coordinate energy estimate after the affine ramp is removed, but P8/source certificates are stated on the **absolute** source coordinates `(q,v,w)`. A relative Lyapunov barrier is therefore not, by itself, a source-domain coverage theorem.

The missing bridge is a sharp algebraic transport:

> relative energy bound + ramp parameter bound -> explicit absolute `(q,v,w)` box bound.

For block `(4,5)` the moving frame is

```text
x = q - h w - r c,
y = v - h c,
w(t) = c t,
```

with

```text
h4 = 2340/8699,
h5 = 1520/8699,
r4 = -21912800/75672601,
r5 = -15007200/75672601.
```

The point of this note is to derive the exact coordinate support constants of the `T-P5-017` Lyapunov ellipsoid and then transport them back to the source coordinates without introducing a coarse global Euclidean coercivity constant.

## 2. Exact decoupled representation of the relative Lyapunov functional

Recall

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
B = [[3/4, -3/400],[-3/400, 29/50]],
```

and

```text
V(x,y)
 = 1/2 y^T M y
 + 1/2 x^T B x
 + x^T M y
 + 1/2 x^T D x.
```

Set

```text
s := x + y,
R := B + D - M.
```

Then by direct expansion,

```text
V(x,y) = 1/2 s^T M s + 1/2 x^T R x.          (2.1)
```

For the present block,

```text
R11 = 4299997/3000000,
R12 = -3/400,
R22 = 4719261/4000000,

det(R) = 6764044380739/4000000000000 > 0.
```

Hence `R` is positive definite. This representation is materially better for source-box transport than the previous uniform bound

```text
(66913/8000000) (||x||^2+||y||^2) <= V,
```

because individual coordinate support functions of the ellipsoid can be computed exactly.

## 3. Sharp coordinate support constants

For a positive-definite quadratic form, the support of one coordinate is given by the corresponding diagonal entry of the inverse form. In dimension two this can be proved by one Schur completion, so no matrix-inverse API is logically necessary.

Define

```text
alpha4 := 2 (R^{-1})44
        = 9438522000000 / 6764044380739,

alpha5 := 2 (R^{-1})55
        = 34399976000000 / 20292133142217.
```

Then

```text
x4^2 <= alpha4 V,
x5^2 <= alpha5 V.                              (3.1)
```

These constants are sharp for the `V`-ellipsoid.

For `y=s-x`, the block diagonal form `(2.1)` gives the exact dual support

```text
beta_i := 2 (M_i^{-1} + (R^{-1})ii).
```

Thus

```text
beta4
 = 43887777300000000000 / 2367435825391792217,

beta5
 = 56414160640000000000 / 1357807504945166121,
```

and

```text
y4^2 <= beta4 V,
y5^2 <= beta5 V.                               (3.2)
```

Numerically, only as orientation,

```text
alpha4 ~ 1.39539623,
alpha5 ~ 1.69523705,
beta4  ~ 18.53810643,
beta5  ~ 41.54798116.
```

The proof of `(3.2)` is not a triangle-inequality estimate. For each coordinate one combines the exact one-dimensional effective stiffness from the Schur complement of `R` with the diagonal kinetic coefficient `M_i`; the weighted Cauchy inequality is attained on the dual direction, so `beta_i` is again the actual ellipsoid support constant.

## 4. Exact affine-center cost on a finite time interval

From the moving frame and `w=ct`,

```text
q_i(t) = x_i(t) + c (h_i t + r_i),
v_i(t) = y_i(t) + c h_i.                       (4.1)
```

For any `0 <= t <= T`, affine convexity gives the exact endpoint bound

```text
|h_i t + r_i|
 <= max(|r_i|, |h_i T + r_i|).                 (4.2)
```

This is sharper than the crude `|h_i|T+|r_i|` bound.

For `T=1` the current rational coefficients satisfy

```text
h4+r4 = -1557140/75672601 < 0,
h5+r5 = -1784720/75672601 < 0,
r4 < 0,
r5 < 0,
h4 > 0,
h5 > 0.
```

Therefore the affine centers stay negative throughout `[0,1]` and their absolute values decrease. Consequently

```text
max_[0,1] |h4 t+r4| = |r4|,
max_[0,1] |h5 t+r5| = |r5|.                   (4.3)
```

No time discretization is needed for this part.

## 5. Square-root-free two-term box criterion

The transport back to the absolute source box can be checked without introducing square roots.

### Lemma: two-term square envelope

Let real `a,b` and nonnegative budgets `X,Y,D` satisfy

```text
a^2 <= X,
b^2 <= Y,
0 < D-X-Y,
4 X Y < (D-X-Y)^2.                            (5.1)
```

Then

```text
(a+b)^2 < D.                                   (5.2)
```

Proof. If `(a+b)^2 >= D`, then

```text
D-X-Y <= 2ab.
```

The left side is strictly positive, hence `ab>0`; squaring gives

```text
(D-X-Y)^2 <= 4 a^2 b^2 <= 4XY,
```

contradicting `(5.1)`. QED.

This is the same discriminant geometry that appeared in `T-P5-021`, but here it is used directly on absolute-coordinate transport. It is exact for the independent two-term envelope and is friendly to `ring_nf`/`nlinarith`: no `Real.sqrt` is required.

## 6. Typed source-box transport theorem

Assume on an interval `0 <= t <= T`:

```text
V(x(t),y(t)) <= Vstar,
c^2 <= C2,
x = q-hw-rc,
y = v-hc,
w = ct.
```

For each position coordinate define

```text
Ai(T) := max(|ri|, |hi T+ri|),
Xqi    := alpha_i Vstar,
Yqi    := C2 Ai(T)^2.
```

For each velocity coordinate define

```text
Xvi := beta_i Vstar,
Yvi := C2 hi^2.
```

Let `Q_i>0`, `V_i>0`, `W>0` be the absolute source-box radii. If

```text
0 < Q_i^2-Xqi-Yqi,
4 Xqi Yqi < (Q_i^2-Xqi-Yqi)^2,                (6.1)

0 < V_i^2-Xvi-Yvi,
4 Xvi Yvi < (V_i^2-Xvi-Yvi)^2,                (6.2)

C2 T^2 < W^2,                                  (6.3)
```

then throughout the interval

```text
q_i(t)^2 < Q_i^2,
v_i(t)^2 < V_i^2,
w(t)^2   < W^2.                                (6.4)
```

For non-strict source-box inclusion, replace the strict inequalities by the corresponding closed inequalities with the usual boundary care.

This theorem is algebraic. It does **not** consume ODE uniqueness, a flowpipe algorithm, or source semantics. Those remain separate layers.

## 7. Current block-(4,5), `T=1`, `c^2<=3`

Using `(4.3)`, the center-square budgets are exactly

```text
Yq4 = 3 r4^2
    = 1440512411520000 / 5726342542105201
    ~ 0.251558897,

Yq5 = 3 r5^2
    = 675648155520000 / 5726342542105201
    ~ 0.117989476,

Yv4 = 3 h4^2
    = 16426800 / 75672601
    ~ 0.217077248,

Yv5 = 3 h5^2
    = 6931200 / 75672601
    ~ 0.091594579.
```

At the convenient relative barrier `Vstar=1/4`, the relative-coordinate square budgets are

```text
Xq4 = alpha4/4
    = 2359630500000 / 6764044380739
    ~ 0.348849056,

Xq5 = alpha5/4
    = 8599994000000 / 20292133142217
    ~ 0.423809263,

Xv4 = beta4/4
    = 10971944325000000000 / 2367435825391792217
    ~ 4.634526608,

Xv5 = beta5/4
    = 14103540160000000000 / 1357807504945166121
    ~ 10.386995291.
```

For intuition only, the resulting sufficient absolute radii are approximately

```text
|q4| < 1.09220,
|q5| < 0.99451,
|v4| < 2.61872,
|v5| < 3.52554,
```

when one separately saturates the relative ellipsoid and the allowed ramp amplitude. These are safe envelope values, not claims that a single physical trajectory simultaneously realizes all extremizers.

## 8. Exact independent obstruction from the ramp coordinate

The `w` condition is qualitatively different from the `q/v` envelopes. Because `w=ct` exactly, source coverage of the whole allowed ramp family on `[0,T]` necessarily requires

```text
C2 T^2 <= W^2.                                 (8.1)
```

Thus for the current family `c^2<=3` on `[0,1]`, any absolute source box with `|w|<=0.01` is mathematically incapable of covering the whole ramp family:

```text
3 > 0.0001.
```

This failure is independent of how small the relative Lyapunov energy is. A moving-frame energy proof cannot repair an undersized absolute `w` source domain; the P8 source box must be widened, parameter-sliced, or the admissible `c/T` family must be reduced.

The `q/v` discriminant tests `(6.1)-(6.2)` are sufficient for the decoupled envelope. They are not asserted to be necessary for actual coupled trajectories, because trajectory dynamics may correlate the signs and extremizers of the relative state and ramp center. In contrast, `(8.1)` is a genuinely necessary condition for whole-family `w=ct` coverage.

## 9. Minimal Lean theorem decomposition

Recommended source-independent formalization targets:

1. `relative_energy_as_decoupled_square`
   - prove `(2.1)` by `ring` after substituting `R=B+D-M`;
2. `block45_relative_x_coordinate_support`
   - two Schur-completion lemmas specialized to the rational `R` above;
3. `block45_relative_y_coordinate_support`
   - combine the effective `R` coordinate stiffness with diagonal `M` by weighted Cauchy;
4. `affine_interval_abs_max`
   - `0<=t<=T -> |h*t+r| <= max |r| |(h*T+r)|`;
5. `two_term_square_envelope`
   - statement `(5.1)->(5.2)`; intended proof is positivity plus `nlinarith` and one product monotonicity step;
6. `moving_frame_source_box_transport_block45`
   - consume the preceding algebraic leaves plus typed `w=ct`, `c^2<=C2`, `V<=Vstar`.

The rational constants should stay exact in the theorem statements. Decimal values above are commentary only.

## 10. Dependencies and remaining open boundaries

Consumes:

- the exact moving-frame identities and rational `h,r` from `T-P5-017`;
- a relative barrier `V<=Vstar` from `T-P5-017/019/021` or any stronger later P5 lane;
- the P8 ramp identity `w=ct` when the theorem is used on a source trajectory.

Does not prove:

- that the deployed Julia source is semantically identical to the mathematical first-12 vector field;
- Float64/runtime residual bounds;
- cell/flowpipe coverage;
- ODE existence/continuation;
- that any current absolute `q/v` source box satisfies `(6.1)-(6.2)`;
- P5, P8, or M4 closure/admission.

The practical next consumer is a source-domain checker: given the actual per-coordinate source-box radii, evaluate `(6.1)-(6.3)` exactly. If the `w` radius remains `0.01` for the full `c^2<=3, T=1` family, no further energy tightening can close that particular coverage gap.
