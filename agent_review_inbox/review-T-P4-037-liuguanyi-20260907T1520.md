---
kind: review_result
review_id: review-T-P4-037-liuguanyi-20260907T1520
task_id: T-P4-037
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-07T15:10:00-06:00
created_at: 2026-09-07T15:20:00-06:00
inspected_commit: ce3e6e614de2ea6f5276b9bb4803fba6c411e51a
inspected_paths:
  - README.md
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-030-honglianmozun-20260907T1502.md
related_tasks:
  - T-P4-024
  - T-P4-025
  - T-P4-026
  - T-P4-030
  - T-P4-032
  - T-P4-033
integration_status: pending
admission_label: pending
proposed_integration_target: P4.combined_schur_sign_repair_bridge
requested_action: when_a_combined_cross_block_contains_the_corrected_port_map_use_the_exact_interference_margin_identity_if_the_cross_term_is_available_otherwise_replace_the_sign_sensitive_mixed_square_by_the_rational_sign_robust_matrix_Young_envelope_do_not_reuse_an_old_plus_sign_combined_Schur_receipt_from_its_final_PSD_status_alone
---

# T-P4-037 — sign-robust transport for a combined Schur cross block

## 0. Result

`T-P4-030` correctly identifies the remaining sign-sensitive case: an isolated port square is invariant under `R_port=-R_gain`, but a **combined** cross block can change when the port term is added to a fixed baseline block before the Schur square is formed.

This child closes the missing algebraic bridge.  There are two safe lanes:

1. **Interference-aware lane.**  If the mixed baseline/port quadratic is retained, the old plus-sign Schur margin transports to the corrected minus-sign margin by one exact identity.  This gives a necessary-and-sufficient same-diagonal reuse test and a minimal additive-slack repair.
2. **Interference-free fallback.**  If the mixed term was not retained, a rational matrix Young inequality gives one sign-robust upper envelope for both `C0+Cport` and `C0-Cport`, while preserving the anisotropic matrix quadratic instead of collapsing immediately to a scalar Frobenius norm.

No source, interval, solver, Lean, coverage, or admission claim is made here.

---

## 1. Setup and the exact sign-difference identity

Work over finite-dimensional real vectors.  Let

```text
H = H^T >= 0,
C0 : X -> Y,
Cp : X -> Y.
```

For the current P4 sign repair, interpret `Cp` as the cross-block contribution written using the historical positive map `R_gain`; hence

```text
historical combined block : C_plus  = C0 + Cp,
physical combined block   : C_minus = C0 - Cp.             (1.1)
```

Define the three symmetric quadratic matrices

```text
A0 := C0^T H C0,
Ap := Cp^T H Cp,
X  := C0^T H Cp + Cp^T H C0.                               (1.2)
```

and

```text
Q_plus  := C_plus^T  H C_plus,
Q_minus := C_minus^T H C_minus.                            (1.3)
```

Direct expansion gives

```text
Q_plus  = A0 + Ap + X,
Q_minus = A0 + Ap - X,                                    (1.4)
```

therefore

```text
Q_minus - Q_plus = -2 X.                                  (1.5)
```

This is the exact amount by which the Schur quadratic changes after correcting the port sign.

A useful corollary is the exact orthogonality criterion

```text
Q_minus = Q_plus
    <=> X = 0.                                            (1.6)
```

Thus the old combined certificate is genuinely sign-invariant not merely when the port is isolated, but also when the baseline and port cross blocks are `H`-orthogonal in the symmetric sense `X=0`.

---

## 2. Exact transport of an existing Schur margin

Let `D=D^T` be the diagonal/top-left budget against which the combined Schur term is charged.  Define

```text
M_plus  := D - Q_plus,
M_minus := D - Q_minus.                                   (2.1)
```

Using (1.5),

```text
M_minus = M_plus + 2 X.                                   (2.2)
```

This is the key adapter identity.

Consequently, **for the same fixed budget `D`**,

```text
D - Q_minus >= 0
    <=> M_plus + 2 X >= 0.                                (2.3)
```

So an old plus-sign PSD result by itself is not the right reusable object.  The reusable interface is the pair

```text
(old margin M_plus, mixed interference X).                (2.4)
```

Several immediate bridge lemmas follow.

### 2.1 Free reuse under favorable interference

If

```text
M_plus >= 0,
X >= 0,                                                   (2.5)
```

then

```text
M_minus >= 0.                                             (2.6)
```

Thus a positive-semidefinite mixed interference means the physical minus sign can only improve the old plus-sign Schur margin.

### 2.2 Same-budget reuse from a lower interference bound

Suppose a symmetric `Delta>=0` satisfies

```text
X >= -Delta                                               (2.7)
```

and the old certificate has explicit matrix margin

```text
M_plus >= 2 Delta.                                        (2.8)
```

Then (2.2) gives

```text
M_minus >= 2 Delta - 2 Delta = 0.                         (2.9)
```

This is a useful fail-closed replacement for a blanket statement that the old combined Schur receipt is unchanged.

### 2.3 Minimal additive-budget repair from the same interference bound

If one only has

```text
M_plus >= 0,
X >= -Delta,
Delta >= 0,                                               (2.10)
```

then increasing the Schur budget from `D` to `D+2 Delta` is enough:

```text
(D + 2 Delta) - Q_minus
 = M_plus + 2 (X + Delta)
 >= 0.                                                    (2.11)
```

The coefficient `2` is forced by the exact sign-difference (1.5), not by a loose triangle inequality.

---

## 3. Why some extra mixed information is mathematically necessary

There is no implication

```text
D - Q_plus >= 0  ==>  D - Q_minus >= 0                   (3.1)
```

without information about `X` or separate control of `A0,Ap`.

A one-dimensional exact counterexample is

```text
H=1,
C0=1,
Cp=-1,
D=0.                                                      (3.2)
```

Then

```text
Q_plus  = (1 + (-1))^2 = 0,
Q_minus = (1 - (-1))^2 = 4.                              (3.3)
```

Hence the old plus-sign certificate is exact with zero margin,

```text
D-Q_plus=0,                                               (3.4)
```

while the corrected minus-sign certificate fails maximally:

```text
D-Q_minus=-4.                                             (3.5)
```

Therefore a final boolean/PSD status for the old combined block cannot be a typed source for the corrected sign.  One must retain either the mixed interference or the separated baseline/port quadratic charges.

---

## 4. Sign-robust matrix Young fallback with no square roots

Suppose the old combined receipt did not retain `X`, but the separated even quantities

```text
A0 = C0^T H C0,
Ap = Cp^T H Cp                                            (4.1)
```

are available.  Then there is a single rational certificate that works for **both** signs.

For any rational `theta>0` and either `s=+1` or `s=-1`, set

```text
Q_s := (C0 + s Cp)^T H (C0 + s Cp).                       (4.2)
```

Then

```text
Q_s <= (1+theta) A0 + (1+1/theta) Ap.                    (4.3)
```

The important source-facing form is division-free:

```text
theta Q_s
 <= theta(1+theta) A0 + (1+theta) Ap.                    (4.4)
```

Indeed, subtracting the left side from the right side gives exactly

```text
theta(1+theta)A0 + (1+theta)Ap - theta Q_s
 = theta^2 A0 + Ap - s theta X
 = (theta C0 - s Cp)^T H (theta C0 - s Cp)
 >= 0.                                                    (4.5)
```

Thus no square root, spectral norm, floating diagonalization, or sign-specific mixed coefficient is required.  If `theta` and all matrix entries are rational, (4.4) is an exact-rational PSD target.

For `theta=1`, this becomes the especially simple common envelope

```text
Q_plus  <= 2(A0+Ap),
Q_minus <= 2(A0+Ap).                                     (4.6)
```

The weighted family (4.3) is preferable when the baseline and port charges have very different scales.

### Sharpness for fixed `theta`

The Young envelope is not an arbitrary overcharge.  In one dimension with `H=1`, equality in (4.5) is attained whenever

```text
Cp = s theta C0.                                         (4.7)
```

So for a fixed `theta`, the coefficients in (4.3) cannot both be uniformly decreased using only the separated quadratic information `A0,Ap`.

---

## 5. Consumer form that preserves anisotropy

Assume source/earlier leaves provide matrix upper bounds

```text
A0 <= P0,
Ap <= Pp.                                                 (5.1)
```

Then for either sign,

```text
Q_s <= (1+theta) P0 + (1+1/theta) Pp.                    (5.2)
```

This is stronger as an interface than first replacing `C0` and `Cp` by scalar Frobenius/operator norms, because the directional structure of `P0` and `Pp` survives into the Schur consumer.

For a fixed vector `x`, the same theorem can be stated without Loewner-order matrix API.  Define

```text
q_H(y) := y^T H y.                                        (5.3)
```

Then

```text
theta q_H(C0 x + s Cp x)
 <= theta(1+theta) q_H(C0 x)
    + (1+theta) q_H(Cp x).                               (5.4)
```

This evaluation-level statement is probably the smallest Lean interface; the matrix-order corollary can be added later if useful.

---

## 6. Exact relation to the corrected P4 port sign

`T-P4-030` fixes

```text
R_port = -R_gain.                                         (6.1)
```

The present theorem should be instantiated only after deciding which object the downstream cross-block symbol denotes.

- If `Cp` is constructed from **historical `R_gain`**, the physical combined block is `C0-Cp`.
- If the source adapter has already constructed `Cp` from **physical `R_port`**, the physical combined block is `C0+Cp`.

Do not apply a second sign flip after a typed adapter has already switched to `R_port`.  This is the sign analogue of the earlier normalization rule: a source-to-consumer coordinate/sign conversion occurs exactly once.

The same point matters for defect-aware O1.  If a defect correction has already been converted to the physical convention upstream, its contribution belongs in `C0` or `Cp` with that physical sign; `T-P4-037` is not a license to negate every term carrying a historical-looking symbol.

---

## 7. Domain / parameter compatibility

All statements above are pointwise algebraic.  For state- or parameter-dependent matrices

```text
H(z), C0(z), Cp(z), D(z),                                 (7.1)
```

the theorem is valid on a domain `Omega` only when the corresponding premises hold on the **same** `Omega`.

In particular:

1. a cellwise bound `X(z)>=-Delta_k` may be used with the old margin only on the same cell;
2. a single global `Delta` may be obtained by a common upper envelope, but must not be assembled from unrelated cells without a valid cover/partition theorem;
3. `theta` may vary by certified cell, but the downstream ledger must preserve that partition if it consumes the sharper cellwise values;
4. none of these algebraic transports establishes trajectory coverage or true-DH/source equality.

---

## 8. Minimal theorem statements for Lean / checker

I recommend the following small leaves, in this order.

### `combined_cross_sign_difference`

For symmetric `H`, prove by `ring`/matrix algebra:

```text
Qminus - Qplus = -2 * X.                                 (8.1)
```

An evaluation-level version for a fixed `x` is enough initially.

### `combined_schur_margin_transport`

With

```text
Mplus  = D-Qplus,
Mminus = D-Qminus,                                        (8.2)
```

prove

```text
Mminus = Mplus + 2*X.                                    (8.3)
```

### `combined_schur_reuse_of_interference_lower_bound`

Premises:

```text
Mplus >= 2*Delta,
X >= -Delta.                                              (8.4)
```

Conclusion:

```text
Mminus >= 0.                                              (8.5)
```

### `combined_schur_additive_repair`

Premises:

```text
Mplus >= 0,
X + Delta >= 0.                                           (8.6)
```

Conclusion:

```text
(D+2*Delta)-Qminus >= 0.                                 (8.7)
```

### `sign_robust_quadratic_young_mul`

For `theta>=0` and `H>=0`, prove directly

```text
theta*q_H(C0*x + s*Cp*x)
 <= theta*(1+theta)*q_H(C0*x)
    + (1+theta)*q_H(Cp*x),                               (8.8)
```

for the two concrete signs separately if that keeps the Lean API simpler.  The proof target after expansion is exactly

```text
q_H(theta*C0*x - s*Cp*x) >= 0.                           (8.9)
```

The unmultiplied rational corollary can require `theta>0`.

---

## 9. Integration recommendation

For any P4 combined-Schur/S-lemma artifact affected by the `R_gain -> R_port=-R_gain` repair, do **not** rerun or discard it blindly.  Classify it by what evidence it retained:

```text
A. retained M_plus and X
   -> use the exact margin identity M_minus=M_plus+2X;

B. retained separated A0 and Ap but not X
   -> use the sign-robust rational matrix Young envelope;

C. retained only final boolean/PSD status of Q_plus
   -> insufficient for sign transport; keep pending and regenerate a typed
      cross/interference or separated-square witness.
```

This reduces the sign repair to a small exact algebraic adapter instead of a wholesale numerical recomputation whenever the right intermediate witness still exists.

---

## 10. Open boundaries

Still open and intentionally untouched:

- identifying the concrete combined cross block(s) in current P4/S-lemma artifacts;
- proving that their `Cp` is actually induced by the same-key physical `R_port`/historical `R_gain` pair;
- exact-real / Float64 source binding of `C0`, `Cp`, `H`, and any interference enclosure `Delta`;
- cell/domain/trajectory coverage;
- Lean compilation, axiom inspection, comparator receipt, and registry admission.

`T-P4-037` is therefore a **pending mathematical/interface child**, not P4/M4 closure.
