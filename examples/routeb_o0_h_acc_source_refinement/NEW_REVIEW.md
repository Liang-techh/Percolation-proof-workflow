# H_acc source export intake: occurrence-aware refinement design

Current result: **pending / OPEN_H_ACC**, checker exit **3**. There is no real
Julia source export in this submission. `NEW_INTAKE.json` keeps the graph, its
digest, array mapping, six source updates, runtime observations and interval
candidate null. No H_acc constant values, loaded global bits, source DAG or
proof certificate have been exported. No Julia, Lean or Lake execution occurred.

This is an independent candidate protocol, not a replacement installed into the
workflow. All task writes are `NEW_*.py`, `NEW_*.json` or `NEW_*.md` in this
directory. Existing checker, intake, reviews and receipts are untouched. State,
registry, O1 and other agents' files are not modified.
At handoff, Git reports concurrent changes in shared `state.json` and
`scripts/register_routeb_sidecar_frontier.py`, as well as other agents' new files.
Those changes were observed and left untouched; this task makes no claim that
the entire shared worktree stayed unchanged. The five pre-existing files in
this refinement directory retain their initially observed SHA256 hashes.

## Concrete interface bottleneck and change

The original `check_refinement.py` requires every `source_map[role]` reference's
**node definition span** to lie inside that role's anchor. This is awkward for
source operations that introduce an array view or alias without arithmetic:

* `Ri = Tc[ii+1][1:3,1:3]` is a line-51 use of frame entries defined at lines 32–40.
* `Jw[:,jj] = z[:,jj]` is a line-56 use of axis entries selected at line 36.
* `z[:,ii] = Tc[end][1:3,3]` uses the previous frame, including the initial identity.

The same scalar node cannot have one definition span wholly inside disjoint
anchors. This prevents direct cross-role aliases under the old map rule; stage
coverage could still be filled with separately attributed nodes, but would not
explain those aliases. Inserting `add(x,0)` to obtain another span would impose
an extra source-refinement obligation and could alter machine semantics.

`NEW_source_intake.py` therefore uses **definition spans on nodes** and separate
**occurrence spans on dense array records**. Array references may point to an
existing node with a different definition role. Both spans must independently
match the pinned raw source bytes. Explicit slice aliases are checked by node
identity and typed coordinates. This distinguishes where a scalar is defined
from where an array entry uses it; hashes alone still do not prove either claim.

`NEW_INTAKE_SCHEMA.json` is a closed JSON Schema Draft 2020-12 shape schema.
`NEW_source_intake.py` implements the additional semantic consistency rules.
It imports only utility/coordinate/span definitions from the existing checker;
it does **not** submit this new graph to the old `check_export` / `inspect` API.
Old v1 `source_map` submissions are not silently adapted: the new source export
has exactly `layer,source_sha256,nodes,roots`, with occurrence mapping in the
separate `array_mapping` field. Missing new evidence stays pending. An existing
old graph cannot become a new-format source export merely by stripping its map.

## Closed envelope and semantic mapping

Top-level fields are exactly those in `NEW_INTAKE.json`. The source hash is
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`, checked
against the local raw-byte snapshot. The checker does not re-read the deployed
external Julia library. Constant policy is source decimal rationals and exact
pi; input policy is finite binary64 vectors whose decoding lies in Q1000.
Neither policy is a statement about observed loaded Julia values.

Graph nodes retain the original `id,op,args,payload,semantic_role,source_span`
encoding. Operations are input, rat, pi, neg, add, mul, div_nat, sin and cos;
references must be earlier nodes. There is exactly one input node for each joint.
Rational node payloads are reduced numerator/positive-denominator integer
strings. Unknown fields, duplicate keys, boolean indices, nonfinite JSON,
hash drift and unsupported operations are rejected. The graph digest uses the
original UTF-8 sorted-key compact JSON convention; array order is preserved.

| Dense output | Records | Coordinate | Zero-based slot |
|---|---:|---|---|
| `pre_regularizer` | 36 | `[r,c]` | `6*(c-1)+(r-1)` |
| `body_contribution` | 216 | `[b,r,c]` | `36*(b-1)+6*(c-1)+(r-1)` |
| `accumulator_after_body` | 216 | `[b,r,c]` | `36*(b-1)+6*(c-1)+(r-1)` |

Both triangles and every zero coordinate must appear. Roots use
`{coordinate,node_id}`. All output-root definition spans must match their source
anchors: initial zero at line 48, body and accumulator at line 58, final at
58–59. Line 60 is excluded. `S0` must be an exact rational zero node;
each `S_b[r,c]` must literally be `add(S_(b-1)[r,c], B_b[r,c])`, in that operand
order, and final roots must alias `S6`. Sharing a node never permits dropping a
coordinate. The full unsimplified body nodes retain explicit additions even
when their mathematical values vanish.

`array_mapping` has exactly the following tables. Each record is
`{coordinate,node_id,source_span}`; coordinates are index-outer, column-middle,
row-inner for matrices and index-outer, component-inner for vectors.

| Table | Coordinate | Records | Source use / definition obligation |
|---|---|---:|---|
| `A` | `[joint,r,c]`, 4x4 | 96 | DH transform, line 39 |
| `Tc` | `[frame,r,c]`, 4x4, frame 0..6 | 112 | Identity and six transforms, 32–40 |
| `o` | `[frame,component]`, frame 0..6 | 21 | Origin, 33–41 |
| `z` | `[joint,component]` | 18 | Parent axis, 34–36 |
| `COM` | `[body,component]` | 18 | Midpoint, 50 |
| `Ri` | `[body,r,c]`, 3x3 | 54 | Body frame block, 51 |
| `Ii` | `[body,r,c]`, 3x3 | 54 | Inertia with division by 3, 52 |
| `Jv`, `Jw` | `[body,component,joint]`, 3x6 | 108 each | Active prefix and explicit inactive zeros, 53–56 |
| `translation`, `rotation` | `[body,r,c]`, 6x6 | 216 each | Two unsimplified body terms, 58 |

Human indices are 1..6, except frames 0..6. Checked identities are:

```text
Tc[0] is the explicit 4x4 identity; o[0] is explicit zero.
Julia Tc[f+1] <-> mapped Tc[f]; Julia o[:,f+1] <-> mapped o[f].
z[j,r] = Tc[j-1,r,3]                  (same node ID)
o[f,r] = Tc[f,r,4], f >= 1            (same node ID)
Ri[b,r,c] = Tc[b,r,c]                 (same node ID)
Jw[b,r,j] = z[j,r], j <= b            (same node ID)
Jv[b,r,j] = Jw[b,r,j] = 0, j > b      (explicit rational zero)
B[b,r,c] = add(translation[b,r,c], rotation[b,r,c])
```

These identity/zero literals are requirements read from source initialization,
not claimed Julia observations. The schema does not encode guessed loaded DH,
mass or inertia values. Scalar array entries may share definition nodes.

`source_updates` has six records in body order, each with exactly
`body,source_span,before,body_roots,after`. The last three fields are 36-node-ID
arrays in dense column-major order. Before-body-1 repeats the `S0` ID; later
before arrays equal the preceding accumulator slice. Terms and after arrays
must equal the corresponding 36-root slices. This redundantly binds the six
source update occurrences to the literal graph fold and locates each at line 58.

## Mathematical obligations still open

The source gives the following ideal-real target, with no regularizer:

```text
T0 = I4;  Tb = T_(b-1) A_b
p_b = (o_(b-1) + o_b)/2
Jv_b[:,j] = z_j cross (p_b - o_(j-1)), j <= b; zero otherwise
Jw_b[:,j] = z_j, j <= b; zero otherwise
Ii_b = (I_val_b/3) I3
B_b = m_b (Jv_b' Jv_b) + Jw_b' ((Ri_b Ii_b) Ri_b') Jw_b
S0 = 0; Sb = S_(b-1) + B_b; M_NE^0 = S6
```

The occurrence checker establishes some literal indexing and alias conditions.
It does not prove DH literals, A entries, frame products, COM, cross products,
inertia division, or matrix multiplication lowerings. In particular,
`rotation` stage labels and a top-level body addition do not prove the internal
`Ri Ii Ri'` expression: that unsimplified rotation is still C4's target. Source
associativity, reductions and dispatch also need explicit refinement. Shared
zero IDs and alias checks are not substitutes for these equations.

Once C4 is proved, the existing literal fold offers a small C5 induction:
zero gives the base case, and each ordered addition extends the partial sum by
one body. This is the useful mathematical reduction, but no induction witness
or source-to-DAG theorem is supplied here. Required source/target/environment
semantic keys and verified proof dependencies remain future admission inputs;
the new graph digest is only a content binding.

## Runtime intake: observations, not reconstruction

`runtime_observation` is optional and null in the delivered intake. Its closed
shape is in the JSON schema. It binds the source hash and graph digest, and
requires declared Julia exporter/instrumentation/environment/stdout/stderr hashes
plus integer exit code 0. These five artifact hashes are checked for syntax only:
this checker neither reads their referenced artifact bytes nor authenticates
the exporter, selected methods, immutable globals or instrumentation.

Input has six lowercase 16-hex-digit binary64 bit strings. `loaded_constants`
requires all 24 DH and six each of m/I_val entries, with explicit Julia array
types and dense coordinates. No bits are inferred from source tokens. Binary64
values are decoded using exact integer/rational arithmetic; NaN/Inf are rejected,
subnormals are supported, and inputs must decode into Q1000. Original bit strings
are retained, so positive and negative zero differ in observation continuity.

Each of six update events has exactly
`body,source_span,kind,before,body_value,after`. The three value tables each have
36 `{coordinate,bits}` records, including both triangles. `kind` is
`observed_source_update`; before-body-1 must match the positive-zero allocation,
every subsequent before table must equal the preceding after table bit for bit,
and final must equal after-body-6. Observation is strictly after line 58 in body
6 and before line 60. Post-hoc sums, symmetry filling, return-value regularizer
subtraction and zero-regularizer calls are not accepted as observation kinds.

The event tag and continuous values **do not prove** actual execution. In
particular, this checker does not re-evaluate Float64 additions or reductions,
validate body arithmetic, or establish that the logger observed live values.
R0, loaded-constant refinement, kernel/trig semantics and instrumentation
noninterference remain open even for a complete well-shaped observation.

## Interval intake: checkable finite geometry and rational consistency

`interval_candidate` binds the graph digest and canonical runtime-object digest.
It requires a binary partition of the fixed real cube `[-1/1000,1/1000]^6`:

```text
leaf  = {kind: "leaf", id: nonempty unique string}
split = {kind: "split", axis: integer 1..6, cut: canonical rational,
         left: partition, right: partition}
```

Boxes are derived from ancestors, never trusted from submitted leaf bounds.
The cut must be strictly interior to the parent's interval on that axis; its
two children inherit `[lo,cut]` and `[cut,hi]`, and all other axes. Shared closed
faces are intentional. Starting at Q1000, this construction covers the parent
at each split. Exactly one leaf record is required per leaf ID, in left-first
order. Duplicate, missing and extraneous leaves reject. A single whole-cube
leaf is valid partition geometry; it is not an interval certificate by itself.

Each leaf contains every DAG node once in DAG order, all 216 body and accumulator
entries, and all 36 final errors. Node fields are exactly
`node_id,real,constant_error,execution_error,local_rounding,rule_witness`.
Every interval is `[lower,upper]` with canonical rational strings (`"0"`,
`"-1/1000"`; no floats, unreduced fractions or negative denominators).
`rule_witness` must remain null: non-null proof claims are unsupported and reject.

Per-node intended meanings, for the same input and matched node semantics:

```text
real             encloses E_star
constant_error   encloses E_loaded - E_star
execution_error  encloses J_node - E_loaded
local_rounding   encloses the local machine/kernel error (not propagated here)
```

For inputs, rationals, negation, addition, multiplication and positive-natural
division, the submitted real interval must contain the elementary rational
interval extension of its operands. This deliberately accepts a conservative
box-arithmetic protocol; a tighter, dependency-aware bound can be mathematically
valid and still require a new reviewed witness path. Pi, sin and cos interval
soundness, **all error propagation**, and local rounding bounds remain unchecked.
Passing rational rules downstream of an unchecked trig interval is conditional
consistency, not an enclosure theorem. No sampling is used.

Body/accumulator interval rows must alias the referenced node's intervals exactly.
For each final root and every leaf, the checker forms the rational Minkowski sum
of the two signed error intervals and requires

```text
[L,U] = constant_error + execution_error
0 <= max(abs(L), abs(U)) <= leaf_epsilon[r,c] <= global_epsilon[r,c].
```

Thus a final bound that accounts only for execution error rejects. This checks
the algebraic assembly of supplied bounds, not whether either bound is sound.
The identity underlying it is
`J_acc - M_NE^0 = (J_acc - E_loaded) + (E_loaded - E_star) + (E_star - M_NE^0)`.
Only a verified H_acc_expr makes the third term zero. No interval receipt can
discharge that exact identity. All-real input conversion still needs the separate
RN64 input error and expanded cover required by OPEN_CONTRACT.

## Fixtures, status and validation

Final duplicate-key check requested before handoff: `NEW_INTAKE.json` now has
exactly one `source_updates` and one `runtime_observation` key, each null. The
final bytes are parsed with `base.decode`, whose `object_pairs_hook` rejects
duplicate keys at every object depth **before** schema checking. There is no
first-value/last-value-wins interpretation. A new regression injects each named
key twice, both with identical null values and with conflicting null/object
values; the actual audit returns rejected / exit 2 for all four cases without
creating a duplicate-key fixture file. Earlier template concerns must not be
resolved by loading and reserializing with a permissive JSON parser, which could
silently discard a duplicate. Consumers must use this strict intake parser.

`NEW_LAYOUT_FIXTURE.json` contains 36/216/216 expected coordinates, six source
update **slot** mappings and one exact partition geometry example. All evidence
fields remain null. It is explicitly not an intake/export and the checker rejects
it as a submission. The unit tests additionally build transient, incomplete toy
graphs and bit tables to exercise validators. They lack valid export/provenance
envelopes and are never saved as Julia evidence. Their arithmetic operands and
dummy bounds are test data only; no toy data enters `NEW_INTAKE.json` or receipt.

| Submitted condition | Result / CLI exit |
|---|---|
| Missing file or null evidence component | pending / 3 |
| Present malformed data, wrong order/hash/span, promotion claim | rejected / 2 |
| Component referencing an absent graph; interval without runtime binding | rejected / 2, orphan bundle |
| All candidate consistency checks pass | pending / 3, C0–C5 and R0–R2 unverified |

There is no admission-success exit. `--template` returns 0 solely for printing
an empty template; tests returning 0 certify only their assertions. JSON Schema
validation is shape checking only. Existing receipt/child-runner semantics are
not changed or installed into state. Future proof verification needs its own
reviewed contract; this version never accepts a theorem-success flag.

Run from the repository root; both commands are read-only and suppress bytecode:

```powershell
python -B examples/routeb_o0_h_acc_source_refinement/NEW_source_intake.py
python -B -m unittest discover -s examples/routeb_o0_h_acc_source_refinement -p NEW_test_source_intake.py -v
```

The focused extension suite passed 18 tests, including named duplicate-key attacks, malformed submissions,
all dense orders, role spans/line-60 exclusion, occurrence aliases, literal six
updates, runtime bit continuity, rational canonicality, exact partition geometry,
node/root coverage, interval bindings and final two-bridge error domination.
Full genuine source-export integration remains untested because no export was
supplied. `NEW_RECEIPT.json` records the empty-intake audit, not a theorem result.
The untouched original checker suite also passed all 12 tests. The new JSON
schema passed `Draft202012Validator.check_schema`, and the empty template passed
shape validation. The saved receipt is the direct CLI output from the final
checker run, which returned 3. These are development checks only. PowerShell
wrappers should preserve the native code explicitly with `exit $LASTEXITCODE`;
a shell's generic nonzero status must not replace the checker's 2/3 distinction.

**收割结论：schema checker 只做结构、索引、字节绑定和有理数一致性检查。
结构检查通过仍为 pending / exit 3；畸形或重复 key 提交为 rejected / exit 2。
没有真实 Julia export，H_acc_expr、H_acc_round 与 source binding 均未证明，
不能进入 registry 或关闭 H_acc。共享 state 未修改。**
