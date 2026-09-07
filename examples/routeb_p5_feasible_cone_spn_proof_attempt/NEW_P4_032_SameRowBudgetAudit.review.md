# Same-row positive-budget audit

Status: **OPEN_UNCOMPILED**. Read-only evidence inspection on 2026-09-07; only this new review and companion Lean sidecar were written. No Lean/Lake, Julia, solver, simulation or regression run; no registry/source edits.

**Current result: F-L is UNDETERMINED.** No inspected candidate row/manifest supplies the seven exact budget quantities with their same-domain interpretation. Neither F≤L nor F>L is established for the current physical candidate. Missing evidence is not evidence of mathematical infeasibility.

For one fully bound row, the exact test is

`F = offsetFloor + alphaFloor * frontFloor`,
`L = gainCap * (betaCap * qCap)`.

Some positive scalar target exists iff `F>L`. A prescribed target needs **both** `target>0` and `target≤F-L`. If `F≤L`, only this fixed budget allocation is obstructed; this does not prove that the physical system has no positive margin or that no stronger certificate exists.

## Frozen evidence scope

External base: `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.

| Artifact | Live SHA-256 |
|---|---|
| `routeB_certificate_manifest.toml` | `d9ae90af1860364eae950649b3ffbf1810d78583383781ec9fa6949fdd24f495` |
| `routeB_meanvalue_schur_local_probe.csv` | `5832a5f492df29a46a38859eefeef8bc143ed54c5158612779ca3a783393d734` |
| `routeB_compact_energy_fd_remainder_bridge.csv` | `032baf1d4a0bc12408dee95c5694ba660af643af2a9253c1140611201e9ac9f3` |
| `debug_13_bracket_candidate.csv` | `67537b0136a30271c762b4c2cd29ca9db6b1a70613cb18abb8f764822f969df7` |
| `routeB_residual_matrix_certificate.csv` | `c1cf61553720df83f974f13f1d5ab22676ecea2f2349e886a62aefa206274853` |

An exact-name/underscore-alias scan of these five records found zero occurrences of the seven budget fields. This bounded inspection does not assert that no other artifact anywhere could supply a mapping.

The manifest has `eta_star=5.6`, `alpha_target=alpha_selected=12`, the block p-region, regularizer `1e-6`, and centered C/G FD step `1e-5`; it has no sf or seven-slot budget contract. `routeB_pmi_certificate.jl:37,298` identifies the alpha role as terminal qpoly containment. Thus 12 is neither the front scale floor nor the prescribed scalar margin target.

The single meanvalue probe has `sf=2`, radius `0.001`, `cg_enclosure=meanvalue_fd`, `interval_solver=weighted_krawczyk`, `h_lo≈1.89274`, `schur_lower≈0.833399`, `robust_remainder_lower≈0.808843`, and **coverage_complete=false**. These are labels and decimal output, not a constructed `FrontFloors`/`ResidualCaps` packet. Its eta text ends in `...9986`; interpreted as an exact finite decimal it differs from 28/5. No rounding/reification bridge was supplied, so it was not silently identified with the manifest's eta.

The debug file has separate eta/sf rows (2.7/1, 2.7/2, 5.6/1, 5.6/2). Sampled `min_h` is not a uniform front credit. The residual-matrix file's `negative_micro`, eta=2.7, sf=1, identity row is marked `REJECTED_STRICT_NEGATIVE` and has negative h bounds, but no identity `h=F-L` is supplied. Neither that row nor the positive local probe determines this seven-slot budget.

## Minimal missing obligations

| Budget field | Required meaning on one domain D; currently absent as a bound slot |
|---|---|
| frontFloor | `0≤frontFloor≤mu(x)*frontEnergy(front(x))` for all x∈D; a remainder eigenvalue alone omits the front-vector factor |
| offsetFloor | `offsetFloor≤offset(x)` on D, in the scalar margin normalization |
| alphaFloor | `0≤alphaFloor≤alpha(x)` on D; no proof that sf or terminal alpha is this alpha |
| gainCap | `0≤gain(x)≤gainCap` on D |
| betaCap | `0≤beta(x)≤betaCap` on D; beta is distinct from alpha |
| qCap | `0≤q(x)≤qCap` on D, with q exactly the specified squared generalized-force residual |
| target | One exact prescribed scalar, its margin unit/normalization, and positivity/allocation proofs |

For deciding the sign alone the six non-target fields suffice; to certify the requested target all seven are needed. Decimal outputs require exact rational reification or outward enclosure proofs, not nearest-value substitution.

| Object group requested in the follow-up | Missing same-state identification |
|---|---|
| energy | `f.energy(embed y)=src.energy y`; p45, saved V and mechanical energy cannot be equated by name |
| residual | `f.residual(embed y)=norm2(forceResidual y)^2`; acceleration/force conversion is unproved here |
| remainder | Identify the actual matrix and mu; full regularized six-body M/C/G is not a BODY6-only Schur remainder |
| front | Identify the same front test vector used by the remainder quadratic |
| scale | Bind alpha and beta separately at the same state; no sf→both-scales shortcut |
| gain | Bind the exact multiplier of beta*q, with its normalization |
| offset | Bind the scalar offset used in F and the nominal expression |
| nominal | Bind the same nominal and the required lower direction; the existing composition also has an upper direction, so together they require equality to the body expression |
| margin | Bind the same scalar Schur/PMI margin and external normalized comparison |

Also needed: a single source/manifest/artifact/row identity, stage, domain and coverage map, eta/sf interpretation, and a checked dimensional conversion contract. The dimensions of alpha*frontFloor, offsetFloor, gainCap*betaCap*qCap and target must agree after normalization; individual factors need not share units. No actual dimensional inconsistency is proved merely from missing units.

In particular, the energy FD bridge's `dq_cap_assumed=8/3` is a velocity cap, not qCap. Its positive `unit_supply_margin` and positive raw remaining margin explicitly come with `homogeneous_remainder_absorbed=False` and `formal_certificate_allowed=False`. They cannot fill this scalar Schur budget without a new same-object, same-domain absorption proof.

## Exact counterexamples and sidecar boundary

Synthetic rational rows, unrelated to physical candidate measurements:

- A: offset=0, alpha=beta=gain=1, front=4, qCap=5, target=1. F-L=-1.
- B: offset=0, alpha=beta=gain=1, front=1, qCap=2, target=1. F-L=-1.
- Illegally taking A's front floor with B's other entries gives F-L=2 and appears to allocate target=1. A real row context must prevent this splice, even when eta happens to match.
- With offset=0, alpha=beta=gain=1, front=2 and target=1 fixed, the single missing qCap can be 1 (allocation succeeds) or 3 (F-L=-1). This proves underdetermination from even one missing field.

`NEW_P4_032_SameRowBudgetAudit.lean` models optional exact values and per-slot origins; missing values or a different origin block completion. It supplies the rational allocation equivalence and counterexamples, then requires typed same-domain floors/caps, all `SameDomainBinding` equalities, composition and nominal realization before its conditional source-view margin conclusion.

Context strings and hashes are declarations, not source authentication, semantic unit checks or an executed importer. No concrete `ObservedRow`, `CompleteRow`, `BoundRow` or source-binding proof is instantiated from the inspected CSV/TOML. Completing those bindings is the next narrow obligation; there is no basis to select a favorable numerical F-L now. All Lean declarations remain uncompiled candidates, with no PSD, global coverage, physical certificate or admission claim.
