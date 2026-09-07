---
kind: review_result
task_id: T-P4-020
review_id: T-P4-020-kuangmanmozun-20260907T0752
source_agent: 狂蛮魔尊
created_at: 2026-09-07T07:52:00-06:00
integration_status: pending
admission: pending
claim_status: self_claimed
inspected_commit: bf7397a9a82e1142bb7c95b1eb8e1e938c28d9e8
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-019-kuangmanmozun-20260907T0550.md
depends_on:
  - T-P4-007
  - T-P4-014
  - T-P4-016
  - T-P4-017
  - T-P4-019
---

# Review Result — T-P4-020

## 0. Claim / smallest open mathematical child

At the inspected commit, no `T-P4-020` entry/result was discoverable in the current queue/repository search. I therefore self-claim the next disjoint inequality child: **joint consumption of one P4 Schur channel by a transverse state-relative remainder and a genuinely additive execution bias at the same time**.

This is not a new source-binding claim. It only closes a mathematical bookkeeping gap between `T-P4-014` (transverse reserve) and `T-P4-019` (additive bias): their separate allowances cannot in general be spent independently.

## 1. Problem

Let

`Q(x,y,z) = p x^2 + 2 x (a y + gamma z + b) + d y^2 + h z^2 + s`,

where:

- `a y` is the already-aggregated same-coordinate residual;
- `gamma z` is one effective transverse state-relative residual;
- `h z^2` is the positive quadratic reserve paying for that transverse term;
- `b` is a genuinely additive execution bias with `|b| <= B`;
- `s` is a **real independent nonnegative constant reserve** already present in the certificate (not invented slack).

Define

`P := p h - gamma^2`,

`Omega := p d h - a^2 h - d gamma^2 = d P - a^2 h`.

For the strictly coercive case assume `p>0`, `d>0`, `h>0`, and `Omega>0`. Then automatically `P>0`.

The question is: after paying the transverse term, what exact reserve remains for `b`?

## 2. Exact division-free SOS identity

A direct `ring` identity is

`P h^2 Omega Q`
`= P h Omega (h z + gamma x)^2`
`  + h Omega (P x + a h y + b h)^2`
`  + h^2 (Omega y - a b h)^2`
`  + P h^2 (Omega s - d h b^2)`.

Derivation is a two-stage completion, which also explains the constants.

First,

`h Q = (h z + gamma x)^2 + Q2`,

where

`Q2 = P x^2 + 2 a h x y + d h y^2 + 2 b h x + h s`.

Now apply the additive-bias completion from `T-P4-019` to `Q2` with

`p' = P`, `a' = a h`, `d' = d h`, `b' = b h`, `s' = h s`.

Its determinant is

`Delta' = P d h - a^2 h^2 = h Omega`,

which yields the displayed identity with no division or square root.

## 3. Sharp joint budget

If `B>=0`, `|b|<=B`, and

**`d h B^2 <= Omega s`,**

then `Q(x,y,z)>=0` for every `x,y,z` and every admissible `b`.

The condition is sharp. If `Omega s < d h B^2` and `B>0`, choose `b=B` and

`x = -B d h / Omega`,

`y = a B h / Omega`,

`z = gamma B d / Omega`.

Then all three square terms in the identity vanish and

`Q = s - d h B^2/Omega < 0`.

Therefore, in the strictly coercive case, the exact uniform criterion supplied by only these magnitude data is

**`Omega s >= d h B^2`.**

No independent Young-parameter tuning can improve it.

### Boundary `Omega=0`

At `Omega=0` the state quadratic is only semidefinite. A nonzero additive bias still cannot be uniformly absorbed: the null direction can be taken proportional to

`(x,y,z) = (1, -a/d, -gamma/h)`,

and the linear term `2 b x` makes the form unbounded below when `b != 0`.

Thus spending the transverse budget exactly to the Schur boundary leaves **zero additive tolerance**.

## 4. Normalized transverse cost: one shared curvature budget

Write the transverse dual cost as

`kappa := gamma^2 / h`.

Since

`Omega/h = p d - a^2 - d kappa`,

the sharp condition becomes

**`d B^2 <= (p d - a^2 - d kappa) s`.**

This is the main reusable interface. It says same-coordinate, transverse, and additive errors all consume the **same Schur curvature**.

When `s>0`, the equivalent budget-simplex form is

`a^2 + d kappa + d B^2/s <= p d`,

or, after dividing by `p d`,

`a^2/(p d) + kappa/p + B^2/(p s) <= 1`.

The three terms are therefore not independent allowances.

This also extends the aggregate bookkeeping of `T-P4-016`: if a source/checker has already compressed several transverse remainders to a single certified dual cost `KAPPA`, then the correct remaining additive condition is

`d B^2 <= (p d - a^2 - d KAPPA) s`,

not the conjunction of the old transverse-only and additive-only inequalities checked separately.

## 5. Concrete counterexample: separate checks can both pass while the combined form fails

Take the fully rational example

`p=d=h=1`, `a=0`, `gamma=1/2`, `B=b=1`, `s=1`.

The transverse-only check from `T-P4-014` passes:

`d gamma^2 = 1/4 <= (p d-a^2) h = 1`.

The additive-only check from `T-P4-019` (ignoring the transverse term) also passes:

`d B^2 = 1 <= (p d-a^2) s = 1`.

But jointly

`Omega = 1-1/4 = 3/4`,

so the true condition would require `1 <= 3/4`, which fails.

Indeed choose

`x=-4/3`, `y=0`, `z=2/3`.

Then

`Q = -1/3 < 0`.

Hence **checking the full transverse allowance and the full additive allowance independently is mathematically unsound**. This is a concrete failure witness, not just a conservative-budget warning.

## 6. Correct canonical block-4 specialization

Use the corrected canonical block-4 values from `T-P4-017`:

`p4 = 3/5`,

`d4 = 116667666666667 / 10^15`,

`p4*d4 = 350003000000001 / 5000000000000000`.

### 6.1 Total same-coordinate coefficient `a=1/4`

Then

`Delta4 := p4*d4-(1/4)^2`
`        = 37503000000001 / 5000000000000000`.

For aggregate transverse cost `KAPPA` and additive envelope `B`, the exact joint budget is

**`583338333333335 * B^2`
`<= (37503000000001 - 583338333333335*KAPPA) * s`.**

Checks:

- `KAPPA=0` recovers `T-P4-019`: `37503000000001*s >= 583338333333335*B^2`;
- `B=0` recovers the transverse ceiling from `T-P4-014/016`: `583338333333335*KAPPA <= 37503000000001`;
- if `KAPPA` is spent all the way to that ceiling, the right-hand curvature is zero, so any `B>0` is impossible regardless of finite `s`.

### 6.2 Canonical `kc=1/20` alone (`a=1/20`)

Before spending extra same-coordinate allowance,

`Delta4,kc = 337503000000001 / 5000000000000000`.

The exact joint budget is

**`583338333333335 * B^2`
`<= (337503000000001 - 583338333333335*KAPPA) * s`.**

Thus keeping the same-coordinate envelope small preserves curvature simultaneously for both transverse and additive execution errors.

## 7. Formalizable theorem decomposition

The core identity is a pure `ring` theorem:

```lean
theorem joint_transverse_additive_square_identity
    (p d a gamma h x y z b s : ℝ) :
    let P := p*h-gamma^2
    let Omega := p*d*h-a^2*h-d*gamma^2
    P*h^2*Omega *
      (p*x^2 + 2*x*(a*y+gamma*z+b) + d*y^2 + h*z^2 + s)
      = P*h*Omega*(h*z+gamma*x)^2
        + h*Omega*(P*x+a*h*y+b*h)^2
        + h^2*(Omega*y-a*b*h)^2
        + P*h^2*(Omega*s-d*h*b^2) := by
  ring
```

Minimal forward consumer:

```lean
-- hypotheses: 0<p, 0<d, 0<h, 0<Omega,
-- 0<=B, |b|<=B, d*h*B^2 <= Omega*s
-- conclusion: 0 <= Q
```

Recommended additional theorem/corollaries:

1. `joint_transverse_additive_schur` — forward inequality from the identity;
2. `joint_transverse_additive_sharpness` — explicit witness above when the budget fails;
3. `separate_budget_checks_not_composable` — the rational `(1,1,1,0,1/2,1,1)` counterexample giving `Q=-1/3`;
4. `block4_joint_execution_budget` — exact rational corollary for `a=1/4`;
5. `block4_kc_only_joint_execution_budget` — exact rational corollary for `a=1/20`.

No new matrix library or source model is needed for this child.

## 8. Failure branches / boundaries

1. `s` must be a real reserve already present in the target certificate or a separately proved uniform positive floor. One may not add a constant merely to make the theorem close.
2. `KAPPA` must be the **aggregate** transverse dual cost after the non-double-counting rules of `T-P4-016`; per-remainder full allowances cannot be summed naively.
3. If `s=0`, the joint theorem forces `B=0` in the strictly coercive regime, recovering the no-additive-slack obstruction.
4. If `KAPPA` reaches the state-only Schur boundary, additive tolerance is also zero. Therefore source lanes must not spend transverse and additive margins as if they were separate budgets.
5. This theorem does not prove physical values of `KAPPA`, `B`, or `s`, and does not replace remote-mass transfer, source semantic binding, or domain coverage.
6. No P4/M4 status, registry, provenance, receipt, or admission state is changed here.

## 9. Recommended next step

The source/execution lane should report a **single per-channel tuple** `(a, KAPPA, B, s)` rather than separate pass/fail flags for relative, transverse, and additive errors. The consumer should check the one joint inequality

`d B^2 <= (p d-a^2-d KAPPA) s`.

If there is no genuine constant reserve, set `s=0` and fail closed on any `B>0`. If an execution remainder can instead be proved state-relative, move it into `KAPPA` before taking a global additive envelope.

**Result:** `T-P4-014` and `T-P4-019` do not provide independently spendable allowances. Their sharp composition is the joint curvature budget above. Status remains `pending`;待封不觉独立验证 / 待梁智炜收割与最终整合。
