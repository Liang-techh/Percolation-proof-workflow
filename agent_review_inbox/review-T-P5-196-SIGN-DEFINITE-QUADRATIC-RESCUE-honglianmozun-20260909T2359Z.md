---
kind: review_result
review_id: review-T-P5-196-sign-definite-quadratic-rescue-honglianmozun-20260909T2359Z
task_id: T-P5-196-SIGN-DEFINITE-QUADRATIC-RESCUE
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T23:59:00Z
claim_commit: 63bb1602b273c69b60c539bcd8ea85cf28fac361
inspected_commit: 8a2330df003fb53b5642daef814f073f7e1ef979
upstream_commits:
  - 86d3e6a59cf11c4d1bd28ffa5a6ab7a66cd20eda  # T-P5-192 selector-cone Lyapunov margin
  - f6a493131c273ba0739ede6c2f7a986b71660ae1  # T-P5-194 correlated-zonotope defect adapter
  - 85a96adf98569071e07bb7b8b2ed1f098d492d35  # T-P5-195 projected-skew affine-generator gate
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_exact_fixed_sign_cone_gate; add_affine_amplitude_cubic_obstruction; route_constant_on_cone_amplitudes_back_to_TP5_192; preserve_bounded_domain_fallback
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional cone scaling, copositivity pullback, homogeneous-degree separation, rational strict-ray construction; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-196 — exact sign-definite rescue for failed projected-skew sectors, and the cubic Lyapunov obstruction

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-195 left one particularly useful nongeneric rescue route open. If the projected-skew gate fails, the projected generator scalar

`phi(e) = ell^T e + e^T S e`, `S=S^T`,

need not have a curved sign change: it may still be nonnegative or nonpositive on the entire selector cone. This review proves that, on an unbounded polyhedral cone, fixed sign is decidable **exactly** by the already-developed linear and copositivity machinery.

For `C=cone(V)`, and `sigma in {+1,-1}`, the following are equivalent:

**`sigma phi(e) >= 0` for every `e in C`**

iff both

**`sigma V^T ell >= 0` entrywise**

and

**`sigma V^T S V` is copositive.**

So T-P5-195 projected-skew failure does not force a semialgebraic sign split. A fixed-sign quadratic projection can be rescued with one exact linear sign test plus one ordinary copositivity test.

However, there is an important second result. For an affine nonnegative zonotope amplitude

`a(e)=h^T e+h0 >= 0`,

the fixed-sign identity removes the absolute value but generically creates a **positive cubic robust defect**:

`a(e)|phi(e)| = sigma (h^T e+h0)(ell^T e+e^T S e)`.

Under the fixed-sign and amplitude-nonnegativity gates, its degree-three leading form is

**`p3(e) = (h^T e) [sigma e^T S e] >= 0` on `C`.**

If both factors are nontrivial on the cone, there is a ray on which `p3>0`; hence no global Lyapunov inequality whose remaining terms grow only quadratically can dominate this defect on the whole unbounded cone. Thus fixed sign rescues the **sign geometry**, but not automatically the **quadratic degree** needed by T-P5-192.

There is an exact dichotomy: under the nonnegativity gates, the cubic leading form vanishes identically on `C` iff either

1. `h^T e=0` for all `e in C` — the amplitude is constant on the consumed cone; or
2. `e^T S e=0` for all `e in C` — equivalently `V^T S V=0`, which collapses back to the T-P5-195 projected-skew/degree-preserving branch on the cone span.

No source extraction, deployed residual containment, selector coverage, Float64/controller/PDE semantics, Lean/kernel proof, independent verification, admission, or registry promotion is claimed.

---

## 1. Setup

Fix one selector cone

`C = cone(V) = { V y : y >= 0 }`.

The columns of `V` are finite cone generators. The cone may be lower dimensional.

For one affine state-rotating generator from T-P5-195, after symmetrizing the quadratic part write

`phi(e) = ell^T e + e^T S e`,

where

`ell = G^T z0`,

and

`S = (R^T G + G^T R)/2`.

Only `S` matters to the scalar quadratic form.

Let the zonotope amplitude be

`a(e)=h^T e+h0`.

The pointwise support identity still gives a contribution proportional to

`a(e)|phi(e)|`

whenever `a(e)>=0`.

The questions are:

1. can `phi` have a fixed sign on all of `C` even when `S` is nonzero?;
2. if yes, does removing `|.|` preserve the quadratic Lyapunov route?

The answers are respectively **yes** and **only under an additional degree gate**.

---

## 2. T196-A — homogeneous-degree separation on a cone

Define for one ray direction `r in C`

`l(r)=ell^T r`,

`q(r)=r^T S r`.

For every `t>=0`, because `C` is a cone,

`t r in C`,

and

`phi(t r)=t l(r)+t^2 q(r)`.

### Theorem A1 — nonnegative sign

The following are equivalent:

1. `phi(e)>=0` for every `e in C`;
2. `ell^T e>=0` and `e^T S e>=0` for every `e in C`.

### Proof

`(2)->(1)` is immediate by addition.

For `(1)->(2)`, fix `r in C`.

If `l(r)<0`, then for sufficiently small positive `t`, the linear term `t l(r)` dominates `t^2 q(r)`, giving `phi(t r)<0`, contradiction. Hence `l(r)>=0`.

If `q(r)<0`, then for sufficiently large positive `t`, the quadratic term `t^2 q(r)` dominates `t l(r)`, again giving `phi(t r)<0`. Hence `q(r)>=0`.

Since `r` was arbitrary, both homogeneous pieces are nonnegative on the cone.

### Theorem A2 — nonpositive sign

Likewise,

`phi(e)<=0` for every `e in C`

iff

`ell^T e<=0` and `e^T S e<=0` for every `e in C`.

Apply Theorem A1 to `-phi`.

### Unified form

For `sigma in {+1,-1}`,

**`sigma phi >=0 on C`**

iff

**`sigma ell^T e>=0` and `sigma e^T S e>=0` on C.**

This is stronger than a sufficient bound: cone scaling makes it exact.

---

## 3. T196-B — exact pullback to the existing copositivity checker

Write `e=V y`, `y>=0`.

Then

`ell^T e = (V^T ell)^T y`,

so

`ell^T e>=0 for all e in C`

iff

**`V^T ell >=0` entrywise.**

Necessity follows by choosing `y` to be each standard basis vector; sufficiency follows because every coefficient of `y` is nonnegative.

For the quadratic term,

`e^T S e = y^T (V^T S V) y`.

Therefore

`e^T S e>=0 for all e in C`

iff

**`V^T S V` is copositive.**

Hence the exact fixed-sign theorem is:

### Theorem B — cone fixed-sign iff gate

For `sigma in {+1,-1}`,

**`sigma phi(e)>=0` for all `e in cone(V)`**

iff

1. **`sigma V^T ell >=0` entrywise**, and
2. **`sigma V^T S V` is copositive.**

This is precisely compatible with the T-P5-158+ fixed-rational copositivity stack: PSD/Z/forest/pivot fast paths may be used first, with support-KKT fallback if needed.

If `V,S,ell` are rational, the entire packet is rational.

No polynomial root isolation or curved sign-cell decomposition is needed for this branch.

---

## 4. T196-C — exact nonnegative affine-amplitude gate on an unbounded cone

Before multiplying by `a(e)`, its nonnegativity should itself be checked exactly.

For

`a(e)=h^T e+h0`,

the condition

`a(e)>=0` for every `e in C`

is equivalent to

**`h0>=0` and `V^T h>=0` entrywise.**

### Proof

At `e=0`, nonnegativity forces `h0>=0`.

Along every ray `t r`,

`a(t r)=t h^T r+h0`.

If `h^T r<0`, large `t` violates nonnegativity. Hence `h^T r>=0` on `C`, equivalent to `V^T h>=0` entrywise.

Conversely these conditions plainly imply `a(e)>=0`.

This gate is useful because it gives the sign of every homogeneous factor used below.

---

## 5. T196-D — fixed sign removes the absolute value exactly

Assume the Theorem B gate for one `sigma`, so

`sigma phi(e)>=0` on `C`.

Then

**`|phi(e)| = sigma phi(e)`**

for every `e in C`.

If also `a(e)>=0`, then

`a(e)|phi(e)|`

`= sigma (h^T e+h0)(ell^T e+e^T S e)`

`= sigma h0 ell^T e`

`  + sigma h0 e^T S e`

`  + sigma (h^T e)(ell^T e)`

`  + sigma (h^T e)(e^T S e)`.

The first term is linear, the next two are quadratic, and the final term is cubic.

The middle bilinear scalar can be written as a symmetric quadratic form:

`(h^T e)(ell^T e)`

`= e^T [(h ell^T + ell h^T)/2] e`.

Thus the only degree-three term is

**`p3(e)=sigma (h^T e)(e^T S e)`.**

---

## 6. T196-E — constant-amplitude rescue returns exactly to T-P5-192

If the amplitude is constant on the consumed cone, i.e.

`h^T e=0` for every `e in C`,

then on `C`

`a(e)=h0`,

and

`a(e)|phi(e)| = sigma h0 ell^T e + sigma h0 e^T S e`.

This is exactly quadratic-plus-linear.

For the common full-dimensional representation this is simply `h=0`; for a lower-dimensional cone the exact generator gate is

**`V^T h=0`.**

Therefore a T-P5-195 projected-skew failure can still be fully rescued into the T-P5-192 quadratic/copositive Lyapunov route when:

1. `phi` has fixed sign by Theorem B; and
2. the amplitude linear part vanishes on the selector cone.

The resulting robust contribution can be merged into T-P5-192 by adding

`Q_defect = sigma h0 S`,

`r_defect = sigma h0 ell`,

with the usual outer support factor (for example the factor `2` already used in T-P5-194/195) applied by the consumer.

No semialgebraic split and no higher-degree positivity engine is needed.

---

## 7. T196-F — the cubic leading form is nonnegative

Assume both:

- fixed sign: `sigma phi>=0` on `C`;
- amplitude nonnegativity: `a>=0` on `C`.

By Theorem A, the homogeneous pieces satisfy

`sigma e^T S e>=0`,

and by Theorem C,

`h^T e>=0`

for every `e in C`.

Therefore

**`p3(e)=(h^T e)[sigma e^T S e] >=0` on `C`.**

This is an important direction-of-sign fact: the cubic term is not an oscillatory remainder that might help the Lyapunov derivative. It is the leading part of a worst-case support penalty and is nonnegative on the entire fixed-sign sector.

---

## 8. T196-G — exact cubic-vanishing dichotomy

Under the same nonnegativity gates, the following are equivalent:

1. `p3(e)=0` for every `e in C`;
2. either `h^T e=0` for every `e in C`, or `e^T S e=0` for every `e in C`.

### Proof

The reverse direction is immediate.

For the forward direction, suppose neither factor vanishes identically.

Then there exists `x in C` with

`h^T x>0`,

and there exists `y in C` with

`sigma y^T S y>0`.

Because `C` is a convex cone, `y+eps x in C` for every `eps>=0`.

The first factor obeys

`h^T(y+eps x) >= eps h^T x >0`

for every `eps>0`.

The quadratic factor is continuous in `eps` and is strictly positive at `eps=0`, so it remains strictly positive for all sufficiently small positive `eps`.

Thus `p3(y+eps x)>0`, contradiction.

Hence one factor must vanish identically.

### Exact generator-matrix form

The first alternative is equivalent to

**`V^T h=0`.**

The second is equivalent to

**`V^T S V=0`.**

Indeed, if `A=V^T S V` is symmetric and `y^T A y=0` for every `y>=0`, choosing `y=e_i` gives all diagonals zero and choosing `y=e_i+e_j` gives all off-diagonals zero.

Therefore:

**`p3 identically zero on C` iff `V^T h=0` or `V^T S V=0`.**

The second branch is exactly the old degree-preserving condition on the consumed cone: the quadratic projected term vanishes there. So, apart from returning to projected-skew, the only genuinely new way to keep degree <=2 is for the amplitude to be constant on the cone.

---

## 9. T196-H — global quadratic Lyapunov-rate obstruction

Suppose the remaining frozen Lyapunov derivative plus target decay terms have degree at most two along the external state:

`B(e)=e^T K e + d^T e + b0`

(or any function satisfying `B(t r)=O(t^2)` on each fixed ray).

Assume the robust defect appears with a positive prefactor `c>0`:

`B(e) + c a(e)|phi(e)| <= 0`.

If there exists `r in C` with

`p3(r)>0`,

then this inequality cannot hold on the full unbounded ray `{t r:t>=0}`.

### Proof

Along the ray,

`a(t r)|phi(t r)|`

has leading term

`t^3 p3(r)`.

Hence

`B(t r)+c a(t r)|phi(t r)|`

`= c p3(r) t^3 + O(t^2)`.

Since `c p3(r)>0`, the expression is strictly positive for all sufficiently large `t`.

Therefore no global nonpositivity inequality is possible.

### Consequence for T-P5-192

T-P5-192 certifies a quadratic storage / quadratic-rate derivative packet on selector cones. If a failed projected-skew generator is rescued only by fixed sign, while both

`V^T h != 0`

and

`V^T S V != 0`, 

then the robust support term has a strictly positive cubic ray and **cannot** be absorbed into the same global quadratic-rate checker on an unbounded cone.

This is a mathematical degree obstruction, not a source/admission problem.

The correct next route is one of:

1. use a physical bounded-domain cap and explicitly absorb the linear amplitude into a finite coefficient;
2. redesign the storage/dissipation with a higher-degree term;
3. prove the amplitude is actually constant on the consumed cone;
4. prove the projected quadratic part vanishes on the consumed cone after all;
5. use a different residual representation with lower state degree.

---

## 10. T196-I — rational strict-ray witness when the cubic is nontrivial

For rational checker data, the obstruction can be made exact.

Let

`cvec = V^T h >=0`,

`A = sigma V^T S V`,

with `A` rational, symmetric, and copositive.

Assume

`cvec != 0`,

`A != 0`.

Then there exists a rational `y>=0` such that

`cvec^T y>0`,

`y^T A y>0`.

### Construction

Choose a basis vector `e_j` with `cvec_j>0`.

Because `A` is copositive and nonzero, there is a rational nonnegative vector `y_q` with positive quadratic value:

- if some `A_ii>0`, take `y_q=e_i`;
- otherwise all diagonals are zero. Copositivity then forces every `A_ij>=0`; since `A!=0`, some `A_ij>0`, and `y_q=e_i+e_j` gives `y_q^T A y_q=2A_ij>0`.

Now take

`y = y_q + eps e_j`

with any sufficiently small positive rational `eps`. Then `cvec^T y>0`, while continuity (equivalently, an exact rational polynomial check in `eps`) preserves `y^T A y>0`.

Set

`r=V y`.

Then `r in C` and `p3(r)>0` exactly.

So the FAIL side of the global quadratic-rate branch can carry an exact rational ray witness; it need not rely on floating scaling experiments.

---

## 11. Decisive rational regression

Take

`C=R_+^2`, `V=I`,

`S=[[1,0],[0,0]]`,

`ell=(0,1)`.

Then

`phi(x,y)=x^2+y`.

The T-P5-195 projected-skew gate fails because `S!=0`, but the T196 fixed-sign gate passes exactly:

`V^T ell=(0,1)>=0`,

and

`V^T S V=S`

is PSD, hence copositive.

Therefore

`phi>=0` on the whole positive quadrant and no semialgebraic sign subdivision is needed.

### Constant-amplitude rescue

If

`a(x,y)=1`,

then

`a|phi|=x^2+y`,

which is exactly quadratic-plus-linear and can be returned to the T-P5-192 cone/copositivity route.

### Affine-amplitude obstruction

If instead

`a(x,y)=1+x`,

then

`a|phi|=(1+x)(x^2+y)`

`=x^3+x^2+xy+y`.

Along the cone ray `(t,0)`, this is

`t^3+t^2`.

Thus no negative quadratic base term `-K t^2` with finite `K` can dominate the robust defect for all `t>=0`.

This example cleanly separates:

- **fixed sign / no curved sign cells**: PASS;
- **quadratic degree preservation**: FAIL unless the amplitude linear growth is removed or the domain is bounded.

---

## 12. Checker routing

For each state-rotating generator on one T-P5-192 selector cone:

1. Try T-P5-195 projected-skew gate `V^T S V=0` (equivalently the restricted symmetric projected matrix vanishes).
2. If that fails, try T196 fixed-sign gates for `sigma=+1` and `sigma=-1`:
   - linear: `sigma V^T ell>=0` entrywise;
   - quadratic: `sigma V^T S V` copositive.
3. If neither sign passes, route to factorization / semialgebraic sign-cell machinery; do **not** report mathematical FAIL.
4. If fixed sign passes, remove the absolute value exactly.
5. Check amplitude nonnegativity by `h0>=0`, `V^T h>=0`.
6. For reuse of the global T-P5-192 quadratic-rate checker on an unbounded cone, require either:
   - `V^T h=0` (amplitude constant on the cone), or
   - `V^T S V=0` (which actually returns to T-P5-195).
7. If both are nonzero, construct/record a strict cubic ray witness and route to a bounded-domain or higher-degree Lyapunov branch rather than forcing an unsound quadratic absorption.

This keeps the dispatcher fail-closed while rescuing a substantial class of projected-skew failures.

---

## 13. Minimal formal theorem statements

Suggested source-independent leaves:

1. `quadLinear_nonneg_on_cone_iff_parts_nonneg`
   - for a cone `C`, `ell^T x+x^T S x>=0` on `C` iff both homogeneous parts are nonnegative on `C`.

2. `quadLinear_sign_on_finitelyGeneratedCone_iff`
   - for `C=cone(V)`, fixed sign `sigma` iff `sigma V^T ell>=0` entrywise and `sigma V^T S V` is copositive.

3. `affine_nonneg_on_finitelyGeneratedCone_iff`
   - `h^T x+h0>=0` on `cone(V)` iff `h0>=0` and `V^T h>=0`.

4. `fixedSign_abs_projection_expand`
   - under fixed sign and amplitude nonnegativity, expand `a|phi|` into linear, quadratic, and the single cubic leading term.

5. `nonnegative_cubic_product_zero_iff`
   - if `h^T x>=0` and `sigma x^T S x>=0` on a convex cone, their product vanishes identically iff one factor does.

6. `affineAmplitude_quadraticRate_ray_obstruction`
   - a strictly positive cubic coefficient on one cone ray rules out domination by any degree-2 Lyapunov-rate polynomial on the full ray.

The first three are cone scaling / finite-dimensional linear algebra. The copositivity predicate should reuse the existing theorem/checker stack rather than be reimplemented.

---

## 14. What this closes

The T-P5-195 failure branch can now be refined as

`projected-skew fails`

`-> test fixed sign of phi by linear + copositive gates`

`-> if fixed sign fails: semialgebraic/factorization branch`

`-> if fixed sign passes: remove |phi| exactly`

`-> if amplitude constant on consumed cone: quadratic-plus-linear defect`

`-> reuse T-P5-192`

while

`fixed sign + genuinely affine amplitude + genuinely quadratic projection`

produces an exact positive cubic ray and therefore cannot be silently fed to the old global quadratic-rate checker on an unbounded cone.

This closes both a positive rescue route and the precise energy obstruction that limits it.

---

## 15. Remaining open boundaries

This result does not close:

1. actual extraction of `ell,S,h,h0,V` from one deployed residual / selector packet;
2. proof that the physical residual is contained in the state-dependent zonotope on the full cell or tube;
3. bounded physical-domain absorption of the affine-amplitude cubic term;
4. special factorable but sign-changing quadratics requiring only a finite linear split;
5. generic semialgebraic sign cells;
6. higher-degree Lyapunov/storage redesign if the cubic obstruction is genuine globally;
7. state-dependent selector gradient beyond the T-P5-195 linear `G e` contract;
8. state-rotating viability quadratic-on-faces;
9. Float64/controller/FD semantics, PDE unresolved-mode reduction, P8/M4 physical coverage, Lean/kernel compilation, independent verification by 封不觉, admission, or registry promotion.

The smallest useful next mathematical child is a **bounded-cone-slice cubic absorption theorem**: if the physical selector region additionally carries an exact cap on `h^T e` (or another homogeneous gauge), convert `a(e)|phi(e)|` into a quadratic-plus-linear upper bound without discarding correlation, and quantify the sharp extra Lyapunov debit.