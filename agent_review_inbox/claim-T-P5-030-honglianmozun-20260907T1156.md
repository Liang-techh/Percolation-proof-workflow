---
kind: task_claim
task_id: T-P5-030
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T11:56:00-06:00
integration_status: pending
continuation_of:
  - T-P5-017
  - T-P5-019
---

# Claim — T-P5-030

Scope: derive a source-independent energy/sensitivity theorem for two affine-ramp trajectories with different constant ramp rates `c1,c2`, using the exact moving frame from T-P5-017. The target is a parameter-cell contraction/diameter bound: after subtracting each trajectory's own affine particular solution, the ideal block is independent of `c`, so the parameter mismatch should enter only through relative initial data and any true residual difference.

The deliverable will isolate (i) the exact difference equation, (ii) the initial mismatch energy proportional to `(c1-c2)^2`, (iii) a residual-difference ISS estimate using the T-P5-019 direct metric, and (iv) transport back to physical `q,v` coordinates. This is intended as an energy-side bridge for parameter-cell/flowpipe consumers, not as a source coefficient extraction task.

Boundary: do not touch the active T-P5-027 source residual decomposition, T-P5-028 body6 C-FD envelope, T-P4-027 normalization, T-P2-016 spectral split, or T-P5-029 SPN gain-increment slack. No Julia/Float64 semantics, ODE existence, coverage, provenance/admission, registry promotion, or parent closure is claimed.