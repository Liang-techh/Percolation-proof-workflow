---
kind: review_result
review_id: review-T-P5-071-signed-two-cycle-contact-kuangmanmozun-20260908T0556
task_id: T-P5-071-SIGNED-TWO-CYCLE-CONTACT
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T05:35:00-06:00
created_at: 2026-09-08T05:56:00-06:00
claim_commit: 1a6af2236e892fbf2fbf856dda05387ecc791ff4
inspected_commits:
  - 628211d6ff10ed09c10eb0380539048ec24c0459
  - a3aca25105c5523ed4c0d98ef2a7c3aa8353e14a
  - 3a4784366f29802d446f6c859ab528c99dd49a07
  - 6b4685d7e8952aa50de8f284247f96076987cb37
parent_tasks:
  - T-P5-070-TRIANGULAR-MULTICONTACT-CHART
  - T-P5-066-ZERO-SURFACE-RECENTERING
  - T-P5-068-RECENTERED-UNIT-C11
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a source-independent two-contact cyclic recentering theorem after T-P5-070; use the opposite-orientation branch before any small-gain rejection, then use the strict unsigned small-gain branch; treat failure of both branches as NOT_APPLICABLE rather than a proof of noninvertibility; keep concrete source binding, Lean validation, coverage and admission separate
---

# T-P5-071 — signed two-cycle contact chart: negative feedback without small gain

## 0. Mathematical seam and result

T-P5-070 closes simultaneous recentering for an acyclic/triangular dependency graph. It also gives the exact cyclic linear obstruction

`xi = [[1,-a],[-b,1]] x`, `det = 1-ab`,

showing that scalar simple-root certificates alone do not imply a unique simultaneous chart when a directed cycle is present.

The smallest remaining cyclic problem is therefore a **two-contact cycle**. This review proves a source-independent exact classification with two robust branches:

1. **unsigned / no orientation information:** a strict small-gain gate gives a unique chart and a division-free inverse budget;
2. **opposite root orientation / negative feedback:** no small-gain gate is needed at all. The cycle is globally one-sided coercive on the certified core, even if the available cross-Lipschitz product is greater than one.

The second branch is the main new result. It prevents a checker from rejecting a safe negative-feedback cycle merely because an absolute-value gain product is large.

This review is mathematics only. It does not inspect or claim concrete deployed factors, Float64/libm, controller/FD semantics, P8 coverage, receipt/provenance, Lean/kernel compilation, admission, parent closure, or registry mutation.

---

## 1. Two scalar root maps

Let

`I1 = [c1-H1,c1+H1]`, `I2 = [c2-H2,c2+H2]`,

with `H1,H2>0`, and let `(Y,d)` be a base-parameter metric space.

Assume T-P5-066/T-P5-070 have already produced continuous scalar root maps

`rho1 : I2 × Y -> I1`,

`rho2 : I1 × Y -> I2`.

Thus for each fixed transverse coordinate and base parameter, the corresponding source factor has exactly one simple root in its active interval.

Assume exact nonnegative root-variation charges

`a,b,p,q >= 0`

such that

**(1.1)**

`|rho1(z,y)-rho1(z',y')| <= a |z-z'| + p d(y,y')`,

**(1.2)**

`|rho2(x,y)-rho2(x',y')| <= b |x-x'| + q d(y,y')`.

T-P5-070 already shows how such charges arise division-free from source cross-variation bounds.

Define the cyclic recentered coordinates

**(1.3)**

`xi1 = x1 - rho1(x2,y)`,

`xi2 = x2 - rho2(x1,y)`.

The problem is to decide when `(xi1,xi2,y)` determines a unique `(x1,x2)` and to retain an exact quantitative inverse budget.

---

## 2. Common product core gives existence before uniqueness

Assume uniform root-displacement envelopes

**(2.1)**

`|rho1(z,y)-c1| <= delta1`,

`|rho2(x,y)-c2| <= delta2`,

with

**(2.2)** `0 <= delta1 < H1`, `0 <= delta2 < H2`.

Set

**(2.3)** `K1=H1-delta1`, `K2=H2-delta2`.

Take any chart target satisfying

**(2.4)** `|xi1|<=K1`, `|xi2|<=K2`.

For fixed `(xi,y)`, define the scalar self-map on `I1`

**(2.5)**

`F(s) = xi1 + rho1(xi2 + rho2(s,y), y)`.

For every `s in I1`, the inner argument obeys

`|xi2 + rho2(s,y)-c2| <= K2+delta2 = H2`,

so it lies in `I2`. Then the outer displacement obeys

`|F(s)-c1| <= K1+delta1 = H1`,

so `F(s) in I1`.

Because the root maps are continuous, `F:I1->I1` is continuous. Any continuous self-map of a closed real interval has a fixed point: at the left endpoint `l`, `F(l)-l>=0`; at the right endpoint `u`, `F(u)-u<=0`; the intermediate value theorem applies.

If `x1=F(x1)` and

**(2.6)** `x2 = xi2 + rho2(x1,y)`,

then both equations (1.3) hold.

### Theorem 2.1 — cyclic core existence

Under only continuity and the displacement packet (2.1)-(2.4), **every** `xi` in the product core `[-K1,K1]×[-K2,K2]` has at least one physical preimage in `I1×I2`.

No small-gain or orientation assumption is required for existence.

The hard issue in a cycle is uniqueness/stability, not bare existence.

---

## 3. Baseline unsigned small-gain theorem

Take two chart/source triples `(x,xi,y)` and `(x',xi',y')` satisfying (1.3). Write

`X1=|x1-x1'|`, `X2=|x2-x2'|`,

`Z1=|xi1-xi1'|`, `Z2=|xi2-xi2'|`,

`D=d(y,y')`.

From (1.1)-(1.3), triangle inequality gives

**(3.1)** `X1 <= Z1 + a X2 + p D`,

**(3.2)** `X2 <= Z2 + b X1 + q D`.

Eliminating `X2` from (3.1),

`X1 <= Z1 + a(Z2+bX1+qD)+pD`,

hence

**(3.3)**

`(1-ab) X1 <= Z1 + a Z2 + (p+a q)D`.

Similarly,

**(3.4)**

`(1-ab) X2 <= b Z1 + Z2 + (b p+q)D`.

Therefore:

### Theorem 3.1 — unsigned two-cycle small-gain inverse

If

**(3.5)** `ab<1`,

then the cyclic chart is injective on the source box and, together with Theorem 2.1, has a unique inverse on the common product core.

The exact cleared inverse budget is (3.3)-(3.4). A trusted checker does not need to divide by `1-ab`.

For fixed `y` and equal chart coordinates (`Z1=Z2=D=0`), strict positivity of `1-ab` forces `X1=X2=0`.

For simultaneous contact centers `xi=0`, two base parameters satisfy

**(3.6)**

`(1-ab)|r1(y)-r1(y')| <= (p+a q)D`,

**(3.7)**

`(1-ab)|r2(y)-r2(y')| <= (b p+q)D`.

So the same gate controls both chart inversion and transport of the coupled contact center.

---

## 4. Source-cleared form with no normalized division

Suppose instead the source packet is kept in the T-P5-070 cleared form

**(4.1)**

`mu1 |rho1(z,y)-rho1(z',y')| <= C12 |z-z'| + L1 D`,

**(4.2)**

`mu2 |rho2(x,y)-rho2(x',y')| <= C21 |x-x'| + L2 D`,

with `mu1,mu2>0` and all constants nonnegative.

Define the determinant-style reserve

**(4.3)**

`Delta = mu1*mu2 - C12*C21`.

Starting directly from the two cleared triangle inequalities and eliminating one physical difference gives

**(4.4)**

`Delta X1`
`<= mu1*mu2 Z1 + C12*mu2 Z2`
` + (mu2*L1 + C12*L2) D`,

and

**(4.5)**

`Delta X2`
`<= C21*mu1 Z1 + mu1*mu2 Z2`
` + (C21*L1 + mu1*L2) D`.

Hence the completely division-free source gate is simply

**(4.6)** `C12*C21 < mu1*mu2`.

This is preferable when the source adapter already has exact `Cij` and `mui`; the normalized `a,b` branch is equivalent when the charges are tight, and remains a sound sufficient gate when they are rounded upward rational witnesses.

---

## 5. Signed root orientation

Absolute-value gains throw away a crucial datum: the **orientation** of each root graph.

Say `rho1` is nondecreasing in its transverse coordinate if

`z<=z' -> rho1(z,y)<=rho1(z',y)`

for fixed `y`, and nonincreasing if the inequality reverses. Define the same for `rho2`.

Call the two-cycle **negative feedback** when the root maps have opposite orientation:

- `rho1` nondecreasing and `rho2` nonincreasing; or
- `rho1` nonincreasing and `rho2` nondecreasing.

Then, for fixed `(eta,y)`, the scalar composition

**(5.1)**

`Phi_{eta,y}(s) = rho1(eta + rho2(s,y), y)`

is nonincreasing.

Define

**(5.2)** `G_{eta,y}(s)=s-Phi_{eta,y}(s)`.

If `s<t`, nonincrease of `Phi` gives

`Phi(s)>=Phi(t)`, so

**(5.3)**

`G(t)-G(s)`
`= (t-s) + (Phi(s)-Phi(t))`
`>= t-s`.

Thus `G` is not merely strictly increasing: it has a **unit one-sided coercivity reserve** independent of the size of `a*b`.

Equivalently,

**(5.4)** `|G(t)-G(s)| >= |t-s|`.

This is the mechanism missing from the unsigned small-gain estimate.

---

## 6. Main theorem: negative feedback removes the small-gain denominator

Keep the notation `X1,X2,Z1,Z2,D` from Section 3 and assume opposite root orientation.

For the first coordinate, write

`G_{xi2,y}(x1)=xi1`,

`G_{xi2',y'}(x1')=xi1'`.

Using (5.4) with the first parameter packet frozen,

`X1`
`<= |G_{xi2,y}(x1)-G_{xi2,y}(x1')|`.

Insert the second equation and use triangle inequality:

`X1`
`<= Z1`
` + |Phi_{xi2,y}(x1')-Phi_{xi2',y'}(x1')|`.

By (1.1)-(1.2), at the fixed physical argument `x1'`,

`|Phi_{xi2,y}(x1')-Phi_{xi2',y'}(x1')|`
`<= a Z2 + (p+a q)D`.

Therefore

**(6.1)**

`X1 <= Z1 + a Z2 + (p+a q)D`.

Running the symmetric scalar elimination through the second coordinate gives

**(6.2)**

`X2 <= b Z1 + Z2 + (b p+q)D`.

### Theorem 6.1 — negative-feedback two-cycle chart

Assume the root maps have opposite orientation. Then:

1. every chart target in the common product core has a preimage by Theorem 2.1;
2. that preimage is unique;
3. the exact inverse bounds are (6.1)-(6.2);
4. **no condition `ab<1` is required**.

The same result holds for the simultaneous center `xi=0`:

**(6.3)**

`|r1(y)-r1(y')| <= (p+a q)D`,

**(6.4)**

`|r2(y)-r2(y')| <= (b p+q)D`.

Comparing with (3.6)-(3.7), the entire dangerous denominator `1-ab` disappears.

This is not a heuristic sign cancellation. It follows from an exact monotonicity/coercivity inequality.

---

## 7. Cleared negative-feedback budget

Combining Theorem 6.1 with the source-cleared variation packet (4.1)-(4.2) yields a particularly clean division-free form:

**(7.1)**

`mu1*mu2 X1`
`<= mu1*mu2 Z1 + C12*mu2 Z2`
` + (mu2*L1 + C12*L2)D`,

**(7.2)**

`mu1*mu2 X2`
`<= C21*mu1 Z1 + mu1*mu2 Z2`
` + (C21*L1 + mu1*L2)D`.

Compare (7.1)-(7.2) with the unsigned formulas (4.4)-(4.5):

- unsigned branch left coefficient: `mu1*mu2 - C12*C21`;
- negative-feedback branch left coefficient: `mu1*mu2`.

The right-hand numerators are identical.

So exact sign/orientation information recovers **all** of the cross-product coercivity loss, not merely part of it.

---

## 8. Deriving root orientation from the original source factors

The root-orientation packet does not need to be guessed numerically.

Consider one scalar factor `h(s,z,y)` with sign `sigma` and a unique root `rho(z,y)`. Assume its active coordinate satisfies the T-P5-070 signed lower secant condition, so `sigma*h(·,z,y)` is strictly increasing in `s`.

For fixed `y` and `z<z'`, suppose the source proves one of the exact cross-monotonicity signs:

### Cross-up branch

**(8.1)**

`sigma*(h(s,z',y)-h(s,z,y)) >= 0`

for every active `s`.

At `s=rho(z,y)`, the old fiber is zero, so the new fiber is nonnegative. Since the new fiber is strictly increasing in the active variable and vanishes at `rho(z',y)`, this forces

**(8.2)** `rho(z',y) <= rho(z,y)`.

Thus cross-up in the source factor makes the root graph **nonincreasing**.

### Cross-down branch

If instead

**(8.3)**

`sigma*(h(s,z',y)-h(s,z,y)) <= 0`,

then the same argument gives

**(8.4)** `rho(z',y) >= rho(z,y)`.

Thus cross-down makes the root graph **nondecreasing**.

### Theorem 8.1 — source cross sign to root orientation

The root orientation is the opposite of the signed transverse orientation of the source factor. For a two-cycle, the two minus signs cancel, so the root maps have opposite orientation exactly when the two certified source cross orientations are opposite.

This gives the source adapter a concrete route to the negative-feedback branch without differentiating the implicit root map.

---

## 9. Exact regression: negative feedback with gain product greater than one

Take

`I1=I2=[-1,1]`, no base parameter, and source factors

**(9.1)**

`h1(s,z)=s-z^3/2`,

`h2(s,x)=s+x^3/2`.

Both active derivatives are exactly `1`, so `mu1=mu2=1`.

The scalar roots are

**(9.2)**

`rho1(z)=z^3/2`,

`rho2(x)=-x^3/2`.

On `[-1,1]`,

`|z^3-z'^3| <= 3|z-z'|`,

so each root map is Lipschitz with exact rational charge

**(9.3)** `a=b=3/2`.

Hence

**(9.4)** `ab=9/4>1`.

The unsigned small-gain gate rejects this packet.

However `rho1` is nondecreasing and `rho2` is nonincreasing, so the signed negative-feedback theorem applies with no size condition.

Moreover

`|rho1|,|rho2| <= 1/2`,

so `delta1=delta2=1/2` and the common chart core is nontrivial:

**(9.5)** `|xi1|<=1/2`, `|xi2|<=1/2`.

Every point in that chart core has a unique physical preimage.

At the simultaneous center,

`x1=x2^3/2`, `x2=-x1^3/2`,

so

`x1 = -x1^9/16`,

hence

`x1*(1+x1^8/16)=0`.

The only real center is exactly `(0,0)`.

This is a direct counterexample to the rule

> `cross-Lipschitz product >= 1 => cyclic chart unsafe`.

That rule is mathematically false once orientation is known.

---

## 10. Strict small-gain boundary is sharp in the unsigned class

Take the same interval `[-1,1]` and

**(10.1)** `rho1(z)=z`, `rho2(x)=x`.

Then `a=b=1`, so `ab=1`, and the center equations are

`x1=x2`, `x2=x1`.

Every point on the diagonal is a simultaneous center. The cyclic chart is singular.

Therefore the robust unsigned gate cannot be weakened from

`ab<1`

to

`ab<=1`.

The zero reserve `1-ab=0` is genuinely boundary-only.

---

## 11. The `1-ab` blow-up is quantitatively sharp

Let

**(11.1)** `rho1(z)=z`,

**(11.2)** `rho2(x)=(99/100)x`.

Then

`a=1`, `b=99/100`,

and

**(11.3)** `1-ab=1/100`.

Compare the origin with

**(11.4)**

`x=(1,99/100)`.

Its chart coordinate is

`xi1 = 1-99/100 = 1/100`,

`xi2 = 99/100-(99/100)*1 = 0`.

Thus for the first component

`(1-ab)X1 = (1/100)*1 = 1/100`

and

`Z1+aZ2 = 1/100`.

Equality holds in (3.3). Likewise equality holds in (3.4).

Hence the inverse condition number really can grow like

`1/(1-ab)`

as the positive-feedback boundary is approached. The denominator is not an artifact of the proof.

---

## 12. Failure of small gain is NOT an impossibility certificate

Even without opposite orientation, `ab>1` does not decide the mathematics.

### Unique same-orientation example

Take

`rho1(z)=z`,

`rho2(x)=x^3/2`

on `[-1,1]`.

The root maps are both nondecreasing. Their Lipschitz charges may be taken as

`a=1`, `b=3/2`,

so `ab=3/2>1`.

The center equation becomes

`x=x^3/2`,

or

`x(1-x^2/2)=0`.

The only solution in `[-1,1]` is `x=0`.

### Multiple-center same-orientation example

Now take

`rho1(z)=z`,

`rho2(x)=x^3`.

Again both maps are nondecreasing, and `ab` may be bounded by `3>1`. But the center equation

`x=x^3`

has three solutions in the box:

`x=-1,0,1`.

Therefore, when the root orientations are not opposite and the strict small-gain gate fails, the correct generic checker result is

**`NOT_APPLICABLE`**,

not `FAIL_NONINVERTIBLE`.

A source-specific determinant, monotone-operator, interval-Newton, degree, or implicit-function certificate may still prove uniqueness.

---

## 13. Recommended decision layer

For a certified two-contact cycle, the math checker should use this order:

### Branch A — signed negative feedback

If exact root orientation is opposite, return

`PASS_SIGNED_TWO_CYCLE`

and consume (6.1)-(6.2) or the cleared form (7.1)-(7.2).

Do **not** test `ab<1` first. Doing so would reject the exact regression in Section 9.

### Branch B — unsigned strict small gain

If orientation is absent or same, but

`ab<1`

or directly

`C12*C21 < mu1*mu2`,

return

`PASS_SMALL_GAIN_TWO_CYCLE`

with the cleared reserve formulas (3.3)-(3.4) or (4.4)-(4.5).

### Branch C — unresolved cyclic regime

If neither Branch A nor Branch B applies, return

`NOT_APPLICABLE_CYCLIC`

unless another independently proved cyclic certificate is supplied.

In particular:

- `ab=1` is not a strict PASS boundary;
- `ab>1` is not by itself a counterexample;
- a directed cycle is not itself a mathematical failure;
- source sign information should never be discarded before the gain test.

---

## 14. Lean-friendly theorem decomposition

The formal leaves are small and mostly ordered-ring arguments.

### Leaf A — interval self-map fixed point

```text
continuous_Icc_selfmap_has_fixed_point
  (F : Icc l u -> Icc l u)
  (hcont : Continuous F)
  : exists x, F x = x
```

This can be proved by IVT from `F(l)>=l` and `F(u)<=u`; no multidimensional Brouwer theorem is needed.

### Leaf B — antitone coercivity

```text
sub_antitone_strongMono_one
  (hanti : Antitone Phi)
  : |(t-Phi t) - (s-Phi s)| >= |t-s|
```

### Leaf C — unsigned cleared small-gain inverse

```text
two_cycle_small_gain_cleared
  (h1 : mu1*X1 <= mu1*Z1 + C12*X2 + L1*D)
  (h2 : mu2*X2 <= mu2*Z2 + C21*X1 + L2*D)
  (hDelta : C12*C21 < mu1*mu2)
  :
    (mu1*mu2-C12*C21)*X1
      <= mu1*mu2*Z1 + C12*mu2*Z2
         + (mu2*L1+C12*L2)*D
    /\
    (mu1*mu2-C12*C21)*X2
      <= C21*mu1*Z1 + mu1*mu2*Z2
         + (C21*L1+mu1*L2)*D
```

### Leaf D — negative-feedback inverse

```text
two_cycle_antitone_inverse_bound
  (hopposite : OppositeOrientation rho1 rho2)
  (root variation packets)
  :
    X1 <= Z1 + a*Z2 + (p+a*q)*D
    /\
    X2 <= b*Z1 + Z2 + (b*p+q)*D
```

### Leaf E — source cross sign to root orientation

```text
root_antitone_of_active_increasing_cross_up
root_monotone_of_active_increasing_cross_down
```

Each consumes only unique roots, active signed monotonicity, and the transverse sign inequality.

### Regression leaves

```text
identity_two_cycle_boundary_nonunique
negative_cubic_two_cycle_unique_without_small_gain
same_orientation_ab_gt_one_can_be_unique
same_orientation_ab_gt_one_can_be_nonunique
small_gain_near_boundary_sharp_99_100
```

No Lean compilation is claimed here.

---

## 15. Remaining boundary

**Closed mathematically in this child:**

- existence of a two-cycle inverse on a common recentered product core;
- strict unsigned small-gain uniqueness and exact inverse reserve;
- source-cleared determinant reserve `mu1*mu2-C12*C21`;
- opposite-orientation / negative-feedback uniqueness with no small-gain condition;
- exact removal of the cross-product denominator in the negative-feedback branch;
- root-orientation derivation from source cross-monotonicity signs;
- sharp `ab=1` boundary counterexample for the unsigned class;
- sharp near-boundary `1/(1-ab)` conditioning example;
- counterexamples proving `ab>1` can be either unique or nonunique and therefore must not be treated as a generic impossibility certificate.

**Still open / not claimed:**

- whether any deployed P5 contact graph actually contains a certified two-cycle;
- concrete source factors, root maps, cross signs, `C12,C21,mu1,mu2,L1,L2` or displacement envelopes;
- cycles with three or more nodes;
- two-cycles lacking both opposite orientation and strict small gain;
- interval-Newton / degree / monotone-operator / source-specific determinant certificates for that unresolved regime;
- multiple-root clusters from T-P5-067;
- C1,1 unit regularity beyond consuming T-P5-068 after a unique chart is established;
- reduced-packet bounds after full cyclic substitution;
- Float64/libm/FD/controller/solve semantics;
- P8/ODE coverage;
- Lean/kernel/comparator/receipt/provenance;
- independent validation by 封不觉;
- P5/P8/M4 parent closure, admission, or registry mutation.

The key advance is that **a two-contact directed cycle is not automatically a small-gain problem**. If the certified root graphs form negative feedback, the scalar composition is antitone and `Id-Phi` has a unit coercivity reserve. The absolute gain product may exceed one by an arbitrary amount without creating the positive-feedback singularity measured by `1-ab`.