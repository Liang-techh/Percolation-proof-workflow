---
kind: review_result
review_id: review-T-P4-BODY4-SOURCE-JACOBIAN-BRIDGE-20260914T2110Z
task_id: T-P4-BODY4-SOURCE-JACOBIAN-BRIDGE
source_agent: Codex-Body4-source-seam
created_at: "2026-09-14T21:10:37Z"
inspected_commit: 53e497f9d09de120db0f16da87b7d6e07e0e6e00
integration_status: pending
admission_label: pending
proof_status: FIELD_REQUIREMENTS_COMPLETE_SOURCE_WITNESSES_MISSING
source_binding_proven: false
runtime_equality_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_lake_run: false
julia_run: false
state_mutation: false
registry_mutation: false
proposed_integration_target: Body4 source Jacobian field and domain seam
requested_action: retain field inventory and obstruction; independently verify geometry, source readouts and coverage before claiming target or runtime closure
---

# Body4 source Jacobian: complete field requirements, not completed witnesses

## Outcome and current evidence

No authenticated same-source Jacobian witness was found in the inspected
Body4 candidate/receipt lane. The existing definitions and conditional proof
scripts support a precise interface, but their presence is not elaboration,
source authentication or runtime evidence. Status remains pending.

The new companion is
`examples/routeb_o1_body4_source_gram_proof_attempt/NEW_SOURCE_JACOBIAN_20260914_FIELD_COVERAGE.json`.
It lists 27 scalar frame requirements and all 36 Jacobian component requirements.
Each semantic witness is null and verified=false. Its coverage flag means ONLY
that the requirement coordinates were enumerated; actual source-witness coverage
and cell/domain coverage remain null. It is not an export or a fabricated run.

Resumption on September 14 rechecked the repository HEAD, relevant directory
inventory and file hashes. HEAD remains the inspected revision above. The source
snapshot is `artifacts/task_routeb_body_trace_sink_current/source_snapshot/dhport_lib.jl`,
SHA256 `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.
The companion binds 14 reviewed inputs by fresh SHA256, including the original
targets, semantic core, source/frame adapters, RealDHStep, existing minimal-Z/O
and PORTS candidates, translation candidate and snapshot manifest. The snapshot
was read in full; the generator's frame/Jacobian construction was inspected.
The snapshot manifest's historical status is not a fresh generator/runtime check.

The bounded search covered the named Body4 proof-attempt directory, its JSON
handoff, original target/adapter files, prior frame-source audit and related
inbox references. It found a NOT_RUN compile handoff and proof candidates, not
a newly verified exact-target receipt. This does not assert that no differently
encoded witness exists elsewhere. No Lean/Lake, Julia, generator or regression
was run, and no old artifact was edited.

## 1. Index and phase table: the active zero column is not inactive

Original definitions: Body/Joint=Fin 6; Axis=Fin 3; Q6=Joint->Real.
Jv/Jw entries are [spatial row, joint column]. Each Jacobian has 18 entries.

| Item | Lean/Python index | Julia source instance | Required meaning |
|---|---|---|---|
| human body 4 | body=3 | mass_matrix ii=4 | One body, not body=4 |
| COM endpoints | origin slots 3,4 | o[:,4],o[:,5], line 50 | Midpoint of consecutive body endpoints |
| active joints | j=0,1,2,3 | jj=1,2,3,4 | Source loop uses 1:ii, including jj=4 |
| active axis j | parent frame slot j | z[:,j+1], originally filled before FK push | Not the current frame slot j+1 |
| active parent origin j | origin slot j | o[:,j+1] | Subtracted from the body COM at line 55 |
| joint index 3 | human joint 4 | jj=4, lines 55/56 | Jv zero by parallelism; Jw remains the parent axis |
| inactive joints | j=4,5 | columns 5,6 | Fresh line-53 zeros, no inner assignment |

Source state matters: the target readout is the body-4 Jacobian after the
completed inner loop and before line 58 consumes it. Source equality needs the
line-36 pre-push axis read, preservation through FK return, line-47 binding,
fresh per-body allocation and column-write preservation. A final array with the
right shape, or an entry attributed to the right line, supplies none of those
execution facts. Reusing the previous body's array is not this readout.

There are 12 active and 6 inactive component obligations per Jacobian. The
three Jv components at active j=3 are attributed to line 55, not initialization.
The three Jw components at that same active joint are attributed to line 56.
Both sets are explicitly distinguished in the companion manifest.

## 2. Minimal sufficient ideal geometry cut, field by field

Write F_s=routeBFrameSlot(q,s), Z_s=zAxis(F_s), O_s=origin(F_s).
The existing MINIMAL_ZO_BRIDGE exposes a sufficient cut:

```text
Z_s = prefixZ(q,s),     s=0,1,2,3;              12 scalar equations
O_s = prefixO(q,s),     s=0,1,2,3;              12 scalar equations
O_4 = O_3 + (19/100) Z_3;                       3 scalar equations
```

This is minimal relative to what the existing handoff consumes, not a proof
that 27 independent scalar hypotheses are mathematically indispensable. For
example initial-frame fields have their own structural producers. It does NOT
inhabit the original full Body4PrefixColumnsTarget: that target also asks for
X/Y columns and has 48 scalar fields.

The direct lower-level cut is actual axes plus actual COM displacements;
neither cut may substitute arbitrary vectors for the imported sourceContract.

| Exit | Sufficient ideal-source premises | Separate obligations |
|---|---|---|
| Jw for j=0..3 | Four parent Z columns and active source guard | Source axes/readout correspondence |
| Jv for j=0..2 | Parent Z/O, midpoint O3/O4, signed cross formulas | Same-q displacement and oriented lift transport |
| Jv for j=3 | O4=O3+(19/100)Z3 and parent-slot/COM adapters | No full prefix trig or isometry needed |
| Jv/Jw for j=4,5 | Strict guard 3<j.val in BodySemanticCore | For external Julia: initialization and nonassignment preservation |

For active j=3, exactly

```text
COM=(O3+O4)/2,
COM-O3=(19/200) Z3,
Jv[:,3]=Z3 cross ((19/200)Z3)=0,
Jw[:,3]=Z3.
```

The target is Z3=vec(q,sin(phi),0,cos(phi)), phi=q1+q2. Its Euclidean squared
length is one. Thus marking joint 3 inactive would force a zero angular column
in contradiction with the ideal target. This is an exact indexing obstruction,
not a numerical observation.

The source step with index 3 has translation column (0,0,19/100,1) in the ideal
DH definition. F4=F3*T3 gives the translation identity by four-term matrix
multiplication; no orthogonality of F3 is required for that column equation.
The existing NEW_FINITE_SUM_20260908_STEP3_TRANSLATION.lean attempts precisely
this producer, but its handoff is NOT_RUN. It is not treated as verified here.

The mass regularizer at line 60, mass coefficient and inertia division do not
enter this Jacobian cut. Jacobian closure would not by itself close
Body4SourceGramTarget, expected-entry, Fourier trace or h_body_4. Also, a
cross-product array named Jv is not automatically a Frechet-derivative theorem
about the COM map; that interpretation requires its own kinematic proof.

## 3. lift, Euclidean dot and orientation are different interfaces

The existing lift is

```text
L_q(r,t,z)=(r*cos(q0)-t*sin(q0), r*sin(q0)+t*cos(q0), z).
```

Its dot preservation and oriented cross transport are separate identities:
dot(Lu,Lv)=dot(u,v), and (Lu) cross (Lv)=L(u cross v). The latter uses the
orientation det(L)=+1, not just orthogonality. Target vcol/wcol are already
world-coordinate lifted vectors and must not be lifted a second time.

Two exact obstructions explain why local identities do not bind source columns:

1. Reflection H(x,y,z)=(x,y,-z) preserves dot. For u=e1,v=e2, Hu cross Hv=e3
   while H(u cross v)=-e3. Dot preservation alone does not justify oriented cross.
2. The proper cyclic rotation P(x,y,z)=(z,x,y) preserves both dot and oriented
   cross. Applying P to all candidate world columns leaves every Gram entry
   unchanged, yet changes the fixed world axis e3 to e1. At q=0 the target's
   joint-0 angular column is e3. Thus even Gram plus correct cross covariance
   does not establish equality to that source column without an orientation/
   coordinate-frame binding.

These are mathematical alternatives showing missing premises, not claimed
Julia executions. The Euclidean dot claim is also not metric Isometry for the
default Pi/sup norm on Fin 3->Real: a non-axis-aligned planar rotation generally
changes the sup norm. No Lean Isometry instance is inferred from the name
lift_dot_isometry.

## 4. Coverage-aware proof skeleton: do not promote a cell to all Q6

The original Body4JvTarget and Body4JwTarget quantify over ALL real q, not a
sample set and not a binary64 input cube. A safe paper-level interface is:

```text
JacobianAt(q) :=
  (forall a j, bodyJv(sourceContract(q),body=3)[a,j]=vcol(q,j)[a]) AND
  (forall a j, bodyJw(sourceContract(q),body=3)[a,j]=wcol(q,j)[a]).

LocalGeometry(i,q)                         external actual-frame premise
LocalGeometry(i,q) -> JacobianAt(q)        conditional algebraic consumer
cell_proof : forall i q, D(q) -> Cell(i,q) -> LocalGeometry(i,q)
cover      : forall q, D(q) -> exists i, Cell(i,q)
--------------------------------------------------------------
forall q, D(q) -> JacobianAt(q).
```

Proof: choose a covering i for the given q, apply cell_proof, then the local
consumer. Coverage and local geometry are both EXPLICIT inputs; no cell data
or proof is fabricated. To recover the original two global target types one
additionally needs D(q) for every q (or an independently valid all-q proof).

Exact countermodel to dropping cover: let all cells be empty. Every local
implication is true regardless of a false target at an uncovered q. More
concretely, equalities known only on Q1000 cannot determine an arbitrary source
readout at q=(1,0,0,0,0,0), outside that cube. This is a logical domain obstruction,
not a counterexample to the fixed DH target. Even exhaustive finite-binary64
observations do not cover Q6's continuum of real inputs.

An external ideal-source readout additionally needs an independent relation
q_read(x)=q and Jv_read(x)=bodyJv(sourceContract(q),3), likewise Jw, at the
specified source phase. Its semantics must be derived from the independently
identified idealized source operations. Defining the readout equal to the target
would make the relation circular. The local algebra then transports equality
on valid covered x only. It does not create a source execution or extend the
readout beyond its domain.

## 5. Ideal and Float64 boundary: retain the nonparallel defect

Three layers must not be merged:

- Lean/exact Fourier idealization: source decimal rationals and exact phases;
  ideal trig, matrix, midpoint, subtraction and cross operations.
- An independently interpreted ideal Julia source: needs source-token/index/
  operation correspondence to the Lean definitions, not just matching bytes.
- Actual Julia arrays: loaded Float64 constants, angle/trig evaluation,
  reductions, midpoint/subtraction and cross rounding, with actual provenance.

The snapshot generator and Julia code visibly use the same intended parent-
axis/COM/active-prefix pattern. That is useful textual evidence, not proof that
their values agree. In particular ideal simplification of shifted angles into
sin/cos and exact pi/2 alpha values need not hold bit-for-bit in Julia.

For the delicate active joint 3 let zhat be the decoded actual parent axis,
dhat the decoded displacement fed to cross, and jhat the decoded output column.
All must come from the SAME call/body/column. Define exact-real residuals

```text
e := 19/200                         ideal reference scalar
eta := dhat - e*zhat                nonparallel displacement defect
rho_cross := jhat - (zhat cross dhat).
```

Then bilinearity gives the exact conditional identity

```text
jhat = zhat cross eta + rho_cross.                         (R)
```

This requires no assertion that dhat is exactly parallel to zhat. Any loaded
constant discrepancy, frame error, midpoint or subtraction rounding is retained
in eta; cross arithmetic discrepancy is retained in rho_cross. The definitions
alone do not bound either residual and are not runtime observations.

If separately source-certified Euclidean bounds are supplied on the same cell,
||zhat||<=Z, ||eta||<=E, ||rho_cross||<=R, then ||jhat||<=Z*E+R. No such numerical
bounds are proposed here. The ideal zero can transfer only under additional
conditions annihilating the RHS of (R); a known ideal zero alone is insufficient.
Equivalently, with zhat=z+dz and dhat=e*z+dd, the cross part expands to
z cross (dd-e*dz)+dz cross dd. This is a signed error identity, not an enclosure.

An exact logical example is zhat=e3, dhat=e*e3+t*e1, rho_cross=0: the output is
t*e2 for t!=0. It shows that an uncontrolled nonparallel defect prevents the
zero inference. It is not a simulated or observed DH state.

Inactive columns and active copies have different machine obligations: inactive
zeros require valid allocation/no overwrite; active Jw copies require that the
actual parent-axis values and types are preserved. Copying those values does
not prove that they equal the ideal trigonometric Z3. NaN/Inf, signed-zero and
loaded-type behavior belong to the runtime contract, not these Real equations.

## 6. Required next evidence and validation scope

The field manifest is ready to match future evidence by source/model/input/
coordinate/phase key. Still required are verified actual-prefix and translation
inhabitants for the selected ideal model; the independent ideal-source readout
and preservation bridge; and any local-to-domain cover. Runtime use additionally
needs loaded values/provenance and sound error bounds, never inferred constants.

The companion's 14 file hashes, 27 frame requirements, 18+18 dense Jacobian
requirements, active/inactive partitions and pending/null witness fields are
subject to read-only consistency checks. Such checks do not elaborate Lean or
verify a single source equation. Only this review and the new
NEW_SOURCE_JACOBIAN_20260914_FIELD_COVERAGE.json are authored for this task.
State, registry, prior agents' files and shared scripts are not modified by it.
