---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-BUDGET-CLOSURE-20260908T105720
task_id: GH-MATH-P4-SCHUR-BUDGET-CLOSURE
source_agent: Codex-signed-source-packet-audit
created_at: "2026-09-08T10:57:20-06:00"
inspected_commit: 03ef9a97394449967e2b29fbc984ebd3d565e957
integration_status: pending
admission: pending
admission_label: pending
status: SAME_CONFIGURATION_SIGNED_PROJECTION_WITNESS_MISSING
source_binding_proven: false
actual_residual_cap_proven: false
packet_constructed: false
merge_decision: refuse_as_completed_source_closure
lean_compile_status: not_run
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
predecessor_review: agent_review_inbox/review-GH-MIXED-schur-absorption-reassigned-20260908T105121.md
predecessor_sha256: 13DFD890298527FDF5D6AC36B72C8AB3B99161622FB575B72D90E43E407D61C7
requested_action: obtain one source/configuration residual chart and signed dual-projection enclosures; do not splice old analytic absolute remainder data into actual Schur binding
---

# Schur budget closure: a dependent same-source packet, still unfilled

## 1. Outcome

The requested continuation consumes the signed-defect result supplied as
revision802 through its hash-pinned predecessor, not by reading or editing state.

A complete same-source packet for E_A, ell, r0, actual defect d, H, beta and t
was NOT found among the inspected DH/analytic artifacts. The first missing
item is an actual residual chart with authenticated configuration and complete
defect, followed by matching signed projection bounds. The missing proof is
not another generic Young inequality.

This review gives a precise dependent packet and a smaller dual-projection
interface. No synthetic packet is constructed by defining conveniently named
functions. No source closure, actual cap or physical counterexample is claimed.
Only this new review is written.

## 2. Bind objects once, instead of joining independent scalar certificates

Fix a configuration kappa and one complete state domain Omega. Configuration
includes source bytes, loaded/model coefficient semantics, controller branch,
regularizer exactly once, FD versus analytic versus decoded runtime meaning,
block order, reference acceleration/model and force-defect sign convention.

All fields below are functions of this same (kappa,x), x in Omega:

| Field | Required identity / role |
|---|---|
| a_C | actual/reference acceleration projection used by BOTH port construction and E_A |
| E_A | specified energy, e.g. a_C^T B_up a_C; B_up and nonnegativity source-bound |
| ell | specified nominal force residual, not the affine-observable covector from adjugate work |
| r0 | specified nominal port R a_C or a separately bound nominal residual |
| d | actual minus nominal port, with all model/FD/controller/solve corrections assigned once |
| r_actual | r0+d, with equality to the intended actual source residual |
| l_actual | ell+r_actual, tied to the intended total residual, not just a new definition |
| H | the same symmetric positive-definite force metric in ALL inner products, e.g. the correctly ordered regularized nominal M0_CC inverse |
| beta | actual budget polynomial/evaluator of the target builder; not interchangeable with feedback base |
| t | requested target in exactly the same units, normalization and domain |

Only AFTER these identities define
L=ell^T H ell, c0=ell^T H r0, Q0=r0^T H r0,
u=ell^T H d, s=(ell+r0)^T H d, D=d^T H d,
Qactual=r_actual^T H r_actual,
P0=beta-(ell+r0)^T H(ell+r0),
Pactual=beta-l_actual^T H l_actual.

The minimal scalar signed witness then is:

    u <= U,  s <= S,  D <= Dcap,
    2U <= beta-L-2c0-E_A,
    2S+Dcap <= P0-t.

Or, more minimally, directly certify the two correlated expressions
2u<=beta-L-2c0-E_A and 2s+D<=P0-t.
The latter avoids splitting s and D at all.
These supply the predecessor's binding and direct-target gates. Every bound
must quantify over the same domain, not merely have numerically compatible endpoints.

For the legacy AbsorbedAt route additionally require
Qactual<=rho E_A+B, E_A>=0, delta>0, rho+delta<=1.
If obtaining target solely from that floor, require t+B<=delta E_A.
A directly proved target gate does not need this extra conservative floor.
FeedbackBinding remains a separate premise and is not introduced by this packet.

## 3. Where the current artifact join fails

External root P is
C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized.

### Source/chart anchor

The recent ACTUAL-THREE-ROW-WITNESS refresh records that actual preconditioned
rows456, signed weighted constraints and physical rows remain unproved.
Its corrected-builder artifact is a SPECIFICATION, not an executed correction.
This turn's targeted interval_bounds filename search for *force*dh*v2* also
found no matching file; no claim is made about all possible paths on the machine.

Therefore neither actual d nor its signed projections may be supplied from
that specification. A coordinate transform or corrected polynomial expansion
does not prove actual acceleration makes the descriptor zero or a bounded defect.

### Existing remainder artifacts

Fresh metadata/domain reads show:

| Artifact | Actual content | Not the requested source witness |
|---|---|---|
| descriptor_defect_contribution_audit_v1.json | EXACT_DECOMPOSITION_OF_EXISTING_BOUND_NOT_NEW_FLOWPIPE; gravity/coriolis/mass_variation contributions to existing acceleration bounds | actual d, signed u/s, same-H defect norm |
| combined_descriptor_remainder_v1.json | COMBINED_POLYNOMIAL_DESCRIPTOR_BOUND, formal=false; analytic CSV model, not a flowpipe; preconditioned and acceleration-remainder absolute arrays | actual FD/runtime residual or block456 metric projection |
| half_active_vanis2_domain_probe.json | RATIONAL_FIRST_NONLINEAR_SLAB, formal=false; analytic first-slab candidate, X, contraction data and acceleration radius | same-call actual defect or source row equation |

The first two artifacts enumerate exactly
initial_analytic_slab_v1.json, expanded_analytic_slab_v1.json,
adaptive_domain_0_v1.json, adaptive_domain_1_v1.json, adaptive_domain_2_v1.json.
They do not list half_active_vanis2_domain_probe.json.
Their transfer would require domain inclusion AND source/chart compatibility;
shared dimension or labels do not establish either.

The decomposition JSON has no top-level formal or scope field; missing values
are not silently treated as false/true. Its explicit status already limits
it to decomposition of existing bounds.

Fresh reading of descriptor_defect_contribution_audit.py shows that its
contribution map is (I-C)^-1 |X| applied to nonnegative force-component bounds.
It checks an algebraic supersolution relation and sums those components back
to existing acceleration_remainder_abs. This matrix is not H=M0_CC^-1.
The absolute X operation loses signed cancellation; it cannot recover the sign
of ell^T H d or (ell+r0)^T H d.

With suitable source and metric conversions, absolute bounds could still supply
conservative symmetric signed bounds. But those conversions and actual residual
meaning are absent. The issue is not that absolute bounds are intrinsically
invalid; it is that their existing semantics cannot be relabeled as this packet.

### Budget anchor

The current block456 E_A=Aup, betaC, nominal lBase/rC/lT and metric are defined
in a distinct symbolic descriptor/Schur interface. A legacy analytic slab's X
or comparison operator is not that metric, and its acceleration remainder is
not automatically the block port defect.
No fresh numerical constant, domain merge, or phantom correction was introduced.

## 4. Smaller signed witness through a source-bound affine defect chart

An implementation need not first certify every physical force row as zero,
nor estimate a generic inverse norm. A conditional alternative is to prove,
for the SAME configuration and x,

    d = A y + b,

where y is an authenticated measured/defined source defect vector and A,b
include the actual reference/force convention. If y=Xz for a physical residual
z, both that identity and the exact map from z to d must be proved.
In general a source reference correction creates b≠0; do not suppress it.

Then, using symmetric H, set

    w_u = A^T H ell,
    w_s = A^T H (ell+r0).

The exact projections are

    u = ell^T H b + w_u^T y,
    s = (ell+r0)^T H b + w_s^T y.

For certified same-point signed intervals lo_j<=y_j<=hi_j,
a direct support-function enclosure is

    u <= ell^T H b + sum_j max(w_u,j*lo_j, w_u,j*hi_j),
    s <= (ell+r0)^T H b + sum_j max(w_s,j*lo_j, w_s,j*hi_j).

This preserves coefficient signs and needs only TWO dual directions.
If w or b vary with x, a precomputed cell constant must certify the supremum
of the complete right-hand side; substituting one sampled direction is invalid.
The interval endpoints must enclose the actual same y, not old residual tokens.

D=(Ay+b)^T H(Ay+b) is another same-chart quadratic obligation.
For fixed A,b,H and a genuine rectangular y-box, convexity permits a maximum
at a vertex; this is a mathematical option, NOT a vertex computation run here.
Alternatively bound the combined 2s+D expression directly, preserving correlation.

Current artifacts provide neither this source-bound affine chart nor its actual
signed y enclosure. Defining y, A or b to force an identity without independent
bounds just renames the missing witness. No new producer/sidecar is written.

## 5. Conditional obstruction retained, not promoted

The predecessor's sharp defect-ball threshold remains an algebraic boundary:

    beta >= max(E_A+L+2c0+2sqrt(L)*epsilon,
                t+(sqrt(L+2c0+Q0)+epsilon)^2),

for a fixed nominal center and all d in the common H-ball.
It is not a necessary condition on a smaller actual source graph.

Its strict example H=1, ell=1, r0=0, d=1/4, E_A=1, beta=2, t=0
has actual cap Q=1/16, positive target P=7/16, but fails binding
E_A-Q=15/16<=P. This review does not re-execute or reinterpret it as a robot state.

For the present source join, the obstruction is precise:
same norm/absolute remainder data alone do not identify the actual signed
projections. Even in that abstract example, replacing d by -1/4 preserves
the defect magnitude and Q, while changing the binding outcome.
A same-H norm bound can justify the robust worst-case threshold, but cannot
certify favorable cancellation on the actual graph without the extra signed
source information. This distinction does not prove physical instability.

## 6. Reopen / admission boundary

To reopen source closure, submit ONE coherent witness with the fields in section2
and either directly certified signed expressions or the affine-dual route in
section4. Cite exact producer/config/domain identities and use the intended
actual source acceleration. A full runtime claim additionally needs loaded
configuration/assembly/solve/model refinement; an exact-model theorem must
state that different semantic target explicitly.

No current artifact fills this packet. Reject completion/source admission;
retain this review as pending with actual-source binding blocked.
Generic Young, the new scalar Lean-prep, corrected-builder specifications and
nonnegative bound decompositions are not substitutions for that missing packet.

## 7. Fresh hashes and checks

W=C:/Users/z5242/Desktop/重构版/工作流.
All entries below were hashed this turn; they bind bytes, not correctness.

| Path | SHA-256 |
|---|---|
| W/agent_review_inbox/review-GH-MIXED-schur-absorption-reassigned-20260908T105121.md | 13DFD890298527FDF5D6AC36B72C8AB3B99161622FB575B72D90E43E407D61C7 |
| W/examples/routeb_p4_schur_joint_threshold_lean/NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.lean | 91A3A598BA6C6FB0278A127C8B94A34839F74EB3CD88D46B6D2CA4D4169C5BA7 |
| W/agent_review_inbox/review-GH-MATH-P4-ACTUAL-THREE-ROW-WITNESS-codex-20260908T105206.md | A69099FC606C32FD7C2B4761E6B7CD73F30092641E6A7E217902DD93E2E838C4 |
| P/robot_formal_v1/interval_bounds/descriptor_defect_contribution_audit_v1.json | 65A4D583913E8CC7402A22B3AD5A09676FEC74E7251B48E491F9F82F13CBBFD9 |
| P/robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json | 68596F1557AA709D86BC8711ED7985552684DFFE7FDE290ABF03B511F6BD9805 |
| P/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |
| P/robot_formal_v1/exact_checks/descriptor_defect_contribution_audit.py | FBD6FF362469E3C353251870A9BBCD63AC467658234FB9163DD0FB36CDEAB984 |

Executed only read-only text/JSON metadata/domain inspection and SHA checks,
plus this review write. No numerical bound, interval producer, sample, solver,
Lean/Lake, Julia, full regression, state/registry edit or source promotion.
Large bound arrays were not independently audited; only their declared roles,
domains and current producer formula were examined.

