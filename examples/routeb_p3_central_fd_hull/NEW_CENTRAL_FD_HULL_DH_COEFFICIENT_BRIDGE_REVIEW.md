# P3 DH coefficient identity to C2/C3 Taylor bridge

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt candidate.

## Separation and bridge

`TaylorRemainderSide` holds the C2/C3-style regularity, same-box derivative
hulls, offset radius, remainder bound, rounding endpoints, and per-box gap/cap
chain. `DHCoefficientIdentitySide` separately holds the DH coefficient
functions `M`, `C`, `G` and the identity `M = C + G` on its domain.

`DHToTaylorBridge` requires explicit domain binding, DH-domain binding, and
same-box function binding. `dh_taylor_to_per_box_gap` consumes these bindings
plus the Taylor/rounding/gap premises and exports the per-box gap lower bound
and the DH identity at the same point.

## Obstructions

`arbitrary_function_identity_obstruction` shows that an arbitrary function is
not automatically a DH coefficient identity. `wrong_domain_binding_obstruction`
shows that an identity proved only on a restricted domain leaves an omitted
point unbound. Regularity, endpoint soundness, coverage, and all physical
interpretations remain external premises. No local Lean/Lake command or broad
regression was run.

No concrete DH implementation, source or numerical payload, continuous-domain
upgrade, admission, registry promotion, or Lean compilation claim is made.
