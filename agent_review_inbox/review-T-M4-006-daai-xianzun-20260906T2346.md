---
kind: review_result
review_id: review-T-M4-006-daai-xianzun-20260906T2346
task_id: T-M4-006
source_agent: 大爱仙尊
claimed_at: 2026-09-06T23:42:00-06:00
created_at: 2026-09-06T23:46:00-06:00
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_cross_branch_budget_transfer_then_bind_sources
---

# T-M4-006 — P7 × P8 × M4 cross-branch residual-budget transfer

## Scope

This review composes three already-established mathematical ingredients without reopening their source/provenance lanes:

1. **P7 tail absorption**: after a typed Schur binding, one coupled tail can be charged by
   `rho(t) * (1/160000) * s(t)^2`.
2. **P8 ramp reconstruction**: on the lifted ramp lane, `s(t)=c*t` with `c^2<=3` on `t in [0,1]`.
3. **M4 weighted terminal split**: the improved exact-rational terminal consumer accepts any total residual budget
   `D_total <= 1401/625`.

The purpose is to derive the smallest composition theorem that tells the C4/C5 ledger exactly how much P7 tail charge can be added to an already-existing residual budget.

Inspected mathematical sources:

- `review-T-P7-001-honglianmozun-20260906T2244.md`
  - P7 Schur absorption cost and ramp-integrated conditional bound;
- `review-T-P8-006-guyuefangyuan-20260906T2218.md`
  - exact ramp reconstruction `s(t)=c*t` and terminal transfer;
- `review-T-M4-003-kuangmanmozun-20260906T2258.md`
  - exact weighted terminal family and safe rational window `D<=1401/625`.

No source binding, flowpipe coverage, receipt/provenance, registry, or admission claim is made.

## 1. Integrated P7 charge under the P8 ramp

Assume on `t in [0,1]`:

```text
0 <= rho(t) <= rho_bar,
s(t) = c*t,
c^2 <= 3.
```

The P7 pointwise charge is

```text
C_tail(t) = rho(t) * (1/160000) * s(t)^2.
```

Hence

```text
C_tail(t)
 <= rho_bar/160000 * c^2 * t^2.
```

Integrating from `0` to `1` gives

```text
D_tail
:= integral_0^1 C_tail(t) dt
<= rho_bar/160000 * c^2 * integral_0^1 t^2 dt
= rho_bar/160000 * c^2/3
<= rho_bar/160000.                                  (1)
```

This is exactly the conditional estimate already implicit in P7, now packaged as a residual-ledger object that can be added to the C4 budget.

## 2. Cross-branch budget composition theorem

Let `D_base` denote every residual contribution already charged by C4 except this P7 tail. Define

```text
D_total := D_base + D_tail.
```

From (1),

```text
D_total <= D_base + rho_bar/160000.                 (2)
```

Therefore the improved M4 terminal theorem applies whenever

```text
D_base + rho_bar/160000 <= 1401/625.                (3)
```

Under the existing C5 hypotheses `Q(x_lin)<=L` and `Q(r)<=g*D_total`, the `eta=81/160` weighted split then gives

```text
Q(x_lin+r) < 12.                                    (4)
```

This is the shortest exact theorem chain connecting the three branches:

```text
P7 Schur binding
  -> pointwise tail charge
P8 ramp reconstruction
  -> integrated charge <= rho_bar/160000
C4 base budget D_base
  -> D_total <= D_base + rho_bar/160000
M4 eta81 consumer
  -> terminal qpoly < 12.
```

## 3. Concrete corollary at the old C4 gate: rho_bar <= 16

The old residual gate is

```text
D_old = 4483/2000 = 2.2415.
```

The improved safe M4 gate is

```text
D_new = 1401/625 = 2.2416.
```

Their exact difference is

```text
D_new - D_old = 1/10000.                            (5)
```

If the non-P7 residual ledger still satisfies

```text
D_base <= 4483/2000,
```

then condition (3) is guaranteed by

```text
rho_bar/160000 <= 1/10000,
```

i.e.

```text
rho_bar <= 16.                                      (6)
```

Thus we obtain the useful exact corollary:

```text
D_base <= 4483/2000,
0 <= rho(t) <= 16,
s(t)=c*t,
c^2<=3,
P7 Schur absorption hypotheses,
Q(x_lin)<=L,
Q(r)<=g*(D_base+D_tail)
---------------------------------------------------
Q(x_lin+r) < 12.
```

The boundary `rho_bar=16` still fits exactly inside the enlarged residual gate because

```text
4483/2000 + 16/160000
= 4483/2000 + 1/10000
= 1401/625.
```

The strict terminal inequality comes from the already-proved positive arithmetic margin of the M4 `eta=81/160` theorem at `D=1401/625`, not from strictness in the budget inequality itself.

## 4. Sharpness / information boundary of this composition

The constant `16` is sharp **for this bookkeeping route** when one assumes only

```text
D_base <= 4483/2000
```

and uses the worst-case P8/P7 estimate

```text
D_tail <= rho_bar/160000.
```

If `rho_bar>16`, the upper bound in (2) exceeds `1401/625`, so the current M4 safe rational corollary no longer closes automatically.

This does **not** prove failure of the physical theorem for `rho_bar>16`. It proves only that one must then obtain at least one of:

1. a strictly smaller actual `D_base`;
2. a sharper bound on `integral rho(t)t^2 dt` than `rho_bar/3`;
3. a smaller actual ramp amplitude than `c^2<=3`;
4. correlation/orthogonality information improving the terminal split beyond separate quadratic bounds;
5. a better P7 tail normalization than the coarse `tau=1/160000` charge.

Hence `rho_bar>16` is a clean trigger for where further mathematics is actually needed rather than more ledger rearrangement.

## 5. More general residual-slack form

Define the available terminal slack

```text
Delta := 1401/625 - D_base.
```

If `Delta>=0`, then the exact sufficient condition is

```text
rho_bar <= 160000 * Delta.                          (7)
```

This form is more useful downstream because any improvement in C4 immediately converts into allowable P7 normalization budget. Conversely, a source theorem proving a concrete `rho_bar` immediately tells C4 how much residual budget must remain unspent:

```text
D_base <= 1401/625 - rho_bar/160000.                (8)
```

This is the recommended interface between the P7 source-binding lane and the M4 residual ledger.

## 6. Lean-friendly theorem decomposition

Suggested source-independent statements:

```lean
-- Pure arithmetic budget transfer.
theorem tail_budget_transfer
    (Dbase rhoBar Dtail : ℝ)
    (hDtail : Dtail <= rhoBar / 160000)
    (hbudget : Dbase + rhoBar / 160000 <= (1401/625 : ℝ)) :
    Dbase + Dtail <= (1401/625 : ℝ)
```

```lean
-- Old-gate concrete corollary.
theorem old_gate_plus_tail_of_rho_le_16
    (Dbase Dtail rhoBar : ℝ)
    (hbase : Dbase <= (4483/2000 : ℝ))
    (hrho : rhoBar <= 16)
    (hDtail : Dtail <= rhoBar / 160000)
    (hrho0 : 0 <= rhoBar) :
    Dbase + Dtail <= (1401/625 : ℝ)
```

```lean
-- Ramp integration interface, after choosing a suitable Mathlib integral API.
theorem ramp_tail_integral_bound
    (rho : ℝ -> ℝ) (rhoBar c : ℝ)
    (hrho0 : forall t in Set.Icc 0 1, 0 <= rho t)
    (hrho : forall t in Set.Icc 0 1, rho t <= rhoBar)
    (hc : c^2 <= 3) :
    integral (fun t => rho t / 160000 * (c*t)^2) 0 1
      <= rhoBar / 160000
```

For fastest formalization, prove the first two algebraic lemmas first and keep the integral lemma separate. The latter depends on the exact interval-integral API and measurability/integrability hypotheses, whereas the budget transfer itself is elementary and immediately reusable.

## 7. What remains open

This composition does not establish any of the physical premises:

- the P7 checker variables are the deployed Schur variables;
- a global physical upper bound `rho(t)<=rho_bar` exists;
- the P7 scalar `s` is exactly the P8 ramp variable on the same trajectory;
- C4's `D_base` has same-domain coverage and no double charging;
- P8 flowpipe/existence/continuation is established;
- the terminal `L,g` premises are source-bound.

It also does not authorize changing the authoritative M4 gate. It supplies a theorem-level interface for 梁智炜 to consume once the source lanes discharge their hypotheses.

## Recommended next action

1. Formalization lane: prove the two pure arithmetic transfer lemmas immediately; they are tiny and should compile with `norm_num`/`linarith`.
2. P7/P3 source lane: seek a concrete same-domain bound on the physical normalization multiplier `rho`; `rho_bar<=16` is now a meaningful target if C4 remains at the old gate.
3. C4 lane: report not just `D<=gate`, but the exact residual slack `1401/625-D_base`; this turns directly into allowable P7 tail budget via (7).
4. If the best source-side `rho_bar` exceeds the available `160000*Delta`, stop rearranging terminal Young constants and improve the residual/kernel or exploit time variation in `rho(t)`.

No Lean/checker command was run in this mathematical pass. Formalization belongs to the Lean agents; independent validation belongs to 封不觉; final integration and task release belong to 梁智炜.
