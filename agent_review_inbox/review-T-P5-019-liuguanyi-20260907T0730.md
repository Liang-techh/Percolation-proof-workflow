---
kind: review_result
review_id: review-T-P5-019-liuguanyi-20260907T0730
task_id: T-P5-019
source_agent: 柳冠一
claimed_at: 2026-09-07T07:12:00-06:00
created_at: 2026-09-07T07:30:00-06:00
inspected_commit: 09472a05742559e829ba0e5f83f391ba18355e34
claim_commit: ab0591fe6b7d413aa72727a92e10242ca0a9be59
continuation_of:
  - review-T-P5-009-liuguanyi-20260907T0606
related_reviews:
  - review-T-P5-014-liuguanyi-20260907T0417
  - review-T-P5-016-guyuefangyuan-20260907T0538
  - review-T-P5-018-guyuefangyuan-20260907T0634
  - review-T-P4-018-liuguanyi-20260907T0522
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_block45_fd_to_euclidean_tube_adapter_and_source_bind_the_forceerror_sign_index_contract
---

# T-P5-019 — exact block-(4,5) FD/runtime envelope -> Euclidean residual-tube adapter

## 0. Result in one sentence

`T-P5-018` changes the useful destination of the positive-offset FD bounds from a homogeneous damping estimate to an additive **two-channel Euclidean residual budget**.  For that destination the current affine envelopes are mathematically adequate without a velocity floor or a centered-increment theorem: on any source domain where `0 <= cap <= Ccap`, the axis-(4,5) FD contribution has an explicit exact polynomial `L2` bound, and any additional runtime/nominal component boxes can be added sharply before squaring.

The review also isolates two interface rules that must not be blurred:

1. the existing six-channel weighted power budget is **not** itself the `L2` consumed by `T-P5-018`, although there is a sharp conversion constant `8/5` for the block; and
2. `FDForceBudget.efd` is already typed as an additive generalized-force error at the abstract Lean layer, so the block normalization `I_B` must not be silently applied a second time.  If a concrete source interval is produced in a pre-force/raw coordinate, its normalization belongs upstream in the source binding.

No source authentication, Float64 interval proof, ODE coverage, CI/admission, or P5/P8/M4 closure is claimed.

---

## 1. The exact consumer required by T-P5-018

`T-P5-018` studies the incremental block dynamics

```text
x' = y,
M y' + D y + B x = -r,
```

with the block generalized-force mismatch

```text
r = l - lbar.
```

Its residual-only barrier consumes a scalar `L2` satisfying

```text
||r||^2 = r4^2 + r5^2 <= L2.                         (1)
```

For a common physical-domain margin `sigma>0`, the division-free sufficient condition from `T-P5-018` is

```text
24435333 * sigma^2 > 5246976000 * L2.                (2)
```

Thus a source-facing adapter only needs to manufacture a genuine two-channel bound (1) on the same first-exit domain.  It does **not** need to manufacture a homogeneous estimate `|r_i| <= rho |v_i|`.

This is precisely why the positive affine offsets that obstructed the strict relative route in `T-P5-009` are no longer a mathematical obstruction here.

---

## 2. Axis indexing: the first adapter boundary

`FDForceBudget.lean` stores six components as `Fin 6`, hence internally uses zero-based indices `0,...,5`.  The Route-B block in `T-P5-016/T-P5-018` is named by the source's one-based mechanical axes `(4,5)`.

Therefore the intended abstract extraction is

```text
source axis 4  <->  Fin 6 index 3,
source axis 5  <->  Fin 6 index 4.                     (3)
```

This mapping should become a named typed adapter in any formalization rather than being repeated as an unlabelled numeral conversion.  The mathematics below assumes (3); concrete source binding must still certify that the generated FD interval vector uses the same ordering.

From `FDForceBudget.slope/offset`, the corresponding affine envelopes are

```text
E4(c) = s4 c + b4,
s4 = 173713 / 300832000000000,
b4 = 6867   / 8000000000000000,

E5(c) = s5 c + b5,
s5 = 520451 / 1353744000000000,
b5 = 6867   / 4000000000000000.                       (4)
```

Both offsets are positive.  This is consistent with `T-P5-009`: only internal channels `0` and `5` have zero offset; the human axes `(4,5)` are internal channels `(3,4)` and therefore both lie in the positive-offset class.

---

## 3. Sharp component-box -> block Euclidean norm lemma

The basic theorem is elementary but is exactly the interface `T-P5-018` needs.

### Lemma 3.1 — `component_box_to_block_l2`

Let `R4,R5 >= 0`.  If

```text
|r4| <= R4,
|r5| <= R5,
```

then

```text
r4^2 + r5^2 <= R4^2 + R5^2.                           (5)
```

The bound is sharp from independent box information alone: equality is attained by choosing `r4=±R4`, `r5=±R5`.

There is no factor `2` loss here.  In particular, if a residual component is already described by a single affine envelope, one should square that envelope directly rather than first splitting slope and offset and applying `(a+b)^2 <= 2a^2+2b^2`.

### Runtime and nominal mismatch

Suppose an actual-minus-nominal block mismatch has component decomposition

```text
r_i = eps_i + zeta_i - n_i,                            (6)
```

where `eps` is the FD/model component, `zeta` is a runtime/solve/controller component, and `n` is a certified nominal-model residual.  If

```text
|eps_i|  <= E_i,
|zeta_i| <= Z_i,
|n_i|    <= N_i,
Z_i,N_i >= 0,
```

then

```text
|r_i| <= E_i + Z_i + N_i,
```

and hence

```text
||r||^2
 <= (E4+Z4+N4)^2 + (E5+Z5+N5)^2.                     (7)
```

Again (7) is sharp under only independent component-box information.  For an ideal nominal model set `N4=N5=0`.

This is preferable to artificially decomposing a positive offset into a `relative + bias` vector: the incremental tube only needs the total box.

---

## 4. Exact FD-only block polynomial

For FD-only residual and the envelopes (4), define

```text
P45(c) := E4(c)^2 + E5(c)^2.                           (8)
```

Direct rational expansion gives

```text
P45(c)
 = A45 c^2 + B45 c + C45,                              (9)
```

with

```text
A45 = 3527749689493
      / 7330491270144000000000000000000,

B45 = 397329089
      / 171904000000000000000000000000,

C45 = 47155689
      / 12800000000000000000000000000000.             (10)
```

Numerically, only as a scale check,

```text
A45 ~= 4.81243283634e-19,
B45 ~= 2.31134289487e-21,
C45 ~= 3.68403820313e-24.
```

The exact fractions in (10), not these decimal checks, are the intended theorem constants.

### Lemma 4.1 — monotone cap adapter

All four coefficients `s4,b4,s5,b5` are nonnegative.  Therefore if

```text
0 <= c <= Ccap,                                        (11)
```

then

```text
P45(c) <= P45(Ccap).                                   (12)
```

Consequently, if a source/domain theorem gives (11) and

```text
|eps4| <= E4(c),
|eps5| <= E5(c),                                       (13)
```

then

```text
 eps4^2 + eps5^2 <= P45(Ccap).                         (14)
```

This is the key change relative to `T-P5-009`: for an additive tube consumer, a **uniform cap bound on the first-exit domain is sufficient**.  One does not need `cap <= K|v_i|`, a velocity floor, or a centered Lipschitz theorem.

### Immediate T-P5-018 specialization

For FD-only residual with ideal nominal model, the common-margin tube is certified whenever

```text
24435333 * sigma^2
  > 5246976000 * P45(Ccap).                            (15)
```

Equation (15) is an exact rational checker target and contains no square root.  It is conditional only on the source/domain premises just stated; it does not authenticate those premises.

With runtime/nominal boxes, replace `P45(Ccap)` in (15) by

```text
(E4(Ccap)+Z4+N4)^2 + (E5(Ccap)+Z5+N5)^2.              (16)
```

---

## 5. Existing weighted power budget -> Euclidean tube: a sharp `8/5` bridge

There is also a useful fallback if the source lane initially exposes only the already-existing weighted force budget.

For the Route-B block damping

```text
d4 = 4/5,
d5 = 13/20,                                            (17)
```

define

```text
W45(r)
 := r4^2/(2 d4) + r5^2/(2 d5)
  = (5/8) r4^2 + (10/13) r5^2.                        (18)
```

Then there is the exact identity

```text
(8/5) W45(r) - (r4^2+r5^2)
 = (3/13) r5^2 >= 0.                                  (19)
```

Hence

```text
r4^2+r5^2 <= (8/5) W45(r).                            (20)
```

The constant `8/5` is sharp if all that is known is `W45`: take `r5=0` and equality holds.

Since every summand in the six-channel weighted budget is nonnegative,

```text
W45(r) <= W6(r)
 := sum_i r_i^2/(2 d_i),                               (21)
```

whenever the block components are entries of that same six-channel generalized-force vector.  Therefore

```text
||r45||^2 <= (8/5) W6(r).                              (22)
```

This gives a direct mathematical adapter from the existing `DHPowerBinding/FDForceBudget` weighted consumer to the new `T-P5-018` Euclidean tube consumer.

### Existing polynomial fallback

For FD-only error, `FDForceBudget` already defines

```text
polynomialBudget(c) = sum_i envelope(c,i)^2/(2 d_i).
```

Thus, under the component envelope hypotheses,

```text
||eps45||^2 <= (8/5) polynomialBudget(c).              (23)
```

Combining with the existing convenient polynomial upper bound gives

```text
||eps45||^2
 <= (8/5) * (3103 c^2 + 152 c + 4) / 10^21.           (24)
```

If `0<=c<=Ccap`, the right-hand side may be evaluated at `Ccap`.

Together with the common-margin theorem, a coarse but immediately reusable sufficient condition is

```text
24435333 * 10^21 * sigma^2
 > 8395161600 * (3103 Ccap^2 + 152 Ccap + 4).          (25)
```

because

```text
5246976000 * (8/5) = 8395161600.
```

No square roots or transcendental operations appear.

### Why direct block extraction is preferable

The fallback (23)-(25) pays for all six channels before converting back to a two-channel norm.  The direct block polynomial (9) is much tighter.  Coefficientwise, the `(8/5)` full-six-channel fallback is about

```text
10.3 x larger in the c^2 coefficient,
104.8 x larger in the c coefficient,
1551.6 x larger in the constant coefficient
```

than the direct axis-(4,5) polynomial.

Therefore (23) is a good fast bridge to existing formalized infrastructure, but (14)-(16) are the right source/checker target for a serious P8 domain bootstrap.

---

## 6. Coordinate normalization: apply it exactly once

`T-P4-018` established that the frozen reduced certificate's raw block expression `f_B` is not itself the generalized-force residual coordinate; the force map is

```text
I_B = diag(1/5,1/10).                                  (26)
```

For any raw block error `u=(u4,u5)`, the mathematical normalization theorem is

```text
r = I_B u
=> ||r||^2 = u4^2/25 + u5^2/100.                      (27)
```

Thus raw component boxes `|u4|<=U4`, `|u5|<=U5` imply

```text
||r||^2 <= U4^2/25 + U5^2/100.                        (28)
```

More generally, for `J=diag(j4,j5)`,

```text
||J u||^2 = j4^2 u4^2 + j5^2 u5^2.                    (29)
```

### Critical layer distinction

The abstract `FDForceBudget.lean` theorem does **not** place `efd` in the raw PMI `f_B` coordinate.  Its hypothesis is

```text
forceError(...) = efd + runtime,
```

and `forceError` is defined by `DHPowerBinding.implemented_force_identity` through

```text
Ma*a + cA + gA = tauA + forceError.                    (30)
```

So at that abstract Lean layer, `efd` is already typed as an additive **generalized-force** error.  The correct `T-P5-019` adapter therefore uses `J=I` after hypothesis (30) has been source-bound.

If a concrete interval generator instead emits an error bound in the pre-normalized reduced `f_B` coordinate, then (26)-(29) must be applied **before** asserting the `FDForceBudget`/`forceError` hypothesis.  Re-applying `I_B` after an error has already been bound as `forceError` would double-normalize it and understate the residual tube by factors up to `25`/`100` in squared magnitude.

This is the same class of layer error detected in `T-P4-018`, now stated at the P5/P8 tube interface.

---

## 7. Sign convention does not affect the norm, but semantic binding is still required

The reduced block review uses

```text
l := I_B f_B - M a_B,
```

whereas the full six-axis `DHPowerBinding.forceError` is introduced through (30).  Depending on which side of the descriptor equation is called the residual, a concrete bridge may identify a block component as `l_i = forceError_i` or `l_i = -forceError_i`.

For (1) this sign is immaterial:

```text
(-e_i)^2 = e_i^2.                                      (31)
```

But the **index and force-coordinate binding are not immaterial**.  To reuse `FDForceBudget` inside `T-P5-018`, the source lane still needs a theorem of the form

```text
r4 = sigma4 * forceError(index3),
r5 = sigma5 * forceError(index4),
sigma4^2 = sigma5^2 = 1,                               (32)
```

or the corresponding actual-minus-nominal version, on the same domain as the interval envelopes.

Equation (32) is a semantic/source obligation, not something the present algebra can infer from two independently defined residual names.

---

## 8. First-exit compatibility and what source lane now has to prove

A sound P5/P8 bootstrap can now be organized as follows.

Assume the nominal P8 tube has a block margin `sigma` inside a source-valid domain `K`.  Before a hypothetical first exit of the actual trajectory from `K`, source/checker provides

```text
0 <= cap(z(t)) <= Ccap,                                (33)
```

plus either

```text
(A) direct block component envelopes, including runtime/nominal terms,
```

or

```text
(B) a full weighted generalized-force envelope W6 <= Wbar.
```

Route (A) yields the sharp bound (16).  Route (B) yields

```text
L2 <= (8/5) Wbar.                                      (34)
```

If the resulting `L2` satisfies (2), `T-P5-018` makes the block error-energy boundary inward.  Its coordinate coercivity then prevents the actual block from consuming the nominal margin, closing the same-domain first-exit loop for those coordinates.

Notice the logical improvement over the older relative route: (33) is a **domain supremum** statement.  It does not have to collapse with velocity at equilibrium.

---

## 9. Minimal Lean theorem decomposition

The following sidecar statements are enough; there is no need to re-formalize the hypocoercive derivative from `T-P5-018`.

### 9.1 Generic box theorem

```text
component_box_to_block_l2
  (h4 : |r4| <= R4) (h5 : |r5| <= R5)
  : r4^2 + r5^2 <= R4^2 + R5^2
```

with the mild/nonnegative envelope premises made explicit if required by the proof style.

### 9.2 Sharp weighted-to-Euclidean bridge

```text
block45_weighted_to_euclidean
  : r4^2 + r5^2
      <= (8/5) * (r4^2/(2*(4/5)) + r5^2/(2*(13/20)))
```

A particularly robust proof is to `ring_nf` the difference and reduce it to `(3/13)*r5^2 >= 0`.

### 9.3 Diagonal normalization

```text
diagonal_block_l2_identity
  : (j4*u4)^2 + (j5*u5)^2 = j4^2*u4^2 + j5^2*u5^2
```

and the concrete corollary

```text
ib_block_l2_identity
  : (u4/5)^2 + (u5/10)^2 = u4^2/25 + u5^2/100.
```

### 9.4 Exact current FD polynomial

Introduce named axis adapters rather than bare `Fin` numerals, then prove

```text
block45_fd_polynomial_exact (c : R) :
  E4(c)^2 + E5(c)^2
    = A45*c^2 + B45*c + C45.
```

This is pure `norm_num/ring` over exact rationals.

### 9.5 Cap monotonicity and T-P5-018 composition

```text
block45_fd_of_cap_le
  (0 <= c) (c <= Ccap)
  (|e4| <= E4(c)) (|e5| <= E5(c))
  : e4^2 + e5^2 <= P45(Ccap).
```

Then a theorem that only composes hypotheses,

```text
block45_fd_common_margin_budget
  (hL2 : e4^2+e5^2 <= P45(Ccap))
  (hbudget : 5246976000*P45(Ccap) < 24435333*sigma^2)
  : 5246976000*(e4^2+e5^2) < 24435333*sigma^2.
```

No ODE API belongs in this sidecar.

---

## 10. Exact obstructions / failure boundaries

### 10.1 A six-channel weighted budget is not definitionally a two-channel Euclidean budget

Using `polynomialBudget` as if it literally equalled `r4^2+r5^2` is a type/metric error.  The correct fallback is the proven conversion (22), with the `8/5` factor and a block-index contract.

### 10.2 Positive offsets still forbid the old homogeneous route

This review does not contradict `T-P5-009`.  If one insists on `|e_i|<=rho|v_i|` on a set containing `v_i=0`, the positive offsets remain an obstruction absent a centered increment theorem.  The new result works because `T-P5-018` accepts an additive `L2`.

### 10.3 A cap bound must be on the same first-exit domain

An unrelated global/sample cap or a nominal-only cap cannot be substituted for (33).  The source theorem must bound the actual state-dependent cap on the domain whose invariance is being bootstrapped, or provide a monotone enclosure that is valid there.

### 10.4 Do not double-normalize

If the source result is already a `forceError` bound, multiplying by `I_B` again creates a falsely small tube.  Conversely, if the source result is still in raw `f_B` units, omitting `I_B` creates the opposite coordinate mismatch.  The theorem boundary must say which one it consumes.

---

## 11. Remaining source/math obligations after this child

The algebraic bridge itself is closed.  The unresolved obligations are now concrete and typed:

1. `BLOCK45_AXIS_INDEX_BINDING` — certify that source axes `(4,5)` are the `Fin 6` entries `(3,4)` of the emitted FD/error vector.
2. `BLOCK45_RESIDUAL_FORCEERROR_BINDING` — identify the `T-P5-018` actual-minus-nominal residual with the corresponding generalized-force `forceError` components, up to explicit sign and nominal terms.
3. `BLOCK45_FORCE_COORDINATE_BINDING` — state whether the concrete interval generator emits raw `f_B` errors or already-normalized generalized-force errors; apply `I_B` exactly once.
4. `P8_SAME_DOMAIN_CAP_BOUND` — prove `0<=cap<=Ccap` on the same domain used by the nominal-margin/first-exit argument.
5. `RUNTIME_COMPONENT_BOXES` — give same-domain `Z4,Z5` (and `N4,N5` if the nominal model is not ideal) for Float64/solve/controller/model terms not included in the FD envelope.

Once these are available, the checker can feed the sharp expression (16) directly into the already-derived `T-P5-018` barrier.  None is solved merely by the rational algebra in this review.

---

## 12. Suggested coordination

For the formalization agents: this child is deliberately small.  Prefer the five theorem statements in section 9 and import the existing `FDForceBudget` constants if practical; do not duplicate the `T-P5-018` hypocoercive sidecar.

For the source/checker lane: prefer direct axis-(4,5) component extraction over the full-six-channel weighted fallback.  The latter is immediately valid after semantic binding but is especially pessimistic in the constant-offset coefficient.

For 梁智炜: the main integration value is a new clean seam

```text
T-P5-009 affine component envelopes
        + same-domain cap/runtime boxes
        + explicit force/index adapter
        -> exact block L2
        -> T-P5-018 incremental tube.
```

This seam avoids the equilibrium obstruction of the old pure-relative route without weakening `T-P5-009`'s negative result.

**Status: pending.  Await formalization / independent validation / coordinator harvest; no final integration claim.**
