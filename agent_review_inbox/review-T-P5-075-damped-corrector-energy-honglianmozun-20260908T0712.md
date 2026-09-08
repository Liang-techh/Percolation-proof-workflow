---
kind: review_result
review_id: review-T-P5-075-damped-corrector-energy-honglianmozun-20260908T0712
task_id: T-P5-075-DAMPED-CORRECTOR-ENERGY
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-08T07:12:00-06:00
claim_commit: c9cd94b7c907133ec74b3b305c34f48bb6a9ba97
inspected_commits:
  - 48c78207c758636227a8bb3f5be2e1f6c247e6c4
  - 18618ab0213677d83867b347a3b3acd7c9857b98
inspected_paths:
  - agent_review_inbox/review-T-P5-074-weighted-strong-monotone-scc-guyuefangyuan-20260908T0700.md
  - agent_review_inbox/review-T-P5-073-affine-offset-relative-decay-kuangmanmozun-20260908T0655.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Add this only as a downstream Lyapunov/corrector consumer of a same-weight
  strong-monotonicity plus squared-Lipschitz packet. Do not merge it into the
  T-P5-074 source certificate itself. The persistent-defect barrier is a
  candidate consumer for T-P5-073/O2-style evaluator bounds, but no deployed
  source or iteration is certified here.
---

# T-P5-075 — damped corrector Lyapunov descent and sharp evaluator-defect barrier

## 0. Result in one line

T-P5-074 gives a useful weighted strong-monotonicity certificate for a general
contact SCC, but **strong monotonicity alone does not certify the explicit
corrector used to invert the chart**. If, in the same weighted norm, one also
has the squared secant bound

`||F(x)-F(y)||_W^2 <= Lambda ||x-y||_W^2`,

then the damped corrector

`T_h(x) = x - h F(x)`

has the exact Lyapunov factor

`q_h = 1 - 2 h mu + h^2 Lambda`.

The division-free strict step gate is

`h > 0`, `h Lambda < 2 mu`.

For a certified evaluator defect `e`, the first-exit test can be made **sharp
at the norm-envelope level and entirely radical-free**. If `V*=Vstar>0`,
`||e||_W^2<=E`, and

`R = (1-q_h)Vstar - h^2 E`,

then

`R > 0`,

`4 h^2 q_h Vstar E < R^2`

imply one defective corrector step remains strictly inside `V<Vstar`.
No Young parameter, square root, matrix inverse, or eigenvalue is needed in the
trusted scalar gate.

This is a mathematics-only downstream child. It does not prove a deployed
source Lipschitz constant, an actual P5 corrector implementation, Float64/FD/
controller/solve semantics, P8/ODE coverage, Lean compilation, provenance,
admission, or parent closure.

---

## 1. Direct connection to T-P5-074

T-P5-074 studies the chart map

`Phi_y(x) = x - rho(x,y)`.

For a requested chart coordinate `xi`, inversion is the root problem

`F_xi(x) = Phi_y(x) - xi = 0`.

The target `xi` disappears from every secant:

`F_xi(x)-F_xi(x') = Phi_y(x)-Phi_y(x')`.

Therefore any weighted strong-monotonicity certificate for `Phi_y` is inherited
unchanged by `F_xi`. The only genuinely new analytic input required by the
explicit corrector is a same-domain, same-weight squared-Lipschitz packet.

Let `W=diag(w_i)` with `w_i>0`. Write

`<u,v>_W = sum_i w_i u_i v_i`,

`Q(u) = ||u||_W^2 = <u,u>_W`.

Assume for all relevant `x,x'` in the certified box, with

`d = x-x'`, `f = F(x)-F(x')`,

that

**(SM)** `<f,d>_W >= mu Q(d)`, with `mu>0`,

and

**(L2)** `Q(f) <= Lambda Q(d)`, with `Lambda>=0`.

The use of `Lambda` as a **squared** Lipschitz constant is deliberate: all
checker gates below remain polynomial/rational.

---

## 2. Exact damped-corrector energy identity

Define

`T_h(x)=x-h F(x)`.

Then

`T_h(x)-T_h(x') = d-hf`,

so bilinearity gives the exact identity

**(2.1)**

`Q(d-hf) = Q(d) - 2h <f,d>_W + h^2 Q(f)`.

Using (SM) and (L2), for `h>=0`,

**(2.2)**

`Q(T_h(x)-T_h(x'))`

`<= [1 - 2h mu + h^2 Lambda] Q(x-x')`.

Define

**(2.3)** `q_h := 1 - 2h mu + h^2 Lambda`.

This is the exact source-independent Lyapunov consumer.

### Theorem 2.1 — weighted damped-corrector secant contraction

Under (SM), (L2), and `h>=0`,

`Q(T_h(x)-T_h(x')) <= q_h Q(x-x')`.

No differentiability is required once the two secant inequalities are supplied.

---

## 3. Division-free strict-step gate and nonnegativity

The strict reserve is itself polynomial:

**(3.1)**

`1-q_h = h(2mu-h Lambda)`.

Hence

**(3.2)**

`h>0` and `h Lambda < 2mu`

imply `q_h<1`.

For nonnegativity, the natural compatibility relation is

`mu^2 <= Lambda`.

Then the exact SOS decomposition is

**(3.3)**

`q_h = (1-h mu)^2 + h^2 (Lambda-mu^2) >= 0`.

On any nontrivial secant, `mu^2<=Lambda` is in fact forced by (SM), weighted
Cauchy, and (L2):

`mu Q(d) <= <f,d>_W`,

`<f,d>_W^2 <= Q(f)Q(d) <= Lambda Q(d)^2`.

If `Q(d)>0`, canceling `Q(d)^2` gives `mu^2<=Lambda`.

Thus a checker-friendly strict contraction packet is

`0 < mu`, `0 <= Lambda`, `mu^2 <= Lambda`, `0 < h`,

`h Lambda < 2mu`.

It yields

`0 <= q_h < 1`.

### Sharp step boundary

Take the one-dimensional linear map

`F(x)=mu*x`, `mu>0`.

Here the exact squared-Lipschitz constant is `Lambda=mu^2`, and

`T_h(x)=(1-hmu)x`,

`q_h=(1-hmu)^2`.

At the boundary `h Lambda = 2mu`, equivalently `hmu=2`, one has `q_h=1` and
`T_h(x)=-x`: energy is preserved, not strictly decreased. Beyond that boundary
energy expands. Therefore `h Lambda < 2mu` cannot be enlarged uniformly from
only the `(mu,Lambda)` packet.

---

## 4. Optimal-step identity without calculus or radicals

Assume `Lambda>0`. The entire step-size optimization is encoded by one square:

**(4.1)**

`Lambda q_h - (Lambda-mu^2) = (Lambda h-mu)^2`.

Consequently

`Lambda q_h >= Lambda-mu^2`

for every `h`, and the exact minimum is attained precisely when

**(4.2)** `Lambda h = mu`.

This is preferable to exposing the quotient `h=mu/Lambda` in a trusted
checker. A rational checker can simply verify the product equality (or a small
rational neighborhood if a prescribed step cannot attain it exactly).

At (4.2),

**(4.3)** `Lambda q_h = Lambda-mu^2`.

Thus even the optimal-rate comparison can remain division-free.

Candidate Lean proof shape: `ring` for (4.1), `sq_nonneg`, then `nlinarith`.

---

## 5. Root Lyapunov function

Suppose T-P5-074's existence layer supplies a root `x*` of `F`, so `F(x*)=0`.
Set

`V(x)=Q(x-x*)`.

Theorem 2.1 with `x'=x*` gives

**(5.1)** `V(T_h(x)) <= q_h V(x)`.

Therefore, on any source domain where the same `(mu,Lambda,W)` packet remains
valid, the strict step gate gives geometric Lyapunov decrease. To promote this
to an actual iterative solver theorem one still needs the relevant weighted
ball/sublevel to lie inside the certified source box (or a separate self-map
argument). This domain premise is intentionally not hidden in the algebraic
child.

---

## 6. Certified evaluator defect

Now suppose the evaluated residual is perturbed by a vector `e`:

**(6.1)** `x_plus = x - h(F(x)+e)`.

Let

`d=x-x*`, `f=F(x)`, `a=d-hf`.

Then

`d_plus = a-he`,

and the exact energy identity is

**(6.2)**

`Q(d_plus) = Q(a) - 2h<a,e>_W + h^2 Q(e)`.

The exact corrector theorem gives

`Q(a) <= q_h Q(d)`.

Assume a certified defect budget

**(6.3)** `Q(e) <= E`, `E>=0`.

At a proposed barrier `Vstar>0`, every point with `V(x)<=Vstar` therefore
satisfies

`Q(a) <= q_h Vstar`,

and weighted Cauchy gives

**(6.4)**

`<a,e>_W^2 <= q_h Vstar E`.

---

## 7. Sharp radical-free first-exit barrier gate

Define the scalar reserve

**(7.1)**

`R := (1-q_h)Vstar - h^2 E`.

Assume

**(7.2)** `R>0`,

and

**(7.3)**

`4 h^2 q_h Vstar E < R^2`.

From (6.4),

`4h^2 <a,e>_W^2 <= 4h^2 q_h Vstar E < R^2`.

Because `R>0` and `2h|<a,e>_W|>=0`, this implies

`2h|<a,e>_W| < R`.

Using (6.2),

`Q(d_plus)`

`<= q_h Vstar + 2h|<a,e>_W| + h^2E`

`< q_h Vstar + R + h^2E`

`= Vstar`.

Hence:

### Theorem 7.1 — defective corrector strict barrier

If

`0<=q_h<1`, `h>=0`, `Vstar>0`, `E>=0`,

`R=(1-q_h)Vstar-h^2E>0`,

`4h^2 q_h Vstar E < R^2`,

then every state with `V<=Vstar` and every evaluator defect with `Q(e)<=E`
are mapped strictly into `V<Vstar`.

This theorem has no square roots and no tunable Young parameter. The scalar
gate is built only from addition, multiplication, squares, and strict rational
comparison.

### Why the two inequalities are the exact envelope-level gate

Let

`A=q_h Vstar`, `H=h^2E`.

The worst independent norm-envelope case is attained when `a` and `e` are
oppositely aligned, giving output norm

`sqrt(A)+sqrt(H)`.

The strict condition

`(sqrt(A)+sqrt(H))^2 < Vstar`

is exactly equivalent to

`R=Vstar-A-H>0`,

`R^2>4AH`.

But `4AH=4h^2 q_h Vstar E`, which is precisely (7.2)-(7.3). Thus the polynomial
gate is not merely a convenient Young relaxation: it is sharp for the
uncertainty class described only by the two independent squared-norm bounds.

A one-dimensional aligned witness saturates the boundary, so no universally
larger bias budget can be certified from only `(q_h,Vstar,h,E)`.

---

## 8. Exact obstruction: strong monotonicity alone is not enough

A strong-monotonicity certificate such as T-P5-074's does **not** by itself
justify a fixed explicit corrector step.

Take on `R`

**(8.1)** `F(x)=x+x^3`.

For all `x,y`,

`(F(x)-F(y))(x-y)`

`=(x-y)^2 [1+x^2+xy+y^2]`

and

`x^2+xy+y^2 = (x+y/2)^2 + 3y^2/4 >= 0`.

Therefore `F` is globally `mu=1` strongly monotone.

But for any fixed `h>0`,

`T_h(x)=x-h(x+x^3)`,

so for `x!=0`,

`|T_h(x)|/|x| = |1-h-hx^2| -> infinity`

as `|x|->infinity`.

Hence there is no global contraction factor for any fixed positive step. A
same-domain squared-Lipschitz/derivative upper bound (or a state-dependent line
search/trust region theorem) is a real mathematical obligation, not a proof
artifact.

This is an exact obstruction to the invalid implication

`strong monotonicity => globally stable explicit corrector`.

---

## 9. Persistent evaluator bias cannot converge to the original root

Even when the exact corrector is contractive, a nonzero persistent evaluator
bias generally prevents convergence to the true root.

Take the one-dimensional linear map

`F(x)=mu x`, `mu>0`,

with constant defect `e=b!=0` and a stable step `0<hmu<2`.

Then

`x_plus=(1-hmu)x-hb`.

Its unique fixed point is

**(9.1)** `x_bias = -b/mu`,

not `0`.

Thus an absolute evaluator defect must be consumed as an invariant/ultimate
ball or first-exit budget; it cannot be silently relabelled as a zero-convergent
relative error. This is consistent with the zero-slice obstruction in
T-P5-073, but here it appears directly at the Lyapunov-iteration consumer.

---

## 10. Candidate formal statements

A minimal formalization can be split into source-independent scalar/vector
leaves:

1. `weighted_corrector_energy_identity`
   - exact expansion of `Q(d-hf)`.

2. `weighted_corrector_contraction_of_strong_mono_lipschitz_sq`
   - consumes `(SM)` and `(L2)` and returns `Q(nextDiff)<=q_h Q(diff)`.

3. `corrector_factor_nonneg_of_mu_sq_le_Lambda`
   - uses
     `q_h=(1-hmu)^2+h^2(Lambda-mu^2)`.

4. `corrector_strict_step_gate`
   - `h>0`, `h Lambda<2mu` imply `q_h<1`.

5. `corrector_optimal_step_square_identity`
   - `Lambda*q_h-(Lambda-mu^2)=(Lambda*h-mu)^2`.

6. `defective_corrector_radical_free_barrier`
   - consumes squared Cauchy plus (7.2)-(7.3) and yields `V_plus<Vstar`.

7. `linear_step_boundary_sharp`
   - one-dimensional `F(x)=mu*x` witness for `h Lambda=2mu`.

The core algebra can be kept independent of matrix APIs. A diagonal-weight
finite-sum adapter may be added later if T-P5-074's exact `W` packet is selected
for formal consumption.

---

## 11. Dependencies and unresolved obligations

This child can consume T-P5-074 only after a concrete SCC packet supplies the
same positive diagonal weight `W` and strong-monotonicity constant `mu`.
It additionally needs a **same-box, same-weight squared-Lipschitz constant
`Lambda`** for the chart residual. T-P5-074 does not provide that constant by
itself.

For the defective gate, the evaluator error must be in the same root-residual
coordinates and weighted norm. An acceleration-space, force-space, or unrelated
absolute error cannot be substituted without a typed coordinate bridge.

No statement here proves that the deployed solver actually performs
`x-hF(x)`, that an iterate stays in the source box, that a Float64 evaluator
satisfies `Q(e)<=E`, or that a selected `h` is used by deployed code.

Accordingly this review remains **pending mathematical child**. The useful next
mathematical/source seam is narrow: obtain one concrete same-weight `Lambda`
(or prove a local trust-region version) before attempting any solver-level
closure.

## Evidence boundary

- Mathematical derivation: exact bilinear expansions, weighted Cauchy, square
  completion, and explicit one-dimensional counterexamples.
- No Lean/Lake compile executed in this review.
- No source comparator, Float64 checker, coverage checker, registry mutation,
  provenance audit, or admission action was performed.
