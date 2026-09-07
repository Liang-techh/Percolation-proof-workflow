# P4：domain / storage / mass-object separation

Status: `OPEN_UNCOMPILED`; manually integrated review of the accompanying
proof-attempt sidecar. No Lean/Lake execution, CSV reification, registry
mutation, or broad regression was performed.

## Domain separation

`BlockRegion` is the state predicate `blockP ≤ 28/5`. `StorageOneRegion` is a
separate predicate `V≤1`, while `StorageTube` is the time-dependent predicate
`V≤t²` with `0≤t≤1`. The sidecar proves `StorageTube → StorageOneRegion` by
the elementary time bound. The reverse implications are not automatic:
`tube_in_block` and `storage_one_in_block` each require an explicit positive
localization multiplier and a same-domain comparison inequality.

The remote velocity coordinates are not bounded by a block-only `blockP`
predicate; `block_region_remote_unbounded` gives an exact witness. Therefore a
block projection cannot silently stand in for the full state domain.

The saved CSV point is only a conditional counterexample: after the caller
supplies an exact `storageAt V savedPoint` equality, the sidecar proves the
point lies in `BlockRegion` but not in `StorageOneRegion`. The equality is not
reconstructed from the CSV in Lean and does not establish a global domain
inclusion. The arbitrary `V=0` example separately shows that an unconstrained
storage function cannot imply block membership.

## Mass and Schur-object separation

`FullRegularizedMCG` is a full six-dimensional M/Cforce/G object with a global
regularizer. `Body6UnregularizedMass` and `Body6UnregularizedRemainder` are
single-body objects of different dimensions. `MassObjectBinding` makes the
six-body sum, the other-five contribution, `regularizer=1/1000000`, and
`fdStep=1/100000` explicit. It does not identify the full mass with the
single-body mass. `RemainderObjectBinding` separately requires the exact
body-6 Schur formula.

The exact `full_mass_diagonal_strict` theorem shows that a nonnegative
other-body diagonal plus the positive regularizer makes the full diagonal
strictly larger. The `schur_sum_counterexample` and
`schur_regularizer_counterexample` witnesses show that Schur elimination is
not additive over body contributions and that regularizing before elimination
is not the same as adding a regularizer after elimination. Thus the BODY6
unregularized null-direction obstruction cannot be transferred to the full
regularized six-body Schur complement by relabeling.

## Remaining obligations

1. Prove the actual source identity for the stored `V`, `blockP`, and the
   chosen Route-B state domain, including time dependence and coordinate map.
2. Bind any CSV decimal value to an authoritative exact-real or interval
   receipt; a conditional point equality is not a global checker result.
3. Supply a valid full-M-to-body/block Schur comparison if the downstream
   certificate needs one; the current sidecar explicitly does not provide it.
4. Keep `Float64`/solver/coverage evidence and Lean kernel verification as
   independent gates.

The sidecar is mathematically useful as an obstruction and type-separation
contract, but it does not prove the Route-B certificate false or true, does
not prove full-system PSD, and does not alter `formal_certificate_allowed` or
the verified registry.
