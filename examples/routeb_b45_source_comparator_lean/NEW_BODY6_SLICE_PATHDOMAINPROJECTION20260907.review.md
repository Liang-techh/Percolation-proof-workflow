# Full-state path to source configuration domain

Status: **OPEN_UNCOMPILED**. This independent 91-line leaf imports Mathlib
only. It does not repeat or import the Alignment proof. No Lean/Lake,
broad regression, registry or state update was performed.

## Typed implication

X is the full-state type, C is the configuration type, and
`project : X -> C` is the explicitly supplied coordinate map. The caller
must use the actual q projection, including the correct state order,
units and any lift/state transformation. No projection is guessed from a
dimension or a digest.

The two independent premises are

```text
DomainProjection project D Q:
  forall t in [0,1], forall x in D(t), project(x) in Q

WholePathMembership D path:
  forall t in [0,1], path(t) in D(t).
```

`project_whole_path_attempt` composes them to give
`project(path(t)) in Q` throughout the unit horizon. D(t) may contain q,v,
disturbance, clock and circle coordinates. The projection forgets those
coordinates only after the full-state membership and domain implication
have been supplied. Extra physical/lift constraints are not proved here.

For the ACTUALSTORAGEALIGN consumer, C can be `Fin 6 -> Real`. Its
configuration identity applies at q(t)=project(path(t)) once the other
state inputs, including v(t), match the full-state path. A different
velocity or state map cannot be substituted without a new binding.

## Initial membership is weaker

`InitialMembership D path` asserts only path(0) in D(0).
`whole_path_has_initial_attempt` obtains it from whole-path membership;
`project_initial_only_attempt` obtains only the projected initial point.
Neither lemma upgrades initial membership to a whole-path statement.

The exact counterexample takes D(t)=(-infinity,0] and path(t)=t. Its initial
point lies in D(0), but path(1)=1 lies outside D(1). The path is smooth;
no lack of regularity is responsible for the failed implication. This is
a logical example, not a claim about a DH trajectory or source ODE.

In particular, defining D(t) using a desired energy barrier and then
assuming WholePathMembership to derive that same barrier is not a
first-exit proof. Membership/continuation must be established independently
or handled by a valid stopping-time/first-exit argument with the right
interval. This sidecar supplies neither.

## Shift counted once

`ShiftIdentityOnQ` is an explicit *input* saying, at admissible configurations,
`G(t,x)=F(t,x)+B`. The separate alignment lane must supply it for the selected
source expressions. This file does not establish Alignment, physical-source
semantics or the shifted identity merely from the name of a storage.

Two consumers keep the bound's meaning distinct:

1. `projected_shift_cap_transfer_attempt` takes an unshifted cap F<=cap and
   requires cap+B<=bar. It returns G<=bar along the admitted path.
2. `already_shifted_cap_transfer_attempt` takes F+B<=cap and returns G<=cap
   with no further B. This includes an already shifted initial/tube budget.

Both consumers explicitly use the full-state path-to-Q implication before
applying the storage identity. Neither manufactures an integrated cap from
initial scalar data.

For the recorded B=4079979/400000, take F=0,G=B and cap=B. The correct
already-shifted bound holds, while the twice-charged inequality 2B<=B is
false. Double counting is an unnecessary stronger restriction that can
cause false rejection; it is not a means of making an unsound acceptance.
Conversely F<=1 holds and G<=1 fails, so dropping the shift at the unchanged
threshold can cause a false transfer. The exact scalar conjunction is
encoded in `shift_accounting_counterexample_attempt`.

## Required evidence and limits

Before instantiation, provide the same full-state path, projection, D(t), Q,
whole-path membership, and the domain projection theorem. Bind the selected
storage expressions and B to the same source/state map, and provide the
appropriately normalized source cap. Candidate/domain/parameter digests
remain provenance labels; they do not prove these predicates.

The file asserts no actual instance of those inputs, no ODE, v=q', ramp
reconstruction, circle invariance, path existence or continuation. The old
compiled storage receipts do not constitute compilation of this independent
sidecar. Static definition/premise review and file hashing were the only
checks. Lean receipt and axiom/dependency review remain pending.

SHA-256: `c3d0432fb2b53815bb9e23271ecadfa871e5526a96b9bf7b533efe392d2aa6ac`.
Final status: **OPEN_UNCOMPILED**.
