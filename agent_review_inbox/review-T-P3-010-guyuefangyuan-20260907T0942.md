---
kind: review_result
review_id: review-T-P3-010-guyuefangyuan-20260907T0942
task_id: T-P3-010
source_agent: 古月方源
agent: 古月方源
claimed_at: 2026-09-07T00:29:00-06:00
created_at: 2026-09-07T09:42:00-06:00
inspected_commit: 6772c6b75ffbb848c073e9d668719e5011e3b312
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_exact_B45_source_mass_formula_then_bind_Float64_execution_error_separately
---

# T-P3-010 — exact DH/Jacobian formula and rigorous source-math interval for `M_BB(q)`

## 0. Result in one sentence

For the **ideal-real, unregularized** Route-B source mass assembled from the repository's exact DH/frame recursion, midpoint COM Jacobians, source mass table and scalar body inertias, the block for Julia joints 4 and 5 (Lean indices `3,4`) is exactly

```text
M_BB^0(q) =
[ 7/60 + (147/800000) sin^2(q5)      0
  0                                   40147/800000 ],
```

where `q5` is Julia's one-based fifth joint, i.e. Lean `q ⟨4,...⟩`.  Consequently the following interval is valid **globally in q**, hence in particular on every deployed q-box:

```text
7/60 <= M44^0(q) <= 280441/2400000,
M45^0(q) = 0,
M55^0(q) = 40147/800000.
```

This derivation uses neither `M0` nor sampling.  The repository's mathematical `+ 10^-6 I` regularizer can then be added exactly, but the real lift of the actual Float64 execution still requires a separate IEEE/source-semantic error enclosure and is not silently identified with the exact-real formula.

No work from `T-P3-009` or `T-P3-011`, no provenance/admission, and no P5/P8/M4 closure is claimed.

---

## 1. Source-level mathematical inputs

The derivation consumes the existing exact source-facing chain only:

```text
examples/routeb_real_dh_step_lean/RealDHStep.lean
examples/routeb_source_contract_adapter_lean/SourceContractAdapter.lean
examples/routeb_body_contract_core_lean/BodyContractCore.lean
examples/routeb_source_mass_table_minimal_lean/SourceMassTableMinimal.lean
examples/routeb_agent_source_mass_binding_lean/AgentSourceMassBinding.lean
```

The relevant definitions are:

```text
sourceMass(body)       = sourceMassTable(body),
sourceInertia(body)    = scalarIdentity(sourceInertiaScalarTable(body)),
sourceBodyMass(q,body) = contractMass(sourceContract(q), body, mass, inertia),
sourceMassSum(q)       = sum_body sourceBodyMass(q,body).
```

The mass/inertia table for bodies 3,4,5 is

```text
body 3: m3 = 1,    I3 = (1/15) I,
body 4: m4 = 1/2,  I4 = (1/30) I,
body 5: m5 = 3/20, I5 = (1/60) I.
```

`BodyContractCore` uses the midpoint of consecutive frame origins as each body COM; a Jacobian column is active iff its joint index is no larger than the body index, with

```text
Jv_j = z_j x (c_body - o_j),
Jw_j = z_j.
```

The exact DH rows relevant after frame 3 have

```text
joint 4: a4=0, d4=19/100, alpha4=-pi/2,
joint 5: a5=0, d5=0,      alpha5=+pi/2,
joint 6: a6=0, d6=7/100,  alpha6=0.
```

All statements below are therefore formula-level consequences of the exact source model, not fitted constants.

---

## 2. Local frame geometry for joints 4 and 5

Because all dot/cross products are invariant under the common upstream orthogonal frame, compute in frame-3 coordinates.  Put

```text
z3 = e3.
```

After joint 4,

```text
z4 = Rz(q4) Rx(-pi/2) e3
   = (-sin(q4), cos(q4), 0),
```

so

```text
z3 . z4 = 0.
```

After joint 5,

```text
z5 = Rz(q4) Rx(-pi/2) Rz(q5) Rx(+pi/2) e3
   = (cos(q4) sin(q5), sin(q4) sin(q5), cos(q5)).
```

Hence the exact identities needed by the mass block are

```text
||z3||^2 = ||z4||^2 = ||z5||^2 = 1,
z3 . z4 = 0,
z4 . z5 = 0,
z3 . z5 = cos(q5),
||z3 x z5||^2 = sin^2(q5),
||z4 x z5||^2 = 1,
(z3 x z5) . (z4 x z5) = 0.
```

The last equality follows from

```text
(a x c).(b x c) = (a.b)||c||^2 - (a.c)(b.c)
```

with `a=z3`, `b=z4`, `c=z5`.

---

## 3. Origins and midpoint COMs

Because the three relevant `a` offsets vanish,

```text
o4 = o3 + (19/100) z3,
o5 = o4,
o6 = o5 + (7/100) z5.
```

Therefore

```text
c3 = (o3+o4)/2 = o3 + (19/200) z3,
c4 = (o4+o5)/2 = o4,
c5 = (o5+o6)/2 = o4 + (7/200) z5.
```

For the B block, i.e. columns 3 and 4 in zero-based Lean indexing:

### body 3

Only column 3 is active and

```text
Jv_3,3 = z3 x (c3-o3) = 0.
```

Column 4 is inactive.

### body 4

`c4=o4`.  For column 3, `c4-o3=(19/100)z3`, hence its cross product is zero.  Column 4 is based at `o4`, hence also zero:

```text
Jv_4,3 = 0,
Jv_4,4 = 0.
```

### body 5

Since `c5-o3=(19/100)z3+(7/200)z5` and `c5-o4=(7/200)z5`,

```text
Jv_5,3 = (7/200) (z3 x z5),
Jv_5,4 = (7/200) (z4 x z5).
```

Thus

```text
||Jv_5,3||^2 = (49/40000) sin^2(q5),
||Jv_5,4||^2 = 49/40000,
Jv_5,3 . Jv_5,4 = 0.
```

This shows directly why no earlier joint coordinate occurs in the B45 block: all upstream rotations are a common orthogonal factor and disappear from these inner products.

---

## 4. Exact unregularized B45 mass formula

The scalar-inertia body contribution is

```text
m_b Jv_b^T Jv_b + I_b Jw_b^T Jw_b.
```

### `M44^0`

The rotational contribution from bodies 3,4,5 is

```text
1/15 + 1/30 + 1/60 = 7/60.
```

Only body 5 contributes translationally, with coefficient

```text
m5 * (7/200)^2
 = (3/20)*(49/40000)
 = 147/800000.
```

Therefore

```text
M44^0(q) = 7/60 + (147/800000) sin^2(q5).             (1)
```

### `M55^0`

Only bodies 4 and 5 are active in column 4.  Their rotational contribution is

```text
1/30 + 1/60 = 1/20.
```

Body 5 adds the same translational scalar `147/800000`, because `||z4 x z5||^2=1`.  Hence

```text
M55^0(q)
 = 1/20 + 147/800000
 = 40147/800000.                                      (2)
```

### `M45^0`

Every rotational cross term contains `z3.z4=0`.  The only possible translational cross term is body 5 and equals zero by Section 2.  Therefore

```text
M45^0(q) = M54^0(q) = 0.                              (3)
```

Combining (1)-(3):

```text
M_BB^0(q) =
[ 7/60 + (147/800000) sin^2(q5)      0
  0                                   40147/800000 ].  (4)
```

---

## 5. Rigorous interval, with no q-box approximation

Using only

```text
0 <= sin^2(q5) <= 1,
```

(1) gives

```text
7/60 <= M44^0(q)
     <= 7/60 + 147/800000
      = 280441/2400000.                               (5)
```

Together with (2)-(3), a global source-math enclosure is

```text
M44^0(q) in [7/60, 280441/2400000],
M45^0(q) = 0,
M55^0(q) = 40147/800000.                              (6)
```

Numerically, only as a sanity display and **not as proof input**,

```text
M44^0 in [0.116666666666..., 0.116850416666...],
M55^0  = 0.05018375.
```

Because (6) is valid for every real `q`, no sampling density, deployed-box endpoint, monotonicity subdivision, or `M0` surrogate is needed for this particular block.

---

## 6. Exact mathematical `+10^-6 I` regularizer

If the mathematical source model is defined by

```text
M^reg(q) := M^0(q) + (1/1000000) I,
```

then diagonal entries shift and the off-diagonal entry does not.  Exact rational arithmetic gives

```text
M44^reg(q) in
  [350003/3000000, 1402217/12000000],

M45^reg(q) = 0,

M55^reg(q) = 200739/4000000.                          (7)
```

Indeed

```text
7/60 + 1/1000000                  = 350003/3000000,
280441/2400000 + 1/1000000        = 1402217/12000000,
40147/800000 + 1/1000000          = 200739/4000000.
```

This is the exact-real **mathematical regularized** model.  It is useful to keep (6) and (7) as separate theorem statements because downstream arguments sometimes need the unregularized physical mass while the runtime solve uses the regularized matrix.

---

## 7. Float64/deployed-source boundary that must remain explicit

The actual Julia path evaluates trigonometric functions, cross products, matrix products/sums, and the literal `1e-6` in Float64.  Therefore the real lift of executed bits is not definitionally the same object as either (4) or the exact-rational regularized model (7).

Let a source checker eventually certify absolute execution discrepancies

```text
|M44_exec - M44^reg| <= eps44,
|M45_exec - M45^reg| <= eps45,
|M55_exec - M55^reg| <= eps55,
```

on the same source domain, with nonnegative `eps44,eps45,eps55`.  Then (7) immediately transports to the deployed execution enclosure

```text
M44_exec in
  [350003/3000000 - eps44,
   1402217/12000000 + eps44],

M45_exec in [-eps45, eps45],

M55_exec in
  [200739/4000000 - eps55,
   200739/4000000 + eps55].                           (8)
```

Equation (8) is the correct source-to-runtime adapter shape.  This task does **not** invent numerical epsilon values from sampling, and it does not identify the Float64 literal with exact `1/1000000` without a rounding theorem.

Thus the precise remaining source obligation is now only the IEEE/execution error around a closed exact-real formula, rather than an unknown analytic mass interval.

---

## 8. Suggested minimal Lean theorem decomposition

The most useful formalization is to prove geometry first, then reduce the final source matrix entries by `norm_num`/`ring`.

Index convention: Julia one-based joint 5 is Lean `q ⟨4,...⟩`.

Suggested atomic statements:

```lean
-- Exact source formula.
theorem source_M44_exact (q : Fin 6 -> Real) :
    sourceMassSum q 3 3 =
      (7/60 : Real) + (147/800000 : Real) * (Real.sin (q 4))^2 := ...

theorem source_M45_exact (q : Fin 6 -> Real) :
    sourceMassSum q 3 4 = 0 := ...

theorem source_M55_exact (q : Fin 6 -> Real) :
    sourceMassSum q 4 4 = (40147/800000 : Real) := ...

-- Global interval.
theorem source_B45_interval (q : Fin 6 -> Real) :
    (7/60 : Real) <= sourceMassSum q 3 3 /\
    sourceMassSum q 3 3 <= (280441/2400000 : Real) /\
    sourceMassSum q 3 4 = 0 /\
    sourceMassSum q 4 4 = (40147/800000 : Real) := ...

-- Mathematical regularizer adapter.
def regularizedMass (M : Fin 6 -> Fin 6 -> Real) (i j : Fin 6) : Real :=
  M i j + if i = j then (1/1000000 : Real) else 0

-- Execution-error transport should remain parametric in eps44/45/55.
```

Helpful source-geometry lemmas that keep the final theorem small are:

```text
body3_B_translational_zero,
body4_B_translational_zero,
body5_col3_sqnorm = (49/40000) sin^2(q5),
body5_col4_sqnorm = 49/40000,
body5_col3_col4_dot = 0,
axis3_dot_axis4 = 0.
```

A formalizer should consume the existing `sourceContract`/`sourceMassSum` definitions rather than restating a free matrix with the target entries as hypotheses; otherwise the source-binding content would be lost.

---

## 9. Boundaries / non-overlap

This review intentionally does not perform:

- `T-P3-009`: inverse/correction or independent matrix-bound validation;
- `T-P3-011`: global structural lower-bound/PSD lane beyond the exact B45 entry facts above;
- any use of `M0` as evidence;
- any sampled estimate of a source interval;
- any Float64 bit-level claim without an explicit execution-error theorem;
- provenance, receipt, admission, registry promotion, or final integration.

The mathematical result is ready for the formalization lane, but remains `pending` until independent verification and coordinator integration.

**待封不觉独立验证 / 待梁智炜收割与最终整合。**
