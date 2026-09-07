---
kind: review_result
review_id: review-T-P5-029-kuangmanmozun-20260907T1152
task_id: T-P5-029
source_agent: 狂蛮魔尊
agent: 狂蛮魔尊
claimed_at: 2026-09-07T11:45:00-06:00
created_at: 2026-09-07T11:52:00-06:00
inspected_commit: 15672d6f25c6098d681d9ab8b26a45b89b95bec3
continuation_of:
  - review-T-P5-026-guyuefangyuan-20260907T1031
  - T-P5-026-Kpath-interface
  - review-T-P5-028-liuguanyi-20260907T1112
related_reviews:
  - review-T-P5-025-liuguanyi-20260907T1020
  - review-T-P5-027-kuangmanmozun-20260907T1044
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_a_source_independent_spn_certificate_transport_lemma_for_nonnegative_gain_increments_and_rank_one_parameter_corrections_without_recomputing_existing_psd_witnesses
---

# T-P5-029 — reuse an SPN certificate under a nonnegative `K_path` increment

## 0. Result in one sentence

The new `T-P5-026-Kpath-interface` correctly says that an actual component gain may be replaced by any componentwise larger nonnegative gain before the 18-cone/SPN consumer.  The next useful question is whether a previously found SPN certificate for a base gain must be recomputed from scratch when the gain is enlarged, for example by the moving-frame correction

```text
K_eff = K0 + kappa tensor gamma
```

from `T-P5-028`.

It does **not** need to be recomputed if the old entrywise-nonnegative SPN slack is large enough.  On every physical feasible cone, any nonnegative gain increment produces an **entrywise-nonnegative quadratic correction in the cone coordinates**.  Therefore that correction can be subtracted directly from the old `N_C` part of an SPN decomposition while leaving the PSD part `S_C` and its LDL/kernel witness unchanged.

For a rank-one increment this charge has an explicit outer-product formula.  The resulting check is division-free, rational when the inputs are rational, and consists only of entrywise inequalities.  Failure of this cheap update is not a counterexample: it only means the fixed `N_C` slack is insufficient and one must recompute/split the SPN witness or fall back to another consumer.

This is source-independent inequality mathematics.  It does not supply a concrete `K_path`, `kappa`, `gamma`, source/Jacobian/Float64 semantics, P8 coverage, or registry admission.

---

## 1. Existing exact consumer and notation

Use the same P5 state and force ordering as `T-P5-025/026`:

```text
z = (x4,x5,y4,y5)^T in R^4,
Lz = (x4+y4, x5+y5)^T in R^2.
```

For a nonnegative component gain `K in R_{>=0}^{2 x 4}`, define the direct absolute envelope

```text
F_K(z) := |Lz|^T K |z|.                                (1)
```

The source-facing component contract is

```text
|r_a| <= sum_k K[a,k] |z_k|.                           (2)
```

Then

```text
|(Lz)^T r| <= F_K(z).                                   (3)
```

`T-P5-026` covers `R^4` by the 36 physical product cones, paired into 18 global-sign representatives.  Fix one physical cone `C` and write its nonnegative coordinates as

```text
z = T_C u,

u >= 0 componentwise.                                  (4)
```

Because the cone fixes the signs of all four state coordinates and both channel sums, there are exact nonnegative matrices

```text
A_C in R_{>=0}^{4 x 4},
B_C in R_{>=0}^{2 x 4}                                 (5)
```

such that on this cone

```text
|T_C u|   = A_C u,
|L T_C u| = B_C u.                                     (6)
```

For the six one-channel charts these matrices have only integer `0/1` entries; the theorem below only needs entrywise nonnegativity and the exact identities (6).

Hence

```text
F_K(T_C u)
 = (B_C u)^T K (A_C u).                                (7)
```

Let the frozen dissipation be `Q(z)` and let `mu` be the relative power budget.  A cone gap matrix `H_C(K)` represents

```text
mu Q(T_C u) - F_K(T_C u) = u^T H_C(K) u.              (8)
```

An SPN witness is

```text
H_C(K) = S_C + N_C,                                    (9)
S_C PSD,
N_C entrywise >= 0.                                    (10)
```

No symmetry assumption on the stored `N_C` is needed for the argument, although a rational checker will normally emit symmetric matrices.

---

## 2. Nonnegative gain increments become nonnegative cone quadratics

Let

```text
E in R_{>=0}^{2 x 4}                                   (11)
```

be any nonnegative gain increment and define

```text
K_plus := K + E.                                       (12)
```

The added absolute-envelope power on cone `C` is exactly

```text
DeltaF_C(E,u)
 := F_{K_plus}(T_C u) - F_K(T_C u)
  = (B_C u)^T E (A_C u).                               (13)
```

Define the unsymmetrized matrix

```text
M_C(E) := B_C^T E A_C                                  (14)
```

and its symmetric quadratic representative

```text
C_C(E) := sym(M_C(E))
        = (M_C(E) + M_C(E)^T)/2.                       (15)
```

### Lemma 2.1 — exact cone correction identity

For every real `u`,

```text
DeltaF_C(E,u) = u^T C_C(E) u.                          (16)
```

### Proof

By (13)-(14),

```text
DeltaF_C(E,u) = u^T M_C(E) u.
```

A scalar quadratic depends only on the symmetric part, so

```text
u^T M_C(E) u
 = u^T ((M_C(E)+M_C(E)^T)/2) u.
```

This is a pure ring identity.  QED.

### Lemma 2.2 — the correction matrix is entrywise nonnegative

Under (5) and (11),

```text
C_C(E)[i,j] >= 0                                       (17)
```

for every `i,j`.

### Proof

Every entry of the unsymmetrized matrix is

```text
M_C(E)[i,j]
 = sum_a sum_k B_C[a,i] E[a,k] A_C[k,j].               (18)
```

Every factor in every summand is nonnegative, hence `M_C(E)[i,j]>=0`.  The same is true of `M_C(E)[j,i]`; their average is therefore nonnegative.  QED.

This is the key structural fact.  A nonnegative gain increment is not generally a PSD perturbation in the original signed state coordinates.  It is, however, an entrywise-nonnegative quadratic charge after passing to the **physical nonnegative cone coordinates**.

---

## 3. Main theorem: charge the old `N_C` slack and keep `S_C` unchanged

From (8) and (16), the new cone gap is

```text
mu Q(T_C u) - F_{K_plus}(T_C u)
 = u^T (H_C(K) - C_C(E)) u.                            (19)
```

Suppose the old SPN witness (9)-(10) satisfies the additional entrywise charge condition

```text
C_C(E)[i,j] <= N_C[i,j]                                (20)
```

for all entries.

Define

```text
N_C_plus := N_C - C_C(E).                              (21)
```

Then (20) gives `N_C_plus>=0` entrywise, while

```text
H_C(K) - C_C(E)
 = S_C + N_C_plus.                                     (22)
```

The PSD matrix `S_C` is unchanged.

### Theorem 3.1 — fixed-SPN nonnegative-gain update

Assume on cone `C`:

```text
H_C(K) = S_C + N_C,
S_C PSD,
N_C >= 0 entrywise,
E >= 0 entrywise,
C_C(E) <= N_C entrywise.                               (23)
```

Then the enlarged gain `K+E` has the SPN certificate

```text
H_C(K+E) = S_C + (N_C-C_C(E)),                         (24)
```

where the first term is the **same PSD witness** and the second term is entrywise nonnegative.

Consequently the old LDL/PSD certificate for `S_C` does not need to be regenerated.

### Proof

Equation (19) gives the exact new gap.  Substitute (9) and rearrange to (22).  PSD of `S_C` is unchanged; (20) gives entrywise nonnegativity of (21).  The existing SPN orthant lemma then proves the new gap is nonnegative for every `u>=0`.  QED.

### Sharpness relative to a fixed decomposition

If one insists on keeping **exactly the same** `S_C` and representing the entire correction by replacing `N_C` with `N_C-C_C(E)`, then (20) is necessary and sufficient for the new `N` part to remain entrywise nonnegative.  Thus (20) is sharp for this zero-recompute update of a fixed SPN decomposition.

It is **not** necessary for the existence of some other SPN decomposition; see Section 7.

---

## 4. Rank-one moving-frame correction

`T-P5-028` gives the exact controlled-parameter-mismatch form

```text
K_eff = K0 + kappa tensor gamma,                        (25)
```

where

```text
kappa in R_{>=0}^2,
gamma in R_{>=0}^4.                                    (26)
```

Set

```text
E := kappa gamma^T.                                    (27)
```

On cone `C`, define

```text
alpha_C := B_C^T kappa  in R_{>=0}^4,
beta_C  := A_C^T gamma  in R_{>=0}^4.                  (28)
```

Then

```text
M_C(E)
 = B_C^T (kappa gamma^T) A_C
 = alpha_C beta_C^T.                                   (29)
```

Therefore the exact symmetric charge is

```text
C_C(E)[i,j]
 = (alpha_C[i] beta_C[j]
    + beta_C[i] alpha_C[j]) / 2.                       (30)
```

The added power factorizes as

```text
DeltaF_C(E,u)
 = (alpha_C dot u)(beta_C dot u).                      (31)
```

Both linear forms are nonnegative on `u>=0`.

### Corollary 4.1 — division-free rank-one SPN slack test

A base SPN witness for `K0` can be reused unchanged on its PSD side if, for every cone entry `i,j`,

```text
alpha_C[i] beta_C[j] + beta_C[i] alpha_C[j]
 <= 2 N_C[i,j].                                        (32)
```

No square root, determinant, eigenvalue, or new LDL factorization is required.

When `kappa`, `gamma`, `A_C`, `B_C`, and `N_C` are rational, (32) is an exact rational checker condition.

This is the natural cheap consumer for the rank-one parameter correction from `T-P5-028`.

---

## 5. A reusable robustness radius for a correction template

Suppose a fixed nonnegative template `E0` is scaled by `t>=0`:

```text
E(t) = t E0.                                            (33)
```

Linearity gives

```text
C_C(E(t)) = t C_C(E0).                                 (34)
```

Hence the fixed-SPN witness survives for every `t` satisfying the finite division-free ledger

```text
t C_C(E0)[i,j] <= N_C[i,j]                             (35)
```

for all entries of all 18 representative cones.

An external rational checker may summarize this as the finite minimum ratio over entries with positive `C_C(E0)[i,j]`, but the formal theorem should consume (35) directly.  Entries with zero correction impose no restriction and no division-by-zero branch is needed.

This gives a concrete notion of an **SPN nonnegative-slack radius** around a certified base component gain.

---

## 6. Composition with the already harvested `K_path` comparison interface

The new result fits immediately after the conditional componentwise interface that has already been harvested.

Let `K_actual` be whatever exact/source-side component gain is eventually justified, and let a checker choose a nonnegative rational upper gain

```text
K_actual <=cw G0 + E.                                  (36)
```

Suppose:

1. `G0` already has the 18 base SPN witnesses;
2. `E>=0` is in the same force/state coordinate ordering;
3. every cone passes the charge inequalities (20), or the rank-one specialization (32).

Then Theorem 3.1 constructs SPN witnesses for `G0+E`, after which the existing componentwise comparison theorem gives

```text
|(Lz)^T r| <= mu Q(z).                                 (37)
```

Thus no exact equality `K_actual=G0+E` is required.  The source lane may safely use a rational componentwise majorant, while the mathematical consumer remains exact.

Two important specializations are:

```text
(a) rationalization / interval widening:
    E = G_upper - G0 >= 0;

(b) T-P5-028 controlled parameter mismatch:
    E = kappa tensor gamma >= 0.                        (38)
```

For common ramp parameter, `gamma=0`, hence `E=0` and the update is free, exactly as T-P5-028 predicts.

---

## 7. Two counterexamples that delimit the theorem

### 7.1 Nonnegative gain increment does NOT imply PSD/Loewner matrix order

Consider one channel with

```text
L = [1 1],
E = [1 0].                                              (39)
```

On the same-sign cone `x>=0,y>=0`, the added absolute-envelope power is

```text
|x+y| * |x|
 = (x+y)x
 = x^2 + xy.                                            (40)
```

Its symmetric matrix in `(x,y)` is

```text
C = [1   1/2
     1/2 0].                                            (41)
```

`C` is entrywise nonnegative, but

```text
det C = -1/4 < 0,                                      (42)
```

and at `v=(1,-2)` one has

```text
v^T C v = -1.                                           (43)
```

So `C` is not PSD.

This rules out the tempting but invalid shortcut

```text
E >= 0 componentwise
  ==> cone correction is PSD
  ==> gap matrices are Loewner-monotone.               (44)
```

The correction is nonnegative only on the physical orthant; that is exactly why it belongs naturally in the `N_C` part of an SPN certificate.

### 7.2 Failure of the `N`-slack test is NOT a counterexample to the enlarged gain

Take in two dimensions

```text
S = I,
N = 0,
C = diag(1/2,0).                                        (45)
```

The cheap condition `C<=N` fails.  Nevertheless

```text
S-C = diag(1/2,1)                                       (46)
```

is still PSD, so the corrected gap has a perfectly valid SPN witness

```text
(S-C) + 0.                                              (47)
```

Therefore a failed entrywise charge test means only

```text
FIXED_N_SLACK_INSUFFICIENT.                             (48)
```

It must not be recorded as non-copositivity, small-gain failure, or a source counterexample.  The checker may then recompute an SPN decomposition, charge part of the correction to PSD slack, or use the T-P5-025 / T-P5-027 fallbacks.

---

## 8. Optional hybrid update theorem

The algebra admits a slightly more general reusable statement.

Suppose the correction matrix is split exactly as

```text
C = C_S + C_N.                                          (49)
```

If

```text
S-C_S is PSD,
N-C_N is entrywise nonnegative,                         (50)
```

then

```text
H-C = (S-C_S) + (N-C_N)                                (51)
```

is again an SPN witness.

This subsumes:

```text
N-only cheap update: C_S=0, C_N=C;
PSD-only update:     C_S=C, C_N=0;
hybrid update:       split the charge.                 (52)
```

The theorem is trivial algebraically but useful architecturally: it prevents a checker from interpreting failure of the cheapest `N`-only test as a mathematical dead end.

For the first implementation I recommend formalizing the `N`-only theorem and the generic split theorem, while leaving any optimization of the split outside the trusted core.

---

## 9. Minimal Lean theorem decomposition

The existing T-P5-026 sidecar already provides `quad`, `IsPSD`, `SPNWitness`, cone cover, and the generic SPN consumer.  The new child can stay small.

### 9.1 `cone_gain_increment_matrix`

Given nonnegative finite matrices `Aabs`, `Babs`, and `E`, define

```text
M := Babs^T * E * Aabs,
C := (M + M^T)/2.
```

Prove

```text
quad C u = dot (Babs*u) (E*(Aabs*u)),
forall i j, 0 <= C i j.                                (53)
```

The proof is finite sums plus `ring`; no spectral API is needed.

### 9.2 `spn_charge_entrywise_increment`

Inputs:

```text
H = S+N,
IsPSD S,
0 <= N entrywise,
0 <= C entrywise,
C <= N entrywise.
```

Conclusion:

```text
H-C = S+(N-C),
IsPSD S,
0 <= N-C entrywise.                                    (54)
```

This is the fixed-witness update theorem.

### 9.3 `rankOne_cone_charge`

For `E[a,k]=kappa[a]*gamma[k]`, prove

```text
M = alpha * beta^T,
alpha = Babs^T*kappa,
beta = Aabs^T*gamma,
C_ij = (alpha_i*beta_j + beta_i*alpha_j)/2.             (55)
```

### 9.4 `spn_charge_rankOne`

Consume (32) directly and return the updated SPN witness.

### 9.5 `spn_charge_split`

Formalize the optional generic split (49)-(51).

### 9.6 Block/P5 wrapper

After the concrete cone-index sidecar exposes the absolute-value maps for its 18 representatives, instantiate (53)-(55) and feed the updated witnesses back to the existing `componentwise_spn_power` consumer.

No new theorem about source calculus, P8 coverage, or ODEs belongs in this sidecar.

---

## 10. Assumptions and interface boundaries

The gain increment theorem is valid only when all compared objects are in the same typed coordinates.

Required mathematical assumptions:

```text
- E is a component-gain increment in the same two generalized-force rows and
  four P5 state columns as the base gain;
- E>=0 componentwise;
- the cone chart supplies exact absolute-value maps A_C,B_C with nonnegative
  entries;
- the old gap identity and SPN decomposition use the same mu,Q,cone chart;
- for the T-P5-028 rank-one specialization, kappa>=0 and gamma>=0 and the
  parameter-control inequality is valid on the same comparison domain.      (56)
```

Still open and explicitly not supplied here:

```text
- concrete source-bound K_path/G0/E/kappa/gamma;
- source/Jacobian or centered-increment validity;
- Float64/controller/solve discontinuous remainder handling;
- any additive bias that does not vanish at z=0;
- proof of common-c or a concrete gamma for parameter mismatch;
- P8 cell/path coverage, ODE continuation, and terminal transfer;
- source hashes/provenance/admission/registry effects.                       (57)
```

A genuine additive execution bias cannot be hidden by choosing a larger homogeneous `E`: at `z=0` every finite component envelope still vanishes.  Such a term remains on the additive/transverse branch.

---

## 11. Recommended next action

When the first concrete rational base `G0` and 18 SPN witnesses arrive, retain the emitted `N_C` matrices instead of discarding them after proving copositivity.  They are a **reusable robustness budget**.

For any later rational widening or `T-P5-028` rank-one parameter correction:

```text
1. build the exact cone charge C_C(E);
2. try the entrywise test C_C(E)<=N_C on all 18 representatives;
3. if PASS, reuse the old PSD/LDL witness verbatim and emit N_C-C_C(E);
4. if FAIL, record FIXED_N_SLACK_INSUFFICIENT and either recompute/split the
   SPN witness or fall back to the global-PSD/scalar consumers.              (58)
```

This is strictly cheaper than blindly rerunning 18 semidefinite searches and is mathematically aligned with the reason SPN was introduced in the first place: physical feasibility is an orthant condition, not global PSD.

Status remains **pending mathematical child**.  Wait for a formalization agent, independent verification by 封不觉, and final integration by 梁智炜.
