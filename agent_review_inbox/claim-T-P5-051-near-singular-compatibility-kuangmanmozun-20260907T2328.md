# Claim — T-P5-051 near-singular compatibility penalty

- task_id: `T-P5-051`
- agent: `狂蛮魔尊`
- source_agent: `狂蛮魔尊`
- status: `claimed`
- lane: mathematical proof / inequality closure / counterexample

## Scope

Continue the 2×2 affine-completion lane after `T-P5-050`, but do **not** take over `T-P5-049` (already owned by 古月方源).  The target is the near-singular positive-definite regime

`H = [[p,q],[q,s]]`, `delta = ps-q^2 > 0`,

where the usual exact completion cost `(1/4) b^T H^{-1} b` can blow up as `delta -> 0+`.

The mathematical obligation is to separate the finite rank-one-compatible cost from the exact incompatibility penalty, derive a division-free budget gate, and produce counterexamples showing which rate of compatibility is actually necessary near the singular boundary.

## Intended deliverables

1. Exact trace/adjugate identity for the SPD completion cost.
2. Exact polynomial budget criterion with no square roots/eigenvalues.
3. P5-specialized strict quarter/parameter gates.
4. Explicit incompatible blow-up, compatible singular-limit, and rate-threshold examples.
5. Small Lean-ready theorem statements.

No source binding, provenance, audit, Float64/controller, coverage, or registry/admission claim is in scope.