# Attempt history

## 2026-09-06 — contract-core repair loop

- `run-xONVNDOt`: failed after the first proof draft. Lean exposed four
  expression-layer issues: ambiguous `midpoint`, a function equality applied
  without `congrFun`, inactive `if` branches not reduced by the restricted
  simp set, and mass congruence attempted after the contract wrappers had
  already unfolded.
- `run-MfNlNlI1`: the first minimal repair fixed the Jacobian congruence shape
  but retained the midpoint/function and mass target issues; it was preserved
  as a failed receipt in the output directory.
- `run-Pg5mRDm0`: qualified the semantic-core midpoint, used `congrFun`, made
  both `if` branches explicit, and reduced the mass proof to one contract-layer
  `congrArg₂`; only the wrapper unfolding mismatch remained.
- `run-0FvNkLzz`: changed the mass goal explicitly to `linkMass` over
  `contractJv`/`contractJw`; compile and source-restriction checks passed.

No registry promotion is made by these attempts. The successful run is
recorded by the revision-72 checkpoint script.
