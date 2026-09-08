# Review result — T-P5-051 exact near-singular compatibility penalty

- task_id: `T-P5-051`
- agent: `狂蛮魔尊`
- source_agent: `狂蛮魔尊`
- status: `pending mathematical child`
- scope: inequalities / coercivity boundary / sharp affine completion / counterexample

## 0. Purpose

`T-P5-050` classifies the **exactly singular** PSD 2×2 completion problem.  The missing neighboring question is quantitative:

> when `H` is positive definite but `det(H)` is tiny, what exactly measures the price of being slightly incompatible with the rank-one singular limit?

The answer is an exact trace/adjugate decomposition.  It yields a radical-free budget gate and shows that merely having `adj(H)b -> 0` is not enough: the correct threshold is

`||adj(H)b|| = O(sqrt(det H))`.

Everything below is algebraic over an ordered field except the interpretation as a normed Euclidean 2-space.

---

## 1. Setup

Let

`H = [[p,q],[q,s]]`,

with

`tau := p+s > 0`,

`delta := ps-q^2 > 0`.

Thus `H` is positive definite.  Put

`A := adj(H) = [[s,-q],[-q,p]]`,

`b := (b4,b5)^T`,

`k := A b`,

`N := b^T A b = s b4^2 - 2q b4 b5 + p b5^2`.

For the affine quadratic

`J(u) := -u^T H u - b^T u`,

the ordinary sharp completion cost is

`C_* = (1/4) b^T H^{-1} b = N/(4 delta)`.

The point of this note is to rewrite this in a way that remains meaningful as `delta -> 0+`.

---

## 2. Two 2×2 identities

Because this is dimension two,

`A = tau I - H`.

Cayley-Hamilton gives

`H^2 - tau H + delta I = 0`.

Hence

`A^2 = (tau I-H)^2 = tau A - delta I`.      (2.1)

Applying (2.1) to `b` gives the key numerator identity

`||k||^2 = b^T A^2 b`

`          = tau b^T A b - delta ||b||^2`

`          = tau N - delta ||b||^2`.          (2.2)

Equivalently,

**`tau N = ||adj(H)b||^2 + delta ||b||^2`.**   (2.3)

This is completely polynomial and uses no inverse, eigenvalue, or square root.

---

## 3. Exact trace-defect decomposition

Substitute (2.3) into `C_*=N/(4delta)`:

**THEOREM T-P5-051-A**

For `tau>0`, `delta>0`,

`C_* = ||b||^2/(4 tau)`

`      + ||adj(H)b||^2/(4 tau delta)`.          (3.1)

Both terms are nonnegative.

Interpretation:

- `||b||^2/(4tau)` is exactly the rank-one-compatible trace cost from `T-P5-050`;
- `||adj(H)b||^2/(4 tau delta)` is the exact **incompatibility penalty**.

So the singular theorem is not a disconnected endpoint.  The SPD cost splits into the singular trace cost plus a nonnegative defect that blows up precisely when compatibility is lost too fast.

The decomposition is sharp because it is an identity, not an estimate.

---

## 4. Division-free exact budget gate

Let `C >= 0` be a proposed completion budget.  From (3.1),

`C_* <= C`

if and only if

**`||k||^2 <= delta (4 tau C - ||b||^2)`.**    (4.1)

Similarly,

`C_* < C`

if and only if

**`||k||^2 < delta (4 tau C - ||b||^2)`.**     (4.2)

No division is needed in the checker.  In particular, strict PASS automatically forces the ordinary trace budget `4tau C > ||b||^2`; that condition does not need to be added as a separate assumption.

This gate has a useful geometric reading:

`available trace slack × determinant`

must dominate

`compatibility defect squared`.

The determinant is therefore not merely a denominator nuisance; it is exactly the scale converting a compatibility residual into budget consumption.

---

## 5. Polynomial completion identity behind the consumer

There is also a denominator-free exact-square identity.  Since `AH=HA=delta I`,

`(2Hu+b)^T A (2Hu+b)`

`= 4 delta u^T H u + 4 delta b^T u + N`.       (5.1)

Because `A` is positive definite when `H` is, the right side is nonnegative, yielding

`J(u) <= N/(4delta)=C_*`.

Combining (5.1) with (2.3) and the budget gate (4.1) gives a Lean-friendly path from rational coefficient checks directly to the universal affine-completion inequality, without ever constructing `H^{-1}`.

---

## 6. P5-specialized strict gates

The singular child `T-P5-050` exposed the two trace-only strict budgets

`200 ||b||^2 < (109-r) tau`

and

`600 ||g||^2 < (109-r) tau`.

For `delta>0`, these are only the **base-slack** parts.  The exact SPD gates are stronger by the incompatibility penalty.

### 6.1 Quarter channel

Using `C=(109-r)/800`, (4.2) is exactly

**`delta [(109-r)tau - 200||b||^2]`
`    > 200 ||adj(H)b||^2`.**                   (6.1)

### 6.2 Parameter channel

Using `C=(109-r)/2400`, (4.2) is exactly

**`delta [(109-r)tau - 600||g||^2]`
`    > 600 ||adj(H)g||^2`.**                   (6.2)

Thus a P5 checker can remain exact-rational all the way through the nearly singular regime.  It should not replace these by a determinant lower bound unless that extra conservatism is deliberately desired.

At `delta -> 0`, (6.1)/(6.2) also make the singular compatibility condition emerge automatically: unless `adj(H)b` or `adj(H)g` collapses at least on the `sqrt(delta)` scale, no fixed positive budget can survive.

---

## 7. Sharp near-singular threshold

From (3.1), for a family with `tau` bounded below away from zero and `||b||` bounded,

`C_*` stays bounded whenever

`||adj(H)b||^2 / delta`

stays bounded.

Conversely, if `C_*` and `tau` are bounded above, then (3.1) forces

`||adj(H)b||^2 <= 4 tau C_* delta`,

so

`||adj(H)b|| = O(sqrt(delta))`.

Hence `sqrt(det H)` is the exact compatibility scale.  Requiring `adj(H)b = O(delta)` is unnecessarily strong; requiring only `adj(H)b -> 0` is too weak.

---

## 8. Counterexamples and exact regressions

### 8.1 Fixed incompatible direction blows up

Let, for `eps>0`,

`H_eps = diag(eps,1)`,

`b=(1,0)`.

Then

`tau=1+eps`, `delta=eps`,

`adj(H_eps)=diag(1,eps)`,

`k=(1,0)`.

The exact cost is

**`C_*(eps)=1/(4eps) -> +infinity`.**

This is the ordinary singular-kernel obstruction seen quantitatively before the determinant reaches zero.

### 8.2 Compatible singular limit has no blow-up

For the same matrix, take

`b=(0,1)`.

Then

`k=(0,eps)`

and

`C_*(eps)=1/4` exactly for every `eps>0`.

The trace-defect split is

`1/[4(1+eps)] + eps/[4(1+eps)] = 1/4`.

As `eps -> 0`, this lands exactly on the `T-P5-050` singular cost for `H_0=diag(0,1)`, `b=(0,1)`.

### 8.3 `k -> 0` by itself is NOT enough

Take

`H_eps = diag(eps^4,1)`,

`b_eps=(eps,0)`.

Then

`delta=eps^4`,

`k_eps=(eps,0) -> 0`,

but

**`C_*(eps)=1/(4 eps^2) -> +infinity`.**

So a checker or asymptotic argument that records only `adj(H)b -> 0` can be catastrophically wrong.

### 8.4 Critical `sqrt(delta)` scaling is sufficient and sharp

Take

`H_eps = diag(eps^2,1)`,

`b_eps=(eps,0)`.

Then

`delta=eps^2`,

`||k_eps||=eps=sqrt(delta)`,

and

**`C_*(eps)=1/4`**

for every `eps>0`.

This demonstrates that the `sqrt(delta)` threshold cannot be strengthened universally.

---

## 9. Important failed shortcuts

### Failure A — trace gate alone

Near singularity, checking only

`c ||b||^2 < (109-r)tau`

is not enough.  The incompatible example `diag(eps,1), b=(1,0)` can satisfy a fixed trace gate while its true completion cost diverges like `1/eps`.

### Failure B — compatibility residual merely tends to zero

`adj(H_eps)b_eps -> 0` does not imply bounded completion cost; §8.3 is an explicit counterexample.

### Failure C — determinant lower bound as a mathematical necessity

A uniform lower bound `delta>=delta0>0` is sufficient but not necessary.  §8.2 and §8.4 remain uniformly bounded while `delta->0`.  The correct object is the coupled ratio

`||adj(H)b||^2/delta`.

### Failure D — blindly apply the nonzero singular gate at `delta>0`

At positive determinant there is no exact kernel compatibility requirement.  A small nonzero incompatibility can be paid for.  What matters is whether the exact defect fits the determinant-scaled budget (4.1)/(4.2).

---

## 10. Lean-ready child statements

Suggested small sidecar lemmas:

1. `adj_sq_eq_trace_mul_adj_sub_det_mul_one`

   For 2×2 `H`, prove `adj(H)^2 = trace(H) • adj(H) - det(H) • I`.

2. `adj_bias_norm_identity`

   Under the scalar-coordinate definitions,

   `||adj(H)b||^2 + delta||b||^2 = tau (b^T adj(H)b)`.

3. `spd_completion_polynomial_identity`

   `(2Hu+b)^T adj(H)(2Hu+b) = 4delta(u^T H u+b^T u)+b^T adj(H)b`.

4. `spd_completion_cost_trace_defect_decomposition`

   For `tau>0`, `delta>0`, derive (3.1).

5. `spd_completion_budget_iff_defect_gate`

   For `C>=0`, prove weak and strict versions of (4.1)/(4.2).

6. `p5_quarter_near_singular_gate`

   Specialize to (6.1).

7. `p5_parameter_near_singular_gate`

   Specialize to (6.2).

8. Regression lemmas for the four diagonal families in §8.

Most of the algebra should close with `ring`; positivity only enters when consuming the completion square and when clearing `tau,delta`.

---

## 11. Handoff / architectural consequence

For a unified 2×2 affine-completion implementation, the natural branch structure is now:

- `delta>0`: use the exact defect gate of `T-P5-051`;
- `delta=0`, `tau>0`: use the pivot-free compatibility classifier/cost of `T-P5-050`;
- `delta=0`, `tau=0`: finite iff `b=0`, again from `T-P5-050`.

This closes the mathematical discontinuity between the SPD and singular branches without imposing an artificial determinant floor.

A useful source-level diagnostic is therefore to emit not only `delta`, but also

`||adj(H)b||^2`

(or its exact rational enclosure), because that is the quantity controlling whether a nearly singular cell is genuinely dangerous.

---

## 12. Status boundary

This is a **pending mathematical child** only.

Not claimed here:

- concrete P5 source binding,
- correctness of any computed `H,b,g`,
- Float64/FD/controller or true-DH seam,
- P8 coverage,
- Lean compilation/kernel admission,
- P5/M4 or registry closure.

`T-P5-049` remains untouched and owned by its existing agent.