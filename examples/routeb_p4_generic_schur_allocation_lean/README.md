# P4 Generic Schur Allocation Lean sidecar

Agent: 苏梦辰

Task: `GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION`

This standalone sidecar formalizes the source-independent finite-dimensional Euclidean Schur/Young allocation seam extracted from `NEW_P4_032_GenericSchurAllocation20260908.lean`.

It proves only exact real/vector algebra:

- nonnegativity and expansion of the Euclidean square on `Fin n → ℝ`;
- exact completed-square identity for `ell + r`;
- the generic port-budget consumer for any finite dimension;
- exact-total residual dominance over the single relaxed Schur charge;
- the no-double-charge corollary;
- an exact zero-radius/nonzero-port regression.

It intentionally does **not** prove or silently identify:

- dense `M0_CC⁻¹` metric transport with the Euclidean metric;
- deployed DH/source expressions for `ell` or `r`;
- source reification or same-domain coverage;
- Float64/FD/controller/solve behavior;
- ODE/flowpipe coverage;
- registry admission or final integration.

## Portable verification

The sidecar pins `leanprover/lean4:v4.32.0`, uses the repository `examples/local_fkg/lake-manifest.json`, resolves `lake` and `lean` from `PATH`, and can be run under the portable sidecar workflow with `CI_PORTABLE=1`:

```bash
bash examples/routeb_p4_generic_schur_allocation_lean/verify.sh
```

`verify.sh` uses `-DwarningAsError=true`, rejects `sorry`/`admit`, requires an axiom report for all eight exported theorems, and rejects `sorryAx`.

Status remains pending until a real focused Actions execution is available. Even after compile/axiom success, this sidecar is only a candidate for independent verification and final integration.

待封不觉独立验证 / 待梁智炜最终整合。
