# Route-B P8 first-exit/domain bridge

This directory contains a minimal conditional Lean decomposition. It does not
claim the Route-B trajectory remains in its source domain, exists through
`T = 1`, or is covered by the current reachability probe.

`FirstExitBridge.lean` separates:

1. `LocalCertificate`: a bound usable only when the state is in the declared
   source domain;
2. `FirstExitAttainment`: continuity/compactness data producing an attained
   first boundary hit from a hypothetical domain failure;
3. `PrefixLimitMargin` and `BoundarySeparated`: the non-circular estimate at
   that hit and the strict contradiction;
4. `ContinuationCriterion`: the independent ODE extension premise needed to
   conclude that the maximal solution exists through the target horizon.

The assembly theorem merely composes these interfaces. In particular, it does
not infer first-exit attainment from a total Lean function, and it does not
infer continuation from domain membership alone.

The current P8 local probe has horizon `0.001`, initial and disturbance radii
`0.001`, reports 35 reachsets, and retains `coverage_complete=false`. The
`coverageFalse_probe_cannot_discharge` theorem encodes the corresponding
fail-closed gate: such a receipt cannot be admitted as a proof of any closure
claim.

Strict compile command:

```powershell
lake update
lake env lean -DwarningAsError=true .\FirstExitBridge.lean
```

Still open for a concrete Route-B instantiation:

- the exact 12-state initial inclusion and ramp-input lift for `T = 1`;
- a continuous/maximal solution for the source-bound exact-real dynamics;
- first-exit attainment for every source-domain face used by local bounds;
- same-prefix strict margins for all joint, remote-state, inverse, and
  implementation-semantics side conditions;
- a local-Lipschitz/compact-containment continuation theorem;
- a complete flowpipe/partition receipt and terminal transfer.

No existing file, state, registry, canonical source, solver output, or probe was
modified or regenerated.
