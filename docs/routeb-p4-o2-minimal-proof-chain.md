# Route-B O2: minimal trustworthy proof chain for T-P4-036.1-.4

This document is a mathematical design for the four virtual O2 leaves. It is
not a metadata audit and does not turn the virtual frontier into theorem nodes.
The intended chain is

```text
exact-real angle/trig contract
        -> Float64 argument inclusion
        -> safe range/quadrant reduction
        -> actual Float64/libm sin/cos enclosure
        -> finite source-order DH propagation
```

The current source anchor is the frozen `dhport_lib.jl` hash
`AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936`; the
finite operation schedule hash is
`58209B231ED2BD1662B74B95CBBE5EE206AB1911BFDF03C8AED99C1BFF80C7C1`.
Those hashes identify the statements being checked. They are not proof of the
runtime or of any numerical enclosure.

## 1. Data types and proof levels

Use exact rational endpoints for every interval consumed by the kernel:

```lean
structure RatInterval where
  lo hi : ℚ
  le : lo ≤ hi

def Contains (I : RatInterval) (x : ℝ) : Prop :=
  (I.lo : ℝ) ≤ x ∧ x ≤ (I.hi : ℝ)

structure Bin64 where
  bits : UInt64

def decode (x : Bin64) : ℝ := -- exact dyadic interpretation of the bits
  ...
```

`decode` is an exact interpretation of a bit pattern. It is not a claim that a
Julia execution produced that bit pattern. An execution trace and its source
binding are separate premises.

There are three different kinds of statement in this chain:

1. **Kernel theorem:** exact real arithmetic, rational interval operations,
   finite products/folds, and trig identities/remainders for an explicitly
   defined real function.
2. **Conditional adapter theorem:** a kernel theorem whose premises include a
   supplied Float64/libm/operation trace. Lean checks the consequence, but the
   trace premise is external unless IEEE-754 and the relevant libm are itself
   formally verified.
3. **External execution receipt:** actual source/runtime identity, bit patterns,
   directed interval results, operation order, and per-box coverage. A hash of
   metadata or a successful numerical run is not such a receipt by itself.

No part of this design sets `formal_certificate_allowed` or
`registry_promoted`.

## 2. Minimal dependency order

The leaves must be consumed in this order; sibling rows in the virtual frontier
do not imply parallel composability.

```text
A0 exact angle contract
  -> 036.1 Float64 angle formation
  -> 036.2 range/quadrant reduction
  -> 036.3 actual libm sin/cos
  -> 036.4 finite DH link/chain propagation
  -> downstream M/P, central-FD, regularizer, solve leaves
```

The source has six links and both `theta` and `alpha`, so the natural counts
are 12 formation inclusions, 12 reduction inclusions, 12 libm enclosures, and
6 link-DAG enclosures. The exact source angle formulas are
`theta_i = q_i + DH[i,1]` and `alpha_i = DH[i,4]`, with phase vectors

```text
theta: 0, -1, +1, 0, 0, 0
alpha: -1, 0, +1, -1, +1, 0.
```

These vectors are useful inputs to a proof, but a reviewed metadata field is
not a proof of the source expression.

## 3. A0: exact-real contract (Lean-formalizable core)

Let `Q` be a rational input box and let `thetaBox i`, `alphaBox i` be rational
intervals. The exact contract should expose the source ordering and constants,
not a Float64 evaluator:

```lean
def theta (q : Fin 6 → ℝ) (i : Fin 6) : ℝ := q i + dhOffset i
def alpha (i : Fin 6) : ℝ := dhAlpha i

theorem exact_angle_contract
    (hq : ∀ i, Contains (qBox i) (q i)) :
    ∀ i, Contains (thetaBox i) (theta q i)
       ∧ Contains (alphaBox i) (alpha i) := by
  -- rational interval addition and exact constants
  ...

theorem exact_sin_cos_cell_sound
    (hx : Contains angleBox x)
    (hred : x = (k : ℝ) * (π / 2) + r)
    (hr : Contains reducedBox r)
    (hquadrant : quadrantSound k) :
    Contains sinBox (Real.sin x) ∧
    Contains cosBox (Real.cos x) := by
  -- exact real identities plus a proved remainder bound
  ...
```

The second theorem can be implemented with rational Taylor remainder bounds
and quadrant identities. It says nothing about Julia, binary64, or libm. It is
therefore a valid Lean target even while `.1-.4` remain open.

## 4. T-P4-036.1: Float64 `pi/2` and angle formation

This leaf binds machine operands to exact-real intervals. The minimum trace has
the bits for `q_i`, the DH constants, `pi`, `pi/2` where used, and the result of
each deployed addition/constant conversion. The required relation is:

```lean
structure AngleFormationTrace where
  qBits thetaBits alphaBits : Fin 6 → Bin64
  sourceKey : String
  runtimeKey : String

theorem float64_angle_formation_inclusion
    (tr : AngleFormationTrace)
    (htrace : traceMatchesSource tr)
    (hq : ∀ i, Contains (qBox i) (decode (tr.qBits i)))
    (hadd : ∀ i, roundedAddSound (tr.qBits i) (dhBits i) (tr.thetaBits i))
    (halpha : ∀ i, roundedConstantSound (dhAlphaBits i) (tr.alphaBits i)) :
    ∀ i, Contains (thetaMachineBox i) (decode (tr.thetaBits i)) ∧
         Contains (alphaMachineBox i) (decode (tr.alphaBits i)) := by
  ...
```

The interval arithmetic and the implication are Lean-formalizable. The facts
`traceMatchesSource`, `roundedAddSound`, and the runtime identity are external
unless a complete IEEE-754 model plus a verified execution trace is supplied.
The receipt must record rounding mode and reject NaN/Inf/overflow; decimal
text equality is insufficient.

## 5. T-P4-036.2: range reduction and quadrant

`.2` consumes the machine argument boxes from `.1` and returns a reduced exact
real cell. It must not be described as a proof of the hidden range-reduction
algorithm inside an opaque libm call:

```lean
structure ReductionWitness where
  input : Bin64
  quadrant : Int
  reduced : RatInterval
  sourceKey : String

theorem range_reduction_sound
    (w : ReductionWitness)
    (hin : Contains inputBox (decode w.input))
    (hidentity : reductionIdentity w)
    (hpi : Contains piBox Real.pi)
    (hcell : reducedCellValid w.reduced) :
    Contains w.reduced
      (decode w.input - (w.quadrant : ℝ) * (Real.pi / 2)) := by
  ...

theorem quadrant_transport
    (hred : reductionSound w)
    (hcell : exact_sin_cos_cell_sound ...) :
    Contains sinBox (Real.sin (decode w.input)) ∧
    Contains cosBox (Real.cos (decode w.input)) := by
  ...
```

The first theorem is a good Lean target when the reduction identity and the
`pi` enclosure are explicit. If the receipt only records a chosen `k` and a
Taylor interval, it proves an exact-real helper, not libm behavior. Libm's
internal reduction is discharged only by `.3`'s certified external libm
contract, or by a separately verified libm specification.

## 6. T-P4-036.3: actual Float64/libm enclosure

The minimum authoritative object is a per-call receipt, not a metadata row:

```text
source_sha256, operation_schedule_hash
runtime: Julia version, OS/arch, libm, BLAS, rounding mode,
         FMA/fastmath/threading configuration
input_bits, output_sin_bits, output_cos_bits
sin_interval, cos_interval          # directed/outward endpoints
finite_non_nan_no_overflow
certificate_id or interval-kernel provenance
```

The Lean-facing interface should treat the receipt as a premise:

```lean
structure LibmSinCosReceipt where
  input : Bin64
  sinBits cosBits : Bin64
  sinBox cosBox : RatInterval
  runtimeKey sourceKey : String
  certified : Bool

theorem libm_sin_cos_inclusion
    (r : LibmSinCosReceipt)
    (hsource : r.sourceKey = canonicalSourceKey)
    (hruntime : pinnedLibm r.runtimeKey)
    (hcert : externalLibmCertificate r)
    (hfinite : r.certified = true) :
    Contains r.sinBox (decode r.sinBits) ∧
    Contains r.cosBox (decode r.cosBits) := by
  -- check the supplied bit/interval witness
  ...
```

The consequence can be checked in Lean, but `externalLibmCertificate` is not
created by a source review, a BigFloat point sample, or a Taylor interval. In
the present project it remains an external receipt obligation.

## 7. T-P4-036.4: finite source-order DH propagation

Freeze the deployed order for each link:

```text
T_prev
  -> extract z_i from T_prev
  -> form A_i from theta_i, alpha_i, sin/cos, d_i, a_i
  -> T_i = T_prev * A_i
  -> origin o_i and rotation R_i
  -> pcom and ancestor-truncated Jv/Jw
  -> link mass/potential contribution
  -> ordered M/P accumulation
```

In particular, `z_i` is the parent transform's z-axis before multiplying by
`A_i`; replacing it by the current transform's z-axis changes the statement.
The source separately calls `fk_frames` from `mass_matrix` and `potential`.
The runtime receipt must show both calls unless a separately proved cache
equivalence is supplied.

The minimal reusable Lean theorem is a generic finite-DAG soundness theorem:

```lean
structure OpWitness where
  opId : String
  inputs outputs : List RatInterval
  outward : Bool

theorem finite_dag_enclosure_sound
    (dag : FiniteOperationDAG)
    (horder : dagRealizesSourceOrder dag)
    (hop : ∀ op ∈ dag.ops, operationSound op)
    (hinput : inputsContained dag)
    (hfinite : noNaNInfOverflow dag) :
    outputsContained dag := by
  induction dag using FiniteOperationDAG.induction <;>
    -- exact interval addition/multiplication/matrix product lemmas
    ...

theorem dh_link_enclosure_sound
    (hprev : TPrevContained)
    (hangles : angleFormationAndReductionContained)
    (htrig : libmSinCosContained)
    (hops : sourceOrderOperationWitness)
    (hfinite : noNaNInfOverflow) :
    AContained ∧ TContained ∧ originContained ∧ zParentContained := by
  exact finite_dag_enclosure_sound ...

theorem dh_chain_geometry_enclosure_sound
    (hlink : ∀ i : Fin 6, dh_link_enclosure_sound i)
    (hcoverage : q ∈ coveredBox) :
    geometryOutputsContained := by
  -- finite fold over six links
  ...

theorem dh_mass_potential_enclosure_sound
    (hgeom : geometryOutputsContained)
    (hmassOps : massMatrixOperationWitness)
    (hpotentialOps : potentialOperationWitness) :
    massOutputContained ∧ potentialOutputContained := by
  ...
```

The interval lemmas, finite fold, matrix product, cross-product, midpoint, and
ordered accumulation can be formalized in Lean. The premises `dagRealizesSourceOrder`,
`operationSound`, the two actual `fk_frames` call traces, and per-box coverage
are external/runtime obligations in the current setup. `.4` therefore cannot
be closed from an abstract interval program or from a matching operation hash
alone.

## 8. What remains after `.4`

Even a valid D3 `M/P` enclosure is not the whole O2 evaluator. The remaining
dependencies are:

```text
D3 M/P
  + O0 regularizer scalar/diagonal bridge
  + h and 2h endpoint Float64 inclusions
  -> q +/- h e_k mass/potential DAG copies
  -> central-FD C/G enclosure
  -> exact_ddq tau - C - G RHS enclosure
  -> explicit M\b conditioning/inverse and solve-residual receipt
  -> per-box O2 composition and coverage
```

The O0 bridge only supplies the conditional diagonal shift
`M_float = M_exact - delta*I` under a common unregularized base. It does not
supply a solve inverse bound. Likewise, a resolvent theorem may consume a
separately proved exact-real inverse bound, but must not be inferred from
regularizer positivity.

## 9. Admission boundary

The smallest trustworthy composition receipt for the four virtual leaves must
bind, per covered box:

```text
source hash and operation-schedule hash
q-box identity and coverage partition
all q/DH/pi/mu/h/2h input and output bit patterns
angle, reduction, libm, and finite-DAG interval witnesses
runtime/libm/BLAS/rounding/FMA/threading identity
finite/non-NaN/no-overflow flags
the two fk_frames call instances for mass and potential
```

Missing runtime/interval evidence is `pending`; malformed or mismatched
evidence is rejected. A metadata review may establish the names and hashes of
these obligations, but it cannot discharge any of the four theorem premises or
close O2. No Lean/Lake compilation or comparator result is implied by this
design.
