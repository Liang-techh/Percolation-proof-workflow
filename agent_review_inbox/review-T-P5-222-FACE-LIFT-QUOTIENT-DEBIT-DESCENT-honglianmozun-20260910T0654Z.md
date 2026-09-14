---
kind: review_result
review_id: review-T-P5-222-face-lift-quotient-debit-descent-honglianmozun-20260910T0654Z
task_id: T-P5-222-FACE-LIFT-QUOTIENT-DEBIT-DESCENT
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T06:54:00Z
claim_commit: c895f42dc6cea82bfeb734fe46ed9122a6d1404a
inspected_commit: f326741ad2a86a14d3fcce545a70c48bbfaa5349
upstream_commits:
  - 4daeafdb1733f8bba97cd4576b68989cdcf31890  # T-P5-215 compatibility / one-pair endpoint theorem
  - 8e18bf65daa1c307c154506d86e85bd5b5df6c7b  # T-P5-219 same-chart fraction-free debit pullback
  - d5426eb17fb3d2466af3e287237ce6f18d4f55f5  # T-P5-221 heterogeneous-chart bilinear transport
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_face_lift_quotient_radical_gate; add_restricted_packet_radical_gate; add_cross_chart_cross_face_debit_pullback; add_gauge_obstruction_formula; add_exact_regressions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional symmetric-bilinear algebra, quotient/radical argument, Lyapunov endpoint/debit transport, rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-222 — face-lift quotient descent for Lyapunov endpoint debit

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-221 closes the chart problem for a **fixed physical endpoint/debit form**: atoms emitted from unrelated PD-prefix charts can be paired without forcing them into one reduced coordinate system. It correctly leaves a different seam open: two physical zero atoms may be consumed through different face-dependent tangent/endpoint lifts. If one simply forms one local `Qeff=L_f^T Q L_f` on each face, then a cross-face pair has no canonical meaning until the lift ambiguity is shown to be invisible to the endpoint quadratic.

This child gives the exact mathematical gate.

Let `Y` be the ambient tangent space, let `N subset Y` be the face-lift gauge subspace, and let `Q=Q^T` be the symmetric second-order debit form. Then the bilinear form

`B_Q(v,w)=v^T Q w`

 descends to the quotient `Y/N` **iff**

**`N subset ker(Q)`.**

For a finite/relevant zero-atom packet one does not need the global condition on all of `Y`. If `W` spans the chosen lifted atom representatives and `G` spans the allowed lift-gauge directions, then all self/cross debit pairings are representative-independent on

`U=span(W,G)`

iff

**`G^T Q W=0` and `G^T Q G=0`.**

This is the exact restricted radical condition `span(G) subset rad(Q|_U)`. It can be strictly weaker than `QG=0` globally, because directions outside the emitted endpoint packet need not be controlled.

Combining this with T-P5-221, a chart `a` with reconstruction numerator `M_a` and positive denominator `d_a`, plus a face lift `L_f`, has tangent numerator

`J_{a,f}:=L_f M_a`.

For arbitrary charts/faces `(a,f)` and `(b,g)`, define

**`Qhat_{af,bg}:=J_{a,f}^T Q J_{b,g}`.**

Then

**`d_a d_b (L_f x_a(lambda))^T Q (L_g x_b(mu)) = lambda^T Qhat_{af,bg} mu`.**

When the lift-gauge radical gate holds, this scalar is independent of every admissible face-lift representative. Thus the T-P5-215 one-ray / compatible-pair endpoint decision becomes genuinely physical rather than face-choice dependent.

Conversely, a `K`-zero or reconstruction gauge is **not** automatically `Q`-invisible. If the radical gate fails, the exact formula

`q_Q(w+t g)-q_Q(w)=2t g^TQw+t^2 g^TQg`

exhibits the obstruction. An explicit rational PSD regression below shows the same physical zero atom having zero debit under one face lift and positive debit under another. Therefore no cross-face endpoint theorem may silently identify face lifts merely because their difference is zero-energy for the storage matrix.

No actual P5 same-key lift family, selector/cell/tube source, trajectory coverage, Float64/interval semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Abstract endpoint-lift setup

Let `Z` be a physical zero-coordinate space and `Y` an ambient tangent/endpoint space. A face label `f` carries a linear lift

`L_f : Z_f -> Y`,

where `Z_f` is the physical zero subspace/cone relevant on that face.

At a physical state/vector lying in an overlap of two face descriptions, the two lifts need not be literally equal. Assume their difference is a gauge vector in a fixed linear subspace

`N subset Y`:

**`L_f z - L_g z in N`.**

The endpoint second-order form is a symmetric matrix

`Q=Q^T`

on `Y`. Write

`B_Q(v,w):=v^TQw`,

`q_Q(v):=v^TQv`.

The question is not whether two lifts have the same storage energy. The question needed by T-P5-210/215 is whether `B_Q` and `q_Q` are well-defined on the physical tangent class modulo the lift gauge.

---

## 2. T222-A — global quotient/radical theorem

### Theorem A

The following are equivalent:

1. `B_Q` induces a well-defined symmetric bilinear form on the quotient `Y/N` by

   `bar B([v],[w]) := v^TQw`;

2. changing either representative by any gauge vector leaves every pairing unchanged;
3. **`N subset ker(Q)`**.

### Proof

Assume item 3. If `n,m in N`, then `Qn=Qm=0`. Hence

`(v+n)^TQ(w+m)`

`=v^TQw+n^TQw+v^TQm+n^TQm`

`=v^TQw`.

So the form descends.

Conversely, suppose the quotient pairing is well-defined. For every `n in N` and every `w in Y`, the classes `[n]=[0]` give

`n^TQw = bar B([0],[w]) = 0`.

Thus the row vector `n^TQ` is zero. Since `Q` is symmetric, `Qn=0`. Hence `N subset ker(Q)`.

QED.

### Corollary A1 — quadratic descent

Under the same condition,

`q_Q(v+n)=q_Q(v)`

for every `v in Y`, `n in N`. Therefore the endpoint debit is a genuine quadratic form on `Y/N`.

### Corollary A2 — face-lift invariance

If all admissible face-lift differences lie in `N` and `N subset ker(Q)`, then for any physical zero vectors `x,y` and any admissible faces `f,f',g,g'`,

**`(L_f x)^TQ(L_g y) = (L_{f'}x)^TQ(L_{g'}y)`.**

So both self debit and cross debit are independent of face choice.

---

## 3. T222-B — exact restricted packet criterion

The global gate `N subset ker(Q)` may be stronger than a finite endpoint consumer needs. T-P5-215 eventually sees only the span of the emitted lifted zero atoms and their admissible face-gauge differences.

Let the columns of

`W=[w_1 ... w_r]`

span chosen lifted representatives, and let the columns of

`G=[g_1 ... g_s]`

span the allowed gauge space `N_0` for this packet. Define

`U := span(W,G)`.

### Theorem B — restricted radical iff two Gram blocks vanish

The following are equivalent:

1. `N_0 subset rad(B_Q|_U)`, i.e. `n^TQu=0` for every `n in N_0`, `u in U`;
2. **`G^T Q W=0` and `G^T Q G=0`.**

### Proof

If item 1 holds, take `n` successively from the columns/span of `G` and `u` from the columns/spans of `W` and `G`; both matrix blocks vanish.

Conversely, any `n in N_0` and `u in U` can be written

`n=G a`,

`u=W b+G c`.

Then

`n^TQu`

`=a^T G^TQW b + a^T G^TQG c`

`=0`.

QED.

### Corollary B1 — packetwise representative independence

Assume each alternative face lift of packet representative `w_i` differs from `w_i` by a vector in `N_0`. Under the two exact zero-block tests above, every allowed replacement

`w_i -> w_i+n_i`

preserves every self/cross entry

`w_i^TQw_j`.

This is enough for the T-P5-215 self/pair endpoint scan even when `QG` is nonzero on ambient directions outside `U`.

### Why both blocks are needed

`G^TQW=0` alone kills the first-order representative error but not gauge-gauge cross terms. `G^TQG=0` alone kills pure-gauge debit but not the interaction with a physical lifted zero direction. Both are required for a bilinear table to descend on the relevant quotient.

---

## 4. T222-C — heterogeneous chart + heterogeneous face pullback

Use T-P5-221 notation. Chart `a` has positive denominator `d_a`, full reconstruction numerator map `M_a`, and reduced coordinate `lambda`:

`x_a(lambda)=M_a lambda/d_a`.

Chart `b` similarly has `(d_b,M_b,mu)`.

Let face `f` use tangent lift `L_f` and face `g` use `L_g`. Define tangent numerator maps

**`J_{a,f}:=L_f M_a`,**

**`J_{b,g}:=L_g M_b`.**

Define the cross-face/cross-chart debit numerator

**`Qhat_{af,bg}:=J_{a,f}^T Q J_{b,g}`.**

### Theorem C — fraction-free cross-face debit identity

For arbitrary reduced vectors `lambda,mu`,

**`d_a d_b (L_f x_a(lambda))^T Q (L_g x_b(mu))`**

**`=lambda^T Qhat_{af,bg} mu`.**

### Proof

`L_f x_a(lambda)=L_f M_a lambda/d_a=J_{a,f}lambda/d_a`,

and similarly for chart `b`. Substitute into the bilinear form and multiply by the positive denominator `d_a d_b`.

QED.

This extends T-P5-219/221 only at the endpoint-lift layer. No new copositivity premise is needed for the algebra.

### Corollary C1 — matrix-level invariance under a global radical gate

Suppose two face lifts satisfy

`(L_f-L_{f'}) range(M_a) subset N`

and `N subset ker(Q)`. Then

`M_a^T L_f^T Q L_g M_b`

is unchanged if `f` is replaced by `f'`; likewise on the `b` side. Hence `Qhat_{af,bg}` itself is canonical on the full chart reconstruction ranges.

### Corollary C2 — statewise invariance under the weaker packet gate

If only the emitted atom numerators are known to have lift differences in `N_0`, Theorem B still makes every contracted scalar

`lambda_i^T Qhat_{af,bg} lambda_j`

canonical, even though the ambient matrices `Qhat_{af,bg}` need not be literally equal away from the certified atom span.

This distinction matters: a producer must not upgrade packetwise invariance into an unrestricted matrix identity.

---

## 5. T222-D — exact obstruction when the radical gate fails

Let `w` be one endpoint representative and `g` an allowed gauge direction. For any scalar `t`,

### Theorem D1 — self-debit gauge polynomial

**`q_Q(w+t g)-q_Q(w)`**

**`=2t g^TQw+t^2 g^TQg`.**

This is immediate by expansion.

Consequences:

- if `g^TQw != 0`, then all sufficiently small nonzero `t` of one sign change the debit at first order;
- if `g^TQw=0` but `g^TQg != 0`, every nonzero `t` changes it at second order;
- therefore a continuous linear gauge is debit-invisible exactly when both coefficients vanish against every relevant representative/gauge direction.

### Theorem D2 — cross-debit obstruction

For another representative `z`,

**`B_Q(w+t g,z)-B_Q(w,z)=t g^TQz`.**

Thus a single nonzero exact scalar `g^TQz` is already a cross-face obstruction.

### Interpretation

A direction can be zero-energy for the storage/copositivity matrix `K` and still satisfy `Qg != 0`. There is no algebraic implication from `Kg=0` or `g^TKg=0` to `Qg=0`, because `Q` is an independent endpoint/debit form.

This is the second-order analogue of the derivative-gauge issue exposed earlier in T-P5-189: value gauge does not automatically imply derivative/debit gauge.

---

## 6. T222-E — handoff to the T-P5-215 one/pair theorem

Assume:

1. the physical zero-atom packet is complete for the endpoint family being tested;
2. T-P5-221 has provided sound cross-chart compatibility edges;
3. every physical endpoint atom may have several face-lift representatives whose differences lie in a packet gauge `N_0`;
4. the exact restricted radical gate

   `G^TQW=0`, `G^TQG=0`

   has passed;
5. the inherited T-P5-210/215 clique-wise debit copositivity hypothesis holds.

Then the full debit Gram table on each zero compatibility clique is independent of all face-lift choices. Consequently the T-P5-215 sparse alternative is physical and face-independent:

- one atom with positive self debit; or
- two compatible atoms with zero self debits and positive cross debit.

No face-selection consistency or differentiability is needed once the quotient gate has passed.

Conversely, if the radical gate fails, a positive self/pair debit found in one face representation may be a pure lift artifact. The endpoint decision must then either:

- bind one unique physical lift/gauge convention from source semantics, or
- prove a different one-sided robust bound;

it may not silently mix local `Qeff` packets.

---

## 7. Exact rational regressions

### Regression A — safe gauge: quotient descent really works

Take physical coordinate `x in R` and ambient tangent space `Y=R^2`. Use two face lifts

`L_0 x=(x,0)`,

`L_1 x=(x,x)`.

Their difference is

`g(x)=(0,x)`

in `N=span(e_2)`.

Choose

`Q_safe=diag(1,0)`.

Then `N subset ker(Q_safe)`. Hence

`q_Q(L_0 x)=x^2`,

`q_Q(L_1 x)=x^2`,

and for arbitrary `x,y`,

`(L_i x)^TQ_safe(L_j y)=xy`

for every `i,j in {0,1}`.

The face lift is genuinely nonunique, but the debit descends exactly to the physical quotient.

### Regression B — zero/storage gauge is not debit gauge

Keep the same two lifts, but choose the PSD debit

`Q_fail=diag(0,1)`.

For the same physical vector `x=1`,

`q_Q(L_0 1)=0`,

while

`q_Q(L_1 1)=1`.

The gauge direction `e_2` satisfies

`e_2^T Q_fail e_2=1>0`,

so the restricted/global radical gate fails.

Therefore the exact same physical zero atom can appear to have **no** positive second-order debit under one face lift and a **strictly positive** self-debit under another. This directly changes which branch of the T-P5-215 endpoint theorem fires.

The example remains rational and uses a PSD `Q`; the obstruction is not an artifact of indefiniteness or floating arithmetic.

### Regression C — why the mixed block matters

Take

`Q_mix=[[0,1],[1,0]]`,

`w=e_1`, `g=e_2`.

Then `g^TQ_mix g=0`, but

`g^TQ_mix w=1`.

So checking only pure-gauge energy `G^TQG=0` would incorrectly declare the gauge harmless. In fact

`q(w+t g)=2t`.

This is the exact reason Theorem B needs both `G^TQG=0` and `G^TQW=0`.

---

## 8. Rational trusted-checker packet

For rational `Q`, chart maps, lift maps, atom numerators, and gauge bases, every new gate is exact rational linear algebra.

A source-independent packet may contain:

1. representative numerator matrix `W` for the endpoint atoms actually consumed;
2. gauge basis `G` generated by proved face-lift differences;
3. exact zero checks

   **`G^TQW=0`,**

   **`G^TQG=0`;**

4. for chart/face pair `(a,f),(b,g)`, cached numerator

   **`Qhat_{af,bg}=(L_fM_a)^TQ(L_gM_b)`;**

5. positive chart denominators `d_a,d_b` when quantitative, rather than sign-only, pair values are exported.

No eigenvector, square root, pseudoinverse, numerical nullspace tolerance, or floating gauge normalization is needed.

If lift maps themselves are represented fraction-free with positive denominators `s_f`, the same construction simply acquires the positive factor `s_f s_g` in the common denominator; zero/sign semantics remain unchanged.

---

## 9. Candidate theorem statements

Recommended mathematical leaves:

- `symmetricBilinear_descends_quotient_iff_gauge_le_kernel`
  - a symmetric matrix `Q` defines a bilinear form on `Y/N` iff `N <= ker Q`.
- `restrictedGauge_radical_iff_gramBlocks_zero`
  - for `U=span(W,G)`, `span(G) <= rad(Q|_U)` iff `G^TQW=0` and `G^TQG=0`.
- `faceLift_debit_invariant_of_restrictedRadical`
  - all allowed representative replacements preserve self/cross debit.
- `pdChart_faceLift_crossDebit_fractionFree`
  - `d_a d_b <L_f x_a,Q L_g x_b>=<lambda,Qhat_afbg mu>`.
- `faceLift_selfDebit_gaugePolynomial`
  - `q(w+tg)-q(w)=2t<g,Qw>+t^2<g,Qg>`.
- `faceLift_crossDebit_gaugeDifference`
  - cross pairing changes by `t<g,Qz>`.
- `endpointOnePair_faceIndependent_of_gaugeRadical`
  - the T-P5-215 self/pair classification is independent of face lift once the radical packet passes.

These are finite-dimensional linear-algebra leaves and should be considerably smaller to formalize than the surrounding atom-search machinery.

---

## 10. Failure / non-FAIL boundaries

1. **Lift difference is not proved to be gauge.** Similar-looking face formulas are not enough; the quotient theorem needs an exact relation between their physical tangent representatives.
2. **Global radical fails but packet radical passes.** This is not a failure. The finite endpoint consumer may use the weaker Theorem B, but must not claim an ambient quotient theorem.
3. **Packet radical fails.** Cross-face debit is representation-dependent. Bind one unique source lift or develop a separate robust bound; do not mix face-local `Qeff` matrices.
4. **Only storage gauge is known.** `Kg=0` does not imply `Qg=0`; Regression B is the exact counterexample pattern.
5. **Only `G^TQG=0` is checked.** Insufficient; the mixed block `G^TQW` can still change debit at first order.
6. **Only self debits are compared.** Insufficient for T-P5-215; cross-pair entries can remain face-dependent even when selected self entries coincide.
7. **Statewise packet invariance is promoted to matrix identity.** Unsound unless lift differences on the whole chart reconstruction range lie in a global/relevant radical.
8. **Different physical debit forms are used on two faces.** The present theorem handles different lifts of one symmetric physical form `Q`, not an unexplained change of `Q` itself.
9. **Incomplete zero-atom packet or unproved clique debit copositivity.** The quotient gate only makes the debit table well-defined; it does not by itself prove endpoint completeness.
10. **Floating near-zero gauge tests.** The gate is exact. Float64 tolerances require independent interval/rational reification before trusted use.

---

## 11. Boundaries left open

- actual same-key P5 family of face-dependent endpoint lifts and their exact overlap/gauge identities;
- whether the deployed producer has a single canonical physical lift, making this quotient layer unnecessary in practice;
- extraction of a minimal rational gauge basis `G` from actual face transition identities;
- selector/cell/tube and trajectory coverage;
- final clique-wise debit copositivity / decay-margin consumption;
- Float64/interval reification;
- Lean/kernel compilation and axiom audit;
- 封不觉 independent validation;
- admission, registry mutation, and P5/P8/M4 parent propagation.

The source-independent mathematical seam is now explicit: **cross-chart transport alone is not enough when endpoint lifts vary by face. The exact additional gate is that the lift gauge lie in the radical of the debit form on the relevant endpoint span. When it does, the whole one-ray/pair Lyapunov endpoint table descends to the physical quotient; when it does not, the obstruction is an exact linear/quadratic gauge polynomial rather than a provenance issue.**