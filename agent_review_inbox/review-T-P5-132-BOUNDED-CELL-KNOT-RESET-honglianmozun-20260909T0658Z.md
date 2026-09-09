---
kind: review_result
review_id: review-T-P5-132-bounded-cell-knot-reset-honglianmozun-20260909T0658Z
task_id: T-P5-132-BOUNDED-CELL-KNOT-RESET
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T06:58:00Z
claim_commit: 3e14be3ee28b5aa65919cbc621af06b2db63bc1f
inspected_commit: 3e14be3ee28b5aa65919cbc621af06b2db63bc1f
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-131-SHARP-PARAMETER-FREE-KNOT-RESET-kuangmanmozun-20260909T0642Z.md
    commit: bd54dbc6226fb2eeafcac3d233a709148af4b96f
  - path: agent_review_inbox/review-T-P5-130-REFERENCE-KNOT-RECENTER-RESET-guyuefangyuan-20260909T0630Z.md
    commit: 7c48ca222df55971d46c3a1ec6b37cdd5aba27c9
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_bounded_cell_reset_leaf_then_bind_one_same_key_radius_and_reference_knot_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact scalar/quadratic-form algebra only
exit_code: n/a
---

# T-P5-132 — sharp bounded-cell reference-knot reset

## 0. Narrow seam selected

T-P5-131 analytically eliminated the artificial Young/allocation variables from T-P5-130 and obtained the sharp **global** reset gate for

`Wp <= Wm + p + ell*Qx + C`,

with

`m*Qx <= Wm`,

`p^2 <= B*Qx`,

`4*mu*C <= B`,

and

`A := m*(kappa-1) - ell`.

Its global theorem requires enough quadratic headroom: for `B>0`, a finite uniform reset on an unbounded information model forces `A>0`. T-P5-131 explicitly leaves open the different case where the actual same-cell packet supplies a finite radius

`0 <= Qx <= R`.

This review closes exactly that seam. The finite radius does two things:

1. it rescues the globally impossible `A<0` branch with a finite additive reset floor;
2. even when `A>0`, if the unconstrained worst state lies outside the physical cell, it replaces the global `B/(4A)` charge by the smaller **boundary** charge.

The final checker is again square-root-free and division-free. It needs only one branch comparison involving `4*A^2*R` and two polynomial inequalities. No source, controller, Float64, P8 coverage, Lean receipt, independent verification, admission, or registry claim is made.

---

## 1. Scalar reset envelope

Retain the T-P5-131 scalar interface. Let

`Qx >= 0`,

`Wm = W-(q)`,

`Wp = W+(q)`,

`p = <g,q-q->`.

Assume

**(1.1)** `m*Qx <= Wm`, with `m>0`;

**(1.2)** `p^2 <= B*Qx`, with `B>=0`;

**(1.3)** `4*mu*C <= B`, with `mu>0`;

**(1.4)** `Wp <= Wm + p + ell*Qx + C`;

**(1.5)** `kappa>=1` and

`A := m*(kappa-1)-ell`.

As in T-P5-131,

**(1.6)**

`Wp-kappa*Wm <= p - A*Qx + C`.

The new physical premise is the same-cell radius cap

**(1.7)**

`Qx <= R`, with `R>=0`.

Everything below is about the sharp upper envelope of `p-A*Qx` on this bounded interval.

---

## 2. Where the worst state lies

For interpretation only, maximizing over the retained scalar information gives

`p <= sqrt(B*Qx)`,

so the extremal profile is

`f(q)=sqrt(B*q)-A*q`, `0<=q<=R`.

There are two regimes.

### Interior regime

If `A>0` and

`B <= 4*A^2*R`,

the unconstrained maximizer

`q*=B/(4*A^2)`

lies inside the cell. Then the sharp state-dependent charge is the same as T-P5-131:

`max f = B/(4*A)`.

### Boundary regime

If either

`A<=0`

or

`4*A^2*R <= B`,

the worst retained state occurs at the physical boundary `q=R`, and

`max f = sqrt(B*R)-A*R`.

The trusted theorem below never mentions the square root. It encodes this boundary value by a nonnegative square comparison.

At equality `B=4*A^2*R` with `A>=0`, the interior and boundary formulas coincide exactly.

---

## 3. Root-free boundary-maximality lemma

The key new algebraic fact is the following.

### Lemma A — bounded-cell linear/quadratic envelope

Assume

`0 <= q <= R`,

`p^2 <= B*q`,

`B>=0`, `R>=0`.

Let `A,T` be real and suppose

**boundary branch**

`A <= 0`

or

`4*A^2*R <= B`.

If

**(3.1)** `T>=0`,

**(3.2)** `T^2 >= B*R`,

then

**(3.3)**

`p + A*(R-q) <= T`,

hence

**(3.4)**

`p-A*q <= T-A*R`.

### Proof, branch `A<=0`

Because `R-q>=0` and `A<=0`,

`p + A*(R-q) <= p`.

If `p<=0`, (3.3) follows from `T>=0`. If `p>0`, then

`p^2 <= B*q <= B*R <= T^2`.

Since `p,T` are nonnegative, `p<=T`. Thus (3.3).

### Proof, branch `A>0` and `4*A^2*R<=B`

Put

`s := R-q >= 0`,

`y := p + A*s`.

First prove the exact endpoint-square domination

**(3.5)**

`y^2 <= B*R`.

Indeed,

`B*R-y^2`

` = (B*q-p^2) + s*(B-2*A*p-A^2*s)`.

The first term is nonnegative. It remains to show the bracket is nonnegative.

Since `B>=4*A^2*R` and `0<=s<=R`,

`B-A^2*s >= 0`.

Moreover,

`(B-A^2*s)^2 - 4*A^2*p^2`

` >= (B-A^2*s)^2 - 4*A^2*B*(R-s)`

` = B*(B-4*A^2*R) + 2*A^2*B*s + A^4*s^2`

` >= 0`.

Both `B-A^2*s` and `2*A*p` are now comparable by their squares. If `p<=0`, then

`B-2*A*p-A^2*s >= B-A^2*s >=0`.

If `p>0`, the displayed square comparison gives

`2*A*p <= B-A^2*s`,

so again the bracket is nonnegative. This proves (3.5).

If `y<=0`, then `y<=T` because `T>=0`. If `y>0`, then

`y^2 <= B*R <= T^2`

and nonnegativity gives `y<=T`. Therefore (3.3).

This proof uses only products, squares and order. No root, derivative, inverse or division is part of the trusted statement.

---

## 4. Main bounded-cell reset theorem

Let `E>=0` be the allowed additive reset floor and define the cleared boundary scalar

**(4.1)**

`S := 4*mu*E - B + 4*mu*A*R`.

Assume the boundary regime

**(4.2)**

`A<=0`

or

`4*A^2*R <= B`.

Check only

**(4.3)** `S>=0`,

**(4.4)** `S^2 >= 16*mu^2*B*R`.

Then:

### Theorem B — sharp bounded-cell knot reset

**(4.5)**

`Wp <= kappa*Wm + E`.

### Proof

Apply Lemma A with the comparison target represented in cleared form by `S`.

From (4.3)-(4.4), `4*mu>0`, and Lemma A's square argument,

**(4.6)**

`4*mu * [p + A*(R-Qx)] <= S`.

Subtract `4*mu*A*R`:

`4*mu*(p-A*Qx) <= S-4*mu*A*R`

` = 4*mu*E-B`.

Add the relocation packet `4*mu*C<=B`:

`4*mu*(p-A*Qx+C) <= 4*mu*E`.

Since `mu>0`,

`p-A*Qx+C <= E`.

Combine with (1.6) to obtain (4.5).

---

## 5. Complete sharp piecewise checker

T-P5-131 and Theorem B now give a complete bounded-cell feasibility test under the retained scalar information.

For fixed `kappa`, compute

`A=m*(kappa-1)-ell`.

### Branch I — interior worst state

Use this branch when

`0 < A`

and

`B <= 4*A^2*R`.

Then T-P5-131's parameter-free global gate is already sharp:

**(5.1)**

`A*(4*mu*E-B) >= B*mu`.

Equivalently, for interpretation only,

`E >= B/(4*mu)+B/(4*A)`.

### Branch II — physical-boundary worst state

Use this branch when

`A<=0`

or

`4*A^2*R <= B`.

Then the sharp root-free gates are (4.3)-(4.4):

`S=4*mu*E-B+4*mu*A*R >=0`,

`S^2 >= 16*mu^2*B*R`.

For interpretation only, they say

`E >= B/(4*mu)+sqrt(B*R)-A*R`.

At `B=4*A^2*R`, `A>0`, the two exact floors agree. At `A=0,B=0`, the boundary branch gives the exact endpoint `E>=0` without a separate special theorem.

Thus a rational checker never needs to approximate a square root: compare `B` with `4*A^2*R`, then check either one product inequality or one sign-plus-square pair.

---

## 6. Information-theoretic sharpness on the bounded cell

The new branch is not merely sufficient.

Under the scalar envelope (1.1)-(1.7), the boundary value is attained by taking

`Qx=R`,

`p^2=B*R` with the positive-sign extremizer,

`4*mu*C=B`,

and saturating (1.6).

Therefore any universal additive floor must satisfy

`E >= B/(4*mu)+sqrt(B*R)-A*R`

in the boundary regime. Conditions (4.3)-(4.4) are exactly the square-cleared form of that threshold. Hence the bounded-cell gate is sharp for the information retained by T-P5-130/T-P5-131.

A rational saturation family can avoid even interpretive irrationality: choose rational `r,t>=0` and set

`R=r^2`,

`B=t^2`,

`Qx=R`,

`p=t*r`.

Then `p^2=B*R` exactly, and all trusted regression arithmetic stays rational.

---

## 7. Exact quadratic-potential example: finite radius rescues `A<0`

Use the same genuine quadratic potential family as T-P5-131, but restrict it to a finite physical cell:

`Q(x)=x^2`,

`F-(x)=x^2`,

`F+(x)=3*x^2+x`.

Then

`m=1`,

`mu=3`,

`ell=2`,

`B=1`,

and for `kappa=1`,

`A=m*(kappa-1)-ell=-2 < 0`.

The post critical point is `x+=-1/6`, so

`W-(x)=x^2`,

`W+(x)=3*x^2+x+1/12`.

Globally,

`W+(x)-W-(x)=2*x^2+x+1/12`

is unbounded above, exactly as T-P5-131's `A<0` obstruction predicts.

Now restrict to the same physical cell

`x^2 <= R=1/16`, i.e. `|x|<=1/4`.

The exact maximum is at `x=1/4`:

`W+-W- <= 11/24`.

Our cleared boundary gate certifies this without roots. Set `E=11/24`. Then

`S = 4*3*(11/24) - 1 + 4*3*(-2)*(1/16)`

`  = 3`,

and

`S^2=9`

while

`16*mu^2*B*R = 16*9*1*(1/16)=9`.

So the theorem is saturated exactly.

This example is the main structural reason to keep the bounded-cell child separate from the global T-P5-131 theorem: a negative global curvature headroom is not a local impossibility once the physical radius is certified.

---

## 8. Bounded cell can also improve a positive-`A` reset

Even when `A>0`, the global T-P5-131 floor may overcharge if its unconstrained extremizer lies outside the source cell.

Take

`A=1`, `B=4`, `R=1/4`, `mu=1`.

Here

`4*A^2*R=1 < B=4`,

so the worst state is at the cell boundary, not at `B/(4A^2)=1`.

The global state-dependent charge would be

`B/(4A)=1`,

whereas the bounded-cell state-dependent charge is

`sqrt(BR)-A*R = 1-1/4 = 3/4`.

Including relocation, the exact floor drops from `2` to `7/4`.

Thus the radius packet is useful even in a nominally healthy `A>0` branch; it is not only an emergency fallback for `A<=0`.

---

## 9. Radius need not be a new primitive if pre-knot headroom already exists

Suppose the hybrid proof already knows the pre-knot storage is inside a headroom level

**(9.1)** `Wm <= H`,

while coercivity gives

`m*Qx <= Wm`, `m>0`.

If a same-cell radius `R` satisfies the division-free comparison

**(9.2)**

`H <= m*R`,

then automatically

`Qx <= R`.

Indeed,

`m*Qx <= Wm <= H <= m*R`,

and `m>0` implies `Qx<=R`.

Therefore a consumer that already propagates `Wm<=H` does not necessarily need a second independent state-radius estimator. It only needs to prove that the chosen headroom sublevel is contained in the common pre/post reference cell, encoded by `H<=mR` plus the actual cell/source coverage witness.

This is a mathematical implication only; it does **not** prove that any current Route-B headroom level is covered by the real source cell.

---

## 10. Direct connection to the dwell/headroom consumer

T-P5-131 writes the reset+dwell capacity as

`J := P*H - kappa*QN*H - P*(kappa-1)*R0`,

with `P>0`, and interprets `J/P` as the largest additive reset floor allowed by the dwell step.

The bounded-cell branch can eliminate `E` exactly as T-P5-131 did for its global branch.

Define

**(10.1)**

`S_J := 4*mu*J - B*P + 4*mu*A*R*P`.

In the boundary regime, it is sufficient and sharp under the same envelope to check

**(10.2)** `J>=0`,

**(10.3)** `S_J>=0`,

**(10.4)** `S_J^2 >= 16*mu^2*B*R*P^2`.

These are exactly (4.3)-(4.4) with `E=J/P`, after clearing the positive denominator `P`.

In the interior regime, retain T-P5-131's existing combined gate

`A*(4*mu*J-B*P) >= B*mu*P`.

Hence the hybrid checker can scan only the semantic reset multiplier `kappa` and choose the correct exact branch from the rational comparison `B ? 4*A^2*R`; it does not need any Young parameters or a square-root evaluator.

---

## 11. Lean-friendly theorem shape

The genuinely new formal leaf should be the bounded scalar helper, independent of potential calculus:

```lean
-- Schematic only; adapt naming to the existing P5 sidecar conventions.
theorem bounded_linear_quadratic_boundary
    (A B R q p T : Real)
    (hB : 0 <= B) (hR : 0 <= R)
    (hq0 : 0 <= q) (hqR : q <= R)
    (hdual : p^2 <= B*q)
    (hbranch : A <= 0 ∨ 4*A^2*R <= B)
    (hT0 : 0 <= T)
    (hTsq : B*R <= T^2) :
    p + A*(R-q) <= T := by
  ...
```

The `A>0` branch should expose the polynomial identity

```text
(B-A^2*s)^2 - 4*A^2*B*(R-s)
 = B*(B-4*A^2*R) + 2*A^2*B*s + A^4*s^2
```

with `s=R-q`.

A thin reset specialization can then state:

```lean
theorem bounded_knot_reset
    ...
    (hRadius : Qx <= R)
    (hBranch : A <= 0 ∨ 4*A^2*R <= B)
    (hS0 : 0 <= 4*mu*E-B+4*mu*A*R)
    (hSsq :
      16*mu^2*B*R <= (4*mu*E-B+4*mu*A*R)^2) :
    Wp <= kappa*Wm + E := by
  ...
```

The complementary interior theorem is already T-P5-131; do not duplicate it in Lean except as a dispatcher/corollary.

---

## 12. Fail-closed boundaries

1. **The radius must be same-cell and pre/post compatible.** A generic `Qx<=R` number from another metric, another reference key, or another chart cannot be inserted into (4.4).
2. **Do not use the boundary formula in the interior regime without the branch test.** If `A>0` and `B<4*A^2*R`, the true maximizer lies strictly inside the cell and the boundary floor underestimates the reset.
3. **Do not use the global T-P5-131 obstruction `A<0` after a finite radius has been proved.** It is an unbounded-information obstruction, not a bounded-cell impossibility theorem.
4. **The relocation packet remains a separate cost.** The radius only controls the state-dependent term; `4*mu*C<=B` is still required unless a stronger signed correlation is available.
5. **A storage headroom cap is not automatically a source-domain coverage proof.** Section 9 gives `Qx<=R` algebraically if `H<=mR`; the actual pre/post potential, Hessian and source identities must still hold throughout that same cell.
6. **No double charging.** If a downstream packet has already absorbed the reference-knot state mismatch into another signed reset term, it must not also be reintroduced through `B` here.

---

## 13. Result and next action

**Result: `CONDITIONAL_PASS / pending mathematical child`.**

The new closed mathematical interface is:

1. inherit T-P5-130/T-P5-131's reset envelope and define `A=m(kappa-1)-ell`;
2. bind a same-cell radius `Qx<=R`;
3. if `A>0` and `B<=4*A^2*R`, use the existing T-P5-131 interior/global gate;
4. otherwise use the bounded-cell root-free gate
   `S>=0`, `S^2>=16*mu^2*B*R`, with `S=4*mu*E-B+4*mu*A*R`;
5. for reset+dwell, replace `E` by the available capacity `J/P` and check the cleared `S_J` inequalities;
6. if pre-knot headroom already gives `Wm<=H`, the radius follows from `H<=mR`, provided the same-cell source coverage is independently valid.

The highest-value next source step is now very narrow: bind one actual pre/post reference knot with same-key `m,mu,B,ell`, one common quadratic radius `R` (or a headroom-to-radius inclusion `H<=mR`), and the real dwell packet. The mathematics no longer needs to reject a knot merely because `A<=0`; it can decide locally from exact rational radius/headroom data.

Still open and not claimed: actual source/reference identity, same-cell Hessian and segment coverage, controller/FD/Float64 semantics, P8 reachable-set/flowpipe, Lean/kernel compilation, independent verification by 封不觉, admission, registry eligibility, or P5/M4 parent closure.
