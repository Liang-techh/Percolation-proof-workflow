---
kind: review_result
review_id: review-T-P5-220-nested-pd-prefix-schur-chart-associativity-liuguanyi-20260910T0558Z
task_id: T-P5-220-NESTED-PD-PREFIX-SCHUR-CHART-ASSOCIATIVITY
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T05:58:00Z
claim_commit: b2a5af8f36322bb0e35bff77b6b26b1f206b53ce
inspected_commit: dccf420f7e90fc110091920bce6ebf869a4fd295
upstream_commits:
  - a81288eb83a2a4e7d3c596893c200dd814197bc0  # T-P5-217 PD-prefix completeness / branch-bound
  - 809f83025a985324d83dcb36280958fc56375db8  # T-P5-218 support-fixed LCP linearization
  - 8e18bf65daa1c307c154506d86e85bd5b5df6c7b  # T-P5-219 reduced compatibility/debit transport
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_nested_schur_associativity; add_fraction_free_prefix_chart_scaling; add_fraction_free_reconstruction_composition; add_graded_debit_scaling; add_prefix_chart_normalized_margin_invariant; add_singular_transition_boundary
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional block algebra, Schur completion, determinant scaling, rational regression; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-220 — nested PD-prefix Schur chart associativity and graded projective transport

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-217 grows a positive-definite support prefix, T-P5-218 eliminates such a prefix by a fraction-free Schur packet, and T-P5-219 consumes the resulting reduced atoms for compatibility / endpoint-debit tests. What was still implicit is whether a producer may grow the PD prefix **incrementally** without changing the mathematical object seen by the downstream consumer.

This child proves the required chart theorem.

For a three-block symmetric matrix with an initial PD block `A`, an added block `J`, and a remainder `R`, assume both the initial prefix and the enlarged prefix are positive definite. Then:

1. eliminating `A` and then the reduced `J` block gives exactly the same ordinary Schur complement as eliminating the enlarged prefix `A union J` in one step;
2. the reconstructed physical vector is exactly the same in both routes;
3. the fraction-free packets differ only by a **positive projective scale** `alpha = det(A)^m`, where `m=dim J`;
4. the reconstruction numerator, residual/Schur numerator, and common denominator all scale by `alpha`;
5. a pulled-back quadratic endpoint/debit numerator scales by `alpha^2`;
6. therefore support feasibility, zero residuals, residual masks, zero compatibility, and debit signs are prefix-chart invariant;
7. quantitative inequalities mixing a state-energy numerator and a debit numerator are invariant only after the denominator is carried with the correct homogeneous degree.

The last point is important: a raw fraction-free matrix is not a canonical normalized matrix. The canonical object is a graded packet.

No actual P5 source matrix, selector/cell/tube binding, Float64 semantics, trajectory coverage, Lean receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Three-block setup

Let

`K = [[A, B, C],
      [B^T, D, E],
      [C^T, E^T, F]]`

be symmetric, where

- `A` is `n x n`,
- `D` is `m x m`, with `m>=1`,
- `F` is `r x r`.

Interpret the coordinates as

- old PD prefix `T` with variable `x`,
- added prefix block `J` with variable `y`,
- remaining coordinates `R` with variable `z`.

Assume

**(H1)** `A > 0`.

Define the ordinary first-stage Schur data

`P := D - B^T A^{-1} B`,

`Q := E - B^T A^{-1} C`,

`R0 := F - C^T A^{-1} C`.

Assume in addition

**(H2)** `P > 0`.

Let the enlarged prefix matrix be

`S := [[A,B],[B^T,D]]`.

By the standard PD Schur criterion,

**`S>0  <=>  A>0 and P>0`.**

So H1-H2 are exactly the condition that both the old and enlarged prefix are legal T-P5-217/218 PD charts.

---

## 2. Theorem A — two successive completions equal one enlarged-prefix completion

For arbitrary `x,y,z`, complete the `A` square:

`[x;y;z]^T K [x;y;z]`

`= (x + A^{-1}(By+Cz))^T A (x + A^{-1}(By+Cz))`

`  + [y;z]^T [[P,Q],[Q^T,R0]] [y;z]`.

Now complete the `P` square:

`[y;z]^T [[P,Q],[Q^T,R0]] [y;z]`

`= (y + P^{-1}Qz)^T P (y + P^{-1}Qz)`

`  + z^T H z`,

where

**`H := R0 - Q^T P^{-1} Q`.**

On the other hand, because `S>0`, completing the whole enlarged prefix gives

`[x;y;z]^T K [x;y;z]`

`= ([x;y] + S^{-1}[C;E]z)^T S ([x;y] + S^{-1}[C;E]z)`

`  + z^T H_dir z`,

with

`H_dir := F - [C^T,E^T] S^{-1} [C;E]`.

The minimizing pair `(x,y)` for fixed `z` is unique because `S>0`. The two-stage completion has minimizer

`y_*(z) = -P^{-1}Qz`,

`x_*(z) = -A^{-1}(B y_*(z) + C z)`.

This pair satisfies

`S [x_*;y_*] + [C;E]z = 0`:

- the first block equation is the definition of `x_*`;
- substituting that into the second gives `P y_* + Qz = 0`.

Hence the two-stage minimizer is exactly the direct enlarged-prefix minimizer,

**`[x_*;y_*] = -S^{-1}[C;E]z`.**

The residual minimum is therefore unique, giving

### Theorem A

**`R0 - Q^T P^{-1}Q = F - [C^T,E^T]S^{-1}[C;E]`.**

Thus ordinary Schur elimination is associative along a nested PD-prefix chain.

No global copositivity hypothesis is required for Theorem A; it is pure finite-dimensional block algebra.

---

## 3. Theorem B — reconstruction maps compose exactly

Define the first reconstruction map

`L_A(y,z) := (-A^{-1}(By+Cz), y, z)`.

Define the second reduced reconstruction map

`L_P(z) := (-P^{-1}Qz, z)`.

Define the direct enlarged-prefix reconstruction map

`L_S(z) := (-S^{-1}[C;E]z, z)`.

The minimizer calculation above proves the exact linear-map identity

### Theorem B

**`L_A o L_P = L_S`.**

This is the basic coordinate-transform theorem needed by any incremental PD-prefix producer.

In particular, a physical zero/tangent reconstructed after two eliminations is not merely equivalent in energy: it is literally the same full-coordinate vector as the direct enlarged-prefix reconstruction.

---

## 4. Fraction-free first-stage packet

Let

`d := det(A) > 0`.

Write

`AdjA := adj(A)`.

The T-P5-218 first-stage fraction-free matrix on `(y,z)` is

`Hhat_A := d [[D,E],[E^T,F]]
            - [[B^T],[C^T]] AdjA [B,C]`.

Partition it as

`Hhat_A = [[Phat,Qhat],[Qhat^T,Rhat]]`.

Because `AdjA=d A^{-1}`,

**`Phat = d P`,**

**`Qhat = d Q`,**

**`Rhat = d R0`.**

Hence `Phat>0` by H2.

Let

`delta := det(Phat)`.

Since `Phat=dP` is `m x m`,

**`delta = d^m det(P) > 0`.**

Let the second-stage fraction-free reconstruction numerator be

`C2 := -adj(Phat) Qhat`.

Then

`C2/delta = -Phat^{-1}Qhat = -P^{-1}Q`,

so the second-stage reduced reconstruction is exactly `y_*(z)=C2 z/delta`.

---

## 5. Theorem C — exact positive scaling of the nested fraction-free Schur numerator

Define the two-stage fraction-free remainder numerator

`Hhat_2 := delta Rhat - Qhat^T adj(Phat) Qhat`.

By the defining T-P5-218 identity applied algebraically to the block `Phat`,

`Hhat_2 = delta (Rhat - Qhat^T Phat^{-1}Qhat)`.

Using `Rhat=dR0`, `Qhat=dQ`, `Phat=dP`,

`Rhat - Qhat^T Phat^{-1}Qhat`

`= dR0 - (dQ)^T (dP)^{-1} (dQ)`

`= d(R0-Q^T P^{-1}Q)`

`= d H`.

Therefore

`Hhat_2 = delta d H`

`= d^(m+1) det(P) H`.

Now define the direct enlarged-prefix determinant

`s := det(S)`.

Since `A>0`,

`det(S)=det(A) det(P)`, hence

**`s = d det(P) > 0`.**

The direct T-P5-218 numerator is

`Hhat_S := s F - [C^T,E^T] adj(S) [C;E]`

and therefore

`Hhat_S = s H`.

Combining the two formulas gives:

### Theorem C — fraction-free Schur chart scaling

**`Hhat_2 = d^m Hhat_S`.**

Set

**`alpha := d^m > 0`.**

Then the nested and direct reduced Schur numerators differ only by the positive scalar `alpha`.

Consequences for all `z,w`:

- `z^T Hhat_2 z >=0  <=>  z^T Hhat_S z >=0`;
- `Hhat_2 z=0  <=>  Hhat_S z=0`;
- coordinate signs and zero masks of `Hhat_2 z` and `Hhat_S z` agree;
- `z^T Hhat_2 w=0  <=>  z^T Hhat_S w=0`.

Thus T-P5-219 residual-mask compatibility is independent of whether the PD prefix was eliminated incrementally or in one enlarged step.

---

## 6. Theorem D — fraction-free reconstruction numerator scales by the same alpha

For the old prefix define its reconstruction numerator on `(y,z)`:

`C_A := -adj(A)[B,C]`.

Then

`x = C_A [y;z]/d`.

The second-stage reconstruction is

`y = C2 z/delta`.

Put both old and newly added prefix coordinates over the common denominator `d delta`:

`[x;y]`

`= 1/(d delta) *
   [ C_A [C2; delta I_r] z ;
     d C2 z ]`.

Define the sequential full-prefix numerator

`C_seq := [ C_A [C2; delta I_r] ; d C2 ]`.

The common sequential denominator is

`t_seq := d delta`.

But

`t_seq = d * d^m det(P) = d^m * s = alpha s`.

Let the direct enlarged-prefix numerator be

`C_S := -adj(S)[C;E]`,

so direct reconstruction is

`[x;y]=C_S z/s`.

By Theorem B both reconstructions are identical for every `z`. Therefore

`C_seq/(alpha s)=C_S/s`, hence

### Theorem D — fraction-free reconstruction chart scaling

**`C_seq = alpha C_S`,**

**`t_seq = alpha s`.**

This is stronger than equality of Schur energies: it is an exact denominator-cleared coordinate-transform identity.

---

## 7. Direct reconstruction cone equals the nested reconstruction cone

Because `alpha>0`, Theorem D gives

`C_seq z >=0  <=>  C_S z>=0`.

The lower block of `C_seq z` is `d C2 z`; since `d>0`, it records exactly the condition `y_*(z)>=0`. The upper block records exactly `x_*(z)>=0` after the common positive denominator is restored.

Hence for `z>=0`:

### Corollary D1 — reconstruction-cone invariance

**direct enlarged-prefix feasibility**

`C_S z>=0`

is equivalent to **sequential feasibility**

`C2 z>=0`

and

`C_A [C2 z; delta z] >=0`.

This is the correct semantic replacement for a dangerous recursive shortcut.

### Important warning: do not recursively assume global copositivity of `Hhat_A`

T-P5-218 already exhibits cases where the first Schur numerator is not copositive on the whole reduced orthant; it is only nonnegative on its inherited reconstruction cone.

Therefore an implementation must **not** say:

`K copositive -> Hhat_A copositive on all (y,z)>=0 -> recursively apply the global T-P5-218 theorem`.

That implication is false in general.

What is valid is:

- carry the inherited cone `C_A[y;z]>=0`, or
- use Theorem D to jump directly to the enlarged-prefix numerator `C_S`, or
- reconstruct the candidate and appeal back to the original globally copositive `K`.

The chart algebra is recursive; the global copositivity premise is not automatically recursive.

---

## 8. Theorem E — quadratic endpoint/debit pullback has degree-two chart scaling

Let `G=G^T` be any symmetric full-coordinate quadratic form. This may be a T-P5-219 endpoint/debit matrix after a fixed linear tangent lift.

Define the ordinary direct pulled-back form

`G_red := L_S^T G L_S`.

By Theorem B,

`G_red = L_P^T (L_A^T G L_A) L_P`.

So ordinary pullback is exactly associative.

T-P5-219's fraction-free debit packet for a reconstruction denominator `t` is precisely

`t^2 * (ordinary pulled-back matrix)`.

For the direct enlarged prefix this gives

`Ghat_S = s^2 G_red`.

After the first stage,

`Ghat_A = d^2 L_A^T G L_A`.

If the second fraction-free pullback is applied to that already fraction-free matrix, its numerator is

`Ghat_2 = delta^2 L_P^T Ghat_A L_P`

`= delta^2 d^2 G_red`

`= (d delta)^2 G_red`

`= (alpha s)^2 G_red`.

Therefore:

### Theorem E — graded debit scaling

**`Ghat_2 = alpha^2 Ghat_S`.**

Thus all T-P5-219 self/cross debit sign tests are chart invariant:

- `z^T Ghat_2 z >0  <=>  z^T Ghat_S z>0`;
- `z^T Ghat_2 w >0  <=>  z^T Ghat_S w>0`;
- zero debit is likewise invariant.

The power `2` is not cosmetic. It is forced by the fact that a quadratic form contains two copies of the reconstructed vector numerator.

---

## 9. Graded projective packet

The direct enlarged-prefix fraction-free packet is

`(s, C_S, Hhat_S, Ghat_S)`.

The sequential packet is

`(t_seq, C_seq, Hhat_2, Ghat_2)`.

Theorems C-D-E prove the single transformation law

### Theorem F — graded projective chart equivalence

For `alpha=d^m>0`,

**`t_seq = alpha s`,**

**`C_seq = alpha C_S`,**

**`Hhat_2 = alpha Hhat_S`,**

**`Ghat_2 = alpha^2 Ghat_S`.**

Therefore these are two fraction-free representatives of the same physical chart.

The physical objects are recovered as

`reconstruction = C z / t`,

`reduced K-energy/residual matrix = Hhat / t`,

`reduced debit matrix = Ghat / t^2`.

All three are exactly invariant under the graded rescaling above.

This is the recommended typed mathematical contract:

`FractionFreePDChart := {den>0, recon_num, schur_num, quadratic_num}`

with projective equivalence

`(den,C,H,G) ~ (alpha den, alpha C, alpha H, alpha^2 G)` for `alpha>0`.

---

## 10. Normalization theorem for quantitative Lyapunov margins

Zero and sign tests are insensitive to positive scaling. Quantitative comparisons are subtler.

Suppose the physical reduced matrices satisfy a quadratic domination target

`G_red <= kappa H_red`

in whatever cone/order the downstream theorem uses.

Since

`G_red=Ghat/t^2`,

`H_red=Hhat/t`,

the equivalent fraction-free condition is

### Theorem G — denominator-aware margin identity

**`Ghat <= kappa * t * Hhat`.**

This form is invariant under Theorem F, because both sides scale by `alpha^2`.

By contrast, the raw comparison

`Ghat <= kappa Hhat`

is **not chart invariant**: after a nested prefix extension its left side scales by `alpha^2` and its right side only by `alpha`.

Thus any support-margin / decay-rate consumer that mixes the T-P5-218 Schur numerator with a T-P5-219 debit numerator must carry the positive denominator explicitly, or normalize both matrices back to the ordinary pullback.

This is a genuine interface requirement, not formatting metadata.

---

## 11. Exact rational regression — scaling is visible and nontrivial

Take scalar old prefix and scalar added prefix:

`K = [[2,1,1],
      [1,3,1],
      [1,1,4]]`.

Here

`A=[2]`, `d=2`,

`P = 3-1/2 = 5/2 >0`,

`Q = 1-1/2 = 1/2`,

`R0 = 4-1/2 = 7/2`.

The enlarged prefix is

`S=[[2,1],[1,3]]`,

with

`s=det(S)=5`.

The ordinary final Schur scalar is

`H = 7/2 - (1/2)^2/(5/2) = 17/5`.

### Direct fraction-free route

`Hhat_S = s H = 5*(17/5)=17`.

### Two-stage fraction-free route

First-stage numerators are

`Phat=5`, `Qhat=1`, `Rhat=7`.

Thus

`delta=5`,

`Hhat_2 = 5*7-1^2 = 34`.

Because `m=1`,

`alpha=d^m=2`,

and indeed

`Hhat_2 = 2*17 = alpha Hhat_S`.

### Reconstruction

The reduced added-prefix variable is

`y=-z/5`.

Then

`x=-1/2(y+z)=-2z/5`.

So the physical full reconstruction is

`(-2/5,-1/5,1)z`,

whether obtained directly from `S^{-1}` or sequentially.

The direct numerator/denominator are

`C_S=(-2,-1)^T`, `s=5`.

The sequential common numerator/denominator are

`C_seq=(-4,-2)^T`, `t_seq=10`,

again exactly scaled by `alpha=2`.

### Debit-degree regression

Take endpoint/debit matrix `G=I_3`.

Along the reconstructed ray,

`G_red = (4+1+25)/25 = 6/5`.

Direct T-P5-219 numerator:

`Ghat_S = s^2 G_red = 25*(6/5)=30`.

After the first elimination,

`Ghat_A = [[5,1],[1,5]]`.

The second fraction-free pullback with `delta=5` gives

`Ghat_2=120`.

Thus

`Ghat_2 = 4*30 = alpha^2 Ghat_S`.

The raw ratio changes:

`Ghat_S/Hhat_S = 30/17`,

`Ghat_2/Hhat_2 = 120/34 = 60/17`.

It differs by the factor `alpha=2`.

But the denominator-aware ratio is invariant:

`Ghat_S/(s Hhat_S)=30/(5*17)=6/17`,

`Ghat_2/(t_seq Hhat_2)=120/(10*34)=6/17`.

This regression is an exact counterexample to treating raw fraction-free matrices from different PD-prefix depths as already normalized to the same scale.

---

## 12. Singular transition boundary

The nested theorem deliberately assumes `P>0`.

If `P` becomes singular, the enlarged prefix is no longer positive definite, `delta=det(Phat)=0`, and the second PD chart cannot be formed.

The canonical exact example is

`K = [[1,-1],[-1,1]]`.

Choose old prefix `A=[1]>0`. The reduced Schur scalar is

`P = 1-(-1)^2 = 0`.

The full matrix is PSD singular and has the genuine minimal zero atom `(1,1)`, but attempting to continue PD elimination would divide by zero.

This is **not** a failure of the atom or of copositivity. It is exactly the T-P5-217 `sigma=0` emission boundary / earlier singular-kernel regime.

Therefore the dispatcher rule is:

- `P>0`: nested PD chart transport is legal and Theorems A-G apply;
- `P` reaches a corank-one strict-positive kernel boundary: emit/test the atom rather than extending the PD chart;
- higher singularity or non-PD branch: return to the T-P5-214/216 singular-support/kernel machinery as appropriate;
- never introduce a pseudoinverse merely to keep the PD chart alive.

---

## 13. Relation to T-P5-217/218/219

### T-P5-217

Its branch-and-bound grows PD prefixes. Theorem F shows that an implementation may update the fraction-free packet incrementally at each positive Schur step without changing the physical chart.

### T-P5-218

Its support-fixed reconstruction can be reused after a nested prefix extension, but the inherited reconstruction cone must be transported. Theorem D supplies the exact division-free cone identity.

### T-P5-219

Its reduced compatibility and debit signs are invariant under the chart transport by Theorems C and E. Therefore repeated reconstruction in the full coordinates is unnecessary merely because the PD prefix was grown in stages.

For quantitative debit-vs-energy margins, Theorem G adds the denominator normalization that T-P5-219's sign-only use did not need.

---

## 14. Minimal theorem leaves for formalization

Recommended source-independent leaves:

- `nestedPD_iff_schurPD`
  - `S>0 <=> A>0 and P>0`.
- `nestedSchur_assoc`
  - `schur_P(schur_A(K)) = schur_S(K)`.
- `pdReconstruction_comp`
  - `L_A ∘ L_P = L_S`.
- `fractionFree_nested_den_scale`
  - `d*det(dP) = d^m*det(S)`.
- `fractionFree_nested_reconstruction_scale`
  - `C_seq = d^m C_S`.
- `fractionFree_nested_schur_scale`
  - `Hhat_2 = d^m Hhat_S`.
- `fractionFree_nested_quadratic_scale`
  - `Ghat_2 = d^(2m) Ghat_S`.
- `fractionFree_reconstructionCone_invariant`
  - direct cone iff sequential inherited cone.
- `fractionFree_residualMask_invariant`
  - positive scaling preserves zero/positive residual masks.
- `fractionFree_margin_normalization`
  - physical `G<=kappa H` iff `Ghat<=kappa*den*Hhat`.

A formal implementation should keep matrix dimensions explicit and should not require square roots, eigenvectors, pseudoinverses, or floating normalization.

---

## 15. Failure / non-FAIL boundaries

1. **Intermediate `P` not PD.** The nested PD chart is unavailable; this is a routing boundary, not automatically a physical FAIL.
2. **Reduced `Hhat_A` not globally copositive.** This is allowed. Only the inherited reconstruction cone is relevant. Do not recursively assume full-orthant copositivity.
3. **Raw fraction-free matrices disagree numerically across prefix depth.** Expected: `Hhat` has degree one and debit `Ghat` degree two in the positive chart scale. Compare normalized physical forms or carry the denominator.
4. **Different physical endpoint/tangent lifts.** Theorem E only transports the same fixed full-coordinate symmetric form `G`. Face-dependent changes in the lift remain separate source/branch obligations.
5. **Floating determinant/rank decisions.** `P>0`, `det`, zero residual masks, and the singular transition are exact gates; Float64 tolerances cannot replace exact rational/interval evidence.
6. **Source binding absent.** The theorem is source-independent and cannot identify the actual P5 matrix, selector, cell, tube, or trajectory.

---

## 16. Recommended dispatcher contract

For a T-P5-217 PD-prefix search, maintain a graded fraction-free chart

`(den, recon_num, schur_num, debit_num)`.

On a strict PD extension of dimension `m`:

1. perform the local fraction-free Schur update;
2. update the common reconstruction denominator and numerator;
3. record the positive projective scale implied by the determinant identity;
4. keep inherited cone feasibility through the reconstruction numerator rather than asserting global copositivity of the reduced matrix;
5. use `schur_num` directly for zero/residual/compatibility sign tests;
6. use `debit_num` directly for debit sign tests;
7. for any quantitative debit-vs-energy margin, consume the invariant combination `debit_num <= kappa * den * schur_num` (or its cone-order analogue), not the unnormalized raw pair.

At the first singular Schur transition, stop the PD chart and hand the branch to the atom/singular-kernel logic already supplied by T-P5-217 and T-P5-214/216.

---

## 17. Boundaries left open

- actual same-key P5 `K/G` and endpoint-lift source binding;
- physical selector/cell/tube identity and trajectory coverage;
- deciding which PD-prefix order is computationally best;
- exact interval/Float64 reification of determinant and zero-mask gates;
- Lean/kernel compilation and axiom audit;
- 封不觉 independent validation;
- admission, registry mutation, and P5/P8/M4 parent propagation.

The mathematical child itself closes the nested-prefix coordinate-transform and normalization seam: incremental PD elimination is exact, but only as a **graded projective chart with inherited cone semantics**.