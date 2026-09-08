# ActualStorage / ActualShift exact alignment companion

Status: **OPEN_UNCOMPILED**. This independent companion imports ActualStorage
and ActualShift but has not been compiled. Only this new open sidecar and
review were written; no existing leaf, registry, source data or gate was
changed. No Lean/Lake or broad regression ran.

## Exact comparison being made

The companion explicitly specializes ActualStorage to f=1,h=0, with fixed
p,H,Uzero and the same q/v coordinates. This is a mathematical branch, not
a selected or inferred active-candidate parameter tuple. Its expression is

```text
S(q,v) = kinetic(Mactual(q),v) + R(q)
R(q) = U(q)-Uzero-kinetic(H,q)+(7/75)*q4^2+sum p_i*q_i^2.
```

The other expression is

```text
E(q,v) = RouteBShiftedStorage.kinetic(Mencoded(q),v)
         + RouteBPotentialSlice.W(q)
Eshift(q,v) = E(q,v)+B,  B=4079979/400000.
```

The two imported kinetic definitions are definitionally the same finite
quadratic form. `actual_base_decomposition_attempt` uses the existing
`W0_actual_energy` identity to expose R. No PSD or gap estimate is needed
for this algebraic decomposition.

## Source-domain alignment contract

For a specified configuration domain Q, `Alignment` contains only:

1. `sameMass`: Mactual(q)=Mencoded(q) for every q in Q.
2. `sameRemainder`: R(q)=the imported encoded W(q) for every q in Q.

These are sufficient source-readable conditions, not a claim that full
matrix equality is logically necessary in every imaginable representation;
equal kinetic quadratic forms would suffice for an energy-only comparison.
No current physical-source instance of either field is supplied.

The companion also gives a structured way to prove the second field:

```text
U(q)-Uzero = encodedPotential(q)-encodedPotential(0),
sum p_i*q_i^2+(7/75)*q4^2 = kinetic(H,q)+proportionalEnergy(q).
```

The first identity fixes the **normalized potential**, so an irrelevant
common additive offset may cancel only when it is handled consistently.
The second is an actual quadratic compensation identity, not a scalar
budget equality. In particular, choosing p from a number such as V0 is not
a proof of it; off-diagonal terms in H must also be accounted for.

Under these fields, `aligned_base_identity_attempt` proves S=E on Q.
`aligned_shifted_identity_attempt` then proves S+B=Eshift. It does not prove
S=Eshift. The constant B is the exact shift from ActualShift and cannot be
discarded by a same-storage label.

For other f,h or time-dependent synthesis coefficients, one must supply
the resulting full value identity, including f times kinetic/potential,
the slope-square contribution and time dependence. This specialization
does not cover those cases automatically. A new coordinate/velocity map
would also need to appear explicitly in the definitions and domain map.

## How path inclusion enters barrier transfer

`aligned_path_cap_transfer_attempt` requires, for every t in [0,1]:

- q(t) lies in Q, where the source/mass/remainder identities hold;
- the actual source expression S(q(t),v(t)) is bounded by cap;
- cap+B is at most the desired target bar.

It concludes Eshift(q(t),v(t))<=bar. Thus identity and the correct cap are
both necessary inputs to this particular transfer. If one starts with a
bound on S+B directly, the same equality transfers it without another B.
No shift is charged twice.

Path inclusion is a hypothesis, not inferred from the conclusion being
proved. For a full state domain D(t), the caller must supply a projection
implication from D(t) to Q and establish actual path membership in D(t).
Initial membership q(0) in Q does not establish this for later times.
The companion contains no ODE, kinematic condition v=q', circle invariance,
continuation or integrated-energy theorem. If an earlier bound uses those
hypotheses, the same path/state/source must be used when supplying it here.

## Exact counterexample from the actual definitions

Take q=v=0, the encoded potential U, and Uzero=U(0). For arbitrary p,H,M,
the specialized ActualStorage expression has value zero. The imported W
also has value zero by its exact definition
`potential(q)-potential(0)+proportionalEnergy(q)`.
Consequently Eshift(0,0)=B=4079979/400000>1.

`actual_origin_fixed_bar_counterexample_attempt` states the exact pair:
S(0,0)<=1 and not Eshift(0,0)<=1. This prevents transfer at the unchanged
threshold 1 when the shift was omitted. It uses the actual definitions,
not an approximate eigenvalue or a sampled DH trajectory. It does not
assert failure of a correctly shifted barrier or the real controller.

## Relationship to existing transfer interfaces

- STORAGE_IDENTITY_TRANSFER / STORAGEIDENTITY supplies generic equality
  transfer. Here `Alignment` states concrete sufficient fields that could
  supply equality of these two unshifted expressions on the projected
  domain. Equality to the shifted target requires adding B on the source.
- COMPILED_LEDGER_BINDING / COMPILEDLEDGERBINDING exposes the existing
  initial theorem, positivity and path/tube premises. This companion
  supplies no gap, mass positivity, initial upper bound or source tube.
  Its field equations would have to be composed with those obligations.
- KEYEDSTORAGETRANSFER permits a one-sided comparison with delta. If S=E,
  then Eshift=S+B gives delta=B in that direction. Candidate/parameter/domain
  digests must identify the same selected expressions; matching strings
  do not prove the two Alignment fields.

The existing `ActualStorage.lean` and `ActualShift.lean` historical success
receipts were checked in COMPILEDLEDGERBINDING. They cover the old source
snapshots only, not this companion. The exact W definition used here was
read from `examples/routeb_potential_slice/PotentialSlice.lean:54-61`.
No physical DH/Float64 binding was inferred from that encoded definition.

## Remaining minimum evidence and validation

Select the actual parameter/state map, identify Q and the same mass source,
and prove normalized-potential plus quadratic-compensation identities (or
directly R=W). For barrier use, bind the same initial set and path, prove
the source cap on Q, and adjust the target threshold by B where applicable.
These are unfilled contracts; no candidate or registry promotion occurred.

Only targeted source reads, static algebra/premise inspection and hashing
were performed. The 116-line companion has no proof-hole declarations and
no new compiler receipt. SHA-256:
`f8da2e44f9afc4c80fc14e81a1c59626d5af98071300a009aecd33463d3bef56`.
Final status: **OPEN_UNCOMPILED**.
