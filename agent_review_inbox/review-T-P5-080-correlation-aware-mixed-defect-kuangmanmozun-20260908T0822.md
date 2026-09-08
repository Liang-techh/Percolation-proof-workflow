---
kind: review_result
review_id: review-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0822
task_id: T-P5-080-CORRELATION-AWARE-MIXED-DEFECT
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T08:22:00-06:00
claim_commit: a65ba327719751264a0f1fe83b83adce41f28d72
inspected_commits:
  - 038772083818be60fa274d5e9d60162a686d2dde
  - f2769764ff5a9c983114c3de525808be97eb98c7
  - f0d1df5605088ee79b7416d61af04cf78c2d2f65
  - 9c64f802352405144b36baeec96d2b438cd7aa9c
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Use this only when a concrete source packet proves signed inner-product/correlation
  information. It is a strict refinement of T-P5-078's independent norm-envelope
  uncertainty class, not a replacement for it. Preserve signed Gram/cross terms until
  after summation; if the source cannot prove the correlation hypotheses, fall back to
  T-P5-078. Keep T-P5-079 similarity normalization disjoint.
---

# T-P5-080 — correlation-aware mixed evaluator-defect closure

## 0. Result in one line

T-P5-078 is sharp when the nominal corrector error, relative evaluator defect,
and persistent additive defect are known only through **independent norm
envelopes**. Its own Section 6 leaves one mathematical escape hatch: a concrete
source may prove signed/correlated identities, in which case the triangle/Cauchy
worst case is needlessly pessimistic.

That escape hatch has an exact radical-free form.

Let `Q(v)=<v,v>_W` be the same positive weighted quadratic form used by the P5
corrector lane, let `V=Q(d)`, and suppose the nominal corrector vector `a` and
root-relative evaluator defect `e_r` satisfy

`Q(a) <= q V`,

`Q(e_r) <= K V`,

`<a,e_r>_W >= gamma V`,

with `h>=0`. For

`b = a - h e_r`,

the exact expansion gives immediately

**(0.1)** `Q(b) <= kappa_corr V`,

where

**(0.2)** `kappa_corr = q - 2 h gamma + h^2 K`.

Thus a signed correlation theorem replaces T-P5-078's radical-free elimination
of the worst-case term `2 h sqrt(qK)` by the actual certified scalar
`-2 h gamma`. The strict relative-contraction gate is simply

**(0.3)** `0 <= kappa_corr < 1`.

No square root, auxiliary `kappa`, Young parameter, matrix inverse, or spectral
computation is needed.

For the persistent part, let `e_0` be the additive evaluator defect and suppose
one can prove on the relevant sublevel

`Q(e_0) <= E1 V + E0`,

`<b,e_0>_W >= -(J1 V + J0)`.

Then the implemented update

`d_plus = b - h e_0`

obeys the exact affine energy comparison

**(0.4)** `Q(d_plus) <= A V + B`,

with

**(0.5)** `A = kappa_corr + 2 h J1 + h^2 E1`,

**(0.6)** `B = 2 h J0 + h^2 E0`.

Hence a candidate invariant level `Vstar>0` is strictly inward whenever

**(0.7)** `0 <= A < 1`,

**(0.8)** `B < (1-A) Vstar`.

This gives a fully rational correlation-aware alternative to the square-root
cross barrier of T-P5-075/T-P5-078. It is valid only when the signed cross
packet is itself source-certified.

This is mathematics only. It does not bind a deployed SCC/evaluator, source
Jacobian, Float64/FD/controller implementation, source-domain coverage,
P8/ODE semantics, Lean/kernel evidence, provenance, admission, or registry
state.

---

## 1. Relative defect: signed correlation factor

Expand the same weighted quadratic form:

`Q(a-h e_r)`

`= Q(a) - 2h<a,e_r>_W + h^2 Q(e_r)`.

Because `h>=0`, the three certified inequalities give

`Q(a-h e_r)`

`<= qV - 2h gamma V + h^2 K V`

`= (q - 2h gamma + h^2 K)V`.

Therefore:

### Theorem 1.1 — correlation-aware relative-defect factor

Assume

- `V>=0`, `h>=0`;
- `Q(a)<=qV`;
- `Q(e_r)<=KV`;
- `<a,e_r>_W>=gamma V`.

Define

`kappa_corr=q-2h gamma+h^2K`.

Then

`Q(a-h e_r)<=kappa_corr V`.

If additionally `0<=kappa_corr<1`, the relative-defective corrector is a strict
energy contraction for every `V>0`.

The nonnegativity guard on `kappa_corr` is a convenient non-vacuity/interface
guard. If a nonzero realization exists while the hypotheses imply a negative
upper bound for `Q(a-he_r)`, the scalar packet is inconsistent.

### Exact relation to the T-P5-078 independent-envelope factor

Without a signed lower bound, weighted Cauchy permits

`<a,e_r>_W = -sqrt(qK) V`,

and the worst robust factor is

`q + 2h sqrt(qK) + h^2K`.

A genuine source theorem with

`gamma > -sqrt(qK)`

strictly improves that factor. No such improvement is valid from norm data
alone.

For a checker-friendly nonvacuous sharpness packet, one may additionally verify

`gamma^2 <= qK`.

Then in dimension at least two the saturated Gram matrix

`[[q, gamma],[gamma,K]]`

is positive semidefinite, so vectors with

`Q(a)=qV`, `Q(e_r)=KV`, `<a,e_r>=gamma V`

exist. For that uncertainty class, `kappa_corr` is attained exactly and cannot
be lowered.

---

## 2. A rational regression where correlation recovers a factor of two

Take ordinary Euclidean `Q`, `V=1`,

`q=K=1/4`, `h=1`, `gamma=0`.

The independent-envelope T-P5-078 factor is

`(1/2+1/2)^2 = 1`,

so no strict contraction follows.

But if source analysis proves the signed fact

`<a,e_r> >= 0`,

then

`kappa_corr = 1/4 + 1/4 = 1/2`.

This is sharp. Choose

`a=(1/2,0)`, `e_r=(0,1/2)`.

Then all three scalar bounds are saturated and

`Q(a-e_r)=1/2`.

The benefit can be even larger for favorable positive correlation. With

`a=e_r=(1/2,0)`,

one has `gamma=1/4` and

`kappa_corr=1/4-1/2+1/4=0`:

the evaluator term cancels the nominal corrector error exactly.

---

## 3. Why sampled/favorable angles are not a certificate

The same norm envelopes from Section 2 also admit

`a=(1/2,0)`, `e_r=(-1/2,0)`.

Then

`<a,e_r>=-1/4`

and

`Q(a-e_r)=1`.

So observing orthogonality, positive correlation, or cancellation at sampled
states cannot justify `gamma=0` or `gamma>0` on the source cell. A signed lower
bound must be proved on the same domain and with the same weighted inner
product.

This is a strict fail-closed rule:

- signed source theorem available -> T-P5-080 may improve the factor;
- only separate norm envelopes available -> use T-P5-078;
- sampled angle/correlation only -> no certification upgrade.

---

## 4. Persistent defect: signed post-relative cross budget

Let

`b=a-h e_r`

and suppose Theorem 1.1 has supplied

`Q(b)<=kappa_corr V`.

Now retain a persistent defect `e_0` and assume source analysis proves

**(4.1)** `Q(e_0)<=E1 V+E0`,

**(4.2)** `<b,e_0>_W >= -(J1 V+J0)`.

Here `E0,E1,J0,J1>=0` are rational source envelopes. Expanding once more,

`Q(b-h e_0)`

`=Q(b)-2h<b,e_0>+h^2Q(e_0)`

`<=kappa_corr V + 2h(J1V+J0) + h^2(E1V+E0)`

`= A V+B`,

where

`A=kappa_corr+2hJ1+h^2E1`,

`B=2hJ0+h^2E0`.

### Theorem 4.1 — signed mixed-defect affine energy recurrence

Under the hypotheses above,

`Q(d_plus)<=A Q(d)+B`.

If `0<=A<1` and `B<(1-A)Vstar`, then every state with

`Q(d)<=Vstar`

is mapped strictly into

`Q(d_plus)<Vstar`.

The proof is just

`Q(d_plus)<=A V+B<=A Vstar+B<Vstar`.

There are no radicals in either the theorem statement or trusted scalar gate.

---

## 5. Orthogonal additive errors can pass when the independent gate is boundary-only

Take `kappa_corr=1/4`, `h=1`, `E0=1/4`, `E1=0`, `Vstar=1`.

If only `Q(e_0)<=1/4` is known, the independent norm envelope allows

`sqrt(kappa_corr Vstar)+sqrt(E0)=1/2+1/2=1`,

which is only boundary and cannot certify strict inwardness.

If source instead proves

`<b,e_0> >= 0`,

then `J0=J1=0` and

`A=1/4`, `B=1/4`.

Hence

`A Vstar+B=1/2<1`.

The bound is attained by the rational orthogonal witness

`b=(1/2,0)`, `e_0=(0,1/2)`,

for which

`Q(b-e_0)=1/2`.

Again, without the signed source theorem the antiparallel witness

`e_0=(-1/2,0)` reaches energy `1` and destroys strictness. Thus the improvement
comes entirely from certified correlation, not from a looser reinterpretation
of the old norm packet.

---

## 6. Source-friendly signed-Gram handoff

A source implementation does not have to form `b` first. Since

`b=a-h e_r`,

`<b,e_0> = <a,e_0> - h<e_r,e_0>`.

Therefore if source proves

`<a,e_0> >= -(A1 V+A0)`

and

`<e_r,e_0> <= C1 V+C0`,

then automatically

`<b,e_0> >= -[(A1+hC1)V+(A0+hC0)]`.

So one may set

`J1=A1+hC1`,

`J0=A0+hC0`.

This is the same structural lesson as T-P5-076: **form the signed weighted Gram
cross terms before taking absolute values**. Entrywise absolute-value bounds are
a safe fallback, but they erase exactly the cancellation T-P5-080 is designed
to certify.

No sampled sign may substitute for these cell-uniform inequalities.

---

## 7. Division-free asymptotic floor certificate

The affine recurrence also quantifies the persistent floor without division.
Suppose

`0<=A<1`

and choose any rational candidate `Vfloor>=0` satisfying

**(7.1)** `B <= (1-A)Vfloor`.

Then

`Q(d_plus) <= A Q(d)+(1-A)Vfloor`.

Consequently:

1. `Q(d)<=Vfloor` implies `Q(d_plus)<=Vfloor`;
2. for `Q(d)>=Vfloor`, the excess obeys the one-sided comparison
   `Q(d_plus)-Vfloor <= A[Q(d)-Vfloor]`;
3. strict `<` in (7.1) gives a strict inward reserve at the floor boundary.

The analytic optimal floor is `B/(1-A)`, but the trusted checker never needs to
divide: it verifies the product inequality (7.1) for a rational/dyadic proposed
floor.

This refines T-P5-078's qualitative statement that persistent additive error
creates a nonzero floor.

---

## 8. Counterexample boundary and assumptions that must not be dropped

### 8.1 Wrong sign on the correlation inequality

Because the update is `a-h e_r`, the dangerous configuration is a **negative**
inner product. An upper bound `<a,e_r><=gamma V` does not control the dangerous
cross term. The theorem needs a lower bound.

### 8.2 Different weights are not interchangeable

All `Q` and inner products must use the same `W`. A Euclidean correlation sign
need not be preserved by an unrelated weighted metric if different coordinate
components carry opposite products.

### 8.3 Cross information must share the source cell

A lower bound on `<a,e_r>` from one cell and norm envelopes from another cannot
be combined unless a coverage theorem proves the common domain.

### 8.4 No improvement without correlation evidence

The antiparallel rational witnesses in Sections 3 and 5 show that T-P5-078 is
already optimal for independent envelopes. T-P5-080 is a conditional
refinement, not evidence that the old bound was loose in the absence of new
source information.

---

## 9. Lean-friendly theorem leaves

A minimal formalization can be split into:

1. `correlated_relative_defect_factor`
   - expand `Q(a-h*e)`;
   - consume `Q(a)<=qV`, `Q(e)<=KV`, `<a,e>>=gamma*V`;
   - conclude `Q(a-h*e)<=(q-2*h*gamma+h^2*K)*V`.

2. `correlated_relative_strict_contraction`
   - add `0<=kappa_corr`, `kappa_corr<1`, `V>0`.

3. `signed_postrelative_cross_from_gram`
   - derive the `J1,J0` packet from bounds on `<a,e0>` and `<er,e0>`.

4. `signed_mixed_defect_affine_recurrence`
   - return `Q(d_plus)<=A*V+B`.

5. `affine_energy_floor_certificate`
   - consume `0<=A<1`, `B<=(1-A)*Vfloor`.

6. exact rational regressions:
   - orthogonal relative packet `(q,K,h,gamma)=(1/4,1/4,1,0)`;
   - antiparallel no-correlation obstruction;
   - orthogonal additive packet `(kappa,E,Vstar)=(1/4,1/4,1)`.

The proofs need only bilinearity, positivity, multiplication and linear/nonlinear
arithmetic. No square-root API is required.

---

## 10. Recommended routing

The source-side decision order should be:

1. if a same-domain signed Gram/correlation packet is available, use T-P5-080;
2. otherwise use the independent-envelope sharp gates of T-P5-078/T-P5-075;
3. never infer a favorable correlation from sampling;
4. keep source binding, coordinate normalization (T-P5-079), evaluator
   implementation semantics, coverage, Lean/kernel verification and admission
   as separate obligations.

Current status: **pending mathematical child**. No concrete deployed source
correlation packet has been shown here.