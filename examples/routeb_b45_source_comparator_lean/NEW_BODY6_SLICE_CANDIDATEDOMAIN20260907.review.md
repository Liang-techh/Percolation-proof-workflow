# Candidate-domain origin witness and BODY6 obstruction

Status: **OPEN_UNCOMPILED**. This is a bounded proof attempt and read-only
source/domain audit. No Lean/Lake execution, numerical simulation, wide
regression, state/registry mutation, or admission was performed.

## Result and exact scope

The new leaf gives exact-real typed origin-witness proof terms for the
explicit O1 configuration cell and the original delivery region transcribed
below. The active energy domain has only a **conditional** origin witness:
`V(0,0) <= 1` remains an external premise. These domains are not identified
with one another, or automatically with an arbitrary current candidate `D`.
In particular, neither inclusion between `p_B<=28/5` and `V<=1` is
established here; each would require a separate comparison theorem.

For the unregularized BODY6 3-by-3 remainder, the minimal conditional
refutation is

```text
CenterOffsetTarget
0 in D
R(0) = sourceCoefficient(0, 3/20, 1/60)
-------------------------------------------------------
not exists mu > 0, UniformMargin D R mu
```

`physical_weights_attempt` supplies the literal physical-weight identity
from `routeBMass 5` and `routeBInertiaScalar 5`. The remaining geometric
`CenterOffsetTarget` is still supplied explicitly. All proof terms,
including these arithmetic terms and the imported null-vector proof, are
uncompiled; none is reported as kernel-verified.

## Three different domain identities

| Domain | Evidence and exact-real predicate | Origin result in this leaf |
| --- | --- | --- |
| O1 consumer cell | `O1_PER_BODY_COMPARATOR_RECEIPT.json` records center `(0,0,0,0,0,0)`, radius `1/1000`; `O1_BODY_6_CANONICAL_EXPORT_CONTRACT.json` explicitly says `forall k, abs(q k) <= 1/1000` | `zero_mem_o1_cell_attempt` proves the literal predicate by exact rational arithmetic. This is a local source-comparator consumer cell. |
| Original delivery region | External `robot_final/routeB_certificate_manifest.toml:24-26` records the joint bounds and `p_B <= 5.6 = 28/5` | `zero_delivery_state_attempt` uses `q=0,v=0`; `zero_mem_delivery_projection_attempt` supplies `v=0` in the configuration projection. These are proofs for the transcribed predicate. |
| Active energy region | External `robot_formal_v1/README.md:92-95` identifies the active route as `V<=1`, then transfer to `p_B<=45`; `P5_COMPACT_SOURCE_TO_FLOW_INTERFACE.md:89-94` defines the lifted set using `V<=1` and circle equations | `zero_mem_active_projection_attempt V hV` requires the external `hV : V 0 0 <= 1`. No concrete current `V` is instantiated or normalized here. |

The delivery joint bounds are open intervals with radii
`(pi, pi, 5*pi/6, pi, pi, 2*pi)`. Its state predicate is

```text
jointBounds(q) and
(3/2)*(q4^2+q5^2) + (4/5)*(v4^2+v5^2) <= 28/5.
```

Lean indices are zero-based: joints 4,5 use indices 3,4. The full six-entry
configuration and velocity vectors are retained. The initial-ball predicate
`sum(q_i^2)+sum(v_i^2)<=9/400` and the horizon/disturbance predicate
`0<=t<=1, slope^2<=3, w=slope*t` also have the exact origin witness in
`zero_initial_and_disturbance_attempt`. This is not a claim that their
conjunction exhausts an external candidate's restrictions.

The active lifted witness is `(q,v,cosine,sine)=(0,0,1,0)`; the all-zero
lifted vector violates the circle equations. `origin_lift_has_correct_angles_attempt`
also checks the actual angle values at zero. Using all six circle pairs in
the leaf is a conservative transcription; a concrete dephased export must
still supply its active-coordinate map. The disturbance slope and the
cosine coordinates are separate objects despite the overloaded letter `c`
in external documentation.

The earlier terminal artifact
`artifacts/routeb_agent_terminal_one_lemma_20260906T075912Z/RouteBTerminalOneLemma.lean`
defines a strict `blockP < 28/5` domain. Its existence does not identify it
with the manifest's nonstrict region or the active `V<=1` domain. Similarly,
the source-binding checker's test fixture is not a domain authority.

## BODY6 source/null-vector bridge

The imported `NEW_BODY6_SLICE_ENTRYMARGIN20260907` supplies the exact-source
attempt at `q=0`, with direction `u=(0,-19,40)`, `sum u_i^2=1961`, and
`R_source(0) u=0`. A positive margin would require `1961*mu <= 0`, a
contradiction. This leaf reuses that algebra; it performs no numerical
eigenvalue or sampled-domain test.

`Body6RAtZeroBinding R` is just the equality at zero. The stronger existing
`ExactPhysicalFamily D R` implies it when zero belongs to `D`, via
`family_implies_zero_binding_attempt`; an all-configuration source equality
or a global domain cover is unnecessary for this one-point refutation.

`minimal_candidate_obstruction_attempt` packages the minimal consumer.
`delivery_bound_candidate_obstruction_attempt` and
`active_bound_candidate_obstruction_attempt` make domain transfer explicit
with a projection-subset premise. A supplied `0 in D` is even weaker and
sufficient. `o1_body6_strict_obstruction_attempt` directly specializes the
canonical source family to the explicit O1 cell, conditional on the source
geometry and weight premises.

The BODY6 object uses body index 5, front joint indices `(0,1,2)` and tail
indices `(3,4)`, with physical `m=3/20`, `kappa=1/60`, offset `7/200`.
It is **not** the full six-body mass matrix or the full O1 `(B,D)`
partition, where `B=(3,4)` and `D=(0,1,2,5)` in zero-based indexing.
No full-system Schur complement is equated to this body-only remainder.

## Full M/C/G source binding is a separate interface

The authoritative index points to `routeB_dense_Mq`. Its `dhport_lib.jl`
defines body contributions and a regularized sum at lines 46-60, potential
at 63-70, and `arm_MCG` at 73-99. The return is `(Mq, Cdq, Gq)`:
`Cdq` is the Coriolis **force vector**, not a matrix called `C`.

The new exact-real definitions preserve this structure:

```text
sourceAggregateM(q) = sum_body sourceBodyMass(q,body) + epsMass*I
epsMass = 1/1000000
sourcePotential(q) = sum_body m_body*(981/100)*COM_body(q)[2]
fdStep = 1/100000
sourceCForce = Christoffel central differences of sourceAggregateM,
               contracted against v_j*v_k
sourceG = central differences of sourcePotential.
```

These are transcriptions linked to the same local exact-real DH source
terms. `ExactRealMCGSourceBinding` exposes extensional obligations for
external `M,Cforce,G,U`; it does not assert that those obligations have been
discharged. `BoundBody6Request` retains that binding and separately requires
the BODY6 `R(0)` equality. Its contradiction theorem uses only the BODY6
and origin fields: M/C/G identities cannot manufacture a body-only
remainder identity.

The full mass regularizer `epsMass` must not be confused with requested
margin `mu` or body inertia `kappa`. A singular unregularized BODY6 remainder
does not refute positivity of the regularized six-body mass, a full-system
Schur margin, the controller, or the continuous trajectory certificate.
No nonstrict PSD conclusion is obtained merely by ruling out positive `mu`.

## Minimal remaining fields and proof obligations

1. **Candidate domain identity / membership:** a typed current `D`, its
   state/configuration projection and any extra restrictions, plus `0 in D`.
   Domain equality is sufficient but not necessary. For the active branch,
   bind the actual `V` and prove `V(0,0)<=1`; this remains external, not a
   fact inferred from the name “physical energy” or from `p_B(0)=0`.
2. **Requested remainder identity:** identify `R` as the unregularized
   BODY6 remainder with the stated index map, and prove its equality at
   zero. If the target is the aggregate regularized Schur complement, this
   equality must not be supplied by relabeling; the present obstruction
   does not apply without a separate, valid mathematical argument.
3. **Local source geometry:** supply `CenterOffsetTarget` and compile its
   dependency chain. The literal weights have a proof attempt here; they
   are not missing numerical data. The O1 global DH-to-Fourier `h_body_6`
   is a separate obligation and is not discharged by a zero-point result.
4. **Full exact-real M/C/G, if the whole model is claimed:** instantiate
   the four extensional fields, pin the source/parameters/index order,
   preserve the finite-difference force-vector semantics, and cover shifted
   inputs `q +/- h*e_k`. A certificate restricted to `q in D` alone does
   not ensure the shifts stay within its source-enclosure domain.
5. **Deployed/flow claims, if requested later:** actual Float64 evaluation
   needs the roundoff/transcendental/solve enclosure required by
   `P5_COMPACT_EXACT_REAL_MODEL_BOUNDARY.md`; exact-real transcription or
   matching hashes do not establish it. Flow/coverage and registry admission
   remain separate gates. None is needed merely to state the conditional
   BODY6 algebraic contradiction.

Items 1-3 are the bounded obstruction interface. Items 4-5 are deliberately
not additional prerequisites for the body-only contradiction, but prevent
it from being promoted to a claim about full deployed M/C/G dynamics.

## Provenance and validation

External root inspected read-only:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
SHA-256 values from this inspection:

| Path relative to external root | SHA-256 |
| --- | --- |
| `robot_formal_v1/manifest.json` | `951f263780cc0fb9e35b54d119eed91289de45eb02da75b3bcf3a70aca600ae3` |
| `robot_formal_v1/README.md` | `41e82581c476a3ec94faf6e374c2605c215df36dc3b4b430cde029fb24a572c0` |
| `robot_final/routeB_certificate_manifest.toml` | `d9ae90af1860364eae950649b3ffbf1810d78583383781ec9fa6949fdd24f495` |
| `routeB_dense_Mq/dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |
| `routeB_dense_Mq/P5_COMPACT_SOURCE_TO_FLOW_INTERFACE.md` | `832a0b575b9b58dfee0a698946fe63ae01b6d1e14f38154f538578b8397c7d70` |
| `routeB_dense_Mq/P5_COMPACT_EXACT_REAL_MODEL_BOUNDARY.md` | `33af68226c691dae568924fcd4501c01cb6c35571721aa2cf1cb85a9858b8313` |

The index is generated at `2026-09-05T16:12:18Z`; its recorded gate remains
`UNKNOWN_NEEDS_COVERAGE`, `formal_certificate_allowed=false`,
`coverage_complete=false`, `remainder_absorbed=false`. The delivery
manifest's `coverage_completed=true` is qualified as
`trajectory_monte_carlo_only`, with `global_box_coverage=false`; it is not
proof-domain coverage. No gate was changed.

Static checks only: inspected definitions, source constants, finite-difference
index order, domain witnesses, theorem premise direction and new-file content.
No `sorry`, `admit`, or `axiom` tokens occur in the new Lean leaf. This
textual check says nothing about elaboration or imported dependencies.
No Lean/Lake or broad regression was run.

Lean leaf: `NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907.lean`, 208 lines.
SHA-256: `a29b912819ee043209e49f56448244cfc4ab1502713fbb7cceaef36ae3e51086`.

Final status: **OPEN_UNCOMPILED**. Exact witness proof attempts for the two
literal domains are present; a current active-domain membership theorem
and an unconditional full-model infeasibility claim are not established.
