---
kind: review_result
review_id: review-T-P5-204-support-slack-lyapunov-margin-liuguanyi-20260910T0200Z
task_id: T-P5-204-SUPPORT-SLACK-LYAPUNOV-MARGIN
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T02:00:00Z
claim_commit: d26092ebc0e13a35a4546e499e0cc5741702320d
inspected_commit: 76a42490eb98ba0a65528e9676f480aa4faae3bc
upstream_commits:
  - 12a92536fc8371342e54845225a423ad33323407  # T-P5-200 gauge-invariant affine-amplitude cubic absorption
  - a46f974e740bee066051d944e10f1338c62fc6e3  # T-P5-203 PSD sharp polar/Schur support dual
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_support_cap_copositive_threshold; add_support_error_budget_bridge; add_zero_slack_obstruction; add_multi_generator_cap_region; add_no_division_reserve_transport
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact homogeneous quadratic derivation; copositive-order monotonicity; generalized copositive Rayleigh quotient; reserve decomposition; exact rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-204 — exact support-slack / Lyapunov-margin bridge

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-200 converts an exact signed affine-amplitude support cap

`b^T y <= B`

into the quadratic debit

`D_B = (h0+B) Q + sym(b c^T)`,

with `Q` copositive on the consumed selector cone.  Its downstream T-P5-192-shaped gate is

`l_tot <= 0`

and

`-M_tot(B)` copositive,

where

`M_tot(B) = M0 + (h0+B)Q + sym(b c^T)`.

T-P5-203 then shows that, on the PSD mixed-domain corridor, a support solver can approach the true support `s_*` by strict rational caps `B>s_*` and can emit a root-free rational support packet.

The missing cross-layer question is: **how much strict overestimate in `B` can the Lyapunov gate actually afford?**

This child gives an exact answer.

Write

`M_fix := M0 + h0 Q + sym(b c^T)`

and

`A := -M_fix`.

Then the quadratic Lyapunov certificate at cap `B` is exactly

**`C(B) := A - B Q` copositive.**

Since `Q` is copositive, the set of safe support caps is a downward-closed interval.  More precisely, apart from a necessary `Q`-null-direction compatibility condition, its exact upper endpoint is the generalized copositive Rayleigh quotient

**`B_crit = inf_{y>=0, y^TQy>0} (y^T A y)/(y^T Q y)`.**

Consequently, if `s_*` is the true physical support, the exact admissible support-overestimate budget is

**`Delta_crit = B_crit - s_*`.**

This yields three sharply distinct outcomes:

1. `s_* < B_crit`: there is positive room for a strict support cap, hence T-P5-203's rational strict-margin packet can in principle be chosen inside the Lyapunov-safe corridor;
2. `s_* = B_crit`: the energy packet has zero support slack; every strict cap `B>s_*` breaks the exact quadratic gate, so a merely convergent support solver is not enough;
3. `s_* > B_crit`: even the exact sharp support is too large; no improvement in support-solver precision can rescue the present Lyapunov packet.

There is also a separate fourth obstruction: if some `Q`-null selector direction already has negative `A` energy, then **no value of `B` can help at all**, because the support debit vanishes on that direction.

The review also gives a no-division reserve-transport certificate and the finite multi-generator cap region.  No actual P5 source binding, real support value, cell/tube coverage, Float64 enclosure, Lean/kernel proof, independent verification, admission, or registry promotion is claimed.

---

## 1. Setup inherited from T-P5-200

Fix one selector sector with

`y >= 0`.

Assume T-P5-200's fixed-sign decomposition has already provided a symmetric matrix `Q` satisfying

`q(y) := y^T Q y >= 0`

for every `y>=0`.

The full nominal calculation, including any desired decay-rate debit already chosen upstream, has the form

`dot L <= l_tot^T y + y^T M_tot(B) y`,

where the support cap enters only through

`M_tot(B) = M_fix + BQ`.

Equivalently, define

`A := -M_fix`

and

`C(B) := -M_tot(B) = A-BQ`.

The quadratic part of the T-P5-192 gate is

`C(B)` copositive, i.e.

`y^T C(B) y >=0`

for every `y>=0`.

The linear gate `l_tot<=0` is independent of `B` in T-P5-200 and is therefore orthogonal to the present sensitivity theorem.  It remains an explicit upstream/downstream premise.

---

## 2. T204-A — exact affine transport in the support cap

For every real `B` and increment `Delta`,

**`C(B+Delta) = C(B) - Delta Q`.**

Hence for every `y>=0`,

**`y^T C(B+Delta)y = y^T C(B)y - Delta q(y)`.**

This is the entire sensitivity mechanism: a support overestimate does not create a new matrix structure; it subtracts exactly `Delta Q` from the downstream copositive margin.

### Monotonicity

If `Delta>=0` and `C(B+Delta)` is copositive, then `C(B)` is copositive because

`C(B)=C(B+Delta)+Delta Q`

is a sum of copositive matrices.

Equivalently:

> if a cap is safe, every tighter cap is safe;
> if a cap fails, every looser cap fails.

Thus the set

`S := { B in R : C(B) is copositive }`

is downward closed.

This is a mathematical statement in the copositive order; it does not depend on any particular copositivity checker.

---

## 3. T204-B — exact safe-cap threshold

For `y>=0`, write

`a(y):=y^T A y`,

`q(y):=y^T Q y>=0`.

Define the `Q`-null compatibility condition

**`q(y)=0 -> a(y)>=0` for every `y>=0`.**

When there exists at least one `y>=0` with `q(y)>0`, define the extended-real threshold

**`B_crit := inf { a(y)/q(y) : y>=0, q(y)>0 }`.**

### Theorem

`C(B)=A-BQ` is copositive iff both

1. `Q`-null compatibility holds; and
2. `B <= B_crit`.

### Proof

For a fixed `y>=0`, the copositive inequality is

`a(y)-Bq(y)>=0`.

If `q(y)=0`, this is exactly `a(y)>=0`, independent of `B`.

If `q(y)>0`, it is equivalent to

`B <= a(y)/q(y)`.

Requiring the latter inequality for every positive-`q` direction is exactly

`B <= inf_{q(y)>0} a(y)/q(y)=B_crit`.

No other condition remains. QED.

### Degenerate cases

- If `q(y)=0` for every `y>=0`, then the support cap never enters the quadratic gate; provided null compatibility holds, every `B` is safe and one may set `B_crit=+infinity`.
- If null compatibility fails, no `B` is safe, even `B -> -infinity`.
- The infimum can be `-infinity`; then no finite support cap can satisfy the present quadratic gate.

These cases should be represented explicitly rather than hidden inside a numerical generalized-eigenvalue call.

---

## 4. T204-C — exact support-error budget

Let the true support on the actually consumed physical domain be

`s_* := sup b^T y`.

Any sound T-P5-200 support cap must satisfy

`B >= s_*`.

Any sound downstream quadratic Lyapunov cap must satisfy

`B <= B_crit`.

Therefore there exists a common mathematically valid cap iff

1. the `Q`-null compatibility condition of T204-B holds; and
2. **`s_* <= B_crit`.**

Define

**`Delta_crit := B_crit-s_*`.**

If a producer reports

`B=s_*+Delta`, `Delta>=0`,

then the support cap and quadratic Lyapunov gate are simultaneously valid exactly when

**`0<=Delta<=Delta_crit`.**

This is the desired source-to-energy interface quantity.

### Interpretation

#### Positive-slack corridor: `s_* < B_crit`

There is a nonempty open interval

`(s_*, B_crit)`.

Hence there exists a rational `B` in that interval.  Under the rational-data PSD + Slater hypotheses of T-P5-203, T203-5 then supplies a fully rational, root-free **support** certificate at such a `B`.

The downstream copositivity evidence remains its own gate, but the support solver is no longer being asked for impossible exact sharpness.

#### Zero-slack contact: `s_* = B_crit`

Only the exact cap `B=s_*` can satisfy both inequalities.  Every strict overestimate fails the quadratic gate.

This matters because T-P5-203 guarantees rational certificates for **strict** rational margins, not an exact rational packet at an arbitrary sharp real support.  Thus, if the sharp support is algebraic/irrational and the Lyapunov margin is exactly zero in the support direction, a rational-overcap interface cannot close this branch.  One must instead obtain an exact algebraic support packet or improve the Lyapunov margin/storage design.

#### Negative-slack obstruction: `s_* > B_crit`

Even the true sharp support lies beyond the energy threshold.  No support optimizer, tighter numerical tolerance, or better rational approximation can repair the present T-P5-200/T-P5-192 quadratic certificate.

This is a genuine **architecture-level mathematical obstruction for this packet**, not a source-provenance or solver-accuracy issue.

---

## 5. T204-D — hard contact when `Q` is strictly copositive

Assume the stronger condition

`q(y)>0`

for every nonzero `y>=0`.

Normalize to the compact simplex

`Sigma={y>=0 : sum_i y_i=1}`.

On `Sigma`, `q` is continuous and strictly positive, so

`a(y)/q(y)`

is continuous and attains its minimum at some `y_* in Sigma`.

Therefore

`B_crit = a(y_*)/q(y_*)`

and

**`y_*^T C(B_crit)y_*=0`.**

For every `Delta>0`, the same witness gives

`y_*^T C(B_crit+Delta)y_*`

`= -Delta q(y_*) < 0`.

Hence a finite attained threshold is a literal copositive contact: any support overestimate, however small, produces an explicit negative witness on that same direction.

If `Q` is only copositive, the exact threshold theorem T204-B remains valid, but the quotient infimum need not be represented by a single positive-`q` contact without an additional compactness/coercivity premise.  A minimizing sequence is enough for the threshold semantics; do not invent a contact vector in that case.

---

## 6. T204-E — no-division reserve transport

Often the downstream proof does not know `B_crit` numerically.  It may instead possess a certified copositive reserve against some reference matrix `R`.

Assume:

1. `R` is copositive;
2. `mu>=0`;
3. `C(B0)-mu R` is copositive;
4. `kappa>=0` and `kappa R-Q` is copositive.

Then for every `Delta>=0` satisfying

**`kappa*Delta <= mu`,**

`C(B0+Delta)` is copositive.

### Proof

Use the exact decomposition

`C(B0+Delta)`

`=[C(B0)-mu R]`

` +(mu-kappa Delta)R`

` +Delta(kappa R-Q)`.

Every coefficient is nonnegative and every bracketed matrix is copositive, so the sum is copositive. QED.

### Why this is checker-friendly

The trusted packet does not divide by `kappa`.  It checks only

`mu>=0`, `Delta>=0`, `kappa*Delta<=mu`,

plus the existing copositivity certificates for

`C(B0)-mu R`, `R`, and `kappa R-Q`.

With `R=Q` and `kappa=1`, this reduces to the especially simple rule:

> a certified `Q`-relative reserve `mu` at `B0` allows any support overestimate `Delta<=mu`.

This is the preferred adapter if the downstream Lyapunov proof already exposes a rational reserve rather than an exact real `B_crit`.

---

## 7. T204-F — finite multi-generator cap region

T-P5-200-H allows finitely many affine-amplitude generators.  After all `B`-independent terms are collected, the downstream quadratic gate has the form

**`C(B_vec)=A-sum_k B_k Q_k`,**

where each `Q_k` is copositive and each sound support cap satisfies

`B_k >= s_k`,

with `s_k` the true generator support.

Define

`Safe := { B_vec : C(B_vec) is copositive }`.

Then:

1. `Safe` is convex, because the copositive cone is convex and `B_vec -> C(B_vec)` is affine;
2. `Safe` is coordinatewise downward closed, because decreasing `B_k` adds a nonnegative multiple of copositive `Q_k`;
3. the physically usable cap region is `Safe intersect {B_vec>=s_vec}`.

Thus independent support solvers should not be assigned arbitrary per-generator tolerances: their admissible errors form one coupled convex downward-closed region.

### Exact one-dimensional allocation ray

Fix a baseline cap vector `B0` and a nonnegative error-allocation direction `w>=0`.  Set

`Q_w := sum_k w_k Q_k`,

which is copositive, and consider

`B(t)=B0+t w`, `t>=0`.

Then

`C(B(t))=C(B0)-t Q_w`.

T204-B applies verbatim.  The exact maximum shared error parameter is

**`t_crit = inf_{y>=0, y^TQ_wy>0} y^T C(B0)y / y^TQ_wy`,**

subject again to the `Q_w`-null compatibility condition.

This turns a many-support tolerance allocation into the same scalar threshold problem without dropping the individual signed/gauge-preserving generator geometry.

---

## 8. Exact rational regressions

### Regression 1 — positive support slack

Take one-dimensional selector space with

`Q=[1]`,

`A=[2]`.

Then

`C(B)=[2-B]`

and

`B_crit=2`.

Suppose the true physical support is

`s_*=3/2`.

Then

`Delta_crit=1/2`.

A rational cap

`B=7/4`

has error `Delta=1/4` and leaves

`C(B)=1/4>=0`.

A looser cap

`B=5/2`

has

`C(B)=-1/2`,

so `y=1` is an exact FAIL witness.

At the sharp support baseline `B0=3/2`, choose `R=Q`, `mu=1/2`, `kappa=1`.  T204-E recovers exactly the full allowable error budget `Delta<=1/2` without division.

### Regression 2 — zero-slack interface obstruction

Take

`Q=[1]`, `A=[1]`,

and a physical support problem with

`s_*=1`.

Then

`B_crit=1=s_*`.

At the exact cap,

`C(1)=0`.

For every `epsilon>0`,

`C(1+epsilon)=-epsilon<0`.

Thus every strict overestimate fails, even though arbitrarily accurate strict support caps exist.  This is the minimal example showing that **support-certification convergence and Lyapunov closure are not the same requirement**.

### Regression 3 — a `Q`-null obstruction that no support cap can repair

Take

`Q=diag(1,0)`,

`A=diag(2,-1)`.

For `y=e2=(0,1)`,

`q(y)=0`

but

`a(y)=-1`.

Hence

`y^T C(B)y=-1`

for every real `B`.

No refinement of the support constant can affect this direction.  The nominal/storage packet itself must change.

---

## 9. Optional decay-rate corollary

T-P5-200 treats the desired decay rate as already absorbed into `M0`.  If a particular downstream formulation exposes the rate explicitly as

`C_gamma(B)=A-BQ-gamma R_gamma`

with `R_gamma` copositive, then increasing `gamma` can only shrink the safe-cap set.  In particular,

`gamma2>=gamma1`

implies

`Safe(gamma2) subseteq Safe(gamma1)`.

Thus

`B_crit(gamma)`

is nonincreasing in `gamma` whenever the rate enters with this copositive sign.  This gives a clean rate-versus-support-precision Pareto interface.  No such sign representation should be assumed unless the actual Lyapunov normalization provides it.

---

## 10. Minimal theorem statements for formalization

### T204-1 `supportCap_matrix_transport`

For symmetric `A,Q`,

`C B := A-B•Q`.

Prove

`C (B+Delta)=C B-Delta•Q`

and the corresponding quadratic-form identity.

### T204-2 `copositive_supportCap_antitone`

If `Q` is copositive, `Delta>=0`, and `C(B+Delta)` is copositive, then `C(B)` is copositive.

### T204-3 `copositive_supportCap_iff_threshold`

Assume `Q` copositive.  Then `A-BQ` is copositive iff

- every nonnegative `Q`-null vector has nonnegative `A` quadratic form; and
- for every `y>=0` with `y^TQy>0`, `B(y^TQy)<=y^TAy`.

This multiplication-only statement is preferable in Lean to defining an extended-real infimum first.

A corollary may introduce `B_crit` as the infimum quotient.

### T204-4 `supportAndLyapunov_cap_exists_iff`

Given true support `s_*`, prove that a real cap `B` with

`s_*<=B`

and

`A-BQ` copositive

exists iff the null compatibility holds and `s_*<=B_crit`.

### T204-5 `copositive_reserve_supportSlack`

If

- `C(B0)-mu R` copositive,
- `R` copositive,
- `kappa R-Q` copositive,
- `Delta>=0`,
- `kappa Delta<=mu`,

then `C(B0+Delta)` is copositive.

The proof is one exact matrix decomposition and closure of the copositive cone under nonnegative scaling/addition.

### T204-6 `multiSupport_safeRegion_convex_antitone`

For copositive `Q_k`, prove that

`{B_vec : A-sum_k B_k Q_k is copositive}`

is convex and coordinatewise downward closed.

### T204-7 `strictCopositive_supportThreshold_contact`

If `Q` is strictly copositive on nonzero nonnegative vectors and `B_crit` is finite, prove existence of normalized `y_*>=0` with

`y_*^T(A-B_crit Q)y_*=0`,

and show the same `y_*` makes every `B>B_crit` fail.

---

## 11. Suggested interface/checker routing

For one actual T-P5-200 generator or a finite generator packet:

1. keep the support problem and the Lyapunov-margin problem as separate typed objects;
2. obtain a sound physical support cap `B` from T-P5-203/T-P5-201/T-P5-199 or another source-bound route;
3. expose the downstream cap dependence exactly as `C(B)=A-BQ` rather than burying `B` inside one large matrix;
4. check the `Q`-null directions first: a negative null direction is irreparable by support tightening;
5. if an exact threshold is needed, use the multiplication form `B q(y)<=a(y)` / generalized copositive quotient;
6. if a rational reserve is already available, prefer T204-E and pass a rational error budget back to the support solver without computing `B_crit`;
7. for multiple generators, allocate support tolerances jointly in the convex downward-closed safe cap region rather than independently;
8. only label a support-precision obstruction when `s_*>B_crit` (or the null gate fails); failure to find a particular copositivity certificate is not itself that mathematical obstruction.

---

## 12. Boundaries remaining OPEN

This review does not prove:

1. the actual source-bound values of `A,Q,b,c,h0` or any `B_k`;
2. the actual sharp physical support `s_*` or `s_k`;
3. that the actual consumed selector/domain packet satisfies the T-P5-200 fixed-sign hypotheses;
4. actual cell/tube/trajectory/global coverage;
5. that the linear gate `l_tot<=0` holds;
6. that the actual P5 matrices admit a computable positive `Delta_crit`;
7. a Float64/directed-rounding implementation of threshold or reserve checks;
8. a Lean/kernel proof or axiom scan;
9. independent verification by 封不觉;
10. admission, registry, P5/P8/M4, or global Route-B closure.

All remain open.

---

## 13. New structural fingerprint

The cross-layer chain is now

**physical support optimization**

`-> sharp support s_* / certified cap B`

`-> T-P5-200 exact debit A-BQ`

`-> Q-null compatibility`

`-> generalized copositive support threshold B_crit`

`-> admissible support error Delta_crit=B_crit-s_*`

`-> rational reserve/tolerance packet`

`-> T-P5-192 cone-wise Lyapunov gate`.

The important separation is semantic:

- a support solver answers whether `B` is a valid upper bound on the physical amplitude slope;
- the Lyapunov checker answers whether that valid cap is sufficiently tight;
- T204 quantifies the exact bridge between the two.

A valid support certificate can therefore still be useless for Lyapunov closure, and a failed Lyapunov gate does not by itself invalidate the support certificate.

---

## 14. Next mathematical seam

After T204, the next genuinely new interface is not another scalar tightening argument.  It is the **source-bound reserve extraction problem**: derive a concrete `Q`-relative or reference-matrix copositive reserve `(mu,R,kappa)` from the actual T-P5-192 sector certificate, so T204-E can return a rational tolerance budget directly to the T-P5-203 support solver.

A second, disjoint mathematical continuation is the multi-generator allocation problem: optimize rational error shares inside the convex safe-cap region while preserving the common physical/source key.

Neither continuation should be confused with provenance/admission work.