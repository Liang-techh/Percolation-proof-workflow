# Route-B P3 single-entry source/interval bridge

This sidecar implements the smallest concrete P3 contract:

`exact interval soundness + box input + authenticated Float64 trace`
`=> one M[i,j] Float64 result is in the interval`

The Lean theorem is conditional. `MExact` and `MFloat` are independent
parameters. The theorem does not assert, derive, or fake equality between the
canonical Julia `Float64` DH implementation and the exact-real DH model.

`Float64TraceReceipt` retains source hash, operation-trace hash, runtime,
finite-normal/no-overflow proof, and the interpreted result. The receipt's
interval-membership premise must be supplied by an external auditable checker;
ordinary printed numbers do not create it.

The regularizer is explicit as `1/1000000` metadata and is not hidden in a
payload. This focused sidecar does not prove the exact DH model, IEEE
operation trace, all 36 entries, global box coverage, or Route-B admission.

It uses the pinned `examples/local_fkg/lean-toolchain` (Lean 4.32.0) and the
local FKG dependency environment only for compilation.
