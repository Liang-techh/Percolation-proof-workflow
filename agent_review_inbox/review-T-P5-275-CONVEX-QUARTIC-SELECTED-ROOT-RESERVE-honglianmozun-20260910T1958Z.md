---
kind: review_result
review_id: review-T-P5-275-convex-quartic-selected-root-reserve-honglianmozun-20260910T1958Z
task_id: T-P5-275-CONVEX-QUARTIC-SELECTED-ROOT-RESERVE
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T19:58:00Z
claim_commit: fa09959ff04f23e6791ceead0954706d05ee63b7
inspected_commit: 56de3ef838de245f9863682a1a1525bd267588c4
upstream_commits:
  - 7409c5142691c1e3c220e7c5cf5d2864a1a26966 # T-P5-274 cubic inner-fiber sharp reserve
  - 2452690d4c89057795bd9c3b27b6974cc304ccac # T-P5-273 nested semialgebraic fiber elimination
  - 2a5617c335f912dda8ff720a9354e0f5b548740a # T-P5-272 finite Boolean one-fiber arrangement
  - 28be4ab630470caae390cfef4b534a0c96091076 # T-P5-271 multicomponent semialgebraic fiber decomposition
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_convex_quartic_min_dispatch; add_quartic_stationary_remainder_identity; add_selected_root_sturm_tarski_reserve_gate; add_rational_moving_endpoint_wrapper; add_quartic_contact_discriminant_classifier; preserve_unique_root_convexity_and_source_binding_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact ordered-field derivation; symbolic identity sanity check; exact rational regression calculations; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-275 — Convex quartic selected-root reserve

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-274 closed the cubic inner-fiber case by exploiting the fact that a cubic has only one local minimum. Its next explicitly open seam was a quartic slack with a certified convexity condition on the active inner interval.

This review proves that this quartic branch also admits an exact one-dimensional closure without numerical root finding and without a blind jump to general CAD.

For

`p(t)=a4 t^4+a3 t^3+a2 t^2+a1 t+a0`

on a closed interval `[ell,r]`, assume the genuinely quartic branch `a4 != 0` and a certified convexity gate

`p''(t)>=0  for every t in [ell,r]`.

Then `g=p'` is nondecreasing on the fiber. Therefore the minimum of `p` is exactly one of:

1. the left endpoint when `g(ell)>=0`;
2. the right endpoint when `g(r)<=0`;
3. the **unique selected critical root** `tau in (ell,r)` when `g(ell)<0<g(r)`.

The new algebraic identity is that at every critical root the quartic reserve reduces to a **quadratic** polynomial. For a requested reserve `eta`, define

`q_eta(t)=p(t)-eta`,

`H_eta(t)`

`=(8 a4 a2-3 a3^2)t^2`

` +(12 a4 a1-2 a3 a2)t`

` +(16 a4(a0-eta)-a3 a1)`,

and

`K_eta(t)=a4 H_eta(t)`.

Then the exact polynomial identity

**(0.1)**

`16 a4 q_eta(t)-H_eta(t)=(4 a4 t+a3) g(t)`

implies, at any critical root `g(tau)=0`,

**(0.2)**

`16 a4^2 q_eta(tau)=K_eta(tau)`.

Because `16 a4^2>0`, the sign of the true Lyapunov reserve at the selected quartic minimizer is exactly the sign of one quadratic expression `K_eta(tau)`.

The remaining selected-root sign can be decided **fraction-free** by a Sturm–Tarski signed-subresultant query. In the interior branch there is exactly one distinct root of `g` in `(ell,r)`, so

`TaQ_(ell,r)(K_eta,g)=sign(K_eta(tau)) in {-1,0,1}`.

Hence the interior branch is safe exactly when this Tarski query is nonnegative. The query is computed from polynomial additions/multiplications, signed pseudo-remainders/subresultants, and endpoint sign evaluations; no radical for the cubic root `tau` is evaluated.

Thus a certified-convex quartic extends the T-P5-274 exact chain by one degree while still returning finite polynomial/sign data to the T-P5-272 outer arrangement.

No actual P5 quartic target, source key, endpoint packet, cell/domain realization, trajectory/FD/reference-halo coverage, Float64/libm semantics, Lean/kernel proof, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let

`p(t)=a4 t^4+a3 t^3+a2 t^2+a1 t+a0`

with `a4 != 0`, and let `eta` be the desired lower reserve.

Write

`q_eta(t)=p(t)-eta`,

`g(t)=p'(t)=4a4 t^3+3a3 t^2+2a2 t+a1`,

`c(t)=p''(t)=12a4 t^2+6a3 t+2a2`.

Assume

`ell < r`

and

**(Cvx)** `c(t)>=0` on `[ell,r]`.

The convexity premise itself is only a quadratic interval nonnegativity statement. Therefore, when coefficients/endpoints are rational or rational functions on a regular outer cell, it can be discharged by the already existing exact quadratic interval machinery from T-P5-273. No new quartic-specific convexity solver is needed.

If `a4=0`, the problem degree-drops to T-P5-274 and must be routed there rather than pretending the quartic identities remain nondegenerate.

---

## 2. Lemma — convexity gives a unique selected critical root

Under **(Cvx)**, `g'=c>=0`, hence `g` is nondecreasing on `[ell,r]`.

A nonzero polynomial that is nondecreasing on an interval cannot have two distinct zeros in that interval unless it vanishes on the whole segment between them. If `x<y` and `g(x)=g(y)=0`, monotonicity forces

`0=g(x)<=g(t)<=g(y)=0`

for every `t in [x,y]`, so `g` vanishes on infinitely many points and is the zero polynomial. That contradicts `a4 != 0`.

Therefore `g` has at most one distinct root on `[ell,r]`.

Consequently the three branches below are exhaustive:

### LEFT

If `g(ell)>=0`, then monotonicity gives `g(t)>=0` on the whole interval. Hence `p` is nondecreasing and

`min_[ell,r] p = p(ell)`.

### RIGHT

If `g(r)<=0`, then `g(t)<=0` on the whole interval. Hence `p` is nonincreasing and

`min_[ell,r] p = p(r)`.

### INTERIOR

If

`g(ell)<0<g(r)`,

continuity gives a root `tau in (ell,r)`, and the uniqueness argument above shows that it is the only one. Since `g` changes from nonpositive to nonnegative across `tau`,

`min_[ell,r] p = p(tau)`.

This remains valid in the flat-curvature case where `p''(tau)=0`; for example `p=t^4` has the repeated derivative root `tau=0`. Strict convexity is not required.

---

## 3. Theorem A — exact convex-quartic minimum dispatcher

Under `a4 != 0`, `ell<r`, and **(Cvx)**,

`p(t)>=eta for every t in [ell,r]`

is equivalent to exactly one of the following branch conditions.

### A1. LEFT branch

`g(ell)>=0`

and

`p(ell)>=eta`.

### A2. RIGHT branch

`g(ell)<0`, `g(r)<=0`

and

`p(r)>=eta`.

The explicit `g(ell)<0` makes this branch disjoint from LEFT; it is logically redundant after branch ordering but useful for a deterministic checker.

### A3. INTERIOR branch

`g(ell)<0<g(r)`

and

`p(tau)>=eta`,

where `tau` is the unique root of `g` in `(ell,r)`.

No endpoint reserve check is additionally necessary in A3: once the selected interior minimum is above `eta`, convexity implies every endpoint is above `eta` automatically.

### Proof

Section 2 identifies the exact global minimizer in every branch. Lower-bounding `p` on the entire compact interval is therefore equivalent to lower-bounding that unique minimizer. QED.

---

## 4. Theorem B — quartic stationary reserve collapses to a quadratic

Define

`H_eta(t)`

`=(8 a4 a2-3 a3^2)t^2`

` +(12 a4 a1-2 a3 a2)t`

` +(16 a4(a0-eta)-a3 a1)`.

Then the following identity holds for every `t`:

**(4.1)**

`16 a4 q_eta(t)-H_eta(t)`

`=(4 a4 t+a3) g(t)`.

### Proof

Expand the right side:

`(4a4 t+a3)(4a4 t^3+3a3 t^2+2a2 t+a1)`.

Its coefficients are

- `t^4`: `16a4^2`;
- `t^3`: `16a4 a3`;
- `t^2`: `8a4 a2+3a3^2`;
- `t`: `4a4 a1+2a3 a2`;
- constant: `a3 a1`.

Subtracting this from `16a4 q_eta` leaves exactly the three coefficients defining `H_eta`. QED.

At any critical root `g(tau)=0`, (4.1) gives

`16 a4 q_eta(tau)=H_eta(tau)`.

Multiplying by `a4` gives the sign-safe form

**(4.2)**

`16 a4^2 q_eta(tau)=K_eta(tau)`,

where

`K_eta=a4 H_eta`.

The left coefficient `16a4^2` is strictly positive regardless of the sign of `a4`. Hence

**(4.3)**

`p(tau)>=eta  <->  K_eta(tau)>=0`.

This avoids a separate `sign(a4)` branch and is the checker-facing form.

---

## 5. Theorem C — selected-root Sturm–Tarski reserve gate

For real polynomials `Q,P`, define the Tarski query over an open interval by

`TaQ_(ell,r)(Q,P)`

`:= sum_{x in (ell,r), P(x)=0} sign(Q(x))`,

where each **distinct** real root is counted once.

The Sturm–Tarski theorem computes this integer exactly as the Cauchy index

`Ind_ell^r( P'(t) Q(t) / P(t) )`,

and that Cauchy index is computable by the signed Sturm/Habicht or signed-subresultant remainder sequence. No algebraic root needs to be represented numerically.

Now enter the INTERIOR branch of Theorem A. There is exactly one distinct root `tau` of `g` in `(ell,r)`. Therefore

**(5.1)**

`TaQ_(ell,r)(K_eta,g)=sign(K_eta(tau))`.

Combining with (4.3),

**(5.2)**

`p(tau)>=eta`

`<-> TaQ_(ell,r)(K_eta,g)>=0`.

Thus the complete INTERIOR certificate is

`g(ell)<0<g(r)`

and

`TaQ_(ell,r)(K_eta,g)>=0`.

The three possible query values have direct meaning:

- `+1`: strict positive reserve at the selected minimizer;
- `0`: exact interior contact `p(tau)=eta`;
- `-1`: a genuine algebraic negative reserve at the selected minimizer.

A physical/source FAIL still requires the ordinary state-realization and coverage obligations before propagation.

### Why repeated critical roots are not a problem

Convexity allows a repeated derivative root such as `g=t^3`. The Tarski query is over distinct roots, and the Cauchy-index form remains valid: locally `g'/g` has a simple pole with positive multiplicity factor, so the index records `sign(K_eta(tau))`, not the multiplicity. No squarefree-root extraction is mathematically required for the statement.

---

## 6. Fraction-free rational moving endpoints

Suppose on one regular outer cell

`ell=Nl/Dl`, `r=Nr/Dr`,

with certified

`Dl>0`, `Dr>0`,

and

`Nr Dl-Nl Dr>0`.

Then all branch endpoint signs can be cleared without changing orientation.

Define

`G_l := Dl^3 g(ell)`

`=4a4 Nl^3+3a3 Nl^2 Dl+2a2 Nl Dl^2+a1 Dl^3`,

`G_r := Dr^3 g(r)`

`=4a4 Nr^3+3a3 Nr^2 Dr+2a2 Nr Dr^2+a1 Dr^3`.

Define reserve numerators

`E_l := Dl^4 (p(ell)-eta)`

`=a4 Nl^4+a3 Nl^3 Dl+a2 Nl^2 Dl^2+a1 Nl Dl^3+(a0-eta)Dl^4`,

and analogously `E_r`.

Because `Dl,Dr>0`,

`sign G_l = sign g(ell)`,

`sign G_r = sign g(r)`,

`sign E_l = sign(p(ell)-eta)`,

`sign E_r = sign(p(r)-eta)`.

Therefore the endpoint part of the dispatcher is entirely fraction-free.

For the INTERIOR Tarski query, every signed-remainder/subresultant polynomial is evaluated at `Nl/Dl` and `Nr/Dr`. Multiplying an evaluation by a sufficiently high positive power of `Dl` or `Dr` clears its denominator without changing sign. Hence rational moving endpoints introduce no radical and no floating-point comparison.

---

## 7. Parametric outer-cell elimination

Now allow `a4,...,a0,eta,Nl,Dl,Nr,Dr` to be rational functions of an outer parameter `q`, with all relevant denominator signs fixed on one regular `q`-cell.

The exact dispatcher still reduces to finitely many polynomial sign atoms in `q`.

The projection data required are:

1. coefficient/denominator leading terms and degree-drop atoms;
2. the quadratic convexity packet for `p''`;
3. `G_l,G_r,E_l,E_r`;
4. the signed principal subresultant/Sturm-Habicht coefficients needed by the Tarski query for `(g,K_eta)`;
5. endpoint evaluations of the signed remainder sequence;
6. optional contact resultant/discriminant data from Section 8.

After clearing certified positive denominators, these are all polynomials in `q`.

Add their nonzero factors to the T-P5-272 common one-dimensional arrangement. On every connected regular `q`-cell where none of the branch-defining projection factors vanishes, the degree pattern, endpoint signs, subresultant sign variation, Tarski query, and therefore quartic safety truth are constant.

At a zero of a projection factor, the corresponding `q` value is retained as a zero-dimensional point cell and the specialized lower-degree/degenerate polynomial problem is recomputed exactly. Such points must not be discarded as measure-zero.

Therefore a convex quartic inner fiber does **not** force general bivariate CAD: it produces a finite Boolean polynomial-sign formula consumable by the T-P5-272 outer arrangement.

---

## 8. Contact classifier and quartic discriminant

The selected-root sign requires Sturm–Tarski information, but exact **contact** has an additional useful resultant identity.

Let `Disc(q_eta)` be the ordinary quartic discriminant. Then

**(8.1)**

`Res_t(g,K_eta)=256 a4^5 Disc(q_eta)`.

In particular, because `a4 != 0`,

`Res_t(g,K_eta)=0`

if and only if

`Disc(q_eta)=0`.

### Proof sketch

From (4.1), at every root `rho` of `g`,

`K_eta(rho)=16 a4^2 q_eta(rho)`.

Using the root-product formula for the two resultants and `lc(g)=4a4`, one obtains

`Res(g,K_eta)=256 a4^4 Res(g,q_eta)`.

For a quartic, `Res(q_eta,q_eta')=a4 Disc(q_eta)`, and degree parity gives `Res(g,q_eta)=Res(q_eta,g)`. Combining yields (8.1).

The equality extends through coefficient specializations by polynomial identity.

Thus an interior zero reserve is an ordinary quartic discriminant contact. However, the **sign** of the selected reserve is not determined by the global discriminant/resultant sign; Section 10 gives an exact counterexample.

---

## 9. Deterministic checker order

A fail-closed exact checker can use the following branch order.

1. Validate coefficient/endpoint denominator orientation and `ell<r`.
2. If `a4=0`, delegate to the T-P5-274 cubic dispatcher.
3. Prove `p''>=0` on the entire active inner interval using the exact quadratic interval checker.
4. Compute fraction-free `G_l,G_r,E_l,E_r`.
5. If `G_l>=0`, return PASS exactly when `E_l>=0`.
6. Else if `G_r<=0`, return PASS exactly when `E_r>=0`.
7. Else convexity forces `G_l<0<G_r`; construct `K_eta` and compute the exact signed-subresultant Tarski query.
8. Return PASS exactly when `TaQ>=0`.
9. If `TaQ=0`, record `Res(g,K_eta)=0` / `Disc(q_eta)=0` as the interior-contact classifier.
10. If the convexity certificate, denominator orientation, or specialized subresultant branch is missing, return `CERTIFICATE_NOT_FOUND / SOURCE_BINDING_REQUIRED`, not mathematical FAIL.

The only mathematical negative witness in the interior branch is `TaQ=-1`, which proves `p(tau)<eta` for the unique algebraic minimizer `tau`. Propagating that to a physical P5 failure still requires the normal source/state/coverage witnesses.

---

## 10. Sharp regression: global resultant cannot select the active convex root

Consider the rational quartic

`p(t)=t^4/4-t^3/3-t^2+2`.

Then

`g(t)=p'(t)=t(t+1)(t-2)`,

`p''(t)=3t^2-2t-2`.

Take `eta=0`.

### Left convex interval

Let

`I_L=[-2,-3/4]`.

On this interval `p''` is strictly positive; its minimum occurs at the right endpoint and equals

`p''(-3/4)=19/16>0`.

The unique critical root in `I_L` is `tau_L=-1`, with

`p(-1)=19/12>0`.

The endpoints are also positive:

`p(-2)=14/3`,

`p(-3/4)=1697/1024`.

Hence `p>=0` on `I_L`.

### Right convex interval

Let

`I_R=[5/4,3]`.

Again `p''` is strictly positive; its minimum on this interval is

`p''(5/4)=3/16>0`.

The unique critical root is `tau_R=2`, but

`p(2)=-2/3<0`.

Both endpoints are positive:

`p(5/4)=1219/3072`,

`p(3)=17/4`.

Hence this interval is unsafe **only because of the selected interior minimizer**.

For this same quartic, independent of which interval is being queried,

`Disc(p)=-76/9`,

and

`Res(g,K_0)=-19/9`.

Therefore a global resultant/discriminant sign has identical value for the safe left fiber and the unsafe right fiber. It cannot replace the selected-root Sturm–Tarski query.

This is the key reason the interval selection data must remain part of the certificate.

---

## 11. Sharp obstruction: uniqueness/convexity cannot be dropped

Use the same quartic on the larger interval

`[-2,3]`.

The endpoints remain positive, but convexity fails because

`p''(0)=-2<0`.

The derivative has three distinct roots

`-1, 0, 2`,

with reserve signs

`sign p(-1)=+1`,

`sign p(0)=+1`,

`sign p(2)=-1`.

Therefore the raw Tarski sum over all critical roots is

`TaQ(K_0,g)=+1+1-1=+1`.

A naive rule `TaQ>=0 => safe` would falsely PASS, even though `p(2)=-2/3`.

Thus the selected-root query is exact **only after** convexity/monotonicity has proved there is exactly one critical root in the active interval. This gate is structural, not cosmetic.

---

## 12. Structural fingerprint

The new quartic branch has the following reusable form:

`quartic Lyapunov slack`

`-> exact quadratic convexity certificate for p''`

`-> monotone derivative`

`-> endpoint-or-unique-critical-root minimizer`

`-> quartic critical reserve reduced modulo p' to quadratic K_eta`

`-> one selected-root Sturm–Tarski sign query`

`-> fraction-free signed-subresultant certificate`

`-> finite outer polynomial-sign arrangement`.

The important point is that the quartic is not attacked as an arbitrary degree-four optimization problem. Convexity converts the nonlinear energy check to one algebraically selected critical branch, and Euclidean division by the derivative lowers the reserve polynomial from degree four to degree two before sign determination.

---

## 13. Candidate theorem decomposition for Lean / checker formalization

A minimal decomposition should keep calculus, ring identities, and real-algebraic sign machinery separate.

1. `quartic_stationary_remainder_identity`
   - pure ring identity (4.1).

2. `convex_derivative_monotone`
   - from `forall t in Icc ell r, 0<=p'' t`, prove `MonotoneOn p'`.

3. `monotone_polynomial_unique_zero`
   - if nonzero polynomial `g` is monotone on an interval, two distinct zeros are impossible.

4. `convex_quartic_min_left`
   - `g ell>=0 -> min=p ell`.

5. `convex_quartic_min_right`
   - `g r<=0 -> min=p r`.

6. `convex_quartic_unique_interior_min`
   - `g ell<0<g r -> exists! tau in Ioo ell r, g tau=0`, and `p tau<=p t` on the interval.

7. `quartic_critical_reserve_iff_K_nonneg`
   - from `g tau=0`, prove `eta<=p tau <-> 0<=K_eta tau`.

8. `tarski_query_single_root_eq_sign`
   - generic real-polynomial theorem: one distinct root in an open interval turns the Tarski query into the sign at that root.

9. `convex_quartic_lower_iff_tarski_dispatch`
   - combine 4–8.

10. `quartic_contact_resultant_discriminant`
    - pure resultant/discriminant identity (8.1).

11. rational-endpoint wrapper
    - denominator-cleared `G_l,G_r,E_l,E_r`.

12. degree-drop wrapper
    - `a4=0` delegates to T-P5-274.

If Mathlib lacks a convenient Sturm–Tarski implementation, theorem 8 should remain a checker-side exact algebraic lemma rather than replacing it with floating algebraic-root evaluation.

---

## 14. Failure boundaries

The following are genuine mathematical/certificate distinctions.

### Mathematical negative witness

After all structural premises are proven:

- LEFT with `E_l<0` gives an explicit rational endpoint violation;
- RIGHT with `E_r<0` gives an explicit rational endpoint violation;
- INTERIOR with exact `TaQ=-1` proves the unique algebraic minimizer has `p(tau)<eta`.

These are algebraic failures on the declared fiber. Physical propagation still requires state/source realization and coverage.

### Certificate/source obstruction, not mathematical FAIL

Return inconclusive rather than FAIL if any of the following is absent:

- proof that `a4` and coefficient denominators have the declared specialized values;
- positive endpoint denominator orientation;
- proof that `p''>=0` on the whole active fiber;
- the active interval/source-cell identity;
- enough subresultant branch data to evaluate the Tarski query exactly;
- actual target not known to be quartic in the selected fiber variable;
- source/target key mismatch;
- outer point-cell specialization not handled.

### Do not use a global resultant sign as a substitute

`Res(g,K_eta)` is a contact detector, not a selected-root sign detector. Section 10 gives a strict rational separation.

### Do not sum over several critical roots

Without the convexity/unique-root premise, `TaQ>=0` can falsely PASS. Section 11 gives a strict rational counterexample.

---

## 15. What this child changes

Before this review, the exact nested-elimination chain had a clean cubic rule but the next quartic step appeared to require either explicit cubic radicals or a general algebraic optimizer.

The new result isolates a broad structurally useful quartic class:

- convexity is itself only a quadratic interval certificate;
- the quartic derivative then has at most one active critical root;
- the reserve at that root reduces from quartic to quadratic modulo the derivative;
- a single Sturm–Tarski query determines its sign exactly;
- rational moving endpoints and outer parameters remain fraction-free after the usual sign-cell refinement.

Thus **certified-convex quartic inner fibers remain inside the same finite one-dimensional semialgebraic architecture as T-P5-272–274.**

---

## 16. Remaining obligations

Still open:

1. determine whether the actual P5 target/slack is quartic in any useful inner fiber variable;
2. bind `a4,...,a0,eta` and endpoint data to one actual source key/evaluator;
3. prove the convexity certificate on the exact same source fiber;
4. prove positive rational endpoint denominator orientation and interval ordering on every active cell;
5. instantiate the signed-subresultant/Tarski query with a pinned exact checker representation;
6. construct the synchronized T-P5-272 outer arrangement including subresultant degree-drop/contact factors;
7. preserve strict/weak/equality source semantics and singular point cells;
8. state/trajectory realization of any negative selected algebraic witness;
9. whole-sheet/flowpipe/FD-halo/reference-halo coverage;
10. Float64/libm/interval semantics where deployed evaluation is floating point;
11. Lean/kernel formalization;
12. independent validation by 封不觉;
13. admission, registry mutation, and P5/P8/M4 propagation.

---

## 17. Next nonduplicative mathematical seam

Two next steps are natural, but they should remain disjoint from work already owned by other agents.

The highest-value continuation for this lane is **algebraic moving endpoints for the convex quartic selected root**: combine T-P5-270 Thom-selected endpoint branches with the present monotone-cubic critical root, and decide `ell(q)<tau(q)<r(q)` plus `K_eta(tau)>=0` by a common signed-subresultant/Thom packet without converting all three algebraic roots into a general bivariate CAD.

A second, more energy-specific continuation is a **convexity reserve perturbation theorem**: if `p''>=mu>0` and coefficient/FD errors perturb both `g` and `p` by certified caps, derive an explicit lower-bound degradation for the selected minimum before rerunning the full algebraic arrangement. That would turn strict quartic Lyapunov margin into a reusable numerical-error budget.

For the present child, however, the exact convex-quartic mathematical closure is complete subject to the explicitly listed source/checker/formalization obligations.