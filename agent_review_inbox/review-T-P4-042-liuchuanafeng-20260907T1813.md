---
kind: review_result
review_id: review-T-P4-042-liuchuanafeng-20260907T1813
task_id: T-P4-042
agent: 流川枫
source_agent: 流川枫
created_at: 2026-09-07T18:13:00-06:00
inspected_commit: 9d19b9b400398aa3c8b290c90bf376e8370c6799
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-T-P4-038-guyuefangyuan-20260907T1521.md
  - agent_review_inbox/review-T-P4-038-juyangxianzun-20260907T1558.md
  - agent_review_inbox/review-T-P4-039-liuguanyi-20260907T1616.md
  - agent_review_inbox/review-T-P4-039-common-lambda-kuangmanmozun-20260907T1542.md
  - examples/routeb_p4_young_feasibility_lean/P4YoungFeasibility.lean
related_tasks:
  - T-P4-038
  - T-P4-039
  - T-P4-024
  - T-P4-027
integration_status: pending
admission_label: pending
proposed_integration_target: P4.combined_schur_shared_theta_scalar_adapter_bridge
requested_action: keep T-P4-038 theorems as per-row checkers only; require one explicit common_theta (or common_lambda) on the cell tag before any multi-row fold; do not treat rowwise discriminant PASS or row-center witnesses as a shared-parameter certificate; do not write registry/state
---

# T-P4-042 — minimal typed bridge from T-P4-039 onto the T-P4-038 scalar adapter

## 0. Result

The existing T-P4-038 sidecar
`examples/routeb_p4_young_feasibility_lean/P4YoungFeasibility.lean` is a
**single-row** scalar adapter. Every public theorem is quantified over one
quadruple `(A, P, D, theta)` (or the equivalent `(A, P, G)` / `(A, P, D, m)`).
There is no cell tag, no finite row index, and no `common_theta` / `common_lambda`
argument. That is the correct boundary for T-P4-038; it is also the exact place
where a silent multi-row fold would be an admission error.

T-P4-039 supplies the missing same-cell layer, in two compatible mathematical
packages:

1. 柳冠一: rational inner-radius intervals `[L_i, U_i]` and a common midpoint
   `theta_c = (L+U)/2` when `L = max L_i <= min U_i = U`.
2. 狂蛮魔尊: square-free pairwise overlap `C_ij <= U_ij + V_ij` or
   `(C_ij - U_ij - V_ij)^2 <= 4 U_ij V_ij`, plus a dominating-envelope
   sufficient construction and a trusted final check of one supplied rational
   `theta0` against every row quadratic.

The **minimal typed bridge** is therefore not a new Young identity. It is a
contract that reuses T-P4-038's already compiled checker

```text
young_scalar_budget_mul_iff :
  0 < theta ->
  youngCost theta A P <= D
    <-> A*theta^2 - (D-A-P)*theta + P <= 0
```

on **one shared parameter**. The cell-level object must carry a single
`common_theta : Rat` (equivalently `common_lambda = 1 + 1/common_theta > 1`)
and a finite list of row charges. The trusted predicate is

```text
0 < common_theta
/\  forall i,  A_i * common_theta^2 - G_i * common_theta + P_i <= 0
```

with `G_i = D_i - A_i - P_i` (or `G_i^m = D_i - m_i - A_i - P_i` if a named
reserve is required).

This predicate is **not** implied by the family of rowwise T-P4-038 results

```text
forall i,  exists theta_i > 0,  youngCost theta_i A_i P_i <= D_i.
```

The two statements differ by a quantifier swap. Treating the second as the first
is exactly the degradation this lane forbids.

No concrete P4 source cell is asserted. No registry, StateStore, comparator, or
formal-admission object is written.

---

## 1. What the T-P4-038 adapter actually exports

Inspected Lean namespace: `RouteBP4YoungFeasibility`.

Public theorems (all single-row):

| theorem | role in a bridge |
|---|---|
| `young_gap_mul_identity` | exact multiplication identity |
| `young_scalar_budget_mul_iff` | **trusted per-row checker** once `theta` is fixed |
| `young_scalar_discriminant_necessary` | one-row impossibility / necessity |
| `young_theta_gap_identity` / `young_scalar_discriminant_constructive` | one-row constructive center `theta = G/(2A)` |
| `young_lambda_gap_identity` / `young_scalar_lambda_constructive` | one-row historical `lambda = 1 + 2A/G` |
| `young_scalar_strict_margin_constructive` / `young_scalar_strict_extra_reserve` | one-row named reserve |
| `rational_example_sharp_vs_theta_one` / `obstruction_example_no_theta` | sanity examples |

The sidecar README/verify comments already mark
`P4_SHARED_LAMBDA_MULTIROW=OPEN`. T-P4-038 §9 (古月方源) independently forbids
using separate rowwise discriminant PASS results as a shared-`theta`/`lambda`
certificate. The compiled candidate of 巨阳仙尊 does not close that hole; it
only makes the single-row algebra kernel-checkable.

Bridge rule: the constructive centers `G_i/(2A_i)` and `1 + 2A_i/G_i` are
**row witnesses**, not cell witnesses. They may be used as untrusted candidate
generators. They must not be stored as the cell parameter unless they also pass
every other row through `young_scalar_budget_mul_iff`.

---

## 2. Minimal interface types (source-independent)

Suggested receipt-facing records; these are planning types, not Lean admission.

```text
YoungRowCharge := {
  A : Rat,          -- require A > 0
  P : Rat,          -- require P >= 0
  D : Rat,
  m : Rat := 0      -- optional named reserve
}

YoungSharedCell := {
  cell_id : String,                 -- opaque tag; not erased by the fold
  rows : List YoungRowCharge,       -- finite, nonempty
  common_theta : Rat,               -- the only parameter consumed by P4-024 lambda form
  optional_radius : List Rat        -- construction metadata only
}
```

Trusted checks, in order:

1. `common_theta > 0`.
2. For each row, set `G := D - m - A - P` and evaluate the T-P4-038 quadratic
   `A * common_theta^2 - G * common_theta + P <= 0`.
3. Optionally record `common_lambda := 1 + 1/common_theta` and, if a lambda
   consumer is used, the equivalent division-free form
   `P * s^2 - G * s + A <= 0` with `s = common_lambda - 1`
   (T-P4-039 狂蛮魔尊 §9). Do not keep a second independent parameter.

Untrusted / construction-only (must not replace step 2):

- per-row discriminant `G_i > 0` and `G_i^2 >= 4 A_i P_i`;
- rational radii `s_i^2 <= Delta_i` and inner endpoints `(G_i ± s_i)/(2 A_i)`;
- pairwise square-free overlap polynomials;
- dominating envelope `(Abar, Pbar, Glow)` with `theta_bar = Glow/(2 Abar)`;
- midpoint `(max L_i + min U_i)/2`.

If any construction is used, the receipt must still emit the shared `common_theta`
and pass step 2 on every row. Construction failure of a sufficient corollary
(envelope, row-center scan) is **not** an impossibility proof. Pairwise
failure of the exact overlap gate **is** an impossibility proof for this
scalar shared-parameter model.

---

## 3. Shared theta is not rowwise theta: exact counterexamples already on file

Both T-P4-039 reviews give the same first obstruction, which this bridge must
keep as a regression fixture:

```text
row 1: A=1, P=2,  D=6   -> G=3,  feasible theta in [1, 2]
row 2: A=1, P=12, D=20  -> G=7,  feasible theta in [3, 4]
```

Each row separately passes T-P4-038 (`Delta = 1`, constructive centers `3/2`
and `7/2`). The intervals are disjoint, so no shared positive theta exists.
The pairwise polynomials are `C=16`, `U=1`, `V=1`, and both branches of the
overlap disjunction fail.

A second, already recorded, obstruction to “just try each row center” is the
overlapping pair whose centers lie outside the intersection (柳冠一 §6 /
狂蛮魔尊 §5). Those examples show why the adapter must accept an externally
constructed common rational and then run the T-P4-038 quadratic, rather than
internally defaulting to `theta_i = G_i/(2A_i)`.

---

## 4. What this child does *not* close

Still open and not claimed:

- concrete same-cell P4 values of `(A_i, P_i, D_i, m_i)` or source identity;
- whether current combined-Schur artifacts still expose separated baseline/port
  charges required by T-P4-037;
- Lean compilation of a multi-row sidecar (that is T-P4-041's lane if released);
- T-P4-040's division-free Real/Rat compression and T-P4-043's boundary-only
  / midpoint-failure mathematics;
- true-DH / Float64 semantics, domain, trajectory, or flowpipe coverage;
- registry, StateStore, comparator admission, P4/M4 closure.

`admission_label` is therefore `pending`: this is a typed interface audit plus
an exact quantifier-boundary correction. It is not compiled evidence and not a
registry event.

---

## 5. Suggested next leaf (not executed here)

If a later Lean slot formalizes the bridge, the smallest source-independent
theorems are:

1. `young_shared_of_common_theta` — finite list, one `theta>0`, reuse
   `young_scalar_budget_mul_iff` row-wise.
2. `young_rowwise_exists_not_shared` — encode the `[1,2]` vs `[3,4]` fixture as
   a kernel example that `forall i, exists theta_i` does not yield
   `exists theta, forall i`.
3. `young_common_lambda_of_common_theta` — `lambda = 1 + 1/theta`, no second
   free parameter.

Until those exist, any integrator that folds several T-P4-038 row receipts into
one combined-Schur cell without an explicit `common_theta` field should be
rejected as a protocol error, not as a missing numerical search.
