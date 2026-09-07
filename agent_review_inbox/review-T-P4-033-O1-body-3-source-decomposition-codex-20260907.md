# O1 body-3 source decomposition review

Status: OPEN / targets only / not Lean-compiled

Scope is restricted to human body-3, CSV body `3`, zero-based Lean body `2`. No body-4 or body-5 source was changed. The same source and state binding is retained:

- `source_key = routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)`
- `state_key = routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity`

## Concrete typed targets

`RouteBO1PerBodyTraceAdapter.lean` now exposes the following body-3-only targets:

1. `h_body_3_prefix_slots_target`: slots 0 and 1 are
   `(0,0,0)` and `(2/25*cos(q0), 2/25*sin(q0), 1/10)`; the exact differences are
   `slot2-slot1 = (21/100*sin(q1)*cos(q0), 21/100*sin(q1)*sin(q0), 21/100*cos(q1))`
   and `slot3-slot2 = ((-1/20)*sin(q0), (1/20)*cos(q0), 0)`.
2. `h_body_3_axes_target`: `z0=(0,0,1)` and `z1=z2=(-sin(q0),cos(q0),0)`.
3. `h_body_3_active_jacobian_target`: body-2 columns 0,1,2 are the active `bodyJv_active_formula`/`bodyJw_active_formula` instances; columns 3,4,5 are zero via the inactive lemmas.
4. `body_3_translational_gram`, `body_3_angular_gram`, and `body_3_unexpanded_gram`, with the bridge target `h_body_3_bodyMass_to_unexpanded_gram_target`.
5. `h_body_3_unexpanded_gram_to_piecewise_target`, whose RHS is the existing exact body-3 piecewise expression.
6. `h_body_3_minimal_trig_target`, requiring only `sin²+cos²=1` and `cos(2*x)=2*cos²(x)-1` as real-lift normalization seams.

## Minimal proof decomposition

The next Lean agent should prove the targets in this order:

1. Expand `routeBFrameSlot` only for slots 0..3, using `routeB_source_origin_slot` and `routeB_source_axis_slot`, then finite-case the real DH entries. The `q0` terms must remain exact real `Real.sin`/`Real.cos` terms until the Gram step.
2. Instantiate `bodyJv_active_formula` and `bodyJw_active_formula` for joints 0,1,2, and `bodyJv_zero_of_inactive`/`bodyJw_zero_of_inactive` for joints 3,4,5. This is a support/entry proof, not a source-to-trace proof.
3. Rewrite `sourceBodyMass_eq_bodyMass`, `bodyMass_is_linkMass`, and the definitions of the two Gram sums to obtain `h_body_3_bodyMass_to_unexpanded_gram_target`; do not identify this rewrite with the piecewise Fourier equality.
4. Reduce the active cross products and finite sums. Use `routeBMass 2 = 3/5`, diagonal `routeBInertia 2` with scalar `7/60`, `Real.sin_sq_add_cos_sq`, and `Real.cos_two_mul`; finish rational normalization with `ring_nf`/controlled `ring` after all finite indices are split.
5. Stop at this source-side child. Its completion would still be only the exact body-3 source reduction; it does not prove the separate source-to-trace bridge.

## Exact obstruction

No premise in the current state supplies any of the above pointwise source expansions as a proof. The existing `routeB_source_origin_slot`/`routeB_source_axis_slot` are only the slot bridge; the DH matrix-entry expansion, active cross-product reduction, Gram-to-piecewise identity, and trace fold remain separate obligations. Therefore this review does not provide `h_body_3`, `h_body_3_source_entry_target`, or a verified source bridge.

Hashes are recorded in `O1_BODY_3_SOURCE_DECOMPOSITION_RECEIPT.json`; the adapter hash after this target-only edit is `6B50AE63C9770E3481F79511141C8CC55D592B5C550F686654C5E756584399EF`. No Lean/Lake command was run.
