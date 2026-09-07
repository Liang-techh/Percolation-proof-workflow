---
kind: review_result
review_id: review-T-P4-007-liuguanyi-20260907T0212
task_id: T-P4-007
source_agent: 柳冠一
claimed_at: 2026-09-07T02:00:00-06:00
created_at: 2026-09-07T02:12:00-06:00
inspected_commit: 9143285a7dbd562c1f873dae3b693074a6f84c70
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_execution_lift_block_residual_identity_then_bind_centered_runtime_remainders
---

# T-P4-007 — actual block-(4,5) residual decomposition with solve defect and centered FD/runtime seams

## Scope

This pass completes the algebraic/source-to-math part of the coordinator-assigned `T-P4-007`.  It starts from the corrected normalization in `T-P4-008`, but removes one hidden exact-solve assumption that becomes invalid as soon as the deployed Julia `Float64` execution is lifted to real numbers.

The main result is an exact typed decomposition of the actual block force residual

```text
l_F := I_B f_B - M0_BB a_B
```

into local mass, remote mass action, central-FD C/G, normalized `kc`, controller/evaluation remainder, and linear-solve defect.  It also gives a centered gravity/runtime identity that avoids introducing a fake equilibrium bias, and a zero-slice obstruction showing what would be required before the *entire* source residual could be fed to a one-coordinate Schur envelope.

Inputs used:

- `review-T-P4-008-liuguanyi-20260907T0120.md`: typed `I_B` normalization and exact-solve block identity;
- `review-T-P4-012-youhunmozun-20260907T0130.md`: remote mass-metric consumer (not reproved here);
- `review-T-P4-013-kuangmanmozun-20260907T0145.md`: corrected normalized `kc` coefficient budget (not reproved here);
- `review-T-P3-008-guyuefangyuan-20260907T0141.md`: exact-real central-FD Christoffel indexing/remainder seam;
- `examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`: deployed `M`, central-FD `Cdq/Gq`, controller and `M \ rhs` solve;
- `examples/routeb_source_binding_audit/REPORT.md`, item `B45-5`.

No Float64 error bound, source provenance, trajectory coverage, admission, or P4/M4 closure is claimed.

## 1. Execution-lift solve defect is an independent typed object

Let all tilded quantities denote real lifts of the values produced by one execution of the deployed source:

```text
M~, C~, G~, tau~, a~.
```

The source computes

```text
a~ = lift( Float64 solve of M \ (tau-C-G) ).
```

A real lift of a floating solve must **not** be silently rewritten as the exact real equation `M~ a~ = tau~-C~-G~`.  Define instead the exact solve defect

```text
s := M~ a~ - (tau~ - C~ - G~).                         (1)
```

This is a definition, so it needs no numerical assumption.  Rearranging gives

```text
M~ a~ + C~ + G~ = tau~ + s,

tau~ = M~ a~ + C~ + G~ - s.                          (2)
```

Project the full vector into `B=(4,5)` and its complementary coordinates `D`.  Then

```text
tau~_B
 = M~_BB a~_B + M~_BD a~_D + C~_B + G~_B - s_B.       (3)
```

The sign of the solve defect in (3) is fixed by definition (1).

## 2. Exact execution-level block residual identity

Define the actual P4 generalized-force residual

```text
l~_F := I_B f~_B - M0_BB a~_B.                        (4)
```

Add and subtract `tau~_B` and use (3):

```text
l~_F
 = (I_B f~_B - tau~_B)
   + (M~_BB-M0_BB) a~_B
   + M~_BD a~_D
   + C~_B + G~_B
   - s_B.                                             (5)
```

Equation (5) is the execution-lift replacement for the exact-solve identity in `T-P4-008`.  The latter is recovered by the explicit premise `s_B=0`; without that premise it is missing the term `-s_B`.

This matters for units: every summand in (5) is a generalized force.  No acceleration residual has been introduced.

A minimal formal statement is therefore:

```text
solveDefect := M*a - (tau-C-G)
lF          := I*f - M0*aB
------------------------------------------------------
lF = (I*f-tauB) + (MBB-M0)*aB + MBD*aD + CB + GB
     - solveDefectB.
```

It is pure linear algebra and does not require a matrix inverse theorem.

## 3. Separate the intended PMI/controller identity from execution assembly

For the intended exact coefficient model define `f*_B` and `tau*_B` using the same block ordering and the exact decimal/rational parameters.  The normalization result from `T-P4-008` gives

```text
I_B f*_B - tau*_B
 = -mgl_B q_B - G0_B + rho_kc^F(q_B),                  (6)

rho_kc^F(q4,q5) = (q5/100, q4/200).                   (7)
```

Here `G0_B` is the source's reference gravity value used by the controller.  To avoid claiming that two different floating evaluation trees are identical merely because their intended coefficients agree, define the controller/evaluation remainder

```text
delta_ctrl
 := (I_B f~_B - tau~_B) - (I_B f*_B - tau*_B).        (8)
```

Then (5)--(8) give the exact typed ledger

```text
l~_F
 = (M~_BB-M0_BB) a~_B
   + M~_BD a~_D
   + C~_B
   + (G~_B-G0_B)
   - mgl_B q_B
   + rho_kc^F(q_B)
   + delta_ctrl
   - s_B.                                             (9)
```

Thus the source theorem does **not** need to guess whether floating coefficient/evaluation differences are zero.  It may prove `delta_ctrl=0`, or supply a bound, but the residual identity remains correct either way.

At the coefficient level the intended channel formulas are exactly

```text
channel 4: I4*f4 - tau4 = -(3/20) q4 - G0_4 + q5/100,
channel 5: I5*f5 - tau5 = -(2/25) q5 - G0_5 + q4/200,
```

before the execution remainder (8) is charged.

## 4. Center gravity/runtime error at the same source reference

A useful interface simplification comes from the fact that the controller's `G0` is the value of the same gravity routine at the zero state.  Let `G_fd^R(q)` be an exact-real central-difference semantic center, and write

```text
G~(q) = G_fd^R(q) + DeltaG(q).                        (10)
```

If

```text
G0 = G~(0) = G_fd^R(0) + DeltaG(0),                   (11)
```

then the gravity term in (9) has the exact centered split

```text
G~(q)-G0-mgl*q
 = [G_fd^R(q)-G_fd^R(0)-mgl*q]
   + [DeltaG(q)-DeltaG(0)].                           (12)
```

This is preferable to charging `DeltaG(q)` and `G0` independently.  The second bracket in (12) vanishes identically at `q=0`, even if the floating gravity routine has a nonzero absolute rounding offset there.

For the frozen cosine potential used in the exact-real lane, `G_fd^R(0)=0`; after the still-open physical potential binding, the first bracket becomes simply

```text
G_fd^R(q)-mgl*q.
```

Equation (12) is a generic source-to-math lemma and does not depend on that special Fourier fact.

## 5. Exact-real / execution remainder expansion

For a future source theorem, choose exact-real semantic centers

```text
M~ = M^R + DeltaM,
C~ = C_fd^R + DeltaC,
G~ = G_fd^R + DeltaG.                                  (13)
```

Substituting (12)--(13) into (9) yields the complete no-hidden-remainder decomposition

```text
l~_F =
    (M^R_BB-M0_BB) a~_B               [local exact-real mass]
  + M^R_BD a~_D                        [remote exact-real mass]
  + C_fd^R_B                            [exact-real central-FD C]
  + (G_fd^R_B(q)-G_fd^R_B(0)-mgl_B q_B) [centered FD gravity/model]
  + rho_kc^F(q_B)                       [normalized PMI-only kc]

  + DeltaM_BB a~_B + DeltaM_BD a~_D     [mass execution/source remainder]
  + DeltaC_B                            [C execution/contraction remainder]
  + (DeltaG_B(q)-DeltaG_B(0))           [centered G execution remainder]
  + delta_ctrl                          [PMI/controller evaluation remainder]
  - s_B.                                [linear-solve defect]              (14)
```

Every term has generalized-force units.  This is the requested source-to-math interface behind `B45-5`.

`T-P3-008` may further refine the exact-real C term as

```text
C_fd^R = C_an^R + C(R_fd),                            (15)
```

where `R_fd` is the central-difference derivative tensor remainder.  That refinement is optional for P4 and should not be conflated with `DeltaC`, which is the execution/IEEE remainder after the exact central-difference semantic center is fixed.

## 6. What the existing child lemmas can consume

The fresh parallel results now attach cleanly to distinct summands of (14):

- `T-P4-013` consumes only `rho_kc^F`, with coefficients `1/100` and `1/200` after `I_B` normalization.
- `T-P4-012` consumes the exact-real remote term `M^R_BD a_D` through the mass PSD/distal-energy interface.  It does not automatically cover `DeltaM_BD a_D`.
- `T-P3-008` supplies the exact-real `C_fd^R` indexing and its analytic/FD remainder split.  It does not cover `DeltaC` or the solve defect.
- The centered gravity identity (12) says a runtime gravity offset at zero should be charged as `DeltaG(q)-DeltaG(0)`, not as an unrelated additive constant.

This prevents double charging and, more importantly, prevents a proof about one semantic layer from silently consuming an error belonging to another layer.

## 7. Zero-slice criterion for a one-coordinate Schur adapter

Suppose a downstream scalar channel wants to prove on a domain `Omega`

```text
|l_i(z)| <= k |y_i(z)|                                    (16)
```

for a Schur auxiliary `y_i` identified with `q5` (channel 4) or `q4` (channel 5).  A necessary condition is

```text
y_i(z)=0  ==>  l_i(z)=0.                                  (17)
```

This follows immediately from (16), and is independent of the value of `k`.

Equation (14) shows why this condition must be checked for the **total** source residual, not merely for `kc`: on a `q_cross=0` slice the local/remote mass terms, C term, centered gravity term in the other coordinates, execution remainders, or solve defect can remain nonzero.  Separate absolute bounds on those terms cannot prove (17); one needs either

1. a genuine slice-cancellation/vanishing theorem,
2. a domain relation forcing the relevant terms to vanish with `q_cross`, or
3. a different quadratic/slack consumer (for example the mass-metric route of `T-P4-012`) instead of forcing the full residual through the single-coordinate envelope.

Thus the corrected `kc` constants solve only the `kc` seam; they do not turn the whole source residual into a quarter-relative residual by themselves.

## 8. Lean-friendly theorem package

The minimal formalization should keep the semantic layers abstract:

```lean
-- Pure block algebra with an explicit solve defect.
theorem block_residual_with_solve_defect
    (lF ctrl massLocal massRemote C G solve : VecB)
    (hl : lF = ctrl + massLocal + massRemote + C + G - solve) :
    ...
```

In practice it is better to define `solve := M*a-(tau-C-G)` and prove the equality by `ring`/finite-sum algebra rather than pass `hl` as a premise.

```lean
-- Generic centering identity.
theorem centered_reference_split
    (Gexec Gref delta : VecB)
    (hG : Gexec = Gref + delta) :
    (Gexec q - Gexec 0)
      = (Gref q - Gref 0) + (delta q - delta 0)
```

and a separate theorem should insert the already-formalizable
`rho_kc^F=(q5/100,q4/200)` normalization.

The zero-slice implication can be a one-line scalar theorem:

```lean
theorem relative_envelope_zero_slice
    (l y k : R) (h : |l| <= k*|y|) (hy : y=0) : l=0
```

No source object, hash, or floating arithmetic should be hidden inside these lemmas.

## 9. Remaining blockers / shortest next step

This review closes the **algebraic decomposition** of `B45-5`, but not the quantitative source bounds.  The remaining obligations are now typed and disjoint:

1. source/IEEE lane: bound `DeltaM`, `DeltaC`, centered `DeltaG(q)-DeltaG(0)`, `delta_ctrl`, and the solve defect `s` on the same covered domain;
2. P8/source lane: bound distal acceleration energy for the `T-P4-012` mass-metric consumer;
3. exact-real lane: bind `M^R`, `C_fd^R`, `G_fd^R` to the deployed DH semantics and quantify the local mass/gravity model terms;
4. P4 consumer lane: decide which summands use the one-coordinate Schur budget and which use independent quadratic/slack consumers; do not force (14) wholesale into `|l_i|<=k|q_cross|` unless the zero-slice condition (17) is proved.

A particularly important follow-up is a focused runtime theorem for the *centered* gravity/solve/controller remainders.  If those are only given positive constant envelopes, the zero-slice theorem immediately blocks a global single-coordinate relative adapter on any domain containing `q_cross=0`.

Admission remains `pending`.  This is a mathematical/source-interface result only; it is for 梁智炜 to harvest and for the formalization agents to decompose.  It does not modify P4/M4 status or the registry.
