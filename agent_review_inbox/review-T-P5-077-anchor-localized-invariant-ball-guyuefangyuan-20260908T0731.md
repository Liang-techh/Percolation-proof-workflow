---
kind: review_result
review_id: review-T-P5-077-anchor-localized-invariant-ball-guyuefangyuan-20260908T0731
task_id: T-P5-077-ANCHOR-LOCALIZED-INVARIANT-BALL
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-08T07:31:00-06:00
claim_commit: 4685230405c524bb9f2af5f6c7eebbde95430b36
inspected_commits:
  - 48c78207c758636227a8bb3f5be2e1f6c247e6c4
  - 038772083818be60fa274d5e9d60162a686d2dde
  - f2769764ff5a9c983114c3de525808be97eb98c7
inspected_paths:
  - agent_review_inbox/review-T-P5-074-weighted-strong-monotone-scc-guyuefangyuan-20260908T0700.md
  - agent_review_inbox/review-T-P5-075-damped-corrector-energy-honglianmozun-20260908T0712.md
  - agent_review_inbox/review-T-P5-076-weighted-gram-lipschitz-liuguanyi-20260908T0716.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Add this as the missing local-domain/self-map consumer after T-P5-074/075/076.
  The source packet should provide one same-weight anchor residual budget and
  axis-aligned source-box halfwidths. The radical-free coordinate gates below
  then certify that the unknown-root Lyapunov sublevel stays inside the source
  box, so the T-P5-075 defective-corrector barrier can be iterated. Keep actual
  SCC/source binding, implementation semantics, coverage, Lean/kernel and
  admission separate.
---

# T-P5-077 — anchor residual localization and radical-free local invariant ball

## 0. Result in one line

T-P5-074 supplies a same-weight strong-monotonicity packet for a contact SCC,
T-P5-076 supplies the missing same-weight squared-Lipschitz packet, and
T-P5-075 supplies a sharp defective-corrector Lyapunov barrier.  One domain
obligation remained explicit in T-P5-075: the Lyapunov ball used by the
corrector must actually lie inside the source box where those two secant
inequalities are valid.

That domain obligation can be closed with one anchor residual budget and a
fully radical-free coordinate test.

Let

`Q(v) = sum_i w_i v_i^2`, `w_i>0`,

let the source box be

`B = {x : |x_i-c_i| <= H_i}`, `H_i>0`,

and suppose `x* in B` is a root, `F(x*)=0`.  Assume on `B`

`<F(x)-F(y),x-y>_W >= mu Q(x-y)`, `mu>0`,

and at the anchor `c`

`Q(F(c)) <= B0`, `B0>=0`.

Then the unknown root obeys the exact square localization

**(0.1)** `mu^2 Q(c-x*) <= B0`.

Fix a candidate Lyapunov level `Vstar>=0`.  For each coordinate define

**(0.2)**

`A = mu^2 Vstar`,

`C = B0`,

`T_i = mu^2 w_i H_i^2`,

`R_i = T_i - A - C`.

If for every `i`

**(0.3)** `R_i >= 0`,

**(0.4)** `4*A*C <= R_i^2`,

then every state satisfying

`Q(x-x*) <= Vstar`

lies in the source box `B`.

The test uses only rational addition, multiplication, squares and order.  No
`sqrt(w_i)`, root coordinate, matrix inverse, eigenvalue, or floating norm is
needed by the trusted scalar checker.

If additionally

**(0.5)** `B0 <= mu^2 Vstar`,

then the anchor itself satisfies `Q(c-x*)<=Vstar`.  Combining (0.3)-(0.5) with
the T-P5-075 defective-corrector barrier turns its one-step theorem into a
true local invariant iteration theorem: starting at `c` (or any point in the
same sublevel), every certified defective step stays in that sublevel and
therefore remains inside the source box where T-P5-074/076 continue to apply.

This is mathematics only.  It does not identify a deployed SCC, prove a source
residual budget, bind a corrector implementation, or certify Float64/FD/
controller/solve, P8/ODE coverage, Lean/kernel evidence, provenance, admission,
registry mutation, or parent closure.

---

## 1. Weighted setting and exact assumptions

Use the same positive diagonal weight as T-P5-074 and T-P5-076:

`W = diag(w_1,...,w_n)`, `w_i>0`,

`Q(v)=v^T W v = sum_i w_i v_i^2`.

Let `B` be the closed axis-aligned box centered at an anchor `c`:

**(1.1)** `B = product_i [c_i-H_i, c_i+H_i]`, `H_i>0`.

Assume a root `x* in B` is already supplied by the existence layer of
T-P5-074 (or another same-domain existence theorem):

**(1.2)** `F(x*)=0`.

Assume the weighted strong-monotonicity secant inequality on `B`:

**(1.3)**

`<F(x)-F(y), x-y>_W >= mu Q(x-y)`, `mu>0`.

For the later corrector consumer also assume the T-P5-076 same-weight squared
secant bound

**(1.4)**

`Q(F(x)-F(y)) <= Lambda Q(x-y)`

on the same box.  Sections 2-5 below need only (1.2)-(1.3); `Lambda` is used
only when attaching the T-P5-075 corrector.

Finally suppose source analysis gives the anchor residual certificate

**(1.5)** `Q(F(c)) <= B0`, `B0>=0`.

The important point is that `B0` is a squared weighted residual budget in the
same coordinates as the strong-monotonicity theorem.  A force-space,
acceleration-space, differently weighted, or unrelated residual cannot be
substituted without an explicit typed bridge.

---

## 2. Anchor residual localizes the unknown root without radicals

Set

`d = c-x*`, `V0=Q(d)`.

From strong monotonicity with `(x,y)=(c,x*)` and `F(x*)=0`,

**(2.1)** `mu V0 <= <F(c),d>_W`.

Weighted Cauchy gives

**(2.2)** `<F(c),d>_W^2 <= Q(F(c)) V0 <= B0 V0`.

The left side of (2.1) is nonnegative.  Squaring (2.1) and using (2.2),

**(2.3)** `mu^2 V0^2 <= B0 V0`.

If `V0=0`, the desired result is immediate.  If `V0>0`, cancel one factor
`V0` to obtain

### Theorem 2.1 — anchor residual root localization

**(2.4)** `mu^2 Q(c-x*) <= B0`.

This is the square form of the familiar inverse estimate
`||c-x*||_W <= ||F(c)||_W/mu`, but (2.4) is the preferable checker interface:
no square root and no division are required.

A useful initialization corollary is immediate:

### Corollary 2.2 — anchor starts inside a chosen root sublevel

If

**(2.5)** `B0 <= mu^2 Vstar`,

then

**(2.6)** `Q(c-x*) <= Vstar`.

Again this is purely multiplicative rational arithmetic.

---

## 3. Generic radical-free two-square envelope lemma

The source-box problem contains a sum of two unknown signed displacements:

`x_i-c_i = (x_i-x*_i) + (x*_i-c_i)`.

The cross term cannot be discarded.  The following scalar lemma is the exact
radical-free envelope needed repeatedly.

Let `K>0`, `A>=0`, `C>=0`, `T>=0`, and suppose real numbers `a,b` satisfy

**(3.1)** `K a^2 <= A`,

**(3.2)** `K b^2 <= C`.

Define

**(3.3)** `R=T-A-C`.

Assume

**(3.4)** `R>=0`,

**(3.5)** `4AC <= R^2`.

Then

`(2K|ab|)^2 = 4 (K a^2)(K b^2) <= 4AC <= R^2`.

Both `2K|ab|` and `R` are nonnegative, so

**(3.6)** `2K|ab| <= R`.

Therefore

`K(a+b)^2`

`= K a^2 + K b^2 + 2K ab`

`<= A+C+2K|ab|`

`<= A+C+R = T`.

Hence:

### Theorem 3.1 — scaled two-square sum gate

Under (3.1)-(3.5),

**(3.7)** `K(a+b)^2 <= T`.

The strict version is equally useful: if `R>0` and `4AC<R^2`, then

**(3.8)** `K(a+b)^2 < T`.

No radical appears anywhere in the proof.  In envelope language, (3.4)-(3.5)
are exactly the polynomial elimination of

`sqrt(A)+sqrt(C) <= sqrt(T)`.

The theorem is useful beyond this child: it is the same two-budget geometry
that appears in T-P5-075's sharp evaluator-defect barrier.

---

## 4. Radical-free containment of a root-centered weighted sublevel in the source box

Fix a state `x` with

**(4.1)** `Q(x-x*) <= Vstar`.

For coordinate `i`, write

`a_i=x_i-x*_i`,

`b_i=x*_i-c_i`.

From (4.1),

**(4.2)** `w_i a_i^2 <= Vstar`.

Multiplying by `mu^2`,

**(4.3)** `mu^2 w_i a_i^2 <= mu^2 Vstar`.

From the anchor localization (2.4),

**(4.4)** `mu^2 w_i b_i^2 <= B0`.

Apply Theorem 3.1 with

`K_i = mu^2 w_i`,

`A = mu^2 Vstar`,

`C = B0`,

`T_i = mu^2 w_i H_i^2`.

Thus define

**(4.5)**

`R_i = mu^2 w_i H_i^2 - mu^2 Vstar - B0`.

If

**(4.6)** `R_i >= 0`,

**(4.7)** `4 mu^2 Vstar B0 <= R_i^2`,

then

`mu^2 w_i (x_i-c_i)^2 <= mu^2 w_i H_i^2`.

Since `mu^2 w_i>0`, cancel it:

**(4.8)** `(x_i-c_i)^2 <= H_i^2`,

hence `|x_i-c_i|<=H_i`.

Doing this for every coordinate proves:

### Theorem 4.1 — anchor-localized root sublevel is inside the source box

Assume `x* in B`, (1.2)-(1.5), and let `Vstar>=0`.  If for every coordinate
`i`, the rational gates (4.6)-(4.7) hold, then

**(4.9)**

`{x : Q(x-x*) <= Vstar} subset B`.

Strict versions of (4.6)-(4.7) yield strict coordinate interior
`|x_i-c_i|<H_i`, which can be useful if a source derivative packet is only
stated on an open neighborhood of the certified box.

### Trusted-checker arithmetic

For rational/dyadic `mu,w_i,H_i,Vstar,B0`, the checker computes only

- `mu^2`;
- `T_i=mu^2*w_i*H_i^2`;
- `A=mu^2*Vstar`;
- `R_i=T_i-A-B0`;
- `R_i>=0`;
- `R_i^2 >= 4*A*B0`.

There is no root finding, square root, matrix inversion, eigenvalue, or
continuous optimization.

---

## 5. Why `A+C <= T` alone is mathematically unsafe

A tempting but invalid simplification is to drop the cross term and check only

`A+C <= T`.

There is an exact one-dimensional counterexample compatible with the root
localization geometry.

Take

`mu=1`, `w=1`, `c=0`,

`F(x)=x-1/2`, so `x*=1/2`,

`B0=F(c)^2=1/4`,

`Vstar=1/4`,

and source halfwidth

`H=3/4`, hence `T=H^2=9/16`.

The naive gate passes:

`A+C = 1/4+1/4 = 1/2 <= 9/16=T`.

But the root sublevel contains

`x=x*+1/2=1`,

for which

`Q(x-x*)=1/4=Vstar`,

while

`|x-c|=1>3/4=H`.

So the alleged contained sublevel actually leaves the source box.

The exact radical-free gate correctly rejects this case:

`R=T-A-C=1/16`,

`R^2=1/256`,

while

`4AC=1/4`.

Thus (4.7) fails by a large exact margin.

At `H=1`, the same aligned example saturates the correct gate:

`T=1`, `R=1/2`, and `R^2=4AC=1/4`.

Therefore the two-square gate is sharp for the uncertainty class described only
by the two independent square budgets.

---

## 6. Local invariant theorem for the defective damped corrector

Now attach T-P5-075 and T-P5-076.

Assume on the same source box `B`:

**(6.1) strong monotonicity**

`<F(x)-F(y),x-y>_W >= mu Q(x-y)`, `mu>0`,

and

**(6.2) squared Lipschitz**

`Q(F(x)-F(y)) <= Lambda Q(x-y)`, `Lambda>=0`.

Let the exact root satisfy `F(x*)=0`, and define

**(6.3)** `V(x)=Q(x-x*)`.

For step `h>=0`, define

**(6.4)** `q = 1 - 2h mu + h^2 Lambda`.

Assume the T-P5-075 contraction packet

**(6.5)** `0<=q<1`.

Suppose each evaluator defect `e` obeys the same-weight budget

**(6.6)** `Q(e)<=E`, `E>=0`.

Define

**(6.7)** `Rdef = (1-q)Vstar - h^2 E`.

Assume the sharp T-P5-075 barrier gates

**(6.8)** `Rdef>0`,

**(6.9)** `4 h^2 q Vstar E < Rdef^2`.

Then every defective step

**(6.10)** `x+ = x - h(F(x)+e)`

maps

`V(x)<=Vstar`

strictly into

**(6.11)** `V(x+)<Vstar`.

By Theorem 4.1, if the coordinate containment gates (4.6)-(4.7) hold, every
such input and output remain inside `B`.  Therefore the hypotheses (6.1)-(6.2)
remain available at the next step.

This closes the domain induction that T-P5-075 intentionally left external.

### Theorem 6.1 — defective corrector local invariant sublevel

Assume:

1. root `x* in B`, `F(x*)=0`;
2. same-box `(mu,Lambda,W)` strong-monotonicity/squared-Lipschitz packet;
3. anchor budget `Q(F(c))<=B0`;
4. all coordinate containment gates (4.6)-(4.7);
5. `0<=q<1` and the defective barrier gates (6.8)-(6.9);
6. same-coordinate evaluator defect budget `Q(e)<=E`.

Then

**(6.12)** `V(x)<=Vstar => x in B and V(x+)<Vstar`.

If in addition

**(6.13)** `B0 <= mu^2 Vstar`,

then the anchor `c` itself satisfies `V(c)<=Vstar`, so the corrector may be
started from `c` without any separate root-location oracle.

### Corollary 6.2 — iteration remains in the certified source box

For any sequence

`x_0=c`,

`x_{k+1}=x_k-h(F(x_k)+e_k)`,

with `Q(e_k)<=E` at every step, the above hypotheses imply by induction

**(6.14)** `V(x_k)<=Vstar` and `x_k in B` for all `k`.

After the first step the Lyapunov inequality is strict:

`V(x_k)<Vstar` for every `k>=1`.

This is a true mathematical self-map theorem, but still not a deployed solver
receipt: one must separately prove that deployed code computes this update and
that its evaluator defect is the same `e_k` certified in (6.6).

---

## 7. Relation to T-P5-074 / 075 / 076

The division of labor is now clean:

- **T-P5-074:** same-weight lower secant geometry / strong monotonicity and root
  uniqueness/inverse conditioning for a general SCC;
- **T-P5-076:** same-weight upper secant geometry / squared Lipschitz from a
  signed weighted-Gram source packet;
- **T-P5-075:** one-step damped-corrector Lyapunov factor and sharp evaluator
  defect barrier;
- **T-P5-077:** root localization from one anchor residual and radical-free
  proof that the chosen Lyapunov sublevel stays in the source box, allowing the
  one-step barrier to be iterated.

The four layers share the same diagonal weight `W`.  Changing weights between
layers is not a harmless implementation detail: it requires an explicit norm
comparison theorem and can alter every numerical margin.

The new source obligation is narrow.  Once an actual SCC/cell is selected, the
source side should try to provide

`B0 >= Q_W(F(c))`

at a convenient rational anchor `c`, plus rational source-box halfwidths `H_i`.
The trusted checker can then evaluate (4.6)-(4.7) exactly.

---

## 8. Counterexample-guided fail-closed rules

1. **Do not drop the root-offset cross term.**
   `A+C<=T` is insufficient; Section 5 gives an exact counterexample.

2. **Do not infer root existence from the anchor residual bound.**
   Theorem 2.1 localizes an already supplied same-domain root.  Existence still
   belongs to T-P5-074's Brouwer/self-map layer or another explicit theorem.

3. **Do not use strong monotonicity outside its certified domain.**
   If the only proof of (1.3) is on `B`, then the premise `x* in B` is essential
   for the anchor localization step.

4. **Do not mix weighted coordinates.**
   `B0`, `Vstar`, `E`, `mu`, `Lambda`, and the source-box containment calculation
   must all refer to the same root-residual coordinates and the same `W`.

5. **Containment-gate failure is not a physical counterexample.**
   It only means `NOT_CERTIFIED_BY_ANCHOR_LOCALIZED_BALL`.  A smaller `Vstar`, a
   better anchor, a tighter residual budget, anisotropic/componentwise root
   localization, or a non-ellipsoidal invariant set may still work.

6. **Persistent absolute defect gives invariance, not zero convergence.**
   T-P5-075's exact linear counterexample remains in force.  This child does
   not reinterpret `E>0` as a relative error.

---

## 9. Suggested Lean theorem decomposition

The useful first formal targets are deliberately scalar and finite-sum based.

### Leaf A — root localization

`strong_mono_anchor_root_localization_sq`

Input:

- `mu>0`;
- `F xstar = 0`;
- strong monotonicity between `c` and `xstar`;
- weighted Cauchy;
- `Q(F c)<=B0`.

Output:

`mu^2 * Q(c-xstar) <= B0`.

### Leaf B — generic radical-free envelope

`scaled_two_square_sum_le_of_gate`

Input:

`0<K`, `K*a^2<=A`, `K*b^2<=C`,

`R=T-A-C`, `0<=R`, `4*A*C<=R^2`.

Output:

`K*(a+b)^2<=T`.

This is likely the smallest and most reusable first Lean child.

### Leaf C — one-coordinate source containment

`coordinate_mem_box_of_anchor_root_budget`

Instantiate Leaf B with

`K=mu^2*w_i`, `A=mu^2*Vstar`, `C=B0`,

`T=mu^2*w_i*H_i^2`.

### Leaf D — finite box containment

`weighted_root_sublevel_subset_box_of_anchor_budget`

A `Fin n` wrapper around Leaf C.

### Leaf E — anchor initialization

`anchor_mem_root_sublevel_of_residual_budget`

From `mu^2 Q(c-x*)<=B0<=mu^2 Vstar` and `mu>0`, conclude
`Q(c-x*)<=Vstar`.

### Leaf F — local invariant consumer

`defective_corrector_invariant_on_certified_box`

Consume T-P5-075's one-step theorem plus Leaf D.  Keep the actual iteration
recursion/induction as a later wrapper if desired.

No matrix API is required for Leaves A-C/E, and no square-root API is required
at all.

---

## 10. Remaining boundary

This review closes only the source-independent mathematical seam

`same-domain root + strong monotonicity + anchor residual`

`-> root localization`

`-> radical-free root-sublevel/source-box containment`

`-> iterative consumption of the T-P5-075 one-step barrier`.

Still open:

1. selecting the deployed SCC/contact chart and source box;
2. same-key source binding of the actual `W,mu,Lambda` packet;
3. a real anchor residual certificate `B0>=Q_W(F(c))`;
4. same-key evaluator defect `E` in root-residual coordinates;
5. proof that deployed code uses the damped corrector update with the certified
   `h`;
6. Float64/libm/FD/controller/solve semantics;
7. P8/ODE/physical coverage;
8. Lean/kernel compilation and `#print axioms`;
9. independent 封不觉 validation, comparator/admission, and registry state.

If no rational `Vstar` satisfies both the source-box containment gates and the
T-P5-075 defect barrier, the correct conclusion is only

`NO_COMMON_INVARIANT_LEVEL_FOUND_FOR_THIS_PACKET`.

It is not evidence that the chart is noninvertible or the physical closed loop
is unstable.

---

## 11. Admission boundary

**Admission label: `pending`.**

No authoritative P5/P8/M4 state is changed by this review.
