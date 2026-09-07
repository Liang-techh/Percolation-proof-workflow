# T-P4-033 O0 H_acc — evaluator, interval receipt, and child decomposition

Verdict: `OPEN_H_ACC_SOURCE_REFINEMENT_AND_INTERVAL_SOUNDNESS`.
This is a source audit and executable-contract design, not a semantic export
or a theorem receipt. Companion:
`examples/routeb_o0_h_acc_semantic_export/OPEN_CONTRACT.json`.
The companion checker checks the design and evidence pins only.

## Current evidence and a provenance correction

The deployed file and the workspace snapshot were read and hashed afresh:

```text
deployed = C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/dhport_lib.jl
snapshot = examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
actual SHA256 = aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
```

The earlier H_acc review instead prints
`aebe6db09b2d943448c5d701631109db8a5eeb070cc66593e5dbaca26485936`.
The `ba8`/`b8a` transcription mismatch is real; it is not source drift.
The authoritative instrumentation REPORT and its manifest contain the actual
hash. Do not silently accept the earlier review's source key. This addendum
preserves that review, including its SHA256
`346fbcd9321a3b8766886117f410314c62b9b5503ef73972d974fa3804b9ce3e`.

Observed workflow state: schema version 1, revision 579, project
`routeb-6dof-external`. `P4.O0.physical_baseline_factor` is open.
Seven O1 source-comparator nodes carry H_acc metadata with
`h_acc_status=OPEN_H_ACC_NO_DEPLOYED_SEMANTIC_EXPORT` and
`h_acc_proven=false`; there is no independently named H_acc node.
This is an observation at the pinned state hash, not a future state assertion.

The existing `routeb_agent_body_trace_design_20260906T071911Z/manifest.schema.json`
checks coefficient payload provenance and a source-binding status enum. It
does not require a source-to-evaluator map, dense matrix outputs, input typing,
constant interpretation, interval coverage, or evidence supporting that enum.
The older `minimum_source_trace_spec.json` expressly leaves Julia Float64
equality and directed rounding open. The 727-row trace and 610-row aggregate
are Fourier coefficient data, not 216 body-value entries or a Julia trace.
Their reported exact coefficient check does not supply H_acc.

## Resolve the meaning of RealSemantics first

Define three different functions, with no coercion between their claims:

1. `E_star(q)`: the source operation graph evaluated over reals using decimal
   literals as rationals and source `pi` as exact π. This is an explicitly
   idealized source lift, not the decoding of the loaded Julia constants.
2. `E_loaded(q)`: the corresponding unrounded real graph with the actually
   loaded Float64 constants decoded as exact dyadics. Keep the `/3` operation
   as a node; if a compiler folds it, the folded value and its error belong
   to the runtime refinement map.
3. `J_acc(qhat)`: the actual machine accumulator immediately after body 6,
   before line 60. Its execution environment and input type must be fixed.

For example, the usual nearest binary64 encoding of the source token `0.8`
is `0x3fe999999999999a`, whose exact decoding differs from `4/5`:

```text
3602879701896397/4503599627370496 - 4/5
    = 1/22517998136852480.
```

This exact rational calculation rules out identifying these two *leaves*.
It is not a computed counterexample for the complete mass matrix. Julia
loaded bits have not been exported here. The DH offsets/twists `±pi/2` and
the division `I_val/3` require the same distinction. A bare
`RealSemantics(Julia DAG)=M_NE` statement is underspecified until this choice
is made. In particular, roundoff bounds relative to `E_loaded` do not yet
bound error relative to the ideal physical target.

The globals `DH`, `m`, and `I_val` are mutable arrays in the source, and `q`
has no declared element type. Bind an isolated inclusion of the pinned file,
the complete post-load values/types of those three arrays, the selected
methods, and an immutable call environment with no intervening mutation.
For the runtime theorem choose an ordinary six-element `Vector{Float64}`.
A source hash alone cannot characterize arbitrary sessions or arbitrary `q`.

## Exact target and smallest evaluator

Use full human joint order 1..6, frame slots 0..6. The source's
`Tc[k+1]` and `o[:,k+1]` represent frame k; `z[:,j]` is column 3 of
frame j-1, captured before transform j. With the exact constants in the
companion, define recursively:

```text
T_0 = I4; o_0 = 0
theta_b = q_b + offset_b
A_b = [[ct, -st*ca,  st*sa, a_b*ct],
       [st,  ct*ca, -ct*sa, a_b*st],
       [ 0,     sa,     ca,    d_b],
       [ 0,      0,      0,      1]]
T_b = T_(b-1) A_b; o_b = T_b[1:3,4]
z_j = T_(j-1)[1:3,3]; R_b = T_b[1:3,1:3]
p_b = (o_(b-1)+o_b)/2; I_b = (Ival_b/3) I3
V_b[:,j] = cross(z_j,p_b-o_(j-1)), W_b[:,j] = z_j  if j<=b
V_b[:,j] = 0,                       W_b[:,j] = 0    if j>b
B_b = m_b V_b^T V_b + W_b^T (R_b I_b R_b^T) W_b
S_0 = 0; S_b = S_(b-1) + B_b
M_NE^0(q) = S_6(q).
```

Do not remove `R_b I_b R_b^T` in the export. Exact rotation orthogonality
permits a separate isotropy lemma; machine rotations need their own error
bound. Existing ideal body definitions with isotropic world inertia are
possible mathematical comparison targets, not a proof of Julia binding.

The minimal reified evaluator is a finite scalar DAG with operations
`input`, `rat`, `pi`, `neg`, `add`, `mul`, `div_nat`, `sin`, `cos`.
Rationals are reduced signed numerator/positive-denominator strings;
`div_nat` accepts only a positive integer (here 2 or 3). Node IDs are unique
and topologically ordered. Each non-leaf references earlier operands with
the declared arity. Leaves have no operands. `input` carries a joint in
1..6; `pi` is a distinguished exact-real constant, never a decimal string.
Subtraction, cross products, matrix products and transposes expand into
these nodes with explicit index maps. A real evaluator handles sin/cos as
real functions; a numerical evaluation is not an exact evaluator proof.

For each `(stage,body/frame,row,column)` record the source span, root ID,
shape and semantic role. Required stages are constants, angle/trig nodes,
`A`, `Tc`, `o`, `z`, COM, `Ri`, `Ii`, `Jv`, `Jw`, translation and rotation
products, `B_b`, `S_b`, and `S_6`. Source lines 31–43 and 46–60 alone specify
the mathematical array operations. They do not establish the dispatched
matrix multiplication reduction, fusion, or compiler lowering. A scalar
reference loop is a proposed refinement target, not automatically the
deployed machine trace. The source-refinement child must bind this map.

This finite exact graph can be shared by all 36 outputs and all six bodies;
no 610-row Fourier expansion is needed to prove this H_acc expression child.
Prove loop invariants once, rather than 216 unrelated identities.

## Minimum 36-entry/body/index artifact

The future bundle must contain the pinned source snapshot, exact constants,
source map, scalar DAG, root manifest, typed runtime environment, proof
receipts, and, for the interval branch, a box cover and node enclosures.
The exact target serialization and each file require SHA256 bindings.
The legacy Fourier source/state keys are context only: add a semantic key
containing the deployed source, DAG, target, constant policy, and runtime
environment hashes. An inherited `mu=1/1000000` key must not insert mu into
this pre-regularizer target.

The mandatory output root arrays, and the value arrays for every state/box,
are dense and ordered as follows:

| Array | Coverage | Order |
|---|---|---|
| `pre_regularizer` | all 36 `(r,c)` | column c outer, row r inner |
| `body_contribution` | 216 `(b,r,c)` | body b outer, then c, then r |
| `accumulator_after_body` | 216 `(b,r,c)` | body b outer, then c, then r |

The flat zero-based matrix slot is `(c-1)*6+(r-1)`. Julia human b/j/r/c
convert to `Fin` by subtracting 1; frame k already has range 0..6.
All entries, including inactive-column zeros, both matrix triangles and
zeros in the final matrix, must have records. Reusing the same DAG zero
root is allowed; omitting its coordinate is not. In exact DAG evaluation
symmetry may be a lemma. Runtime output must not be filled by copying one
triangle. Preserve six actual accumulator updates; a post-hoc sum of body
values is not a trace of those updates. `S_0` is a declared exact zero matrix.

Every box must bind the same roots and include intermediate node enclosures.
Each state trace records q's raw 64-bit words, body and accumulator raw
words at the source observation points, and run stdout/stderr/exit code.
Instrumented code requires its own hash, patch, and refinement evidence.
`mass_matrix(q; regularization=0.0)` still executes line 60; it is not the
specified observation point without a separate return-to-accumulator lemma.
Subtracting a regularizer from a rounded return value is also insufficient.

## Interval branch: a quantified relation, not a sample receipt

Two input policies must be distinguished. The minimal runtime policy is

```text
forall qhat : FiniteBinary64^6,
  q = Decode(qhat), q in Q1000 ->
  abs(Decode(J_acc(qhat))[r,c] - M_NE^0(q)[r,c]) <= epsilon[r,c].
```

This quantifies over all representable inputs in the domain, not all real
inputs. If a downstream theorem needs every real q, require the stronger
contract with `qhat=RN64(q)` and an input-conversion error child. Enclose
these rounded inputs even when they fall just outside the original box.
State which policy the receipt proves; neither policy is inferred from
finite runtime samples.

For a rational box `X`, maintain a real target enclosure `R_n(X)` and an
error interval `D_n(X)` for machine-value-minus-target at each node. Leaf
errors include constant loading and, if applicable, input conversion.
For a binary multiplication, an outward recurrence is

```text
D_mul includes R_left*D_right + R_right*D_left
                 + D_left*D_right + delta_machine_mul
D_add includes D_left + D_right + delta_machine_add
D_acc[b,r,c] includes D_acc[b-1,r,c] + D_body[b,r,c]
                       + delta_machine_acc[b,r,c].
```

All interval operations use rational outward bounds. Real sin/cos range
and pointwise `|sin(x+d)-sin(x)|<=|d|`, likewise cos, handle argument error;
an additional bound for the actual runtime trig implementation is still
required. Do not assume it is correctly rounded. Pin π bounds, range
reduction, precision and remainder proof. Products must enclose the actual
selected kernels (or a proved set of allowed reduction/FMA behaviours),
including their intermediate values. Rounding lemmas need overflow,
subnormal and underflow handling; `gamma_n` alone without its hypotheses
does not close these nodes. Runtime selection/lowering is currently absent.

An equivalent, often simpler proof organization is

```text
|J_acc(qhat)-M_NE^0(q)|
 <= |J_acc(qhat)-E_loaded(Decode(qhat))|
  + |E_loaded(Decode(qhat))-E_star(Decode(qhat))|
  + |E_star(Decode(qhat))-E_star(q)|.
```

The last term is zero only for decoded-input policy. The equality
`E_star=M_NE^0` is a separate expression child. Bounds on loaded constants
cannot be silently deleted from the middle term.

Use a finite partition tree of rational closed boxes with root Q1000. Each
split partitions one coordinate at an interior rational cut; both children
retain other bounds. Check every leaf, not a volume sum or sampled cover.
For each matrix coordinate take the maximum certified leaf error radius.
Two independently sound intervals can give a conservative difference bound
by interval subtraction; mere overlap proves no prescribed error bound and
never proves functional equality. Zero-width differences must themselves
be established by a sound checker before they can imply equality.

`H_acc_round` does not discharge `H_acc_expr`, nor can it be consumed by an
exact physical-mass equality. It can serve only a downstream statement that
explicitly carries its error budget. No such budget is consumed here.

## Proposed theorem children (all OPEN; not inserted into state)

The companion lists dependency edges and exact responsibilities. The useful
induction invariants are `Tc[b+1]=T_b`, `o[:,b+1]=o_b`, the parent-axis
identity before each update, active/inactive Jacobian columns, and
`S_b=sum_{k=1}^b B_k`.

| Child | Required conclusion |
|---|---|
| C0 source refinement | Pinned source and environment map to the reified array/scalar graph; literal idealization is explicit |
| C1 evaluator soundness | Every scalar DAG operation has its stated real semantics |
| C2 frames | Six DH steps, seven frame slots, origins and parent axes agree |
| C3 Jacobians | Midpoint COM, cross-product sign, and all prefix/zero columns agree |
| C4 body | For each b and all q/r/c, exported body root equals the unsimplified NE body term |
| C5 accumulator | Initial zero and six ordered updates yield all 36 entries of M_NE^0 |
| H_acc_expr | C0–C5 imply the idealized deployed-source expression identity |
| R0 environment | Actual constants, input policy, methods and kernel execution are bound |
| R1 intervals | Constant/input/trig/arithmetic/kernel enclosures are sound |
| R2 cover | Every required input is covered and all 36 final errors are bounded |
| H_acc_round | Expression identity plus R0–R2 gives the chosen machine-error theorem |

C4 is one generic body theorem instantiated six times (with 216 roots),
not six Fourier `h_body_i` assumptions. C5 is a finite loop-fold theorem,
not the Fourier aggregate function lift. C2/C3 may use existing exact frame
lemmas only after C0 identifies their definitions; names containing
`juliaExact` and syntactically present Lean proofs are not this identification.
No existing O1 adapter needs to change for this decomposition.

## Executable checks and admission boundary

Run `python examples/routeb_o0_h_acc_semantic_export/check_contract.py`.
It checks pinned source/review/schema bytes, the explicit coordinate
order, exact constants, acyclic child dependencies, required artifact list,
and false admission flags. State bytes are compared with the recorded
observation separately: a concurrent state revision is reported as stale
observation, not used to rewrite history or alter source evidence. During
this audit another task updated state and O1 files; those edits were left
untouched. It deliberately returns OPEN as the mathematical
verdict even when the design checks pass. `--self-test` checks rejection of
missing/duplicate entries, broken dependencies, wrong source hash and false
promotion. It is not an interval checker, Julia exporter, or proof checker.

Missing evidence remains pending. A future submitted receipt with wrong
hash/order, missing coordinates, unknown operations, unsupported kernels or
unsupported promotion is rejected as evidence; it never closes the theorem.
A successful executable or schema check is not a formal receipt. Future
formal admission requires source-bound definitions, actual proof artifacts,
dependency/axiom audit and the existing explicit verification gate.

The immediate missing artifact is therefore the same-source finite DAG and
source-refinement witness with 36 final, 216 body and 216 accumulator roots,
plus the explicit index/literal policy. The interval branch additionally
needs a supported runtime kernel contract and a complete box receipt. No
such artifact was supplied by the examined reviews, state or schemas.
No Julia, Lean or Lake was executed; state, registry, deployed source and
Route-B O1 adapters were not edited. Numerical evidence was not promoted.
