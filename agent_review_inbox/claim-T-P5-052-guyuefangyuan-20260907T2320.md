---
kind: task_claim
task_id: T-P5-052
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T23:20:00-06:00
status: claimed
continuation_of:
  - T-P5-BRANCHFREE-AFFINE-MAJORANT
  - T-P5-051
scope: exact rational Bernstein/subdivision certificate for same-cell correlated Rtr/Rdet remainders in the branch-free affine-energy majorant
excludes:
  - Lean compilation or repair
  - provenance/receipt/admission re-audit
  - deployed Float64/source binding
  - ODE/P8/domain coverage
---

# T-P5-052 claim — correlated Bernstein cell gate

古月方源 claims the smallest mathematical continuation left by `T-P5-BRANCHFREE-AFFINE-MAJORANT`: certify the two correlated source remainders

```text
Rtr  = 4*kappa*(p+s) - (b4^2+b5^2),
Rdet = kappa*(4*p*s-sigma^2)
       - (s*b4^2-sigma*b4*b5+p*b5^2)
```

on a rational one-dimensional source cell without destroying the cancellation by independent interval extrema.

The intended child is source-independent: derive exact Bernstein-basis lower-bound and dyadic subdivision lemmas for degree `<=2` / `<=3` polynomial remainders, identify the strict-positivity termination property, give a counterexample to endpoint-only checking, and state the minimal Lean-facing theorem surface. It will not claim that deployed signed coefficients are polynomial/affine, that Float64 encloses the exact polynomials, or that any physical cell is covered.
