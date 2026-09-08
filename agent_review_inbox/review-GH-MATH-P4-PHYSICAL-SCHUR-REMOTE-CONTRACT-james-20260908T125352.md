---
kind: review_result
review_id: review-GH-MATH-P4-PHYSICAL-SCHUR-REMOTE-CONTRACT-james-20260908T125352
task_id: GH-MATH-P4-PHYSICAL-SCHUR-REMOTE-CONTRACT
source_agent: James-local-takeover
created_at: 2026-09-08T12:53:52-06:00
inspected_commit: dc0e6b77c1c9eb8162517198e1ccc0dd62451059
status: pending
integration_status: pending
admission_label: pending
proof_status: ANALYTIC_SLAB_CHECKED_ACTUAL_REMOTE_BINDING_OPEN
source_binding_proven: false
runtime_verified: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: bind actual remote acceleration or remote forcing with explicit defect on the same cell; do not feed an additive port cap into a homogeneous residual consumer
---

# Physical Schur: executable analytic candidate, missing remote forcing contract

## 1. Outcome and scope

Located an existing executable **full six-state-coordinate analytic slab checker**
and ran it once on the existing vanis2 payload. It validates rational mass/force/
acceleration enclosure arithmetic, not actual Float64 dynamics or a formal
covered-cell theorem. The missing contract is more precise than "no remote
bound exists": an analytic candidate exists, but its actual-source refinement,
cell/consumer binding and homogeneous residual premise remain open.

This review does not repeat a q=0 projection obstruction. Section 5 gives a
different logical countermodel with bounded remote force, positive definite
full mass and positive Schur complement on a nonzero abstract interval cell.
It is NOT a robot/source witness or a synthetic helper pass.

Only this immutable review is added. No source, sidecar, producer, prior review,
state, registry or formal gate is changed. No Julia, Lean, Monte Carlo, solver,
full regression, new capture, or generated source packet was executed.

Let E denote
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
External paths below are relative to E. Workflow HEAD is inspection context,
not a claim that these external files belong to that commit.

## 2. Actual source edges located

1. `routeB_dense_Mq/dhport_lib.jl:102-109` computes M, Cdq, Gq, G0 and
   `F=tau-Cdq-Gq`, then returns `M \ F`. The actual solve does not expose a
   certified zero defect. For a selected real source model use `z=M*a-F` and
   carry z explicitly; runtime/model refinement is needed to bound it.
2. `routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl:16-70`
   fixes B=(4,5,6), D=(1,2,3), mu=1/1000000, mass blocks and nominal reference.
   It imposes `M_DD v_D + DeltaM_DB a_B = 0`, `r_B=M_BD v_D`, and
   `l_total=l_base+r_B` as descriptor equalities. No source valuation identifies
   v_D with actual remote acceleration, or proves the homogeneous balance.
3. `routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.jl:105-140`
   reads a q2..q5 cover row, fixes q1=q6=0 and encloses
   `R=-M_BD M_DD^-1 DeltaM_DB`. Its `rho2_m0_upper` uses the matching nominal
   inverse metric (lines 169-184), but bounds **R a_B**, not arbitrary
   `M_BD a_D` or a forced remote equation. The cover CSV contains no dq, w,
   a_D or F_D enclosure fields. Do not infer that an actual full-state point
   belongs to this slice; extension requires an explicit independence or
   domain-inclusion argument, not matrix field-name matching.
4. `robot_formal_v1/exact_checks/initial_analytic_slab.py:12-50` constructs
   full 6x6 analytic mass intervals, all six force intervals, and all six
   acceleration caps. The selected payload has angle radii
   `(9/20,19/50,37/100,19/50,37/100,9/20)`, velocity radius 3,
   measurable |w|<=2, initial full-ball radius 3/20 and time step 1/512.
   It uses mu=1/1000000 and the stated DH design gains, but analytic C/G,
   not a proved interpretation of the runtime finite-difference calculation.

Different B/D partitions cannot be spliced: the older physical-acceleration
lift with B=(4,5), D=(1,2,3,6) is not this 3+3 block456 contract.

## 3. Small executable route that really exists

Executed exactly one existing independent checker, without running its producer:

```powershell
python -B -c "import runpy; m=runpy.run_path('C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/exact_checks/check_initial_analytic_slab.py'); m['main']('half_active_vanis2_domain_probe.json')"
```

Exit 0; stdout: `INDEPENDENT_ANALYTIC_FIRST_SLAB_CHECK_OK 1/512`.
This ordinary Python run used assertions enabled. No -O result is claimed.
The checker independently reads the three analytic mass/gravity/Coriolis CSVs,
checks their payload hashes and recomputes rational intervals. It checks
`C >= |I-XM|`, positive weights with `C w <= kappa w`, `kappa<1`,
`|XF|<=d`, `d+C alpha<=alpha`, and the recorded first-slab endpoint inequalities.
Here C is the nonnegative comparison matrix, NOT the Coriolis matrix.

Mathematically these premises imply, for the exact analytic equation M a=F,
invertibility and `|a|<=alpha` by the weighted contraction/positive inverse
argument. They do not prove that an actual runtime a solves that equation.
For `M a=F+z`, replace d by an enclosure of `|X(F+z)|` and re-establish the
supersolution; silently retaining the old d is unsound.

On that SAME analytic cell, the direct port route can use

```text
c_i = sum_(j in D) sup_cell |M_ij| * alpha_j, i in B,
|p_B,i| <= c_i, where p_B=M_BD a_D.
W = sum_(i,j in B) |H_ij| c_i c_j,
p_B^T H p_B <= W.
```

This needs the actual acceleration refinement, matching H, and the exact
consumer residual definition. It is an additive cap, not a relative gain.
No W was exported or presented as an actual source bound here. For a smaller
covered cell, prove inclusion in this slab and use the same source/configuration;
for cells outside it, the checked slab supplies no bound.

## 4. Full-state elimination contract, including signs

Fix one cell Omega, disjoint exhaustive block indices, units, controller,
regularizer, source interpretation and reference. Let z=M a-F. At EVERY state
of Omega require the actual block equations and a valid inverse J of M_DD:

```text
M_BB a_B + M_BD a_D = F_B + z_B,
M_DB a_B + M_DD a_D = F_D + z_D,
J M_DD = M_DD J = I.
```

Then, with L=M_BD J,

```text
a_D = J(F_D+z_D-M_DB a_B),
p_B = L(F_D+z_D) - L M_DB a_B,
(M_BB-L M_DB) a_B = F_B+z_B-L(F_D+z_D).
```

The remote forcing enters the condensed RHS with a MINUS sign. SPD/PSD of
the Schur complement alone does not bound that RHS.

To recover the producer's Delta form without assuming it, define
`g_D=F_D+z_D-M0_DB a_B`. If v_D is actual a_D, then

```text
M_DD a_D + DeltaM_DB a_B = g_D,
p_B = R a_B + L g_D,
R=-L DeltaM_DB.
```

Thus the existing homogeneous R budget applies to the actual port only if
`g_D=0`, or after bounding the additional `L g_D` term. If v_D instead means
an acceleration deviation, its reference identity and shifted g_D must be
derived explicitly; it cannot be renamed a_D.

Minimal alternatives for a caller:

- Direct route: actual `|a_D|<=alpha_D` and same-cell M_BD enclosure.
- Eliminated route: same-cell inverse/solve enclosure plus bounds on
  `F_D,z_D,a_B`, retaining all correlations or enclosing them safely.
- Centered route: actual v_D/reference identity and a bound for g_D. With
  `||R a_B||_H^2<=gamma E_B` and `||L g_D||_H^2<=Delta`, Young gives
  `||p_B||_H^2 <= (1+theta)gamma E_B+(1+1/theta)Delta` for theta>0.

The consumer must separately identify its residual with local terms plus the
SIGNED port (and any additional defect). Condensed RHS and positive port use
opposite signs; do not count z or the remote port twice.

## 5. Minimal exact countermodel: bounded remote forcing is not homogeneous gain

Take an abstract cell xi in [1,2], not a robot q=0 slice. Use one B and one D
coordinate and constant rational mass

```text
M = [[2,1],[1,2]],  a_B=0,  a_D=xi/2,
F_B=xi/2,          F_D=xi,  z_B=z_D=0.
```

Both full block equations hold identically. M is SPD since
`(x,y)^T M (x,y)=x^2+y^2+(x+y)^2`; M_DD=2 and the Schur complement is 3/2.
All forces and accelerations are bounded on this cell, yet
`p_B=M_BD a_D=xi/2` is strictly positive when a_B=0. Therefore for EVERY finite
beta the homogeneous claim `p_B^2<=beta^2*a_B^2` is false. At xi=1 it reads
`1/4<=0`. Choosing nominal M0_DB=M_DB makes Delta=0 and R=0, while the missing
`L g_D=xi/2` remains. This pinpoints the omitted forcing, not a q=0 projection.

The exact algebra above is proved by substitution on paper in this review;
no synthetic Fraction helper or Lean run is used. It refutes the GENERIC
implication from SPD/block-only information to homogeneous port gain, not a
particular robot trajectory or source-bound certificate.

`ExplicitResidualEnclosure.sq_le` in the current physical Schur consumer requires
`residual(state,y)^2 <= beta^2*y^2` for every state and y. A bounded remote
acceleration supplies an additive cap but not this premise: y=0 requires the
residual to vanish. To use the existing consumer unchanged, supply a genuinely
centered proportional residual-action identity and bound. Otherwise an additive
budget consumer is required; this review does not implement or silently select it.

## 6. Admission blockers and minimum reopen packet

The packet must contain ONE cell/configuration key and actual state embedding;
M_BD/M_DB/M_DD and F_D source identities; a_D or inverse/remote-balance witness;
runtime/model defects if applicable; H/reference and residual sign convention;
the corresponding additive or homogeneous budget; and target/coverage binding.

The located analytic slab cannot be joined to a q-only producer row merely by
matching gains. Cell inclusion, q1/q6 treatment, FD/analytic force refinement,
regularizer interpretation, controller runtime values, and the physical residual
valuation are still missing. No complete actual covered-cell packet was found
in these inspected sources. Status remains pending; no formal or registry gain.

## 7. Current byte provenance

SHA-256 values were computed from the files read this turn. The analytic checker
also checked the payload's three CSV content hashes; this is content consistency,
not source execution authenticity or a theorem receipt.

| Path relative to E (except workflow consumer) | SHA-256 |
|---|---|
| routeB_dense_Mq/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl | 9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79 |
| routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.jl | 62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129 |
| routeB_dense_Mq/routeB_compact_qbox_cover_depth3.csv | 85b907bf8d12f46ee003731c5518a00a9a106c8f5a12e492037ae8fc52b04fdf |
| robot_formal_v1/exact_checks/initial_analytic_slab.py | 97c96fb01bc9318af258a75d6b1371e3eef665fa760f401ce9f5a422ca164998 |
| robot_formal_v1/exact_checks/check_initial_analytic_slab.py | efa9f57d42e6cd70bd0cc5afdeef68a35673a880f5c53e992a2a182c4ca36340 |
| robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e |
| workflow: examples/routeb_physical_schur_binding_lean/PhysicalSchurBinding.lean | bf9678f8595c03006eaa2eb99a7398599468fb88f669553ea312686019558adf |

Existing concurrent changes to state and other agents' reviews were observed
and left untouched. No integration script was invoked.
