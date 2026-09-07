---
kind: review_result
task_id: T-P5-027
source_agent: codex-local
created_at: 2026-09-07
integration_status: pending
admission_label: pending
proposed_integration_target: theorem-sidecar
---

# T-P5-027 — near-sharp exact rational scalar fallback

## Result

Added a disjoint, source-independent sidecar containing the minimum algebraic
chain requested by the P5-027 review:

1. weighted AM-GM for `alpha = 75/106`;
2. the four exact leading principal minors of
   `H = c P - alpha R - alpha⁻¹ I` and their positivity;
3. an exact LDL identity for the same weighted gap;
4. the division-free joint bound and its generic scalar residual consumer;
5. the exact lower witness at `(2379,73046,1832,68229)`.

The new files are:

- `examples/routeb_p5_scalar_fallback/NEW_P5_027_near_sharp_scalar_fallback.lean`
- `examples/routeb_p5_scalar_fallback/NEW_check_exact.py`
- `examples/routeb_p5_scalar_fallback/NEW_P5_027_REVIEW.md`

No other file was changed.

## Exact claims formalized

With the P5-024 block-(4,5) quadratic `Q`,

```text
U = (x4+y4)^2 + (x5+y5)^2,
N = x4^2+x5^2+y4^2+y5^2,
alpha = 75/106,
c = 47984317/10000000,
```

the sidecar records the exact Sylvester data

```text
D1 = 9399719209/6360000000,
D2 = 395359846106875447280719 /
     404496000000000000000000,
D3 = 359556829343316384950230880641180953 /
     449440000000000000000000000000000000,
D4 = 1337085894390964667090754208081695830761861 /
     17977600000000000000000000000000000000000000000000.
```

All four are strictly positive.  The accompanying exact LDL identity proves
the weighted comparison

```text
(75/106) U + (106/75) N <= (47984317/10000000) Q.
```

Weighted AM-GM then gives the division-free bound

```text
400000000000000 U N <= 2302494677956489 Q^2.
```

The generic residual consumer is kept abstract: from
`coupling^2 <= U*rcSq`, `rcSq <= ell2*N`, and

```text
2302494677956489*ell2 <= 400000000000000*mu^2
```

it concludes `|coupling| <= mu*Q` under the explicit nonnegativity premises.

The lower witness proves the exact cross-multiplication obstruction

```text
U*N/Q^2 > 11512473/2000000.
```

Thus the scalar constant is bracketed by the stated rational lower witness and
the new upper constant, without any numerical optimization claim.

## Arithmetic correction recorded

The P5-027 inbox review's displayed exact difference in its Section 3,
equation (15), has a numerator typo.  Exact arithmetic gives

```text
144/25 - 2302494677956489/400000000000000
  = 1505322043511/400000000000000,
```

not `150503411/400000000000000`.  The new Lean arithmetic theorem and the
independent checker use the corrected value.  The new constant, the width
`77956489/400000000000000`, and the lower-witness cross product agree with the
P5-027 review.

## Independent checker evidence

Command run:

```text
python examples/routeb_p5_scalar_fallback/NEW_check_exact.py
```

Observed result:

```text
P5_027_EXACT_RATIONAL_CHECK=PASS
SYLVESTER_PRINCIPAL_MINORS=PASS
LDL_MATRIX_IDENTITY=PASS
DIVISION_FREE_CONSTANT=2302494677956489/400000000000000
LOWER_WITNESS_THRESHOLD=11512473/2000000
SOURCE_BINDING=OPEN
P8_COVERAGE_AND_CLOSURE=OPEN
```

The checker uses exact `Fraction` arithmetic.  It verifies the weighted-gap
matrix construction from `P`, `R`, and `I`, all leading minors, the universal
matrix identity `H = L D Lᵀ`, the exact constant arithmetic, and the witness.
It does not replace a kernel proof.

## Lean/environment status

Although `lean.exe`/`lake.exe` names are visible on PATH, no usable pinned
local Mathlib/Lake environment was established for this task, and compilation
was deliberately not attempted.  Consequently the `.lean` file is an
uncompiled candidate only:

```text
LEAN_COMPILE=NOT_RUN
LEAN_VERIFIED=false
ADMISSION_LABEL=pending
```

The `#print axioms` lines are included for a future pinned-environment run;
they are not a compile receipt.

## DAG and admission boundary

The local Route-B DAG was read at revision `596` with `122` nodes.  The
relevant physical nodes, including `P5.sparse_disjunctive_sos`, remain open;
the P8 reachability branch is also open.  This sidecar is an independent
abstract leaf and was not inserted into that DAG.

It does not provide or imply:

- a concrete `K_path` or `ell2_path` source bound;
- source/Jacobian, DH, Float64, solve-bias, anchor-bias, or IEEE binding;
- a P8 cell chain, domain coverage, flowpipe, or terminal transfer;
- P5/P8/M4 closure, provenance admission, registry promotion, or `VERIFIED`.

The correct downstream interpretation is therefore a pending mathematical
child that can be consumed by a later explicitly bound scalar checker.  If a
concrete scalar checker proposes a universal constant at or below
`11512473/2000000`, the displayed rational witness is an exact rejection.
