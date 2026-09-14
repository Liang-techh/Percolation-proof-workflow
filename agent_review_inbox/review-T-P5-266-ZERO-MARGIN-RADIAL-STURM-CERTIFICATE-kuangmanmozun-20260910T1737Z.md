---
kind: review_result
review_id: review-T-P5-266-zero-margin-radial-sturm-certificate-kuangmanmozun-20260910T1737Z
task_id: T-P5-266-ZERO-MARGIN-RADIAL-STURM-CERTIFICATE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T17:37:00Z
claim_commit: c0688a6b2b22d3dd686f659c4c72ce560c9da467
inspected_commit: f027ff66827c872da510b17df3467d44d7c2459f
upstream_commits:
  - 913ed31d66c77016e82fe2371d3734b033e76e5f  # T-P5-265 rational Bernstein interval certificate
  - 32dbdb379152b48355b110682cfc1314c0ff231a  # T-P5-264 parity-symmetric homogeneous energy allocator
  - f4704792f1420aef65ad19af2e03ece571bf494e  # T-P5-263 higher-degree matched-metric polarization
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_squarefree_parity_factorization; add_open_interval_odd_root_Sturm_count; add_zero_margin_nonnegativity_iff; add_rational_negative_witness_extraction; add_radial_zero_reserve_consumer; preserve_Bernstein_fast_path
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact rational squarefree decomposition, Sturm-chain sign variation, rational sample-grid argument, exact counterexample regressions; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-266 — Zero-margin rational radial closure by multiplicity parity and Sturm counting

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-265 gives a finite rational Bernstein-subdivision certificate that is complete whenever the radial reserve is strict. It deliberately leaves the touching case open: if

`p(q) := K - A(q)`

is merely nonnegative on `[0,R]` and vanishes at one or more points, a Bernstein tree need not expose an all-nonnegative coefficient leaf around every contact point.

This child closes that zero-margin gap for every **univariate rational polynomial**. The exact obstruction is not “has a real root”; it is “has an **odd-multiplicity** root in the **open** interval.” Even-multiplicity contacts are harmless, and odd roots at the two interval endpoints are also harmless for a closed-interval nonnegativity statement.

The resulting decision packet uses only:

- rational gcd / squarefree decomposition;
- exact polynomial division;
- a Sturm chain over `Q`;
- sign evaluations at rational points.

No floating root finder, SOS search, eigenproblem, square root, pseudoinverse, or sampling-based maximization is required. Unlike the strict Bernstein completeness statement, this packet is complete for the non-strict zero-margin case as well.

No deployed P5 radial polynomial, source metric/radius, chart, cell/trajectory/FD-halo coverage, Float64 semantics, Lean/kernel proof, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup: the exact zero-reserve question

Let

`p in Q[q]`, `a,b in Q`, `a < b`.

The consumer question is

**(1.1)** `p(x) >= 0  for every real x in [a,b]`.

For T-P5-265 one has the specialization

`a=0`, `b=R`, `p(q)=K-A(q)`.

The degenerate interval `a=b` is trivial and should be routed separately: the exact condition is simply `p(a)>=0`. Below assume `a<b`.

If `p=0` identically, (1.1) is an immediate PASS. Hence assume from now on `p != 0`.

---

## 2. Squarefree multiplicity decomposition without irreducible factorization

Over `Q`, write the squarefree decomposition

**(2.1)**

`p(q) = c * product_{j=1}^m f_j(q)^j`,

where:

- `c in Q \ {0}`;
- each nonconstant `f_j` is monic and squarefree;
- the `f_j` are pairwise coprime;
- factors equal to `1` may be omitted.

This is the standard gcd/squarefree decomposition; no irreducible factorization is required.

Define

**(2.2)** `E(q) := product_j f_j(q)^(floor(j/2))`,

and the **odd-multiplicity kernel**

**(2.3)** `O(q) := product_{j odd} f_j(q)`.

Then the exact identity is

**(2.4)** `p(q) = c * E(q)^2 * O(q)`.

Every real root of `O` is exactly a real root of `p` whose multiplicity in `p` is odd. Roots represented only in `E^2` have even multiplicity and cannot change the sign of `p`.

### Formal/checker packet

A producer may submit `(c,{f_j})`, but the checker should verify or recompute:

1. the exact identity (2.1);
2. `gcd(f_j,f_j')=1` for each nonconstant `f_j`;
3. `gcd(f_i,f_j)=1` for `i!=j`;
4. the derived identity (2.4).

Missing a repeated factor is a parity bug, not a harmless provenance detail.

---

## 3. Endpoint stripping: closed interval is not open interval

An odd-multiplicity root at an endpoint does **not** force negativity on the closed interval. The simplest example is

`p(q)=q` on `[0,1]`.

The root at `q=0` is simple, yet `p>=0` on the whole interval.

Because `O` is squarefree, each endpoint can occur in `O` at most once. Define

`epsilon_a := 1 if O(a)=0, else 0`,

`epsilon_b := 1 if O(b)=0, else 0`,

and divide exactly

**(3.1)**

`O_int(q) := O(q) / [(q-a)^epsilon_a (q-b)^epsilon_b]`.

Then

`O_int(a) != 0`, `O_int(b) != 0`,

and the real roots of `O_int` in `[a,b]` are exactly the odd-multiplicity roots of `p` in the **open interval** `(a,b)`.

If `O_int` is constant, its interior root count is zero by convention.

---

## 4. Exact Sturm count for interior odd roots

For nonconstant `O_int`, construct the ordinary Sturm chain over `Q`:

`S_0 = O_int`,

`S_1 = O_int'`,

**(4.1)** `S_{k+1} = -rem(S_{k-1},S_k)`,

until a nonzero constant is reached.

For a rational point `x` at which `O_int(x)!=0`, let `V(x)` be the number of sign variations in

`(S_0(x),S_1(x),...,S_r(x))`,

with zero entries ignored in the standard way.

Since endpoint factors were stripped, the endpoints are not roots of `O_int`, and Sturm's theorem gives the exact integer

**(4.2)** `N_odd := V(a)-V(b)`.

This is precisely the number of distinct odd-multiplicity roots of `p` in `(a,b)`.

### Fraction-free serialization warning

All chain coefficients are rational. To serialize with integers, each `S_k` may be multiplied by a **positive** common denominator and then divided by a positive integer content. Positive rescaling preserves every pointwise sign and hence every variation count.

Do **not** independently flip a Sturm polynomial by a negative scalar merely to make its leading coefficient positive. Such a sign flip can change the variation count and invalidate the certificate unless the recurrence is rebuilt consistently.

---

## 5. Theorem A — complete zero-margin nonnegativity criterion

Let `p!=0`, and define `O_int` and `N_odd` as above. Choose any rational point

`r in (a,b)` with `p(r)!=0`.

Such an `r` always exists because a nonzero polynomial has only finitely many roots and `Q` is dense in `R`.

Then the following are equivalent:

**(A1)** `p(x)>=0` for every real `x in [a,b]`.

**(A2)**

1. `N_odd=0`, and
2. `p(r)>0`.

Endpoint sign tests are optional redundant guards once (A2) holds; continuity then already gives `p(a)>=0` and `p(b)>=0`. A checker may still evaluate them explicitly because a negative endpoint is an immediate rational FAIL witness.

### Proof: (A1) -> (A2)

Suppose `p>=0` on `[a,b]`.

An interior root of odd multiplicity would reverse sign across that root, forcing one adjacent side to be negative. Hence there are no odd-multiplicity roots in `(a,b)`, so `N_odd=0`.

Since `p` is nonzero, it cannot vanish on the whole interval. Its zeros are finite. Therefore there exists an interior rational `r` with `p(r)!=0`; nonnegativity forces `p(r)>0`.

### Proof: (A2) -> (A1)

From (2.4),

`p = c E^2 O`.

All zeros contributed by `E^2` are even contacts. Since `N_odd=0`, `O` has no roots in the open interval except the stripped endpoint factors, whose signs are fixed throughout `(a,b)`.

Therefore `p` has a constant strict sign on every point of `(a,b)` that is not a root of `p`; crossing an `E^2` root does not change that sign. The single anchor `p(r)>0` fixes this constant sign to positive.

At every interior root, `p=0`. Thus `p>=0` on `(a,b)`, and continuity extends the inequality to `a,b`.

This proves equivalence.

---

## 6. Deterministic rational sign anchor: no search oracle is needed

The existential point `r` can be replaced by a fixed finite grid.

Let `d=deg(p)`. Define the `d+1` rational interior points

**(6.1)**

`r_k := a + (b-a) k/(d+2)`, `k=1,...,d+1`.

They are distinct and all lie in `(a,b)`. A degree-`d` nonzero polynomial cannot vanish at all `d+1` points. Hence at least one has `p(r_k)!=0`.

Let `k_*` be the first such index. Then Theorem A can be implemented by the finite exact rule

**(6.2)**

`p>=0 on [a,b]`

iff

`N_odd=0` and `p(r_{k_*})>0`.

Thus the whole zero-margin consumer is a terminating rational decision procedure, not merely a semi-decision certificate.

---

## 7. Theorem B — exact FAIL and rational negative-witness extraction

The same packet can return mathematical FAIL, not merely `CERTIFICATE_NOT_FOUND`.

### Branch B1 — no interior odd root

If `N_odd=0`, choose the deterministic nonzero sample `r_{k_*}`.

- If `p(r_{k_*})>0`, PASS by Theorem A.
- If `p(r_{k_*})<0`, then `r_{k_*}` itself is an exact rational negative witness.

There is no third case because `r_{k_*}` was selected to be nonzero.

### Branch B2 — at least one interior odd root

If `N_odd>0`, pick one odd root `xi in (a,b)` and isolate it by exact Sturm bisection. Refine to rational endpoints `l<u` such that:

1. `l<xi<u`;
2. the squarefree radical of `p` has exactly one root in `(l,u)`;
3. `p(l)!=0` and `p(u)!=0`.

Because the enclosed root has odd multiplicity and there is no other root of `p` in the interval, `p(l)` and `p(u)` have opposite signs. Therefore one of `l,u` is a rational point with

**(7.1)** `p(point)<0`.

So an interior odd root yields a constructive rational counterexample to nonnegativity.

The root itself may be algebraic and need never be serialized as a floating number; only the rational isolating interval and exact Sturm counts are needed.

---

## 8. Sharp counterexamples against tempting but wrong gates

### 8.1 Rejecting every real root is wrong

Take

`p(q)=(q-1/2)^2` on `[0,1]`.

Then `p>=0` and the reserve is exactly zero at `q=1/2`. The ordinary squarefree radical has the interior root `1/2`, but its multiplicity in `p` is two. The squarefree decomposition gives

`E=q-1/2`, `O=1`, hence `N_odd=0`.

A checker that rejects “any interior real root” would false-negative precisely the zero-margin contact this child is meant to recover.

### 8.2 Rejecting endpoint odd roots is wrong

Take

`p(q)=q` on `[0,1]`.

The root at zero is simple. It is removed by endpoint stripping; `O_int=1`, `N_odd=0`, and any interior sample is positive. The correct verdict is PASS.

### 8.3 No odd root alone does not determine the sign

Take

`p(q)=-(q-1/2)^2` on `[0,1]`.

Again `O=1` and `N_odd=0`, but every nonroot interior sample is negative. Therefore the sign anchor is indispensable.

### 8.4 Endpoint checks alone are unsound

Take

`p(q)=(q-1/4)(q-3/4)` on `[0,1]`.

One has

`p(0)=p(1)=3/16>0`,

but

`p(1/2)=-1/16<0`.

Both roots are simple and interior. In a normalized Sturm chain

`S0=q^2-q+3/16`,

`S1=2q-1`,

`S2=1/16`,

the variations are `V(0)=2`, `V(1)=0`, so `N_odd=2`. The Sturm gate catches exactly the hidden negative interval.

### 8.5 The midpoint is not a sufficient sign anchor

For the nonnegative contact polynomial `(q-1/2)^2`, the midpoint value is zero. A checker must not interpret a zero midpoint as a failure or as evidence that the polynomial vanishes identically. The finite `d+1` grid rule in Section 6 guarantees a nonzero rational sample.

---

## 9. Radial consumer specialized to T-P5-264/265

Suppose upstream has already derived on a source region

**(9.1)** `||P(u)||^2 <= Q(u) A(Q(u))`,

with

`Q(u)=u^T W u`, `0<=Q(u)<=R`,

and a desired reserve `K Q(u)`.

Set

**(9.2)** `p(q)=K-A(q)`.

Then:

- if `p=0`, the radial allocation is exactly saturated and PASS;
- if `p!=0`, compute its squarefree multiplicity decomposition;
- strip odd endpoint factors at `q=0,R`;
- Sturm-count the odd kernel on `(0,R)`;
- if the count is zero, evaluate one deterministic nonzero rational sample;
- positive sample gives exact non-strict PASS;
- negative sample gives an exact rational FAIL witness;
- positive odd-root count gives a rational negative witness after exact root isolation.

Therefore the strict Bernstein route from T-P5-265 and this parity/Sturm route can be layered as:

1. **Bernstein fast path:** cheap all-leaf coefficient PASS, especially strong when positive reserve exists;
2. **Sturm zero-margin fallback:** complete exact decision when Bernstein subdivision stalls at touching roots.

A Bernstein search failure must still never be interpreted as a mathematical FAIL; the Sturm/parity fallback is the decisive layer.

---

## 10. Formalizable theorem statements

### Theorem `oddKernel_factorization`

For a nonzero rational polynomial with verified squarefree decomposition

`p=c * product_j f_j^j`,

define

`E=product_j f_j^(j/2 floor)`,

`O=product_{j odd} f_j`.

Then

`p=c*E^2*O`.

### Theorem `noInteriorOddRoot_of_nonneg`

If a real polynomial is nonnegative on `[a,b]`, then every root in `(a,b)` has even multiplicity. Equivalently the endpoint-stripped odd kernel has Sturm count zero.

### Theorem `nonnegOn_interval_iff_oddSturm_zero_and_positive_anchor`

Let `p in Q[X]`, `p!=0`, `a<b in Q`. Let `O_int` be the endpoint-stripped odd kernel of a verified squarefree decomposition of `p`. If `r in Q`, `a<r<b`, `p(r)!=0`, then

`(forall x:R, a<=x -> x<=b -> eval x p >=0)`

iff

`SturmCount(O_int,a,b)=0` and `eval r p >0`.

The reverse implication uses the parity factorization; the forward implication uses sign change at odd multiplicity and density of rationals only to obtain an anchor if one was not supplied.

### Theorem `oddInteriorRoot_gives_rational_negative_witness`

If the endpoint-stripped odd kernel has positive Sturm count on `(a,b)`, then there exists `r in Q` with `a<r<b` and `p(r)<0`.

For an executable theorem, carry a rational isolating interval around one odd root and exact root-count facts for the radical of `p`.

### Theorem `finiteGrid_anchor_exists`

For nonzero `p` of degree `d`, among

`a+(b-a)k/(d+2)`, `1<=k<=d+1`,

at least one evaluation is nonzero.

Combining this theorem with the previous one removes any search oracle from the checker interface.

---

## 11. Boundaries intentionally left open

This child solves only exact-real **univariate rational-polynomial** interval nonnegativity.

It does not by itself prove that a deployed P5 quantity really reduces to the radial polynomial `A(q)`, that `0<=Q(u)<=R` covers the physical domain, that stored binary64 coefficients equal the rational coefficients, or that a trajectory/FD halo lies in the source region. Those remain source/coverage semantics.

It also does not claim a Lean compile receipt. A Lean implementation would need polynomial multiplicity/squarefree and Sturm/root-count infrastructure or a small verified checker layer. Until then this is a mathematical theorem packet only.

For multivariate residuals that do not reduce to one radial variable, this theorem is not a substitute for the binary/ternary quartic or quotient-Gram lanes.

---

## 12. Requested next step

For the mathematics lane, the natural next seam is no longer zero-margin radial sign. That layer is decision-complete over `Q[q]`.

The next substantive question is **source realization**: whether the actual signed homogeneous allocation produced upstream can be reduced exactly to a rational `A(q)` on a same-key radial interval. If it can, T-P5-265 + T-P5-266 give a complete strict/touching interval consumer. If it cannot because coefficients depend on an additional cell parameter, the next mathematical child should be a two-variable structured certificate rather than another univariate inequality lemma.
