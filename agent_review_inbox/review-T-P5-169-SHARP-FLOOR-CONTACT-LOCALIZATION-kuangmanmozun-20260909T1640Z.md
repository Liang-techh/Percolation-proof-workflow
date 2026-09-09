---
kind: review_result
review_id: review-T-P5-169-sharp-floor-contact-localization-kuangmanmozun-20260909T1640Z
task_id: T-P5-169-SHARP-FLOOR-CONTACT-LOCALIZATION
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T16:40:00Z
claim_commit: 6d6041814e66e1cf07a5a1ffeedc916775932708
inspected_commit: a3b6eff3b7be324a493c80383543799a44a22acb
upstream_commits:
  - 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9  # T-P5-159 symbolic floor/contact
  - f1c26726dcc54201ced3886d51fe0d5f40102ad4  # T-P5-165 negative-component factorization
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: localize_positive_sharp_floor_contacts_to_one_negative_component; solve_symbolic_floor_per_initial_negative_component_and_take_the_max; restrict_principal_kernel_root_search_to_a_winning_component
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional order/quadratic-form algebra only
exit_code: n/a
---

# T-P5-169 — sharp-floor contact localization and componentwise exact floor

## 0. Verdict and non-overlap

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-159 proves that the uniform additive floor family has a unique sharp threshold `D_*`, that a zero contact at a valid positive floor proves sharpness, and that a positive sharp contact yields a principal zero mode. T-P5-165 proves that, at a fixed `D`, copositivity factors over connected components of the graph of strictly negative off-diagonal entries.

The missing link is the **zero level**, not the negative level: T-P5-165 localizes strict FAIL witnesses, but does not state what happens to a sharp contact `q_{D_*}(x)=0`. At zero, nonnegative within-component and cross-component charges can in principle tie, so this needs an explicit argument.

This child proves that every positive sharp contact decomposes into zero contacts on its active strict-negative components; consequently at least one single component by itself attains the entire global sharp floor. It also gives a stronger static decomposition: the global sharp floor equals the maximum of the sharp floors of the connected components of the negative graph at `D=0`.

No source/provenance audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, admission, or independent re-audit is performed.

---

## 1. Setup

Use the T-P5-154/T-P5-159 floor family. Let `g_i>0` and symmetric pair data `K_ij=K_ji`, `K_ii=0`. For `D>=0`, define the symmetric matrix

`M_D[i,i] = D g_i`,

`2 M_D[i,j] = K_ij + D(g_i+g_j)` for `i!=j`.

For `x>=0`, write

`q_D(x) := x^T M_D x`.

The exact homogeneous identity is

**(1.1)**

`q_D(x) = Q_0(x) + D L(x)`,

where

`Q_0(x)=sum_{i<j} K_ij x_i x_j`,

`L(x)=(sum_i x_i)(sum_i g_i x_i)`.

For every nonzero `x>=0`,

**(1.2)** `L(x)>0`.

Let `D_*` be the least `D>=0` for which `M_D` is copositive. By T-P5-159, this exists, the valid set is `[D_*,infinity)`, and if `D_*>0` there is a nonzero contact `x_*>=0` with

**(1.3)** `q_{D_*}(x_*)=0`.

Let `Gamma_*(D)` denote the strict-negative graph of `M_D`:

`{i,j}` is an edge iff `M_D[i,j]<0`, equivalently

**(1.4)** `K_ij + D(g_i+g_j)<0`.

---

## 2. Main zero-level theorem: contact decomposes componentwise

Fix any `D>=0` such that `M_D` is copositive, and let

`C_1,...,C_s`

be the connected components of `Gamma_*(D)`.

For a vector `x>=0`, let `x^(a)` be its restriction to `C_a`, extended by zero outside that component.

T-P5-165 gives the exact decomposition

**(2.1)**

`q_D(x)
 = sum_a q_D(x^(a))
 + 2 sum_{a<b} sum_{i in C_a, j in C_b} M_D[i,j] x_i x_j`.

Because `M_D` is copositive, every principal component block is copositive, so

**(2.2)** `q_D(x^(a))>=0`.

By definition of the strict-negative components, every cross-component entry satisfies

**(2.3)** `M_D[i,j]>=0`.

Therefore every term on the right side of (2.1) is nonnegative.

### Theorem T169-A — `zero_contact_splits_over_negative_components`

Assume `M_D` is copositive, `x>=0`, and

`q_D(x)=0`.

Then for every component `C_a` with `x^(a)!=0`,

**(2.4)** `q_D(x^(a))=0`.

Moreover every cross-component charge between active coordinates vanishes:

**(2.5)** `M_D[i,j] x_i x_j = 0`

whenever `i,j` lie in distinct components.

### Proof

Equation (2.1) is a finite sum of nonnegative real numbers by (2.2)-(2.3), and the sum equals zero. Hence every summand equals zero. In particular each component quadratic term is zero. Each cross-block sum is itself a finite sum of nonnegative coordinate terms, so every coordinate term in it also vanishes. QED.

### Interpretation

A zero contact is allowed to touch several negative components simultaneously, but it can do so only as a **tie of independent zero contacts**, with zero cross charge on all active cross pairs. There is never an essential multi-component cancellation at the sharp floor, because every cross-component term has the wrong sign for cancellation.

---

## 3. Positive sharp floor localizes completely to one component

Now set `D=D_*>0` and take any global sharp contact `x_*` from (1.3). Apply T169-A to the components of `Gamma_*(D_*)`.

Choose any active component `C`, so `x_C:=x_*^(C)!=0`. Then

**(3.1)** `q_{D_*}(x_C)=0`.

Define the local sharp floor of the principal family on `C` by

`D_C^* := inf {D>=0 : M_D[C] is copositive}`.

T-P5-159 applies verbatim to this restricted finite family because all `g_i` on `C` remain positive.

### Theorem T169-B — `active_contact_component_has_global_sharp_floor`

For every active component `C` of a positive global sharp contact,

**(3.2)** `D_C^* = D_*`.

### Proof

Since the full `M_{D_*}` is copositive, its principal block `M_{D_*}[C]` is copositive. Hence

`D_C^* <= D_*`.

On the other hand, by (1.1) restricted to `C`, for every `D<D_*`,

`q_D(x_C)
 = q_{D_*}(x_C) - (D_*-D)L(x_C)
 = -(D_*-D)L(x_C)`.

Because `x_C!=0`, (1.2) gives `L(x_C)>0`; therefore

**(3.3)** `q_D(x_C)<0` for every `D<D_*`.

Thus no smaller `D` can make the local block copositive, so `D_C^*>=D_*`. Combine the two inequalities. QED.

### Corollary T169-B1 — a single component is an exact global sharpness witness

At a positive global sharp floor, at least one strict-negative component alone supplies:

1. a local fixed-`D_*` copositivity PASS;
2. a nonzero local zero contact;
3. an exact FAIL witness for every lower `D<D_*` by (3.3).

Hence global symbolic sharpness never requires a support spanning distinct components of `Gamma_*(D_*)`.

### Corollary T169-B2 — winning component has at least two vertices

If `D_*>0`, no active zero-contact component can be a singleton. For a singleton `{i}`,

`q_{D_*}(x_i e_i)=D_* g_i x_i^2>0`

whenever `x_i!=0`.

Therefore every winning component contains at least one strict negative edge.

---

## 4. Stronger static decomposition at `D=0`

The dynamic components at `D_*` are useful for a sharp contact, but the entire symbolic floor problem can be separated **before any bracketing**.

Let

`B_1,...,B_r`

be the connected components of the strict-negative graph at `D=0`. Since

`2 M_0[i,j]=K_ij`,

indices in different `B_a` satisfy

**(4.1)** `K_ij>=0`.

For every `D>=0`,

`2 M_D[i,j]=K_ij+D(g_i+g_j)>=0`

across distinct `B_a`, because `g_i+g_j>0`.

Thus the same fixed partition `B_1,...,B_r` has nonnegative cross entries for **every** `D>=0`.

Let `D_{B_a}^*` be the sharp floor of the principal family on `B_a`.

### Theorem T169-C — `global_floor_eq_max_initial_negative_component_floors`

**(4.2)**

`D_* = max_a D_{B_a}^*`.

### Proof

For every fixed `D`, T-P5-165's nonnegative-cross partition theorem gives

`M_D copositive`

iff

`M_D[B_a] copositive for every a`.

Each local valid set is `[D_{B_a}^*,infinity)`. Their finite intersection is

`[max_a D_{B_a}^*, infinity)`.

But the global valid set is `[D_*,infinity)`. Therefore the left endpoints are equal. QED.

### Operational consequence

T-P5-159 rational PASS/FAIL bracketing can run **independently on the connected components of the negative graph at `D=0`**, and the global certified floor is simply the maximum of the local floors/brackets. No support/KKT search ever needs to cross those initial components.

This is stronger than recomputing only a fixed-`D` split: it factorizes the entire one-parameter optimization problem.

Singleton initial components have local sharp floor `0`, so they may be discarded immediately when searching for a positive `D_*`.

---

## 5. Symbolic kernel/root search also localizes

T-P5-159 shows that at a positive sharp floor there is a support `S` with a positive normalized vector `lambda_S` satisfying

**(5.1)** `M_{D_*,SS} lambda_S = 0`.

T169-B allows the zero contact to be chosen inside one winning strict-negative component `C` of `Gamma_*(D_*)`. Applying the same face-minimizer/KKT argument to that local zero contact gives a support

**(5.2)** `S subseteq C`

with the positive kernel property (5.1).

Therefore a symbolic determinant/root search for sharpness candidates does not need principal supports spanning distinct strict-negative components at the candidate floor. A root candidate that can only be realized by a support crossing such components is structurally redundant: one active component already contains an equally sharp zero mode.

This does **not** mean the component is fixed while moving `D` downward. Negative edges can reappear as `D` decreases and components can merge. The theorem only says the same local contact, zero-extended to the full space, remains a valid strict FAIL witness for every lower floor by (3.3).

---

## 6. Degenerate tie regression: original contact need not itself be one-component

The theorem must say **a sharp contact can be localized**, not that every zero contact has support in only one component.

Take four vertices with

`g_1=g_2=g_3=g_4=1`,

`K_12=K_34=-4`,

and every cross-pair coefficient between `{1,2}` and `{3,4}` equal to `-2`.

At `D_*=1`,

`M_1 =
 [[ 1,-1, 0, 0],
  [-1, 1, 0, 0],
  [ 0, 0, 1,-1],
  [ 0, 0,-1, 1]]`.

This matrix is PSD and hence copositive. Each pair block has the zero contact `(1,1)`, and for any `D<1`, that same pair vector has quadratic value

**(6.1)** `4(D-1)<0`.

Hence the global sharp floor is exactly `D_*=1`.

The strict-negative graph of `M_1` has two components `{1,2}` and `{3,4}`. Yet

`x=(1,1,1,1)`

is also a global zero contact spanning **both** components, because all cross-component entries are exactly zero at `D=1`.

So uniqueness of the winning component is false in degenerate ties. T169-A gives the correct statement: every active component restriction is itself a zero contact and every active cross charge vanishes.

---

## 7. Endpoint obstruction: `D_*=0` needs separate wording

The size-at-least-two conclusion is false at the zero-floor endpoint.

Take `K_ij=0` for every pair. Then `D_*=0`, `M_0=0`, and every singleton basis vector `e_i` is a zero contact.

Thus the statement

> every sharp contact component contains a negative edge

requires **`D_*>0`**. The componentwise zero-splitting theorem T169-A itself remains valid at `D=0`; only the positive-diagonal exclusion of singleton contacts disappears.

This endpoint should remain explicit in any formal theorem rather than being hidden behind a division or strict-positivity assumption.

---

## 8. Lean-friendly theorem statements

### Lemma L1 — zero finite sum of nonnegative component charges

For a finite partition of coordinates, assume a symmetric matrix `M` satisfies:

1. every block restriction is copositive;
2. every cross-block entry is nonnegative.

If `x>=0` and `x^T M x=0`, then every block restriction `x_a` satisfies

`x_a^T M x_a=0`,

and every cross coordinate charge `M_ij x_i x_j=0`.

This is finite-sum order algebra only.

### Lemma L2 — local zero contact gives lower-floor strict failure

For `g_i>0`, nonzero `x>=0`, and `D'<D`, if

`q_D(x)=0`,

then

`q_{D'}(x)=-(D-D') (sum_i x_i)(sum_i g_i x_i) < 0`.

No division is required.

### Lemma L3 — fixed initial partition remains cross-nonnegative

If `K_ij>=0` for indices in distinct blocks and `D>=0`, `g_i,g_j>0`, then

`K_ij+D(g_i+g_j)>=0`.

Combined with T-P5-165's partition theorem, this yields T169-C without graph-library machinery.

---

## 9. What this closes and what remains open

### New mathematical closure

- zero-level analogue of T-P5-165: a global copositive zero contact decomposes into local zero contacts on every active strict-negative component;
- at a positive global sharp floor, every active contact component has **exactly the same local sharp floor `D_*`**;
- the same localized contact is a strict exact FAIL witness for **every** lower floor;
- the whole symbolic floor problem factors once and for all over the negative components at `D=0`, with global floor equal to the maximum of local floors;
- principal kernel/determinant sharpness search may be restricted to a winning component;
- explicit degenerate tie example prevents a false uniqueness claim;
- explicit `D_*=0` endpoint prevents a false size-at-least-two claim.

### Still open

- actual same-key source values `{g_i,K_ij}` and exact/interval sign table;
- actual uncertainty-simplex / homothetic semantics and coverage;
- exact source binding of any candidate floor or contact;
- Float64/direct-rounding/runtime/controller/P8 obligations;
- Lean/kernel compilation and independent verification by 封不觉;
- registry/admission and P5/P8/M4 parent closure.

Therefore the result remains

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`.**

---

## 10. Recommended next use

Before launching any global symbolic support/root search, construct the strict-negative graph of the base pair data `K_ij` at `D=0`. Solve or bracket each connected component independently and take the maximum local floor. At a candidate sharp endpoint, recompute the strict-negative graph at that `D`; any zero contact can then be reduced to one winning component, and that local contact certifies strict failure for every smaller floor.
