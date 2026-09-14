---
kind: review_result
review_id: T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET-guyuefangyuan-20260909T0030Z
task_id: T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET
reviewer: 古月方源
source_agent: 古月方源
source_commit: 90563d1f5afab6b94dc4eb24e8b76a57fd5b0b0d
verdict: PASS
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_compile_status: not_run
---

# T-P5-112: inverse-free implicit-graph jet -> same-cell affine-anchor budget

## 0. Scope and why this is a new leaf

The current exact DH source-jet packet gives exact `M,DM,R,DR` on the physical `(q,v,w)` source representation, while the graph-jet reviews correctly isolate the implicit graph

`M(z) alpha(z) = R(z)`

and its first jet without ever materializing `M^{-1}`.  The remaining P5 anchor-budget question is finite rather than pointwise: if an anchor `z0` and its graph jet `(alpha0,Y0)` are known/certified, how much can the true graph value at another point `z1` differ from the affine predictor

`alpha_pred = alpha0 + Y0 * (z1-z0)`?

This child gives a smallest exact-rational bridge.  It does not generate any real numerical P5 budget because the required second-jet cap and quantitative lower-gain witness have not yet been source-certified.

## 1. Physical same-cell segment and second implicit jet

Let `Omega` be a physical `(q,v,w)` cell and assume the physical straight segment

`z_s = z0 + s*delta`, `delta = z1-z0`, `0 <= s <= 1`

lies in the open source neighborhood on which the exact graph is `C^2` and single-valued.  All trigonometric lift variables are re-evaluated from the physical `q_s`; **this is not a straight segment in independent `(c_i,s_i)` variables**.

Write

`a(s) = alpha(z_s)`.

The first graph jet is

`M a' = DR[delta] - DM[delta_q] a`.

Differentiating once more along the same physical segment gives the exact inverse-free identity

`M a'' = J2`,

where

`J2 := D2R[delta,delta] - D2M[delta_q,delta_q] a - 2 DM[delta_q] a'`.

For the present DH model `M=M(q)`, so only `delta_q` enters the derivatives of `M`; `R` may depend on all physical `(q,v,w)` directions.  The identity is a source/derivative statement and must be proved with the physical `q -> (q,cos q,sin q)` pullback, exactly as for the existing first jet.

The current extractor does not yet emit `D2M,D2R`; that is a source-side missing object, not a reason to introduce an explicit inverse.

## 2. Quantitative inverse-free lower-gain premise

Fix PSD quadratic forms `Q_A` on acceleration space and `Q_R` on descriptor-RHS space.  Assume a **uniform squared lower gain** on the same segment:

`gamma * Q_A(v) <= Q_R(M(z_s) v)` for all `s in [0,1]`, all `v`, with `gamma > 0`.

This is stronger than mere nonsingularity but is exactly the quantitative information required for a numerical anchor budget.  It can be certified by a direct coercivity/singular-value-square witness or derived from a preconditioner packet; no inverse entries are required in the theorem.

Assume also the correlated second-jet RHS cap

`Q_R(J2(s)) <= H2`

for every point of the same physical segment.  From `M a''=J2` we immediately get

`gamma * Q_A(a''(s)) <= H2`.

No division is needed in the trusted inequality chain.

## 3. Main affine-anchor remainder theorem

Define the anchor remainder

`r_anchor := alpha(z1) - alpha(z0) - Dalpha(z0)[delta]`.

Since `a` is `C^2`, Taylor with integral remainder gives

`r_anchor = integral_0^1 (1-s) a''(s) ds`.

For every PSD quadratic form `Q`, weighted Cauchy/Jensen gives

`Q(integral k(s)u(s) ds) <= (integral k) * integral k(s) Q(u(s)) ds`

for nonnegative `k`.  Taking `k(s)=1-s`, using `integral_0^1 (1-s) ds = 1/2`, and the bound above,

`gamma * Q_A(r_anchor)
 <= (1/2) * integral_0^1 (1-s) H2 ds
 = H2/4`.

Hence the exact division-free conclusion is

**`4 * gamma * Q_A(r_anchor) <= H2`.**

Therefore a proposed rational anchor budget `D_anchor >= 0` is certified by the single checker gate

**`H2 <= 4 * gamma * D_anchor`.**

The checker never evaluates `M^{-1}`, a square root, a smallest singular value, or a floating-point Taylor remainder.

## 4. Cell-radius specialization

Often the second-jet producer is homogeneous in the segment displacement.  Let `Q_Z(delta) <= S` for every target point relative to the chosen anchor and suppose the source certificate proves

`Q_R(J2(s)) <= K2 * Q_Z(delta)^2`.

Then

**`4 * gamma * Q_A(r_anchor) <= K2 * S^2`.**

Thus the entire anchor cell is covered by the exact-rational gate

**`K2 * S^2 <= 4 * gamma * D_anchor`.**

This is the natural real-P5 anchor-budget interface: the geometry/search layer may propose the anchor and a rational `D_anchor`; the trusted layer only checks same-cell identity, `S`, `gamma`, `K2`, and the final polynomial inequality.

If the downstream budget is measured in a different fixed quadratic metric `Q_*`, first provide an exact comparator `m Q_*(v) <= M_c Q_A(v)` and cross-multiply.  One must not silently reuse a moving P5 metric at a different state as `Q_A`.

## 5. Preconditioner-to-lower-gain corollary

The graph-jet review notes an existing candidate interface of the form

`||I - X M||_A <= kappa < 1`.

To turn that qualitative invertibility packet into an anchor budget, one more quantitative field suffices.  Suppose, in compatible quadratic norms,

1. `||(I-XM)v||_A <= kappa ||v||_A`, with `0 <= kappa < 1`;
2. `Q_A(Xy) <= chi * Q_R(y)`, with `chi >= 0`.

Then triangle inequality gives

`(1-kappa)||v||_A <= ||X M v||_A`,

hence after squaring and using (2),

**`(1-kappa)^2 * Q_A(v) <= chi * Q_R(Mv)`.**

Combining this directly with the second-jet cap avoids division by `chi`:

**`4*(1-kappa)^2 * Q_A(r_anchor) <= chi * H2`.**

A rational proposed budget therefore passes whenever

**`chi * H2 <= 4*(1-kappa)^2 * D_anchor`.**

This is useful because the currently discussed P5 cell packet already has a preconditioner `X` and contraction parameter `kappa`; the genuinely new quantitative source field is an exact squared operator cap `chi` for `X` in the chosen RHS/acceleration metrics, together with the same-cell second-jet bound.

## 6. Two exact obstructions

### 6.1 Anchor-only curvature is insufficient

Take the scalar graph `alpha(x)=x^3`, anchor `x0=0`, target `x1=1`.  Then

`alpha''(0)=0`,

but

`r_anchor = alpha(1)-alpha(0)-alpha'(0) = 1`.

So a Hessian/second-jet value certified only at the anchor cannot justify any finite-segment remainder gate.  The second-jet cap must cover the **whole physical anchor-to-target segment** (or another explicitly certified connecting path).

### 6.2 Nonsingularity alone gives no uniform numerical budget

For any `eps>0`, let the scalar implicit graph be

`M=eps`, `R(x)=x^2/2`, so `alpha(x)=x^2/(2 eps)`.

The second RHS derivative is uniformly `R''=1`, while

`alpha''=1/eps` and, from `0` to `1`, `r_anchor=1/(2 eps)`.

Every `eps>0` gives a nonsingular `M`, yet the anchor remainder diverges as `eps -> 0`.  Therefore the graph-IFT/nonempty-unique theorem cannot by itself produce a numerical P5 anchor budget.  A quantitative lower gain/coercivity field such as `gamma` (or the preconditioner corollary above) is mathematically indispensable.

## 7. Exact source packet needed for a real P5 instance

The smallest source-side extension is now concrete:

1. same source key / cell hash / coefficient digest already used by `M,DM,R,DR`;
2. physical `D2M,D2R` derivative identities, or an equivalent exact evaluator for `J2`;
3. same-cell graph totality/regularity sufficient for `C^2` along the physical segment;
4. a uniform quantitative lower-gain witness `gamma>0`, **or** preconditioner fields `(X,kappa,chi)` supporting the corollary;
5. a certified correlated bound `Q_R(J2)<=H2` (preferably `<=K2*Q_Z(delta)^2`);
6. an exact anchor-to-cell displacement cap `Q_Z(delta)<=S` and proof that every physical segment remains in the certified cell/neighborhood;
7. downstream acceleration/normalization metric identity for `Q_A` and the actual consumer of `D_anchor`.

The existing exact first-jet extraction is therefore enough to identify the missing mathematical object, but not enough to instantiate the finite anchor budget numerically.  No synthetic `K2`, `gamma`, `chi`, or `D_anchor` should be filled in.

## 8. Minimal Lean theorem decomposition

Recommended order, keeping source algebra separate from analysis:

```lean
-- Pure quadratic/integral leaf.
theorem quadratic_kernel_remainder_four_mul_le ... :
  4 * gamma * Q r <= H2

-- Algebraic implicit-jet leaf; no inverse.
theorem implicit_graph_second_jet ... :
  M (a'') = D2R δ δ - D2M δq δq a - 2 • DM δq (a')

-- Lower-gain transport.
theorem second_jet_energy_le_of_lower_gain ... :
  gamma * QA (a'') <= H2

-- Final finite anchor theorem.
theorem same_cell_graph_affine_anchor_budget ... :
  QA (alpha z1 - alpha z0 - Dalpha z0 δ) <= Danchor

-- Optional source-friendly preconditioner leaf.
theorem lower_gain_sq_of_approx_left_inverse ... :
  (1-kappa)^2 * QA v <= chi * QR (M v)
```

The first and last leaves can be proved independently of the DH source.  The second/source-specialized leaf should wait until the actual second derivative evaluator and pullback conventions are frozen.

## 9. Status / non-claims

Mathematical child: **CONDITIONAL_PASS**.

This review does not claim: actual `D2M/D2R`, a real numeric `H2/K2`, a real lower-gain `gamma/chi`, graph source binding, whole-cell segment coverage, actual P5 normalization identity, runtime/Float64/FD equivalence, Lean compilation, kernel proof, validator acceptance, admission, or registry promotion.

It does close the theorem-design question of how a same-cell exact implicit graph jet can feed a finite anchor budget without explicit inversion or radicals, and it identifies exactly why first-jet/IFT data alone cannot do so.
