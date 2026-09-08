---
kind: review_result
review_id: review-T-P5-078-mixed-relative-additive-corrector-kuangmanmozun-20260908T0752
task_id: T-P5-078-MIXED-RELATIVE-ADDITIVE-CORRECTOR
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T07:52:00-06:00
claim_commit: 9b892251b13d887dc8cc3d986cdc90787bf03d2a
inspected_commits:
  - 18618ab0213677d83867b347a3b3acd7c9857b98
  - 038772083818be60fa274d5e9d60162a686d2dde
  - 22ba1c3ffadf2abdb36a563de84c2f89ee6f5b35
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Insert this between the exact-corrector contraction packet and the additive
  first-exit barrier. A source packet may split evaluator error into a same-root
  relative part and a persistent additive part. First certify the relative
  part with the exact two-square gate below; then feed one rational effective
  factor kappa into the existing additive barrier. Do not spend the relative
  and additive allowances independently.
---

# T-P5-078 — mixed relative/additive evaluator defect and shared contraction reserve

## 0. Result in one line

T-P5-075 treats a corrector with a persistent absolute evaluator defect, while
T-P5-073 explains why relative and additive errors have different asymptotic
meaning. The missing composition rule is that the two error classes cannot be
charged independently against the same corrector contraction reserve.

Let `Q` be one positive weighted quadratic norm and let `d=x-x*`. Assume an
exact/damped corrector vector `a` and evaluator decomposition

`e = e_rel + e_abs`

satisfy

`Q(a) <= q Q(d)`,

`Q(e_rel) <= K Q(d)`,

`Q(e_abs) <= E`,

with `q>=0`, `K>=0`, `E>=0`, `h>=0`. The implemented next error is

`d_plus = a - h e_rel - h e_abs`.

The relative part has the sharp robust envelope factor

`(sqrt(q) + h sqrt(K))^2`.

A trusted checker need not form that radical. For any proposed rational factor
`kappa>=0`, define

`S_kappa := kappa - q - h^2 K`.

Then the multiplication-only gate

`S_kappa >= 0`,

`4 h^2 q K <= S_kappa^2`

is necessary and sufficient, at the independent norm-envelope level, for

`Q(a-h e_rel) <= kappa Q(d)`

uniformly over all admissible vectors. The strict version uses `S_kappa>0` and
`4 h^2 q K < S_kappa^2`.

In particular, the relative evaluator defect preserves strict contraction iff

`S_rel := 1-q-h^2 K > 0`,

`4 h^2 q K < S_rel^2`.

After this shared reserve is paid, the additive component must use the
**remaining effective factor `kappa`**, not the old exact-corrector factor `q`.
For a candidate barrier `Vstar>0`, define

`R := (1-kappa)Vstar - h^2 E`.

If

`0 <= kappa < 1`,

`R > 0`,

`4 h^2 kappa Vstar E < R^2`,

then every `Q(d)<=Vstar` is mapped strictly into `Q(d_plus)<Vstar`.

All trusted scalar checks use only addition, multiplication, squares and order.
No square root, inverse, eigenvalue or tunable Young parameter is required.

This is a mathematics-only child. It does not bind a deployed SCC, evaluator,
Float64/FD/controller implementation, source box, P8/ODE coverage, Lean/kernel,
provenance, admission, registry state, or parent closure.

---

## 1. Exact relative-defect composition

Set

`b := a - h e_rel`.

Weighted Cauchy gives

`|<a,e_rel>_W|^2 <= Q(a) Q(e_rel)`.

Therefore, writing `V=Q(d)`,

`Q(b)`
` = Q(a) - 2h<a,e_rel>_W + h^2 Q(e_rel)`
` <= qV + 2h sqrt(qK) V + h^2 K V`.

The only non-polynomial-looking term is the cross term. Introduce a proposed
factor `kappa` and

`S_kappa = kappa-q-h^2K`.

If `S_kappa>=0` and

`4h^2qK <= S_kappa^2`,

then, because both sides are nonnegative,

`2h sqrt(qK) <= S_kappa`.

Consequently

`Q(b) <= kappa V`.

### Theorem 1.1 — radical-free relative-defect factor gate

Assume

- `q>=0`, `K>=0`, `h>=0`, `kappa>=0`;
- `Q(a)<=qV`, `Q(e_rel)<=KV`, `V>=0`;
- `S_kappa=kappa-q-h^2K>=0`;
- `4h^2qK<=S_kappa^2`.

Then

`Q(a-h e_rel) <= kappa V`.

The strict scalar gate (`S_kappa>0` and strict square inequality) gives a
strict factor whenever `V>0` and the vector envelopes can attain their
boundaries.

### Sharpness / necessity for the uncertainty class

The condition is not merely sufficient. In one dimension choose

`a = sqrt(qV)`,

`e_rel = -sqrt(KV)`.

Then

`Q(a-h e_rel) = (sqrt(q)+h sqrt(K))^2 V`.

Thus no uniformly smaller factor can follow from only the two independent norm
bounds. Equivalently, for nonnegative data,

`(sqrt(q)+h sqrt(K))^2 <= kappa`

is exactly equivalent to the two polynomial gates above.

The same witness shows the strict boundary is real: equality gives no strict
reserve.

---

## 2. Exact strict relative-contraction gate

Set `kappa=1`. Then

`S_rel = 1-q-h^2K`.

Hence the implemented corrector with **only** relative evaluator defect is a
strict robust contraction precisely when

`S_rel>0`,

`4h^2qK<S_rel^2`.

This is the radical-free elimination of

`sqrt(q)+h sqrt(K)<1`.

### Counterexample to the naive energy-addition rule

It is unsafe to check only

`q+h^2K<1`.

Take

`q=9/25`, `h=1`, `K=1/4`.

Then

`q+h^2K = 61/100 < 1`,

but the sharp factor is

`(3/5+1/2)^2 = 121/100 > 1`.

In one dimension take `a=(3/5)d` and `e_rel=-(1/2)d`; then

`d_plus=(11/10)d`,

so energy expands by `121/100`. The missing term is exactly the correlation
cross term between the nominal corrector error and the relative evaluator
error.

At `q=1/4`, `h=1`, `K=1/4`, the naive sum is only `1/2`, yet the sharp factor
is exactly `1`; this is a clean boundary-only regression.

---

## 3. Composition with a persistent additive defect

Now retain `e_abs`. Once Theorem 1.1 gives

`Q(b)<=kappa V`,

where `b=a-h e_rel`, the implemented update is

`d_plus=b-h e_abs`.

This is exactly the geometry of T-P5-075 with `q_h` replaced by the already
spent factor `kappa`. For `V<=Vstar`,

`Q(b)<=kappa Vstar`,

`Q(e_abs)<=E`,

and therefore

`<b,e_abs>_W^2 <= kappa Vstar E`.

Define

`R=(1-kappa)Vstar-h^2E`.

If

`0<=kappa<1`, `Vstar>0`, `E>=0`,

`R>0`,

`4h^2kappa Vstar E<R^2`,

then

`Q(d_plus)<Vstar`.

### Theorem 3.1 — mixed relative/additive defective-corrector barrier

Assume the hypotheses of Theorem 1.1 and choose one common `kappa` satisfying
its factor gate. If the additive barrier gates above hold, then every state
with `Q(d)<=Vstar` and every admissible pair `(e_rel,e_abs)` is mapped strictly
inside the same root-centered sublevel.

The theorem is modular on purpose: a checker may search for a rational/dyadic
`kappa`. There is no need to serialize the irrational exact factor. With strict
slack, any rational `kappa` lying between the exact relative envelope factor
and the additive-barrier ceiling is a valid certificate.

---

## 4. Separate full allowances are unsound

A relative allowance that passes by itself and an additive allowance that
passes against the **old** nominal factor `q` need not pass jointly.

Take one dimension with

`q=1/4`, `h=1`, `K=1/16`, `E=4/25`, `Vstar=1`.

Relative-only worst-case norm factor is

`sqrt(q)+sqrt(K)=1/2+1/4=3/4`,

so its energy factor is `9/16<1`.

Additive-only against the nominal factor also passes strongly:

`sqrt(q)+sqrt(E)=1/2+2/5=9/10<1`.

But jointly the three admissible vectors can align adversarially, giving norm
factor

`1/2+1/4+2/5 = 23/20 > 1`,

hence energy factor

`529/400>1`.

An exact witness is `d=1`, `a=1/2`, `e_rel=-1/4`, `e_abs=-2/5`; then

`d_plus = 23/20`.

Therefore the correct ledger is sequential/shared:

`nominal q -> pay relative K -> obtain kappa -> pay additive E`,

not

`check K against q` AND `check E against q` independently.

A boundary-only version is

`q=1/4`, `h=1`, `K=1/16`, `E=1/16`, `Vstar=1`,

for which the joint norm factor is exactly

`1/2+1/4+1/4=1`.

Every individual component is strictly below its own nominal allowance, but
there is no strict joint inward map.

---

## 5. Asymptotic split: relative error does not create a floor; additive error does

### 5.1 `E=0`

If `E=0` and a factor `kappa<1` is certified, then

`Q(d_{n+1}) <= kappa Q(d_n)`.

Hence repeated certified steps converge geometrically to the true root. A
nonzero relative evaluator error is therefore compatible with zero asymptotic
error, provided it is genuinely root-relative and the shared contraction gate
passes.

### 5.2 `E>0`

A persistent additive defect generally leaves a nonzero floor. This cannot be
removed by making the relative component small.

For example, take `F(x)=x`, `h=1`, `e_rel=0`, and constant `e_abs=b!=0`.
Then the implemented update is

`x_plus = -b`,

and `-b` is a fixed point of the defective iteration. Thus zero convergence to
the original root is impossible in general whenever the additive component is
allowed to persist.

This is why `K` and `E` must remain separately typed in source packets.
Relabeling a constant evaluator bias as a relative error changes the theorem.

---

## 6. Correlation boundary

The gates above are **sharp for the uncertainty class described only by the
three independent weighted-norm envelopes**. If a concrete evaluator supplies
extra signed/correlated identities between `a`, `e_rel`, and `e_abs`, a less
conservative theorem may be possible. Such a theorem must consume those exact
identities.

Conversely, absent a correlation theorem, the one-dimensional aligned witnesses
above prove that no universal improvement is possible. Sampling favorable
angles is not evidence for a larger certified budget.

---

## 7. Lean-friendly theorem decomposition

A small formalization can be split as follows.

1. `two_square_factor_gate`
   - scalar lemma: nonnegative `A,B,S`, `4*A*B<=S^2` imply
     `2*sqrt(A*B)<=S` if a square-root API is desired;
   - preferable vector consumer avoids exposing roots by squaring the Cauchy
     cross term against `S^2` and using sign premises.

2. `relative_defect_effective_factor`
   - consumes `Q(a)<=qV`, `Q(e)<=KV`,
     `S=kappa-q-h^2*K>=0`, `4*h^2*q*K<=S^2`;
   - returns `Q(a-h*e)<=kappa*V`.

3. `relative_defect_strict_contraction_gate`
   - specialization `kappa=1` with strict gates.

4. `mixed_defect_barrier`
   - compose theorem 2 with the already-formalized/additive radical-free
     barrier shape using effective `kappa`.

5. `naive_relative_energy_sum_counterexample`
   - exact rational regression `(q,h,K)=(9/25,1,1/4)`.

6. `separate_allowances_counterexample`
   - exact rational regression
     `(q,h,K,E,V)=(1/4,1,1/16,4/25,1)`.

The key proof implementation should avoid division. Expand `Q(a-h e)` exactly,
use Cauchy in squared form, and compare the cross term with `S` using
nonnegativity plus `nlinarith`. The scalar certificate data are rational.

---

## 8. Recommended downstream routing

The P5 corrector lane can now keep three layers distinct:

1. T-P5-074/076/075 exact source-independent packet gives nominal `q`;
2. a **same-root relative evaluator** budget `K` is charged by T-P5-078 to
   produce an effective rational `kappa<1`;
3. a **persistent additive evaluator** budget `E` is charged against the
   remaining `1-kappa` barrier reserve, then T-P5-077 checks that the selected
   invariant sublevel lies inside the source box.

This ordering prevents double-spending the nominal contraction reserve and
preserves the correct zero-floor versus nonzero-floor semantics.

Still open are the deployed same-key `K,E` source bounds, the actual SCC/chart
binding, source-box/anchor data, Float64/FD/controller semantics, P8/ODE
coverage, Lean/kernel receipt, admission and registry integration.