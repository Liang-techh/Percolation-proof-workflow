---
kind: review_result
review_id: review-T-P5-231-anisotropic-kernel-fiber-scaling-bridge-liuguanyi-20260910T0903Z
task_id: T-P5-231-ANISOTROPIC-KERNEL-FIBER-SCALING-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T09:03:00Z
claim_commit: aaae3685d5dcf114539640a1685275e310215781
inspected_commit: 54466e6b4a03cb9a4f0d289dcd733e9065e46b9f
upstream_commits:
  - 95fc7a17795dda55ed0f493d5588c573ef84151d  # T-P5-230 ellipsoid trust-region / semidefinite curvature
  - 575e296e13600ee0aa7b043dde8dd3b0f97b2ca1  # T-P5-229 bounded flat-fiber support
  - 6a10ef29433a4dd050d593d8053383f4ba7fd204  # T-P5-226 higher-corank Schur/range gate
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_semidefinite_curvature_kernel_support_decomposition; add_anisotropic_support_exponent_threshold; add_product_fiber_exact_classifier; preserve_source_dilation_under_coordinate_transport
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic/support-function mathematics only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-231 — anisotropically shrinking kernel-fiber scaling bridge

## 0. Verdict and mathematical seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-230 isolated the correct near-origin dichotomy for a semidefinite pure-gauge curvature block `H>=0`:

- forcing in `range(H)` is Schur-completable and stays quadratic order;
- forcing seen by `ker(H)` behaves like a flat fiber and, at fixed radius, leaks at first order.

Its explicit next seam was the anisotropically shrinking kernel fiber. This child closes that seam at the mathematical level.

The key result is an exact decomposition. For

`q_t(alpha) = t^2 c + 2 t b^T alpha - alpha^T H alpha`,

split the admissible gauge fiber into a curved component in `range(H)` and a shrinking flat component in `ker(H)`. Once the curved Schur center is admissible,

**`sup q_t = t^2 A + 2 t h_{K_N(t)}(b_N)`**,

where `A` is the already-absorbed quadratic coefficient and `h_{K_N(t)}` is the support function of the actual kernel fiber.

Therefore the only quantity controlling the remaining asymptotic obstruction is the support exponent of the kernel fiber. If

`h_{K_N(t)}(b_N) ~ L t^p`, `L>0`,

then the unresolved cross leakage has order

**`t^(1+p)`**.

The sharp threshold against a finite quadratic Lyapunov margin is therefore

**`p=1`.**

- `p<1`: unavoidable subquadratic leakage, hence small-amplitude FAIL;
- `p=1`: leakage competes exactly with the quadratic margin;
- `p>1`: leakage is higher order and is absorbable whenever the quadratic margin is strictly negative.

This simultaneously recovers T-P5-230 fixed-radius kernel obstruction (`p=0`) and T-P5-229 linear radius/amplitude scaling (`p=1`).

No actual P5 fiber identity, source chart, trajectory/cell coverage, Float64 enclosure, Lean/kernel receipt, independent validation, admission, registry promotion, or parent closure is claimed.

---

## 1. Semidefinite curvature setup

Let `E` be a finite-dimensional real inner-product space and let

`H : E -> E`

be symmetric positive semidefinite.

Write

`R := range(H)`,

`N := ker(H)`.

Because `H` is symmetric,

`E = R orthogonal_sum N`.

Decompose the cross vector

`b = b_R + b_N`,

with `b_R in R`, `b_N in N`.

Choose `x in R` solving

`H x = b_R`.

This `x` is unique inside `R`, because `H|_R` is positive definite.

For physical amplitude `t>0`, consider

`q_t(alpha) := t^2 c + 2 t <b,alpha> - <alpha,H alpha>`.

Assume the admissible gauge fiber has product/direct-sum form

`F_t = U_t + K_N(t)`,

where

- `U_t subset R`,
- `K_N(t) subset N`,
- each `alpha in F_t` is represented as `u+z`, `u in U_t`, `z in K_N(t)`.

The product assumption is a real mathematical premise. A coupled source fiber must not be silently replaced by this equality; outer and inner approximations have different PASS/FAIL semantics, recorded below.

---

## 2. Exact curved-range plus kernel-support decomposition

### Theorem A — `semidefinite_curvature_kernel_support_decomposition`

For every `u in R`, `z in N`,

`q_t(u+z)`

`= t^2 c + 2t <b_R,u> - <u,H u> + 2t <b_N,z>`.

Moreover,

`2t <b_R,u> - <u,H u>`

`= t^2 <b_R,x> - <u-tx, H(u-tx)>`.

Therefore for every `U_t subset R`,

`sup_{u in U_t} [2t<b_R,u>-<u,Hu>] <= t^2 <b_R,x>`.

If the Schur center is admissible,

**`t x in U_t`,**

then equality holds.

Consequently, if `tx in U_t`,

**`Theta(t) := sup_{alpha in F_t} q_t(alpha)`**

satisfies the exact identity

**`Theta(t) = t^2 A + 2t h_{K_N(t)}(b_N)`,**

where

`A := c + <b_R,x> = c + <x,Hx>`,

and

`h_K(v) := sup_{z in K} <v,z>`.

### Proof

Since `Hz=0`, symmetry gives

`<u,Hz>=<Hu,z>=0`,

and `b_R orthogonal N`, `b_N orthogonal R`. Hence all curved/kernel cross terms vanish and the first displayed decomposition follows.

Because `Hx=b_R`,

`<u-tx,H(u-tx)>`

`= <u,Hu> - 2t<b_R,u> + t^2<x,Hx>`.

Rearranging proves the completion formula. The quadratic remainder is nonnegative because `H>=0`, so the curved term is at most `t^2<b_R,x>` and reaches it at `u=tx`. The remaining maximization over `z` is exactly the support function. QED.

### Important implementation consequence

The semidefinite problem does **not** require a pseudoinverse. A producer may supply an exact solve packet

`Hx=b_R`, `b_N=b-Hx`, `H b_N=0`,

plus a proof that the chosen `x` lies in the curved complement and that `tx` is source-admissible. In rational data, this can be checked by exact linear algebra / the same range machinery already used around T-P5-226.

---

## 3. General support-exponent theorem

The exact identity from Theorem A reduces all remaining near-origin geometry to one scalar support law.

### Theorem B — `kernel_support_exponent_threshold`

Assume the hypotheses of Theorem A and suppose for some finite `p>=0` and `L>0`,

`h_{K_N(t)}(b_N) = L t^p + o(t^p)`

as `t -> 0+`.

Then

**`Theta(t) = A t^2 + 2 L t^(1+p) + o(t^(1+p))`.**

Hence:

#### B1. Sublinear shrink: `p<1`

`1+p<2`, so the positive kernel-support term dominates every finite quadratic coefficient `A`.

Therefore

**`Theta(t)>0` for all sufficiently small `t>0`.**

Uniform nonpositivity is mathematically impossible.

#### B2. Linear shrink: `p=1`

`Theta(t)/t^2 -> A+2L`.

Therefore:

- if `A+2L<0`, the gate is safe for all sufficiently small `t`;
- if `A+2L>0`, the gate fails for all sufficiently small `t`;
- if `A+2L=0`, leading order alone is insufficient and the next support order must be inspected unless a stronger exact product formula is available.

#### B3. Superlinear shrink: `p>1`

`Theta(t)/t^2 -> A`.

Therefore:

- if `A<0`, the kernel leakage is asymptotically absorbable;
- if `A>0`, the quadratic base already fails;
- if `A=0` and the kernel support is genuinely positive for every small `t`, then `Theta(t)>0`: a zero quadratic reserve cannot pay even a higher-order positive debit.

### Structural reading

The exponent threshold is not `bounded` versus `unbounded`, and not even `flat` versus `curved`. The source-level discriminator is

**`kernel support radius / physical amplitude`.**

The critical scaling is linear in physical amplitude.

---

## 4. Anisotropic dilation computes the exponent exactly

The preceding theorem only assumes a support asymptotic. Now derive that asymptotic from a typed anisotropic source chart.

Let the flat kernel split orthogonally as

`N = N_1 orthogonal_sum ... orthogonal_sum N_m`,

with orthogonal projections `P_a` and source-supplied exponents

`p_a >= 0`.

Define the dilation

**`D_t := sum_a t^(p_a) P_a`.**

Let `Z subset N` be compact, convex, and contain a relative neighborhood of `0` in `N`. Define

**`K_N(t) := D_t Z`.**

Decompose

`b_N = sum_a b_a`, `b_a=P_a b_N`.

Because `D_t` is self-adjoint,

**`h_{K_N(t)}(b_N) = h_Z(D_t b_N)`.**

If `b_N !=0`, set

`p_* := min { p_a : b_a !=0 }`,

`b_* := sum_{a:p_a=p_*} b_a`.

Then

`D_t b_N = t^(p_*) [ b_* + sum_{p_a>p_*} t^(p_a-p_*) b_a ]`.

The support function of a compact set is continuous and positively homogeneous, so

**`h_{K_N(t)}(b_N)`**

**`= t^(p_*) ( h_Z(b_*) + o(1) )`.**

Since `Z` contains a relative neighborhood of zero and `b_* !=0`,

`h_Z(b_*)>0`.

Thus the support exponent in Theorem B is exactly

**`p=p_*`.**

### Theorem C — anisotropic threshold

Under the above dilation model, the earliest shrinking kernel block actually seen by the cross vector controls the Lyapunov order:

**`leakage order = 1 + min{p_a : P_a b_N !=0}`.**

So:

- an active block with `p_a<1` gives an unavoidable small-amplitude obstruction;
- active blocks with `p_a=1` consume quadratic margin;
- blocks with `p_a>1` are higher order and only need a strict quadratic reserve.

This is the requested unification of T229 and T230.

---

## 5. Product fibers give a complete exact classifier

For a stronger source contract, suppose

`Z = Z_1 + ... + Z_m`

with independent direct-product factors `Z_a subset N_a` (every choice of `z_a in Z_a` is jointly admissible). Define

`s_a := h_{Z_a}(b_a) >=0`.

Then support additivity on the product gives the **exact**, not merely asymptotic, formula

**`h_{K_N(t)}(b_N) = sum_a s_a t^(p_a)`.**

Hence

**`Theta(t) = A t^2 + 2 sum_a s_a t^(1+p_a)`.**

This yields a complete small-`t` decision rule.

### Theorem D — `product_anisotropic_kernel_exact_classifier`

Assume every active factor has `s_a>0`.

1. If any active `p_a<1`, uniform nonpositivity fails near zero.
2. Otherwise define the effective quadratic coefficient

   **`A_eff := A + 2 sum_{p_a=1} s_a`.**

3. If `A_eff<0`, the inequality is safe for all sufficiently small `t`.
4. If `A_eff>0`, it fails for all sufficiently small `t`.
5. If `A_eff=0`, then:
   - if any active `p_a>1`, the remaining positive higher-order term makes `Theta(t)>0` for every `t>0`;
   - if no such active factor exists, `Theta(t)=0` exactly.

Thus the product case has no unresolved asymptotic boundary.

### Weighted-box specialization

If each kernel block is one-dimensional,

`Z_j=[-rho_j,rho_j] e_j`,

then

`s_j = rho_j |(b_N)_j|`,

and

**`Theta(t) = A t^2 + 2 sum_j rho_j |(b_N)_j| t^(1+p_j)`.**

This is a directly checkable source-to-math packet with no optimization solver.

---

## 6. Exact coordinate-transport law

The exponents above belong to the **source dilation**, not to arbitrary coordinate names.

Let `S:N'->N` be invertible and change kernel coordinates by `z=S z'`. Transport all data:

`Z' := S^{-1} Z`,

`D'_t := S^{-1} D_t S`,

`b'_N := S^T b_N`.

Then

`D_t'^T b'_N = S^T D_t^T b_N`,

and therefore

**`h_{Z'}(D_t'^T b'_N) = h_Z(D_t^T b_N)`.**

So the physical support law and its critical exponent are invariant under exact coordinate transport.

### Warning

It is unsafe to mix kernel coordinates and then continue treating the old per-axis radii/exponents as independent. A coordinate change must conjugate the dilation and transform the base fiber simultaneously. Otherwise one can manufacture a false exponent and therefore a false PASS/FAIL near the origin.

Allowed simplification without changing the diagonal exponent chart is blockwise mixing **inside equal-exponent groups**. Mixing distinct exponent groups is valid only if the full conjugated `D'_t` is retained.

---

## 7. Source outer/inner semantics

This distinction is essential for honest repository routing.

### Outer product envelope

If the actual source fiber satisfies only

`F_t^actual subseteq U_t + K_N(t)`,

then Theorem A gives a safe **upper bound** on the actual supremum.

Therefore a nonpositive outer-envelope bound is a valid PASS route.

But a positive outer-envelope supremum is **not** a mathematical FAIL: the maximizing kernel displacement may be spurious.

### Inner product witness

If instead a source-proved product set satisfies

`U_t + K_N(t) subseteq F_t^actual`,

then any positive value constructed inside that product is a genuine physical obstruction.

In particular, the `p<1` failure theorem requires either exact fiber equality or an inner source witness carrying the corresponding active kernel displacement. An outer radius alone cannot justify FAIL.

### Coupled fibers

If kernel radius depends on the curved coordinate `u`, the exact factorization need not hold. The correct object is then the conditional support

`h_{K_N(t,u)}(b_N)`

inside the remaining maximization over `u`. Replacing it by a uniform outer support is safe for PASS but may be conservative for FAIL.

---

## 8. Exact regressions

### Regression R1 — fixed kernel radius recovers T230 obstruction

Take

`H=diag(1,0)`, `b=(1,1)`, `c=-3`,

with curved center admissible and kernel fiber `[-1,1]e_2`.

Here `x=e_1`, so

`A=c+x^THx=-2`.

The kernel exponent is `p=0`, hence

`Theta(t)=-2t^2+2t`.

Thus `Theta(t)>0` for every `0<t<1` despite the negative quadratic reserve. This is exactly T-P5-230's fixed-radius flat-kernel leakage.

### Regression R2 — linear collapse competes at quadratic order

Keep `H=diag(1,0)`, `b=(1,1)`, but take `c=-4`, so `A=-3`, and let

`K_N(t)=[-t,t]e_2`.

Then

`Theta(t)=-3t^2+2t^2=-t^2<=0`.

The nonzero kernel cross term is now safe because the fiber collapses linearly.

If instead `c=-2`, then `A=-1` and

`Theta(t)=t^2>0`.

So `p=1` is not automatically safe; it consumes the same quadratic budget as the nominal Lyapunov term.

### Regression R3 — superlinear collapse is higher order

Take again `H=diag(1,0)`, `b=(1,1)`, `c=-2`, so `A=-1`, but now

`K_N(t)=[-t^2,t^2]e_2`.

Then

`Theta(t)=-t^2+2t^3<=0`

for `0<t<=1/2`.

Thus a nonzero flat-kernel cross term need not be radical when the actual source fiber collapses faster than linearly.

### Regression R4 — one slow anisotropic axis dominates arbitrarily large quadratic margin

Take

`H=diag(1,0,0)`, `b=(1,1,1)`, `c=-101`,

so `A=-100`.

Let the kernel box have radii

`|alpha_2|<=t^(1/2)`,

`|alpha_3|<=t^2`.

Then

`Theta(t)=-100t^2+2t^(3/2)+2t^3`.

The `p=1/2` axis forces `Theta(t)>0` for all sufficiently small `t`, no matter how large the finite coefficient `-100` is. The earliest active exponent controls the obstruction.

---

## 9. Relation to T-P5-229, T-P5-230, and T-P5-226

### T-P5-230 recovered

A fixed full-dimensional kernel neighborhood corresponds to `p=0`. If `b_N!=0`, the support term is `Theta(t)~2L t`, so uniform quadratic-order safety is impossible. Hence T230's necessary range gate

`b in range(H)`

is exactly the `p=0` special case.

### T-P5-229 recovered

If `H=0`, every gauge direction is kernel-flat. If the whole bounded fiber scales linearly,

`K(t)=t Z`,

then

`sup q_t = t^2 [c+2h_Z(b)]`.

This is precisely the radius/amplitude threshold: a linearly shrinking flat fiber contributes at quadratic order rather than first order.

### T-P5-226 relation

The equation

`Hx=b_R`

is the vector version of the signed-lineality range condition. T231 says what happens to the leftover kernel forcing when the lineality is not actually free but source-bounded with a known amplitude law: it need not vanish identically if its admissible support shrinks sufficiently fast.

So `range(B) subseteq range(P)` remains necessary for genuinely free/fixed-radius signed directions, but a state-dependent shrinking source fiber can replace exact radicality by a quantified support-exponent contract.

---

## 10. Minimal theorem statements for formalization

### Candidate theorem 1 — `semidefinite_curved_kernel_support_exact`

Assume:

- `H=H^T>=0`;
- `E=range(H) orthogonal_sum ker(H)`;
- `b=b_R+b_N` accordingly;
- `Hx=b_R`;
- `F_t=U_t+K_t`, `U_t subset range(H)`, `K_t subset ker(H)`;
- `tx in U_t`.

Then

`sup_{alpha in F_t} [t^2c+2t b^Talpha-alpha^THalpha]`

`= t^2(c+b_R^Tx)+2t h_{K_t}(b_N)`.

### Candidate theorem 2 — `kernel_support_power_threshold`

If additionally

`h_{K_t}(b_N)=L t^p+o(t^p)`, `L>0`,

then

`Theta(t)=A t^2+2L t^(1+p)+o(t^(1+p))`,

with the sharp `p<1`, `p=1`, `p>1` classification above.

### Candidate theorem 3 — `anisotropic_dilation_support_asymptotic`

For

`D_t=sum_a t^(p_a)P_a`, `K_t=D_tZ`,

with compact `Z` containing a neighborhood of zero,

`p_*=min{p_a:P_ab_N!=0}`

implies

`t^(-p_*) h_{K_t}(b_N) -> h_Z(sum_{p_a=p_*}P_ab_N)>0`.

### Candidate theorem 4 — `product_anisotropic_support_exact`

For independent factors `Z_a subset N_a`,

`h_{D_t Z}(b_N)=sum_a t^(p_a)h_{Z_a}(P_ab_N)`.

This yields the exact finite classifier of Theorem D.

### Candidate theorem 5 — `kernel_dilation_coordinate_covariance`

For invertible `S`, with

`Z'=S^{-1}Z`, `D'_t=S^{-1}D_tS`, `b'=S^Tb`,

prove

`h_{Z'}(D_t'^T b')=h_Z(D_t^Tb)`.

---

## 11. Suggested exact/rational interface

For a rational source chart, no spectral floating-point decomposition is required. A checker-facing packet can consist of:

- rational symmetric `H>=0` certificate;
- exact kernel basis / range solve packet;
- rational `x` with `Hx=b_R`;
- source dilation blocks and symbolic exponents `p_a`;
- a compact kernel-body support certificate (box formula, polytope LP dual, ellipsoid bound, or exact product factor);
- source proof of equality / outer inclusion / inner inclusion for the admissible fiber;
- center-admissibility inequality for `tx` when exact Schur completion is invoked.

The trusted mathematical leaves are linear algebra, support monotonicity/homogeneity, exponent comparison, and the already-existing support primitives. No pseudoinverse, numerical eigenvector, or generic nonlinear optimizer is intrinsically required by this bridge.

---

## 12. Failure boundaries and OPEN items

This result intentionally does **not** close:

1. actual P5 identification of `H`, `b`, `U_t`, `K_N(t)`, or the physical amplitude `t`;
2. proof that a source fiber really factors as a curved-range product plus kernel fiber;
3. coupled fibers where kernel admissibility depends on the curved coordinate;
4. indefinite pure-gauge curvature (`H` not PSD), which belongs to a stronger trust-region/S-lemma branch;
5. exact contact at the general non-product `p=1`, `A+2L=0` boundary beyond leading support order;
6. source charts whose dilation law is only empirical/Float64 rather than exact or interval-certified;
7. cell/tube/trajectory coverage and PDE/ODE semantics;
8. Lean/kernel proof, independent validation by 封不觉, admission, registry, and P5/P8/M4 parent closure.

A positive supremum from an **outer** fiber envelope remains only an adapter obstruction, never a physical FAIL. Conversely, the `p<1` mathematical FAIL requires an exact or inner source witness showing that the slow-shrinking kernel direction is actually realizable.

---

## 13. New structural fingerprint

The completed fingerprint is

**semidefinite gauge curvature**

`-> split range(H) / ker(H)`

`-> Schur-complete range(H)`

`-> reduce ker(H) to a source support function`

`-> read its amplitude exponent p`

`-> p<1: subquadratic obstruction`

`-> p=1: debit against quadratic Lyapunov margin`

`-> p>1: higher-order perturbation requiring strict quadratic reserve`

`-> preserve the source dilation under coordinate transport`.

This is the exact mathematical bridge between T229 bounded-flat support scaling and T230 curved-range absorption, and it states precisely when a non-radical flat-kernel cross term is genuinely harmless rather than merely hidden by a bounded coordinate chart.
