---
kind: review_result
review_id: review-T-P5-059-quadratic-form-parity-kuangmanmozun-20260908T0148
task_id: T-P5-059-QUADRATIC-FORM-PARITY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T01:34:00-06:00
created_at: 2026-09-08T01:48:00-06:00
claim_commit: 5f2521916f14c407e251defdc2c2eab7186ef556
parent_tasks:
  - T-P5-057-RADICAL-FACTOR-CANCEL
  - T-P5-058-QUADRATIC-RADICAL-CANCEL
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add an exact parity-block consumer for mixed quadratic forms at removable radical zero contacts; diagonal square-only consumers are automatically safe, but balanced even/odd cross couplings require an explicit structural gate
---

# T-P5-059 — exact parity cancellation for mixed quadratic-form consumers

## 0. Bottleneck and non-overlap

T-P5-057 gives the sharp signed primitive classification for

`u_i = G_i / sqrt(A_i)`

when

`A_i = h^(2m_i) S_i`, `G_i = h^(q_i) J_i`, `S_i>0`.

T-P5-058 then observes that `u_i^2` loses the balanced odd sign obstruction. That is exact for diagonal square-only energy terms, but it does **not** answer what happens to a mixed quadratic form

`Q(u) = u^T K u`.

A P5 energy or completion consumer can contain cross terms. Two individually harmless squares do not imply that their cross term is harmless at a sign-changing zero of the common factor `h`.

This review gives the exact structural gate. It is source-independent mathematics only. It does not alter signed/centered consumers, source binding, Float64/controller behavior, factor discovery, coverage, Lean compilation, verification, provenance, or admission.

---

## 1. Pairwise factor law

For each component assume

`A_i = h^(2m_i) S_i`,

`G_i = h^(q_i) J_i`,

with integers `m_i>=1`, `q_i>=m_i`, and `S_i>0`.

Put

`k_i := q_i-m_i >= 0`,

`v_i := J_i/sqrt(S_i)`.

At every point where `h!=0`, T-P5-057 gives

`u_i = sign(h)^(q_i) |h|^(k_i) v_i`.

Therefore every quadratic pair obeys the exact identity

**(1.1)**

`u_i u_j = sign(h)^(q_i+q_j) |h|^(k_i+k_j) v_i v_j`.

This immediately separates two regimes.

### 1.1 At least one over-cancelled factor

If `k_i+k_j>0`, then the scalar factor

`sign(h)^(q_i+q_j) |h|^(k_i+k_j)`

has a continuous extension equal to zero at `h=0`.

Hence **no parity obstruction survives in such a pair**. A balanced-odd component may be discontinuous by itself, but its product with an over-cancelled component still tends to zero.

### 1.2 Balanced-balanced pair

If `k_i=k_j=0`, both components are balanced and

**(1.2)**

`u_i u_j = sign(h)^(m_i+m_j) v_i v_j`.

Thus:

- if `m_i+m_j` is even, the sign cancels exactly;
- if `m_i+m_j` is odd, the pair changes sign when `h` changes sign, unless its coefficient/product vanishes or aggregate cancellation is separately proved.

This is the exact mixed-term analogue of the T-P5-057 / T-P5-058 distinction.

---

## 2. Exact quadratic-form parity theorem

Let `B` be the set of balanced indices, i.e. `q_i=m_i`. Split it into

`B_even := {i in B : m_i even}`,

`B_odd  := {i in B : m_i odd}`.

Let `K` be a fixed real symmetric matrix. Let `K_BB` denote its balanced-balanced block.

Define the parity matrix on the balanced sector

`P := diag((-1)^(m_i))_(i in B)`.

At a sign-changing zero of `h`, suppose the reduced vector `v_B` has the same finite limit from both sides. Then the two one-sided quadratic-form limits contributed by the balanced sector are

**(2.1)**

`Q_+ = v_B^T K_BB v_B`,

`Q_- = v_B^T P K_BB P v_B`.

All terms containing at least one over-cancelled index vanish at the contact by Section 1.1.

Therefore the quadratic form has a **universal removable extension for arbitrary reduced contact data `v_B`** iff

**(2.2)** `P K_BB P = K_BB`.

Entrywise, (2.2) is exactly

**(2.3)**

`K_ij = 0` whenever `i in B_even` and `j in B_odd`.

Equivalently, the balanced quadratic form must be block diagonal with respect to the even/odd vanishing-order split.

This condition is necessary and sufficient for a structural checker that cannot rely on accidental cancellation in the particular contact vector.

### Proof

For a balanced entry `(i,j)`, conjugation by `P` multiplies `K_ij` by

`(-1)^(m_i+m_j)`.

Hence `P K_BB P=K_BB` automatically on same-parity pairs and forces `K_ij=0` on opposite-parity pairs. Conversely, if every opposite-parity entry vanishes, all remaining entries are unchanged by parity conjugation. This proves (2.2) iff (2.3).

With (2.2), the two limits in (2.1) coincide for every `v_B`; without it, choose contact data supported on one nonzero opposite-parity matrix entry to obtain a jump.

---

## 3. Exact jump formula and weaker trajectory-specific condition

Writing the balanced contact vector as

`v_B = (v_E,v_O)`

and the symmetric balanced matrix as

`K_BB = [[K_EE, K_EO], [K_EO^T, K_OO]]`,

we have

**(3.1)**

`Q_+ - Q_- = 4 v_E^T K_EO v_O`.

Thus for one **particular** contact vector, continuity only requires

**(3.2)** `v_E^T K_EO v_O = 0`.

But (3.2) is not a stable source-independent structural certificate: it can hold accidentally at one point and fail under an arbitrarily small perturbation of the reduced contact data.

For a reusable P5 theorem over a whole envelope, the correct fail-closed structural gate is therefore `K_EO=0`, unless a separate exact source theorem proves the scalar cancellation (3.2) throughout the relevant contact set.

---

## 4. Sharp two-channel counterexample: squares pass, mixed energy jumps

Take a common factor

`h(t)=t`.

Channel 1:

`A_1=t^2`, `G_1=t`, so `m_1=q_1=1` and

`u_1=sign(t)` for `t!=0`.

Channel 2:

`A_2=t^4`, `G_2=t^2`, so `m_2=q_2=2` and

`u_2=1` for `t!=0`.

Both square-only quantities are perfectly regular:

`u_1^2=u_2^2=1`.

Now choose the positive-definite rational matrix

`K = [[1,1/2],[1/2,1]]`.

Its eigenvalues are `1/2` and `3/2`, so this is not an indefinite-cancellation pathology.

The quadratic form is

`Q = u_1^2 + u_1 u_2 + u_2^2`

and therefore

`Q(t)=2+sign(t)`.

Hence

`lim_(t->0+) Q(t)=3`,

`lim_(t->0-) Q(t)=1`.

So **both diagonal square certificates PASS, while the mixed positive-definite quadratic energy has a genuine jump**.

The obstruction is exactly the forbidden even/odd coupling `K_12=1/2`.

This proves that T-P5-058 cannot be lifted from diagonal squares to a generic quadratic form without the parity-block gate.

---

## 5. Opposite phenomenon: signed primitives can jump while the full quadratic form is regular

The parity gate is also strictly less conservative than demanding every primitive be continuous.

Take two balanced odd channels:

`m_1=q_1=1`, `m_2=q_2=1`,

with `v_1,v_2` continuous. Then both signed primitives acquire the same factor `sign(h)`:

`u = sign(h) v`.

For **every** symmetric matrix `K`,

`u^T K u = sign(h)^2 v^T K v = v^T K v`.

Thus an entire all-odd balanced block may have arbitrary internal cross couplings and still be exactly regular at the quadratic-form level, even though every nonzero signed component jumps.

Likewise an all-even balanced block is trivially regular. Only couplings **between** the even and odd balanced sectors are structurally dangerous.

This is why the correct checker is a parity block condition, not the stronger and unnecessary demand that every normalized primitive individually have a continuous extension.

---

## 6. Quantitative Lipschitz transport after the parity gate

The same pair law gives a source-friendly variation estimate.

Assume on one cell

`|h|<=H`,

`|h-h0|<=Lh |eta-eta0|`,

and for each reduced primitive

`|v_i|<=M_i`,

`|v_i-v_i0|<=L_i |eta-eta0|`.

For a pair `(i,j)`, put

`r_ij := k_i+k_j`.

### 6.1 Positive total excess order `r_ij>=1`

The scalar factor

`chi_ij(h):=sign(h)^(q_i+q_j)|h|^(r_ij)`

has

`|chi_ij|<=H^(r_ij)`

and the exact elementary Lipschitz bound

`|chi_ij(h)-chi_ij(h0)| <= r_ij H^(r_ij-1) |h-h0|`.

Therefore

**(6.1)**

`Lip(u_i u_j)` is bounded by

`r_ij H^(r_ij-1) Lh M_i M_j`

`+ H^(r_ij)(L_i M_j + M_i L_j)`.

No sign split is needed.

### 6.2 Balanced-balanced same-parity pair

Here `r_ij=0` and `q_i+q_j` is even, so the sign factor is identically one. Thus

**(6.2)**

`Lip(u_i u_j) <= L_i M_j + M_i L_j`.

### 6.3 Quadratic form

If the parity gate `K_EO=0` holds on the balanced block, summing the absolute coefficient-weighted pair bounds from (6.1)-(6.2) yields a finite exact Lipschitz constant for `Q` across a sign-changing zero of `h`.

If `H,Lh,M_i,L_i,K_ij` are rational certificate constants, the resulting bound is rational and uses only integer powers; the common zero itself introduces no inverse power or square-root singularity.

The residual `v_i=J_i/sqrt(S_i)` bounds can be supplied by the already-separated reduced-radicand lane of T-P5-057.

---

## 7. Failure branches that must remain explicit

### 7.1 Under-cancelled component

This theorem assumes `q_i>=m_i`. If `q_i<m_i`, generic blow-up remains possible. Quadratic-form cancellation can occur for specially degenerate `K`, but a structural checker must not infer it from parity alone.

Example: `u_1=1/|t|` and `K_11=1` gives `Q=1/t^2`.

### 7.2 Accidental contact-vector cancellation is weaker than block cancellation

For an opposite-parity cross block, one can have `v_E^T K_EO v_O=0` at a single contact despite `K_EO!=0`. This proves continuity only for that exact contact data. It gives no robust neighborhood certificate unless the scalar cancellation itself is propagated by a separate theorem.

### 7.3 Square-only PASS is insufficient

Section 4 gives a positive-definite counterexample. Therefore a checker must never replace a mixed quadratic form by separately certified diagonal squares unless it also controls the cross terms.

### 7.4 Signed/centered consumer still belongs to T-P5-057

Quadratic parity cancellation does not manufacture a continuous signed primitive. If downstream needs `u_i-u_i0`, component signs, a centered residual, or a linear functional of `u`, this review is inapplicable.

---

## 8. Lean-friendly theorem surface

A minimal sidecar does not need matrix APIs initially. The following scalar/two-channel lemmas are enough to lock the mathematics:

1. `balanced_pair_even_parity_cancel`
   - encode `sigma^2=1` and prove same-parity product invariance.

2. `opposite_parity_quadratic_jump`
   - for
     `Qplus = a*x^2 + 2*c*x*y + b*y^2`,
     `Qminus = a*x^2 - 2*c*x*y + b*y^2`,
     prove
     `Qplus-Qminus = 4*c*x*y` by `ring`.

3. `opposite_parity_cross_zero_invariant`
   - `c=0 -> Qplus=Qminus`.

4. `quadratic_form_parity_counterexample`
   - instantiate `a=b=1`, `c=1/2`, `x=y=1` and prove the two limits are `3` and `1`.

5. `all_odd_quadratic_invariant`
   - prove `Q(-x,-y)=Q(x,y)` for arbitrary `a,b,c`.

6. optional finite-index theorem:
   - if `K_ij=0` whenever balanced parities differ, then conjugation by the diagonal parity sign leaves the balanced quadratic form invariant.

The quantitative pair Lipschitz estimate can be a later consumer; it is not required to establish the structural obstruction.

---

## 9. Integration recommendation

The zero-contact decision tree should distinguish consumer type:

- signed/linear/centered primitive -> T-P5-057;
- diagonal square-only primitive -> T-P5-058;
- mixed symmetric quadratic form -> T-P5-059 parity-block gate;
- any under-cancelled factor -> fail closed unless a stronger exact factor or nullspace theorem is supplied.

For a mixed quadratic form, after exact factor packets expose `(m_i,q_i)`:

1. discard no information about cross terms;
2. identify balanced components `q_i=m_i`;
3. split them by parity of `m_i`;
4. require the balanced opposite-parity block of `K` to vanish, unless an exact trajectory-specific cross-cancellation theorem exists;
5. all pairs involving an over-cancelled component are removable by positive total excess order.

This is the minimal structural condition needed to safely consume zero-contact normalized primitives inside a quadratic energy without imposing the unnecessarily strong requirement that every signed primitive be continuous.

---

## 10. Status boundary

**Result:** mathematical child complete; integration pending.

**Proved here:** exact pairwise parity law, necessary-and-sufficient universal balanced-block condition, exact jump formula, positive-definite counterexample to square-only lifting, all-odd regularity, and quantitative post-cancellation Lipschitz bound.

**Not claimed:** factor discovery, concrete P5 source binding, actual deployed `K`, Float64/FD/controller semantics, interval coverage, Lean/kernel compilation, verifier receipt, parent closure, M4 closure, or registry admission.
