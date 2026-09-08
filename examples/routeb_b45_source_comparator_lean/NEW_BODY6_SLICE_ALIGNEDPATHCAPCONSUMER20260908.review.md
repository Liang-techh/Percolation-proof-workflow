# Aligned initial-growth/path-cap consumer

Status: **OPEN_UNCOMPILED**, pending integration. This is one bounded
74-line composition leaf. It imports INITIALPATHCAPS and ACTUALSTORAGEALIGN;
it does not reprove their identities, domain lemmas or growth statements.
No Lean/Lake, broad regression, registry or state modification occurred.

## Concrete objects

`Model` fixes H, the actual and encoded mass evaluators Ma/Me, U, Uzero and
p. The mechanical state is explicitly `(q,v)`, each with six coordinates.
`source` is ACTUALSTORAGEALIGN's `actualBase`, the stated specialization
f=1,h=0 with fixed parameters and identical q/v coordinates. `target` is
the encoded kinetic+W+B expression, with B=4079979/400000.

This specialization is not inferred to be the active Route-B candidate.
Time-dependent synthesis coefficients or additional state/lift variables
would need their own embedding/identity; the source here is time-independent
as a state function, while its value along the path may change with time.

## Every consumer premise

| Field | Required mathematical statement |
| --- | --- |
| `alignment` | On Q, Ma=Me and the actual configuration remainder equals encoded W, with the fixed model's normalization and quadratic correction |
| `initial` | The same source storage at t=0 is <=a for every state in the explicitly supplied X0 |
| `startsInInitial` | The same path satisfies path(0) in X0 |
| `growth` | Source(path(t)) <= source(path(0))+b(t) on [0,1]; this is an integrated theorem input, not a derivative label |
| `uniformGrowth` | b(t)<=beta throughout [0,1] |
| `projection` | Every x in the full mechanical domain D(t) has q=x.1 in Q |
| `wholePath` | path(t) belongs to D(t) throughout [0,1], not only initially |
| `shiftedBudget` | a+beta+B<=bar, using the target's exact shift B |

`consume_aligned_path_cap_attempt` first obtains the shifted value identity
from ACTUALSTORAGEALIGN, then invokes INITIALPATHCAPS. It concludes only
`FullPathCap (target model) path bar`. The intermediate unshifted cap is
a+beta, and B is charged exactly once. Neither cap nor the budget is inferred
from a V0 scalar match. An already shifted source bound would need the
corresponding existing already-shifted consumer, without adding B again.

No claim of logical necessity for every possible representation is made:
the record is a minimal direct composition of these two specific interfaces.
For example, a separately proved direct full cap could replace the initial
and integrated-growth route, but this leaf adds no second consumer.

## Exact counterexample

`normalizedOriginModel` sets U to the encoded potential and Uzero=U(0),
using the same arbitrary M in Ma and Me. Along `originPath(t)=(0,0)`, the
actual specialized source is exactly zero for arbitrary H and p. Therefore
it has a full-path source cap of zero, not merely an initial cap.

The target equals B=4079979/400000>1 along that same path. Thus
`source_full_cap_does_not_pay_shift_attempt` proves the source full cap and
rejects a target full cap of one. This makes the missing shift budget
explicit even after a source full cap is available. It is a constant-state
algebraic example, not an assertion that this path solves the DH equations.
It does not contradict the consumer because its required budget 0+B<=1
is false.

## What is not concluded

No current candidate Model or ConsumerPremises instance is supplied.
The result does not prove initial gap/coefficient bounds, integrated growth,
path-domain inclusion, v=q', ODE existence, continuation, circle invariance,
physical DH/Fourier/Float64 binding, a BODY6/full-system Schur identity or
registry admission. Assuming whole-path membership in a desired sublevel
is not a replacement for the missing first-exit proof.

## Dependency and validation boundary

The new leaf and all three involved sidecars are OPEN_UNCOMPILED. Historical
success receipts for the underlying ActualStorage/ActualShift files do not
cover this composition. Source signatures and hashes were inspected; no
compiler, dependency rebuild or wide regression was run.

| File under `examples/routeb_b45_source_comparator_lean` | SHA-256 |
| --- | --- |
| `NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean` | `f698d8c56c83005df0e0a907452ae7a6f083eb3736e6df60db4d0190084367dd` |
| `NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean` | `5cad04f2e8b0af13c8d8a099455812fe1f6d17a66a0d567be5b85963252d224f` |
| `NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean` | `f8da2e44f9afc4c80fc14e81a1c59626d5af98071300a009aecd33463d3bef56` |
| `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean` | `c3d0432fb2b53815bb9e23271ecadfa871e5526a96b9bf7b533efe392d2aa6ac` |

The new source contains no proof-hole declarations. Independent Lean
elaboration and axiom/dependency receipts, followed by actual premise
instantiation, remain pending. Final status: **OPEN_UNCOMPILED**.
