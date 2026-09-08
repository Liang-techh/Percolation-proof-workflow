# Review result — GH-MATH-P4-TARGET-CAPS

- `kind`: `review_result`
- `task_id`: `GH-MATH-P4-TARGET-CAPS`
- `review_id`: `GH-MATH-P4-TARGET-CAPS`
- `agent`: `古月方源`
- `source_agent`: `古月方源`
- `status`: `partial_math_result_blocked_on_source_packet`
- `claim`: `agent_review_inbox/claim-GH-MATH-P4-TARGET-CAPS-guyuefangyuan-20260908T1430Z.md`
- `inspected_main`: `61dc6639c45bfa558305974e153340b2a27758f1`

## 1. Executive result

There are **two opposite set-inclusion obligations** that must not be conflated when binding the advertised target box

- `|q| <= 5/2`,
- `|v| <= 15`,
- `|w| <= 2`

(componentwise if that is indeed the frozen target-domain convention)
to a source theorem whose hypothesis is `V <= 1`.

Let `E := {z : V(z) <= 1}` and let `B(H)` denote the target box.

1. `E ⊆ B(H)` is an **energy-to-coordinate** statement. A lower/coercive bound on `V` can prove it.
2. `B(H) ⊆ E` is the **target-to-energy** statement required if a theorem proved only on `V <= 1` is to be consumed on the whole advertised target box. A lower/coercive bound does **not** prove it; one needs an upper bound for `V` on `B(H)`, or a direct same-source inclusion theorem.

This direction split is the main mathematical gate. It prevents a plausible but invalid reversal of the energy argument.

At the inspected `main`, the task-named source file `combined_descriptor_remainder_v1.json` is not present under that filename in the recursive tree and code search for both `combined_descriptor` and `remainder_v1` returns no hit. I also did not find a frozen real-DH target-domain theorem/formula exposing the exact `V` needed to instantiate the gates below. Therefore the **deployed target-cell binding cannot honestly be closed from the currently committed source packet**. The exact generic theorem and the missing source interface are given below so the lane can close immediately once the packet is frozen.

No receipt/provenance/admission conclusion is made here.

---

## 2. Exact radical-free theorem: energy sublevel is inside a coordinate box

Suppose for coordinate `z_i` the source proves

`V(z) >= a_i z_i^2`, with `a_i > 0`.

If `V(z) <= 1`, then

`a_i z_i^2 <= 1`.

Hence the exact square-only gate

`1 <= a_i H_i^2`

implies

`z_i^2 <= H_i^2`,

and therefore, for `H_i >= 0`, `|z_i| <= H_i`.

No square root or division is required in the trusted checker.

For the advertised half-widths this becomes, per coordinate,

- q-coordinate, `H_q = 5/2`: `25 a_q >= 4` (equivalently `a_q >= 4/25`);
- v-coordinate, `H_v = 15`: `225 a_v >= 1`;
- w-coordinate, `H_w = 2`: `4 a_w >= 1`.

If the source has anisotropic coefficients, apply the corresponding gate to every coordinate separately.

### Important limitation

These gates prove only

`E ⊆ B(H)`.

They do **not** prove that every target point lies in the energy-certified domain.

---

## 3. Exact sufficient theorem in the needed direction: target box is inside `V <= 1`

The correct same-source certificate is an **upper envelope** for `V` on the target box.

### 3.1 Affine-quadratic storage

After expanding around the actual target-box center, suppose the frozen source gives

`V(z) = c + sum_i l_i z_i + sum_{i,j} P_ij z_i z_j`

and the target box is `|z_i| <= H_i`.

Then termwise triangle inequality gives the exact rational upper envelope

`V(z) <= U(H)`

with

`U(H) := c + sum_i |l_i| H_i + sum_{i,j} |P_ij| H_i H_j`.

Therefore

`U(H) <= 1`

is a finite exact-rational sufficient certificate for

`B(H) ⊆ E`.

This checker uses only absolute value, addition, multiplication, and order comparison. It requires no roots, spectral computation, optimization, or floating-point arithmetic.

For a symmetric quadratic written without the full double sum, the equivalent sharper bookkeeping is

`U(H) = c + sum_i |l_i|H_i + sum_i |P_ii|H_i^2 + 2 sum_{i<j}|P_ij|H_iH_j`.

If the actual storage is centered at a nonzero point, expand `z = z0 + xi` first and use the exact coefficients in `xi`; do not silently reuse an origin-centered formula.

### 3.2 Diagonal upper packet

A particularly small source interface is

`V(z) <= c + sum_i b_i z_i^2`, with `b_i >= 0`.

Then

`c + sum_i b_i H_i^2 <= 1`

immediately proves the whole target box is energy-certified.

### 3.3 Exact finite vertex checker when the storage is known convex quadratic

If the frozen storage is a convex quadratic (`P` positive semidefinite), an exact but potentially larger alternative is to evaluate `V` at every sign vertex of the box. A convex function on a compact polytope has a maximizer at an extreme point, so

`max_{z in B(H)} V(z) = max_{s_i in {-1,+1}} V(s_1 H_1,...,s_n H_n)`

for an origin-centered box (use translated vertices for a shifted box).

Thus `V(vertex) <= 1` for every vertex is necessary and sufficient for `B(H) ⊆ E` in that convex-quadratic case. This is useful as an offline exact compressor, although the triangle-envelope gate above is much cheaper.

---

## 4. Homothetic inner-box fallback when the full target box does not pass

Even if the full target box cannot be certified, the same source coefficients can produce a rigorous smaller target domain rather than a binary dead end.

For the affine-quadratic envelope define

`L := sum_i |l_i| H_i`,

`Q := sum_{i,j} |P_ij| H_i H_j`.

For any rational `r` with `0 <= r <= 1`, the homothetic box `B(rH)` satisfies

`V(z) <= c + r L + r^2 Q`.

Therefore the exact-rational gate

`c + r L + r^2 Q <= 1`

certifies

`B(rH) ⊆ E`.

No quadratic root needs to be computed: an offline search may propose rational/dyadic `r`, while the trusted consumer rechecks the displayed polynomial inequality exactly.

This gives a concrete fail-closed interface:

- full PASS if `r=1` passes;
- otherwise retain the largest proposed rational `r<1` that passes;
- the conservative target region not covered by that inner-box certificate is `B(H) \ B(rH)`.

The **exact** energy-uncovered shell is instead

`B(H) \ E = {z in B(H) : V(z) > 1}`.

The homothetic shell may be larger because points outside `B(rH)` can still have `V<=1`.

---

## 5. Counterexample-guided obstruction: coercivity cannot prove the needed reverse inclusion

A lower energy estimate alone can never justify `B(H) ⊆ E`.

Already in one dimension, let

`V_N(x) = N x^2`, `N > 0`.

This has an arbitrarily strong coercive lower bound, but at the target endpoint `x=H`,

`V_N(H) = N H^2`.

Choosing `N H^2 > 1` gives an exact target point outside `E`.

For the q half-width `H=5/2`, the elementary model `V(x)=x^2` gives

`V(5/2)=25/4 > 1`.

This is only a logical countermodel to the inference pattern, **not** a claim about the deployed DH storage. It proves that no theorem of the form

`coercivity + target coordinate caps => target box lies in V<=1`

can be valid without additional upper/source information.

Accordingly, if the current P4 remainder packet was proved under `V<=1`, and only coercivity is available, the advertised target cell must remain unbound rather than being admitted by reversing the inequality.

---

## 6. Exact three-state source-domain decision interface

The eventual source consumer should distinguish:

1. `TARGET_BOX_INSIDE_ENERGY`: an exact upper packet proves `U(H) <= 1` (or all exact convex-quadratic vertices pass).
2. `TARGET_POINT_OUTSIDE_ENERGY`: an exact source-grounded `z0 in B(H)` satisfies `V(z0) > 1`; this proves a nonempty uncovered shell.
3. `UNRESOLVED_SOURCE_GAP`: neither certificate exists yet.

Separately, coercivity may certify `ENERGY_INSIDE_TARGET_BOX`. That flag is useful but is **not interchangeable** with state 1.

This type-level separation is recommended because the two inclusions have opposite logical directions and are easy to confuse in downstream assembly.

---

## 7. Minimal Lean theorem decomposition

The smallest useful sidecar does not need the deployed DH constants yet.

### 7.1 Coercive coordinate consumer

Suggested theorem shape (prefer square conclusions):

```lean
theorem energy_sublevel_coord_sq_le
    (a H x V : ℚ)
    (ha : 0 < a)
    (hcoerc : a * x^2 <= V)
    (hV : V <= 1)
    (hgate : 1 <= a * H^2) :
    x^2 <= H^2 := by
  -- linear/order arithmetic after multiplying by positive a
  sorry
```

A real-valued wrapper can derive `|x| <= H` under `0 <= H`.

### 7.2 Box upper-envelope consumer

A generic finite-index theorem:

```lean
theorem affine_quadratic_box_upper
    {n : Nat}
    (c : ℚ)
    (l H z : Fin n -> ℚ)
    (P : Fin n -> Fin n -> ℚ)
    (hH : forall i, 0 <= H i)
    (hz : forall i, |z i| <= H i) :
    c + (sum i, l i * z i) + (sum i, sum j, P i j * z i * z j)
      <= c + (sum i, |l i| * H i)
           + (sum i, sum j, |P i j| * H i * H j) := by
  sorry
```

Then a one-line wrapper consumes `U(H)<=1`.

### 7.3 Homothetic inner-box consumer

```lean
theorem affine_quadratic_scaled_box_inside
    ...
    (hr0 : 0 <= r) (hr1 : r <= 1)
    (hgate : c + r*L + r^2*Q <= 1) :
    V z <= 1 := by
  ...
```

Keep the source-specific target numbers (`5/2`, `15`, `2`) in a small data theorem rather than hard-coding them into the generic analytic lemma.

---

## 8. Missing source data required to close the deployed target binding

At inspected `main = 61dc6639c45bfa558305974e153340b2a27758f1`, I could not locate the task-referenced `combined_descriptor_remainder_v1.json` or a committed exact target-domain/storage packet under that name/search family.

To instantiate this review, the source lane needs to freeze, under one source key:

1. the actual path/blob for `combined_descriptor_remainder_v1.json` (or its renamed successor);
2. exact semantics of `|q|<=5/2`, `|v|<=15`, `|w|<=2` (componentwise box vs vector norm, coordinate dimensions, center);
3. the exact storage `V` or a same-source upper-envelope packet valid on that target cell;
4. if only `V<=1` is available, the exact theorem showing the intended inclusion direction;
5. if the full target fails, either an exact target witness with `V>1` or a rational inner-cell scale `r` plus the corresponding source envelope.

Until those are present, the mathematical status is **source-domain binding unresolved**, not failure of the descriptor theorem itself.

## 9. What remains open

- deployed target-cell inclusion (`B_target ⊆ {V<=1}` or a certified smaller replacement);
- actual source JSON/blob and exact V coefficients/upper packet;
- descriptor remainder numerical constants and their same-source binding;
- any Float64/runtime connection;
- Lean compilation of the proposed generic consumers;
- verifier review and all P4/M4 admission decisions.

No claim is made here about receipt, provenance, admission, Float64, or registry promotion.
