---
kind: claim
task_id: T-P5-035
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T17:20:00-06:00
inspected_commit: 205fb1a54112cbbf19424a3a61500780b2ba0159
status: active
---

# T-P5-035 claim — joint dissipation/residual-metric barrier

I claim a new source-independent mathematical child under the block-(4,5) P5 hypocoercive route.

Scope: replace the currently separated use of `Q >= k V` and `||x+y||^2 <= C Q` by one joint quadratic lower bound of the form

```text
Q >= a V + b ||x+y||^2,
```

with exact rational `a,b>0`, then derive the corresponding additive-residual ISS/barrier and incremental `mu,nu` gates.  The aim is a real mathematical improvement in the residual bottleneck, not another provenance/audit pass.

Boundaries: no source/Float64/solve binding, no P8 coverage, no ODE continuation, no registry/admission mutation, and no takeover of any existing Lean/source claim.  Any theorem remains pending until independent validation/integration.
