---
kind: review_result
review_id: review-T-P5-039-guyuefangyuan-20260907T1931
task_id: T-P5-039
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T19:24:00-06:00
created_at: 2026-09-07T19:31:00-06:00
inspected_commit: 4405ff80d2821d782dd67b7049e681f54b18b567
continuation_of:
  - review-T-P5-036-guyuefangyuan-20260907T1906
related_tasks:
  - T-P5-037
  - T-P5-038
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_exact_pareto_optimizer_then_feed_same_domain_componentwise_source_caps_E4_E5
---

# T-P5-039 — exact rational optimizer for the T-P5-038 Pareto first-exit gate

## 0. Result in one line

`T-P5-038` has already formalized the convex Pareto family obtained from the T-P5-037 scalar endpoint and the T-P5-036 anisotropic endpoint.  At the existing quarter barrier, its abstract source-independent gate is

```text
300000 E4 + 1200(250+53r) E5 < (109-r)(250+53r),
0 <= r <= 1.                                           (0.1)
```

There is no need to grid-search `r`.  Define

```text
A := 27250 - 300000(E4+E5),
B := 5527 - 63600 E5.                                  (0.2)
```

Then the exact signed margin of (0.1) is

```text
F(r) := (109-r)(250+53r)
        - 300000 E4 - 1200(250+53r)E5
      = A + B r - 53 r^2.                              (0.3)
```

Hence the maximizing parameter on `[0,1]` is explicitly

```text
r_opt = 0,          if B <= 0,
        1,          if B >= 106,
        B/106,      if 0 < B < 106.                    (0.4)
```

This selector is rational whenever the source caps `E4,E5` are rational.  It is also **independent of E4**: component 4 changes only the constant offset `A`, while the optimal interpolation parameter is selected entirely by the component-5 residual cap.

The exact maximal margin is

```text
Fmax = A,                         if B <= 0,
       A + B - 53,                if B >= 106,
       A + B^2/212,               if 0 < B < 106.       (0.5)
```

Thus existence of any `r in [0,1]` closing the entire T-P5-038 Pareto family has a square-root-free necessary-and-sufficient test.  In the interior branch one merely checks

```text
212 A + B^2 > 0.                                    (0.6)
```

If the corresponding branch maximum is nonpositive, then **no real or rational choice of `r` in this whole convex certificate family can close**.  At that point the correct response is to tighten `E4/E5` or leave this family for a stronger matrix/SPN/source-correlated certificate; continuing a parameter grid is mathematically pointless.

---

## 1. Exact expansion

Start from the T-P5-038 quarter-barrier gate.  Move the left side to the right and define

```text
F(r)
 := (109-r)(250+53r)
    - 300000 E4
    - 1200(250+53r) E5.
```

Expanding over the rationals gives

```text
(109-r)(250+53r)
  = 27250 + 5527 r - 53 r^2,

1200(250+53r)E5
  = 300000 E5 + 63600 E5 r.
```

Therefore

```text
F(r)
 = [27250 - 300000(E4+E5)]
   + [5527 - 63600 E5] r
   - 53 r^2
 = A + B r - 53 r^2.                                  (1.1)
```

This is a strictly concave quadratic in `r`; all optimization below is exact rational algebra and does not use numerical eigenvalues, floating optimization, differentiation APIs, or source assumptions.

---

## 2. Three exact maximizer branches

### 2.1 Left endpoint: `B <= 0`

For `0 <= r <= 1`,

```text
F(0) - F(r)
 = -B r + 53 r^2
 = r(53r-B).                                           (2.1)
```

If `B <= 0`, both factors on the right are nonnegative, so

```text
F(r) <= F(0) = A.                                      (2.2)
```

Thus `r_opt=0`, and the Pareto family is feasible iff

```text
A > 0.                                                 (2.3)
```

This is exactly the T-P5-037 scalar endpoint:

```text
A > 0
<=> 27250 > 300000(E4+E5)
<=> 1200(E4+E5) < 109.                                 (2.4)
```

### 2.2 Right endpoint: `B >= 106`

For `0 <= r <= 1`,

```text
F(1) - F(r)
 = (1-r)[B - 53(1+r)].                                 (2.5)
```

Since `r <= 1`, one has `53(1+r) <= 106`.  Hence `B >= 106` implies

```text
F(r) <= F(1) = A + B - 53.                             (2.6)
```

Thus `r_opt=1`, and feasibility is exactly

```text
A+B-53 > 0.                                            (2.7)
```

Expanding (2.7),

```text
32724 - 300000 E4 - 363600 E5 > 0
<=> 25000 E4 + 30300 E5 < 2727,                        (2.8)
```

which is precisely the T-P5-036 anisotropic endpoint.

### 2.3 Interior vertex: `0 < B < 106`

Set

```text
r_star := B/106.                                       (2.9)
```

Then `0 < r_star < 1`.  Completing the square gives the exact identity

```text
F(r_star) - F(r)
 = 53 (r-r_star)^2 >= 0.                               (2.10)
```

Therefore

```text
Fmax = F(r_star)
     = A + B^2/212.                                    (2.11)
```

The strict gate is therefore equivalent to the division-free inequality

```text
212 A + B^2 > 0.                                       (2.12)
```

No square root is needed either for selection or checking.

---

## 3. Source-facing threshold form

Because

```text
B = 5527 - 63600 E5,
```

the three branches can be selected directly from `E5`:

```text
B >= 106
<=> E5 <= 5421/63600
<=> E5 <= 1807/21200,                                  (3.1)

B <= 0
<=> E5 >= 5527/63600.                                  (3.2)
```

So a checker consuming rational same-domain caps can use

```text
if E5 <= 1807/21200:
    r := 1
    check 25000 E4 + 30300 E5 < 2727

else if E5 >= 5527/63600:
    r := 0
    check 1200(E4+E5) < 109

else:
    B := 5527 - 63600 E5
    r := B/106
    A := 27250 - 300000(E4+E5)
    check 212 A + B^2 > 0.                              (3.3)
```

The interior band is narrow:

```text
1807/21200 < E5 < 5527/63600,
```

but it is mathematically real, and the interior branch can certify cases that **both endpoints reject**.

---

## 4. Strict gain over endpoint-only selection

In the interior branch, the optimizer beats the scalar endpoint by

```text
F(r_star) - F(0) = B^2/212 > 0,                        (4.1)
```

and beats the anisotropic endpoint by

```text
F(r_star) - F(1)
 = (106-B)^2/212 > 0.                                  (4.2)
```

Thus the vertex is not merely a convenient parametrization; it strictly enlarges the certifiable `(E4,E5)` region whenever `0 < B < 106`.

A fully exact rational witness makes this concrete.  Take

```text
E5 = 2737/31800,
E4 = 75803/15900000.                                   (4.3)
```

Then

```text
B = 53,
A = -1,
r_star = 1/2.                                          (4.4)
```

Consequently

```text
F(0) = -1,
F(1) = -1,                                             (4.5)
```

so **both T-P5-037 and T-P5-036 endpoint gates fail**.  But

```text
F(1/2)
 = -1 + 53/2 - 53/4
 = 49/4 > 0.                                           (4.6)
```

Hence the interior Pareto certificate succeeds with a strict exact margin.  This is a genuine new certified region, not just removal of a search loop.

---

## 5. Necessary-and-sufficient fail-fast theorem

Let `A,B` be (0.2).  Combining the three branches gives the exact statement

```text
exists r, 0 <= r <= 1 and F(r) > 0
```

iff exactly one of the following branch conditions applies and its maximal margin is positive:

```text
(B <= 0   and A > 0)

or

(B >= 106 and A+B-53 > 0)

or

(0 < B and B < 106 and 212A+B^2 > 0).                 (5.1)
```

At `B=0`, the vertex coincides with `r=0`; at `B=106`, it coincides with `r=1`, so there is no missing boundary case.

A useful fail-fast obstruction is the negation: if the appropriate quantity in (5.1) is `<=0`, then no `r` in `[0,1]` can satisfy T-P5-038.  This obstruction is internal to this particular convex certificate family only; it is **not** a counterexample to the underlying dynamics or to stronger SPN/matrix/source-correlated certificates.

---

## 6. Suggested minimal Lean decomposition

The math can be formalized without an optimizer library.  Suggested theorem surface:

```text
pareto_margin_expand
```

Prove the ring identity (1.1).

```text
pareto_margin_left_max
```

Inputs: `0 <= r`, `r <= 1`, `B <= 0`.
Conclusion: `A + B*r - 53*r^2 <= A`.
Use (2.1).

```text
pareto_margin_right_max
```

Inputs: `0 <= r`, `r <= 1`, `106 <= B`.
Conclusion: `A + B*r - 53*r^2 <= A+B-53`.
Use (2.5).

```text
pareto_margin_vertex_gap
```

Identity for arbitrary `r,B`:

```text
A + B*(B/106) - 53*(B/106)^2
 - (A + B*r - 53*r^2)
 = 53*(r-B/106)^2.                                    (6.1)
```

```text
pareto_margin_vertex_value
```

Prove

```text
A + B*(B/106) - 53*(B/106)^2 = A + B^2/212.           (6.2)
```

```text
pareto_optimal_selector
```

Define the piecewise `r_opt` in (0.4), prove `0<=r_opt<=1`, and prove every admissible `r` has `F(r)<=F(r_opt)`.

```text
pareto_gate_exists_iff
```

Package (5.1), preferably retaining the division-free interior check `212A+B^2>0`.

```text
pareto_interior_strictly_beats_endpoints
```

Under `0<B<106`, prove (4.1) and (4.2).

```text
pareto_interior_endpoint_failure_witness
```

Instantiate (4.3)–(4.6) with `norm_num/ring`; this is a useful regression test ensuring future refactors do not collapse the family back to endpoint-only selection.

No theorem here needs source identities, trajectory existence, coverage, Float64 semantics, or admission machinery.

---

## 7. Dependencies and open obligations

Dependencies:

1. T-P5-036 anisotropic endpoint certificate;
2. T-P5-037 scalar endpoint certificate;
3. T-P5-038 convex Pareto bridge and first-exit consumer.

What T-P5-039 closes mathematically:

- exact maximization of the abstract T-P5-038 quarter-barrier gate over `r in [0,1]`;
- constructive rational `r_opt`;
- exact maximal inward margin;
- necessary-and-sufficient fail-fast test for this entire Pareto family;
- an exact rational example where the optimized interior succeeds while both endpoints fail.

Still open and explicitly **not** claimed here:

- same-domain source production of valid componentwise `E4,E5`;
- centered/incremental Float64, finite-difference, controller, solve-defect semantics;
- P8 flowpipe/coverage and ODE first-exit continuation;
- source identity tying the abstract frozen block-(4,5) derivative to deployed execution;
- pinned Lean compilation/axiom receipt for the new optimizer theorems;
- any P5/P8/M4 registry/admission transition.

Status: **pending mathematical child**.  The recommended next source-facing action is now deterministic: produce rational `E4,E5`, compute `B`, select `r_opt` from (0.4), and check exactly one branch of (0.5)/(3.3).