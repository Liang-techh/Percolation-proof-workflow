---
kind: review_result
review_id: review-T-P5-170-iterated-sign-compatible-pivot-energy-chain-honglianmozun-20260909T1657Z
task_id: T-P5-170-ITERATED-SIGN-COMPATIBLE-PIVOT-ENERGY-CHAIN
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T16:57:00Z
claim_commit: 569178d2513ecf42a3393138b4db1bfc61e61b40
inspected_commit: 4ec8e21480d6cddcc182e1a82d8158e3c8bab2a9
upstream_commits:
  - d1c6c32499fe4f792fdacd80639f1738fa7da616  # T-P5-168 one-step sign-compatible pivot + exact 3-path
  - fec7f1ad78ecff83ef62bc6e889f63bfbca97c59  # T-P5-166 negative-forest shared diagonal budget
  - 300fec2e52d7a3a78107110f25df0ab016dc81d2  # T-P5-169 sharp-floor contact localization
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: promote_repeated_sign_compatible_pivots_from_dispatch_heuristic_to_exact_energy_chain; preserve_positive_nonedges; use_division_free_backward_witness_lift; allow_certified_copositive_terminal_core; at_positive_floor_lift_terminal_zero_contact_to_global_sharpness_witness
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional real/rational quadratic-form algebra only
exit_code: n/a
---

# T-P5-170 — iterated sign-compatible pivot energy chain

## 0. Verdict and non-overlap

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-168 proves the exact one-step copositive pivot theorem and explicitly suggests recursively trying another sign-compatible pivot after reduction. However, that recursive route is left as a dispatcher strategy: there is no stated multi-step iff theorem, no accumulated energy identity, no exact backward FAIL/contact lift, and no proof that a terminal cone-only certificate can be composed without reverting to PSD.

This child closes exactly that seam.

The result is an exact finite chain theorem:

> every valid sign-compatible pivot removes one coordinate by a scaled Schur completion; a sequence of such pivots is an iff reduction from the original copositivity problem to the terminal core; the full original quadratic form admits a nested sum-of-squares-plus-terminal-energy identity; and every terminal nonnegative FAIL or zero contact lifts backward by exact multiplication/addition only.

This is materially stronger than T-P5-166's negative-skeleton sufficient route because all positive nonedges are retained. It is also stronger than an ordinary PSD/Schur path because the terminal core is allowed to be copositive and indefinite.

No source/provenance audit, runtime/Float64 claim, Lean/kernel validation, independent re-audit, admission, or registry mutation is performed.

---

## 1. One-step notation

Let `M_k` be a real symmetric matrix on the current coordinate set. After placing a proposed pivot first, write

`M_k = [[b_k, -r_k^T],
        [-r_k, A_k]]`.

Assume

**(1.1)** `b_k > 0`,

**(1.2)** `r_k >= 0` componentwise.

Thus every current off-diagonal coupling from the pivot to a retained nonnegative coordinate is nonpositive.

For a current state `x_k=(t_k,y_k)`, define

`q_k(x_k) := x_k^T M_k x_k`.

Define the scaled reduced matrix

**(1.3)** `M_{k+1} := b_k A_k - r_k r_k^T`.

T-P5-168's one-step completion is the exact identity

**(1.4)**

`b_k q_k(t_k,y_k)
 = (b_k t_k-r_k^T y_k)^2
   + y_k^T M_{k+1} y_k`.

The sign condition `r_k>=0` is what makes the one-step implication an iff on the nonnegative cone.

---

## 2. Main theorem: an iterated pivot chain is an exact copositivity reduction

Let the chain have `m` valid pivots. Starting from `M_0`, recursively choose a pivot satisfying (1.1)-(1.2) in the **current reduced matrix** and form `M_{k+1}` by (1.3), for

`k=0,...,m-1`.

No sign condition is imposed on the retained block `A_k`; in particular positive couplings are preserved exactly and may survive into the terminal matrix `M_m`.

### Theorem T170-A — `iterated_copositive_pivot_iff_terminal`

Under the stagewise gates `b_k>0` and `r_k>=0`,

**(2.1)**

`M_0 is copositive  <=>  M_m is copositive`.

### Proof

At every stage, T-P5-168 gives

`M_k copositive <=> M_{k+1} copositive`.

Compose these finitely many equivalences. No PSD assumption is introduced at any stage. QED.

### Consequence

A producer does not need to eliminate to a scalar. It may stop as soon as the terminal core is certified by any exact cone theorem already available, for example:

- entrywise nonnegative terminal matrix;
- exact 2x2 root-free copositivity gate;
- T-P5-155 three-vertex exact gate;
- T-P5-158 support-KKT fallback;
- T-P5-161 PSD only when the terminal sign corridor genuinely permits it.

The pivot chain itself is just an exact dimension-reduction adapter.

---

## 3. New energy identity: all eliminated coordinates become explicit squares

For one fixed original state `x_0>=0`, let `x_{k+1}` denote the retained subvector of `x_k` after dropping the stage-`k` pivot coordinate. Define the stage residual

**(3.1)**

`sigma_k := b_k t_k-r_k^T x_{k+1}`.

Let an empty product equal `1`.

### Theorem T170-B — `iterated_pivot_energy_decomposition`

The exact identity

**(3.2)**

`(prod_{j=0}^{m-1} b_j) q_0(x_0)
 = sum_{k=0}^{m-1}
     (prod_{j=k+1}^{m-1} b_j) sigma_k^2
   + q_m(x_m)`

holds for every real `x_0`.

### Proof

For `m=1`, this is (1.4).

For two stages,

`b_0 q_0 = sigma_0^2 + q_1`,

`b_1 q_1 = sigma_1^2 + q_2`.

Multiply the first equality by `b_1` and substitute the second:

`b_0 b_1 q_0 = b_1 sigma_0^2 + sigma_1^2 + q_2`.

Repeating this substitution gives (3.2) by finite induction. QED.

### Energy/Lyapunov interpretation

The decomposition separates the original cone energy into two qualitatively different pieces:

1. **pivot-completion dissipation gaps** `sigma_k^2`, each manifestly nonnegative;
2. one residual **terminal cone energy** `q_m`.

Therefore a positive nonedge does not need to be converted into a PSD tax or deleted into a negative skeleton. It may remain in the terminal core and provide the exact cone-only cancellation needed for nonnegativity.

This is the structural reason recursive cone-aware completion can succeed even when both ordinary PSD and the negative-skeleton route fail.

---

## 4. Division-free backward lift of FAIL witnesses and zero contacts

The one-step theorem can be made operational without dividing by `b_k`.

Fix a stage and a retained vector `z>=0`. Define

**(4.1)** `s_k := r_k^T z >= 0`.

Define the lifted current state by

**(4.2)**

`L_k(z) := (s_k, b_k z)`

in the ordering `(pivot, retained coordinates)`.

Because `b_k>0` and `r_k,z>=0`, the lifted state is nonnegative.

### Lemma T170-C — `pivot_backward_lift_identity`

**(4.3)**

`q_k(L_k(z)) = b_k q_{k+1}(z)`.

### Proof

Expand directly:

`q_k(s_k,b_k z)
 = b_k s_k^2
   -2 s_k r_k^T(b_k z)
   +(b_k z)^T A_k(b_k z)`

`= b_k s_k^2-2b_k s_k^2+b_k^2 z^T A_k z`

`= b_k z^T(b_k A_k-r_k r_k^T)z`

`= b_k q_{k+1}(z)`.

QED.

### Corollary T170-C1 — exact terminal FAIL lifts to exact original FAIL

Let `z_m>=0` satisfy

`q_m(z_m)<0`.

Recursively define

`z_k := L_k(z_{k+1})`

for `k=m-1,...,0`.

Then every `z_k>=0` and

**(4.4)**

`q_0(z_0) = (prod_{k=0}^{m-1} b_k) q_m(z_m) < 0`.

Thus the chain gives not merely a PASS reducer but a constructive exact nonnegative counterexample lift.

If all matrix data and the terminal witness are rational, every lifted coordinate remains rational: the lift uses only dot products and multiplication by positive rational pivots.

### Corollary T170-C2 — terminal zero contact lifts to an original zero contact

If nonzero `z_m>=0` satisfies

`q_m(z_m)=0`,

then the same backward construction gives nonzero `z_0>=0` with

**(4.5)** `q_0(z_0)=0`.

This contact lift is useful at sharp additive floors; Section 7 connects it to T-P5-169.

---

## 5. Exact fail-closed pivot boundaries

A recursive implementation must distinguish a real mathematical obstruction from failure of the chosen elimination order.

### 5.1 Negative pivot diagonal

If a proposed/current pivot has

`b_k<0`,

the pivot basis vector itself is a nonnegative FAIL witness:

`q_k(e_p)=b_k<0`.

So the current matrix is not copositive.

### 5.2 Zero pivot with a strictly negative coupling

Suppose

`b_k=0`

and some component `r_{k,j}>0`.

Then copositivity is impossible. There is even a division-free explicit witness.

Let

`a := (A_k)_{jj}`,

choose retained state

`y = 2 r_{k,j} e_j`,

and pivot coordinate

`t = a^2+1`.

Both are nonnegative. Direct expansion gives

**(5.1)**

`q_k(t,y)
 = 4 r_{k,j}^2 (a-a^2-1)`

`= -4 r_{k,j}^2 (a^2-a+1)`.

Since

`a^2-a+1=(a-1/2)^2+3/4>0`,

we have

**(5.2)** `q_k(t,y)<0`.

Thus a zero diagonal cannot support any strictly negative pivot edge.

### 5.3 Zero pivot and zero row

If

`b_k=0` and `r_k=0`,

the pivot coordinate contributes identically zero and decouples:

`q_k(t,y)=y^T A_k y`.

The coordinate may be dropped exactly without a Schur update.

### 5.4 Positive off-diagonal in the proposed pivot row

If `b_k>0` but some current pivot off-diagonal is positive, the sign-compatible iff theorem is unavailable. This is **not** a mathematical FAIL. It only means this pivot/order cannot be used by this chain.

A different pivot, a low-dimensional exact gate, or generic support/KKT must be tried.

Crucially, the sign test is performed on the current reduced matrix `M_k`, not only on the original negative graph: Schur reduction changes signs.

---

## 6. Exact four-vertex regression: skeleton and PSD fail, iterated energy chain succeeds

Consider

**(6.1)**

`M = [[ 1,-1, 0, 0],
      [-1, 2,-1, 2],
      [ 0,-1, 1,-1],
      [ 0, 2,-1, 1]]`.

Its strictly negative graph is the path

`1 -- 2 -- 3 -- 4`,

while the positive nonedge/chord is

`M_24=M_42=2`.

### 6.1 T-P5-166 negative skeleton genuinely fails

Delete the positive chord and keep only the diagonal plus negative edges:

`N = [[ 1,-1, 0, 0],
      [-1, 2,-1, 0],
      [ 0,-1, 1,-1],
      [ 0, 0,-1, 1]]`.

For the nonnegative vector `u=(1,1,1,1)`,

**(6.2)**

`u^T N u = 5-6 = -1`.

So the forest skeleton is not copositive/PSD. T-P5-166 must correctly return only "fast path failed" here.

### 6.2 Ordinary PSD also fails for the original matrix

Exact expansion gives

**(6.3)** `det(M)=-1<0`.

A PSD symmetric matrix cannot have negative determinant, so ordinary PSD certification is impossible.

### 6.3 First exact pivot

Pivot coordinate `1`. Here

`b_0=1`,

`r_0=(1,0,0)>=0`.

The scaled reduced matrix on coordinates `(2,3,4)` is

**(6.4)**

`M_1 = [[ 1,-1, 2],
        [-1, 1,-1],
        [ 2,-1, 1]]`.

The first completion identity is simply

**(6.5)**

`q_M(x_1,x_2,x_3,x_4)
 = (x_1-x_2)^2 + q_1(x_2,x_3,x_4)`.

### 6.4 Second exact pivot

In `M_1`, pivot the middle coordinate `x_3`. Again

`b_1=1`,

`r_1=(1,1)>=0`.

The terminal reduced matrix on `(x_2,x_4)` is

**(6.6)**

`M_2 = [[0,1],
        [1,0]]`.

This terminal matrix is **not PSD** (its determinant is `-1`), but it is trivially copositive because

**(6.7)** `q_2(x_2,x_4)=2 x_2 x_4>=0`

for `x_2,x_4>=0`.

Therefore T170-A proves the original 4x4 `M` is copositive.

### 6.5 Full explicit cone-energy identity

Combining the two completion steps yields

**(6.8)**

`x^T M x
 = (x_1-x_2)^2
   +(x_3-x_2-x_4)^2
   +2 x_2 x_4`.

For every `x>=0`, all three terms on the right are nonnegative.

This is a strict separation example:

- negative-forest skeleton: FAIL;
- ordinary PSD: FAIL;
- terminal ordinary PSD: FAIL;
- exact iterated sign-compatible cone-energy chain: PASS.

Hence the new chain is not cosmetic repackaging of T-P5-166 or T-P5-161. The positive chord is the essential cone-only rescue term, and the recursive completion preserves it exactly.

---

## 7. Sharp-floor corollary: terminal contact can certify the global floor

Return to the T-P5-154/T-P5-159 additive floor family

`q_D(x)=Q_0(x)+D L(x)`, 

where for nonzero `x>=0` and `g_i>0`,

`L(x)=(sum_i x_i)(sum_i g_i x_i)>0`.

Fix a candidate `D_*>0`.

Assume:

1. the exact matrix `M_{D_*}` admits a valid T170 pivot chain;
2. the terminal core `M_m` is copositive;
3. there is a nonzero terminal contact `z_m>=0` with `z_m^T M_m z_m=0`.

By T170-C2, lift `z_m` backward to a nonzero original contact `z_0>=0` satisfying

**(7.1)** `q_{D_*}(z_0)=0`.

By T170-A, `M_{D_*}` is copositive, so `D_*` is a valid floor.

For any `D<D_*`, use the **same original lifted contact**:

**(7.2)**

`q_D(z_0)
 = q_{D_*}(z_0)-(D_*-D)L(z_0)`

`= -(D_*-D)L(z_0)<0`.

Therefore no smaller floor is valid.

### Corollary T170-D — `terminal_contact_lifts_to_exact_sharp_floor`

Under the three assumptions above,

**(7.3)** `D_*` is the exact global sharp floor.

A useful point is that the pivot sign gates need only be certified at the candidate `D_*` for this sharpness proof. They do not need to persist for all lower `D`: once the original zero contact is lifted, equation (7.2) itself supplies every lower-floor FAIL witness.

This directly complements T-P5-169's contact-localization result.

---

## 8. Structural fingerprint

The new reusable fingerprint is:

> **cone-compatible completion chain**: if a current energy coordinate has positive self-energy and only nonpositive couplings to all retained nonnegative coordinates, complete that coordinate exactly, keep every signed coupling inside the reduced core, and repeat only after rechecking the new row signs.

This differs from three common lossy moves:

1. deleting all positive nonedges into a negative skeleton;
2. replacing the entire form by ordinary PSD;
3. applying independent Young bounds to each negative cross term.

The chain preserves signed correlation all the way to the terminal cone energy.

In Lyapunov language, each pivot contributes a literal square gap `sigma_k^2`; only the irreducible terminal cone interaction remains to be certified by another structural fingerprint.

---

## 9. Exact checker packet

For one fixed exact candidate matrix, a minimal machine-checkable chain can contain, at each stage `k`:

- current vertex order / pivot index;
- exact `b_k` with `b_k>0`;
- exact vector `r_k` with `r_k>=0`;
- exact retained block `A_k`;
- exact equality `M_{k+1}=b_k A_k-r_k r_k^T`.

The terminal packet contains one of:

- an exact copositivity PASS certificate for `M_m`; or
- a nonnegative exact FAIL witness `z_m`.

For a FAIL, the consumer may replay T170-C1 backward and emit the original nonnegative witness. For a sharp-floor contact, it may replay T170-C2 and then T170-D.

No inverse, square root, eigenvalue, floating optimizer, or division is required by the trusted chain itself.

---

## 10. Lean-friendly theorem decomposition

### L1 — one-step scaled completion identity

Reuse the algebraic core already exposed by T-P5-168:

`b*q(t,y) = (b*t-dot r y)^2 + qReduced(y)`.

### L2 — finite iterated energy identity

Prove by induction over a list of stages:

`prod b * q0 = weightedSumSquares + qTerminal`.

The matrix API can be avoided initially by treating each stage identity as an abstract equality and composing it algebraically.

### L3 — backward witness lift

For `s=dot r z`, prove

`q(s,b*z)=b*qReduced(z)`.

Then iterate over the stage list.

### L4 — zero-pivot negative-edge obstruction

Prove the explicit polynomial witness (5.1)-(5.2), using

`a^2-a+1>0`.

### L5 — sharp-floor contact lift

Combine terminal contact lift with the affine floor identity

`q_D=q_Dstar-(Dstar-D)L`

and positivity of `L` on nonzero nonnegative states.

None of these leaves needs a generic eigenvalue or inverse API.

---

## 11. Failure boundaries and remaining obligations

The theorem deliberately does **not** claim that every copositive matrix admits such an elimination order.

Exact boundaries:

- each pivot row-sign gate must be rechecked after every reduction;
- failure to find a sign-compatible pivot is a fallback, not a mathematical FAIL;
- a positive pivot coupling invalidates the one-step iff and cannot be silently clipped;
- terminal copositivity still needs its own exact certificate;
- for symbolic `D`, reduced entries can increase polynomial degree and pivot signs may change with `D`; this review proves the fixed-candidate chain, not a global symbolic elimination partition;
- T170-D requires `D_*>0`, `g_i>0`, and a nonzero nonnegative contact; the zero-floor endpoint retains the separate T-P5-169 boundary;
- interval/correlated source families still require the family-level sign/source logic of T-P5-167 or a stronger source adapter.

Still open and external to this review:

- actual same-key source values `{g_i,K_ij}` or a deployed matrix instance;
- actual component/pivot ordering and source-certified stage signs;
- uncertainty-simplex / physical-cell / trajectory coverage;
- Float64, interval rounding, runtime/controller/P8 semantics;
- Lean/kernel compilation and independent verification by 封不觉;
- admission, theorem registry, and P5/P8/M4 parent closure.

Therefore the correct state remains

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`.**

---

## 12. Recommended mathematical use

At a fixed exact floor/component, before deleting positive nonedges or launching generic support enumeration:

1. search for a current pivot with `b>0` and all current off-diagonals `<=0`;
2. apply the exact scaled reduction;
3. repeat while the sign gate survives;
4. stop at the smallest terminal core and use the strongest exact available cone certificate there;
5. on terminal FAIL, lift the witness backward exactly;
6. at a positive candidate floor with terminal zero contact, lift the contact and use T170-D to certify sharpness.

The four-vertex identity (6.8) is the canonical regression: any implementation that first drops the positive chord or insists on PSD will reject a matrix whose cone energy is in fact exactly nonnegative.