# Storage identity and initial-bound transfer

Status: **OPEN_UNCOMPILED**. This short independent leaf imports only
`Mathlib`. No Lean/Lake, wide regression or external audit script ran.
Only this new `.lean` and review were written; registry/state are unchanged.

## Four distinct objects

| Object | Meaning | Missing transfer |
| --- | --- | --- |
| `Vfull_DH` | Full kinetic + gravity + controller storage; its constant must be specified | Not identified with `V_eps` |
| `V_eps` | The targeted-gain, cross-term storage cited by the storage-to-block audit | Its bounds belong to this function and branch |
| `initial_storage_upper = 492033745203/25600000000000` | A scalar exported for the block-only initial set | The scalar alone is not a bound on `Vfull_DH` |
| `V_BAR = 1` | The active energy sublevel threshold | Neither a storage definition nor an initial-bound certificate |

The prior `NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907.review.md` records
the inspected source chain and hashes. In particular,
`routeB_compact_block_energy_barrier_audit.py:18,50,54,92` reads the scalar
from the storage-to-block CSV and labels its domain full physical energy;
`routeB_compact_energy_storage_to_block_audit.py:4,17,75,78,101` describes
targeted-gain `V_eps`, a cross term and block-only initial conditions.
This leaf formalizes the missing transfer, not a repaired source identity.

## Contracts and valid transfer

`SameStorageIdentity D V W` is the pointwise equality `V(x)=W(x)` only on
the explicitly supplied comparison domain `D`. It does not demand equality
on all states or treat names/hashes as mathematical identities.

`InitialBoundBinding X0 V upper` contains exactly
`forall x in X0, V(x)<=upper`. Both the storage and initial set occur in
its type. `initial_bound_transfer_attempt` transfers this bound to `W`
only using identity on a domain that contains `X0`.

`blockOnlyInitial` keeps state order `(q1..q6,v1..v6)`, fixes all coordinates
outside indices `3,4,9,10` to zero, and bounds the four retained squares by
`9/400`. It is not the full twelve-dimensional ball. `RouteBInitialTransfer`
keeps `Vfull_DH` and `V_eps` as separate inputs and requires their identity,
initial-domain inclusion and the actual exported-storage bound. No instance
for the current external candidate is supplied.

`SublevelBarrier T V path bar` expresses only the conclusion
`V(path(t))<=bar` on `[0,T]`. `barrier_transfer_attempt` transfers that
conclusion using storage identity on the path's domain. It does not prove
an ODE, a first-exit argument, or continuation. A source already proving a
strict barrier also needs a transfer of its strict inequality if strictness
is required; the counterexamples here already fail the weaker nonstrict one.

Equality is the minimal *identity* contract on the needed set, not a claim
that equality is logically necessary for every transfer. A proved one-sided
comparison `W<=V`, or a bounded difference with a corresponding budget
adjustment, can also suffice. `offset_barrier_iff_attempt` explicitly proves
that replacing `V` by `V+beta` preserves the barrier when the threshold is
also changed from `bar` to `bar+beta`.

## Two exact counterexamples

1. **Even the same valid initial bound is insufficient by itself.**
   On `X0={0}`, take `V(x)=0`, `W(x)=2x`, and path `x(t)=t` for `0<=t<=1`.
   Both initial bounds use `upper=0`. The source barrier `V<=1` holds, while
   `W(1)=2>1`. Their derivative bounds differ. Thus merely sharing a scalar
   or even proving the same initial scalar bound does not transfer a future
   barrier without a target growth argument or a comparison.
2. **The same derivative is insufficient by itself.**
   Take constant storages `V=0`, `W=2`. Their derivatives are both zero,
   including along the identity path, but the fixed threshold `1` accepts
   only the first. Here the target initial bound `W(0)<=0` is deliberately
   absent: derivative equality does not determine the additive constant.

These are smooth exact algebraic counterexamples, not numerical tests or
claims about a particular DH trajectory. They refute the two insufficient
inferences separately. They do **not** refute a valid theorem supplied with
both the target initial bound and a sufficient target derivative/integrated
budget. Equal derivatives plus an appropriate initial-value comparison can
also support transfer under the usual regularity and interval hypotheses.

## Remaining evidence

To consume the current exported initial bound, provide the exact storage
expression, normalization, gains/cross term and initial-set map, together
with an `InitialBoundBinding` for that same expression. If changing storage,
provide a domain-local identity/comparison and charge any nonzero difference
to the bound and threshold. `recordedInitialUpper < vBar` is checked by a
rational proof attempt but does not supply any of these functional bindings.

To transfer a full first-exit proof, also bind the pointwise/flow derivative
budget, path domain, initial set and threshold to that same storage. This
leaf supplies no proof of the current external equalities or of the source
initial bound. It also makes no claim about delivery `p_B<=28/5`, active
circle coverage, BODY6's unregularized remainder, or full M/C/G positivity.

Validation was limited to static definition/premise review and file hashing.
The new leaf contains 117 lines with no `sorry`, `admit` or `axiom` tokens;
that textual check is not Lean verification.
SHA-256: `486f16cebdcf6a9c9a370f2519fda1be9c8c577858bace0d9611274606ac4a40`.

Final status: **OPEN_UNCOMPILED**. The transfer contracts and exact
counterexample proof attempts are present; current candidate instantiation
and compilation remain open.
