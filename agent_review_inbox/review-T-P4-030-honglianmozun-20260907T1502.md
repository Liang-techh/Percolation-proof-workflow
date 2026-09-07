---
kind: review_result
review_id: review-T-P4-030-honglianmozun-20260907T1502
task_id: T-P4-030
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T14:48:00-06:00
created_at: 2026-09-07T15:02:00-06:00
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - scripts/record_routeb_true_dh_port_binding_decomposition.py
  - scripts/record_routeb_true_dh_source_formula_audit.py
continuation_of:
  - abce0d21c9ff175afb5ddc989cce0d6d01ccc686
  - 727086574670cb753dbd3212161ac9589f649111
related_tasks:
  - T-P4-024
  - T-P4-025
  - T-P4-026
  - T-P4-028
  - T-P4-029
  - T-P4-032
integration_status: pending
admission_label: pending
proposed_integration_target: theorem_and_consumer_sign_ledger
requested_action: use_R_port_for_every_linear_port_occurrence_keep_R_gain_only_after_an_explicit_even_norm_square_elimination_and_recheck_any_combined_Schur_cross_block_before_reusing_old_receipts
---

# T-P4-030 — exact port-sign ledger for residual, co-state, power, Young and Schur consumers

## 0. Result in one sentence

The corrected nominal-distal elimination forces

```text
r_B = R_port a_B = - R_gain a_B,
R_port := -M_BD M_DD(mu)^(-1) DeltaM_DB,
R_gain := +M_BD M_DD(mu)^(-1) DeltaM_DB.                 (0.1)
```

Therefore every consumer that is **odd in the disputed port coefficient** must flip sign, while a consumer may reuse the historical `R_gain` only after the port has been reduced to an **even** quantity such as `||R a||^2`, `||R||_F^2`, or an isolated `R^T H R`.  In particular the compact `T-P4-024` Young budget is numerically unchanged once its premise is already `||r_B||^2 <= rho A_up`, but the exact residual/co-state/power identities feeding that budget must use `R_port`.

This review gives the exact algebra and a failure boundary.  It does not redo the source audit, port-norm proof, Float64 enclosure, partition search, controller-damping reconciliation, registry admission, or the independent verifier receipt.

---

## 1. Exact elimination and the sign that cannot be chosen conventionally

Write

```text
Delta := M_DB - M0_DB,
A     := M_DD(mu),
B     := M_BD.                                           (1.1)
```

Assume the declared nominal-distal equations

```text
A v + Delta a_B = 0,                                     (1.2)
r_B - B v = 0,                                           (1.3)
```

and that `A` is invertible on the exact-real lane.  Then

```text
v = -A^(-1) Delta a_B,                                   (1.4)
```

so (1.3) gives

```text
r_B
 = B v
 = -B A^(-1) Delta a_B
 = R_port a_B.                                           (1.5)
```

If the historical positive quantity is retained as

```text
R_gain := B A^(-1) Delta,                                (1.6)
```

then necessarily

```text
R_port = -R_gain,
r_B    = -R_gain a_B.                                    (1.7)
```

There is no sign convention left to choose after (1.2)-(1.3) are fixed.  Hence the triple

```text
A v + Delta a_B = 0,
r_B - B v = 0,
r_B = R_gain a_B                                         (1.8)
```

is inconsistent in general.

### Exact scalar obstruction receipt

Take the one-dimensional exact data

```text
A=1, Delta=1, B=1, a_B=1.                               (1.9)
```

Then (1.2) gives `v=-1`, (1.3) gives `r_B=-1`, while

```text
R_port=-1,
R_gain=+1.                                               (1.10)
```

Thus `R_port a_B=r_B` is exact and `R_gain a_B=r_B` is false.  For the test covector `s_B=1`,

```text
s_B r_B = -1,
s_B R_gain a_B = +1,                                    (1.11)
```

whereas

```text
|r_B|^2 = |R_gain a_B|^2 = 1.                            (1.12)
```

This tiny exact witness isolates precisely which downstream operations erase the global sign and which do not.

---

## 2. Minimal coefficient/sign ledger

Let

```text
g_B := R_gain a_B,
so r_B = -g_B.                                           (2.1)
```

Then the downstream ledger is:

| consumer | physical identity | may reuse positive `R_gain` without an explicit minus? |
|---|---|---|
| typed residual coefficient | `r_B = R_port a_B = -g_B` | **no** |
| co-state / multiplier pairing | `s_B^T r_B = -s_B^T R_gain a_B` | **no** |
| port power | `a_B^T r_B = -a_B^T R_gain a_B` | **no** |
| base/port cross term | `2 l_base^T r_B = -2 l_base^T R_gain a_B` | **no** |
| exact total residual | `l_base+r_B = l_base-R_gain a_B` | **no** |
| port norm square | `||r_B||^2 = ||R_gain a_B||^2` | yes |
| Frobenius square | `||R_port||_F^2 = ||R_gain||_F^2` | yes |
| weighted port square | `r_B^T W r_B = (R_gain a_B)^T W(R_gain a_B)` | yes |
| isolated quadratic map contraction | `R_port^T H R_port = R_gain^T H R_gain` | yes |
| absolute-value / Young RHS | depends only on norms | yes, after the sign-sensitive equality has been instantiated correctly |

The safe criterion is **parity in the disputed coefficient**, not polynomial degree in the state.  This matters for the explicitly requested term `a_B^T r_B`: it is quadratic in `a_B`, but it contains `R_port` only once, so it changes sign.

---

## 3. Dissipation/power consequence: only the symmetric part of `R_gain` contributes, with the corrected minus sign

For real vectors,

```text
a_B^T r_B
 = -a_B^T R_gain a_B
 = -a_B^T Sym(R_gain) a_B,                               (3.1)
```

where

```text
Sym(R_gain) := (R_gain + R_gain^T)/2.                    (3.2)
```

The skew part drops out exactly.  Hence a source-independent energy corollary is:

```text
Sym(R_gain) >= gamma I
    ==> a_B^T r_B <= -gamma ||a_B||^2.                   (3.3)
```

Conversely, if only a norm bound on `R_gain` is available, one may conclude only

```text
|a_B^T r_B| <= ||R_gain||_op ||a_B||^2,                  (3.4)
```

not a dissipative sign.  Therefore any old argument that read the positive `R_gain` directly as physical port power must be re-signed before it can support a dissipation claim.

The same rule holds for a co-state or Lyapunov cross term:

```text
2 s_B^T r_B = -2 s_B^T R_gain a_B.                       (3.5)
```

A cancellation identity that is useful as a checker target is simply

```text
s_B^T R_port a_B + s_B^T R_gain a_B = 0.                 (3.6)
```

---

## 4. Why the existing Young port-energy budget can survive unchanged

The exact residual must be written

```text
l_total = l_base + r_B
        = l_base - R_gain a_B.                           (4.1)
```

For any fixed rational `lambda>1`, the ordinary Young inequality gives

```text
||l_total||^2
 <= lambda/(lambda-1) ||l_base||^2
    + lambda ||R_gain a_B||^2.                           (4.2)
```

Proof: expand

```text
||l_base-r||^2 = ||l_base||^2 - 2<l_base,r> + ||r||^2   (4.3)
```

with `r=R_gain a_B`, and use

```text
-2<l_base,r>
 <= (1/(lambda-1))||l_base||^2 + (lambda-1)||r||^2.      (4.4)
```

Exactly the same right-hand side is obtained for `l_base+r`.  Therefore, once a separate source-facing theorem supplies

```text
||R_gain a_B||^2 = ||R_port a_B||^2 <= rho A_up,         (4.5)
```

one recovers the existing compact consumer

```text
||l_total||^2
 <= lambda/(lambda-1)||l_base||^2 + lambda rho A_up.     (4.6)
```

Consequently the scalar/PMI gate used by `T-P4-024`,

```text
b_base >= lambda rho A_up
          + lambda/(lambda-1)||l_base||^2,               (4.7)
```

is **sign-invariant at the port-energy consumption layer**.  No new `rho` proof or broad partition recomputation is mathematically required merely because `R_port=-R_gain`.

However, (4.6)-(4.7) do **not** license the false exact identity `l_total=l_base+R_gain a_B`.  The exact decomposition and any cross-term receipt must first use (4.1); only the later Young/norm-square elimination erases the sign.

This also clarifies the roles of the neighboring children:

- `T-P4-025` norm-square expansion is unchanged as an abstract identity, but when instantiated with the physical port its cross term is `2<l_base,r_B> = -2<l_base,R_gain a_B>`;
- `T-P4-026` Young's bound remains numerically unchanged because its final right-hand side is even in `r_B`;
- fixed-`lambda` arithmetic that consumes only `rho A_up` is not altered by the global sign.

---

## 5. Schur/S-lemma parity: isolated cross-block flips are PSD-equivalent, mixed cross-blocks are not automatically safe

There is one useful but limited sign-invariance theorem.  For a symmetric block matrix

```text
H(C) = [[A, C],
        [C^T,D]],                                        (5.1)
```

let

```text
J = diag(I,-I).                                          (5.2)
```

Then

```text
H(-C) = J^T H(C) J.                                      (5.3)
```

Therefore

```text
H(C) >= 0  <=>  H(-C) >= 0.                              (5.4)
```

and, when the Schur expression is isolated,

```text
(-C)^T A^(-1)(-C) = C^T A^(-1) C.                       (5.5)
```

So a Schur consumer that uses the disputed port map **only as the entire cross block** can reuse a magnitude/PSD certificate after the sign repair.

But this does not justify blindly reusing a combined cross block.  If

```text
C_total = C0 + C_port                                    (5.6)
```

with `C0` fixed independently of the port sign, then for symmetric `H`

```text
(C0+C_port)^T H(C0+C_port)
 -(C0-C_port)^T H(C0-C_port)
 = 2 C0^T H C_port + 2 C_port^T H C0.                    (5.7)
```

In scalar form (or symmetric scalar contraction) this is `4 C0^T H C_port`, generally nonzero.  Thus a **combined-Schur receipt is not sign-safe merely because it contains a square**: one must check whether the disputed port term was isolated before squaring or was first added to another fixed cross coefficient.

This is the explicit obstruction for any downstream combined-S-lemma/Schur ledger whose coefficient binding is not visible.  Until that binding is inspected, the correct status is `pending`, not “unchanged by sign”.

---

## 6. Exact error if the old plus-sign residual decomposition is retained

Define

```text
L_true  := l_base - R_gain a_B,
L_wrong := l_base + R_gain a_B.                          (6.1)
```

Then

```text
L_wrong - L_true = 2 R_gain a_B = -2 r_B.                (6.2)
```

Thus the old plus-sign decomposition is not a harmless notation swap.  It is physically exact only on the exceptional set

```text
R_gain a_B = 0.                                          (6.3)
```

Likewise an exact co-state equality using the wrong sign differs by

```text
2 s_B^T R_gain a_B.                                      (6.4)
```

and an exact port-power equality differs by

```text
2 a_B^T R_gain a_B.                                      (6.5)
```

These formulas provide direct regression targets for any source-bound downstream recorders.

---

## 7. Affected theorem/file ledger

### Must use the physical minus sign

1. `P4.true_dh_residual_map_coefficient_binding` and the typed target attached to it must state

```text
R_port a_B = r_B.                                        (7.1)
```

It must not state `R_gain a_B=r_B` together with the nominal-distal equations.

2. `T-P4-032` is the correct formal leaf for the exact-real typed identity.  This review deliberately does not duplicate its Lean compilation task.

3. `scripts/record_routeb_true_dh_port_binding_decomposition.py` and any residual decomposition emitted from it must keep the physical coefficient `R_port` until a norm-square elimination is explicit.

4. `scripts/record_routeb_true_dh_source_formula_audit.py` must keep the source formula with the leading minus sign.  The coordinator sign-repair commit already changed this source-level formula; this review only records the downstream algebraic consequence.

5. Any receipt containing `s_B^T r_B`, `a_B^T r_B`, `l_base^T r_B`, a multiplier/co-state pairing, or an exact S-lemma cross coefficient must be regenerated or checked with `r_B=-R_gain a_B`.

### Can retain the old magnitude after an explicit sign-erasing step

1. Frobenius / operator / vector norm-square bounds on the isolated port map;
2. the scalar `rho A_up` consumer in `T-P4-024`;
3. `T-P4-026` after the exact cross term has been handed to Young;
4. isolated `R^T H R` or isolated Schur-tail consumers.

### Explicitly pending inspection

Any existing combined-Schur or S-lemma ledger in which the port coefficient may have been added to another fixed cross block before squaring.  Formula (5.7) shows why a blanket “norm-square is sign-invariant” statement is insufficient in that case.  This review does not claim such a ledger is wrong; it records the exact condition that must be checked before reuse.

---

## 8. Candidate small theorem statements for formalization

The following source-independent leaves are sufficient for the downstream sign layer.

### `port_linear_pairing_neg`

Premise:

```text
R_port = -R_gain.                                        (8.1)
```

Conclusion:

```text
<s, R_port a> = -<s, R_gain a>.                          (8.2)
```

### `port_power_sym_part`

For real matrices/vectors:

```text
<a, R_port a>
 = -<a, R_gain a>
 = -<a, Sym(R_gain) a>.                                  (8.3)
```

### `port_weighted_square_sign_invariant`

```text
(R_port a)^T W(R_port a)
 = (R_gain a)^T W(R_gain a).                             (8.4)
```

No positivity assumption on `W` is required for the equality; positivity is only needed when the expression is used as an energy upper/lower bound.

### `young_residual_sign_erasure`

For `lambda>1` and `r=-g`,

```text
||l+r||^2
 <= lambda/(lambda-1)||l||^2 + lambda||g||^2.            (8.5)
```

### `isolated_cross_block_sign_congruence`

```text
[[A,-C],[-C^T,D]]
 = diag(I,-I)^T [[A,C],[C^T,D]] diag(I,-I).              (8.6)
```

Hence PSD is equivalent for the isolated global cross-block sign flip.

### `mixed_schur_sign_difference`

For symmetric `H`,

```text
(C0+C)^T H(C0+C) - (C0-C)^T H(C0-C)
 = 2 C0^T H C + 2 C^T H C0.                             (8.7)
```

This is the formal obstruction lemma against reusing a combined-Schur receipt without inspecting its coefficient decomposition.

All of (8.2)-(8.7) are ring/inner-product identities plus ordinary Young; they are suitable for tiny Lean sidecars.  No new Lean compile is claimed here because `T-P4-032` already owns the typed matrix-elimination compilation lane.

---

## 9. Integration recommendation and remaining blockers

The safest downstream interface is a two-stage contract:

```text
Stage A (sign-sensitive source semantics):
  R_port a_B = r_B,
  R_port = -R_gain.

Stage B (optional sign erasure):
  prove an explicit even consequence such as
  ||r_B||^2 = ||R_gain a_B||^2 <= rho A_up.

Only after Stage B may a consumer forget the minus sign.                (9.1)
```

This prevents a magnitude certificate from being silently reused as a linear residual/co-state coefficient.

Current mathematical conclusion:

- the corrected minus sign is forced exactly by the nominal-distal equations;
- all linear residual/co-state/power consumers must flip;
- the existing compact Young port-energy budget can retain its scalar form once the norm-square premise is explicit;
- isolated Frobenius and Schur-square consumers are sign-invariant;
- combined cross-block Schur/S-lemma consumers remain **explicitly pending inspection** unless their port term is demonstrably isolated before squaring.

Open non-mathematical/source blockers remain those already tracked by the queue: exact deployed source binding, Float64 evaluator enclosure, controller-semantics reconciliation, complete coverage, and independent verification.  This review does not promote any existing `rho^2` candidate or close P4/M4.
