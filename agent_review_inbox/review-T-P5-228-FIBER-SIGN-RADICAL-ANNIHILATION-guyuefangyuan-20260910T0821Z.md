---
kind: review_result
review_id: review-T-P5-228-fiber-sign-radical-annihilation-guyuefangyuan-20260910T0821Z
task_id: T-P5-228-FIBER-SIGN-RADICAL-ANNIHILATION
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T08:21:00Z
claim_commit: 895ef4080a23c01edea3eae5c543acf61e742058
inspected_commit: 671b1808c978b761cfab1def3660aa0547d20e7f
upstream_commits:
  - 467527fa4670608070e0d74e64e6b7087a8b3094  # T-P5-222 face-lift quotient debit descent
  - 53af0acf2a6a9f7146f0847d7ff860560cb035ae  # T-P5-224 lineality Schur endpoint reduction
  - 3ea6316491536353fd7908122a0926e494906e13  # T-P5-225 signed-lineality Schur follow-on
  - 6a10ef29433a4dd050d593d8053383f4ba7fd204  # T-P5-226 arbitrary-corank fraction-free branch
  - 068792f0a320dfe3195ef2bfdf1081506b5b4db0  # T-P5-227 quotient/Schur commutation
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_flat_fiber_radicalization; add_lineality_flatness_corollary; add_bounded_fiber_obstruction; connect_zero_curvature_branch_to_signed_schur_dispatch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional symmetric-bilinear algebra and rational regressions only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-228 — flat two-sided fibers force debit-radical annihilation

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-222 identified the exact quotient gate for endpoint debit: for a consumed packet with representative matrix `W`, gauge matrix `G`, and symmetric debit form `Q`, representative-independence requires

`G^T Q G = 0`,

`G^T Q W = 0`.

T-P5-227 then proved that, once this radical gate is valid, quotienting the face gauge commutes with the signed physical-lineality Schur reduction. Its handoff explicitly asked for a structural annihilation theorem that can make the cross-radical block automatic rather than another singular-Schur variant.

This child gives that theorem.

The main result is:

> If the purported gauge is a genuine **two-sided admissible fiber**, the endpoint quadratic is one-sided nonpositive on the whole fiber, and pure gauge has exactly zero quadratic curvature, then the gauge is automatically bilinearly radical against every consumed endpoint representative.

In matrix form, if

`q(x) := x^T Q x`, `Q=Q^T`,

and for every consumed representative `w` and every `alpha in R^g`,

`q(w + G alpha) <= 0`,

while

`G^T Q G = 0`,

then necessarily

**`G^T Q w = 0`.**

Hence for a finite packet `W`,

**`G^T Q G = 0` + full-fiber sign validity => `G^T Q W = 0`,**

which is exactly the T-P5-222 restricted radical gate.

This is not merely another sufficient inequality. It says that in the flat branch, any failed cross-radical entry is an exact mathematical witness that at least one of the following source statements is false: the direction is a genuine free gauge, the sign theorem applies to all representatives, or pure gauge is truly debit-flat.

The same argument shows that T-P5-222's flat quotient branch is precisely the zero-curvature specialization of T-P5-224/225/226 signed-coordinate Schur elimination. A nonflat two-sided direction should not be silently quotiented: negative curvature belongs in the Schur branch; positive curvature or a kernel-cross defect gives an explicit positive-debit obstruction.

No actual P5 face/tangent source identity, selector/cell/tube coverage, Float64/interval semantics, Lean/kernel receipt, independent validation by 封不觉, admission, or registry mutation is claimed.

---

## 1. Abstract setup

Let `Y` be a finite-dimensional real vector space with symmetric bilinear form

`B_Q(x,y) := x^T Q y`

and quadratic form

`q_Q(x) := x^T Q x`.

Let the columns of `G` span a candidate face-lift gauge space `N = range(G)`. Let `w` be one consumed endpoint representative.

A **two-sided fiber** through `w` means that every

`w + G alpha`, `alpha in R^g`,

is an admissible representative to which the same endpoint sign claim applies.

The relevant safe sign in the current P5 debit convention is

`q_Q(w + G alpha) <= 0`.

Everything below has a sign-reversed analogue for nonnegative quadratic forms.

---

## 2. T228-A — flat-fiber annihilation theorem

### Theorem A

Assume

1. `Q=Q^T`;
2. `G^T Q G = 0`;
3. for a fixed `w`, `q_Q(w+G alpha) <= 0` for every `alpha in R^g`.

Then

**`G^T Q w = 0`.**

### Proof

Let

`b := G^T Q w`.

Because `G^TQG=0`, expansion gives

`q_Q(w+G alpha) = q_Q(w) + 2 alpha^T b`.

If `b != 0`, choose `alpha = t b` with `t>0`. Then

`q_Q(w+G(t b)) = q_Q(w) + 2t ||b||^2`.

For sufficiently large `t`, this is strictly positive, contradicting the assumed nonpositivity for every gauge representative.

Therefore `b=0`, i.e.

`G^T Q w=0`.

QED.

### Corollary A1 — finite packet radicalization

Let `W=[w_1 ... w_m]`. If the hypotheses of Theorem A hold for every column `w_j`, then

`G^T Q W=0`.

Combined with `G^TQG=0`, this is exactly T-P5-222's restricted radical condition on

`span(W,G)`.

Thus the endpoint debit descends to the quotient on the whole consumed packet without separately checking every gauge/representative cross pairing.

### Corollary A2 — bilinear invariance

Under the same packet conditions, for arbitrary `u,v` in `span(W)` and arbitrary gauge vectors `Ga,Gb`,

`(u+Ga)^T Q (v+Gb) = u^T Q v`.

Proof: every term containing `G` vanishes by `G^TQW=0` and `G^TQG=0`.

Therefore all T-P5-215 self/cross debit decisions become representative-independent.

---

## 3. T228-B — why full gauge flatness means the whole block, not diagonal tests

The assumption

`G^TQG=0`

is equivalent to

`q_Q(G alpha)=0` for every `alpha`.

It is **not** enough to check only each chosen gauge basis vector individually.

Indeed, polarization gives

`2 B_Q(n_1,n_2) = q_Q(n_1+n_2)-q_Q(n_1)-q_Q(n_2)`.

Thus vanishing of the quadratic form on the entire gauge subspace forces every gauge/gauge cross term to vanish. But basiswise self-zeros alone do not.

### Exact rational regression B1

Take

`Q = [[0,1],[1,0]]`, `G=I_2`.

Then

`q(e_1)=0`, `q(e_2)=0`,

but

`q(e_1+e_2)=2`,

and

`G^TQG=Q != 0`.

So a producer that checks only `g_i^TQg_i=0` for each basis column can falsely label a nonflat gauge as flat.

The exact packet gate must certify the full symmetric block `G^TQG=0`, or an equivalent all-combinations theorem from the source identity.

---

## 4. T228-C — cone/lineality structural corollary

The flat-fiber theorem has a geometric form that is especially useful for T-P5-224 physical lineality.

Let `C` be a convex cone and let

`L := C cap (-C)`

be its lineality space. Let `N subset L`.

Assume

`q_Q(x) <= 0` for every `x in C`,

and

`q_Q(n)=0` for every `n in N`.

Then

**`B_Q(n,x)=0` for every `n in N`, `x in C`.**

Hence

**`N subset rad(B_Q | span(C))`.**

### Proof

Because `n,-n in C`, for every real `t` and every `x in C`,

`x+t n in C`.

Indeed for `t>=0`, use `x+t n`; for `t<0`, use `x+(-t)(-n)`.

Since `q_Q(n)=0`,

`q_Q(x+t n) = q_Q(x)+2t B_Q(n,x)`.

This is nonpositive for every `t in R`. The linear coefficient must therefore vanish:

`B_Q(n,x)=0`.

QED.

### Meaning for the P5 dispatcher

A genuine physical lineality direction with zero debit curvature is automatically radical once global nonpositivity on the endpoint cone is known. Conversely, a lineality direction with nonzero negative curvature is not a quotient gauge; it belongs in T-P5-224/225/226's signed Schur block.

This yields a clean semantic distinction:

- **flat lineality/fiber** -> radical quotient branch;
- **negative-curvature signed lineality** -> Schur elimination branch;
- **positive curvature** -> immediate positive-debit witness;
- **zero curvature plus nonzero cross term** -> unbounded linear positive-debit witness along the two-sided fiber.

---

## 5. T228-D — the flat branch is exactly the kernel-cross branch of signed Schur

Fix a gauge/signed coordinate matrix `G` and one representative `w`. Write

`A := G^TQG`,

`b := G^TQw`,

`c := q_Q(w)`.

Then

`q_Q(w+G alpha) = alpha^T A alpha + 2 alpha^T b + c`.

If this quantity is nonpositive for every `alpha in R^g`, then necessarily:

1. `A <= 0` (negative semidefinite);
2. `b` is orthogonal to `ker(A)`, equivalently `b in range(A)` for symmetric `A`.

The proof is exact:

- if some `v` has `v^TAv>0`, then `alpha=t v` makes the positive `t^2` term dominate;
- if `z in ker(A)` and `z^T b !=0`, then `alpha=t z` leaves only a nonzero linear term `2t z^Tb`, which becomes positive for one sign of `t` and arbitrarily large magnitude.

Now specialize to the **flat** case `A=0`. Then `ker(A)=R^g`, so the range/kernel condition forces

`b=0`.

Therefore T-P5-222's radical gate is not an unrelated extra condition. It is exactly the zero-curvature branch of the signed-coordinate quadratic dispatcher already underlying T-P5-224/225/226.

This gives a source/checker rule:

> Never quotient a free two-sided coordinate merely because its storage energy is zero. First classify its debit block `A=G^TQG`. Only the exact flat branch `A=0` can become a quotient gauge, and in that branch full-fiber nonpositivity forces all cross terms to vanish. If `A<0` in some directions, retain them as signed Schur coordinates.

---

## 6. T228-E — exact obstruction when cross-radicality fails

Suppose pure gauge is flat:

`q_Q(g)=0`,

but for some consumed representative `w`,

`b := g^TQw != 0`.

Then

`q_Q(w+t g)=q_Q(w)+2t b`.

Thus the debit along this purported gauge fiber is unbounded above and below as `t` ranges over `R`.

In particular there is an explicit positive-debit witness. If `b>0`, choose any rational

`t > -q_Q(w)/(2b)`.

If `b<0`, choose a sufficiently large negative rational `t`.

Therefore a failed T-P5-222 cross-radical entry has a strong interpretation in the two-sided-flat model: it is not merely 'quotient ambiguity'; it proves that the full fiber cannot obey a one-sided endpoint debit theorem.

### Exact rational regression E1

Take

`Q=[[0,1],[1,0]]`,

`g=e_1`, `w=e_2`.

Then

`q(g)=0`, `q(w)=0`, `g^TQw=1`.

Hence

`q(w+t g)=2t`.

The same physical class cannot be declared nonpositive for all two-sided gauge representatives.

---

## 7. T228-F — bounded ambiguity does NOT imply radicality

The preceding theorem critically uses a **free two-sided fiber**, not merely a bounded family of alternative lifts.

Suppose `q(g)=0` and only

`|t| <= T`

is admissible. Then

`q(w+t g)=q(w)+2t b`, `b=g^TQw`.

Requiring nonpositivity for all `|t|<=T` is equivalent to

**`q(w)+2T |b| <= 0`.**

This permits `b !=0` whenever the base representative has enough negative reserve.

### Exact rational regression F1

Take

`Q=[[0,1],[1,-2]]`,

`g=e_1`, `w=e_2`, `T=1`.

Then

`q(g)=0`, `q(w)=-2`, `g^TQw=1`,

and

`q(w+t g)=-2+2t <=0`

for every `t in [-1,1]`.

Yet the cross-radical term is nonzero.

Therefore a source producer must distinguish:

- true quotient gauge: coefficient free in all `R`;
- bounded lift uncertainty: coefficient lies in a bounded set.

The second case must be carried as uncertainty/slack and cannot be collapsed by T-P5-222 quotient descent.

### Finite symmetric-probe bound

More generally, if pure gauge is flat and both `w+Tg` and `w-Tg` are known safe, then

`2T |g^TQw| <= -q(w)`.

At a zero-debit contact `q(w)=0`, just the two probes `+Tg` and `-Tg` already force

`g^TQw=0`.

Away from contact they only bound the cross term; they do not annihilate it.

---

## 8. T228-G — zero curvature is essential

Full-fiber sign validity alone does not force radicality if the fiber has genuine negative curvature.

### Exact rational regression G1

Take

`Q=[[-1,1],[1,-1]]`.

This matrix is negative semidefinite because

`q(x_1,x_2)=-(x_1-x_2)^2 <=0`

on all of `R^2`.

Let the two-sided direction be `g=e_1` and take `w=e_2`.

Then

`q(g)=-1<0`,

`g^TQw=1 !=0`.

Nevertheless `q(w+t g)<=0` for every real `t`.

So the correct theorem is not 'two-sided sign implies radical'. It is:

**two-sided sign + exact zero curvature implies radical.**

Negative-curvature free directions are precisely the signed-Schur situation, not the quotient situation.

---

## 9. T228-H — source-factorization corollary

There is an even stronger structural route if the actual endpoint debit scalar is known to factor through the physical quotient.

Let `pi:Y -> Y/N` be the quotient map. Suppose a twice differentiable physical scalar has the form

`F = Fbar o pi`.

Then for every `n in N`, translation by `n` leaves `F` unchanged. Differentiating gives

`D F(y)[n]=0`

for all `y`, and differentiating this identity in any direction `v` gives

`D^2 F(y)[v,n]=0`.

Hence every Hessian representing the second-order debit satisfies

**`N subset ker(Hess F(y))`.**

So if the P5 face/tangent source can prove that the second-order endpoint scalar itself is a function only of the physical tangent class, the T-P5-222 radical gate follows structurally and no packetwise cross-block calculation is mathematically necessary.

This is the cleanest eventual source theorem. The current child does not claim the real P5 source already satisfies this factorization; it records exactly what identity would suffice.

---

## 10. Consequences for the existing P5 route

The T-P5-222 -> T-P5-224/225/226 -> T-P5-227 chain can now use the following semantic dispatcher.

Given a candidate free lift direction block `G` and endpoint debit `Q`:

1. compute or structurally identify `A=G^TQG`;
2. if `A=0` and the source certifies full two-sided fiber validity of the endpoint sign theorem, T228-A forces `G^TQW=0`; quotienting is sound on the consumed packet;
3. if `A` is negative semidefinite but nonzero, do **not** quotient it as gauge; retain it as signed coordinates and use the T-P5-224/225/226 Schur/range dispatcher;
4. if `A` has a positive direction, that direction itself is a positive-debit witness;
5. if `A` is singular and some kernel direction has nonzero cross term against the pointed packet, signed scaling gives an unbounded positive-debit witness;
6. if the source only allows bounded lift changes, use the exact bounded-fiber inequality from T228-F rather than radical quotienting.

This removes a conceptual ambiguity left after T-P5-227: **flat true gauge and curved signed lineality are not two unrelated kinds of nuisance coordinates; they are the zero-curvature and nonzero-curvature branches of the same two-sided quadratic fiber analysis.**

---

## 11. Suggested Lean decomposition

The first formalization should stay small and avoid quotient types initially.

Suggested leaves:

- `flatFiber_nonpos_forall_imp_cross_zero`
  - hypotheses `Q.IsSymm`, `G^T*Q*G=0`, `forall a, quad Q (w+G*a) <= 0`;
  - conclusion `G^T*Q*w=0`.

- `flatFiber_packet_imp_restrictedRadical`
  - columnwise lift of the previous lemma to `W`.

- `lineality_flat_nonpos_imp_radical`
  - cone/lineality form of T228-C.

- `signedFiber_nonpos_imp_negSemidef_and_kernelCrossZero`
  - derive `A<=0` and `ker(A) subset ker(b^T)` from full-fiber nonpositivity.

- `boundedFlatFiber_nonpos_iff_crossBound`
  - one-dimensional exact formula `q(w)+2T|b|<=0`.

- `quadraticFactorThroughQuotient_imp_radical`
  - algebraic quadratic version of T228-H before introducing general Hessians.

No pseudoinverse, eigensystem, square root, or optimizer is required for the flat branch.

---

## 12. Remaining open boundaries

This child does **not** prove that the actual P5 face-lift family is saturated by a free two-sided gauge. It also does not prove that pure gauge has zero endpoint debit curvature. Those are source identities that must be established from the actual tangent/endpoint construction.

In particular, a bounded coordinate freedom, a one-sided freedom, or a numerical near-null direction must not be upgraded to quotient gauge by this theorem.

Still open:

- actual same-key face/tangent lift maps and their gauge parameter domain;
- proof that pure gauge is exactly debit-flat, preferably by quotient-factorization of the physical second-order scalar;
- source/cell/tube and trajectory coverage;
- rational/Float64 enclosure semantics if source matrices are numerical;
- Lean/kernel compilation;
- independent validation by 封不觉;
- admission/registry.

The mathematical child itself is complete: under exact flatness and genuine two-sided fiber validity, the T-P5-222 cross-radical gate is forced, and failure of that gate supplies an explicit obstruction rather than an ambiguous implementation mismatch.
