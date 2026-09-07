# V0 exact parameter mapping and remaining candidate identity

Status: **OPEN_UNCOMPILED**. Only this new proof-attempt/review pair was
written. No Lean/Lake, Julia audit execution, wide regression, registry or
state mutation occurred. This leaf extends COMPILEDLEDGERBINDING with the
scalar's exact source formula and a structural identity condition; it does
not repeat the earlier generic counterexamples.

## Exact scalar provenance is closed

The producer is `routeB_compact_energy_storage_to_block_audit.py:17-24,49-51`.
It computes

```text
eps = 1/1000
Mmax = 163847401/96000000
Hblock = 24185409/40000000
r = 3/20
A = max(Hblock/2, Mmax/2) + eps*Mmax/2
V0 = A*r^2 = 492033745203/25600000000000.
```

Since `Hblock<Mmax`, the maximum selects `Mmax/2`, giving
`A=164011248401/192000000000`. The exact split is

```text
base initial budget  = 491542203/25600000000
cross initial budget = 491542203/25600000000000
V0 = base + cross.
```

A focused `Fraction` calculation checked these identities. The new
`v0_generator_identity_attempt` and `v0_base_plus_cross_budget_attempt`
encode them as uncompiled Lean proof terms. This establishes scalar
provenance, not the validity of the producer's storage upper envelope.

## Source / CSV / Lean mapping

External paths here are relative to
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

| Field | Exact source/CSV evidence | ActualStorage / ActualShift mapping | Status |
| --- | --- | --- | --- |
| `Mmax` | Nonlinear strictification source computes `maximum(Mrow_l1)`; its CSV `mass_row_sum_upper=163847401//96000000` matches the producer literal | Different from compiled M0<=I; no proof here of this bound for the same state-dependent M(q) | Number and generating expression found; typed operator-bound/source identity missing |
| `Hblock` | Producer literal and CSV `block_potential_hessian_upper=24185409/40000000` | Not a field of either compiled storage theorem | The inspected Hessian CSV exports lower bounds, not this upper-bound row; a same-domain upper-Hessian proof remains required |
| `m_pot` | Hessian CSV `full_configuration_hessian_lower=18289737/160000000`, with targeted gains | Used by the local positivity/diagonalization branch | It does not enter V0's formula; it is not a replacement for an upper bound |
| `eps` and cross | `routeB_compact_targeted_nonlinear_strictification_audit.jl:16,27,35` fixes eps=1/1000, `Wmass=sum q_i M_ij dq_j`, and includes `-EPS*dotWmass` in the energy derivative | `storageV` has f*W0, diagonal q² and slope² terms; ActualShift has kinetic+W+B; neither includes this odd velocity term with the same state variables | Concrete derivative-level cross expression found; same-storage identity not supplied |
| Gains | Strictification source uses `Kp_target=Kp+(0,6,2,0,0,0)` | ActualShift uses imported original Kp; ActualStorage has separate f,p,H and no automatic targeted-gain selection | Global branch mismatch; on block-only X0 the added potential `3*q2²+q3²` vanishes exactly, so gain mismatch alone does not obstruct an initial-only comparison |
| Initial set | Producer CSV says block-only q4,q5,v4,v5 ball of radius3/20, remote coordinates zero | ActualStorage initial theorem covers a full12 ball under additional gap/ramp premises; restricting to the block subset is possible | Coordinate inclusion is available mathematically, but does not supply a storage identity or envelope |
| Constant / normalization | Derivative expression fixes K+Ugrav+Uctrl_target+eps*Wmass only up to a constant; producer assumes a homogeneous quadratic initial envelope | ActualStorage uses U-Uzero-H quadratic correction; ActualShift's W subtracts potential(0), then its comparison adds B=4079979/400000 | Missing explicit value-level V_eps evaluator and additive constant for the bound being consumed |
| ActualStorage budget | Compiled initial theorem gives `(9/400)*beta+3f/10000+3h` | No f,p,h,beta selection is stored by the V0 producer | Numeric matching is possible but does not identify its storage |
| ActualShift budget | No initial upper-bound theorem in ActualShift; its block comparison is for E+B | No epsilon or beta field; fixed exact B must remain in bounds and thresholds | Cannot obtain the producer's V0 merely by matching Kp or the potential table |
| Barrier consumer | Barrier script loads producer CSV's initial upper value, with V_BAR=1 and a full-physical-energy label | No current identity to either imported storage expression | Same evaluator/normalization/domain binding still missing |

The exact RHS in the producer can be matched numerically to the
ActualStorage bound by taking f=1,h=0 and
`beta=161451248401/192000000000`:
`9*beta/400+3/10000=V0`, with beta>=1/2. This is only an algebraic observation,
encoded in `scalar_match_only_attempt`; these are not parameters extracted
from the producer or a selected candidate. Taking p=0 would merely inflate
the known W0 bound when its gap/ball premises hold. It would not turn W0 into
the cross-term V_eps or the active physical energy.

## Concrete structural identity condition

For fixed f,p,h,H,M(q),U(q),Uzero and disturbance slope, `ActualStorage.storageV`
is even in v. This follows directly from the compiled `W0_actual_energy`
identity and quadratic kinetic energy; the sidecar proves the corresponding
attempt. The encoded ActualShift kinetic+W+B expression is also even in v.

In contrast, `q'M(q)v` is odd in v. Therefore, at velocity-paired states
in the same comparison domain, an identity

```text
S(q,v) = E(q,v) + (1/1000)*q'M(q)v
```

between an even S and an even E requires `q'M(q)v=0` there. This is exactly
`same_candidate_requires_zero_cross_attempt`, a necessary condition for
the actual value identity, not a generic numerical counterexample. The
block-only initial ball is velocity-symmetric; no vanishing-cross proof
for that whole set was found or supplied. Nonzero configuration and velocity
in retained coordinates are permitted by that set.

This conclusion is limited to the same variables and fixed source inputs.
A velocity transformation such as completing the kinetic square would
change the state map and add a configuration-dependent correction, and
would require fresh identity, initial-set and path bindings. It cannot be
inserted as a mere f,p,h parameter choice. No blanket impossibility theorem
for all redesigned storages or coordinate maps is claimed.

## Minimal remaining contract

For using this V0, a global identity between all storage candidates is not
necessary. The new `InitialEnvelopeBinding X0 Vexport` asks only for

```text
forall (q,v) in X0, ||q||^2+||v||^2 <= r^2
forall (q,v) in X0, Vexport(q,v) <= A*(||q||^2+||v||^2).
```

`envelope_delivers_v0_attempt` then derives the exact recorded bound.
`CandidateInitialBinding` additionally requires pointwise equality of
Vledger and Vexport on that X0, and transfers the bound. No current
instance of these records is asserted.

The smallest missing evidence is thus:

1. A value-level Vexport with fixed constant, gains, cross term and source
   M/potential/state map, matching the producer's intended expression.
2. The initial envelope for that expression on the precise block-only X0.
   To derive it from the cited components, supply the same-source mass
   upper bound, the restricted potential upper bound plus normalization
   and zero-gradient conditions, and the cross-term upper estimate.
3. Equality on X0 to the ledger storage, or a proved one-sided comparison
   strong enough to transfer the upper bound. Numeric budget equality,
   a derivative identity, or the compiled W0 initial implication does not
   supply this field.

Alternatively, instantiate ActualStorage's own initial premises and prove
its upper formula fits V0, then bind ledger V to that storage on X0. That
is a separate valid route; it does not retroactively identify the producer's
V_eps. Later use of the barrier still needs a same-storage integrated/path
bound. No new path or derivative contract is added in this leaf.

## Provenance and validation

| Source | SHA-256 |
| --- | --- |
| `routeB_compact_energy_storage_to_block_audit.py` | `80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9` |
| `routeB_compact_energy_storage_to_block_audit.csv` | `8d37219ea1b6189ec84e2eec16aa4fe29e2ee4bd263b946a639fafb7692b2bf1` |
| `routeB_compact_targeted_nonlinear_strictification_audit.jl` | `41dd63be6fab08b3398913490cb90d5f3571cce2e3ea833c52e9d1b97674f5b1` |
| `routeB_compact_targeted_nonlinear_strictification_audit.csv` | `57cbc0988ff999d53f6ce6065ca0b361e2e0826c8594f134625363096452c309` |
| `routeB_compact_targeted_gain_hessian_box_audit.csv` | `9051a2453948e09f1c9c564e84325eaa15e5bd47f49f48b568465551fab1bb51` |

Only focused Fraction arithmetic, source/CSV reads, static theorem review
and file hashing were used. No source audit was executed. The 107-line new
Lean leaf remains **OPEN_UNCOMPILED**, including its imported uncompiled
sidecar. SHA-256:
`7b0b3ccd87f2d2ae860a780f21905964f5fc97927bfc6af5ed8543c708cd8668`.

Result: exact V0 generator and parameter provenance established at the
arithmetic/source-text level; a same-candidate storage identity and the
typed initial envelope are still not established.
