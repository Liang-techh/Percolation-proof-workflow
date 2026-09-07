---
kind: review_result
task_id: T-P5-026
review_id: review-T-P5-026-juyangxianzun-20260907T1048
agent: 巨阳仙尊
source_agent: 巨阳仙尊
math_source_agent: 古月方源
related_math_review: review-T-P5-026-guyuefangyuan-20260907T1031
created_at: 2026-09-07T10:48:00-06:00
status: compiled_candidate
integration_status: pending
---

# T-P5-026 Lean formalization result — 巨阳仙尊

## Scope

This review formalizes the source-independent part of 古月方源's feasible-cone/SPN small-gain result. It does **not** bind a concrete `K_path`, does not search 18 rational cone certificates, and does not claim Julia/Float64 semantics, P8 coverage, ODE continuation, P5/M4 closure, registry admission, or final integration.

Claim record:

- `agent_review_inbox/claim-T-P5-026-juyangxianzun-20260907T1029.md`

Portable sidecar:

- `examples/routeb_p5_feasible_cone_spn_lean/P5FeasibleConeSPN.lean`
- `examples/routeb_p5_feasible_cone_spn_lean/README.md`
- `examples/routeb_p5_feasible_cone_spn_lean/verify.sh`
- `examples/routeb_p5_feasible_cone_spn_lean/lean-toolchain`

Lean toolchain is pinned to `leanprover/lean4:v4.32.0`; `verify.sh` discovers `lake` from `PATH`, checks the repository `examples/local_fkg/lake-manifest.json`, and is registered with `CI_PORTABLE=1`.

## Formalized theorem decomposition

### 1. Physical six-cone cover

`channel_cone_cover (x y : ℝ)` proves that every pair belongs to one of the six explicit feasible parametrizations with `a,b ≥ 0`:

```text
(x,y) = ( a,       b)
      | (-a,      -b)
      | ( a+b,    -a)
      | ( a,    -a-b)
      | (-a,     a+b)
      | (-a-b,     a).
```

This is the physical compatibility reduction for the signs of `(x,y,x+y)`; the two impossible formal sign triples are never introduced.

`two_channel_cone_cover` applies the theorem independently to channels 4 and 5 and produces the exact 36-cone product cover before global-sign pairing.

### 2. Generic finite quadratic/SPN leaves

The sidecar defines an explicit finite-sum quadratic

```text
quad M u = sum_i sum_j u_i M_ij u_j
```

and a minimal PSD-facing premise

```text
IsPSD S := forall u, 0 <= quad S u.
```

It proves:

- `quad_add`;
- `entrywise_nonnegative_quadratic_nonnegative`;
- `spn_quadratic_nonnegative_on_orthant`.

The last theorem has the checker-facing statement:

```text
H_ij = S_ij + N_ij
IsPSD S
forall i j, 0 <= N_ij
forall i, 0 <= u_i
--------------------------------
0 <= quad H u.
```

Thus exact rational `LDL^T` witnesses can remain an upstream checker representation; the Lean consumer needs only the verified PSD quadratic premise and entrywise signs.

### 3. Global-sign invariance leaves

The sidecar proves:

- `quad_global_sign_invariant`:
  `quad M (-u) = quad M u`;
- `absEnvelope_global_sign_invariant`:
  simultaneous global sign reversal of the state and `Lz` leaves the direct absolute envelope unchanged.

These are the algebraic leaves behind pairing globally reversed feasible cones. The **concrete 36 -> 18 representative enumeration/equality table is intentionally still open**; no fabricated finite table is asserted without a concrete cone-index/checker object.

### 4. Direct component residual power consumer

With

```text
rowEnvelope K z a = sum_j K[a,j] |z_j|
absEnvelope K Lz z = sum_a |Lz_a| rowEnvelope K z a,
```

`component_residual_power_bound` proves

```text
forall a, |r_a| <= rowEnvelope K z a
-------------------------------------
|(Lz)^T r| <= absEnvelope K Lz z.
```

Notably, after the component envelope is supplied, the final consumer does not require a redundant separate hypothesis `K[a,j] >= 0`; nonnegativity of a concrete checker table remains a source/checker sanity obligation, not a logical dependency of this theorem.

### 5. Exact cone reduction

`exact_feasible_cone_reduction` proves the abstract exact equivalence

```text
(forall z, lhs z <= rhs z)
  <->
(forall feasible cone c, forall u>=0, 0 <= gap c u)
```

provided the cone family covers all states and `rhs(T_c u)-lhs(T_c u)=gap(c,u)` exactly on each cone.

This separates exact mathematics from the SPN sufficient representation.

### 6. Generic feasible-cone SPN small gain

`global_abs_envelope_of_spn` proves that a covering family of cone identities

```text
mu * Q(T_c u) - absEnvelope K (L(T_c u)) (T_c u)
  = quad (H_c) u
```

plus `H_c=S_c+N_c`, PSD `S_c`, and entrywise nonnegative `N_c` implies the global direct envelope

```text
absEnvelope K (L z) z <= mu * Q z.
```

`spn_feasible_cone_small_gain` then combines this with the component residual envelope to obtain

```text
|(Lz)^T r| <= mu * Q(z).
```

This is the source-independent formal core of the proposed 18-cone rational checker.

## GitHub Actions / focused compile

The sidecar was exercised by the real repository workflow:

- workflow: `.github/workflows/lean-agent-sidecars.yml`
- run: `34144219022`
- job: `101812603228`
- head SHA: `febdb3b65bed943f6b3c809d7269aaa05e1d2e94`
- Lean: `4.32.0`

The real job log contains the following lines for this sidecar:

```text
AXIOM_AUDIT=PASS
P5_FEASIBLE_CONE_SPN_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_feasible_cone_spn_lean/verify.sh
```

All 11 printed public theorems report only:

```text
[propext, Classical.choice, Quot.sound]
```

No `sorryAx` appears in this sidecar.

The shared workflow job nevertheless concludes red because **other independent sidecars** fail in the same all-sidecars loop. The same real log shows, among others:

- `examples/anthropic_flt_quotient_transport_sidecar/verify.sh`: bad `../local_fkg` working-directory path;
- `routeb_m4_cross_branch_budget_lean`: noncomputable definitions plus unused hypotheses;
- `routeb_p5_componentwise_relative_decay_lean`: three finite-sum/rewrite proof failures with `sorryAx`;
- `routeb_p5_weighted_dual_residual_lean`: unused `hκ1`, invalid projection from a disjunction, `sorryAx`;
- `routeb_p7_tail_schur_completion_lean`: open nonnegativity/linarith goals, `sorryAx`;
- `routeb_p8_ramp_reconstruction_sidecar`: missing interval-integral API/import/syntax and `sorryAx`.

Those are separately owned lanes and were not modified in this task.

## Dependencies and remaining formal obligations

Closed here:

- six physical single-channel cone cover;
- two-channel 36-cone product cover;
- generic orthant entrywise-nonnegative quadratic lemma;
- generic SPN orthant consumer;
- exact abstract cone-cover equivalence;
- generic component residual-power bound;
- generic feasible-cone SPN small-gain theorem;
- global-sign quadratic/envelope invariance leaves.

Still open:

1. A concrete finite `ConeIndex`/`T_C` object that enumerates the 36 physical product cones and identifies 18 global-sign representatives in Lean.
2. Concrete sign-fixed identity `|L(T_C u)|^T K|T_C u| = u^T(T_C^T B_C T_C)u` for the frozen P5 `L`, `P`, and future rational `K_path`.
3. Concrete source-bound nonnegative `K_path : Fin 2 -> Fin 4 -> ℚ/ℝ` on the same P8/first-exit domain.
4. Rational SPN decompositions for the 18 representatives and exact rational PSD/`LDL^T` witness checking.
5. Float64/controller/solve discontinuous defects and genuine anchor bias remain on the additive-bias branch unless separately centered.
6. P8 same-domain coverage, initial binding, and ODE continuation remain independent.

Failure to find an SPN decomposition for a future concrete `K_path` is **not** a mathematical counterexample to copositivity; the checker must remain fail-closed and may fall back to T-P5-025 global PSD or T-P5-024 scalar `ell2` consumer.

## Status

`compiled_candidate` only.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
