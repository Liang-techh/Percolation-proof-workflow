# H_acc minimal source-refinement intake — 2026-09-07

Verdict: **pending / OPEN_H_ACC**. This independent artifact supplies a closed
executable schema/checker and an empty intake. No real source export was supplied
to this intake. No Julia constants, loaded bits, DAG nodes or roots were created.
`source_export`, its hash, and `runtime_evidence` remain JSON `null`.

Files: `check_refinement.py` defines the executable schema; `intake.json` is its
empty template; `RECEIPT.json` is the captured read-only audit output;
`test_refinement.py` checks the intake boundary. The checker itself does not
read or write O1, workflow state, registry, or admission machinery. The user has
reported attaching this checker to the H_acc child; that attachment is an intake
check dependency only. It supplies no semantic evidence and cannot close H_acc.

## Source and span binding

The existing snapshot is
`examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`.
Its raw-byte SHA256, also checked against the deployed file during this task, is
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.
The earlier review's `...109db8a...` transcription is not accepted.

The checker reads the snapshot, never includes or executes Julia, and does not
continually audit the external deployed file. Receipt spans are one-based,
inclusive line intervals hashed with original newline bytes preserved. Important
anchors are constants 6–13, frames 31–43, COM 50, rotation 51, inertia 52,
Jacobians 53–56, initial zero 48, and body/accumulator expression 58. Final
observation is after the sixth update and before line 60. Per-role span hashes,
the submission byte hash and checker byte hash are in `RECEIPT.json`.

Hashes identify bytes. They do not authenticate an exporter or establish that a
node implements the source expression at its declared span.

## Dense output contract

| Array | Count | Human coordinate record | Iteration order | Zero-based flat slot |
|---|---:|---|---|---|
| `pre_regularizer` | 36 | `[row,column]` | column, then row | `(column-1)*6+(row-1)` |
| `body_contribution` | 216 | `[body,row,column]` | body, then column, then row | `(body-1)*36+(column-1)*6+(row-1)` |
| `accumulator_after_body` | 216 | `[body,row,column]` | body, then column, then row | `(body-1)*36+(column-1)*6+(row-1)` |

Human bodies, joints, rows and columns are 1..6; frames are 0..6.
`Tc[frame+1]` and `o[:,frame+1]` represent that frame. `z[:,joint]` is the
parent frame's axis before the current transform. COM uses frames body-1/body;
Jacobian columns joint<=body are active. Human indices convert to Fin by
subtracting one; frame indices are already zero-based.

Both triangles and inactive zeros require records. A shared zero root is legal,
but omitted coordinates are not. Require `S0=0`, then literal DAG additions
`S_b[r,c]=add(S_(b-1)[r,c],B_b[r,c])` in body order 1..6. Final roots alias S6.
The checker enforces this syntax, not the mathematical meaning of B_b.

## Semantic layers and runtime policy

`E_star` is the unrounded real graph with decimal source tokens interpreted as
rationals and pi as exact pi. `E_loaded` uses actual Julia-loaded Float64
constants decoded as exact dyadics, retaining division nodes. `J_acc` is actual
machine execution at the pre-regularizer observation point. Loaded constants
and the machine trace are absent. Source tokens are not asserted to be Julia
loaded values. No orthogonality/isotropy simplification may silently remove
`Ri*Ii*Ri'` from the intended body target.

The exact expression target is the full unsimplified six-body Newton–Euler sum:
`B_b=m_b*Jv_b'*Jv_b + Jw_b'*(Ri_b*((I_val_b/3)*I3)*Ri_b')*Jw_b`,
`M_NE^0=S6`. Proving `E_star=M_NE^0` remains separate from bounding
`E_loaded-E_star` and `J_acc-E_loaded`. A canonical export digest below is a
structural content key, not the future exact-target/proof/environment semantic
key and not a theorem identifier.

The fixed runtime policy quantifies over all finite six-entry
`Vector{Float64}` inputs whose exact decoding lies in Q1000. An all-real-input
extension requires a separate RN64 input-error proof and expanded cover.
Isolated inclusion, actual DH/m/I_val types/shapes/raw bits, immutable globals,
selected methods, Julia/compiler/platform, BLAS kernels/threads, trig behavior,
reduction/fusion/folding, rounding, overflow and subnormal behavior must be bound.
No such execution environment is supplied or assumed by this artifact.

Runtime evidence must observe all six actual updates and all dense coordinates.
A post-hoc sum, symmetry filling, subtracting the regularizer, or calling with
regularization=0 does not establish that observation. Instrumentation needs its
own source/patch hashes and refinement evidence plus stdout/stderr/exit code.
Intervals need a complete rational partition of Q1000, all intermediate/body/
accumulator enclosures, 36 final error bounds, and soundness/coverage evidence.
No interval or runtime proof is implemented here.

## Executable schema and fail-closed result

The top-level fields are exactly those in `intake.json`; unknown fields or altered
policy/admission fields are rejected. The supported optional `source_export`
object has exactly `layer`, `source_sha256`, `nodes`, `roots`, `source_map`.
Only `layer="E_star"` is supported. Its SHA256 is computed over UTF-8 JSON with
sorted keys, compact separators, ensure_ascii=false, and no nonfinite values.
Array order is preserved. Duplicate JSON keys are rejected before checking.

Nodes have exactly `id,op,args,payload,semantic_role,source_span`. IDs must be
unique and operands earlier in the list. Operations/arity are input(0), rat(0),
pi(0), neg(1), add(2), mul(2), div_nat(1), sin(1), cos(1). Input payload is
`{joint: integer 1..6}`; rat payload uses reduced integer strings
`{numerator,denominator}` with positive denominator; div_nat has a positive
integer `divisor`; other payloads are empty objects. These are encoding rules,
not exported constants. Node spans must match the pinned bytes and role anchors.

`roots` has exactly `initial_zero` (an existing zero node ID) plus the three
arrays above. Array records have exactly `coordinate,node_id`. `source_map`
contains the complete stage-key set in the checker's `SPANS`, each mapped to
nonempty existing-node lists; output-stage lists must match the ordered root
arrays. All nodes must occur under their declared role. This is stage coverage;
full intermediate array shapes, index semantics, literal/source correspondence,
unsimplified body identity and dispatch refinement still require C0–C5 evidence.

| Input | Receipt | CLI exit | Admission |
|---|---|---:|---|
| Missing file or null source export | pending | 3 | false |
| Present malformed export, wrong hashes/order/refs, or promotion request | rejected | 2 | false |
| Structurally valid E_star candidate | pending / PASS_STRUCTURE_ONLY | 3 | false |

There is no theorem-success exit. `--template` alone exits 0 for printing an
empty template. Future proof/runtime submissions need a separately implemented
and reviewed verification path; this version does not consume proof claims.

Run from the repository root:

```powershell
python -B examples/routeb_o0_h_acc_source_refinement/check_refinement.py
python -B -m unittest discover -s examples/routeb_o0_h_acc_source_refinement -p test_refinement.py -v
```

All 12 focused tests passed; a direct CLI run also returned exit 3 with the
pending JSON saved in `RECEIPT.json`. Validation covers missing evidence,
malformed submissions and JSON, source/hash
drift, policy/promotion tampering, all coordinate slots and reordering/omission/
duplication/type attacks, and source spans including rejection of line 60.
Tests use no fabricated Julia constants or roots. Full real-export execution of
the optional DAG path remains unavailable until a genuine source export arrives.

The saved receipt is pending with `REAL_SOURCE_EXPORT_ABSENT`,
`SOURCE_REFINEMENT_WITNESS_ABSENT`, and `RUNTIME_AND_INTERVAL_EVIDENCE_ABSENT`.
Its explicit scope is `intake_schema_and_structural_consistency_only`, and its
`checker_exit_code` is 3. A child runner must preserve pending on this exit and
must not interpret successful checker invocation, parseable JSON, or attachment
to a child as a successful theorem check. Present malformed evidence exits 2;
even a structurally valid source candidate remains pending/exit 3.

Julia, Lean and Lake were not run. This task did not modify O1, state or registry;
no source theorem, VERIFIED status, baseline or Schur budget was claimed.
