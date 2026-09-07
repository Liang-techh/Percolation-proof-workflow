# Route-B P8 interval-local ramp sidecar

Task: `T-P8-009`  
Agent: `苏梦辰`

This sidecar refines the existing P8 ramp reconstruction theorem so that it no
longer assumes derivatives on all of `ℝ`.  The theorem only uses continuity on
`[0,1]` and one-sided/right derivative witnesses on `[0,1)`, which is sufficient
for the endpoint transfer at `t=1`.

Formalized statements:

- `ramp_c_constant_on_Icc`
- `ramp_w_eq_mul_on_Icc`
- `ramp_reconstruction_on_Icc`
- `state_tail_reconstruction_on_Icc`
- `state_terminal_one_interval`

The 14-state tail slots remain typed as `Fin 14`, with slot 12 for `w` and slot
13 for `c` in zero-based indexing.  This sidecar does **not** prove source
binding, ODE existence or uniqueness, interval enclosure, first-exit closure,
flowpipe coverage, or Route-B admission.

`verify.sh` is portable for the shared GitHub Actions harness: it resolves
`lake` from `PATH`, checks the pinned local-FKG toolchain, compiles with
`-DwarningAsError=true`, audits the printed theorem axioms for `sorryAx`, and
keeps all physical gates explicitly open.
