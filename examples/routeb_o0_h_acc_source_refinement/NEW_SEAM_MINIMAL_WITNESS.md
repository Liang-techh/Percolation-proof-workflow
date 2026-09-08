# H_acc: non-circular source witness boundary

Status: pending / OPEN_H_ACC. This is an additional interface specification,
not an export, theorem certificate, or replacement admission rule. Existing
NEW_* files, state, registry and shared scripts are not edited.

## Inspected source and minimal sites

Read NEW_REVIEW.md, NEW_INTAKE_SCHEMA.json, NEW_source_intake.py, existing
NEW_SEAM_REVIEW.md / NEW_SEAM_source.py, and the actual snapshot
`examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`.
Its verified raw SHA256 is
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.

The following are freshly located raw-byte intervals, zero-based half-open;
they are not character columns or proposed additional v1 span fields.

| Occurrence | Line | Bytes | Semantic obligation |
|---|---:|---|---|
| z parent-frame read | 36 | [1303,1329) | Read frame j-1 before push |
| Ri body-frame read | 51 | [1830,1853) | Read frame b, not parent b-1 |
| Jw active column | 56 | [2046,2066) | Copy z column j only for j<=b |
| translation | 58 | [2088,2107) | m[b] times Jv transpose-product |
| rotation | 58 | [2110,2136) | Unsimplified Jw'*(Ri*Ii*Ri')*Jw |
| body RHS B | 58 | [2088,2136) | Ordered addition of the two terms |
| accumulator update | 58 | [2083,2136) | New M equals old M plus B |

Necessary context is separate from arithmetic nodes: initialization 32-34,
parent/current sequencing 35-41, fk_frames call 47, zero allocation 48,
body loop 49/59 and active loop 54/57. Inactive Jacobian coordinates retain
line-53 zeros; they have no dynamic line-56 assignment. Line 60 is outside
the observation boundary. A line-58 hash alone cannot distinguish its four
nested expressions, nor instantiate six executions.

## The minimal non-circular contract

Fix one bundle K containing source bytes, graph G, mapping O, updates U,
input interpretation, idealization/environment definition, and an independently
identified target definition. Hashes bind these objects but prove no equations.
Future proof dependencies must reference this same K, including O and U digests;
a graph digest alone does not bind separately supplied occurrence records.
These extra proof bindings belong in a separately reviewed sidecar, not in the
closed v1 intake. No sidecar-verification protocol is installed here.

Let eval(G,q,n) denote the total topological Real evaluator: input is q[j],
rat is its exact quotient, pi is mathematical pi, and neg/add/mul/div_nat/sin/cos
have their Real meanings. Positive natural divisors make this interpretation
total. E_star[r,c] is eval at the final root; it is not a Float64 replay.

For each used occurrence, a source witness must relate the referenced node's
evaluation to the independently defined ideal-real source state at that site
and loop instance. Merely defining source state to equal eval is circular.
Likewise, assuming E_star=M_NE^0 as a record field does not discharge refinement.
Source syntax, source idealization and scalar lowering must have independently
specified semantics. The existing checker supplies structural predicates only.

| Layer | Available candidate predicate | Still-required semantic premise |
|---|---|---|
| Scalar DAG | Topological order, arities, payloads, definition spans | Evaluator equations and literal/input correspondence |
| Occurrences | Dense coordinates, span hashes, same node IDs | Time-indexed source reads and preserved source state |
| Body | B node is add(translation,rotation) | Each operand equals its own source matrix expression |
| Fold | S0 zero; Sb literal add(previous,Bb); final aliases S6 | Source loop-state invariant and target-definition bridge |

Definition and occurrence spans must remain distinct. Same node ID implies
same Real value under the same G and q; it does not assert Julia heap aliasing.
Do not introduce add(x,0), reconstruct a constant node, or alter a definition
span to make a later use fit an anchor.

The occurrence identities are:

```text
z[j,k]   -> Tc[j-1,k,3]
Ri[b,k,l]-> Tc[b,k,l]
Jw[b,k,j]-> z[j,k]       (j<=b)
Jv[b,k,j]=Jw[b,k,j]=0    (j>b)
```

Here frame f corresponds to Julia Tc[f+1]. Establishing these source facts
requires the pre-push/post-push invariant, active-prefix assignment and absence
of interfering mutations. Pure node congruence supplies only the value-equality
transport after those facts are established.

## Body and fold proof obligations, without circular target assumptions

For every b=1..6 and r,c=1..6, independently lower the actual source arrays:
DH literals and angle/trig/A; Tc products; origins; COM midpoint; cross product;
Ri block; Ii=(I_val[b]/3)I; active and inactive Jacobian columns.
Do not export numerical values to stand in for any missing lowering witness.

With v=Jv, w=Jw, R=Ri and I=Ii, required operand conclusions are

```text
eval(N_translation[b,r,c]) = m[b] * sum_k v[k,r]*v[k,c]
eval(N_rotation[b,r,c])
  = sum_l (sum_k w[k,r]*(sum_h (sum_t R[k,t]*I[t,h])*R[l,h]))*w[l,c]
```

All k,l,h,t run from 1 to 3. The second expression keeps both internal matrix
products and the transposed R index. It follows the Real target
(w^T*((R*I)*R^T))*w, not a claim about Julia's machine reduction tree.
Associativity/reduction-tree correspondence is a separate lowering obligation;
no orthogonality cancellation or inertia simplification is required.

The top-level add equation then yields the body equality with one substitution.
It cannot supply either missing operand equality. Every one of 216 coordinates,
including zeros and both triangles, is covered; node sharing does not reduce
coordinate obligations.

For each (r,c), use the independent ideal source-state invariant

```text
before body b: M[r,c] = sum over k<b of B_source[k,r,c]
after body b:  M[r,c] = sum over k<=b of B_source[k,r,c]
```

Line 48 establishes the base. Line 58 and the proved body correspondence give
the step. The existing graph syntax supplies S_b=add(S_(b-1),B_b), with S0 for
b=1, and the final-root alias supplies S6. Thus source-loop semantics plus
evaluator induction identify E_star with the ideal pre-line-60 M.
An independently defined M_NE^0 still needs equality to that ideal source M.
Naming S6 or the source loop result M_NE^0 is not that bridge.

source_updates redundantly checks before/body_roots/after in dense column-major
order, slot 36*(b-1)+6*(c-1)+(r-1). It neither proves loop execution nor observes
the heap. M += is modeled by successive M values, not assumed in-place mutation.

## Exact stopping boundary and next evidence

Current NEW_INTAKE.json has null graph, digest, mapping, updates, runtime and
interval candidate. A fresh read-only seam audit returned status pending,
checker code 3, 27 located fragments, and no export digest. The PowerShell
wrapper surfaced generic process status 1 in that invocation; the displayed
audit object's code was 3. No claim of a Julia or theorem run follows.

The next useful input is a genuine provenance-bound source export with complete
scalar graph, occurrence mapping and six updates, followed by independently
verified source/evaluator/lowering/loop/target witnesses for the same bundle.
All these proof witnesses remain absent here. Missing evidence stays pending;
malformed supplied evidence is rejected by the existing intake rules. Even a
fully shape-consistent candidate has no admission-success path in v1.

H_acc_round remains separate: E_star equality would eliminate only the final
term in J_acc-M_NE^0=(J_acc-E_loaded)+(E_loaded-E_star)+(E_star-M_NE^0).
No loaded constant bits, error constants, runtime observations, interval bounds,
Julia execution or Lean/Lake verification were generated in this refinement.
