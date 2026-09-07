---
kind: review_result
review_id: review-T-P4-005-liuguanyi-20260906T2206
task_id: T-P4-005
source_agent: 柳冠一
claimed_at: 2026-09-06T22:06:28-06:00
created_at: 2026-09-06T22:06:28-06:00
integration_status: pending
admission_label: pending
---

# T-P4-005 — one-channel residual source-binding mathematics

## Claim and scope

`task_queue.md` explicitly assigns `T-P4-005` to 柳冠一 with boundary “one-channel residual source binding”. This review takes that assignment as the active claim and works only on the mathematical interface needed to feed one source residual channel into the already kernel-checked P4 quadratic consumer. It does **not** perform provenance/receipt/admission work and does not claim true-DH or domain coverage.

Inspected main commit at start of work:

`56795d1b67cab6da1c8a0d8f8a4ee332905b1efb`

Relevant repository objects:

- `agent_review_inbox/task_queue.md` — git blob `c15dc403d2c628232cdb49d6e6b9014f84b50111`
- `agent_review_inbox/review-T-P4-001-p4-audit.md` — git blob `a20b5e82c6726dec8f63dd5c2ebac2ddbc8ef965`
- `agent_review_inbox/review-T-P4-003-residual-normalization.md` — git blob `758471955a37f3d068b158a5d0f95fe6967603ea`
- `agent_review_inbox/review-T-P4-004-normalization-sidecar.md` — git blob `b4e9d4730aa623eae7a6810681aef2a20f6a3ca2`
- `examples/routeb_p4_next_child/P4RationalSchurAbsorption.lean` — git blob `d85c2e1c258a88355b076ac5cce322180eb827ad`
- `examples/routeb_p4_next_child/README.md` — git blob `1df2c147d8447970e1010261ed433f5bea03f39b`
- `examples/routeb_p4_next_child/REPORT.md` — git blob `a0cc002c7bdccd97f71aa07c31093b6bef6977ac`
- `examples/routeb_p4_decimal_source_binding_audit/audit_report.json` — git blob `c58aeaa8cc41e9fd5133da475e1264aa71341100`
- `docs/routeb-c2-d-normalization-audit.md`

## Mathematical observation: the current source-binding target is much stronger than necessary

The existing checked child proves nonnegativity of

```text
Q(x,y,r) = p*x^2 + 2*x*r + d*y^2
```

for the concrete channel

```text
p = 3/5,
d = 116667666666667 / 10^15,
ell = 1/100,
```

by assuming

```text
r^2 <= ell^2*y^2.
```

That premise is sufficient, but it is not the sharp mathematical interface. For fixed `r,y`, and any `p>0`, completing the square gives the exact identity

```text
Q(x,y,r)
 = (p*x+r)^2 / p + (p*d*y^2-r^2) / p.
```

Therefore:

```text
(∀ x, 0 <= Q(x,y,r))  <->  r^2 <= p*d*y^2.          (1)
```

This is both necessary and sufficient. Necessity is obtained by choosing the minimizing value `x = -r/p`; sufficiency follows because both terms in the completed-square expression are then nonnegative.

For the concrete P4 block-4 values,

```text
p*d = (3/5) * (116667666666667/10^15)
    = 350003000000001 / 5000000000000000
    = 0.0700006000000002.
```

By contrast,

```text
ell^2 = 1/10000 = 0.0001.
```

So the checked `residual_absorption` premise currently asks for a squared residual coefficient about 700 times smaller than the sharp PSD budget. In coefficient form, the exact admissible proportionality threshold is approximately

```text
sqrt(p*d) ≈ 0.2645762649974487,
```

whereas the current sufficient theorem uses `ell=0.01`.

**Consequence for T-P4-005:** the one-channel source-binding layer should not unnecessarily target `r^2 <= ell^2*y^2`. The mathematically minimal target for this scalar PMI channel is the no-square-root rational condition

```text
r_source^2 <= (350003000000001 / 5000000000000000) * y^2.   (2)
```

If the source layer can prove (2), the same quadratic nonnegativity follows even when the much stronger `1/100` envelope fails.

## Source-to-math bridge

The C2 normalization audit gives the force-side block identity

```text
l_F = (M_BB-M0_BB) a_B + M_BD a_D + r_B,
```

where the remainder `r_B` contains the C/G/controller/reference terms spelled out there. For one selected channel `i`, define

```text
m_i := ((M_BB-M0_BB) a_B)_i,
q_i := (M_BD a_D)_i,
g_i := (r_B)_i,
l_i := m_i + q_i + g_i.
```

A source enclosure can be composed entirely on the force side. If, on the same state/cell,

```text
|m_i| <= alpha*|y|,
|q_i| <= beta*|y|,
|g_i| <= gamma*|y|,
alpha,beta,gamma >= 0,
alpha+beta+gamma <= c,
```

then triangle inequality gives

```text
|l_i| <= c*|y|,
```

and hence

```text
l_i^2 <= c^2*y^2.                                    (3)
```

Thus it is enough to close the concrete source budgets with any rational `c` satisfying

```text
c^2 <= p*d.
```

This decomposition is the useful adapter theorem: it keeps `l_F` force-typed, does not rename it as an acceleration residual, and isolates exactly which source terms must be bounded to feed the P4 quadratic.

A particularly convenient rational target is any `c <= 1/4`: since

```text
(1/4)^2 = 1/16 = 0.0625 < p*d = 0.0700006000000002,
```

proving a composed one-channel force envelope `|l_i| <= (1/4)|y|` is already sufficient. This is still 25 times looser in coefficient than the current `1/100` envelope and avoids introducing an irrational square root into Lean/source receipts.

## Exact obstruction: additive residual bias cannot satisfy the global P4 envelope

Equation (1) also exposes a structural obstruction that should be checked before spending effort on source receipts.

At `y=0`, universal nonnegativity requires

```text
r^2 <= p*d*0 = 0,
```

therefore `r=0`.

Equivalently, if the source residual channel contains a nonzero additive bias at any admissible state with `y=0`, then no constant choice of positive `p,d` can make `Q(x,0,r)` nonnegative for every `x`: choosing `x=-r/p` yields

```text
Q(-r/p,0,r) = -r^2/p < 0.
```

So a global source-binding proof must establish one of the following, explicitly:

1. the selected source residual vanishes when the associated `y` vanishes, with a quantitative proportional envelope such as (2)/(3); or
2. the physical domain excludes `y=0` and supplies a lower bound on `|y|`; or
3. the P4 quadratic/interface is changed to include an additional constant/slack budget capable of absorbing an additive source bias.

A mere absolute bound `|r| <= epsilon` with `epsilon>0` is **not** sufficient for the present universal scalar PMI.

## Minimal theorem statements for formalization

The highest-value Lean child is the sharp equivalence, independent of source provenance:

```text
schur_residual_nonnegative_iff
  (p d r y : ℝ) (hp : 0 < p) :
  (∀ x : ℝ, 0 <= p*x^2 + 2*x*r + d*y^2)
    <-> r^2 <= p*d*y^2
```

A second small bridge composes source-term envelopes:

```text
one_channel_residual_envelope
  (m remote drift y alpha beta gamma c : ℝ)
  (hm : |m| <= alpha*|y|)
  (hr : |remote| <= beta*|y|)
  (hg : |drift| <= gamma*|y|)
  (hsum : alpha + beta + gamma <= c) :
  (m + remote + drift)^2 <= c^2*y^2
```

with nonnegativity hypotheses on the envelope coefficients added explicitly if Lean needs them for monotonicity. A concrete corollary can use `c=1/4` and the exact rational `p,d` above to feed the existing P4 quadratic.

These are appropriate handoffs to 苏梦辰 / 臭屁猪. No compile result is claimed in this review; the proof above is ordinary exact-real algebra and should be formalized independently.

## What is proved here / what remains open

Mathematical progress:

- derived the **necessary and sufficient** one-channel residual condition for the present scalar P4 quadratic;
- identified a rational sufficient budget `c=1/4`, much less conservative than the existing `ell=1/100` source target;
- supplied an exact force-side decomposition-to-envelope bridge;
- proved the zero-`y` obstruction showing why a nonzero additive source bias cannot be hidden inside the current universal PMI.

Still open and intentionally not claimed:

- binding `l_i` to a pinned canonical Julia/DH execution over a covered cell;
- actual interval bounds for the three source-side pieces `m_i`, `q_i`, `g_i`;
- Float64/outward-rounding semantics and regularization witness;
- domain coverage and P4/M4 admission;
- kernel compilation of the proposed new lemmas.

## Recommended next action

Formalization agents should first prove `schur_residual_nonnegative_iff` and its concrete `c=1/4` corollary. In parallel, a math/source worker can try to bound the actual selected force-residual decomposition against `|y|` using the relaxed rational budget `1/4`. If the source residual does not vanish on the `y=0` slice, stop trying to force it into the current envelope and instead introduce an explicit slack/bias term in the P4 interface.
