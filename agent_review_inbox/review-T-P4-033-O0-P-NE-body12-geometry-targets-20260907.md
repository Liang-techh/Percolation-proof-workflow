# T-P4-033 O0/P-NE — body-1/2 exact geometry targets

**Status:** `CONDITIONAL_BODY12_GEOMETRY_DERIVATION`

This is a symbolic derivation target, not a proof receipt. It uses the current
exact `sourceContract`, `bodyMass`, and generated `bodyTraceEvaluator`; it does
not audit the payload and does not use Float64, `L_base`, or registry state.

## Index convention

The existing Lean targets use zero-based `Fin 6` bodies:

```text
b0 := (0 : Fin 6)   -- human body-1
b1 := (1 : Fin 6)   -- human body-2
q0 := q 0
q1 := q 1
```

Define the exact real vectors

```text
e3(x) := (0, 0, 1)
er(x) := (cos x, sin x, 0)
et(x) := (-sin x, cos x, 0)
```

The target is all `q : Fin 6 → ℝ`; no small-cell hypothesis is needed for this
symbolic identity.

## Reusable exact geometry lemmas

These are the smallest useful lemmas before expanding `bodyMass`.

```text
L-INDEX-01
  routeBSourceOrigins q / routeBSourceAxes q at slots 0,1,2 reduce to
  origin(I), origin(T0), origin(T0*T1) and zAxis(I), zAxis(T0).

L-DH-01
  origin(T0) = (2/25) * er(q0) + (1/10) * e3.

L-DH-02
  zAxis(I) = e3,
  zAxis(T0) = et(q0).

L-DH-03
  origin(T0*T1) = origin(T0)
                  + (21/100) * sin(q1) * er(q0)
                  + (21/100) * cos(q1) * e3.

L-TRIG-01
  cos(x)^2 + sin(x)^2 = 1.

L-TRIG-02
  er(x) · er(x) = 1,
  et(x) · et(x) = 1,
  er(x) · et(x) = 0,
  e3 · er(x) = e3 · et(x) = 0.
  These follow from L-TRIG-01 and componentwise `ring`.

L-CROSS-01
  e3 × er(x) = et(x),
  et(x) × er(x) = -e3,
  et(x) × e3 = er(x).

L-INERTIA-01
  For diagonal `routeBInertia b a b = if a=b then κ_b else 0`,
  Σ a b, u_a * routeBInertia b a b * v_b
    = κ_b * Σ a, u_a * v_a.

L-FOLD-01
  `bodyTraceEvaluator b q i j` reduces from the global `foldl` to the finite
  tagged slice for body `b`, with nonmatching body/row/col terms equal to zero.
```

The frame products in `L-DH-03` should be normalized with explicit
`Matrix.mul_apply`, finite `Fin 4` sums, `one_mul`, `mul_one`, and only then
`mul_assoc`; no opaque matrix-normalization premise is intended.

## Human body-1 (`b0 = 0`)

Let `o0=origin(I)` and `o1=origin(T0)`. The exact frame/COM reduction is

```text
o0 = (0,0,0)
o1 = (2/25) er(q0) + (1/10) e3
com0 = (1/2) o1
r0 := com0-o0 = (1/25) er(q0) + (1/20) e3
axis0 = e3
```

Only joint `0` is active. Therefore

```text
Jv(b0) column 0 = e3 × r0 = (1/25) et(q0)
Jv(b0) column j = 0                 for j ≠ 0
Jw(b0) column 0 = e3
Jw(b0) column j = 0                 for j ≠ 0.
```

With `mass(b0)=1` and `inertiaScalar(b0)=1/3`, the exact body-mass target is

```text
T0(q,i,j) :=
  if i=0 ∧ j=0 then 628/1875 else 0

∀ q i j, sourceBodyMass q b0 i j = T0(q,i,j).
```

The only nontrivial scalar normalization is

```text
‖(1/25) et(q0)‖² + (1/3)‖e3‖²
  = 1/625 + 1/3
  = 628/1875,
```

where `L-TRIG-01` discharges `sin(q0)^2+cos(q0)^2=1`.

The matching trace target is

```text
∀ q i j, bodyTraceEvaluator b0 q i j = T0(q,i,j),
```

which requires only `L-FOLD-01`, the one body-1 zero-frequency row, and
`traceAtom` at frequency zero. The source and trace halves compose to the
existing `h_body_1` target.

## Human body-2 (`b1 = 1`)

Set

```text
A := 2/25 + (21/200) sin(q1)
B := (21/200) sin(q1)
C := (21/200) cos(q1).
```

Using `o1=origin(T0)` and `o2=origin(T0*T1)`,

```text
com1-o0 = A er(q0) + (1/10 + C) e3
com1-o1 = B er(q0) + C e3
axis0 = e3
axis1 = et(q0).
```

Only joints `0` and `1` are active. The exact Jacobian target is

```text
Jv(b1) column 0 = e3 × (com1-o0) = A et(q0)
Jv(b1) column 1 = et(q0) × (com1-o1) = C er(q0) - B e3
Jv(b1) column j = 0                         for j ≥ 2

Jw(b1) column 0 = e3
Jw(b1) column 1 = et(q0)
Jw(b1) column j = 0       for j ≥ 2.
```

The Gram eliminations are

```text
Jv0 · Jv1 = 0
‖Jv0‖² = A²
‖Jv1‖² = B²+C² = 441/40000
Jw0 · Jw1 = 0
‖Jw0‖² = ‖Jw1‖² = 1.
```

The identity `B²+C²=441/40000` is the primary reusable
`Real.sin_sq_add_cos_sq q1` combination. The q0 cancellations use the same
identity through `L-TRIG-02`.

With `mass(b1)=4/5` and `inertiaScalar(b1)=1/5`, the exact mass target is

```text
T1(q,0,0) = 20953/100000 + (21/3125) sin(q1)
             - (441/100000) cos(2*q1)
T1(q,1,1) = 10441/50000
T1(q,i,j) = 0                         otherwise.
```

The first line is obtained from

```text
(4/5) A² + 1/5
  = 20953/100000 + (21/3125) sin(q1)
    - (441/100000) cos(2*q1),
```

using `sin(q1)^2=(1-cos(2*q1))/2`; this is a trigonometric double-angle
rewrite, not a numerical fit. The second diagonal entry is

```text
(4/5)(441/40000) + 1/5 = 10441/50000.
```

The matching trace target is

```text
∀ q i j, bodyTraceEvaluator b1 q i j = T1(q,i,j).
```

Its only nonzero trace atoms are the five `(0,0)` rows at frequencies
`-2,-1,0,1,2` in coordinate `q1`, plus the zero-frequency `(1,1)` row.
`L-FOLD-01` and `realFourierAtom`/`traceAtom` sign normalization must show
that the two `±1` imaginary rows combine to `+(21/3125) sin(q1)` and the two
`±2` real rows combine to `-(441/100000) cos(2*q1)`.

## Composition targets

The minimal proof order is:

```text
1. prove L-INDEX-01 and L-DH-01..03;
2. prove L-TRIG-01..02, L-CROSS-01, L-INERTIA-01;
3. prove source body-1 Jacobian/mass target T0;
4. prove body-1 fold/trace target T0;
5. prove source body-2 Jacobian/mass target T1;
6. prove body-2 fold/trace target T1;
7. exact sourceBodyMass_eq_bodyMass + the two compositions yield h_body_1,h_body_2.
```

No claim is made for bodies `2..5` by this child. The remaining bodies cannot
be inferred from body-1/2 geometry.

## Fail-closed boundary

The current repository contains the exact source definitions and the concrete
trace targets, but not the above body-1/2 theorems. In particular,
`h_body_1_source_entry_target`, `h_body_1_trace_entry_target`, and the six
`h_body_i` propositions are targets, not proofs. The generated body trace is
also not a compiled semantic theorem. Therefore this child is not consumable
as P-NE and does not set `source_binding_proven`.
