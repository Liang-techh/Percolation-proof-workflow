---
kind: review_result
task_id: T-P4-036.2
source_agent: Codex
created_at: 2026-09-07
integration_status: pending
---

# T-P4-036.2 exact-real trig child review

## Decision

The smallest locally closable object is the **exact-real range-reduction and
trigonometric-cell sublayer** of `.2`, for the declared local input box. Its
status is:

```text
EXACT_REAL_TRIG_CELL_CLOSED_CONDITIONALLY
Float64/libm binding: OPEN
D1/D2/D3 composition: OPEN
```

This is a mathematical child result only. It is not a closure of the virtual
frontier row, the O2 node, or the theorem registry. No metadata review is used
as a proof premise.

## Mathematical payload

The canonical exact-real contract uses, for link `i` and atom `a ∈ {theta,
alpha}`,

```text
x_i,a = q_i + k_theta[i] * pi/2       (theta)
x_i,a =       k_alpha[i] * pi/2       (alpha)
r_i,a = x_i,a - k_a[i] * pi/2.
```

The phase vectors are

```text
k_theta = (0,-1,+1,0,0,0)
k_alpha = (-1,0,+1,-1,+1,0).
```

For the declared local contract, `q_i ∈ [-3/20,3/20]`; the alpha rows are the
singleton `q=0` rows. The rational `pi` enclosure and the CSV's reduced
intervals put every reduced argument in the Taylor domain `|r| ≤ 1`. The
quarter-turn center table is exact:

```text
k mod 4:       0       1       2        3
(sin c,cos c): (0,1)   (1,0)   (0,-1)   (-1,0).
```

The order-12 Taylor remainder, exact rational coefficient arithmetic, and
quadrant transport therefore give a conditional exact-real interval for each
of the 12 `sin/cos` calls. The claim is conditional on the stated input box,
the exact `pi` enclosure, and the row-wise phase/reduction data; it is not a
claim about a machine call.

## Minimal theorem interface

The smallest Lean-facing interface is independent of Julia and binary64:

```lean
theorem exact_trig_range_reduction
    (hq : q ∈ qBox)
    (hpi : Real.pi ∈ piBox)
    (hphase : phase k)
    (hrow : reducedRowSound qBox piBox k reducedBox) :
    reducedBox.contains (q + (k : ℝ) * (Real.pi / 2)
                         - (k : ℝ) * (Real.pi / 2)) := by
  ...

theorem exact_sin_cos_cell_sound
    (hred : reducedBox.contains r)
    (hcenter : centerTableSound k)
    (htaylor : order12TaylorRemainderSound reducedBox) :
    sinBox.contains (Real.sin ((k : ℝ) * (Real.pi / 2) + r)) ∧
    cosBox.contains (Real.cos ((k : ℝ) * (Real.pi / 2) + r)) := by
  ...
```

The interval endpoint order, rational arithmetic, finite row fold, Taylor
remainder, and exact quarter-turn identities are suitable for Lean
formalization. This review does not claim that these declarations have been
compiled: no Lean/Lake run was performed. The output status is therefore a
conditional mathematical child, not `LEAN_VERIFIED`.

## Dependency boundary

### Canonical source dependency

The child is source-indexed, but not runtime-bound. Its source contract is:

```text
canonical source: robot_final/dhport_lib.jl
state-bound mirror: routeB_dense_Mq/dhport_lib.jl
source SHA-256: AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
source semantics: theta=q[ii]+DH[ii,1], alpha=DH[ii,4], then cos/sin
```

The exact-real row artifacts are:

```text
P3_DH_TRIG_CHAIN_CONTRACT.md
  SHA-256: 78E8AB5695BC47ED3347D6AA10F3BD7E2BC7B84D6C0A9120ADB31E277EC09CA1
routeb_p3_dh_trig_chain_contract.csv
  SHA-256: 87C326FD0E2F2A69EB330A562E30917521DB2C35C69E5A4AFECC6932998CA8E3
```

The source hash binds the formula being modeled. It does not prove that
Julia's `Float64` operations or libm outputs lie in the exact-real rows.

### State dependency

At review time the routing snapshot was:

```text
node: P4.true_dh_float64_evaluator_enclosure
node status: open / OPEN_INTERFACE_DRAFT__UNCOMPILED
state revision: 502
state checksum: e394753701c9654a8de69d525cf29c9af3f522ee5cb1ae42406ee6d750c391ca
virtual composition: T-P4-036.1-.4, all required, per-box coverage required
```

This state snapshot is only an integration key. The review does not modify it,
close the parent, or infer proof status from its metadata. If the node's source
or contract artifact hashes change, this child must be re-bound.

### Coverage dependency

The child covers only the declared local angle rows:

```text
12 rows = 6 links × {theta, alpha}
q_i ∈ [-3/20,3/20] for theta
alpha rows at singleton q=0
```

It does **not** provide the O2 per-box partition, full `q/dq/w` coverage, or
coverage composition with D1/D2/D3. A parent may consume this child only when
its input box is exactly within the declared local contract and the row index
is mapped to the same canonical source/link order. A coverage receipt remains a
separate external dependency.

## Why this child closes and the next ones do not

The exact-real child has a finite list of rational rows, exact center values,
an explicit reduced-domain premise, and a finite Taylor remainder calculation.
No hidden runtime behavior is needed for that conditional statement.

The following are deliberately not discharged:

1. `.1`: binary64 storage of `pi`, `pi/2`, DH constants, and `q+offset`;
2. `.3`: actual Julia/libm `sin/cos` outputs and argument-rounding error;
3. `.4` D1: `T_prev -> A_i -> T_i`, with parent `z_i` extracted before `A_i`;
4. `.4` D2/D3: finite FK/COM/Jacobian/mass/potential propagation and ordered
   accumulation;
5. per-box coverage and the repeated `fk_frames` calls used separately by
   `mass_matrix` and `potential`.

In particular, a Taylor enclosure for `Real.sin`/`Real.cos` cannot be reused as
a libm receipt. To compose into D1, the next required object is a per-call
`Float64` argument/libm inclusion with pinned runtime and finite flags; only
then can the generic finite-DAG interval theorem consume it.

## Targeted evidence and boundary

A focused read-only check of the canonical CSV found 12 rows, the expected
theta/alpha phase vectors, ordered reduced/sin/cos endpoints, and reduced
endpoints within `[-1,1]`. This is a shape/arithmetic consistency check for the
declared exact-real payload, not an independent libm or source-execution proof.

No Julia, Lean/Lake, SOS, trajectory, registry, or broad regression run was
performed. The parent remains `OPEN`; `formal_certificate_allowed=false` and
`registry_promoted=false` remain unchanged.
