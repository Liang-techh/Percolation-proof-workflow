# B45-1 source comparator status

The candidate is `SourceBodyMassExtensionalProbe.lean`.  It contains the
exact-real layers for the Julia DH step, seven-slot frame prefix, COM, parent
axis, and the resulting function/all-body/summed `contractMass` extensional
bridges.  It does not introduce `Float64`, machine trigonometry, or a source
registry/state mutation.

Pinned environment observed before the attempt:

- Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Mathlib checkout `0df444a360eaa60ab8c11dca51a86af692955474`.
- Imported olean dependencies: `SourceContractAdapter`, `FrameSlotAccessor`,
  `BodyContractCore`, `BodySemanticCore`, `FramePrefixIndex`,
  `FrameOriginAxis`, `RealDHStep`, and `FourierNormalForm` from the existing
  pinned run directories.

Compilation evidence is intentionally incomplete.  An earlier attempt
reached Lean diagnostics for ambiguous `midpoint`/`IMat` names and was
corrected in the working candidate.  The corrected pinned attempt was then
stopped after approximately 30 seconds at the user's instruction not to
continue a heavy compilation.  Its temporary compile log was empty and no
`SourceBodyMassExtensionalProbe.olean` was produced.  Therefore this
candidate is **not** a compiled or comparator-accepted result.

Open boundary remains the Julia `Float64`/machine-trigonometry/rounding
binding; the current file only states the exact-real bridge.
