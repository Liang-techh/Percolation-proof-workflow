---
kind: review_result
review_id: review-T-P4-BODY4-MINIMAL-TRANSVERSE-WITNESS-20260914T2122Z
task_id: T-P4-BODY4-SOURCE-JACOBIAN-BRIDGE
source_agent: Codex-Body4-minimal-witness
created_at: "2026-09-14T21:22:12Z"
inspected_commit: d2a2b8836700ef49883f3169c244447363c40d63
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_QUOTIENT_EQUIVALENCE_CANDIDATE_UNCOMPILED
source_binding_proven: false
runtime_equality_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_lake_run: false
julia_run: false
state_mutation: false
registry_mutation: false
requested_action: use the transverse witness contract for genuine source export; verify the conditional adapter and supply source/coverage proofs without promoting this review
---

# Body4: contract the geometry to axes plus transverse displacement classes

## Result, including the necessary index correction

For the original Body4JvTarget/Body4JwTarget, the correct zero column is
zero-based joint 3 = HUMAN JOINT 4. Human joint 3 is zero-based joint 2 and is
active with a generally nonzero linear column. Inactive columns are zero-based
4,5 = HUMAN COLUMNS 5,6, not human columns 4-6. These facts follow from
body=3 and the source guard j.val<=body.val / Julia jj in 1:ii with ii=4.

The earlier 27-frame-field cut is sufficient but stronger than needed for the
Jacobian outputs. Under the actual axis binding and source assignment semantics,
Jv determines displacement only modulo its axis. The new sufficient-and-necessary
ideal semantic cut is:

```text
four active source axes = their target axes;
four source displacements = target displacements modulo the corresponding axis;
both final inactive columns of both Jacobians are zero.
```

In native coordinates this can be supplied as 4 vector axis equalities (12
scalar equalities) plus EIGHT signed transverse scalar equalities. The 12
inactive output entries are supplied by the specific source's allocation and
write-footprint theorem, not twelve fabricated zero observations. The 36 output
requirements remain covered: 12 active angular entries, 12 active linear entries
determined by the eight transverse equalities, and 12 inactive entries.

The precise minimality claim is two independent signed linear measurements per
active displacement AFTER its axis is fixed. This is not a claim that 20 scalar
conditions form the globally smallest proof/encoding across all DH dependencies.
For example, existing verified initial-axis or repeated-axis source theorems
could discharge some axis fields without new exported data. Those proofs must
be referenced, not silently assumed.

New files under examples/routeb_o1_body4_source_gram_proof_attempt:

- NEW_SOURCE_JACOBIAN_20260914_QUOTIENT_PORT.lean: conditional, uncompiled Lean
  candidate consuming the imported actual sourceContract; no geometry inhabitant.
- NEW_SOURCE_JACOBIAN_20260914_MINIMAL_WITNESS_CONTRACT.json: proposed field and
  provenance contract, not an export. All source/proof/runtime payloads are null.

No genuine same-source witness was supplied or found in the inspected lane.
Admission remains pending. Existing files, state and registry are not modified.

## 1. Exact necessary-and-sufficient geometric statement

Fix q and one active j in Fin 4, embedded in Joint=Fin 6. Let

```text
Z_j = (sourceContract q).axes j;
D_j = bodyCom((sourceContract q).origins,body=3) - source parent origin j;
W_j = prefixZ(q,j);
Delta_j = displacement(q,j);
V_j = vcol(q,j).
```

The local target algebra gives W_j cross Delta_j=V_j and wcol(q,j)=W_j. Each W_j
is a unit vector, hence nonzero. Active source semantics gives Jw_j=Z_j and
Jv_j=Z_j cross D_j. Consequently:

```text
(Jw_j=W_j AND Jv_j=V_j)
  iff (Z_j=W_j AND W_j cross (D_j-Delta_j)=0)
  iff (Z_j=W_j AND exists t_j : Real, D_j=Delta_j+t_j W_j).     (Q)
```

First equivalence: substitute Z_j=W_j and use bilinearity of cross. The reverse
direction obtains the axis equality directly from Jw, then subtracts the known
target cross identity. Second equivalence uses ker(d -> W_j cross d)=span(W_j)
for nonzero W_j. Thus all along-axis displacement values can be omitted from a
Jacobian-only witness. This does not omit them from any later COM/frame theorem.

The Lean candidate represents the kernel by its vector equality, avoiding a
chosen scalar chart in the core interface. It provides sourceDisp, JacobiansOn D,
QuotientWitness D, cross_eq_iff_kernel, the two conditional directions, their iff,
and an explicit cover constructor. It imports existing BODY4_PORTS for finite
indices, inactive guards and local target cross algebra. Those imports and the
new file have NOT been compiled in this task; no successful axiom audit is
asserted. No source equality is introduced as an axiom or a supplied inhabitant.

## 2. Eight scalar fields, with exact signs

Use the already defined oriented cylindrical-to-world rotation L_q=lift q.
For the ACTUAL ideal-source displacement D_j define its local coordinates

```text
r_j = cos(q0)*D_j.x + sin(q0)*D_j.y;
t_j = -sin(q0)*D_j.x + cos(q0)*D_j.y;
h_j = D_j.z.
```

They satisfy D_j=L_q(r_j,t_j,h_j). This coordinate relation must be proved for
the source readout; exporting numbers with these labels is not that proof.
Write s=sin(phi(q)), c=cos(phi(q)), with phi=q1+q2. Target aa,qq,pp,d,e are the
unchanged imported definitions, not fitted or newly estimated constants.

| zero-based j / human joint | Local target W_j | Required signed source projections | Not required for Jv |
|---|---|---|---|
| 0 / 1 | (0,0,1) | r_0=aa(q), t_0=d | h_0 |
| 1 / 2 | (0,1,0) | r_1=qq(q), h_1=pp(q) | t_1 |
| 2 / 3 | (0,1,0) | r_2=e*s, h_2=e*c | t_2 |
| 3 / 4 | (s,0,c) | t_3=0, c*r_3-s*h_3=0 | s*r_3+c*h_3 |

Proof by local cross formulas and oriented lift transport:

```text
(0,0,1) cross (r,t,h) = (-t,r,0);
(0,1,0) cross (r,t,h) = (h,0,-r);
(s,0,c) cross (r,t,h) = (-c*t,c*r-s*h,s*t).
```

For the final row, vanishing first/third components implies t=0 because
s^2+c^2=1; the second component then gives c*r-s*h=0. No component division by
s or c is allowed or needed, so the chart remains valid when either is zero.

This table is exactly equivalent to the kernel fields in (Q). A formal Lean
adapter from these eight scalar equations to the kernel is NOT implemented in
the candidate; the paper derivation above supplies its specification. The
candidate already consumes the equivalent vector-kernel witness. This distinction
is explicit in the JSON, rather than reporting scalar-to-kernel elaboration.

Why two transverse fields are minimal in this class: the cross map has rank 2.
One scalar linear measurement has at least a two-dimensional kernel and cannot
force a vector into the one-dimensional span of W. Two independent transverse
measurements do suffice. For j=3 the row vectors (0,1,0) and (c,0,-s) are nonzero
and orthogonal; their independence is uniform since s^2+c^2=1. Correlated DH
source identities may reduce export work further, but have to be proved first.

In particular the old translation condition O4-O3=(19/100)Z3 fixes the along-axis
length e=19/200. For the active zero Jacobian column, any D3=k*Z3 works. Therefore
that particular length is sufficient but NOT necessary for the Jacobian target.
This is not permission to change source geometry: it says that a Jacobian-only
consumer need not demand an independently exported longitudinal component.

## 3. What must actually be exported or proved

The minimal mathematical quotient does not replace source authenticity. A
source-export bundle must bind the following objects to ONE key K:

| Field family | Required content / proof | Why it cannot be omitted |
|---|---|---|
| Source/model identity | Raw source hash; independent idealization and input definitions; relevant DH environment; original target definitions | Same formulas at a different source are not this theorem |
| State and phase | q identity, body index 3 / Julia ii=4; readouts after inner loop, before line 58; explicit zero-based spatial/joint layout | Same line/hash does not identify a body or pre/post state |
| Active axes | Four vector readout/expression roots, source equality and preservation proofs to W_j | Jw requires these axes; a Gram table does not identify them |
| Displacement projections | Eight signed expression roots/functions, source-readout/lowering proofs and target equalities from section 2 | Labels or single sampled values do not prove functions on the domain |
| Active assignment semantics | Parent axis read before FK push; COM and parent-origin correspondence; line-55 cross and line-56 copy; later writes preserve each column | Kernel geometry alone is not a source Jacobian readout |
| Inactive semantics | Fresh Jv/Jw zeros at line 53 for THIS body; loop jj=1..4; no write/interference in human columns 5,6; transport to final readout | No synthetic line-55/56 event exists for inactive columns |
| Coverage | D definition, cell definitions, per-cell quantified witnesses and proof every q in D belongs to a certified cell | Missing cells cannot become valid by an empty local implication |
| Verified dependencies | Proof artifacts, exact statements, source/target/import/toolchain bindings and validation results | Digests identify content, not logical validity |

Witnesses can reference already verified source theorems rather than duplicate
raw values. No requirement to export full X/Y frame columns, every full origin,
full slot4 rotation, full displacement vectors, full Gram matrices or 36 sampled
Jacobian values remains at this interface. The 36 conclusions still exist;
their provenance is compressed, not their coverage.

Necessary/sufficient must be used carefully: final inactive zeros are the
necessary semantic condition for the target, while fresh allocation plus no
write is the sufficient provenance route justified by this PARTICULAR pinned
source. Freshness is not logically necessary for every conceivable program
that returns a zero column. The protocol uses it to certify the current program,
not to assert an invalid universal characterization of zero arrays.

All active-axis/projection roots in the new JSON are null because no real
export was supplied. A producer must not fill them by defining source readouts
equal to prefixZ or the table's RHS. Independent interpretation, source lowering
and equality proof are three separate pieces. Counts and index tables are
requirements only, never execution or enclosure evidence.

## 4. Coverage and the Lean handoff boundary

QuotientWitness D concerns actual imported sourceContract functions on D.
The candidate proves the conditional equivalence with JacobiansOn D. Its
quotient_of_cover requires BOTH:

```text
cover : forall q, D(q) -> exists i, Cell(i,q);
localWitness : forall i, QuotientWitness (D intersect Cell_i).
```

The original global targets follow only from QuotientWitness True, or from a
separate proof that the chosen D covers ALL Q6. Finite binary64 observations or
Q1000 enclosures cannot be silently promoted to all-real target inhabitants.
Cell index, source phase, decoded input and ideal q must all commute through
the same readout map. An all-empty cover is an exact countermodel to omitting
the cover premise: its local statements are vacuous and prove no global value.

This candidate is ideal-source logic only. It does not say any actual Julia
output equals the Lean bodyJv or bodyJw. A separately supplied ideal Julia/Lean
bridge is still required; a runtime target needs additional error semantics.

## 5. Parallel-cross versus fresh-zero in Float64

For active joint index 3, the source really calls cross at line 55. Given finite
decoded actual readouts zhat,dhat,jhat, define

```text
eta = dhat - e*zhat;
rho_cross = jhat - (zhat cross dhat);
jhat = zhat cross eta + rho_cross.
```

The equality is a real residual identity, not a bound or a fabricated run.
Actual midpoint/subtraction/trig/constants can give a nonzero transverse eta;
the arithmetic cross residual also needs control. Ideal transverse equations
do not prove runtime bitwise zero. Retain signed transverse error quantities
until a valid enclosure is formed; do not label this an inactive zero column.

For inactive indices 4,5 the source performs no cross/copy iteration. Their
zero guarantee comes instead from allocation and noninterference. Copying the
active Jw axis preserves actual values only under the relevant type/copy facts;
it does not make those actual values equal to ideal W_j. No Float64 constants,
cross-error budget or runtime observation is generated in this task.

## 6. Evidence and verification scope

Freshly matched raw SHA256 bindings:

| Path relative to workspace | SHA256 |
|---|---|
| artifacts/task_routeb_body_trace_sink_current/source_snapshot/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| examples/routeb_b45_source_comparator_lean/RouteBO1Body4SourceGramTargets.lean | 2d0d2794edfe745d63a2970c36b53765f3b4bd747480107b1eab51cf2e2c3ca9 |
| examples/routeb_o1_body4_source_gram_proof_attempt/NEW_SOURCE_JACOBIAN_20260908_BODY4_PORTS.lean | 95997701cd6ac1de61537121f91e629a9e030fa45b36f6fca5e85422deabbe42 |
| examples/routeb_o1_body4_source_gram_proof_attempt/NEW_SOURCE_JACOBIAN_20260914_FIELD_COVERAGE.json | 3f1a237368e735667588e4de5c2a1d29677876b75858cfa670df6454ec93f101 |

The original targets, BodySemanticCore, active/inactive PORTS and actual Julia
lines 31-60 were reread. Only local text/hash/contract consistency and focused
algebra checks are in scope. No Lean/Lake, Julia, source generator, full-project
regression, state/registry write or remote compile dispatch was performed.
The equivalence adapter remains UNCOMPILED, its geometry witness uninstantiated,
and scalar-to-kernel formalization a separately identified next step.
