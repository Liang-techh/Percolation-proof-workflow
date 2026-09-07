---
kind: review_result
review_id: review-T-P4-036.2-guyuefangyuan-robust-phase-cells-20260907T1434
task_id: T-P4-036.2
source_agent: 古月方源
created_at: 2026-09-07T14:34:00-06:00
integration_status: pending
admission: pending
inspected_head: 971644898f6961b01803d04dc5b8edf6aa796491
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-036.2-exact-real-child-codex-20260907.md
  - agent_review_inbox/review-T-P4-036.2-range-reduction-lemma-codex-20260907.md
  - robot_final/dhport_lib.jl
proposed_integration_target: O2 exact interval/range-reduction math leaf between angle-formation error and libm enclosure
---

# T-P4-036.2 — all-12 robust quarter-turn cells from q-box + angle error

## Decision

The exact interval/range-reduction mathematics can be made substantially smaller than the current conditional row contract.

For all six theta rows and all six alpha rows, the source phases are only `k in {-1,0,+1}`.  Therefore the exact-real reduction does **not** need a rational enclosure for `pi`, a CSV reduced-row hypothesis, or a Taylor polynomial row witness.  It is an exact cancellation followed by three quarter-turn identities.

More importantly, the same argument gives a robust interface for the deployed path: if the upstream angle-formation leaf supplies only an absolute real-lift error `eps` for the formed Float64 argument, then this review turns that error directly into an exact-real `sin/cos` target cell.  The libm leaf may then prove that the actual machine result encloses the exact `Real.sin/Real.cos` value at that formed argument.  This avoids modeling libm's internal range-reduction algorithm inside the mathematical leaf.

This is a mathematical result only.  No Float64/libm semantics, authoritative coverage receipt, D1/D2/D3 propagation, or O2 closure is claimed.

## Canonical phase data

The source-indexed phase vectors already recorded by the existing exact-real child are

```text
k_theta = ( 0, -1, +1,  0, +0,  0)
k_alpha = (-1,  0, +1, -1, +1,  0)
```

(the `+0` is only typographical emphasis; it is zero).  The source semantics are

```text
theta_i = q_i + k_theta[i] * pi/2
alpha_i =       k_alpha[i] * pi/2
```

with `q_i in [-3/20,3/20]` for theta and `q=0` for alpha.  The canonical source hash recorded by the parent reviews is

```text
AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
```

for `robot_final/dhport_lib.jl` / the state-bound mirror.  This review uses the hash only as the inspected source key; it does not infer runtime semantics from it.

## 1. Exact reduction is symbolic cancellation

For any real `q` and `k in {-1,0,+1}`, define

```text
x = q + k*pi/2,
r = x - k*pi/2.
```

Then by ring arithmetic over the exact real `pi`,

```text
r = q.
```

For alpha, set `q=0`, hence `r=0` exactly.

Consequences:

1. the exact-real range-reduction theorem needs no `hpi : pi in piBox` premise;
2. it needs no row-wise `reducedRowSound` premise;
3. the P3 CSV may remain a source-indexed artifact, but its reduced endpoints are not a mathematical premise for this layer;
4. all approximation/rounding of `pi/2` belongs to the upstream Float64 angle-formation leaf, where it can be summarized by an error budget.

This is stronger and cleaner than a theorem whose exact-real statement carries a rational `pi` enclosure despite subtracting the same exact quarter-turn center.

## 2. Base trigonometric cell needs no sine Taylor remainder

Let `b >= 0` and `|r| <= b`.  Two global inequalities suffice:

```text
|sin r| <= |r|,
1 - r^2/2 <= cos r <= 1.
```

Since `r^2 <= b^2`, define

```text
c(b) = 1 - b^2/2.
```

Then

```text
-b <= sin r <= b,
c(b) <= cos r <= 1.                    (BASE)
```

No small-angle assumption such as `b<=1` is needed for validity; if `b` is large the cosine lower bound merely becomes conservative.

For the declared exact theta box `b=3/20`,

```text
c(3/20) = 1 - (9/400)/2 = 791/800.
```

Thus

```text
-3/20 <= sin q <= 3/20,
791/800 <= cos q <= 1.
```

This strictly improves the previous theta2 draft's cosine-transport interval `[-2409/16000,2409/16000]`: the transported sine coordinate can use `[-3/20,3/20]` directly.  The cubic sine remainder is unnecessary for this purpose.

## 3. Exact quarter-turn transport

Using only the exact identities

```text
sin(r - pi/2) = -cos r,
cos(r - pi/2) =  sin r,
sin(r + pi/2) =  cos r,
cos(r + pi/2) = -sin r,
```

(BASE) gives three phase cells.

For phase `k=0`:

```text
sin(r) in [-b,b]
cos(r) in [c(b),1]
```

For phase `k=-1`:

```text
sin(r-pi/2) in [-1,-c(b)]
cos(r-pi/2) in [-b,b]
```

For phase `k=+1`:

```text
sin(r+pi/2) in [c(b),1]
cos(r+pi/2) in [-b,b].
```

These formulas are exact and retain a single scalar radius `b` rather than twelve unrelated interval hypotheses.

## 4. All 12 exact-real source rows from q-box alone

Set `b=3/20`, `c=791/800` for theta.  In link order 1..6:

```text
row          phase     sin interval                 cos interval
--------------------------------------------------------------------------
theta_1       0        [-3/20, 3/20]               [791/800, 1]
theta_2      -1        [-1, -791/800]              [-3/20, 3/20]
theta_3      +1        [791/800, 1]                [-3/20, 3/20]
theta_4       0        [-3/20, 3/20]               [791/800, 1]
theta_5       0        [-3/20, 3/20]               [791/800, 1]
theta_6       0        [-3/20, 3/20]               [791/800, 1]
```

For alpha, `q=0`, hence `b=0`, `c=1` and the cells collapse to exact points:

```text
row          phase     sin                         cos
-------------------------------------------------------
alpha_1      -1        -1                           0
alpha_2       0         0                           1
alpha_3      +1         1                           0
alpha_4      -1        -1                           0
alpha_5      +1         1                           0
alpha_6       0         0                           1
```

Therefore the full 12-row **exact-real** trig contract is derivable from the q-box and phase table alone.  A future integration may widen/replace the CSV trig endpoints with these proved cells, or separately prove that any retained narrower CSV endpoints are sound; it must not use the CSV endpoint claims as premises for this theorem.

## 5. Robust bridge from Float64 angle formation to exact trig target

The more useful deployed-path theorem is parametric in the upstream angle-formation error.

Let the ideal source angle be

```text
x = q + k*pi/2,
```

and let `xhat` be the exact real value obtained by decoding the actually formed Float64 argument.  Assume the upstream `.1` leaf proves

```text
|xhat - x| <= eps,
eps >= 0,
|q| <= a.
```

Define the **mathematical** reduced variable

```text
rhat = xhat - k*pi/2.
```

Then exactly

```text
rhat - q = xhat - (q + k*pi/2),
```

so

```text
|rhat-q| <= eps,
|rhat| <= a + eps.
```

Set

```text
b = a + eps,
c = 1 - b^2/2.
```

The phase-cell formulas in Section 3 now enclose exact `sin(xhat), cos(xhat)`.

For theta row `i`, take `a=3/20` and its own certified `eps_theta_i`:

```text
b_theta_i = 3/20 + eps_theta_i,
c_theta_i = 1 - b_theta_i^2/2.
```

For alpha row `i`, take `a=0` and its storage/formation error `eps_alpha_i`:

```text
b_alpha_i = eps_alpha_i,
c_alpha_i = 1 - eps_alpha_i^2/2.
```

Thus a Float64 angle-formation receipt only needs to export one nonnegative rational/dyadic error radius per call; it does not need to export a separately trusted reduced interval.  If the angle-error radii are dyadic/rational, all downstream cell endpoints remain exact rational expressions.

This bridge is intentionally about the exact transcendental values at `xhat`.  It does **not** claim that Julia/libm returns those exact values.  The `.3` leaf must separately prove its machine-output enclosure around `Real.sin xhat` / `Real.cos xhat` under the pinned runtime and flags.

## 6. Suggested Lean decomposition

The smallest source-independent theorem family is:

```lean
-- no machine semantics
lemma base_trig_cell_of_abs_le
    {r b : Real} (hb : 0 <= b) (hr : |r| <= b) :
    -b <= Real.sin r /\ Real.sin r <= b /\
    1 - b^2/2 <= Real.cos r /\ Real.cos r <= 1

lemma formed_angle_error_to_reduced_radius
    {q xhat eps : Real} {k : Int}
    (heps : 0 <= eps)
    (hform : |xhat - (q + (k:Real)*(Real.pi/2))| <= eps)
    (hq : |q| <= a) (ha : 0 <= a) :
    |xhat - (k:Real)*(Real.pi/2)| <= a + eps

lemma phase_neg_quarter_cell ...
lemma phase_zero_cell ...
lemma phase_pos_quarter_cell ...
```

Then use a finite phase enum rather than a generic integer theorem, because the source table contains only `-1,0,+1`:

```lean
inductive QuarterPhase | neg | zero | pos

def phaseTheta : Fin 6 -> QuarterPhase := ...
def phaseAlpha : Fin 6 -> QuarterPhase := ...
```

The source-facing targets can be stated as

```lean
theta_all12_exact_cells_from_qbox
alpha_all12_exact_cells
robust_theta_cell_of_formed_angle_error
robust_alpha_cell_of_formed_angle_error
```

A particularly useful theorem boundary is that `robust_*` consumes an already-decoded real `xhat` and an error inequality; it should not contain `Float64`, libm, receipt parsing, leaf ids, or provenance fields.  Those adapters belong to their own leaves.

## 7. Why this advances T-P4-036 rather than duplicating the theta2 child

The existing theta2 child proves one exact row and currently routes through a local sine Taylor remainder.  This review adds three genuinely new facts:

1. all 12 exact-real rows follow uniformly from one base inequality and the phase table;
2. the exact-real layer can delete `piBox` and `reducedRowSound` hypotheses because the reduction cancels symbolically;
3. most importantly, the same proof accepts an upstream angle-formation error `eps` and produces a robust exact trig cell, giving a clean mathematical seam between `.1` angle formation and `.3` libm inclusion.

The result therefore reduces the deployed interface from twelve ad-hoc trig envelope premises to per-call angle-error radii plus one finite phase table.

## 8. Remaining open obligations

This review does not provide or claim:

- the actual `eps_theta_i` / `eps_alpha_i` for Float64 formation/storage;
- proof that decoded Float64 arguments satisfy the stated error bounds;
- any Julia/libm correctly-rounded or directed enclosure theorem;
- finite/non-NaN/no-overflow runtime semantics;
- D1/D2/D3 outward propagation or repeated `fk_frames` composition;
- authoritative receipt-to-Lean `RectBox13` membership, parent/sibling coverage join, or all-box coverage;
- source execution equality, registry promotion, or O2/P4/M4 closure.

The current authority/coverage blocker for theta2 remains untouched.  This result is meant to make the *mathematical* consumer of a future angle-formation receipt minimal.

## Requested coordinator action

Please harvest this as a source-independent exact interval/range-reduction theorem target under `T-P4-036.2`.  The preferred next formal step is to compile the four generic lemmas (`base_trig_cell_of_abs_le`, formed-angle error transport, and the +/- quarter-turn transports) and then instantiate the finite source phase table.  The preferred next source step is for `.1` to provide per-row real-lift angle-error radii; `.3` must still provide the independent libm-output inclusion.

## Status

`pending` only.  待封不觉独立验证 / 待梁智炜最终整合。
