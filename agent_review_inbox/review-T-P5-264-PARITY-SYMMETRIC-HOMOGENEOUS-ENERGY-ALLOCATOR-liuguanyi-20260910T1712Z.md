---
kind: review_result
review_id: review-T-P5-264-parity-symmetric-homogeneous-energy-allocator-liuguanyi-20260910T1712Z
task_id: T-P5-264-PARITY-SYMMETRIC-HOMOGENEOUS-ENERGY-ALLOCATOR
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T17:12:00Z
claim_commit: 043ca3c9a201dc44bb549efd47c215352c4c8614
inspected_commit: c2bc716919d62ba984a02eda8e16c4bcced824ca
upstream_commits:
  - f4704792f1420aef65ad19af2e03ece571bf494e  # T-P5-263 higher-degree matched-metric Banach polarization
  - f17933375d1275a5ad9ecff9bf810d0678e5c113  # T-P5-261 matched-metric polarization
  - 7a684d6d780bc287bd62ffab96d4db3897767851  # T-P5-262 rational AM-GM metric bridge
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_parity_reflection_energy_identity; add_minimax_degree_allocator; add_rational_weighted_fallback; add_same_parity_cross_energy_contract; add_fail_closed_nonhomogeneous_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: finite-dimensional Hilbert algebra, homogeneous scaling, weighted Cauchy-Schwarz/Young inequalities, exact one-dimensional regressions; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-264 — Parity-symmetric homogeneous energy allocator for nonhomogeneous polynomial remainders

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-263 closes the matched-metric problem for a *single* homogeneous component `P_d`. A deployed polynomial remainder is generally nonhomogeneous,

`P(u)=sum_{d in D} P_d(u)`,

so the remaining mathematical issue is how the degreewise energy certificates may be combined without inventing cancellation that is not uniform on a centered symmetric source ball.

This child proves five facts.

1. The full squared energy has a canonical decomposition by **total degree**. Under reflection `u -> -u`, every odd-total-degree energy layer changes sign and every even-total-degree layer is fixed.
2. Equivalently, if `E` and `O` are the sums of the even- and odd-degree vector components, then

   `max(||P(u)||^2,||P(-u)||^2)=||E(u)||^2+||O(u)||^2+2|<E(u),O(u)>`.

   Therefore a negative even/odd cross term at one point cannot be spent as a uniform reserve on a symmetric source set.
3. If the only information retained from each degree is

   `||P_d(u)||^2 <= kappa_d Q(u)^d`,

   then the ordinary triangle allocation on `Q(u)<=R` is not merely sufficient; its constant

   `K_*=(sum_d sqrt(kappa_d R^(d-1)))^2`

   is **minimax sharp** over all polynomial packets consistent with those degreewise constants.
4. Square roots need not appear in an exact certificate. For any positive rational weights `omega_d` with `sum omega_d=1`,

   `||P(u)||^2 <= Q(u) sum_d kappa_d R^(d-1)/omega_d`.

   The infimum over weights is exactly `K_*`; under a strict Lyapunov margin, rational weights can approximate the optimizer closely enough to preserve PASS.
5. Actual symbolic cancellation should not be discarded. Same-parity blocks and, more canonically, contributions of the same total degree can be aggregated before any absolute-value/Young allocation. This yields a typed cross-energy interface that stays rational because same-parity total degrees are even.

No actual deployed P5 polynomial, source ball, metric, cell/trajectory coverage, Float64 semantics, interval enclosure, Lean/kernel proof, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let `V=R^r`, let `W=W^T>0`, and define

`Q(u)=u^T W u`.

Let `H` be a finite-dimensional real Hilbert output space. Fix a finite degree set

`D subset {1,2,...}`

and homogeneous polynomial maps

`P_d : V -> H`,  `P_d(tu)=t^d P_d(u)`.

Define the nonhomogeneous remainder

**(1.1)** `P(u)=sum_{d in D} P_d(u)`.

For every active degree assume a T-P5-263-style realized-direction energy bound

**(1.2)** `||P_d(u)||^2 <= kappa_d Q(u)^d`,  `kappa_d>=0`.

The centered source ball is

**(1.3)** `B_R={u: Q(u)<=R}`,  `R>0`.

If `kappa_d=0`, (1.2) forces `P_d=0`; such degrees may be deleted. Below `D_+` denotes the remaining active degrees.

---

## 2. Canonical total-degree energy layers

For every integer `n>=2`, define the ordered-pair energy layer

**(2.1)**

`H_n(u) := sum_{d,e in D, d+e=n} <P_d(u),P_e(u)>`.

Because the sum is over ordered pairs, no extra factor of two is needed. Expanding the squared Hilbert norm gives the exact identity

**(2.2)** `||P(u)||^2 = sum_n H_n(u)`.

Each summand in `H_n` has homogeneous degree `d+e=n`, hence

**(2.3)** `H_n(tu)=t^n H_n(u)`

and in particular

**(2.4)** `H_n(-u)=(-1)^n H_n(u)`.

Thus `n` is the intrinsic type key for energy cancellation: every algebraic cancellation among different degree pairs with the same `d+e=n` survives radial rescaling exactly.

### Example: cancellation that a degreewise triangle bound would destroy

In one dimension take scalar output

`P_1(x)=x`, `P_2(x)=x^2`, `P_3(x)=-(1/2)x^3`.

The total-degree-four layer is

`H_4=P_2^2+2 P_1 P_3=x^4-x^4=0`

identically. Bounding `P_2^2` and `2P_1P_3` separately by absolute values would charge a fictitious degree-four debit. The correct interface should simplify or certify `H_4=0` before allocation.

---

## 3. Even/odd reflection theorem

Define the parity blocks

**(3.1)**

`E(u)=sum_{d even} P_d(u)`,

`O(u)=sum_{d odd} P_d(u)`.

Then

`E(-u)=E(u)`, `O(-u)=-O(u)`,

so

**(3.2)** `P(u)=E(u)+O(u)`,

**(3.3)** `P(-u)=E(u)-O(u)`.

The parallelogram identity yields

**(3.4)**

`[||P(u)||^2+||P(-u)||^2]/2 = ||E(u)||^2+||O(u)||^2`.

Subtracting the two energies gives

**(3.5)**

`[||P(u)||^2-||P(-u)||^2]/2 = 2 <E(u),O(u)>`.

Hence the exact paired worst case is

**(3.6)**

`max(||P(u)||^2,||P(-u)||^2)`

`= ||E(u)||^2+||O(u)||^2+2 |<E(u),O(u)>|`.

In the total-degree language,

**(3.7)**

`sum_{n even} H_n = ||E||^2+||O||^2`,

`sum_{n odd} H_n = 2<E,O>`.

### Consequence: cross-parity signed cancellation is not a uniform reserve

Because `B_R` is centered, `u in B_R` iff `-u in B_R`. If `<E,O><0` at `u`, then the same cross contribution is positive at `-u`. Therefore a uniform upper bound on `B_R` cannot spend the *sign* of the even/odd cross term as negative reserve.

What may still be used is structural cancellation *inside* the aggregate cross term before its absolute value is taken. Equation (3.6) says precisely where the absolute value belongs: around the complete even/odd cross energy, not mechanically around every monomial.

### Exact rational regression

Take `V=H=R`, `Q(x)=x^2`, `R=1`,

`P_1(x)=x`, `P_2(x)=-x^2`.

At `x=1`, the components cancel and `P(1)=0`. But at the reflected point `x=-1`,

`P(-1)=-2`, so `|P(-1)|^2=4`.

Thus endpoint cancellation at one sign gives no symmetric-ball reserve. This same example will attain the minimax triangle constant below.

---

## 4. Degreewise-only allocator

From (1.2), for `u in B_R` with `q=Q(u)`,

`||P_d(u)|| <= sqrt(kappa_d) q^(d/2)`

`= sqrt(q) sqrt(kappa_d q^(d-1))`

`<= sqrt(q) sqrt(kappa_d R^(d-1))`.

Define

**(4.1)** `a_d := kappa_d R^(d-1)`.

Then the triangle inequality gives

**(4.2)**

`||P(u)|| <= sqrt(q) sum_d sqrt(a_d)`.

Therefore

**(4.3)**

`||P(u)||^2 <= K_* Q(u)`,

where

**(4.4)**

`K_* := (sum_{d in D_+} sqrt(a_d))^2`

`= (sum_d sqrt(kappa_d) R^((d-1)/2))^2`.

This is the natural bridge from multiple T-P5-263 homogeneous packets into one quadratic Lyapunov debit.

---

## 5. Theorem — the triangle constant is minimax sharp if only degreewise constants are known

The constant (4.4) cannot be improved by any universal allocator whose only mathematical inputs are `R` and the separate constants `kappa_d`.

### Proof

It is enough to exhibit one admissible family attaining equality.

Take one-dimensional source and scalar output, with `W=1`. For every active degree let

**(5.1)** `P_d(x)=sqrt(kappa_d) x^d`.

Then

`|P_d(x)|^2 = kappa_d |x|^(2d)=kappa_d Q(x)^d`,

so every degreewise premise (1.2) is saturated.

At the positive boundary point `x=sqrt(R)`, all components point in the same output direction and have the same sign. Hence

`|P(sqrt(R))|^2`

`= (sum_d sqrt(kappa_d) R^(d/2))^2`

`= R (sum_d sqrt(kappa_d)R^((d-1)/2))^2`

`= K_* Q(sqrt(R))`.

So any purported universal constant `K<K_*` fails on this admissible packet. QED.

### Interpretation

If a consumer throws away all cross-degree information and keeps only the separate `kappa_d`, there is no theorem-level trick that beats triangle allocation. Improvement requires **additional mathematical data**: exact source coefficients, parity-block energy identities, same-total-degree cancellation, angular restrictions, parameter signs, or another source-specific cross-energy certificate.

The symmetric-domain parity theorem does not lower this minimax constant: the positive boundary point already aligns all degree components.

---

## 6. Fraction-free / square-root-free rational weighted fallback

Although `K_*` is the sharp real constant, an exact checker need not serialize square roots.

Choose positive weights

`omega_d>0`, `sum_d omega_d=1`.

Weighted Hilbert-space Cauchy-Schwarz gives

**(6.1)**

`||sum_d P_d||^2 <= sum_d ||P_d||^2 / omega_d`.

Using (1.2) and `q<=R`,

`||P_d(u)||^2/omega_d`

`<= (kappa_d/omega_d) q^d`

`<= q [kappa_d R^(d-1)/omega_d]`.

Thus

**(6.2)**

`||P(u)||^2 <= K_omega Q(u)`,

with

**(6.3)** `K_omega := sum_d a_d/omega_d`.

If `R`, every `kappa_d`, and every `omega_d` are rational, then `K_omega` is rational. No square root, whitening map, eigendata, or algebraic-number serialization is required.

### Optimality of the weighted family

Cauchy-Schwarz gives

`(sum_d sqrt(a_d))^2`

`= (sum_d sqrt(a_d/omega_d) sqrt(omega_d))^2`

`<= (sum_d a_d/omega_d)(sum_d omega_d)`

`=K_omega`.

Hence

**(6.4)** `inf_{omega in simplex} K_omega = K_*`.

Equality holds exactly when, for active degrees,

**(6.5)** `omega_d proportional sqrt(a_d)`.

### Strict-margin rationalization theorem

Suppose a downstream Lyapunov budget can tolerate any `K<Gamma` and the sharp real constant satisfies

`K_*<Gamma`.

The positive rational simplex is dense in the positive real simplex and `omega -> K_omega` is continuous away from zero coordinates. Therefore there exists a **rational** weight vector with

**(6.6)** `K_omega<Gamma`.

Thus strict PASS can always be serialized with rational weights even when the exact optimizer (6.5) is irrational.

Boundary warning: if `K_*=Gamma` and the unique optimal weights are irrational, rational approximations only approach equality from above. A zero-reserve proof then needs the exact algebraic optimizer or a different exact certificate; it must not round an approximate weight and claim equality.

### Simple all-rational default

With `m=|D_+|`, choosing `omega_d=1/m` gives

**(6.7)** `K_omega=m sum_d kappa_d R^(d-1)`.

This is generally less sharp but is a trivial square-root-free fallback.

---

## 7. Same-parity cancellation may be retained exactly

Reflection only destroys the *sign* of the cross energy between `E` and `O`. It does **not** require discarding cross terms within `E` or within `O`.

Indeed

**(7.1)**

`||E||^2 = sum_{d,e even} <P_d,P_e>`,

`||O||^2 = sum_{d,e odd} <P_d,P_e>`.

Every term in either sum has even total degree. Consequently every such term is reflection-even and its matched-metric model uses an integer power of `Q`.

A source-specific producer may therefore certify two rational radial envelopes

**(7.2)**

`||E(u)||^2 <= Q(u) A(Q(u))`,

`||O(u)||^2 <= Q(u) B(Q(u))`

for `0<=Q(u)<=R`, where `A` and `B` are rational polynomials or exact rational upper envelopes assembled from the even total-degree layers.

All signed same-parity cancellations are already contained in (7.2) and should not be replaced by componentwise absolute values.

For any `theta>0`, Young's inequality gives

`2<E,O> <= theta ||E||^2 + theta^(-1)||O||^2`.

Therefore

**(7.3)**

`||P(u)||^2`

`<= (1+theta)||E(u)||^2 + (1+theta^(-1))||O(u)||^2`

`<= Q(u)[(1+theta)A(Q(u))+(1+theta^(-1))B(Q(u))]`.

If `theta` is rational, this cross-parity allocation is again square-root-free.

This two-block allocator is strictly more informative than applying (6.1) to every degree whenever the producer has proved nontrivial same-parity cancellation.

---

## 8. Same-total-degree cancellation is the canonical symbolic layer

The finest safe algebraic preprocessing is the `H_n` decomposition from Section 2.

Suppose, for a fixed even `n`, a producer proves the aggregate matched-metric estimate

**(8.1)** `H_n(u) <= c_n Q(u)^(n/2)`.

The exponent `n/2` is an integer. If the source coefficients, `W`, and `c_n` are rational, (8.1) is a rational homogeneous polynomial inequality after denominator clearing.

Crucially, `H_n` must be formed **before** pairwise magnitude bounds. Distinct pairs `(d,e)` with the same `d+e=n` scale identically and may cancel as a polynomial identity, as in the `H_4=0` example of Section 2.

For an odd `n`, `H_n` is reflection-odd. A negative bound at `u` cannot be consumed as symmetric reserve because `H_n(-u)=-H_n(u)`. Odd layers should either be retained together inside the complete cross-parity aggregate

**(8.2)** `C_EO(u)=sum_{n odd} H_n(u)=2<E(u),O(u)>`

and then enclosed in absolute value, or be bounded by a verified two-sided/absolute source theorem.

### Typed mathematical contract

A loss-aware adapter should therefore distinguish:

- `degree_component(d,P_d,kappa_d)`: the T-P5-263 homogeneous diagonal certificate;
- `energy_layer(n,H_n)`: the exact sum of all ordered degree pairs with `d+e=n`;
- `parity_energy(even,E)` and `parity_energy(odd,O)`: exact vector sums, preserving all same-parity cross terms;
- `cross_parity_energy(C_EO=2<E,O>)`: reflection-odd as a whole;
- a final allocator chosen only after the above exact identities are available.

These are mathematical equalities/contracts, not provenance claims.

---

## 9. Important radial boundary: outer-radius cancellation is not uniform even within one parity

Parity alone is not enough to justify cancellation between *different* total degrees over the whole ball.

Take the scalar odd polynomial

**(9.1)** `P_1(x)=x`, `P_3(x)=-x^3`

on `|x|<=1`.

Both components are odd, so reflection preserves their mutual energy cross term. At the outer boundary,

`P(1)=P(-1)=0`.

But in the interior

**(9.2)** `P(x)^2=x^2(1-x^2)^2`.

For example at `x^2=1/3`,

`P(x)^2/x^2=(1-1/3)^2=4/9`.

Therefore a cancellation seen only at `Q=R` cannot be promoted to a uniform same-parity reserve.

The correct remedy is not to discard the cancellation, but to keep the exact radial polynomial

`Q(1-Q)^2`

and verify its bound on the entire interval `0<=Q<=R`.

This is why the `energy_layer(total_degree)` type is preferable to a single endpoint number.

---

## 10. Minimal downstream theorem statements

### Theorem A — reflection-safe parity energy

For any finite sum of homogeneous maps on a centered symmetric domain,

`max(||P(u)||^2,||P(-u)||^2)`

`=||E(u)||^2+||O(u)||^2+2|<E(u),O(u)>|`.

A uniform symmetric-domain proof may not use a negative sign of `<E,O>` as reserve.

### Theorem B — minimax degree allocator

If `||P_d(u)||^2<=kappa_d Q(u)^d` and `Q(u)<=R`, then

`||sum_d P_d(u)||^2 <= K_* Q(u)`

with

`K_*=(sum_d sqrt(kappa_d R^(d-1)))^2`.

No smaller constant follows from those degreewise premises alone.

### Theorem C — rational weighted certificate

For positive `omega_d` summing to one,

`||sum_d P_d(u)||^2 <= Q(u) sum_d kappa_d R^(d-1)/omega_d`.

If all data and weights are rational, the certificate is rational. Whenever `K_*<Gamma`, some rational weights satisfy the strict budget `<Gamma`.

### Theorem D — parity-block consumer

If source-specific exact mathematics proves

`||E||^2<=Q A(Q)`, `||O||^2<=Q B(Q)`

on `[0,R]`, then every rational `theta>0` gives

`||P||^2 <= Q[(1+theta)A(Q)+(1+theta^(-1))B(Q)]`.

This retains same-parity cancellation and spends no cross-parity sign.

---

## 11. Suggested exact consumer interface

A later implementation can serialize a nonhomogeneous packet as follows.

```text
homogeneous_sum_energy_packet:
  source_metric: W
  source_radius: R
  components:
    - degree: d
      polynomial: P_d
      diagonal_constant: kappa_d
      homogeneous_identity_checked: true/false
  optional_energy_layers:
    - total_degree: n
      exact_polynomial: H_n = sum_{d+e=n}<P_d,P_e>
      aggregate_bound: ...
  optional_parity_blocks:
    E = sum_{d even} P_d
    O = sum_{d odd} P_d
    E_energy_bound: Q*A(Q)
    O_energy_bound: Q*B(Q)
  allocator:
    kind: rational_weights | rational_parity_Young | exact_radial_polynomial
    rational_parameters: ...
  final_relative_budget: K or a verified radial expression
```

Required checker discipline:

- verify the homogeneous split as a polynomial identity;
- if only `kappa_d` are present, use Theorem B/C and do not invent cross-degree cancellation;
- if same-total-degree or parity-block data are present, verify their exact identities/bounds before consuming them;
- verify a radial polynomial on the full interval, not only at `R`, whenever signed contributions of different total degrees are retained;
- on a centered symmetric cell, never consume a negative even/odd cross sign without pairing `u` and `-u` or proving a stronger source restriction.

---

## 12. Fail-closed boundaries

1. **Centered symmetry is substantive.** If the true source cell is not invariant under `u -> -u`, Section 3 is not the right worst-case reduction. Then actual one-sided geometry may permit a signed cross-term reserve, but it requires a source-domain theorem.
2. **Degreewise constants do not encode direction.** Failure of the triangle/weighted budget is only `INCONCLUSIVE_FROM_DEGREEWISE_SUMMARY`; it is not a physical FAIL.
3. **Same-parity does not mean same scaling.** Cancellation between degrees `d` and `e` with the same parity but different total-energy powers must be checked over the radial interval.
4. **Negative high-order energy layers cannot automatically be converted to a constant quadratic reserve at `Q=R`.** Multiplying `Q^k<=R^(k-1)Q` by a negative coefficient reverses the inequality. Keep the signed radial polynomial or drop the negative contribution conservatively.
5. **Zero reserve is algebraically delicate.** Rational Young weights approximate the real optimum under strict margin; they do not certify an irrational sharp equality by rounding.
6. **No source split is inferred.** A deployed polynomial must actually be decomposed into homogeneous components in the same coordinates and same output metric before this theorem applies.
7. **No coverage is inferred.** A coefficient identity does not prove that the centered ball is the actual reachable/FD-halo/trajectory domain.

---

## 13. What this closes and the next mathematical seam

This child closes the abstract `sum of homogeneous degrees` allocator left open by T-P5-263:

- the reflection-safe even/odd identity is exact;
- triangle allocation is proved minimax sharp under degreewise-only information;
- strict certificates can remain rational through weighted Cauchy/Young parameters;
- source-specific same-parity and same-total-degree cancellations have a precise mathematical place where they can be retained without unsound cross-parity reserve.

The next genuinely source-facing seam is **homogeneous-component extraction and cross-energy simplification for the actual P5 polynomial packet**: identify the real degree split in one source chart/output metric, compute the exact `H_n`, and determine whether any same-total-degree identities or parity-block bounds materially beat the minimax degreewise allocator. If the actual source cell is shifted or one-sided rather than centered, a separate affine-cell reflection/one-sided energy theorem is required instead of silently using Section 3.

All source binding, actual cell symmetry, parameter compatibility, trajectory/FD-halo coverage, Float64/interval semantics, Lean/kernel receipt, independent verifier action, admission, and registry decisions remain OPEN.
