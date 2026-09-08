---
kind: review_result
review_id: review-T-P5-044-honglianmozun-20260907T2050
task_id: T-P5-044
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T20:48:00-06:00
created_at: 2026-09-07T20:50:00-06:00
claim_commit: b5fecc271bc264dd199c73ecb43a4a8d775d2813
inspected_commit: ad5849b8c19b37a56cc546c3d99a76009d10f36a
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-040-honglianmozun-20260907T1950.md
  - agent_review_inbox/review-T-P5-041-liuguanyi-20260907T2020.md
  - agent_review_inbox/review-T-P5-043-kuangmanmozun-20260907T2050.md
source_hashes:
  review-T-P5-040: 80f950d571eb6124e6fb7df819f50d2eab67f1ea
  review-T-P5-041: a85bd01d469fe8d925db9d1331d861cfd6a854ab
  review-T-P5-043: 264ed36e39ba0a5d5de7f3dba6cb6d50b221dbd6
continuation_of:
  - review-T-P5-040-honglianmozun-20260907T1950
  - review-T-P5-041-liuguanyi-20260907T2020
related_tasks:
  - T-P5-037
  - T-P5-039
  - T-P5-040
  - T-P5-041
  - T-P5-042
  - T-P5-043
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: preserve_the_signed_2x2_u_to_l_block_before_entrywise_absolute_scalarization; formalize_the_adjugate_SOS_completion_and_use_the_correlated_gate_as_the_next_route_when_T-P5-043_independent_scalar_feasibility_fails
---

# T-P5-044 — correlated two-channel signed-residual Lyapunov completion

## 0. Result

`T-P5-043` gives an exact feasibility/obstruction test for the **independent scalar-channel** mixed residual model and explicitly identifies signed/correlated structure as the next route after a genuine scalar FAIL.  The missing energy theorem is therefore not another `rho` optimizer.  It is the two-channel completion obtained by keeping the signed residual block inside the power pairing.

Start from the frozen P5 Pareto energy inequality

```text
V' <= -c V - u^T A u - u^T l,                          (0.1)

u = (u4,u5),
A = diag(a4,a5),

c  = (109-r)/200,
a4 = (250+53r)/1500,
a5 = 1/6,
0 <= r <= 1.                                            (0.2)
```

Suppose a source-side decomposition is preserved in signed form

```text
l = K u + b,                                             (0.3)
```

where `K` is a real `2x2` block and `b` is the remaining additive/transverse residual.  `K` and `b` may be pointwise state-dependent; the theorem below is pointwise.  Define

```text
H := A + Sym(K)
   = [[p,q],[q,s]],

p := a4 + k44,
q := (k45+k54)/2,
s := a5 + k55,
Delta := p*s-q^2.                                       (0.4)
```

Then the whole residual-power term closes through `H`, not through the entrywise absolute size of `K`:

```text
V' <= -c V - u^T H u - u^T b.                          (0.5)
```

If

```text
p > 0,
Delta > 0,                                               (0.6)
```

set

```text
B_H(b) := s*b4^2 - 2*q*b4*b5 + p*b5^2.                 (0.7)
```

The exact completion is

```text
-u^T H u - u^T b <= B_H(b)/(4*Delta).                   (0.8)
```

More importantly for Lean/checkers, (0.8) has a completely division-free exact SOS certificate.  Therefore at the current barrier `Vstar=1/4`, the strict first-exit gate is simply

```text
200*B_H(b) < (109-r)*Delta.                             (0.9)
```

No square root, eigenvalue, matrix inverse, `rho`, or auxiliary channel budget is required.

This correlated theorem strictly contains the diagonal adverse completion of `T-P5-040`, while preserving a structural cancellation that every entrywise-absolute scalarization destroys: an arbitrarily large skew-symmetric residual block costs **exactly zero** energy.

---

## 1. Only the symmetric part of the signed residual gain enters energy

Write

```text
K = Sym(K) + Skew(K),
Sym(K)  = (K+K^T)/2,
Skew(K) = (K-K^T)/2.                                    (1.1)
```

For every real `u`,

```text
u^T Skew(K) u = 0.                                      (1.2)
```

Indeed the scalar on the left equals its own transpose,

```text
u^T Skew(K) u
 = u^T Skew(K)^T u
 = -u^T Skew(K) u,                                      (1.3)
```

hence it vanishes.  In coordinates this is even more explicit:

```text
u^T K u
 = k44*u4^2 + (k45+k54)*u4*u5 + k55*u5^2.              (1.4)
```

Thus the antisymmetric combination `k45-k54` cannot appear in the Lyapunov charge.  Combining (0.1) and (0.3),

```text
-u^T A u-u^T l
 = -u^T(A+Sym(K))u-u^T b,
```

which is (0.5).

This is the structural fingerprint missed by an absolute row bound: the energy consumer needs a lower bound on the **symmetric part** of the signed `u -> l` map, not an upper bound on every individual entry.

---

## 2. Exact 2x2 adjugate completion without inverses

Let

```text
H = [[p,q],[q,s]],
Delta = p*s-q^2,
adj(H) = [[s,-q],[-q,p]].                                (2.1)
```

For `b=(b4,b5)`, define `B_H(b)=b^T adj(H)b`, exactly (0.7), and set

```text
z := 2 H u + b,

z4 = 2*p*u4 + 2*q*u5 + b4,
z5 = 2*q*u4 + 2*s*u5 + b5.                              (2.2)
```

Two polynomial identities give the whole theorem:

```text
z^T adj(H) z
 = 4*Delta*(u^T H u + u^T b) + B_H(b),                  (2.3)
```

and

```text
p * (z^T adj(H) z)
 = (p*z5-q*z4)^2 + Delta*z4^2.                          (2.4)
```

Both are exact ring identities.  Under `p>0` and `Delta>0`, the right side of (2.4) is nonnegative, hence (2.3) gives (0.8).

A still cleaner theorem statement avoids division altogether.  For any `gamma`,

```text
4*p*Delta*(u^T H u + u^T b + gamma)
 = (p*z5-q*z4)^2
   + Delta*z4^2
   + p*(4*gamma*Delta-B_H(b)).                           (2.5)
```

Therefore

```text
p>0,
Delta>0,
B_H(b) <= 4*gamma*Delta

==>

-u^T H u-u^T b <= gamma.                                (2.6)
```

This is a direct `ring + sq_nonneg + nlinarith` target.  No matrix API is necessary.

---

## 3. Exact current first-exit gate

At a first exit through `V=Vstar`, (0.5) gives

```text
V' <= -(c*Vstar + u^T H u + u^T b).                    (3.1)
```

Apply (2.5) with `gamma=c*Vstar`.  If

```text
B_H(b) < 4*c*Vstar*Delta,                               (3.2)
```

then the final term on the right of (2.5) is strictly positive, so

```text
c*Vstar + u^T H u + u^T b > 0,
V' < 0.                                                  (3.3)
```

For the current `Vstar=1/4` and (0.2), (3.2) becomes exactly

```text
B_H(b) < c*Delta,
```

or, after clearing only the fixed positive denominator `200`,

```text
200*(s*b4^2 - 2*q*b4*b5 + p*b5^2)
  < (109-r)*(p*s-q^2).                                  (3.4)
```

Together with

```text
0 <= r <= 1,
p > 0,
p*s-q^2 > 0,                                           (3.5)
```

this is a fully polynomial correlated first-exit consumer.

If the source does not expose exact `b` but can prove a uniform correlated budget

```text
B_H(b(z)) <= E                                           (3.6)
```

on the candidate boundary/domain, then it is enough to check

```text
200*E < (109-r)*Delta                                   (3.7)
```

when `H` is fixed.  For state-dependent `H`, the pointwise form (3.4), or a separately certified uniform lower determinant / upper adjugate budget, is the correct interface.

---

## 4. `T-P5-040` is the diagonal adverse special case

The mixed absolute model of `T-P5-040` treats a relative coefficient in the worst possible sign.  Embed that model as the signed diagonal block

```text
K = -diag(rho4,rho5).                                   (4.1)
```

Then

```text
p = a4-rho4 =: t4,
s = a5-rho5 =: t5,
q = 0,
Delta = t4*t5,                                          (4.2)
```

and

```text
B_H(b) = t5*b4^2 + t4*b5^2.                             (4.3)
```

Hence (0.8) reduces identically to

```text
B_H(b)/(4*Delta)
 = b4^2/(4*t4) + b5^2/(4*t5),                           (4.4)
```

which is exactly the sharp channelwise square completion in `T-P5-040`.

So the correlated theorem is not a competing ledger.  It is a strict matrix extension of the already derived scalar consumer.  The old route is recovered by setting the off-diagonal signed structure to zero and taking both diagonal gains in the maximally adverse sign.

---

## 5. Exact witness: arbitrarily large skew gain costs zero energy

Take, for any nonzero real `M`,

```text
K_M = [[0, M],
       [-M,0]],
b = 0.                                                   (5.1)
```

Then

```text
Sym(K_M)=0,
H=A,
Delta=a4*a5>0,                                          (5.2)
```

and pointwise

```text
u^T K_M u
 = M*u4*u5-M*u5*u4
 = 0.                                                    (5.3)
```

Thus **the exact Lyapunov dissipation is independent of `M`**, even as `|M| -> infinity`.

By contrast, a centered own-channel relative representation cannot encode this block at all.  The first row is

```text
l4 = M*u5.                                               (5.4)
```

A bound `|l4| <= rho4*|u4|` fails for every finite `rho4` by taking `u4=0,u5=1`; the second row fails symmetrically.

The additive fallback of `T-P5-041` is safe but necessarily pays for the lost cancellation.  On `V<=1/4`, its exact energy-dual formula assigns, when each row targets its own channel,

```text
B4 = M^2/(2*m5),
B5 = M^2/(2*m4),                                        (5.5)
```

with the frozen positive masses

```text
m4 = 350003/3000000,
m5 = 200739/4000000.                                    (5.6)
```

Hence every independent scalar additive charge grows like `M^2`, while the correlated signed energy charge remains identically zero.  `T-P5-043` cannot repair this by tuning `rho_i` in this witness because the own-channel coefficients are zero; the information was already destroyed when the off-diagonal signed pair was scalarized.

This is an exact strict-separation witness for the two proof interfaces.  It also explains the correct source-side priority after a genuine `T-P5-043` FAIL: preserve the signed `2x2` `J_u` block, especially its skew/cross cancellation, before taking entrywise absolute values.

---

## 6. Correlated parameter-cell / incremental tube gate

The same identity gives a sharper incremental consumer for `T-P5-030`.  Suppose a true incremental residual decomposition has the signed homogeneous form

```text
Delta l = K*(Delta u) + g*(Delta c),                    (6.1)
```

where `g=(g4,g5)`.  Let the incremental energy use the same Pareto reserve and define `H,Delta` as above.  Then

```text
Vd'
 <= -c*Vd
    -(Delta u)^T H (Delta u)
    -(Delta c)*(Delta u)^T g.                           (6.2)
```

This is (0.5) with

```text
b = g*(Delta c).                                        (6.3)
```

Define

```text
G_H(g) := s*g4^2 - 2*q*g4*g5 + p*g5^2.                 (6.4)
```

For a candidate homogeneous tube

```text
Vd = Kc*(Delta c)^2,                                    (6.5)
```

the strict inward condition for `Delta c != 0` is exactly

```text
G_H(g) < 4*c*Kc*Delta.                                  (6.6)
```

For the already used `Kc=1/12`, this becomes

```text
600*G_H(g) < (109-r)*Delta.                             (6.7)
```

Again there are no square roots or separate channel slacks.  If `Delta c=0`, the additive term vanishes and positive-definite `H` gives the centered decay branch directly.

This is the correlated analogue of the earlier scalar incremental gates: source-side signed parameter sensitivities may be kept as one vector `g` instead of being charged independently.

---

## 7. Precise failure boundary of this completion

The positive-definite hypothesis in (0.6) is not cosmetic.

Assume first `p>0`.  Complete the quadratic form in the first coordinate:

```text
u^T H u
 = p*(u4+(q/p)u5)^2 + (Delta/p)*u5^2.                  (7.1)
```

If

```text
Delta < 0,                                              (7.2)
```

choose `u4=-(q/p)u5` and scale `|u5| -> infinity`.  Then `u^T H u -> -infinity`, so even with `b=0`

```text
-u^T H u-u^T b
```

has no finite global additive upper charge.  No completion of the form (2.6) can exist.

At the singular boundary

```text
Delta = 0,                                              (7.3)
```

the direction

```text
n = (-q/p,1)                                            (7.4)
```

lies in `ker(H)`.  If

```text
n^T b != 0,                                             (7.5)
```

then along `u=t*n` the quadratic term vanishes and the linear term is unbounded in one sign.  Thus there is again no finite global additive charge.  If `n^T b=0`, a degenerate pseudoinverse completion may exist, but there is no strict quadratic reserve in the null direction; that special branch is intentionally outside this child.

If `p<0`, the simpler direction `u=(t,0)` already makes `u^T H u -> -infinity`.  Cases with `p=0` reduce either to an indefinite cross term (`q!=0`) or a singular reserve and require the same nullspace check.

These are obstructions only to the **separated global quadratic completion** developed here.  They are not a claim that the full constrained `V<=Vstar` P5 problem is impossible; a later proof could still exploit the energy sublevel geometry jointly with an indefinite residual block.

---

## 8. Candidate theorem split for Lean

A minimal formalization can stay purely over `Real` and avoid matrix libraries:

```text
skew_two_channel_power_cancel
```

Prove directly that

```text
u4*(m*u5) + u5*(-m*u4) = 0.
```

Then

```text
two_by_two_adjugate_completion_identity
```

for (2.3), and

```text
two_by_two_adjugate_sos_identity
```

for (2.4).  Both are `ring` identities.

Use them in

```text
correlated_residual_completion
```

with hypotheses `0<p`, `0<Delta`, `B_H(b)<=4*gamma*Delta`, proving (2.6) by square nonnegativity and `nlinarith`.

Finally expose

```text
correlated_residual_quarter_barrier_gate
```

with the current rational `c(r)` and the polynomial gate (3.4), plus

```text
correlated_incremental_one_twelfth_gate
```

for (6.7).

No theorem in this child requires `sqrt`, eigenvalues, inverse matrices, ODE libraries, or source semantics.

---

## 9. Assumptions, dependencies, and unresolved obligations

This child depends only on the frozen P5 Pareto reserve/energy identity from `T-P5-037/039/040` and on the `u=x+y` signed-Jacobian coordinate viewpoint of `T-P5-041`.  It deliberately does **not** alter or re-audit `T-P5-042/043`; those remain the exact consumers for the independent scalar model.

The new source obligation is precise: after transforming the signed Jacobian into `(u,x)` coordinates as in `T-P5-041`, do **not** immediately take entrywise absolute values of the `u -> l` `2x2` block.  Preserve a signed block `K` (or a certified lower envelope for `A+Sym(K)`) and place only the transverse/inhomogeneous remainder into `b`.  Then certify (3.5) and the correlated bias gate uniformly on the same candidate domain.

Still open and explicitly out of scope here:

- binding `K,b` to the deployed `forceError` / FD / controller source;
- robust interval treatment when `K(z)` varies and only interval entries are exposed;
- domain/flowpipe/ODE continuation;
- Float64 semantics;
- Lean compilation and axiom receipt;
- provenance, registry admission, or any claim that P5/P8/M4 is closed.

Status: **pending mathematical child**.  The main new conclusion is structural: after the independent scalar obstruction gate is exhausted, the next mathematically meaningful move is a signed symmetric-part energy contract, because skew and correlated residual gains can be arbitrarily large entrywise while costing little or exactly zero Lyapunov power.