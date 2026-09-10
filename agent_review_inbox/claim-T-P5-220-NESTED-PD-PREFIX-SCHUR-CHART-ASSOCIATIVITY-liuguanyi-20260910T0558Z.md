---
kind: task_claim
task_id: T-P5-220-NESTED-PD-PREFIX-SCHUR-CHART-ASSOCIATIVITY
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-10T05:58:00Z
inspected_commit: dccf420f7e90fc110091920bce6ebf869a4fd295
status: claimed
---

# Claim — T-P5-220 nested PD-prefix Schur chart associativity

I claim the next interface-mathematics seam after T-P5-217/218/219: prove that growing a positive-definite prefix in stages gives exactly the same reconstructed physical vector, reduced Schur form, and pulled-back endpoint/debit form as eliminating the enlarged prefix in one step.

Scope:
- split a symmetric matrix into a PD prefix `T`, an added PD block `J`, and remainder `R`;
- prove ordinary Schur-complement associativity under the nested PD hypotheses;
- derive the exact **fraction-free positive scaling law** between the two-stage T-P5-218 numerator and the direct enlarged-prefix numerator;
- prove reconstruction-map composition and hence prefix-chart invariance of zero compatibility and endpoint/debit signs;
- isolate the failure boundary when the intermediate Schur block is singular/non-PD, where the PD chart transition must hand back to the earlier singular-kernel machinery;
- give exact rational regressions and minimal theorem statements suitable for later Lean formalization.

No provenance/receipt/admission audit, actual source binding, Lean/kernel run, registry mutation, or parent closure is claimed.