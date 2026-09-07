# O1 body-6 canonical export: support coincidence and source theorem boundary

Status: `COEFFICIENT_REPLAY_MATCH_SOURCE_THEOREM_OPEN`

Scope: human body 6 / CSV `body=6` / Lean `(5 : Fin 6)` only.
The canonical CSV, receipt, contract and target sidecar are separate additions.
The main adapter, existing body-3/4/5 files, old support/reviews, and workflow
state were not edited by this work. No local Lean/Lake, Julia, comparator,
registry admission, or source-bridge execution was performed.

## Evidence changes the interpretation of the old support artifact

The existing `O1_BODY_6_SUPPORT_TARGET.json` correctly records 610 rows,
32 nonempty matrix entries and the open source binding. Its stronger
interpretation, that the aggregate-shaped support itself makes this an
incorrect human-body slice, is not established by those counts.

The focused audit distinguishes support equality from coefficient equality:

| Check | Observed result |
|---|---|
| Selected body-6 rows / frozen aggregate rows | 610 / 610 |
| `(row,col,nu1..nu6)` support sets | Equal |
| Keys with different exact Gaussian-rational coefficients | 57 |
| Pre-accumulation body-6 callbacks | 36 distinct matrix entries |
| Fresh selected callback map versus existing body-6 CSV map | Exact match |
| Nonempty / empty entries | 32 / 4 |
| Conjugate-frequency / transpose symmetry | Both pass at coefficient level |

One discriminating key, using one-based matrix indices, is
`(row,col,nu)=(1,1,(0,-2,-2,0,0,0))`:

```text
body 6:   -699/512000       + 0*i
aggregate: -63683/12800000  + 0*i
```

This is a counterexample to equality of the two coefficient maps, not a
counterexample to the existing body-6 source theorem. It does not establish
either source-to-Fourier theorem. It also does not rely on numerical sampling.

The pinned artifact-local exporter already captures the individual body term:
`routeB_fourier_rational_probe_trace_sink.py:149` forms `body_term`, line 153
calls `body_trace_sink(i+1,r+1,c+1,body_term)`, and line 154 updates the
aggregate. The audit invokes `build(body_trace_sink=sink)` and retains only
callback body 6. It does not execute the exporter's `main()` or reconstruct
body 6 by subtracting other body contributions from the aggregate.

Thus a new set of different coefficients is not presently justified. The
existing values can be independently serialized as a body-6 candidate with
explicit pre-accumulation provenance. The remaining semantic gap is between
that exact Python construction and the actual Lean `sourceBodyMass` function.
Deployed Julia equivalence remains outside this result.

## Files delivered and minimum receipt

All files below are under `examples/routeb_b45_source_comparator_lean/`:

- `O1_BODY_6_CANONICAL_SLICE.csv`: independently emitted body-6-only payload.
- `O1_BODY_6_CANONICAL_EXPORT_CONTRACT.json`: source, indexing, serialization,
  regularization, receipt and downstream theorem contract.
- `O1_BODY_6_CANONICAL_EXPORT_RECEIPT.json`: observed replay evidence and
  explicit missing proof receipts; no fabricated theorem/compile result.
- `RouteBO1Body6CanonicalExportTargets.lean`: uncompiled proposition targets.
- `audit_body6_canonical_export.py`: read-only pinned replay, emitting a JSON
  bundle to stdout. It does not write the CSV, receipt, state or other files.

The CSV is generated from the selected callback map, sorted by exact integer
key, with reduced rational coefficients, positive denominators and full signed
frequencies. Its serialization is UTF-8 without BOM and LF with a final newline.
The four absent entries are `(4,5),(5,4),(5,6),(6,5)` in one-based notation;
their zero complement must be included in a future all-entry theorem.

The receipt binds the original O1 `source_key` and `state_key`, an independent
`body6_export_key`, the payload/hash/counts, pinned input/sink/audit hashes,
the replay entrypoint and result, the hashed contract and target files, and
explicit absent proof evidence. The aggregate hash in the inherited
`source_key` is context, not the body-6 payload's identity. Renaming that
context would break the existing consumer contract.

The same-key `mu=1/1000000` is retained as consumer context, but the body term
contains no regularizer. `mu*I` belongs outside the six-body sum. A change in
domain, body label, sign convention, index mapping, source/state key or
regularization requires a new compatible receipt; malformed or mismatched
present evidence is rejected. Missing theorem evidence stays pending.

The audit is specific to these pinned inputs. It is not a general intake
validator for arbitrary external receipts. Its exit code 0 and the receipt
status establish only the recorded coefficient checks and provenance.

## Concrete mathematical targets

Use zero-based joints and origins in this paragraph. Write `o_j` for the
source origin and `z_j` for the parent-frame axis. Since the sixth DH step has
`a6=0` and `d6=7/100`, the small geometry target is

```text
o6 = o5 + (7/100) z5,
c6 = (o5+o6)/2 = o5 + (7/200) z5,
v_i = z_i cross (c6-o_i),  i=0,...,5.
```

The body-6 mass is `3/20`; its isotropic inertia is `(1/60) I_3`, already
divided by three, with no extra mass factor on the angular term. Define

```text
G6_ij(q) = (3/20) sum_a v_i[a] v_j[a]
         + (1/60) sum_a z_i[a] z_j[a].
```

The sidecar separates these goals:

1. `Body6EndpointTarget`, `Body6CenterTarget`: bind the sixth endpoint and
   midpoint to the concrete source frame chain.
2. `Body6SourceGramTarget`: prove `sourceBodyMass q 5 i j = G6_ij(q)`.
3. `Body6GramFourierTarget rows`: prove the Gram expression equals the real
   Fourier evaluator of the canonical rows, for every `q,i,j`, including
   the zero complement.
4. `Body6LegacyTraceTarget rows`: prove that evaluator equals the immutable
   `bodyTraceEvaluator 5 q i j` currently used by the main adapter.

The explicit `rows : List CanonicalRow` parameter has no supplied inhabitant.
The canonical CSV must still be reified into typed rows with its hash and
finite-sum semantics checked. Merely choosing arbitrary rows or putting a
proof field in a receipt does not satisfy any target. Rational coefficient
tags are interpreted by `a*cos(nu*q)-b*sin(nu*q)`; signed frequency pairs
are retained and no extra factor two is inserted.

Several smaller structural leaves can be pursued before expanding 610 atoms:

- `v_5 = z_5 cross ((7/200) z_5) = 0` by the alternating cross product.
- `sourceBodyMass(q,5)_(i,5) = (1/60) dot(z_i,z_5)` after the source Gram step.
- The `(5,5)` entry is `1/60` once `dot(z_5,z_5)=1` is proved from the source
  rotation chain. The CSV has precisely this constant coefficient; that
  observation is not the source proof.
- The body matrix is independent of the last coordinate `q(5)`: axes are
  captured before their respective steps, and the last endpoint translation
  does not depend on the last rotation. The corresponding source target is
  explicit. The CSV check `nu6=0` is only coefficient-side evidence.

All these sidecar declarations are propositions, not proofs. The file has
not been compiled. In particular, no source geometry assumption has been
silently replaced with CSV coefficient identities.

## Downstream theorem boundary

For the actual reified canonical row list `rows`, equality transitivity gives
the proposed dependency chain:

```text
SourceGram + GramFourier
    => CanonicalSource(rows): sourceBodyMass q 5 i j = CanonicalEval(rows,q,i,j)
CanonicalSource(rows) + LegacyTrace(rows)
    => existing adapter h_body_6
```

Both arrows describe conditional mathematical composition, not supplied Lean
proofs. The current `h_body_6` at `RouteBO1PerBodyTraceAdapter.lean:36` still
uses the old generated evaluator. A new CSV, a new evaluator name or matching
CSV bytes cannot rewrite its right-hand side automatically. Here the old and
new selected maps match exactly at the coefficient level; the typed
reification/finite-fold equality remains an independent obligation.

The existing adapter quantifies over **all** `q : Fin 6 -> Real`. A theorem
only at `q=0` or only on the inherited radius-`1/1000` cell cannot discharge
that target. Even a future proof of `h_body_6` would not supply the other five
body proofs, the independent aggregate real-function lift, typed `M_DD45`
binding, or an O1 left-inverse witness.

## State and validation disposition

The first state inspection observed revision 579; the saved receipt binds a
single read of revision 580, SHA-256
`ed3d600323877d00b2edc4f18dfce31b6688e23337cd12f7758a269391686207`.
The node `3ad9bd4fa1d040da995906fc487913fd`, named
`P4.O1.source_comparator.h_body_6`, remains `open`. This is a read-only
snapshot, not a current-state admission claim. The old support status
`OPEN_BODY_LABEL_SEMANTIC_MISMATCH` remains recorded in state and in its
original artifact; this review supplies the narrower, evidence-backed
interpretation without mutating historical state.

At the final read, concurrent workspace activity had advanced state to
revision 582 (body-6 node still `open`) and changed a separate body-5 target
file. Neither change was made or reverted by this work. The receipt retains
its revision-580 observation; it is not rebound to an unrelated later state.
The main adapter SHA-256 remained
`6b50ae63c9770e3481f79511141c8cc55d592b5c550f686654c5e756584399ef`.

Final persistence checks passed: the CSV bytes match the receipt's payload
hash, all pinned input and evidence-file hashes match, all five output hashes
listed below match disk, and every proof/admission flag remains false.

The focused audit completed with exit code 0; the user also reported a local
exit-code-0 run. Its explicit exact checks cover pinned input hashes, body-6
mass/inertia and endpoint constants, 36 callback entries, replay equality,
57 distinguishing coefficients, signed conjugacy, transpose symmetry,
`nu1=nu6=0`, and the sixth diagonal constant. No broad regression was run.

`source_binding_proven`, `trace_reification_proven`, `h_body_6_proven`,
`aggregate_function_lift_proven`, `comparator_accepted`, `registry_eligible`
and `formal_certificate_allowed` are all false. Compile status is `NOT_RUN`;
registry status is `pending`. No source bridge or VERIFIED claim is made.

## Bound output hashes

```text
O1_BODY_6_CANONICAL_SLICE.csv
46f59e5db4d74a03d5106cee4bd501090dbeec51cc897edcfd68e559ac939c7c

O1_BODY_6_CANONICAL_EXPORT_RECEIPT.json
4271e4c75bf822e6db99ad4919aa86235623357de7c2587cf67e19eeef816458

O1_BODY_6_CANONICAL_EXPORT_CONTRACT.json
0e03ea7e7a216574f3f76ae433a0b3bef1463675d490739da94a5635aba2eeb1

RouteBO1Body6CanonicalExportTargets.lean
24635bd0356e6c9a83b15eb0f616327b547caf9257f8992f99b5fb1b7983ce2c

audit_body6_canonical_export.py
b88588960f48feca9eae913aec172090ee9d0e9d53e88bfd4a437c41197a1981
```
