---
kind: review_result
review_id: review-T-P4-040-divfree-liuguanyi-20260907T1816
task_id: T-P4-040
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T18:16:00-06:00
inspected_commit: ef81e9d0f507af8cb1b815c5fd5846892a5c2c64
dispatch_commit: 326fff46971995a254e652ede5b0b35c9872faac
claim_commit: 99e778dabdf1dd20ccadb895f766a5773793891c
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-038-guyuefangyuan-20260907T1521.md
  - agent_review_inbox/review-T-P4-039-liuguanyi-20260907T1616.md
related_tasks:
  - T-P4-037
  - T-P4-038
  - T-P4-039
  - T-P4-041
  - T-P4-042
  - T-P4-043
integration_status: pending
admission_label: pending
proposed_integration_target: P4.common_lambda_division_free_core
requested_action: formalize the four ordered-ring polynomial lemmas below and compose them with the existing T-P4-038 Real consumer using one shared theta; keep rational witness construction outside the semantic theorem and do not infer source, coverage, or admission
---

# T-P4-040 — division-free common-parameter algebra and exact `Rat`/`Real` seam

## 0. Result

Revision 742 explicitly assigned 柳冠一 the mathematical child: compress the `T-P4-039` common-parameter argument into four Lean-friendly, division-free theorems and make the rational/real boundary explicit.

The main simplification is stronger than merely deleting `/` from the displayed formulas:

**all four core lemmas need only an ordered ring.**

They do not require square roots, fields, matrix APIs, finite sets, source cells, or even positivity assumptions that belong only to the witness-construction layer.  Therefore the same theorem statements can be instantiated over `ℚ` for exact checker arithmetic and over `ℝ` for the semantic P4 consumer.

Write

```text
q(A,G,P,theta) := A*theta^2 - G*theta + P,
Delta(A,G,P)   := G^2 - 4*A*P.
```

The trusted common-parameter core can consume one supplied `theta` using only

```text
G_i - s_i <= 2*A_i*theta,
2*A_i*theta <= G_i + s_i,
s_i^2 <= Delta_i.
```

No endpoint division `(G±s)/(2A)` is required inside the theorem.

A second useful compression is that the radius-to-polynomial theorem does **not** require `theta>0`, `s>=0`, `G>0`, or `P>=0`.  Those hypotheses belong to other layers.  The only sign premise needed there is `A>0`.  Keeping them out of the algebraic theorem makes the later Lean interface smaller and avoids false source obligations.

---

## 1. Core theorem 1 — completed square, multiplication only

For any commutative ring,

```text
(2*A*theta - G)^2 - (G^2 - 4*A*P)
  = 4*A*(A*theta^2 - G*theta + P).                 (1.1)
```

Equivalently,

```text
Delta - (2*A*theta-G)^2 = -4*A*q.                  (1.2)
```

Suggested theorem name:

```text
young_completed_square_mul
```

Suggested Lean shape:

```text
[R : Type*] [CommRing R]
(A G P theta : R) :
  (2*A*theta-G)^2 - (G^2-4*A*P)
    = 4*A*(A*theta^2-G*theta+P)
```

Proof is `ring`; there are no hypotheses.

This is preferable to the divided reserve formula from `T-P4-039` because every later inequality can be derived from the same polynomial identity.

---

## 2. Core theorem 2 — radius certificate implies polynomial feasibility

Let the coefficient type be a linear ordered ring.  Assume only

```text
0 < A,                                                     (2.1)
(2*A*theta-G)^2 <= s^2,                                   (2.2)
s^2 <= G^2 - 4*A*P.                                      (2.3)
```

Then

```text
A*theta^2 - G*theta + P <= 0.                             (2.4)
```

Suggested theorem name:

```text
young_radius_poly_nonpos
```

Proof: (2.2)-(2.3) imply

```text
(2*A*theta-G)^2 - Delta <= 0.
```

By (1.1),

```text
4*A*q <= 0.
```

Since `A>0`, also `4*A>0`, hence `q<=0`.

### Minimality note

The following `T-P4-039` construction hypotheses are deliberately **not** needed here:

- `theta>0` — required only when converting `q<=0` to the Young expression containing `1/theta`;
- `s>=0` — irrelevant once the checker already supplied the squared radius inequalities;
- `P>=0`, `G>0` — useful for constructing a positive inner interval, not for this implication.

This separation is important for a Lean sidecar with warnings-as-errors: these hypotheses should not be carried into a theorem that mathematically does not use them.

---

## 3. Core theorem 3 — division-free inner tube

The old interval statement used

```text
(G-s)/(2A) <= theta <= (G+s)/(2A).
```

That introduces field division and denominator-sign bookkeeping even though the underlying certificate is polynomial.  Replace it by the exactly equivalent multiplication-side premises (under `A>0`):

```text
0 < A,
0 <= s,
G - s <= 2*A*theta,
2*A*theta <= G + s,
s^2 <= G^2 - 4*A*P.                                      (3.1)
```

Then

```text
A*theta^2 - G*theta + P <= 0.                             (3.2)
```

Suggested theorem name:

```text
young_inner_tube_poly_nonpos
```

Proof: set `x=2*A*theta-G`.  The two affine inequalities give

```text
-s <= x <= s.
```

Together with `s>=0`,

```text
x^2 <= s^2.
```

Now invoke theorem 2.

Again, `P>=0` and `G>0` are not needed by this consumer.  If the rational search layer derives the tube from discriminant geometry, it may use those stronger premises there; the semantic theorem should not inherit them.

### Shared-parameter corollary

For a row family indexed by any type `I`, no finiteness is needed **after one common witness has already been supplied**.  Put `theta` outside the row quantifier:

```text
shared theta
forall i,
  0 < A_i,
  0 <= s_i,
  G_i-s_i <= 2*A_i*theta,
  2*A_i*theta <= G_i+s_i,
  s_i^2 <= G_i^2-4*A_i*P_i
------------------------------------------------
forall i, q_i(theta) <= 0.                                (3.3)
```

This is just theorem 3 pointwise, but its quantifier placement is the typed contract that prevents the invalid downgrade

```text
forall i, exists theta_i, q_i(theta_i)<=0
```

from being mistaken for

```text
exists theta, forall i, q_i(theta)<=0.
```

Finiteness belongs only to the external intersection/search constructor (`max L_i`, `min U_i`), not to the final polynomial consumer.

---

## 4. Core theorem 4 — reserve charging without division

Let `m` denote a requested downstream reserve measured in the original Young budget.  A multiplication-only certificate can be stated as

```text
0 < A,
(2*A*theta-G)^2 <= s^2,
s^2 + 4*A*theta*m <= G^2 - 4*A*P.                         (4.1)
```

Then

```text
A*theta^2 - G*theta + P + theta*m <= 0.                  (4.2)
```

Suggested theorem name:

```text
young_radius_poly_reserve
```

Proof: combine (4.1) to get

```text
(2*A*theta-G)^2 + 4*A*theta*m <= Delta.
```

Using (1.2),

```text
4*A*theta*m <= -4*A*q,
```

and `A>0` gives (4.2).

This formulation is more useful than storing

```text
[Delta-(2*A*theta-G)^2]/(4*A*theta)
```

because it never divides and it lets the exact rational checker charge a requested `m` directly.

To interpret `m` as a nonnegative real Young-budget reserve, the **bridge** to `T-P4-038` additionally assumes

```text
0 < theta,
0 <= m,
G = D-A-P.                                                (4.3)
```

The existing multiplication identity from `T-P4-038` gives

```text
theta * (D - Young(theta)) = -q(theta).                  (4.4)
```

From (4.2),

```text
-q(theta) >= theta*m.
```

Since `theta>0`,

```text
D - Young(theta) >= m.                                   (4.5)
```

Thus the new theorem stops at the polynomial reserve; the old scalar adapter remains the only place where positivity of `theta` and the reciprocal Young expression are needed.

If `m>0` and `theta>0`, (4.2) also implies strict `q(theta)<0`, but the boundary/strict-intersection classification is intentionally left to the separately assigned `T-P4-043` lane.

---

## 5. Exact `Rat` / `Real` boundary

The safest formal interface is **not** “prove a theorem in `ℚ`, serialize a boolean, and trust a cast to `ℝ`.”  Instead:

1. the search/checker layer emits exact rationals `A_i,G_i,P_i,s_i,theta,m_i` as numerator/denominator pairs;
2. the four core theorems are stated generically over a `LinearOrderedRing` where possible;
3. the physical P4 theorem instantiates them directly over `ℝ` using the canonical coercions of those same rationals;
4. exact rational inequalities are discharged in Lean by exact arithmetic (`norm_num`/`norm_cast` or equivalent), never by `Float64` evaluation.

The reason this is exact is algebraic: the canonical map

```text
ℚ -> ℝ
```

preserves `0,1,+,-,*`, powers by natural numbers, strict/non-strict order, and therefore every premise and conclusion in sections 1–4.

A useful implementation choice is therefore:

```text
core theorem type      : LinearOrderedRing R
checker witness type   : Rat
semantic instantiation : Real
```

No theorem requires a field merely because the **constructor** used rational midpoint or endpoint division.

### Midpoint construction boundary

The finite search layer may still construct

```text
theta = (L+U)/2
```

or

```text
L_i=(G_i-s_i)/(2*A_i), U_i=(G_i+s_i)/(2*A_i)
```

inside exact rational arithmetic.  But after construction, the trusted proof payload should contain the resulting rational `theta` and verify the multiplication-only premises from section 3.  The semantic theorem never needs to replay those divisions.

Therefore a parser/adapter must not route

```text
Rat -> Float64 -> Real.
```

That would create a new rounding theorem obligation and defeat the exact seam.  The admissible route is exact rational syntax/coercion directly into Lean `ℝ`.

---

## 6. Minimal theorem surface recommended to the Lean lane

The four mathematical leaves should be kept separate:

```text
young_completed_square_mul
young_radius_poly_nonpos
young_inner_tube_poly_nonpos
young_radius_poly_reserve
```

Recommended typeclass strength:

```text
young_completed_square_mul      : CommRing
young_radius_poly_nonpos        : LinearOrderedRing
young_inner_tube_poly_nonpos    : LinearOrderedRing
young_radius_poly_reserve       : LinearOrderedRing
```

A fifth theorem is unnecessary for the common-row consumer: one shared `theta` plus `forall i` premises can invoke `young_inner_tube_poly_nonpos` pointwise.  A finite `Finset.max/min` theorem may remain an optional constructor theorem, but it should not block this algebraic core.

The bridge into `T-P4-038` is likewise a corollary, not a replacement of the already compiled/scalar-budget theorem.  Its only new typed discipline is that the **same** `theta` is supplied to every row.

---

## 7. Coordination / task-label collision

The repository already contains an earlier historical `T-P4-040-RATIONAL-LAMBDA-GUARD` result by 狂蛮魔尊 and a corresponding Lean sidecar/review by 巨阳仙尊.  Revision 742 later reused the short label `T-P4-040` for this explicitly assigned division-free child.

This review does **not** supersede, rewrite, or invalidate those earlier files.  To avoid semantic collision in the DAG, integration should use a distinct child key such as

```text
P4.common_lambda_division_free_core
```

while retaining `task_id: T-P4-040` as the latest dispatch label/provenance.  The earlier robust-lambda-interval child remains a sibling result.

---

## 8. Open boundaries / non-claims

Still open and untouched:

- Lean compilation, theorem API repair, `#print axioms`, placeholder scan, or receipt (`T-P4-041`/Lean lanes);
- independent `T-P4-038` adapter audit and shared-theta typing (`T-P4-042`);
- strict-intersection/boundary-only closure classification (`T-P4-043`);
- concrete row coefficients, actual source cell identity, true-DH/Float64 semantics;
- source/P8/trajectory/domain coverage;
- comparator, registry, P4/M4 admission.

No source or coverage fact is inferred from these algebraic lemmas.  Admission remains `pending`.
