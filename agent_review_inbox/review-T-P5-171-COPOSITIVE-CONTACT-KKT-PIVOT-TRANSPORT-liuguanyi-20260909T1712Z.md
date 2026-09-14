---
kind: review_result
review_id: review-T-P5-171-copositive-contact-kkt-pivot-transport-liuguanyi-20260909T1712Z
task_id: T-P5-171-COPOSITIVE-CONTACT-KKT-PIVOT-TRANSPORT
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T17:12:00Z
claim_commit: a42898cd998d786f4803c70ab9a978f0839fbee8
inspected_commit: 9c2533146fa4f6992395a43650253bfaf77fe60f
upstream_commits:
  - f1eb76d8657edac28a04aaec289a7198a8c648d1  # T-P5-170 iterated sign-compatible pivot energy chain
  - 300fec2e52d7a3a78107110f25df0ab016dc81d2  # T-P5-169 sharp-floor contact localization
  - 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9  # T-P5-159 symbolic floor/contact bracketing
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: expose_zero_contact_to_orthant_complementarity_as_the_support_bridge; transport_terminal_gradient_exactly_through_T170_backward_lifts; reuse_lifted_support_as_principal_kernel/root_witness_instead_of_resolving_original_KKT; keep_strict_complementarity_and_symbolic_D_chain_as_separate_open_obligations
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional ordered-field/real quadratic algebra; SymPy exact regression only for the displayed 4x4 example
exit_code: 0 for local symbolic regression; no Lean/kernel run
---

# T-P5-171 — copositive zero-contact KKT/complementarity transport through pivot reduction

## 0. Verdict and narrow seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-170 already proves that a sign-compatible scaled-Schur chain is an exact copositivity reduction, gives a nested energy decomposition, and lifts a terminal FAIL or zero-contact witness backward without division. T-P5-159/T-P5-169, on the other hand, use a sharper support statement at a floor contact: on the positive support one wants a principal zero mode / KKT contact so determinant-root and active-support reasoning can proceed.

The missing bridge is therefore not another copositivity test. It is the exact relationship between

- a terminal cone zero contact,
- the terminal gradient / orthant complementarity conditions,
- the T-P5-170 backward state lift,
- and the original principal-support kernel.

This review proves that relationship exactly. The key identity is stronger than the quadratic lift:

`M * L(z) = pad_0(S*z)`.

Thus a pivot lift scales the **state**, but it does **not** scale the surviving gradient residual. Iterating gives an exact zero-padding transport of the terminal gradient to the original coordinates. As a consequence, a terminal zero contact of a certified copositive core yields an explicit original orthant-KKT contact and a positive kernel vector for the lifted principal support, with no new KKT solve.

No provenance/receipt/admission work, runtime/Float64 claim, Lean/kernel validation, independent re-audit, registry mutation, or source/coverage promotion is performed.

---

## 1. Cone contact implies orthant complementarity

Let `M=M^T` be a finite real symmetric matrix. Write

`q_M(x)=x^T M x`.

Assume `M` is copositive:

`x>=0  =>  q_M(x)>=0`.

Let `z>=0` be nonzero and satisfy

**(1.1)** `q_M(z)=0`.

Define the gradient-half vector

`g := M z`.

(The gradient of `q_M` is `2Mz`; the factor `2` is irrelevant here.)

### Theorem T171-A — `copositive_zero_contact_is_orthant_complementary`

Under the assumptions above,

**(1.2)** `g>=0` coordinatewise,

and

**(1.3)** `z_i g_i = 0` for every coordinate `i`.

Equivalently,

`z>=0`, `Mz>=0`, and `<z,Mz>=0`

hold with coordinatewise complementarity, not merely a zero total dot product.

### Proof of `Mz>=0` without derivatives or division

Copositivity first implies every diagonal entry is nonnegative:

`M_jj=q_M(e_j)>=0`.

Fix a coordinate `j`. Suppose for contradiction that

`g_j=(Mz)_j<0`.

Set

`a := -g_j > 0`,

`m := M_jj >= 0`,

`c := m+1 > 0`.

Consider the nonnegative vector

**(1.4)** `y := c z + a e_j >=0`.

Because `q_M(z)=0` and `g_j=-a`, exact expansion gives

`q_M(y)`
`= c^2 q_M(z) + 2 c a g_j + a^2 m`
`= -2 c a^2 + a^2 m`
`= -a^2(m+2) < 0`.

This contradicts copositivity. Hence `g_j>=0` for every `j`.

### Proof that every active coordinate has zero residual

Now suppose `z_j>0` and, for contradiction,

`g_j>0`.

Again let `m=M_jj>=0`, and define

`c := g_j + m z_j + 1 >0`,

`a := g_j z_j >0`.

Use the downward but still nonnegative test vector

**(1.5)** `y := c z - a e_j`.

For the `j` coordinate,

`y_j=(c-g_j)z_j=(m z_j+1)z_j>=0`,

and every other coordinate is `c z_i>=0`. Thus `y>=0`.

Exact expansion gives

`q_M(y)`
`= c^2 q_M(z) - 2 c a g_j + a^2 m`
`= -2 c g_j^2 z_j + g_j^2 z_j^2 m`
`= -g_j^2 z_j (2 g_j + m z_j + 2) <0`,

again contradicting copositivity. Therefore `z_j>0` forces `g_j=0`.

If `z_j=0`, the product `z_j g_j` is already zero. This proves (1.2)-(1.3). QED.

### Corollary T171-A1 — positive support is a principal kernel support

Let

`S := supp(z) = {i : z_i>0}`.

Then `z_S>0` componentwise and

**(1.6)** `M[S,S] z_S = 0`.

Indeed, for `i in S`, `(Mz)_i=0`, while all coordinates outside `S` have `z_j=0`; therefore the active row equation is exactly the principal equation.

Hence every nonzero copositive zero contact gives a singular principal block:

**(1.7)** `det(M[S,S])=0`.

This is the support/kernel statement needed by the T-P5-159 sharp-floor root machinery.

### Why the global copositivity premise is essential

A zero quadratic value alone does **not** imply complementarity. For example

`M=[[0,-1],[-1,0]]`, `z=(1,0)`

satisfies `z>=0` and `q_M(z)=0`, but

`Mz=(0,-1)`

has a negative inactive residual. The missing premise is exactly the fixed-candidate copositivity PASS.

---

## 2. One sign-compatible pivot transports the full residual vector exactly

Use the T-P5-168/T-P5-170 one-step block convention

`M = [[b, -r^T],`
`     [-r,   A ]]`,

with

**(2.1)** `b>0`,

**(2.2)** `r>=0` componentwise.

Define the scaled reduced matrix

**(2.3)** `S := b A - r r^T`.

For any retained vector `z`, define the T-P5-170 division-free backward lift

**(2.4)**

`L(z) := (r^T z, b z)`

in pivot-first ordering.

T-P5-170 proves the quadratic identity

`q_M(L(z)) = b q_S(z)`.

The stronger interface identity is the following.

### Theorem T171-B — `pivot_lift_mulVec_exact`

For every real retained vector `z`,

**(2.5)**

`M L(z) = (0, S z)`.

### Proof

The pivot component is

`b(r^T z) - r^T(bz) = 0`.

The retained block is

`-r(r^T z) + A(bz)`
`= (bA-r r^T)z`
`= S z`.

QED.

### Important scaling consequence

The state is scaled by `b` on retained coordinates, but the surviving residual is **not** multiplied by `b`:

`state: z -> (r^Tz, b z)`,

`residual: Sz -> (0,Sz)`.

A consumer must not insert a spurious pivot-product factor into the gradient/KKT residual when replaying a T-P5-170 chain.

### Corollary T171-B1 — nonnegative cone/KKT transport

If `z>=0`, then `L(z)>=0` by `b>0` and `r>=0`.

If additionally

`S z>=0`

and

`z_i(Sz)_i=0` for every retained coordinate,

then

**(2.6)** `M L(z)>=0`,

and

**(2.7)** `L(z)_i (M L(z))_i=0` for every original coordinate.

The pivot residual is exactly zero; on retained coordinates the state has only been multiplied by the positive scalar `b`, so complementarity is unchanged.

### Corollary T171-B2 — full kernel transport

If

`S z=0`,

then

**(2.8)** `M L(z)=0`.

Thus a terminal full-kernel vector lifts to a full-kernel vector of the pre-pivot matrix, not merely to a zero-energy vector.

### Corollary T171-B3 — support activity criterion for the pivot

Let `z>=0`. The lifted pivot coordinate is

`s=r^Tz`.

Because both vectors are nonnegative,

**(2.9)**

`s>0`

iff

there exists `i in supp(z)` with `r_i>0`.

Likewise `s=0` iff `r_i=0` on the whole active retained support.

Therefore a pivot enters the lifted positive support exactly when it has at least one strictly negative current coupling to the active future support. No sign cancellation can make the pivot activity ambiguous.

---

## 3. Iterated pivot chain: terminal residual is only zero-padded

Consider a valid T-P5-170 chain

`M_0 -> M_1 -> ... -> M_m`,

where at stage `k`, after placing the chosen pivot first,

`M_k=[[b_k,-r_k^T],[-r_k,A_k]]`,

`b_k>0`, `r_k>=0`, and

`M_{k+1}=b_k A_k-r_k r_k^T`.

Let `E_k` denote the coordinate embedding that inserts a zero residual at the stage-`k` pivot position and restores the current coordinate ordering.

Starting from any terminal vector `z_m`, define the usual backward states

**(3.1)** `z_k := L_k(z_{k+1})`

for `k=m-1,...,0`.

### Theorem T171-C — `iterated_pivot_gradient_zero_padding`

For every terminal vector `z_m`,

**(3.2)**

`M_0 z_0 = E_0 E_1 ... E_{m-1} (M_m z_m)`.

In words: the terminal residual vector is carried back to the original coordinates with zeros inserted at every eliminated pivot, and with **no scalar multiplier**.

### Proof

T171-B at each stage gives

`M_k z_k = E_k(M_{k+1} z_{k+1})`.

Compose the finite identities. QED.

### Corollary T171-C1 — terminal orthant complementarity lifts exactly

Assume

`z_m>=0`,

`M_m z_m>=0`,

and

`z_m,i (M_m z_m)_i=0` for every terminal coordinate.

Then the recursively lifted original vector satisfies

**(3.3)** `z_0>=0`,

**(3.4)** `M_0 z_0>=0`,

**(3.5)** `z_0,i (M_0 z_0)_i=0` for every original coordinate.

All surviving coordinates are multiplied only by products of positive pivots, and all eliminated pivot residuals are zero.

### Corollary T171-C2 — certified terminal zero contact is enough

If the terminal core `M_m` is copositive and

`z_m>=0`, `z_m!=0`, `q_{M_m}(z_m)=0`,

then T171-A first derives terminal orthant complementarity. T171-C1 then gives original orthant complementarity automatically.

Thus a producer does **not** need to separately solve or certify a second KKT system in the original dimension after a successful T-P5-170 reduction.

### Corollary T171-C3 — full terminal kernel lifts to full original kernel

If `M_m z_m=0`, then

**(3.6)** `M_0 z_0=0`.

Again, no pivot-product factor appears in the residual identity.

---

## 4. Principal support/kernel transport after the full chain

Let `z_m` be a nonzero terminal orthant-complementary contact and let `z_0` be its T171-C lift.

Define the lifted positive support

`S_0 := supp(z_0)`.

By complementarity,

`(M_0 z_0)_i=0`

for every `i in S_0`.

All coordinates outside `S_0` have `z_0,j=0`. Therefore

### Theorem T171-D — `lifted_contact_principal_kernel`

**(4.1)**

`M_0[S_0,S_0] (z_0)_{S_0}=0`,

with

**(4.2)** `(z_0)_{S_0}>0` componentwise.

Consequently

**(4.3)** `det(M_0[S_0,S_0])=0`.

This is exactly the original-coordinate active-support kernel witness that T-P5-159 obtains abstractly from a sharp contact. Here it is constructed directly from the terminal reduced witness and the pivot-chain data.

### Operational gain

After a fixed-candidate T-P5-170 PASS with a terminal zero contact, the consumer may:

1. replay the backward state lift;
2. compute `S_0=supp(z_0)`;
3. use `(z_0)_{S_0}` as the positive principal-kernel witness;
4. feed that support directly to determinant/root or active-face sharpness logic.

No original-dimension KKT solve, pseudoinverse, eigenvector solve, or support search is mathematically necessary.

---

## 5. Sharp-floor bridge to T-P5-159/T-P5-169

Return to the additive floor family

`M_D`,

`q_D(x)=Q_0(x)+D L(x)`,

with `g_i>0`, so `L(x)>0` for every nonzero `x>=0`.

Fix a candidate `D_*>0`. Assume:

1. `M_{D_*}` admits a valid T-P5-170 pivot chain;
2. the terminal core is copositive;
3. there is a nonzero terminal zero contact `z_m>=0`.

T-P5-170 already gives a lifted nonzero original zero contact `z_0` and proves `D_*` is the exact sharp floor by reusing `z_0` for every `D<D_*`.

T171 strengthens the support conclusion.

### Corollary T171-E — `terminal_contact_gives_original_support_root`

Let

`S_0=supp(z_0)`.

Then

**(5.1)** `M_{D_*}[S_0,S_0] (z_0)_{S_0}=0`,

with positive kernel vector `(z_0)_{S_0}>0`. Hence

**(5.2)** `det(M_{D_*}[S_0,S_0])=0`.

Therefore the terminal contact not only certifies sharpness; it identifies an explicit original principal support on which the T-P5-159 determinant polynomial vanishes.

This does **not** assert that the determinant root is isolated, simple, or the unique winning support. Degenerate ties and identically singular support polynomials remain separate cases.

---

## 6. Exact regression using the T-P5-170 four-vertex example

Reuse T-P5-170's matrix

`M = [[ 1,-1, 0, 0],`
`     [-1, 2,-1, 2],`
`     [ 0,-1, 1,-1],`
`     [ 0, 2,-1, 1]]`.

T-P5-170 pivots coordinate `1`, then coordinate `3`, reaching the terminal core on `(x2,x4)`

**(6.1)**

`M_2=[[0,1],[1,0]]`.

This matrix is copositive. Choose the terminal zero contact

**(6.2)** `z_2=(1,0)`.

Then

**(6.3)** `M_2 z_2=(0,1)`.

Thus `z_2` is not a full kernel vector, but it is an exact orthant-complementary contact: the active coordinate has zero residual and the inactive coordinate has positive residual.

At the second pivot, `b_1=1`, `r_1=(1,1)`. In pivot-first order `(x3 | x2,x4)`,

`r_1^T z_2=1`,

so the lifted state is `(1,1,0)`, which in current order `(x2,x3,x4)` is

**(6.4)** `z_1=(1,1,0)`.

The exact residual identity gives

**(6.5)** `M_1 z_1=(0,0,1)`

in `(x2,x3,x4)` ordering.

At the first pivot, `b_0=1`, `r_0=(1,0,0)`, so

**(6.6)** `z_0=(1,1,1,0)`.

Direct exact multiplication gives

**(6.7)**

`M z_0=(0,0,0,1)`

and

**(6.8)** `z_0^T M z_0=0`.

The lifted positive support is

`S_0={1,2,3}`.

Its principal matrix is

`[[ 1,-1, 0],`
` [-1, 2,-1],`
` [ 0,-1, 1]]`,

and

**(6.9)**

`M[S_0,S_0] (1,1,1)^T = 0`,

so

**(6.10)** `det(M[S_0,S_0])=0`.

This regression separates three notions cleanly:

- the terminal contact is cone-KKT but not a full kernel vector;
- the residual survives backward exactly on the one terminal inactive coordinate;
- the active original support nevertheless acquires an explicit positive principal-kernel vector.

A local exact symbolic check reproduces (6.7)-(6.10).

---

## 7. Strict-complementarity boundary

The transport preserves weak orthant complementarity, but not strict complementarity of all inactive coordinates.

Consider one stage with

`b=1`,

`r=(1,0)`,

and terminal reduced matrix

`S=[[1,1],[1,0]]`.

`S` is copositive. For

`z=(0,1)`,

we have

`Sz=(1,0)`.

Thus the terminal contact is strictly complementary on its sole inactive coordinate: the inactive residual equals `1>0`.

Choose

`A=S+r r^T=[[2,1],[1,0]]`,

so the pre-pivot matrix is

`M=[[ 1,-1,0],`
`   [-1, 2,1],`
`   [ 0, 1,0]]`.

Because `r^Tz=0`, the lifted pivot coordinate is zero:

`L(z)=(0,0,1)`.

T171-B gives

`M L(z)=(0,1,0)`.

The newly reintroduced pivot is inactive **and has zero residual**. Therefore strict complementarity on all inactive original coordinates fails even though the terminal surviving inactive coordinate was strict.

### Exact boundary

Weak complementarity is invariant under the pivot lift.

Strict complementarity is preserved on surviving terminal coordinates, but an eliminated pivot with `r^Tz=0` is reintroduced as an inactive zero-residual coordinate. Hence uniqueness of the active set, strict KKT margins, and root transversality require additional hypotheses and must not be inferred from T171.

---

## 8. Minimal typed mathematical contract

A useful source-independent interface can be kept very small.

### 8.1 Terminal contact packet

For a symmetric terminal matrix `M_m`, provide either:

- `copositive(M_m)`, `z_m>=0`, `z_m!=0`, `z_m^T M_m z_m=0`;

or directly the stronger typed witness

- `z_m>=0`, `M_m z_m>=0`, `z_m .* (M_m z_m)=0`.

The first form derives the second by T171-A.

### 8.2 Pivot-stage packet

For each T-P5-170 stage provide exactly:

- pivot/current ordering;
- `b_k>0`;
- `r_k>=0`;
- retained block `A_k`;
- exact identity `M_{k+1}=b_k A_k-r_k r_k^T`.

The consumer forms

`z_k=(r_k^T z_{k+1}, b_k z_{k+1})`

and checks/reuses the exact vector theorem

`M_k z_k = padPivotZero(M_{k+1} z_{k+1})`.

### 8.3 Support packet

After replaying the chain, define support from the **actual lifted state**:

`S_0={i:z_0,i>0}`.

Then the principal-kernel theorem is

`M_0[S_0,S_0](z_0)_{S_0}=0`.

Do not transport a terminal support label without replaying pivot activity: a pivot joins the support iff `r_k^T z_{k+1}>0`.

### Lean-friendly theorem leaves

Suggested theorem decomposition:

1. `copositive_zero_contact_mulVec_nonneg`;
2. `copositive_zero_contact_active_mulVec_eq_zero`;
3. `pivotLift_mulVec`;
4. `pivotLift_complementarity`;
5. `iteratedPivotLift_mulVec_padZeros`;
6. `liftedContact_principalSubmatrix_kernel`;
7. `terminalContact_originalSupportRoot`.

The first two can use the explicit polynomial contradiction vectors from Section 1, avoiding derivative/KKT APIs. The pivot theorems need only finite sums and matrix-vector algebra.

---

## 9. Failure boundaries and remaining obligations

This review deliberately keeps the following boundaries open.

### Mathematical boundaries

- Symmetry matters. For a nonsymmetric source matrix, the quadratic form only sees the symmetric part; do not identify raw `Mz` with the quadratic gradient unless the source has been symmetrized/bound correctly.
- A zero-energy vector without a copositivity PASS need not satisfy `Mz>=0`; Section 1 gives a two-coordinate counterexample.
- The algebraic identity `M L(z)=(0,Sz)` does not itself require `r>=0`, but **cone transport does**: if `r^Tz<0`, the lifted pivot coordinate leaves the nonnegative orthant.
- `b>0` is required by the T-P5-170 copositive iff chain and by positive scaling of retained state coordinates.
- Weak complementarity transports; strict complementarity and active-set uniqueness do not automatically transport.
- A lifted principal determinant zero is a root/contact certificate, not root isolation, multiplicity control, or uniqueness of the winning support.
- This is a fixed-candidate chain theorem. T-P5-170's symbolic-`D` issue remains: reduced entries can have higher polynomial degree and stage sign gates can change with `D`.

### External/source boundaries

Still open:

- actual same-key `{g_i,K_ij}` / deployed floor-matrix source;
- actual fixed candidate `D` and source-certified pivot ordering;
- exact terminal contact from the deployed matrix instance;
- uncertainty/cell/trajectory coverage;
- Float64 / interval outward rounding / runtime controller semantics;
- P8/M4 propagation;
- Lean/kernel compilation;
- independent verification by 封不觉;
- admission/registry/P5 parent closure.

Therefore the correct state remains

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`.**

---

## 10. Recommended use

When T-P5-170 reduces a fixed exact copositivity candidate to a small terminal core and that core has a zero contact, do **not** solve a second original-dimensional KKT problem.

Instead:

1. derive terminal orthant complementarity from terminal copositivity plus zero energy;
2. replay the existing division-free backward state lifts;
3. simultaneously zero-pad the terminal residual using T171-C;
4. take the positive support of the lifted state;
5. reuse that support and state as the original principal-kernel witness for T-P5-159/T-P5-169 sharp-floor logic.

This is an exact cross-layer bridge: terminal cone certificate -> original KKT contact -> principal support kernel, with no inverse, square root, eigenvector solve, pseudoinverse, or new support optimization.