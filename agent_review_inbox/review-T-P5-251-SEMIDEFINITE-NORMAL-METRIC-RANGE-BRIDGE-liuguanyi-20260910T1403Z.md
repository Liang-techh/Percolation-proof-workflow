---
kind: review_result
review_id: review-T-P5-251-semidefinite-normal-metric-range-bridge-liuguanyi-20260910T1403Z
task_id: T-P5-251-SEMIDEFINITE-NORMAL-METRIC-RANGE-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T14:03:00Z
claim_commit: f60d424f823506edfb91c8107d107a57bceb3dbd
inspected_commit: 835f80db550c24f0b9058645406d08077a7cebd5
upstream_commits:
  - 3e31954f21aa78b31754e314e8ded0b27922cc38  # T-P5-250 thick affine tube equality multiplier
  - 90206be9153fffcb2d5363624794346e4879dc8c  # T-P5-249 rectangular affine image/equality multiplier
  - a25de2d6e01b16133af9dc40d46efcfef6731ef8  # T-P5-247 affine GL(n) covariance
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_semidefinite_tube_slemma; add_range_gated_generalized_schur; add_fraction_free_maximal_anchor_packet; correct_zero_radius_dispatch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic algebra; generalized Schur factorization; rational maximal-principal-anchor elimination; counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-251 — Semidefinite normal metric, range gate, and partial-tube quotient bridge

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-250 closed the thick affine-tube branch under `W>0` and explicitly left the
semidefinite normal metric `W>=0`, `ker(W) != 0` as the next distinct seam.
The key distinction is that a singular normal metric defines a **partial tube**:
it controls only the `range(W)` component of the residual and leaves
`ker(W)` directions unpenalized.

This review proves four facts needed by the adapter mathematics:

1. the one-constraint S-lemma from T-P5-250 remains lossless for `W>=0`; positive definiteness of `W` was not needed there;
2. the **metric-reserve reuse** of an exact-image equality multiplier acquires an exact range/annihilation gate `range(Y) subset range(W)`;
3. after that gate, the generalized Schur complement has an inverse-free solution witness `W Z = Y`, and for rational data admits a fully fraction-free maximal-principal-anchor packet;
4. the `eta=0` dispatcher changes qualitatively: for singular `W`, zero tube radius means `W C ξ=0`, not `C ξ=0`.

A range-gate failure is a hard failure of the specific normal-metric reserve packet,
**not** automatically a failure of the original tube safety problem; an explicit
safe counterexample is included below.

No actual P5 `C,W,Y,S,eta` source identity, tube/trajectory coverage, Float64
semantics, Lean receipt, independent validation, admission or registry mutation is
claimed.

---

# Part I — the exact S-lemma does not need `W>0`

## 1. Partial tube

Let

`ξ=[y;1] in R^N`,

`C in R^{r x N}`,

`W=W^T >= 0`,

and `eta>0`.

Define

`e(y):=C ξ`,

`T_eta(W):={y : e(y)^T W e(y) <= eta^2}`.

Let `E=e_N e_N^T`, so `ξ^T E ξ=1` on the affine slice.
Let `B=B^T` be the quadratic slack whose nonnegativity is required.
Assume strict Slater for the single quadratic inequality:

`exists y0, e(y0)^T W e(y0) < eta^2`.

For the intended thickening of a nonempty exact image this is automatic whenever
`eta>0`, since `Cξ=0` gives strict inequality.

## 2. Theorem 1 — semidefinite-tube S-lemma

Under the preceding Slater assumption,

`ξ^T B ξ >= 0  for all y in T_eta(W)`

if and only if there exists `tau>=0` such that

**`B + tau C^T W C - tau eta^2 E >= 0`.**

### Proof

The constraint is the single quadratic

`g(y)=eta^2-e(y)^T W e(y)`.

The usual lossless one-constraint S-lemma uses strict feasibility of `g`; it does
not require the quadratic part of `g` to be negative definite. Therefore

`B - tau(eta^2 E-C^TWC) >= 0`

for some `tau>=0` is equivalent to nonnegativity of `B` on `g>=0`. QED.

### Consequence

A singular `W` does **not** create a new obstruction for the exact one-tube
criterion itself. The obstruction appears only when one tries to reuse the
T-P5-249 exact-image equality multiplier through the metric-reserve completion
used in T-P5-250.

---

# Part II — generalized Schur complement with the exact range gate

## 3. Abstract block theorem

Let

`A=A^T in R^{N x N}`,

`Y in R^{r x N}`,

`W=W^T >=0`,

`tau>0`.

Consider

`M_tau(A,Y,W) = [[A, Y^T], [Y, tau W]]`.

## 4. Theorem 2 — `semidefiniteMetric_blockPSD_iff`

The following are equivalent:

(A) `M_tau(A,Y,W) >=0`.

(B) both

**range gate**

`ker(W) subset ker(Y^T)`,

or equivalently

**`range(Y) subset range(W)`**, 

and there exists a matrix `Z` with

**`W Z = Y`**

such that

**`A - tau^{-1} Y^T Z >=0`.**

The matrix `Y^T Z` is independent of the chosen solution `Z`, is symmetric, and
is positive semidefinite.

### Proof — necessity of the range gate

Take `k in ker(W)` and arbitrary `x in R^N`. PSD of the block gives for every
real `s`

`0 <= [x;sk]^T M_tau [x;sk]`

`   = x^T A x + 2 s k^T Y x`.

The right side is affine in `s`. It can be nonnegative for all `s` only if

`k^T Y x=0`

for every `x`; hence `Y^T k=0`. Therefore

`ker(W) subset ker(Y^T)`.

Because `W` is symmetric finite dimensional,

`range(W)=ker(W)^perp`,

so every column of `Y` lies in `range(W)` and some `Z` satisfies `WZ=Y`.

### Proof — exact factorization

For any such `Z`,

`Y^T Z = Z^T W Z`.

Hence it is symmetric PSD. Moreover

`M_tau`

`= [[I, tau^{-1}Z^T],[0,I]]`

`  [[A-tau^{-1}Z^TWZ, 0],[0,tau W]]`

`  [[I,0],[tau^{-1}Z,I]]`.

This proves the iff statement.

If `Z1,Z2` both solve `WZ=Y`, then `W(Z1-Z2)=0`, and

`Y^T(Z1-Z2)=Z1^T W(Z1-Z2)=0`,

so the dual charge is solution-independent. QED.

## 5. Rationality corollary

If `W,Y` have rational entries and `WZ=Y` is consistent over `R`, it has a
rational solution by exact Gaussian elimination. Thus the range gate does not
force a pseudoinverse or an algebraic-number extension.

For a certificate, the producer may simply provide rational `Z` and the exact
identity `WZ=Y`.

---

# Part III — applying the range gate to the T-P5-250 reserve packet

## 6. Exact-image lift

As in T-P5-250, suppose an exact-image certificate has

`S = B + C^T Y + Y^T C >=0`.

The thick-tube S-lemma matrix is

`L_Y(tau)`

`= S + tau C^T W C - C^T Y - Y^T C - tau eta^2 E`.

The T-P5-250 metric-reserve packet used the block

`R_tau := [[S-tau eta^2 E, Y^T], [Y, tau W]]`.

For `W>0`, Schur completion paid the equality multiplier by
`Y^T W^{-1}Y/tau`.

## 7. Theorem 3 — semidefinite reserve completion

For `W>=0`, `tau>0`, the block packet `R_tau>=0` is equivalent to

1. `range(Y) subset range(W)`;
2. there exists `Z` with `WZ=Y`;
3. **`S - tau eta^2 E - tau^{-1} Y^T Z >=0`.**

Under these conditions,

`L_Y(tau)` admits the exact square decomposition

**`L_Y(tau)`**

`= S - tau eta^2 E - tau^{-1} Z^T W Z`

`  + tau (C-tau^{-1}Z)^T W (C-tau^{-1}Z)`.

Therefore `R_tau>=0` implies the exact one-tube S-lemma certificate and hence
thick-tube safety.

### Interpretation

The unpenalized normal directions cannot be charged through the singular metric.
The equality multiplier must annihilate them:

`k in ker(W)  =>  Y^T k=0`.

After that hard gate, the old `W/W^{-1}` dual charge is replaced by the intrinsic,
solution-independent quantity

`Y^T Z`, where `WZ=Y`.

This is the correct inverse-free analogue of `Y^T W^{-1}Y`.

---

# Part IV — fully fraction-free maximal-principal-anchor packet

## 8. Rational anchor data

For exact rational checking, even the solve `WZ=Y` can be eliminated from the
consumer interface.

After a simultaneous row/column permutation, split residual indices as `I union J`.
Let

`R := W_II`,

with `R>0`, `k=|I|`,

`delta := det(R) >0`,

`H := adj(R)`.

Assume the **rank-closure identity**

**`delta W_JJ = W_JI H W_IJ`.**

Since `R^{-1}=H/delta`, this is precisely zero Schur complement of `R`; hence it
implies

`W>=0`, `rank(W)=k`.

No eigenvector, square root, rank-revealing SVD or pseudoinverse is needed.

## 9. Theorem 4 — fraction-free range gate

Under the rank-closure identity,

`range(Y) subset range(W)`

if and only if

**`delta Y_J = W_JI H Y_I`.**

### Proof

The rank closure gives the row identity

`W_J* = W_JI R^{-1} W_I*`.

Hence every vector in `range(W)` obeys

`v_J=W_JI R^{-1}v_I`.

Conversely, if `Y_J=W_JI R^{-1}Y_I`, choose a solution supported only on `I`:

`Z_I=R^{-1}Y_I`, `Z_J=0`.

Then `WZ=Y`. Multiplication by `delta` gives the displayed division-free identity.
QED.

## 10. Theorem 5 — fraction-free generalized Schur gate

Let `A=A^T`. Under the same anchor/rank closure and `tau>0`,

`[[A,Y^T],[Y,tau W]] >=0`

if and only if both

**`delta Y_J = W_JI H Y_I`**

and

**`tau delta A - Y_I^T H Y_I >=0`.**

Indeed the support-on-`I` solution has

`Y^T Z = delta^{-1} Y_I^T H Y_I`,

and multiplication of the Schur inequality by the positive scalar `tau delta`
gives the second gate.

### T-P5-250 specialization

Taking

`A=S-tau eta^2 E`

gives the completely division-free sufficient packet

**range:**

`delta Y_J = W_JI H Y_I`,

**reserve:**

**`tau delta S - tau^2 delta eta^2 E - Y_I^T H Y_I >=0`.**

For rational `W,S,Y,eta,tau`, every field is rational.

This is the recommended exact adapter shape.

---

# Part V — common-metric reserve survives unchanged after the range gate

## 11. Intrinsic dual charge

Let `Z` solve `WZ=Y` and suppose a common PSD reference metric `R0` satisfies

`S >= rho R0`,

`E <= alpha R0`,

`Y^T Z <= beta R0`.

Then

`S-tau eta^2E-tau^{-1}Y^TZ`

`>= [rho - tau eta^2 alpha - beta/tau] R0`.

Thus the same scalar survival condition as in T-P5-250 applies:

`rho >= tau eta^2 alpha + beta/tau`.

Optimizing over positive `tau` yields

**`rho >= 2 eta sqrt(alpha beta)`.**

The only new ingredient is the hard range gate. Once it passes, singularity of
`W` creates no additional quantitative debit on the controlled quotient.

For exact rational strict margins one may choose a rational `tau` in the open
admissible interval, exactly as in the positive-definite branch.

---

# Part VI — coordinate covariance of the partial-normal packet

## 12. Residual-coordinate transport

Let `U in GL(r)` and define a new residual coordinate

`e' = U e`,

hence

`C' = U C`.

Transport the metric and equality multiplier by

`W' = U^{-T} W U^{-1}`,

`Y' = U^{-T}Y`.

Then

`e'^T W' e' = e^T W e`,

and

`C'^T Y' + Y'^T C' = C^T Y + Y^T C`.

If `WZ=Y`, let `Z'=UZ`. Then

`W'Z'=Y'`,

and

**`Y'^T Z' = Y^T Z`.**

Therefore the range gate, intrinsic dual charge, tube set, and reserve condition
are all invariant under arbitrary invertible residual-coordinate changes.

This proves that the range/quotient split is mathematical, not an artifact of a
chosen eigenbasis. A rational LDL/congruence chart may be used by an
implementation, but no canonical orthonormal basis is required by the theorem.

---

# Part VII — the zero-radius dispatcher needs correction in the singular case

## 13. Lemma — zero quadratic value of a PSD form

For `W>=0`,

**`e^T W e =0  iff  W e=0`.**

A square-root proof is possible but unnecessary. If `e^TWe=0`, positivity of

`(e+t v)^T W(e+t v)`

for every real `t` forces its linear coefficient `2 e^T Wv` to vanish for every
`v`, hence `We=0`.

## 14. Consequence at `eta=0`

For singular `W`,

`T_0(W)={y : e(y)^T W e(y)=0}`

is therefore

**`T_0(W)={y : W C ξ=0}`.**

This is generally **strictly larger** than the exact affine image `Cξ=0`.

Hence the T-P5-250 sentence

`eta=0 -> use T-P5-249 exact equality Cξ=0`

is valid only when `W>0` (or when a separate source theorem proves
`WCξ=0 -> Cξ=0` on the relevant affine slice).

The correct dispatcher is:

- `W>0, eta=0`: exact equality `Cξ=0`, use T-P5-249;
- `W>=0` singular, `eta=0`: exact **partial equality** `WCξ=0`; T-P5-249 may be applied to the equality matrix `WC`, preserving its rectangular/dependent-row semantics;
- `W>=0, eta>0` with strict Slater: use the semidefinite one-tube S-lemma of Theorem 1;
- metric-reserve reuse of a previously chosen exact-image multiplier additionally requires the range gate of Theorem 2/3.

This is a genuine interface correction, not a numerical issue.

---

# Part VIII — exact regressions and obstruction boundaries

## 15. Rational maximal-anchor example

Take

`W=[[1,1],[1,1]]`.

This is PSD of rank one. Choose `I={1}`. Then

`R=[1]`, `delta=1`, `H=[1]`,

and rank closure is exact because

`W_22 = W_21 H W_12 =1`.

### Good multiplier

Let

`Y=[1;1]`, `A=[2]`, `tau=1`.

The range gate is

`Y_2=W_21 H Y_1=1`.

The fraction-free Schur gate is

`tau delta A - Y_I^T H Y_I =2-1=1>0`.

Hence

`[[2,1,1],[1,1,1],[1,1,1]] >=0`.

### Bad multiplier

Let

`Y=[1;0]`.

The range residual is

`delta Y_2-W_21 H Y_1 = -1`.

So no finite normal-metric Schur charge exists. Indeed

`[[2,1,0],[1,1,1],[0,1,1]]`

has determinant `-1` and is indefinite.

This regression directly checks the necessity of the range gate.

## 16. Partial-tube physical obstruction

Use two state coordinates `(x,z)` and augmented `ξ=[x,z,1]`.
Let

`C=[[1,0,0],[0,1,0]]`,

`W=diag(1,0)`.

Then the tube is merely

`x^2<=eta^2`; `z` is completely unpenalized.

Choose the exact-image lift `S=0` and multiplier

`Y=[[0,0,0],[0,0,1]]`.

Then

`B=S-C^TY-Y^TC`

represents

`ξ^T B ξ = -2z`.

On the exact image `x=z=0` the slack is zero, but on every partial tube, even at
`eta=0`, choosing `z>0` gives a negative slack. The multiplier acts in
`ker(W)=span(e2)`, exactly the direction that the tube does not see.

## 17. Important fail-closed counterexample: range failure is not physical FAIL

Keep the same `C,W`, but choose the actual slack

`ξ^T B ξ = z^2+1`,

which is globally positive and hence certainly safe on the partial tube.

Take

`Y=[[0,0,0],[0,1,0]]`.

Then

`C^TY+Y^TC` contributes `2z^2`, so

`S=B+C^TY+Y^TC`

is also PSD. Yet `Y` has a nonzero component in `ker(W)`, so the range gate for
**reusing this particular equality-multiplier reserve packet** fails.

The original safety statement is still true; Theorem 1 can certify it already at
`tau=0` because `B>=0` globally.

Therefore the correct failure label for the reserve packet is

**`INCONCLUSIVE_FROM_SINGULAR_NORMAL_RESERVE_REUSE__TRY_DIRECT_TUBE_SLEMMA_OR_DIFFERENT_LIFT`.**

Do not upgrade range-gate failure to a mathematical/physical FAIL unless an actual
state witness gives positive Lyapunov debit.

---

# Part IX — minimal theorem statements for formalization

## 18. Candidate theorem A

`semidefiniteTube_slemma_iff`

Inputs:

- symmetric `B,W`, `W>=0`, `eta>0`;
- affine residual `C`;
- strict Slater.

Conclusion:

`B>=0` on `(Cξ)^TW(Cξ)<=eta^2`

iff

`exists tau>=0, B+tau C^TWC-tau eta^2 E >=0`.

## 19. Candidate theorem B

`semidefiniteMetric_blockPSD_iff`

For `W>=0`, `tau>0`,

`[[A,Y^T],[Y,tau W]]>=0`

iff

`(exists Z, WZ=Y) and A-tau^{-1}Y^TZ>=0`.

The theorem should also expose the equivalent nullspace statement

`forall k, Wk=0 -> Y^Tk=0`

and prove solution-independence of `Y^TZ`.

## 20. Candidate theorem C

`semidefiniteMetric_maximalAnchor_blockPSD_iff`

Given a principal anchor `R=W_II`, `delta=det R>0`, `H=adj R`,

`delta W_JJ=W_JI H W_IJ`,

then block PSD is equivalent to the two division-free gates

`delta Y_J=W_JI H Y_I`,

`tau delta A-Y_I^T H Y_I>=0`.

This is the preferred exact-rational checker theorem.

## 21. Candidate theorem D

`psd_zeroRadius_partialEquality`

For `W>=0`,

`(Cξ)^T W(Cξ)=0 <-> W Cξ=0`.

A downstream dispatcher corollary should explicitly require `W>0` before replacing
this with `Cξ=0`.

---

# Part X — suggested typed adapter packet

## 22. Minimal source-facing fields

A semidefinite partial-tube producer that wants to use the fraction-free reserve
branch should provide:

- `same_source_key / same_cell_key`;
- exact rational `C,W,Y,S,eta`;
- principal residual index set `I` and complement `J`;
- `R=W_II`, `delta=det R`, `H=adj R`;
- positive-definite anchor proof for `R`;
- rank closure `delta W_JJ=W_JI H W_IJ`;
- multiplier range closure `delta Y_J=W_JI H Y_I`;
- a rational `tau>0`;
- reserve PSD `tau delta S-tau^2 delta eta^2 E-Y_I^THY_I>=0`.

No field named `pinv`, `eigenvector`, `sqrtW`, or floating rank tolerance is
mathematically necessary.

If the producer cannot supply the range closure, it should fall back to the direct
one-tube S-lemma matrix `B+tau C^TWC-tau eta^2E`, not declare the target false.

---

# Part XI — exact boundaries and next seam

## 23. Boundaries

1. **The range gate belongs to reserve reuse, not to the exact tube S-lemma.**
   Direct tube safety may still hold when a chosen `Y` fails the range gate.

2. **No generic two-constraint losslessness.** If a source ellipsoid and a partial
   tube must cooperate, this child does not turn the generic two-quadratic
   S-procedure into an iff.

3. **No actual P5 normal metric identified.** Nothing here proves that a nonlinear
   chart defect, FD halo, mechanics graph residual or trajectory enclosure has the
   declared `C,W,eta` form.

4. **Zero radius is partial equality for singular `W`.** It must not be routed to
   exact `Cξ=0` without an injectivity/source implication.

5. **Coverage remains external.** A valid partial-tube inequality does not prove
   the physical trajectory or stencil remains inside that tube.

6. **No Float64 rank tests.** Near-singular numerical metrics require interval or
   exact reification before choosing the algebraic rank/anchor branch.

## 24. Next distinct seam

The clean source-facing continuation is now no longer another abstract Schur
variant. It is to bind an actual P5 residual metric and decide whether its
singularity is **structural**:

- identify the true normal residual map `C` and metric `W` from the same source/tube key;
- prove an exact rank/anchor packet for `W`;
- determine whether the equality multiplier lies in `range(W)`;
- if not, decide whether the direct one-tube S-lemma can use physical slack curvature to absorb the ignored normal directions;
- at `eta=0`, bind the real partial equality `WCξ=0` and prove or refute the stronger implication `WCξ=0 -> Cξ=0` on the actual source slice.

That is the point where this mathematical bridge should meet the real adapter.

---

## 25. Non-claims

This review does not establish:

- actual P5 source identity for `C,W,Y,S,eta`;
- trajectory/tube/FD-halo/flowpipe coverage;
- a lossless generic source-ellipsoid plus tube two-constraint theorem;
- Float64 or interval rank semantics;
- a Lean/kernel receipt;
- independent verification by 封不觉;
- admission or registry eligibility;
- P5/P8/M4 parent closure.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.