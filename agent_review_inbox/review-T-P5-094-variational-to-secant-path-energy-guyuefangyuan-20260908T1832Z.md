---
kind: review_result
review_id: review-T-P5-094-variational-to-secant-path-energy-guyuefangyuan-20260908T1832Z
task_id: T-P5-094-VARIATIONAL-TO-SECANT-PATH-ENERGY
agent: 古月方源
source_agent: 古月方源
reviewer: 古月方源
created_at: 2026-09-08T18:32:00Z
claim_commit: f2e1d45f915504f239f704a66e9c2bc0c2c936b3
inspected_commit: d564426654e0b78209010ba16cfaaf9bae3a62fb
inspected_upstream:
  - agent_review_inbox/review-T-P5-090-moving-metric-contraction-congruence-liuguanyi-20260908T1710Z.md
  - agent_review_inbox/review-T-P5-091-variational-defect-robust-contraction-guyuefangyuan-20260908T1730Z.md
  - agent_review_inbox/review-T-P5-093-base-flow-lie-defect-honglianmozun-20260908T1758Z.md
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_rational_decay_and_constant_metric_secant_leaves_then_bind_same_tube_path_family
commands: none_math_derivation_only
---

# T-P5-094 — variational contraction to finite separation via rational path energy

## 0. Question and scope

T-P5-090 proves the exact moving-metric differential contraction congruence, but
explicitly leaves a finite-step/secant certificate open.  T-P5-091 closes robust
**variational** defects, but likewise does not upgrade a tangent-vector theorem to
a statement about two distinct states.

This child closes the missing mathematical bridge at two levels:

1. for a constant/frozen quadratic metric on a convex segment, a pointwise
   Jacobian contraction implies a genuine secant contraction;
2. for a state/time-dependent metric, the coordinate-invariant finite-separation
   object is path energy (and its infimum), not a raw coordinate chord.

A second issue is trusted arithmetic.  The usual finite-horizon factor
`exp(-2 mu h)` is analytically natural but undesirable as a primitive exact
certificate.  The first theorem below derives an arbitrarily sharp **rational,
division-free polynomial decay factor** directly from `Vdot <= -2 mu V`.

No deployed source binding, Float64/FD/controller/P8 semantics, Lean receipt,
provenance, admission, or registry promotion is claimed here.

---

## 1. Scalar differential decay without an exponential

Let `V : [0,h] -> R` be continuously differentiable and suppose

**(1.1)** `V(t) >= 0`,

**(1.2)** `mu >= 0`,

**(1.3)** `V'(t) <= -2 mu V(t)` for every `t in [0,h]`.

Because the right-hand side is nonpositive, `V` is nonincreasing.  Fix
`0 <= a <= b <= h`.  Hence for every `t in [a,b]`,

`V(t) >= V(b)`.

Integrating (1.3),

`V(b)-V(a) <= -2 mu * integral_a^b V(t) dt`

and monotonicity gives

`integral_a^b V(t) dt >= (b-a) V(b)`.

Therefore

**(1.4) ONE-STEP RATIONAL DECAY**

`(1 + 2 mu (b-a)) V(b) <= V(a)`.

This is weaker than the exponential Gronwall factor, but it contains no
transcendental operation and is already exact-rational whenever `mu` and the
step length are rational/dyadic.

### 1.1 N-slice sharpening

Let `N >= 1` be an integer and split `[0,h]` into `N` equal pieces.  Applying
(1.4) on every piece and multiplying gives

**(1.5)**

`(1 + 2 mu h / N)^N V(h) <= V(0)`.

Clear the denominator once and for all:

**(1.6) DIVISION-FREE N-SLICE GATE**

`(N + 2 mu h)^N V(h) <= N^N V(0)`.

Thus the certified squared contraction factor may be taken as

`q_N = N^N / (N + 2 mu h)^N`.

For fixed `mu h`, increasing `N` monotonically approaches the usual
`exp(-2 mu h)` factor from above, but **the checker never needs to evaluate an
exponential**.  A generator may choose any convenient positive integer `N`; the
trusted theorem checks only additions, multiplications, natural powers, and
order.

More generally, for any partition with lengths `Delta_k >= 0`,

**(1.7)**

`[product_k (1 + 2 mu Delta_k)] V(h) <= V(0)`.

Equal pieces are the natural strongest symmetric choice at fixed `N`.

### 1.2 Relative-defect reuse

If T-P5-091 supplies a purely relative/signed variational defect and therefore

`Vdot <= -2 nu V`, `nu = mu-rho > 0`,

all statements above hold verbatim with `mu` replaced by `nu`.  An irreducible
additive variational defect is different: T-P5-091 correctly gives an
ultimate/invariant tube rather than homogeneous pairwise contraction, so this
child does not silently treat an additive defect as a Jacobian contraction.

---

## 2. Constant metric: Jacobian contraction implies secant contraction

Let `W` be a fixed symmetric PSD matrix and write

`Q_W(v) = v^T W v`.

Let `K` be a set with the property that the straight segment from `y` to `x`
stays inside the certified domain.  Let `Psi` be `C^1` on that segment.  Suppose
there are nonnegative exact scalars `A,B` with `A > 0` such that throughout the
segment

**(2.1)**

`A Q_W(D Psi(z) v) <= B Q_W(v)`

for every tangent vector `v`.

Set `delta=x-y` and `gamma(s)=y+s delta`, `0<=s<=1`.  The fundamental theorem of
calculus gives

`Psi(x)-Psi(y) = integral_0^1 D Psi(gamma(s)) delta ds`.

For a PSD quadratic form, integral Jensen/Cauchy gives

**(2.2)**

`Q_W(integral_0^1 u(s) ds) <= integral_0^1 Q_W(u(s)) ds`.

Therefore

`A Q_W(Psi(x)-Psi(y))`
` <= integral_0^1 A Q_W(DPsi(gamma(s)) delta) ds`
` <= integral_0^1 B Q_W(delta) ds`
` = B Q_W(x-y)`.

Hence

**(2.3) CONSTANT-METRIC SECANT THEOREM**

`A Q_W(Psi(x)-Psi(y)) <= B Q_W(x-y)`.

This is the exact finite-separation statement missing from a purely variational
certificate.  If the tangent bound comes from Section 1 with horizon `h`, choose

`A=(N+2 mu h)^N`, `B=N^N`.

Then (2.3) is fully division-free.

### 2.1 Why segment coverage is a real premise

The theorem does not merely need derivative bounds at the two endpoints.  The
entire segment must lie in the domain where (2.1) is certified.  If a domain is
disconnected, one may define a map that is locally constant on each component
but has different constants on different components: the derivative is zero on
each component, yet cross-component secants can be arbitrarily large.

Thus `pointwise tangent contraction on K` does not imply a chord contraction
between arbitrary points of a nonconvex/non-path-covered `K`.

---

## 3. Moving metric: path energy is the correct finite-separation object

For a state-dependent metric, a raw endpoint chord is not coordinate invariant.
The clean object is the energy of a connecting path.

At time `t`, let `W_t(x)` be symmetric PSD.  For a `C^1` path
`gamma:[0,1]->Omega_t`, define

**(3.1)**

`E_t(gamma) := integral_0^1 Q_{W_t(gamma(s))}(gamma'(s)) ds`.

Now let `Psi : Omega_0 -> Omega_1` be a differentiable map.  Suppose a
pointwise finite-time tangent certificate holds:

**(3.2)**

`A Q_{W_1(Psi(x))}(D Psi(x) v) <= B Q_{W_0(x)}(v)`

for all certified `x,v`, with `A>0`, `B>=0`.

For any admissible path `gamma`, the image path `eta=Psi o gamma` satisfies

`eta'(s)=D Psi(gamma(s)) gamma'(s)`.

Integrating (3.2) along the path gives immediately

**(3.3) PATH-ENERGY CONTRACTION**

`A E_1(Psi o gamma) <= B E_0(gamma)`.

No Jensen loss is incurred here; the moving metric is evaluated at the correct
point of the image path.

### 3.1 Infimum-energy finite separation

Define the energy infimum

**(3.4)**

`D_t(x,y) := inf { E_t(gamma) : gamma admissible from x to y }`.

This is deliberately called `D_t` rather than automatically claiming a genuine
distance: if `W` is only PSD it may be degenerate, and standard topology/
coercivity hypotheses are needed to identify it with a squared Riemannian
distance.

If every admissible initial path may be flowed/mapped through the same certified
tube, then from (3.3), for every initial path `gamma`,

`A D_1(Psi(x),Psi(y)) <= A E_1(Psi o gamma) <= B E_0(gamma)`.

Taking the infimum over `gamma` yields

**(3.5) FINITE-SEPARATION PATH-INFIMUM THEOREM**

`A D_1(Psi(x),Psi(y)) <= B D_0(x,y)`.

This needs neither an attained geodesic nor a matrix inverse.

---

## 4. Apply T-P5-090 to a whole connecting path

Let `Phi_h` be the time-`h` flow map of the physical system from T-P5-090.  Pick
an initial connecting path `gamma_0(s)` and flow every point on it:

`gamma_t(s) = Phi_t(gamma_0(s))`.

Assume the full spacetime sheet

`{ (t,gamma_t(s)) : 0<=t<=h, 0<=s<=1 }`

stays inside the tube on which T-P5-090's contraction tensor certificate holds.
Then

`xi(t,s) := partial_s gamma_t(s)`

is a variational vector and its moving-metric energy

`V_s(t)=Q_{W_t(gamma_t(s))}(xi(t,s))`

obeys

`d/dt V_s(t) <= -2 mu V_s(t)`.

Section 1 therefore gives, pointwise in `s`,

**(4.1)**

`(N+2 mu h)^N V_s(h) <= N^N V_s(0)`.

Integrating in `s` gives the path-energy form directly:

**(4.2)**

`(N+2 mu h)^N E_h(gamma_h) <= N^N E_0(gamma_0)`.

Taking infima as in Section 3 yields

**(4.3) RATIONAL FINITE-SEPARATION CONTRACTION**

`(N+2 mu h)^N D_h(Phi_h(x),Phi_h(y)) <= N^N D_0(x,y)`.

This is an exact-rational replacement for the usual informal statement

`D_h <= exp(-2 mu h) D_0`.

The price is only a controllable rational slack indexed by `N`.

### 4.1 Same-tube obligation

The new geometric coverage obligation is explicit: it is not enough that the
two endpoint trajectories stay in the tube.  The **flowed connecting path** must
stay in the contraction-certified tube.  If the tube is forward invariant and
path-convex in the relevant metric, this may be easy; otherwise it is a separate
source/coverage child and must not be inferred from endpoint coverage alone.

---

## 5. Exact naturality under a nonlinear moving chart

Use T-P5-090's chart at each time,

`x = T_t(z)`, `J_t(z)=D T_t(z)`,

and pulled-back metric

**(5.1)** `M_t(z)=J_t(z)^T W_t(T_t(z)) J_t(z)`.

For any normalized `C^1` path `zeta(s)`, chain rule gives

`(T_t o zeta)' = J_t(zeta) zeta'`.

Therefore pointwise

`Q_{M_t(zeta)}(zeta') = Q_{W_t(T_t(zeta))}((T_t o zeta)')`,

and after integration

**(5.2) EXACT PATH-ENERGY PULLBACK**

`E_{M_t}(zeta) = E_{W_t}(T_t o zeta)`.

Thus the finite-separation object itself is coordinate natural; there is no
Jacobian condition-number loss.

If `T_t` is a diffeomorphism between the admissible normalized and physical path
domains (so admissible paths lift in both directions), then the infimum energies
are exactly equal:

**(5.3)**

`D_{M_t}(z0,z1) = D_{W_t}(T_t(z0),T_t(z1))`.

Without a path-lifting/surjectivity hypothesis, (5.2) remains exact for every
witness path, but equality of the two infima should not be claimed automatically.

If normalized and physical flow maps commute with the moving chart,

`T_h o Psi_h = Phi_h o T_0`,

then (4.3) transports to the normalized chart with **exactly the same rational
factor**:

**(5.4)**

`(N+2 mu h)^N D_{M_h}(Psi_h(z0),Psi_h(z1))`
` <= N^N D_{M_0}(z0,z1)`.

This is the finite-separation companion to T-P5-090's differential tensor
congruence.

---

## 6. Exact obstruction: raw normalized coordinate chord can expand

A finite-separation theorem in a moving nonlinear chart must not silently replace
path energy by the Euclidean chord in normalized coordinates.

Take the physical half-line `x>0` with constant metric `W=1` and the exact map

**(6.1)** `Phi(x)=x/2`.

Its tangent factor is exactly

`Q_W(DPhi v) = v^2/4`.

Now use the nonlinear chart on `z>0`

**(6.2)** `T(z)=1/z`.

Then

`J(z)=-1/z^2`,

so the pullback metric is

**(6.3)** `M(z)=1/z^4`.

The conjugate normalized map is

**(6.4)** `Psi(z)=T^{-1}(Phi(T(z)))=2z`.

Hence its raw normalized Euclidean chord **expands**:

**(6.5)**

`|Psi(z1)-Psi(z2)|^2 = 4 |z1-z2|^2`.

Nevertheless the correct pulled-back tangent energy contracts by the physical
factor:

`M(Psi(z)) (DPsi(z)v)^2`
` = [1/(2z)^4] * (2v)^2`
` = (1/4) * v^2/z^4`
` = (1/4) M(z) v^2`.

Thus physical contraction by `1/4` is perfectly preserved while raw normalized
coordinate chord squared expands by `4`.

This is an exact algebraic counterexample.  Therefore any generic theorem

`moving-metric differential contraction => Euclidean secant contraction in an arbitrary nonlinear chart`

is false.  The path-energy/pulled-back-metric formulation is not cosmetic; it is
required for coordinate invariance.

---

## 7. Source/checker interface suggested by this child

For a deployed finite-separation claim, the smallest honest packet is:

1. a same-tube variational contraction rate `mu >= 0` from T-P5-090 or an
   effective relative-defect rate `nu>0` from T-P5-091;
2. an exact horizon `h >= 0` and a chosen positive integer sharpening parameter
   `N`;
3. coverage of the full flowed connecting-path sheet, not only two endpoint
   trajectories;
4. the time-0/time-h metric fields, or their exact pulled-back chart metrics;
5. if an infimum-energy statement is desired, an admissible path family stable
   under the flow/map; and
6. if equality of physical and normalized infimum energies is used, the required
   chart path-lifting/diffeomorphism fact.

The trusted numerical gate for the contraction factor is only

`A=(N+2 mu h)^N`, `B=N^N`,

followed by

`A * E_out <= B * E_in`

or the corresponding infimum/secant theorem.  No exponential, square root,
metric inverse, or generalized eigenvalue is intrinsically required.

---

## 8. Suggested Lean decomposition

The first Lean pass should stay small and avoid formalizing a full Riemannian
manifold API.

### Leaf A — scalar rational decay

Suggested statement shape:

`rational_decay_one_step_of_deriv_le`

Assume on `[a,b]` that `0<=V`, `0<=mu`, and `deriv V t <= -2*mu*V t`; conclude

`(1 + 2*mu*(b-a))*V b <= V a`.

The only analytic ingredients are monotonicity from the derivative sign and the
fundamental theorem/integral comparison.

### Leaf B — finite partition algebra

`rational_decay_equal_partition_pow`

Consume the one-step inequalities on `N` equal intervals and prove

`(N + 2*mu*h)^N * V h <= N^N * V 0`.

Once the one-step premises are supplied, this is essentially finite-product
algebra/induction.

### Leaf C — quadratic integral Jensen

`quadratic_integral_jensen_psd`

For fixed PSD `W`, prove

`Q_W(integral u) <= integral Q_W(u)`

on a unit interval.

### Leaf D — constant-metric Jacobian-to-secant

`jacobian_bound_implies_secant_bound_const_metric`

Under segment coverage and

`A*Q_W(DPsi z v) <= B*Q_W(v)`,

prove

`A*Q_W(Psi x-Psi y) <= B*Q_W(x-y)`.

This is likely the most immediately reusable finite-dimensional leaf.

### Leaf E — pullback path-energy identity

`pullback_path_energy_identity`

For `M=J^T W J`, prove equality of the integrands and hence witness-path energies.
The infimum/geodesic corollary can be delayed until the repository actually has a
consumer that needs it.

---

## 9. Open obligations / fail-closed boundary

This child remains conditional.  It does **not** prove:

- that the deployed P5 lane has a same-tube rate `mu` or `nu`;
- that every relevant connecting path sheet stays inside the certified source
  tube;
- that the deployed metric is coercive enough for `D_t` to be a genuine metric;
- that a physical path always lifts through the deployed nonlinear chart;
- additive/noisy finite-separation contraction (T-P5-091 correctly changes that
  conclusion to a tube unless the defect is homogeneous in the variation);
- Float64/FD/controller/P8 semantics;
- Lean/kernel success, independent verification, receipt/provenance/admission,
  or registry closure.

Failure of the path-sheet coverage or path-lifting gate means
`NOT_CERTIFIED/NOT_APPLICABLE` for this route, not that the physical flow is
noncontracting.

---

## 10. Bottom line

The main new reusable certificate is

**`(N+2 mu h)^N D_h(Phi_h x, Phi_h y) <= N^N D_0(x,y)`**,

where `D_t` is the infimum of moving-metric path energy.  It follows from
T-P5-090-style differential contraction using only a finite rational partition;
no trusted exponential is needed.  In a fixed metric on a covered straight
segment this collapses to an ordinary quadratic secant bound.  Under a nonlinear
moving chart, path energy pulls back exactly and therefore keeps the same
contraction factor with no Jacobian condition-number loss.

The algebraic chart `T(z)=1/z`, physical map `x -> x/2`, normalized map `z -> 2z`
shows why this formulation is necessary: the true pulled-back metric contracts by
`1/4` while the raw normalized Euclidean chord squared expands by `4`.
