---
kind: review_result
review_id: review-T-P5-195-projected-skew-affine-generator-gate-kuangmanmozun-20260909T2337Z
task_id: T-P5-195-PROJECTED-SKEW-AFFINE-GENERATOR-GATE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T23:37:00Z
claim_commit: e98ddd132502203e35072658dd8b152bc57c2154
inspected_commit: ec13d69d59d1008c90a75e7bbf74423013631c8e
upstream_commits:
  - 86d3e6a59cf11c4d1bd28ffa5a6ab7a66cd20eda  # T-P5-192 selector-cone Lyapunov margin
  - f6a493131c273ba0739ede6c2f7a986b71660ae1  # T-P5-194 correlated-zonotope defect adapter
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_projected_skew_gate; add_span_restricted_gate; reuse_polyhedral_latent_sign_fan_when_gate_passes; preserve_semialgebraic_fallback_when_gate_fails
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic-form algebra, span restriction, sign-fan expansion, exact rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-195 — projected-skew gate for affine state-rotating zonotope generators

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-194 closes the correlation-preserving defect adapter for a fixed generator matrix `Z` and affine nonnegative amplitudes. Its selector branch relies on the fact that, for a frozen-selector gradient `G e`, each projected generator scalar is linear:

`z_k^T G e`.

The remaining question is what survives if the generator direction itself moves with state.

This review proves a sharp algebraic gate for the affine model

`z_k(e) = z_k^0 + R_k e`.

For a selector gradient `G e`, define

`phi_k(e) := z_k(e)^T G e`.

Then

**`phi_k(e) = (z_k^0)^T G e + e^T R_k^T G e`.**

The quadratic term disappears on a linear span `L=range(U)` exactly when

**`U^T (R_k^T G + G^T R_k) U = 0`.**

Equivalently, the restriction of `R_k^T G` to the consumed span is skew in quadratic-form sense. Under this gate, `phi_k` is linear on the whole selector span, so the T-P5-194 latent sign fan remains a finite **polyhedral cone fan**, and affine amplitudes still produce only a quadratic-plus-linear robust defect. The existing T-P5-192 copositivity/linear pullback therefore applies without introducing cubic or semialgebraic obligations.

If the gate fails, the old polyhedral-cone checker is not generically sound as a complete sign decomposition. A two-dimensional exact rational example gives

`phi(x,y)=x^2-y`,

whose sign changes along a single positive ray. Hence no conic sign fan can represent the exact sign pattern. This is a genuine degree barrier, not a source/provenance issue.

The gate is deliberately **sufficient for reuse, not necessary for every special nongeneric case**: `phi(x,y)=x^2+y^2` has a trivial positive sign despite failing the skew gate. Therefore gate failure must route to a special factorization/sign-definite or semialgebraic branch and must not be labeled mathematical FAIL.

No actual `Z(e)` source extraction, interval soundness, selector coverage, PDE reduction, Lean/kernel proof, independent verification, or admission is claimed.

---

## 1. Setup

Fix one T-P5-192 selector cone `C` in external state space `R^p`. Let its linear span be

`L := span(C)`.

Choose any full-column-rank matrix

`U in R^(p x r)`

with

`range(U)=L`.

The selector frozen gradient is

`w(e)=G e`.

For each latent zonotope generator `k`, assume an affine state-dependent direction

`z_k(e)=z_k^0+R_k e`,

with `z_k^0 in R^p` and `R_k in R^(p x p)`.

As in T-P5-194, let the latent amplitude be nonnegative and affine on the consumed domain:

`a_k(e)=h_k^T e+h0_k >= 0`.

At a fixed state `e`, the zonotope support identity itself remains valid pointwise:

`sup_(|xi_k|<=1) sum_k xi_k a_k(e) z_k(e)^T G e`

`= sum_k a_k(e) |z_k(e)^T G e|`.

The issue is not the support identity. The issue is the geometry and polynomial degree of the signs of the projected scalars.

---

## 2. T195-A — exact projected affine-generator expansion

For one generator, suppress `k` and write

`z(e)=z0+R e`.

Then

`phi(e)=z(e)^T G e`

`=(z0+R e)^T G e`

`=z0^T G e + e^T R^T G e`.

Define

`A := R^T G`.

Since a scalar quadratic form sees only the symmetric part,

`e^T A e = (1/2) e^T (A+A^T)e`.

Thus the only obstruction to the old linear sign fan is the symmetric part of `R^T G` on the consumed state span.

---

## 3. T195-B — full-space projected-skew iff theorem

### Theorem

The following are equivalent:

1. `e^T R^T G e = 0` for every `e in R^p`;
2. `R^T G + G^T R = 0`;
3. `phi(e)` is linear in `e` on all of `R^p`.

When these hold,

`phi(e)=(G^T z0)^T e`.

### Proof

`(2) -> (1)` is immediate because `R^T G` is skew-symmetric and every real skew-symmetric quadratic form vanishes.

`(1) -> (2)`: let

`S=(R^T G+G^T R)/2`.

Then `S=S^T` and `e^T S e=0` for every `e`. Taking `e=e_i` gives every diagonal entry `S_ii=0`. Taking `e=e_i+e_j` then gives `2 S_ij=0`. Hence `S=0`.

`(1) <-> (3)`: the expansion is a linear term plus a homogeneous quadratic term. If the whole expression is linear, the homogeneous degree-two term must vanish. Explicitly, if `q(e)=e^T R^T G e` were also linear, then for every scalar `t`, homogeneity gives both `q(te)=t^2 q(e)` and `q(te)=t q(e)`; taking any `t notin {0,1}` forces `q(e)=0`.

This is an exact algebraic equivalence, not a norm estimate.

---

## 4. T195-C — span-restricted gate

The full-space gate can be unnecessarily strong because a selector cone may live in a proper subspace.

Write every state in the selector span as

`e=U eta`.

Then

`e^T R^T G e = eta^T U^T R^T G U eta`.

Therefore the quadratic term vanishes for every `e in L` iff

**`U^T (R^T G+G^T R) U = 0`.**

This is the exact span-restricted projected-skew gate.

It is basis-independent. If `U2=U T` with `T` invertible, then

`U2^T (R^T G+G^T R) U2`

`=T^T [U^T (R^T G+G^T R)U] T`,

so vanishing does not depend on the chosen basis.

### Practical consequence

A source packet does not need to prove a global skew identity. It only needs to prove the rational matrix equality on the span of the actual selector cone being consumed.

For a full-dimensional selector cone one may take `U=I`, recovering the global condition.

---

## 5. T195-D — exact polyhedral latent sign fan under the gate

Assume the span-restricted gate holds for every active latent generator `k`.

Define

`ell_k := G^T z_k^0`.

Then for every `e in C`,

`phi_k(e)=ell_k^T e`.

For a sign vector

`sigma in {+1,-1}^m`,

define the sign cell

`C_sigma := C intersect {e : sigma_k ell_k^T e >= 0 for all k}`.

Because `C` is polyhedral conic and every new inequality is homogeneous linear, each `C_sigma` is again a polyhedral cone. Empty cells may be discarded.

On `C_sigma`,

`|phi_k(e)| = sigma_k ell_k^T e`,

so the exact worst zonotope contribution is

`Delta_sigma(e)`

`= sum_k (h_k^T e+h0_k) sigma_k ell_k^T e`.

Define

`Q_sigma := (1/2) sum_k sigma_k (h_k ell_k^T + ell_k h_k^T)`,

`r_sigma := sum_k sigma_k h0_k ell_k`.

Then exactly

**`Delta_sigma(e)=e^T Q_sigma e+r_sigma^T e`.**

Thus affine state rotation satisfying the projected-skew gate costs **no increase in polynomial degree** relative to T-P5-194.

---

## 6. T195-E — direct reuse of the T-P5-192 margin packet

Suppose a T-P5-192 selector branch has base seam-safe derivative bound

`D^+ Phi(e) <= e^T L e + 2 c^T G e`

before the zonotope defect is added.

The zonotope perturbation enters with the standard frozen-gradient factor `2`, hence on `C_sigma`,

`D^+ Phi(e)`

`<= e^T (L+2Q_sigma)e + 2 (G^T c+r_sigma)^T e`.

For target decay rate `gamma>=0` and branch energy matrix `Q_alpha`, it is enough to check

`e^T [L+2Q_sigma+2 gamma Q_alpha] e <= 0`

and

`(G^T c+r_sigma)^T e <= 0`

for all `e in C_sigma`.

If

`C_sigma=cone(V_sigma)`,

these are exactly the old finite algebraic gates:

**quadratic gate**

`-V_sigma^T [L+2Q_sigma+2 gamma Q_alpha] V_sigma` is copositive;

**linear gate**

`V_sigma^T (G^T c+r_sigma) <= 0` entrywise.

Therefore no new nonlinear positivity engine is needed when the projected-skew gate passes.

---

## 7. T195-F — rational exactness of the gate

If `U,R_k,G` are rational matrices, the span gate

`U^T (R_k^T G+G^T R_k) U = 0`

is a finite set of exact rational equalities.

Likewise `ell_k=G^T z_k^0`, the sign-cell inequalities, `Q_sigma`, and `r_sigma` are rational whenever the input packet is rational.

Hence a checker can use the order:

1. compute an exact rational basis `U` for the selector-cone span;
2. test the projected-skew matrices exactly;
3. if all vanish, construct the same finite linear sign fan as T-P5-194;
4. run the existing rational cone/copositivity and linear-sign gates.

No eigenvectors, square roots, floating sign sampling, or polynomial root isolation is introduced by this branch.

---

## 8. T195-G — decisive curved-boundary counterexample when the gate fails

Take

`p=2`, `G=I`, `m=1`, constant amplitude `a(e)=1`,

`z0=(0,-1)^T`,

`R=[[1,0],[0,0]]`.

Then

`z(x,y)=(x,-1)`,

and

`phi(x,y)=z(x,y)^T(x,y)=x^2-y`.

The symmetric projected matrix is nonzero:

`R^T G+G^T R=2R != 0`.

On the positive quadrant, consider the single ray

`e(t)=t(1,2)`, `t>0`.

Then

`phi(e(t))=t^2-2t=t(t-2)`.

So

- `phi<0` for `0<t<2`;
- `phi=0` at `t=2`;
- `phi>0` for `t>2`.

### Consequence

No sign-constant **conic** fan can represent this exact sign pattern on the whole positive quadrant. Any cone containing one positive multiple of `(1,2)` contains all positive multiples of that same ray, but the sign changes along the ray.

The zero set `y=x^2` is also genuinely curved, so an exact finite union of ordinary polyhedral cells cannot reproduce the full boundary either: the boundary of a finite polyhedral union lies in a finite union of affine lines, whereas the parabola contains no nontrivial segment of a line and has infinitely many tangent/slope directions.

Thus the failure mode is genuinely semialgebraic, not merely “more sign sectors”.

---

## 9. Gate failure is NOT a mathematical FAIL

The projected-skew condition is exact for **degree preservation**, but it is not necessary for every special state-rotating generator to admit a simple sign treatment.

Take

`z0=0`, `R=I`, `G=I`.

Then

`phi(e)=e^T e=||e||^2 >= 0`

for every state, while

`R^T G+G^T R=2I !=0`.

No sign partition is needed at all.

A second special case is a factorable quadratic such as

`phi(x,y)=x^2-y^2=(x-y)(x+y)`;

on the positive quadrant its sign boundary reduces to the single linear ray `x=y` even though the quadratic part is nonzero.

Therefore the correct checker semantics are:

- projected-skew PASS -> reuse T-P5-194 polyhedral sign-fan / T-P5-192 copositivity route;
- projected-skew FAIL -> `PROJECTED_SKEW_GATE_NOT_APPLICABLE`;
- only a separate sign-definite/factorization or semialgebraic theorem may continue from there.

Do not turn gate failure into a source or mathematical counterexample.

---

## 10. Distinction from the viability branch

For completeness, state-dependent generators behave differently against a **fixed facet normal** `n`.

There

`n^T z_k(e)=n^T z_k^0+(R_k^T n)^T e`,

which is affine regardless of the projected-skew gate.

Hence the normal sign partition can still be made by finite polyhedral affine cells. However, multiplying that affine projection by affine amplitude `a_k(e)` produces a quadratic face condition, so the linear T-P5-191 Metzler lift no longer applies directly.

Thus:

- the present projected-skew theorem specifically preserves the **selector-Lyapunov** quadratic/copositive route;
- the state-rotating **viability** route remains a separate quadratic-on-faces closure problem.

This prevents the selector result from being overclaimed as a full replacement for T-P5-194's fixed-`Z` viability theorem.

---

## 11. Minimal formal theorem statements

Suggested source-independent leaves:

1. `quadForm_vanish_iff_sym_eq_zero`
   - for a square real matrix `A`, `forall x, x^T A x=0` iff `A+A^T=0`.

2. `quadForm_vanish_on_span_iff_restricted_sym_eq_zero`
   - for basis matrix `U`, `forall eta, (U eta)^T A (U eta)=0` iff `U^T(A+A^T)U=0`.

3. `affineGenerator_projected_linear_of_restrictedSkew`
   - if the restricted gate holds for `R^T G`, then on `range(U)`, `(z0+R e)^T G e=(G^T z0)^T e`.

4. `affineGeneratorZonotope_signSector_expansion`
   - under all projected-skew gates and `a_k(e)>=0`, the support on one sign sector is `e^T Q_sigma e+r_sigma^T e`.

5. `affineGeneratorZonotope_selectorDecay_pullback`
   - combine the previous expansion with the T-P5-192 base derivative packet and finite cone generators.

The first three are linear algebra; the sector expansion is finite-sum/ring algebra. The final theorem should reuse the existing copositivity consumer rather than reimplement it.

---

## 12. What this closes

For the selector-Lyapunov branch, the exact state-rotating path is now:

`z_k(e)=z_k^0+R_k e`

`-> test U^T(R_k^T G+G^T R_k)U=0`

`-> phi_k(e)=ell_k^T e on the selector span`

`-> finite polyhedral latent sign fan`

`-> affine amplitude times linear signed projection`

`-> exact quadratic + linear defect`

`-> existing T-P5-192 copositivity + linear gates`.

This identifies a nontrivial class of genuinely moving generator directions that are **invisible to the selector quadratic form** and therefore cost no checker complexity.

---

## 13. Remaining open boundaries

This result does not close:

1. actual same-key extraction of `z_k^0,R_k` from the deployed residual producer;
2. proof that the real residual lies in the state-dependent zonotope on the full cell/tube;
3. outward-rounded validity and nonnegativity of `a_k(e)`;
4. actual selector-cone spans `U` and their physical cover;
5. special nongeneric rescue when the projected-skew gate fails but the quadratic is sign-definite or factorable;
6. generic curved semialgebraic sign cells and positivity of the resulting cubic robust defect;
7. state-dependent selector gradient beyond the linear `G e` contract;
8. the separate state-rotating viability quadratic-on-faces problem;
9. Float64/controller/FD semantics, PDE unresolved-mode reduction, P8/M4 physical coverage, Lean/kernel compilation, independent verification by 封不觉, admission, or registry promotion.

The smallest useful next mathematical child is a **sign-definite quadratic rescue gate** for failed projected-skew sectors: certify `phi_k(e)>=0` or `<=0` on a polyhedral selector cone by the already-developed copositivity machinery, thereby avoiding a semialgebraic split whenever the quadratic projection has fixed sign.