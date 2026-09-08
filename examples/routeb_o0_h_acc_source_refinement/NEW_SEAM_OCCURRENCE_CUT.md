# H_acc source theorem seam: instance-indexed minimal cut

Status: pending / OPEN_H_ACC. This is a proposed proof interface, not an
export, installed intake extension, or verified theorem. It refines the existing
NEW_SEAM_MINIMAL_WITNESS.md by making use instances and the sufficient semantic
premises explicit. No existing file is changed.

## Evidence inspected and current stopping point

Read NEW_REVIEW.md, NEW_INTAKE_SCHEMA.json, NEW_source_intake.py and the actual
`examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`.
The raw snapshot hash is
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.
The accompanying NEW_SEAM_OCCURRENCE_CUT_AUDIT.json is fresh stdout from
`python -B examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_source.py`:
native exit 3, 27 located source fragments, graph digest null, all evidence
components absent. It records Python source-location/consistency inspection
only. It is not Julia output. A null occurrence_line_gaps means no mapping
was available to inspect, not that occurrence refinement passed.

## 1. Bind definitions, uses and semantic instances separately

Proposed external proof bundle K must identify the raw source, G (scalar DAG),
O (array mapping), U (six updates), Real evaluator definition, source
idealization definition, target M_NE^0 definition and input interpretation.
G/O/U each need their own content binding. The source idealization must specify
source-token rational/exact-pi constants independently of G and preserve the
input/global bindings through the call. It must not be defined as eval(G).
Actual loaded Float64 globals remain a different layer.

A proposed use witness key is
`(K, procedure, site, loop_indices, phase, coordinate, node_id)`.
Here `site` binds the exact source fragment bytes; `phase` locates the read or
post-assignment value in an independently defined ideal source execution.
This is NOT a new field accepted by the closed v1 JSON schema. A future
sidecar verifier is needed; no such verifier is installed by this document.

| Use family | Raw half-open bytes; line | Instance and required state fact |
|---|---|---|
| z[j,k] | [1303,1329); 36 | fk_frames ii=j, pre-push: Tc has j entries, end is frame j-1; post-copy z[j,k]=Tc[j-1,k,3] |
| Ri[b,k,l] | [1830,1853); 51 | mass_matrix ii=b, returned fk_frames table: Julia Tc[b+1] is frame b; preserve block through body RHS |
| Jw[b,k,j], j<=b | [2046,2066); 56 | ii=b,jj=j, post-copy: equals z[j,k]; later columns do not overwrite column j |
| Jw/Jv[b,k,j], j>b | line 53 allocation | fresh arrays for this b; no jj=j iteration; preserve initialized zero to line 58 |
| translation[b,r,c] | [2088,2107); 58 | body b, RHS state after inner loop, before update |
| rotation[b,r,c] | [2110,2136); 58 | same b and same RHS state, distinct expression occurrence |
| B[b,r,c] | [2088,2136); 58 | addition of the preceding two operand values |
| S_b[r,c] | [2083,2136); 58 | pre-update M=S_(b-1); post-update M=S_b |

Indices k,l range 1..3; b,j,r,c range 1..6 where applicable. Mapped frame f
uses Julia Tc[f+1]. Source context at lines 32-41,47-49,53-57,59 establishes
initialization, call return, iteration and preservation. The listed fragments
alone cannot establish this context. Line 60 is excluded.

There are 18 z, 54 Ri and 63 active Jw coordinate obligations, plus 45 inactive
coordinates per Jacobian. These are coverage counts, not exported values.
The existing dense Jw table still contains all 108 coordinates. Reusing one
scalar node does not remove uses. Node identity is Real-value congruence under
one G and input; it is not a Julia heap-alias claim. Do not add add(x,0), move
a definition span to a later use, or synthesize source nodes to satisfy spans.

## 2. Smallest sufficient semantic premises for the final fold

Let V_q(n)=eval_Real(G,q,n). The evaluator obeys input, rat, pi, neg, add, mul,
div_nat, sin and cos equations in topological order, with positive divisors.
Let Tsrc_b and Rsrc_b be independently interpreted source operands at line 58,
and Msrc_b the source M just after body b (Msrc_0 after line 48).

The sufficient cut is:

1. Evaluator equations and the checked graph/root/occurrence/update structure
   all refer to the same K. In particular V_q(S0)=0 and final roots alias S6.
2. For every b,r,c, operand refinement gives
   V_q(O.translation[b,r,c])=Tsrc_b[r,c] and
   V_q(O.rotation[b,r,c])=Rsrc_b[r,c]. These cannot be inferred from stage labels.
3. Independent source loop semantics gives Msrc_0=0 and
   Msrc_b[r,c]=Msrc_(b-1)[r,c]+(Tsrc_b[r,c]+Rsrc_b[r,c]).
   This is a value-state rule for M +=, not an assumed in-place mutation rule.
4. An independent target bridge gives Msrc_6(q)=M_NE^0(q) for the same constants,
   dimensions and input. Calling Msrc_6 or E_star 'M_NE^0' is not this proof.

Then the body add syntax and evaluator add equation give
V_q(B_b[r,c])=Tsrc_b[r,c]+Rsrc_b[r,c]. For each coordinate, induction on b
gives V_q(S_b[r,c])=Msrc_b[r,c]: zero is the base; the literal ordered graph
add, preceding induction equality and body equality give the step. Final-root
congruence and premise 4 yield E_star(q)[r,c]=M_NE^0(q)[r,c]. This is a paper
derivation of a conditional theorem, not a verified instance of its premises.

No commutativity, SPD, orthogonality, numerical evaluation or interval bound
is needed for this final induction. The 216 B and 216 S coordinates, including
both triangles and zero entries, remain mandatory. Six source_updates records
bind their 36-entry before/body_roots/after lists to these same roots.

## 3. Producing the operand premise without assuming the conclusion

The upstream obligation is source-to-array-to-scalar lowering, not another
assumption of E_star=M_NE^0. It covers source literals and A, Tc multiplication,
o, COM midpoint, cross-product signs, Ii division by 3 and the instance-indexed
aliases above. For source arrays v=Jv, w=Jw, R=Ri, I=Ii at the same body:

```text
Tsrc_b[r,c] = m[b] * sum_k v[k,r]*v[k,c]
H[k,h] = sum_t R[k,t]*I[t,h]
Q[k,l] = sum_h H[k,h]*R[l,h]
P[r,l] = sum_k w[k,r]*Q[k,l]
Rsrc_b[r,c] = sum_l P[r,l]*w[l,c]
```

All summation indices range 1..3. H/Q/P are mathematical names here, not
claimed Julia temporaries or new exported nodes. This displays the unsimplified
(w^T*((R*I)*R^T))*w target and the transposed index R[l,h]. Julia uses adjoints;
the Real idealization needs the real-entry adjoint-to-transpose lemma. Any
chosen scalar reduction tree needs a Real finite-sum/lowering proof. Do not
attribute that tree to Julia dispatch, BLAS, FMA or runtime evaluation order
without separate evidence. Isotropic-inertia or orthogonality simplification
would introduce extra proof obligations and is unnecessary for this cut.

## 4. Minimal missing fields and discriminating checks

Currently missing intake evidence: source_export (including complete nodes and
roots), source_export_sha256, array_mapping and source_updates. No genuine
export was supplied. Future semantic witness references also need independent
definitions, use-instance/preservation proofs, operand lowerings, loop proof
and target bridge tied to K. A digest is an identifier, never such a proof.

Distinguish these checks when a genuine candidate arrives:

- Wrong parent/current node IDs, active Jw IDs, B operand order or S predecessor:
  existing intake structural rejection. Correct IDs alone prove no source use.
- A valid broad role span covering initialization instead of the required use:
  existing NEW_SEAM_source.py can report a seam line gap; this is not a new
  rejection rule installed in v1.
- Same valid line/hash but wrong loop instance or stale source state: needs the
  proposed semantic witness; line hashing cannot detect it.
- Well-shaped arbitrary translation/rotation subgraphs: body-add checks are
  insufficient; independent operand refinement is the missing discriminator.
- Complete structure with absent proofs: still pending, not admission success.

The graph/occurrence/fold seam concerns H_acc_expr only. Loaded-constant error,
machine execution error and sound interval coverage are separately open for
H_acc_round. No constants, fake graphs, runtime bits, numeric bounds, Julia
execution or Lean/Lake evidence were generated. Only this new NEW_SEAM_*.md
and its new NEW_SEAM_*.json audit are written; existing NEW_*, state, registry
and shared scripts are untouched by this task.
