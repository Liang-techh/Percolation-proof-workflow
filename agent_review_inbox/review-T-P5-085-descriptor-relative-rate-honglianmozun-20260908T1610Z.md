---
kind: review_result
review_id: review-T-P5-085-descriptor-relative-rate-honglianmozun-20260908T1610Z
task_id: T-P5-085-DESCRIPTOR-RELATIVE-RATE
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-08T16:10:00Z
claim_commit: 0d2211e574a1499755ccc26839f1efa79113e01c
inspected_commits:
  - 91f03a726d8135b787b52ef5846e2cfdafc9de85
  - a88e9abb1e3a5caca3b37e32d1401c3c87695c3d
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-GH-MATH-P4-DESCRIPTOR-PUPPER-guyuefangyuan-20260908T1552Z.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DescriptorPUpper.lean
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Add this as a P5 energy-side alternative/companion to the absolute P4
  DescriptorPUpper route. If a same-source descriptor RHS admits a Lyapunov-
  relative (or relative-plus-additive) squared bound, consume it as loss of
  decay rate plus explicit bias rather than first constructing an absolute
  acceleration/port cap. Keep source binding, Lean compilation, coverage and
  admission separate.
---

# T-P5-085 — descriptor-relative Lyapunov rate absorption

## 0. Result in one line

The fresh `GH-MATH-P4-DESCRIPTOR-PUPPER` review correctly identifies that full-mass
coercivity alone cannot give an **absolute** acceleration/port cap: a same-cell
absolute RHS bound `||rhs||^2 <= H_i` is irreducible for that route.

For a Lyapunov proof, however, an absolute `P_upper` is not the only mathematically
valid consumer. If the *same descriptor RHS* instead satisfies a state-relative or
relative-plus-additive bound

`||rhs||^2 <= H_rel V + H_abs`,

then the existing descriptor coercivity and producer-metric inequality propagate
this directly to a **rate charge + bias charge**. The resulting trusted gate can be
written entirely with products, squares and rational inequalities; no inverse,
square root, eigenvalue or absolute acceleration cap is needed.

The pure relative branch `H_abs=0` preserves the zero slice and converts the port
term into a loss of exponential decay rate rather than an additive ultimate-ball
constant.

This is mathematics/interface only. No claim is made that the deployed DH RHS
currently has such a relative packet.

---

## 1. Upstream descriptor packet already available abstractly

Use the notation of `NEW_P4_032_DescriptorPUpper.lean`.

Let

`M a = rhs`

and suppose full-mass coercivity holds with `mu>0`:

`mu * fullSq(a) <= <a, M a>`.

The existing square-difference argument gives

**(1.1)** `mu^2 * fullSq(a) <= fullSq(rhs)`.

The current producer metric obeys

**(1.2)** `A_up <= Bmax * fullSq(a)`,

with the exact rational

`Bmax = 1402217/12000000`.

If the port packet on the same cell is

**(1.3)** `R := ||r_port||^2 <= rhoSq * A_up`, `rhoSq>=0`,

then multiplying through by `mu^2` yields the division-free descriptor estimate

**(1.4)**

`mu^2 R <= rhoSq * Bmax * fullSq(rhs)`.

This is the only descriptor fact needed below.

---

## 2. New relative-plus-additive descriptor theorem

Assume a nonnegative Lyapunov storage `V` and a same-source RHS packet

**(2.1)** `fullSq(rhs) <= H_rel V + H_abs`,

with `H_rel,H_abs>=0`.

Then (1.4) gives

**(2.2)**

`mu^2 R <= K_rel V + K_abs`,

where it is enough to use the exact products

`K_rel = rhoSq * Bmax * H_rel`,

`K_abs = rhoSq * Bmax * H_abs`.

No intermediate `K_i` or absolute `P_i` witness is required.

### Candidate theorem 2.1 — descriptor port relative/additive propagation

A Lean-friendly statement can avoid defining `K_rel,K_abs` as separate data:

```lean
theorem descriptor_port_relative_additive
    ...
    (hmu : 0 < mu)
    (hdescriptor : M *ᵥ a = rhs)
    (hcoercive : mu * fullSq a <= dot6 a (M *ᵥ a))
    (hmetric : metric <= metricMax * fullSq a)
    (hport : portSq <= rhoSq * metric)
    (hrho : 0 <= rhoSq)
    (hV : 0 <= V)
    (hHrel : 0 <= Hrel)
    (hHabs : 0 <= Habs)
    (hrhs : fullSq rhs <= Hrel * V + Habs) :
    mu^2 * portSq <=
      rhoSq * metricMax * Hrel * V + rhoSq * metricMax * Habs
```

The proof is only the existing `full_descriptor_energy_bound`, `metric_le_full`,
nonnegative multiplication and reassociation.

---

## 3. Division-free power absorption lemma

The useful Lyapunov consumer should not first divide (2.2) by `mu^2` and should not
introduce square roots.

Let `u` be the velocity/multiplier channel paired with `r_port`, and write

`P = <u,r_port>`.

Assume a Cauchy packet and a block dissipation lower bound

**(3.1)** `P^2 <= U R`,

**(3.2)** `d U <= D`,

with `d>0`, `U,R,D>=0`.

Suppose (2.2) holds and choose nonnegative bookkeeping charges

`lambda >= 0`, `alpha >= 0`, `beta >= 0`

such that

**(3.3)** `K_rel <= 4 lambda d mu^2 alpha`,

**(3.4)** `K_abs <= 4 lambda d mu^2 beta`.

Then

**(3.5)** `P <= lambda D + alpha V + beta`.

### Proof without division or square roots

From (3.1), (3.2), and (2.2), using nonnegative multiplication,

`d mu^2 P^2`

`<= d mu^2 U R`

`<= D (K_rel V + K_abs)`.

By (3.3)-(3.4),

`D (K_rel V + K_abs)`

`<= 4 lambda d mu^2 D (alpha V + beta)`.

Since `d mu^2>0`, cancellation gives

**(3.6)** `P^2 <= 4 lambda D (alpha V + beta)`.

Now use the exact square identity

**(3.7)**

`(lambda D + alpha V + beta)^2`

`- 4 lambda D (alpha V + beta)`

`= (lambda D - alpha V - beta)^2 >= 0`.

The right side `lambda D+alpha V+beta` is nonnegative, so (3.6)-(3.7) imply
`P <= lambda D+alpha V+beta`.

This is a pure ordered-ring argument once the Cauchy packet has been supplied.

### Candidate theorem 3.1 — generic squared-packet absorption

```lean
theorem relative_additive_power_absorption
    (mu d U R D V P Krel Kabs lambda alpha beta : ℝ)
    (hmu : 0 < mu) (hd : 0 < d)
    (hU : 0 <= U) (hR : 0 <= R) (hD : 0 <= D) (hV : 0 <= V)
    (hlambda : 0 <= lambda) (halpha : 0 <= alpha) (hbeta : 0 <= beta)
    (hcauchy : P^2 <= U*R)
    (hdiss : d*U <= D)
    (hres : mu^2*R <= Krel*V + Kabs)
    (hrel : Krel <= 4*lambda*d*mu^2*alpha)
    (habs : Kabs <= 4*lambda*d*mu^2*beta) :
    P <= lambda*D + alpha*V + beta
```

No `sqrt`, `/`, matrix inverse, or eigenvalue appears in the statement.

---

## 4. Direct descriptor-to-Lyapunov gate

Substituting the descriptor constants means the source/checker never needs to
materialize either absolute `K_i` or absolute `P_i`.

It is sufficient to check

**(4.1)**

`rhoSq * Bmax * H_rel <= 4 lambda d mu^2 alpha`,

and

**(4.2)**

`rhoSq * Bmax * H_abs <= 4 lambda d mu^2 beta`.

Then the harmful port power satisfies

**(4.3)** `P <= lambda D + alpha V + beta`.

If the pre-port energy ledger is

**(4.4)** `Vdot <= -c V - D + P`,

we obtain

**(4.5)**

`Vdot <= -(c-alpha)V - (1-lambda)D + beta`.

Hence a homogeneous decay theorem follows whenever

`0 <= lambda <= 1`,

`0 <= alpha < c`,

and `beta=0`.

For a first-exit barrier `V=Vstar`, the mixed branch needs only

**(4.6)** `(c-alpha) Vstar > beta`

(with `lambda<=1`) to make the boundary derivative strictly negative.

This is the natural interface when other evaluator/controller terms already force
an additive-bias lane: descriptor-relative forcing reduces the decay rate, while
only the truly additive descriptor part is charged to the ultimate-ball/first-exit
reserve.

---

## 5. Pure relative corollary: no absolute `P_upper`

If

`fullSq(rhs) <= H_rel V`

with no additive term, then `H_abs=beta=0` and the entire descriptor/port chain is
homogeneous.

The single division-free gate becomes

**(5.1)**

`rhoSq * (1402217/12000000) * H_rel`

`<= 4 lambda d mu^2 alpha`.

Under (4.4), this gives

**(5.2)**

`Vdot <= -(c-alpha)V - (1-lambda)D`.

Thus the absolute-RHS obstruction from `GH-MATH-P4-DESCRIPTOR-PUPPER` does not imply
that a Lyapunov consumer must pay an additive constant. It implies only that an
absolute cap cannot be obtained from coercivity alone. A same-source **relative
RHS theorem** is a different, strictly homogeneous route.

The tradeoff has an explicit Pareto form: keeping a larger fraction of `D` means
smaller admissible `lambda`, which in turn forces a larger rate charge `alpha` for
the same descriptor packet.

---

## 6. Sharpness of the factor 4 at the generic information level

The scalar Young factor in (3.3) is sharp.

Take

`d=mu=lambda=alpha=V=D=U=1`,

`R=K_rel=4`, `K_abs=beta=0`, and `P=2`.

Then

`P^2 = U R = 4`,

`d U = D`,

`mu^2 R = K_rel V`,

`K_rel = 4 lambda d mu^2 alpha`,

and the conclusion is equality:

`P = lambda D + alpha V = 2`.

Therefore the coefficient `4` cannot be improved if the checker knows only the
squared Cauchy packet, dissipation coercivity, and the relative residual square.
A better constant would require additional signed/correlated geometry.

---

## 7. Exact zero-slice obstruction

The pure relative source premise

`fullSq(rhs(x)) <= H_rel V(x)`

with finite `H_rel` forces

**(7.1)** `V(x)=0 -> rhs(x)=0`.

Indeed `fullSq(rhs)>=0`, so at a zero-storage state the right side is zero and every
RHS component must vanish.

Therefore a deployed equilibrium/reference for which `V=0` but the descriptor RHS
contains a nonzero regularization/controller/reference/rounding bias cannot enter
the pure relative branch. That term must go into `H_abs` (or a stronger
correlation-aware packet).

This is especially important for shifted storages whose zero set is not obviously
the physical equilibrium: the source owner must prove vanishing on the actual
zero-storage set, not merely at one nominal coordinate point.

This is a mathematical obstruction, not a weakness of the Young estimate.

---

## 8. Why positive pairing dissipation is also irreducible for this generic route

A port **norm** bound alone does not control its power if the paired multiplier can
be arbitrarily large and no dissipation/state bound controls that multiplier.

Exact scalar counterexample: let `V=1`, `R=1`, `r_port=1`, `D=0`, and `u=t`. Then
`P=t` is unbounded as `t->infinity` although the port norm is fixed.

Hence the generic rate route needs either

- a positive `d` with `d||u||^2<=D`, as above;
- a direct Lyapunov/state bound on `u`; or
- stronger signed correlation between `u` and the port.

One cannot silently set `d=0` and retain a finite universal rate charge.

---

## 9. Recommended source handoff

For each actual descriptor cell, do **not** search only for an absolute `H_i` if the
end goal is Lyapunov decay. The source lane can try to prove the more informative
packet

`fullSq(rhs(x)) <= H_rel,i * V(x) + H_abs,i`

on the same source/domain key as

- full descriptor `M a = rhs`,
- full-mass coercivity `mu>0`,
- acceleration-to-producer metric identity,
- port inequality `portSq<=rhoSq_i*A_up`, and
- the block dissipation lower bound used by the paired power term.

Then the trusted energy checker only needs (4.1)-(4.2). If `H_abs,i=0`, the result is
a homogeneous decay-rate charge; if not, the architecture automatically falls back
to the already-established relative-plus-additive/ultimate-bound lane.

### Explicit non-closures

I have not proved any deployed `H_rel`, `H_abs`, `mu`, `d`, `rhoSq`, descriptor source
equality, true-DH cell coverage, Float64/FD/controller semantics, P8 trajectory,
Lean compile, receipt, provenance, admission, registry update, or P4/P5/M4 parent
closure. This review should remain `pending mathematical child` until those typed
premises are independently supplied.