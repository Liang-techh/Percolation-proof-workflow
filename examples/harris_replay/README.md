# Harris replay benchmark

Stage acceptance target: the one-dimensional Harris integral inequality from the percolation
development. This benchmark reconstructs a proof in a separate namespace using only
`Mathlib.MeasureTheory.Integral.Prod` and `Mathlib.Tactic`, plus its own child modules.
Do not import existing Percolation modules or reference the original theorem.

Child A proves nonnegativity of the product of monotone differences and its iterated integral.
Child B expands the inner integral assuming three integrability hypotheses.
The parent must derive integrability from bounded measurable inputs and perform the outer expansion.
Success here is a staged test, not completion of the full research workflow.
