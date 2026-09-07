# Fresh statement/source comparator receipt: B45-5 force-scale seam

## Comparator identity

- Comparator: `routeb_b45_5_force_scale_source_contract_v1`
- Comparator implementation: `source_contract_comparator.py`
- Execution mode: read-only focused anchor comparator
- Result: `ANCHOR_PASS_DH_EXECUTION_BINDING_OPEN`
- This is not an upstream/global theorem comparator and emits no registry
  acceptance; it is the smallest source-binding receipt for this adapter seam.

## Fresh statement/source result

- Lean statement surface for `forceScaleKc_eq_rhoKc`: `PASS`
- `DescriptorTermsAdapter` source-premise surface: `PASS`
- lifted literal/inertia anchors: `PASS`
- source hash binding: `PASS`
- derived literal coefficients: `q5 -> 1/100`, `q4 -> 1/200`
- deployed `tau` formula anchor: `PASS` at `dhport_lib.jl:108`
- deployed `tau` equivalence: `NOT_CLAIMED / OPEN`

The comparator matched the following source anchors:

- lifted `routeB_fourier_lifted_descriptor_model.jl:153`: `Ival[4]=1/5`,
  `Ival[5]=1/10`;
- lifted `:162`: `Q(1,20) * q[5]`;
- lifted `:164`: `Q(1,20) * q[4]`;
- lifted `:165-166`: `Ival[4] * f4` and `Ival[5] * f5`;
- deployed `dhport_lib.jl:108`: `tau = -Kp .* q - (Kd + b_fr) .* dq + G0v +
  (gw_coef .* I_val) .* w`.

## Hash-bound inputs

| Input | SHA-256 |
|---|---|
| deployed `robot_final/dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |
| lifted `routeB_fourier_lifted_descriptor_model.jl` | `0fcf733144b3d7b1b08f328fe4ad24477057c56976f0ef53633c450d8fc4729d` |
| Lean `ResidualDecomposition.lean` | `3946389828b94aff3b258a4635b58a7ca1be6ff2ce4414e9bef9553e25653cc9` |
| Lean-side `DescriptorTermsAdapter.lean` | `1455d987f899102e68346a7d8d074b8aa472d721151b6992d373f005a955750a` |

## Source-binding boundary

The receipt establishes only that the pinned lifted source literals and force
scale factors match the stated adapter contract, and that the deployed source
has the recorded `tau` formula. It does not produce either of the two concrete
premises required by `DescriptorTermsAdapter`:

```text
sourceBlockForce = expectedSourceForce q v w t
sourceBlockForce = sourceDescriptorRhs t
```

Those premises require a concrete source runtime/state witness binding block
indices, controller/C/G terms, the regularized DH mass block split, and the
returned solve. No Float64-to-`ℝ`, finite-difference, matrix-solve, or DH
execution equivalence is claimed here.

Accordingly:

- `statement_comparator = PASS` for the focused surface check;
- `source_anchor_comparator = PASS`;
- `deployed_source_binding = OPEN`;
- `registry_promotion = false`;
- `deployed tau equivalence = NOT CLAIMED`.

