# H_acc source seam: phase-indexed producers for the occurrence cut

Status: **pending / OPEN_H_ACC**. This is a conditional mathematical interface,
not a source export, verified source theorem, runtime receipt or admission rule.
It adds concrete producer invariants to NEW_SEAM_OCCURRENCE_CUT.md and
NEW_SEAM_CONTRACT_PLAN.md; it does not replace either file or the closed intake.

## 1. Live evidence and precise scope

Inspected NEW_REVIEW.md, NEW_INTAKE_SCHEMA.json, NEW_source_intake.py, the existing
occurrence-cut/contract-plan documents and the complete raw Julia snapshot:
`examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`.
The verified snapshot SHA256 is
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.
The companion JSON binds the reviewed files and source sites, and records
explicitly absent evidence. It is an authored obligation manifest, not exporter
stdout or a proof-verification receipt.

Fresh `python -B .../NEW_source_intake.py` returned native exit **3**, pending.
NEW_INTAKE.json has null source_export, source_export_sha256, array_mapping,
source_updates, runtime_observation and interval_candidate. Thus graph checks
were NOT_RUN_NO_SOURCE_EXPORT; mapping/update checks were NOT_RUN_ABSENT.
This is an observation of this intake, not an exhaustive search of other paths.
No constants, scalar DAG, Float64 bits, error bounds or runtime observations
are generated. No Julia, Lean or Lake was run.

The increment here is the missing producer between a source location and a
value used at line 58: two loop invariants plus preservation to the RHS state.
The final fold theorem already has a sufficient cut; repeating that theorem
without these producers does not close occurrence refinement.

## 2. Typed objects: keep a source state independent of the scalar DAG

Fix a bundle key K binding source bytes, G (DAG), O (occurrences), U (updates),
input interpretation, evaluator definition, source-idealization definition,
target definition and the applicable environment/operation semantics. G/O/U
need separate content bindings. Absent content has no digest, not hash(null).
Verified dependency references must bind this same key; none exist here.

For this intake q = Decode(qhat), with qhat finite binary64 and q in Q1000.
Let V_q(n) be the topological Real evaluator of G. Its nine equations interpret
input, rat, pi, neg, add, mul, div_nat, sin and cos; div_nat has a positive
natural divisor. All node identities below are relative to one G and one q.
E_star(q)[r,c] is V_q at the submitted pre_regularizer root.

Separately, let sigma_p be an ideal-source state at phase p, with arrays and
local/global bindings. Its transition relation must interpret the pinned source
independently of G. Define array reads from sigma, not by evaluating O's node
IDs. The policy must explicitly explain real identity/zero allocation despite
the source's Float64 allocation syntax, decimal-token rationals, exact pi,
real-entry adjoint-to-transpose, slicing, assignment and matrix operations.
This is a source idealization, NOT running the literal Float64 Julia program
over Real values and NOT a claim about selected deployed methods.

The intended proposition is

```text
Use(K, phase, site, coordinate, n):
  V_q(n) = independently interpreted source entry at that phase/site.
```

A same-ID check only transports V_q. A preservation lemma transports a source
entry between phases. Neither one supplies the other. In particular these
are scalar-value aliases, not claims that Julia slices share heap storage.
No new field is inserted in NEW_INTAKE_SCHEMA.json.

## 3. Minimal sites and their dynamic phases

Ranges are zero-based, half-open raw UTF-8 byte offsets; intake line spans stay
one-based inclusive with original newlines. These fragments were freshly
located in the pinned bytes. The nested line-58 sites have the same line hash
but different fragment hashes; neither kind of hash identifies a loop instance.

| Family | Line; raw bytes | Phase and semantic obligation |
|---|---|---|
| z[j,k] | 36; [1303,1329) | FK step j, read before push; preserve assigned column to return |
| Ri[b,k,l] | 51; [1830,1853) | Body b after slice assignment; preserve block to RHS |
| active Jw[b,k,j] | 56; [2046,2066) | Body b, completed inner step j; preserve through steps j+1..b |
| inactive Jv[b,k,j] | 53; [1919,1935) | Fresh allocation for this b; j>b never assigned |
| inactive Jw[b,k,j] | 53; [1937,1953) | Separate fresh allocation for this b; j>b never assigned |
| translation[b,r,c] | 58; [2088,2107) | Body b RHS, after completed inner loop |
| rotation[b,r,c] | 58; [2110,2136) | Same body b and same RHS environment |
| B[b,r,c] | 58; [2088,2136) | Ordered addition of those two operands |
| accumulator transition | 58; [2083,2136) | M before update versus M after update |

Context is necessary too: lines 32-34 initialize, 35-41 order the FK step,
43/47 return and bind the arrays, 48 initializes M, 49/59 control the body loop,
and 53-57 control fresh Jacobians and their active prefix. Line 60 is excluded
from the pre-regularizer result. A value after the sixth update is not an
observation of the regularized return, even with regularization set to zero.

There are 18 z, 54 Ri, 63 active Jw and 45 inactive coordinates per Jacobian.
These count quantified obligations, not observed source executions. The dense
Jw mapping still has 108 records. Reusing a node never deletes an occurrence.

## 4. FK producer: a completed-step invariant, including preservation

Define abstract Real frame matrices independently by T_0=I_4 and
T_j=T_(j-1) A_j, where A_j must come from a separately justified lowering of
lines 37-39 under the source-token policy. Let F_k be the source state just
after k completed FK iterations (F_0 after initialization), for 0<=k<=6.
A sufficient invariant is:

```text
length(Tc in F_k) = k+1;
Tc[f+1] in F_k = T_f                         for 0<=f<=k;
o[:,1] in F_k = 0;
o[:,f+1] in F_k = T_f[1:3,4]                 for 1<=f<=k;
z[:,j] in F_k = T_(j-1)[1:3,3]               for 1<=j<=k;
unwritten o columns and z columns retain their initialized zeros.
```

Initialization supplies F_0. Assuming the invariant for k<6, step j=k+1:

1. At line 36, Tc[end] denotes T_k because the list has k+1 entries. Column j
   receives T_k[1:3,3]. Reading after line 40 instead would give the wrong frame.
2. Lines 37-39 supply A_j. Line 40 appends T_k A_j without changing earlier
   frame values; list length becomes k+2.
3. Line 41 copies the NEW last frame's origin into column j+1. Other origin
   and axis columns retain their values. This establishes F_(k+1).

These steps require semantic transition/footprint lemmas: the array operations
read the stated operands, writes affect only the stated destinations, matrix
products do not corrupt retained frames, and q/DH remain fixed. Text order is
not a verified footprint lemma. FK termination/return and line-47 binding must
transport F_6's arrays unchanged into mass_matrix.

Combining this invariant with an independent frame-node refinement theorem
V_q(O.Tc[f,k,l])=T_f[k,l] and the checked node-ID equations yields:

```text
V_q(O.z[j,k])    = T_(j-1)[k,3];
V_q(O.Ri[b,k,l]) = T_b[k,l].
```

The first source equality is at FK assignment and then return; the second is
at body b's line-51 slice and then RHS. Ri must not be substituted by frame
b-1. Frame f maps to Julia Tc[f+1], including initial frame f=0.

## 5. Jacobian producer: active prefix, not a full-column alias

Fix body b after its COM, Ri and Ii bindings. Let p_b be the source midpoint,
v_j=z_j cross (p_b-o_(j-1)), w_j=z_j for 1<=j<=b. The origin o_(j-1) is Julia
o[:,j]; p_b uses Julia origin columns b and b+1. J_(b,k), for 0<=k<=b, denotes
the phase after initialization and k COMPLETE inner-loop iterations.

```text
Jv[:,j] = v_j and Jw[:,j] = w_j                for 1<=j<=k;
Jv[:,j] = 0   and Jw[:,j] = 0                  for k<j<=6;
returned Tc/o/z, p_b, Ri, Ii and relevant globals are unchanged.
```

Fresh allocations give k=0. At inner step k+1, line 55 writes only Jv's
column k+1 and line 56 writes only Jw's column k+1. The completed-step invariant
holds after BOTH assignments, not between them. Preservation of other columns
and source operands gives the inductive step. Exit k=b gives active aliases
and all inactive zeros at the line-58 RHS. Each new body resets k=0 by fresh
allocations; the previous body's Jacobians are not the next body's state.

The minimal source-to-graph transport for active Jw is therefore:

```text
V_q(O.Jw[b,k,j])
  = V_q(O.z[j,k])             [checked same ID, j<=b]
  = source returned z[k,j]    [FK refinement + return preservation]
  = source RHS Jw[k,j]        [inner prefix invariant + preservation].
```

For j>b use initialization and nonassignment, not a fictitious line-56 event.
No conclusion that an inactive column aliases z is allowed, even if values
happen to coincide. Jv's cross-product producer separately needs the signed
three-component lowering; the Jw alias cannot establish it.

## 6. Operand lowering, body add and the exact six-step fold

At one body's RHS state set v=Jv, w=Jw, R=Ri and I=Ii. All inner indices below
range from 1 to 3; r,c range from 1 to 6. Required unsimplified operand lemmas:

```text
L_b[r,c] = m_b * sum_k v[k,r]*v[k,c]
H[k,h]   = sum_t R[k,t]*I[t,h]
Q[k,l]   = sum_h H[k,h]*R[l,h]
P[r,l]   = sum_k w[k,r]*Q[k,l]
R_b[r,c] = sum_l P[r,l]*w[l,c]

V_q(O.translation[b,r,c]) = L_b[r,c]
V_q(O.rotation[b,r,c])    = R_b[r,c].
```

Here H,Q,P are mathematical intermediate names, not exported nodes or observed
Julia temporaries. I is the source inertia with its division by 3 retained.
The R[l,h] index records the adjoint/transpose correctly. Real finite-sum and
associativity lemmas must connect these formulas to the ACTUAL candidate DAG's
reduction tree. No statement about Julia multiargument multiplication dispatch,
BLAS reduction order, FMA or rounding follows. No isotropic or orthogonality
simplification is required.

Given both operand lemmas, the checked literal node
B_b[r,c]=add(O.translation[b,r,c],O.rotation[b,r,c]) and one evaluator equation
give V_q(B_b[r,c])=L_b[r,c]+R_b[r,c]. This cannot prove either operand lemma.

Independently let Msrc_0 be source M after line 48, and Msrc_b after the b-th
line-58 update. Source transition/loop lemmas must establish Msrc_0=0 and
Msrc_b=Msrc_(b-1)+(L_b+R_b), then exit after body 6. This uses successive values
of M; `M +=` is NOT silently treated as an elementwise in-place update.

For each r,c, graph syntax gives S0=rat(0,1) and
S_b=add(S_(b-1),B_b), in that operand order. The conditional proof is exactly:

```text
base: V_q(S0) = 0 = Msrc_0[r,c];
step: V_q(S_b) = V_q(S_(b-1)) + V_q(B_b)
                  = Msrc_(b-1)[r,c] + (L_b[r,c]+R_b[r,c])
                  = Msrc_b[r,c].
```

Final roots alias S6, so E_star=Msrc_6. An independently defined target still
requires the separate bridge Msrc_6=M_NE^0 with the same q, source parameters,
dimensions and pre-regularizer boundary. Defining Msrc_6 as eval(G), or renaming
S6 to M_NE^0, would make the proof circular.

All 216 body and 216 accumulator entries, and 36 final entries, remain in scope,
including both triangles and zeros. Each of six source_updates binds 36 before,
body_roots and after IDs in column-major order. It binds content to this fold;
it does not certify that a source transition happened.

## 7. What can reject now, and what still needs a semantic witness

| Candidate defect | Existing structural check | Missing semantic discriminator |
|---|---|---|
| Wrong parent/current ID, active Jw ID, B operands or S predecessor | Rejects literal mismatch | Correct IDs still need source-value refinement |
| Broad valid span at initialization instead of required use | v1 may permit it; seam can flag occurrence-line gap | Phase and preservation witness |
| Correct line/hash but wrong body or before/after phase | Hash alone cannot distinguish | FK/Jacobian/body instance relation |
| Wrong array values in well-shaped translation/rotation subgraphs | Stage/add shape is insufficient | Both operand lowerings for the same RHS state |
| Ri copied correctly but later changed before RHS | Copy-site fact alone is insufficient | Ri preservation to the RHS |
| Full graph and all mappings but no source-model/target bridge | Remains pending | Independent definitions and verified dependencies |

This table describes discriminators, not tested synthetic exports. No fake DAG
or run was made to demonstrate them. Line/site/phase additions remain a proposed
external proof interface; they are not silently installed as new v1 fields or
new registry acceptance rules.

The next useful artifact is a real provenance-bound G/O/U export. The next
semantic producers are the source idealization/footprints, frame/DH lowering,
the two invariants, COM/cross/Ii lowering, both operand lowerings, the source
M transition, evaluator equations and independent target bridge. All are
pending for an actual bound instance. H_acc_round separately needs loaded
constant and execution-error semantics plus sound interval coverage. This
paper derivation closes neither H_acc_expr nor H_acc_round.

Only the new NEW_SEAM_PHASE_INVARIANTS_20260908T2030Z.md and its companion JSON
are authored by this task. Existing NEW_* (including earlier NEW_SEAM_*),
state, registry and shared scripts are not modified.
