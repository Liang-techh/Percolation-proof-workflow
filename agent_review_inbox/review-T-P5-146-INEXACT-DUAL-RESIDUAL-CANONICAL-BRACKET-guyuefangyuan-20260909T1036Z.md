---
kind: review_result
review_id: review-T-P5-146-inexact-dual-residual-canonical-bracket-guyuefangyuan-20260909T1036Z
task_id: T-P5-146-INEXACT-DUAL-RESIDUAL-CANONICAL-BRACKET
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T10:36:00Z
claim_commit: c1db98d6af0a35acc736424cda6762478ed49506
inspected_commit: 35c7cbfc6249407c95f1acac944e4fe6ab524df8
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-143-ROOT-FREE-SINGULAR-BOUNDARY-CANONICALIZATION-kuangmanmozun-20260909T0942Z.md
    commit: 9d748de3be2b2cec2602ac9a96f90a5867cff405
  - path: agent_review_inbox/review-T-P5-144-SEMIDEFINITE-CELL-NULLSPACE-ELIMINATION-honglianmozun-20260909T1003Z.md
    commit: 39889bbfd45bbc9bd541a7a8c51f0005a60b0881
  - path: agent_review_inbox/review-T-P5-145-canonical-range-dual-descent-liuguanyi-20260909T1012Z.md
    commit: d5adca58a70ff24d658275d6cbd3c5f0d9e261c3
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: split_an_inexact_dual_residual_into_exact_range_and_G_kernel_parts_before_norm_bounding; exact_Hodge_pair_recovers_the_T-P5-145_canonical_packet_without_a_kernel_basis; otherwise_use_the_rankone_residual_cap_for_a_sharp_canonical_energy_deadband_and_polynomial_threshold_gates; do_not_infer_exact_canonicality_or_a_uniform_right_step_from_a_small_raw_residual_alone
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional linear/quadratic algebra only
exit_code: n/a
---

# T-P5-146 — inexact dual residual: exact Hodge correction and canonical-energy bracket

## 0. Narrow seam and non-overlap

T-P5-145 gives a basis-free **exact** canonical packet

`K y = b`,

`K w = G y`,

for `K>=0`, `G>0`, and then derives the singular-boundary multiplier gate and a root-free right-step descent certificate.  Its Section 12 deliberately leaves one seam fail-closed: what may be concluded when the second solve is only approximate.

This child closes exactly that seam.  It does not redo T-P5-141's inexact **primal** range solve `K y approximately b`, T-P5-143's canonical representative theorem, or T-P5-144's semidefinite **physical** metric quotient.  Here `G` stays positive definite and `K y=b` is exact.

The main new observation is stronger than a generic residual norm estimate:

> For symmetric `K` and `G>0`, every dual residual has a unique `G(ker K)` component.  The `range(K)` part is harmless and merely changes the dual witness; the `G(ker K)` part is exactly the noncanonical nullspace translation of the primal range solve.

Thus an exact residual decomposition repairs an inexact dual solve all the way back to T-P5-145, with no kernel basis, pseudoinverse, square root, or eigendecomposition.  If only a residual cap is available, the same decomposition gives a sharp fail-closed interval for the true canonical energy.

No source binding, Float64/runtime semantics, coverage, receipt/provenance/admission, Lean compile, P8, registry, or parent closure is claimed.

---

## 1. Setup

Work in a finite-dimensional real vector space.  Let

- `K` be symmetric positive semidefinite;
- `G` be symmetric positive definite;
- `b` be in `range K`;
- `y` be any exact primal range solve, `K y=b`;
- `w` be an arbitrary candidate dual vector.

Define the dual residual

**(1.1)** `r := G y - K w`.

Let

`N := ker K`.

By T-P5-143 there is a unique canonical primal solve `y_c` satisfying

**(1.2)** `K y_c=b`,

**(1.3)** `n^T G y_c=0` for every `n in N`.

Write

**(1.4)** `v_* := y-y_c in N`.

The intrinsic canonical energy is

**(1.5)** `s_c := Q_G(y_c)=y_c^T G y_c`.

Since `y_c` is `G`-orthogonal to `N`,

**(1.6)** `Q_G(y)=s_c+Q_G(v_*)`.

The whole problem is therefore to determine or bound the single scalar `Q_G(v_*)` without requiring a nullspace basis.

---

## 2. Exact residual Hodge splitting

### Theorem A — `range K` and `G(ker K)` form a direct sum

For symmetric `K` and positive-definite `G`,

**(2.1)** `V = range(K) direct_sum G(N)`.

### Proof

For a symmetric matrix,

`range K = N^perp`

in the Euclidean pairing.  First show the intersection is trivial.  Suppose

`u=K z=G v`

with `v in N`.  Pair with `v`:

`v^T u = v^T K z = (K v)^T z = 0`,

while also

`v^T u=v^T G v=Q_G(v)`.

Positive definiteness of `G` gives `v=0`, hence `u=0`.

Next,

`dim range K + dim G(N)`

`= rank K + dim N`

`= dim V`,

because `G` is injective.  The trivial intersection plus the dimension count proves (2.1).

### Consequence

Every residual `r` admits a decomposition

**(2.2)** `r = K z + G v`,

**(2.3)** `K v=0`.

The vector `v` is unique.  The vector `z` is unique only modulo `ker K`, which is harmless because only `Kz` is consumed.

If `K,G,r` are rational, a rational pair `(z,v)` exists: (2.2)-(2.3) is a consistent linear system with rational coefficients, so rational Gaussian elimination supplies a rational solution.  No irrational nullspace basis is logically required.

---

## 3. Main correction identity: an inexact dual packet becomes exact

Assume a pair `(z,v)` satisfies (2.2)-(2.3).  Define

**(3.1)** `y_hat := y-v`,

**(3.2)** `w_hat := w+z`.

Then

**(3.3)** `K y_hat=b`,

because `Ky=b` and `Kv=0`, and

**(3.4)** `K w_hat = G y_hat`.

Indeed,

`K(w+z)=Kw+Kz`

`= Gy-r + (r-Gv)`

`= G(y-v)`.

Therefore `(y_hat,w_hat)` is exactly the T-P5-145 basis-free canonical packet.  In particular

**(3.5)** `y_hat=y_c`,

and the unique Hodge vector is precisely

**(3.6)** `v=v_*=y-y_c`.

This gives the exact energy recovery

**(3.7)** `s_c = Q_G(y)-Q_G(v)`.

The fixed-multiplier floor scalar does not change under the correction:

`b^T v = y^T K v=0`,

so

**(3.8)** `b^T y_hat=b^T y`.

Thus a producer that started from a noncanonical primal solve and an inexact dual solve may repair both with one exact residual Hodge packet; it does not need to restart the multiplier derivation.

### Exact multiplier consequences

Once (2.2)-(2.3) are source-certified, define

`s:=Q_G(y_hat)`, `U:=Q_G(w_hat)`.

- If `s<=4R`, T-P5-145 certifies the left multiplier boundary as globally optimal.
- If `s>4R`, put `h=s-4R`.  Any rational `d>0` satisfying

  **(3.9)** `4 d^2 U s <= h^2`

  inherits T-P5-145's quantitative strict right-step reserve.

So the exact Hodge branch fully closes the mathematical inexact-dual seam.

---

## 4. Why the raw residual norm is the wrong object

Equation (2.2) separates two effects:

- `Kz` is a **range residual**.  It only changes the dual witness from `w` to `w+z` and says nothing bad about canonicality.
- `Gv` with `v in ker K` is the **kernel-visible residual**.  It is exactly the primal noncanonical component.

A raw norm of `r` mixes these two effects and can therefore be arbitrarily pessimistic.

### Pure-range example

Take

`K=diag(1,0)`, `G=I`, `b=(1,0)`, `y=(1,0)`.

Then `y` is already canonical.  For any `M`, choose

`w=(1-M,0)`.

The residual is

`r=(M,0)=K(M,0)`,

which can be arbitrarily large, yet the Hodge kernel component is exactly `v=0`.  Correcting the range part restores `w_hat=(1,0)` and zero residual.

Therefore **a large raw residual does not imply a large canonicality defect**.

Conversely, an arbitrarily small pure-kernel residual can destroy exact canonicality; see Section 8.

---

## 5. Approximate Hodge packet and a root-free canonical-energy bracket

Often the producer can remove a known range part and a known kernel component but leaves a small remainder.  Let candidate vectors `z,v` satisfy only

**(5.1)** `K v=0`.

Define

**(5.2)** `e := r-Kz-Gv`,

**(5.3)** `y_0 := y-v`,

**(5.4)** `w_0 := w+z`.

Then exactly

**(5.5)** `K y_0=b`,

**(5.6)** `G y_0-K w_0=e`.

Let `y_c` be the canonical solve and put

**(5.7)** `n:=y_0-y_c in ker K`.

For every `x in ker K`,

`x^T e = x^T G y_0`

because `x^T K w_0=0`, hence by canonical orthogonality

**(5.8)** `x^T e = x^T G n`.

In particular, taking `x=n`,

**(5.9)** `n^T e=Q_G(n)`.

Now assume a basis-free rank-one residual domination

**(5.10)** `sigma G - e e^T >= 0`, `sigma>=0`.

Equivalently,

**(5.11)** `(e^T x)^2 <= sigma Q_G(x)` for every `x`.

Applying (5.11) to `n` and using (5.9) gives

`Q_G(n)^2 <= sigma Q_G(n)`.

Since `Q_G(n)>=0`,

**(5.12)** `Q_G(n)<=sigma`.

The Pythagorean identity

`Q_G(y_0)=s_c+Q_G(n)`

therefore yields the main fallback interval

### Theorem B — canonical-energy deadband

**(5.13)** `Q_G(y_0)-sigma <= s_c <= Q_G(y_0)`.

No inverse, square root, eigenvalue, kernel basis, or division appears in the trusted gate.

For the physical threshold `T:=4R`:

- if `Q_G(y_0)<=T`, then `s_c<=T`, so the boundary is certified optimal;
- if `Q_G(y_0)-sigma>T`, then `s_c>T`, so the boundary is strictly nonoptimal;
- if `Q_G(y_0)-sigma<=T<Q_G(y_0)`, this packet alone is genuinely inconclusive.

The constant `1` multiplying `sigma` is sharp; Section 8 gives equality.

---

## 6. Intrinsic meaning: the best residual cap equals the lost canonical energy

The previous interval is not merely a loose norm estimate.

For the original residual `r`, consider arbitrary exact range corrections `z` and residuals

`e_z:=r-Kz`.

Suppose a scalar `sigma` satisfies

`sigma G-e_z e_z^T>=0`.

Let `v_*=y-y_c`.  Since `v_* in ker K`,

`v_*^T e_z=v_*^T r=Q_G(v_*)`.

Therefore the same argument as Section 5 gives

**(6.1)** `Q_G(v_*)<=sigma`

for **every** range correction and every valid full-space rank-one cap.

On the other hand, choose the exact Hodge correction from Section 2.  Then

`e_*=Gv_*`.

The `G`-Cauchy inequality gives, for every `x`,

`(x^T e_*)^2=(x^T Gv_*)^2`

`<=Q_G(x)Q_G(v_*)`.

Hence

**(6.2)** `Q_G(v_*) G - e_* e_*^T >=0`.

So the smallest feasible rank-one cap after exact range correction is attained and equals

**(6.3)** `sigma_* = Q_G(v_*)`.

Combining with (1.6),

**(6.4)** `s_c=Q_G(y)-sigma_*`.

This is an exact quotient interpretation: the optimized residual cap is precisely the energy of the primal nullspace translation that must be removed to reach the canonical range solve.

For implementation, solving the linear Hodge packet `(Kz+Gv=r, Kv=0)` is preferable to numerically minimizing `sigma`; the latter identity is mainly a structural guarantee and a regression oracle.

---

## 7. A second fallback from the corrected dual scalar

The approximate packet (5.5)-(5.6) also exposes a useful signed scalar.  Define

**(7.1)** `a:=b^T w_0`.

Since `K y_c=b`,

`a=y_c^T K w_0`

` = y_c^T(G y_0-e)`

` = s_c-y_c^T e`.

Thus

**(7.2)** `s_c-a=y_c^T e`.

Applying the same rank-one domination to `y_c` gives the exact scalar cone

### Theorem C — inexact-dual scalar cone

**(7.3)** `(s_c-a)^2 <= sigma s_c`.

This can be consumed without solving the quadratic or taking a square root.

Let

`P(t):=(t-a)^2-sigma t`.

Then `P(s_c)<=0`.  For any threshold `T`, the following purely polynomial gates hold.

### Theorem D — root-free upper threshold gate

If

**(7.4)** `2T >= 2a+sigma`,

**(7.5)** `(T-a)^2 >= sigma T`,

then

**(7.6)** `s_c<=T`.

Proof: if `s_c>T`, then

`P(T)-P(s_c)`

`=(T-s_c)(T+s_c-2a-sigma)<0`

because the first factor is negative and the second is positive by (7.4), contradicting `P(T)>=0>=P(s_c)`.

### Theorem E — root-free lower threshold gate

If

**(7.7)** `2T <= 2a+sigma`,

**(7.8)** `(T-a)^2 > sigma T`,

then

**(7.9)** `T<s_c`.

The proof is the same factorization with signs reversed.  If `s_c<=T`, then the second factor is nonpositive while `T-s_c>=0`, contradicting `P(T)>0>=P(s_c)`.

For `T=4R`, Theorems D/E provide an alternative boundary-optimal/nonoptimal decision that can be tighter than the simple interval (5.13), especially after most of the residual has been removed as an exact range term.

The checker never materializes the roots

`a+sigma/2 +/- sqrt(sigma(4a+sigma))/2`.

---

## 8. Sharpness and exact obstructions

### 8.1 The deadband constant is sharp

Take

`K=diag(1,0)`, `G=I`, `b=(1,0)`,

`y=(1,t)`, `w=(1,0)`.

Then

`r=(0,t)`,

`y_c=(1,0)`,

`v_*= (0,t)`,

`Q_G(y)=1+t^2`,

`s_c=1`.

The full rank-one cap holds with the exact value

`sigma=t^2`,

and

`s_c=Q_G(y)-sigma`.

So the coefficient `1` in (5.13) cannot be improved from the stated information.

### 8.2 Arbitrarily small residual does not imply exact canonicality

In the same example, choose any nonzero `t=epsilon`.  Then the optimal residual cap is

`sigma_*=epsilon^2 -> 0`,

but `y=(1,epsilon)` is noncanonical for every `epsilon!=0`.

Therefore no theorem of the form

> sufficiently small residual => exact canonicality

is valid at a singular `K` without an exact range/kernel statement.  Exact canonicality is recovered by `sigma=0`, by the exact Hodge packet, or by an equivalent exact range condition—not by a positive tolerance.

### 8.3 A residual bound alone cannot provide a uniform right-step size

Even residual **zero** does not give a multiplier step independent of the positive curvature scale.

Take the one-dimensional family

`G=1`, `K=epsilon>0`, `b=epsilon`, `y=1`, `w=1/epsilon`,

so the dual residual is exactly zero and `s_c=1`.  Set `R=1/8`, so `4R=1/2<s_c`, and take the left multiplier as `tau_0=0` with `H=K`.

For a right step `d>0`, the exact shifted solve is

`y_d=epsilon/(epsilon+d)`.

The sharp floor difference is

**(8.1)** `4(E_d-E_0)= d(d-epsilon) / [2(epsilon+d)]`.

Hence descent occurs iff

**(8.2)** `d<epsilon`.

Given any fixed positive proposed step `d_0`, choosing `0<epsilon<d_0` makes that step fail, despite zero residual and the same values `s_c=1`, `R=1/8`.

Thus the approximate-residual fallback may classify the boundary, but an executable quantitative right step still needs one of:

- the exact corrected dual energy `U` from the Hodge branch and T-P5-145;
- a certified restricted curvature/lower-gain scale for `K`;
- or an actual shifted solve/secant certificate.

Residual smallness by itself is not a substitute.

---

## 9. Recommended producer/checker packet

Under one immutable source/reference/cell key, the strongest packet is:

```text
K symmetric PSD
G symmetric PD
K y = b
r = G y - K w
K v = 0
K z + G v = r

y_c = y-v
w_c = w+z
s = Q_G(y_c)
U = Q_G(w_c)
```

The checker verifies only matrix-vector equalities, PSD/PD facts already needed upstream, and rational quadratic evaluations.  It then consumes T-P5-145 unchanged.

If the exact Hodge split is unavailable, keep

```text
K v = 0
e = r-Kz-Gv
sigma G - e e^T >= 0
y0 = y-v
w0 = w+z
q0 = Q_G(y0)
a = b^T w0
```

and use both safe fallbacks:

```text
q0-sigma <= s_c <= q0
(s_c-a)^2 <= sigma s_c
```

with the polynomial threshold gates of Section 7.  Do **not** declare `y0` canonical unless the residual is eliminated exactly.

Source-side priority should be:

1. remove exact `range(K)` residual first;
2. solve the exact Hodge pair if possible;
3. only then bound the remaining residual;
4. retain its sign/linear structure until after `e=r-Kz-Gv` is formed.

Bounding the raw residual before step 1 can be arbitrarily wasteful.

---

## 10. Suggested Lean leaves

The best first leaf is pure algebra and does not require any projection API:

```lean
-- schematic
theorem dualResidual_hodge_correction
    (hKy : K.mulVec y = b)
    (hr : r = G.mulVec y - K.mulVec w)
    (hKv : K.mulVec v = 0)
    (hsplit : K.mulVec z + G.mulVec v = r) :
    K.mulVec (y-v) = b /\
    K.mulVec (w+z) = G.mulVec (y-v)
```

Then formalize the scalar/quadratic consumers independently:

```lean
theorem kernelEnergy_le_of_rankOneResidual
  (hnonneg : 0 <= qn)
  (hdiag : qn^2 <= sigma * qn) :
  qn <= sigma
```

```lean
theorem residualCone_threshold_upper
  (hcone : (s-a)^2 <= sigma*s)
  (hvertex : 2*a + sigma <= 2*T)
  (hout : sigma*T <= (T-a)^2) :
  s <= T
```

```lean
theorem residualCone_threshold_lower
  (hcone : (s-a)^2 <= sigma*s)
  (hvertex : 2*T <= 2*a + sigma)
  (hout : sigma*T < (T-a)^2) :
  T < s
```

These two threshold leaves should be `nlinarith`-scale Real algebra after exposing

`P(T)-P(s)=(T-s)*(T+s-2*a-sigma)`.

A later finite-dimensional theorem may state the direct-sum existence

`range K direct_sum G(ker K)=V`,

but source consumers do not need to wait for that abstract theorem if they already provide concrete exact `(z,v)` witnesses.

---

## 11. Remaining obligations

This child is mathematical only.  It does not provide actual values of `K,G,b,y,w,r,z,v,sigma`, does not prove that a runtime solver's residual has exact-real semantics, and does not bind any source cell/reference/controller key.  It also does not close Float64, FD, P8, Lean/kernel, independent verification, admission, or registry gates.

The key source question is now much narrower than “is the dual solve accurate?”:

> Can the actual same-key residual be split as `r=Kz+Gv` with `Kv=0`, or at least as `r=Kz+Gv+e` with an exact rank-one cap on the final `e`?

That is the correct fail-closed interface.

## 12. Status

`T-P5-146-INEXACT-DUAL-RESIDUAL-CANONICAL-BRACKET` is a

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`**.

Its strongest result is the exact residual Hodge correction, which converts an inexact dual packet back into the exact T-P5-145 canonical packet without a kernel basis.  The residual-cap branch gives a sharp canonical-energy deadband and root-free threshold tests when the exact split is unavailable.  No parent/admission state is changed.
