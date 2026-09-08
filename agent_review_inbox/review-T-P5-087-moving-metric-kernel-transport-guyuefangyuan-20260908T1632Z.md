---
kind: review_result
review_id: review-T-P5-087-moving-metric-kernel-transport-guyuefangyuan-20260908T1632Z
task_id: T-P5-087-MOVING-METRIC-KERNEL-TRANSPORT
agent: 古月方源
source_agent: 古月方源
reviewer: 古月方源
created_at: 2026-09-08T16:32:00Z
claim_commit: adc01a97abf721d2659189587293aafc3377e36d
reviewed_commit: 6f96c363348d39ac218b07ba30f5011edbe70314
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
summary: >-
  Close the mathematical gap explicitly left by T-P5-086 when the physical
  quadratic metric varies with time/state. A uniform quadratic-form comparator
  from each path metric to the exact endpoint metric transports the correlated
  moving-frame curvature packet through the triangular kernel with no square
  roots or matrix inverses. The trusted gate is h^4 M K <= 4 m D. A second
  exact theorem derives the comparator from a common anchor coercivity plus
  two metric-drift envelopes, and a diagonal-dominance certificate reduces a
  general symmetric matrix comparator to rational scalar inequalities.
---

# T-P5-087 — moving-metric transport for the T-P5-086 Euler defect

## 0. Why this child is needed

T-P5-086 proved, for a **fixed** physical PSD weight `W`, that the moving-frame
Euler defect

`r_mov = h^2 ∫_0^1 (1-s) C(s) ds`

satisfies

`Q_W(r_mov) <= h^4 K_C / 4`

whenever `Q_W(C(s)) <= K_C` along the entire spacetime Euler path. That review
explicitly left state/time-dependent physical metrics open.

The missing point is subtle: if the source naturally proves a local packet in a
metric `W_s = W(gamma(s))`, one may **not** simply put `W_s` inside the old Jensen
line and conclude a bound in an endpoint metric. The quadratic form used after
the integral must first be held fixed, or the moving forms must be compared to
that fixed consumer metric.

This review supplies the minimal comparison theorem and two exact-rational ways
to certify it.

## 1. Main theorem: moving path metrics -> endpoint metric

For any symmetric PSD weight `W`, write

`Q_W(v) := v^T W v`.

Let `W_*` be the exact metric in which the downstream consumer wants to measure
the defect. It may be, for example, the metric at `T(t+h,z-hG0)` or at the
physical Euler endpoint, but the source key must say which one. Let `W_s` be a
possibly state/time-dependent path metric.

Assume constants

`m > 0`, `M >= 0`, `K >= 0`

such that for every `s in [0,1]` and every vector `v`,

**(1.1) metric comparison**

`m Q_{W_*}(v) <= M Q_{W_s}(v)`,

and along the T-P5-086 spacetime path

**(1.2) moving curvature packet**

`Q_{W_s}(C(s)) <= K`.

Then, with

`I := ∫_0^1 (1-s) C(s) ds`,

one has the division-free inequality

**(1.3)** `4 m Q_{W_*}(I) <= M K`.

Consequently, for `r_mov=h^2 I`,

**(1.4)** `4 m Q_{W_*}(r_mov) <= h^4 M K`.

Hence an exact-rational requested budget `D_mov>=0` is certified by the single
scalar gate

**(1.5)** `h^4 M K <= 4 m D_mov`.

No square root, generalized eigenvalue, matrix inverse, or division is needed by
the trusted consumer.

### Proof

Because `W_*` is fixed, weighted Cauchy/Jensen for the positive kernel
`a(s)=1-s` gives

`Q_{W_*}(I)`
` <= (∫ a)(∫ a Q_{W_*}(C(s)))`
` = (1/2) ∫_0^1 (1-s) Q_{W_*}(C(s)) ds`.

Multiply by `m` before using any ratio. From (1.1)-(1.2),

`m Q_{W_*}(C(s)) <= M K`.

Therefore

`m Q_{W_*}(I)`
` <= (1/2) ∫_0^1 (1-s) M K ds`
` = M K / 4`.

This is (1.3). Quadratic homogeneity gives
`Q_{W_*}(h^2 I)=h^4 Q_{W_*}(I)`, yielding (1.4), and (1.5) closes the requested
budget.

### Exact sharpness at the information level

The factor `1/4` and the metric-comparison loss are jointly sharp from only
(1.1)-(1.2). In one dimension take constant path metric

`Q_{W_s}(v)=m v^2`,

endpoint metric

`Q_{W_*}(v)=M v^2`,

and constant `C(s)=1`. Then (1.1) is equality, `K=m`, and
`I=1/2`. Thus

`4m Q_{W_*}(I)=mM=MK`.

Any generic improvement needs additional signed/correlated information about
`C(s)` or the metric path.

## 2. Cheaper post-transport corollary

If T-P5-086 is already run in one fixed anchor metric `W0`, so that

**(2.1)** `4 Q_{W0}(r_mov) <= h^4 K0`,

then only an endpoint comparator is needed:

**(2.2)** `m Q_{W_*}(v) <= M Q_{W0}(v)` for every `v`.

Immediately

**(2.3)** `4m Q_{W_*}(r_mov) <= M h^4 K0`.

So the source lane should prefer this cheaper route when it can bound the whole
correlated curvature in one anchor metric. The fully moving theorem in Section 1
is needed only when the natural curvature packet itself is expressed in `W_s`.

## 3. Source-friendly comparator from a common anchor + drift

A source usually will not want to solve a generalized eigenvalue problem for
every `s`. The following exact theorem converts ordinary quadratic metric-drift
bounds into (1.1).

Let `W0` be a fixed anchor metric and suppose, for every `v`,

**(3.1) anchor coercivity**

`m0 ||v||^2 <= Q_{W0}(v)`,

**(3.2) path drift**

`|Q_{W_s}(v)-Q_{W0}(v)| <= delta_p ||v||^2`,

**(3.3) endpoint drift**

`|Q_{W_*}(v)-Q_{W0}(v)| <= delta_e ||v||^2`.

Instead of forming `m0-delta_p` by division-sensitive downstream arithmetic,
let the certificate choose rational `m,M` and check only

**(3.4)** `0 < m`,

**(3.5)** `m + delta_p <= m0`,

**(3.6)** `m0 + delta_e <= M`.

Then for every `s,v`,

**(3.7)** `m Q_{W_*}(v) <= M Q_{W_s}(v)`.

### Proof

From (3.1)-(3.2) and (3.5),

`Q_{W_s}(v)`
` >= Q_{W0}(v)-delta_p||v||^2`
` >= (m0-delta_p)||v||^2`
` >= m||v||^2`.

Also (3.2)-(3.3) imply

`Q_{W_*}(v) <= Q_{W_s}(v)+(delta_p+delta_e)||v||^2`.

Multiplying by `m` and using `m||v||^2<=Q_{W_s}(v)`,

`m Q_{W_*}(v)`
` <= (m+delta_p+delta_e)Q_{W_s}(v)`
` <= (m0+delta_e)Q_{W_s}(v)`
` <= M Q_{W_s}(v)`.

Thus a common anchor coercivity plus two additive metric-drift envelopes gives a
uniform moving-metric comparator using only rational addition, multiplication,
absolute-value bounds, and order checks.

For a symmetric uniform drift budget `delta_p=delta_e=delta`, one may choose any
positive rational reserve `m` with `m+delta<=m0`, and `M=m0+delta`.

## 4. Exact matrix-entry certificate; no eigenvalue calculation required

The direct comparator (1.1) is the PSD statement

`D_s := M W_s - m W_* >= 0`.

A simple rational sufficient certificate is symmetric diagonal dominance. For
uniform rational bounds `c_ij>=0`, assume for all `s`:

- `D_s` is symmetric;
- `|(D_s)_ij| <= c_ij` for `i != j`, with `c_ij=c_ji`;
- `(D_s)_ii >= sum_{j != i} c_ij` for every `i`.

Then for every vector `v`,

`v^T D_s v`
` >= sum_i (D_ii-sum_{j!=i} c_ij) v_i^2 >= 0`,

because each cross term obeys

`2 c_ij |v_i v_j| <= c_ij(v_i^2+v_j^2)`.

Therefore (1.1) follows. This gives a direct CSE/interval path: form the **signed
matrix difference `M W_s - m W_*` first**, then enclosure its diagonal and
off-diagonal entries. Do not separately replace both metrics by scalar norms
before forming the difference; that destroys useful cancellation.

A Lean-facing helper can be finite-dimensional and purely algebraic:

`diagDominant_psd_of_offdiag_abs_le`.

## 5. Exact obstruction: pointwise SPD is not enough

There is no theorem of the form

"each `W_s` and `W_*` is positive definite, and `Q_{W_s}(C(s))<=1`, therefore the
endpoint defect has a uniform bound independent of metric comparison."

For any positive integer `N`, in one dimension set

`Q_{W_s}(v) = v^2 / N^2` for every `s`,

`Q_{W_*}(v) = v^2`,

and `C(s)=N`.

Every metric is strictly positive definite and

`Q_{W_s}(C(s))=1` exactly.

But

`I = ∫_0^1 (1-s)N ds = N/2`,

so

`Q_{W_*}(I)=N^2/4`,

which is unbounded as `N` grows. All quantities can be chosen rational. Thus a
quantitative cross-metric comparison such as (1.1), or an equivalent anchor
packet such as Section 3, is mathematically irreducible.

This also shows why checking only `W_*>0` and `W_s>0` is not a valid repair for
the state-dependent-metric gap in T-P5-086.

## 6. Consumer semantics and an important boundary

The endpoint metric key must be explicit. The following are different objects:

- `W(t+h, x_E)` at the physical Euler endpoint;
- `W(t+h, x_chart)` at the charted Euler endpoint;
- a metric at a corrected endpoint after an additional P5 corrector.

T-P5-087 transports to whichever `W_*` appears in the comparator; it does not
silently identify these evaluations. If the corrector changes the metric
argument, add another comparator or enlarge the common drift tube.

Also, this theorem concerns a **metric used to measure the defect**. If the
Lyapunov storage itself is state/time dependent, for example
`V(t,x)=x^T W(t,x)x`, its continuous/discrete evolution contains separate
`W_t`/`D_x W` terms. T-P5-087 does not erase those terms and must not be used as
a replacement for a moving-storage derivative theorem.

## 7. Suggested minimal Lean decomposition

The smallest useful formalization order is:

1. `quad_compare_trans` — pointwise scalar transport
   `m*Qstar v <= M*Qs v` plus `Qs v<=K`;
2. `anchor_drift_quad_compare` — Sections 3.1-3.7, purely ordered-ring algebra;
3. `diagDominant_psd_of_offdiag_abs_le` — finite-sum algebraic PSD certificate;
4. `moving_metric_triangle_kernel_sq` — fixed endpoint quadratic form + integral
   kernel + path comparator;
5. `moving_metric_defect_budget_of_mul_le` — final scalar gate
   `h^4*M*K <= 4*m*D`.

If the T-P5-086 fixed-weight integral lemma is formalized first, the cheap
Section-2 post-transport corollary can land before the fully moving integral
lemma.

## 8. Dependencies and remaining obligations

Depends mathematically on T-P5-086's exact moving-frame Euler identity and its
triangular-kernel weighted square argument. It is compatible with the existing
P5 additive/correlation-aware defect lane.

Still open and explicitly not claimed here:

- deployed chart/source identity and exact endpoint metric semantics;
- a same-path rational `K` for the correlated curvature;
- a same-tube comparator packet `(m,M)` or anchor packet
  `(m0,delta_p,delta_e)`;
- spacetime path/tube inclusion;
- state/time-dependent **storage** derivative terms if the Lyapunov functional
  itself moves;
- Float64/FD/controller/solve semantics;
- P8/ODE trajectory coverage;
- Lean/kernel compilation, comparator, independent validation by 封不觉;
- receipt/provenance/admission/registry or P5/P8/M4 parent closure.

Status is **pending mathematical child / conditional pass** until those typed
source and formal consumers exist.
