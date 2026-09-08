---
kind: review_result
review_id: review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013
task_id: T-P5-054
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T00:05:00-06:00
created_at: 2026-09-08T00:13:00-06:00
claim_commit: a5ae735b4ddfbc40f53ff737a973a35c4d1ea4f3
inspected_commit: 8e327d61ac9de3a70c15952305a1a542d6cdec67
inspected_paths:
  - README.md
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-BRANCHFREE-AFFINE-MAJORANT-liuguanyi-20260907T2312.md
  - agent_review_inbox/review-T-P5-053-honglianmozun-20260907T2350.md
continuation_of:
  - T-P5-BRANCHFREE-AFFINE-MAJORANT
  - T-P5-053
related_tasks:
  - T-P5-045
  - T-P5-051
  - T-P5-052
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a correlation-preserving nominal-model perturbation layer between exact polynomial/Bernstein packets and the existing branch-free affine-energy consumer; allow either exact correlated determinant-correction bounds or the weaker entry-radius fallback; do not independently intervalize determinant factors
---

# T-P5-054 — correlation-preserving matrix perturbation bridge for approximate source packets

## 0. Question

The current P5 chain now has two useful exact mathematical endpoints:

1. `T-P5-BRANCHFREE-AFFINE-MAJORANT` reduces a fixed positive energy charge `kappa` to two correlated scalar inequalities.
2. `T-P5-052/053` can certify exact one-dimensional or tensor polynomial remainders on a whole cell by Bernstein controls.

The missing source-to-math seam is what to do when the deployed/source packet is not itself an exact polynomial, but an exact polynomial or rational nominal model plus a rigorously bounded approximation error.

The wrong interface is to intervalize the factors of

```text
4*p*s - sigma^2
```

and

```text
s*b4^2 - sigma*b4*b5 + p*b5^2
```

separately. That destroys the same signed correlation which motivated T-P5-045 and the branch-free gate.

This review gives a smaller invariant interface: form the **branch-free 2x2 symmetric packet first**, then transport a correlated matrix perturbation through exact trace/determinant identities.

The trusted core is polynomial, division-free, square-root-free, and source-independent.

---

## 1. The scaled branch-free matrix packet

For `kappa>0`, define directly in the scaled `sigma=k45+k54` convention

```text
G(p,s,sigma,b4,b5;kappa)
 := [[4*kappa*p - b4^2,       2*kappa*sigma - b4*b5],
     [2*kappa*sigma - b4*b5,  4*kappa*s - b5^2]].
```

Write its entries as

```text
g11 = 4*kappa*p - b4^2,
g22 = 4*kappa*s - b5^2,
g12 = 2*kappa*sigma - b4*b5.
```

The two old branch-free remainders are

```text
Rtr
 = 4*kappa*(p+s) - (b4^2+b5^2),

Rdet
 = kappa*(4*p*s-sigma^2)
   - (s*b4^2 - sigma*b4*b5 + p*b5^2).
```

Then, exactly,

```text
trace(G) = Rtr,                                           (1.1)

det(G)   = 4*kappa*Rdet.                                 (1.2)
```

Equation (1.2) is the cancellation-preserving form of the old determinant gate. No inverse or division appears.

Because `kappa>0`,

```text
trace(G)>=0 and det(G)>=0
```

are exactly the two scalar conditions needed by the existing 2x2 branch-free consumer.

---

## 2. Exact 2x2 perturbation identity

Let the actual matrix be

```text
G = Ghat + E,
```

where

```text
Ghat = [[a,m],[m,c]],
E    = [[e11,e12],[e12,e22]].
```

### Theorem T-P5-054-A — exact determinant update

The determinant difference is the ring identity

```text
det(G)-det(Ghat)
 = c*e11 + a*e22 - 2*m*e12
   + e11*e22 - e12^2.                                   (2.1)
```

Also

```text
trace(G)-trace(Ghat) = e11+e22.                          (2.2)
```

### Proof

Expand

```text
(a+e11)(c+e22) - (m+e12)^2
```

and subtract `a*c-m^2`.

This identity is the main interface theorem. It says that a source checker may keep the full correlation of the approximation error by enclosing the **single correction polynomial/expression**

```text
Cdet
 := c*e11 + a*e22 - 2*m*e12
    + e11*e22 - e12^2.                                  (2.3)
```

instead of separately bounding determinant factors.

If it proves

```text
Cdet >= -delta_det,
```

then immediately

```text
det(G) >= det(Ghat)-delta_det.                           (2.4)
```

Likewise an exact lower bound

```text
e11+e22 >= -delta_tr
```

gives

```text
trace(G) >= trace(Ghat)-delta_tr.                        (2.5)
```

No positivity assumption on `Ghat` is needed for (2.1)-(2.5); they are pure transport identities.

---

## 3. Exact entry-radius fallback

Sometimes the source layer cannot enclose `Cdet` directly and only has entrywise symmetric error radii.

Assume nonnegative rational caps

```text
|a|   <= M11,
|c|   <= M22,
|m|   <= M12,

|e11| <= eta11,
|e22| <= eta22,
|e12| <= eta12.
```

### Theorem T-P5-054-B — determinant lower bound from entry radii

Define

```text
Pdet
 := M22*eta11
    + M11*eta22
    + 2*M12*eta12
    + eta11*eta22
    + eta12^2.                                           (3.1)
```

Then

```text
det(G) >= det(Ghat)-Pdet.                               (3.2)
```

Also

```text
trace(G) >= trace(Ghat)-(eta11+eta22).                  (3.3)
```

### Proof

From (2.1), termwise

```text
c*e11       >= -M22*eta11,
a*e22       >= -M11*eta22,
-2*m*e12    >= -2*M12*eta12,
e11*e22     >= -eta11*eta22,
-e12^2      >= -eta12^2.
```

Summing proves (3.2). Equation (3.3) is immediate from (2.2).

This is intentionally a **fallback**. The direct `Cdet` route in section 2 is always at least as correlation-aware.

---

## 4. Nominal polynomial reserve -> actual branch-free gate

Suppose an exact nominal polynomial/Bernstein packet certifies, uniformly on a cell,

```text
trace(Ghat) >= Treserve,
det(Ghat)   >= Dreserve.                                 (4.1)
```

There are now two valid consumers.

### Theorem T-P5-054-C1 — direct correlated correction consumer

If uniformly on the same cell

```text
e11+e22 >= -Tloss,
Cdet     >= -Dloss,
Treserve >= Tloss,
Dreserve >= Dloss,
```

then

```text
trace(G)>=0,
det(G)>=0.                                               (4.2)
```

### Theorem T-P5-054-C2 — entry-radius consumer

If the hypotheses of section 3 hold uniformly and

```text
Treserve >= eta11+eta22,
Dreserve >= Pdet,                                        (4.3)
```

then again (4.2) holds.

By (1.1)-(1.2) and `kappa>0`, the actual source packet satisfies

```text
Rtr>=0,
Rdet>=0,
```

and therefore the existing branch-free theorem yields, for every real `x,y`,

```text
-(p*x^2 + sigma*x*y + s*y^2)
-(b4*x+b5*y)
<= kappa.                                                (4.4)
```

This is the desired cross-layer bridge:

```text
exact nominal polynomial/Bernstein reserve
    + correlated model-error theorem
    -> actual branch-free energy charge.
```

The nominal and error statements must be for the **same physical point/cell/source key**. A nominal reserve from one cell and an error bound from another cannot be composed.

---

## 5. From source-variable errors to a matrix-error packet

The previous sections deliberately consume `Ghat` and `E`. For source checkers that naturally approximate the five signed quantities, there is a second exact bridge.

Write

```text
p     = phat     + ep,
s     = shat     + es,
sigma = sigmahat + esigma,
b4    = b4hat    + e4,
b5    = b5hat    + e5.
```

Then `E=G-Ghat` has the exact entries

```text
e11 = 4*kappa*ep
       - 2*b4hat*e4 - e4^2,                              (5.1)

e22 = 4*kappa*es
       - 2*b5hat*e5 - e5^2,                              (5.2)

e12 = 2*kappa*esigma
       - b4hat*e5 - b5hat*e4 - e4*e5.                   (5.3)
```

These are again ring identities.

Assume `kappa>=0` and exact rational bounds

```text
|ep|     <= dp,
|es|     <= ds,
|esigma| <= dsigma,
|e4|     <= d4,
|e5|     <= d5,

|b4hat| <= B4,
|b5hat| <= B5,
```

with all radii/caps nonnegative. Then a valid matrix-error radius packet is

```text
eta11 = 4*kappa*dp + 2*B4*d4 + d4^2,                    (5.4)
eta22 = 4*kappa*ds + 2*B5*d5 + d5^2,                    (5.5)
eta12 = 2*kappa*dsigma
        + B4*d5 + B5*d4 + d4*d5.                        (5.6)
```

Thus a Taylor/rational/interval source approximation can remain completely separate from the Lyapunov proof: it only needs to produce signed nominal quantities plus exact error radii, after which (5.1)-(5.6) and section 3 are deterministic algebra.

However, if the source layer can form `Cdet` before taking absolute values, section 2 is preferable.

---

## 6. Why the direct correlated correction must remain available near singularity

The entry-radius fallback is sound but can be arbitrarily conservative on a rank-deficient correlated family.

Consider the exact family

```text
G(t) = [[1, t],
        [t, t^2]]
     = [1,t]^T [1,t].                                   (6.1)
```

For every real `t`,

```text
det(G(t))=0
```

and `G(t)` is PSD of rank one (except the trivial interpretation at no special point is needed).

Take the nominal point

```text
Ghat = G(0) = [[1,0],[0,0]],
```

so

```text
E(t) = [[0,t],[t,t^2]].
```

The exact determinant correction in (2.1) is

```text
Cdet = 1*t^2 - t^2 = 0.                                 (6.2)
```

Hence the direct correlated route loses **zero** determinant reserve.

But on `|t|<=eps`, independent absolute radii give

```text
eta11=0,
eta12=eps,
eta22=eps^2,
M11=1,
M12=M22=0.
```

The generic penalty (3.1) becomes

```text
Pdet = 2*eps^2.                                          (6.3)
```

Since `det(Ghat)=0`, the entry-radius consumer cannot certify the family for any `eps>0`, even though the exact determinant is identically zero.

This is not a failure of the branch-free theorem. It is an **interface-information loss** caused by forgetting the relation

```text
e22 = e12^2
```

in this example.

Therefore the source contract should support two lanes:

```text
preferred: direct correlated lower bound on Cdet;
fallback:  independent entry radii + Pdet.
```

Near a singular PSD boundary, the first lane can be essential.

---

## 7. Relation to T-P5-053 tensor Bernstein

T-P5-053 proves that exact tensor Bernstein controls can certify a polynomial remainder over a whole rational box. The present child says what the polynomial should certify when the actual source is only approximately represented.

There are two useful placements.

### Placement A — Bernstein on the nominal reserves

Use Bernstein to prove exact polynomial lower bounds

```text
trace(Ghat) >= Treserve,
det(Ghat)   >= Dreserve,
```

then use a non-polynomial/source error enclosure only for `E` or `Cdet`.

### Placement B — Bernstein on the correlated correction itself

If `Cdet` admits an exact polynomial or polynomial lower enclosure, certify

```text
Cdet + Dloss >= 0
```

directly with Bernstein controls. This preserves more correlation than converting `E` to independent radii.

In both placements, outward rounding should occur **after** forming the signed matrix/correction expression. It should not be applied separately to the determinant factors and then recombined.

---

## 8. Minimal theorem statements for formalization

A small Lean package can avoid matrix APIs entirely by representing a symmetric 2x2 packet as three scalars.

Suggested theorems:

```text
branchfree_packet_trace_identity
```

Prove (1.1).

```text
branchfree_packet_det_identity
```

Prove (1.2).

```text
det2_add_exact
```

Prove (2.1) for six real scalars.

```text
det2_add_lower_of_abs_bounds
```

Prove (3.2) from nonnegative absolute-value caps.

```text
branchfree_packet_error_entries
```

Prove (5.1)-(5.3).

```text
branchfree_packet_error_abs_bounds
```

Prove (5.4)-(5.6).

```text
branchfree_of_nominal_correlated_reserve
```

Consume (4.1) plus `Tloss/Dloss` and the existing branch-free theorem.

```text
rank_one_correlated_error_regression
```

Formalize (6.1)-(6.3) so a future checker cannot silently replace the direct `Cdet` lane with independent entry radii near singularity.

The algebraic identities are valid over an ordered commutative ring where appropriate; the final `kappa>0` branch-free consumption is naturally over `ℝ`.

---

## 9. Typed source contract suggested by the mathematics

A future source packet should keep the following fields distinct:

```text
source_key / cell_key / coordinate_convention,
kappa,
nominal_g11, nominal_g12, nominal_g22,
nominal_trace_reserve,
nominal_det_reserve,
```

and then either

```text
correlated_trace_error_lower,
correlated_det_correction_lower,
```

or the weaker fallback

```text
eta11, eta12, eta22,
M11, M12, M22.
```

If the source approximation is expressed before forming `G`, it may additionally expose

```text
dp, ds, dsigma, d4, d5,
B4, B5,
```

which deterministically generate the matrix radii by (5.4)-(5.6).

The important typed boundary is that `sigma` remains signed. An adapter that first replaces the two cross Jacobian entries by independent absolute values cannot reconstruct this packet without losing the skew/correlation structure already identified in T-P5-041/T-P5-045.

---

## 10. What this closes and what it does not

This review proves the **source-independent mathematical transport** from a nominal correlated 2x2 branch-free packet plus certified model error to the actual branch-free affine-energy gate.

It does not prove any of the following:

- that deployed `forceError`, DH, controller, finite-difference, solve, or libm expressions admit the assumed nominal/error split;
- a concrete Taylor or rational enclosure for trigonometric terms;
- Float64/outward-rounding correctness;
- a real same-key cell packet for `p,s,sigma,b4,b5`;
- an authoritative `kappa` across physical cells;
- first-exit, trajectory, branch, or P8 coverage;
- pinned Lean compilation or axiom status of the proposed theorems;
- comparator/provenance/admission/registry promotion.

Admission remains **pending mathematical/interface child**.

The main new obstruction is equally explicit: near a singular correlated family, independent entry-radius errors may be insufficient even when the actual determinant is identically nonnegative. In that regime, the source layer must preserve a direct lower bound on the correlated determinant correction `Cdet` (or on the complete `Rdet`) rather than force every approximation through absolute entry boxes.
