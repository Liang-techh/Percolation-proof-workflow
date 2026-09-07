# BODY6 compiled-ledger binding review

Status: `OPEN_UNCOMPILED`; adapter over previously compiled storage leaves.

The sidecar introduces typed `StorageData`, `InitialLedgerBinding`, and
`PathLedgerBinding` records. It consumes the existing `ActualStorage`
theorem only with its full premises: nonnegative coefficients, the full
initial ball, the signed-gap bound, ramp bound, and beta inequalities. It then
transfers that bound to a ledger function only after pointwise equality at the
initial set. For a future barrier it separately requires identity on every
time-domain slice, path inclusion, a source tube bound, and tube `< 1`.

This makes the current gap explicit: the scalar
`492033745203/25600000000000` is not itself a bound for an arbitrary ledger or
for `Vfull_DH`. The imported `ActualShift` comparison is also kept honest: it
applies to `E + 4079979/400000` under a mass premise, not automatically to the
active `V≤1` candidate. The exact sidecar records that the shift baseline alone
already exceeds the `p45≤45` threshold under its coarse coefficient.

`component_cap_does_not_imply_storage_cap_attempt` prevents confusing a
component/domain cap with the stronger storage cap needed for the energy
barrier. No ODE existence, source/Float64 identity, coverage, flowpipe,
residual absorption, terminal transfer, pinned compilation, or registry
promotion is claimed.
