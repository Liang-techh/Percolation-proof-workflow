---
task_id: T-P3-014
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
status: pending
created_at: 2026-09-08
scope: exact trig monotonicity endpoint-enclosure source-boundary bridge
depends_on:
  - P3.trig_endpoint_enclosure_leaf
  - declared canonical Route-B interval evaluator iv_sin/iv_cos cell
---

# Review result — T-P3-014 exact trig monotonicity endpoint-enclosure bridge

## 0. Result / scope

This child closes the exact mathematical contract needed to feed a canonical Route-B `iv_sin` / `iv_cos` monotonicity cell into the abstract `P3.trig_endpoint_enclosure_leaf`.

The core conclusion is simple but source-critical: **endpoint evaluation is a sound enclosure only after the whole input cell has been certified to lie in one trig monotonicity cell**. If the cell crosses an interior turning point, it must be split there (or the evaluator must use a different range-reduction theorem); endpoint values alone are not a sound range certificate.

This review does **not** claim executable MPFR/BigFloat directed-rounding evidence, source provenance/admission, or that a particular deployed evaluator call site has already been bound. Current repository search did not expose a uniquely identifiable implementation artifact containing the declared names `iv_sin` or `iv_cos`, so the mathematical/source contract below is closed while the executable source binding remains pending.

## 1. Generic endpoint-enclosure lemma

Let `a <= b`, `x in [a,b]`, and suppose outward endpoint evaluations satisfy

`La <= f(a) <= Ua`,

`Lb <= f(b) <= Ub`.

### Increasing branch

If `f` is nondecreasing on `[a,b]`, then

`f(a) <= f(x) <= f(b)`.

Combining with the directed endpoint enclosures gives

**`La <= f(x) <= Ub`.**

Hence the sharp orientation-aware endpoint leaf is

**`Iout = [La, Ub]`.**

### Decreasing branch

If `f` is nonincreasing on `[a,b]`, then

`f(b) <= f(x) <= f(a)`.

Therefore

**`Lb <= f(x) <= Ua`,**

and the corresponding endpoint leaf is

**`Iout = [Lb, Ua]`.**

A direction-free hull `[min(La,Lb), max(Ua,Ub)]` is also sound once monotonicity of the whole cell is known, but it is weaker and needlessly loses orientation information.

## 2. Exact sine monotonicity cells

The turning points of `sin` are

`t_k = pi/2 + k*pi`, `k in Z`.

On the closed cell

**`t_k <= a <= b <= t_(k+1)`**

there is no interior sign change of `cos`, hence `sin` is monotone on the entire interval. More precisely:

- if `k` is even, `cos <= 0` on `[t_k,t_(k+1)]`, so `sin` is nonincreasing;
- if `k` is odd, `cos >= 0` there, so `sin` is nondecreasing.

Equality with a turning point is harmless: the derivative may vanish at the endpoint while monotonicity on the closed cell is preserved.

Therefore an `iv_sin` leaf with certified branch index `k` may return

- `k even`: `[Lb, Ua]`;
- `k odd`: `[La, Ub]`.

Equivalent conventional cells are `[-pi/2+2m*pi, pi/2+2m*pi]` for the increasing branch and `[pi/2+2m*pi, 3pi/2+2m*pi]` for the decreasing branch.

## 3. Exact cosine monotonicity cells

The turning points of `cos` are

`s_k = k*pi`, `k in Z`.

On

**`s_k <= a <= b <= s_(k+1)`**

`sin` has fixed sign and therefore `-sin`, the derivative of `cos`, has fixed sign. More precisely:

- if `k` is even, `cos` is nonincreasing on `[k*pi,(k+1)*pi]`;
- if `k` is odd, `cos` is nondecreasing there.

Thus an `iv_cos` leaf with certified branch index `k` may return

- `k even`: `[Lb, Ua]`;
- `k odd`: `[La, Ub]`.

Again, equality with a turning point is allowed once it is certified.

## 4. Source-boundary bridge to `P3.trig_endpoint_enclosure_leaf`

A minimal mathematical record for one canonical evaluator leaf is:

```text
kind : sin | cos
a b  : input endpoints
a_le_b : a <= b
k : Int
cell_cert :
  kind=sin -> pi/2+k*pi <= a and b <= pi/2+(k+1)*pi
  kind=cos -> k*pi <= a and b <= (k+1)*pi
endpoint_left  : La <= f(a) <= Ua
endpoint_right : Lb <= f(b) <= Ub
```

The bridge theorem then dispatches only on `(kind, parity k)` and applies the generic monotone endpoint lemma:

```text
increasing cell -> output [La, Ub]
decreasing cell -> output [Lb, Ua]
```

with postcondition

**`forall x, a <= x -> x <= b -> lower <= f(x) <= upper`.**

This is the exact contract that a source `iv_sin` / `iv_cos` cell must establish before invoking the abstract P3 endpoint-enclosure leaf. If the canonical evaluator instead returns a precomputed interval `J`, it is enough to prove that `J` outwardly contains the orientation-aware endpoint interval above.

## 5. Turning-point certification with outward `pi` bounds

If source code does not carry an exact symbolic branch certificate and instead constructs turning points numerically, branch certification itself must be outward-safe.

Suppose a turning point `t` has certified enclosure `[tL,tU]`.

To prove the left cell boundary lies before the input, `t <= a`, the sound comparison is

**`tU <= a`.**

To prove the input lies before the right cell boundary, `b <= t_next`, the sound comparison is

**`b <= tNextL`.**

Using `tL <= a` for the first obligation or `b <= tNextU` for the second is insufficient: those comparisons can pass even while the exact critical point lies inside `[a,b]`.

Consequently, if an outward critical-point interval overlaps an input endpoint so that the branch relation is not decidable, the correct result is **`SUBDIVIDE/UNDECIDED`**, not a guessed monotonicity branch. An upstream exact integer branch index can replace these numerical comparisons entirely; in that architecture the leaf need not evaluate `pi` itself and consumes the branch certificate as an assumption.

## 6. Exact obstruction: unsplit cells crossing a turning point

The split/domain obligation is mathematically necessary, not merely a limitation of this proof style.

### Sine witness

On `[0,pi]`,

`sin(0)=sin(pi)=0`,

but

`sin(pi/2)=1`.

Therefore the endpoint hull `[0,0]` is false as a range enclosure. Any generic endpoint-only leaf applied to this unsplit interval is unsound.

### Cosine witness

On `[-pi/2,pi/2]`,

`cos(-pi/2)=cos(pi/2)=0`,

while

`cos(0)=1`.

Again, endpoint values alone miss the interior extremum exactly.

Thus a cell crossing an interior trig turning point must either be split at every such point or handled by a different theorem that explicitly inserts the interior extremal value.

## 7. Finite split closure

Let

`a=t_0 <= t_1 <= ... <= t_n=b`

be a partition such that every `[t_i,t_(i+1)]` lies in one certified trig monotonicity cell. Suppose the local endpoint leaf gives a sound enclosure `I_i=[L_i,U_i]` on each subcell. Then the whole cell is enclosed by

**`[min_i L_i, max_i U_i]`.**

Proof: every `x in [a,b]` belongs to at least one covered subcell, so `f(x) in I_i` there, and every `I_i` is contained in the global hull. This separates the mathematical range proof from the implementation obligation that the source splitter actually produces a gap-free ordered partition.

## 8. Executable BigFloat/MPFR evidence still required

The exact mathematics above reduces the remaining source boundary to a short list of executable obligations:

1. outward construction/enclosure of `k*pi` and `pi/2+k*pi`, or an equivalent exact/certified branch-index mechanism;
2. sound branch comparisons proving the whole input interval lies in one monotonicity cell;
3. fail-closed subdivision/refinement if a turning-point relation is ambiguous or the input crosses a turning point, including gap-free coverage of the original cell;
4. directed-round lower/upper endpoint calls for `sin(a), sin(b)` or `cos(a), cos(b)`;
5. outward `min/max` hull operations when subcell results are merged;
6. if BigFloat endpoints are converted/serialized into exact rational interval endpoints, evidence that the conversion preserves outward containment.

Internal MPFR argument reduction does not need to be re-proved by this mathematical child if it is explicitly part of the admitted primitive trust boundary, but nearest-rounded endpoint calls or nearest-rounded turning-point comparisons are not substitutes for the directed obligations above.

## 9. Candidate theorem statements for formalization

The smallest useful theorem set is:

```text
trig_endpoint_enclosure_of_monotone
sin_critical_cell_monotone
cos_critical_cell_monotone
trig_monotone_cell_endpoint_leaf
trig_split_hull_enclosure
unsplit_sin_turning_point_endpoint_obstruction
unsplit_cos_turning_point_endpoint_obstruction
```

The first four are the direct bridge to `P3.trig_endpoint_enclosure_leaf`; the split theorem supports a canonical evaluator that recursively subdivides; the last two should remain as regression witnesses preventing accidental removal of the turning-point precondition.

## 10. Dependencies, assumptions, and remaining gap

Mathematical dependencies are only the standard monotonicity of real `sin/cos` on consecutive critical cells, endpoint order, and interval hull transitivity. No Lyapunov/provenance/admission or floating-point theorem is used here.

The remaining non-mathematical gap is source binding. Current repository inspection/search did not expose a uniquely identifiable source implementation under the declared names `iv_sin` or `iv_cos`; therefore I do not claim that the canonical Route-B evaluator already meets the directed-rounding and branch-certification contract. The source owner/coordinator still needs to identify the actual call site (or its differently named equivalent) and attach the executable MPFR/BigFloat evidence listed in Section 8.

**Status: pending mathematical/source-boundary child.** The exact endpoint/turning-point theorem and obstruction are closed; executable evaluator binding is not.
