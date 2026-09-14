---
kind: review_result
review_id: review-T-P5-137-ellipsoidal-knot-reset-multiplier-honglianmozun-20260909T0811Z
task_id: T-P5-137-ELLIPSOIDAL-KNOT-RESET-MULTIPLIER
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T08:11:00Z
claim_commit: 5fe61fdce00c2bd5bcfe82dc4333f57929013d0d
inspected_commit: 200e1928ef0d0264cd911ec1aa44dac815ec5b61
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-132-BOUNDED-CELL-KNOT-RESET-honglianmozun-20260909T0658Z.md
    commit: a521dbad9a0c1dac213ed61e745dff9c2c54cc4f
  - path: agent_review_inbox/review-T-P5-135-PHYSICAL-SECANT-RADIUS-NO-CURVATURE-TAX-kuangmanmozun-20260909T0743Z.md
    commit: 31f635c582323ac71285d878c50674e94229941e
  - path: agent_review_inbox/review-T-P5-136-TANGENT-TO-PHYSICAL-COERCIVITY-BRIDGE-liuguanyi-20260909T0801Z.md
    commit: 865615dd454c608b79a4fc3eb2f6fcef32c508bf
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: preserve_full_signed_physical_quadratic_reset_packet_and_check_scalar_multiplier_block_psd_before_scalarizing_to_A_B_R
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact quadratic-form / PSD / scalar-multiplier algebra only
exit_code: n/a
---

# T-P5-137 — ellipsoidal knot-reset multiplier

## 0. Narrow seam and non-overlap

T-P5-132 gives a sharp bounded-cell reset consumer after the physical reset has already been scalarized to

`W_+ - kappa W_- <= p - A Qx + C`,

with `p^2 <= B Qx` and `0 <= Qx <= R`. T-P5-135/136 then improve how a nonlinear chart supplies the physical radius and physical coercivity needed by that scalar consumer.

There is still one loss before those consumers: a producer may actually know the **signed quadratic reset geometry**

`b^T x - x^T H x + C`

on an anisotropic physical ellipsoid, but replacing it by one scalar lower curvature `A`, one scalar dual constant `B`, and one scalar radius `R` destroys directional information. The loss can be arbitrarily large when a weak/negative quadratic direction is nearly orthogonal to the linear reset covector.

This child keeps the full matrices and derives a one-scalar multiplier / block-PSD certificate. It does not replace T-P5-135 or T-P5-136: those remain source/chart bridges. It is a stronger downstream reset consumer whenever the full signed physical packet is available.

No actual source binding, same-cell coverage, Float64/controller semantics, P8 flowpipe, Lean/kernel receipt, admission, registry promotion, or independent verification is claimed.

---

## 1. Physical ellipsoid and reset packet

Let `G` be symmetric positive definite and let `R>0`. Define the physical same-cell ellipsoid

**(1.1)** `E_R := { x : x^T G x <= R }`.

Assume the actual knot/reset algebra supplies, on this same cell,

**(1.2)**

`W_+(x) - kappa W_-(x) <= b^T x - x^T H x + C`.

Only the symmetric part of `H` matters. Indeed,

`x^T H x = x^T ((H+H^T)/2) x`,

because `x^T(H-H^T)x=0`. Hence below `H` may be assumed symmetric without loss of information.

The target is a certified reset floor `E` such that

**(1.3)** `W_+(x) <= kappa W_-(x) + E`

for every `x in E_R`.

Equivalently, it is enough to prove

**(1.4)**

`f_E(x) := x^T H x - b^T x + E - C >= 0`

whenever `x^T G x <= R`.

---

## 2. Main block-PSD multiplier theorem

Choose a scalar multiplier `tau >= 0` and define the augmented symmetric matrix

**(2.1)**

`M(tau,E) := [[ H + tau G,   -b/2 ],`

`             [ -b^T/2,  E-C-tau R ]]`.

### Theorem A — ellipsoidal reset from one block PSD gate

If

**(2.2)** `tau >= 0`,

and

**(2.3)** `M(tau,E) >= 0`  (positive semidefinite),

then for every `x` satisfying `x^T G x <= R`,

**(2.4)** `W_+(x) <= kappa W_-(x) + E`.

### Exact proof

Let `z := (x,1)`. Then

`z^T M(tau,E) z`

` = x^T H x - b^T x + E-C + tau(x^T G x-R)`

` = f_E(x) + tau(x^T G x-R)`.

By (2.3), the left side is nonnegative. By `tau>=0` and `x^T G x-R<=0`,

`-tau(x^T G x-R) >= 0`.

Therefore

`f_E(x)`

` = z^T M(tau,E)z - tau(x^T G x-R)`

` >= 0`.

This is exactly (1.4), which inserted into (1.2) gives (2.4).

The trusted proof uses only matrix/quadratic-form nonnegativity, multiplication, addition, and order. There is no inverse, square root, generalized eigenvalue, or coordinatewise norm in the theorem statement.

---

## 3. Direct dwell/headroom consumer

Often the hybrid/dwell layer already supplies a maximum admissible knot charge `J` rather than asking for a separately named `E`. Then no intermediate reset-floor variable is needed.

Define

**(3.1)**

`M_J(tau) := [[ H + tau G,   -b/2 ],`

`             [ -b^T/2,  J-C-tau R ]]`.

If

**(3.2)** `tau>=0`,

**(3.3)** `M_J(tau)>=0`,

then directly

**(3.4)** `W_+ - kappa W_- <= J`

throughout the physical cell.

Thus the existing reset/dwell capacity from T-P5-131/132 can consume the full matrix packet by checking one scalar `tau` plus one exact PSD certificate.

---

## 4. Why this is the natural one-constraint multiplier

Write the cell slack as

`g(x) := R - x^T G x`.

Then the desired implication is

`g(x)>=0  =>  f_E(x)>=0`.

The block theorem is exactly the certificate

**(4.1)** `f_E(x) - tau g(x) >= 0` for every `x`, with `tau>=0`.

Since `G>0` and `R>0`, the cell has a strict interior point: at `x=0`, `g(0)=R>0`. Under the classical real one-quadratic-constraint S-lemma, this Slater condition makes the multiplier form **lossless**:

**(4.2)**

`f_E(x)>=0` on `E_R`

if and only if there exists a real `tau>=0` for which `M(tau,E)>=0`.

For the trusted repository path, only the forward implication in Theorem A is needed and was proved directly above. Therefore no external duality theorem needs to be trusted by the checker. The S-lemma is only the mathematical explanation that, over the reals and with strict ellipsoid interior, there is no intrinsic loss in searching a single scalar multiplier before scalarizing the geometry.

A useful fail-closed interpretation follows: under the stated Slater hypotheses, if **no real** `tau>=0` makes the block PSD for a proposed `E`, then the proposed reset level is genuinely false for the quadratic envelope; some point of the ellipsoid violates it. This is not merely a weakness of Young/Cauchy tuning.

---

## 5. Exact-rational checker packet

When `G,H,b,C,R,E,tau` are rational, (2.2)-(2.3) are an exact rational certificate.

A checker may verify the symmetric PSD matrix using, for example:

1. all principal minors;
2. an exact rational `P^T L D L^T P` decomposition with nonnegative diagonal pivots and symmetric permutation;
3. any already-supported exact rational PSD witness.

No square root is necessary. The multiplier enters the block **affinely**, so an offline search can optimize or scan `tau`, while the trusted consumer receives only the chosen rational witness and its exact PSD evidence.

For interpretation only, if `H+tau G` is positive definite, the block Schur complement says

`E >= C + tau R + (1/4) b^T (H+tau G)^(-1) b`.

The first term `tau R` pays for relaxing negative/weak curvature using the bounded cell; the final term pays for the linear reset covector in the resulting metric. This inverse formula is not needed by the checker.

### Rational-boundary caveat

The real lossless S-lemma does **not** imply that an optimal boundary multiplier must be rational when the source data are rational. Therefore the repository must not silently replace “there exists a real `tau`” by “there exists an exact rational `tau`” at a zero-margin optimum.

With strict PSD/slack, rational density gives a nearby rational multiplier and a slightly enlarged rational `E`. At an exact boundary where only an irrational multiplier works, either:

- allow an arbitrarily small rational reset slack and certify a nearby rational multiplier; or
- use a separate exact algebraic/elimination certificate.

The present child claims exactness only for the provided multiplier witness; it does not claim every real boundary optimum has a rational witness.

---

## 6. Exact recovery of the T-P5-132 negative-curvature bounded-cell example

Take the one-dimensional packet

`G=1`,

`R=1/16`,

`H=-2`,

`b=1`,

`C=1/12`.

Then the reset term is

`b x - H x^2 + C = x + 2x^2 + 1/12`

on `|x|<=1/4`.

Its exact maximum is at `x=1/4`:

`1/4 + 2*(1/16) + 1/12`

` = 1/4 + 1/8 + 1/12`

` = 11/24`.

Set

**(6.1)** `E=11/24`, `tau=4`.

Then

`H+tau G = -2+4 = 2`,

and

`E-C-tau R`

` = 11/24 - 1/12 - 4/16`

` = 1/8`.

Therefore

**(6.2)**

`M(4,11/24) = [[2,-1/2],[-1/2,1/8]]`.

Its diagonal entries are nonnegative and

`det M = 2*(1/8) - (1/2)^2 = 0`.

Hence it is PSD, exactly at the sharp boundary. The multiplier certificate therefore reproduces the T-P5-132 finite-cell rescue of negative global curvature with **zero additional slack**.

The role of the multiplier is transparent here: `H=-2` is globally destabilizing, but adding `tau G=4` produces positive quadratic curvature `2` while charging exactly `tau R=1/4` against the finite physical radius.

---

## 7. Strict anisotropic improvement over scalarization

The full matrix packet can be dramatically stronger than replacing `H` by its worst scalar direction and `b` by one global dual constant.

Take in two dimensions

`G=I`, `R=1`,

`H=diag(-1,100)`,

`b=(0,10)`,

`C=0`.

The reset envelope is

**(7.1)** `phi(x1,x2)=x1^2 + 10 x2 - 100 x2^2`

on `x1^2+x2^2<=1`.

A scalar reduction sees only

`H >= -I`

and

`(b^T x)^2 <= 100 (x^T x)`.

Those two independent facts permit the crude worst-case combination

`phi <= 10 + 1 = 11`.

But the bad quadratic direction `x1` and the linear covector direction `x2` are orthogonal, so they cannot simultaneously saturate.

Choose

**(7.2)** `tau=1`, `E=126/101`.

Then

`H+tau I = diag(0,101)`,

and

`E-tau R = 126/101 - 1 = 25/101`.

The augmented matrix is

`M =`

`[[0,   0,       0],`

` [0, 101,      -5],`

` [0,  -5, 25/101]]`.

The active `2x2` block has determinant

`101*(25/101)-25 = 0`

and nonnegative diagonal entries, so `M>=0`. Hence

**(7.3)** `phi(x)<=126/101` on the unit disk.

This value is exact. For fixed `x2`, the positive `x1^2` term is maximized at the boundary `x1^2=1-x2^2`, giving

`phi <= 1 + 10 x2 - 101 x2^2`.

Complete the square algebraically:

`126/101 - (1 + 10x2 - 101x2^2)`

` = (101 x2 - 5)^2 / 101 >= 0`,

with equality at

`x2=5/101`, `x1^2=1-25/10201`.

Thus the full ellipsoidal multiplier gives the exact reset floor

`126/101 ~= 1.247525`,

where the independent scalar worst-case data allow `11`. This is not a small numerical tightening; it is a structural gain from retaining signed directional geometry.

---

## 8. Matrix coercivity can itself define the physical cell

The ellipsoid need not come from a separate geometric producer. Suppose a pre-knot Lyapunov packet already proves the full matrix coercivity

**(8.1)** `x^T G x <= W_-(x)`

and the current pre-knot level satisfies

**(8.2)** `W_-(x) <= R`.

Then immediately

**(8.3)** `x^T G x <= R`.

So the same anisotropic coercivity matrix can be carried directly into the reset multiplier. Replacing (8.1) by a scalar `m Qx<=W_-` before reset may unnecessarily destroy exactly the directional information used in section 7.

Source-facing recommendation: if the producer already owns a full quadratic coercivity matrix, preserve it alongside any scalar comparator needed by other consumers.

---

## 9. Candidate theorem statements

### Theorem T-P5-137-A — `ellipsoid_reset_of_multiplier_psd`

Assume:

- `G=G^T > 0`, `R>0`;
- `H=H^T`;
- `tau>=0`;
- `M(tau,E)>=0`;
- `x^T G x<=R`;
- `W_+-kappa W_- <= b^T x-x^T H x+C`.

Then

`W_+ <= kappa W_- + E`.

### Theorem T-P5-137-B — `ellipsoid_reset_capacity_of_multiplier_psd`

Under the same hypotheses with `E` replaced by available reset capacity `J`, if

`[[H+tau G,-b/2],[-b^T/2,J-C-tau R]] >= 0`,

then

`W_+-kappa W_- <= J`.

### Optional mathematical corollary — real losslessness under Slater

If `G>0`, `R>0`, then over the reals the existence of some reset bound `E` for the quadratic envelope on the ellipsoid is equivalent to the existence of a real `tau>=0` satisfying the block PSD gate, by the one-constraint S-lemma.

Only A/B are proposed as the minimal trusted child theorem. The losslessness corollary may remain commentary unless the project wants a formal S-lemma dependency.

---

## 10. Failure boundaries and exact obstructions

### 10.1 No same-cell semantics, no certificate

`G,H,b,C,R` must describe the **same physical reset event / same reference key / same chart semantics**. Combining a radius from one knot with a quadratic envelope from another is not licensed by the algebra.

### 10.2 Missing terms remain missing

Any frame-power, moving-anchor, controller saturation, finite-difference, or chart-switch term absent from (1.2) must be charged separately. The multiplier cannot certify terms that were omitted from the signed reset envelope.

### 10.3 Nonsymmetric `H`

Only `sym(H)` is visible to `x^T Hx`. A producer should either emit `sym(H)` or prove that the provided quadratic matrix has been symmetrized. Antisymmetric entries must not be counted as restoring curvature.

### 10.4 Degenerate cell

If `G` is merely PSD or `R=0`, Theorem A remains a valid **sufficient** statement whenever the block PSD gate is proved, but the compact-ellipsoid / strict-Slater losslessness interpretation no longer follows automatically. Null directions may make the physical set unbounded.

### 10.5 Approximate constant term

If source gives only `C<=Cbar`, replacing `C` by `Cbar` in the block is safe, but any losslessness statement then applies to the enlarged envelope, not to the unknown exact reset term.

### 10.6 No rational multiplier at an exact boundary

As noted in section 5, a real feasible boundary multiplier need not be rational. A rational checker must either accept a small rational slack or receive another exact algebraic witness. Do not report “no physical reset certificate exists” merely because one rational grid failed.

### 10.7 If no real multiplier exists under Slater

Conversely, once the quadratic envelope and strict ellipsoid are exact, failure of the real multiplier feasibility problem is a genuine mathematical obstruction: the requested `E` is too small for some state inside the cell. At that point tuning Young parameters or scalar bounds cannot repair the same envelope.

---

## 11. What this changes downstream

The preferred order for a physical knot reset should now be:

1. retain the actual signed quadratic packet `(G,H,b,C,R)` if available;
2. attempt the one-scalar block-PSD multiplier gate;
3. only if full geometry is unavailable, fall back to scalarization `(A,B,R)` and the sharp T-P5-131/132 branch;
4. use T-P5-135/136 only for the chart-to-physical radius/coercivity obligations they were designed to solve.

This ordering prevents the source layer from discarding nonlinear cancellation/directional compatibility before the Lyapunov consumer sees it.

---

## 12. Remaining source obligations / nonclaims

To instantiate this child on an actual knot, the source/consumer still must provide:

- a same-key physical displacement `x` and cell matrix/radius `G,R`;
- the actual signed quadratic reset envelope `H,b,C`;
- evidence that all terms in the reset identity are accounted for exactly once;
- a rational multiplier/PSD witness, or enough exact source data for an offline search;
- actual dwell/headroom `J` if using the direct capacity form;
- same-cell coverage across the knot.

This review proves only the mathematical consumer. It does **not** prove that the deployed source has such a packet; it does not close Float64/controller semantics, runtime/P8 coverage, provenance/receipt/admission, Lean compilation, verifier acceptance, or registry eligibility.
