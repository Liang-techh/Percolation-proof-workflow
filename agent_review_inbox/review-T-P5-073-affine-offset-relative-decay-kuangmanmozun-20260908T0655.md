---
kind: review_result
task_id: T-P5-073-AFFINE-OFFSET-RELATIVE-DECAY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
status: pending_mathematical_child
scope: mathematics_only
parent_tasks:
  - P5-COMPONENTWISE-RELATIVE-DECAY
claim_commit: 077c9f5927c904823c4dceed069050b9c32846a1
---

# T-P5-073 — exact affine-offset relative-decay / zero-slice obstruction gate

## 0. Result in one line

A pure componentwise certificate

`|R_i(v)| <= kappa_i |v_i|`

on a cell that contains `v_i=0` is not merely a small-error estimate: it forces the **entire transverse zero-slice identity** `R_i(0,v_{-i})=0`.  If an additive slice bias survives, pure relative decay is mathematically impossible on that cell.  The correct replacement is either (a) absorb the bias on a gap cell `|v_i|>=delta_i` by the sharp gate

`beta_i < (1-kappa_i) delta_i`,

or (b) keep the zero-containing cell and close a bias-aware bootstrap box by

`beta_i + sum_j A_ij r_j < r_i`.

All gates are division-free; the boundary equalities are sharp and give zero strict reserve.

---

## 1. Zero-slice obstruction: necessary condition for pure componentwise decay

Let `D` be any domain and let `R_i : D -> R`.  Suppose

`|R_i(v)| <= kappa_i |v_i|`

for every `v in D`, with any finite `kappa_i >= 0`.  Then for every admissible point with `v_i=0`,

`R_i(v)=0`.

Proof: the right-hand side is zero, hence `|R_i(v)|<=0`.

So the necessary condition is stronger than `R_i(0)=0`: one needs

`R_i(0,v_{-i}) = 0`

for the whole transverse slice that lies in the cell.

### Counterexample 1: center vanishing is not enough

On `[-1,1]^2`, take

`R_1(v_1,v_2)=v_2`.

Then `R_1(0,0)=0`, but at `(0,1/2)` one has `R_1=1/2` while `kappa |v_1|=0` for every finite `kappa`.  Therefore no componentwise relative-decay theorem can follow from center vanishing alone.

### Exact obstruction versus weak envelope

If a source theorem exhibits one admissible point with `v_i=0` and `R_i(v) != 0`, this is a **mathematical impossibility certificate** for pure componentwise relative decay on that cell.

By contrast, merely having a coarse bound `|R_i(0,v_{-i})| <= beta_i` with `beta_i>0` is not an impossibility proof: the true residual might still vanish.  Failure of the coarse envelope must therefore be labelled `NOT_CERTIFIED_BY_THIS_BOUND`, not `FAIL`, unless a nonzero slice witness or exact source identity is available.

---

## 2. Exact decomposition: transverse bias + relative factor

Whenever the source algebra permits the decomposition

`R_i(v) = b_i(v_{-i}) + v_i Q_i(v)`,                 (2.1)

with

`|b_i(v_{-i})| <= beta_i`,
`|Q_i(v)| <= kappa_i`,

one immediately has the affine envelope

`|R_i(v)| <= beta_i + kappa_i |v_i|`.              (2.2)

The pure relative branch is recovered exactly when the transverse bias vanishes identically:

`b_i == 0`.

For polynomial/rationalized polynomial source expressions this is particularly checker-friendly: if `R_i` is polynomial in `v_i` with polynomial transverse coefficients, then

`R_i(0,v_{-i}) == 0  <=>  v_i divides R_i`.

Hence the trusted route can be:

1. exact CSE/simplification;
2. verify the zero-slice polynomial identity;
3. divide symbolically by the exact factor `v_i` in the untrusted generator;
4. trusted checker verifies `R_i = v_i Q_i` by a polynomial identity;
5. prove `|Q_i| <= kappa_i < 1`.

No small absolute error estimate can replace step 2 on a zero-containing cell.

### Smooth rectangular corollary

Let `D` be a rectangle, so fixing `v_{-i}` and moving `v_i` to zero stays in `D`.  If

`R_i(0,v_{-i})=0`

for every transverse slice and

`|partial_i R_i(v)| <= kappa_i`

throughout `D`, then the one-dimensional mean-value theorem along the `i`-fiber gives

`|R_i(v)| <= kappa_i |v_i|`.

Thus for a smooth source the desired relative theorem reduces cleanly to two independent obligations: **exact slice vanishing** plus a **one-coordinate derivative bound**.

Zero-slice vanishing alone is not sufficient without such divisibility/regularity.  For example `R(v)=sqrt(|v|)` has `R(0)=0` but `|R(v)|/|v|=1/sqrt(|v|)` is unbounded near zero.

---

## 3. Gap-cell absorption of an additive offset

Assume the affine envelope (2.2) and suppose the current cell is separated from the contact slice:

`|v_i| >= delta_i > 0`.

Then

`beta_i <= (beta_i/delta_i)|v_i|`,

so

`|R_i(v)| <= (kappa_i + beta_i/delta_i)|v_i|`.

To obtain a strict relative factor `<1`, it is enough and, given only the two envelope constants, universally sharp to require

`beta_i < (1-kappa_i) delta_i`,                    (3.1)

with `0 <= kappa_i < 1`.

The trusted checker does not need the quotient `beta_i/delta_i`: (3.1) is already division-free.

More generally, for a requested rational target `q_i >= kappa_i`, the exact sufficient gate is

`beta_i <= (q_i-kappa_i) delta_i`

for `|R_i|<=q_i |v_i|`, with strict `<` for strict reserve.

### Sharpness

On the positive gap `v>=delta>0`, take

`R(v)=beta+kappa v`,  `beta,kappa>=0`.

At `v=delta`,

`R(v)/v = kappa + beta/delta`.

Therefore the threshold `beta=(1-kappa)delta` gives ratio exactly `1`, and any larger `beta` violates strict decay.  No better universal constant is possible from unsigned `(beta,kappa,delta)` data alone.

Signed source information can of course improve this: if bias and linear part provably oppose each other, the triangle envelope may be conservative.  Exact source cancellation should be simplified before applying this unsigned gate.

---

## 4. Zero-containing cells: exact bias-aware box closure

When the cell contains `v_i=0` and a nonzero bias survives, forcing pure relative decay is the wrong objective.  The natural closure object is an invariant/bootstrap box.

Let `beta_i>=0`, `A_ij>=0`, `r_i>0`, and suppose on

`B_r = {v : |v_j| <= r_j for all j}`

we have

`|R_i(v)| <= beta_i + sum_j A_ij |v_j|`.           (4.1)

Then the exact componentwise budget

`beta_i + sum_j A_ij r_j < r_i`                    (4.2)

for every `i` implies `R(B_r)` lies strictly inside `B_r`.

Define the division-free reserve

`s_i := r_i - beta_i - sum_j A_ij r_j`.

The strict box closure is simply `s_i>0` for every component.

### Why (4.2) is sharp for envelope-only certification

Consider the uncertainty class of all maps satisfying (4.1).  If (4.2) fails for some `i`, choose

`R_i(v)=beta_i + sum_j A_ij |v_j|`

and all other components zero.  At the positive corner `v_j=r_j`, the `i`-th output equals or exceeds `r_i`.  Hence (4.2) is not just sufficient: it is **necessary and sufficient for the envelope data alone to certify strict box invariance for every admissible residual map**.

For an actual affine map

`R_i(v)=b_i+sum_j a_ij v_j`

on a symmetric box, the exact maximum is

`sup_{B_r}|R_i| = |b_i| + sum_j |a_ij| r_j`,

because the corner signs can align with `b_i` and each `a_ij`.  Thus

`|b_i| + sum_j |a_ij| r_j < r_i`

is the exact strict-invariance criterion for that affine component.

### Boundary equality

If

`beta_i + sum_j A_ij r_j = r_i`,

one has at best closed-box invariance and zero strict reserve.  It must not be promoted to a strict bootstrap/decay certificate.

---

## 5. Scalar bootstrap floor: additive error does not disappear

For a scalar nonnegative bootstrap recurrence

`x_{n+1} <= beta + kappa x_n`,

with `0<=kappa<1`, induction gives

`x_n <= kappa^n x_0 + beta (1-kappa^n)/(1-kappa)`.

Thus the asymptotic floor is

`beta/(1-kappa)`.

Equivalently, a target radius `r` is strictly invariant exactly under the envelope gate

`beta + kappa r < r`

or, division-free,

`beta < (1-kappa)r`.

So an additive force/FD floor should not be disguised as a pure contraction.  It consumes an explicit fraction of the bootstrap radius.

---

## 6. Decision rule for the P5 componentwise-relative lane

For each component `i`:

### Branch A — cell intersects `v_i=0`

1. Check exact source/CSE slice `R_i(0,v_{-i})`.
2. If a certified nonzero slice witness exists: `PURE_RELATIVE_IMPOSSIBLE`; route to bias-aware box.
3. If slice identity is proved: bound the exact quotient `Q_i=R_i/v_i` or the fiber derivative.  If `<1`, pure componentwise relative decay PASSes.
4. If slice identity is merely unknown: `NOT_CERTIFIED`, not mathematical FAIL.

### Branch B — cell has a certified gap `|v_i|>=delta_i>0`

If `|R_i|<=beta_i+kappa_i|v_i|`, use the division-free absorption gate

`beta_i < (1-kappa_i)delta_i`.

PASS yields a strict relative factor on that gap cell.

### Branch C — additive bias is real and the cell includes zero

Use a bias-aware scalar/vector box and verify

`beta_i + sum_j A_ij r_j < r_i`.

Do not continue searching for a pure componentwise relative theorem unless the source algebra removes the slice bias.

---

## 7. Counterexample packet

1. **Origin-only test is unsound:** `R_1(v1,v2)=v2`.  `R_1(0,0)=0`, but no finite `kappa` works on any product cell with points `(0,v2!=0)`.
2. **Slice vanishing without slope control is insufficient:** `R(v)=sqrt(|v|)`.
3. **Gap threshold is sharp:** `R(v)=beta+kappa v` at `v=delta>0`; equality `beta=(1-kappa)delta` gives ratio exactly one.
4. **Bias-box equality is boundary only:** same affine example at `v=r` with `beta=(1-kappa)r` maps boundary to boundary.
5. **A positive coarse beta is not itself a mathematical obstruction:** the true map `R(v)=kappa v` also satisfies the weaker estimate `|R(v)|<=beta+kappa|v|` for any `beta>0`.  Therefore envelope failure must not be confused with a nonzero source-slice witness.

---

## 8. Lean-friendly theorem leaves

Suggested small leaves, all independent of provenance/source binding:

- `componentwise_relative_implies_zero_slice`
- `rect_zero_slice_deriv_bound_implies_relative`
- `poly_zero_slice_iff_coordinate_factor`
- `affine_offset_gap_absorption`
- `affine_offset_gap_strict_decay`
- `box_envelope_strict_invariant`
- `box_envelope_gate_sharp_universal`
- `affine_box_exact_sup`
- `scalar_affine_bootstrap_bound`
- regressions for `R1(v1,v2)=v2`, gap equality, and box equality.

The first, gap, and box gates are essentially `abs` + linear arithmetic.  The polynomial factor corollary can be handled separately by ring normalization/divisibility infrastructure.

---

## 9. What this does and does not close

This child closes the **mathematical logic around additive offsets** in a componentwise-relative-decay obligation.  In particular it identifies when a pure relative target is structurally impossible, when a gap absorbs an offset, and when a bias-aware bootstrap is the correct replacement.

It does **not** claim that the deployed forceError/FD source has a nonzero bias, that a particular `beta,kappa,delta,A,r` packet has been proved, that Float64/controller effects are bounded, or that P5/P8/M4/registry/admission is closed.  Those remain source/verification tasks outside this Agent's lane.

Status remains `pending_mathematical_child` until a concrete source packet selects one of Branch A/B/C and the corresponding theorem is formalized/consumed.