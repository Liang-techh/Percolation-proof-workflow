# T-P4-033 O0/P-NE — human body-3 exact geometry target

**Status:** `CONDITIONAL_BODY3_GEOMETRY_DERIVATION`

Scope is only zero-based body `b2 := (2 : Fin 6)` (human body-3). This is a
symbolic exact target derived from the existing `sourceContract` and
`bodyMass`; it does not consume baseline data, repeat body-1/2 work, audit the
payload, run Lean/Lake, or modify registry state.

## Reused generic seams

The derivation reuses the previously identified generic lemmas for slot
access, `er/et/e3` normalization, cross products, diagonal inertia collapse,
and finite trace-fold reduction. Only the body-3 instances are new here.

Use

```text
q0 := q 0       q1 := q 1       q2 := q 2
er := (cos q0, sin q0, 0)
et := (-sin q0, cos q0, 0)
e3 := (0,0,1)
D  := 1/40
A  := 2/25 + (21/100) sin q1
B  := (21/100) sin q1
C  := (21/100) cos q1.
```

The target is valid for every `q : Fin 6 → ℝ`; `q2` disappears for a structural
reason, not by truncation: step 2 has `a=0`, its translation is along the
existing frame z-axis, and the body-3 Jacobian uses the parent frame before
step 2.

## Exact slot and axis target

Let `o_k` denote the origin at frame slot `k` and `z_k` the recorded parent
axis at slot `k`. The new slot lemmas needed are

```text
L3-SLOT-01:
  o0 = origin(I) = (0,0,0)
  o1 = origin(T0) = (2/25) er + (1/10) e3

L3-SLOT-02:
  o2 = origin(T0*T1)
     = (2/25 + (21/100) sin q1) er
       + (1/10 + (21/100) cos q1) e3

L3-SLOT-03:
  o3 = origin(T0*T1*T2) = o2 + (1/20) et

L3-AXIS-01:
  z0 = e3,
  z1 = et,
  z2 = et.
```

`L3-SLOT-03` is the q2-elimination point: the local translation of `T2` is
`(0,0,1/20)` and `T0*T1` maps its local z-axis to `et`; the q2-dependent
rotation in `T2` does not enter the endpoint translation or the recorded
parent axes.

The frame product proof should expose `Matrix.mul_apply` and finite `Fin 4`
sums, normalize `one_mul`/`mul_one`, and use `mul_assoc` explicitly. No
Float64 or opaque matrix evaluator is part of these targets.

## Exact COM displacements and Jacobian

For body `b2`, `bodyCom` uses `(o2+o3)/2 = o2 + D*et`. The three active joint
displacements are therefore

```text
r0 := com2 - o0 = A er + D et + (1/10 + C) e3
r1 := com2 - o1 = B er + D et + C e3
r2 := com2 - o2 = D et.
```

The exact Jacobian instance is

```text
L3-JAC-01:
  Jv(b2) column 0 = e3 × r0 = A et - D er
  Jv(b2) column 1 = et × r1 = C er - B e3
  Jv(b2) column 2 = et × r2 = 0
  Jv(b2) column j = 0       for j ≥ 3

L3-JAC-02:
  Jw(b2) column 0 = e3
  Jw(b2) column 1 = et
  Jw(b2) column 2 = et
  Jw(b2) column j = 0       for j ≥ 3.
```

The term `D et` in `r1` is killed by `et × et`; it must not be dropped before
the cross-product lemma is applied.

## Exact Gram target

Using the reusable `sin_sq_add_cos_sq q0` identities for `er/et` and the
corresponding q1 identity for `B,C`, the translational Gram matrix on active
columns is

```text
L3-GRAM-v:
  Gv00 = A^2 + D^2
  Gv01 = Gv10 = -D*C = -(21/4000) cos q1
  Gv11 = B^2 + C^2 = 441/10000
  Gv02 = Gv20 = Gv12 = Gv21 = Gv22 = 0.
```

The angular Gram matrix is

```text
L3-GRAM-w:
  Gw = [[1,0,0],
        [0,1,1],
        [0,1,1]].
```

The reusable exact combinations are

```text
sin(q0)^2 + cos(q0)^2 = 1
sin(q1)^2 + cos(q1)^2 = 1
er · et = 0
e3 · er = e3 · et = 0
```

The first q0 identity removes all q0 dependence from the Gram entries; the
second gives `B²+C²=441/10000`.

## Exact body-mass/Fourier target

For body-3 constants `mass=3/5` and `inertiaScalar=7/60`, diagonal inertia
collapse plus `L3-GRAM-v/w` yields the matrix target `T2`:

```text
T2(q,0,0) = 80467/600000 + (63/3125) sin q1
             - (1323/100000) cos(2*q1)

T2(q,0,1) = T2(q,1,0) = -(63/20000) cos q1

T2(q,1,1) = 21469/150000

T2(q,1,2) = T2(q,2,1) = T2(q,2,2) = 7/60

T2(q,i,j) = 0 otherwise.
```

The exact source theorem target is

```text
L3-MASS:
  ∀ q i j, sourceBodyMass q (2 : Fin 6) i j = T2(q,i,j).
```

The only trigonometric polynomial rewrite beyond the unit-circle identity is

```text
sin(q1)^2 = (1 - cos(2*q1))/2,
```

used in `T2(q,0,0)`. The `q1` imaginary `±1` trace atoms combine to
`+(63/3125) sin q1`; the real `±2` atoms combine to
`-(1323/100000) cos(2*q1)`. The real `±1` atoms in `(0,1)` and `(1,0)` combine
to `-(63/20000) cos q1`.

## Trace-fold target

The evaluator target is

```text
L3-TRACE:
  ∀ q i j, bodyTraceEvaluator (2 : Fin 6) q i j = T2(q,i,j).
```

Its finite-fold reduction must establish:

```text
(0,0): frequencies -2,-1,0,1,2 in q1
(0,1),(1,0): frequencies -1,1 in q1
(1,1),(1,2),(2,1),(2,2): zero-frequency constants
all other entries: zero.
```

This is a definitional fold/atom normalization target. It is not a claim that
the generated trace has already been kernel-proved equal to the source.

## Minimal composition and obstruction

The smallest new composition is

```text
L3-MASS ∧ L3-TRACE
  ⇒ h_body_3 : ∀ q i j,
       sourceBodyMass q (2 : Fin 6) i j
         = bodyTraceEvaluator (2 : Fin 6) q i j.
```

The current source definitions are sufficient to state the exact formula, but
the repository does not yet contain proofs of `L3-SLOT-01..03`, `L3-AXIS-01`,
`L3-JAC-01..02`, `L3-GRAM-v/w`, or `L3-TRACE`. Therefore this child remains
conditional and cannot change P-NE source-binding status.
