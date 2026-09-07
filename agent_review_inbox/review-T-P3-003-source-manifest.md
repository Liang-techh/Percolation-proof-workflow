---
kind: review_result
task_id: T-P3-003
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-P3-003 canonical source-manifest binding audit

## Scope

Read-only audit only. I checked the authoritative Julia/DH source, the current
delivery-side exact snapshot, the source-manifest file, the coordinate-order
contract, and the arithmetic/finite-difference convention. I did not run a full
interval search, did not modify any state/registry, and did not touch any
external source.

## Exact inspected paths and hashes

Source and manifest evidence:

- `examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`
  - SHA-256: `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`
- `examples/routeb_source_binding_audit/SHA256SUMS.csv`
  - SHA-256: `4a4ffd1abfab53fb30cde9a40f1449b2db3f117b15425e16397bc93a86b7a631`
- `examples/routeb_source_binding_audit/snapshots/current_exact/reference.json`
  - SHA-256: `26ca4f2d80e1237e3d3e87a6a9f11c62abe9304cfe006409ef225a682dff5dc9`

The manifest itself lists the same authoritative source hash for
`snapshots/original_target/dhport_lib.jl`, and the same exact mass/potential
CSV hashes as the current exact snapshot:

- `snapshots/original_target/routeB_fourier_mass_full_rational.csv`
  - SHA-256: `a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8`
- `snapshots/original_target/routeB_fourier_potential_rational.csv`
  - SHA-256: `4ebbb10e32639f54b18f259cbb762c04f2be842a856cae85e1fe94dad5478b6c`
- `snapshots/original_target/routeB_fourier_rational_probe.py`
  - SHA-256: `9460181770e47be0ecbde43a8a29ef285da1168c3121fab18d5378c671401a7b`

## Binding facts

The authoritative Julia/DH source is the include-only `dhport_lib.jl` in the
original-target snapshot. Its relevant contract is explicit and stable:

- `MASS_REGULARIZER = 1e-6`
- `CG_FINITE_DIFF_STEP = 1e-5`
- `DYNAMICS_SEMANTICS = "DH-chain M with explicit mass regularizer; C/G central finite differences"`
- `fk_frames(q)` uses the 6-link DH chain with `q[1]..q[6]` in Julia's
  1-based order.
- `mass_matrix(q; regularization = MASS_REGULARIZER)` accumulates the linkwise
  translational and rotational terms and adds `Float64(regularization) * I_6`.
- `arm_MCG(q, dq; mass_regularization = MASS_REGULARIZER, fd_step = CG_FINITE_DIFF_STEP)`
  computes `C dq` and `G` by centered finite differences with the same
  regularizer.

The current delivery-side exact snapshot is a derived exact-coupled reference,
not a new Julia execution trace. `reference.json` explicitly says:

- `arithmetic = "fractions.Fraction"`
- `Lean_compiled = false`
- `physical_DH_identification_proved = false`
- `Float64_binding_proved = false`
- `mu = "1/1000000"`
- `state_order` is the full 14-state sequence `q1..q6, v1..v6, w, c`

That gives a consistent provenance bundle, but it is still documentary. It does
not prove the deployed Julia/DH semantics were re-executed from the manifest,
and it does not give an admissible source-binding receipt on its own.

## Coordinate order and arithmetic convention

The coordinate order is fixed and consistent across the binding checker and the
snapshot reference:

- `q1..q6, v1..v6, w, c`

The arithmetic convention is also fixed:

- exact snapshot arithmetic is `fractions.Fraction`
- the Julia source uses `Float64`
- the mass regularizer is exactly `1e-6`
- the finite-difference step is exactly `1e-5`

This is the smallest admissible contract I can defend from the available
artifacts:

1. the manifest and receipt must agree on `state_order = q1..q6,v1..v6,w,c`;
2. `domain`, `normalization`, `fd`, and `float64_marker` must match exactly;
3. every listed source path must be relative, inside the declared `source_root`,
   and hash to the declared lowercase SHA-256;
4. the declared Julia/DH source root must be the original-target snapshot that
   contains `dhport_lib.jl` and the paired CSV/probe sources;
5. the receipt must remain evidence-only, with no registry promotion or
   interval-search inference.

## Blocker

The blocker is that the current artifact set stops at provenance and exact
snapshot agreement. It does not include a standalone, machine-checkable receipt
that binds the authoritative Julia source root to a separately executed delivery
source root under the same manifest contract.

So the binding is still pending in the strict sense requested by the task:
the hashes line up, the coordinate order and arithmetic conventions are explicit,
but I cannot upgrade that to a verified canonical source-manifest binding without
a dedicated receipt from the executable delivery path.

## Conclusion

`integration_status` remains `pending`.

The smallest admissible next step is to keep the manifest fixed, keep the
`q1..q6,v1..v6,w,c` order fixed, and require a separate delivery receipt that
replays the authoritative `dhport_lib.jl` source root under the same hash
contract. I did not perform that replay here.
