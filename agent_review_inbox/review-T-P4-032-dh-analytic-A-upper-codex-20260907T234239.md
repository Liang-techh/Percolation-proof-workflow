---
kind: review_result
review_id: review-T-P4-032-dh-analytic-A-upper-codex-20260907T234239
task_id: T-P4-032
agent: Codex-P4-math-lane
source_agent: Codex-P4-math-lane
created_at: 2026-09-07T23:42:39-06:00
inspected_commit: d7f5af8fa96d7345a5370979e5f91d54b8e3f848
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHAnalyticAUpper.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHProducerBaseBridge.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ExactCellLambdaConsumer.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_NormalizedTargetGuard.lean
related_tasks:
  - T-P4-039
  - T-P4-040
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.same_cell_DH_analytic_A_upper
requested_action: retain the exact analytic residual envelope and acceleration-domain obstruction as pending mathematical evidence; obtain a same-source acceleration bound before constructing RationalCharges.A_upper; do not promote registry status
---

# Concrete analytic A_upper route from existing source/descriptor documents

The inspected documents do not supply an independently proved same-cell D_lower or a numerical acceleration envelope suitable for line 9. They do supply a concrete source formula and identify the missing domain inequality. From that formula this round derives an exact global polynomial estimate, then a conditional rational A_upper field. No sample/empirical bound or unrelated cell constant is imported.

## Source/document finding

External base: `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.

- `P5_COMPACT_DBASE_MAPPING.md` defines `l_base=F_B-B0*a_B` and the distinct dissipation expansion `D_aug=D_base+h'r_B+s_res*r_B'r_B`. It requires a complete acceleration descriptor or an independent acceleration-domain generator. It provides an interface, not a lower bound on the consumer's b_base.
- `P5_COMPACT_PMI_ACCEL_ENVELOPE_INTERFACE.md` explicitly proposes `g_a=A_bar-a_B'B_up*a_B≥0`, with A_bar a fixed rational established independently from the true DH model. It explicitly says the interface itself is not such a bound and rejects an empirical maximum.
- `P5_COMPACT_DIRECT_DESCRIPTOR_STRUCTURE_DH.md` supplies the chosen DH branch and algebraic residual/port identities, with no nonnegativity or coverage claim.
- `P5_COMPACT_TWO_STAGE_RESIDUAL_BRIDGE_AUDIT.md` calls beta_a=1/100, beta_x=1/10 and beta_w=1/20 placeholders pending independent Stage-R verification. They cannot be substituted for A_i or D_i.

No Dbase-to-b_base equality, complete storage lower bound or certified acceleration cap was found in this bounded document chain. This is not a claim that no future/source-specific certificate can provide them.

## Exact inequality derived from the same DH polynomial

Use the already transcribed compact-DH lBase and the SAME nominal inertias and producer metric:

`l_base=F-M0*a`, `M0=diag(350003/3000000,200739/4000000)`,

`M=A_up=(1402217/12000000)a4²+(200739/4000000)a5²`.

For the two four-term nominal-force components, Cauchy gives

`||F||²≤(16/5)p45+(1/5)w²`.

The exact inertia comparison is `2||M0*a||²≤M/4`. Its coefficient slacks are respectively

`8955743741/4500000000000 > 0`,
`60073353879/8000000000000 > 0`.

Combining `||F-M0*a||²≤2||F||²+2||M0*a||²` therefore yields the global polynomial inequality

**`||l_base||²≤(32/5)p45+(2/5)w²+M/4`.**

This is an exact analytic derivation, not an existing verified physical inequality copied from a record. It needs no source-domain premise as an identity/inequality for the transcribed polynomial, but identifying that polynomial with the actual residual still needs the source bridge.

On any ONE cell with proved `p45≤28/5`, `w²≤3` and `M≤K_i`, it specializes to

**`||l_base||²≤926/25+K_i/4`.**

The disturbance bound must be proved in the same source domain (for example from an explicitly bound ramp and time interval); it is not inferred solely from a similar manifest label. Choosing a nonnegative rational K_i gives a nonnegative rational cap A_i=926/25+K_i/4, or any larger rational. This is deliberately conservative and is not optimized.

## Exact type connection

The new `NEW_P4_032_DHAnalyticAUpper.lean` contains `dh_residual_analytic_upper`, `conditional_cell_A_upper`, and `rational_A_upper_field`. The last theorem has exactly the A_upper field shape for `SameSourceCharges (source key D base) c`, given same-cell p45/disturbance/acceleration bounds and the rational scalar comparison `926/25+K_i/4≤c.A i`.

This completes only that conditional field constructor. `RationalCharges` still needs P_i, D_i and its positive target; `SameSourceCharges` still needs port/base inequalities and a cover. Neither a common rational lambda nor a target is established by a large A_i cap.

After those separate obligations and the rational guard are proved, `NormalizedTargetGuard` still requires same-state residual/nominal/gain-beta normalization and `0<T≤nu*t` for a prescribed P4 target T. The new A_upper estimate supplies no D_lower and no normalization factor.

## Minimal missing inequality and exact obstruction

The immediate missing domain premise is **`A_up(x)≤K_i` on the same full source cell**, or a proved descriptor restriction that directly controls l_base. Geometry alone cannot supply it.

For any proposed finite cap C≥0, take the formal acceleration ray q=v=w=0 and

`a4=(3000000/350003)(C+1)`, `a5=0`.

Then p45=0, w²=0 and the producer's four-angle geometry holds, but the exact source polynomial gives `||l_base||²=(C+1)²>C`. `no_cap_from_angles_and_block_only` encodes this counterexample for every C≥0. It is not asserted to satisfy the full physical acceleration equations; that distinction is exactly why a complete descriptor or independent acceleration bound is needed.

This identifies a concrete missing inequality rather than repeating an abstract missing-field list. The reported generator `g_a` would supply it only after independent proof and source/domain binding; no arbitrary K_i is selected here.

## Checks and provenance

- Read the cited documents and existing local typed interfaces only. No producer, solver, sampling routine, Lean/Lake or regression was executed.
- Two inertia slack fractions were checked with exact BigInt rational arithmetic (no floating-point arithmetic). The four-term Cauchy and source-coefficient comparisons were reviewed algebraically.
- PowerShell text/hash inspection of the new 107-line Lean file returned exit code 0, with 0 proof placeholders and 0 trailing-whitespace lines. This is not elaboration/axiom verification. The new file remains OPEN_UNCOMPILED; no registry action occurred.

| Artifact | SHA-256 |
|---|---|
| `NEW_P4_032_DHAnalyticAUpper.lean` | `6b1db125678b95ed08bf19f94f350b9c227681bc72a3d16fa3b8aacb4664d6cc` |
| `P5_COMPACT_DBASE_MAPPING.md` | `aa3601ec85bfe2f7acb71c6bd1edc8c0044b05feeab52cd4bf3c85233f433268` |
| `P5_COMPACT_PMI_ACCEL_ENVELOPE_INTERFACE.md` | `b89c263c83219b69934cbaf25d5ae52bbf3818b5826c3daf9ad8b10574da6a59` |
| `P5_COMPACT_DIRECT_DESCRIPTOR_STRUCTURE_DH.md` | `69e53ddd1a34d19ae96517d30a8cbd9817b478ab1c6ef5e29648fed8c03c63d8` |
| `P5_COMPACT_TWO_STAGE_RESIDUAL_BRIDGE_AUDIT.md` | `76cce05743180b6a5b4dfc044010812b4da6373f74856c9567c010557f75a5a6` |

Disposition: **pending/open**. This is a constructive analytic A_upper route plus an exact obstruction to omitting its acceleration-domain premise; no concrete complete cell certificate is admitted.
