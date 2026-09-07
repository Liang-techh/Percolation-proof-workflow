---
kind: review_result
review_id: review-T-P3-010-guyuefangyuan-20260907T0035
task_id: T-P3-010
source_agent: 古月方源
claimed_at: 2026-09-07T00:29:00-06:00
created_at: 2026-09-07T00:35:00-06:00
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_exactized_block45_formula_and_feed_T-P3-009_while_preserving_Float64_source_boundary
---

# T-P3-010 — exact-real DH block-(4,5) mass formula and sharp global interval

## Scope

This mathematical pass attacks the coordinator-assigned source-math leaf for the physical axes `(4,5)` without taking over `T-P3-009`'s independent matrix-bound/validation lane.

Inspected repository facts:

- `docs/routeb-dh-source-coefficient-binding-next.md` gives the exactized DH parameters, parent-axis convention, COM midpoint convention, Jacobian construction, isotropic inertia convention, and the separation of `1e-6 I` from the 610-row Fourier payload.
- `examples/routeb_source_binding_audit/snapshots/current_exact/routeB_fourier_mass_full_rational.csv` has exactly three aggregate rows for `(4,4)`, no rows for `(4,5)` or `(5,4)`, and one row for `(5,5)`.
- `examples/routeb_source_binding_audit/snapshots/current_exact/ReferenceMass.lean` records the regularized `q=0` entries `M0[4,4]=350003/3000000`, `M0[4,5]=0`, `M0[5,5]=200739/4000000` in one-based physical naming.
- `examples/routeb_source_binding_audit/REPORT.md` explicitly keeps exact-real/Fourier semantics separate from the deployed Julia `Float64` execution semantics.

No receipt/provenance/admission or Float64 equality is claimed here.

## 1. Direct exact-real DH/Jacobian reduction

Use the canonical exactized source parameters from the source-map document:

```text
alpha/pi/2 = [-1,0,1,-1,1,0]
d            = [1/10,0,1/20,19/100,0,7/100]
a            = [2/25,21/100,0,0,0,0]
m            = [1,4/5,3/5,2/5,3/10,3/20]
I_val        = [1,3/5,7/20,1/5,1/10,1/20].
```

Let `z_k` denote the parent-frame joint axis, `o_k` the frame origin, and for body `b`

```text
p_b = (o_{b-1}+o_b)/2,
Jv_b[:,k] = z_k x (p_b-o_{k-1}),
Jw_b[:,k] = z_k,
```

for `k<=b`, exactly as in the documented source recursion.

Only bodies 4,5,6 contribute to columns 4 and 5. The exact geometry collapses to the following scalar inner products.

### Body 4

```text
Jv_4[:,4] = 0,
||Jw_4[:,4]||^2 = 1.
```

Hence its `(4,4)` contribution is purely rotational:

```text
(I_val_4/3) = (1/5)/3 = 1/15.
```

### Body 5

Because `a_5=d_5=0`, the midpoint COM is at the frame origin for the translational columns:

```text
Jv_5[:,4] = Jv_5[:,5] = 0.
```

The `alpha_4=-pi/2` parent-axis relation gives

```text
||Jw_5[:,4]||^2 = ||Jw_5[:,5]||^2 = 1,
Jw_5[:,4] dot Jw_5[:,5] = 0.
```

Therefore body 5 contributes

```text
M44^(5) = 1/30,
M45^(5) = 0,
M55^(5) = 1/30.
```

### Body 6

For the midpoint of the final `d_6=7/100` link, direct DH simplification gives the coordinate-free norm/dot identities

```text
||Jv_6[:,4]||^2 = (49/40000) sin(q5)^2,
||Jv_6[:,5]||^2 = 49/40000,
Jv_6[:,4] dot Jv_6[:,5] = 0,

||Jw_6[:,4]||^2 = ||Jw_6[:,5]||^2 = 1,
Jw_6[:,4] dot Jw_6[:,5] = 0.
```

With `m_6=3/20` and `I_val_6/3=1/60`, this yields

```text
M44^(6) = 1/60 + (147/800000) sin(q5)^2,
M45^(6) = 0,
M55^(6) = 1/60 + 147/800000
          = 40441/2400000.
```

Summing bodies 4--6 therefore gives the **unregularized exact-real source formula**

```text
Mhat_BB(q)
 = [[ 7/60 + (147/800000) sin(q5)^2,  0 ],
    [ 0,                                  40147/800000 ]].       (1)
```

This is independent of `q1,q2,q3,q4,q6`.

## 2. Independent agreement with the frozen exact Fourier support

The current exact mass payload has, for `(4,4)`, exactly

```text
nu5=-2 : -147/3200000
nu5= 0 :  560441/4800000
nu5=+2 : -147/3200000,
```

so its real evaluator is

```text
560441/4800000 - (147/1600000) cos(2 q5)
= 7/60 + (147/800000) sin(q5)^2,
```

using `1-cos(2x)=2 sin(x)^2`.

There is no aggregate `(4,5)` support row, and `(5,5)` is the single zero-frequency row

```text
40147/800000.
```

Thus the direct DH/Jacobian reduction and the frozen exact Fourier aggregate give the same three block formulas. This is a much smaller target than the 610-row full-map theorem.

Important boundary: aggregate support emptiness alone would not prove bodywise zero. The direct Jacobian calculation above supplies the missing mathematical reason: both translational and rotational cross inner products vanish for the only bodies that can contribute.

## 3. Regularizer bridge

The deployed source adds `regularization=1e-6` to the diagonal only. Therefore the exact-real regularized block is

```text
M_BB(q)
 = [[ 7/60 + 1/1000000 + (147/800000) sin(q5)^2, 0 ],
    [ 0, 40147/800000 + 1/1000000 ]].                (2)
```

Equivalently,

```text
M44(q) = 350003/3000000 + (147/800000) sin(q5)^2,
M45(q) = 0,
M55(q) = 200739/4000000.
```

At `q5=0` this reproduces the corresponding literal `ReferenceMass.M0` block exactly.

## 4. Sharp interval and coercivity consequences

Since `0 <= sin(q5)^2 <= 1` for every real `q5`, no branch-and-bound or local q-cell is needed for this block:

```text
350003/3000000 <= M44(q) <= 1402217/12000000,
M45(q) = 0,
M55(q) = 200739/4000000.                             (3)
```

The lower endpoint of `M44` is attained at `q5=0`; the upper endpoint is attained whenever `sin(q5)^2=1`. The proof-facing Route-B domain contains `q5=0`, and the global bound (3) is valid even without using the domain contract.

Therefore, in exact-real semantics,

```text
M_BB(q) >= diag(350003/3000000, 200739/4000000)
        >= (200739/4000000) I_2.                    (4)
```

So the block coercivity constant can be taken as

```text
lambda_B = 200739/4000000 ~= 0.05018475,
```

which is more than fifty thousand times the bare `1e-6` regularizer floor.

Because the block is diagonal, its inverse is also explicit and the exact-real upper bounds are

```text
(M_BB(q)^-1)44 <= 3000000/350003,
(M_BB(q)^-1)45 = 0,
(M_BB(q)^-1)55 = 4000000/200739.                    (5)
```

In particular

```text
||M_BB(q)^-1||_2 <= 4000000/200739 ~= 19.93.        (6)
```

These are immediately consumable by `T-P3-009` / P7 Schur mathematics **once the source semantic adapter is accepted**.

## 5. What is closed mathematically and what remains open

Closed in this review at the exact-real DH algebra level:

1. block `(4,5)` depends only on `q5`;
2. exact formulas (1)--(2);
3. the cross mass entry is identically zero for structural Jacobian-orthogonality reasons;
4. global/sharp rational interval (3);
5. strong coercivity and inverse bounds (4)--(6);
6. exact agreement of these block formulas with the frozen Fourier support and with `M0` at `q=0`.

Still open and deliberately not hidden:

- The canonical Julia source executes `Matrix{Float64}`, Float64 `sin/cos`, ordered matrix products and Float64 accumulation. This review does **not** prove bitwise or exact equality between that execution and (2).
- Full `B45-1` source/Fourier equality for all 610 aggregate coefficients remains a separate semantic theorem. The block result reduces the `(4,5)` subproblem to four source statements rather than requiring a global full-matrix proof.
- No claim is made about central-FD `C/G`, solve error, P4 residual closure, P8 coverage or registry admission.

The important obstruction is therefore now sharply localized: for block `(4,5)`, the difficult remaining source issue is **Float64/exact-real semantic binding**, not trigonometric interval geometry or matrix positivity.

## 6. Lean-friendly theorem package

A source-independent sidecar can encode the already-reduced exact-real block without importing the full 610-row payload:

```lean
def m44Hat (q5 : R) : R :=
  7/60 + (147/800000) * (Real.sin q5)^2

def m44 (q5 : R) : R := m44Hat q5 + 1/1000000

def m55 : R := 40147/800000 + 1/1000000

theorem block45_exact_formula ...
-- from the exactized DH Jacobian inner-product premises

theorem m44_bounds (q5 : R) :
    350003/3000000 <= m44 q5 /
    m44 q5 <= 1402217/12000000

theorem block45_coercive (q5 x4 x5 : R) :
    (200739/4000000) * (x4^2+x5^2)
      <= m44 q5*x4^2 + m55*x5^2

theorem block45_inverse_entry_bounds ...
```

For the semantic adapter, the smallest useful source statement is not full-matrix equality but the block slice:

```text
ExactizedDHMass_BB(q)
  = [[m44Hat(q5),0],[0,40147/800000]]
```

followed by the separate `+1/1000000 I_2` regularizer theorem. If this block-slice theorem is source-bound, `T-P3-009` no longer needs sampled eigenvalues or a generic interval eigensolver for the `(4,5)` mass block.

## Recommended next action

1. Formalization lane: encode the exact-real block formula, global rational bounds, coercivity and inverse-entry bounds as a tiny sidecar.
2. Source-binding lane: prove only the block-slice exactized DH recursion first; do not wait for all 610 rows. The bodywise identities above make that target small.
3. `T-P3-009`: consume (4)--(6) conditionally and keep its independent validation/source-gate boundary.
4. If a true Float64 enclosure rather than exact equality is required, use (2) as the real center and add an explicit operation-level/interval error term; do not silently identify Float64 evaluation with the exact-real formula.
