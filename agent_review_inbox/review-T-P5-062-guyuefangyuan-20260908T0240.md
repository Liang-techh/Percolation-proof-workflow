---
kind: review_result
review_id: review-T-P5-062-guyuefangyuan-20260908T0240
task_id: T-P5-062-MULTIFACTOR-LIPSCHITZ-STRATA
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-08T02:26:00-06:00
created_at: 2026-09-08T02:40:00-06:00
claim_commit: 3a3b5e66505e4b9ee37070f2d443fac5978d6838
parent_tasks:
  - T-P5-057-RADICAL-FACTOR-CANCEL
  - T-P5-058-QUADRATIC-RADICAL-CANCEL
  - T-P5-061
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a quantitative multi-factor monomial regularity gate distinguishing deepest-stratum removability from whole-cell Lipschitz regularity; use exact excess support plus reachable sign characters, with rational Lipschitz constants and a partial-stratum counterexample
---

# T-P5-062 — multi-factor Lipschitz / partial-stratum gate

## 0. Bottleneck and non-overlap

T-P5-061 closes the algebraic contact-value problem for several active zero factors by attaching an `F_2^r` parity mask to each balanced channel and testing the reachable sign action. It explicitly leaves **quantitative Lipschitz/Hölder rates after multi-factor cancellation** open.

There is a second issue hidden inside that quantitative obligation: vanishing at the *deepest intersection* of several zero surfaces does not imply continuity, let alone Lipschitz regularity, on a whole cell containing the lower-codimension partial strata. A factor may damp the value only when one coordinate tends to zero while an undamped odd sign from another coordinate still produces a jump along its own zero surface.

This child gives an exact monomial-level criterion, an explicit rational Lipschitz constant, the reachable-subgroup refinement, and a sharp counterexample. It does not redo the T-P5-061 contact-action theorem and makes no source binding, reachability, Float64, ODE, Lean compilation, provenance, verification, or admission claim.

---

## 1. Canonical monomial packet after multi-factor cancellation

Take active factors `h_1,...,h_r`. For channel `i`, assume the T-P5-061 packet

`A_i = S_i * prod_a h_a^(2 m_{i,a})`,

`G_i = J_i * prod_a h_a^(q_{i,a})`,

`q_{i,a} >= m_{i,a} >= 0`, `S_i>0`, and put

`k_{i,a}=q_{i,a}-m_{i,a} >= 0`,

`v_i=J_i/sqrt(S_i)`.

Away from the zero surfaces,

`u_i = [prod_a sign(h_a)^(q_{i,a}) |h_a|^(k_{i,a})] v_i`.

Now consider one canonical consumer monomial

`M(u)=prod_i u_i^(n_i)`, `n_i in N`.

Collect its exact factor data:

**(1.1) excess order**

`e_a := sum_i n_i k_{i,a} in N`,

**(1.2) parity mask**

`beta_a := (sum_i n_i q_{i,a}) mod 2 in F_2`,

and reduced monomial

`R := prod_i v_i^(n_i)`.

Then on every punctured sign chamber,

**(1.3)**

`M = psi_(e,beta)(h) * R`,

where

`psi_(e,beta)(h) = [prod_a sign(h_a)^(beta_a)] [prod_a |h_a|^(e_a)]`.

Let

`P := {a : e_a>0}`

be the set of **damped factors**, and `Z=P^c` the zero-excess factors.

This `(e,beta)` packet is all that the quantitative contact checker needs from the radical factor layer.

---

## 2. Full-box theorem: exact regularity criterion

Assume the source cell contains all sign chambers of a box

`|h_a| <= H_a`, with rational `H_a>0`.

### Theorem 2.1 — full-box Lipschitz iff odd parity is supported on damped factors

The scalar contact factor `psi_(e,beta)` has a globally Lipschitz extension through every coordinate zero surface in the box if and only if

**(2.1)**

`beta_a=0` for every `a` with `e_a=0`.

Equivalently,

**(2.2)** `supp(beta) subseteq P`.

When (2.1) holds, define for `a in P`

**(2.3)**

`C_a := H_a^(e_a-1) * prod_(b != a) H_b^(e_b)`.

Then with the `l1` metric,

**(2.4)**

`Lip(psi) <= L_psi := max_(a in P) e_a C_a`,

with `L_psi=0` if `P` is empty.

Also

**(2.5)** `|psi(h)| <= B_psi := prod_a H_a^(e_a)`.

All quantities are exact rational numbers when the `H_a` are rational.

### Proof — sufficiency

For each coordinate with `e_a>0`, the one-dimensional factor is either

`|x|^(e_a)` when `beta_a=0`,

or

`sign(x)|x|^(e_a) = x |x|^(e_a-1)` when `beta_a=1`.

Both are globally Lipschitz on `[-H_a,H_a]` with Lipschitz constant

`e_a H_a^(e_a-1)`

and sup norm `H_a^(e_a)`.

If `e_a=0`, condition (2.1) forces the coordinate factor to be identically `1`, so there is no sign discontinuity.

A telescoping product estimate therefore gives

`|psi(x)-psi(y)|`

`<= sum_(a in P) e_a C_a |x_a-y_a|`

`<= L_psi ||x-y||_1`.

This also defines the unique continuous extension at coordinates where some `h_a=0`.

### Proof — necessity

Suppose there is a coordinate `a` with `e_a=0` and `beta_a=1`. Fix every other coordinate at a nonzero value inside the box, and approach `h_a=0` from the two signs. The magnitude factor does not contain `|h_a|`, while the sign character changes sign. Hence the two one-sided values are nonzero opposites. No continuous extension exists across that partial zero surface, so Lipschitz regularity is impossible.

Thus (2.1) is necessary and sufficient.

---

## 3. Sharp obstruction: deepest-intersection vanishing does NOT imply whole-cell continuity

The simplest exact radical packet already shows why T-P5-061 contact-value vanishing is not enough for quantitative cell certification.

Take two active factors `s,t` and one channel

**(3.1)**

`A(s,t)=s^2 t^2`,

`G(s,t)=s^2 t`,

with `S=J=1`.

Then

`m=(1,1)`,

`q=(2,1)`,

`k=(1,0)`,

so

**(3.2)**

`u(s,t)=G/sqrt(A)=|s| sign(t)`

whenever `st != 0`.

At the deepest intersection `(s,t)->(0,0)`,

`|u(s,t)|=|s| -> 0`.

So the channel is over-cancelled in the `s` factor and has the perfectly removable full-intersection value `0`.

But on every box around the origin, fix any `s0 != 0`. Then

`lim_(t->0+) u(s0,t)=|s0|`,

`lim_(t->0-) u(s0,t)=-|s0|`.

Thus the same channel has a genuine jump across the partial stratum `t=0, s=s0`.

In packet language,

`e=(1,0)`, `beta=(0,1)`.

The odd parity sits on the undamped factor `t`, violating (2.1).

**Conclusion:** `over-cancelled on at least one active factor -> zero at the deepest stratum` is a correct contact-value statement, but it must not be promoted to `whole cell is continuous/Lipschitz`. A whole-cell certificate must control every partial stratum, exactly as Theorem 2.1 does.

This is the main obstruction found in this child.

---

## 4. Reachable-chamber refinement

A full sign cube can be too strong when the source domain permits only selected sign chambers. Let `Omega subset {+1,-1}^r` be the certified chamber set.

For a chamber `eps`, write

`chi_beta(eps)=prod_a eps_a^(beta_a)`.

The correct finite condition is:

**(4.1) damped-sign compatibility**

For every `eps,eta in Omega`,

if `chi_beta(eps) != chi_beta(eta)`, then there exists `a in P` with `eps_a != eta_a`.

Equivalently:

**(4.2)** if two reachable chambers agree on all damped-factor signs, then they must have the same `beta` character.

### Theorem 4.1 — reachable-chamber Lipschitz sufficiency

If (4.1) holds, then on the union of the corresponding punctured orthant boxes, `psi_(e,beta)` has a Lipschitz extension to the closure with the same bound

`L_psi = max_(a in P) e_a C_a`.

### Proof

Take two punctured points `x,y`.

If their `beta` characters agree, the sign prefactor is the same and the ordinary telescoping bound for the magnitude product gives (2.4).

If the characters differ, (4.1) provides some damped coordinate `a in P` whose signs differ. Then

`|x_a-y_a|=|x_a|+|y_a|`.

Since `e_a>=1`, with `C_a` from (2.3),

`|psi(x)-psi(y)| <= |psi(x)|+|psi(y)|`

`<= C_a(|x_a|+|y_a|)`

`= C_a |x_a-y_a|`

`<= L_psi ||x-y||_1`.

So the same exact rational constant works across different reachable chambers as well.

### Necessity for orthant-complete source cells

If the source domain contains full radial pieces of every chamber in `Omega`, then (4.1) is also necessary: if two reachable chambers have opposite `beta` character but agree on every damped-factor sign, keep all damped magnitudes fixed and send only their differing zero-excess coordinates to zero. The two points converge to the same partial stratum while `psi` tends to nonzero opposite values.

For a lower-dimensional constrained source set this necessity can weaken, because geometric relations between magnitudes may supply extra damping. Such a relation must be source-bound explicitly; it cannot be inferred from sign data alone.

---

## 5. Subgroup/coset form compatible with T-P5-061

T-P5-061 packages relative reachable flips as a subgroup `H <= F_2^r`. For a chamber-complete coset `Omega=eps0 H`, let

`U_P := span{standard basis vector e_a : a in P}`.

Then condition (4.1) is equivalent to the linear-algebra gate

**(5.1)**

`beta in H^perp + U_P`.

Interpretation: after changing `beta` by a character that is trivial on all reachable flips, every remaining odd sign can be moved onto a factor with positive excess order.

### Proof

If `beta=gamma+sigma` with `gamma in H^perp` and `sigma in U_P`, then on `eps0 H`, `chi_gamma` is constant. Hence the reachable sign dependence of `chi_beta` is represented by `sigma`, whose support lies only on damped factors. Theorem 4.1 applies.

Conversely, if `beta notin H^perp+U_P`, finite-dimensional `F_2` duality gives a flip

`g in H intersection U_P^perp`

with `beta dot g=1`.

Such a `g` changes the `beta` character but flips no damped coordinate, contradicting (4.1).

### Important special cases

1. **full box:** `H=F_2^r`, so `H^perp={0}` and (5.1) reduces exactly to `beta in U_P`, i.e. `supp(beta) subseteq P`.

2. **balanced monomial:** `P` is empty, so (5.1) reduces to `beta in H^perp`, exactly the T-P5-061 contact-invariance gate.

3. **fixed-sign / one chamber:** `H={0}`, so `H^perp=F_2^r`; every parity mask passes, as expected.

4. **partial damping can neutralize a reachable sign:** if a sign character is nontrivial globally but differs from a damped-factor character by an element of `H^perp`, the monomial remains Lipschitz on the constrained source domain.

---

## 6. Exact constrained-domain example: a globally bad zero-excess sign becomes safe

Reuse

`psi(s,t)=|s| sign(t)`,

so `e=(1,0)`, `beta=(0,1)`, `P={s}`.

On the full four-chamber box this fails Theorem 2.1 because `t` has zero excess and odd parity.

Now suppose the certified source domain approaches only the diagonal sign chambers

`Omega={(+,+),(-,-)}`.

Then `sign(t)=sign(s)` on the punctured source set, so

**(6.1)** `psi(s,t)=s`.

It is globally 1-Lipschitz in the `s` coordinate despite the zero-excess odd `t` parity.

In subgroup form, `H=span{(1,1)}`,

`H^perp=span{(1,1)}`,

`U_P=span{(1,0)}`,

and indeed

`beta=(0,1)=(1,1)+(1,0) in H^perp+U_P`.

This shows why the quantitative gate must retain the T-P5-061 reachable-domain information rather than reverting to a global sign-cube test.

---

## 7. Transport through the reduced monomial

The scalar factor is only half of the source packet. Suppose on the same cell the reduced monomial `R` satisfies

`|R| <= M_R`

and

`|R(x)-R(y)| <= L_R ||x-y||_1`.

Under the gate of Section 2 or 4, use

`M=psi R`.

From (2.5) and the product difference identity,

**(7.1)**

`Lip(M) <= M_R L_psi + B_psi L_R`.

This is exact and rational whenever the source supplies rational `M_R,L_R,H_a`.

For a canonical polynomial/CSE consumer

`F=sum_s c_s M_s`,

if each retained monomial has its own admissible packet and bound `L_s`, then

**(7.2)**

`Lip(F) <= sum_s |c_s| L_s`.

This monomialwise rule is a safe no-cancellation consumer. If source CSE proves exact cancellation between individually incompatible terms, that stronger aggregate identity may be used separately; this theorem does not silently infer such cancellation.

---

## 8. Stratified interpretation for P5 cells

The practical lesson is that a multi-factor cell has a **stratum lattice**.

At the deepest intersection, any monomial with some positive excess order vanishes and may look harmless. But a partial stratum can keep every damped factor nonzero while setting an undamped odd factor to zero. Section 3 shows that this creates a jump.

Therefore a whole-cell P5 consumer should use one of two exact routes:

1. **global packet route:** certify Theorem 2.1 / 4.1 once for the complete monomial packet; or
2. **stratified route:** split the cell by active zero-factor subsets and re-run the T-P5-061 character gate plus the present excess-support gate on every stratum that the source domain can reach.

A certificate valid only at the highest-codimension intersection must not be reused on its faces without this check.

This is especially relevant to first-exit and residual Jacobian consumers: continuity of the Lyapunov power at one intersection point does not justify a uniform residual/Lipschitz constant over the enclosing cell.

---

## 9. Lean-friendly theorem decomposition

No Lean lane is claimed. A minimal formalization can avoid matrix APIs and most group theory.

### Core scalar lemmas

1. `abs_pow_lipschitz_on_box`
   - for natural `e>=1`, prove `x -> |x|^e` is Lipschitz on `|x|<=H` with constant `e H^(e-1)`.

2. `signed_abs_pow_lipschitz_on_box`
   - for natural `e>=1`, use `x*|x|^(e-1)` rather than a `sign` primitive and prove the same constant.

3. `product_lipschitz_l1`
   - bounded coordinate factors with constants `L_a,M_a` give product constant `max_a (L_a prod_{b!=a} M_b)` for the `l1` metric.

4. `fullbox_multifactor_lipschitz_of_parity_supported`
   - if every zero-excess coordinate has even parity, combine 1–3.

### Exact obstruction regression

5. `deep_contact_zero_not_whole_cell_continuous`
   - encode the packet `A=s^2*t^2`, `G=s^2*t` and the punctured identity `u=|s| sign(t)`; record the opposite one-sided values across `t=0` at fixed `s!=0`.

### Reachable-sign layer

6. `reachable_pair_damped_flip_lipschitz`
   - if opposite output characters imply a sign difference in one positive-excess coordinate, prove the cross-chamber bound in Section 4.

7. optional finite-bit theorem `subgroup_damped_gate_iff`
   - `beta in H^perp + U_P` iff every H-flip that is trivial on `P` has trivial `beta` character.

The trusted checker can use item 7 as finite XOR/bit-linear arithmetic; it does not need topology or square roots.

---

## 10. New fail-fast rule

For a proposed whole-cell monomial packet `(e,beta)`:

- if the source cell is full-sign and some `a` has `e_a=0`, `beta_a=1`, then **fail whole-cell regularity immediately**; either split at `h_a=0`, prove a source-domain sign restriction, or prove an exact aggregate cancellation;
- if only selected chambers are reachable, apply (4.1), or in a chamber-complete subgroup model use `beta in H^perp+U_P`;
- only after this structural gate passes should source work spend effort on numerical/rational Lipschitz constants for the reduced packet.

This prevents wasted interval/Jacobian work on a cell that is mathematically discontinuous before any numerical enclosure issue appears.

---

## 11. Status boundary

**Result:** mathematical child complete; integration pending.

**Proved here:**

- exact full-box necessary-and-sufficient parity/excess criterion for monomial Lipschitz regularity;
- explicit rational `l1` Lipschitz constant;
- reachable-chamber sufficient gate and exact necessity on orthant-complete domains;
- subgroup specialization `beta in H^perp+U_P`;
- exact radical counterexample `A=s^2t^2, G=s^2t` showing deepest-stratum vanishing but partial-stratum jump;
- exact constrained-domain example where reachable sign correlation restores Lipschitz regularity;
- reduced-monomial/product transport bound.

**Not claimed:** concrete source factorization, source proof of `Omega/H`, orthant-completeness, reduced-packet bounds, Float64/libm/FD/controller/solve semantics, P8/ODE coverage, Lean/kernel compilation, comparator/receipt/provenance, parent closure, P5/P8/M4 admission, or registry mutation.
