---
kind: review_result
review_id: review-T-P5-219-pd-prefix-zero-debit-pair-reduction-honglianmozun-20260910T0550Z
task_id: T-P5-219-PD-PREFIX-ZERO-DEBIT-PAIR-REDUCTION
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T05:50:00Z
claim_commit: 7a7f4b2dac328aefcd27304f85551ce07af45916
inspected_commit: fadd6bacf5b726bf6549abc839f951218bfad3c6
upstream_commits:
  - 809f83025a985324d83dcb36280958fc56375db8  # T-P5-218 PD-prefix support LCP linearization
  - 4daeafdb1733f8bba97cd4576b68989cdcf31890  # T-P5-215 zero compatibility / one-pair debit theorem
  - 803e7681f61385fee8a9c1c00b97c1d76061ee71  # T-P5-216 minimal-zero atom residual-growth bridge
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_pd_prefix_cross_energy_pullback; add_reduced_residual_compatibility_mask; add_fraction_free_debit_pullback; add_reduced_one_pair_endpoint_checker; add_exact_regressions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional block algebra, conic zero-energy identities, Lyapunov/debit pullback, rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-219 — PD-prefix zero/debit pair reduction

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-218 closes exact zero-atom existence at a fixed remaining support after a positive-definite prefix has been eliminated, but its dispatcher still reconstructs full vectors before handing genuine atoms to T-P5-215. T-P5-215 then decides zero compatibility and second-order endpoint debit using full zero rays / lifted tangents.

This child composes the two layers and removes that unnecessary reconstruction step from the energy consumer.

For the T-P5-218 fraction-free objects

`d = det(A) > 0`,

`C = -adj(A) B`,

`Hhat = d D - B^T adj(A) B`,

and reduced coordinate `lambda`, define

`x(lambda) = (C lambda / d, lambda)`.

Then for **two** reduced vectors `lambda,mu`, not only for a self-energy,

**`d * x(lambda)^T K x(mu) = lambda^T Hhat mu`.**

For genuine copositive zeros, `Hhat lambda >= 0`; hence compatibility is exactly

**`lambda^T Hhat mu = 0`,**

or equivalently

**`supp(mu) subseteq {j : (Hhat lambda)_j = 0}`.**

Thus the T-P5-215 compatibility graph can be built entirely from the reduced T-P5-218 support-LP outputs.

For any symmetric endpoint debit matrix `Q`, partitioned conformally as

`Q = [[P,R],[R^T,S]]`,

define the fraction-free reduced debit

**`Qhat = C^T P C + d(C^T R + R^T C) + d^2 S`.**

Then

**`d^2 * x(lambda)^T Q x(mu) = lambda^T Qhat mu`.**

Therefore all T-P5-215 one-ray / compatible-pair debit signs can also be checked in reduced coordinates, with no inverse, square root, eigenvector, pseudoinverse, or rational division in the trusted sign checker.

The result is an exact energy-side dispatcher:

`T-P5-218 support LP -> reduced atom lambda -> Hhat-residual compatibility -> Qhat self/cross debit -> T-P5-215 one-ray/pair endpoint witness`.

No actual P5 same-key matrix, selector/cell/tube source, Float64/interval semantics, Lean/kernel receipt, independent validation, registry admission, or parent closure is claimed.

---

## 1. Setup

Let `K=K^T` be globally copositive on the nonnegative orthant and split its coordinates into a positive-definite prefix `T` and remaining coordinates `R`:

`K = [[A,B],[B^T,D]]`,

with `A=A^T>0`.

Let

`d := det(A) > 0`,

`C := -adj(A) B`,

`Hhat := d D - B^T adj(A) B`.

For any reduced vector `lambda in R^R`, set

`x(lambda) := (C lambda / d, lambda)`.

T-P5-218 proves the exact reconstruction identity

`K x(lambda) = (0, Hhat lambda / d)`.

It also proves that when a fixed-support normalized LP succeeds under the inherited global copositivity premise, the reconstructed vector is a genuine copositive zero and its inactive residual is nonnegative.

The present child uses that result; it does not redo support enumeration or Farkas admission.

---

## 2. T219-A — fraction-free cross-energy identity

### Theorem A

For arbitrary reduced vectors `lambda,mu`,

**`d * x(lambda)^T K x(mu) = lambda^T Hhat mu`.**

### Proof

From T-P5-218 reconstruction,

`K x(mu) = (0, Hhat mu/d)`.

Hence

`x(lambda)^T K x(mu)`

`= (C lambda/d)^T 0 + lambda^T(Hhat mu/d)`

`= lambda^T Hhat mu/d`.

Multiply by the positive scalar `d`.

QED.

Because `Hhat` is symmetric, the right-hand side is symmetric in `lambda,mu`, as required.

### Corollary A1 — self-energy

Setting `mu=lambda` recovers

`d * x(lambda)^T K x(lambda) = lambda^T Hhat lambda`.

The cross version is the new piece needed by the T-P5-215 compatibility layer.

---

## 3. T219-B — reduced residual and exact compatibility mask

Let `lambda` be a genuine reduced zero produced by T-P5-218, so

`x(lambda)>=0`,

`x(lambda)^T K x(lambda)=0`.

Since `K` is copositive, zero complementarity gives

`K x(lambda)>=0`.

Using the reconstruction identity and `d>0`,

**`Hhat lambda >= 0`.**

Now let `mu` be another genuine reduced zero from the same PD-prefix branch.

### Theorem B

The following are equivalent:

1. `x(lambda)` and `x(mu)` are T-P5-215 compatible zeros;
2. `x(lambda)^T K x(mu)=0`;
3. `lambda^T Hhat mu=0`;
4. `(Hhat lambda)^T mu=0`;
5. `supp(mu) subseteq Z(lambda)`, where

   `Z(lambda):={j:(Hhat lambda)_j=0}`.

### Proof

T-P5-215 defines zero compatibility by item 2. Theorem A and `d>0` give `2 <=> 3`. Symmetry of `Hhat` gives `3 <=> 4`.

For item 5, every coordinate of `Hhat lambda` and of `mu` is nonnegative. Therefore

`(Hhat lambda)^T mu = sum_j (Hhat lambda)_j mu_j`

is zero iff every coordinate with positive reduced residual has `mu_j=0`.

QED.

### Corollary B1 — support-LP pair pruning

Suppose atom `a` is produced on support `J_a` and atom `b` on support `J_b`. Define the exact reduced residual mask

`P_a := {j:(Hhat lambda_a)_j>0}`.

Then

**`a` and `b` are compatible iff `J_b cap P_a = emptyset`.**

Thus pair compatibility can be implemented as a support-mask / bitset test after one exact matrix-vector product per atom.

No reconstructed full rational vector is needed.

### Important boundary

T-P5-218 already warns that `Hhat` need not be copositive on the full reduced orthant. The argument above does **not** assume that. It uses only the fact that `Hhat lambda>=0` for a **genuine reconstructed copositive zero**. Applying the residual-mask test to an arbitrary reduced vector that has not passed the T-P5-218 zero gate is unsound.

---

## 4. T219-C — fraction-free pullback of an arbitrary symmetric debit

Let the symmetric quadratic debit / second-order form be

`Q = [[P,R],[R^T,S]]`,

with the same `T|R` coordinate split as `K`.

Define

**`Qhat := C^T P C + d(C^T R + R^T C) + d^2 S`.**

`Qhat` is symmetric.

### Theorem C

For arbitrary reduced `lambda,mu`,

**`d^2 * x(lambda)^T Q x(mu) = lambda^T Qhat mu`.**

### Proof

Expand directly:

`x(lambda)^T Q x(mu)`

`= (C lambda/d)^T P(C mu/d)`

`  + (C lambda/d)^T R mu`

`  + lambda^T R^T(C mu/d)`

`  + lambda^T S mu`.

Multiplying by `d^2` gives

`lambda^T C^T P C mu`

`+ d lambda^T C^T R mu`

`+ d lambda^T R^T C mu`

`+ d^2 lambda^T S mu`

`= lambda^T Qhat mu`.

QED.

Because `d^2>0`, all self- and cross-debit signs are preserved exactly.

### Corollary C1 — linear endpoint lifts

If T-P5-215's endpoint tangent is `L x(lambda)` for a fixed linear map `L`, replace `Q` above by

`Qeff := L^T Q L`.

Then the same formula applies verbatim. Hence a fixed Schur/active-kernel lifting layer need not be carried into every atom-pair check.

### Corollary C2 — cone pullback

For any nonnegative coefficients `a_i` and reduced atoms `lambda_i`, linearity gives

`sum_i a_i x(lambda_i) = x(sum_i a_i lambda_i)`.

Therefore on any compatibility clique the full debit quadratic and the reduced `Qhat` quadratic differ only by the positive factor `d^2`.

So copositivity of the lifted debit on that zero cone is equivalent to copositivity of its reduced Gram/pullback.

---

## 5. T219-D — reduced one-ray / compatible-pair endpoint theorem

Assume now a finite packet of genuine T-P5-218 minimal-zero atoms

`lambda_1,...,lambda_N`

is complete for the endpoint zero family under consideration, and every nonzero member of that family uses the same strict-positive PD prefix `T`.

Let

`x_i := x(lambda_i)`.

Assume also the inherited T-P5-215/T-P5-210 common-zero hypothesis: on every compatibility clique, the endpoint debit pullback is copositive.

Define exact reduced scalars

`k_ij := lambda_i^T Hhat lambda_j`,

`q_ij := lambda_i^T Qhat lambda_j`.

Then `k_ij>=0` for genuine zero atoms, and

`k_ij=0 <=> i,j compatible`.

Moreover

`q_ij = d^2 x_i^T Q x_j`.

### Theorem D

There exists a positive-debit endpoint zero direction in this complete PD-prefix family iff at least one of the following holds:

**(A) Reduced one-atom witness**

there exists `i` with

**`q_ii>0`.**

**(B) Reduced compatible-pair witness**

there exist distinct `i,j` such that

**`k_ij=0`,**

**`q_ii=q_jj=0`,**

and

**`q_ij>0`.**

In case (B), an explicit witness is represented by

`lambda_* = lambda_i + lambda_j`,

because

`x(lambda_*)=x_i+x_j`

is still a zero and

`d^2 x(lambda_*)^T Q x(lambda_*)`

`=q_ii+2q_ij+q_jj`

`=2q_ij>0`.

### Proof

The reverse direction follows from Theorems B and C.

For the forward direction, T-P5-215 proves that under completeness of the atom packet and copositivity of the debit pullback on each zero compatibility clique, every positive-debit witness can be reduced to either one atom with positive self debit or two compatible atoms with zero self debits and positive cross debit.

Theorem C multiplies every debit Gram entry by the same positive scalar `d^2`, and Theorem B replaces full compatibility by `k_ij=0`. Hence the T-P5-215 alternatives are exactly (A) and (B).

QED.

### Consequence

After T-P5-218 has generated genuine atoms, the T-P5-215 second-order decision layer can run entirely on the reduced packet

`(lambda_i, Hhat lambda_i, Qhat)`.

Full `x_i=(C lambda_i/d,lambda_i)` reconstruction is needed only if a downstream consumer explicitly requests a physical/full-coordinate witness.

---

## 6. Exact rational checker packet

For rational input matrices, all trusted checks are rational and division-free after `d,C,Hhat,Qhat` have been formed.

For each T-P5-218 atom `lambda_i`:

1. retain its already-checked support LP / minimality receipt;
2. compute `rhat_i := Hhat lambda_i` exactly;
3. verify `rhat_i>=0` as a redundant sanity check if desired;
4. store the positive-residual mask `P_i={j:rhat_i,j>0}`;
5. compute `q_ii=lambda_i^T Qhat lambda_i`.

For a candidate pair `(i,j)`:

6. reject compatibility immediately if `supp(lambda_j)` intersects `P_i`;
7. otherwise `k_ij=0` exactly;
8. if both self debits are zero, compute only the cross scalar `q_ij`;
9. `q_ij>0` produces the explicit reduced witness `lambda_i+lambda_j`.

All sign decisions use exact integer/rational arithmetic. No division by `d`, no reconstruction of `C lambda/d`, and no square root or eigensolver is needed in this stage.

---

## 7. Regression A — two strict-prefix zero atoms that are incompatible

Take

`K = [[1,-1,-1],[-1,1,2],[-1,2,1]]`.

For nonnegative `(x1,x2,x3)`,

`x^T K x = (x1-x2-x3)^2 + 2 x2 x3 >= 0`,

so `K` is copositive.

Choose prefix `T={1}`. Then

`A=[1]`, `d=1`,

`C=[1,1]`,

`Hhat=[[0,1],[1,0]]`.

The singleton support LPs produce

`lambda_1=(1,0)`, `lambda_2=(0,1)`,

with reconstructed zeros

`x_1=(1,1,0)`, `x_2=(1,0,1)`.

Their reduced residuals are

`Hhat lambda_1=(0,1)`,

`Hhat lambda_2=(1,0)`.

Hence each atom's positive residual mask forbids the other's remaining support, and

`lambda_1^T Hhat lambda_2=1>0`.

Indeed

`x_1^T K x_2=1`,

and

`(x_1+x_2)^T K(x_1+x_2)=2>0`.

This is an exact negative-control for accidental mixing of T-P5-218 atoms.

---

## 8. Regression B — pair-only positive debit after PD-prefix elimination

Take instead the PSD matrix

`K = [[1,-1,-1],[-1,1,1],[-1,1,1]]`.

Its energy is

`x^T K x=(x1-x2-x3)^2>=0`.

Again `T={1}` gives

`A=[1]`, `d=1`, `C=[1,1]`,

but now

`Hhat=0`.

The same two singleton atoms

`lambda_1=(1,0)`, `lambda_2=(0,1)`

reconstruct to

`x_1=(1,1,0)`, `x_2=(1,0,1)`.

They are compatible because

`lambda_1^T Hhat lambda_2=0`.

Choose the symmetric debit

`Q = [[0,0,0],[0,0,1],[0,1,0]]`.

Here `P=0`, `R=0`, and

`S=[[0,1],[1,0]]`,

so

`Qhat=[[0,1],[1,0]]`.

The atom self debits vanish:

`q_11=q_22=0`,

while the reduced cross debit is

`q_12=1>0`.

Thus neither atom alone is a positive-debit endpoint witness, but the compatible pair is:

`lambda_*=(1,1)`,

`x(lambda_*)=(2,1,1)`,

and

`x(lambda_*)^T Q x(lambda_*)=2>0`.

This regression shows that the reduced pair test retains the genuinely new T-P5-215 phenomenon; it is not merely a self-debit screen.

---

## 9. Why the debit-copositivity premise cannot be dropped

The sparse T-P5-215 alternative is not valid for an arbitrary indefinite debit Gram.

For example on a compatible two-atom cone take

`D=[[-1,2],[2,-1]]`.

Then neither atom has positive self debit, neither self debit is zero, yet

`(1,1)^T D(1,1)=2>0`.

Thus without the inherited T-P5-210 small-perturbation / clique-copositivity gate, a positive endpoint combination can arise from competition between negative diagonal terms and a positive cross term, and Theorem D's restricted one/pair sign pattern is not complete.

The reduced fraction-free identities A-C remain valid algebraically, but the sparse existence theorem D must then be reported as unavailable rather than silently applied.

---

## 10. Failure / non-FAIL boundaries

1. **Missing global copositivity of `K`.** The algebraic cross/debit identities remain true, but automatic nonnegative reduced residuals and support-mask compatibility do not follow. Report premise missing, not a mathematical FAIL.
2. **Prefix not positive definite.** `d>0` and the T-P5-218 reconstruction packet are unavailable. Singular/PSD active blocks must return to the earlier kernel/range-compatible Schur machinery.
3. **Incomplete atom packet.** A reduced one/pair scan can certify a found witness but cannot certify absence of all endpoint witnesses.
4. **Zeros outside the chosen strict-prefix family.** T-P5-218 atoms only cover the branch for which the selected prefix is positive. Boundary zeros not belonging to that branch require another support/prefix packet.
5. **Face-dependent nonlinear lift.** A single `Qeff=L^TQL` only applies to a fixed linear lift. If the endpoint tangent map changes by face, form a separate `Qhat` per face/branch and do not merge them without a compatibility proof.
6. **Debit pullback not copositive on zero cliques.** Theorem D cannot be used; Regression in section 9 is the exact obstruction.
7. **Floating near-zero arithmetic.** `k_ij=0`, `q_ii=0`, rank/corank and residual masks are exact gates. Float64 tolerances are not substitutes for rational/interval proof.

---

## 11. Candidate theorem leaves

A minimal formal decomposition is:

- `pdPrefix_crossEnergy_fractionFree`
  - `d * <x(lambda),K x(mu)> = <lambda,Hhat mu>`.
- `pdPrefix_zero_reducedResidual_nonneg`
  - genuine copositive zero implies `Hhat lambda>=0`.
- `pdPrefix_zeroCompatibility_iff_reducedCrossZero`
  - compatibility iff `lambda^T Hhat mu=0`.
- `pdPrefix_zeroCompatibility_supportMask`
  - under nonnegative residual, cross-zero iff support avoids the positive mask.
- `pdPrefix_debitPullback_fractionFree`
  - `d^2 * <x(lambda),Q x(mu)> = <lambda,Qhat mu>`.
- `pdPrefix_linearLift_debitPullback`
  - absorb fixed tangent lift via `Qeff=L^TQL`.
- `pdPrefix_reduced_onePair_endpointWitness`
  - consume T-P5-215 completeness/copositivity assumptions and return the reduced one/pair alternative.

These are source-independent exact-real/rational leaves suitable for later Lean work, but no Lean receipt is claimed here.

---

## 12. Recommended dispatcher

For the PD-prefix branch the mathematical decision flow can now be:

`T-P5-217 family prune`

`-> T-P5-218 support LP / minimal atom`

`-> compute one reduced residual Hhat*lambda per atom`

`-> build compatibility graph from residual masks`

`-> compute Qhat once per fixed endpoint/debit lift`

`-> scan self debits`

`-> scan only compatible pairs whose self debits vanish`

`-> reconstruct a full witness only on demand`.

This is still conditional on atom completeness and the T-P5-210/T-P5-215 debit-copositivity premise, but it removes repeated full-coordinate Schur reconstruction from the hottest energy/Lyapunov pair-search loop.

---

## 13. Boundaries left open

- actual same-key P5 `K,Q` / endpoint-lift source binding;
- completeness of the selected PD-prefix atom family for the physical endpoint zero set;
- selector/cell/tube and trajectory coverage;
- Float64/interval implementation of exact-zero gates;
- Lean/kernel compilation and axiom audit;
- 封不觉 independent validation;
- admission, registry mutation, and P5/P8/M4 parent propagation.

The mathematical child itself is complete as a fraction-free composition layer between T-P5-218 atom production and T-P5-215 sparse second-order energy witnessing.