---
kind: review_result
task_id: T-P4-018
review_id: review-T-P4-018-juyangxianzun-20260907T0546
agent: 巨阳仙尊
source_agent: 巨阳仙尊
status: compiled_candidate
parent_review: review-T-P4-018-liuguanyi-20260907T0522
claim: claim-T-P4-018-juyangxianzun-20260907T0532
final_integration: false
registry_mutation: false
---

# T-P4-018 Lean result — nominal/acceleration-style to generalized-force coordinate congruence

## Scope

This review formalizes the source-independent mathematical interface proved by 柳冠一 in `review-T-P4-018-liuguanyi-20260907T0522.md` and its companion log. It does **not** re-prove the source semantics, authenticate Julia/Float64 execution, mutate P4/M4 state, or perform admission/provenance work.

Portable sidecar:

- `examples/routeb_p4_force_coordinate_congruence_lean/P4ForceCoordinateCongruence.lean`
- `examples/routeb_p4_force_coordinate_congruence_lean/README.md`
- `examples/routeb_p4_force_coordinate_congruence_lean/verify.sh`
- `examples/routeb_p4_force_coordinate_congruence_lean/lean-toolchain`

The verifier is tagged `CI_PORTABLE=1`, locates `lake` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, requires the pinned `examples/local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, requires an axiom report for every exported theorem, and rejects `sorryAx`.

## Formalized theorem decomposition

The sidecar exports eleven focused results.

1. `kc_force_normalization` proves the exact two-layer map

   `diag(1/5,1/10) * (q5/20,q4/20) = (q5/100,q4/200)`.

2. `schur_coordinate_congruence` proves the division-free scalar transport theorem. Under

   `xA = j*xF`, `rF = j*rA`, `pF = j^2*pA`,

   Lean proves exactly

   `pF*xF^2 + 2*xF*rF + d*y^2 = pA*xA^2 + 2*xA*rA + d*y^2`.

   Thus the nominal/acceleration-style and generalized-force Schur calculations are the same quadratic form when the coordinate scale is transported consistently.

3. `mixed_normalization_residual_bound` proves the typed mixed-coordinate envelope. If

   `|eA| <= betaA*|y|`, `|eF| <= betaF*|y|`, `j>=0`, `c>=0`,

   then

   `|j*(c*y+eA)+eF| <= (j*(c+betaA)+betaF)*|y|`.

4. `mixed_normalization_extremizer` gives an aligned `y=1`, `eA=betaA`, `eF=betaF` equality witness for nonnegative coefficients. Hence the mixed coefficient is attained when the two independent remainder envelopes align; it is not merely a loose artifact of the proof.

5. `channel4_kc_force` proves `(1/5)*(1/20)=1/100`.

6. `channel5_kc_force` proves `(1/10)*(1/20)=1/200`.

7. `channel4_positive_coefficient_transport` proves the exact congruent positive coefficient identity

   `3/5 = (1/5)^2 * 15`.

8. With

   `d4 = 116667666666667 / 1000000000000000`,

   `channel4_force_margin` proves

   `(3/5)*d4 - (1/100)^2 = 349503000000001 / 5000000000000000`.

9. `channel4_margin_congruence` proves the acceleration-style margin is exactly twenty-five times the force-coordinate margin:

   `15*d4 - (1/20)^2 = 25*((3/5)*d4 - (1/100)^2)`.

10. `channel4_force_margin_pos` proves the force-side isolated-`kc` margin is strictly positive.

11. `channel4_mixed_quarter_envelope` gives the source-facing mixed budget. If

    `(1/5)*betaA + betaF <= 6/25`,

    together with the two component envelope hypotheses, then

    `|(1/5)*((1/20)*y+eA)+eF| <= (1/4)*|y|`.

    This is the exact typed bridge into the already-used force-side quarter consumer: acceleration-style remainder costs are scaled by `1/5`, while native generalized-force remainder costs are not scaled again.

## Real GitHub Actions loop

The sidecar was not declared successful from inspection alone; it went through the requested CI repair loop on the repository-pinned environment.

### Attempt 1

- Actions run: `34117033875`
- Job: `101726245513`
- Environment: Lean `4.32.0`, pinned local-FKG Lake environment.
- Failure: `-DwarningAsError=true` rejected the proof tail in `mixed_normalization_extremizer` because `convert ... <;> ring` triggered the linter (`Used tac1 <;> tac2 where (tac1; tac2) would suffice`).
- Action: replaced the linter-triggering tactic rather than disabling the linter.

### Attempt 2

- Actions run: `34117439280`
- Job: `101727434166`
- Commit under test: `152aa549f9999de3834115155c8861dfffc79c2a`.
- Failure: the replacement `exact abs_of_nonneg hsum` exposed a real target-shape mismatch: Lean expected the right-hand factor `(...)*1` while the lemma produced `...` directly. The failed theorem correctly showed `sorryAx` in its axiom report because compilation had not closed it.
- Action: changed the proof to `simpa only [abs_one, mul_one] using abs_of_nonneg hsum`.

### Attempt 3 — focused sidecar PASS

- Actions run: `34117911622`
- Job: `101728931585`
- Commit under test: `3bd258327b3cb6cec503226ecab2f15c3a9458e9`.
- Environment recorded by CI: Lean `4.32.0`, Lake `5.0.0-src+8c9756b`, pinned `examples/local_fkg/lake-manifest.json`.
- The sidecar emitted:

  `AXIOM_AUDIT=PASS`

  `P4_FORCE_COORDINATE_CONGRUENCE_FOCUSED_CHECK=PASS`

  `SIDECAR_RESULT=PASS path=examples/routeb_p4_force_coordinate_congruence_lean/verify.sh`

All eleven exported declarations reported only

`[propext, Classical.choice, Quot.sound]`

and none reported `sorryAx`.

The shared `Lean agent sidecars` workflow remains red for unrelated pre-existing lanes: `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` still uses a bad `../local_fkg` relative path, and `examples/routeb_p5_weighted_dual_residual_lean` still has the existing unused-`hκ1` / invalid-disjunction-projection errors with corresponding `sorryAx`. This T-P4-018 sidecar itself is explicitly PASS; those independent tasks were not claimed here.

## Interface boundary / remaining obligations

This result closes only the pure coordinate mathematics. The physical/source layer still has to provide a typed classification for each execution remainder before the mixed theorem can be consumed safely:

- label each bound as **acceleration-style** (to be multiplied by the appropriate `I_B` scale) or **native generalized-force** (already in `l_F` units);
- bind the literal source `I_B=diag(1/5,1/10)` and the PMI nominal `kc=(q5/20,q4/20)` to the same source snapshot/domain;
- produce same-domain `betaA`, `betaF` bounds for the relevant remainder components;
- keep Julia/Float64 solve/model/controller/central-FD execution errors separate until their coordinate units are established;
- connect those typed bounds to the appropriate generic P4 Schur consumers and to P8 same-domain coverage.

A source checker must not multiply a native force-coordinate error by `I_B` a second time, and it must not omit `I_B` for an acceleration-style error. The theorem `channel4_mixed_quarter_envelope` makes this bookkeeping explicit through `(1/5)*betaA + betaF <= 6/25`.

## Status

`compiled_candidate` only. No P4/M4 state change and no registry mutation is claimed.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
