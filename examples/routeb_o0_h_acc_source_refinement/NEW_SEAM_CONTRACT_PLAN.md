# Source theorem seam: executable obligation plan

Status: **pending / OPEN_H_ACC**. This addition operationalizes the existing
instance-indexed cut; it is not another source exporter, semantic verifier or
admission rule. Existing NEW_* (including existing NEW_SEAM_*), state, registry
and shared scripts are unchanged by this task.

## Actual source and current evidence

Read NEW_REVIEW.md, the complete NEW_INTAKE_SCHEMA.json and NEW_source_intake.py,
the earlier source-seam reviews/checker, and the actual snapshot
`examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`.
The independently checked raw-byte SHA256 is
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.
NEW_INTAKE.json has null export, graph digest, mapping, updates, runtime and
interval evidence. This only reports that intake; it does not claim an
exhaustive search for exports elsewhere or attest the deployed Julia library.

NEW_SEAM_contract_audit.py reuses the unchanged strict intake and source-location
checks, then emits a **proof-obligation plan**, not the scalar DAG E_star.
It separates graph, occurrence-mapping and update content bindings; an absent
component stays null, never hash(null). Evaluator/source/target/environment
definition and proof-dependency bindings also remain null. A future non-null
component digest binds candidate content only, not its authenticity or semantics.

## Minimal source-span and instance contracts

Ranges below are zero-based half-open raw UTF-8 bytes, not character columns;
v1 line spans remain one-based inclusive, including original newline bytes.
The sidecar does not add fields to the closed v1 schema.

| Family | Line; bytes | Required source instance and preservation |
|---|---|---|
| z[j,k] | 36; [1303,1329) | Before push at ii=j, Tc has j entries; read frame j-1, preserve z column through return and use |
| Ri[b,k,l] | 51; [1830,1853) | Returned table, Tc[b+1] is frame b; preserve selected block value to rotation RHS |
| Jw[b,k,j], j<=b | 56; [2046,2066) | Current body's fresh Jw, copy z[:,j]; later column writes preserve column j |
| inactive Jv/Jw, j>b | 53; distinct allocation fragments | Fresh per body; no corresponding inner-loop assignment; zero persists to line 58 |
| translation | 58; [2088,2107) | Same body and RHS state as rotation |
| rotation | 58; [2110,2136) | Unsimplified adjoint/matrix expression |
| B | 58; [2088,2136) | Ordered addition of the two operand values |
| S_b update | 58; [2083,2136) | M before update and M after update are distinct source states |

There are 18 z, 54 Ri, 63 active Jw uses and 45 inactive uses per Jacobian.
These are quantified obligation counts, not observed executions or graph nodes.
One reused scalar node still has multiple required occurrences. The instance
key is `(K, procedure, site_fragment, loop_indices, phase, coordinate, node_id)`.
Frame f maps to Julia Tc[f+1]. Node equality transports Real values under one G
and q; it does not imply Julia heap aliasing or establish source-state timing.
Do not insert add(x,0), move definition spans, or reconstruct missing constants.

Context required for the source proof includes initialization 32-34, the
pre-/post-push order 35-41, fk_frames return/call 43/47, M allocation/body loop
48-49, fresh Jacobians and active loop 53-57, and loop end 59. Text order alone
is not an execution proof. The program point is after body 6 line 58 and before
line 60; neither the regularized return nor subtraction of its regularizer is
an admissible substitute. M += is modeled by successive values, not assumed
elementwise in-place mutation. Global/input binding preservation is required.

## Non-circular theorem inputs and assembly

Fix K identifying independently defined source idealization, Real evaluator,
target, input, environment and candidate G/O/U. The graph checker predicates
are premises throughout. Define Vq(n) by the topological equations for input,
rat, pi, neg, add, mul, positive div_nat, sin and cos. All values are Real;
decimal-token rationals and exact pi are a policy, not loaded binary64 values.
Equal node IDs entail equal Vq values without changing any source definition.

The new plan makes ten dependency families explicit:

| Obligation | Semantic inputs needed |
|---|---|
| K | independent definitions and same-bundle bindings |
| EVAL | K; nine evaluator equations and node congruence |
| SOURCE_ARRAY | K; literals/DH, A, frames, origins, COM, cross, Ii and source invariants |
| USE | EVAL, SOURCE_ARRAY; instance correspondence and preservation |
| OPERANDS | EVAL, SOURCE_ARRAY, USE; actual scalar lowerings of both line-58 terms |
| BODY | EVAL, OPERANDS; checked ordered top-level add |
| SOURCE_LOOP | K; independent source-state recurrence and six-step termination |
| FOLD | EVAL, BODY, SOURCE_LOOP; checked roots and source_updates |
| TARGET | SOURCE_ARRAY, SOURCE_LOOP; independent M_NE^0 definition bridge |
| H_ACC_EXPR | FOLD, TARGET; same-input matrix equality |

This is one sufficient proof decomposition, not a claim that every dependency
is logically necessary in every formalization. Its acyclicity check rejects
a circular plan description only; it cannot detect circular definitions or
hidden assumptions in future proof artifacts. Those require semantic review.

OPERANDS must produce, for all b,r,c, with all summed indices in 1..3:

```text
Vq(Ntranslation[b,r,c]) = m[b] sum_k v[k,r] v[k,c]
H[k,h] = sum_t R[k,t] I[t,h]
Q[k,l] = sum_h H[k,h] R[l,h]
P[r,l] = sum_k w[k,r] Q[k,l]
Vq(Nrotation[b,r,c]) = sum_l P[r,l] w[l,c]
```

Here v,w,R,I are independently interpreted source arrays at that body's RHS;
I=(I_val[b]/3)I3. H,Q,P are mathematical names, not exported temporaries.
Keep the transposed index R[l,h] and the Real adjoint-to-transpose premise.
Finite-sum identities must justify the candidate's actual reduction trees;
these formulas do not assert Julia dispatch, BLAS or FMA evaluation order.
No isotropic or orthogonality simplification is needed.

From the operand equalities and checked B=add(translation,rotation), one
evaluator step yields Vq(B)=Lsrc+Rsrc. SOURCE_LOOP must independently prove
Msrc_0=0 and Msrc_b=Msrc_(b-1)+(Lsrc_b+Rsrc_b). Given checked
S0=rat(0,1), Sb=add(S_(b-1),Bb) in that order, coordinatewise induction gives
Vq(Sb)=Msrc_b. Final roots alias S6; TARGET then gives E_star=M_NE^0.
Calling eval(G) the source state or renaming S6 to M_NE^0 would be circular.
All 216 body and accumulator entries and all 36 final entries are required,
including zero coordinates and both triangles; source_updates has six dense
36-slot before/body_roots/after bindings. Slots are 6(c-1)+(r-1), plus
36(b-1) for a body block. The induction alone supplies no operand refinement.

## Boundaries and reproduction

All plan artifacts and semantic witnesses remain null/verified=false even
when source locations and structure pass. A null occurrence_line_gaps means
no mapping was available, not that aliases passed. Missing evidence is pending
/ exit 3; malformed intake or source drift is rejected / exit 2. There is no
admission-success path. CLI output records only Python inspection, never Julia
execution. The tests use actual snapshot/empty intake and in-memory malformed
envelopes or plan metadata, not synthetic scalar DAGs or observations.

```powershell
python -B examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_contract_audit.py
exit $LASTEXITCODE
```

```powershell
python -B -m unittest discover -s examples/routeb_o0_h_acc_source_refinement -p NEW_SEAM_test_contract_audit.py -v
exit $LASTEXITCODE
```

H_acc_round separately needs actual loaded constants, runtime provenance,
execution/constant-error propagation and interval soundness/coverage. None are
produced here. The current input contract quantifies finite binary64 inputs
whose decoding lies in Q1000; an all-real extension still needs its separate
input-conversion and cover arguments. No H_acc constants, Float64 bits, Julia,
Lean or Lake execution, proof certificate or registry eligibility is claimed.

Validation in this task: all 9 focused tests passed; the actual CLI returned
pending / native exit 3. NEW_SEAM_CONTRACT_REPORT.json was saved from that
Python stdout and strictly re-read equal to a fresh audit object. All 22
pre-existing files in this directory retained their initially read SHA256;
tracked git diff was empty. Two pre-existing untracked .olean files outside
this directory were observed and left untouched. This task added only
NEW_SEAM_contract_audit.py, NEW_SEAM_test_contract_audit.py,
NEW_SEAM_CONTRACT_PLAN.md and NEW_SEAM_CONTRACT_REPORT.json.
