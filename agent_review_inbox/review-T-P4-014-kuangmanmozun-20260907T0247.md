---
kind: review_result
review_id: review-T-P4-014-kuangmanmozun-20260907T0247
task_id: T-P4-014
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T02:38:00-06:00
created_at: 2026-09-07T02:47:00-06:00
inspected_commit: d14eed2eef80a97ed356efbf6615c36bdc3aa06a
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_sharp_relative_plus_transverse_schur_and_keep_runtime_bias_out_of_one_coordinate_envelope_without_a_reserve
---

# T-P4-014 — sharp relative-plus-transverse Schur reserve after the execution-residual split

## Scope

`T-P4-013` gave the sharp same-coordinate composition rule for normalized `kc` plus a residual satisfying `|e| <= beta |y|`.  The newer execution decomposition `T-P4-007` shows that the actual block residual also contains terms such as `DeltaM*a`, `DeltaC`, centered `DeltaG`, `delta_ctrl`, and the solve defect `-s_B`; those terms are not currently known to vanish on the `y=0` slice.

This child answers the next inequality question without taking over their source bounds:

> If one part of the residual is relative to the Schur coordinate `y`, while another part is only controlled by a different coordinate/reserve, what is the **sharp** extra positive quadratic cost needed for universal absorption?

The answer is an exact 3-variable Schur formula.  It also proves that an unchanged one-coordinate P4 block cannot robustly absorb a genuinely additive execution bias from a magnitude bound alone.

Inputs inspected:

- `review-T-P4-013-kuangmanmozun-20260907T0145.md` for the normalized `kc` and same-coordinate coefficient budget;
- `review-T-P4-007-liuguanyi-20260907T0212.md` for the execution-lift residual ledger and zero-slice obstruction;
- `examples/routeb_p4_sharp_schur_sidecar/P4SharpSchur.lean` through the constants recorded in `T-P4-013`.

No source/IEEE bound, remote-mass claim, P3 mass geometry, formalization, validation, or P4/M4 closure is asserted.

## 1. Generic robust problem

Let

```text
r = c*y + e + b,
|e| <= beta*|y|,
|b| <= gamma*|z|,
```

with

```text
p > 0,
c,beta,gamma >= 0.
```

The scalar P4 block is enlarged by a transverse positive reserve `h*z^2`:

```text
Q = p*x^2 + 2*x*r + d*y^2 + h*z^2.                       (1)
```

Define

```text
a     := c + beta,
Delta := p*d - a^2.                                       (2)
```

The interesting regime is `Delta>0`.  This means the same-coordinate relative residual has **not** spent the entire sharp Schur margin.

By triangle inequality,

```text
|r| <= a*|y| + gamma*|z|.                                (3)
```

Put `Y=|y|`, `Z=|z|`.  The exact identity

```text
Delta * [p*d*Y^2 + p*h*Z^2 - (a*Y + gamma*Z)^2]
 = (Delta*Y - a*gamma*Z)^2
   + p*(Delta*h - d*gamma^2)*Z^2                         (4)
```

is obtained by expansion using `Delta=p*d-a^2`.

Hence, if

```text
Delta > 0,
d*gamma^2 <= Delta*h,                                    (5)
```

then the bracket in (4) is nonnegative, so

```text
r^2 <= p*(d*y^2 + h*z^2).                                (6)
```

Completing the square in `x` gives

```text
Q = (p*x+r)^2/p + d*y^2 + h*z^2 - r^2/p >= 0.             (7)
```

Thus (5) is a source-independent sufficient condition for absorption.

## 2. The reserve coefficient is sharp under only the two magnitude envelopes

Condition (5) is not a loose Young bound.  It is necessary for a universal theorem under only

```text
|e| <= beta|y|,
|b| <= gamma|z|.
```

Assume `Delta>0` and take the same-sign extremizer

```text
z = 1,
y = a*gamma/Delta,
e = beta*y,
b = gamma.
```

Then `r=a*y+gamma`.  Choose the minimizing

```text
x = -r/p.
```

A direct calculation gives

```text
Q = h - d*gamma^2/Delta.                                  (8)
```

Therefore if

```text
Delta*h < d*gamma^2,                                      (9)
```

this admissible choice makes `Q<0`.

So, for `Delta>0`, the exact information-only robust threshold is

```text
h_min = d*gamma^2 / Delta.                                (10)
```

Equivalently, the division-free condition `d*gamma^2 <= Delta*h` is sharp.

This is the main new bridge: a remainder that is not `y`-relative can still be consumed if it is relative to a second typed coordinate `z` carrying enough positive quadratic reserve; otherwise the one-coordinate Schur block cannot absorb it robustly.

## 3. Additive-bias/slack corollary

Take `z=1`, `gamma=B`, and rename `h=sigma`.  If

```text
|b| <= B,
```

then the smallest state-independent positive slack that makes the robust block nonnegative is

```text
sigma_min = d*B^2 / Delta.                                (11)
```

The Lean-friendly condition is simply

```text
d*B^2 <= Delta*sigma.                                     (12)
```

This sharpens the zero-slice obstruction in `T-P4-007`:

- if the actual P4 polynomial supplies **no** independent positive slack (`sigma=0`), then (12), together with `d>0` and `Delta>0`, forces `B=0`;
- therefore a nonzero uniform bound on `delta_ctrl`, `solveDefect`, or another execution term does **not** by itself justify putting that term inside the unchanged one-coordinate residual envelope;
- to keep the current P4 architecture one needs either a vanishing/correlation theorem, a bound relative to another state coordinate with its own positive quadratic term, or an explicitly budgeted slack elsewhere in the certificate.

This is stronger than saying merely that the remainder must vanish at one equilibrium: it quantifies exactly what a second quadratic reserve must pay when no such vanishing theorem is available.

## 4. Failure boundaries

The parameter boundary is equally useful for excluding bad proof routes.

### `Delta < 0`

Even with `b=0`, the relative residual itself exceeds the sharp Schur budget.  Taking `e=beta*y` with the same sign and letting `|y|` grow makes the minimized block negative.  No finite constant slack can repair an unrestricted quadratic instability.

### `Delta = 0`

The relative term exactly saturates the Schur budget.  If `a*gamma>0`, then after eliminating `x` the remaining expression contains a nonzero linear cross direction in `Y,Z`; no finite state-independent slack gives a universal bound on unrestricted `y`.

Consequently, **transverse/additive robustness requires strict Schur reserve `Delta>0`**.  Spending the relative coefficient all the way to the sharp boundary destroys the ability to tolerate an independent execution remainder.

## 5. Concrete block-4 reserve after the normalized `kc`

From `T-P4-013`, the abstract block-4 constants are

```text
p4 = 3/5,
d4 = 116667666666667 / 10^15,
p4*d4 = 350003000000001 / 5000000000000000.              (13)
```

If the normalized `kc` plus all same-coordinate remainder is kept inside the existing quarter envelope,

```text
c = 1/100,
beta = 6/25,
a = c+beta = 1/4.                                         (14)
```

Then the **unused sharp Schur reserve** is still positive:

```text
Delta4
 = p4*d4 - (1/4)^2
 = 37503000000001 / 5000000000000000
 > 0.                                                       (15)
```

So `1/4` does not actually exhaust the true block-4 Schur budget; it leaves about `0.0075006` in squared coefficient units.

For a transverse error

```text
|b4| <= gamma*|z|,
```

condition (5) becomes exactly

```text
583338333333335 * gamma^2
 <= 37503000000001 * h.                                    (16)
```

Equivalently,

```text
h >= (583338333333335 / 37503000000001) * gamma^2
  ~= 15.5544445333 * gamma^2.                              (17)
```

If the transverse reserve is normalized to `h=1`, the square-only source target is

```text
gamma^2 <= 37503000000001 / 583338333333335
         ~= 0.06429030608,                                 (18)
```

corresponding numerically to `gamma ~= 0.2535553`; the rational squared condition (18), not the square root, is the preferable formal interface.

For a genuine uniform bias `|b4|<=B` with an external scalar slack `sigma`, the exact condition is the same arithmetic:

```text
583338333333335 * B^2
 <= 37503000000001 * sigma.                                (19)
```

If no such `sigma` exists in the actual certificate, (19) reduces to `B=0`; one must not reinterpret the unused value of `Delta4` as a free constant offset.  `Delta4` only converts a **quadratic reserve in another variable** into cross-residual capacity.

## 6. Why preserving reserve can be better than maximizing the relative envelope

The exact maximum same-coordinate coefficient is `sqrt(p4*d4) ~= 0.2645763`, whereas the current quarter consumer uses `0.25`.  One could enlarge the relative envelope beyond `1/4`, but (10) shows the tradeoff:

```text
transverse cost multiplier = d / (p*d-a^2).               (20)
```

This multiplier diverges as `a^2 -> p*d`.

For block 4:

- with normalized `kc` alone (`a=1/100`), the additive-slack multiplier is about `1.66905`;
- after spending the relative budget up to `a=1/4`, it is about `15.55444`.

Therefore, once `T-P4-007` exposes non-`y`-relative execution terms, maximizing the same-coordinate coefficient is not automatically optimal.  Retaining some Schur curvature can be much more valuable because it buys finite cross-coordinate robustness.

## 7. Minimal formalizable theorem statements

A square-root-free core theorem is:

```lean
theorem relative_plus_transverse_schur
    (p d c beta gamma h x y z e b : R)
    (hp : 0 < p)
    (hc : 0 <= c) (hbeta : 0 <= beta) (hgamma : 0 <= gamma)
    (hDelta : 0 < p*d - (c+beta)^2)
    (he : |e| <= beta*|y|)
    (hb : |b| <= gamma*|z|)
    (hreserve : d*gamma^2 <= (p*d-(c+beta)^2)*h) :
    0 <= p*x^2 + 2*x*(c*y+e+b) + d*y^2 + h*z^2
```

The key algebra helper can be made completely division-free by setting

```text
a = c+beta,
Delta = p*d-a^2,
Y=|y|,
Z=|z|
```

and formalizing identity (4) with `ring`; the remainder is square nonnegativity plus `nlinarith`.

Two useful corollaries should remain separate:

```lean
-- z = 1, gamma = B, h = sigma
additive_bias_with_slack

-- p=3/5, d=d4, c=1/100, beta=6/25
block4_quarter_plus_transverse
```

A separate sharpness theorem may use the explicit extremizer from section 2.  The positive theorem does not require division or square roots.

## 8. Remaining source obligations and routing

This review does not decide which execution residual in `T-P4-007` should be assigned to which `z`/reserve.  That is the next source-to-math step.  The routing rule is now precise:

1. terms proved `y`-relative may enter `beta`;
2. exact-real remote `M_BD a_D` stays on the independent mass-metric route `T-P4-012`;
3. a runtime/solve term only bounded in absolute magnitude needs an explicit scalar slack, or it fails the unchanged block robustly;
4. a runtime/solve term bounded by another state coordinate can enter this new transverse theorem provided the certificate supplies the matching `h*z^2` reserve;
5. do not spend `a` up to `sqrt(p*d)` if an independent transverse remainder still needs absorption, because the required reserve blows up at that boundary.

Recommended next formalization is the division-free identity (4), `relative_plus_transverse_schur`, and the exact block-4 arithmetic corollary (16).  Source/IEEE agents can then bind `DeltaM/DeltaC/DeltaG/delta_ctrl/s` to either a same-coordinate, transverse-coordinate, or explicit-bias class without changing the theorem.

Admission remains `pending`; this is a mathematical inequality/obstruction child only, awaiting formalization, independent validation, and 梁智炜 integration.
