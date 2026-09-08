---
kind: review_result
review_id: review-T-P5-060-honglianmozun-20260908T0158
task_id: T-P5-060
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-08T01:51:00-06:00
created_at: 2026-09-08T01:58:00-06:00
claim_commit: fdbd09c9ee0e52eff1ce04b9bdebf0bc7c86e3ac
inspected_commit: 010f223b3a29f4f834dd97fa281f05ff301fefe2
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-056-honglianmozun-20260908T0100.md
  - agent_review_inbox/review-T-P5-057-radical-factor-cancel-liuguanyi-20260908T0122.md
  - agent_review_inbox/review-T-P5-058-guyuefangyuan-20260908T0120.md
  - agent_review_inbox/review-T-P5-059-quadratic-form-parity-kuangmanmozun-20260908T0148.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add an affine-quadratic / bilinear contact-parity gate for Lyapunov power and multiplier consumers; keep source binding, Float64 semantics, coverage, ODE continuation, Lean compilation, provenance and admission separate
---

# T-P5-060 — affine-energy parity contact gate

## 0. Bottleneck and non-overlap

`T-P5-057` classifies the signed primitive

`u_i = G_i / sqrt(A_i)`

at an exact removable radical contact. `T-P5-058` shows that a diagonal square `u_i^2` can remain regular even when a balanced odd signed primitive jumps. `T-P5-059` then gives the exact parity gate for a **pure quadratic form** `u^T K u`.

The remaining energy-method gap is that a Lyapunov derivative is usually not a pure quadratic form. Residual power, multiplier terms, and affine completion produce expressions of the form

`Phi(u) = c + a^T u + u^T K u`

or, more generally,

`B(x,u) = x^T C u`.

A square-only certificate does not control the signed linear term, and the quadratic parity gate alone does not say when a regular multiplier can couple to a balanced odd radical channel. This child gives the exact necessary-and-sufficient structural gate, the contact jump formula, and the strict-dissipation boundary needed by first-exit/Lyapunov arguments.

This is source-independent mathematics. It does not overlap the currently claimed Lean work for `T-P5-058` or `T-P5-059` and makes no deployed-source, Float64, coverage, ODE, provenance, comparator, registry, or admission claim.

---

## 1. Radical contact packet

Assume one common real factor `h` and, for each channel `i`,

`A_i = h^(2 m_i) S_i`,

`G_i = h^(q_i) J_i`,

with integers `m_i >= 1`, `q_i >= m_i`, and `S_i > 0`.

Set

`k_i := q_i - m_i >= 0`,

`v_i := J_i / sqrt(S_i)`.

For `h != 0`, the exact factor law from the preceding radical children is

**(1.1)**

`u_i = G_i/sqrt(A_i) = sign(h)^(q_i) |h|^(k_i) v_i`.

Call `i` **balanced** when `k_i=0`, hence `q_i=m_i`. Split the balanced indices into

`E = {i : k_i=0 and m_i even}`,

`O = {i : k_i=0 and m_i odd}`.

Assume the reduced vector `v_B=(v_E,v_O)` has one common finite contact limit from both sides. Every over-cancelled component `k_i>0` tends to zero. Therefore at a sign-changing contact of `h`, the two balanced one-sided limits are

**(1.2)**

`u_B^+ = (v_E, v_O)`,

`u_B^- = (v_E,-v_O)`.

Equivalently, with the parity involution

`P = diag(+1 on E, -1 on O)`,

we have `u_B^- = P v_B`.

This is the only contact information used below.

---

## 2. Affine-quadratic contact theorem

Let `K` be symmetric and consider the balanced-sector affine energy correction

`F(u_B) = c + a_B^T u_B + u_B^T K_BB u_B`.

All terms involving at least one over-cancelled channel vanish at the contact, so they do not affect the contact jump. The two balanced contact values are

**(2.1)**

`F_+ = c + a_B^T v_B + v_B^T K_BB v_B`,

`F_- = c + a_B^T P v_B + v_B^T P K_BB P v_B`.

Hence the exact jump is

**(2.2)**

`F_+ - F_-`

`= a_B^T (I-P) v_B + v_B^T (K_BB-P K_BB P) v_B`.

Writing

`a_B=(a_E,a_O)`

and

`K_BB = [[K_EE,K_EO],[K_EO^T,K_OO]]`,

this simplifies to the explicit formula

**(2.3)**

`F_+ - F_- = 2 a_O^T v_O + 4 v_E^T K_EO v_O`.

### Theorem 2.1 — universal affine-energy contact gate

The affine-quadratic correction has the same two-sided contact value for **every** reduced contact vector `(v_E,v_O)` if and only if

**(2.4)** `a_O = 0`

and

**(2.5)** `K_EO = 0`.

Equivalently,

**(2.6)** `P a_B = a_B`

and

**(2.7)** `P K_BB P = K_BB`.

### Proof

Sufficiency follows immediately from (2.2).

For necessity, assume the jump vanishes for every contact vector. First set `v_E=0`. Then (2.3) gives

`2 a_O^T v_O = 0`

for every `v_O`, so `a_O=0`. With that term removed, (2.3) becomes

`4 v_E^T K_EO v_O = 0`

for every pair `(v_E,v_O)`, hence `K_EO=0`.

Thus the conditions are necessary and sufficient, with no PSD, eigenvalue, inverse, or square-root argument.

---

## 3. Why this is genuinely stronger than T-P5-059

The pure quadratic theorem does not see `a^T u`. A balanced odd channel can therefore pass every square-only and parity-block quadratic check while still breaking the Lyapunov power through a linear residual coupling.

Exact one-channel witness:

`h(t)=t`, `A=t^2`, `G=t`, so `u(t)=sign(t)` for `t!=0`.

Choose

`K=0`, `a=1`, `c=0`.

Then

`F(t)=u(t)=sign(t)`,

so

`lim_(t->0+) F=1`,

`lim_(t->0-) F=-1`.

But `u^2=1` is perfectly regular. Thus a diagonal square certificate cannot be substituted for the affine-energy gate.

The obstruction is exactly `a_O != 0`.

---

## 4. Contact-specific cancellation versus reusable structural cancellation

For one particular contact vector, continuity needs only

**(4.1)**

`2 a_O^T v_O + 4 v_E^T K_EO v_O = 0`.

This can hold by accidental cancellation even when `a_O` or `K_EO` is nonzero. Such a pointwise identity is mathematically valid if a source theorem proves it on the entire contact set.

However, it is not a stable source-independent envelope certificate. If the checker must cover arbitrary reduced contact data in a box or cone, the correct fail-closed gate is the universal pair

`a_O=0`, `K_EO=0`.

This separation matters: a sampled contact where the two terms happen to cancel cannot justify a neighborhood-wide Lyapunov closure.

---

## 5. General bilinear multiplier theorem

The same mechanism applies before one specializes to a quadratic form.

Let two channel families `x` and `u` have removable common-factor packets with balanced parity involutions `P_X` and `P_U`. Assume all over-cancelled components vanish at the contact and the reduced balanced vectors `x_B,u_B` have common finite two-sided limits.

For a fixed bilinear multiplier

`B(x,u) = x_B^T C_BB u_B`,

the two one-sided contact values are

**(5.1)**

`B_+ = x_B^T C_BB u_B`,

`B_- = x_B^T P_X C_BB P_U u_B`.

Therefore:

### Theorem 5.1 — universal bilinear parity gate

`B_+=B_-` for every pair of reduced contact vectors if and only if

**(5.2)**

`P_X C_BB P_U = C_BB`.

Entrywise, a coefficient `C_ij` must vanish whenever the balanced parity of `x_i` and `u_j` differs.

If `E_X/O_X` and `E_U/O_U` denote the even/odd balanced splits, then

**(5.3)**

`B_+ - B_-`

`= 2 x_E^T C_EO u_O + 2 x_O^T C_OE u_E`.

The same-parity blocks `C_EE` and `C_OO` cancel automatically.

### Important special cases

1. A regular non-radical multiplier is parity-even. Therefore a linear pairing with a balanced odd radical channel must have zero structural coefficient unless a source-specific cancellation is proved. This is exactly the affine condition `a_O=0`.

2. Two balanced odd signed primitives may each jump, yet their bilinear product is contact-safe because odd × odd has even parity.

3. An even balanced primitive times an odd balanced primitive is the dangerous mixed block.

For a symmetric quadratic form `x=u` and `C=K`, (5.3) reduces to the T-P5-059 jump `4 v_E^T K_EO v_O`.

---

## 6. Exact two-channel sanity witnesses

### 6.1 Safe odd-odd multiplier despite signed jumps

Take

`u_1(t)=sign(t)`, `u_2(t)=sign(t)`.

Both signed channels jump, but

`u_1 u_2 = 1`

on both sides. This is the same-parity `O x O` safe block.

### 6.2 Unsafe even-odd multiplier

Take

`u_E(t)=1`, `u_O(t)=sign(t)`.

Then

`u_E u_O = sign(t)`

jumps. This is exactly a forbidden `E x O` block.

### 6.3 Positive-definite quadratic plus linear obstruction

Take the positive-definite matrix

`K=[[1,0],[0,1]]`

with `u_E=1`, `u_O=sign(t)`, and choose `a=(0,1)`.

The quadratic part is constant:

`u^T K u=2`.

But the affine energy is

`F=2+sign(t)`,

so it still jumps from `1` to `3`. Positive definiteness of `K` does not repair a forbidden odd linear power channel.

---

## 7. Consequence for Lyapunov / first-exit arguments

Suppose a Lyapunov derivative on a punctured cell has the decomposition

`Vdot = D_reg + F(u)`,

where `D_reg` has a common finite contact limit and `F` is the affine-quadratic radical correction above.

If the parity gate

`a_O=0`, `K_EO=0`

holds, then `F` has a well-defined two-sided contact extension, hence so does `Vdot`.

This allows a uniform strict dissipation estimate to pass through the removable contact:

if there is an exact `delta>0` such that on both punctured sides

**(7.1)** `Vdot <= -delta`,

then continuity gives at the contact

**(7.2)** `Vdot_contact <= -delta`.

This is the energy-method payoff: a removable radical zero need not force a cell split if the full Lyapunov power respects the parity symmetry.

### Failure boundary: pointwise strict negativity is not enough

A strict statement without a uniform gap cannot be promoted through the contact. Exact scalar witness:

`phi(t)=-t^2`.

For every `t!=0`, `phi(t)<0`, but `phi(0)=0`.

Therefore a first-exit argument that needs strict inwardness must carry a **uniform positive dissipation margin** across the punctured neighborhood; continuity alone only transports a non-strict limit.

This is independent of the radical issue and must remain explicit in downstream theorem statements.

---

## 8. Structural fingerprint for source CSE / energy consumers

For a radical contact candidate, the energy-side checker should distinguish the following layers:

1. factor layer: obtain exact `A_i=h^(2m_i)S_i`, `G_i=h^(q_i)J_i`, with `q_i>=m_i` and `S_i>0`;
2. vanishing-order layer: mark `k_i=q_i-m_i`; over-cancelled channels vanish at contact;
3. parity layer: among balanced channels, record `m_i mod 2`;
4. consumer layer:
   - diagonal squares need no parity gate;
   - pure quadratic forms require `K_EO=0`;
   - affine-quadratic Lyapunov power additionally requires `a_O=0`;
   - general bilinear multipliers require `P_X C P_U=C`;
5. strictness layer: if the contact is used in a first-exit/barrier proof, carry an explicit uniform dissipation margin `delta>0`.

This avoids two opposite errors:

- false rejection: demanding every signed primitive be continuous even when the energy consumer is parity-invariant;
- false acceptance: using square-only regularity to justify a signed linear or even-odd multiplier term.

---

## 9. Lean-friendly candidate statements

No Lean lane is claimed here. If the coordinator later dispatches formalization, the smallest algebraic children are:

1. `affine_parity_jump_two_channel`

   `Fplus-Fminus = 2*aO*z + 4*kEO*y*z`.

2. `affine_parity_universal_iff_two_channel`

   universal zero jump for all `y,z` iff `aO=0` and `kEO=0`.

3. `bilinear_parity_jump_four_block`

   `Bplus-Bminus = 2*xE*CEO*uO + 2*xO*COE*uE` in the scalar block case.

4. `uniform_strict_limit_consumer`

   continuity plus `delta>0` and punctured `f<=-delta` imply contact `f<=-delta`.

The first three are `ring`-level identities; the fourth is an order/limit consumer and should remain separate from source/ODE semantics.

---

## 10. Exact obstruction / scope boundary

This theorem assumes one common factor `h` for the contact packet. If different channels vanish on different independent factors or several zero surfaces intersect, a single parity involution is insufficient; the correct object is a contact-stratum/sign-action classification. That is a distinct child and is not silently covered here.

Likewise, the theorem does not prove that deployed residual/source coefficients actually have the required factorization, that a source cell crosses the zero, that reduced contact data have common limits, or that the real trajectory reaches/stays in the cell.

---

## 11. Evidence and admission boundary

Evidence in this review is exact algebra:

- contact involution `u^- = P u^+` on balanced channels;
- exact affine jump formula (2.3);
- exact bilinear jump formula (5.3);
- explicit rational/scalar counterexamples in Sections 3, 6, and 7.

No numerical sampling, eigenvalue computation, solver status, Float64 claim, or source-range monotonicity is used.

Admission remains **pending**. In particular, this result does not establish deployed `forceError`/FD/controller factorization, source CSE identity, trajectory coverage, ODE continuation, Lean compilation, comparator acceptance, provenance admission, or registry promotion.
