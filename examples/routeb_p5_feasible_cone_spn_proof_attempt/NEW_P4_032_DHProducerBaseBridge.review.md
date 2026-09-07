# Compact DH producer-to-base bridge

**OPEN_UNCOMPILED.** A new proof attempt and review only; no Lean/Lake, Julia, solver, regression, registry or source-file mutation. This round chooses the compact descriptor's **DH branch prospectively**; it does not claim line 9 recorded that branch or that the compact nominal field equals the complete physical DH dynamics.

The selected chain now has explicit state variables, the two DH residual polynomials, the producer metric, a conditional descriptor-to-port identity, and one remaining base-dominance inequality. No repeated field inventory is needed.

## Exact formula chain

Use q=(q2,q3,q4,q5), v=(dq4,dq5), a=(a4,a5), the four-component distal acceleration correction, and the two-component force port at ONE state. The compact DH branch gives

`l4 = -3q4/4 - 4dq4/5 + w/5 + q5/100 - (350003/3000000)a4`,

`l5 = -29q5/50 - 13dq5/20 + w/10 + q4/200 - (200739/4000000)a5`.

These are the force-scale form of the script's `IVAL*fB-M0BB_CONST*aB`; the cross coefficients are 1/100 and 1/200 after multiplication by I4=1/5 and I5=1/10. No acceleration-to-force norm substitution is made.

The same acceleration vector defines

`A_up = (1402217/12000000)a4² + (200739/4000000)a5²`.

The first metric coefficient differs from nominal M0_BB,44=350003/3000000. The metric is not silently replaced by the nominal block.

`source key D base` fixes those lBase/acceleration functions and the state port. `source_metric_eq` identifies its consumer metric definitionally with the producer formula. The storage-dependent `base` remains an explicit function rather than a borrowed descriptor polynomial.

## Conditional port connection

`ProducerChain` requires, on the SAME D, a left inverse and the actual descriptor equations

`MDDinv*MDD=I`, `MDD*delta_aD+DeltaMDB*aB=0`, `rB-MBD*delta_aD=0`.

The new bridge reuses `NEW_P4_032_BlockDefects.zero_defect_port_identity` to derive

`rB = -MBD*MDDinv*DeltaMDB*aB`.

Given the validated operator bound for that expression, `rowEvidenceFromProducer` constructs the previous packet's `RowSourceEvidence`. The minus sign is preserved; norm equivalence alone would not justify reversing it in the residual sum.

The left inverse, matrix/source identities, zero-defect equations and operator bound remain supplied premises. The old `full_equations_to_port` has additional distal/local defect terms in the general case. They cannot be set to zero merely because the compact source defines a reduced descriptor relation. No physical defect closure or interval run is supplied by this bridge.

## Domain restriction exposed by the producer

The producer's `tighten_ball` sums lower squared bounds over ALL FOUR coordinates q2,q3,q4,q5 (lines 244–254), and its main loop passes radius_sq=eta/1.5 (line 402). At the intended exact eta=28/5 its modeled angle domain is

`q2²+q3²+q4²+q5²≤56/15`, with `|q3|≤5π/6`.

The script's floating-point endpoints and ball arithmetic still need exact/outward reification. `ProducerChain.geometry` explicitly requires D to lie within this intended producer geometry; it does not derive interval coverage from the formula.

This is stronger than the block condition `p45=(3/2)(q4²+q5²)+(4/5)(dq4²+dq5²)≤28/5`. At q2=2 and all other displayed angles/velocities zero, p45=0 while the four-angle sum is 4>56/15. `block_domain_not_producer_domain` encodes this exact polynomial counterexample. It refutes an automatic domain implication, not physical flowpipe inclusion established by some other proof. Any enlargement beyond the producer geometry needs an independent certificate.

## The remaining typed base inequality

`BaseDominance D base charge target` asks for exactly

`target>0` and `target+2(l4²+l5²)+charge*A_up≤base` on D.

`packetFromProducer` combines this with the conditional port chain to construct the existing `ConsumerPacket`. The previous P4 normalization adapter can then be used with its own explicit residual/nominal/gain-scale equalities. Neither `Dbase` nor an arbitrary positive source coefficient is substituted for this base lower bound.

The new exact discriminating slice sets q=v=w=0 and a=(z,0). Its producer metric and base residual are

`l4²+l5²=(350003/3000000)²*z²`,

`A_up=(1402217/12000000)*z²`.

Thus every such slice point that actually belongs to D requires

`base(z) ≥ target + [2*(350003/3000000)² + charge*(1402217/12000000)]*z²`.

`required_base_on_ray` is a directly consumable necessary condition. The
`block_domain_not_producer_domain` theorem shows that the block condition and
the producer's angle geometry are not interchangeable; membership in the full
descriptor/physical D is deliberately a separate premise. At z=1, charge≥0
and base≤0 contradict every positive target (`zero_base_ray_obstruction`).
This uses the transcribed source residual coefficients rather than an
arbitrary residual magnitude.

The complete base bound is not available: no same-instance storage inequality currently supplies this dominance. The port operator/source validation also remains open. What has advanced is the exact algebra connecting those two obligations; neither is hidden inside a status flag or inferred from coefficient slack.

## Directed interface review for WIP

- `ConsumerPacket` is an existing declaration in `NEW_P4_032_SameSourceConsumerPacket.lean:120`, with exactly `row_source : RowSourceEvidence row src` and `allocation : Allocation row src target`. The import and constructor fields used by `packetFromProducer` were checked against that live file; this is not an invented type name or a compilation claim.
- `source` maps the same D/base and state acceleration/port into `SourceFields`; only lBase is fixed to the transcribed DH branch. It does not silently populate a storage lower bound. Its metric equality is definitional.
- `ProducerChain.operator_bound` is an upper bound on the squared producer port. The descriptor identity rewrites the state port into that expression, preserving the direction required by `RowSourceEvidence`. Branch/eta/geometry are declared gates; their presence does not authenticate matrices or reify the CSV.
- `required_base_on_ray` assumes the ray point is in D. `zero_base_ray_obstruction` additionally assumes base≤0 there and charge≥0. Geometry alone establishes neither full-D membership nor those base values. The result blocks that conditional allocation, not the actual ODE or all certificates.
- `block_domain_not_producer_domain` disproves only the implication from the block-p predicate to producer geometry. It supplies no trajectory or missing coverage automatically.

## Live source anchors

Base directory: `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.

| Source | Relevant definitions | SHA-256 |
|---|---|---|
| `routeB_compact_direct_descriptor_structure.jl` | branch 24–28; M0_BB 38; fB/lBase/port 77–91 | `2c2f623f966425952cbbbd3c04bae84858147fe7fdd386f5bc5f4ff35e2fb98c` |
| `routeB_factorized_descriptor_model.jl` | IVAL 15; Kp/GwI 192–195 | `c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427` |
| `routeB_compact_composed_interval_probe.py` | B_up 115–120; ball contraction 244–254; domain 388–402; negative R 274–279 | `ab6a4e34ecb391247eef796496f57b28407587b366c360f4e0ad441fedd04ba6` |

The formulas were manually transcribed and reviewed against these live files; no source importer or Lean compilation validates that transcription yet. Existing source-key digests remain provenance declarations, and no complete candidate packet or P4 margin theorem is admitted.
