---
kind: review_result
review_id: review-GH-MATH-P4-METRIC-REFERENCE-IDENTITY-james-20260908T130629
task_id: GH-MATH-P4-METRIC-REFERENCE-IDENTITY
source_agent: James-local-takeover
created_at: 2026-09-08T13:06:29-06:00
inspected_commit: a21f4dcd88d8efeb075f9e23e861a347528f126e
status: pending
integration_status: pending
admission_label: pending
proof_status: EXACT_FACTOR_AVAILABLE_PARTITION_AND_REFERENCE_BINDINGS_OPEN
source_binding_proven: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: retain distinct metric identities and supply source/reference reification plus a typed linear transport; do not identify principal inverse with inverse principal block
---

# Metric identity audit: block456 is not block45 with a zero coordinate

## 1. Bounded result

The block456 nominal analytic matrix admits an explicit exact real linear
transport. The obstruction is NOT an unavailable dense square-root algorithm.
However the inspected block456, block45, Euclidean ledger and physical-lift
metrics are not all the same matrix or the same reference. In particular,
restricting the block456 inverse to coordinates 4/5 does not recover the inverse
of the block45 nominal mass block, even when the supplied vector has v6=0.

This turn reads source text, literal CSV records and hashes only. No Python
arithmetic checker, producer, source regeneration, Lean, regression, remote
forcing audit, first-slab audit or Monte Carlo was run. Formulas below are
exact algebraic analysis, not new kernel/source receipts. Only this immutable
review is added; all existing files, states and gates remain unchanged.

E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
External paths below are relative to E. Workflow HEAD labels inspection
context; byte hashes identify the external files, not their execution history.

## 2. Matrix/reference inventory

| Object | Coordinates/reference | Where used; identity status |
|---|---|---|
| H456 = M0_CC^-1 | C=(4,5,6); analytic mass, all cos=1/sin=0; +mu=1/1000000 once | `routeB_compact_block456_descriptor_structure_audit.jl:16-50` and `...residual_schur_interface_audit.jl:21-35`; true source formula for the nominal inverse, but no concrete Lean reification claimed |
| H45,nom = M0_BB^-1 | B=(4,5), D=(1,2,3,6); same analytic nominal reference | `routeB_compact_direct_descriptor_structure.jl:32-38,63-73` fixes diagonal M0BB_CONST; inverse is not the 4/5 principal block of H456 |
| H45(q)=M_BB(q)^-1 | B=(4,5), current q5, analytic mass | `routeB_compact_port_bi_partition_probe.jl` constructs the LEFT output scaling from current `massdiag`; not the fixed nominal inverse for every q |
| I2 output / B_up input | Euclidean port norm; B_up=diag(1402217/12000000,200739/4000000) on acceleration | `routeB_compact_combined_schur_interface.py:3-10`; `NEW_P4_032_SameSourceConsumerPacket.lean:33-49,80-82` has Euclidean totalSq and a separate acceleration metric. Neither is H456. |
| S_metric = S^T MDD_decimal S | lift coordinates (y1,y2,y3); physical remote D=(1,2,3,6) | `build_physical_acceleration_bridge.py:46-68`; a remote acceleration ENERGY pullback from decimal M0, not an inverse mass on force coordinates (4,5,6) |
| generic sq | Fin n Euclidean sum of squares | `NEW_P4_032_GenericSchurAllocation20260908.lean`; no built-in physical H, coordinate permutation or reference |

Equal dimension, the name "metric", SPD, or a shared controller name is not
equality of any two rows. The metric on the input acceleration and metric on
the output force are different objects with different roles/units.

## 3. Exact block456 factor and the concrete source slice

The current analytic CSV has seven CxC records, at lines 269-272,289,296-297:
three M44 terms, M46=(1/60)cos(q5), M55=40147/800000,
M64=(1/60)cos(q5), M66=1/60. The M44 terms are
`560441/4800000 + (147/1600000)sin(q5)^2 - (147/1600000)cos(q5)^2`.
There are no CxC 45/54/56/65 entries in this slice.
`load_mass` accumulates exact num/den terms without implicit symmetry or
regularization; the descriptor adds mu on the diagonal after substitution.

Writing

```text
a=350003/3000000, b=200739/4000000, f=50003/3000000, c=1/60,
M0_CC = [[a,0,c],[0,b,0],[c,0,f]], N=5000400003,
H456 = [[50003000000/N,0,-50000000000/N],
        [0,4000000/200739,0],
        [-50000000000/N,0,350003000000/N]].
```

The existing metric-transport review already provides these inverse/LDL
formulas and reports its earlier rational checks. This turn reads the actual
CSV rows and source convention and preserves the distinction between that
historical arithmetic evidence and a new source/kernel verification.

Let k=c/a=50000/350003, h=f-c^2/a=5000400003/350003000000. Then

```text
U=[[1,0,0],[0,1,0],[k,0,1]], D=diag(a,b,h),
M0_CC=U D U^T,
H456=U^-T D^-1 U^-1.
```

Since a,b,h>0, for every v=(v4,v5,v6),

```text
v^T H456 v = v4^2/a + v5^2/b + (v6-k*v4)^2/h,
T456(v)=(v4/sqrt(a), v5/sqrt(b), (v6-k*v4)/sqrt(h)),
sq(T456(v))=v^T H456 v.
```

This is a constructible real linear map. Its coefficients may use exact real
square roots; no floating approximation is required. If a downstream checker
must remain rational, keep the displayed positive rational weighted squares.
For a Cholesky factor M=C C^T the correct map is C^-1, not C^-T in general.
Apply the SAME T to baseline, port and total vector, preserving linearity.
This is not an orthogonal map of the unweighted Euclidean space and not the
default Pi/sup norm. No new Lean declaration was compiled in this turn.

## 4. New discriminating mismatch: inverse and restriction do not commute

The same analytic nominal source has M0_45=diag(a,b), hence
`H45,nom=diag(1/a,1/b)` and
`T45(v4,v5)=(v4/sqrt(a),v5/sqrt(b))`.
Let E45(v4,v5)=(v4,v5,0). By the exact square decomposition,

```text
sq(T456(E45(v))) = v4^2/a + v5^2/b + k^2*v4^2/h.
```

Because k is nonzero and h positive, this differs from v^T H45,nom v whenever
v4 is nonzero. Equivalently,

```text
(H456)44 - (H45,nom)44
 = f/(af-c^2) - 1/a = c^2/[a(af-c^2)] > 0.
```

This is a matrix identity obstruction, not a q=0 state-projection countermodel
and not an assertion about reachability. It cannot be repaired by padding a
block45 residual with a zero joint6 entry. A different embedding or an
inequality transport requires its own source/metric proof.

The corresponding inverse block of the full mass uses a Schur complement,
not the inverse of its principal mass block. Thus changing which joint belongs
to D changes the metric, even at the identical nominal reference.

## 5. Other noninterchangeable metrics in current sources

- Current q5 metric: the nonconstant M44(q5) above is not identically a.
  `diag(M44(q5),b)^-1` therefore differs from H45,nom in general. A pointwise
  T(q) is possible but must be kept distinct from constant T456. Using it for
  pointwise algebra needs only pointwise identity; differentiating a transformed
  storage would require additional derivative terms, not supplied here.
- B_up is an acceleration upper envelope, not an output inverse mass. Its
  first diagonal is 1402217/12000000, whereas a=1400012/12000000. Its matching
  second diagonal does not establish equality of matrices or their inverses.
- The actual Euclidean ledger has lower block proportional to I2. A bridge to
  a physical H target requires a proved transformed residual and budget, or an
  explicitly budgeted comparison; copying its rho to the H target is not exact.
- The raw decimal M0 CSV has nonzero M45 token `3.06161699786838e-18`, whereas
  the analytic M45 polynomial is exactly zero. `decimal_rat` in the physical
  lift builder retains this nonzero rational; it does not round it away.
  Therefore that literal decimal reference cannot be declared exactly equal
  to the analytic reference. This is an exact literal mismatch, not a claim
  that the tiny difference defeats a bound; enclosure/refinement could handle it.
- `S_metric` pulls back remote acceleration energy through a 4x3 complement S.
  Even an independently verified Gram factor for it would concern lift y,
  not block456 generalized-force v. A 3x3 shape match does not supply a state
  map or a mass-inverse identity.

## 6. Minimal source-to-consumer identity packet

Require all of the following together; none is implied by digest equality:

1. Exact source evaluator/CSV and additive row semantics; origin substitution,
   regularizer amount and exactly-once convention; decimal/analytic/runtime
   semantics explicitly selected.
2. Ordered B and D embeddings, reference configuration, force-coordinate order
   and units. A permutation P must transform H by P H P^T when v'=P v; it must
   also transform all vectors and operators consistently.
3. Entrywise source reification `M0_source=M0_literal`; inverse identity for
   the SAME reference; no totalized singular inverse shortcut.
4. A linear T with `forall v, sq(Tv)=v^T H v`, plus the actual residual,
   baseline and target identities in these coordinates.
5. A cap expressed in that H or transported by a proved comparison, with
   normalization and cell key unchanged. `rho2_m0_upper`, current-q mass
   weighted rho and Euclidean rho are not interchangeable labels.
6. A concrete typed consumer invocation and independent checking/admission
   under existing policy. This review supplies no invocation or gate change.

For the current generic n=3 Schur consumer, the literal factor above removes
the pure linear-algebra unknown. The remaining indispensable step is the
source/reference identity packet. Old block45 typed consumers cannot be made
block456-compatible by renaming H, dropping a coordinate, or using S_metric.

## 7. Fresh byte hashes

External paths are relative to E; workflow paths are explicitly marked.

| Artifact | SHA-256 |
|---|---|
| routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451 |
| routeB_dense_Mq/routeB_factorized_descriptor_model.jl | c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427 |
| routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl | 9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79 |
| routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3d68fff2e71e3c912d45463ce1166e4381a98cefb049478b989cc279520d4d98 |
| routeB_dense_Mq/routeB_compact_direct_descriptor_structure.jl | 2c2f623f966425952cbbbd3c04bae84858147fe7fdd386f5bc5f4ff35e2fb98c |
| routeB_dense_Mq/routeB_compact_combined_schur_interface.py | c6d2af78691325991d6b91c163cd01ac8cfc8ee8b455fc963920a9e3fdf3529c |
| routeB_dense_Mq/routeB_compact_port_bi_partition_probe.jl | b565f0c5d6ab7778ec08553cb302246c91c550f26b7d7cd5f70939a39985b85a |
| routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.jl | 62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129 |
| routeB_dense_Mq/routeB_Mq_M0.csv | 28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40 |
| robot_formal_v1/exact_checks/build_physical_acceleration_bridge.py | 5424fb59df6b88b07c3577b907abfef7300113ec781f4cb0ed2fad2283cc10f7 |
| robot_formal_v1/interval_bounds/physical_acceleration_bridge_v1.json | 01022d32673ad10e9b1b1da398da15ce624c3f077734c2343e1ec9813fc6bede |
| workflow: examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SameSourceConsumerPacket.lean | 8c49603aa1c2193a5440026474d8ddc4b90e3a308c7c32ac862ace7b8c1a160e |
| workflow: examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean | a76375770d563f86f7de80fdea970e8d0d0fadd1ed917c262b725c7a8ba47648 |
| workflow: agent_review_inbox/review-GH-MATH-P4-DIRECT-BLOCK456-METRIC-TRANSPORT-codex-20260908T090216.md | 3a6a5c87109cd54beeb71fffca70fde9876ebf05186a09160a86daa0cd520eea |

The last review was read for its existing exact factor, not treated as an
actual source or runtime receipt. Status stays pending; no registry/formal
admission is requested or performed.
