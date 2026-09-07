---
kind: review_result
task_id: T-P3-003
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-P3-003 canonical source-manifest binding audit

## Scope and conclusion

This is a read-only Route-B source-manifest audit. I checked the authoritative Julia/DH source snapshot, the delivery-side exact snapshot, the coordinate-order and arithmetic conventions visible in those files, and the manifest/hash material that binds them. I did not run any full interval search, and I did not modify any state, registry, or external source.

**Conclusion: `PENDING_BLOCKER`.** The workspace contains consistent frozen source and delivery artifacts, but it does not contain a stronger proof that the delivery manifest is semantically bound to the authoritative Julia/DH source beyond exact-file hashing and literal snapshot equality. The existing checker is intentionally fail-closed and only validates declared hashes and metadata; the Lean artifacts here are literal reconstructions, not an admitted source-binding theorem.

## Exact paths and hashes

Authoritative Julia/DH source:

- `examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`
  - SHA-256: `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`

Delivery-side source and manifest evidence:

- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_export_traj.jl`
  - SHA-256: `35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf`
- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_fourier_mass_full_rational.csv`
  - SHA-256: `a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8`
- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_fourier_potential_rational.csv`
  - SHA-256: `4ebbb10e32639f54b18f259cbb762c04f2be842a856cae85e1fe94dad5478b6c`
- `examples/routeb_source_binding_audit/snapshots/current_exact/reference.json`
  - SHA-256: `26ca4f2d80e1237e3d3e87a6a9f11c62abe9304cfe006409ef225a682dff5dc9`
- `examples/routeb_source_binding_audit/snapshots/current_exact/ReferenceMass.lean`
  - SHA-256: `b77e00ab3cf236edc143fa963aba362a8279f2ca6caecaf5277726fac0c91607`
- `examples/routeb_source_binding_audit/snapshots/current_exact/PotentialSlice.lean`
  - SHA-256: `25e9ebe489b4f819f56e7334693d1d808e6ebd234139f659b14eb67125b846e7`
- `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean`
  - SHA-256: `7546f38946f67bb3dfe6cca27c97b007c5320a9fbf4059d58742005f4f707c7c`
- `examples/routeb_source_binding_audit/SHA256SUMS.csv`
  - SHA-256: `28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40`

## Coordinate order and arithmetic convention

The binding checker in `scripts/routeb_source_binding_manifest.py` fixes the exact 14-state order as
`q1, q2, q3, q4, q5, q6, v1, v2, v3, v4, v5, v6, w, c`.

The authoritative Julia source declares the arithmetic conventions directly in `dhport_lib.jl`:

- `MASS_REGULARIZER = 1e-6`
- `CG_FINITE_DIFF_STEP = 1e-5`
- `DYNAMICS_SEMANTICS = "DH-chain M with explicit mass regularizer; C/G central finite differences"`

Within `mass_matrix`, the COM point is `0.5 .* (o[:, ii] + o[:, ii+1])`, the rotational inertia term is `(I_val[ii] / 3) .* I_3`, and the mass matrix returns `M + Float64(regularization) .* I_6`.

Within `arm_MCG`, the Coriolis/centrifugal term uses central differences with `h = Float64(fd_step)` and the Christoffel-like contraction is
`0.5 * (dM[ii, jj, kk] + dM[ii, kk, jj] - dM[jj, kk, ii])`.

The current exact Lean snapshots preserve the same literal coordinate interpretation:

- `ReferenceMass.lean` states `Fin` indices `0,...,5` correspond to physical axes `1,...,6`.
- `PotentialSlice.lean` says the 17 CSV rows are kept “in their original order” and explicitly says no physical-DH identification is asserted.
- `ChristoffelPower.lean` fixes the tensor index order as `T k i j`.

## Smallest admissible source-binding contract

The smallest contract I can justify from the current workspace is:

1. a manifest and receipt that are both JSON objects;
2. an exact `state_order` of `q1..q6, v1..v6, w, c`;
3. equal `domain`, `normalization`, `fd`, and literal `float64_marker: true` in both manifest and receipt;
4. a shared `sources` array whose entries are relative paths with lowercase SHA-256 values;
5. all source files resolved under the declared `--source-root`, with hash equality checked file-by-file;
6. no inference of global correctness, interval bounds, or theorem admission from those hashes alone.

This is exactly the contract implemented by `scripts/routeb_source_binding_manifest.py`; it is a consistency check, not a semantic admission proof.

## Blocker

The blocker is not a hash mismatch. The blocker is that the current exact snapshot provides only frozen literal reconstructions (`ReferenceMass.lean`, `PotentialSlice.lean`, `ChristoffelPower.lean`) and a fail-closed manifest checker. What is still missing is an explicit theorem or equivalent proof object that binds the delivery manifest to the authoritative Julia/DH semantics, including coordinate order and arithmetic convention, without relying on a full interval search.

In practical terms: the source files are identifiable and hashed, but the repository does not yet expose an admissible proof that the delivery manifest is the semantic image of the authoritative Julia/DH source rather than just a hash-consistent snapshot.
