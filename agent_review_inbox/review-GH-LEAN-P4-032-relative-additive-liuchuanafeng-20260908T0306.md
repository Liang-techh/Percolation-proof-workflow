---
kind: review_result
review_id: review-GH-LEAN-P4-032-relative-additive-liuchuanafeng-20260908T0306
task_id: GH-LEAN-P4-032-relative-additive
agent: 流川枫
source_agent: 流川枫
created_at: 2026-09-08T03:06:00-06:00
inspected_commit: cfe49413a024e86c3b282af469797327d095799e
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_RelativeAdditive.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_RelativeAdditive_REVIEW.md
integration_status: pending
admission_label: architecture_only
proposed_integration_target: P4.relative_additive_budget_open_contract
requested_action: keep as OPEN_UNCOMPILED typed regrouping of an already-weighted squared budget; do not treat rho_eff/B_eff as source, coverage, sqrt-free physical residual, or registry evidence; reserve pinned compile/axioms for the :40 Lean slot
---

# GH-LEAN-P4-032-relative-additive — independent statement audit

## 0. Result

`NEW_P4_032_RelativeAdditive.lean` is a **source-independent parameter regrouping** of a previously declared three-term weighted squared budget. It defines

```text
rho_eff = λ0 * rhoA + λ1 * tau² * kappaD + λ2 * kappaB
B_eff   = λ1 * tau² * biasD + λ2 * biasB
```

and proves, under explicit nonnegativity and two affine envelope inequalities on the same scalar `energy`,

```text
weightedBudget(energy, ED, EB) ≤ rho_eff * energy + B_eff.
```

Force and acceleration consumers stay on distinct defect types and distinct `ActionBound` objects (`MBD*J` vs `MBD`). There is no sqrt, no concrete cell numbers, and no source/coverage claim in the file.

This lane did **not** run Lake/Lean, `#print axioms`, or a placeholder scan. Companion `NEW_P4_032_RelativeAdditive_REVIEW.md` is a proof-attempt note, not kernel evidence. `admission_label` is therefore `architecture_only`.

No registry, StateStore, comparator, or formal-admission object is written.

## 1. What the sidecar actually states

Namespace: `RouteBP4032RelativeAdditive`.
Import: `NEW_P4_032_WeightedThreeTerm` only (then opens BlockDefects / DefectNormBudget / WeightedThreeTerm).

`Parameters` packages one `Weights` object plus `rhoA, tau, kappaD, kappaB, biasD, biasB` with six nonnegativity fields.

`EnvelopesAt` is a same-point predicate:

- `energy, ED, EB ≥ 0`
- `ED ≤ kappaD * energy + biasD`
- `EB ≤ kappaB * energy + biasB`

ED/EB are squared envelopes, not unsquared norm caps. `weightedBudget` is

```text
λ0 * (rhoA * energy) + λ1 * (tau² * ED) + λ2 * EB.
```

Theorems present in the file:

| name | role |
|---|---|
| `effective_coefficients_nonnegative` | `rho_eff ≥ 0` and `B_eff ≥ 0` from weights and parameter signs |
| `affine_budget_identity` | ring identity after substituting the *envelope endpoints* |
| `weighted_budget_le_relative_additive` | monotone substitution of the two envelope inequalities |
| `relative_additive_budget_nonnegative` | nonnegativity of the regrouped right-hand side |
| `consume_weighted_budget` | transports any `q ≤ weightedBudget` |
| `force_relative_additive` | consumes `force_defect_budget` with `forceTerm` / `DistalForceDefect` |
| `accel_relative_additive` | consumes `accel_defect_budget` with `accelTerm` / `DistalAccelDefect` |
| `zero_bias_corollary` | drops `B_eff` only after explicit `biasD = biasB = 0` |

`tau` is squared exactly once on the distal channel. The file does not re-prove Cauchy, triangle, or convention adapters.

Text scan of this sidecar: no `sorry`, `admit`, or `sqrt`. `#print axioms` commands are present but **unexecuted** here.

## 2. Force vs acceleration boundary (must stay split)

`force_relative_additive` requires

- identity `rB = R aB + forceTerm MBD J eD + eB`
- `ActionBound (MBD * J) tau`
- squared port bound on `R aB` against `rhoA * energy`

`accel_relative_additive` requires

- identity `rB = R aB + accelTerm MBD eD + eB`
- `ActionBound MBD tau`

The two conclusions look identical (`||rB||² ≤ rho_eff energy + B_eff`) but the certificates are not interchangeable. Queue forbidden clause “verify rho_eff/B_eff statements and no sqrt/source admission” is respected: the symbols are definitional regroupings, not measured residuals.

`zero_bias_corollary` is a substitution lemma. Positive weights or small energy do **not** imply `B_eff = 0`.

## 3. What this child does *not* close

Still open and not claimed here:

- pinned toolchain compile, exit code, `#print axioms`, placeholder scan of this file or of `NEW_P4_032_WeightedThreeTerm`
- binding of `Weights`, `rhoA`, `tau`, `kappa*`, `bias*` to one certified cell/metric/normalization
- identification of `energy` with a named port-energy source
- true-DH / Float64 / interval enclosure / domain coverage
- absorption of `rho_eff energy + B_eff` into a storage or Schur remainder
- P4/M4 closure or registry admission

Queue owner for compile/repair remains `巨阳仙尊`. This proportional-lane file only records the typed boundary.

## 4. Integration note

Integrator should treat this inbox file as documentation-only routing:

- keep the sidecar `OPEN_UNCOMPILED` until a Lean slot returns exit code and axioms;
- do not promote `rhoEff` / `biasEff` to a verified residual envelope;
- do not merge force and accel consumers;
- next mathematical leaf is a same-instance envelope binding for `ED`/`EB`;
- next Lean leaf is compile + axioms + sorry/admit scan of this sidecar and its weighted parent only.

`admission_label: architecture_only`.
