# Initial source cap, full-path cap and shift budget

Status: **OPEN_UNCOMPILED**. This 92-line companion imports the pending
PATHDOMAINPROJECTION leaf. No Lean/Lake, wide regression, registry/state
mutation or source audit execution was performed.

## What the existing evidence actually gives

| Evidence | Valid scope | What it does not supply |
| --- | --- | --- |
| Compiled `ActualStorage.W0_initial_upper` | W0<=231/20000 under the full12 ball and gap>=-3/10000 hypotheses | Gap/source instantiation or an upper bound at future path points |
| Compiled `storageV_initial_upper` / `synthesisV_initial_upper` | Initial bound `9*beta/400+3f/10000+3h`, or the coefficient-sum specialization, under stated hypotheses | A selected candidate, integrated growth estimate, path membership or full-path cap |
| Compiled nonnegativity / `synthesisV_terminal` | Conditional nonnegativity on its domain, and synthesis value zero at t=1 | An upper tube on the interior of [0,1] |
| Compiled `ActualShift.actual_p45_bound` | Pointwise `p45<=(1600000/9401)*(E+B)` under same-point mass and energy-identity premises | An initial upper bound or time-uniform upper bound on E+B |
| Current barrier CSV | Initial number `492033745203/25600000000000`, a recorded scalar tube/margin and `energy_first_exit_closed=True` | A typed same-storage/actual-path theorem for that tube |

The old leaves have compilation receipts as checked in COMPILEDLEDGERBINDING;
their premises remain explicit. The CSV is not itself a compiled Lean
ledger theorem. Its current flags remain `descriptor_flowpipe_closed=False`,
`fd_remainder_semantics_closed=False`, `formal_certificate_allowed=False`.
Thus the evidence is not “only initial facts” in every respect, but its
compiled upper-cap results relevant here are initial or pointwise; no
actual source full-path upper-cap instantiation is supplied.

## Minimal separated contract

The new definitions distinguish:

```text
InitialSetCap X0 F a:  forall x in X0, F(0,x)<=a
InitialPathCap F path a: F(0,path(0))<=a
FullPathCap F path cap: forall t in [0,1], F(t,path(t))<=cap
ShiftBudget cap B bar: cap+B<=bar.
```

An initial-set theorem becomes an initial-path bound only after supplying
`path(0) in X0`. The same initial set, storage parameters, state map and
normalization must be used. A point named zero is not automatically the
actual initial condition, and V0 is an initial-set upper scalar, not Uzero.

The missing bridge is exposed as `IntegratedGrowth`:

```text
F(t,path(t)) <= F(0,path(0)) + b(t),  t in [0,1].
```

Together with b(t)<=beta and the initial-path cap a, it yields the full-path
cap a+beta. This is a consumer of an already established integrated bound,
not a theorem integrating a derivative or proving regularity/ODE semantics.
For the current scalar ledger, the intended b(t) would have to be bound to
its same-source energy/growth expression (for example the stated cubic
supply term plus linear defect); the mere values gamma/defect do not fill
the `IntegratedGrowth` field.

`initial_growth_shifted_barrier_attempt` composes this bridge with the
existing DomainProjection, WholePathMembership and ShiftIdentityOnQ inputs,
then requires `(a+beta)+B<=bar`. No field is inferred from the desired
conclusion. If D(t) is an energy sublevel used in a first-exit argument,
whole-path membership cannot simply be assumed as a replacement for the
missing stopping/continuation proof.

## Exact logical obstructions

First, the smooth time-dependent storage `F(t,x)=8*t*(1-t)` has initial
upper value zero on every state, is nonnegative on [0,1], and has terminal
value zero. Along the constant Unit-valued path it equals 2 at t=1/2, so
there is no full-path cap 1. This shows that initial upper information,
nonnegativity and terminal zero by themselves do not imply an upper tube.
It is an abstract logical obstruction, not a counterexample to a fully
instantiated ActualStorage/ODE theorem or a proposed DH trajectory.

Second, the ActualShift constant is B=4079979/400000>1. For every cap>=0,
`cap+B<=1` is false. If a source path starts at exact energy zero, any full
cap on a time interval containing zero must be nonnegative, so it cannot
satisfy this shifted budget at bar=1. Both statements have exact proof
attempts; the second derives cap>=0 from the actual initial point of the
full cap instead of assuming it arbitrarily.

This is a failure of that normalization/threshold combination, not a
controller-failure theorem. An already-shifted cap on F+B is handled by
PATHDOMAINPROJECTION's `already_shifted_cap_transfer_attempt` without
adding B again. A correctly changed threshold or another verified storage
comparison is a different contract. The obstruction does not authorize
silently changing the active candidate.

## Remaining evidence and provenance

To consume an initial receipt, instantiate its candidate/source/coefficients,
initial-set hypotheses and path start. To obtain a full cap, provide the
same-path integrated growth theorem and its uniform budget (or a direct
full cap). To transfer to ActualShift, bind the same-domain energy identity,
whole path and projection, then check the correctly normalized shift budget.
These are separate obligations; a compiled initial implication or positive
CSV margin does not replace them.

The ledger was freshly read without execution:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block_energy_barrier_audit.csv`,
SHA-256 `b10f0118c3dd3e6708084421baf38624977e6b18cd77dbb93e11f5a7f183f875`.
The ActualStorage final receipt and ActualShift theorem signature were also
read directly. Existing successful receipts do not cover this companion
or its pending PATHDOMAINPROJECTION import.

Only static signature/premise checks and hashing were performed. The new
source has no proof-hole declarations and no Lean/axiom receipt.
SHA-256: `5cad04f2e8b0af13c8d8a099455812fe1f6d17a66a0d567be5b85963252d224f`.
Final status: **OPEN_UNCOMPILED**, integration pending.
