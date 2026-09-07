kind: review_result

review_id: review-T-P5-004-kuangmanmozun-20260906T2153
task_id: T-P5-004
source_agent: 狂蛮魔尊
created_at: 2026-09-06T21:53:00-06:00
result_class: mathematical_child_proved
admission: pending_formalization_and_binding

# T-P5-004 — dissipative residual-power inequality child

## Goal

Extract a reusable mathematical closure step from the existing P5 energy/power
lane. This result deliberately starts *after* the exact energy/power identity and
before source/domain binding. It answers the following question:

> If the power derivative consists of a coercive damping contribution plus a
> bounded residual forcing contribution, what is the smallest exact scalar
> inequality needed to retain dissipation and obtain a strict negativity
> threshold?

Relevant existing mathematical interface:

- `agent_review_inbox/review-T-P5-002-energy-child.md` isolates the exact
  Newton–Euler / Christoffel energy-power child.
- `examples/routeb_dh_power_binding/DHPowerBinding.lean` exposes the abstract
  residual power as a dot product.

No claim below depends on Float64/DH source equality, receipt freshness,
provenance, registry state, or Route-B admission.

## 1. Vector-to-scalar reduction

Let `v` be the velocity/state-rate vector, `D` a damping operator, and `r` a
residual forcing vector. Assume an already-established power identity of the
form

```text
E_dot = - <v, D v> + <v, r>.
```

Assume for constants `delta > 0` and `epsilon >= 0`:

```text
<v, D v> >= delta * ||v||^2,
||r|| <= epsilon.
```

Cauchy–Schwarz gives

```text
<v, r> <= ||v|| ||r|| <= epsilon ||v||.
```

Therefore, with `x := ||v|| >= 0` and `y := E_dot`,

```text
(*)    y <= -delta*x^2 + epsilon*x.
```

Everything below is an exact consequence of this one scalar inequality.

## 2. Sharp global upper bound

From the nonnegative square

```text
(2*delta*x - epsilon)^2 >= 0
```

we obtain

```text
4*delta^2*x^2 - 4*delta*epsilon*x + epsilon^2 >= 0.
```

Combining with `(*)` and `delta > 0` yields

```text
THEOREM A:
4*delta*y <= epsilon^2.
```

Equivalently,

```text
y <= epsilon^2 / (4*delta).
```

For `epsilon >= 0` this constant is sharp: equality in the quadratic upper
bound occurs at

```text
x = epsilon / (2*delta).
```

This is the best uniform upper bound obtainable from `(*)`, but it discards the
negative quadratic term and is therefore not the best form for downstream
stability closure.

## 3. Retained-dissipation bound

Using instead

```text
(delta*x - epsilon)^2 >= 0,
```

we have

```text
delta^2*x^2 - 2*delta*epsilon*x + epsilon^2 >= 0.
```

Again combining with `(*)` gives the division-free statement

```text
THEOREM B:
2*delta*y <= -delta^2*x^2 + epsilon^2.
```

Since `delta > 0`, this is equivalent to

```text
y <= -(delta/2)*x^2 + epsilon^2/(2*delta).
```

This form deliberately sacrifices a factor `1/2` of damping in exchange for a
constant forcing floor, while preserving a coercive negative quadratic term.
It is the useful form for an ultimate-bound / absorbing-region argument.

Equality in the Young step occurs when

```text
delta*x = epsilon.
```

## 4. Parameterized Young family

The previous retained-dissipation estimate is one member of a full exact
family. For any `eta` with

```text
0 < eta < delta,
```

use

```text
(2*eta*x - epsilon)^2 >= 0.
```

Then

```text
THEOREM C:
4*eta*y <= -4*eta*(delta-eta)*x^2 + epsilon^2.
```

Equivalently,

```text
y <= -(delta-eta)*x^2 + epsilon^2/(4*eta).
```

Thus downstream code may choose `eta` to trade retained damping against the
forcing floor. `eta = delta/2` recovers Theorem B.

## 5. Exact strict-negativity threshold

The unsplit quadratic is stronger for detecting when the derivative is
strictly negative:

```text
-delta*x^2 + epsilon*x = x*(epsilon - delta*x).
```

Hence, if

```text
epsilon >= 0,
x > epsilon/delta,
```

then `x > 0` and `epsilon - delta*x < 0`, so

```text
THEOREM D:
y < 0.
```

At the threshold `x = epsilon/delta`, `(*)` only gives `y <= 0`; strict
negativity cannot be concluded without additional information. This boundary
is therefore exact for the information contained in `(*)`.

## 6. Counterexample / sharpness warning

A common but false strengthening would be

```text
y <= -delta*x^2 + C
```

with `C = 0` for nonzero residual `epsilon`.

Take the scalar equality model

```text
y = -delta*x^2 + epsilon*x
```

with `delta > 0`, `epsilon > 0`, and `x = epsilon/(2*delta)`.
Then

```text
y = epsilon^2/(4*delta) > 0.
```

Therefore no argument using only coercivity `delta` and residual norm bound
`epsilon` can prove global strict decay when `epsilon > 0`. One must either:

1. prove `epsilon = 0`,
2. establish a state-dependent residual bound stronger than a constant norm
   envelope,
3. add another negative term, or
4. settle for an absorbing/ultimate-bound conclusion.

This is a genuine mathematical obstruction, not a provenance or checker issue.

## 7. Lean-friendly theorem statements

The division-free forms avoid field normalization and should be extremely small
formalization targets.

Suggested scalar child 1:

```lean
theorem residual_power_global_bound
    {delta epsilon x y : ℝ}
    (hdelta : 0 < delta)
    (hy : y <= -delta * x^2 + epsilon * x) :
    4 * delta * y <= epsilon^2 := by
  have hs : 0 <= (2 * delta * x - epsilon)^2 := sq_nonneg _
  nlinarith
```

Suggested scalar child 2:

```lean
theorem residual_power_dissipative_bound
    {delta epsilon x y : ℝ}
    (hdelta : 0 < delta)
    (hy : y <= -delta * x^2 + epsilon * x) :
    2 * delta * y <= -(delta^2) * x^2 + epsilon^2 := by
  have hs : 0 <= (delta * x - epsilon)^2 := sq_nonneg _
  nlinarith
```

Suggested parameterized child:

```lean
theorem residual_power_young_family
    {delta eta epsilon x y : ℝ}
    (heta : 0 < eta)
    (hy : y <= -delta * x^2 + epsilon * x) :
    4 * eta * y <= -4 * eta * (delta - eta) * x^2 + epsilon^2 := by
  have hs : 0 <= (2 * eta * x - epsilon)^2 := sq_nonneg _
  nlinarith
```

Note: `eta < delta` is not required for the algebraic inequality itself; it is
required only when interpreting `delta-eta` as positive retained damping.

Suggested strict-decay child:

```lean
theorem residual_power_negative_outside
    {delta epsilon x y : ℝ}
    (hdelta : 0 < delta)
    (hepsilon : 0 <= epsilon)
    (hx : epsilon / delta < x)
    (hy : y <= -delta * x^2 + epsilon * x) :
    y < 0 := by
  -- field/order normalization + nlinarith
  ...
```

These snippets are theorem proposals, not claimed compile evidence in this
review.

## 8. Downstream mathematical obligations

This child isolates the exact two quantities the physical lane must now supply:

1. a coercivity constant `delta > 0` satisfying
   `<v,Dv> >= delta ||v||^2` on the target domain;
2. a residual envelope `epsilon` satisfying `||r|| <= epsilon` on the same
   domain.

Once those are available, the power-to-decay step itself is no longer a
mathematical bottleneck. Conversely, without these two bounds, repeatedly
rechecking the abstract energy identity cannot close the stability argument.

For a stronger asymptotic-decay theorem, the highest-value next mathematical
question is whether the current residual can be bounded proportionally to the
state,

```text
||r|| <= rho ||v||
```

with `rho < delta`. In that case

```text
E_dot <= -(delta-rho)||v||^2,
```

giving genuine global/local exponential-type dissipation at the energy level
instead of an ultimate-bound floor.

## 9. Handoff

Recommended formalization handoff: `苏梦辰` or `臭屁猪`.

Minimal formalization order:

1. Theorem A (global sharp quadratic bound),
2. Theorem B (retained-dissipation bound),
3. Theorem C (parameterized family),
4. Theorem D (strict negativity threshold),
5. only then add an inner-product-space wrapper consuming coercivity and
   Cauchy–Schwarz.

Recommended verifier handoff after formalization: `封不觉`.

## Conclusion

A reusable mathematical closure has been proved:

```text
E_dot <= -delta ||v||^2 + epsilon ||v||
```

implies both the sharp global bound

```text
E_dot <= epsilon^2/(4 delta)
```

and the retained-dissipation bound

```text
E_dot <= -(delta/2)||v||^2 + epsilon^2/(2 delta),
```

with strict decay outside `||v|| > epsilon/delta`.

The remaining bottleneck is no longer this inequality manipulation; it is the
substantive mathematical/source-domain work needed to produce a valid coercivity
constant `delta` and residual envelope `epsilon` for the actual model.
