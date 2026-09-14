---
kind: review_result
review_id: review-T-P5-116-homogeneous-anchor-small-gain-honglianmozun-20260909T0158Z
task_id: T-P5-116-HOMOGENEOUS-ANCHOR-SMALL-GAIN
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T01:58:00Z
claim_commit: e34591f57ea68fb198728eb2c2a797fef4264e24
inspected_commit: 4bc87f6f203025d6fc67c71c3bc231b91f2dbb9b
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET-guyuefangyuan-20260909T0030Z.md
    commit: 3072f9b62a333f96448defd626a67039adb50168
  - path: agent_review_inbox/review-T-P5-113-anchor-defect-power-absorption-honglianmozun-20260909T0057Z.md
    commit: de258fc7cb4ab6aa6df6ddf09d8ad137537c971d
  - path: agent_review_inbox/review-T-P5-114-SIGNED-SECOND-JET-ENERGY-CLOSURE-guyuefangyuan-20260909T0136Z.md
    commit: e07b619f6584356f39333601ea73b51fca216fa3
  - path: agent_review_inbox/review-T-P5-115-ROOT-FREE-SECOND-JET-INDEPENDENT-ENERGY-kuangmanmozun-20260909T0143Z.md
    commit: 940c7ba38cea17892253b00b2d2c1429378a1917
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
---

# T-P5-116 — homogeneous second-jet anchor defect as a Lyapunov small-gain term

## 0. New seam

T-P5-112 proves the inverse-free affine-anchor remainder bound

`4 gamma Q_A(r_anchor) <= H2`.

T-P5-113 shows how an absolute `H2` enters the energy ledger through the signed
power `p_A=<u,r_anchor>`, but that treatment makes the anchor error look like an
additive disturbance.

T-P5-115 contains more structure.  Before the cell-radius collapse, its
homogeneous specialization is pointwise in the anchor displacement:

`Q_R(J2) <= h * Q_Z(delta)^2`.

Combined with T-P5-112 this gives

**(0.1)** `4 gamma Q_A(r_anchor) <= h * Q_Z(delta)^2`.

The purpose of this child is to retain that factor instead of immediately
replacing `Q_Z(delta)` by a cell-wide constant `S`.  The result is a standard
nonlinear small-gain phenomenon: the affine-anchor error is quadratic in the
state displacement, its power is cubic, and on a sufficiently small Lyapunov
sublevel it consumes only decay rate/dissipation reserve.  No additive ultimate
ball is mathematically necessary for this channel when the homogeneous packet is
really available.

No actual source identity, segment coverage, deployed metric, Float64 behavior,
Lean receipt, admission, or registry promotion is claimed here.

---

## 1. Pointwise anchor-power packet

Let all quadratic quantities below be nonnegative.  Assume on the same physical
anchor segment / Lyapunov domain:

1. homogeneous second-jet anchor control

   **(1.1)** `4 gamma Q_A(r_A) <= h Q_Z(delta)^2`, with `gamma>0`, `h>=0`;

2. the actual energy pairing uses the same anchor error,

   **(1.2)** `p_A^2 <= Q_U(u) Q_A(r_A)`;

3. positive dissipation coercivity for the multiplier/velocity channel,

   **(1.3)** `d Q_U(u) <= Qd`, with `d>0`.

Multiplying the nonnegative inequalities gives the exact square-only packet

**(1.4)**

`4 gamma d p_A^2 <= h Q_Z(delta)^2 Qd`.

This is already stronger than the absolute T-P5-113 packet whenever the state is
near the anchor: it records that the anchor power vanishes at least quadratically
in the displacement norm before its final pairing with `u`.

The same formula works with any smaller `h` produced by the signed/correlated
T-P5-114 packet.  T-P5-115's independent-energy discriminant fallback simply
provides one source-independent way of certifying a rational coefficient `h`
when signed Gram data are unavailable.

---

## 2. Storage coercivity turns the quartic second-jet scale into `V^2`

Assume the **same Lyapunov storage appearing in the derivative ledger** controls
the anchor displacement through a rational/nonnegative comparator

**(2.1)** `m Q_Z(delta) <= V`, with `m>0`, `V>=0`.

Because both sides are nonnegative,

**(2.2)** `m^2 Q_Z(delta)^2 <= V^2`.

Multiplying (1.4) by `m^2` and using (2.2) yields

**(2.3)**

`4 gamma d m^2 p_A^2 <= h V^2 Qd`.

Now restrict to a candidate Lyapunov sublevel

**(2.4)** `0 <= V <= R`, `R>=0`.

Then `V^2 <= R V`, hence

**(2.5) HOMOGENEOUS ANCHOR POWER ENVELOPE**

`4 gamma d m^2 p_A^2 <= h R V Qd`.

This is the key new bridge.  An anchor remainder that would have been charged as
an absolute constant after the replacement `Q_Z(delta)<=S` becomes a
radius-dependent relative power packet if the homogeneous factor is preserved.

---

## 3. General reserve-allocation theorem

Suppose the nominal energy ledger is

**(3.1)** `Vdot <= -c V - Qd + p_A`,

with `c>=0`, `V>=0`, `Qd>=0`, and (2.5) holds on `V<=R`.

Choose desired losses `alpha>=0` and `theta>=0`.  Check the single
root-free/division-free scalar gate

**(3.2)**

`h R <= 16 gamma d m^2 alpha theta`.

From (2.5) and (3.2), positivity of `gamma,d,m` gives

`p_A^2 <= 4 alpha theta V Qd`.

The exact square identity

**(3.3)**

`(alpha V + theta Qd)^2 - 4 alpha theta V Qd`
`= (alpha V - theta Qd)^2 >= 0`

therefore implies

**(3.4)** `p_A <= |p_A| <= alpha V + theta Qd`.

Substitution into (3.1) gives

**(3.5)**

`Vdot <= -(c-alpha) V - (1-theta) Qd`.

Thus if

`alpha < c`, `theta < 1`,

the anchor defect is absorbed **homogeneously** and leaves positive decay and
positive dissipation reserve.  There is no additive `beta` and hence no
anchor-induced ultimate-ball floor.

### Target-margin form

If the desired retained margins are `c_keep>=0`, `d_keep>=0` with

`c_keep < c`, `d_keep < 1`,

set

`alpha = c-c_keep`, `theta = 1-d_keep`.

Then the one checker gate is

**(3.6)**

`h R <= 16 gamma d m^2 (c-c_keep)(1-d_keep)`,

and the conclusion is exactly

**(3.7)** `Vdot <= -c_keep V - d_keep Qd`.

This is a useful certificate interface because the trusted checker can keep all
parameters rational and never compute a critical radius by division.

---

## 4. Simple half-reserve corollary

A particularly clean fixed choice is

`alpha=c/2`, `theta=1/2`.

Then (3.2) reduces to

**(4.1)**

`h R <= 4 gamma d m^2 c`.

Whenever `c>0` and (4.1) holds,

**(4.2)**

`Vdot <= -(c/2) V - (1/2) Qd`.

This gives a no-tuning bootstrap suitable for a first implementation: certify a
sublevel radius `R`, check one polynomial inequality, and retain exactly half of
both the nominal `V` rate and the dissipative quadratic reserve.

---

## 5. Critical-radius interpretation and sharpness

For mere nonincrease one may spend the full nominal reserves, `alpha=c` and
`theta=1`.  The limiting gate is

**(5.1)** `h R <= 16 gamma d m^2 c`.

A strict inequality in (5.1) is precisely what permits some choice
`alpha<c`, `theta<1` and hence strictly positive retained margins.  In ordinary
real notation, when `h>0`, this corresponds to the critical small-gain radius

`R_crit = 16 gamma d m^2 c / h`,

but the checker should use the cross-multiplied form (5.1), not the division.

The constant in (3.2) is sharp under only the squared-envelope information
(2.5).  Indeed, after normalizing the positive coefficient, the question is
whether every scalar `p` satisfying

`p^2 <= C V Qd`

also satisfies

`p <= alpha V + theta Qd`.

The minimum over positive ratios `V/Qd` of

`(alpha V + theta Qd)^2/(V Qd)`

is exactly `4 alpha theta`, attained when `alpha V=theta Qd`.  Therefore if
`C>4 alpha theta`, a one-dimensional aligned witness violates the proposed power
bound.  No different Young tuning can improve (3.2) without additional signed or
correlation information.

So the only ways to enlarge the certified sublevel are structural:

- reduce `h` by preserving signed second-jet cancellation (T-P5-114);
- improve the lower gain `gamma`;
- improve the storage/displacement coercivity `m`;
- improve the dissipation comparator `d`;
- or use extra correlation between `p_A`, `V`, and `Qd`.

---

## 6. Preconditioner route

T-P5-112 also gives the preconditioner alternative

`4(1-kappa)^2 Q_A(r_A) <= chi H2`,

with `0<=kappa<1`.  If the homogeneous second-jet packet is kept as

`H2 <= h Q_Z(delta)^2`,

then the same proof gives

**(6.1)**

`4(1-kappa)^2 d m^2 p_A^2 <= chi h V^2 Qd`,

and on `V<=R`,

**(6.2)**

`4(1-kappa)^2 d m^2 p_A^2 <= chi h R V Qd`.

Hence the target-margin gate becomes

**(6.3)**

`chi h R <= 16(1-kappa)^2 d m^2 alpha theta`,

which again implies

`p_A <= alpha V + theta Qd`

and therefore (3.5).  This lets the source choose either the direct lower-gain
packet or the preconditioner packet without changing the downstream Lyapunov
architecture.

---

## 7. Why the source should not collapse to `S^2` too early

T-P5-115 legitimately derives a cell-wide absolute consequence

`Q_R(J2) <= h S^2`

from `Q_Z(delta)<=S`.  That is the right object if the downstream consumer wants
one uniform anchor box budget.  It is **not** the best object for an energy
consumer.

If the pointwise factor is discarded and only the constant `h S^2` remains,
T-P5-113 can conclude only an absolute power budget.  Such a packet no longer
records that the remainder vanishes at the anchor, so it generally enters the
`beta` / ultimate-bound ledger.

By contrast, retaining

`Q_R(J2) <= h Q_Z(delta)^2`

until after the storage comparison exposes the nonlinear order and yields the
homogeneous small-gain gate (3.2).

Therefore the recommended source packet is two-layered:

- preserve `h` and the symbolic factor `Q_Z(delta)^2` for Lyapunov consumers;
- derive `h S^2` only as a separate uniform-cell corollary for consumers that
  genuinely require an absolute box budget.

This is not a stronger source assumption.  It is an information-retention rule.

---

## 8. Exact failure boundaries / obstructions

### 8.1 No storage coercivity, no homogeneous absorption

The field `m>0` in `m Q_Z(delta)<=V` is essential.  A positive-semidefinite
storage can vanish along a nonzero displacement direction that is still visible
to `Q_Z`.

For example, take `V(x,y)=x^2` and `Q_Z(x,y)=x^2+y^2`.  Along `(0,y)` with
`y!=0`, `V=0` while `Q_Z>0`.  A homogeneous second-jet remainder may therefore
remain nonzero on the zero-storage set.  No finite positive `m` exists, and the
radius argument above is invalid.

The fix is a genuine storage/displacement comparator, a restricted state
subspace eliminating the kernel, or fallback to an additive budget.  SPD of an
unrelated metric does not repair this typed gap.

### 8.2 A cell-wide cap alone does not imply the small-gain theorem

Knowing only

`Q_R(J2)<=h S^2`

with fixed `S>0` cannot justify replacing it by `O(V^2)`.  As `V->0`, the right
side stays constant.  The homogeneous conclusion therefore requires the
pointwise factorization in `Q_Z(delta)` (or another state quantity already
coerced by `V`), not merely a numerical cell maximum.

### 8.3 The same storage convention is required

The comparator `m Q_Z(delta)<=V`, the sublevel `V<=R`, and the derivative ledger
`Vdot<=-cV-Qd+p_A` must use the same scalar storage convention.  A Hessian or
`P_active` identity does not by itself fix additive normalization, and silently
shifting `V` changes the value-level sublevel geometry even though `Vdot` is
unchanged.  The active-V normalization obstruction from the earlier P4/P5 work
therefore remains relevant here.

### 8.4 Do not double count the same graph error

If the actual energy identity has already incorporated `r_anchor` inside another
reference/residual channel, the present `p_A` is not an additional debit.  The
source/consumer must expose a typed decomposition showing whether the anchor
remainder is a new term or merely a refinement of an existing one.  T-P5-113's
double-counting guard remains in force.

### 8.5 Segment coverage is still upstream

The homogeneous coefficient `h` is useful only if the second-jet inequalities
hold on the same physical anchor segment used by T-P5-112.  An anchor-point
Hessian value, an independent `(sin,cos)` straight segment, or a different cell
metric cannot be substituted into (1.1).

---

## 9. Candidate theorem statements for a later Lean sidecar

A minimal source-independent decomposition is:

1. `anchor_power_homogeneous_packet`

   assumptions:
   `4*gamma*QA <= h*QZ^2`, `p^2<=QU*QA`, `d*QU<=Qd`;

   conclusion:
   `4*gamma*d*p^2 <= h*QZ^2*Qd`.

2. `storage_coercive_anchor_sublevel_packet`

   assumptions:
   `m*QZ<=V`, `0<=V`, `V<=R`, plus theorem 1;

   conclusion:
   `4*gamma*d*m^2*p^2 <= h*R*V*Qd`.

3. `anchor_small_gain_absorption`

   assumptions:
   theorem 2 plus
   `h*R <= 16*gamma*d*m^2*alpha*theta` and nonnegativity;

   conclusion:
   `p <= alpha*V + theta*Qd`.

4. `anchor_small_gain_energy_decay`

   adds
   `Vdot <= -c*V-Qd+p`, `alpha<=c`, `theta<=1`;

   conclusion:
   `Vdot <= -(c-alpha)*V-(1-theta)*Qd`.

All four statements can be proved with ordered-ring arithmetic, PSD pairing
premises supplied abstractly, and the square identity (3.3).  No square root,
matrix inverse, exponential, or ODE API is required in the algebraic core.

---

## 10. Remaining physical/source obligations

This child is ready to consume an actual packet only after the source lanes bind:

- the exact physical anchor remainder appearing in the deployed energy identity;
- the same-segment homogeneous second-jet coefficient `h` (prefer signed/correlated
  T-P5-114 data; otherwise T-P5-115's discriminant fallback);
- a compatible pairing metric and positive dissipation comparator `d`;
- a same-storage comparator `m Q_Z(delta)<=V` on the candidate sublevel;
- the actual `V` normalization and candidate radius `R`;
- confirmation that the anchor term is not already contained in another residual
  channel.

Until those fields are source-bound and their domain coverage is proved, this
remains a source-independent mathematical child.  It does not alter any parent
status or registry gate.

## 11. Main handoff

The most valuable handoff is not another global constant.  **Keep the
coefficient-level homogeneous packet**

`Q_R(J2) <= h Q_Z(delta)^2`

alive through the source interface.  Once a Lyapunov storage controls
`Q_Z(delta)`, the graph-anchor error behaves as a nonlinear small-gain term and
can be absorbed by the polynomial gate

`h R <= 16 gamma d m^2 (c-c_keep)(1-d_keep)`.

Collapsing to `h S^2` before this point destroys that rate information and can
artificially turn a vanishing nonlinear remainder into an additive disturbance.
